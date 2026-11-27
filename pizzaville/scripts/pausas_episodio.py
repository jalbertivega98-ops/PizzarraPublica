"""Añade silencios entre líneas de un diálogo continuo y reajusta los tiempos del episodio.
python3 scripts/pausas_episodio.py <mp3> <episodio> <base_s> [lNN=extra_s ...]
Lee src/episodes/<ep>_data.ts + public/voz/<ep>/lNN.json (de dialogo_episodio.py, lead 0.5),
escribe public/voz/<ep>/dialogo.mp3 (sin el lead: usar export --audio-at 0.5) y reescribe <ep>_data.ts."""
import json, subprocess, sys
src, ep, base = sys.argv[1], sys.argv[2], float(sys.argv[3]); LEAD = 0.5
extra = {k: float(v) for k, v in (a.split('=') for a in sys.argv[4:])}
p = f'src/episodes/{ep}_data.ts'; txt = open(p).read()
conv = json.loads(txt[txt.index('['):txt.rindex(']') + 1])
ends = {}
for c in conv:
    w = json.load(open(f"public/voz/{ep}/{c['id']}.json"))['words'][-1]; ends[c['id']] = c['at'] + w['t'] + w['d']
cuts = []
for prev, c in zip(conv, conv[1:]):
    cuts.append(((ends[prev['id']] + c['at']) / 2 - LEAD, base + extra.get(c['id'], 0)))
f, parts, t0 = [], [], 0
for n, (cut, g) in enumerate(cuts):
    f.append(f"[0:a]atrim={t0}:{cut},asetpts=PTS-STARTPTS[a{n}]"); parts.append(f"[a{n}]")
    f.append(f"anullsrc=r=44100:cl=mono,atrim=0:{g}[s{n}]"); parts.append(f"[s{n}]"); t0 = cut
n = len(cuts); f.append(f"[0:a]atrim={t0},asetpts=PTS-STARTPTS[a{n}]"); parts.append(f"[a{n}]")
f.append(''.join(parts) + f"concat=n={len(parts)}:v=0:a=1[out]")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-filter_complex', ';'.join(f), '-map', '[out]', '-ar', '44100', '-ac', '1', '-b:a', '192k', f'public/voz/{ep}/dialogo.mp3'], check=True)
sh = 0
for i, c in enumerate(conv):
    if i: sh += cuts[i - 1][1]
    c['at'] = round(c['at'] + sh, 3)
open(p, 'w').write(f'// generado por dialogo_episodio.py + pausas_episodio.py (public/voz/{ep}/dialogo.mp3, --audio-at 0.5)\nexport const CONV = ' + json.dumps(conv, ensure_ascii=False, indent=1) + ' as const\n')
print('total pausas', round(sum(g for _, g in cuts), 2))
