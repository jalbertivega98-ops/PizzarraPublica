"""Builds the timeline for the 2D test scene from an ElevenLabs dialogue (with timestamps):
lines (speaker, start, end, text), words with times, and a per-frame mouth envelope per speaker.
uso: python3 timeline.py <dialogo.json> <dialogo.mp3> <lead_s> <tail_s> <out.json>"""
import json, re, subprocess, sys
import numpy as np
js, mp3, lead, tail, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
FPS = 30
d = json.load(open(js)); al = d['alignment']; segs = d['voice_segments']
ch, cs, ce = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
# words outside [tags]
words, cur, inbr = [], None, False
for c, a, b in zip(ch, cs, ce):
    if c == '[': inbr = True; cur = None; continue
    if c == ']': inbr = False; continue
    if inbr: continue
    if c.isspace():
        cur = None; continue
    if cur is None:
        cur = {'w': '', 'a': a, 'b': b}; words.append(cur)
    cur['w'] += c; cur['b'] = b
lines = []
for i, s in enumerate(segs):
    a, b = s['start_time_seconds'], s['end_time_seconds']
    ws = [w for w in words if a - 0.01 <= w['a'] < b]
    ws = [w for w in ws if re.search(r'\w', w['w'])]
    spk = 'ella' if i % 2 == 0 else 'el'
    lines.append({'spk': spk, 'a': ws[0]['a'] + lead, 'b': ws[-1]['b'] + lead,
                  'text': ' '.join(w['w'] for w in ws),
                  'words': [{'w': w['w'], 'a': w['a'] + lead, 'b': w['b'] + lead} for w in ws]})
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-ac', '1', '-ar', '24000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
dur = len(x) / 24000 + lead + tail
n = int(dur * FPS) + 1
env = {'ella': [0.0] * n, 'el': [0.0] * n}
hop = 24000 // FPS
for f in range(n):
    t = f / FPS - lead
    i0 = int(t * 24000)
    if i0 < 0 or i0 >= len(x): continue
    r = float(np.sqrt(np.mean(x[i0:i0 + hop * 2] ** 2) + 1e-9))
    for L in lines:
        if L['a'] - 0.05 <= t + lead <= L['b'] + 0.05:
            env[L['spk']][f] = r
mx = max(max(env['ella']), max(env['el'])) or 1
for k in env:
    env[k] = [round(min(1, v / (mx * 0.6)), 3) for v in env[k]]
json.dump({'fps': FPS, 'dur': round(dur, 3), 'lead': lead, 'lines': lines, 'env': env}, open(out, 'w'), ensure_ascii=False)
for L in lines: print(L['spk'], round(L['a'], 2), round(L['b'], 2), L['text'])
print('dur', round(dur, 2))
