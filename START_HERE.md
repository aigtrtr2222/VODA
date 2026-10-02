# Windows 11 노트북에서 시작하기

## 1. 압축 풀기

이 ZIP은 사이트 전체 소스와 Codex 인수인계 자료가 들어 있는 개발용 복사본입니다.
예를 들어 `C:\dev\VODA`에 압축을 풉니다. 그 폴더 안에 `server.py`, `AGENTS.md`, `start.bat`이 직접 보여야 합니다.
압축 파일 안에서 실행하지 마세요. Python은 3.11 이상이 필요합니다.

## 2. Codex에서 이어받기

`open_codex.bat`을 더블클릭하면 이 프로젝트 폴더에서 `codex`를 실행합니다.
또는 PowerShell에서 실제 압축을 푼 경로로 이동한 뒤 실행합니다.

```powershell
cd C:\dev\VODA
codex
```

`CODEX_FIRST_TASK.txt` 내용을 Codex에 붙여 넣으세요.
파일이 있는 폴더에서 실행하면 Codex가 로컬 파일을 읽고 수정할 수 있습니다.
이 ChatGPT 대화를 노트북 Codex가 자동으로 이어받는다고 가정하지 않습니다. AGENTS.md와 HANDOFF.md에 필요한 프로젝트 맥락을 넣었습니다.

데스크톱 Codex 앱을 설치한 경우에는 폴더/프로젝트 열기에서 이 `VODA` 폴더를 선택하고 같은 요청문을 넣으면 됩니다.

## 3. 사이트를 직접 먼저 켜보기

`start.bat` 더블클릭 → 첫 관리자 계정 만들기 → 아래 주소 접속.

- 홈페이지: http://127.0.0.1:8000
- 관리자: http://127.0.0.1:8000/admin.html

비밀번호 입력 중 글자가 보이지 않는 것은 정상입니다. 비밀번호는 채팅에 보내지 마세요.
서버 터미널을 켜둔 상태에서 브라우저를 사용합니다. 종료는 Ctrl+C입니다.

## 4. 자동 검사

`test.bat` 더블클릭. 필요한 테스트 패키지를 설치하고 임시 DB에서 API 테스트를 실행합니다.
마지막에 `4 passed`가 나오면 현재 포함된 4개 테스트가 통과한 것입니다.
관리자 계정을 먼저 만들거나 서버를 미리 실행할 필요는 없습니다.

Codex가 명령을 실행할 때는 아래 비대화형 명령을 쓰면 됩니다.

```powershell
.\setup.bat
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

## 5. 실제 화면 검사

TEST_CHECKLIST.md를 따라 공지 하나, 활동 사진, 프로젝트를 등록해보세요.
시크릿 창에서 같은 로컬 주소를 열어 저장한 글이 보이는지 확인하고 서버 재시작 후에도 남는지 확인합니다.
자동 테스트는 화면 배치와 Windows 실행까지 보장하지 않으므로 이 단계가 필요합니다.

## 자주 막히는 경우

- `codex`를 찾을 수 없음: 설치한 터미널을 닫고 새로 열어 `codex --version` 확인. PowerShell에서 스크립트 정책 오류가 나면 `codex.cmd` 또는 `open_codex.bat` 사용.
- Python을 찾을 수 없음: Python 3.11 이상 설치 후 새 터미널. Codex 설치와 Python 설치는 별개입니다.
- 검은 창에 오류: 창을 닫지 말고 오류 텍스트를 Codex에 붙여 넣어 수정을 요청하세요.
- 8000 포트 사용 중: 기존 실행 창을 종료하거나, 별도 포트를 쓸 경우 `VODA_PORT`를 설정하고 출력된 주소로 접속하세요.
- 빈 게시판: 첫 실행은 데이터가 없는 상태입니다. 관리자에서 테스트 공지를 작성하세요.
- GitHub Pages 주소에서 글이 보이지 않음: 아직 기존 공개 사이트와는 연결하지 않았습니다. 여기서는 localhost 주소로 검사합니다.
- 비밀번호를 잊음: 프로젝트 폴더에서 `.\.venv\Scripts\python.exe manage.py create-admin` 실행 후 같은 아이디와 새 비밀번호 입력.

## 다음에 작업을 이어갈 때

같은 `VODA` 폴더에서 Codex를 열고 `HANDOFF.md를 읽고 이어서 작업해줘`라고 요청하면 됩니다.
도메인/배포는 로컬 동작 확인 후 진행합니다. 로컬 주소는 노트북 안에서만 접근 가능합니다.

공식 안내:
- https://learn.chatgpt.com/docs/codex/cli
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
