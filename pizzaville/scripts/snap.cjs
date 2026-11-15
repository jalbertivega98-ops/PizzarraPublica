// node scripts/snap.cjs ep001 out.png t1 t2 ...  → grid of frames (270x480 each)
const { chromium } = require('playwright')
const { execFileSync } = require('child_process')
;(async () => {
  const [ep, out, ...ts] = process.argv.slice(2)
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] })
  const p = await b.newPage({ viewport: { width: 270, height: 480 } })
  p.on('pageerror', (e) => console.log('[pageerror]', e.message))
  await p.goto(`http://localhost:4173/?record=1&episode=${ep}`)
  await p.waitForFunction(() => window.__pv && window.__pv.info, null, { timeout: 180000, polling: 500 })
  await p.evaluate(() => window.__pv.renderAt(0)); await p.evaluate(() => window.__pv.ready())
  const files = []
  for (const t of ts) {
    await p.evaluate((t) => window.__pv.renderAt(t), +t)
    const d = await p.evaluate(() => document.querySelector('canvas').toDataURL('image/png'))
    const f = `/tmp/claude-0/snap_${t}.png`; require('fs').writeFileSync(f, Buffer.from(d.split(',')[1], 'base64')); files.push(f)
  }
  await b.close()
  execFileSync('python3', ['-c', `
import sys
from PIL import Image, ImageDraw
fs=sys.argv[2:]; n=len(fs); c=min(n,6); r=(n+c-1)//c
W=Image.new('RGB',(270*c,480*r))
for i,f in enumerate(fs):
  im=Image.open(f); ImageDraw.Draw(im).text((4,4),f.split('_')[-1][:-4],fill='yellow'); W.paste(im,((i%c)*270,(i//c)*480))
W.save(sys.argv[1])`, out, ...files])
})()
