"""Portada estándar de los episodios (misma plantilla para todos los vídeos).

Fotograma del momento más visual del episodio arriba + franja inferior fija con:
  pastilla «CAPÍTULO N», título en dos líneas (amarillo con contorno) y @pizarrapublica.
El título queda dentro del recorte 4:5 de la cuadrícula de Instagram (y 285-1635).

En el storyboard: "portada": {"t": 7.85, "titulo": "Piz y la casa imposible", "capitulo": 1}
Uso suelto: python3 portada.py storyboards/<slug>.json [--out ../videos]
make_video.py la genera sola al terminar el render si el storyboard trae "portada".
"""
import argparse
import json
import os
import subprocess
import tempfile

import skia

import wb
from universo import estilo

W, H = 1080, 1920
FRANJA = 1370  # desde aquí hacia abajo, panel fijo (tapa subtítulos y notas del fotograma)


def _lineas(titulo):
    """Parte el título en dos líneas lo más equilibradas posible."""
    pal = titulo.upper().split()
    if len(pal) < 3:
        return [" ".join(pal)]
    mejor = min(range(1, len(pal)), key=lambda i: abs(len(" ".join(pal[:i])) - len(" ".join(pal[i:]))))
    return [" ".join(pal[:mejor]), " ".join(pal[mejor:])]


def _ajusta(txt, fuente, size, ancho):
    while wb.font(fuente, size).measureText(txt) > ancho and size > 40:
        size -= 4
    return size


def dibuja(c, titulo, capitulo=None, handle="@pizarrapublica"):
    # panel inferior con borde superior en zigzag de tiza
    p = skia.Path()
    p.moveTo(0, FRANJA + 18)
    for i, x in enumerate(range(0, W + 60, 60)):
        p.lineTo(x, FRANJA + (0 if i % 2 else 18))
    p.lineTo(W, H)
    p.lineTo(0, H)
    p.close()
    c.drawPath(p, skia.Paint(Color=wb.rgb(estilo.TINTA), AntiAlias=True))
    y = FRANJA + 110
    if capitulo is not None:
        cap = f"CAPÍTULO {capitulo}"
        f = wb.font("sub", 40)
        w = f.measureText(cap)
        r = skia.RRect.MakeRectXY(skia.Rect(W / 2 - w / 2 - 34, y - 46, W / 2 + w / 2 + 34, y + 18), 32, 32)
        c.drawRRect(r, skia.Paint(Color=wb.rgb(estilo.COL["rojo"]), AntiAlias=True))
        c.drawString(cap, W / 2 - w / 2, y + 2, f, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        y += 120
    lineas = _lineas(titulo)
    size = min(_ajusta(l, "sub", 112, W - 110) for l in lineas)
    for l in lineas:
        estilo.texto_cartoon(c, l, W / 2, y, size, color="amarillo", fuente="sub")
        y += size * 1.05
    f = wb.font("ui", 38)
    w = f.measureText(handle)
    c.drawString(handle, W / 2 - w / 2, min(H - 60, y + 30), f, skia.Paint(Color=skia.Color(255, 255, 255, 200), AntiAlias=True))


def genera(video, salida, t, titulo, capitulo=None):
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "f.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", png], check=True)
        img = skia.Image.open(png)
        surf = skia.Surface(W, H)
        c = surf.getCanvas()
        c.drawImageRect(img, skia.Rect(0, 0, W, H))
        dibuja(c, titulo, capitulo)
        surf.makeImageSnapshot().save(salida, skia.kPNG)
    return salida


def desde_storyboard(story, outdir):
    cfg = story.get("portada")
    if not cfg:
        return None
    slug = story["slug"]
    video = os.path.join(outdir, f"{slug}.mp4")
    return genera(video, os.path.join(outdir, f"portada_{slug}.png"), cfg.get("t", 2.0),
                  cfg.get("titulo", story.get("title", "")), cfg.get("capitulo"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "videos"))
    a = ap.parse_args()
    st = json.load(open(a.storyboard, encoding="utf-8"))
    print(desde_storyboard(st, os.path.join(a.out, st["slug"])))
