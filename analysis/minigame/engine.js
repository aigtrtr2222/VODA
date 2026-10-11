/* Circle merging simulation. Matter.js is bundled locally under its MIT license. */
class LiberationGame {
  static names = ['유관순', '안중근', '윤봉길', '이육사', '윤동주', '김구', '광복'];
  static radii = [22, 29, 37, 47, 59, 74, 94];
  constructor(onChange) {
    this.onChange = onChange;
    this.engine = Matter.Engine.create({positionIterations: 8, velocityIterations: 8});
    Matter.Events.on(this.engine, 'collisionStart', e => this.queue.push(...e.pairs));
    Matter.Events.on(this.engine, 'collisionActive', e => this.queue.push(...e.pairs));
    this.reset();
  }
  reset() {
    Matter.Composite.clear(this.engine.world, false);
    Matter.Engine.clear(this.engine);
    this.engine.timing.timestamp = 0;
    const wall = {isStatic:true, friction:.4, restitution:.1};
    Matter.Composite.add(this.engine.world, [
      Matter.Bodies.rectangle(2, 300, 20, 700, wall),
      Matter.Bodies.rectangle(418, 300, 20, 700, wall),
      Matter.Bodies.rectangle(210, 585, 440, 30, wall)
    ]);
    this.balls = []; this.queue = []; this.score = 0; this.time = 0;
    this.lastDrop = -1000; this.danger = 0; this.status = 'ready';
    this.current = 0; this.next = this.pick(); this.aim = 210;
    this.onChange?.(this);
  }
  pick() { return Math.floor(Math.random() * 3); }
  start() { if (this.status === 'ready') { this.status = 'playing'; this.onChange?.(this); } }
  setAim(x) {
    const r = LiberationGame.radii[this.current];
    this.aim = Math.max(14+r, Math.min(406-r, x));
  }
  add(level, x, y) {
    const body = Matter.Bodies.circle(x, y, LiberationGame.radii[level], {restitution:.15, friction:.4, frictionAir:.009});
    body.level = level; body.born = this.time;
    this.balls.push(body); Matter.Composite.add(this.engine.world, body);
    return body;
  }
  drop() {
    if (this.status !== 'playing' || this.time - this.lastDrop < 650) return false;
    this.setAim(this.aim);
    this.add(this.current, this.aim, 46);
    this.lastDrop = this.time; this.current = this.next; this.next = this.pick();
    this.setAim(this.aim); this.onChange?.(this); return true;
  }
  step(dt=1000/60) {
    if (this.status !== 'playing') return;
    this.time += dt;
    Matter.Engine.update(this.engine, dt);
    const used = new Set();
    for (const {bodyA:a, bodyB:b} of this.queue) {
      if (a.isStatic || b.isStatic || a.level !== b.level || a.level >= 6 || used.has(a) || used.has(b)) continue;
      if (!this.balls.includes(a) || !this.balls.includes(b)) continue;
      used.add(a); used.add(b);
      const level = a.level + 1, r = LiberationGame.radii[level];
      const x = Math.max(14+r, Math.min(406-r, (a.position.x+b.position.x)/2));
      const y = Math.min(570-r, (a.position.y+b.position.y)/2);
      Matter.Composite.remove(this.engine.world, [a,b]);
      this.balls = this.balls.filter(ball => ball !== a && ball !== b);
      this.add(level, x, y); this.score += 2 ** level * 10;
      if (level === 6) this.status = 'won';
      this.onChange?.(this);
      if (this.status === 'won') break;
    }
    this.queue = [];
    if (this.status !== 'playing') return;
    const overflowing = this.balls.some(b => this.time-b.born > 2200 && b.position.y-b.circleRadius < 100);
    this.danger = overflowing ? this.danger + dt : 0;
    if (this.danger >= 1800) { this.status = 'lost'; this.onChange?.(this); }
  }
}
window.LiberationGame = LiberationGame;
