"""Música original y efectos de Pizzaville, generados por código (sin licencias).
Uso: python3 audio.py cues.json out.wav
cues.json = {"duration": 60, "voices": [{"file":..., "at":...}], "sfx": [{"type": "pop", "at": 3.1}, ...]}
"""
import json, sys, subprocess, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(SR * d)) / SR


def env(n, a=0.005, r=0.3):
    e = np.ones(n)
    na, nr = int(SR * a), min(n, int(SR * r))
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e


def freq(midi):
    return 440 * 2 ** ((midi - 69) / 12)


def pluck(f, d, bright=0.5):
    n = int(SR * d)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    out = np.empty(n)
    # vectorised Karplus-Strong in blocks of one period
    i = 0
    while i < n:
        k = min(p, n - i)
        out[i:i + k] = buf[:k]
        buf = 0.997 * (bright * buf + (1 - bright) * np.roll(buf, -1))
        i += k
    return out * np.exp(-np.linspace(0, 3.5, n))


def bell(f, d):
    t = t_(d)
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t)) * np.exp(-t * 4)


def pad(fs, d):
    t = t_(d)
    s = sum(np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * 0.3 * t)) + 0.3 * np.sin(2 * np.pi * f * 2.001 * t) for f in fs)
    return s / len(fs) * env(len(t), 0.6, 0.6)


def kick(d=0.35):
    t = t_(d)
    return np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 25)) * t) * np.exp(-t * 9)


def hat(d=0.06):
    n = int(SR * d)
    x = rng.uniform(-1, 1, n)
    x = x - np.concatenate([[0], x[:-1]])
    return x * np.exp(-np.linspace(0, 6, n))


def add(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(x) <= 0: return
    j = min(len(buf), i + len(x))
    buf[max(0, i):j] += g * x[max(0, -i):j - i]


def music(duration, bpm=104):
    out = np.zeros(int(SR * (duration + 2)))
    beat = 60 / bpm
    # I – V – vi – IV in C major, warm and optimistic
    prog = [[48, 52, 55, 60], [43, 47, 50, 55], [45, 48, 52, 57], [41, 45, 48, 53]]
    melody = [72, 74, 76, 79, 76, 74, 72, 74, 71, 74, 79, 74, 72, 76, 81, 79, 77, 76, 74, 72]
    t, bar, mi = 0.0, 0, 0
    while t < duration:
        ch = prog[bar % 4]
        intensity = min(1.0, 0.45 + t / 30)
        add(out, pad([freq(m + 12) for m in ch[1:]], beat * 4), t, 0.10)
        add(out, pluck(freq(ch[0] - 12), beat * 2, 0.6), t, 0.32)
        add(out, pluck(freq(ch[0] - 12), beat * 2, 0.6), t + beat * 2, 0.26)
        arp = [ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[2] + 12]
        for k in range(8):
            add(out, pluck(freq(arp[k % 4]), beat * 0.9, 0.5), t + k * beat / 2, 0.16)
        if t > 3:
            for k in range(4):
                add(out, kick(), t + k * beat, 0.35 * intensity)
                add(out, hat(), t + k * beat + beat / 2, 0.08 * intensity)
        if t > 8 and bar % 2 == 0:
            for k in range(4):
                add(out, bell(freq(melody[mi % len(melody)]), beat * 1.5), t + k * beat + (beat / 2 if k == 3 else 0), 0.07)
                mi += 1
        t += beat * 4
        bar += 1
    return out[: int(SR * duration)]


def music_epic(duration, mute=(), bpm=122):
    """minor-key, tense and driving (Pizz 2050): Am F C G, heavy kick, braam hits"""
    out = np.zeros(int(SR * (duration + 2)))
    beat = 60 / bpm
    prog = [[45, 48, 52, 57], [41, 45, 48, 53], [48, 52, 55, 60], [43, 47, 50, 55]]
    t, bar = 0.0, 0
    while t < duration:
        ch = prog[bar % 4]
        intensity = min(1.0, 0.55 + t / 25)
        add(out, pad([freq(m) for m in ch[1:]] + [freq(ch[0] - 12)], beat * 4), t, 0.16)
        for k in range(8):  # driving 8th-note bass
            add(out, pluck(freq(ch[0] - 12), beat * 0.5, 0.75), t + k * beat / 2, 0.30)
        arp = [ch[1] + 24, ch[2] + 24, ch[3] + 12, ch[2] + 24]
        for k in range(16):
            add(out, pluck(freq(arp[k % 4]), beat * 0.4, 0.4), t + k * beat / 4, 0.07 * intensity)
        for k in range(4):
            add(out, kick(0.4), t + k * beat, 0.5 * intensity)
            add(out, hat(), t + k * beat + beat / 2, 0.10 * intensity)
        if bar % 2 == 0:
            add(out, braam(freq(ch[0] - 24), beat * 3), t, 0.22)
        t += beat * 4
        bar += 1
    out = out[: int(SR * duration)]
    for a, b in mute:
        i, j = int(a * SR), int(b * SR)
        r = int(0.15 * SR)
        if i < len(out):
            out[i:i + r] *= np.linspace(1, 0, len(out[i:i + r]))
            out[i + r:j] = 0
    return out


def braam(f, d):
    t = t_(d)
    s = sum(np.sign(np.sin(2 * np.pi * f * m * t + 0.3 * k)) * (0.5 ** k) for k, m in enumerate([1, 1.005, 2, 3]))
    return s * env(len(t), 0.05, d * 0.6) * 0.5


# ------------------------------------------------------------------ sfx
def sfx(kind):
    if kind == 'whoosh':
        d = 1.2; n = int(SR * d); x = rng.uniform(-1, 1, n)
        # sweep a simple one-pole low-pass
        y = np.zeros(n); a = np.linspace(0.02, 0.35, n) ** 1.2; s = 0.0
        for i in range(n): s += a[i] * (x[i] - s); y[i] = s
        return y * np.sin(np.linspace(0, np.pi, n)) ** 2 * 1.6
    if kind == 'pop':
        t = t_(0.14); return np.sin(2 * np.pi * (300 + 900 * t / 0.14) * t) * np.exp(-t * 30)
    if kind == 'thud':
        t = t_(0.3); return np.sin(2 * np.pi * (90 * np.exp(-t * 6)) * t) * np.exp(-t * 14) + 0.2 * rng.uniform(-1, 1, len(t)) * np.exp(-t * 40)
    if kind == 'hammer':
        t = t_(0.09); return (np.sin(2 * np.pi * 1800 * t) * 0.5 + rng.uniform(-1, 1, len(t))) * np.exp(-t * 60) * 0.5
    if kind == 'door':
        t = t_(0.6); return np.sin(2 * np.pi * (180 + 60 * np.sin(t * 30)) * t) * 0.25 * env(len(t), 0.05, 0.3)
    if kind == 'chime':
        o = np.zeros(int(SR * 1.6))
        for k, m in enumerate([84, 88, 91, 96]): add(o, bell(freq(m), 1.2), k * 0.09, 0.5)
        return o
    if kind == 'rumble':
        n = int(SR * 2.5); x = rng.uniform(-1, 1, n); y = np.zeros(n); s = 0.0
        for i in range(n): s += 0.01 * (x[i] - s); y[i] = s
        t = t_(2.5)
        return (y * 25 + 0.5 * np.sin(2 * np.pi * 38 * t)) * env(n, 0.3, 1.0) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))
    if kind == 'riser':
        t = t_(2.0); f = 200 + 1400 * (t / 2.0) ** 2
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + rng.uniform(-1, 1, len(t)) * 0.25) * (t / 2.0) ** 2
    if kind == 'tick':
        t = t_(0.05); return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 90) * 0.6
    if kind == 'hit':
        t = t_(1.5)
        return (np.sin(2 * np.pi * (45 + 60 * np.exp(-t * 8)) * t) * np.exp(-t * 2.5) + rng.uniform(-1, 1, len(t)) * np.exp(-t * 18) * 0.5)
    if kind == 'step':
        t = t_(0.08); return rng.uniform(-1, 1, len(t)) * np.exp(-t * 70) * 0.25
    raise ValueError(kind)


def load_mp3(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float64) / 32768


def main(cues_path, out_path):
    cues = json.load(open(cues_path))
    D = cues['duration']
    mus = music_epic(D, cues.get('mute', [])) if cues.get('music') == 'epic' else music(D)
    voice = np.zeros(int(SR * (D + 1)))
    for v in cues['voices']:
        add(voice, load_mp3(v['file']) * 1.0, v['at'])
    fx = np.zeros(int(SR * (D + 1)))
    for c in cues['sfx']:
        add(fx, sfx(c['type']), c['at'], c.get('g', 0.5))
    voice, fx = voice[: len(mus)], fx[: len(mus)]
    # ducking: music lowers under the voice
    envl = np.convolve(np.abs(voice), np.ones(4410) / 4410, mode='same')
    duck = 1 - 0.55 * np.clip(envl / 0.05, 0, 1)
    mix = mus * 0.55 * duck + voice * 1.0 + fx * 0.6
    fade = int(SR * 1.2)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix /= max(1.0, np.max(np.abs(mix)) / 0.95)
    with wave.open(out_path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print('audio ok', out_path, len(mix) / SR, 's')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
