// Motor HISTORIAS POR CHAT — uso: node chat/render.cjs guion.json salida_dir [--frames-only|--preview t1,t2]
// Genera salida_dir/<slug>.mp4 (1080x1920, 30 fps) con sonidos sintetizados (sonidos.py).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn, execFileSync } = require('child_process');

const BG = '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=brightness=-0.04[bg];';
const fondo = G => path.resolve(path.join(__dirname, 'fondos', (G.fondo || 'bola_musical') + '.mp4'));
(async () => {
  const [guionPath, outDir] = process.argv.slice(2);
  const preview = process.argv.includes('--preview') ? process.argv[process.argv.indexOf('--preview') + 1].split(',').map(Number) : null;
  const G = JSON.parse(fs.readFileSync(guionPath, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const FPS = 30;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  const IMSG = G.estilo === 'imsg';
  await page.goto('file://' + path.join(__dirname, IMSG ? 'imsg.html' : 'chat.html'));
  await page.evaluate(() => document.fonts.ready);
  const vozDir = path.resolve(path.join(__dirname, 'voz', G.slug || ''));
  let voces = null;
  if (G.voces) {
    const vj = path.join(vozDir, 'voces.json');
    if (!fs.existsSync(vj)) { console.error('Faltan las voces:', vj, '(se generan con GitHub Actions al subir el guion)'); process.exit(3); }
    voces = JSON.parse(fs.readFileSync(vj, 'utf8'));
  }
  const info = await page.evaluate(([g, v]) => window.setup(g, { voces: v }), [G, voces]);
  console.log('duración', info.dur.toFixed(2), 's,', G.mensajes.length, 'mensajes');
  fs.writeFileSync(path.join(outDir, 'eventos.json'), JSON.stringify({ ...info, musica: !!G.musica, voces, vozDir }));
  if (preview) {
    for (const t of preview) { await page.evaluate(t => window.draw(t), t); await page.screenshot({ path: path.join(outDir, `preview_${t}.png`), omitBackground: IMSG });
      if (IMSG) execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', String(t + 6), '-i', fondo(G), '-i', path.join(outDir, `preview_${t}.png`), '-filter_complex', BG + '[bg][1:v]overlay', '-frames:v', '1', path.join(outDir, `preview_${t}_fondo.png`)]); }
    await browser.close(); return;
  }
  const wav = path.join(outDir, 'sonido.wav');
  execFileSync('python3', [path.join(__dirname, 'sonidos.py'), path.join(outDir, 'eventos.json'), wav], { stdio: 'inherit' });
  const mp4 = path.join(outDir, (G.slug || 'chat') + '.mp4');
  const ff = spawn('ffmpeg', IMSG ? ['-y', '-loglevel', 'error', '-stream_loop', '-1', '-ss', '6', '-i', fondo(G), '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', '-i', wav,
    '-filter_complex', BG + '[bg][1:v]overlay=shortest=1[v]', '-map', '[v]', '-map', '2:a',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-maxrate', '7M', '-bufsize', '14M', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', mp4] : ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-i', wav,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.ceil(info.dur * FPS);
  for (let f = 0; f < N; f++) {
    await page.evaluate(t => window.draw(t), f / FPS);
    const buf = IMSG ? await page.screenshot({ type: 'png', omitBackground: true }) : await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`frame ${f}/${N}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('OK', mp4);
})();
