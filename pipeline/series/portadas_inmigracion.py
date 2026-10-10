#!/usr/bin/env python3
"""Portadas de la Serie 3 · Inmigración: misma plantilla que Impuestos, con los papeles en lugar de la moneda."""
import os
import sys

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import wb  # noqa: E402

EPISODES = [(1, "psoe", "EL PSOE"), (2, "pp", "EL PP"), (3, "vox", "VOX"), (4, "sumar", "SUMAR")]


def cover(ep, key, name, out_dir):
    s = skia.Surface(1080, 1920)
    c = s.getCanvas()
    c.clear(wb.rgb("paper"))
    c.drawImage(wb.paper_texture(), 0, 0)
    c.drawRect(skia.Rect(0, 0, 1080, 24), skia.Paint(Color=wb.rgb(key)))
    tag = f"INMIGRACIÓN · EP. {ep}/4"
    f = wb.font("ui", 44)
    tw = f.measureText(tag)
    r = skia.Rect(540 - tw / 2 - 34, 400, 540 + tw / 2 + 34, 472)
    c.drawRRect(skia.RRect.MakeRectXY(r, 36, 36), skia.Paint(Color=wb.rgb("ink"), AntiAlias=True))
    c.drawString(tag, 540 - tw / 2, 451, f, skia.Paint(Color=wb.rgb("paper"), AntiAlias=True))
    rng = np.random.default_rng(ep)
    for sp in [
        {"type": "text", "text": "¿QUÉ HACE" if ep == 1 else "¿QUÉ HARÍA", "x": 540, "y": 650, "size": 130},
        {"type": "text", "text": name, "x": 540, "y": 850, "size": 210, "color": key},
        {"type": "text", "text": "CON LA INMIGRACIÓN?", "x": 540, "y": 975, "size": 88},
        {"type": "circle", "x": 540, "y": 1270, "rx": 190, "color": key, "width": 16},
        {"type": "icon", "name": "document", "x": 540, "y": 1270, "scale": 1.35},
        {"type": "text", "text": "propuestas, con fuente y fecha", "font": "body", "x": 540, "y": 1560, "size": 62, "color": "gray"},
    ]:
        wb.Element(sp, 0, rng).draw(c, 999)
    path = os.path.join(out_dir, f"portada_inmigracion_ep{ep}_{key}.png")
    s.makeImageSnapshot().save(path, skia.kPNG)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for ep, key, name in EPISODES:
        print(cover(ep, key, name, out))
