"""Optional Chrome check: isolated DB, no production accounts or content."""
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='voda-quiz-') as temp:
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        base = f'http://127.0.0.1:{port}'
        process = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'server:app', '--port', str(port)], cwd=ROOT,
                                   env={**os.environ, 'VODA_DATA_DIR': temp}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                try:
                    urllib.request.urlopen(base + '/api/health', timeout=1)
                    break
                except OSError:
                    time.sleep(.1)
            with sync_playwright() as p:
                browser = p.chromium.launch(channel='chrome', headless=True)
                page = browser.new_page(viewport={'width':1280, 'height':900}, has_touch=True)
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(base + '/')
                trigger = page.locator('#secret-quiz-trigger')
                for _ in range(4): trigger.click()
                assert page.url == base + '/'
                trigger.click()
                expect(page.locator('#intro')).to_be_visible()
                assert page.url.endswith('/analysis/quiz/')
                data = page.evaluate('window.VODA_QUIZ_QUESTIONS')
                assert len(data)==14 and len({q['id'] for q in data})==14
                assert all(len(set(q['choices']))==4 and q['answer'] in q['choices'] for q in data)
                answers = {q['question']:q['answer'] for q in data}
                page.locator('#start').click()
                seen = []
                for i in range(3):
                    question = page.locator('#question').inner_text()
                    seen.append(question)
                    expect(page.locator('#next')).to_be_hidden()
                    correct = answers[question]
                    buttons = page.locator('.choice')
                    # One wrong answer followed by two correct answers.
                    choice = next(x for x in buttons.all_text_contents() if x != correct) if i==0 else correct
                    buttons.filter(has_text=choice).click()
                    expect(page.locator('#feedback')).to_be_visible()
                    assert all(b.is_disabled() for b in buttons.all())
                    page.locator('#next').click()
                assert len(set(seen))==3
                expect(page.locator('#result-score')).to_have_text('2 / 3')
                expect(page.locator('.review-item')).to_have_count(3)
                page.locator('#restart').click()
                expect(page.locator('#progress-text')).to_have_text('1 / 3 문제')
                expect(page.locator('#score-text')).to_have_text('정답 0개')
                page.reload()
                expect(page.locator('#intro')).to_be_visible()
                page.set_viewport_size({'width':390,'height':844})
                page.goto(base + '/')
                for _ in range(5): page.locator('#secret-quiz-trigger').tap()
                expect(page.locator('#intro')).to_be_visible()
                page.locator('#start').focus()
                page.keyboard.press('Enter')
                expect(page.locator('#game')).to_be_visible()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                page.screenshot(path=str(ROOT / '.tools' / 'quiz-mobile.png'))
                page.set_viewport_size({'width':1280,'height':900})
                page.screenshot(path=str(ROOT / '.tools' / 'quiz-desktop.png'))
                assert not errors, errors
                browser.close()
            print('PASS: hidden entry desktop/mobile, 14 questions, unique draw, scoring, feedback, retry, keyboard, refresh, no JS errors')
        finally:
            process.terminate()
            process.wait(timeout=15)


if __name__ == '__main__':
    main()
