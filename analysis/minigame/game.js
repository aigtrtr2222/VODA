(() => {
  'use strict';
  const $ = id => document.getElementById(id), canvas = $('game'), ctx = canvas.getContext('2d');
  const atlas = new Image(); atlas.src = 'portraits.png';
  const names = LiberationGame.names, radii = LiberationGame.radii;
  let paused = false, tabVisible = true, loaded = false, lastFrame = 0, accumulator = 0;
  function flag(c, x, y, r) {
    c.save(); c.translate(x,y); c.scale(r/100,r/100);
    c.fillStyle='white'; c.fillRect(-81,-54,162,108);
    c.save(); c.rotate(Math.atan2(2,3));
    c.fillStyle='#cd2e3a'; c.beginPath();c.arc(0,0,29,Math.PI,2*Math.PI);c.arc(14.5,0,14.5,0,Math.PI);c.arc(-14.5,0,14.5,0,Math.PI,true);c.fill();
    c.fillStyle='#0047a0';c.beginPath();c.arc(0,0,29,0,Math.PI);c.arc(-14.5,0,14.5,Math.PI,0);c.arc(14.5,0,14.5,Math.PI,0,true);c.fill();c.restore();
    for (const [tx,ty,angle,pattern] of [[-51,-33,-.59,[1,1,1]],[51,33,-.59,[0,0,0]],[51,-33,.59,[0,1,0]],[-51,33,.59,[1,0,1]]]) {
      c.save();c.translate(tx,ty);c.rotate(angle);c.fillStyle='#17232b';
      pattern.forEach((full,i)=>{ const yy=(i-1)*7; if(full)c.fillRect(-14,yy-2,28,4);else {c.fillRect(-14,yy-2,11,4);c.fillRect(3,yy-2,11,4);} });c.restore();
    }
    c.restore();
  }
  function portrait(c, level, x, y, r) {
    c.save(); c.beginPath(); c.arc(x,y,r,0,Math.PI*2); c.clip();
    c.fillStyle='#fff'; c.fillRect(x-r,y-r,2*r,2*r);
    if (level===6) flag(c,x,y,r);
    else if (loaded) {
      const w=atlas.naturalWidth/3,h=atlas.naturalHeight/2;
      c.drawImage(atlas,(level%3)*w,Math.floor(level/3)*h,w,h,x-r,y-r,2*r,2*r);
    }
    c.restore();c.strokeStyle=level===6?'#d5ae48':'#aa9765';c.lineWidth=2;c.beginPath();c.arc(x,y,r,0,Math.PI*2);c.stroke();
  }
  function overlay(title, text, button, symbol='✦') {
    $('overlay').hidden=false;$('heading').textContent=title;$('message').textContent=text;$('start').textContent=button;$('symbol').textContent=symbol;
  }
  function update(g) {
    $('score').textContent=g.score;$('next-name').textContent=names[g.next];
    $('pause').disabled=g.status!=='playing';
    $('drop').disabled=g.status!=='playing'||paused||!tabVisible||!loaded;
    $('aim').min=14+radii[g.current];$('aim').max=406-radii[g.current];$('aim').value=g.aim;
    if(g.status==='won') {overlay('광복','태극기를 완성했습니다! 함께 이어온 만남의 결실입니다.','다시 도전','🇰🇷');$('status').textContent=`광복! 최종 점수 ${g.score}점`;}
    else if(g.status==='lost') {overlay('잠시 쉬어가요',`공이 점선을 넘었습니다. 최종 점수 ${g.score}점`,'다시 도전');$('status').textContent='게임 종료';}
    else if(g.status==='playing') $('status').textContent=`지금 놓을 공: ${names[g.current]}`;
  }
  const game = new window.LiberationGame(update);
  function draw() {
    ctx.clearRect(0,0,420,590);ctx.fillStyle='#fffdf6';ctx.fillRect(0,0,420,590);
    ctx.lineWidth=1;ctx.strokeStyle=game.danger?'#cf514a':'#b8c8c5';ctx.setLineDash([6,6]);ctx.beginPath();ctx.moveTo(14,100);ctx.lineTo(406,100);ctx.stroke();ctx.setLineDash([]);
    ctx.fillStyle='#81938c';ctx.font='11px sans-serif';ctx.fillText('넘치지 않게 조심하세요',20,91);
    for(const b of game.balls) portrait(ctx,b.level,b.position.x,b.position.y,b.circleRadius);
    if(game.status==='playing') {
      ctx.globalAlpha=.25;ctx.strokeStyle='#0b9088';ctx.beginPath();ctx.moveTo(game.aim,56);ctx.lineTo(game.aim,566);ctx.stroke();ctx.globalAlpha=1;
      portrait(ctx,game.current,game.aim,43,radii[game.current]);
    }
    ctx.strokeStyle='#accac1';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(8,107);ctx.lineTo(8,574);ctx.lineTo(412,574);ctx.lineTo(412,107);ctx.stroke();
  }
  function frame(now) {
    const delta=Math.min(now-lastFrame,80);lastFrame=now;
    if(!paused&&tabVisible&&!document.hidden&&loaded) {
      accumulator+=delta;
      while(accumulator>=1000/60) {game.step();accumulator-=1000/60;}
    } else accumulator=0;
    draw();requestAnimationFrame(frame);
  }
  function start() {
    if(!loaded)return;
    if(paused&&game.status==='playing'){paused=false;$('pause').textContent='일시정지';}
    else {game.reset();paused=false;game.start();}
    $('overlay').hidden=true;$('restart-confirm').hidden=true;update(game);canvas.focus();
  }
  $('start').disabled=true;$('start').textContent='이미지 준비 중…';
  atlas.onload=()=>{
    loaded=true;$('start').disabled=false;$('start').textContent='게임 시작';
    names.forEach((name,i)=>{const li=document.createElement('li'),c=document.createElement('canvas');c.width=c.height=84;c.setAttribute('aria-hidden','true');portrait(c.getContext('2d'),i,42,42,39);const label=document.createElement('span');label.textContent=name;li.append(c,label);$('levels').append(li);});
  };
  atlas.onerror=()=>{overlay('이미지를 불러오지 못했어요','페이지를 새로고침해주세요.','새로고침');$('start').disabled=false;$('start').onclick=()=>location.reload();};
  $('start').addEventListener('click',start);
  $('pause').addEventListener('click',()=>{if(game.status!=='playing')return;paused=!paused;$('pause').textContent=paused?'계속하기':'일시정지';if(paused)overlay('잠시 멈춤','준비되면 이어서 플레이하세요.','계속하기');else $('overlay').hidden=true;update(game);});
  $('drop').addEventListener('click',()=>{if(!paused&&tabVisible)game.drop();});
  $('aim').addEventListener('input',e=>game.setAim(Number(e.target.value)));
  function aim(e){const r=canvas.getBoundingClientRect();game.setAim((e.clientX-r.left)/r.width*420);$('aim').value=game.aim;}
  canvas.addEventListener('pointermove',aim);
  let activePointer = null;
  canvas.addEventListener('pointerdown',e=>{if(game.status!=='playing'||paused||!tabVisible)return;activePointer=e.pointerId;e.preventDefault();canvas.focus();canvas.setPointerCapture(e.pointerId);aim(e);});
  canvas.addEventListener('pointerup',e=>{if(activePointer!==e.pointerId)return;activePointer=null;if(game.status!=='playing'||paused||!tabVisible)return;aim(e);game.drop();});
  canvas.addEventListener('pointercancel',()=>{activePointer=null;});
  canvas.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight',' ','Enter'].includes(e.key)){e.preventDefault();if(paused)return;if(e.key==='ArrowLeft')game.setAim(game.aim-15);else if(e.key==='ArrowRight')game.setAim(game.aim+15);else game.drop();$('aim').value=game.aim;}});
  $('restart').addEventListener('click',()=>{if(game.status==='playing'){$('restart-confirm').hidden=false;}else start();});
  $('confirm-restart').addEventListener('click',()=>{game.reset();start();});
  $('cancel-restart').addEventListener('click',()=>{$('restart-confirm').hidden=true;});
  window.addEventListener('message',e=>{if(e.source===parent&&e.data?.type==='voda-game-visibility'){tabVisible=Boolean(e.data.visible);accumulator=0;update(game);}});
  requestAnimationFrame(frame);
})();
