// Exporta un episodio a MP4 vertical: fotogramas deterministas (Playwright) + voz + música + efectos + subtítulos.
// uso: node scripts/export.cjs ep000 [--from 0] [--to 60] [--rw 720 --rh 1280] [--out out/ep000]
const { chromium } = require('playwright')
const { spawn, execFileSync } = require('child_process')
const fs = require('fs')
const path = require('path')

const args = process.argv.slice(2)
const ep = args[0] || 'ep000'
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d }
const FPS = 30, OW = 1080, OH = 1920
const RW = +opt('rw', 720), RH = +opt('rh', 1280)
const from = +opt('from', 0)
const out = path.resolve(opt('out', `out/${ep}`))
const base = opt('url', 'http://localhost:5173')
fs.mkdirSync(out, { recursive: true })

function assTime(t) {
  t = Math.max(0, t - from)
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), s = t % 60
  return `${h}:${String(m).padStart(2, '0')}:${s.toFixed(2).padStart(5, '0')}`
}

function buildAss(info, to) {
  const head = `[Script Info]
ScriptType: v4.00+
PlayResX: ${OW}
PlayResY: ${OH}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Lilita One,112,&H00FFFFFF,&H0000D5FF,&H00201810,&H64000000,0,0,0,0,100,100,1,0,1,8,3,2,60,60,400,1
Style: Tag,Fredoka SemiBold,46,&H00FFFFFF,&H00FFFFFF,&H003D7AFF,&H00000000,0,0,0,0,100,100,2,0,3,14,0,8,60,60,150,1
Style: Big,Lilita One,150,&H003D8AFF,&H00FFFFFF,&H00FFFFFF,&H64000000,0,0,0,0,100,100,3,0,1,10,4,5,40,40,0,1
Style: Mid,Lilita One,78,&H00FFFFFF,&H00FFFFFF,&H00201810,&H64000000,0,0,0,0,100,100,2,0,1,7,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`
  const ev = []
  for (const l of info.lines) {
    // chunks of up to 4 words / 24 chars, karaoke highlight word by word
    const words = l.words
    let chunk = []
    const flush = () => {
      if (!chunk.length) return
      const a = l.at + chunk[0].t - 0.05, b = l.at + chunk[chunk.length - 1].t + chunk[chunk.length - 1].d + 0.12
      // original spelling with punctuation from the text
      let txt = '{\\fad(60,60)\\t(0,120,\\fscx108\\fscy108)\\t(120,220,\\fscx100\\fscy100)}'
      chunk.forEach((w, i) => {
        const dur = Math.round(((i < chunk.length - 1 ? chunk[i + 1].t : w.t + w.d) - w.t) * 100)
        txt += `{\\kf${Math.max(5, dur)}}${w.disp}${i < chunk.length - 1 ? ' ' : ''}`
      })
      ev.push(`Dialogue: 0,${assTime(a)},${assTime(Math.min(b, to))},Sub,,0,0,0,,${txt}`)
      chunk = []
    }
    // map spoken words to display tokens (keep ¡! punctuation)
    const tokens = l.text.split(/\s+/)
    let ti = 0
    for (const w of words) {
      const norm = (x) => x.normalize('NFD').replace(/[^\p{L}\p{N}]/gu, '').toLowerCase()
      while (ti < tokens.length && norm(tokens[ti]) !== norm(w.w) && !norm(tokens[ti]).startsWith(norm(w.w))) ti++
      const disp = ti < tokens.length ? tokens[ti++] : w.w
      chunk.push({ ...w, disp: disp.toUpperCase() })
      const chars = chunk.reduce((s, c) => s + c.disp.length + 1, 0)
      if (chunk.length >= 4 || chars > 20 || /[.!?…,]$/.test(disp)) flush()
    }
    flush()
  }
  if (ep === 'ep000') {
    ev.push(`Dialogue: 1,${assTime(25.2)},${assTime(40.2)},Tag,,0,0,0,,{\\fad(200,200)}SIMULACIÓN · ASÍ SERÁ`)
    ev.push(`Dialogue: 1,${assTime(41.0)},${assTime(50.2)},Tag,,0,0,0,,{\\fad(200,200)}2 ACTUALIZACIONES AL DÍA`)
    ev.push(`Dialogue: 2,${assTime(57.2)},${assTime(to)},Big,,0,0,0,,{\\an5\\pos(540,700)\\fad(250,0)\\t(0,300,\\fscx110\\fscy110)\\t(300,500,\\fscx100\\fscy100)}PIZZAVILLE`)
    ev.push(`Dialogue: 2,${assTime(57.7)},${assTime(to)},Mid,,0,0,0,,{\\an5\\pos(540,850)\\fad(250,0)}1 HABITANTE · 1 CASA`)
    ev.push(`Dialogue: 2,${assTime(58.2)},${assTime(to)},Mid,,0,0,0,,{\\an5\\pos(540,1010)\\fad(250,0)\\c&H004DD3FF&}COMENTA TU PAÍS\\NPARA UNIRTE`)
  }
  return head + ev.join('\n') + '\n'
}

;(async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] })
  const p = await b.newPage({ viewport: { width: RW, height: RH } })
  p.on('pageerror', (e) => console.log('[pageerror]', e.message))
  await p.goto(`${base}/?record=1&episode=${ep}`)
  await p.waitForFunction(() => window.__pv && window.__pv.info, null, { timeout: 180000, polling: 500 })
  await p.evaluate(() => window.__pv.renderAt(0))
  await p.evaluate(() => window.__pv.ready())
  const info = await p.evaluate(() => window.__pv.info())
  const to = Math.min(+opt('to', info.duration), info.duration)
  fs.writeFileSync(path.join(out, 'info.json'), JSON.stringify(info, null, 1))
  console.log('lines with audio:', info.lines.filter((l) => l.hasAudio).length, '/', info.lines.length)

  // ---------------- video frames → ffmpeg
  const silent = path.join(out, 'video_silent.mp4')
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-vf', `scale=${OW}:${OH}:flags=lanczos`, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', silent], { stdio: ['pipe', 'inherit', 'inherit'] })
  const n0 = Math.round(from * FPS), n1 = Math.round(to * FPS)
  const t0 = Date.now()
  for (let f = n0; f < n1; f++) {
    const data = await p.evaluate((t) => { window.__pv.renderAt(t); return document.querySelector('canvas').toDataURL('image/jpeg', 0.93) }, f / FPS)
    const buf = Buffer.from(data.slice(data.indexOf(',') + 1), 'base64')
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r))
    if ((f - n0) % 30 === 0) {
      const el = (Date.now() - t0) / 1000, done = f - n0 + 1
      console.log(`frame ${f}/${n1}  ${(el / done).toFixed(2)} s/f  eta ${Math.round((el / done) * (n1 - f) / 60)} min`)
    }
  }
  ff.stdin.end()
  await new Promise((r) => ff.on('close', r))
  await b.close()

  // ---------------- subtitles
  const ass = path.join(out, 'subs.ass')
  fs.writeFileSync(ass, buildAss(info, to))

  // ---------------- audio
  const voices = info.lines.filter((l) => l.hasAudio).map((l) => ({ file: path.resolve(`public/voz/${ep}/${l.id}.mp3`), at: l.at - from }))
  const cues = { duration: to - from, voices, sfx: info.sfx.map((s) => ({ ...s, at: s.at - from })) }
  fs.writeFileSync(path.join(out, 'cues.json'), JSON.stringify(cues, null, 1))
  const wav = path.join(out, 'audio.wav')
  execFileSync('python3', [path.resolve('scripts/audio.py'), path.join(out, 'cues.json'), wav], { stdio: 'inherit' })

  // ---------------- final mux (subtitles shifted if exporting a range)
  const final = path.join(out, `${ep}.mp4`)
  const fontsdir = path.resolve('scripts/fonts')
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', silent, '-i', wav, '-vf', `setpts=PTS-STARTPTS,ass=${ass}:fontsdir=${fontsdir}`,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', final], { stdio: 'inherit' })
  console.log('OK', final, ((Date.now() - t0) / 60000).toFixed(1), 'min')
})()
