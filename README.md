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

## 7. 서버에 배포하기 (인터넷에 공개)

내 컴퓨터를 꺼도 누구나 `https://내도메인` 으로 접속할 수 있게 하는 방법입니다.

**구성:** Ubuntu 24.04 서버 → `systemd`가 VODA(uvicorn, `127.0.0.1:8000`)를 항상 실행 → `Caddy`가 HTTPS 인증서 자동 발급 + 리버스 프록시.
이 과정은 `deploy/enable-server.sh` 스크립트가 처리합니다.

**필요한 것**

| 항목 | 예시 | 비고 |
|---|---|---|
| Ubuntu 24.04 서버 | Google Cloud `e2-micro`, AWS Lightsail, 집 PC 등 | 공인 IP가 있어야 함. 디스크는 영구 디스크 |
| 도메인 | `myclub.duckdns.org` | [DuckDNS](https://www.duckdns.org)에서 무료로 만들 수 있음 |
| 방화벽 | TCP **80, 443** 허용 | Caddy 인증서 발급에 둘 다 필요 |

### 7-1. 서버 만들기 (Google Cloud 예시)

다른 클라우드를 쓰면 "Ubuntu 24.04 VM 생성 + 80/443 허용"만 하면 됩니다. 이미 서버가 있으면 건너뛰세요.

```bash
# 로컬 또는 Cloud Shell에서 (gcloud 로그인·프로젝트 선택이 되어 있어야 함)
gcloud compute instances create voda-server \
  --zone=us-west1-a --machine-type=e2-micro \
  --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB --tags=http-server,https-server
gcloud compute firewall-rules create allow-web --allow=tcp:80,tcp:443 \
  --target-tags=http-server,https-server   # 이미 있으면 오류가 나도 괜찮음
gcloud compute instances describe voda-server --zone=us-west1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'   # 외부 IP 확인
```

서버 재시작 후에도 IP가 바뀌지 않게 하려면 콘솔에서 외부 IP를 **고정(static)** 으로 바꾸세요.

### 7-2. 도메인을 서버 IP에 연결

DuckDNS에 로그인해 서브도메인을 만들고, `current ip` 칸에 위에서 확인한 서버 외부 IP를 넣고 **update ip**를 누릅니다.
연결 확인 (서버 IP가 나와야 다음 단계로):

```bash
getent hosts myclub.duckdns.org    # 또는 nslookup myclub.duckdns.org
```

### 7-3. 서버에 설치

서버에 SSH로 접속합니다 (GCP: `gcloud compute ssh voda-server --zone=us-west1-a`). **root가 아닌 일반 사용자**로 진행합니다.

```bash
sudo apt update
sudo apt install -y git python3-venv python3-pip caddy
cd ~
git clone https://github.com/aigtrtr2222/VODA.git
cd ~/VODA
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

경로에 공백이 없어야 합니다 (`~/VODA` 권장).

### 7-4. 관리자 계정 만들기 (사람이 직접 입력)

```bash
cd ~/VODA
.venv/bin/python manage.py create-admin
```

아이디와 비밀번호(12자 이상)를 **터미널에 직접** 입력합니다. 이 단계가 끝나야 `data/voda.sqlite3`가 생기고 다음 스크립트가 실행됩니다.

### 7-5. 자동 실행 + HTTPS 켜기

**VODA만 운영하는 새 서버라면:**

```bash
cd ~/VODA
bash deploy/enable-server.sh myclub.duckdns.org
```

스크립트가 하는 일: `voda` systemd 서비스 생성(부팅 시 자동 시작, `VODA_HTTPS=1`), `/etc/caddy/Caddyfile`을 백업 후 VODA용으로 교체, 서비스 재시작, `/api/health` 확인.
`sudo` 비밀번호를 물을 수 있습니다. 스크립트 자체를 `sudo`로 실행하지 마세요.

**이미 Caddy로 다른 사이트를 운영 중인 서버라면** (스크립트가 이를 감지하면 덮어쓰지 않고 멈춥니다):

```bash
cd ~/VODA
VODA_SKIP_CADDY=1 VODA_PORT=8002 bash deploy/enable-server.sh myclub.duckdns.org
```

- `VODA_PORT`는 다른 서비스와 겹치지 않는 포트로 정합니다 (`ss -ltnp`로 사용 중인 포트 확인).
- 스크립트가 출력하는 블록을 `/etc/caddy/Caddyfile` **끝에 추가**한 뒤 적용합니다:

  ```bash
  sudo nano /etc/caddy/Caddyfile        # 아래 블록 추가
  #   myclub.duckdns.org {
  #       reverse_proxy 127.0.0.1:8002
  #   }
  sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
  sudo systemctl reload caddy
  ```

### 7-6. 확인

```bash
curl -fsS http://127.0.0.1:8000/api/health        # VODA (포트를 바꿨다면 그 포트)
curl -fsS https://myclub.duckdns.org/api/health   # 외부 HTTPS
sudo systemctl status voda caddy --no-pager
```

브라우저에서 `https://myclub.duckdns.org` 와 `https://myclub.duckdns.org/admin` 을 열어 확인합니다.
인증서 발급에 1~2분 걸릴 수 있습니다.

### 7-7. 코드 업데이트

```bash
cd ~/VODA
.venv/bin/python manage.py backup --output ~/voda-backup-$(date +%Y%m%d-%H%M).sqlite3
git pull --ff-only
.venv/bin/pip install -r requirements.txt
sudo systemctl restart voda
curl -fsS http://127.0.0.1:8000/api/health
```

### 7-8. 문제 해결

| 증상 | 확인 / 해결 |
|---|---|
| `test -x .venv/bin/python` 에서 멈춤 | 7-3의 venv 생성을 안 함 |
| `test -f data/voda.sqlite3` 에서 멈춤 / `Create an administrator` | 7-4 관리자 계정을 먼저 만들기 |
| `command -v caddy` 에서 멈춤 | `sudo apt install -y caddy` (패키지가 없으면 [Caddy 공식 설치 안내](https://caddyserver.com/docs/install#debian-ubuntu-raspbian)) |
| `already serves other sites` | 7-5의 "이미 다른 사이트가 있는 서버" 방법 사용 |
| HTTPS가 안 열림 | 도메인이 서버 IP를 가리키는지(7-2), 80/443 방화벽, `sudo journalctl -u caddy -n 50 --no-pager` |
| 502 Bad Gateway | VODA가 꺼짐: `sudo journalctl -u voda -n 50 --no-pager` |
| 관리자 로그인이 계속 풀림 | `http://`가 아니라 `https://`로 접속 (Secure 쿠키) |
| 비밀번호 분실 | 서버에서 `cd ~/VODA && .venv/bin/python manage.py create-admin` 후 같은 아이디로 새 비밀번호 |

### 7-9. Claude Code 등 AI 에이전트로 배포할 때

이 README만 보고 에이전트(Claude Code CLI 등)에게 배포를 맡길 수 있습니다. 예시 요청:

> https://github.com/aigtrtr2222/VODA 의 README 7장을 따라 이 서버에 VODA를 배포해줘. 도메인은 `myclub.duckdns.org`.

에이전트가 지켜야 할 규칙:

1. **서버 상태를 먼저 확인**한다: `lsb_release -a`, `ss -ltnp`, `systemctl is-active caddy`, `cat /etc/caddy/Caddyfile`(있다면), `getent hosts <도메인>`과 서버 공인 IP(`curl -s ifconfig.me`) 일치 여부.
2. 7-3 설치는 직접 실행해도 된다. 이미 `~/VODA`가 있으면 새로 clone하지 말고 7-7 업데이트 절차를 따른다.
3. **7-4 관리자 계정은 사람이 직접 입력**하게 한다. 비밀번호를 채팅으로 받거나, 명령줄 인자·환경 변수·파일에 쓰지 않는다. (에이전트가 서버에서 직접 돌고 있으면 사용자에게 `! cd ~/VODA && .venv/bin/python manage.py create-admin` 입력을 요청하고, 로컬에서 SSH로 작업 중이면 사용자가 SSH 창에서 직접 실행하게 한다)
4. Caddyfile에 VODA가 아닌 사이트 블록이 있으면 `VODA_REPLACE_CADDY=1`을 쓰지 말고, `VODA_SKIP_CADDY=1` + 빈 포트로 실행한 뒤 블록을 **추가**한다. 기존 블록은 수정·삭제하지 않는다.
5. 클라우드 VM 생성, 방화벽 규칙, 고정 IP, DNS 변경처럼 비용이 들거나 외부에 영향을 주는 작업은 사용자 확인 후 진행한다.
6. `data/` 폴더와 DB를 지우거나 초기화하지 않는다. 업데이트 전에는 반드시 백업한다. `data/`, 백업 파일, `.env`는 커밋하지 않는다.
7. 끝나면 7-6 확인 명령의 실제 결과(성공/실패)를 그대로 보고하고, 접속 주소와 관리자 주소를 알려준다.

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
| `VODA_SKIP_CADDY` | `0` | `deploy/enable-server.sh` 전용: `1`이면 Caddy 설정을 건드리지 않음 |
| `VODA_REPLACE_CADDY` | `0` | `deploy/enable-server.sh` 전용: `1`이면 다른 사이트가 있어도 Caddyfile 교체 |

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

### 참고

- 개발 인수인계: `HANDOFF.md`, 작업 규칙: `AGENTS.md`, 기능 체크리스트: `TEST_CHECKLIST.md`
- 미니게임 이미지·라이선스 출처: `analysis/minigame/SOURCES.md`
- 원본 프론트엔드: [minzi0/VODA](https://github.com/minzi0/VODA)
