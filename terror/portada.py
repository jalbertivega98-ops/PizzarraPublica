#!/usr/bin/env python3
"""portada.py <fotograma.jpg> <salida.png> <titulo_ep> <linea1> <linea2>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
src, out, ep, l1, l2 = sys.argv[1:6]
F = __file__.rsplit('/', 1)[0] + '/fonts/'
im = Image.open(src).convert('RGB').resize((1080, 1920))
im = ImageEnhance.Brightness(im).enhance(1.25)
d = ImageDraw.Draw(im, 'RGBA')
for y in range(0, 700):  # degradado arriba y abajo
    a = int(200 * (1 - y / 700)); d.line([(0, y), (1080, y)], fill=(0, 0, 0, a)); d.line([(0, 1919 - y), (1080, 1919 - y)], fill=(0, 0, 0, a))
cre = lambda s: ImageFont.truetype(F + 'Creepster-Regular.ttf', s)
eli = lambda s: ImageFont.truetype(F + 'SpecialElite-Regular.ttf', s)
def ctext(y, s, f, fill, glow=None):
    w = d.textlength(s, font=f); x = (1080 - w) / 2
    if glow:
        g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text((x, y), s, font=f, fill=glow)
        im.paste(g.filter(ImageFilter.GaussianBlur(18)), (0, 0), g.filter(ImageFilter.GaussianBlur(18)))
    d.text((x + 6, y + 8), s, font=f, fill=(0, 0, 0, 230)); d.text((x, y), s, font=f, fill=fill)
ctext(150, 'LA CASA', cre(300), (190, 14, 14), glow=(255, 0, 0, 255))
ctext(470, ep, eli(70), (235, 228, 210))
# etiqueta roja
f = eli(64); w = d.textlength(l1, font=f)
d.rounded_rectangle([(1080 - w) / 2 - 36, 1500, (1080 + w) / 2 + 36, 1600], 18, fill=(161, 11, 11, 235))
d.text(((1080 - w) / 2, 1512), l1, font=f, fill='white')
ctext(1640, l2, eli(52), (230, 222, 205))
im.save(out); print('ok', out)
