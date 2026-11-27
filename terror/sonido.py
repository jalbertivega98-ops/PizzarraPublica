#!/usr/bin/env python3
"""Diseño sonoro sintetizado (sin licencias) para el motor de terror.
uso: python3 sonido.py timeline.json salida.wav [carpeta_voz]
timeline.json = {"dur": s, "events": [{"t":..,"s":"nombre","d":..,"v":..}]}"""
import json, sys
import numpy as np
from scipy import signal

SR = 48000
R = np.random.default_rng(13)

def t_(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, r=0.1):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x)
def noise(d): return R.standard_normal(int(d * SR))
def brown(d): x = np.cumsum(noise(d)); x -= signal.savgol_filter(x, 4001, 1) if len(x) > 4001 else x.mean(); return x / (np.abs(x).max() + 1e-9)
def norm(x, p=1.0): return x / (np.abs(x).max() + 1e-9) * p
def reson(x, f, q=30):
    b, a = signal.iirpeak(f, q, fs=SR); return signal.lfilter(b, a, x)

# ---------- sonidos ----------
def viento(d=8, v=1):
    n = noise(d); x = bp(n, 250, 900) * 0.6 + bp(n, 900, 2400) * 0.25
    tt = t_(d); m = 0.55 + 0.45 * np.sin(2 * np.pi * 0.23 * tt + 1) * np.sin(2 * np.pi * 0.11 * tt)
    whistle = np.sin(2 * np.pi * (520 + 60 * np.sin(2 * np.pi * 0.3 * tt)) * tt) * 0.04 * m
    return (norm(x * m, 0.35) + whistle) * 0.7
def drone(d=20, v=1):
    tt = t_(d); sw = np.clip(tt / d, 0, 1)
    x = sum(np.sin(2 * np.pi * f * tt + p) for f, p in [(41.2, 0), (41.9, 1), (61.7, 2), (82.0, 0.5)]) * 0.18
    x += lp(brown(d), 120) * 0.35
    # cuerda disonante que crece
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.1 * tt)
    hi = (np.sin(2 * np.pi * 466.2 * vib * tt) + np.sin(2 * np.pi * 493.9 * vib * tt) * 0.8 + np.sin(2 * np.pi * 698.5 * tt * vib) * 0.4)
    x += hi * 0.05 * sw ** 1.8
    return x * env(len(tt), 1.5, 0.8) * (0.55 + 0.45 * sw) * 0.45
def trueno(d=3.5, v=1):
    crack = hp(noise(0.25), 1500) * np.exp(-t_(0.25) * 25)
    rum = lp(brown(d), 200, 4) * np.exp(-t_(d) * 1.1) * (1 + 0.6 * np.sin(2 * np.pi * 3.3 * t_(d)))
    out = norm(rum, 1.0); out[:len(crack)] += norm(crack, 0.5)
    return out * v
def golpe_titulo(d=2.5, v=1):
    tt = t_(d); f = 55 * np.exp(-tt * 1.4) + 28
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2)
    return (norm(boom, 1) + lp(noise(d), 400) * np.exp(-tt * 6) * 0.4) * v
def paso_tierra(d=0.18, v=0.6):
    tt = t_(d); return norm(bp(noise(d), 600, 3500) * np.exp(-tt * 30) + lp(noise(d), 200) * np.exp(-tt * 40) * 0.6, 0.5) * v
def paso_madera(d=0.35, v=0.8):
    tt = t_(d); th = np.sin(2 * np.pi * 85 * tt) * np.exp(-tt * 28) + lp(noise(d), 500) * np.exp(-tt * 35) * 0.5
    out = norm(th, 0.8)
    if R.random() < 0.45:  # crujido de tabla
        cr = reson(np.where(R.random(len(tt)) < 0.004, 1.0, 0.0), 900 + R.random() * 500, 25) * env(len(tt), 0.05, 0.1)
        out += norm(cr, 0.25)
    return out * v
def chirrido(d=1.5, v=1):
    tt = t_(d); n = len(tt)
    rate = 55 + 45 * np.sin(2 * np.pi * 0.7 * tt + 1) + 25 * np.sin(2 * np.pi * 2.9 * tt)
    ph = np.cumsum(rate) / SR; imp = np.zeros(n); idx = np.nonzero(np.diff(np.floor(ph)) > 0)[0]; imp[idx] = 1 + R.random(len(idx)) * 0.5
    x = reson(imp, 720, 18) + reson(imp, 1480, 22) * 0.7 + reson(imp, 2350, 25) * 0.4 + reson(imp, 380, 12) * 0.6
    return norm(x * env(n, 0.08, 0.25), 0.7) * v
def portazo(d=3.0, v=1):
    tt = t_(d); f = 70 * np.exp(-tt * 3) + 35
    b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 5)
    hit = lp(noise(d), 1500) * np.exp(-tt * 18)
    rattle = bp(noise(d), 2000, 5000) * np.exp(-tt * 9) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 23 * tt)))
    return norm(norm(b) + norm(hit) * 0.8 + norm(rattle) * 0.15, 1) * v
def pelota(d=1.4, v=1):
    tt = t_(d); spd = np.clip(1 - tt / d, 0, 1) ** 0.6
    roll = lp(noise(d), 300) * (0.6 + 0.4 * np.sin(2 * np.pi * (6 * spd) * tt)) * spd
    return norm(roll, 0.45) * env(len(tt), 0.1, 0.2) * v
def toc(d=0.4, v=1):
    tt = t_(d); x = reson(np.r_[1.0, np.zeros(len(tt) - 1)], 190, 8) + reson(np.r_[1.0, np.zeros(len(tt) - 1)], 420, 10) * 0.4
    x += lp(noise(d), 2500) * np.exp(-tt * 120) * 0.3
    return norm(x * np.exp(-tt * 14), 0.9) * v
def zumbido_linterna(d=0.75, v=1):
    tt = t_(d); x = signal.square(2 * np.pi * 100 * tt) * 0.3 + hp(noise(d), 3000) * (R.random(len(tt)) < 0.02) * 2
    gate = (np.sin(2 * np.pi * 13 * tt) > -0.2).astype(float)
    return norm(lp(x, 4000) * gate, 0.3) * env(len(tt), 0.01, 0.05) * v
def susto(d=3.5, v=1):
    tt = t_(d); n = len(tt)
    cl = sum(signal.sawtooth(2 * np.pi * f * (1 + 0.003 * k) * tt) for k, f in enumerate([110, 116.5, 123.5, 155.6, 164.8, 233.1, 246.9, 329.6]))
    cl = lp(cl, 2500) * np.exp(-tt * 1.2)
    scr = np.sin(2 * np.pi * np.cumsum(1800 + 900 * tt + 120 * np.sin(2 * np.pi * 9 * tt)) / SR) * np.exp(-tt * 2.5)
    boom = np.sin(2 * np.pi * np.cumsum(60 * np.exp(-tt * 2) + 30) / SR) * np.exp(-tt * 1.8)
    hit = lp(noise(d), 3000) * np.exp(-tt * 12)
    return norm(norm(cl) * 0.8 + norm(scr) * 0.3 + norm(boom) * 1.0 + norm(hit) * 0.6, 1) * env(n, 0.004, 0.5) * v
def latido(d=7, v=1):
    out = np.zeros(int(d * SR)); t = 0.15; per = 0.95
    while t < d - 0.4:
        for off, a in [(0, 1), (0.16, 0.7)]:
            s = int((t + off) * SR); tt = t_(0.25)
            beat = np.sin(2 * np.pi * (48 + 20 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 18) * a
            out[s:s + len(beat)] += beat[:len(out) - s]
        t += per; per = max(0.62, per * 0.96)
    return norm(lp(out, 150), 0.6) * env(len(out), 0.6, 0.6) * v
def bombilla(d=4.8, v=1):
    tt = t_(d); x = np.sin(2 * np.pi * 120 * tt) * 0.5 + np.sin(2 * np.pi * 240 * tt) * 0.25 + bp(noise(d), 4000, 8000) * 0.05
    flick = np.where(tt < 0.9, (np.sin(2 * np.pi * 7 * tt) > 0).astype(float), 1.0)
    return x * flick * 0.12 * env(len(tt), 0.01, 0.3) * v
def pop(d=0.9, v=1):
    tt = t_(d); x = np.sin(2 * np.pi * (70 * np.exp(-tt * 6) + 40) * tt) * np.exp(-tt * 7)
    x += np.sin(2 * np.pi * 1320 * tt) * np.exp(-tt * 9) * 0.12 + np.sin(2 * np.pi * 1975 * tt) * np.exp(-tt * 11) * 0.06
    return norm(x, 0.35) * v

VOZDIR = '.'
LENTO = True
def voz(f='l1', d=None, v=1):
    """Narrador terrorífico: más lento y grave, capa de susurro, saturación suave."""
    from scipy.io import wavfile
    sr, x = wavfile.read(f'{VOZDIR}/{f}.wav'); x = x.astype(float) / 32768
    if not LENTO: return norm(lp(x, 9000) + lp(x, 200) * 0.35, 1.0) * v   # voz natural (ElevenLabs): solo un poco de cuerpo
    x = signal.resample_poly(x, 10, 9)                     # 10 % más lenta y ~2 semitonos más grave
    x = lp(x, 6500) + lp(x, 220) * 0.8                      # cuerpo grave
    envl = np.abs(signal.hilbert(x)); envl = lp(envl, 30)
    whisper = bp(R.standard_normal(len(x)), 2500, 7000) * envl * 0.35
    y = np.tanh(norm(x) * 1.3 + whisper)
    return norm(y, 1.0) * v

FX = {k: v for k, v in globals().items() if callable(v) and k in [
    'viento', 'drone', 'trueno', 'golpe_titulo', 'paso_tierra', 'paso_madera', 'chirrido', 'portazo', 'pelota', 'toc',
    'zumbido_linterna', 'susto', 'latido', 'bombilla', 'pop', 'voz']}
DRY_ONLY = {'drone', 'viento', 'latido', 'bombilla', 'pop', 'golpe_titulo'}
PAN = {'toc': 0.45, 'pelota': -0.35, 'chirrido': 0.0}

def ir(d=2.2):
    tt = t_(d); x = noise(d) * np.exp(-tt * 3.2); x = lp(x, 5000); return x / np.sqrt((x ** 2).sum())

def main(tl_path, out_path):
    tl = json.load(open(tl_path)); dur = tl['dur']; n = int((dur + 0.1) * SR)
    L = np.zeros(n); Rr = np.zeros(n); wet = np.zeros(n); VL = np.zeros(n)
    for e in tl['events']:
        f = FX[e['s']]; kw = {}
        if e['s'] == 'voz':
            x = voz(e['f']); s = int(e['t'] * SR); x = x[:max(0, n - s)]; VL[s:s + len(x)] += x; continue
        if 'd' in e: kw['d'] = e['d']
        if 'v' in e: kw['v'] = e['v']
        x = f(**kw); s = int(e['t'] * SR); x = x[:max(0, n - s)]
        p = PAN.get(e['s'], (R.random() - 0.5) * 0.3 if e['s'].startswith('paso') else 0)
        L[s:s + len(x)] += x * (1 - max(0, p)); Rr[s:s + len(x)] += x * (1 + min(0, p))
        if e['s'] not in DRY_ONLY: wet[s:s + len(x)] += x * (0.9 if e['t'] > 7 else 0.35)
    rv = signal.fftconvolve(wet, ir())[:n] * 0.5
    L += rv; Rr += np.r_[rv[240:], np.zeros(240)]
    # la música/efectos bajan cuando habla el narrador (ducking)
    mx = max(np.abs(L).max(), np.abs(Rr).max()) + 1e-9; L /= mx; Rr /= mx
    ve = lp(np.abs(VL), 4); ve = np.clip(ve / (ve.max() + 1e-9) * 4, 0, 1); duck = 1 - 0.45 * ve
    L *= duck; Rr *= duck
    vr = signal.fftconvolve(VL, ir(1.6))[:n] * 0.35          # eco de casa vacía
    VL = VL * 0.95 + vr
    L += VL * 0.95; Rr += np.r_[VL[96:], np.zeros(96)] * 0.95
    st = np.stack([L, Rr], 1); st = np.tanh(st / (np.abs(st).max() + 1e-9) * 1.25) * 0.93
    fade = int(0.4 * SR); st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    from scipy.io import wavfile
    wavfile.write(out_path, SR, (st * 32767).astype(np.int16)); print('ok', out_path, round(dur, 2), 's')

if __name__ == '__main__':
    if len(sys.argv) > 3: VOZDIR = sys.argv[3]
    if '--natural' in sys.argv: LENTO = False
    main(sys.argv[1], sys.argv[2])
