"""VODA: same-origin FastAPI + SQLite. Run with python run.py."""
from contextlib import contextmanager
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib, hmac, io, json, os, secrets, sqlite3, time, warnings
from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException, Request, Response, UploadFile, File, Query
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get('VODA_DATA_DIR', str(ROOT / 'data'))).resolve()
DATA.mkdir(parents=True, exist_ok=True)
DB = DATA / 'voda.sqlite3'
SECURE_COOKIE = os.environ.get('VODA_HTTPS', '0') == '1'
KINDS = Literal['board', 'projects', 'activities']
MAX_PHOTO = 10 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 40_000_000

@contextmanager
def db():
    c = sqlite3.connect(DB, timeout=15)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    try:
        with c:
            yield c
    finally:
        c.close()

with db() as c:
    c.execute('PRAGMA journal_mode=WAL')
    c.executescript('''
    CREATE TABLE IF NOT EXISTS admins (username TEXT PRIMARY KEY, salt TEXT NOT NULL, password TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, username TEXT NOT NULL, expires REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS attempts (address TEXT PRIMARY KEY, count INTEGER NOT NULL, started REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS items (id TEXT PRIMARY KEY, kind TEXT NOT NULL, data TEXT NOT NULL, created INTEGER NOT NULL);
    CREATE INDEX IF NOT EXISTS items_kind_created ON items(kind, created DESC);
    CREATE TABLE IF NOT EXISTS photos (id TEXT PRIMARY KEY, name TEXT NOT NULL, data BLOB NOT NULL, created REAL NOT NULL);
    ''')

def password_hash(password, salt):
    return hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()

def set_admin(username, password):
    if not username.strip() or len(username) > 80 or len(password) < 12 or len(password) > 256:
        raise ValueError('관리자 이름은 1~80자, 비밀번호는 12~256자로 입력하세요.')
    salt = secrets.token_hex(16)
    hashed = password_hash(password, salt)
    with db() as c:
        c.execute('INSERT OR REPLACE INTO admins VALUES(?,?,?)', (username.strip(), salt, hashed))
        c.execute('DELETE FROM sessions WHERE username=?', (username.strip(),))

app = FastAPI(title='VODA API', version='1.0.0')

@app.middleware('http')
async def security(request: Request, call_next):
    # A custom header plus same-origin policy prevents cross-site form/JS writes.
    if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
        if request.headers.get('x-voda-request') != '1':
            return Response('Same-origin API request required', status_code=403)
        origin = request.headers.get('origin')
        if origin and origin != str(request.base_url).rstrip('/'):
            return Response('Origin not allowed', status_code=403)
        try:
            size = int(request.headers.get('content-length', '0'))
        except ValueError:
            return Response(status_code=400)
        if size > MAX_PHOTO + 65536:
            return Response(status_code=413)
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store'
    return response

def admin(request: Request):
    token = request.cookies.get('voda_session', '')
    digest = hashlib.sha256(token.encode()).hexdigest()
    with db() as c:
        row = c.execute('SELECT username FROM sessions WHERE token=? AND expires>?', (digest, time.time())).fetchone()
    if not row:
        raise HTTPException(401, '관리자 로그인이 필요합니다.')
    return row['username']

class Login(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=256)

@app.post('/api/auth/login')
def login(body: Login, request: Request, response: Response):
    address = request.client.host if request.client else 'local'
    now = time.time()
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        c.execute('DELETE FROM attempts WHERE started<?', (now - 900,))
        row = c.execute('SELECT * FROM attempts WHERE address=?', (address,)).fetchone()
        if row and row['count'] >= 10:
            raise HTTPException(429, '로그인 시도가 많습니다. 15분 후 다시 시도하세요.')
        c.execute('INSERT INTO attempts VALUES(?,1,?) ON CONFLICT(address) DO UPDATE SET count=count+1', (address, now))
        user = c.execute('SELECT * FROM admins WHERE username=?', (body.username,)).fetchone()
    salt = user['salt'] if user else '00' * 16
    result = password_hash(body.password, salt)
    if not user or not hmac.compare_digest(user['password'], result):
        raise HTTPException(401, '아이디 또는 비밀번호를 확인해주세요.')
    token = secrets.token_urlsafe(32)
    with db() as c:
        c.execute('DELETE FROM attempts WHERE address=?', (address,))
        c.execute('DELETE FROM sessions WHERE expires<?', (now,))
        c.execute('INSERT INTO sessions VALUES(?,?,?)', (hashlib.sha256(token.encode()).hexdigest(), body.username, now + 43200))
    response.set_cookie('voda_session', token, max_age=43200, httponly=True, secure=SECURE_COOKIE, samesite='strict', path='/')
    return {'username': body.username}

@app.get('/api/auth/me')
def me(username=Depends(admin)):
    return {'username': username}

@app.post('/api/auth/logout')
def logout(request: Request, response: Response):
    with db() as c:
        c.execute('DELETE FROM sessions WHERE token=?', (hashlib.sha256(request.cookies.get('voda_session', '').encode()).hexdigest(),))
    response.delete_cookie('voda_session', path='/')
    return {'ok': True}

class PhotoRef(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(min_length=1, max_length=40)

class Content(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str = Field(min_length=1, max_length=120)
    content: str = Field(default='', max_length=50000)
    description: str = Field(default='', max_length=50000)
    category: Literal['notice', 'activity', 'recruit'] = 'notice'
    pinned: bool = False
    projectCategory: str = Field(default='', max_length=80)
    link: str = Field(default='', max_length=2000)
    photos: list[PhotoRef] = Field(default_factory=list, max_length=20)
    updatedAt: int | None = None

@app.get('/api/content/{kind}')
def list_items(kind: KINDS, category: str | None = None, q: str = Query(default='', max_length=120), limit: int | None = Query(default=None, ge=1, le=100), offset: int = Query(default=0, ge=0)):
    with db() as c:
        rows = c.execute('SELECT data FROM items WHERE kind=? ORDER BY created DESC,id DESC', (kind,)).fetchall()
    items = [json.loads(row['data']) for row in rows]
    items = [x for x in items if (not category or category == 'all' or x.get('category') == category) and q.casefold() in x['title'].casefold()]
    return items[offset:offset + limit if limit is not None else None]

@app.get('/api/content/{kind}/{item_id}')
def get_item(kind: KINDS, item_id: str):
    with db() as c:
        row = c.execute('SELECT data FROM items WHERE kind=? AND id=?', (kind, item_id)).fetchone()
    if not row:
        raise HTTPException(404, '게시물을 찾을 수 없습니다.')
    return json.loads(row['data'])

def save(kind, body, item_id=None):
    title = body.title.strip()
    text = (body.content if kind == 'board' else body.description).strip()
    if not title or not text:
        raise HTTPException(422, '제목과 내용을 입력해주세요.')
    if kind == 'projects' and body.link:
        url = urlsplit(body.link)
        if url.scheme not in ('https', 'http') or not url.hostname or url.username or url.password:
            raise HTTPException(422, '프로젝트 링크는 올바른 http 또는 https 주소여야 합니다.')
    if (kind == 'board' and body.photos) or (kind == 'projects' and len(body.photos) > 1):
        raise HTTPException(422, '게시판은 사진 0장, 프로젝트는 대표 사진 1장까지 가능합니다.')
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        existing = None
        if item_id:
            row = c.execute('SELECT data FROM items WHERE id=? AND kind=?', (item_id, kind)).fetchone()
            if not row:
                raise HTTPException(404, '게시물을 찾을 수 없습니다.')
            existing = json.loads(row['data'])
            if body.updatedAt != existing['updatedAt']:
                raise HTTPException(409, '다른 창에서 수정되었습니다. 입력 내용을 따로 복사한 뒤 새로고침해주세요.')
        photos = []
        seen = set()
        for ref in body.photos:
            if ref.id in seen:
                raise HTTPException(422, '같은 사진을 중복으로 추가할 수 없습니다.')
            seen.add(ref.id)
            row = c.execute('SELECT name FROM photos WHERE id=?', (ref.id,)).fetchone()
            if not row:
                raise HTTPException(422, '사진이 없습니다. 다시 업로드해주세요.')
            photos.append({'id': ref.id, 'name': row['name'], 'url': '/media/' + ref.id})
        now = max(int(time.time() * 1000), existing['updatedAt'] + 1 if existing else 0)
        item = {'id': item_id or str(uuid4()), 'title': title, 'createdAt': existing['createdAt'] if existing else now, 'updatedAt': now}
        if kind == 'board':
            item.update(content=text, category=body.category, pinned=body.pinned, date=existing['date'] if existing else datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y.%m.%d'))
        else:
            item.update(description=text, photos=photos)
            if kind == 'projects':
                item.update(projectCategory=body.projectCategory.strip(), link=body.link.strip())
        c.execute('INSERT INTO items VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data', (item['id'], kind, json.dumps(item, ensure_ascii=False), item['createdAt']))
    return item

@app.post('/api/content/{kind}', status_code=201)
def create_item(kind: KINDS, body: Content, username=Depends(admin)):
    return save(kind, body)

@app.put('/api/content/{kind}/{item_id}')
def update_item(kind: KINDS, item_id: str, body: Content, username=Depends(admin)):
    return save(kind, body, item_id)

@app.delete('/api/content/{kind}/{item_id}')
def delete_item(kind: KINDS, item_id: str, updatedAt: int, username=Depends(admin)):
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        row = c.execute('SELECT data FROM items WHERE id=? AND kind=?', (item_id, kind)).fetchone()
        if not row:
            raise HTTPException(404, '게시물을 찾을 수 없습니다.')
        if json.loads(row['data'])['updatedAt'] != updatedAt:
            raise HTTPException(409, '다른 창에서 수정되었습니다. 새로고침 후 확인해주세요.')
        c.execute('DELETE FROM items WHERE id=? AND kind=?', (item_id, kind))
    return {'ok': True}

@app.post('/api/photos', status_code=201)
def upload_photo(file: UploadFile = File(...), username=Depends(admin)):
    raw = file.file.read(MAX_PHOTO + 1)
    if len(raw) > MAX_PHOTO:
        raise HTTPException(413, '사진 한 장은 10MB 이하여야 합니다.')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw)) as image:
                if image.format not in ('JPEG', 'PNG', 'WEBP'):
                    raise ValueError('Unsupported image')
                image.load()
                image = ImageOps.exif_transpose(image)
                image.thumbnail((2400, 2400))
                # Re-encode pixels only: strip EXIF/GPS and embedded payloads.
                clean = Image.new('RGBA', image.size)
                clean.paste(image.convert('RGBA'))
                output = io.BytesIO()
                clean.save(output, format='WEBP', quality=88)
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(422, '올바른 JPG·PNG·WebP 사진을 선택해주세요. 최대 4천만 화소입니다.')
    photo_id = str(uuid4())
    name = Path((file.filename or 'photo').replace('\\', '/')).name[:160]
    with db() as c:
        c.execute('INSERT INTO photos VALUES(?,?,?,?)', (photo_id, name, output.getvalue(), time.time()))
    return {'id': photo_id, 'name': name, 'url': '/media/' + photo_id}

@app.get('/media/{photo_id}')
def media(photo_id: str):
    with db() as c:
        row = c.execute('SELECT data FROM photos WHERE id=?', (photo_id,)).fetchone()
    if not row:
        raise HTTPException(404)
    return Response(row['data'], media_type='image/webp', headers={'Cache-Control': 'public, max-age=86400'})

@app.get('/api/health')
def health():
    return {'status': 'ok'}

# Serve explicit frontend files only. Never expose server code, DB, or .git.
app.mount('/images', StaticFiles(directory=ROOT / 'images'), name='images')
(ROOT / 'analysis').mkdir(exist_ok=True)
@app.get('/analysis/index.html')
def analysis_index(request: Request):
    return RedirectResponse('/analysis/' + ('?' + request.url.query if request.url.query else ''), status_code=308)

app.mount('/analysis', StaticFiles(directory=ROOT / 'analysis', html=True), name='analysis')
PUBLIC = {p.name for p in ROOT.iterdir() if p.suffix in ('.html', '.css', '.js')}
PAGES = {Path(name).stem: name for name in PUBLIC if name.endswith('.html')}
@app.get('/')
def index():
    return FileResponse(ROOT / 'index.html')
@app.get('/{filename}')
def frontend(filename: str, request: Request):
    if filename in PUBLIC and filename.endswith('.html'):
        target = '/' if filename == 'index.html' else '/' + Path(filename).stem
        return RedirectResponse(target + ('?' + request.url.query if request.url.query else ''), status_code=308)
    if filename in PAGES:
        return FileResponse(ROOT / PAGES[filename])
    if filename not in PUBLIC:
        raise HTTPException(404)
    return FileResponse(ROOT / filename)
