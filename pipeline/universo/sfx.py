"""Efectos de sonido cartoon generados por código (sin licencias de terceros), 44,1 kHz mono float32.

pasos, carrera, golpe (bonk), aplastar, tropiezo, sorpresa (silbato que sube), caida (silbato que baja), puerta,
monedas, calculadora, kaching (caja registradora), estrellitas, redoble, scratch (disco rayado), iris, papel.
"""
import numpy as np

SR = 44100


def _t(d):
    return np.arange(int(SR * d)) / SR


def _ruido(n, seed=0):
    return np.random.default_rng(seed).uniform(-1, 1, n)


def _lp(x, k):
    """Paso bajo simple (media móvil de k muestras)."""
    if k <= 1:
        return x
    return np.convolve(x, np.ones(k) / k, mode="same")


def _env(n, a=0.002, d=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    if d:
        e *= np.exp(-t / d)
    return e


def pasos(seed=0, fuerte=1.0):
    """Paso suave de zapatilla: golpe grave + roce."""
    n = int(SR * 0.09)
    t = _t(0.09)
    thump = np.sin(2 * np.pi * (110 + 40 * np.exp(-t * 60)) * t) * np.exp(-t * 55)
    roce = _lp(_ruido(n, seed), 6) * np.exp(-t * 70) * 0.35
    return ((thump * 0.6 + roce) * 0.5 * fuerte).astype(np.float32)


def carrera(seed=0):
    return pasos(seed, 1.25)


def golpe(seed=0):
    """Bonk cartoon: bloque de madera + golpe grave."""
    t = _t(0.35)
    wood = np.sin(2 * np.pi * 820 * t) * np.exp(-t * 38) + 0.5 * np.sin(2 * np.pi * 1260 * t) * np.exp(-t * 50)
    low = np.sin(2 * np.pi * (180 * np.exp(-t * 8) + 50) * t) * np.exp(-t * 12)
    return ((wood * 0.45 + low * 0.7) * 0.6).astype(np.float32)


def aplastar(seed=0):
    """Plaf: golpe + chapoteo descendente."""
    t = _t(0.45)
    f = 600 * np.exp(-t * 9) + 80
    sq = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    n = _lp(_ruido(len(t), seed + 3), 14) * np.exp(-t * 18)
    y = sq * 0.5 + n * 0.6
    g = golpe(seed)
    m = min(len(g), len(y))
    y[:m] += g[:m] * 0.8
    return (y * 0.7).astype(np.float32)


def _silbato(f0, f1, d):
    t = _t(d)
    f = f0 * (f1 / f0) ** (t / d)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 6 * t)
    y = np.sin(2 * np.pi * np.cumsum(f * vib) / SR)
    y += 0.25 * np.sin(2 * 2 * np.pi * np.cumsum(f * vib) / SR)
    return y * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05)


def sorpresa(seed=0):
    """Silbato que sube (la «toma» cartoon cuando a un personaje se le salen los ojos)."""
    return (_silbato(500, 1700, 0.38) * 0.32).astype(np.float32)


def caida(seed=0):
    """Silbato que baja (algo cae del cielo)."""
    return (_silbato(1800, 380, 0.7) * 0.3).astype(np.float32)


def tropiezo(seed=0):
    t = _t(0.18)
    trip = np.sin(2 * np.pi * np.cumsum(900 - 2500 * t) / SR) * np.exp(-t * 14) * 0.3
    g = golpe(seed)
    out = np.zeros(int(SR * 0.6), np.float32)
    out[: len(trip)] += trip
    a = int(SR * 0.17)
    out[a:a + len(g)] += g[: len(out) - a] * 1.2
    return out


def puerta(seed=0):
    """Chirrido + portazo."""
    t = _t(0.45)
    f = 380 + 120 * np.sin(2 * np.pi * 2.2 * t) + 60 * t
    creak = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * _lp(_ruido(len(t), seed), 3) * 0.12 * np.exp(-t * 2)
    slam_t = _t(0.3)
    slam = (_lp(_ruido(len(slam_t), seed + 1), 10) * 0.8 + np.sin(2 * np.pi * 70 * slam_t)) * np.exp(-slam_t * 16)
    out = np.zeros(len(t) + len(slam_t), np.float32)
    out[: len(t)] += creak
    out[len(t) - 1000: len(t) - 1000 + len(slam_t)] += slam * 0.6
    return out


def monedas(seed=0, n=6):
    """Tintineo metálico de varias monedas."""
    rng = np.random.default_rng(seed)
    out = np.zeros(int(SR * (0.15 * n + 0.4)), np.float32)
    for i in range(n):
        t = _t(0.35)
        f = rng.uniform(2800, 4200)
        y = (np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.47 * t) + 0.3 * np.sin(2 * np.pi * f * 2.13 * t))
        y *= np.exp(-t * rng.uniform(14, 22)) * 0.16
        a = int(SR * (i * rng.uniform(0.07, 0.15)))
        out[a:a + len(y)] += y[: len(out) - a]
    return out


def calculadora(seed=0, n=4):
    out = np.zeros(int(SR * (0.1 * n + 0.1)), np.float32)
    rng = np.random.default_rng(seed)
    for i in range(n):
        t = _t(0.06)
        y = np.sign(np.sin(2 * np.pi * rng.choice([1200, 1400, 1600]) * t)) * 0.2 * np.exp(-t * 30)
        a = int(SR * i * 0.1)
        out[a:a + len(y)] += y
    return out


def kaching(seed=0):
    t = _t(0.9)
    bell = (np.sin(2 * np.pi * 2093 * t) + 0.7 * np.sin(2 * np.pi * 3136 * t)) * np.exp(-t * 4) * 0.22
    clack = _lp(_ruido(int(SR * 0.08), seed), 4) * np.exp(-_t(0.08) * 40) * 0.5
    out = np.zeros(len(t) + int(SR * 0.1), np.float32)
    out[: len(clack)] += clack
    a = int(SR * 0.08)
    out[a:a + len(bell)] += bell
    return out


def estrellitas(seed=0):
    out = np.zeros(int(SR * 0.9), np.float32)
    for i, f in enumerate((2637, 3136, 3520, 4186, 3136)):
        t = _t(0.25)
        y = np.sin(2 * np.pi * f * t) * np.exp(-t * 16) * 0.24
        a = int(SR * i * 0.12)
        out[a:a + len(y)] += y[: len(out) - a]
    return out


def redoble(seed=0, d=1.2):
    t = _t(d)
    n = _lp(_ruido(len(t), seed), 3)
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 22 * t)
    return (n * am * np.minimum(1, t / d) * 0.25).astype(np.float32)


def scratch(seed=0):
    """Disco rayado: para el giro (la música se corta)."""
    t = _t(0.35)
    f = 300 + 900 * np.abs(np.sin(2 * np.pi * 2.8 * t))
    y = _lp(_ruido(len(t), seed), 2) * np.sin(2 * np.pi * np.cumsum(f) / SR)
    return (y * 0.35 * np.exp(-t * 3)).astype(np.float32)


def iris(seed=0):
    return (_silbato(900, 300, 0.35) * 0.18).astype(np.float32)


def papel(seed=0):
    t = _t(0.3)
    return (_lp(_ruido(len(t), seed), 2) * np.exp(-t * 10) * 0.25).astype(np.float32)


def rotulador(seed=0, d=1.2):
    """Rotulador sobre papel: roce rápido con golpecitos de trazo (mapas y dibujos que se trazan)."""
    t = _t(max(0.2, d))
    n = _ruido(len(t), seed + 11)
    roce = n - _lp(n, 8)  # agudo
    trazos = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * (5.5 + 1.5 * np.sin(t * 3)) * t))
    fade = np.minimum(1, t / 0.05) * np.minimum(1, (t[-1] - t) / 0.12 + 1e-3)
    return (roce * trazos * fade * 0.22).astype(np.float32)


def bocina(seed=0):
    """Sirena grave de barco."""
    t = _t(0.9)
    y = sum(np.sin(2 * np.pi * f * t) / (i + 1) for i, f in enumerate((110, 220, 330)))
    return (y * np.minimum(1, t / 0.08) * np.minimum(1, (0.9 - t) / 0.25) * 0.18).astype(np.float32)


EFECTOS = {"rotulador": rotulador, "bocina": bocina, "pasos": pasos, "carrera": carrera, "golpe": golpe, "aplastar": aplastar, "tropiezo": tropiezo,
           "sorpresa": sorpresa, "caida": caida, "puerta": puerta, "monedas": monedas, "calculadora": calculadora,
           "kaching": kaching, "estrellitas": estrellitas, "redoble": redoble, "scratch": scratch, "iris": iris,
           "papel": papel}
VOL = {"rotulador": 0.5, "bocina": 0.5, "pasos": 0.5, "carrera": 0.55, "golpe": 0.55, "aplastar": 0.6, "tropiezo": 0.55, "sorpresa": 0.5, "caida": 0.45,
       "puerta": 0.5, "monedas": 0.5, "calculadora": 0.5, "kaching": 0.45, "estrellitas": 0.5, "redoble": 0.4,
       "scratch": 0.5, "iris": 0.4, "papel": 0.4}


def efecto(nombre, seed=0, **kw):
    kw = {k: v for k, v in kw.items() if k in ("d",) and nombre in ("rotulador", "redoble")}
    return EFECTOS[nombre](seed=seed, **kw).astype(np.float32)
