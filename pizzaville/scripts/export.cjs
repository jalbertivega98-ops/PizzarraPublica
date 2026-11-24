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
Style: SubBox,Inter ExtraBold,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,5,0,5,60,60,0,1
Style: Box,Inter ExtraBold,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,5,0,5,40,40,0,1
Style: Mid,Lilita One,78,&H00FFFFFF,&H00FFFFFF,&H00201810,&H64000000,0,0,0,0,100,100,2,0,1,7,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`
  const ev = [], subs = [], tags = []
  if (info.subStyle === 'box') {
    // short italic chunks, the key word on a red box (reels style)
    const norm = (x) => x.normalize('NFD').replace(/[^\p{L}\p{N}]/gu, '').toLowerCase()
    for (const l of info.lines) {
      const tokens = l.text.replace(/[«»]/g, '').split(/\s+/)
      let ti = 0, chunk = []
      const flush = () => {
        if (!chunk.length) return
        const a = l.at + chunk[0].t - 0.04, b = l.at + chunk[chunk.length - 1].t + chunk[chunk.length - 1].d + 0.1
        let key = -1, best = 3
        chunk.forEach((c, i) => { const n = norm(c.disp).length; if (n > best) { best = n; key = i } })
        // toon episodes: colour by speaker (T = Dani's thoughts, D = Dani out loud, H = her)
        const keyC = l.kind === 'T' ? '&HB0399A&' : l.kind === 'H' ? '&HA04FFF&' : l.kind === 'D' ? '&HE07D2E&' : '&H2E2ED6&'
        const fill = l.kind === 'T' ? '{\\1c&H8CF0FF&}' : ''
        const txt = fill + chunk.map((c, i) => (i === key ? `{\\3c${keyC}\\bord17\\1c&HFFFFFF&}${c.disp}{\\3c&H000000&\\bord5}${fill}` : c.disp)).join(' ')
        subs.push({ a, b: Math.min(b, to), txt: `{\\an5\\pos(540,1330)\\fad(40,40)}${txt}` })
        if (l.kind) {
          const who = l.kind === 'T' ? '💭 DANI PIENSA' : l.kind === 'H' ? 'LUCÍA' : 'DANI'
          const c = l.kind === 'T' ? '&H8CF0FF&' : l.kind === 'H' ? '&HC08AFF&' : '&HFFB070&'
          tags.push({ a, b: Math.min(b, to), txt: `{\\an5\\pos(540,1222)\\fs46\\1c${c}\\bord4\\fad(40,40)}${who.replace('💭 ', '')}` })
        }
        chunk = []
      }
      for (const w of l.words) {
        while (ti < tokens.length && norm(tokens[ti]) !== norm(w.w) && !norm(tokens[ti]).startsWith(norm(w.w))) ti++
        const disp = (ti < tokens.length ? tokens[ti++] : w.w).toUpperCase()
        chunk.push({ ...w, disp })
        const chars = chunk.reduce((s, c) => s + c.disp.length + 1, 0)
        if (chunk.length >= 3 || chars > 16 || /[.!?…,]$/.test(disp)) flush()
      }
      flush()
    }
    subs.sort((x, y) => x.a - y.a).forEach((c, i) => {
      const nb = i + 1 < subs.length ? Math.min(c.b, subs[i + 1].a - 0.01) : c.b
      ev.push(`Dialogue: 0,${assTime(c.a)},${assTime(nb)},SubBox,,0,0,0,,${c.txt}`)
    })
    tags.sort((x, y) => x.a - y.a).forEach((c, i) => {
      const nb = i + 1 < tags.length ? Math.min(c.b, tags[i + 1].a - 0.01) : c.b
      ev.push(`Dialogue: 1,${assTime(c.a)},${assTime(nb)},SubBox,,0,0,0,,${c.txt}`)
    })
    if (info.overlays) for (const o of info.overlays) ev.push(`Dialogue: 2,${assTime(o.a)},${assTime(Math.min(o.b, to))},${o.st},,0,0,0,,${o.tx}`)
    return head + ev.join('\n') + '\n'
  }
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
      subs.push({ a, b: Math.min(b, to), txt })
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
  subs.sort((x, y) => x.a - y.a).forEach((c, i) => {
    const nb = i + 1 < subs.length ? Math.min(c.b, subs[i + 1].a - 0.01) : c.b
    ev.push(`Dialogue: 0,${assTime(c.a)},${assTime(nb)},Sub,,0,0,0,,${c.txt}`)
  })
  if (info.overlays) for (const o of info.overlays) ev.push(`Dialogue: 2,${assTime(o.a)},${assTime(Math.min(o.b, to))},${o.st},,0,0,0,,${o.tx}`)
  if (ep === 'ep001') {
    const D = (a, b, st, tx) => ev.push(`Dialogue: 2,${assTime(a)},${assTime(Math.min(b, to))},${st},,0,0,0,,${tx}`)
    D(0, 2.15, 'Mid', '{\\an5\\pos(540,520)\\fad(0,150)}AYER:\\N{\\c&H004DD3FF&\\fs120}1 PERSONA')
    D(2.6, 5.25, 'Mid', '{\\an5\\pos(540,520)\\fad(150,150)\\t(0,250,\\fscx112\\fscy112)\\t(250,450,\\fscx100\\fscy100)}HOY:\\N{\\c&H004DD3FF&\\fs120}62 VECINOS\\N{\\fs70}13 PAÍSES')
    D(34.6, 38.5, 'Mid', '{\\an5\\pos(540,430)\\fad(150,150)}¡NUEVO PAÍS!\\N{\\c&H0039C26B&\\fs110}BRASIL')
    D(38.9, 44.3, 'Big', '{\\an5\\pos(540,300)\\fad(200,150)\\t(0,250,\\fscx112\\fscy112)\\t(250,450,\\fscx100\\fscy100)\\fs150}{\\c&H004DD3FF&}37{\\c&H00FFFFFF&} – {\\c&H00FFE07F&}25\\N{\\fs62\\c&H004DD3FF&}EUROPA {\\c&H00FFFFFF&}· {\\c&H00FFE07F&}AMÉRICA')
    D(42.2, 44.3, 'Mid', '{\\an5\\pos(540,520)\\fad(150,150)}¿OS VAIS A DEJAR GANAR?')
    D(44.6, 49.3, 'Mid', '{\\an5\\pos(540,330)\\fad(200,150)}COMENTA:\\N{\\c&H004DD3FF&}«SOY ANA DE PERÚ,\\NQUIERO UN CASTILLO»')
    D(47.0, 49.3, 'Tag', '{\\fad(150,150)}ETIQUETA A ALGUIEN DE TU PAÍS')
    D(49.6, to, 'Mid', '{\\an5\\pos(540,420)\\fad(200,0)\\t(0,250,\\fscx112\\fscy112)\\t(250,450,\\fscx100\\fscy100)}¿TU CASA AQUÍ?')
    D(52.2, to, 'Big', '{\\an5\\pos(540,700)\\fad(250,0)}PIZZAVILLE')
    D(52.6, to, 'Mid', '{\\an5\\pos(540,850)\\fad(250,0)}EUROPA 37 · 25 AMÉRICA')
  }
  if (ep === 'ep004') {
    const D = (a, b, st, tx) => ev.push(`Dialogue: 2,${assTime(a)},${assTime(Math.min(b, to))},${st},,0,0,0,,${tx}`)
    const POP = '\\t(0,250,\\fscx112\\fscy112)\\t(250,450,\\fscx100\\fscy100)'
    const OUT = '\\bord8\\3c&H00201810&'
    D(0.2, 4.3, 'Mid', `{\\an5\\pos(540,430)\\fad(0,150)${POP}}¿NUNCA HAS COMENTADO?\\N{\\c&H004DD3FF&\\fs110}¡HOY ES TU DÍA!`)
    D(4.4, to, 'Tag', '{\\an8\\pos(540,70)\\fad(200,0)}PUENTE: 0 / 100 PIEDRAS')
    D(6.27, 8.4, 'Big', `{\\an5\\pos(540,380)\\fad(0,150)${POP}\\fs170${OUT}\\c&H003C3CD2&}¡CRAC!`)
    D(15.0, 19.4, 'Mid', `{\\an5\\pos(540,400)\\fad(150,150)${POP}}1 COMENTARIO = 1 PIEDRA\\N{\\c&H004DD3FF&\\fs96}¿PRIMER COMENTARIO?\\N{\\c&H004DD3FF&\\fs120}¡VALE x2!`)
    D(23.1, 25.0, 'Tag', '{\\an8\\pos(540,200)\\fad(150,150)}EMPATE 1–1 · THIAGO CARGA LAS PIEDRAS')
    D(40.6, 46.0, 'Mid', `{\\an5\\pos(540,400)\\fad(150,150)${POP}}7 VECINOS SIN BANDERA\\N{\\c&H004DD3FF&\\fs96}¿DE QUÉ PAÍS SOIS?`)
    D(46.3, 50.2, 'Big', `{\\an5\\pos(540,320)\\fad(200,150)${POP}\\fs150}{\\c&H004DD3FF&}58{\\c&H00FFFFFF&} – {\\c&H00FFE07F&}40\\N{\\fs62\\c&H004DD3FF&}EUROPA {\\c&H00FFFFFF&}· {\\c&H00FFE07F&}AMÉRICA`)
    D(50.4, 55.5, 'Mid', `{\\an5\\pos(540,360)\\fad(200,150)${POP}}COMENTA:\\N{\\fs120\\c&H004DD3FF&}EUROPA {\\c&H00FFFFFF&\\fs80}o {\\fs120\\c&H00FFE07F&}AMÉRICA`)
    D(53.2, 55.5, 'Tag', '{\\an8\\pos(540,200)\\fad(150,150)}CADA AMIGO ETIQUETADO = +1 PIEDRA')
    D(55.7, 58.4, 'Mid', '{\\an5\\pos(540,380)\\fad(200,150)}¿ERES NUEVO? COMENTA:\\N{\\c&H004DD3FF&}«SOY ANA DE PERÚ,\\NQUIERO UN CASTILLO»')
    D(58.5, to, 'Big', `{\\an5\\pos(540,420)\\fad(200,0)${POP}\\fs130}¿TU CASA AQUÍ?`)
    D(61.4, to, 'Mid', '{\\an5\\pos(540,700)\\fad(250,0)}PIZZAVILLE')
    D(61.7, to, 'Mid', '{\\an5\\pos(540,820)\\fad(250,0)\\c&H004DD3FF&}COMENTA Y GANA TU CASA')
  }
  if (ep === 'ep003') {
    const D = (a, b, st, tx) => ev.push(`Dialogue: 2,${assTime(a)},${assTime(Math.min(b, to))},${st},,0,0,0,,${tx}`)
    const POP = '\\t(0,250,\\fscx112\\fscy112)\\t(250,450,\\fscx100\\fscy100)'
    D(0.2, 3.2, 'Mid', `{\\an5\\pos(540,520)\\fad(0,150)${POP}}91 VECINOS\\N{\\c&H004DD3FF&\\fs110}¡Y UN PRESIDENTE!`)
    D(3.4, 8.1, 'Big', `{\\an5\\pos(540,320)\\fad(150,150)${POP}\\fs120\\bord8\\3c&H00201810&\\c&H004DD3FF&}OLIVER 31{\\c&H00FFFFFF&} – {\\c&H00F5A93F&}4 THIAGO\\N{\\fs70\\c&H00FFFFFF&}¡GANA OLIVER!`)
    D(22.1, 24.4, 'Big', `{\\an5\\pos(540,330)\\fad(100,150)${POP}\\fs130\\bord8\\3c&H00201810&\\c&H00B88FFF&}¡ASALTO!`)
    D(24.6, 28.7, 'Mid', `{\\an5\\pos(540,330)\\fad(150,150)${POP}\\c&H0039C26B&}¡LLAMAD AL EJÉRCITO!`)
    D(31.9, 33.4, 'Big', `{\\an5\\pos(540,330)\\fad(150,150)${POP}\\fs120\\bord8\\3c&H00201810&\\c&H004DD3FF&}¡PAZ!`)
    D(33.6, 37.4, 'Tag', '{\\fad(150,150)}QUEDA ESCRITO EN LA HISTORIA DE PIZZAVILLE')
    D(42.6, 45.7, 'Big', `{\\an5\\pos(540,300)\\fad(200,150)${POP}\\fs150}{\\c&H004DD3FF&}51{\\c&H00FFFFFF&} – {\\c&H00FFE07F&}38\\N{\\fs62\\c&H004DD3FF&}EUROPA {\\c&H00FFFFFF&}· {\\c&H00FFE07F&}AMÉRICA`)
    D(45.8, 50.0, 'Mid', `{\\an5\\pos(540,330)\\fad(200,150)${POP}}¿QUÉ HACEMOS CON LA OPOSICIÓN?\\N{\\fs120\\c&H003C3CD2&}MULTA {\\c&H00FFFFFF&\\fs80}o {\\fs120\\c&H006BC239&}PERDÓN`)
    D(48.4, 50.0, 'Tag', '{\\fad(150,150)}COMENTA TU VOTO')
    D(50.3, 52.7, 'Mid', '{\\an5\\pos(540,330)\\fad(200,150)}COMENTA:\\N{\\c&H004DD3FF&}«SOY ANA DE PERÚ,\\NQUIERO UN CASTILLO»')
    D(53.4, 55.0, 'Tag', '{\\fad(150,150)}ETIQUETA A ALGUIEN DE TU PAÍS')
    D(52.8, to, 'Mid', `{\\an5\\pos(540,420)\\fad(200,0)${POP}}¿TU CASA AQUÍ?`)
    D(55.2, to, 'Big', '{\\an5\\pos(540,700)\\fad(250,0)}PIZZAVILLE')
    D(55.5, to, 'Mid', '{\\an5\\pos(540,850)\\fad(250,0)}MULTA o PERDÓN: ¡VOTA!')
  }
  if (ep === 'ep002') {
    const D = (a, b, st, tx) => ev.push(`Dialogue: 2,${assTime(a)},${assTime(Math.min(b, to))},${st},,0,0,0,,${tx}`)
    const POP = '\\t(0,250,\\fscx112\\fscy112)\\t(250,450,\\fscx100\\fscy100)'
    D(0.2, 3.4, 'Mid', `{\\an5\\pos(540,520)\\fad(0,150)${POP}}AYER: 62\\N{\\c&H004DD3FF&\\fs120}HOY: 87 VECINOS\\N{\\fs70}19 PAÍSES`)
    D(12.4, 16.2, 'Big', `{\\an5\\pos(540,330)\\fad(150,150)${POP}\\fs140}ELECCIONES\\N{\\fs80\\bord7\\3c&H00201810&\\c&H004DD3FF&}OLIVER {\\c&H00FFFFFF&}vs {\\c&H00F5A93F&}THIAGO`)
    D(38.6, 44.9, 'Mid', `{\\an5\\pos(540,430)\\fad(150,150)${POP}}¡NUEVOS CONTINENTES!\\N{\\c&H0039C26B&\\fs110}ÁFRICA · ASIA`)
    D(45.5, 48.3, 'Big', `{\\an5\\pos(540,300)\\fad(200,150)${POP}\\fs150}{\\c&H004DD3FF&}49{\\c&H00FFFFFF&} – {\\c&H00FFE07F&}36\\N{\\fs62\\c&H004DD3FF&}EUROPA {\\c&H00FFFFFF&}· {\\c&H00FFE07F&}AMÉRICA`)
    D(48.6, 54.2, 'Mid', `{\\an5\\pos(540,330)\\fad(200,150)${POP}}VOTA EN LOS COMENTARIOS:\\N{\\fs120\\c&H004DD3FF&}OLIVER {\\c&H00FFFFFF&\\fs80}o {\\fs120\\c&H00F5A93F&}THIAGO`)
    D(51.5, 54.2, 'Tag', '{\\fad(150,150)}EL MÁS VOTADO SERÁ PRESIDENTE')
    D(54.6, 57.6, 'Mid', '{\\an5\\pos(540,330)\\fad(200,150)}COMENTA:\\N{\\c&H004DD3FF&}«SOY ___ DE ___\\NY QUIERO SER ___»')
    D(56.2, 57.6, 'Tag', '{\\fad(150,150)}ETIQUETA A ALGUIEN DE TU PAÍS')
    D(57.7, to, 'Mid', `{\\an5\\pos(540,420)\\fad(200,0)${POP}}¿TU CASA AQUÍ?`)
    D(59.2, to, 'Big', '{\\an5\\pos(540,700)\\fad(250,0)}PIZZAVILLE')
    D(59.5, to, 'Mid', '{\\an5\\pos(540,850)\\fad(250,0)}OLIVER o THIAGO: ¡VOTA!')
  }
  if (ep === 'ep000') {
    ev.push(`Dialogue: 2,${assTime(0)},${assTime(3.0)},Mid,,0,0,0,,{\\an5\\pos(540,560)\\fad(0,200)\\t(0,250,\\fscx115\\fscy115)\\t(250,450,\\fscx100\\fscy100)}AQUÍ SOLO VIVE\\N{\\c&H004DD3FF&\\fs120}1 PERSONA`)
    ev.push(`Dialogue: 1,${assTime(25.2)},${assTime(40.2)},Tag,,0,0,0,,{\\fad(200,200)}SIMULACIÓN · ASÍ SERÁ`)
    ev.push(`Dialogue: 2,${assTime(51.0)},${assTime(56.3)},Mid,,0,0,0,,{\\an5\\pos(540,330)\\fad(200,150)}COMENTA:\\N{\\c&H004DD3FF&}«SOY ___ DE ___»`)
    ev.push(`Dialogue: 1,${assTime(41.0)},${assTime(50.2)},Tag,,0,0,0,,{\\fad(200,200)}2 ACTUALIZACIONES AL DÍA`)
    ev.push(`Dialogue: 2,${assTime(41.3)},${assTime(50.2)},Mid,,0,0,0,,{\\an5\\pos(540,1180)\\fad(200,200)}CADA CÍRCULO ES UNA CASA LIBRE\\N{\\c&H004DD3FF&}¿CUÁL SERÁ LA TUYA?`)
    ev.push(`Dialogue: 2,${assTime(57.2)},${assTime(to)},Big,,0,0,0,,{\\an5\\pos(540,700)\\fad(250,0)\\t(0,300,\\fscx110\\fscy110)\\t(300,500,\\fscx100\\fscy100)}PIZZAVILLE`)
    ev.push(`Dialogue: 2,${assTime(57.7)},${assTime(to)},Mid,,0,0,0,,{\\an5\\pos(540,850)\\fad(250,0)}1 HABITANTE · 1 CASA`)
    ev.push(`Dialogue: 2,${assTime(58.2)},${assTime(to)},Mid,,0,0,0,,{\\an5\\pos(540,1010)\\fad(250,0)\\c&H004DD3FF&}COMENTA «SOY ___ DE ___»\\NY TE MUDAS AQUÍ`)
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
  const reuse = opt('video', null)
  if (reuse) { ff.kill(); await new Promise((r) => ff.on('close', r)); fs.copyFileSync(reuse, silent) }
  for (let f = reuse ? n1 : n0; f < n1; f++) {
    const data = await p.evaluate((t) => { window.__pv.renderAt(t); return document.querySelector('canvas').toDataURL('image/jpeg', 0.93) }, f / FPS)
    const buf = Buffer.from(data.slice(data.indexOf(',') + 1), 'base64')
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r))
    if ((f - n0) % 30 === 0) {
      const el = (Date.now() - t0) / 1000, done = f - n0 + 1
      console.log(`frame ${f}/${n1}  ${(el / done).toFixed(2)} s/f  eta ${Math.round((el / done) * (n1 - f) / 60)} min`)
    }
  }
  if (!reuse) { ff.stdin.end(); await new Promise((r) => ff.on('close', r)) }
  await b.close()
  if (args.includes('--frames-only')) { console.log('FRAMES OK', silent); return }

  // ---------------- subtitles
  const ass = path.join(out, 'subs.ass')
  fs.writeFileSync(ass, buildAss(info, to))

  // ---------------- audio
  const voices = info.lines.filter((l) => l.hasAudio).map((l) => ({ file: path.resolve(`public/voz/${ep}/${l.id}.mp3`), at: l.at - from }))
  const cues = { duration: to - from, music: info.music, voices, sfx: info.sfx.map((s) => ({ ...s, at: s.at - from })) }
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
