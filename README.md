# VODA — 설치해서 사용하는 동아리 웹사이트

공지 게시판, 활동 사진, 프로젝트 소개와 관리자 화면을 제공하는 웹사이트입니다.
Python FastAPI + SQLite + HTML/CSS/바닐라 JavaScript로 구성되어 있습니다.

저장소를 내려받아 본인 컴퓨터에서 실행할 수 있습니다. GitHub 계정이나 Codex는 실행에 필요하지 않습니다.
설치한 컴퓨터마다 독립된 DB와 관리자 계정을 사용하며, 처음에는 게시글과 업로드 사진이 비어 있습니다.

## 가장 빠른 실행

Python 3.11 이상이 필요합니다. Windows 11 + Python 3.12.10에서 검증했습니다.
처음 실행할 때 패키지 설치용 인터넷 연결이 필요합니다.

### Windows

1. [Python 공식 사이트](https://www.python.org/downloads/windows/)에서 Python 3.11 이상을 설치합니다. 설치 시 **Add python.exe to PATH**를 선택하고 터미널을 다시 여세요.
2. 이 저장소 상단의 **Code → Download ZIP**으로 내려받아 압축을 풉니다.
3. `start.bat`을 더블클릭합니다. 가상환경 생성과 필요한 패키지 설치가 자동으로 진행됩니다.
4. 열린 터미널에서 관리자 아이디와 비밀번호(12자 이상)를 만듭니다. 비밀번호 입력 중 글자가 보이지 않는 것이 정상입니다.
5. 브라우저에서 **http://127.0.0.1:8000**을 엽니다.
6. **http://127.0.0.1:8000/admin.html**에서 만든 계정으로 로그인해 콘텐츠를 등록합니다.

서버 터미널을 열어 둔 동안 사이트를 사용할 수 있습니다. 다음부터는 `start.bat`만 실행하면 됩니다.
기본 주소는 설치한 컴퓨터 안에서만 접속할 수 있습니다.

| 파일 | 용도 |
|---|---|
| `start.bat` | 설치 준비 후 사이트 실행 |
| `setup.bat` | 가상환경과 실행 패키지 준비 |
| `test.bat` | 실제 DB와 분리된 자동 테스트 |
| `START_HERE.md` | 자세한 Windows 안내와 문제 해결 |
| `TEST_CHECKLIST.md` | 기능 확인 항목과 검증 기록 |

Python 오류가 나오면 `py -3 --version`으로 버전을 확인하세요.
`winget`이 없는 Windows에서도 위 공식 사이트에서 설치 파일을 직접 내려받을 수 있습니다.
다른 컴퓨터에서 가져온 `.venv`는 재사용하지 말고 이름을 바꾼 뒤 `start.bat`을 실행하세요.

### Ubuntu / macOS

프로젝트 폴더에서:

```bash
bash start.sh
```

Ubuntu에서 venv 생성 오류가 나면 `python3-venv` 패키지를 설치한 후 다시 실행하세요.

서버를 끝내려면 터미널에서 Ctrl+C를 누릅니다. 다음 실행부터 기존 계정을 사용합니다.
HTML 파일을 더블클릭하거나 Live Server만 켜면 백엔드가 실행되지 않습니다.

## 사용 흐름

- Board: 공지/활동/모집 분류, 글 등록·수정·삭제, 고정 공지.
- Home: Board의 최신 글 6개와 분류별 목록. 제목을 누르면 상세 페이지.
- Board 방문자 화면: 제목 검색, 분류, 6개씩 페이지 이동, 고정 공지 2개.
- Activities: 제목·설명·사진 최대 20장. 관리자에서 사진 순서 변경 가능.
- Projects: 제목·설명·분류·대표 사진 1장·외부 프로젝트 링크.
- 사진: JPG/PNG/WebP, 원본 5MB 이하·2천만 화소 이하. 서버에서 방향 보정 후 긴 변 2400px 이하 WebP로 변환하고 EXIF/GPS 메타데이터를 제거합니다.
- 방문자는 로그인 없이 조회하고, 저장·수정·삭제·업로드는 관리자만 가능합니다.
- 저장한 데이터는 다른 브라우저에서도 같은 서버 주소로 접속하면 조회할 수 있습니다. 이미 열려 있던 방문자 화면은 새로고침하면 갱신됩니다.

## 데이터와 계정

글, 관리자 비밀번호 해시, 세션, 사진이 `data/voda.sqlite3`에 저장됩니다.
서버를 껐다 켜도 남습니다. 이 폴더를 지우지 마세요. 배포할 때는 영구 디스크가 필요합니다.
비밀번호·DB·테스트 데이터는 제공 소스에 포함되지 않습니다.

관리자 계정 추가 또는 비밀번호 재설정:

```bash
# Windows는 .venv\\Scripts\\python.exe 사용
.venv/bin/python manage.py create-admin
```

동일한 아이디를 입력하면 비밀번호가 갱신되고 그 계정의 기존 로그인 세션이 종료됩니다.
로그인은 12시간 유지됩니다. 한 IP에서 15분 내 로그인 10회 실패 시 제한됩니다.

일관된 DB 백업(서버 실행 중에도 가능):

```bash
.venv/bin/python manage.py backup --output voda-backup-2026-10-02.sqlite3
```

복원은 서버를 종료한 다음, 기존 `data` 폴더를 별도로 보관하고 빈 `data` 폴더에 백업을 `voda.sqlite3`라는 이름으로 복사합니다.
사진도 DB에 포함되므로 같은 백업으로 복구됩니다. 백업에는 계정 정보도 들어가므로 비공개로 보관하세요.
삭제한 게시물의 사진이나 업로드 후 저장하지 않은 사진은 현재 자동 정리하지 않습니다.

## 데이터 분석 파일 연결

`analysis/index.html`은 **준비 중 안내 화면**입니다. 실제 분석 결과는 만들어 넣지 않았습니다.
동현이에게 완성된 분석 HTML과 부속 CSS/JS/데이터를 받으면 `analysis/` 안에 넣고 진입 파일을 `index.html`로 맞추면 됩니다.
Projects의 분석 탭은 이미 이 파일을 iframe으로 표시합니다.
iframe에는 `allow-scripts allow-downloads` 샌드박스를 적용했습니다. 쿠키·부모 화면 접근을 요구하는 자료나 상대 경로 fetch를 사용하는 자료는 추가 연동 검토가 필요합니다.
Python/Dash/Streamlit 형태라면 파일 수령 후 별도 연결 작업이 필요합니다.

## 프론트 담당자 전달사항

기존 화면 디자인과 URL을 유지했습니다. `api.js`가 공통 API 호출을 담당합니다.

| 파일 | 변경 내용 |
|---|---|
| `script.js` | localStorage 대신 서버 게시판 데이터 조회 |
| `content.js` | IndexedDB 대신 서버 활동·프로젝트 조회, 사진 URL 표시 |
| `admin.js` | 관리자 세션, API 등록·수정·삭제, 사진 업로드 |
| `admin.html`, `admin.css` | 로그인 화면·로그아웃 추가 |
| 각 HTML | `api.js` 로드 추가 |
| `projects.html` | 분석 파일 iframe 연결 |
| `server.py` | 인증·콘텐츠·사진·정적 파일 제공 |

기존 브라우저 localStorage/IndexedDB의 데이터는 자동 이전하지 않습니다. 기존에 등록한 내용이 있다면 따로 이전해야 합니다.
현재 프론트와 API를 **같은 주소**로 제공하므로 CORS 설정이 필요 없습니다.
기존 GitHub Pages 사이트에는 변경을 게시하지 않았습니다. 이 프로젝트를 실행한 주소에서만 새 백엔드가 작동합니다.

## API 계약

실행 후 `http://127.0.0.1:8000/docs`에서 스키마를 확인할 수 있습니다.
쓰기 요청에는 `X-Voda-Request: 1` 헤더가 필요합니다. 로그인 응답의 HttpOnly 세션 쿠키를 사용합니다.
Swagger에서 쓰기 테스트를 할 때는 해당 헤더를 별도로 설정해야 하므로 기본적으로 관리자 화면 사용을 권장합니다.

| 메서드 | 경로 | 기능 |
|---|---|---|
| POST | `/api/auth/login` | 아이디·비밀번호로 로그인 |
| GET | `/api/auth/me` | 세션 확인 |
| POST | `/api/auth/logout` | 로그아웃 |
| GET | `/api/content/{kind}` | 목록; q/category/limit/offset 선택 |
| GET | `/api/content/{kind}/{id}` | 상세 |
| POST | `/api/content/{kind}` | 생성 |
| PUT | `/api/content/{kind}/{id}` | 수정; 현재 updatedAt 필요 |
| DELETE | `/api/content/{kind}/{id}?updatedAt=...` | 삭제; 현재 버전 필요 |
| POST | `/api/photos` | multipart/form-data의 file 업로드 |
| GET | `/media/{id}` | WebP 사진 조회 |
| GET | `/api/health` | 상태 확인 |

`kind`는 `board`, `activities`, `projects`입니다.
게시판 필드: title, content, category, pinned.
활동 필드: title, description, photos: [{id}].
프로젝트 필드: 활동 필드 + projectCategory, link. 사진 최대 1장.
id, createdAt, updatedAt, date, 사진 url/name은 서버가 생성합니다.
수정 시 조회한 updatedAt을 보내며, 다른 창에서 먼저 수정하면 409를 반환합니다. 입력 내용을 복사한 후 새로고침해 병합하세요.

## 검증

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

테스트는 임시 DB에서 인증·CSRF·비공개 파일 차단, 공유 조회·CRUD·동시 수정 충돌, 사진 검증·순서·크기 제한, 페이지 연결·로그인 제한을 확인합니다.

## 나중에 배포할 때

지금은 로컬 구축 버전입니다. 무료 도메인 발급과 외부 서버 배포는 아직 하지 않았습니다.
기본 실행은 내 컴퓨터에서만 접속 가능한 127.0.0.1 주소입니다.
추후 HTTPS를 설정한 뒤 `VODA_HTTPS=1`로 Secure 쿠키를 활성화하고, 영구 DB 저장 공간·백업·프록시의 업로드 용량 제한을 설정하세요.
`VODA_DATA_DIR`로 데이터 폴더를 변경할 수 있습니다. 여러 서버로 확장할 경우 외부 DB와 파일 저장소로 전환하세요.

### 이번 구현에서 확인한 결과

- Windows 11 / Python 3.12.10: `test.bat` 및 pytest API 테스트 **4개 통과**.
- 실제 Chrome 자동 검사: 관리자 로그인/로그아웃, 게시글 등록·수정·삭제, 홈 연동, 검색·분류·페이지 이동, 사진 업로드·순서 변경·슬라이더, 프로젝트 표시, 분석 준비 화면 통과.
- 별도 비로그인 브라우저 컨텍스트 조회 및 서버 프로세스 재시작 후 데이터 유지 통과.
- JavaScript 구문, 모바일 폭 메뉴/관리자 입력 화면, 이미지 로딩 검사 통과.
- 테스트에서 Starlette의 httpx 사용 중단 예정 경고 1건이 있으며 기능 테스트는 통과했습니다.

선택적으로 설치된 Chrome을 이용한 브라우저 검사를 실행할 수 있습니다.

```powershell
.\.venv\Scripts\python.exe -m pip install playwright
.\.venv\Scripts\python.exe tests\browser_check.py
```

브라우저 검사도 임시 DB와 자동 생성한 테스트 계정만 사용합니다.

## 개발 및 배포 파일

실제 `data/`, `.env`, DB 백업, 계정 정보, `.venv`, 다운로드한 설치 파일은 Git에 포함하지 않습니다.
사이트에서 업로드한 사진은 DB에 저장됩니다. `images/`에는 사이트 기본 디자인에 쓰는 이미지가 있습니다.
새 버전을 적용할 때는 먼저 DB를 백업하고, 기존 `data/`를 보존하세요.

개발 인수인계는 `HANDOFF.md`, 작업 규칙은 `AGENTS.md`에 있습니다.
원본 프론트: [minzi0/VODA](https://github.com/minzi0/VODA).
