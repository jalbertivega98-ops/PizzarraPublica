"""Mapas dibujados a mano con contornos geográficos reales (Natural Earth, universo/geo/*.json).

Objeto del storyboard: {"type": "objeto", "objeto": "mapa", "props": {"region": "estrecho", ...}, "dibujo": 2.0}
  region     estrecho (península, Estrecho y norte de Marruecos) | atlantico (Norteamérica, Europa, África del norte)
  progreso   0-1 (si no se da, se dibuja solo en "dibujo" segundos): primero el contorno con rotulador y luego el color
  orden      ids en el orden en que se dibujan (los demás, después)
  colores    {id: color}; "otan": color para los territorios de la OTAN (atlantico)
  resalta    [ids] que se iluminan y laten (aparecen con fundido desde el instante del cambio)
  apaga      [ids] que se oscurecen
  ambito6    true: colorea solo el ámbito del artículo 6 del Tratado de la OTAN (Europa, Norteamérica e islas al
             norte del trópico de Cáncer); Ceuta, Melilla y lo que queda al sur del trópico, en gris
  lineas     [{"id", "puntos": [[lon, lat], ...], "color", "discontinua": true, "ancho", "cierra": true}]:
             se dibujan con rotulador desde el instante en que aparecen
  tropico    true: dibuja el trópico de Cáncer (23,44° N)

Los grosores de línea son constantes en pantalla aunque la cámara se acerque mucho (zoom x10 sobre Ceuta).
punto(region, lon, lat, x, y, scale) da la posición en el mundo para colocar barcos, personajes o rótulos.
"""
import json
import math
import os

import numpy as np
import skia

from .estilo import COL, TINTA, mezcla, relleno, rgb, trazo

HERE = os.path.dirname(os.path.abspath(__file__))
REGIONES = {
    # centro (lon, lat) y px por grado de latitud a escala 1
    "estrecho": {"archivo": "estrecho.json", "centro": (-3.6, 39.0), "k": 96.0},
    "atlantico": {"archivo": "atlantico.json", "centro": (-28.0, 45.0), "k": 9.0},
}
TROPICO = 23.44
TIERRA = {  # colores de relleno por territorio (amables, sin colores de partido)
    "Spain": (250, 214, 120), "Balearic Islands": (250, 214, 120), "Ceuta": (250, 214, 120), "Melilla": (250, 214, 120),
    "Portugal": (170, 214, 130), "France": (196, 178, 230), "Andorra": (240, 170, 160), "Gibraltar": (210, 210, 214),
    "Morocco": (236, 168, 120), "Algeria": (232, 206, 160),
}
TIERRA_DEF = (226, 214, 186)
MAR = (126, 196, 236)
_cache = {}


def _datos(region):
    if region not in _cache:
        r = REGIONES[region]
        d = json.load(open(os.path.join(HERE, "geo", r["archivo"])))
        lat0 = d.get("lat0", r["centro"][1])
        kx = r["k"] * math.cos(math.radians(lat0))
        lon_c, lat_c = r["centro"]
        piezas = []
        for f in d["rasgos"]:
            for pl in f["polys"]:
                pts = [((lon - lon_c) * kx, -(lat - lat_c) * r["k"]) for lon, lat in pl]
                p = skia.Path()
                p.moveTo(*pts[0])
                for q in pts[1:]:
                    p.lineTo(*q)
                p.close()
                largo = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
                lats = [lat for _, lat in pl]
                lons = [lon for lon, _ in pl]
                piezas.append({"id": f["id"], "iso": f.get("iso"), "otan": f.get("otan", False), "path": p,
                               "largo": largo, "lat": sum(lats) / len(lats), "lon": sum(lons) / len(lons), "pts": pts})
        _cache[region] = {"piezas": piezas, "kx": kx, "k": r["k"], "centro": r["centro"]}
    return _cache[region]


def local(region, lon, lat):
    d = _datos(region)
    return (lon - d["centro"][0]) * d["kx"], -(lat - d["centro"][1]) * d["k"]


def punto(region, lon, lat, x=540, y=820, scale=1.0):
    """Posición en el mundo (coordenadas de la pizarra) de un lugar del mapa colocado en (x, y) con esa escala."""
    lx, ly = local(region, lon, lat)
    return x + lx * scale, y + ly * scale


def _escala(c):
    m = c.getTotalMatrix()
    return math.hypot(m.getScaleX(), m.getSkewY()) or 1.0


def en_ambito6(p):
    """¿Entra en el ámbito del artículo 6? (territorio de un aliado en Europa o Norteamérica, Turquía o islas del
    Atlántico norte al norte del trópico de Cáncer). Ceuta, Melilla y lo que está al sur del trópico, no."""
    if not p["otan"] or p["id"] in ("Ceuta", "Melilla"):
        return False
    if p["lat"] < TROPICO:  # Hawái, Puerto Rico, Guayana Francesa…
        return False
    return True


def _trozo(path, k):
    """Parte inicial (0-1) del contorno, para dibujarlo con rotulador. Devuelve (path, punta)."""
    pm = skia.PathMeasure(path, False)
    L = pm.getLength()
    out = skia.Path()
    pm.getSegment(0, L * k, out, True)
    pos, _ = pm.getPosTan(L * k)
    return out, (pos.x(), pos.y())


def _primeros(t, cambios, campo):
    """Instante en que aparece por primera vez cada id de una lista de props (resalta, lineas…)."""
    vistos = {}
    for tc, props in cambios:
        for it in props.get(campo, []) or []:
            i = it["id"] if isinstance(it, dict) else it
            vistos.setdefault(i, tc)
    return vistos


def mapa(c, t=0.0, region="estrecho", progreso=1.0, orden=(), colores=None, resalta=(), apaga=(), ambito6=False,
         lineas=(), tropico=False, mar=True, _cambios=(), _t0=0.0, **kw):
    d = _datos(region)
    esc = _escala(c)
    w = 1.0 / esc  # 1 px de pantalla en unidades locales
    colores = colores or {}
    piezas = d["piezas"]
    orden = list(orden)
    piezas = sorted(piezas, key=lambda p: (orden.index(p["id"]) if p["id"] in orden else len(orden), -p["largo"]))
    if mar:  # mar con olitas que se mueven (cubre de sobra lo que ve la cámara)
        R = 9000
        c.drawRect(skia.Rect(-R, -R, R, R), relleno(MAR))
        _olas(c, t, w, esc)
    if tropico:
        _, y = local(region, 0, TROPICO)
        pe = skia.Paint(Color=rgb((70, 110, 170)), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4 * w,
                        PathEffect=skia.DashPathEffect.Make([22 * w, 14 * w], -t * 40 * w))
        c.drawLine(-9000, y, 9000, y, pe)
    # contornos con rotulador: cada trozo de costa tiene su parte del progreso (los largos primero)
    total = sum(p["largo"] for p in piezas) or 1
    acum = 0.0
    tip = None
    t_res = _primeros(t, _cambios, "resalta")
    t_apa = _primeros(t, _cambios, "apaga")
    for p in piezas:
        k0, k1 = acum / total, (acum + p["largo"]) / total
        acum += p["largo"]
        # el trazo va al 70 % del progreso; el color entra en el 30 % final
        kd = min(1.0, max(0.0, (progreso / 0.7 - k0) / max(1e-6, k1 - k0)))
        kc = min(1.0, max(0.0, (progreso - 0.7) / 0.3)) if progreso < 1 else 1.0
        if kd <= 0:
            continue
        col = colores.get(p["id"], colores.get(p["iso"], TIERRA.get(p["id"], TIERRA_DEF)))
        if region == "atlantico":
            col = colores.get("otan", (120, 170, 235)) if p["otan"] else TIERRA_DEF
            if ambito6:
                col = colores.get("otan", (120, 170, 235)) if en_ambito6(p) else (205, 205, 210)
                if p["id"] in ("Ceuta", "Melilla"):
                    col = colores.get("fuera", (230, 70, 60))
        if p["id"] in apaga:
            ka = _eo((t - t_apa.get(p["id"], -9)) / 0.4)
            col = mezcla(col, (150, 150, 158), 0.7 * ka)
        if kd >= 1 and kc > 0:
            # sombrita bajo la tierra (relieve de recortable) y relleno
            c.save(); c.translate(5 * w, 7 * w)
            c.drawPath(p["path"], relleno((40, 70, 110), int(60 * kc)))
            c.restore()
            c.drawPath(p["path"], relleno(col, int(255 * kc)))
        if p["id"] in resalta:
            ka = _eo((t - t_res.get(p["id"], -9)) / 0.4)
            lat = 0.5 + 0.5 * math.sin((t - t_res.get(p["id"], 0)) * 7)
            halo = trazo((14 + 10 * lat) * w * ka + 0.01, (255, 236, 90), int(230 * ka))
            c.drawPath(p["path"], halo)
            c.drawPath(p["path"], relleno(mezcla(col, (255, 240, 120), 0.45), int(255 * ka * kc)))
        gro = 4.2 * w if p["largo"] * esc > 60 else 3.0 * w
        if kd < 1:
            seg, tip = _trozo(p["path"], kd)
            c.drawPath(seg, trazo(gro, TINTA))
        else:
            c.drawPath(p["path"], trazo(gro, TINTA))
    if region == "atlantico" and ambito6 and progreso >= 1:  # Ceuta y Melilla: anillo rojo que late (son diminutas)
        for p in piezas:
            if p["id"] in ("Ceuta", "Melilla"):
                x, y = local(region, p["lon"], p["lat"])
                r = (16 + 5 * math.sin(t * 6)) * w
                c.drawCircle(x, y, r, trazo(5 * w, (230, 50, 40)))
    for ln in lineas or ():
        _linea(c, region, ln, t, w, _primeros(t, _cambios, "lineas").get(ln.get("id"), _t0))
    return tip


def _eo(k):
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 3


def _olas(c, t, w, esc):
    """Olitas «~» repartidas por el mar; su tamaño es fijo en pantalla."""
    m = c.getTotalMatrix()
    inv = skia.Matrix()
    if not m.invert(inv):
        return
    # zona visible en coordenadas locales
    r = inv.mapRect(skia.Rect(0, 0, 1080, 1920))
    paso = 150 * w
    x0 = math.floor(r.left() / paso) * paso
    y0 = math.floor(r.top() / paso) * paso
    pe = trazo(3.2 * w, (232, 246, 255), 200)
    y = y0
    fila = 0
    while y < r.bottom() + paso:
        x = x0 + (paso / 2 if fila % 2 else 0)
        while x < r.right() + paso:
            ox = x + 18 * w * math.sin(t * 1.3 + (x + y) * esc * 0.01)
            p = skia.Path()
            a = 16 * w
            p.moveTo(ox - 2 * a, y)
            p.quadTo(ox - 1.5 * a, y - a * 0.7, ox - a, y)
            p.quadTo(ox - 0.5 * a, y + a * 0.7, ox, y)
            c.drawPath(p, pe)
            x += paso
        y += paso
        fila += 1


def _linea(c, region, ln, t, w, t_apar):
    pts = [local(region, lon, lat) for lon, lat in ln["puntos"]]
    if ln.get("suave", True) and len(pts) > 2:
        from .estilo import suave
        p = suave(pts, close=ln.get("cierra", False))
    else:
        p = skia.Path()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if ln.get("cierra"):
            p.close()
    k = _eo((t - t_apar) / ln.get("dur", 1.0))
    if k <= 0:
        return
    seg, _ = _trozo(p, k)
    col = ln.get("color", "rojo")
    if ln.get("relleno") and k >= 1:
        c.drawPath(p, relleno(ln["relleno"], ln.get("alfa", 70)))
    efecto = skia.DashPathEffect.Make([26 * w, 18 * w], -t * 30 * w) if ln.get("discontinua") else None
    blanco = trazo((ln.get("ancho", 7) + 5) * w, "blanco", 220)
    c.drawPath(seg, blanco)
    pe = trazo(ln.get("ancho", 7) * w, col)
    if efecto is not None:
        pe.setPathEffect(efecto)
    c.drawPath(seg, pe)
