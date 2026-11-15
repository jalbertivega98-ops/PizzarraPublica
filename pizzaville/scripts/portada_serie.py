# portada con el estilo de la serie
# uso: python3 scripts/portada_serie.py fondo.png 'EPISODIO N' 'INSIGNIA' 'línea 1' 'línea 2' salida.png
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
im = Image.open(sys.argv[1]).convert('RGB')
W, H = im.size
F = 'scripts/fonts/LilitaOne.ttf'
# soft dark gradient top and bottom for legibility
g = Image.new('L', (1, H))
for y in range(H):
    a = max(0, 1 - y / 620) * 170 + max(0, (y - 1150) / 770) * 150
    g.putpixel((0, y), int(min(200, a)))
im = Image.composite(Image.new('RGB', (W, H), (15, 20, 35)), im, g.resize((W, H)))
d = ImageDraw.Draw(im)
def text(xy, s, size, fill, stroke=10, sc=(32, 24, 16), anchor='mm'):
    f = ImageFont.truetype(F, size)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 10), s, font=f, fill=(0, 0, 0, 140), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 140))
    im.paste(sh.filter(ImageFilter.GaussianBlur(6)), (0, 0), sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sc)
text((W // 2, 250), 'PIZZAVILLE', 190, (255, 138, 61), 14, (255, 255, 255))
text((W // 2, 420), sys.argv[2], 92, (255, 255, 255), 9)
# badge
f = ImageFont.truetype(F, 120)
s = sys.argv[3]
bw = d.textlength(s, font=f) + 120
bx0, by0 = (W - bw) / 2, 1250
d = ImageDraw.Draw(im)
d.rounded_rectangle((bx0 + 8, by0 + 14, bx0 + bw + 8, by0 + 214), 46, fill=(0, 0, 0))
d.rounded_rectangle((bx0, by0, bx0 + bw, by0 + 200), 46, fill=(255, 213, 61), outline=(32, 24, 16), width=8)
d.text((W // 2, by0 + 104), s, font=f, fill=(32, 24, 16), anchor='mm')
text((W // 2, 1540), sys.argv[4], 80, (255, 255, 255), 8)
text((W // 2, 1640), sys.argv[5], 80, (255, 213, 61), 8)
im.save(sys.argv[6])
