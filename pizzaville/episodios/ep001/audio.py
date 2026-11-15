import json, subprocess, wave
import numpy as np

tl = json.load(open('timeline.json', encoding='utf-8'))
SR, T = 44100, tl['total']
n = int(SR * T)
t = np.arange(n) / SR
bpm = 112; beat = 60 / bpm
# progresión alegre I–V–vi–IV en Do
chords = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
f = lambda m: 440 * 2 ** ((m - 69) / 12)
music = np.zeros(n)
def note(start, dur, freq, amp, kind='pluck'):
    a, b = int(start * SR), min(n, int((start + dur) * SR))
    if a >= n: return
    tt = np.arange(b - a) / SR
    env = np.exp(-tt * (6 if kind == 'pluck' else 1.5)) * np.minimum(1, tt * 200)
    w = np.sin(2 * np.pi * freq * tt) + 0.3 * np.sin(4 * np.pi * freq * tt)
    music[a:b] += amp * env * w
bar = 4 * beat; k = 0; x = 0.0
while x < T:
    ch = chords[k % 4]
    for i in range(8):  # arpegio en corcheas
        note(x + i * beat / 2, beat, f(ch[i % 3] + (12 if i % 4 == 3 else 0)), 0.16)
    note(x, bar, f(ch[0] - 24), 0.22, 'pad')
    for i in range(4):  # ritmo suave
        a = int((x + i * beat) * SR); b = min(n, a + int(0.05 * SR))
        if a < n: music[a:b] += 0.08 * np.random.default_rng(k * 4 + i).standard_normal(b - a) * np.exp(-np.arange(b - a) / SR * 60)
    x += bar; k += 1
music /= np.abs(music).max() + 1e-9
fade = np.minimum(1, np.minimum(t / 1.0, (T - t) / 2.0))
music *= 0.5 * fade
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((music * 32767).astype(np.int16).tobytes())
# mezcla: música (más baja bajo la voz) + voces en su tiempo
ins = ['-i', 'music.wav']; filt = []
for i, s in enumerate(tl['segments']):
    ins += ['-i', s['file']]; d = int(s['start'] * 1000); filt.append(f"[{i+1}:a]adelay={d}|{d},volume=1.6[v{i}]")
vs = ''.join(f'[v{i}]' for i in range(len(tl['segments'])))
filt.append(f"{vs}amix=inputs={len(tl['segments'])}:normalize=0[voz]")
filt.append("[voz]apad,asplit[voz1][voz2]")
filt.append("[0:a]volume=0.35[mus]")
filt.append("[mus][voz2]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[duck]")
filt.append("[duck][voz1]amix=inputs=2:normalize=0,alimiter=limit=0.95[out]")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', ';'.join(filt), '-map', '[out]', '-t', str(T), '-ar', '44100', '-ac', '2', 'mix.wav'], check=True)
print('ok', T)
