# VODA — Claude Code 안내

작업 지침은 `AGENTS.md`를 따른다. 한국어로 소통한다.

- 로컬 실행: `README.md` 2장 (`start.bat` / `bash start.sh`)
- 서버 배포: `README.md` 7장, 에이전트 규칙은 7-9. 배포 스크립트는 `deploy/enable-server.sh`.
- 관리자 비밀번호는 사용자가 터미널에서 직접 입력한다 (`manage.py create-admin`). 비밀번호를 묻거나 저장하지 않는다.
- `data/`(실제 DB)를 지우거나 커밋하지 않는다. 업데이트 전 `manage.py backup`.
- 테스트: `.venv/bin/python -m pytest -q` (Windows: `test.bat`)
