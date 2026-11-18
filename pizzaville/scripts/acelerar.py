# Acelera la voz de un episodio sin cambiar el tono: python3 scripts/acelerar.py pareja02 1.12
# Reescribe public/voz/<ep>/lNN.mp3 (atempo) y escala los tiempos por palabra del .json. No repite si ya está acelerado.
import glob, json, os, subprocess, sys
ep, k = sys.argv[1], float(sys.argv[2])
for j in sorted(glob.glob(f'public/voz/{ep}/l*.json')):
    d = json.load(open(j))
    if d.get('tempo'): print('ya acelerado', j); continue
    mp3 = j[:-5] + '.mp3'; tmp = mp3 + '.tmp.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-filter:a', f'atempo={k}', '-b:a', '128k', tmp], check=True)
    os.replace(tmp, mp3)
    for w in d['words']: w['t'] = round(w['t'] / k, 3); w['d'] = round(w['d'] / k, 3)
    d['tempo'] = k
    json.dump(d, open(j, 'w'), ensure_ascii=False, indent=1)
print('ok', ep, k)
