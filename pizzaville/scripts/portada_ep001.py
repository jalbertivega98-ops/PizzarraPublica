# Portada del episodio 1: fondo del valle + Pizz celebrando + marcador.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
bg, pizz, out = sys.argv[1:4]
F = 'scripts/fonts/LilitaOne.ttf'
im = Image.open(bg).convert('RGB'); W, H = im.size
g = Image.new('L', (1, H))
for y in range(H): g.putpixel((0, y), int(min(210, max(0, 1 - y / 560) * 190 + max(0, (y - 1250) / 670) * 120)))
im = Image.composite(Image.new('RGB', (W, H), (15, 20, 35)), im, g.resize((W, H))).convert('RGBA')

def shadow_text(xy, s, size, fill, stroke=10, sc=(32, 24, 16), anchor='mm'):
    f = ImageFont.truetype(F, size)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + 6, xy[1] + 10), s, font=f, fill=(0, 0, 0, 150), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sc)

shadow_text((W // 2, 210), 'PIZZAVILLE', 180, (255, 138, 61), 14, (255, 255, 255))
shadow_text((W // 2, 370), 'EPISODIO 1', 86, (255, 255, 255), 9)
# VS badge
d = ImageDraw.Draw(im)
y0 = 560
for (x0, x1, col) in [(70, 520, (255, 210, 61)), (560, 1010, (127, 224, 255))]:
    d.rounded_rectangle((x0 + 8, y0 + 12, x1 + 8, y0 + 262), 40, fill=(0, 0, 0, 200))
    d.rounded_rectangle((x0, y0, x1, y0 + 250), 40, fill=col, outline=(32, 24, 16), width=8)
fb, fs = ImageFont.truetype(F, 150), ImageFont.truetype(F, 58)
d.text((295, y0 + 100), '37', font=fb, fill=(32, 24, 16), anchor='mm'); d.text((295, y0 + 205), 'EUROPA', font=fs, fill=(32, 24, 16), anchor='mm')
d.text((785, y0 + 100), '25', font=fb, fill=(32, 24, 16), anchor='mm'); d.text((785, y0 + 205), 'AMÉRICA', font=fs, fill=(32, 24, 16), anchor='mm')
d.ellipse((470, y0 + 55, 610, y0 + 195), fill=(230, 60, 60), outline=(255, 255, 255), width=8)
d.text((540, y0 + 128), 'VS', font=ImageFont.truetype(F, 66), fill=(255, 255, 255), anchor='mm')
# Pizz celebrating, bottom
p = Image.open(pizz).convert('RGBA')
bb = p.getbbox(); p = p.crop(bb)
s = 1000 / p.height; p = p.resize((int(p.width * s), 1000), Image.LANCZOS)
sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 120), (W // 2 - p.width // 2 + 14, 1080 + 14), p)
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
im.alpha_composite(p, (W // 2 - p.width // 2, 1080))
shadow_text((W // 2, 960), '¿QUIÉN GANARÁ?', 96, (255, 255, 255), 10)
shadow_text((250, 1620), '62 VECINOS', 70, (255, 210, 61), 8)
shadow_text((830, 1620), '13 PAÍSES', 70, (127, 224, 255), 8)
im.convert('RGB').save(out)
im.convert('RGB').resize((360, 640)).save('/tmp/claude-0/portada1_s.png')
