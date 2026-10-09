"""Música de fondo y efectos generados por código (sin licencias de terceros)."""
import numpy as np

SR = 44100


def _note(n):  # n = semitonos desde A4
    return 440.0 * 2 ** (n / 12)


def _pluck(freq, dur, rng):
    """Karplus-Strong: cuerda pulsada suave."""
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, period)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % period]
        buf[i % period] = 0.996 * 0.5 * (buf[i % period] + buf[(i + 1) % period])
    return out * np.exp(-np.linspace(0, 4, n))


def background(duration, bpm=92, seed=1):
    """Base tranquila y curiosa: pad + arpegio + percusión muy suave."""
    rng = np.random.default_rng(seed)
    total = int(SR * (duration + 1))
    out = np.zeros(total)
    beat = 60 / bpm
    bar = 4 * beat
    # Am - F - C - G (semitonos relativos a A4, acordes en registro medio)
    chords = [[-12, -9, -5], [-16, -12, -9], [-21, -17, -14 + 12], [-14, -10, -7]]
    t_bar = np.arange(int(SR * bar)) / SR
    env = np.minimum(1, t_bar / 0.6) * np.minimum(1, (bar - t_bar) / 0.6)
    k = 0
    pos = 0
    pluck_cache = {}
    while pos < total:
        ch = chords[k % 4]
        seg = np.zeros(len(t_bar))
        for n in ch:
            f = _note(n)
            for det in (-0.08, 0.08):
                seg += np.sin(2 * np.pi * (f + det) * t_bar) * 0.10
                seg += np.sin(2 * np.pi * 2 * (f + det) * t_bar) * 0.025
        seg += np.sin(2 * np.pi * _note(ch[0] - 12) * t_bar) * 0.12  # bajo
        seg *= env
        end = min(total, pos + len(seg))
        out[pos:end] += seg[: end - pos]
        # arpegio en corcheas
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12, ch[1] + 12, ch[2] + 12]
        for i, n in enumerate(arp):
            st = pos + int(i * beat / 2 * SR)
            if st >= total:
                break
            if n not in pluck_cache:
                pluck_cache[n] = _pluck(_note(n), beat * 1.5, rng)
            p = pluck_cache[n] * (0.16 if i % 2 == 0 else 0.10)
            e = min(total, st + len(p))
            out[st:e] += p[: e - st]
        # percusión: bombo suave en 1 y 3, shaker en contratiempos
        for b in range(4):
            st = pos + int(b * beat * SR)
            if st >= total:
                break
            if b in (0, 2):
                tt = np.arange(int(0.25 * SR)) / SR
                kick = np.sin(2 * np.pi * (50 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14) * 0.22
                e = min(total, st + len(kick))
                out[st:e] += kick[: e - st]
            st2 = st + int(beat / 2 * SR)
            if st2 < total:
                tt = np.arange(int(0.06 * SR)) / SR
                sh = rng.normal(0, 1, len(tt)) * np.exp(-tt * 70) * 0.035
                sh = np.diff(np.concatenate([[0], sh]))  # agudos
                e = min(total, st2 + len(sh))
                out[st2:e] += sh[: e - st2]
        pos += len(seg)
        k += 1
    out = out[: int(SR * duration)]
    fade = int(SR * 1.5)
    out[:int(SR * 0.3)] *= np.linspace(0, 1, int(SR * 0.3))
    out[-fade:] *= np.linspace(1, 0, fade)
    out /= np.abs(out).max() + 1e-9
    return (out * 0.8).astype(np.float32)


def scribble(duration, intervals, seed=2):
    """Sonido de rotulador sobre papel durante los intervalos de dibujo."""
    rng = np.random.default_rng(seed)
    out = np.zeros(int(SR * (duration + 1)))
    for t0, t1 in intervals:
        a, b = int(t0 * SR), int(t1 * SR)
        if b <= a:
            continue
        n = b - a
        noise = rng.normal(0, 1, n)
        noise = np.diff(np.concatenate([[0], noise]))  # paso alto
        k = 12
        noise = np.convolve(noise, np.ones(k) / k, mode="same")  # quita lo más agudo
        tt = np.arange(n) / SR
        rate = rng.uniform(7, 12)
        am = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * rate * tt + rng.uniform(0, 6)))
        ramp = np.minimum(1, np.minimum(tt / 0.04, (tt[-1] - tt) / 0.06 + 1e-9))
        out[a:b] += noise * am * ramp
    out = out[: int(SR * duration)]
    m = np.abs(out).max()
    return (out / m * 0.6 if m > 0 else out).astype(np.float32)
