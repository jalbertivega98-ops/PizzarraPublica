"""Banda sonora por momentos (generada por código, sin licencias): cada escena elige un ánimo con "musica".

Ánimos: curioso (por defecto), alegre, comico, tension, triste, final; "corte" = silencio dramático hasta la voz.
Todo en la misma tonalidad (Do mayor / La menor) para que los fundidos entre escenas suenen naturales.
La voz baja la música automáticamente (ducking) en make_video.build_audio.
"""
import numpy as np

SR = 44100
A4 = 440.0


def _f(n):  # semitonos desde La 4
    return A4 * 2 ** (n / 12)


def _nota(freq, d, timbre="pluck", vol=1.0):
    t = np.arange(int(SR * d)) / SR
    if timbre == "pluck":  # cuerda pulsada / marimba suave
        y = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t) + 0.12 * np.sin(6 * np.pi * freq * t)
        y *= np.exp(-t * 7)
    elif timbre == "xilo":
        y = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * freq * 3.9 * t) * np.exp(-t * 30)
        y *= np.exp(-t * 11)
    elif timbre == "bajo":
        y = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
        y *= np.minimum(1, t / 0.01) * np.exp(-t * 4)
    elif timbre == "tuba":  # bajo cómico «oom-pah»
        y = np.tanh(2.2 * np.sin(2 * np.pi * freq * t)) * np.minimum(1, t / 0.02) * np.exp(-t * 7)
    elif timbre == "pad":
        y = sum(np.sin(2 * np.pi * freq * (1 + dt) * t) for dt in (-0.004, 0, 0.004)) / 3
        y *= np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.4)
    elif timbre == "piano":
        y = (np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(4 * np.pi * freq * t) * np.exp(-t * 3)
             + 0.2 * np.sin(6 * np.pi * freq * t) * np.exp(-t * 5))
        y *= np.exp(-t * 2.5) * np.minimum(1, t / 0.005)
    else:
        y = np.sin(2 * np.pi * freq * t)
    return (y * vol).astype(np.float32)


def _kick(vol=1.0):
    t = np.arange(int(SR * 0.25)) / SR
    return (np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 14) * vol).astype(np.float32)


def _hat(vol=1.0, seed=0):
    t = np.arange(int(SR * 0.05)) / SR
    n = np.random.default_rng(seed).uniform(-1, 1, len(t))
    n = n - np.convolve(n, np.ones(4) / 4, mode="same")  # paso alto
    return (n * np.exp(-t * 80) * vol).astype(np.float32)


def _snap(vol=1.0, seed=1):
    t = np.arange(int(SR * 0.12)) / SR
    n = np.random.default_rng(seed).uniform(-1, 1, len(t))
    return (n * np.exp(-t * 35) * vol * 0.6).astype(np.float32)


# acordes (semitonos desde La 4): C, G, Am, F, Dm, Em
AC = {"C": [-9, -5, -2], "G": [-14, -10, -7], "Am": [-12, -9, -5], "F": [-16, -12, -9], "Dm": [-19, -16, -12],
      "Em": [-17, -14, -10], "E": [-17, -13, -10]}
RAIZ = {"C": -21, "G": -26, "Am": -24, "F": -28, "Dm": -31, "Em": -29, "E": -29}

ANIMOS = {
    "curioso": dict(bpm=96, prog=["Am", "F", "C", "G"], arpe="pluck", bajo="bajo", bat="suave", pad=0.25),
    "alegre": dict(bpm=112, prog=["C", "G", "Am", "F"], arpe="pluck", bajo="bajo", bat="pop", pad=0.2),
    "comico": dict(bpm=124, prog=["C", "G", "C", "G"], arpe="xilo", bajo="tuba", bat="comico", pad=0.0),
    "tension": dict(bpm=100, prog=["Am", "Am", "F", "E"], arpe="pluck", bajo="pulso", bat="tension", pad=0.4),
    "triste": dict(bpm=72, prog=["Am", "F", "C", "E"], arpe="piano", bajo="bajo", bat=None, pad=0.45),
    "final": dict(bpm=116, prog=["F", "G", "C", "Am"], arpe="pluck", bajo="bajo", bat="pop", pad=0.3),
}


def _mezcla(out, x, a, g=1.0):
    if a >= len(out) or a < 0:
        return
    m = min(len(x), len(out) - a)
    out[a:a + m] += x[:m] * g


def tramo(animo, d, seed=1):
    """d segundos de música en ese ánimo (empezando en compás)."""
    cfg = ANIMOS.get(animo, ANIMOS["curioso"])
    beat = 60 / cfg["bpm"]
    out = np.zeros(int(SR * (d + 2)), np.float32)
    rng = np.random.default_rng(seed)
    b = 0
    while b * beat < d + beat:
        ac = cfg["prog"][(b // 4) % len(cfg["prog"])]
        a = int(SR * b * beat)
        notas = AC[ac]
        # arpegio en corcheas
        for k in range(2):
            n = notas[(b * 2 + k) % 3] + (12 if (b * 2 + k) % 4 == 3 else 0) + 12
            if cfg["arpe"] == "piano" and k == 1:
                continue
            _mezcla(out, _nota(_f(n), beat * 1.5, cfg["arpe"], 0.13), a + int(SR * k * beat / 2))
        # bajo
        r = RAIZ[ac]
        if cfg["bajo"] == "tuba":
            _mezcla(out, _nota(_f(r if b % 2 == 0 else r + 7), beat * 0.6, "tuba", 0.22), a)
        elif cfg["bajo"] == "pulso":
            for k in range(2):
                _mezcla(out, _nota(_f(r), beat * 0.45, "bajo", 0.2), a + int(SR * k * beat / 2))
        elif b % 2 == 0:
            _mezcla(out, _nota(_f(r), beat * 2, "bajo", 0.22), a)
        # pad cada compás
        if cfg["pad"] and b % 4 == 0:
            for n in notas:
                _mezcla(out, _nota(_f(n), beat * 4.1, "pad", cfg["pad"] * 0.12), a)
        # batería
        bat = cfg["bat"]
        if bat == "pop":
            if b % 2 == 0:
                _mezcla(out, _kick(0.5), a)
            else:
                _mezcla(out, _snap(0.25, b), a)
            _mezcla(out, _hat(0.12, b), a + int(SR * beat / 2))
        elif bat == "suave":
            if b % 4 == 0:
                _mezcla(out, _kick(0.32), a)
            _mezcla(out, _hat(0.07, b), a + int(SR * beat / 2))
        elif bat == "comico":
            _mezcla(out, _hat(0.12, b), a)
            if b % 2 == 1:
                _mezcla(out, _snap(0.2, b), a)
        elif bat == "tension":
            _mezcla(out, _kick(0.42), a)
            if b % 4 == 3:
                for k in range(4):  # redoble corto
                    _mezcla(out, _snap(0.12, b + k), a + int(SR * k * beat / 4))
        b += 1
    return out[: int(SR * d)]


def partitura(story, scenes, total):
    """Pista completa: cada escena toma su ánimo de una pista continua de ese ánimo, con fundidos de 0,35 s."""
    n = int(SR * (total + 1))
    out = np.zeros(n, np.float32)
    fade = int(SR * 0.35)
    pistas = {}
    previo = "curioso"
    for i, (spec, sc) in enumerate(zip(story["scenes"], scenes)):
        animo = spec.get("animo") or (spec.get("musica") if spec.get("musica") in ANIMOS else None) or previo
        if animo not in pistas:
            pistas[animo] = tramo(animo, total + 1, seed=len(pistas) + 1)
        x = pistas[animo]
        a, b = int(sc["start"] * SR), min(n, int(sc["end"] * SR) + fade)
        seg = x[a:b].copy()
        if i > 0 and animo != previo:
            seg[:fade] *= np.linspace(0, 1, min(fade, len(seg)))
        if i + 1 < len(scenes):
            sig = story["scenes"][i + 1]
            sig_animo = sig.get("animo") or (sig.get("musica") if sig.get("musica") in ANIMOS else None) or animo
            if sig_animo != animo:
                seg[-fade:] *= np.linspace(1, 0, min(fade, len(seg)))
            else:
                seg = seg[: len(seg) - fade]
        out[a:a + len(seg)] += seg
        previo = animo
    peak = np.abs(out).max() or 1
    return out[: int(SR * total)] / peak * 0.8


def ducking(musica, voz, sr_voz, sr=SR, cantidad=0.6):
    """Baja la música mientras habla la voz (envolvente con ataque 40 ms y relajación 300 ms)."""
    v = np.abs(voz.astype(np.float32))
    win = max(1, int(sr_voz * 0.05))
    rms = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, mode="same"))
    act = np.clip(rms / (rms.max() * 0.15 + 1e-6), 0, 1)
    # a la frecuencia de la música
    idx = np.linspace(0, len(act) - 1, len(musica)).astype(int) if len(act) else np.zeros(len(musica), int)
    act = act[idx] if len(act) else np.zeros(len(musica))
    g = np.empty(len(act), np.float32)
    at, rel = np.exp(-1 / (0.04 * sr)), np.exp(-1 / (0.3 * sr))
    cur = 0.0
    # seguimiento de envolvente (por bloques para ir rápido)
    blk = 256
    for i in range(0, len(act), blk):
        tgt = act[i:i + blk].max()
        k = at ** blk if tgt > cur else rel ** blk
        cur = tgt + (cur - tgt) * k
        g[i:i + blk] = cur
    return musica * (1 - cantidad * g)
