"""Personajes reutilizables con expresiones y poses.

dibuja_personaje(cv, tipo, t, cara, pose, ...) dibuja en coordenadas locales: pies en y=+150,
cabeza en y≈-70; unos 330 px de alto a escala 1. Los políticos genéricos van en gris con corbata
amarilla (regla de neutralidad: nunca colores de partido).
"""
import math

import skia

from dibujo import p_fill, p_stroke, rgb, OFF

TIPOS = {
    #            camisa      pelo        piel     extra
    "ciudadano": ("teal", "brown", "skin", None),
    "ciudadana": ("orange", "ink", "skin2", "coleta"),
    "joven": ("purple", "ink", "skin", "gorra"),
    "politico": ("suit", "gray", "skin", "corbata"),
    "medico": ("white", "brown", "skin2", "bata"),
    "funcionario": ("blue", "ink", "skin", "gafas"),
    "trabajador": ("orange", "brown", "skin3", "casco"),
    "viajero": ("blue", "ink", "skin3", "mochila"),
    "jefa": ("red", "brown", "skin", "moño"),
}


def _circ(cv, x, y, r, relleno, tinta="ink", w=6, desplaza=True):
    if relleno:
        cv.drawCircle(x + (OFF[0] * 0.6 if desplaza else 0), y + (OFF[1] * 0.6 if desplaza else 0), r, p_fill(relleno))
    if tinta:
        cv.drawCircle(x, y, r, p_stroke(tinta, w))


def _rrect(cv, l, t, r, b, rad, relleno, tinta="ink", w=7):
    rr = skia.Rect(l, t, r, b)
    if relleno:
        cv.save()
        cv.translate(OFF[0] * 0.7, OFF[1] * 0.7)
        cv.drawRoundRect(rr, rad, rad, p_fill(relleno))
        cv.restore()
    if tinta:
        cv.drawRoundRect(rr, rad, rad, p_stroke(tinta, w))


def _linea(cv, pts, c="ink", w=8):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    cv.drawPath(p, p_stroke(c, w))


def _arco(cv, cx, cy, rx, ry, a0, barrido, c="ink", w=6, relleno=None):
    r = skia.Rect(cx - rx, cy - ry, cx + rx, cy + ry)
    if relleno:
        cv.drawArc(r, a0, barrido, False, p_fill(relleno))
    cv.drawArc(r, a0, barrido, False, p_stroke(c, w))


def _brazo(cv, hombro, mano, color, manga="ink"):
    _linea(cv, [hombro, mano], "ink", 22)
    _linea(cv, [hombro, mano], color, 12)
    _circ(cv, mano[0], mano[1], 12, "skin", "ink", 5, desplaza=False)


POSES = {
    #             mano izq        mano der
    "normal": ((-70, 80), (70, 80)),
    "señala": ((-70, 80), (125, -60)),
    "señala_izq": ((-125, -60), (70, 80)),
    "brazos_arriba": ((-110, -85), (110, -85)),
    "encoge": ((-105, -5), (105, -5)),
    "sostiene": ((-45, 40), (45, 40)),
    "jarras": ((-50, 45), (50, 45)),
    "saluda": ((-70, 80), (110, -80)),
    "cabeza": ((-60, -95), (60, -95)),
}


def cara(cv, expr, t, cx=0, cy=-70, piel="skin"):
    parpadeo = (t % 3.1) < 0.12
    ex, ey = 22, -6
    if expr in ("sorpresa", "nervioso", "shock"):
        for s in (-1, 1):
            _circ(cv, cx + s * ex, cy + ey, 15, "white", "ink", 5, desplaza=False)
            cv.drawCircle(cx + s * ex, cy + ey + 2, 6, p_fill("ink"))
            _linea(cv, [(cx + s * ex - 12, cy + ey - 28), (cx + s * ex + 12, cy + ey - 32)], "ink", 6)
        if expr == "shock":
            _rrect(cv, cx - 16, cy + 18, cx + 16, cy + 50, 14, "ink", "ink", 4)
        elif expr == "nervioso":
            _linea(cv, [(cx - 22, cy + 30), (cx - 11, cy + 24), (cx, cy + 30), (cx + 11, cy + 24), (cx + 22, cy + 30)], "ink", 5)
        else:
            cv.drawOval(skia.Rect(cx - 11, cy + 20, cx + 11, cy + 44), p_fill("ink"))
        if expr == "nervioso":
            gota = skia.Path()
            gota.moveTo(cx + 62, cy - 30)
            gota.quadTo(cx + 74, cy - 8, cx + 64, cy - 2)
            gota.quadTo(cx + 52, cy - 8, cx + 62, cy - 30)
            cv.drawPath(gota, p_fill("blue"))
        return
    # ojos
    for s in (-1, 1):
        if expr == "feliz":
            _arco(cv, cx + s * ex, cy + ey + 4, 10, 8, 200, 140, "ink", 6)
        elif parpadeo:
            _linea(cv, [(cx + s * ex - 8, cy + ey), (cx + s * ex + 8, cy + ey)], "ink", 5)
        else:
            cv.drawCircle(cx + s * ex, cy + ey, 7, p_fill("ink"))
    # cejas
    if expr == "enfado":
        for s in (-1, 1):
            _linea(cv, [(cx + s * (ex + 14), cy + ey - 22), (cx + s * (ex - 8), cy + ey - 12)], "ink", 7)
    elif expr == "triste":
        for s in (-1, 1):
            _linea(cv, [(cx + s * (ex + 12), cy + ey - 12), (cx + s * (ex - 8), cy + ey - 22)], "ink", 6)
    elif expr == "duda":
        _linea(cv, [(cx - ex - 12, cy + ey - 18), (cx - ex + 10, cy + ey - 16)], "ink", 6)
        _arco(cv, cx + ex, cy + ey - 22, 13, 8, 200, 140, "ink", 6)
    elif expr == "listo":
        _linea(cv, [(cx - ex - 12, cy + ey - 16), (cx - ex + 10, cy + ey - 18)], "ink", 6)
        _linea(cv, [(cx + ex - 10, cy + ey - 22), (cx + ex + 12, cy + ey - 16)], "ink", 6)
    # boca
    if expr == "feliz":
        p = skia.Path()
        p.moveTo(cx - 24, cy + 20)
        p.quadTo(cx, cy + 56, cx + 24, cy + 20)
        p.close()
        cv.drawPath(p, p_fill("ink"))
    elif expr in ("enfado", "triste"):
        _arco(cv, cx, cy + 42, 18, 12, 200, 140, "ink", 6)
        if expr == "enfado":
            _circ(cv, cx - 40, cy + 18, 9, "pink", None, desplaza=False)
            _circ(cv, cx + 40, cy + 18, 9, "pink", None, desplaza=False)
    elif expr == "duda":
        _linea(cv, [(cx - 14, cy + 30), (cx + 16, cy + 24)], "ink", 6)
    elif expr == "listo":
        _arco(cv, cx + 6, cy + 18, 18, 12, 20, 120, "ink", 6)
    else:
        _arco(cv, cx, cy + 20, 16, 12, 30, 120, "ink", 6)


def dibuja_personaje(cv, tipo, t, expr="neutral", pose="normal", sostiene=None, mira=1, colores=None):
    camisa, pelo, piel, extra = TIPOS.get(tipo, TIPOS["ciudadano"])
    if colores:
        camisa = colores.get("camisa", camisa)
    li, ld = POSES.get(pose, POSES["normal"])
    if pose == "saluda":
        ld = (ld[0] + 18 * math.sin(t * 14), ld[1])
    cv.save()
    if mira < 0:
        cv.scale(-1, 1)
    # piernas
    for s in (-1, 1):
        _linea(cv, [(s * 22, 90), (s * 26, 140)], "ink", 20)
        cv.drawOval(skia.Rect(s * 26 - 22 + s * 8, 132, s * 26 + 22 + s * 8, 154), p_fill("ink"))
    # mochila (detrás)
    if extra == "mochila":
        _rrect(cv, -78, -5, -40, 70, 14, "orange", "ink", 6)
    # cuerpo
    _rrect(cv, -58, -14, 58, 100, 32, camisa, "ink", 7)
    if extra == "corbata":
        p = skia.Path()
        p.moveTo(-26, -12)
        p.lineTo(0, 28)
        p.lineTo(26, -12)
        p.close()
        cv.drawPath(p, p_fill("white"))
        p2 = skia.Path()
        for i, q in enumerate([(0, -8), (-10, 6), (0, 58), (10, 6)]):
            p2.moveTo(*q) if i == 0 else p2.lineTo(*q)
        p2.close()
        cv.drawPath(p2, p_fill("yellow"))
        cv.drawPath(p2, p_stroke("ink", 4))
    if extra == "bata":
        _linea(cv, [(0, -10), (0, 98)], "ink", 4)
        _linea(cv, [(-24, -12), (-34, 20)], "ink", 4)
        _linea(cv, [(24, -12), (34, 20)], "ink", 4)
        cv.drawRect(skia.Rect(18, 40, 44, 66), p_fill("red"))
        _arco(cv, 0, 0, 26, 30, 0, 180, "gray", 6)
        _circ(cv, 0, 34, 8, "light", "gray", 4, desplaza=False)
    if extra == "mochila":
        _linea(cv, [(-40, -10), (-30, 60)], "brown", 7)
    # brazos
    _brazo(cv, (-48, 8), li, camisa)
    _brazo(cv, (48, 8), ld, camisa)
    # cabeza
    _circ(cv, 0, -70, 60, piel, "ink", 7)
    # pelo / gorros
    if extra == "casco":
        _arco(cv, 0, -88, 64, 50, 180, 180, "ink", 7, relleno="yellow")
        _linea(cv, [(-72, -88), (72, -88)], "ink", 9)
    elif extra == "gorra":
        _arco(cv, 0, -96, 58, 40, 180, 180, "ink", 7, relleno="purple")
        _linea(cv, [(0, -96), (80, -96)], "ink", 11)
    else:
        p = skia.Path()
        p.moveTo(-60, -76)
        p.quadTo(-62, -140, 0, -134)
        p.quadTo(58, -140, 60, -80)
        p.quadTo(30, -112, -10, -104)
        p.quadTo(-40, -102, -60, -76)
        cv.drawPath(p, p_fill(pelo))
        if extra == "coleta":
            cv.drawOval(skia.Rect(46, -120, 96, -70), p_fill(pelo))
        if extra == "moño":
            _circ(cv, 0, -138, 22, pelo, None, desplaza=False)
    if extra == "gafas":
        for s in (-1, 1):
            cv.drawCircle(s * 22, -76, 17, p_stroke("ink", 5))
        _linea(cv, [(-5, -76), (5, -76)], "ink", 4)
    cara(cv, expr, t)
    cv.restore()
    # objeto en la mano (no se refleja)
    if sostiene == "maleta":
        x = li[0] * (1 if mira > 0 else -1)
        _rrect(cv, x - 50, li[1] + 6, x + 40, li[1] + 76, 10, "purple", "ink", 6)
        _linea(cv, [(x - 15, li[1] + 6), (x - 15, li[1] - 6), (x + 5, li[1] - 6), (x + 5, li[1] + 6)], "ink", 5)
    elif sostiene == "papel":
        x = (li[0] + ld[0]) / 2 * (1 if mira > 0 else -1)
        y = (li[1] + ld[1]) / 2
        cv.save()
        cv.rotate(-6)
        _rrect(cv, x - 45, y - 70, x + 45, y + 30, 4, "white", "ink", 5)
        for i in range(3):
            _linea(cv, [(x - 28, y - 45 + i * 22), (x + 28, y - 45 + i * 22)], "gray", 5)
        cv.restore()
    elif sostiene == "sello":
        x, y = ld[0] * (1 if mira > 0 else -1), ld[1]
        _rrect(cv, x - 14, y - 50, x + 14, y - 8, 8, "brown", "ink", 5)
        _rrect(cv, x - 34, y - 12, x + 34, y + 6, 4, "red", "ink", 5)


def dibuja_hucha(cv, t, expr="neutral", etiqueta=None):
    """La hucha de la Seguridad Social, con cara."""
    _linea(cv, [(-60, 60), (-60, 110)], "ink", 22)
    _linea(cv, [(50, 60), (50, 110)], "ink", 22)
    cv.save()
    cv.translate(OFF[0], OFF[1])
    cv.drawOval(skia.Rect(-140, -90, 140, 90), p_fill("pink"))
    cv.restore()
    cv.drawOval(skia.Rect(-140, -90, 140, 90), p_stroke("ink", 8))
    p = skia.Path()
    p.moveTo(-70, -80)
    p.lineTo(-50, -130)
    p.lineTo(-25, -86)
    cv.drawPath(p, p_fill("pink"))
    cv.drawPath(p, p_stroke("ink", 7))
    _rrect(cv, -30, -98, 40, -84, 6, "ink", "ink", 3)  # ranura
    _rrect(cv, 118, -24, 168, 30, 18, "pink", "ink", 7)  # hocico
    cv.drawCircle(136, 3, 6, p_fill("ink"))
    cv.drawCircle(152, 3, 6, p_fill("ink"))
    cv.save()
    cv.translate(40, 10)
    cara(cv, expr, t, cx=0, cy=-10)
    cv.restore()
