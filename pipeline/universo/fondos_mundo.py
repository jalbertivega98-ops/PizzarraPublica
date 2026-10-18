"""Fondos del mundo dibujado: la ciudad de Ceuta (murallas, Monte Hacho, puerto) y el mar de los mapas.

  ceuta     paseo junto a las Murallas Reales y su foso, casas blancas, el Monte Hacho con su fortaleza y, al otro
            lado del Estrecho, la península y el Peñón. Gaviotas, ferri cruzando, banderas ondeando, palmeras.
  carretera carretera en perspectiva entre colinas, rayas y árboles que pasan (velocidad)
  colegio   colegio electoral por dentro (pizarra, ventanales, cartel, banderines)
  mar_mapa  mar infinito con olitas (debajo de un objeto "mapa"; la escena lleva "limites" amplios)
"""
import math

import skia

from .estilo import COL, degradado, elipse, mezcla, pieza, poly, relleno, rrect, suave, trazo
from .fondos import X0, X1, Y0, Y1, SUELO, _nube, _pajaros, _rect
from .mundo import tela


def _casa(c, x, base, w, h, col, techo="teja", ventanas=2):
    pieza(c, rrect(x, base - h, x + w, base, 4), col, 4)
    if techo == "teja":
        pieza(c, poly([(x - 8, base - h), (x + w / 2, base - h - w * 0.32), (x + w + 8, base - h)]), "teja", 4)
    else:  # azotea
        c.drawRect(skia.Rect(x - 4, base - h - 8, x + w + 4, base - h), relleno(mezcla(col, "tinta", 0.15)))
    for i in range(ventanas):
        vx = x + w * (i + 0.5) / ventanas - 9
        pieza(c, rrect(vx, base - h * 0.62, vx + 18, base - h * 0.62 + 24, 4), (90, 150, 200), 3)


def _almenas(c, x0, x1, y, alto, col):
    x = x0
    while x < x1:
        pieza(c, rrect(x, y - alto, x + 34, y + 4, 3), col, 4)
        x += 58


def _palmera(c, x, base, s, t):
    tr = suave([(x, base), (x + 10 * s, base - 160 * s), (x + 24 * s, base - 300 * s)], close=False)
    c.drawPath(tr, trazo(30 * s, (150, 110, 70)))
    c.drawPath(tr, trazo(30 * s, "tinta", 0)); c.drawPath(tr, trazo(4, "tinta", 120))
    tx, ty = x + 24 * s, base - 300 * s
    for i, a in enumerate((-160, -120, -60, -20, 200, 250)):
        a = math.radians(a + 6 * math.sin(t * 1.5 + i))
        ex, ey = tx + math.cos(a) * 150 * s, ty + math.sin(a) * 80 * s + 50 * s
        hoja = suave([(tx, ty), ((tx + ex) / 2, ty - 50 * s), (ex, ey), ((tx + ex) / 2, ty - 10 * s)])
        pieza(c, hoja, "hierba", 4)
    c.drawCircle(tx, ty, 16 * s, relleno((150, 100, 60)))


def ceuta(c, t=0.0, capa=lambda d: None, suelo=SUELO, **kw):
    horiz = 760
    capa(0.12)
    _rect(c, X0 - 600, Y0 - 600, X1 + 600, horiz + 10, "cielo_alto", degradado(Y0, horiz, "cielo_alto", (206, 236, 250)))
    for i, (y, s, v) in enumerate(((170, 1.0, 12), (330, 0.65, 8))):
        _nube(c, (i * 640 + t * v) % 1900 - 400, y, s, 210)
    _pajaros(c, t)
    capa(0.25)
    # al otro lado del Estrecho: la península (azul de lejanía) y el Peñón de Gibraltar
    lejos = (150, 180, 214)
    c.drawPath(suave([(X0 - 600, horiz + 4), (X0 - 300, horiz - 70), (160, horiz - 40), (520, horiz - 90),
                      (760, horiz - 30), (X1 + 600, horiz - 60), (X1 + 600, horiz + 4)]), relleno(lejos))
    pen = poly([(820, horiz), (860, horiz - 150), (900, horiz - 175), (990, horiz - 40), (1010, horiz)])
    c.drawPath(pen, relleno(mezcla(lejos, "tinta", 0.12)))
    # el mar del Estrecho con brillos y un ferri que cruza
    _rect(c, X0 - 600, horiz, X1 + 600, suelo - 260, (88, 168, 222), degradado(horiz, suelo - 260, (120, 190, 235), (60, 140, 200)))
    for i in range(26):
        x = (i * 97 + t * 25) % (X1 - X0 + 800) + X0 - 400
        y = horiz + 20 + (i * 37) % 200
        c.drawLine(x, y, x + 30, y, trazo(4, "blanco", 160))
    fx = (t * 38) % 2200 - 500
    c.save(); c.translate(fx, horiz + 70); c.scale(0.5, 0.5)
    pieza(c, poly([(-120, 0), (130, 0), (110, 40), (-100, 40)]), "blanco", 6)
    pieza(c, rrect(-70, -50, 70, 2, 8), "blanco", 6)
    c.drawRect(skia.Rect(-60, -38, 60, -22), relleno((90, 150, 200)))
    pieza(c, rrect(30, -90, 60, -50, 4), "rojo", 5)
    c.restore()
    capa(0.45)
    # Monte Hacho con la fortaleza arriba
    monte = suave([(X0 - 500, suelo - 260), (X0 - 200, 520), (60, 430), (300, 520), (560, suelo - 300), (560, suelo - 260)])
    pieza(c, monte, (120, 176, 96), 6, shader=degradado(430, suelo - 260, (140, 196, 110), (96, 150, 80)))
    pieza(c, rrect(-40, 380, 200, 450, 6), "piedra", 5)
    _almenas(c, -40, 200, 380, 24, "piedra")
    pieza(c, rrect(60, 330, 110, 380, 4), "piedra", 5)
    # casas del centro (blancas y de colores, escalonadas)
    tonos = [(255, 255, 255), (250, 236, 210), (246, 214, 180), (236, 240, 248), (250, 226, 196)]
    for fila, (base, h0) in enumerate(((suelo - 330, 120), (suelo - 290, 140))):
        x = 330 + fila * 40
        i = 0
        while x < X1 + 300:
            w = 90 + (i * 23) % 50
            h = h0 + (i * 41) % 70
            _casa(c, x, base, w, h, tonos[(i + fila) % len(tonos)], "teja" if (i + fila) % 3 else "azotea")
            x += w + 8
            i += 1
    # campanario y cúpula (la ciudad, desde lejos)
    pieza(c, rrect(980, suelo - 560, 1040, suelo - 330, 4), "fachada", 5)
    pieza(c, poly([(972, suelo - 560), (1010, suelo - 640), (1048, suelo - 560)]), "teja", 5)
    pieza(c, suave([(700, suelo - 420), (760, suelo - 500), (820, suelo - 420)]), (240, 240, 245), 5)
    capa(0.7)
    # Murallas Reales con su foso
    muro = (226, 210, 180)
    pieza(c, rrect(X0 - 300, suelo - 300, X1 + 300, suelo - 120, 0), muro, 6,
          shader=degradado(suelo - 300, suelo - 120, (236, 222, 194), (204, 186, 152)))
    for x in range(X0 - 300, X1 + 300, 70):
        for y in range(suelo - 280, suelo - 130, 44):
            off = 35 if ((y - suelo) // 44) % 2 else 0
            c.drawLine(x + off, y, x + off + 60, y, trazo(2.5, (180, 160, 124)))
    _almenas(c, X0 - 300, X1 + 300, suelo - 300, 34, muro)
    # puerta en arco
    arco = skia.Path()
    arco.moveTo(420, suelo - 120); arco.lineTo(420, suelo - 210); arco.quadTo(480, suelo - 280, 540, suelo - 210)
    arco.lineTo(540, suelo - 120); arco.close()
    pieza(c, arco, (90, 70, 60), 6)
    # banderas sobre la muralla: España y Ceuta
    for bx, dis in ((250, "espana"), (680, "ceuta")):
        c.drawLine(bx, suelo - 330, bx, suelo - 520, trazo(8))
        c.save(); c.translate(bx + 4, suelo - 516)
        tela(c, dis, 130, 86, t + bx * 0.01)
        c.restore()
    # el foso: agua con reflejos
    _rect(c, X0 - 300, suelo - 120, X1 + 300, suelo - 30, (70, 150, 205))
    for i in range(14):
        x = (i * 130 + t * 30) % (X1 - X0 + 600) + X0 - 300
        c.drawLine(x, suelo - 80, x + 50, suelo - 80, trazo(5, "blanco", 170))
    c.drawLine(X0 - 300, suelo - 120, X1 + 300, suelo - 120, trazo(6))
    capa(1.0)
    # paseo de piedra con barandilla, palmeras y farolas
    _rect(c, X0 - 300, suelo - 30, X1 + 300, Y1 + 300, (232, 218, 196), degradado(suelo - 30, Y1, (238, 226, 206), (206, 190, 164)))
    c.drawLine(X0 - 300, suelo - 30, X1 + 300, suelo - 30, trazo(6))
    for x in range(X0 - 300, X1 + 300, 90):
        c.drawLine(x, suelo - 30, x, suelo - 70, trazo(6, (120, 110, 100)))
    c.drawLine(X0 - 300, suelo - 70, X1 + 300, suelo - 70, trazo(8, (120, 110, 100)))
    for x in range(X0 - 300, X1 + 300, 180):
        c.drawLine(x, suelo + 40, x + 120, suelo + 40, trazo(3, (190, 170, 140)))
    for px, s in ((-120, 1.0), (1180, 0.95)):
        _palmera(c, px, suelo - 20, s, t)


def mar_mapa(c, t=0.0, capa=lambda d: None, **kw):
    capa(1.0)
    c.drawRect(skia.Rect(-20000, -20000, 20000, 20000), relleno((126, 196, 236)))


def carretera(c, t=0.0, capa=lambda d: None, suelo=SUELO, velocidad=1.0, **kw):
    """Carretera que se pierde en el horizonte entre colinas; las rayas avanzan (velocidad 0 = parada)."""
    horiz = 820
    capa(0.12)
    _rect(c, X0 - 600, Y0 - 600, X1 + 600, horiz + 10, "cielo_alto", degradado(Y0, horiz, "cielo_alto", (206, 236, 250)))
    for i, (y, s, v) in enumerate(((180, 1.0, 14), (360, 0.7, 9))):
        _nube(c, (i * 700 + t * v) % 2000 - 450, y, s, 215)
    _pajaros(c, t)
    capa(0.3)
    for x0, h, col in ((X0 - 500, 260, (150, 196, 120)), (420, 200, (130, 186, 110)), (900, 300, (146, 200, 118))):
        c.drawPath(suave([(x0 - 300, horiz + 4), (x0 + 200, horiz - h), (x0 + 700, horiz + 4)]), relleno(col))
    capa(0.6)
    _rect(c, X0 - 600, horiz, X1 + 600, Y1 + 600, (120, 186, 90), degradado(horiz, Y1, (140, 200, 100), (100, 168, 76)))
    # asfalto en perspectiva
    cx = 540
    asf = poly([(cx - 30, horiz), (cx + 30, horiz), (cx + 900, Y1 + 400), (cx - 900, Y1 + 400)])
    pieza(c, asf, (96, 100, 110), 6, shader=degradado(horiz, Y1, (120, 124, 134), (80, 84, 94)))
    for s_ in (-1, 1):  # líneas de borde
        c.drawLine(cx + s_ * 26, horiz + 4, cx + s_ * 820, Y1 + 400, trazo(10, "blanco"))
    # rayas centrales que vienen hacia nosotros
    for i in range(10):
        k = ((i / 10) + t * 0.35 * velocidad) % 1.0
        k2 = min(1.0, k + 0.045)
        y0 = horiz + (Y1 + 400 - horiz) * k ** 2.2
        y1 = horiz + (Y1 + 400 - horiz) * k2 ** 2.2
        w0, w1 = 2 + 26 * k ** 2.2, 2 + 26 * k2 ** 2.2
        c.drawPath(poly([(cx - w0 / 2, y0), (cx + w0 / 2, y0), (cx + w1 / 2, y1), (cx - w1 / 2, y1)]), relleno("blanco"))
    # árboles y postes a los lados que pasan
    for i in range(6):
        k = ((i / 6) + t * 0.2 * velocidad) % 1.0
        y = horiz + (Y1 - horiz) * k ** 2
        sc = 0.1 + 1.1 * k ** 2
        for s_ in (-1, 1):
            x = cx + s_ * (60 + 900 * k ** 2)
            c.save(); c.translate(x, y); c.scale(sc, sc)
            c.drawLine(0, 0, 0, -260, trazo(26, (150, 110, 70)))
            pieza(c, elipse(0, -330, 120, 110), (96, 170, 80), 6)
            c.restore()
    capa(1.0)


def colegio(c, t=0.0, capa=lambda d: None, suelo=SUELO, **kw):
    """Colegio electoral: gimnasio/aula con pizarra, cartel «COLEGIO ELECTORAL», banderines y ventanas con sol."""
    capa(0.4)
    _rect(c, X0 - 600, Y0 - 600, X1 + 600, suelo, (246, 236, 214), degradado(Y0, suelo, (250, 242, 224), (236, 222, 196)))
    for x in (60, 760):  # ventanales
        pieza(c, rrect(x, 260, x + 260, 640, 10), (190, 226, 248), 7)
        c.drawLine(x + 130, 260, x + 130, 640, trazo(6)); c.drawLine(x, 450, x + 260, 450, trazo(6))
        c.drawPath(poly([(x + 20, 280), (x + 90, 280), (x + 30, 420)]), relleno("blanco", 120))
    pieza(c, rrect(330, 300, 750, 560, 10), (60, 96, 80), 8)  # pizarra del aula
    pieza(c, rrect(300, 160, 780, 250, 14), "blanco", 6)
    f = _f(52)
    txt = "COLEGIO ELECTORAL"
    c.drawString(txt, 540 - f.measureText(txt) / 2, 224, f, relleno((60, 90, 170)))
    for i in range(14):  # banderines
        x = X0 + i * 120
        y = 30 + 20 * math.sin(i * 0.9)
        c.drawPath(poly([(x, y), (x + 100, y + 6), (x + 50, y + 80)]), relleno(("rojo", "amarillo", "azul", "verde")[i % 4]))
    c.drawLine(X0, 30, X1, 30, trazo(4))
    capa(1.0)
    _rect(c, X0 - 600, suelo - 10, X1 + 600, Y1 + 600, (214, 180, 130), degradado(suelo, Y1, (222, 190, 140), (196, 160, 112)))
    for x in range(X0 - 600, X1 + 600, 120):
        c.drawLine(x, suelo, x - 200, Y1 + 600, trazo(3, (180, 146, 100)))
    c.drawLine(X0 - 600, suelo - 10, X1 + 600, suelo - 10, trazo(6))


def estudio(c, t=0.0, capa=lambda d: None, suelo=SUELO, **kw):
    """Estudio de podcast: pared oscura con paneles acústicos, letrero de neón «ON AIR» y estanterías."""
    capa(0.4)
    _rect(c, X0 - 600, Y0 - 600, X1 + 600, suelo, (40, 38, 52), degradado(Y0, suelo, (52, 48, 68), (30, 28, 40)))
    for i in range(-3, 12):  # paneles acústicos (rombos)
        for j in range(4):
            x, y = 40 + i * 120 + (j % 2) * 60, 120 + j * 120
            c.drawPath(poly([(x, y - 50), (x + 50, y), (x, y + 50), (x - 50, y)]), relleno((70, 64, 92)))
            c.drawPath(poly([(x, y - 50), (x + 50, y), (x, y + 50), (x - 50, y)]), trazo(4, (24, 22, 32)))
    brillo = 0.75 + 0.25 * math.sin(t * 5)
    pieza(c, rrect(380, 40, 700, 140, 20), (60, 20, 30), 7)
    f = _f(66)
    txt = "ON AIR"
    c.drawString(txt, 540 - f.measureText(txt) / 2, 114, f, relleno((255, 70, 80), int(255 * brillo)))
    for x in (-40, 860):  # estanterías con libros
        pieza(c, rrect(x, 560, x + 260, 600, 6), "madera", 6)
        for k in range(6):
            pieza(c, rrect(x + 16 + k * 40, 470 + (k % 2) * 16, x + 48 + k * 40, 560, 4), ("rojo", "amarillo", "azul", "verde")[k % 4], 4)
    capa(1.0)
    _rect(c, X0 - 600, suelo - 10, X1 + 600, Y1 + 600, (96, 70, 60), degradado(suelo, Y1, (110, 80, 68), (80, 58, 50)))
    c.drawLine(X0 - 600, suelo - 10, X1 + 600, suelo - 10, trazo(6))


def plato(c, t=0.0, capa=lambda d: None, suelo=SUELO, rotulo="DEBATE 29N", **kw):
    """Plató de televisión: fondo azul con pantallas, focos y rótulo; suelo brillante."""
    capa(0.4)
    _rect(c, X0 - 600, Y0 - 600, X1 + 600, suelo, (24, 50, 110), degradado(Y0, suelo, (36, 70, 150), (16, 32, 80)))
    for i in range(-2, 11):  # rayos de luz de los focos
        x = i * 120
        c.drawPath(poly([(x, 0), (x + 40, 0), (x + 160 + 40 * math.sin(t + i), suelo), (x - 80, suelo)]), relleno("blanco", 18))
    for i in range(-3, 12):  # focos colgados
        x = i * 120 + 60
        pieza(c, rrect(x - 26, 10, x + 26, 60, 10), (60, 60, 70), 5)
        c.drawCircle(x, 64, 14, relleno((255, 240, 180)))
    pieza(c, rrect(280, 180, 800, 300, 18), (12, 20, 50), 7)
    f = _f(64)
    c.drawString(rotulo, 540 - f.measureText(rotulo) / 2, 262, f, relleno("amarillo"))
    capa(1.0)
    _rect(c, X0 - 600, suelo - 10, X1 + 600, Y1 + 600, (20, 30, 60), degradado(suelo, Y1, (40, 60, 120), (14, 22, 50)))
    for x in range(X0 - 600, X1 + 600, 160):
        c.drawLine(x, suelo, x - 260, Y1 + 600, trazo(3, (70, 100, 170)))
    c.drawLine(X0 - 600, suelo - 10, X1 + 600, suelo - 10, trazo(6))


def _f(size, cual="sub"):
    import wb
    return wb.font(cual, size)


TIPOS = {"ceuta": ceuta, "mar_mapa": mar_mapa, "carretera": carretera, "colegio": colegio, "estudio": estudio, "plato": plato}
