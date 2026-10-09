import os, tempfile, io
os.environ['VODA_DATA_DIR'] = tempfile.mkdtemp(prefix='voda-test-')
from fastapi.testclient import TestClient
from PIL import Image
from server import app, set_admin, db

PASSWORD = 'a-test-only-password-2026'
set_admin('tester', PASSWORD)
HEADERS = {'X-Voda-Request': '1'}

def authenticated():
    client = TestClient(app)
    result = client.post('/api/auth/login', json={'username': 'tester', 'password': PASSWORD}, headers=HEADERS)
    assert result.status_code == 200
    return client

def test_auth_csrf_and_private_files():
    visitor = TestClient(app)
    assert visitor.post('/api/content/board', json={'title': 'x', 'content': 'y'}, headers=HEADERS).status_code == 401
    client = authenticated()
    assert client.get('/api/auth/me').json()['username'] == 'tester'
    assert client.post('/api/content/board', json={'title': 'x', 'content': 'y'}).status_code == 403
    assert client.post('/api/content/board', json={'title': 'x', 'content': 'y'}, headers={**HEADERS, 'Origin': 'https://evil.example'}).status_code == 403
    for path in ['/server.py', '/data/voda.sqlite3', '/.git/config', '/requirements.txt']:
        assert visitor.get(path).status_code == 404
    assert client.post('/api/auth/logout', headers=HEADERS).status_code == 200
    assert client.get('/api/auth/me').status_code == 401

def test_board_shared_persistent_crud_conflict_search():
    client = authenticated()
    value = {'title': '통합 테스트 공지', 'content': '<script>alert(1)</script>\n본문', 'pinned': True, 'category': 'notice'}
    response = client.post('/api/content/board', json=value, headers=HEADERS)
    assert response.status_code == 201, response.text
    post = response.json()
    public = TestClient(app)
    assert public.get('/api/content/board?q=통합&category=notice').json()[0] == post
    assert public.get('/api/content/board/' + post['id']).json() == post
    with db() as c:
        assert c.execute('SELECT 1 FROM items WHERE id=?', (post['id'],)).fetchone()
    edited = client.put('/api/content/board/' + post['id'], json={**value, 'title': '수정 공지', 'updatedAt': post['updatedAt']}, headers=HEADERS)
    assert edited.status_code == 200
    assert client.put('/api/content/board/' + post['id'], json={**value, 'updatedAt': post['updatedAt']}, headers=HEADERS).status_code == 409
    assert client.delete('/api/content/board/' + post['id'], params={'updatedAt':post['updatedAt']}, headers=HEADERS).status_code == 409
    assert client.delete('/api/content/board/' + post['id'], params={'updatedAt':edited.json()['updatedAt']}, headers=HEADERS).status_code == 200
    assert public.get('/api/content/board/' + post['id']).status_code == 404

def test_photos_content_validation_and_order():
    client = authenticated()
    assert client.post('/api/photos', files={'file':('fake.png',b'<script>bad</script>','image/png')}, headers=HEADERS).status_code == 422
    assert client.post('/api/photos', files={'file':('large.png',b'x'*(5*1024*1024+1),'image/png')}, headers=HEADERS).status_code == 413
    ids=[]
    for color in ['red', 'blue']:
        raw=io.BytesIO(); Image.new('RGB',(20,20),color).save(raw,format='PNG')
        r=client.post('/api/photos',files={'file':(color+'.png',raw.getvalue(),'image/png')},headers=HEADERS)
        assert r.status_code == 201, r.text
        photo=r.json(); ids.append({'id':photo['id']})
        assert TestClient(app).get(photo['url']).headers['content-type'] == 'image/webp'
    value={'title':'활동 테스트','description':'활동 기록','photos':list(reversed(ids))}
    result=client.post('/api/content/activities',json=value,headers=HEADERS)
    assert result.status_code == 201
    assert [p['id'] for p in result.json()['photos']] == [p['id'] for p in reversed(ids)]
    assert client.post('/api/content/projects',json={**value,'link':'javascript:alert(1)'},headers=HEADERS).status_code == 422
    assert client.post('/api/content/projects',json=value,headers=HEADERS).status_code == 422
    assert client.post('/api/content/projects',json={**value,'photos':ids[:1],'link':'https://example.org'},headers=HEADERS).status_code == 201
    assert client.post('/api/content/board',json={'title':'  ','content':'abc'},headers=HEADERS).status_code == 422
    assert client.post('/api/content/activities',json={**value,'photos':[{'id':'missing'}]},headers=HEADERS).status_code == 422

def test_static_navigation_and_login_rate_limit():
    client=TestClient(app)
    for path in ['/', '/about.html','/activities.html','/projects.html','/board.html','/apply.html','/admin.html','/api.js','/analysis/index.html']:
        assert client.get(path).status_code == 200
    for _ in range(10):
        assert client.post('/api/auth/login',json={'username':'invalid','password':'wrong'},headers=HEADERS).status_code == 401
    assert client.post('/api/auth/login',json={'username':'invalid','password':'wrong'},headers=HEADERS).status_code == 429

def test_clean_page_urls_and_legacy_redirects():
    client = TestClient(app)
    for name in ['about', 'activities', 'projects', 'board', 'apply', 'admin']:
        assert client.get('/' + name).status_code == 200
        response = client.get('/' + name + '.html?id=a%2Fb&x=1', follow_redirects=False)
        assert response.status_code == 308
        assert response.headers['location'] == '/' + name + '?id=a%2Fb&x=1'
    for old, new in [('/index.html', '/'), ('/analysis/index.html', '/analysis/')]:
        response = client.get(old, follow_redirects=False)
        assert response.status_code == 308
        assert response.headers['location'] == new
        assert client.get(new).status_code == 200
    assert client.get('/analysis/vis-network.min.js').status_code == 200
    for path in ['/server', '/data/voda', '/missing', '/missing.html']:
        assert client.get(path).status_code == 404
