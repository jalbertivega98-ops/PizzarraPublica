# portada de COSAS DE PAREJA: python3 scripts/portada_pareja.py fondo.png 'EP. 1' '«NO TENGO' 'HAMBRE»' salida.png
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
im = Image.open(sys.argv[1]).convert('RGB'); W, H = im.size
F = 'scripts/fonts/LilitaOne.ttf'
g = Image.new('L', (1, H))
for y in range(H): g.putpixel((0, y), int(min(190, max(0, 1 - y / 760) * 175 + max(0, (y - 1500) / 420) * 120)))
im = Image.composite(Image.new('RGB', (W, H), (25, 15, 30)), im, g.resize((W, H)))
def text(xy, s, size, fill, stroke=12, sc=(32, 24, 16), rot=0):
    f = ImageFont.truetype(F, size)
    while f.getlength(s) > W - 120 and size > 60:
        size -= 6; f = ImageFont.truetype(F, size)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((xy[0] + 8, xy[1] + 12), s, font=f, fill=(0, 0, 0, 150), anchor='mm', stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
    lay = lay.filter(ImageFilter.GaussianBlur(7)); ImageDraw.Draw(lay).text(xy, s, font=f, fill=fill, anchor='mm', stroke_width=stroke, stroke_fill=sc)
    if rot: lay = lay.rotate(rot, center=xy, resample=Image.BICUBIC)
    im.paste(lay, (0, 0), lay)
def pill(cy, s, size, bg, fg, pad=60):
    f = ImageFont.truetype(F, size); d = ImageDraw.Draw(im)
    w = d.textlength(s, font=f) + pad * 2; x0 = (W - w) / 2; h = size * 1.5
    d.rounded_rectangle((x0 + 8, cy - h / 2 + 12, x0 + w + 8, cy + h / 2 + 12), h / 2, fill=(0, 0, 0))
    d.rounded_rectangle((x0, cy - h / 2, x0 + w, cy + h / 2), h / 2, fill=bg, outline=(32, 24, 16), width=7)
    d.text((W / 2, cy + 4), s, font=f, fill=fg, anchor='mm')
pill(150, 'COSAS DE PAREJA', 78, (168, 91, 214), (255, 255, 255))
text((W // 2, 360), sys.argv[3], 170, (255, 255, 255), 14, rot=3)
text((W // 2, 540), sys.argv[4], 190, (255, 213, 61), 14, rot=3)
pill(1760, sys.argv[2], 90, (255, 213, 61), (32, 24, 16))
im.save(sys.argv[5])
