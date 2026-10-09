#!/usr/bin/env python3
"""Tres propuestas de foto de perfil con pizarra (1080×1080, seguras para el recorte circular)."""
import math
import os
import sys

import numpy as np
import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wb  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "perfil")
S = 1080
CHALK = (244, 242, 232)


def paint(col, a=255, w=None, fill=False):
    p = skia.Paint(Color=wb.rgb(col, a), AntiAlias=True)
    if not fill:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(w or 8)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def chalk_line(c, pts, rng, col=CHALK, w=9, passes=3):
    """Trazo de tiza: varias pasadas finas con temblor y transparencia."""
    for k in range(passes):
        q = wb.wobble(pts, rng, 1.8, 8)
        wb.draw_poly(c, q, col, w * (0.55 + 0.25 * k), 120 + 40 * k)


def chalk_text(c, txt, x, y, size, rng, col=CHALK, fontname="hand"):
    f = wb.font(fontname, size)
    x0 = x - f.measureText(txt) / 2
    for k in range(3):
        dx, dy = rng.normal(0, 1.2, 2)
        c.drawString(txt, x0 + dx, y + dy, f, skia.Paint(Color=wb.rgb(col, 110 + 50 * k), AntiAlias=True))


def chalk_dust(c, rng, box, n=2500):
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        c.drawCircle(x, y, rng.uniform(0.6, 2.2), skia.Paint(Color=skia.Color(255, 255, 255, int(rng.uniform(4, 18))), AntiAlias=True))


def congreso(c, cx, base, scale, rng, col=CHALK, line=None):
    """Fachada simplificada del Palacio del Congreso: frontón, seis columnas, escalinata y leones."""
    draw = line or (lambda pts, w=9: chalk_line(c, pts, rng, col, w))
    s = scale
    W2 = 230 * s
    top = base - 330 * s
    draw([(cx - W2 - 20 * s, top + 80 * s), (cx, top), (cx + W2 + 20 * s, top + 80 * s), (cx - W2 - 20 * s, top + 80 * s)])
    draw([(cx - W2, top + 105 * s), (cx + W2, top + 105 * s)])
    for i in range(6):
        x = cx - W2 + 25 * s + i * (2 * W2 - 50 * s) / 5
        draw([(x, top + 110 * s), (x, base - 45 * s)], 8)
    for k, wdt in enumerate((W2 + 20 * s, W2 + 45 * s, W2 + 70 * s)):
        y = base - 40 * s + k * 20 * s
        draw([(cx - wdt, y), (cx + wdt, y)], 8)
    for sx in (-1, 1):  # leones esquemáticos
        lx = cx + sx * (W2 + 115 * s)
        draw([(lx - 40 * s, base + 2 * s), (lx - 40 * s, base - 35 * s), (lx + 40 * s, base - 35 * s), (lx + 40 * s, base + 2 * s)], 7)
        hx = lx + sx * 30 * s
        draw(wb.ellipse_pts(hx, base - 60 * s, 22 * s, 22 * s, n=30), 7)


def frame_board(c, color_board, wood=True, inset=150):
    r = skia.Rect(inset, inset + 60, S - inset, S - inset - 40)
    if wood:
        c.drawRRect(skia.RRect.MakeRectXY(r.makeOutset(28, 28), 22, 22), paint((150, 100, 58), fill=True))
        c.drawRRect(skia.RRect.MakeRectXY(r.makeOutset(28, 28), 22, 22), paint((112, 72, 38), w=5))
    c.drawRRect(skia.RRect.MakeRectXY(r, 8, 8), paint(color_board, fill=True))
    return r


def option_a():
    """Pizarra verde de colegio con el Congreso en tiza y el nombre."""
    rng = np.random.default_rng(11)
    s = skia.Surface(S, S); c = s.getCanvas()
    c.clear(wb.rgb((233, 222, 199)))
    r = frame_board(c, (38, 78, 62), inset=120)
    chalk_dust(c, rng, (r.left(), r.top(), r.right(), r.bottom()))
    congreso(c, 540, 690, 0.85, rng)
    chalk_text(c, "Pizarra Pública", 540, 830, 96, rng)
    # subrayado amarillo de tiza
    chalk_line(c, [(345, 860), (735, 852)], rng, (255, 212, 71), 10)
    # tiza en la repisa
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(640, 935, 760, 958), 10, 10), paint(CHALK, fill=True))
    s.makeImageSnapshot().save(os.path.join(OUT, "foto_perfil_A_pizarra_verde.png"), skia.kPNG)


def option_b():
    """Pizarra negra redonda (encaja con el círculo) con bocadillo y signo de interrogación de tiza amarilla."""
    rng = np.random.default_rng(5)
    s = skia.Surface(S, S); c = s.getCanvas()
    c.clear(wb.rgb((150, 100, 58)))
    c.drawCircle(540, 540, 470, paint((32, 35, 38), fill=True))
    chalk_dust(c, rng, (90, 90, 990, 990), 3000)
    # bocadillo grande
    bub = list(wb.ellipse_pts(540, 470, 300, 230, a0=120, sweep=325, n=80)) + [(390, 760), (420, 680)]
    chalk_line(c, bub, rng, CHALK, 12)
    congreso(c, 540, 600, 0.55, rng)
    # interrogación amarilla sobre el frontón
    q = list(wb.arc_pts(540, 300, 50, 200, 400, 30)) + [(552, 380), (540, 405)]
    chalk_line(c, q, rng, (255, 212, 71), 16)
    c.drawCircle(540, 445, 10, paint((255, 212, 71), fill=True))
    chalk_text(c, "PIZARRA PÚBLICA", 540, 870, 70, rng)
    s.makeImageSnapshot().save(os.path.join(OUT, "foto_perfil_B_pizarra_redonda.png"), skia.kPNG)


def option_c():
    """Pizarra blanca con marco de aluminio, la balanza (equilibrio, sin bandos) en rotulador y el nombre."""
    rng = np.random.default_rng(3)
    s = skia.Surface(S, S); c = s.getCanvas()
    c.clear(wb.rgb("yellow"))
    r = skia.Rect(150, 200, 930, 860)
    c.drawRRect(skia.RRect.MakeRectXY(r.makeOutset(22, 22), 18, 18), paint((205, 210, 216), fill=True))
    c.drawRRect(skia.RRect.MakeRectXY(r, 6, 6), paint("white", fill=True))
    ink = lambda pts, col="ink", w=12: wb.draw_poly(c, wb.wobble(pts, rng, 1.4), col, w)
    # balanza
    ink([(540, 300), (540, 640)])
    ink([(470, 640), (610, 640)])
    ink([(330, 360), (750, 360)])
    c.drawCircle(540, 300, 14, paint("ink", fill=True))
    for x in (330, 750):
        ink([(x, 360), (x - 70, 480)], "ink", 7); ink([(x, 360), (x + 70, 480)], "ink", 7)
        pan = list(wb.arc_pts(x, 480, 80, 0, 180, 30))
        ink([(x - 80, 480), (x + 80, 480)])
        ink(pan)
    # pesos iguales: libro e interrogación
    ink(wb.rect_pts(290, 430, 80, 45), "ink", 8)
    f = wb.font("hand", 80)
    c.drawString("?", 728, 476, f, skia.Paint(Color=wb.rgb("ink"), AntiAlias=True))
    wb.draw_poly(c, wb.wobble([(320, 755), (760, 748)], rng, 2), "yellow", 56, 170)
    fh = wb.font("hand", 92)
    t = "Pizarra Pública"
    c.drawString(t, 540 - fh.measureText(t) / 2, 785, fh, skia.Paint(Color=wb.rgb("ink"), AntiAlias=True))
    # rotulador en la bandeja
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(600, 885, 790, 915), 12, 12), paint((60, 64, 76), fill=True))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(760, 885, 800, 915), 10, 10), paint("blue", fill=True))
    s.makeImageSnapshot().save(os.path.join(OUT, "foto_perfil_C_pizarra_blanca.png"), skia.kPNG)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    option_a(); option_b(); option_c()
    print("ok")
