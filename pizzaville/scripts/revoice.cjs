// Cambia SOLO la voz de un episodio ya exportado (misma imagen): nuevas frases + subtítulos al ritmo de la nueva voz.
// uso: node scripts/revoice.cjs <dir_export> <carpeta_voz>   p.ej. node scripts/revoice.cjs /tmp/full ep000_eleven
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process')
const [dir, vdir] = process.argv.slice(2)
const src = fs.readFileSync(path.join(__dirname, 'export.cjs'), 'utf8')
const lib = src.slice(src.indexOf('const FPS'), src.indexOf(';(async'))
const { buildAss } = new Function('require', 'path', 'fs', 'args', 'opt', 'ep', lib.replace(/^fs\.mkdirSync[^\n]*\n/m, '') + '\nreturn { buildAss }')(require, path, fs, [], (k, d) => d, 'ep')
const info = JSON.parse(fs.readFileSync(path.join(dir, 'info.json'), 'utf8'))
const voices = []
for (const l of info.lines) {
  const j = JSON.parse(fs.readFileSync(path.resolve(`public/voz/${vdir}/${l.id}.json`), 'utf8'))
  if (j.text !== l.text) throw new Error('texto distinto en ' + l.id)
  l.words = j.words
  l.dur = j.words.at(-1).t + j.words.at(-1).d
  voices.push({ file: path.resolve(`public/voz/${vdir}/${l.id}.mp3`), at: l.at })
}
const cues = { ...JSON.parse(fs.readFileSync(path.join(dir, 'cues.json'), 'utf8')), voices }
const tag = vdir.replace(/\W/g, '_')
fs.writeFileSync(path.join(dir, `cues_${tag}.json`), JSON.stringify(cues, null, 1))
fs.writeFileSync(path.join(dir, `subs_${tag}.ass`), buildAss(info, info.duration))
const wav = path.join(dir, `audio_${tag}.wav`)
execFileSync('python3', [path.resolve('scripts/audio.py'), path.join(dir, `cues_${tag}.json`), wav], { stdio: 'inherit' })
const final = path.join(dir, `${info.id}_${tag}.mp4`)
execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', path.join(dir, 'video_silent.mp4'), '-i', wav, '-vf', `setpts=PTS-STARTPTS,ass=${path.join(dir, `subs_${tag}.ass`)}:fontsdir=${path.resolve('scripts/fonts')}`,
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', final], { stdio: 'inherit' })
console.log('OK', final)
