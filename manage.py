import argparse, getpass, sqlite3
from pathlib import Path
from server import DB, db, set_admin
p = argparse.ArgumentParser(description='VODA 관리 도구')
p.add_argument('action', choices=['create-admin', 'backup'])
p.add_argument('--output', default='voda-backup.sqlite3')
a = p.parse_args()
if a.action == 'create-admin':
    username = input('관리자 아이디: ').strip()
    password = getpass.getpass('비밀번호 (12자 이상): ')
    if password != getpass.getpass('비밀번호 확인: '):
        raise SystemExit('비밀번호가 다릅니다.')
    set_admin(username, password)
    print('계정을 저장했습니다. 해당 계정의 기존 세션은 종료되었습니다.')
else:
    target = Path(a.output).resolve()
    if target.exists() or target == DB:
        raise SystemExit('새 백업 파일 이름을 지정하세요.')
    with db() as source, sqlite3.connect(target) as dest:
        source.backup(dest)
    print('백업 완료:', target)
