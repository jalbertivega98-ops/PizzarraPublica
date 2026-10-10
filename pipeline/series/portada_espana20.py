#!/usr/bin/env python3
"""Portada de «España en 20 años»: misma plantilla que las series (papel, etiqueta, título en tres líneas),
con una mini gráfica del dato estrella en lugar del icono del partido."""
import os
import sys

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import wb  # noqa: E402

TEMAS = {
    "vivienda": dict(top="¿CÓMO HA CAMBIADO", big="LA VIVIENDA", bottom="DE 2006 A 2026?",
                     foot="datos oficiales, con fuente",
                     points=[(2006, 1990.5, "1.990"), (2008, 2101.4, "2.101"), (2014, 1455.8, "1.456"), (2026, 2355, "2.355")],
                     lo=1100, hi=2450),
    "impuestos": dict(top="¿CÓMO HAN CAMBIADO", big="TUS IMPUESTOS", big_size=138, bottom="DE 2006 A 2026?",
                      foot="datos oficiales, con fuente",
                      points=[(2006, 179380, "179"), (2007, 200676, "201"), (2009, 144023, "144"), (2025, 325356, "325 mil M€")],
                      lo=100000, hi=360000),
}


def cover(tema, out_dir):
    d = TEMAS[tema]
    s = skia.Surface(1080, 1920)
    c = s.getCanvas()
    c.clear(wb.rgb("paper"))
    c.drawImage(wb.paper_texture(), 0, 0)
    c.drawRect(skia.Rect(0, 0, 1080, 24), skia.Paint(Color=wb.rgb("red")))
    tag = "ESPAÑA EN 20 AÑOS"
    f = wb.font("ui", 44)
    tw = f.measureText(tag)
    r = skia.Rect(540 - tw / 2 - 34, 400, 540 + tw / 2 + 34, 472)
    c.drawRRect(skia.RRect.MakeRectXY(r, 36, 36), skia.Paint(Color=wb.rgb("ink"), AntiAlias=True))
    c.drawString(tag, 540 - tw / 2, 451, f, skia.Paint(Color=wb.rgb("paper"), AntiAlias=True))
    rng = np.random.default_rng(3)
    for sp in [
        {"type": "text", "text": d["top"], "x": 540, "y": 640, "size": 98},
        {"type": "text", "text": d["big"], "x": 540, "y": 830, "size": d.get("big_size", 170), "color": "red"},
        {"type": "text", "text": d["bottom"], "x": 540, "y": 960, "size": 96},
        {"type": "text", "text": d["foot"], "font": "body", "x": 540, "y": 1560, "size": 62, "color": "gray"},
    ]:
        wb.Element(sp, 0, rng).draw(c, 999)
    pts = [dict(x=x, value=v, value_label=lab, color="red" if i == len(d["points"]) - 1 else "ink",
                label_dy=10 if i == 2 else -36, label_dx=95 if i == 2 else 0, label="" if i == 1 else x) for i, (x, v, lab) in enumerate(d["points"])]
    pts[0]["label_dx"] = 55
    pts[0]["label_dy"] = 80
    chart = wb.Element(dict(type="linechart", box=[200, 1060, 680, 330], min=d["lo"], max=d["hi"], x_from=2006, x_to=2026,
                            color="ink", width=12, area="red", value_size=52, label_size=32, points=pts, dur=1.0), 0, rng)
    chart.draw(c, 999)
    path = os.path.join(out_dir, f"portada_espana20_{tema}.png")
    s.makeImageSnapshot().save(path, skia.kPNG)
    return path


if __name__ == "__main__":
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out, exist_ok=True)
    print(cover(sys.argv[1] if len(sys.argv) > 1 else "vivienda", out))
