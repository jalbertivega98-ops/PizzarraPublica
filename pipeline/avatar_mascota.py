#!/usr/bin/env python3
"""Foto de perfil con mascota: una pizarra con cara, estilo pegatina (1080×1080)."""
import math
import os
import sys

import numpy as np
import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wb  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "perfil")
S = 1080
INK = (24, 26, 32)
CHALK = (246, 244, 234)
YEL = (255, 212, 71)


def P(col, a=255, w=None, fill=True):
    p = skia.Paint(Color=wb.rgb(col, a), AntiAlias=True)
    if not fill:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w)
        p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def poly(c, pts, col, w):
    path = skia.Path(); path.moveTo(*pts[0])
    for q in pts[1:]:
        path.lineTo(*q)
    c.drawPath(path, P(col, w=w, fill=False))


def chalk(c, pts, rng, col=CHALK, w=10):
    for k in range(3):
        wb.draw_poly(c, wb.wobble(pts, rng, 1.6, 8), col, w * (0.6 + 0.25 * k), 110 + 45 * k)


def sunburst(c, bg, ray):
    c.clear(wb.rgb(bg))
    n = 24
    for i in range(0, n, 2):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        path = skia.Path(); path.moveTo(540, 540)
        path.lineTo(540 + 900 * math.cos(a0), 540 + 900 * math.sin(a0))
        path.lineTo(540 + 900 * math.cos(a1), 540 + 900 * math.sin(a1)); path.close()
        c.drawPath(path, P(ray))


def mascot(c, rng, board=(36, 74, 60)):
    c.save(); c.translate(540, 560); c.rotate(-6)
    # patas de caballete
    for x0, x1 in ((-170, -230), (170, 230)):
        poly(c, [(x0, 150), (x1, 380)], INK, 30)
        poly(c, [(x0, 150), (x1, 380)], (176, 118, 66), 16)
    # brazo izquierdo saludando
    poly(c, [(-300, 20), (-390, -70), (-400, -170)], INK, 26)
    c.drawCircle(-400, -185, 40, P(INK)); c.drawCircle(-400, -185, 30, P("white"))
    # brazo derecho con la tiza
    poly(c, [(300, 40), (380, 90), (420, 20)], INK, 26)
    c.save(); c.translate(430, 0); c.rotate(-35)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-16, -80, 16, 20), 10, 10), P(INK))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-9, -72, 9, 12), 7, 7), P(CHALK))
    c.restore()
    c.drawCircle(420, 22, 40, P(INK)); c.drawCircle(420, 22, 30, P("white"))
    # cuerpo: marco de madera con contorno de pegatina
    outer = skia.Rect(-320, -250, 320, 200)
    c.drawRRect(skia.RRect.MakeRectXY(outer.makeOutset(24, 24), 46, 46), P("white"))
    c.drawRRect(skia.RRect.MakeRectXY(outer.makeOutset(10, 10), 38, 38), P(INK))
    c.drawRRect(skia.RRect.MakeRectXY(outer, 30, 30), P((176, 118, 66)))
    inner = skia.Rect(-280, -212, 280, 162)
    c.drawRRect(skia.RRect.MakeRectXY(inner, 12, 12), P(board))
    # polvo de tiza
    for _ in range(900):
        x, y = rng.uniform(-275, 275), rng.uniform(-205, 155)
        c.drawCircle(x, y, rng.uniform(.6, 2), skia.Paint(Color=skia.Color(255, 255, 255, int(rng.uniform(5, 20))), AntiAlias=True))
    # cara: ojos grandes de dibujo animado
    for ex in (-110, 110):
        c.drawOval(skia.Rect(ex - 62, -150, ex + 62, -10), P("white"))
        c.drawOval(skia.Rect(ex - 62, -150, ex + 62, -10), P(INK, w=10, fill=False))
        c.drawCircle(ex + 16, -70, 30, P(INK))
        c.drawCircle(ex + 26, -82, 10, P("white"))
    # cejas: una levantada (curiosidad)
    chalk(c, [(-165, -182), (-110, -196), (-55, -184)], rng, CHALK, 14)
    chalk(c, [(55, -205), (110, -228), (165, -214)], rng, CHALK, 14)
    # sonrisa de tiza
    chalk(c, list(wb.arc_pts(0, 20, 95, 25, 155, 30)), rng, CHALK, 14)
    # signo de interrogación amarillo escrito en la esquina
    chalk(c, list(wb.arc_pts(220, -155, 26, 200, 400, 24)) + [(226, -118), (220, -100)], rng, YEL, 12)
    c.drawCircle(220, -78, 7, P(YEL))
    c.restore()


def make(name, bg, ray, board=(36, 74, 60), seed=4):
    rng = np.random.default_rng(seed)
    s = skia.Surface(S, S); c = s.getCanvas()
    sunburst(c, bg, ray)
    mascot(c, rng, board)
    s.makeImageSnapshot().save(os.path.join(OUT, name), skia.kPNG)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    make("foto_perfil_D_mascota_amarilla.png", (255, 204, 51), (255, 222, 110))
    make("foto_perfil_E_mascota_turquesa.png", (32, 178, 170), (70, 200, 192))
    make("foto_perfil_F_mascota_coral.png", (255, 140, 105), (255, 168, 138), board=(30, 32, 38))
    print("ok")
