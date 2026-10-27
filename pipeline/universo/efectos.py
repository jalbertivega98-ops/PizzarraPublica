"""Efectos visuales cartoon: onomatopeyas, estrellas, polvo, líneas de velocidad, lluvia de monedas, billetes que vuelan, flash.

Elemento {"type": "efecto", "efecto": ..., "at", "vida": s} con:
  pum        {"x", "y", "text": "¡PUM!", "size", "color"}: estallido con onomatopeya
  estrellas  {"x", "y", "r"}: estrellitas girando (tras un golpe)
  lineas     {"x", "y", "w", "h", "dir": 1|-1}: líneas de velocidad
  lluvia     {"objeto": "moneda", "n", "x0", "x1", "y0", "suelo", "scale"}: caen con gravedad y rebotan
  vuelan     {"objeto": "billete", "n", "x", "y", "scale"}: salen volando y se van (dinero que desaparece)
  flash      {}: destello blanco de pantalla
  polvo      {"x", "y"}: nube de polvo
  fuego      {"x", "y", "scale"}: llamas cartoon que bailan y sueltan chispas (contenedores, coches); "vida" = lo que dura
"""
import math

import numpy as np
import skia

from .estilo import COL, elipse, pieza, poly, relleno, texto_cartoon, trazo

VIDA = {"pum": 0.9, "estrellas": 1.4, "lineas": 0.8, "lluvia": 2.2, "vuelan": 1.8, "flash": 0.3, "polvo": 0.6, "fuego": 3.0}


def tamano(s):
    k = s["efecto"]
    if k == "lluvia":
        return abs(s.get("x1", 900) - s.get("x0", 180)), 600
    if k == "lineas":
        return s.get("w", 500), s.get("h", 300)
    return 360, 300


def _estrella(c, x, y, r, rot=0.0, color="amarillo", w=5):
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36 - 90)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    pieza(c, poly(pts), color, w)


def estrellas_cabeza(c, t, r=150, n=4):
    for i in range(n):
        a = t * 5 + i * 2 * math.pi / n
        _estrella(c, r * math.cos(a), 34 * math.sin(a), 30 + 6 * math.sin(a), t * 200, "amarillo")


def polvo(c, x, y, k, sc=1.0, dirx=0):
    """Nubecitas de polvo que se abren y desaparecen (k de 0 a 1)."""
    a = int(200 * (1 - k))
    for i, (ox, r) in enumerate(((-1, 46), (1, 46), (-0.5, 34), (0.6, 30))):
        px = x + (ox * (90 + 120 * k) - dirx * 60 * k) * sc
        py = y - (10 + 30 * k * (1 + i % 2)) * sc
        rr = r * (0.6 + 0.8 * k) * sc
        c.drawCircle(px, py, rr, relleno((236, 232, 224), a))
        c.drawCircle(px, py, rr, trazo(4 * sc, (120, 116, 110), int(a * 0.7)))


def _rng(e):
    return np.random.default_rng(int(abs(e.spec.get("x", 0)) * 7 + abs(e.spec.get("x0", 0)) + e.t0 * 100) % 2 ** 31)


def dibuja(c, e, t, am):
    s = e.spec
    k_e = s["efecto"]
    vida = s.get("vida", VIDA.get(k_e, 1.0))
    q = (t - e.t0) / vida
    if q < 0 or q >= 1:
        return
    a = int(255 * am * (1 if q < 0.75 else (1 - q) / 0.25))
    sc = s.get("scale", 1.0)
    if k_e == "pum":
        x, y = s.get("x", 540), s.get("y", 800)
        k = min(1.0, q / 0.18)
        z = sc * (0.3 + 0.8 * k - 0.1 * max(0.0, (q - 0.18)))
        c.save(); c.translate(x, y); c.rotate(s.get("rot", -8)); c.scale(z, z)
        if a < 255:
            c.saveLayerAlpha(None, a)
        pts = []
        for i in range(24):
            ang = math.radians(i * 15)
            rr = 190 if i % 2 == 0 else 120 + 18 * ((i * 7) % 3)
            pts.append((rr * math.cos(ang) * 1.25, rr * math.sin(ang)))
        pieza(c, poly(pts), s.get("fondo", "amarillo"), 8)
        texto_cartoon(c, s.get("text", "¡PUM!"), 0, s.get("size", 92) * 0.35, s.get("size", 92), color=s.get("color", "rojo"))
        if a < 255:
            c.restore()
        c.restore()
    elif k_e == "estrellas":
        c.save(); c.translate(s.get("x", 540), s.get("y", 700)); c.scale(sc, sc)
        if a < 255:
            c.saveLayerAlpha(None, a)
        estrellas_cabeza(c, t, s.get("r", 150))
        if a < 255:
            c.restore()
        c.restore()
    elif k_e == "lineas":
        x, y, w, h = s.get("x", 540), s.get("y", 900), s.get("w", 500), s.get("h", 300)
        d = s.get("dir", 1)
        rng = _rng(e)
        for i in range(9):
            yy = y - h / 2 + h * (i + 0.5) / 9
            ln = w * (0.3 + 0.5 * rng.random())
            off = ((t * 1800 * d + rng.random() * w) % (w * 1.4)) - w * 0.7
            x0 = x - d * off
            c.drawLine(x0, yy, x0 - d * ln, yy, trazo(7, "blanco", int(a * 0.9)))
            c.drawLine(x0, yy, x0 - d * ln, yy, trazo(3, (60, 60, 70), int(a * 0.5)))
    elif k_e == "flash":
        c.drawRect(skia.Rect(-400, -400, 1500, 2400), relleno("blanco", int(230 * (1 - q) * am)))
    elif k_e == "polvo":
        polvo(c, s.get("x", 540), s.get("y", 1340), q, sc)
    elif k_e == "fuego":
        fuego(c, s.get("x", 540), s.get("y", 1300), t - e.t0, sc, a, _rng(e))
    elif k_e in ("lluvia", "vuelan"):
        from . import objetos
        rng = _rng(e)
        n = s.get("n", 12)
        tt = t - e.t0
        for i in range(n):
            if k_e == "lluvia":
                t_i = tt - i * s.get("cada", 0.09)
                if t_i < 0:
                    continue
                x0 = s.get("x0", 180) + (s.get("x1", 900) - s.get("x0", 180)) * rng.random()
                suelo = s.get("suelo", 1300) - rng.random() * 40
                y = s.get("y0", -150) + 0.5 * 4200 * t_i ** 2
                t_hit = math.sqrt(max(0.0, 2 * (suelo - s.get("y0", -150)) / 4200))
                ang = t_i * 600 * (1 if i % 2 else -1)
                if t_i > t_hit:  # rebote amortiguado
                    tb = t_i - t_hit
                    v = 4200 * t_hit * 0.35
                    y = suelo - max(0.0, v * tb - 0.5 * 4200 * tb ** 2)
                    ang = 0 if v * tb - 0.5 * 4200 * tb ** 2 <= 0 else ang
                    x0 += 60 * tb * (1 if i % 2 else -1)
                c.save(); c.translate(x0, y); c.rotate(ang); c.scale(sc * 0.5, sc * 0.5)
                if a < 255:
                    c.saveLayerAlpha(None, a)
                objetos.dibuja(c, s.get("objeto", "moneda"), t, gira=True)
                if a < 255:
                    c.restore()
                c.restore()
            else:  # vuelan: salen hacia arriba con aleteo
                t_i = tt - i * 0.06
                if t_i < 0:
                    continue
                vx = (rng.random() - 0.3) * 700
                vy = -900 - rng.random() * 500
                x = s.get("x", 540) + vx * t_i + 40 * math.sin(t_i * 9 + i)
                y = s.get("y", 900) + vy * t_i + 300 * t_i ** 2
                c.save(); c.translate(x, y); c.rotate(25 * math.sin(t_i * 8 + i)); c.scale(sc * 0.55, sc * 0.55 * abs(math.cos(t_i * 6 + i)) + 0.1)
                if a < 255:
                    c.saveLayerAlpha(None, a)
                objetos.dibuja(c, s.get("objeto", "billete"), t)
                if a < 255:
                    c.restore()
                c.restore()


def _llama(c, x, y, w, h, t, fase, color, a):
    """Lengua de fuego: gota invertida cuya punta se mece."""
    dx = w * 0.45 * math.sin(t * 9 + fase)
    p = skia.Path()
    p.moveTo(x - w / 2, y)
    p.cubicTo(x - w * 0.7, y - h * 0.45, x + dx - w * 0.15, y - h * 0.7, x + dx, y - h)
    p.cubicTo(x + dx + w * 0.2, y - h * 0.65, x + w * 0.75, y - h * 0.4, x + w / 2, y)
    p.close()
    c.drawPath(p, relleno(color, a))
    c.drawPath(p, trazo(5, "tinta", a))


def fuego(c, x, y, tt, sc, a, rng):
    """Llamas que crecen al empezar y chispas que suben."""
    k = min(1.0, tt / 0.35)
    c.save(); c.translate(x, y); c.scale(sc * k, sc * k)
    halo = skia.Paint(AntiAlias=True, Color=skia.Color(255, 150, 40, int(70 * a / 255)),
                      MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
    c.drawCircle(0, -110, 170 + 12 * math.sin(tt * 7), halo)
    capas = (((226, 58, 48), 1.0, 0.0), ((255, 140, 30), 0.72, 1.3), ((255, 222, 80), 0.42, 2.6))
    for col, f, fase in capas:
        for j, ox in enumerate((-70, 0, 70)):
            h = (230 if ox == 0 else 170) * f * (1 + 0.12 * math.sin(tt * 11 + j * 1.7 + fase))
            _llama(c, ox * f, 0, 120 * f, h, tt, fase + j, col, a)
    for i in range(7):  # chispas
        u = (tt * 0.9 + rng.random()) % 1
        cx = (rng.random() - 0.5) * 160 + 30 * math.sin(tt * 4 + i)
        c.drawCircle(cx, -120 - u * 320, 9 * (1 - u), relleno((255, 200, 60), int(a * (1 - u))))
    c.restore()
