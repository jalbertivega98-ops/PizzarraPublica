"""Ayudas comunes de la serie «TU DINERO, CON DATOS» (episodios sueltos con Piz y compañía)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import compra2026 as base  # noqa: E402,F401
from compra2026_serie import obj, pj, plano, rot, edif  # noqa: E402,F401
from padres_viva import V  # noqa: E402,F401
from universo import gags  # noqa: E402,F401

C = "red"
MEJOR_HORA = "TikTok martes a jueves 20:00-21:30 · Instagram Reels 13:30 o 20:30"


def quien(q, x, at=0.0, scale=0.75, cara="normal", acciones=(), **kw):
    kw.setdefault("id", q)
    return pj(q, x, at, scale, cara, acciones, **kw)


def etq(texto, x, y, at, color="amarillo", scale=0.75, **kw):
    return obj("etiqueta", x, y, at, scale, props={"texto": texto, "color": color}, entra="pop", sfx="kaching", **kw)


def pum(text, x, y, at, scale=0.75):
    return dict(type="efecto", efecto="pum", text=text, x=x, y=y, at=at, scale=scale, vida=0.8)


def monedas(at, x0=200, x1=880, n=10):
    return dict(type="efecto", efecto="lluvia", objeto="moneda", n=n, x0=x0, x1=x1, at=at, vida=1.8)


def episodio(slug, title, scenes, portada, sources, caption, pinned, hashtags):
    SB = dict(base.SB)
    SB.update(slug=slug, title=title, series_tag="TU DINERO, CON DATOS", scenes=scenes, banda=True, music_volume=0.2,
              scribble_volume=0.0, sfx_volume=1.0, end_hold=0.9, portada=portada, sources=sources, caption=caption,
              pinned_comment=pinned, hashtags=hashtags)
    path = os.path.join(OUT, f"{slug}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
    return SB
