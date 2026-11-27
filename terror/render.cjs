// node render.cjs <ep> [--snap t1,t2,...] [--out dir] [--fps 30]
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const args = process.argv.slice(2); const ep = args[0] || 'index';
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const root = __dirname, out = path.resolve(opt('out', path.join(root, 'out'))); fs.mkdirSync(out, { recursive: true });
const types = { '.html': 'text/html', '.js': 'text/javascript', '.ttf': 'font/ttf', '.json': 'application/json' };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0);
(async () => {
  const port = srv.address().port;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', m => console.log('[page]', m.text())); p.on('pageerror', e => console.log('[err]', e.message));
  await p.goto(`http://localhost:${port}/index.html?ep=${ep}`); await p.waitForFunction('window.ready === true', null, { timeout: 120000 });
  await p.evaluate(() => document.fonts.ready);
  const dur = await p.evaluate('window.DUR'); fs.writeFileSync(path.join(out, 'timeline.json'), JSON.stringify(await p.evaluate('({dur: window.DUR, events: window.EVENTS})')));
  const snap = opt('snap');
  if (snap) { for (const t of snap.split(',').map(Number)) { const t0 = Date.now(); await p.evaluate(t => window.renderAt(t), t); await p.screenshot({ path: path.join(out, `snap_${t}.jpg`), type: 'jpeg', quality: 85 }); console.log('snap', t, Date.now() - t0, 'ms'); } }
  else {
    const fps = +opt('fps', 30), n = Math.round(dur * fps), from = +opt('from', 0), to = +opt('to', n);
    const fdir = path.join(out, 'frames'); fs.mkdirSync(fdir, { recursive: true });
    const t0 = Date.now();
    for (let i = from; i < to; i++) { await p.evaluate(t => window.renderAt(t), i / fps); await p.screenshot({ path: path.join(fdir, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 }); if (i % 30 === 0) console.log('frame', i, '/', n, ((Date.now() - t0) / (i - from + 1)).toFixed(0), 'ms/f'); }
  }
  await b.close(); srv.close();
})();
