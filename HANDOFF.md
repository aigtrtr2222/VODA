# VODA 노트북 Codex 인수인계

## 최신 변경: 2026-10-11 Projects 미니게임

- 관계망 옆 미니게임 탭 추가. `/analysis/minigame/`에 수박게임 규칙을 참고한 독립 구현 '광복을 향해' 연결. 첫 탭 선택 시 로드, 탭 변경 시 물리 계산 일시정지. 별도 창에서도 실행 가능.
- 유관순/안중근/윤봉길/이육사/윤동주/김구 얼굴 모티브 공 6단계 + 태극기 마지막 단계. 내장 image_gen 생성 원본 portraits.png 사용, 프롬프트/출처는 analysis/minigame/SOURCES.md. Matter.js 0.20.0과 MIT 라이선스 로컬 포함, 외부 CDN 불필요.
- 같은 단계 공 충돌 시 다음 단계 하나 생성, 중복 충돌 중복 합성 방지, 점수/다음 공/상단 넘침 패배/태극기 광복 승리/다시 시작/일시정지. 마우스·터치·방향키/스페이스 및 위치 슬라이더/공 놓기 버튼 지원. DB/운영 게시글 변경 없음.
- tests/minigame_browser_check.py 임시 DB+Chrome 통과: 탭/낙하, 같은 공/다른 공/3개 동시 충돌, 태극기 및 광복 승리, 넘침 패배, 재시작/탭 정지/모바일 터치/키보드/가로 넘침. PC/모바일 화면 확인.
- 기존 tests/browser_check.py 전체 통과: 게시판/홈/사진/프로젝트/관계망/모바일/재시작 보존 회귀 없음. 관계망 테스트 선택자를 해당 iframe으로 한정하여 새 iframe과 구분.
- 서버 반영은 `cd ~/VODA && git pull --ff-only`. 기존 analysis 정적 경로 활용으로 재시작 불필요. 운영 적용은 사용자 SSH 실행 대기.

## 최신 변경: 2026-10-11 이미지 제한 2배 확대

- 원본 이미지 용량 한도를 5→10MB(10×1024×1024 bytes), 화소 한도를 2천만→4천만으로 확대. 서버 업로드/요청 본문 제한, 관리자 파일 선택 검사·안내, README 동기화. admin.js 캐시 버전 갱신.
- 저장 이미지는 기존과 같이 긴 변 2400px 이하 WebP로 변환하며 사진 장수 제한은 유지. 운영 DB 변경 없음.
- 임시 DB tests/test_backend.py 6개 통과: 정확히 10MB/4천만 화소 허용, 1바이트/5천 화소 초과 거부, 저장 이미지 크기 제한 유지 포함. 기존 Starlette 경고 1건.
- 서버 적용: `cd ~/VODA && git pull --ff-only && sudo systemctl restart voda`. 관리자 화면 새로고침 필요. GitHub 업로드 후 실제 운영 적용은 사용자 SSH 실행 대기.

## 최신 변경: 2026-10-10 숨은 퀴즈

- 사용자 제공 VODA 부스 퀴즈 대본.pdf 확인. 진행 방식은 14개 번호 중 3개를 뽑는 사람/AI 시 구분 퀴즈이나 실제 비교 지문과 정답표는 없음. 사용자에게 보완 질문 후, 현재 자료로 가능한 작가·작품·주제 퀴즈를 우선 구현한다고 안내함. 사람/AI 판별 정답을 임의 생성하지 않음. 비교 지문 수령 시 해당 방식 전환 가능.
- analysis/quiz/에 14문항, 중복 없는 무작위 3문제 추첨, 보기 순서 변경, 1회 답변/즉시 정오답 및 해설, 점수/오답 복습, 다시 뽑기 구현. 원문 시 전문과 PDF는 배포하지 않음. questions.js에 대본 기반 작가/주제만 수록.
- 메인 캐릭터 가운데를 연속 5번 누르면 `/analysis/quiz/` 접속. 탭 사이 2초 이상 쉬면 횟수 초기화. 키보드 포커스 후 Enter/Space도 가능. 로고 홈 이동과 기존 메뉴는 보존. DB/계정/점수 저장 없음. 숨김은 탐색 장치이며 주소 접근을 차단하는 인증 기능은 아님.
- tests/quiz_browser_check.py: 임시 DB + Chrome에서 PC/모바일 터치 입장, 14개 문항/보기 검증, 중복 없는 추첨, 2/3 채점, 해설, 재시작, 새로고침 초기화, 키보드, 모바일 넘침 및 JS 오류 없음 통과. PC/모바일 화면 확인.
- 기존 tests/browser_check.py 전체도 통과: 게시판/홈/사진/프로젝트/분석/모바일/재시작 보존 회귀 없음.
- 기존 analysis 정적 경로를 사용하므로 서버 반영은 `cd ~/VODA && git pull --ff-only`로 가능. 서버 재시작 불필요. 운영 적용은 사용자 SSH 실행 대기.

## 최신 변경: 2026-10-10 불필요한 안내 문구 제거

- 사용자 요청으로 Activities 소개의 '이 글은…아닙니다' 문구 3종과 'Projects에서 관계망을…읽어보세요' 문장을 제거. 활동/프로젝트의 AI 생성 일러스트 화면 캡션도 제거했으며 이미지 및 생성 기록은 유지.
- cleanup_activity_copy.py는 실행 전 DB를 백업하고 해당 문장만 제거한다. 본문 전체 덮어쓰기 없이 이미지/제목/작성일 보존, updatedAt만 갱신. publish_activities.py로 새로 등록하는 글에도 동일 정리 적용.
- 임시 DB 검증: 해당 문장 삭제, 첨부 이미지/작성일 보존, 반복 실행 시 변경 없음, 신규 등록 본문에 해당 문구 없음 통과.
- GitHub 갱신 후 서버에서 `cd ~/VODA && git pull --ff-only && .venv/bin/python cleanup_activity_copy.py` 실행 필요. 운영 DB 수정은 사용자 SSH 실행 대기. content.js URL 버전 갱신, 서버 재시작 불필요.

## 최신 변경: 2026-10-10 이미지 실제 첨부 누락 수정

- 운영 공개 API 확인: 등록된 Activities 3개/Projects 2개의 photos가 모두 빈 배열. 활동 일러스트는 content.js의 대체 표시만 있었고 프로젝트 이미지 및 관리자 첨부 사진은 없었음. 운영 이미지 정적 URL은 200으로 존재 확인.
- attach_content_images.py 추가: manage.py backup 실행 후 하나의 트랜잭션에서 기존 5개 글에 생성 일러스트를 WebP 사진으로 저장하고 /media/ 참조 연결. 본문/작성일 유지, updatedAt 갱신, 기존 사진이 있으면 보존, 누락된 글은 건너뜀. 역사 프로젝트 2개는 역사 탐구 일러스트 사용.
- 활동/프로젝트 화면에 AI 생성 일러스트 표시 유지. content.js URL 버전을 변경해 이전 캐시 갱신 유도.
- tests/test_content_images.py 임시 DB 검증 통과: 5개 글 첨부, 실제 이미지 API 응답, 정상 관리자 저장 경로에서 이미지 유지, 재실행 중복 없음/기존 데이터 보존/백업 생성.
- 임시 DB + 실제 Chrome에서 활동 이미지 3개/프로젝트 이미지 2개 로딩 및 모바일 가로 넘침 없음/JS 오류 없음 확인.
- 서버 반영: `cd ~/VODA && git pull --ff-only && .venv/bin/python attach_content_images.py`. Attached 5가 최초 정상 결과. 기존 첨부는 preserved, 누락된 글은 missing posts로 구분. 운영 DB 쓰기는 사용자 SSH 실행 대기. 재시작 불필요.

## 최신 변경: 2026-10-10 메인 Activities 연동

- 원인: 메인은 board API만 읽어 활동 분류 게시글만 표시하고 Activities는 제외했음.
- 메인에서 board와 activities를 함께 조회해 작성일 최신순으로 합친 뒤 최대 6개 표시. 전체/활동 탭에 Activities가 포함되고 공지/모집 분류는 유지. Board 목록 자체는 기존대로 유지.
- 활동 링크는 `/activities#activity-ID`로 해당 활동 위치에 이동. 활동 탭 더보기는 `/activities`. AI 이미지의 원본 크기를 지정해 이미지 로딩에 따른 위치 이동 감소.
- tests/browser_check.py에 메인 전체/활동/공지 필터와 활동 이동 검증 추가. 이전 보고서 카드 추가로 중복된 프로젝트 분류 선택자를 프로젝트 항목 안으로 한정하여 테스트 오류 수정.
- 임시 DB + 실제 Chrome 전체 검사 통과: 새 홈 연동, 기존 게시판 CRUD/사진/프로젝트/관계망/모바일/재시작 후 보존. 예상 밖 HTTP·JavaScript 오류 없음.
- 배포는 `cd ~/VODA && git pull --ff-only` 후 브라우저 강력 새로고침. 정적 파일만 변경, DB 변경·서버 재시작 불필요. 운영 반영은 사용자 서버 터미널 실행 대기.

## 최신 변경: 2026-10-10 Activities AI 일러스트

- built-in image_gen으로 스터디/공모전 협업/역사 자료 탐구 일러스트 3장 생성. 원본 PNG를 images/activities/{seminar,team,history}-ai.png로 복사. 프롬프트는 같은 폴더 GENERATION.md에 기록.
- content.js에서 승인된 Activities 3개 ID에 사진이 없을 때만 일러스트를 표시하고 AI 생성 일러스트 캡션 추가. 실제 업로드 사진이 있으면 기존 슬라이더 우선. 운영 DB 수정 없음.
- 임시 DB + Chrome에서 3장 로딩, 모바일 가로 넘침, 업로드 사진 우선 표시, JS 오류 없음 통과. 데스크톱/모바일 스크린샷 검수 완료.
- 서버 반영: `cd ~/VODA && git pull --ff-only`. 아직 활동 글을 등록하지 않았다면 `.venv/bin/python publish_activities.py` 추가 실행. 정적 파일 변경으로 재시작 불필요. 실제 운영 반영은 사용자 SSH 실행 대기.

## 최신 변경: 2026-10-10 Activities 소개 3개 준비

- 사용자 요청으로 지부별 세미나, 공모전 TF, 독립운동 공개 자료 탐구 소개를 publish_activities.py에 작성. 기존 공개 모집 안내 및 제공된 자료에 근거하며 확인하지 않은 행사 날짜·참가 인원·수상 성과·사진은 추가하지 않음.
- publish_content.publish(posts)로 등록 로직을 공유. Activities만 별도로 추가하며 기존 프로젝트/공지를 재등록하지 않는다. 자동 DB 백업, 고정 ID/제목 중복 방지, 기존 글 보존 유지.
- 임시 DB에서 활동 3개 생성 및 공개 API 조회, 반복 실행 시 중복 없음, 기존 글/수정 내용 보존, 백업 생성 검증 통과. 화면 레이아웃 변경 없음.
- GitHub 업로드 후 서버에서 `cd ~/VODA && git pull --ff-only && .venv/bin/python publish_activities.py` 실행 필요. 운영 DB 등록은 사용자 서버 터미널 실행 대기이며 서버 재시작 불필요.

## 최신 변경: 2026-10-10 승인된 프로젝트/공지 등록 준비

- 사용자가 채팅에서 검토한 프로젝트 2개와 공지 3개의 사이트 등록을 승인함. publish_content.py에 승인된 본문과 링크를 준비했다.
- 서버에서 `.venv/bin/python publish_content.py` 실행 시 선택된 VODA_DATA_DIR(기본 data)의 DB를 manage.py backup으로 먼저 백업하고 한 트랜잭션에서 추가한다. 고정 ID 및 동일 제목 검사를 사용해 재실행 시 중복·기존 글 덮어쓰기를 방지한다. 게시일은 실제 실행일.
- 임시 DB에서 5개 생성, 기존 글 보존, 재실행 시 0개 추가, 이미 수정한 글 보존, 백업 파일 생성 통과.
- 공지 출처: 기존 사이트/제공된 관계망·보고서 및 https://linkareer.com/activity/347618 . Instagram 직접 열람은 제한되어 확인한 것처럼 작성하지 않았음. 신규 모집 일정이나 활동 성과를 임의로 만들지 않음.
- 운영 DB에는 아직 쓰지 않았음. 노트북에 서버 SSH 키가 없어 사용자 서버 터미널에서 `cd ~/VODA && git pull --ff-only && .venv/bin/python publish_content.py` 실행 필요. DB 등록만 하므로 재시작 불필요.

## 최신 변경: 2026-10-10 연구 보고서 추가

- 사용자가 루트에 제공한 안동 내앞마을 및 풍산 일대 독립운동 보고서를 Projects 목록 아래 연구 보고서 카드로 추가.
- 본문 보기 `/analysis/reports/andong/`, 원본 Word 다운로드 `/analysis/reports/andong/report.docx`. 웹 본문은 원문 텍스트·표 1개·이미지 4개를 포함하며 원문 주장은 별도 사실 검증하거나 수정하지 않음.
- 운영 DB를 변경하지 않는 정적 자료. 관리자 프로젝트 목록 편집과 별개로 소스에서 관리한다.
- 임시 DB + Chrome 검증: Projects에서 보고서 이동, 본문/표/이미지 4개 로딩, 다운로드 파일과 원본 바이트 일치, 390px 가로 넘침 없음, JavaScript 오류 없음. 데스크톱/모바일 첫 화면 스크린샷 확인.
- Word 원본 자체의 페이지 레이아웃은 재렌더링하지 않았으며 파일 내용 그대로 다운로드 제공.
- GitHub 업로드 후 VM에서 `cd ~/VODA && git pull --ff-only` 실행 필요. 이번 변경은 정적 파일만이므로 이미 이전 서버 변경을 적용했다면 재시작 불필요. 운영 URL 반영은 아직 미확인.

## 최신 변경: 2026-10-09 확장자 없는 페이지 주소

- `/about`, `/activities`, `/projects`, `/board`, `/apply`, `/admin`에서 기존 화면 제공. 홈은 `/`, 관계망은 `/analysis/`.
- 기존 `.html` URL은 308 리디렉션하며 게시글 id 등 쿼리를 보존. 메뉴/홈 공지/관리자/관계망 링크 및 실행 안내도 변경.
- 허용된 HTML 파일에만 경로를 추가하여 DB·서버 코드 비공개 유지. 분석 데이터와 운영 DB는 변경하지 않음.
- 임시 DB pytest 5개 통과. 실제 Chrome에서 확장자 없는 URL로 전체 브라우저 검사 통과: 게시판 CRUD/홈 연동/사진/프로젝트/관계망/모바일/로그아웃 권한/서버 재시작 후 데이터 보존. 예상 밖 HTTP 및 JavaScript 오류 없음.
- GitHub 변경을 VM에 반영할 때 `cd ~/VODA && git pull --ff-only && sudo systemctl restart voda` 필요. 서버 코드 변경이므로 이번 업데이트는 재시작 필수. 운영 반영은 사용자 SSH 실행 후 확인 필요.

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
| `analysis/index.html`, `analysis/vis-network.min.js` | 제공받은 독립운동가 관계망과 그래프 라이브러리 |
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

- Google Cloud VM + Caddy HTTPS 운영. 로컬 기본 바인딩 127.0.0.1:8000.
- 독립운동가 관계망 수령 및 로컬 연결 완료. 운영 반영 상태는 최신 날짜의 기록 참조.
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
- 사용자가 VM 설정 스크립트 실행 후 사이트 접속 및 관리자 게시글 등록 정상 동작을 보고함. 노트북 DB는 서버로 옮기지 않음.
- 외부에서 직접 확인: HTTP 308로 HTTPS 전환, 홈/관리자/health/분석 준비 화면 HTTP 200, 비로그인 auth/me 401, DB 및 server.py 경로 404. 인증서 검증을 켠 연결에서 TLS 1.3 및 인증서 만료 2026-12-31 확인.
- 운영 주소 https://voda-run.duckdns.org, 관리자 https://voda-run.duckdns.org/admin.html. Google Cloud VM에서 운영하므로 사용자 노트북을 꺼도 접속 가능. VM 재부팅 후 자동 시작과 실제 인증서 갱신은 아직 관찰하지 않았으며 설정상 활성화됨.
- 후속: 실제 분석 파일 수령/연결, 활동 자료 등록, 운영 DB 정기 백업 및 VM 외부 IP 변경 시 DNS 갱신 관리. 기존 비용 안내대로 VM 무료 한도와 별도로 외부 IPv4 및 초과 트래픽 비용을 확인해야 함.

## 개인 데이터

배포 대상 소스에는 운영 DB, 실제 관리자 계정/비밀번호, 원격 인증정보를 포함하지 않는다. 로컬 data 폴더는 사용자가 생성한 운영 데이터를 포함할 수 있으므로 보존하고 공유하지 않는다.
소스의 테스트 비밀번호는 격리된 자동 테스트용이다. 운영 계정에 재사용하지 않는다.

## 2026-10-09 독립운동가 관계망 연결

- 사용자 제공 ZIP의 HTML과 vis-network 라이브러리를 analysis/에 배치했다. 원본 분석 데이터는 변경하지 않았다. 제공 자료 기준 인물 208명, 단체 55개, 사건 50개, 관계 492개이며 역사적 정확성을 별도 검증한 것은 아니다.
- Projects 탭/iframe 제목을 독립운동가 관계망으로 변경하고 새 탭 보기 링크를 추가했다. 기존 사이트 디자인과 iframe 샌드박스를 유지했다.
- 격리된 임시 DB 및 실제 Chrome에서 tests/browser_check.py 전체 통과: 관계망 표시/검색/연도 필터/단체 및 관계 선택/사건 표시 전환, 외부 폰트·CDN 차단 상태 표시, 모바일 가로 넘침 검사.
- 기존 게시판 CRUD/홈 연동/활동 사진/프로젝트/비로그인 조회/서버 재시작 후 데이터 유지도 통과했다. 운영 DB·관리자 계정 변경과 마이그레이션은 없다.
- 배포 절차: GitHub main 갱신 후 VM SSH에서 `cd ~/VODA && git pull --ff-only`. 정적 파일 변경으로 서버 재시작은 필요 없다.
- 노트북에 VM SSH 개인키가 없어 서버 갱신은 사용자 터미널 실행 대기. GitHub 업로드와 운영 사이트 반영을 구분하며 운영 반영은 공개 URL 재확인 필요.
