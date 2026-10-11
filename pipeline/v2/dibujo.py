"""Primitivas de dibujo de Pizarra Pública v2: trazo a mano, relleno desplazado, texto con contorno, iconos.

Identidad visual:
- Papel cálido, tinta casi negra, trazo redondeado con un temblor ligero.
- Relleno de color desplazado unos píxeles respecto al contorno (aspecto de viñeta impresa).
- Cifras en Poppins ExtraBold, notas a mano en Kalam.
"""
import math
import os

import numpy as np
import skia

W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "assets", "fonts")

PAL = {
    "papel": (250, 247, 240),
    "ink": (22, 24, 31),
    "red": (236, 56, 48),
    "yellow": (255, 206, 30),
    "blue": (34, 108, 240),
    "green": (22, 168, 96),
    "orange": (255, 128, 20),
    "teal": (0, 168, 168),
    "purple": (124, 77, 230),
    "pink": (255, 112, 160),
    "gray": (140, 145, 155),
    "light": (226, 228, 233),
    "white": (255, 255, 255),
    "skin": (255, 222, 190),
    "skin2": (214, 160, 120),
    "skin3": (150, 100, 70),
    "brown": (110, 70, 40),
    "suit": (96, 102, 115),
    # colores de partido: solo para nombrar al partido, nunca en personajes
    "psoe": (225, 30, 40),
    "pp": (0, 104, 180),
    "vox": (90, 175, 40),
}
OFF = (6, 7)  # desplazamiento del relleno

_TF = {}
FUENTES = {"num": "Poppins-ExtraBold.ttf", "ui": "Poppins-SemiBold.ttf", "mano": "Kalam-Bold.ttf",
           "mano2": "Kalam-Regular.ttf", "cuerpo": "PatrickHand-Regular.ttf"}


def fuente(nombre, tam):
    if nombre not in _TF:
        _TF[nombre] = skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, FUENTES[nombre]))
    f = skia.Font(_TF[nombre], tam)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def rgb(c, a=255):
    if isinstance(c, str):
        c = PAL[c]
    return skia.Color(int(c[0]), int(c[1]), int(c[2]), int(max(0, min(255, a))))


def mezcla(c1, c2, p):
    a, b = (PAL[c1] if isinstance(c1, str) else c1), (PAL[c2] if isinstance(c2, str) else c2)
    return tuple(int(a[i] + (b[i] - a[i]) * p) for i in range(3))


def p_fill(c, a=255):
    return skia.Paint(AntiAlias=True, Color=rgb(c, a), Style=skia.Paint.kFill_Style)


def p_stroke(c, w=7, a=255):
    return skia.Paint(AntiAlias=True, Color=rgb(c, a), Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                      StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)


# ------------------------------------------------------------------ easing
def clamp(t):
    return 0.0 if t < 0 else 1.0 if t > 1 else t


def e_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def e_inout(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def e_back(t, s=1.9):
    t = clamp(t)
    t -= 1
    return t * t * ((s + 1) * t + s) + 1


def e_elastic(t):
    t = clamp(t)
    if t in (0, 1):
        return t
    return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1


def e_in(t):
    t = clamp(t)
    return t ** 3


# ------------------------------------------------------------------ trazo a mano
def temblor(pts, rng, amp=1.5, paso=9.0):
    pts = np.asarray(pts, dtype=float)
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(np.hypot(*(b - a)) / paso))
        for i in range(1, n + 1):
            out.append(a + (b - a) * i / n)
    out = np.array(out)
    if amp <= 0 or len(out) < 3:
        return out
    t = np.linspace(0, 1, len(out))
    ph = rng.uniform(0, 2 * np.pi, 4)
    fr = rng.uniform(1.0, 2.5, 2)
    off = np.stack([np.sin(2 * np.pi * fr[0] * t + ph[0]) + 0.35 * np.sin(13 * t + ph[1]),
                    np.sin(2 * np.pi * fr[1] * t + ph[2]) + 0.35 * np.sin(17 * t + ph[3])], 1)
    return out + off * amp


def camino(pts, cerrado=False):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if cerrado:
        p.close()
    return p


def elipse(cx, cy, rx, ry, a0=-90, barrido=360, n=64):
    a = np.radians(np.linspace(a0, a0 + barrido, n))
    return np.stack([cx + rx * np.cos(a), cy + ry * np.sin(a)], 1)


def rect(x, y, w, h, r=0):
    if r <= 0:
        return np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], float)
    pts = []
    for cx, cy, a0 in [(x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)]:
        pts.extend(elipse(cx, cy, r, r, a0, 90, 10))
    pts.append(pts[0])
    return np.array(pts)


class Trazo:
    """Contorno (que se puede dibujar progresivamente) + relleno opcional desplazado."""

    def __init__(self, pts, tinta="ink", ancho=7, relleno=None, cerrado=False, rng=None, amp=1.4, desplaza=True):
        rng = rng or np.random.default_rng(0)
        self.pts = temblor(pts, rng, amp) if amp > 0 else np.asarray(pts, float)
        self.path = camino(self.pts, cerrado)
        self.relleno_path = camino(np.asarray(pts, float), True) if relleno else None
        self.tinta, self.ancho, self.relleno, self.desplaza = tinta, ancho, relleno, desplaza
        pm = skia.PathMeasure(self.path, False)
        self.len = max(pm.getLength(), 1e-3)

    def dibuja(self, cv, frac=1.0, alpha=255, relleno_alpha=None):
        if self.relleno is not None and frac >= 0.999:
            cv.save()
            if self.desplaza:
                cv.translate(*OFF)
            cv.drawPath(self.relleno_path, p_fill(self.relleno, alpha if relleno_alpha is None else relleno_alpha))
            cv.restore()
        if self.tinta is None or self.ancho <= 0:
            return
        if frac >= 0.999:
            cv.drawPath(self.path, p_stroke(self.tinta, self.ancho, alpha))
        elif frac > 0:
            pm = skia.PathMeasure(self.path, False)
            dst = skia.Path()
            pm.getSegment(0, self.len * frac, dst, True)
            cv.drawPath(dst, p_stroke(self.tinta, self.ancho, alpha))


def dibuja_trazos(cv, trazos, frac=1.0, alpha=255):
    """Dibuja una lista de trazos repartiendo `frac` entre ellos según su longitud (rellenos primero)."""
    total = sum(t.len for t in trazos) or 1
    resto = frac * total if frac < 0.999 else total * 2
    hechos = []
    for t in trazos:
        f = min(1.0, max(0.0, resto / t.len))
        hechos.append(f)
        resto -= t.len
    # rellenos (desplazados) de los trazos ya terminados, debajo de todos los contornos
    for t, f in zip(trazos, hechos):
        if t.relleno is not None and f >= 0.999:
            cv.save()
            if t.desplaza:
                cv.translate(*OFF)
            cv.drawPath(t.relleno_path, p_fill(t.relleno, alpha))
            cv.restore()
    for t, f in zip(trazos, hechos):
        if t.tinta is None or t.ancho <= 0 or f <= 0:
            continue
        if f >= 0.999:
            cv.drawPath(t.path, p_stroke(t.tinta, t.ancho, alpha))
        else:
            pm = skia.PathMeasure(t.path, False)
            dst = skia.Path()
            pm.getSegment(0, t.len * f, dst, True)
            cv.drawPath(dst, p_stroke(t.tinta, t.ancho, alpha))


# ------------------------------------------------------------------ texto
def ancho_texto(txt, f):
    return f.measureText(txt)


def texto(cv, txt, x, y, f, color="ink", contorno="white", grosor=12, alinea="c", alpha=255):
    """Texto con contorno (legible sobre cualquier dibujo). y = línea base."""
    w = f.measureText(txt)
    x0 = x - w / 2 if alinea == "c" else (x - w if alinea == "d" else x)
    if contorno and grosor > 0:
        cv.drawString(txt, x0, y, f, p_stroke(contorno, grosor, alpha))
    cv.drawString(txt, x0, y, f, p_fill(color, alpha))
    return w


def fmt_num(v, dec=0):
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


# ------------------------------------------------------------------ iconos (caja ~200 px centrada en 0,0)
def _t(pts, rng, tinta="ink", ancho=7, relleno=None, cerrado=False, amp=1.3):
    return Trazo(pts, tinta, ancho, relleno, cerrado, rng, amp)


def ico_casa(rng, c="orange"):
    return [_t([(-90, -10), (0, -95), (90, -10)], rng, ancho=9),
            _t(rect(-70, -25, 140, 115), rng, relleno=c, cerrado=True),
            _t(rect(-18, 30, 36, 60), rng, relleno="brown", cerrado=True),
            _t(rect(-55, 0, 30, 28), rng, relleno="light", cerrado=True),
            _t(rect(25, 0, 30, 28), rng, relleno="light", cerrado=True),
            _t([(40, -60), (40, -95), (62, -95), (62, -40)], rng)]


def ico_documento(rng, c="white"):
    S = [_t([(-65, -90), (35, -90), (65, -60), (65, 90), (-65, 90), (-65, -90)], rng, relleno=c, cerrado=True),
         _t([(35, -90), (35, -60), (65, -60)], rng, ancho=5)]
    for i in range(4):
        S.append(_t([(-40, -40 + i * 30), (40 - (i == 3) * 30, -40 + i * 30)], rng, tinta="gray", ancho=6))
    return S


def ico_billete(rng, c="green"):
    return [_t(rect(-95, -50, 190, 100, 10), rng, relleno=c, cerrado=True),
            _t(elipse(0, 0, 30, 30), rng, tinta="ink", ancho=5, relleno="white", cerrado=True)]


def ico_moneda(rng, c="yellow"):
    return [_t(elipse(0, 0, 60, 60), rng, relleno=c, cerrado=True), _t(elipse(0, 0, 42, 42), rng, ancho=4)]


def ico_avion(rng, c="light"):
    body = [(-100, 0), (-80, -16), (90, -16), (110, 0), (90, 16), (-80, 16), (-100, 0)]
    return [_t(body, rng, relleno=c, cerrado=True), _t([(-10, -16), (30, -80), (50, -80), (35, -16)], rng, relleno="blue", cerrado=True),
            _t([(-10, 16), (30, 80), (50, 80), (35, 16)], rng, relleno="blue", cerrado=True),
            _t([(-85, -16), (-100, -55), (-80, -55), (-60, -16)], rng, relleno="blue", cerrado=True)]


def ico_pasaporte(rng, c="red"):
    return [_t(rect(-65, -90, 130, 180, 12), rng, relleno=c, cerrado=True),
            _t(elipse(0, -15, 32, 32), rng, tinta="yellow", ancho=5),
            _t([(-30, 45), (30, 45)], rng, tinta="yellow", ancho=6)]


def ico_hospital(rng, c="white"):
    return [_t(rect(-90, -70, 180, 160), rng, relleno=c, cerrado=True),
            _t([(-15, -45), (15, -45), (15, -15), (45, -15), (45, 15), (15, 15), (15, 45), (-15, 45), (-15, 15), (-45, 15),
                (-45, -15), (-15, -15), (-15, -45)], rng, relleno="red", cerrado=True, ancho=5)]


def ico_calendario(rng, c="white"):
    S = [_t(rect(-80, -70, 160, 150, 10), rng, relleno=c, cerrado=True), _t(rect(-80, -70, 160, 40), rng, relleno="red", cerrado=True)]
    for i in range(3):
        for j in range(3):
            S.append(_t(elipse(-45 + j * 45, 0 + i * 30, 6, 6, n=12), rng, ancho=6))
    return S


def ico_lupa(rng, c="light"):
    return [_t(elipse(-20, -20, 55, 55), rng, relleno=c, cerrado=True, ancho=9), _t([(20, 20), (80, 80)], rng, ancho=18)]


def ico_grua(rng, c="yellow"):
    return [_t([(-40, 100), (-40, -90)], rng, ancho=10), _t([(-80, -90), (100, -90)], rng, ancho=10),
            _t([(-40, -60), (0, -90)], rng, ancho=6), _t([(80, -90), (80, -10)], rng, ancho=4),
            _t(rect(60, -10, 40, 30), rng, relleno=c, cerrado=True), _t([(-90, 100), (10, 100)], rng, ancho=10)]


def ico_euro(rng, c="ink"):
    a = elipse(10, 0, 70, 80, 50, 260)
    return [_t(a, rng, tinta=c, ancho=16), _t([(-85, -15), (20, -15)], rng, tinta=c, ancho=14), _t([(-85, 20), (15, 20)], rng, tinta=c, ancho=14)]


def ico_estetoscopio(rng, c="gray"):
    return [_t(elipse(0, -20, 50, 60, 200, 140), rng, tinta=c, ancho=8), _t([(0, 40), (0, 70)], rng, tinta=c, ancho=8),
            _t(elipse(0, 85, 18, 18), rng, relleno="light", cerrado=True)]


def ico_megafono(rng, c="red"):
    return [_t([(-70, -25), (40, -75), (40, 75), (-70, 25), (-70, -25)], rng, relleno=c, cerrado=True),
            _t(rect(-95, -25, 25, 50), rng, relleno="light", cerrado=True), _t([(-60, 25), (-40, 85)], rng, ancho=10)]


def ico_candado(rng, c="yellow"):
    return [_t(elipse(0, -30, 45, 55, 180, 180), rng, ancho=14), _t(rect(-65, -25, 130, 105, 12), rng, relleno=c, cerrado=True)]


def ico_reloj(rng, c="white"):
    return [_t(elipse(0, 0, 80, 80), rng, relleno=c, cerrado=True, ancho=8), _t([(0, 0), (0, -50)], rng, ancho=8), _t([(0, 0), (35, 15)], rng, ancho=8)]


def ico_cerebro(rng, c="pink"):
    pts = elipse(0, 0, 85, 65)
    return [_t(pts, rng, relleno=c, cerrado=True), _t([(0, -60), (0, 60)], rng, ancho=5),
            _t(elipse(-40, -10, 22, 18, 0, 200), rng, ancho=5), _t(elipse(40, 15, 22, 18, 180, 200), rng, ancho=5)]


def ico_grafica(rng, c="red"):
    return [_t([(-90, -90), (-90, 90), (95, 90)], rng, ancho=8), _t([(-70, 50), (-20, 10), (20, 30), (80, -60)], rng, tinta=c, ancho=12),
            _t([(55, -62), (82, -62), (80, -35)], rng, tinta=c, ancho=12)]


def ico_maleta(rng, c="purple"):
    return [_t(rect(-80, -45, 160, 115, 14), rng, relleno=c, cerrado=True), _t(rect(-28, -75, 56, 32, 8), rng, ancho=8),
            _t([(-40, -45), (-40, 70)], rng, ancho=5), _t([(40, -45), (40, 70)], rng, ancho=5)]


def ico_bandera_ue(rng, c="blue"):
    S = [_t(rect(-100, -65, 200, 130, 6), rng, relleno=c, cerrado=True)]
    for k in range(12):
        a = 2 * math.pi * k / 12
        S.append(_t(elipse(55 * math.cos(a), 45 * math.sin(a), 5, 5, n=10), rng, tinta="yellow", ancho=7))
    return S


def ico_interrogacion(rng, c="red"):
    return [_t(list(elipse(0, -40, 50, 50, 200, 250)) + [(0, 20), (0, 45)], rng, tinta=c, ancho=22), _t(elipse(0, 85, 8, 8, n=12), rng, tinta=c, ancho=18)]


def ico_check(rng, c="green"):
    return [_t([(-60, 0), (-15, 50), (70, -60)], rng, tinta=c, ancho=22)]


def ico_cruz(rng, c="red"):
    return [_t([(-55, -55), (55, 55)], rng, tinta=c, ancho=22), _t([(55, -55), (-55, 55)], rng, tinta=c, ancho=22)]


def ico_llave(rng, c="yellow"):
    return [_t(elipse(-50, 0, 35, 35), rng, relleno=c, cerrado=True, ancho=8), _t([(-15, 0), (90, 0)], rng, ancho=12),
            _t([(60, 0), (60, 30)], rng, ancho=10), _t([(80, 0), (80, 25)], rng, ancho=10)]


def ico_edificio(rng, c="light"):
    S = [_t([(-110, -50), (0, -110), (110, -50), (-110, -50)], rng, relleno=c, cerrado=True),
         _t(rect(-100, -50, 200, 20), rng, relleno=c, cerrado=True), _t(rect(-110, 100, 220, 20), rng, relleno=c, cerrado=True)]
    for x in (-75, -25, 25, 75):
        S.append(_t(rect(x - 10, -30, 20, 130), rng, relleno="white", cerrado=True, ancho=5))
    return S


ICONOS = {k[4:]: v for k, v in globals().items() if k.startswith("ico_")}
