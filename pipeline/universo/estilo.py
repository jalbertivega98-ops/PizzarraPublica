"""Estilo gráfico del universo Pizarra Pública (docs/identidad/README.md).

Cartoon 2D: contorno negro grueso, colores vivos pero equilibrados, sombra suave y un brillo.
Todo se dibuja con vectores (skia), así cada pieza se puede animar por separado.
"""
import math

import numpy as np
import skia

TINTA = (28, 28, 34)
COL = {
    "tinta": TINTA,
    "blanco": (255, 255, 255),
    "pizarra": (251, 251, 248),
    "pizarra_sombra": (226, 231, 238),
    "marco": (196, 200, 208),
    "marco_claro": (232, 234, 238),
    "marco_oscuro": (122, 127, 137),
    "guante_sombra": (214, 219, 230),
    "rojo": (226, 58, 48),
    "rojo_osc": (170, 32, 30),
    "boca": (96, 22, 30),
    "lengua": (236, 92, 96),
    "amarillo": (255, 205, 60),
    "naranja": (247, 146, 48),
    "verde": (60, 170, 90),
    "verde_osc": (36, 120, 60),
    "azul": (52, 120, 230),
    "azul_claro": (150, 200, 245),
    "rosa": (232, 90, 150),
    "gris": (150, 154, 162),
    "gris_claro": (215, 218, 224),
    "cielo": (150, 210, 245),
    "cielo_alto": (92, 170, 232),
    "piedra": (232, 224, 210),
    "piedra_osc": (196, 186, 170),
    "teja": (214, 108, 70),
    "fachada": (246, 214, 180),
    "madera": (176, 118, 72),
    "cristal": (200, 230, 245),
    "luz": (255, 236, 190),
    "hierba": (120, 190, 80),
    "acera": (200, 200, 204),
    "billete": (120, 196, 120),
    "oro": (246, 196, 60),
    # partidos (solo para nombrarlos)
    "psoe": (225, 30, 40), "pp": (0, 104, 180), "vox": (90, 175, 40),
}
# nombres del motor de pizarra (wb.PALETTE) también valen
COL.update({"red": COL["rojo"], "green": COL["verde"], "blue": COL["azul"], "yellow": COL["amarillo"], "gray": COL["gris"],
            "ink": TINTA, "orange": COL["naranja"], "white": COL["blanco"]})
GROSOR = 6.0  # contorno base a escala 1


def rgb(c, a=255):
    if isinstance(c, str):
        c = COL[c]
    if len(c) == 4:
        return skia.Color(*c)
    return skia.Color(c[0], c[1], c[2], a)


def mezcla(a, b, k):
    a, b = (COL[a] if isinstance(a, str) else a), (COL[b] if isinstance(b, str) else b)
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def relleno(color, alpha=255, shader=None):
    p = skia.Paint(Color=rgb(color, alpha), AntiAlias=True)
    if shader is not None:
        p.setShader(shader)
    return p


def trazo(width=GROSOR, color=TINTA, alpha=255):
    return skia.Paint(Color=rgb(color, alpha), AntiAlias=True, Style=skia.Paint.kStroke_Style,
                      StrokeWidth=width, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)


def degradado(y0, y1, c0, c1, x0=0, x1=0):
    return skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [rgb(c0), rgb(c1)])


def pieza(c, path, color, w=GROSOR, alpha=255, shader=None, sombra=None, brillo=None):
    """Rellena + contornea un path. sombra = (path, color) opcional para dar volumen."""
    c.drawPath(path, relleno(color, alpha, shader))
    if sombra is not None:
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        c.drawPath(sombra[0], relleno(sombra[1], int(alpha * 0.9)))
        c.restore()
    if brillo is not None:
        c.drawPath(brillo, trazo(w * 0.7, "blanco", int(alpha * 0.85)))
    if w > 0:
        c.drawPath(path, trazo(w, TINTA, alpha))


def rrect(x0, y0, x1, y1, r):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r))
    return p


def elipse(cx, cy, rx, ry):
    p = skia.Path()
    p.addOval(skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry))
    return p


def poly(pts, close=True):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    return p


def suave(pts, close=True, tension=0.5):
    """Curva Catmull-Rom por los puntos (formas orgánicas)."""
    pts = [np.array(p, float) for p in pts]
    n = len(pts)
    p = skia.Path()
    p.moveTo(*pts[0])
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        if not close:
            p0 = pts[max(i - 1, 0)]
            p3 = pts[min(i + 2, n - 1)]
        c1 = p1 + (p2 - p0) * tension / 3
        c2 = p2 - (p3 - p1) * tension / 3
        p.cubicTo(*c1, *c2, *p2)
    if close:
        p.close()
    return p


def sombra_suelo(c, x, y, rx, ry=None, alpha=55):
    ry = ry or rx * 0.18
    p = skia.Paint(Color=skia.Color(0, 0, 0, alpha), AntiAlias=True)
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
    c.drawOval(skia.Rect(x - rx, y - ry, x + rx, y + ry), p)


def manguera(c, p0, p1, curva=0.25, w=18, lado=1):
    """Brazo/pierna «de manguera» (rubber hose): trazo negro curvo."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    nrm = np.array([-d[1], d[0]]) * curva * lado
    ctrl = (p0 + p1) / 2 + nrm
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(*ctrl, *p1)
    c.drawPath(path, trazo(w, TINTA))
    # tangente al final (para orientar guante o zapato)
    t = p1 - ctrl
    return math.degrees(math.atan2(t[1], t[0]))


def texto_cartoon(c, txt, x, y, size, color="amarillo", fuente=None, borde=None, align="center", alpha=255):
    """Rótulo con contorno negro y sombra (como «¡NUESTRA CASA!» de la referencia)."""
    import wb
    f = wb.font(fuente or "hand", size)
    w = f.measureText(txt)
    x0 = x - (w / 2 if align == "center" else (w if align == "right" else 0))
    b = borde or max(4, size * 0.09)
    sh = skia.Paint(Color=skia.Color(0, 0, 0, int(70 * alpha / 255)), AntiAlias=True)
    c.drawString(txt, x0 + size * 0.04, y + size * 0.06, f, sh)
    st = skia.Paint(Color=rgb(TINTA, alpha), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=b * 2,
                    StrokeJoin=skia.Paint.kRound_Join)
    c.drawString(txt, x0, y, f, st)
    c.drawString(txt, x0, y, f, relleno(color, alpha))
    return x0, w
