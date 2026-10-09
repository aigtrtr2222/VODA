"""Local first-run setup and server. Secrets are entered on this computer only."""
import getpass
import os
import uvicorn
from server import db, set_admin

if __name__ == '__main__':
    with db() as c:
        exists = c.execute('SELECT 1 FROM admins LIMIT 1').fetchone()
    if not exists:
        print('VODA 첫 실행: 관리자 계정을 만듭니다.')
        username = input('관리자 아이디 [admin]: ').strip() or 'admin'
        while True:
            password = getpass.getpass('비밀번호 (12자 이상): ')
            confirm = getpass.getpass('비밀번호 확인: ')
            if password != confirm:
                print('비밀번호가 다릅니다. 다시 입력하세요.')
                continue
            try:
                set_admin(username, password)
                break
            except ValueError as error:
                print(error)
    host = os.environ.get('VODA_HOST', '127.0.0.1')
    port = int(os.environ.get('VODA_PORT', '8000'))
    print(f'\n홈페이지: http://127.0.0.1:{port}\n관리자: http://127.0.0.1:{port}/admin\n종료: Ctrl+C\n')
    uvicorn.run('server:app', host=host, port=port)
