# Portada de COSAS DE PAREJA (nueva etapa, estilo sobrio): fotograma + frase en mayúsculas cursivas con una palabra en caja.
# python3 scripts/portada_pareja2.py fondo.png "¿HAS VISTO MIS" "LLAVES?" "EP. 1" salida.png   (2.ª línea va en caja)
import sys
from PIL import Image, ImageDraw, ImageFont
bg, l1, l2, ep, out = sys.argv[1:6]
im = Image.open(bg).convert('RGB').resize((1080, 1920)); W, H = im.size
F = 'scripts/fonts/Inter-ExtraBoldItalic.otf'
sh = Image.new('L', (1, H))
for y in range(H): sh.putpixel((0, y), int(max(0, 1 - abs(y - 1250) / 420) * 150))
im = Image.composite(Image.new('RGB', (W, H), (10, 8, 12)), im, sh.resize((W, H)))
d = ImageDraw.Draw(im)
def fit(s, size):
    f = ImageFont.truetype(F, size)
    while f.getlength(s) > W - 160: size -= 4; f = ImageFont.truetype(F, size)
    return f
f1 = fit(l1, 120); d.text((W / 2, 1130), l1, font=f1, fill='white', anchor='mm', stroke_width=8, stroke_fill='black')
f2 = fit(l2, 150); w = d.textlength(l2, font=f2)
d.rectangle((W / 2 - w / 2 - 30, 1210, W / 2 + w / 2 + 30, 1390), fill=(30, 106, 138))
d.text((W / 2, 1300), l2, font=f2, fill='white', anchor='mm', stroke_width=6, stroke_fill='black')
fe = ImageFont.truetype(F, 54); d.text((W / 2, 1480), f'COSAS DE PAREJA · {ep}', font=fe, fill=(255, 230, 190), anchor='mm', stroke_width=5, stroke_fill='black')
im.save(out)
