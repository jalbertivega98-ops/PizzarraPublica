"""Sonidos sintetizados para el motor de chat (estilo app de mensajería, sin samples con copyright).
uso: python3 sonidos.py eventos.json salida.wav
Eventos: recv (burbuja "plop" de mensaje recibido), sent ("pup" de enviado), key (tecla), sys (aviso).
Música: bucle cómico de pizzicato + bajo + palmas, compuesto aquí (original), a volumen bajo.
"""
import json, sys, wave
import numpy as np

SR = 44100
ev = json.load(open(sys.argv[1]))
dur = ev["dur"] + 0.5
N = int(SR * dur)
out = np.zeros(N)
rng = np.random.default_rng(7)

def env(n, a=0.003, d=0.08):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def sweep(f0, f1, length, d, amp, a=0.002):
    n = int(SR * length)
    f = np.geomspace(f0, f1, n); ph = 2 * np.pi * np.cumsum(f) / SR
    return amp * np.sin(ph) * env(n, a=a, d=d)

def mix(*xs):
    o = np.zeros(max(len(x) for x in xs))
    for x in xs: o[:len(x)] += x
    return o

def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")

def recv():   # "plop" de burbuja: gota que sube + segundo toque
    a = sweep(300, 1100, 0.07, 0.03, 0.55)
    b = sweep(700, 1500, 0.06, 0.025, 0.30)
    o = np.zeros(int(SR * 0.2)); o[:len(a)] += a; s = int(SR * 0.075); o[s:s + len(b)] += b
    return o

def sent():   # "pup" corto y suave
    return mix(sweep(500, 1300, 0.08, 0.025, 0.35), 0.15 * lp(rng.standard_normal(int(SR * .05)) * env(int(SR * .05), d=.01), 6))

def key():    # tecla de móvil
    n = int(SR * 0.025)
    c = rng.standard_normal(n) * env(n, a=0.0003, d=0.004)
    return mix(0.30 * (c - lp(c, 10)), sweep(1800, 1500, 0.02, 0.004, 0.05))

def sys_():
    return mix(sweep(880, 880, 0.18, 0.06, 0.16), np.pad(sweep(1320, 1320, 0.2, 0.07, 0.12), (int(SR * .08), 0)))

F = {"recv": recv, "sent": sent, "key": key, "sys": sys_}
for e in ev["events"]:
    s = F[e["s"]](); i = int(e["t"] * SR)
    if i >= N: continue
    if e["s"] == "key": s = s * rng.uniform(0.6, 1.1)
    out[i:i + len(s)] += s[: N - i]

# ---------- música: bucle cómico (pizzicato) ----------
BPM = 116; beat = 60 / BPM; e8 = beat / 2
def pluck(f, length=0.35, amp=0.5):
    n = int(SR * length); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) * np.exp(-t / 0.05) + 0.25 * np.sin(6 * np.pi * f * t) * np.exp(-t / 0.03)
    return amp * x * env(n, a=0.002, d=0.09)
def bass(f, length=0.3, amp=0.6):
    n = int(SR * length); t = np.arange(n) / SR
    return amp * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * env(n, a=0.004, d=0.12)
def clap():
    n = int(SR * 0.12); c = rng.standard_normal(n) * env(n, a=0.001, d=0.03)
    return 0.25 * (c - lp(c, 6))
NT = {"C4": 261.6, "D4": 293.7, "E4": 329.6, "F4": 349.2, "G4": 392.0, "A4": 440.0, "B4": 493.9, "C5": 523.3, "D5": 587.3, "E5": 659.3, "G3": 196.0, "C3": 130.8, "F3": 174.6, "G2": 98.0, "A2": 110.0, "C2": 65.4, "F2": 87.3}
# 2 compases × 4 tiempos en corcheas (16 pasos), melodía saltarina tipo "travesura"
mel = ["C5", None, "G4", None, "E4", "G4", None, "C5", "D5", None, "B4", None, "G4", None, None, None,
       "A4", None, "F4", None, "C4", "F4", None, "A4", "G4", None, "E4", "D4", "C4", None, None, None]
bas = ["C2", None, None, None, "G2", None, None, None, "C2", None, None, None, "G2", None, None, None,
       "F2", None, None, None, "C2", None, None, None, "G2", None, None, None, "C2", None, None, None]
mus = np.zeros(N)
step = 0; t0 = 0.0
while t0 < dur:
    k = step % 32
    i = int(t0 * SR)
    for seq, fn in ((mel, pluck), (bas, bass)):
        if seq[k]:
            s = fn(NT[seq[k]]); mus[i:i + len(s)] += s[: N - i]
    if k % 8 == 4:
        s = clap(); mus[i:i + len(s)] += s[: N - i]
    step += 1; t0 += e8
t = np.arange(N) / SR
fade = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 1.5)
out = out + 0.13 * mus * fade
out = out / max(1e-9, np.abs(out).max()) * 0.85
st = np.stack([out, out], 1)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
