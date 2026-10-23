"""Efectos de sonido y música generados por código (sin licencias de terceros).

Todo a 44,1 kHz, mono, float32 en [-1, 1].
"""
import numpy as np

SR = 44100


def _t(d):
    return np.arange(int(SR * d)) / SR


def _env(n, a=0.005, r=None):
    """Envolvente ataque rápido + caída exponencial."""
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    if r:
        e *= np.exp(-t / r)
    return e


def _lowpass(x, k):
    if k <= 1:
        return x
    return np.convolve(x, np.ones(k) / k, mode="same")


def _noise(n, seed):
    return np.random.default_rng(seed).uniform(-1, 1, n)


# ------------------------------------------------------------------ efectos
def whoosh(d=0.32, seed=0, sube=True):
    """Barrido de ruido filtrado (transiciones)."""
    n = int(SR * d)
    x = _noise(n, seed)
    # filtro variable: mezcla de dos pasabajos según la posición
    a, b = _lowpass(x, 40), _lowpass(x, 6)
    p = np.linspace(0, 1, n) if sube else np.linspace(1, 0, n)
    y = a * (1 - p) + b * p
    env = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.6
    return (y * env * 0.9).astype(np.float32)


def pop(pitch=1.0, seed=0):
    t = _t(0.09)
    f = 520 * pitch * np.exp(-t * 18) + 260 * pitch
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.002, 0.03)
    return (y * 0.55).astype(np.float32)


def impacto(fuerza=1.0, seed=0):
    """Golpe grave tipo tráiler: bombo sub + ruido."""
    t = _t(0.9)
    f = 32 + 90 * np.exp(-t * 12)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    ruido = _lowpass(_noise(len(t), seed), 8) * np.exp(-t * 14) * 0.6
    y = np.tanh((sub + ruido) * 1.8) * 0.8 * fuerza
    return y.astype(np.float32)


def sello(seed=0):
    """Golpe seco de tampón."""
    t = _t(0.25)
    thump = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-t * 20) + 60) / SR) * np.exp(-t * 25)
    clack = _lowpass(_noise(len(t), seed), 3) * np.exp(-t * 60)
    return (np.tanh((thump + clack * 0.8) * 2) * 0.8).astype(np.float32)


def tick(seed=0):
    t = _t(0.025)
    y = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 300) + _noise(len(t), seed) * np.exp(-t * 400) * 0.3
    return (y * 0.35).astype(np.float32)


def contador(d, seed=0):
    """Tictac acelerado mientras sube un contador."""
    out = np.zeros(int(SR * (d + 0.05)), np.float32)
    k = tick(seed)
    pos, step = 0.0, 0.07
    while pos < d:
        i = int(pos * SR)
        out[i:i + len(k)] += k[: len(out) - i]
        pos += step
        step = max(0.03, step * 0.94)
    return out


def caja(seed=0):
    """Caja registradora / monedas: campanitas metálicas."""
    t = _t(0.6)
    rng = np.random.default_rng(seed)
    y = np.zeros(len(t))
    for k in range(6):
        t0 = k * 0.035 + rng.uniform(0, 0.01)
        f = rng.uniform(2200, 4200)
        tt = np.clip(t - t0, 0, None)
        y += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 18) * (t >= t0) * 0.25
    y += np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 6) * 0.35  # «ding»
    return y.astype(np.float32)


def rotulador(d=0.4, seed=0):
    """Chirrido de rotulador al trazar."""
    n = int(SR * d)
    x = _noise(n, seed)
    x = x - _lowpass(x, 12)  # paso alto
    mod = 0.6 + 0.4 * np.sin(2 * np.pi * 9 * np.arange(n) / SR)
    env = np.minimum(1, np.arange(n) / (0.02 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.04 * SR))
    return (x * mod * env * 0.22).astype(np.float32)


def subida(d=1.2, seed=0):
    """Riser de tensión antes del giro."""
    t = _t(d)
    f = 200 * (4 ** (t / d))
    tono = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    ruido = _lowpass(_noise(len(t), seed), 4) * 0.35
    env = (t / d) ** 2
    return ((tono + ruido) * env * 0.7).astype(np.float32)


def error(seed=0):
    """Zumbido de «incorrecto»."""
    t = _t(0.35)
    y = np.sign(np.sin(2 * np.pi * 140 * t)) * 0.3 + np.sign(np.sin(2 * np.pi * 147 * t)) * 0.3
    return (_lowpass(y, 6) * np.exp(-t * 4) * 0.5).astype(np.float32)


def ding(seed=0):
    t = _t(0.7)
    y = (np.sin(2 * np.pi * 1568 * t) + 0.5 * np.sin(2 * np.pi * 2349 * t)) * np.exp(-t * 5)
    return (y * 0.3).astype(np.float32)


def boing(seed=0):
    t = _t(0.4)
    f = 300 + 140 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 6)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * 0.4).astype(np.float32)


def glitch(seed=0):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(6):
        d = rng.uniform(0.015, 0.04)
        t = _t(d)
        out.append(np.sign(np.sin(2 * np.pi * rng.uniform(200, 1800) * t)) * 0.25)
        out.append(np.zeros(int(SR * rng.uniform(0.005, 0.02))))
    return np.concatenate(out).astype(np.float32)


EFECTOS = {"whoosh": whoosh, "pop": pop, "impacto": impacto, "sello": sello, "caja": caja, "rotulador": rotulador,
           "subida": subida, "error": error, "ding": ding, "boing": boing, "glitch": glitch, "tick": tick}


def efecto(nombre, seed=0, **kw):
    return EFECTOS[nombre](seed=seed, **kw)


# ------------------------------------------------------------------ música
def _nota(n):
    return 440.0 * 2 ** (n / 12)


def _kick():
    t = _t(0.35)
    f = 45 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def _hat(seed):
    t = _t(0.05)
    x = _noise(len(t), seed)
    return (x - _lowpass(x, 4)) * np.exp(-t * 90) * 0.5


def _clap(seed):
    t = _t(0.18)
    x = _lowpass(_noise(len(t), seed), 2)
    return x * (np.exp(-t * 30) + 0.6 * np.exp(-np.clip(t - 0.012, 0, None) * 40) * (t > 0.012))


def musica(dur, bpm=104, tono=0, seed=1, silencios=()):
    """Base tensa tipo «investigación»: pulso de bajo, bombo, hi-hat, arpegio menor.

    silencios: lista de (t0, t1) en segundos donde la música se corta (silencios estratégicos).
    """
    rng = np.random.default_rng(seed)
    n = int(SR * (dur + 1))
    out = np.zeros(n)
    beat = 60 / bpm
    # progresión menor: i - VI - III - VII  (en semitonos respecto a A)
    prog = [[0, 3, 7], [-4, 0, 3], [3, 7, 10], [-2, 2, 5]]
    kick, hats, clap = _kick(), [_hat(s) for s in range(4)], _clap(3)

    def put(sig, t0, g=1.0):
        i = int(t0 * SR)
        if i >= n:
            return
        m = min(len(sig), n - i)
        out[i:i + m] += sig[:m] * g

    nbeats = int(dur / beat) + 2
    for b in range(nbeats):
        t0 = b * beat
        bar, pos = divmod(b, 4)
        ch = prog[(bar // 1) % 4]
        root = ch[0] + tono
        put(kick, t0, 0.55 if pos in (0, 2) else 0.0)
        if pos in (1, 3):
            put(clap, t0, 0.18)
        for h in range(2):
            put(hats[(b * 2 + h) % 4], t0 + h * beat / 2, 0.16 if h else 0.08)
        # bajo pulsado en corcheas
        for h in range(2):
            t = _t(beat / 2 * 0.9)
            f = _nota(root - 36)
            s = np.sin(2 * np.pi * f * t) + 0.3 * np.sign(np.sin(2 * np.pi * f * t))
            put(_lowpass(s, 10) * np.exp(-t * 6), t0 + h * beat / 2, 0.22)
        # arpegio en semicorcheas, suave
        for h in range(4):
            note = ch[(b * 4 + h) % 3] + tono + (12 if h == 3 else 0)
            t = _t(beat / 4 * 1.6)
            f = _nota(note - 12)
            s = (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * 3 * f * t)) * np.exp(-t * 14)
            put(s, t0 + h * beat / 4, 0.07)
    # pad de fondo
    t = np.arange(n) / SR
    pad = np.zeros(n)
    bar_len = 4 * beat
    for k in range(int(dur / bar_len) + 2):
        ch = prog[k % 4]
        i0, i1 = int(k * bar_len * SR), min(n, int((k + 1) * bar_len * SR))
        tt = t[i0:i1] - k * bar_len
        env = np.minimum(1, tt / 0.3) * np.minimum(1, (bar_len - tt) / 0.3)
        for note in ch:
            f = _nota(note + tono - 24)
            pad[i0:i1] += (np.sin(2 * np.pi * f * tt) + np.sin(2 * np.pi * f * 1.003 * tt)) * env * 0.035
    out += pad
    # silencios estratégicos con rampas cortas
    g = np.ones(n)
    for a, b in silencios:
        ia, ib = int(a * SR), int(b * SR)
        r = int(0.04 * SR)
        g[max(0, ia - r):ia] = np.minimum(g[max(0, ia - r):ia], np.linspace(1, 0, ia - max(0, ia - r)))
        g[ia:ib] = 0
        g[ib:ib + r] = np.minimum(g[ib:ib + r], np.linspace(0, 1, len(g[ib:ib + r])))
    out *= g
    out = np.tanh(out * 1.2) * 0.8
    return out[: int(SR * dur)].astype(np.float32)
