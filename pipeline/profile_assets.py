#!/usr/bin/env python3
"""Genera la identidad del perfil: foto de perfil, portadas de destacados y portada de reel."""
import os
import sys

import numpy as np
import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wb  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "perfil")


def canvas(w, h):
    s = skia.Surface(w, h)
    c = s.getCanvas()
    c.clear(wb.rgb("paper"))
    return s, c


def draw(c, specs, seed=1):
    rng = np.random.default_rng(seed)
    for sp in specs:
        wb.Element(sp, 0, rng).draw(c, 999)


def save(s, name):
    os.makedirs(OUT, exist_ok=True)
    s.makeImageSnapshot().save(os.path.join(OUT, name), skia.kPNG)


def house_specs(x, y, sc=1.0, color="ink"):
    p = lambda pts: [[x + a * sc, y + b * sc] for a, b in pts]
    return [
        {"type": "line", "pts": p([(-110, -10), (0, -110), (110, -10)]), "color": color, "width": 12},
        {"type": "line", "pts": p([(-80, -30), (-80, 100), (80, 100), (80, -30)]), "color": color, "width": 12},
        {"type": "rect", "box": [x - 25 * sc, y + 35 * sc, 50 * sc, 65 * sc], "color": color, "width": 10, "fill": "yellow"},
    ]


def avatar():
    """1080×1080. Instagram la recorta en círculo: todo va dentro del círculo central."""
    s, c = canvas(1080, 1080)
    c.drawCircle(540, 540, 540, skia.Paint(Color=wb.rgb("paper"), AntiAlias=True))
    draw(c, [
        {"type": "hemicycle", "x": 540, "y": 640, "r_in": 120, "r_out": 330, "rows": 7, "dot": 13,
         "count": 140, "color": "ink", "highlight": 0},
        {"type": "highlight", "x0": 300, "x1": 780, "y": 770, "width": 70},
        {"type": "text", "text": "PIZARRA", "x": 540, "y": 800, "size": 118, "color": "ink"},
        {"type": "text", "text": "PÚBLICA", "x": 540, "y": 905, "size": 92, "color": "blue"},
    ])
    wb.draw_marker(c, np.array([760, 400]), "blue")
    save(s, "foto_perfil.png")


def highlight(name, label, specs):
    """Portada de destacado: 1080×1920, icono centrado (Instagram muestra el círculo central)."""
    s, c = canvas(1080, 1920)
    c.drawCircle(540, 960, 420, skia.Paint(Color=wb.rgb("white"), AntiAlias=True))
    draw(c, specs + [{"type": "circle", "x": 540, "y": 960, "rx": 420, "color": "ink", "width": 14}])
    save(s, f"destacado_{name}.png")


def highlights():
    highlight("empieza_aqui", "Empieza aquí", [
        {"type": "icon", "name": "question", "x": 540, "y": 900, "scale": 1.7, "color": "blue"}])
    highlight("29N", "29N", [
        {"type": "icon", "name": "calendar", "x": 540, "y": 980, "scale": 1.6},
        {"type": "text", "text": "29 N", "x": 540, "y": 1090, "size": 120, "color": "red"}])
    highlight("vivienda", "Vivienda", house_specs(540, 960, 2.0))
    highlight("partidos", "Qué proponen", [
        {"type": "icon", "name": "ballot", "x": 540, "y": 960, "scale": 1.6}])
    highlight("fuentes", "Fuentes", [
        {"type": "icon", "name": "document", "x": 540, "y": 960, "scale": 1.7},
        {"type": "check", "x": 600, "y": 1050, "r": 70, "color": "green"}])


def reel_cover():
    """Portada del reel 1. El texto va en la franja central que la cuadrícula del perfil muestra."""
    s, c = canvas(1080, 1920)
    draw(c, [
        {"type": "text", "text": "29N", "x": 540, "y": 560, "size": 90, "color": "red"},
        {"type": "text", "text": "¿VOTAS AL", "x": 540, "y": 720, "size": 150},
        {"type": "highlight", "x0": 90, "x1": 990, "y": 850, "width": 120},
        {"type": "text", "text": "PRESIDENTE?", "x": 540, "y": 900, "size": 165, "color": "blue"},
        {"type": "icon", "name": "ballot_box", "x": 330, "y": 1220, "scale": 1.1},
        {"type": "icon", "name": "person", "tie": True, "accent": "light", "x": 760, "y": 1190, "scale": 1.25},
        {"type": "cross", "x": 760, "y": 1200, "r": 130, "color": "red"},
        {"type": "text", "text": "explicado en 60 segundos", "font": "body", "x": 540, "y": 1440, "size": 64, "color": "gray"},
    ])
    save(s, "portada_reel01.png")


if __name__ == "__main__":
    avatar()
    highlights()
    reel_cover()
    print("Guardado en", os.path.abspath(OUT))
