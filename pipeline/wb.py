"""Motor de animación whiteboard: trazos que se dibujan progresivamente.

Cada elemento del storyboard se compila a una lista de trazos (polilíneas con
temblor de mano) y, opcionalmente, rellenos que aparecen al terminar el contorno.
El render usa skia-python (antialiasing, trazos redondeados) a 1080x1920.
"""
import math
import os

import numpy as np
import skia

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "assets", "fonts")

# ---------------------------------------------------------------- identidad
PALETTE = {
    "paper": (251, 248, 241),
    "ink": (31, 36, 48),
    "blue": (46, 107, 230),
    "red": (229, 83, 61),
    "yellow": (255, 212, 71),
    "green": (47, 163, 107),
    "gray": (150, 154, 162),
    "light": (215, 218, 224),
    "white": (255, 255, 255),
    # colores de identificación de partido (solo para nombrarlos)
    "psoe": (225, 30, 40),
    "pp": (0, 104, 180),
    "vox": (90, 175, 40),
    "sumar": (214, 32, 112),
}
FONTS = {
    "hand": "Kalam-Bold.ttf",
    "hand_regular": "Kalam-Regular.ttf",
    "body": "PatrickHand-Regular.ttf",
    "sub": "Poppins-ExtraBold.ttf",
    "ui": "Poppins-SemiBold.ttf",
}
_tf_cache = {}


def typeface(name):
    if name not in _tf_cache:
        _tf_cache[name] = skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, FONTS[name]))
    return _tf_cache[name]


def font(name, size):
    f = skia.Font(typeface(name), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def rgb(c, a=255):
    if isinstance(c, str):
        c = PALETTE[c]
    return skia.Color(c[0], c[1], c[2], a)


# Colores de detalle dentro de los iconos (papeleta, aguja del reloj, calendario…).
# Las series por partido los neutralizan para que solo el partido lleve color.
ICON_ACCENT = {}


def acc(c):
    return ICON_ACCENT.get(c, c)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


# ---------------------------------------------------------------- geometría
class Stroke:
    def __init__(self, pts, color="ink", width=7, alpha=255):
        self.pts = np.asarray(pts, dtype=float)
        self.color, self.width, self.alpha = color, width, alpha
        seg = np.diff(self.pts, axis=0)
        self.seglen = np.hypot(seg[:, 0], seg[:, 1]) if len(self.pts) > 1 else np.zeros(0)
        self.length = float(self.seglen.sum()) + 1e-6


class Fill:
    def __init__(self, pts, color, alpha=255):
        self.pts = np.asarray(pts, dtype=float)
        self.color, self.alpha = color, alpha


def wobble(pts, rng, amp=1.6, step=10.0):
    """Subdivide y añade un temblor suave para que parezca hecho a mano."""
    pts = np.asarray(pts, dtype=float)
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(np.hypot(*(b - a)) / step))
        for i in range(1, n + 1):
            out.append(a + (b - a) * i / n)
    out = np.array(out)
    if amp <= 0 or len(out) < 3:
        return out
    t = np.linspace(0, 1, len(out))
    ph = rng.uniform(0, 2 * np.pi, 4)
    fr = rng.uniform(1.0, 3.0, 2)
    off = np.stack([np.sin(2 * np.pi * fr[0] * t + ph[0]) + 0.4 * np.sin(9 * t + ph[1]),
                    np.sin(2 * np.pi * fr[1] * t + ph[2]) + 0.4 * np.sin(11 * t + ph[3])], 1)
    return out + off * amp


def ellipse_pts(cx, cy, rx, ry, a0=-90, sweep=370, n=72):
    a = np.radians(np.linspace(a0, a0 + sweep, n))
    return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)


def rect_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y - 2)]


def arc_pts(cx, cy, r, a0, a1, n=40):
    a = np.radians(np.linspace(a0, a1, n))
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)


def arrow_strokes(p0, p1, color="ink", width=7, curve=0.15, head=34, rng=None):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    nrm = np.array([-d[1], d[0]])
    ctrl = (p0 + p1) / 2 + nrm * curve
    t = np.linspace(0, 1, 40)[:, None]
    body = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * ctrl + t ** 2 * p1
    tang = body[-1] - body[-4]
    ang = math.atan2(tang[1], tang[0])
    h1 = p1 + head * np.array([math.cos(ang + 2.6), math.sin(ang + 2.6)])
    h2 = p1 + head * np.array([math.cos(ang - 2.6), math.sin(ang - 2.6)])
    return [Stroke(wobble(body, rng, 1.2), color, width),
            Stroke(wobble([h1, p1, h2], rng, 0.8), color, width)]


# ---------------------------------------------------------------- iconos
# Cada icono se define en un cuadro de ~200x200 centrado en (0,0) y devuelve
# (strokes, fills) en coordenadas locales. Se escala y traslada al compilar.

def icon_person(color="ink", accent=None, tie=False, smile=True, rng=None):
    S = []
    S.append(Stroke(ellipse_pts(0, -62, 34, 36), color, 7))
    S.append(Stroke([(-12, -66), (-11, -60)], color, 8))
    S.append(Stroke([(12, -66), (13, -60)], color, 8))
    if smile:
        S.append(Stroke(arc_pts(0, -56, 14, 20, 160), color, 6))
    body = [(-50, 95), (-48, 20), (-30, -14), (30, -14), (48, 20), (50, 95)]
    S.append(Stroke(body, color, 7))
    fills = [Fill([(-48, 95), (-46, 20), (-29, -12), (29, -12), (46, 20), (48, 95)], accent or "light", 255)]
    if tie:
        S.append(Stroke([(0, -12), (-9, 2), (0, 48), (9, 2), (0, -12)], color, 5))
        fills.append(Fill([(0, -12), (-9, 2), (0, 48), (9, 2)], "yellow"))
    return S, fills


def icon_ballot_box(color="ink", rng=None):
    S = [Stroke(rect_pts(-110, -40, 220, 150), color, 8),
         Stroke([(-110, -40), (-70, -80), (110, -80), (110, -40)], color, 8),
         Stroke([(-40, -60), (60, -60)], color, 10),
         Stroke(rect_pts(-30, -150, 70, 80), acc("blue"), 6),
         Stroke([(-14, -125), (24, -125)], acc("blue"), 5),
         Stroke([(-14, -105), (24, -105)], acc("blue"), 5)]
    F = [Fill(rect_pts(-110, -40, 220, 150)[:4], "light")]
    return S, F


def icon_ballot(color="ink", rng=None):
    S = [Stroke(rect_pts(-80, -105, 160, 210), color, 7)]
    for i in range(4):
        y = -60 + i * 42
        S.append(Stroke(ellipse_pts(-50, y, 9, 9), color, 5))
        S.append(Stroke([(-28, y), (60, y)], "gray", 6))
    F = [Fill(rect_pts(-80, -105, 160, 210)[:4], "white")]
    return S, F


def icon_crown(color="ink", rng=None):
    pts = [(-80, 40), (-90, -40), (-45, 0), (0, -60), (45, 0), (90, -40), (80, 40), (-80, 40)]
    S = [Stroke(pts, color, 7), Stroke([(-82, 60), (82, 60)], color, 7)]
    for x, y in [(-90, -40), (0, -60), (90, -40)]:
        S.append(Stroke(ellipse_pts(x, y - 12, 9, 9), acc("red"), 5))
    return S, [Fill(pts[:-1], "yellow")]


def icon_bubble(color="ink", text_dots=True, rng=None):
    pts = list(ellipse_pts(0, 0, 90, 60, a0=110, sweep=330, n=60)) + [(-50, 80), (-30, 55)]
    S = [Stroke(pts, color, 7)]
    if text_dots:
        for x in (-30, 0, 30):
            S.append(Stroke(ellipse_pts(x, 0, 6, 6, n=16), color, 8))
    return S, [Fill(ellipse_pts(0, 0, 88, 58), "white")]


def icon_lectern(color="ink", rng=None):
    S = [Stroke([(-90, -20), (90, -20), (60, 140), (-60, 140), (-90, -20)], color, 8),
         Stroke([(-100, -20), (100, -20)], color, 10),
         Stroke([(0, -20), (-20, -70)], "gray", 6),
         Stroke(ellipse_pts(-24, -78, 10, 10, n=20), "gray", 6)]
    return S, [Fill([(-90, -20), (90, -20), (60, 140), (-60, 140)], acc("blue"), 200)]


def icon_document(color="ink", rng=None):
    S = [Stroke([(-70, -95), (40, -95), (70, -65), (70, 95), (-70, 95), (-70, -95)], color, 7),
         Stroke([(40, -95), (40, -65), (70, -65)], color, 6)]
    for i in range(5):
        S.append(Stroke([(-45, -45 + i * 30), (45 - (i == 4) * 40, -45 + i * 30)], "gray", 6))
    return S, [Fill([(-70, -95), (40, -95), (70, -65), (70, 95), (-70, 95)], "white")]


def icon_clock(color="ink", rng=None):
    S = [Stroke(ellipse_pts(0, 0, 80, 80), color, 8),
         Stroke([(0, 0), (0, -50)], color, 8), Stroke([(0, 0), (38, 18)], acc("red"), 8)]
    return S, [Fill(ellipse_pts(0, 0, 78, 78), "white")]


def icon_calendar(color="ink", rng=None):
    S = [Stroke(rect_pts(-110, -90, 220, 190), color, 8),
         Stroke([(-110, -40), (110, -40)], color, 7),
         Stroke([(-60, -110), (-60, -70)], color, 9), Stroke([(60, -110), (60, -70)], color, 9)]
    F = [Fill(rect_pts(-110, -90, 220, 50)[:4], acc("red"), 230), Fill(rect_pts(-110, -40, 220, 140)[:4], "white")]
    return S, F


def icon_loop(color="blue", rng=None):
    arc = arc_pts(0, 0, 80, -60, 230)
    tip, prev = arc[-1], arc[-3]
    ang = math.atan2(tip[1] - prev[1], tip[0] - prev[0])
    h1 = tip + 26 * np.array([math.cos(ang + 2.5), math.sin(ang + 2.5)])
    h2 = tip + 26 * np.array([math.cos(ang - 2.5), math.sin(ang - 2.5)])
    return [Stroke(arc, color, 9), Stroke([h1, tip, h2], color, 9)], []


def icon_question(color="blue", rng=None):
    S = [Stroke(list(arc_pts(0, -60, 55, 190, 400, 40)) + [(10, 20), (0, 50)], color, 22),
         Stroke(ellipse_pts(0, 100, 6, 6, n=16), color, 26)]
    return S, []


def icon_handshake(color="ink", rng=None):
    S = [Stroke([(-120, 10), (-60, -20), (-10, -20), (30, 10)], color, 8),
         Stroke([(120, 10), (60, -20), (20, -20), (-20, 15), (10, 35)], color, 8),
         Stroke([(-60, 40), (-30, 60), (0, 55), (30, 30)], color, 8),
         Stroke([(-150, 0), (-120, 10), (-100, 60), (-130, 70)], "blue", 8),
         Stroke([(150, 0), (120, 10), (100, 60), (130, 70)], "red", 8)]
    return S, []


def icon_house(color="ink", rng=None):
    S = [Stroke([(-110, -10), (0, -110), (110, -10)], color, 9),
         Stroke([(-80, -30), (-80, 100), (80, 100), (80, -30)], color, 9),
         Stroke(rect_pts(-25, 35, 50, 65), color, 7),
         Stroke(rect_pts(30, -5, 32, 30), color, 6)]
    return S, [Fill([(-80, -30), (0, -100), (80, -30), (80, 100), (-80, 100)], "white"),
               Fill(rect_pts(-25, 35, 50, 65)[:4], "yellow")]


def icon_euro(color="ink", rng=None):
    S = [Stroke(arc_pts(10, 0, 70, 45, 315, 40), color, 10),
         Stroke([(-80, -18), (20, -18)], color, 9), Stroke([(-80, 18), (20, 18)], color, 9)]
    return S, []


def icon_crane(color="ink", rng=None):
    """Grúa de obra: mástil en celosía, pluma, contrapeso y gancho con una carga."""
    S = [Stroke([(-30, 160), (-30, -140)], color, 8), Stroke([(10, 160), (10, -140)], color, 8)]
    for i in range(6):
        y = 160 - i * 50
        S.append(Stroke([(-30, y), (10, y - 50)], color, 5))
    S += [Stroke([(-120, -140), (190, -140)], color, 9),
          Stroke([(-10, -190), (-120, -140)], color, 6), Stroke([(-10, -190), (190, -140)], color, 6),
          Stroke([(-10, -190), (-10, -140)], color, 7),
          Stroke([(150, -140), (150, -20)], color, 4),
          Stroke(rect_pts(120, -20, 60, 40), color, 6),
          Stroke([(-60, 160), (40, 160)], color, 10)]
    return S, [Fill(rect_pts(-120, -150, 50, 40)[:4], "gray"), Fill(rect_pts(120, -20, 60, 40)[:4], acc("yellow"))]


ICONS = {
    "house": icon_house, "crane": icon_crane, "euro": icon_euro,
    "person": icon_person, "ballot_box": icon_ballot_box, "ballot": icon_ballot,
    "crown": icon_crown, "bubble": icon_bubble, "lectern": icon_lectern,
    "document": icon_document, "clock": icon_clock, "calendar": icon_calendar,
    "loop": icon_loop, "question": icon_question, "handshake": icon_handshake,
}


# ---------------------------------------------------------------- elementos
class Element:
    """Un elemento del storyboard con su ventana de tiempo dentro de la escena."""

    def __init__(self, spec, t0, rng):
        self.spec = spec
        self.kind = spec["type"]
        self.t0 = t0
        self.dur = float(spec.get("dur", 0.8))
        self.out = spec.get("out_t")
        self.strokes, self.fills = [], []
        self.compile(rng)
        self.total = sum(s.length for s in self.strokes) or 1.0

    # -- compilación a trazos
    def compile(self, rng):
        s, k = self.spec, self.kind
        col = s.get("color", "ink")
        if k == "icon":
            kwargs = {kk: s[kk] for kk in ("accent", "tie", "smile") if kk in s}
            st, fi = ICONS[s["name"]](color=col, rng=rng, **kwargs) if s["name"] == "person" else ICONS[s["name"]](color=col, rng=rng)
            sc, x, y = s.get("scale", 1.0), s["x"], s["y"]
            flip = -1 if s.get("flip") else 1
            for o in st:
                pts = o.pts * [sc * flip, sc] + [x, y]
                self.strokes.append(Stroke(wobble(pts, rng, 1.3), o.color, o.width * max(0.7, sc ** 0.5), o.alpha))
            if "fill" in s and fi:
                fi[0] = Fill(fi[0].pts, s["fill"], fi[0].alpha)
            for f in fi:
                self.fills.append(Fill(f.pts * [sc * flip, sc] + [x, y], f.color, f.alpha))
        elif k == "arrow":
            self.strokes += arrow_strokes(s["from"], s["to"], col, s.get("width", 7), s.get("curve", 0.15), s.get("head", 34), rng)
        elif k == "line":
            self.strokes.append(Stroke(wobble(s["pts"], rng, 1.2), col, s.get("width", 7)))
        elif k == "rect":
            x, y, w, h = s["box"]
            self.strokes.append(Stroke(wobble(rect_pts(x, y, w, h), rng, 1.4), col, s.get("width", 7)))
            if "fill" in s:
                self.fills.append(Fill(rect_pts(x, y, w, h)[:4], s["fill"], s.get("fill_alpha", 255)))
        elif k == "circle":
            self.strokes.append(Stroke(wobble(ellipse_pts(s["x"], s["y"], s["rx"], s.get("ry", s["rx"]), a0=rng.uniform(-150, -30), sweep=380), rng, 2.0), col, s.get("width", 8)))
        elif k == "cross":
            x, y, r = s["x"], s["y"], s.get("r", 120)
            self.strokes += [Stroke(wobble([(x - r, y - r), (x + r, y + r)], rng, 2), col, s.get("width", 18)),
                             Stroke(wobble([(x + r, y - r), (x - r, y + r)], rng, 2), col, s.get("width", 18))]
        elif k == "check":
            x, y, r = s["x"], s["y"], s.get("r", 60)
            self.strokes.append(Stroke(wobble([(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)], rng, 1.5), col, s.get("width", 16)))
        elif k == "underline":
            x0, x1, y = s["x0"], s["x1"], s["y"]
            self.strokes.append(Stroke(wobble([(x0, y), (x1, y + 4)], rng, 2.5), col, s.get("width", 8)))
        elif k == "highlight":
            x0, x1, y = s["x0"], s["x1"], s["y"]
            self.strokes.append(Stroke(wobble([(x0, y), (x1, y - 3)], rng, 1.5), s.get("color", "yellow"), s.get("width", 60), 150))
        elif k == "hemicycle":
            self.dots = self._hemi_dots(s)
        elif k == "stamp":
            # sello de goma: doble marco girado; el texto aparece al cerrar el marco
            x, y, w, h = s["x"], s["y"], s.get("w", 520), s.get("h", 130)
            a = math.radians(s.get("rotate", -6))
            rot = lambda pts: [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]
            self.strokes.append(Stroke(wobble(rot(rect_pts(-w / 2, -h / 2, w, h)), rng, 1.2), col, 8))
            self.strokes.append(Stroke(wobble(rot(rect_pts(-w / 2 + 12, -h / 2 + 12, w - 24, h - 24)), rng, 1.0), col, 3))
        # text / bars / counter se dibujan con su propia rutina

    @staticmethod
    def _hemi_dots(s):
        n, cx, cy = s.get("count", 350), s["x"], s["y"]
        r0, r1 = s.get("r_in", 120), s.get("r_out", 380)
        rows = s.get("rows", 10)
        radii = np.linspace(r0, r1, rows)
        weights = radii / radii.sum()
        counts = np.floor(weights * n).astype(int)
        counts[-1] += n - counts.sum()
        dots = []
        for r, c in zip(radii, counts):
            for i in range(c):
                a = math.pi - math.pi * (i + 0.5) / c
                dots.append((a, cx + r * math.cos(a), cy - r * math.sin(a)))
        dots.sort(key=lambda d: -d[0])  # de izquierda a derecha
        return [(x, y) for _, x, y in dots]

    # -- render
    def progress(self, t):
        if self.dur <= 0:
            return 1.0 if t >= self.t0 else 0.0
        return min(max((t - self.t0) / self.dur, 0.0), 1.0)

    def alpha_mult(self, t):
        if self.out is None or t < self.out:
            return 1.0
        return max(0.0, 1 - (t - self.out) / 0.25)

    def draw(self, c, t):
        """Dibuja el elemento; devuelve la posición de la punta del rotulador si está dibujando."""
        p = self.progress(t)
        am = self.alpha_mult(t)
        if p <= 0 or am <= 0:
            return None
        k = self.kind
        if k == "text":
            return self._draw_text(c, p, am)
        if k == "hemicycle":
            return self._draw_hemi(c, p, am)
        if k == "bars":
            return self._draw_bars(c, p, am)
        if k == "counter":
            return self._draw_counter(c, p, am)
        if k == "gauge":
            return self._draw_gauge(c, p, am)
        if k == "linechart":
            return self._draw_linechart(c, t, am)
        # rellenos (aparecen al final del contorno)
        fp = ease(min(1.0, (p - 0.75) / 0.25)) if self.fills else 0
        for f in self.fills:
            if fp > 0:
                path = skia.Path()
                path.addPoly([skia.Point(*q) for q in f.pts], True)
                c.drawPath(path, skia.Paint(Color=rgb(f.color, int(f.alpha * fp * am * 0.9)), AntiAlias=True))
        target = p * self.total
        tip = None
        acc = 0.0
        for s in self.strokes:
            if acc >= target:
                break
            remain = target - acc
            pts = s.pts
            if remain < s.length:
                cum = np.concatenate([[0], np.cumsum(s.seglen)])
                i = int(np.searchsorted(cum, remain)) - 1
                i = max(0, min(i, len(pts) - 2))
                f = (remain - cum[i]) / (s.seglen[i] + 1e-9)
                end = pts[i] + (pts[i + 1] - pts[i]) * f
                pts = np.vstack([pts[: i + 1], end])
                tip = end
            draw_poly(c, pts, s.color, s.width, int(s.alpha * am))
            acc += s.length
        if p < 1 and tip is None and self.strokes:
            tip = self.strokes[-1].pts[-1]
        if k == "stamp":
            self._draw_stamp_text(c, p, am)
        return tip if p < 1 else None

    def _draw_stamp_text(self, c, p, am):
        s = self.spec
        ta = ease(min(1.0, max(0.0, (p - 0.6) / 0.4)))
        if ta <= 0:
            return
        c.save()
        c.rotate(s.get("rotate", -6), s["x"], s["y"])
        f = font("ui", s.get("size", 58))
        paint = skia.Paint(Color=rgb(s.get("color", "ink"), int(255 * am * ta)), AntiAlias=True)
        txt = s["text"]
        sub = s.get("sub")
        y = s["y"] + s.get("size", 58) * 0.35 - (18 if sub else 0)
        c.drawString(txt, s["x"] - f.measureText(txt) / 2, y, f, paint)
        if sub:
            fs = font("ui", 30)
            c.drawString(sub, s["x"] - fs.measureText(sub) / 2, y + 42, fs, paint)
        c.restore()

    def _draw_text(self, c, p, am):
        s = self.spec
        f = font(s.get("font", "hand"), s.get("size", 80))
        lines = s["text"].split("\n")
        n = sum(len(l) for l in lines)
        shown = int(round(p * n))
        lh = s.get("size", 80) * s.get("line_height", 1.15)
        paint = skia.Paint(Color=rgb(s.get("color", "ink"), int(255 * am)), AntiAlias=True)
        tip = None
        y = s["y"]
        rot = s.get("rotate", 0)
        if rot:
            c.save(); c.rotate(rot, s["x"], s["y"])
        for line in lines:
            k = min(len(line), max(0, shown))
            shown -= len(line)
            full_w = f.measureText(line)
            align = s.get("align", "center")
            x = s["x"] - (full_w / 2 if align == "center" else (full_w if align == "right" else 0))
            if k > 0:
                c.drawString(line[:k], x, y, f, paint)
                if k < len(line):
                    tip = np.array([x + f.measureText(line[:k]), y - s.get("size", 80) * 0.25])
            y += lh
        if rot:
            c.restore()
            tip = None
        return tip if p < 1 else None

    def _draw_hemi(self, c, p, am):
        s = self.spec
        n = len(self.dots)
        shown = int(p * n)
        hl = s.get("highlight", 0)
        rad = s.get("dot", 9)
        for i, (x, y) in enumerate(self.dots[:shown]):
            col = s.get("hl_color", "blue") if i < hl else s.get("color", "gray")
            c.drawCircle(x, y, rad, skia.Paint(Color=rgb(col, int(255 * am)), AntiAlias=True))
        if p < 1 and shown > 0:
            return np.array(self.dots[shown - 1])
        return None

    def _draw_bars(self, c, p, am):
        s = self.spec
        x0, ybase, bw, gap, hmax = s["x"], s["y"], s.get("bar_w", 160), s.get("gap", 80), s.get("h", 500)
        vmax = s.get("max", max(b["value"] for b in s["bars"]))
        draw_poly(c, wobble([(x0 - 30, ybase), (x0 + len(s["bars"]) * (bw + gap), ybase)], np.random.default_rng(3), 1), "ink", 7, int(255 * am))
        fl = font("hand", 64)
        fv = font("hand", 56)
        tip = None
        for i, b in enumerate(s["bars"]):
            local = ease_out(min(1, max(0, p * len(s["bars"]) - i * 0.6)))
            h = hmax * b["value"] / vmax * local
            x = x0 + i * (bw + gap)
            if h > 1:
                c.drawRect(skia.Rect(x, ybase - h, x + bw, ybase), skia.Paint(Color=rgb(b.get("color", "blue"), int(230 * am)), AntiAlias=True))
                draw_poly(c, wobble(rect_pts(x, ybase - h, bw, h), np.random.default_rng(i), 1.2), "ink", 6, int(255 * am))
                if 0 < local < 1:
                    tip = np.array([x + bw / 2, ybase - h])
            lab = b["label"]
            c.drawString(lab, x + bw / 2 - fl.measureText(lab) / 2, ybase + 70, fl, skia.Paint(Color=rgb("ink", int(255 * am)), AntiAlias=True))
            if local > 0.95 and b.get("show_value", True):
                v = str(b.get("value_label", b["value"]))
                c.drawString(v, x + bw / 2 - fv.measureText(v) / 2, ybase - h - 22, fv, skia.Paint(Color=rgb("ink", int(255 * am)), AntiAlias=True))
        return tip

    def _draw_gauge(self, c, p, am):
        """Barra horizontal que se llena hasta value/max, con marca opcional (p. ej. la mitad)."""
        s = self.spec
        x, y, w, h = s["box"]
        rng = np.random.default_rng(5)
        po = min(1.0, p / 0.3)
        outline = wobble(rect_pts(x, y, w, h), rng, 1.2)
        draw_poly(c, outline[: max(2, int(po * len(outline)))], "ink", 7, int(255 * am))
        pf = ease_out((p - 0.3) / 0.7)
        if pf > 0:
            fw = w * s["value"] / s["max"] * pf
            c.drawRect(skia.Rect(x + 6, y + 6, x + 6 + max(0, fw - 12), y + h - 6),
                       skia.Paint(Color=rgb(s.get("color", "blue"), int(235 * am)), AntiAlias=True))
        if "mark" in s and p > 0.3:
            mx = x + w * s["mark"] / s["max"]
            draw_poly(c, wobble([(mx, y - 30), (mx, y + h + 30)], rng, 1), "red", 7, int(255 * am))
        return np.array([x + w * s["value"] / s["max"] * pf, y + h / 2]) if 0.3 < p < 1 else None

    def _chart_xy(self):
        s = self.spec
        x, y, w, h = s["box"]
        lo, hi = s.get("min", 0), s["max"]
        xs = [p["x"] for p in s["points"]]
        x0, x1 = s.get("x_from", min(xs)), s.get("x_to", max(xs))
        return [(x + w * (p["x"] - x0) / (x1 - x0), y + h - h * (p["value"] - lo) / (hi - lo)) for p in s["points"]]

    def _draw_linechart(self, c, t, am):
        """Gráfica de línea: los ejes se dibujan primero y la línea avanza punto a punto
        según 'reveal_t' (un instante por punto, resuelto en make_video) o, si no hay, en 'dur'."""
        s = self.spec
        x, y, w, h = s["box"]
        rng = np.random.default_rng(11)
        a = int(255 * am)
        pa = ease_out((t - self.t0) / 0.4)
        axes = wobble([(x - 20, y - 30), (x - 20, y + h), (x + w + 30, y + h)], rng, 1.0)
        draw_poly(c, axes[: max(2, int(pa * len(axes)))], "ink", 6, a)
        pts = self._chart_xy()
        rt = s.get("reveal_t") or [self.t0 + 0.4 + i * (self.dur - 0.4) / max(1, len(pts) - 1) for i in range(len(pts))]
        seg_dur = s.get("seg_dur", 0.7)
        # cuánto se ha dibujado: el tramo i→i+1 empieza en reveal_t[i+1] - seg_dur
        drawn, tip = [pts[0]], None
        if t < rt[0]:
            return np.array(axes[-1]) if pa < 1 else None
        for i in range(len(pts) - 1):
            st = max(rt[i], rt[i + 1] - seg_dur)
            f = ease((t - st) / max(0.05, rt[i + 1] - st))
            if f <= 0:
                break
            p0, p1 = np.array(pts[i]), np.array(pts[i + 1])
            end = p0 + (p1 - p0) * f
            drawn.append(tuple(end))
            if f < 1:
                tip = end
                break
        fill_col = s.get("area")
        if fill_col and len(drawn) > 1:
            path = skia.Path()
            path.moveTo(drawn[0][0], y + h)
            for q in drawn:
                path.lineTo(*q)
            path.lineTo(drawn[-1][0], y + h)
            path.close()
            c.drawPath(path, skia.Paint(Color=rgb(fill_col, int(60 * am)), AntiAlias=True))
        line = wobble(drawn, np.random.default_rng(2), 1.0, step=8) if len(drawn) > 1 else np.array(drawn)
        draw_poly(c, line, s.get("color", "ink"), s.get("width", 12), a)
        fv = font("hand", s.get("value_size", 58))
        fl = font("ui", s.get("label_size", 34))
        for i, (q, pt) in enumerate(zip(pts, s["points"])):
            if t < rt[i] - 0.05:
                break
            k = ease_out((t - rt[i] + 0.05) / 0.3)
            col = pt.get("color", s.get("color", "ink"))
            c.drawCircle(q[0], q[1], 16 * k, skia.Paint(Color=rgb(col, a), AntiAlias=True))
            c.drawCircle(q[0], q[1], 7 * k, skia.Paint(Color=rgb("paper", a), AntiAlias=True))
            v = pt.get("value_label", fmt_num(pt["value"], 0, True))
            dy = pt.get("label_dy", -40)
            vx = q[0] - fv.measureText(v) / 2 + pt.get("label_dx", 0)
            c.drawString(v, vx, q[1] + dy, fv, skia.Paint(Color=rgb(col, int(255 * am * k)), AntiAlias=True))
            lab = str(pt.get("label", pt["x"]))
            c.drawString(lab, q[0] - fl.measureText(lab) / 2, y + h + 52, fl, skia.Paint(Color=rgb("gray", int(255 * am * k)), AntiAlias=True))
        return tip

    def _draw_counter(self, c, p, am):
        s = self.spec
        v = s.get("from", 0) + (s["to"] - s.get("from", 0)) * ease_out(p)
        txt = s.get("prefix", "") + fmt_num(v, s.get("decimals", 0), s.get("sep", False)) + s.get("suffix", "")
        f = font(s.get("font", "hand"), s.get("size", 120))
        c.drawString(txt, s["x"] - f.measureText(txt) / 2, s["y"], f, skia.Paint(Color=rgb(s.get("color", "ink"), int(255 * am)), AntiAlias=True))
        return None


def fmt_num(v, decimals=0, sep=False):
    """Número a la española: 641.419 o 44,7."""
    txt = f"{v:,.{decimals}f}" if sep else f"{v:.{decimals}f}"
    return txt.replace(",", "§").replace(".", ",").replace("§", ".")


def draw_poly(c, pts, color, width, alpha=255):
    if len(pts) < 2:
        return
    path = skia.Path()
    path.moveTo(*pts[0])
    for q in pts[1:]:
        path.lineTo(*q)
    paint = skia.Paint(Color=rgb(color, alpha), StrokeWidth=width, Style=skia.Paint.kStroke_Style,
                       AntiAlias=True, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    c.drawPath(path, paint)


def draw_marker(c, tip, color="ink"):
    """Rotulador que sigue la punta del trazo en curso."""
    x, y = float(tip[0]), float(tip[1])
    c.save()
    c.translate(x, y)
    c.rotate(-35)
    # sombra
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(14, 6, 46, 250), 12, 12), skia.Paint(Color=skia.Color(0, 0, 0, 40), AntiAlias=True))
    tipp = skia.Path()
    tipp.addPoly([skia.Point(0, 0), skia.Point(-11, 34), skia.Point(11, 34)], True)
    c.drawPath(tipp, skia.Paint(Color=rgb(color), AntiAlias=True))
    c.drawRect(skia.Rect(-15, 34, 15, 60), skia.Paint(Color=rgb("light"), AntiAlias=True))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-17, 58, 17, 240), 10, 10), skia.Paint(Color=rgb((60, 64, 76)), AntiAlias=True))
    c.drawRect(skia.Rect(-17, 120, 17, 170), skia.Paint(Color=rgb(color), AntiAlias=True))
    c.restore()


def paper_texture(seed=7):
    rng = np.random.default_rng(seed)
    base = np.array(PALETTE["paper"], dtype=float)
    noise = rng.normal(0, 2.2, (H // 4, W // 4))
    noise = np.kron(noise, np.ones((4, 4)))
    fine = rng.normal(0, 1.4, (H, W))
    yy, xx = np.mgrid[0:H, 0:W]
    vign = -10 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
    img = base[None, None, :] + (noise + fine + vign)[..., None]
    img = np.clip(img, 0, 255).astype(np.uint8)
    rgba = np.dstack([img, np.full((H, W), 255, np.uint8)])
    return skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType)
