"""Portada propia de «Si atacan Ceuta, ¿viene la OTAN?» (dibujada, no un fotograma).

Estrecho dibujado con Ceuta resaltada, un buque sin identificar frente a Ceuta, Piz vigilando con
prismáticos, la chapa de la OTAN con interrogante y el sello «NO ES AUTOMÁTICO».
Uso: python3 series/portada_ceuta_otan.py [salida.png]
"""
import os
import sys

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import portada  # noqa: E402
from universo import mapas, mundo, personajes  # noqa: E402
from universo.estilo import texto_cartoon  # noqa: E402

W, H = 1080, 1920
ZOOM = 6.0
FOCO = (540, 830)  # dónde cae Ceuta en pantalla


def main(salida):
    s = skia.Surface(W, H)
    c = s.getCanvas()
    cx, cy = mapas.punto("estrecho", -5.32, 35.89)
    # mapa del Estrecho con Ceuta resaltada
    c.save()
    c.translate(*FOCO); c.scale(ZOOM, ZOOM); c.translate(-cx, -cy)
    c.save(); c.translate(540, 820)
    mapas.mapa(c, 0.4, "estrecho", resalta=["Ceuta"],
               orden=["Spain", "Portugal", "Gibraltar", "Ceuta", "Morocco", "Melilla"])
    c.restore()
    c.restore()
    # Ceuta marcada con su bandera
    c.save(); c.translate(522, 838); c.scale(0.9, 0.9)
    mundo.chincheta(c, 0.3, diseno="ceuta")
    c.restore()
    texto_cartoon(c, "CEUTA", 400, 760, 64, color="blanco", fuente="sub")
    # buque sin identificar frente a Ceuta
    c.save(); c.translate(800, 860); c.scale(0.62, 0.62)
    mundo.barco(c, 0.3, bandera=None, numero="?", rumbo=-1)
    c.restore()
    # chapa de la OTAN con interrogante
    c.save(); c.translate(830, 470); c.rotate(8); c.scale(0.62, 0.62)
    mundo.otan(c, 0.3, texto=False)
    c.restore()
    texto_cartoon(c, "?", 945, 420, 150, color="amarillo", fuente="sub")
    # Piz vigilando
    c.save(); c.translate(270, 1000); c.scale(0.5, 0.5)
    personajes.dibuja(c, "piz", cara="sorpresa", pose="prismaticos", objeto="prismaticos", t=0.3)
    c.restore()
    # sello
    c.save(); c.translate(560, 1262); c.scale(1.05, 1.05)
    mundo.sello(c, 0.3, texto="NO ES AUTOMÁTICO", color="rojo")
    c.restore()
    portada.dibuja(c, "Si atacan Ceuta, ¿viene la OTAN?")
    s.makeImageSnapshot().save(salida, skia.kPNG)
    print(salida)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "videos", "ceuta_otan", "portada_ceuta_otan.png"))
