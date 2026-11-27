// Motor HISTORIAS POR CHAT — uso: node chat/render.cjs guion.json salida_dir [--frames-only|--preview t1,t2]
// Genera salida_dir/<slug>.mp4 (1080x1920, 30 fps) con sonidos sintetizados (sonidos.py).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn, execFileSync } = require('child_process');

(async () => {
  const [guionPath, outDir] = process.argv.slice(2);
  const preview = process.argv.includes('--preview') ? process.argv[process.argv.indexOf('--preview') + 1].split(',').map(Number) : null;
  const G = JSON.parse(fs.readFileSync(guionPath, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const FPS = 30;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'chat.html'));
  await page.evaluate(() => document.fonts.ready);
  const info = await page.evaluate(g => window.setup(g), G);
  console.log('duración', info.dur.toFixed(2), 's,', G.mensajes.length, 'mensajes');
  fs.writeFileSync(path.join(outDir, 'eventos.json'), JSON.stringify({ ...info, musica: !!G.musica }));
  if (preview) {
    for (const t of preview) { await page.evaluate(t => window.draw(t), t); await page.screenshot({ path: path.join(outDir, `preview_${t}.png`) }); }
    await browser.close(); return;
  }
  const wav = path.join(outDir, 'sonido.wav');
  execFileSync('python3', [path.join(__dirname, 'sonidos.py'), path.join(outDir, 'eventos.json'), wav], { stdio: 'inherit' });
  const mp4 = path.join(outDir, (G.slug || 'chat') + '.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-i', wav,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.ceil(info.dur * FPS);
  for (let f = 0; f < N; f++) {
    await page.evaluate(t => window.draw(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`frame ${f}/${N}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('OK', mp4);
})();
