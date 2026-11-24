// Renders escena.html to video (or stills). uso:
//   node render.cjs video <timeline.json> <audio.mp3> <out.mp4> '{"fx":true,"subs":"A","highlight":true}' [ambient.wav]
//   node render.cjs still <timeline.json> <t> <out.jpg> '{"subs":"B"}'
const { chromium } = require('playwright')
const { spawn } = require('child_process')
const fs = require('fs'), path = require('path')
const [mode, tlPath, a3, out, optJson, amb] = process.argv.slice(2)
;(async () => {
  const tl = JSON.parse(fs.readFileSync(tlPath, 'utf8'))
  const opt = JSON.parse(optJson || '{}')
  const b = await chromium.launch()
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } })
  await p.goto('file://' + path.resolve(__dirname, process.env.ESCENA || 'escena.html'))
  await p.evaluate(() => Promise.all([document.fonts.load('700 58px Inter'), document.fonts.load('italic 700 56px Inter'), document.fonts.load('600 50px Inter')]))
  await p.evaluate(([tl, opt]) => setup(tl, opt), [tl, opt])
  if (mode === 'still') {
    const d = await p.evaluate((t) => frame(t), +a3)
    fs.writeFileSync(out, Buffer.from(d, 'base64')); await b.close(); return
  }
  const n = Math.round(tl.dur * tl.fps)
  const inputs = ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(tl.fps), '-c:v', 'mjpeg', '-i', '-',
    '-itsoffset', String(tl.lead), '-i', a3]
  let filt = '[1:a]apad[v]'
  if (amb) { inputs.push('-i', amb); filt = '[1:a]apad[v0];[v0][2:a]amix=inputs=2:duration=first:normalize=0[v]' }
  const ff = spawn('ffmpeg', [...inputs, '-filter_complex', filt, '-map', '0:v', '-map', '[v]', '-t', String(tl.dur),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] })
  for (let i = 0; i < n; i++) {
    const d = await p.evaluate((t) => frame(t), i / tl.fps)
    if (!ff.stdin.write(Buffer.from(d, 'base64'))) await new Promise((r) => ff.stdin.once('drain', r))
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r)); await b.close()
  console.log('ok', out, n, 'frames')
})()
