"""Iluminación y ambiente por escena: "luz": [{"at", "tipo": normal|oscuro|foco|alarma|atardecer|noche, "sobre": id, "r"}].

Se dibuja encima de los elementos (dentro de la cámara), con fundido de 0,3 s entre estados.
"""
import math

import skia

AREA = skia.Rect(-600, -600, 1700, 2600)


def _capa(c, tipo, k, t, els, x):
    if tipo == "normal" or k <= 0:
        return
    if tipo in ("oscuro", "noche"):
        col = (10, 12, 30) if tipo == "noche" else (0, 0, 0)
        c.drawRect(AREA, skia.Paint(Color=skia.Color(*col, int((150 if tipo == "oscuro" else 120) * k))))
    elif tipo == "foco":
        e = next((e for e in els if e.spec.get("id") == x.get("sobre")), None)
        if e is not None:
            x0, y0, x1, y1 = e.bbox()
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        else:
            cx, cy = x.get("x", 540), x.get("y", 900)
        r = x.get("r", 420)
        sh = skia.GradientShader.MakeRadial(skia.Point(cx, cy), r * 1.25,
                                            [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, int(190 * k))],
                                            [0.0, 0.72, 1.0])
        p = skia.Paint(AntiAlias=True)
        p.setShader(sh)
        c.drawRect(AREA, p)
    elif tipo == "alarma":
        a = int(90 * k * (0.5 + 0.5 * math.sin(t * 9)))
        c.drawRect(AREA, skia.Paint(Color=skia.Color(230, 40, 40, a)))
    elif tipo == "atardecer":
        c.drawRect(AREA, skia.Paint(Color=skia.Color(255, 140, 60, int(60 * k))))


def dibuja(c, luces, t, els):
    actual, prev = None, None
    for x in luces:
        if x["t"] <= t:
            prev, actual = actual, x
    if actual is None:
        return
    k = min(1.0, (t - actual["t"]) / actual.get("dur", 0.3))
    if prev is not None and k < 1:
        _capa(c, prev["tipo"], 1 - k, t, els, prev)
    _capa(c, actual["tipo"], k, t, els, actual)
