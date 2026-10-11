"""Real browser integration and deterministic physics fixtures in a temp DB."""
import os, socket, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]

def main():
    with tempfile.TemporaryDirectory(prefix='voda-game-') as temp:
        with socket.socket() as s:
            s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
        base=f'http://127.0.0.1:{port}'
        proc=subprocess.Popen([sys.executable,'-m','uvicorn','server:app','--port',str(port)],cwd=ROOT,env={**os.environ,'VODA_DATA_DIR':temp},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                try: urllib.request.urlopen(base+'/api/health',timeout=1); break
                except OSError: time.sleep(.1)
            with sync_playwright() as p:
                browser=p.chromium.launch(channel='chrome',headless=True)
                page=browser.new_page(viewport={'width':1280,'height':1000},has_touch=True)
                # Observe the normal engine instance without shipping debug controls.
                page.add_init_script("""Object.defineProperty(window,'LiberationGame',{configurable:true,set(C){Object.defineProperty(window,'LiberationGame',{value:class extends C {constructor(...a){super(...a);window.testGame=this;}},configurable:true});}});""")
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(base+'/projects')
                page.locator('[data-project-tab=minigame]').click()
                frame=page.frame_locator('#minigame-frame')
                expect(frame.locator('#start')).to_be_enabled()
                frame.locator('#start').click()
                frame.locator('#game').click(position={'x':200,'y':200})
                expect(frame.locator('#status')).to_contain_text('지금 놓을 공')
                f=next(f for f in page.frames if '/minigame/' in f.url)
                assert f.evaluate('testGame.balls.length')==1
                frame.locator('#pause').click()
                expect(frame.locator('#heading')).to_have_text('잠시 멈춤')
                frame.locator('#start').click()
                page.locator('[data-project-tab=list]').click()
                now=f.evaluate('testGame.time');page.wait_for_timeout(250)
                assert f.evaluate('testGame.time')==now
                page.locator('[data-project-tab=minigame]').click()
                # Equal merge, unequal preservation, no double merge of three balls.
                result=f.evaluate('''() => {
                  const C=window.LiberationGame, g=new C(()=>{});g.start();
                  g.add(0,180,400);g.add(0,220,400);g.step();
                  const merged=g.balls.length===1&&g.balls[0].level===1&&g.score===20;
                  g.reset();g.start();g.add(0,180,400);g.add(1,220,400);g.step();
                  const unlike=g.balls.length===2;
                  g.reset();g.start();g.add(0,170,400);g.add(0,210,400);g.add(0,250,400);g.step();
                  return {merged,unlike,triple:g.balls.length===2&&g.score===20};
                }''')
                assert all(result.values()),result
                # Restore observed real instance after standalone fixtures.
                page.reload();page.locator('[data-project-tab=minigame]').click()
                frame=page.frame_locator('#minigame-frame');expect(frame.locator('#start')).to_be_enabled();frame.locator('#start').click();f=next(f for f in page.frames if '/minigame/' in f.url)
                f.evaluate('testGame.add(5,140,440);testGame.add(5,280,440);testGame.step()')
                expect(frame.locator('#heading')).to_have_text('광복')
                assert f.evaluate('testGame.balls.some(b=>b.level===6)')
                frame.locator('#start').click()
                assert f.evaluate('testGame.balls.length')==0
                f.evaluate('''() => { const b=testGame.add(3,200,75);b.born=-10000;Matter.Body.setStatic(b,true);for(let i=0;i<115;i++)testGame.step(); }''')
                expect(frame.locator('#heading')).to_have_text('잠시 쉬어가요')
                # Mobile standalone play, keyboard controls, local assets only.
                page.set_viewport_size({'width':390,'height':844})
                page.goto(base+'/analysis/minigame/')
                expect(page.locator('#start')).to_be_enabled();page.locator('#start').click()
                page.locator('#game').tap(position={'x':160,'y':230})
                assert page.evaluate('testGame.balls.length')==1
                page.wait_for_timeout(900)
                assert page.evaluate('testGame.balls[0].position.y')>150
                page.locator('#game').focus();page.keyboard.press('ArrowLeft')
                assert page.evaluate('testGame.aim')<210
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.screenshot(path=str(ROOT/'.tools/game-mobile.png'))
                page.set_viewport_size({'width':1000,'height':1000})
                page.screenshot(path=str(ROOT/'.tools/game-desktop.png'))
                assert not errors,errors
                browser.close()
            print('PASS: tab, drop, merges, unequal/triple collisions, flag/win, overflow/loss, restart, pause, mobile/keyboard')
        finally: proc.terminate();proc.wait(timeout=15)
if __name__=='__main__':main()
