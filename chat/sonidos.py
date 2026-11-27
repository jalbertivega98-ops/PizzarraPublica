"""Sonidos sintetizados para el motor de chat (sin samples con copyright).
uso: python3 sonidos.py eventos.json salida.wav
Eventos: recv (pop de mensaje recibido), sent (envío), key (tecla), sys (aviso).
Añade un colchón musical muy suave (acordes de pad) para que no haya silencio total.
"""
import json, sys, wave
import numpy as np

SR = 44100
ev = json.load(open(sys.argv[1]))
dur = ev["dur"] + 0.5
out = np.zeros(int(SR * dur))
rng = np.random.default_rng(7)

def env(n, a=0.003, d=0.08):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def tone(f0, f1, length, d, amp):
    n = int(SR * length); t = np.arange(n) / SR
    f = np.linspace(f0, f1, n); ph = 2 * np.pi * np.cumsum(f) / SR
    return amp * np.sin(ph) * env(n, d=d)

def mix(*xs):
    o = np.zeros(max(len(x) for x in xs))
    for x in xs: o[:len(x)] += x
    return o

def recv():
    return mix(tone(880, 1320, 0.16, 0.05, 0.35), tone(1320, 1760, 0.12, 0.03, 0.15))

def sent():
    n = int(SR * 0.22)
    noise = rng.standard_normal(n) * env(n, a=0.02, d=0.06)
    # filtro paso banda casero (diferencias) para un "fsss"
    noise = np.convolve(noise, np.ones(8) / 8, mode="same") - np.convolve(noise, np.ones(40) / 40, mode="same")
    return mix(0.5 * noise, tone(600, 900, 0.12, 0.04, 0.12))

def key():
    n = int(SR * 0.03)
    click = rng.standard_normal(n) * env(n, a=0.0005, d=0.006)
    return 0.22 * (click - np.convolve(click, np.ones(12) / 12, mode="same"))

def sys_():
    return tone(660, 660, 0.25, 0.08, 0.16)

F = {"recv": recv, "sent": sent, "key": key, "sys": sys_}
for e in ev["events"]:
    s = F[e["s"]](); i = int(e["t"] * SR)
    if e["s"] == "key": s = s * rng.uniform(0.6, 1.1)
    out[i:i + len(s)] += s[: len(out) - i]

# pad suave: Am - F - C - G, 2 s por acorde
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [196, 261.6, 329.6], [196, 246.9, 293.7]]
t = np.arange(len(out)) / SR
pad = np.zeros(len(out))
for k in range(int(dur / 2) + 1):
    a, b = int(k * 2 * SR), int((k + 1) * 2 * SR)
    seg = t[a:b] - k * 2
    if len(seg) == 0: break
    w = np.sin(np.pi * np.clip(seg / 2, 0, 1)) ** 2
    for f in chords[k % 4]:
        pad[a:b] += np.sin(2 * np.pi * f * t[a:b]) * w + 0.3 * np.sin(2 * np.pi * 2 * f * t[a:b]) * w
pad *= 0.018
fade = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.2)
out = out + pad * fade
out = np.clip(out, -1, 1)
st = np.stack([out, out], 1)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
