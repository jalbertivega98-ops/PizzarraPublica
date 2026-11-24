# Eco de «pensamiento» para las frases T (voz interior) de un episodio toon: python3 scripts/pensamiento.py pareja11
# Lee voz/<ep>.json (kind == "T") y aplica a public/voz/<ep>/<id>.mp3 un eco suave + reverb corta. No repite.
import json, os, subprocess, sys
ep = sys.argv[1]
cfg = json.load(open(f'voz/{ep}.json'))
for l in cfg['lines']:
    if l.get('kind') != 'T': continue
    j = f'public/voz/{ep}/{l["id"]}.json'; mp3 = j[:-5] + '.mp3'
    d = json.load(open(j))
    if d.get('fx') == 'pensamiento': continue
    tmp = mp3 + '.tmp.mp3'
    flt = 'highpass=f=140,aecho=0.85:0.6:45|90|160:0.32|0.2|0.12,volume=1.15'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-af', flt, '-b:a', '128k', tmp], check=True)
    os.replace(tmp, mp3)
    d['fx'] = 'pensamiento'
    json.dump(d, open(j, 'w'), ensure_ascii=False, indent=1)
print('ok', ep)
