"""Motor común para las simulaciones hipnóticas: lienzo neón 1080x1920, glow, vídeo y sonido."""
import math, subprocess, wave, os
import numpy as np
import cairo, cv2
from scipy.signal import lfilter

W, H, FPS = 1080, 1920, 60
SR = 44100
BG = (0.02, 0.02, 0.05)
FONT = "Inter"

NEON = [(0.0, 1.0, 0.95), (1.0, 0.2, 0.75), (0.55, 0.35, 1.0), (1.0, 0.85, 0.1),
        (0.2, 1.0, 0.35), (1.0, 0.45, 0.1), (0.25, 0.6, 1.0), (1.0, 0.25, 0.3)]


def hsv(h, s=1.0, v=1.0):
    h = (h % 1.0) * 6
    i = int(h); f = h - i
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    return [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)][i % 6]


class Canvas:
    def __init__(self):
        self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
        self.ctx = cairo.Context(self.surf)
        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        self.ctx.set_line_join(cairo.LINE_JOIN_ROUND)

    def clear(self, col=BG):
        c = self.ctx
        c.save(); c.identity_matrix(); c.set_source_rgb(*col); c.paint(); c.restore()

    def array(self):
        self.surf.flush()
        return np.ndarray((H, W, 4), np.uint8, self.surf.get_data())[:, :, :3]

    def text(self, s, x, y, size, col=(1, 1, 1), weight=cairo.FONT_WEIGHT_BOLD, align="center", alpha=1.0):
        c = self.ctx
        c.save(); c.identity_matrix()
        c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, weight)
        c.set_font_size(size)
        ext = c.text_extents(s)
        if align == "center":
            x = x - ext.width / 2 - ext.x_bearing
        elif align == "right":
            x = x - ext.width - ext.x_bearing
        c.move_to(x, y)
        c.set_source_rgba(*col, alpha)
        c.show_text(s)
        c.restore()


def glow(img, strength=1.0):
    """Bloom en dos escalas sobre BGR uint8."""
    small = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    b1 = cv2.GaussianBlur(small, (0, 0), 3)
    b2 = cv2.GaussianBlur(cv2.resize(small, (W // 16, H // 16), interpolation=cv2.INTER_AREA), (0, 0), 3)
    up1 = cv2.resize(b1, (W, H), interpolation=cv2.INTER_LINEAR)
    up2 = cv2.resize(b2, (W, H), interpolation=cv2.INTER_LINEAR)
    out = cv2.addWeighted(img, 1.0, up1, 0.9 * strength, 0)
    return cv2.addWeighted(out, 1.0, up2, 0.8 * strength, 0)


class Video:
    def __init__(self, path, crf=21):
        self.path = path
        self.tmp = path + ".noaudio.mp4"
        self.p = subprocess.Popen([
            "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
            "-maxrate", "2800k", "-bufsize", "5600k", "-pix_fmt", "yuv420p", self.tmp],
            stdin=subprocess.PIPE)

    def write(self, img):
        self.p.stdin.write(np.ascontiguousarray(img).tobytes())

    def close(self, audio):
        self.p.stdin.close(); self.p.wait()
        wav = self.path + ".wav"
        write_wav(wav, audio)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", self.tmp, "-i", wav,
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                        "-movflags", "+faststart", self.path], check=True)
        os.remove(self.tmp); os.remove(wav)


# ---------------- audio ----------------
class Audio:
    def __init__(self, seconds):
        self.buf = np.zeros(int(seconds * SR) + SR * 3, np.float32)

    def add(self, t, sig, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i < 0 or i >= len(self.buf):
            return
        n = min(len(sig), len(self.buf) - i)
        self.buf[i:i + n] += sig[:n] * gain

    def master(self, reverb=0.25):
        x = self.buf.astype(np.float64)
        if reverb > 0:
            wet = np.zeros_like(x)
            for d, g in [(1557, .82), (1617, .80), (1491, .81), (1422, .79)]:
                wet += lfilter([1], np.r_[1, np.zeros(d - 1), -g], x)
            wet /= 4
            for d in (225, 556):
                wet = lfilter(np.r_[-0.5, np.zeros(d - 1), 1], np.r_[1, np.zeros(d - 1), -0.5], wet)
            x = x + reverb * wet
        peak = np.percentile(np.abs(x), 99.9) + 1e-9
        x = np.tanh(x / peak * 0.9) * 0.89
        return x.astype(np.float32)


_cache = {}


def bell(freq, dur=1.2, bright=0.4):
    key = ("bell", round(freq, 2), dur, bright)
    if key in _cache:
        return _cache[key]
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 4.5) * np.minimum(1, t / 0.003)
    s = (np.sin(2 * np.pi * freq * t) + bright * 0.5 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t * 8)
         + bright * 0.25 * np.sin(2 * np.pi * freq * 3.01 * t) * np.exp(-t * 14))
    _cache[key] = (s * env).astype(np.float32)
    return _cache[key]


def pluck(freq, dur=0.5):
    key = ("pluck", round(freq, 2), dur)
    if key in _cache:
        return _cache[key]
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 9) * np.minimum(1, t / 0.002)
    s = np.sin(2 * np.pi * freq * t + 0.8 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t * 12))
    _cache[key] = (s * env).astype(np.float32)
    return _cache[key]


def click(seed=0, dur=0.04, tone=2500):
    key = ("click", seed % 8, dur, tone)
    if key in _cache:
        return _cache[key]
    rng = np.random.default_rng(seed % 8)
    t = np.arange(int(dur * SR)) / SR
    n = rng.standard_normal(len(t))
    n = lfilter([1, -0.6], [1], n)
    s = (0.6 * n + np.sin(2 * np.pi * tone * t)) * np.exp(-t * 120)
    _cache[key] = (s * 0.5).astype(np.float32)
    return _cache[key]


def thud(freq=90, dur=0.25):
    key = ("thud", round(freq), dur)
    if key in _cache:
        return _cache[key]
    t = np.arange(int(dur * SR)) / SR
    f = freq * (1 + 1.5 * np.exp(-t * 40))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 18)
    _cache[key] = s.astype(np.float32)
    return _cache[key]


def crack(seed=0, dur=0.12):
    key = ("crack", seed % 12, dur)
    if key in _cache:
        return _cache[key]
    rng = np.random.default_rng(100 + seed % 12)
    t = np.arange(int(dur * SR)) / SR
    n = rng.standard_normal(len(t))
    n = lfilter([1, -0.95], [1], n)  # brillante
    s = n * np.exp(-t * 45) * (0.6 + 0.4 * (rng.random(len(t)) > 0.7))
    _cache[key] = (s * 0.35).astype(np.float32)
    return _cache[key]


def write_wav(path, x):
    st = np.stack([x, x], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())


PENTA = [0, 2, 4, 7, 9]


def penta_freq(i, base=261.63):
    o, k = divmod(i, 5)
    return base * 2 ** (o + PENTA[k] / 12)


def midi(n):
    return 440 * 2 ** ((n - 69) / 12)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)
