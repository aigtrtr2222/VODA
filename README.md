# VODA 동아리 웹사이트

공지 게시판, 활동 사진, 프로젝트 소개, 관리자 화면이 있는 동아리 웹사이트입니다.
독립운동가 관계망, 미니게임 '광복을 향해', 숨은 퀴즈도 들어 있습니다.

Python(FastAPI) + SQLite + HTML/CSS/JavaScript로 만들었고, **누구나 자기 컴퓨터에서 내려받아 바로 열 수 있습니다.**
GitHub 계정은 필요 없습니다.

**[⬇ 소스 ZIP 다운로드](https://github.com/aigtrtr2222/VODA/archive/refs/heads/main.zip)**

---

## 1. 준비물

- **Python 3.11 이상** (Windows 11 + Python 3.12에서 확인)
- 처음 실행할 때 패키지 설치를 위한 인터넷 연결

Python이 없다면 [python.org](https://www.python.org/downloads/)에서 설치하세요.
Windows는 설치 첫 화면에서 **"Add python.exe to PATH"를 꼭 체크**하고, 설치 후 터미널을 새로 여세요.

## 2. 사이트 열기

### Windows

1. 위의 **소스 ZIP 다운로드**를 눌러 받은 뒤 **압축을 풉니다** (압축 파일 안에서 바로 실행하면 안 됩니다).
2. 압축을 푼 폴더에서 **`start.bat`을 더블클릭**합니다.
   필요한 패키지가 자동으로 설치됩니다 (처음 한 번, 1~2분).
3. 검은 창에서 **관리자 아이디와 비밀번호(12자 이상)** 를 정합니다.
   비밀번호를 입력할 때 글자가 안 보이는 것이 정상입니다.
4. 브라우저에서 **http://127.0.0.1:8000** 을 엽니다. 🎉

### macOS / Linux

```bash
git clone https://github.com/aigtrtr2222/VODA.git
cd VODA
bash start.sh
```

그다음 브라우저에서 **http://127.0.0.1:8000** 을 엽니다.
(Ubuntu에서 venv 오류가 나면 `sudo apt install python3-venv` 후 다시 실행하세요.)

### 꼭 알아둘 점

- **검은 창(서버)을 켜 둔 동안에만** 사이트가 열립니다. 끄려면 그 창에서 `Ctrl+C`.
- 다음부터는 `start.bat`(또는 `bash start.sh`)만 실행하면 됩니다. 계정과 글은 그대로 남아 있습니다.
- `index.html`을 더블클릭하거나 VS Code Live Server로 열면 **게시판·관리자 기능이 동작하지 않습니다.** 반드시 `start.bat`으로 실행하세요.
- 처음에는 게시판이 비어 있습니다. 관리자 화면에서 글을 올려 보세요.

## 3. 페이지 주소

| 주소 | 내용 |
|---|---|
| http://127.0.0.1:8000 | 홈 |
| http://127.0.0.1:8000/about | 소개 |
| http://127.0.0.1:8000/board | 게시판 |
| http://127.0.0.1:8000/activities | 활동 사진 |
| http://127.0.0.1:8000/projects | 프로젝트 (관계망·미니게임 탭) |
| http://127.0.0.1:8000/apply | 지원 |
| http://127.0.0.1:8000/admin | **관리자** (글·사진 등록, 수정, 삭제) |
| http://127.0.0.1:8000/analysis/ | 독립운동가 관계망 단독 화면 |

🎮 숨은 퀴즈: 홈의 메인 캐릭터 가운데를 **2초 안에 5번 연속** 누르면 열립니다.

## 4. 같은 와이파이의 다른 사람에게 보여주기 (선택)

기본 설정은 **내 컴퓨터에서만** 접속됩니다. 같은 네트워크의 휴대폰·다른 노트북에서 보려면:

```powershell
# Windows PowerShell
$env:VODA_HOST="0.0.0.0"; .\start.bat
```

```bash
# macOS / Linux
VODA_HOST=0.0.0.0 bash start.sh
```

그다음 다른 기기에서 `http://<내 컴퓨터 IP>:8000` 으로 접속합니다 (IP는 Windows `ipconfig`, macOS/Linux `ip a` 또는 `ifconfig`로 확인).
Windows 방화벽 허용 창이 뜨면 "개인 네트워크"를 허용하세요. 공용 와이파이에서는 사용하지 않는 것을 권장합니다.

## 5. 자주 막히는 경우

| 증상 | 해결 |
|---|---|
| `Python 3.11 or newer is required` | Python 3.11+ 설치 후 **터미널/창을 새로 열고** 다시 실행. `py -3 --version`으로 확인 |
| 창이 바로 꺼짐 / 오류 | 압축을 제대로 풀었는지, 폴더 안에 `server.py`와 `start.bat`이 바로 보이는지 확인 |
| 8000 포트 사용 중 | 이미 켜진 서버 창을 닫거나, `$env:VODA_PORT="8080"` 처럼 포트를 바꿔 실행 |
| 관리자 비밀번호를 잊음 | 프로젝트 폴더에서 `.venv\Scripts\python.exe manage.py create-admin` (macOS/Linux: `.venv/bin/python manage.py create-admin`) 실행 후 같은 아이디로 새 비밀번호 입력 |
| 다른 컴퓨터에서 복사한 폴더가 안 됨 | 안에 있는 `.venv` 폴더를 지우고 `start.bat` 다시 실행 |

## 6. 데이터와 백업

- 글, 사진, 관리자 계정은 모두 `data/voda.sqlite3` 한 파일에 저장됩니다. **이 폴더를 지우지 마세요.**
- 각 컴퓨터마다 DB가 따로 생기므로, 내 컴퓨터에 올린 글은 다른 사람 컴퓨터에는 보이지 않습니다.
- 백업 (서버 실행 중에도 가능):

  ```bash
  .venv/bin/python manage.py backup --output voda-backup.sqlite3
  ```

  복원: 서버를 끄고, 기존 `data` 폴더를 따로 보관한 뒤, 빈 `data` 폴더에 백업 파일을 `voda.sqlite3` 이름으로 넣습니다.
  백업에는 계정 정보가 들어 있으니 공개하지 마세요.

---

## 개발자용 정보

### 기능 요약

- **Board**: 공지/활동/모집 분류, 등록·수정·삭제, 고정 공지(2개), 제목 검색, 6개씩 페이지 이동
- **Home**: Board 최신 글 6개와 분류별 목록
- **Activities**: 제목·설명·사진 최대 20장, 관리자에서 사진 순서 변경
- **Projects**: 제목·설명·분류·대표 사진 1장·외부 링크 + 관계망/미니게임 탭
- **사진**: JPG/PNG/WebP, 10MB·4천만 화소 이하. 서버에서 방향 보정 → 긴 변 2400px 이하 WebP 변환, EXIF/GPS 제거
- 방문자는 로그인 없이 조회, 저장·수정·삭제·업로드는 관리자만 가능
- 로그인 12시간 유지, 한 IP에서 15분 내 10회 실패 시 제한

### 폴더 구조

| 경로 | 내용 |
|---|---|
| `server.py` | FastAPI 백엔드 (인증, 콘텐츠, 사진, 정적 파일) |
| `run.py` | 첫 관리자 생성 + 서버 실행 |
| `manage.py` | `create-admin`, `backup` 명령 |
| `*.html`, `style.css`, `script.js`, `content.js`, `api.js` | 방문자 화면 |
| `admin.html`, `admin.js`, `admin.css` | 관리자 화면 |
| `analysis/` | 독립운동가 관계망(`index.html` + `vis-network.min.js`), `minigame/`, `quiz/`, `reports/` |
| `images/` | 사이트 기본 이미지 |
| `deploy/enable-server.sh` | Ubuntu 서버용 systemd + Caddy HTTPS 설정 스크립트 |
| `tests/` | pytest API 테스트, Playwright 브라우저 검사 |

### 환경 변수

| 변수 | 기본값 | 설명 |
|---|---|---|
| `VODA_HOST` | `127.0.0.1` | 바인딩 주소 (`0.0.0.0`이면 외부 접속 허용) |
| `VODA_PORT` | `8000` | 포트 |
| `VODA_DATA_DIR` | `./data` | DB 저장 폴더 |
| `VODA_HTTPS` | `0` | `1`이면 Secure 쿠키 (HTTPS 배포 시) |

### API

실행 후 http://127.0.0.1:8000/docs 에서 스키마를 볼 수 있습니다.
쓰기 요청에는 `X-Voda-Request: 1` 헤더와 로그인 세션 쿠키(HttpOnly)가 필요합니다.

| 메서드 | 경로 | 기능 |
|---|---|---|
| POST | `/api/auth/login` | 로그인 |
| GET | `/api/auth/me` | 세션 확인 |
| POST | `/api/auth/logout` | 로그아웃 |
| GET | `/api/content/{kind}` | 목록 (q/category/limit/offset) |
| GET | `/api/content/{kind}/{id}` | 상세 |
| POST | `/api/content/{kind}` | 생성 |
| PUT | `/api/content/{kind}/{id}` | 수정 (현재 `updatedAt` 필요, 충돌 시 409) |
| DELETE | `/api/content/{kind}/{id}?updatedAt=...` | 삭제 |
| POST | `/api/photos` | 사진 업로드 (multipart `file`) |
| GET | `/media/{id}` | 사진 조회 (WebP) |
| GET | `/api/health` | 상태 확인 |

`kind`: `board`, `activities`, `projects`

### 테스트

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

Windows는 `test.bat`을 더블클릭해도 됩니다. 테스트는 임시 DB만 사용합니다.

### 인터넷에 공개 배포하기

Ubuntu 24.04 서버에 `git`, `python3-venv`, `python3-pip`, `caddy`를 설치하고 저장소를 받은 뒤:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py create-admin
bash deploy/enable-server.sh your-domain.example
```

도메인을 서버 IP에 연결하고 방화벽에서 TCP 80/443을 열어 두어야 합니다.
이 스크립트는 VODA 전용 서버를 가정하고 기존 Caddy 설정을 백업 후 교체합니다. 업데이트 전에는 꼭 `manage.py backup`으로 DB를 백업하세요.

### 참고

- 개발 인수인계: `HANDOFF.md`, 작업 규칙: `AGENTS.md`, 기능 체크리스트: `TEST_CHECKLIST.md`
- 미니게임 이미지·라이선스 출처: `analysis/minigame/SOURCES.md`
- 원본 프론트엔드: [minzi0/VODA](https://github.com/minzi0/VODA)
