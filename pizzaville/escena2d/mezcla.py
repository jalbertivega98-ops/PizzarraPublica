"""Formato «Mi novia me dice…»: monta ella_1 + monólogo de él (pensamiento) + ella_2 con tratamiento de sonido
(ella suena en la habitación, el pensamiento suena seco y cercano) y, si hay tiempos, crea el timeline para la escena.
uso: python3 mezcla.py <ella_1.mp3> <mono.mp3> <ella_2.mp3> <out.mp3> [timeline.json]"""
import json, os, re, subprocess, sys, tempfile
import numpy as np
e1, mono, e2, out = sys.argv[1:5]; tlout = sys.argv[5] if len(sys.argv) > 5 else None
LEAD, G1, G2, TAIL, FPS, SR = 0.4, 0.45, 0.7, 1.6, 30, 44100
ROOM = 'highpass=f=90,aecho=0.8:0.55:23|41:0.16|0.09,loudnorm=I=-19:TP=-2:LRA=11'
THINK = 'highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16.5:TP=-1.5:LRA=9'
def dec(path, filt):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-af', filt + ',aresample=44100', '-ac', '1', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)
def dur(path): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout)
parts = [('ella', 'say', e1, ROOM), ('el', 'think', mono, THINK), ('ella', 'say', e2, ROOM)]
sil = lambda s: np.zeros(int(s * SR), np.float32)
buf, t, starts = [sil(LEAD)], LEAD, []
for k, (spk, kind, p, f) in enumerate(parts):
    a = dec(p, f); starts.append(t); buf.append(a); t += len(a) / SR
    gap = [G1, G2, TAIL][k]; buf.append(sil(gap)); t += gap
y = np.concatenate(buf)
y = np.clip(y, -1, 1)
tmp = tempfile.mktemp(suffix='.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', tmp], input=y.tobytes(), check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-b:a', '160k', out], check=True)
print('audio', out, round(len(y) / SR, 2), 's')
if not tlout: sys.exit()
def words(js, off):
    al = json.load(open(js))['alignment']; res, cur, inbr = [], None, False
    for c, a, b in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if c == '[': inbr = True; cur = None; continue
        if c == ']': inbr = False; continue
        if inbr: continue
        if c.isspace(): cur = None; continue
        if cur is None: cur = {'w': '', 'a': a + off, 'b': b + off}; res.append(cur)
        cur['w'] += c; cur['b'] = b + off
    return [w for w in res if re.search(r'\w', w['w'])]
lines = []
for (spk, kind, p, f), st in zip(parts, starts):
    ws = words(p[:-4] + '.json', st)
    if kind == 'say':
        lines.append({'spk': spk, 'kind': kind, 'a': ws[0]['a'], 'b': ws[-1]['b'], 'text': ' '.join(w['w'] for w in ws), 'words': ws})
        continue
    # thoughts: subtitle chunks that end on punctuation, ≤ 44 characters
    chunk = []
    def flush():
        if chunk: lines.append({'spk': spk, 'kind': kind, 'a': chunk[0]['a'], 'b': chunk[-1]['b'], 'text': ' '.join(w['w'] for w in chunk), 'words': list(chunk)}); chunk.clear()
    for w in ws:
        if chunk and len(' '.join(x['w'] for x in chunk + [w])) > 44: flush()
        chunk.append(w)
        if re.search(r'[.:?…»]$', w['w']) and len(' '.join(x['w'] for x in chunk)) >= 10: flush()
    flush()
# mouth envelope only for spoken lines (thoughts keep the mouth closed)
env = {'ella': [], 'el': []}
n = int(len(y) / SR * FPS) + 1; hop = SR // FPS
for fr in range(n):
    i0 = int(fr / FPS * SR); r = float(np.sqrt(np.mean(y[i0:i0 + hop * 2] ** 2) + 1e-9)) if i0 < len(y) else 0
    sp = [L for L in lines if L['kind'] == 'say' and L['a'] - 0.05 <= fr / FPS <= L['b'] + 0.05]
    env['ella'].append(r if sp and sp[0]['spk'] == 'ella' else 0); env['el'].append(0)
mx = max(env['ella']) or 1
env['ella'] = [round(min(1, v / (mx * 0.6)), 3) for v in env['ella']]; env['el'] = [0] * n
json.dump({'fps': FPS, 'dur': round(len(y) / SR, 3), 'lead': 0, 'lines': lines, 'env': env}, open(tlout, 'w'), ensure_ascii=False)
for L in lines: print(L['spk'], L['kind'], round(L['a'], 2), round(L['b'], 2), L['text'])
