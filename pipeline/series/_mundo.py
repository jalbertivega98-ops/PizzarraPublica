"""Ayudas comunes de los episodios del mundo dibujado (mapas, sellos de verificación, atriles de partidos).
Plantilla de referencia: series/ceuta_otan.py. Norma visual: docs/serie.md, sección 10."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from _tu_dinero import *  # noqa: F401,F403,E402
from _tu_dinero import obj, plano, rot  # noqa: E402
from universo import mapas  # noqa: E402,F401

MX, MY = 540, 820  # los mapas se colocan aquí, a escala 1
LIM = [-6000, -6000, 7000, 7000]  # en los mapas la cámara puede ir lejos (el mar es infinito)
SUELO_ATRIL = 1350


def quien(q, x, at=0.0, scale=0.75, cara="normal", acciones=(), y=1340, **kw):
    kw.setdefault("id", q)
    return dict(type="personaje", quien=q, x=x, y=y, scale=scale, at=at, cara=cara, acciones=list(acciones), **kw)


def P(region, lon, lat):
    return [round(v, 1) for v in mapas.punto(region, lon, lat, MX, MY, 1.0)]


def mapa(region, at=0.0, dibujo=1.6, acciones=(), id="mapa", **props):
    return obj("mapa", MX, MY, at, 1.0, id=id, entra="nada", dibujo=dibujo,
               props={"region": region, **props}, acciones=list(acciones))


def zoom(at, sobre, z, dur=0.9, **kw):
    """Plano sobre un punto del mapa con zoom z (veces el plano general)."""
    return plano(at, "general", list(sobre), dur, zoom=z, **kw)


def sello(texto, color, y, at, out=None, x=540):
    d = obj("sello", x, y, at, 1.0, hud=True, props={"texto": texto, "color": color}, entra="pop", sfx="golpe")
    if out:
        d["out"] = out
    return d


def atriles(t=(0, 0.15, 0.3), xs=(230, 540, 850)):
    """Los tres atriles PSOE, PP y Vox (los personajes van antes, detrás)."""
    return [obj("atril", x, SUELO_ATRIL, at, 0.46, props={"texto": tx, "color": col}, entra="nada")
            for x, at, tx, col in zip(xs, t, ("PSOE", "PP", "VOX"), ("psoe", "pp", "vox"))]


def linea(id, puntos, color="rojo", dur=1.0, **kw):
    return {"id": id, "puntos": [list(p) for p in puntos], "color": color, "dur": dur, **kw}
