"""Sonidos sintetizados para el motor de chat (estilo app de mensajería, sin samples con copyright).
uso: python3 sonidos.py eventos.json salida.wav
Eventos: recv (burbuja "plop" de mensaje recibido), sent ("pup" de enviado), key (tecla), sys (aviso).
Música: bucle cómico opcional (solo si el guion lleva "musica": true). Por defecto, solo sonidos.
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

from scipy.signal import butter, sosfilt

def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)

def drop(f0, f1, length, decay, amp):
    """gota/burbuja: seno con subida de tono exponencial muy rápida (como el "pop" de mensajería)"""
    n = int(SR * length); t = np.arange(n) / SR
    f = f1 - (f1 - f0) * np.exp(-t / 0.012)
    ph = 2 * np.pi * np.cumsum(f) / SR
    e = np.minimum(1, t / 0.0015) * np.exp(-t / decay)
    return amp * np.sin(ph) * e

def recv():   # doble "pop" suave de mensaje recibido en el chat abierto
    a = drop(520, 1150, 0.09, 0.022, 0.75)
    b = drop(700, 1500, 0.09, 0.018, 0.45)
    o = np.zeros(int(SR * 0.22)); o[:len(a)] += a; s = int(SR * 0.085); o[s:s + len(b)] += b
    return bp(o, 250, 4000)

def sent():   # "pop" único y corto al enviar
    o = drop(650, 1400, 0.08, 0.016, 0.55)
    n = int(SR * 0.03)
    air = bp(rng.standard_normal(n), 2500, 7000) * np.exp(-np.arange(n) / SR / 0.006) * 0.12
    return bp(mix(o, air), 250, 8000)

def key():    # clic de teclado de móvil: golpe seco agudo + cuerpo grave muy corto
    n = int(SR * 0.04); t = np.arange(n) / SR
    click = bp(rng.standard_normal(n), 2200, 6500) * np.exp(-t / 0.0035) * 0.5
    body = np.sin(2 * np.pi * rng.uniform(300, 360) * t) * np.exp(-t / 0.006) * 0.35
    return click + body

def sys_():   # aviso de grupo: dos notas muy suaves
    return 0.5 * mix(drop(800, 880, 0.15, 0.05, 0.2), np.pad(drop(1100, 1175, 0.15, 0.05, 0.16), (int(SR * .07), 0)))

import subprocess, os
def cargar_voz(i):
    v = ev["voces"][str(i)]
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", os.path.join(ev["vozDir"], v["archivo"]), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, np.int16).astype(np.float64) / 32768 * 1.6

F = {"recv": recv, "sent": sent, "key": key, "sys": sys_}
for e in ev["events"]:
    s = cargar_voz(e["i"]) if e["s"] == "voz" else F[e["s"]](); i = int(e["t"] * SR)
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
out = out + (0.13 * mus * fade if ev.get('musica') else 0)
out = out / max(1e-9, np.abs(out).max()) * 0.85
st = np.stack([out, out], 1)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
