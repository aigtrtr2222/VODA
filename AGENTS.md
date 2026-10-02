# VODA 프로젝트 작업 지침

## 먼저 읽을 파일

1. `HANDOFF.md`: 목표, 현재 구현, 남은 작업, 검증 현황.
2. `README.md`: 실행 방법과 API 계약.
3. `TEST_CHECKLIST.md`: 노트북에서 완료할 테스트.

한국어로 소통한다. 사용자는 Windows 11 노트북에서 이 프로젝트를 이어서 개발한다.
현재 요청은 기존 VODA 프론트에 연결된 백엔드를 로컬 실행·테스트하고 오류를 고치는 것이다.

## 구현 원칙

- Python FastAPI + SQLite + HTML/CSS/바닐라 JavaScript를 유지한다.
- 원본 디자인, 로고, 메뉴와 사용자 기능을 보존하며 필요한 부분만 수정한다.
- DB 데이터는 `data/voda.sqlite3`, 프론트와 API는 같은 origin에서 제공한다.
- 관리자 로그인은 HttpOnly 쿠키. 쓰기 요청에는 `X-Voda-Request: 1` 헤더가 필요하다.
- 저장/수정/삭제 권한은 서버에서 검사한다. 프론트 버튼을 숨기는 것만으로 대체하지 않는다.
- `data/`, `.env`, 계정 비밀번호, 세션, 개인 사진을 출력·커밋·공유하지 않는다.
- 실제 데이터가 있으면 초기화하지 않는다. 필요한 마이그레이션 전에 `manage.py backup`으로 백업한다.
- 자동 테스트는 임시 DB로 격리한다. 브라우저 테스트도 별도 `VODA_DATA_DIR`를 사용한다.
- 도메인 발급, HTTPS, 외부 배포, GitHub push는 현재 작업 범위에 없다. 사용자가 이후 요청하면 그 요청에 맞춰 진행한다.
- 분석 결과는 아직 미수령이다. `analysis/index.html`의 준비 중 화면을 실제 결과인 것처럼 채우지 않는다.

## Windows 개발 명령

PowerShell에서 프로젝트 루트 기준:

```powershell
.\setup.bat
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe run.py
```

첫 관리자 계정은 `run.py`의 터미널 입력으로 사용자가 직접 만든다. 계정 비밀번호를 채팅에 요구하지 않는다.
테스트 계정은 테스트 DB에서만 만들고, 테스트한 범위와 실패/미확인 범위를 구분해 보고한다.
브라우저 자동화 도구가 있으면 실제 화면 점검을 우선 수행하되, 없으면 수동 체크리스트를 안내한다.
작업 후 `HANDOFF.md`의 현황과 검증 기록을 갱신한다.
