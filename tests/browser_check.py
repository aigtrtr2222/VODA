"""Optional real Chrome smoke check; isolated temporary DB, no production account.

Run: .venv\\Scripts\\python.exe tests\\browser_check.py
Requires: pip install playwright (uses installed Chrome, no browser download).
"""
import io
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

from PIL import Image
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='voda-browser-') as temporary:
        env = {**os.environ, 'VODA_DATA_DIR': temporary, 'PYTHONIOENCODING': 'utf-8'}
        password = secrets.token_urlsafe(24)
        # Send test credentials through stdin, never shell arguments or logs.
        subprocess.run([sys.executable, '-c',
                        'import sys; from server import set_admin; set_admin("browser-test", sys.stdin.read())'],
                       input=password, text=True, cwd=ROOT, env=env, check=True)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        base = f'http://127.0.0.1:{port}'
        process = None

        def start():
            nonlocal process
            process = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'server:app',
                                        '--host', '127.0.0.1', '--port', str(port)],
                                       cwd=ROOT, env=env, stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL)
            for _ in range(100):
                if process.poll() is not None:
                    raise RuntimeError('Test server exited before startup')
                try:
                    with urllib.request.urlopen(base + '/api/health', timeout=1) as response:
                        if response.status == 200:
                            return
                except OSError:
                    time.sleep(.1)
            raise RuntimeError('Test server did not become ready')

        def stop():
            if process and process.poll() is None:
                process.terminate()
                process.wait(timeout=15)

        start()
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(channel='chrome', headless=True)
                context = browser.new_context()
                visitor_context = browser.new_context()  # Separate cookie jar, like incognito.
                admin = context.new_page()
                visitor = visitor_context.new_page()
                page_errors = []
                bad_responses = []
                for page in (admin, visitor):
                    page.on('pageerror', lambda error: page_errors.append(str(error)))
                    page.on('response', lambda response: bad_responses.append(
                        (response.status, response.url.split(base)[-1]))
                        if response.url.startswith(base) and response.status >= 400
                        and response.status not in (401, 403) else None)
                    page.on('dialog', lambda dialog: dialog.accept())

                def visit(path):
                    visitor.goto(base + path, wait_until='networkidle')

                def save(title, body):
                    admin.locator('#editor-form [name=title]').fill(title)
                    admin.locator('#editor-form [name=body]').fill(body)
                    admin.locator('#save-button').click()
                    expect(admin.locator('#admin-message')).to_have_text('저장했습니다.')

                def new():
                    admin.locator('#new-button').click()

                admin.goto(base + '/admin.html')
                admin.locator('#login-form [name=username]').fill('browser-test')
                admin.locator('#login-form [name=password]').fill('wrong-password')
                admin.locator('#login-form button').click()
                expect(admin.locator('#login-message')).to_contain_text('확인')
                admin.locator('#login-form [name=password]').fill(password)
                admin.locator('#login-form button').click()
                expect(admin.locator('#admin-workspace')).to_be_visible()
                expect(admin.locator('#save-button')).to_be_enabled()
                admin.locator('[name=pinned]').check()
                save('브라우저 공지', '공지 본문')
                visit('/')
                expect(visitor.locator('#home-posts')).to_contain_text('브라우저 공지')
                visitor.locator('#home-posts a').filter(has_text='브라우저 공지').click()
                expect(visitor.locator('.board-detail-body')).to_have_text('공지 본문')
                visitor.locator('#voda-board-back').click()
                expect(visitor.locator('#voda-board-list')).to_be_visible()
                save('수정 공지', '수정 본문')
                admin.reload(wait_until='networkidle')
                admin.locator('#admin-list button').filter(has_text='수정 공지').click()
                expect(admin.locator('[name=body]')).to_have_value('수정 본문')
                for number in range(7):
                    new()
                    admin.locator('[name=category]').select_option(['notice', 'activity', 'recruit'][number % 3])
                    if number < 3:
                        admin.locator('[name=pinned]').check()
                    save(f'페이지 테스트 {number}', '목록 본문')
                visit('/board.html')
                expect(visitor.locator('#voda-board-posts .board-post-item')).to_have_count(6)
                expect(visitor.locator('#voda-board-pinned a')).to_have_count(2)
                visitor.locator('#voda-board-pagination button').filter(has_text='2').click()
                expect(visitor.locator('#voda-board-posts .board-post-item')).to_have_count(2)
                for category in ['notice', 'activity', 'recruit']:
                    visitor.locator(f'[data-board-category={category}]').click()
                    assert visitor.locator('.board-post-item').count() > 0
                visitor.locator('[data-board-category=all]').click()
                visitor.locator('[name=keyword]').fill('수정 공지')
                visitor.locator('#voda-board-search button').click()
                expect(visitor.locator('.board-post-item')).to_have_count(1)
                admin.locator('#admin-list button').filter(has_text='수정 공지').click()
                admin.locator('#delete-button').click()
                expect(admin.locator('#admin-message')).to_have_text('삭제했습니다.')
                visit('/')
                expect(visitor.locator('#home-posts')).not_to_contain_text('수정 공지')
                visit('/board.html')
                expect(visitor.locator('#voda-board-posts')).not_to_contain_text('수정 공지')
                print('PASS: board CRUD, home/detail, categories/search/pagination/pinned')

                files = []
                for color in ['red', 'blue']:
                    raw = io.BytesIO()
                    Image.new('RGB', (80, 60), color).save(raw, format='PNG')
                    files.append({'name': color + '.png', 'mimeType': 'image/png', 'buffer': raw.getvalue()})
                admin.locator('[data-tab=activities]').click()
                expect(admin.locator('#image-input')).to_be_visible()
                admin.locator('#image-input').set_input_files(files)
                save('활동 검증', '활동 설명')
                original = admin.locator('#image-preview img').first.get_attribute('src')
                admin.locator('[aria-label="사진 뒤로 이동"]').first.click()
                admin.locator('#save-button').click()
                expect(admin.locator('#admin-message')).to_have_text('저장했습니다.')
                admin.reload(wait_until='networkidle')
                admin.locator('[data-tab=activities]').click()
                admin.locator('#admin-list button').filter(has_text='활동 검증').click()
                assert admin.locator('#image-preview img').nth(1).get_attribute('src') == original
                visit('/activities.html')
                expect(visitor.locator('.activity-slide')).to_have_count(2)
                expect(visitor.locator('.activity-slide').first).to_be_visible()
                visitor.locator('.activity-next').click()
                expect(visitor.locator('.activity-slide').nth(1)).to_be_visible()
                assert visitor.locator('.activity-slide').nth(1).locator('img').evaluate(
                    'img => img.complete && img.naturalWidth > 0')
                admin.locator('[data-tab=projects]').click()
                expect(admin.locator('[name=projectCategory]')).to_be_visible()
                admin.locator('[name=projectCategory]').fill('데이터 분석')
                admin.locator('[name=link]').fill('https://example.org/')
                admin.locator('#image-input').set_input_files(files[:1])
                save('프로젝트 검증', '프로젝트 설명')
                visit('/projects.html')
                expect(visitor.locator('.project-entry')).to_contain_text('프로젝트 검증')
                expect(visitor.locator('.project-category')).to_have_text('데이터 분석')
                expect(visitor.locator('.managed-project-link')).to_have_attribute('href', 'https://example.org/')
                visitor.locator('[data-project-tab=analysis]').click()
                expect(visitor.frame_locator('iframe').locator('body')).to_contain_text('분석 결과를 준비하고 있습니다.')
                print('PASS: photo upload/reorder/slider, project display, analysis placeholder, isolated visitor')

                for path in ['/', '/about.html', '/activities.html', '/projects.html', '/board.html', '/apply.html']:
                    visit(path)
                    visitor.locator('img').evaluate_all("imgs => imgs.forEach(img => img.loading = 'eager')")
                    visitor.wait_for_function('Array.from(document.images).every(img => img.complete)')
                    assert visitor.locator('img').evaluate_all('imgs => imgs.every(img => img.naturalWidth > 0)'), path
                    expect(visitor.locator('#site-header .nav')).to_be_attached()
                visitor.set_viewport_size({'width': 390, 'height': 844})
                visit('/')
                visitor.locator('.menu-button').click()
                expect(visitor.locator('#site-header .nav')).to_be_visible()
                admin.set_viewport_size({'width': 390, 'height': 844})
                expect(admin.locator('#save-button')).to_be_visible()
                assert admin.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                admin.locator('#logout-button').click()
                expect(admin.locator('#login-panel')).to_be_visible()
                denied = context.request.post(base + '/api/content/board',
                                              headers={'X-Voda-Request': '1'},
                                              data={'title': 'denied', 'content': 'denied'})
                assert denied.status == 401
                stop()
                start()
                visit('/activities.html')
                expect(visitor.locator('.activity-row')).to_contain_text('활동 검증')
                assert visitor.locator('.activity-slide img').first.evaluate('img => img.complete && img.naturalWidth > 0')
                visit('/board.html')
                expect(visitor.locator('#voda-board-posts')).to_contain_text('페이지 테스트')
                visit('/projects.html')
                expect(visitor.locator('.project-entry')).to_contain_text('프로젝트 검증')
                assert not page_errors, page_errors
                assert not bad_responses, bad_responses
                print('PASS: page images/navigation/mobile, logout write denial, restart persistence, no unexpected HTTP/page errors')
                browser.close()
        finally:
            stop()


if __name__ == '__main__':
    main()
