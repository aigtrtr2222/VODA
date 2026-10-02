# VODA 노트북 Codex 인수인계

## 목표와 배경

VODA 동아리 소개 사이트의 기존 프론트에 백엔드를 붙이는 작업이다.
원본 공개 프론트: https://minzi0.github.io/VODA/
원본 저장소: https://github.com/minzi0/VODA
원본을 받아 로컬 작업 사본을 수정했다. 원본 GitHub에 push하거나 기존 사이트를 변경하지 않았다.
이 패키지는 2026-10-02에 준비한 노트북 개발용 복사본이며 `.git` 이력은 포함하지 않는다.
사용자는 Windows 11에 Codex를 설치했다. 별도 상시 서버는 없다.
현재 우선순위는 로컬 실행과 브라우저 테스트다. 도메인/배포 결정 때문에 로컬 테스트를 멈추지 않는다.

## 회의록에서 정리된 기능

- Home에서 게시판 제목과 공지 분류를 조회.
- About 소개, Activities 활동 내역/사진, Projects 프로젝트 소개.
- Board 공지·안내 글 목록/상세와 작성 기능.
- 동현이에게 독립유공자 데이터 분석 파일을 받아 Projects 탭에 연결.
- 활동 내용/사진/PPT 등 실제 자료는 운영진에게 받아야 한다.
- 무료 도메인과 HTTPS는 추후 작업. 회의록에 DuckDNS가 추천되어 있다.

## 구현 완료

- 원본 프론트 디자인과 이미지 포함.
- FastAPI 서버가 프론트 파일과 API를 같은 주소로 제공.
- SQLite에 게시글, 활동, 프로젝트, 사진 바이트, 관리자 해시, 로그인 세션 저장.
- 관리자 로그인/로그아웃/세션 확인. 비밀번호 scrypt 해시. 세션 12시간.
- Board 등록·수정·삭제·분류·고정 공지·검색·목록·상세.
- 홈 최신 게시글 6개 표시, Board 상세 링크.
- Activities 설명과 최대 20장 사진, 사진 순서 및 슬라이더.
- Projects 설명·분류·대표 사진 1장·외부 링크.
- 이미지 크기/파일 내용 검증, WebP 변환, EXIF 제거.
- updatedAt을 이용한 수정·삭제 충돌 감지.
- API 쓰기 요청의 사용자 인증과 custom header/origin 검사.
- DB·서버 소스 비공개: 루트 전체를 정적 디렉터리로 노출하지 않음.
- 관리자 계정 생성·재설정 도구, SQLite backup API 기반 백업.

## 파일 지도

| 파일 | 역할 |
|---|---|
| `server.py` | API, 데이터베이스, 인증, 이미지, 프론트 파일 제공 |
| `run.py` | 첫 관리자 계정 설정 후 서버 실행 |
| `manage.py` | create-admin / backup |
| `api.js` | 공통 fetch·서버 오류·사진 업로드 처리 |
| `script.js` | 공통 메뉴/푸터, Home와 Board 조회, 프로젝트 탭 |
| `content.js` | Activities/Projects 렌더링과 슬라이더 |
| `admin.js` | 로그인과 관리자 편집 화면 |
| `*.html`, `style.css`, `admin.css`, `images/` | 원본 기반 프론트 |
| `analysis/index.html` | 아직 자료가 없는 분석 탭의 준비 중 화면 |
| `tests/test_backend.py` | 임시 DB를 쓰는 API 자동 테스트 4개 |
| `setup.bat`, `start.bat`, `test.bat`, `open_codex.bat` | Windows 설치/실행/테스트/Codex 진입 |
| `start.sh` | Linux/macOS 실행 |
| `START_HERE.md` | 사용자가 먼저 읽을 노트북 안내 |
| `CODEX_FIRST_TASK.txt` | Codex에 붙여 넣을 첫 작업 요청 |

## 이전 검증 결과

- Python 3.12 Linux 환경에서 pytest 4개 통과.
- 구문 검사: api.js/admin.js/content.js/script.js 통과.
- jsdom DOM 에뮬레이터 + 실제 HTTP 서버 통합 검사 통과: 로그인, 글 생성/수정/삭제, 별도 방문자 조회, 활동 사진 업로드/재조회/슬라이더, 프로젝트 저장/표시, 분석 탭 전환.
- 해당 DOM 검사는 이전 작업 환경의 임시 스크립트로 실행했다. 패키지에 휴대 가능한 브라우저 자동화 테스트가 포함된 것은 아니다.
- 실제 Chromium 브라우저 화면 검사는 이전 환경에서 브라우저 다운로드 실패 및 로컬 주소 접근 제한으로 미완료.
- Windows 배치 파일의 실제 실행은 Windows 노트북에서 확인해야 한다. Linux API 테스트 통과를 Windows 검증으로 간주하지 않는다.

## 노트북 Codex가 먼저 할 일

1. 루트 경로, Python/Node/Codex 설치 상태를 확인한다.
2. `.venv`를 새로 만들고 의존성을 설치한다. 기존 `.venv`가 있으면 정상인지 확인한다.
3. 임시 DB에서 pytest를 실행하고 실패하면 원인을 고친다.
4. `run.py`를 실행하는 방법을 사용자에게 안내한다. 첫 관리자 암호 입력은 사용자 터미널에서 진행한다.
5. 실제 브라우저로 TEST_CHECKLIST.md 항목을 확인한다. 자동화 가능하면 별도 테스트 DB에서 수행한다.
6. 발견한 오류를 수정하고 관련 검사만 재실행한다.
7. 구현 완료/검증 완료/미완료를 구분해서 한국어로 짧게 보고한다.

## 알려진 제한 / 후속 작업

- 외부 배포와 HTTPS 없음. 기본 바인딩 127.0.0.1:8000.
- 분석 자료 미수령. iframe 경로 연결만 완료.
- Apply는 기존 '모집 기간 아님' 안내 유지. 지원서 수집 기능은 구현하지 않음.
- 이전 localStorage/IndexedDB 데이터 자동 이전 없음.
- 삭제된 게시물의 사진과 저장되지 않은 업로드는 자동 정리하지 않음.
- 이미 열린 방문자 화면에는 실시간 푸시 없음. 새로고침으로 반영.
- 이미지 외 PPT/PDF 첨부 기능 없음. 회의록의 활동 정리 PPT는 현재 입력 자료 요청으로 해석했으며 웹 첨부 요구 여부는 추후 확인 가능.
- SQLite 단일 서버 구성을 전제로 함. 여러 서버 확장이나 외부 서비스 전환은 추후.
- 현재 origin 검사 및 쿠키 설정은 같은 origin 로컬 실행용. HTTPS 프록시 배포 시 forwarded headers, Secure 쿠키와 origin 동작을 함께 점검해야 함.
- `requirements.txt`는 이전 환경에서 설치·검증된 주요 버전을 고정했다. 노트북 설치 실패 시 오류를 보고 실제 PyPI/네트워크/Python 호환성을 확인하고 필요할 때만 조정한다.

## 2026-10-02 Windows 노트북 작업 기록

- 프로젝트 경로 확인: `C:\Users\LG\Downloads\VODA_Codex_Laptop\VODA`.
- AGENTS.md, HANDOFF.md, START_HERE.md, README.md, TEST_CHECKLIST.md 및 실행/테스트 코드를 읽음.
- Python launcher 기준 설치 버전은 3.10.6 및 3.9. 프로젝트가 요구하는 3.11 이상이 없어 가상환경/의존성 설치는 아직 진행하지 못함.
- `tests/test_backend.py`가 서버 import 전에 임시 `VODA_DATA_DIR`를 설정하는 것을 확인. pytest 실행 자체는 미완료.
- 운영 DB `data/voda.sqlite3`는 확인 시 존재하지 않았으며, 운영 관리자 계정 생성이나 DB 초기화를 수행하지 않음.
- Python 공식 사이트에서 `python-3.12.10-amd64.exe`를 프로젝트 루트에 다운로드. 자동 설치 명령은 실행 정책에 의해 거부되어 사용자의 설치 파일 실행이 필요함.
- 설치 파일의 Authenticode 서명이 Valid이며 발행자가 Python Software Foundation임을 확인. api.js/admin.js/content.js/script.js의 Node 구문 검사 모두 통과.
- 서버 실행, 실제 브라우저 검사, 시크릿 조회, 서버 재시작 후 보존 검사는 아직 미완료. 분석 준비 중 화면과 기존 디자인은 변경하지 않음.
- 다음 작업: Python 설치 확인 → setup.bat → 개발 의존성 설치 → 임시 DB pytest → 격리된 브라우저 검증 → 사용자 터미널에서 운영 관리자 생성.

## 2026-10-02 Python 설치 후 Windows 검증

- Python 3.12.10 설치 확인. `setup.bat`으로 `.venv` 생성 및 requirements.txt 설치 성공. 개발 의존성과 선택적 Playwright 설치 완료.
- 임시 DB pytest: **4 passed** (8.41초). `pip check`: 의존성 충돌 없음. Starlette TestClient의 httpx 사용 중단 예정 경고 1건이며 현재 테스트 실패는 아님.
- 새 `tests/browser_check.py`로 실제 설치된 Chrome을 headless 실행해 검증. 임시 디렉터리 DB와 무작위 테스트 비밀번호만 사용하며 운영 계정에는 접근하지 않음. 종료 시 테스트 서버와 DB를 정리함.
- Chrome 통과: 잘못된 비밀번호 거부/로그인/로그아웃 후 서버 쓰기 거부, Board 생성·수정·새로고침·삭제, 홈 공지/상세/목록 복귀, 공지·활동·모집 분류/검색/8개 게시글 페이지 이동/고정 공지 최대 2개.
- Chrome 통과: 활동 사진 2장 업로드·순서 변경·새로고침·슬라이더, 프로젝트 대표 사진·분류·링크 표시, 분석 iframe의 기존 준비 안내, 독립된 쿠키 저장소의 비로그인 방문자 조회.
- Chrome 통과: 홈/About/Activities/Projects/Board/Apply 이미지 로딩과 메뉴, 390px 모바일 메뉴/관리자 저장 버튼/가로 넘침 검사, 테스트 서버 프로세스 종료 및 같은 DB로 재시작 후 글·사진·프로젝트 유지. 예상한 인증 거부 외 사이트 HTTP 오류 및 JavaScript pageerror 없음.
- 첫 브라우저 실행은 검사 문구를 '준비 중'으로 잘못 지정해 실패. 실제 기존 문구 '분석 결과를 준비하고 있습니다.'로 검사만 수정 후 전체 통과. 제품 코드/디자인/분석 화면 변경 없음.
- 운영 관리자 계정은 사용자가 `run.py` 터미널에서 직접 생성해야 함. 운영 계정 생성과 운영 서버의 실제 기동은 사용자 입력 후 확인 필요. GUI 시크릿 창 클릭 및 Ctrl+C 수동 종료 자체는 자동화하지 않았으며 별도 브라우저 컨텍스트/프로세스 재시작으로 동일 기능을 검증함.
- 실행: `start.bat` 또는 `.\.venv\Scripts\python.exe run.py`. 홈 `http://127.0.0.1:8000`, 관리자 `/admin.html`. 서버 종료 Ctrl+C.
- 브라우저 검사 재실행: `.\.venv\Scripts\python.exe tests\browser_check.py` (선택 의존성 `python -m pip install playwright`, 설치된 Chrome 필요). 기본 pytest 수집에는 포함되지 않음.
- 외부 배포/도메인 설정은 수행하지 않음. Duck DNS 인증정보는 파일/테스트에 기록하거나 사용하지 않음.
- `test.bat < NUL` 실제 Windows 배치 실행도 종료 코드 0, **4 passed** (4.31초). 사용자용 PowerShell 창에서 `run.py` 실행을 시작했으며 첫 관리자 입력은 사용자가 직접 완료해야 함.

## 2026-10-02 GitHub 소스 배포 준비

- 사용자가 aigtrtr2222 계정에 설치 가능한 소스와 README를 배포하도록 요청함. 웹 호스팅 배포가 아니라 저장소 배포임.
- README에 ZIP 다운로드 → Python 설치 → start.bat → 관리자 생성 흐름과 현재 검증 결과를 정리함.
- .gitignore에 도구/설치 파일/압축 파일/환경 파일/DB 및 키 파일 제외를 보강함. 운영 data 폴더와 .venv는 추적하지 않음.
- 로컬 Git main 저장소 초기화 및 소스 42개 선별. 제외 파일과 인증정보 패턴 검사 통과. 설치용 ZIP은 추적 제외된 dist에 생성하며 운영 DB는 포함하지 않음.
- GitHub CLI를 추적 제외된 .tools에 준비. 브라우저 인증 완료 후 API로 aigtrtr2222 계정 로그인 확인.
- 사용자가 공개 배포를 승인하여 https://github.com/aigtrtr2222/VODA 공개 저장소 생성 및 main 브랜치 push 완료. 원격 공개 상태와 커밋 일치를 확인함.
- 다운로드: 저장소의 Code → Download ZIP. Python 3.11 이상 설치 후 압축을 풀고 start.bat 실행. 웹 호스팅/도메인 설정은 수행하지 않음.

## 2026-10-02 Google Cloud VM 배포 진행

- 사용자가 Ubuntu 24.04 VM voda-server (us-west1-a)를 만들고 브라우저 SSH에 접속함. 사용자가 VM에서 패키지 설치, 저장소 clone, 가상환경 및 서버 관리자 생성 완료를 보고함.
- 외부 IP 136.86.229.248, voda-run.duckdns.org의 A 레코드가 해당 IP를 가리키며 AAAA는 조회되지 않음을 로컬에서 확인함.
- deploy/enable-server.sh 추가: 기존 VM 관리자/DB를 유지하고 systemd 자동 실행과 Caddy HTTPS 구성을 설치. 백엔드는 127.0.0.1:8000, 프록시 헤더 신뢰는 127.0.0.1에 한정, Secure 쿠키 활성화. 기존 시스템 설정은 덮어쓰기 전 백업함.
- 스크립트는 이 VODA 전용 Ubuntu VM을 전제로 /etc/caddy/Caddyfile을 구성함. 다른 사이트를 운영 중인 서버에서는 먼저 설정 통합 검토 필요.
- 실제 VM 스크립트 실행과 외부 HTTPS/관리자 로그인 검증은 아직 미완료. 노트북 DB는 서버로 옮기지 않음.

## 개인 데이터

배포 대상 소스에는 운영 DB, 실제 관리자 계정/비밀번호, 원격 인증정보를 포함하지 않는다. 로컬 data 폴더는 사용자가 생성한 운영 데이터를 포함할 수 있으므로 보존하고 공유하지 않는다.
소스의 테스트 비밀번호는 격리된 자동 테스트용이다. 운영 계정에 재사용하지 않는다.
