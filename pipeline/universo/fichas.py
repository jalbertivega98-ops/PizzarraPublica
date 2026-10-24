#!/usr/bin/env python3
"""Genera las hojas de modelo del universo en docs/identidad/ (personajes, caras, poses, edificios, objetos, fondos).

Uso: python3 universo/fichas.py   (vuelve a generarlas tras cambiar la biblioteca)
"""
import os
import sys

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from universo import edificios, fondos, objetos, personajes  # noqa: E402
from universo.estilo import texto_cartoon  # noqa: E402

OUT = os.path.join(HERE, "..", "..", "docs", "identidad")
FONDO = skia.Color(246, 242, 234)


def hoja(nombre, W, H, items, cols, cw, ch, escala, dibujar, etiqueta, oy):
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(FONDO)
    for i, it in enumerate(items):
        x, y = cw / 2 + (i % cols) * cw, (i // cols) * ch
        c.save(); c.translate(x, y + oy); c.scale(escala, escala)
        dibujar(c, it)
        c.restore()
        texto_cartoon(c, etiqueta(it), x, y + ch - 30, 44, color="blanco", borde=3)
    s.makeImageSnapshot().save(os.path.join(OUT, nombre))
    print(nombre)


def main():
    os.makedirs(OUT, exist_ok=True)
    P = personajes
    hoja("ficha_personajes.png", 2500, 1700, list(P.PERSONAJES), 5, 500, 850, 0.8,
         lambda c, q: P.dibuja(c, q, t=0.3), lambda q: P.PERSONAJES[q]["nombre"], 400)
    hoja("ficha_caras.png", 2400, 1000, list(P.EXPRESIONES), 8, 300, 500, 0.5,
         lambda c, e: P.dibuja(c, "piz", cara=e, t=0.3), lambda e: e, 230)
    hoja("ficha_poses.png", 2700, 1100, list(P.POSES), 9, 300, 550, 0.45,
         lambda c, p: P.dibuja(c, "piz", pose=p, t=0.3), lambda p: p, 250)
    hoja("ficha_edificios.png", 3000, 1600, list(edificios.TIPOS), 4, 750, 800, 0.62,
         lambda c, b: edificios.dibuja(c, b, {}, 0.3), lambda b: b, 680)
    hoja("ficha_objetos.png", 3000, 1900, list(objetos.TIPOS), 6, 500, 475, 0.62,
         lambda c, o: objetos.dibuja(c, o, 0.3, **({"texto": "TEXTO"} if o in ("cartel", "bocadillo") else {})),
         lambda o: o, 200)
    def fondo(c, f):
        c.clipRect(skia.Rect(0, 0, 1080, 1920))
        fondos.dibuja(c, f, 0.3)
    hoja("ficha_fondos.png", 2400, 900, list(fondos.TIPOS), 6, 400, 900, 0.37, lambda c, f: (c.translate(-540, 0), fondo(c, f)),
         lambda f: f, 0)


if __name__ == "__main__":
    main()
