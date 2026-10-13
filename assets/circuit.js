/* Horn – animierter Installationsplan.
   Ein Unterverteiler (UV) speist mehrere Stromkreise; jeder Stromkreis ist eine
   Leitung mit Abzweigen zu Verbrauchern (Leuchte, Steckdose, Schalter, Motor).
   Gelbe Impulse laufen vom Verteiler zum Verbraucher, Leuchten gehen kurz an.
   Usage: hornCircuit(canvas, {region:(W,H)=>({x0,y0,x1,y1}), circuits:4, alpha:1}) */
(function(global){
  'use strict';
  var ACC = '251,186,0';

  function rng(seed){
    return function(){
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function hornCircuit(canvas, opts){
    opts = opts || {};
    var ctx = canvas.getContext('2d');
    var reduce = global.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var W = 0, H = 0, dpr = 1, g = 24, still = null, sctx = null;
    var board = null, circuits = [], consumers = [], pulses = [];
    var raf = 0, last = 0, nextSpawn = 0, alive = true;
    var A = opts.alpha == null ? 1 : opts.alpha;
    var FONT = '"JB", ui-monospace, Menlo, monospace';

    function snap(v){ return Math.round(v / g) * g; }

    function region(){
      if (opts.region) return opts.region(W, H);
      return { x0: W * 0.5, y0: H * 0.12, x1: W - 48, y1: H * 0.9 };
    }

    /* ---------- build geometry ---------- */
    function layout(){
      var r = canvas.getBoundingClientRect();
      W = Math.max(1, r.width); H = Math.max(1, r.height);
      dpr = Math.min(2, global.devicePixelRatio || 1);
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      var reg = region();
      g = opts.grid ? opts.grid(W, H) : Math.max(16, Math.min(28, Math.round(Math.min(W, H) / 30)));
      var R = rng(opts.seed || 1993);

      var nC = opts.circuits ? opts.circuits(W, H) : 4;
      var bw = g * (nC + 1), bh = g * (nC >= 4 ? 5 : 4);
      var bx = snap(reg.x1 - bw), by = snap(reg.y1 - bh);
      board = { x: bx, y: by, w: bw, h: bh, leds: [] };

      var top = snap(reg.y0 + g), bottom = by - g * 2;
      var span = Math.max(g * 2, bottom - top);
      var gap = span / Math.max(1, nC - 1);
      var compact = W < 600 || g < 17;
      var labels = compact ? ['F1', 'F2', 'F3', 'F4', 'F5']
        : ['F1 · NYM-J 3×1,5 mm²', 'F2 · NYM-J 3×2,5 mm²', 'F3 · NYM-J 5×2,5 mm²', 'F4 · KNX J-Y(St)Y 2×2×0,8', 'F5 · NYM-J 3×1,5 mm²'];
      ctx.font = Math.round(g * 0.42) + 'px ' + FONT;
      var kinds = ['lamp', 'socket', 'lamp', 'switch', 'lamp', 'motor', 'socket', 'lamp'];
      circuits = []; consumers = [];

      for (var i = 0; i < nC; i++){
        // lowest trunk uses the leftmost port, higher trunks move right -> no crossings
        var px = bx + g * (i + 1);
        var ty = nC === 1 ? top : snap(bottom - gap * i);
        var x0 = snap(reg.x0 + R() * g * 3);
        var label = labels[i % labels.length];
        var c = { i: i, px: px, py: by, ty: ty, x0: x0, label: label, drops: [] };
        var start = snap(x0 + ctx.measureText(label).width + g * 1.2);
        var room = px - g * 2 - start;
        var n = Math.max(1, Math.min(4, Math.floor(room / (g * 4))));
        for (var k = 0; k < n; k++){
          var cx = snap(start + room * ((k + 0.5) / n) + (R() - 0.5) * g * 0.8);
          if (cx >= px - g || cx <= start - g) continue;
          var up = (k + i) % 2 === 0;
          var stub = g * (R() > 0.55 ? 2 : 1.2);
          var maxStub = gap * 0.36;
          if (stub > maxStub) stub = Math.max(g * 0.9, maxStub);
          var cy = ty + (up ? -stub : stub);
          if (!up && i === 0 && cy > by - g) { up = true; cy = ty - stub; }
          var clash = function(y){ return consumers.some(function(o){ return Math.abs(o.x - cx) < g * 1.8 && Math.abs(o.y - y) < g * 1.8; }); };
          if (clash(cy)) { cy = ty + (up ? stub : -stub); if (clash(cy) || (i === 0 && cy > by - g)) continue; }
          var kind = kinds[(i * 3 + k) % kinds.length];
          var con = { x: cx, y: cy, ty: ty, kind: kind, lit: 0, circuit: c, r: g * 0.42 };
          var reach = kind === 'socket' ? 0 : (kind === 'switch' ? con.r * 0.38 : con.r);
          con.end = cy + (cy < ty ? reach : -reach);
          con.path = [[px, by], [px, ty], [cx, ty], [cx, con.end]];
          con.len = pathLen(con.path);
          c.drops.push(con); consumers.push(con);
        }
        c.endX = x0;
        circuits.push(c);
        board.leds.push({ x: px, y: by + g * 0.9, on: 0 });
      }
      drawStill();
      pulses = [];
      if (reduce){
        consumers.forEach(function(c, j){ if (c.kind === 'lamp' && j % 2 === 0) c.lit = 0.8; });
      }
      paint(0);
    }

    function pathLen(p){
      var L = 0;
      for (var i = 1; i < p.length; i++) L += Math.abs(p[i][0] - p[i-1][0]) + Math.abs(p[i][1] - p[i-1][1]);
      return L;
    }
    function pointAt(p, d){
      for (var i = 1; i < p.length; i++){
        var seg = Math.abs(p[i][0] - p[i-1][0]) + Math.abs(p[i][1] - p[i-1][1]);
        if (d <= seg){
          var t = seg ? d / seg : 0;
          return [p[i-1][0] + (p[i][0] - p[i-1][0]) * t, p[i-1][1] + (p[i][1] - p[i-1][1]) * t];
        }
        d -= seg;
      }
      return p[p.length - 1];
    }

    /* ---------- static layer ---------- */
    function drawStill(){
      still = still || document.createElement('canvas');
      still.width = canvas.width; still.height = canvas.height;
      sctx = still.getContext('2d');
      var c = sctx;
      c.setTransform(dpr, 0, 0, dpr, 0, 0);
      c.clearRect(0, 0, W, H);

      // drawing grid (dots)
      c.fillStyle = 'rgba(255,255,255,' + (0.075 * A) + ')';
      for (var x = g; x < W; x += g) for (var y = g; y < H; y += g) c.fillRect(x - 0.6, y - 0.6, 1.2, 1.2);

      // warm glow behind the board
      var gr = c.createRadialGradient(board.x + board.w / 2, board.y + board.h / 2, 0, board.x + board.w / 2, board.y + board.h / 2, g * 14);
      gr.addColorStop(0, 'rgba(' + ACC + ',' + (0.10 * A) + ')');
      gr.addColorStop(1, 'rgba(' + ACC + ',0)');
      c.fillStyle = gr; c.fillRect(0, 0, W, H);

      c.lineCap = 'butt'; c.lineJoin = 'miter';
      var wire = 'rgba(255,255,255,' + (0.22 * A) + ')';
      var faint = 'rgba(255,255,255,' + (0.34 * A) + ')';

      // circuits
      circuits.forEach(function(ci){
        c.strokeStyle = wire; c.lineWidth = 1.25;
        c.beginPath();
        c.moveTo(ci.px, ci.py); c.lineTo(ci.px, ci.ty); c.lineTo(ci.endX, ci.ty);
        c.stroke();
        // trunk end tick
        c.beginPath(); c.moveTo(ci.endX, ci.ty - g * 0.25); c.lineTo(ci.endX, ci.ty + g * 0.25); c.stroke();
        ci.drops.forEach(function(d){
          c.beginPath(); c.moveTo(d.x, d.ty); c.lineTo(d.x, d.end); c.stroke();
          c.fillStyle = faint;
          c.beginPath(); c.arc(d.x, d.ty, 2.2, 0, Math.PI * 2); c.fill();
          symbol(c, d, faint, false);
        });
        // cable label on the reserved stretch at the trunk end
        c.font = Math.round(g * 0.42) + 'px ' + FONT;
        c.fillStyle = 'rgba(255,255,255,' + (0.34 * A) + ')';
        c.textBaseline = 'bottom';
        var lx = ci.endX + g * 0.5;
        c.fillText(ci.label, lx, ci.ty - 5);
      });

      // distribution board
      var b = board;
      c.strokeStyle = 'rgba(255,255,255,' + (0.5 * A) + ')'; c.lineWidth = 1.5;
      c.strokeRect(b.x + 0.5, b.y + 0.5, b.w, b.h);
      c.strokeStyle = 'rgba(255,255,255,' + (0.22 * A) + ')'; c.lineWidth = 1;
      c.beginPath(); c.moveTo(b.x + g * 0.4, b.y + g * 1.6); c.lineTo(b.x + b.w - g * 0.4, b.y + g * 1.6); c.stroke(); // DIN rail
      // breakers
      for (var i = 0; i < circuits.length; i++){
        var bx = circuits[i].px - g * 0.22;
        c.strokeStyle = 'rgba(255,255,255,' + (0.42 * A) + ')';
        c.strokeRect(bx + 0.5, b.y + g * 1.15 + 0.5, g * 0.44, g * 0.9);
        c.beginPath(); c.moveTo(bx + g * 0.22, b.y + g * 1.3); c.lineTo(bx + g * 0.22, b.y + g * 1.55); c.stroke();
      }
      // RCD + main switch hints
      c.strokeStyle = 'rgba(255,255,255,' + (0.3 * A) + ')';
      c.strokeRect(b.x + g * 0.6 + 0.5, b.y + g * 2.6 + 0.5, b.w - g * 1.2, g * 0.9);
      c.font = Math.round(g * 0.38) + 'px ' + FONT;
      c.fillStyle = 'rgba(255,255,255,' + (0.38 * A) + ')';
      c.textBaseline = 'middle';
      if (c.measureText('RCD 40/0,03 A').width < b.w - g * 1.6) c.fillText('RCD 40/0,03 A', b.x + g * 0.8, b.y + g * 3.05);
      else c.fillText('RCD', b.x + g * 0.8, b.y + g * 3.05);
      // feed from below: 5 conductors L1 L2 L3 N PE
      var cols = ['rgba(139,90,43,', 'rgba(170,170,170,', 'rgba(120,120,120,', 'rgba(47,111,208,', 'rgba(132,186,52,'];
      for (var j = 0; j < 5; j++){
        var fx = b.x + b.w / 2 + (j - 2) * g * 0.28;
        c.strokeStyle = cols[j] + (0.55 * A) + ')'; c.lineWidth = 1.4;
        c.beginPath(); c.moveTo(fx, b.y + b.h); c.lineTo(fx, Math.min(H, b.y + b.h + g * 2.2)); c.stroke();
      }
      c.font = Math.round(g * 0.42) + 'px ' + FONT;
      c.fillStyle = 'rgba(255,255,255,' + (0.42 * A) + ')';
      c.textBaseline = 'bottom';
      c.fillText('UV 1', b.x, b.y - 6);
      c.textBaseline = 'top';
      c.fillStyle = 'rgba(255,255,255,' + (0.28 * A) + ')';
      var feed = W < 600 ? '400 V' : 'L1 L2 L3 N PE · 400 V';
      c.textAlign = 'right';
      c.fillText(feed, b.x + b.w / 2 - g * 1.0, b.y + b.h + g * 0.6);
      c.textAlign = 'start';
    }

    function symbol(c, d, color, lit){
      var r = d.r, x = d.x, y = d.y;
      c.strokeStyle = color; c.lineWidth = lit ? 1.6 : 1.25;
      if (d.kind === 'lamp'){
        c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.stroke();
        var k = r * 0.7071;
        c.beginPath(); c.moveTo(x - k, y - k); c.lineTo(x + k, y + k); c.moveTo(x + k, y - k); c.lineTo(x - k, y + k); c.stroke();
      } else if (d.kind === 'socket'){
        // flat side faces the wire, half circle points away from the trunk
        var away = d.y < d.ty ? -1 : 1;
        c.beginPath(); c.arc(x, y, r, away > 0 ? 0 : Math.PI, away > 0 ? Math.PI : Math.PI * 2, false); c.stroke();
        c.beginPath(); c.moveTo(x - r * 1.2, y); c.lineTo(x + r * 1.2, y); c.stroke();
      } else if (d.kind === 'switch'){
        c.beginPath(); c.arc(x, y, r * 0.38, 0, Math.PI * 2); c.stroke();
        var a = d.y < d.ty ? -Math.PI / 4 : Math.PI / 4;
        var ex = x + Math.cos(a) * r * 1.5, ey = y + Math.sin(a) * r * 1.5;
        c.beginPath(); c.moveTo(x + Math.cos(a) * r * 0.38, y + Math.sin(a) * r * 0.38); c.lineTo(ex, ey); c.stroke();
        c.beginPath(); c.moveTo(ex, ey); c.lineTo(ex + Math.cos(a + Math.PI / 2) * r * 0.5, ey + Math.sin(a + Math.PI / 2) * r * 0.5); c.stroke();
      } else {
        c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.stroke();
        c.font = Math.round(r * 1.15) + 'px ' + FONT;
        c.fillStyle = color; c.textAlign = 'center'; c.textBaseline = 'middle';
        c.fillText('M', x, y + 0.5);
        c.textAlign = 'start';
      }
    }

    /* ---------- frame ---------- */
    function spawn(){
      if (!consumers.length) return;
      var con = consumers[Math.floor(Math.random() * consumers.length)];
      pulses.push({ con: con, d: 0, speed: g * (10 + Math.random() * 5) });
      board.leds[con.circuit.i].on = 1;
    }

    function paint(dt){
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      if (still) ctx.drawImage(still, 0, 0);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // breaker LEDs
      board.leds.forEach(function(l){
        if (l.on <= 0.01) return;
        ctx.fillStyle = 'rgba(' + ACC + ',' + (l.on * A) + ')';
        ctx.fillRect(l.x - 1.5, l.y - 1.5, 3, 3);
        l.on = Math.max(0, l.on - dt * 1.2);
      });

      // lit consumers
      consumers.forEach(function(con){
        if (con.lit <= 0.01) return;
        var a = con.lit * A;
        if (con.kind === 'lamp'){
          var gr = ctx.createRadialGradient(con.x, con.y, 0, con.x, con.y, con.r * 5);
          gr.addColorStop(0, 'rgba(' + ACC + ',' + (0.35 * a) + ')');
          gr.addColorStop(1, 'rgba(' + ACC + ',0)');
          ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(con.x, con.y, con.r * 5, 0, Math.PI * 2); ctx.fill();
          ctx.fillStyle = 'rgba(' + ACC + ',' + (0.22 * a) + ')';
          ctx.beginPath(); ctx.arc(con.x, con.y, con.r, 0, Math.PI * 2); ctx.fill();
        }
        symbol(ctx, con, 'rgba(' + ACC + ',' + a + ')', true);
        if (!reduce) con.lit = Math.max(0, con.lit - dt * (con.kind === 'lamp' ? 0.45 : 0.9));
      });

      // pulses
      ctx.lineCap = 'round';
      for (var i = pulses.length - 1; i >= 0; i--){
        var p = pulses[i];
        p.d += p.speed * dt;
        var tail = g * 2.6, steps = 7;
        ctx.shadowColor = 'rgba(' + ACC + ',0.9)'; ctx.shadowBlur = 8;
        for (var s = 0; s < steps; s++){
          var d1 = p.d - tail * (s / steps), d0 = p.d - tail * ((s + 1) / steps);
          if (d1 < 0) break;
          var q0 = pointAt(p.con.path, Math.max(0, d0)), q1 = pointAt(p.con.path, Math.min(p.con.len, d1));
          ctx.strokeStyle = 'rgba(' + ACC + ',' + ((1 - s / steps) * A) + ')';
          ctx.lineWidth = 2;
          ctx.beginPath(); ctx.moveTo(q0[0], q0[1]); ctx.lineTo(q1[0], q1[1]); ctx.stroke();
        }
        ctx.shadowBlur = 0;
        if (p.d >= p.con.len && !p.hit){ p.hit = true; p.con.lit = 1; }
        if (p.d - tail >= p.con.len) pulses.splice(i, 1);
      }
      ctx.lineCap = 'butt';
    }

    function frame(t){
      if (!alive) return;
      raf = requestAnimationFrame(frame);
      if (document.hidden) { last = t; return; }
      var dt = last ? Math.min(0.05, (t - last) / 1000) : 0;
      last = t;
      if (t >= nextSpawn && pulses.length < (opts.maxPulses || 5)){
        spawn();
        nextSpawn = t + 380 + Math.random() * 900;
      }
      paint(dt);
    }

    var rt = 0;
    function onResize(){ clearTimeout(rt); rt = setTimeout(layout, 120); }

    layout();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ drawStill(); if (reduce) paint(0); });
    global.addEventListener('resize', onResize);
    if (!reduce) raf = requestAnimationFrame(frame);
    return { destroy: function(){ alive = false; cancelAnimationFrame(raf); global.removeEventListener('resize', onResize); } };
  }

  global.hornCircuit = hornCircuit;
})(window);
