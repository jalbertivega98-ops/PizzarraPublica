"""Fondos de escena (calle, interior del banco, oficina de Hacienda, salón, plano, rayos).

Se dibujan en coordenadas de la pizarra (1080×1920) con margen de sobra para la cámara.
La línea del suelo por defecto está en y = 1300 (donde se apoyan personajes y edificios).
"""
import math

import skia

from .estilo import COL, degradado, elipse, mezcla, pieza, poly, relleno, rrect, trazo

X0, X1, Y0, Y1 = -260, 1340, -260, 2180
SUELO = 1340


def _rect(c, x0, y0, x1, y1, color, shader=None):
    c.drawRect(skia.Rect(x0, y0, x1, y1), relleno(color, 255, shader))


def _nube(c, x, y, s, a=235):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    for dx, dy, r in ((-100, 10, 55), (-40, -30, 75), (40, -40, 70), (105, 5, 55), (0, 20, 60)):
        p.addOval(skia.Rect(dx - r, dy - r, dx + r, dy + r))
    c.drawPath(p, relleno("blanco", a))
    c.restore()


def calle(c, t=0.0, capa=lambda d: None, suelo=SUELO, hora="dia", **kw):
    alto, bajo = ("cielo_alto", "cielo") if hora == "dia" else ((250, 150, 110), (255, 205, 150))
    capa(0.15)
    _rect(c, X0, Y0, X1, suelo, alto, degradado(Y0, suelo, alto, bajo))
    # nubes que se desplazan
    for i, (y, s, v) in enumerate(((180, 1.0, 14), (360, 0.7, 9), (90, 0.55, 6))):
        x = (i * 520 + t * v) % 1700 - 300
        _nube(c, x, y, s, 200)
    _pajaros(c, t)
    capa(0.45)
    # ciudad lejana (silueta suave)
    lejos = mezcla(bajo, "azul", 0.18)
    x = X0
    i = 0
    while x < X1:
        w = 120 + (i * 37) % 90
        h = 220 + (i * 53) % 260
        _rect(c, x, suelo - 60 - h, x + w, suelo, lejos)
        for wy in range(int(suelo - 40 - h), int(suelo - 80), 56):
            for wx in range(int(x + 18), int(x + w - 30), 40):
                _rect(c, wx, wy, wx + 18, wy + 26, mezcla(lejos, "blanco", 0.35))
        x += w + 14
        i += 1
    _bus_lejano(c, t, suelo, mezcla(bajo, "rojo", 0.45))
    capa(0.7)
    # árboles lejanos
    for i in range(9):
        cx = X0 + 90 + i * 190
        c.drawCircle(cx, suelo - 70, 62, relleno(mezcla("hierba", bajo, 0.35)))
    capa(1.0)
    # acera y calzada
    _rect(c, X0, suelo - 20, X1, suelo + 70, "acera", degradado(suelo - 20, suelo + 70, (226, 226, 230), "acera"))
    c.drawLine(X0, suelo - 20, X1, suelo - 20, trazo(6))
    for x in range(X0, X1, 160):
        c.drawLine(x, suelo - 20, x - 30, suelo + 70, trazo(3, "gris"))
    _rect(c, X0, suelo + 70, X1, Y1, (92, 96, 108), degradado(suelo + 70, Y1, (100, 104, 116), (70, 74, 84)))
    c.drawLine(X0, suelo + 70, X1, suelo + 70, trazo(6))
    for x in range(X0, X1, 220):
        _rect(c, x, suelo + 200, x + 120, suelo + 216, "blanco")
    _coches(c, t, suelo)


def _pajaros(c, t):
    """Bandada pequeña que cruza el cielo aleteando."""
    for i in range(4):
        x = (t * 70 + i * 60) % 2000 - 400
        y = 300 + 30 * i + 12 * math.sin(t * 2 + i)
        ala = 14 * math.sin(t * 12 + i)
        p = skia.Path()
        p.moveTo(x - 22, y - ala); p.quadTo(x - 10, y - 8, x, y); p.quadTo(x + 10, y - 8, x + 22, y - ala)
        c.drawPath(p, trazo(4.5, (60, 70, 90)))


def _bus_lejano(c, t, suelo, col):
    x = 1700 - (t * 120) % 2400
    y = suelo - 60
    _rect(c, x, y - 70, x + 220, y, col)
    for k in range(4):
        _rect(c, x + 14 + k * 52, y - 58, x + 50 + k * 52, y - 30, mezcla(col, "blanco", 0.5))
    c.drawCircle(x + 40, y, 13, relleno((70, 70, 80))); c.drawCircle(x + 180, y, 13, relleno((70, 70, 80)))


def _coches(c, t, suelo):
    """Coches que pasan por la calzada (bajo los subtítulos)."""
    from . import objetos
    for i, (v, col, fase) in enumerate(((380, "azul", 0.0), (-300, "amarillo", 0.5))):
        x = (fase * 2600 + t * v) % 2600 - 700
        c.save(); c.translate(x, suelo + 190 + 70 * i); c.scale(0.45 * (1 if v > 0 else -1), 0.45)
        objetos.dibuja(c, "coche", t, color=col, cara="normal")
        c.restore()


def banco_dentro(c, t=0.0, capa=lambda d: None, suelo=SUELO, cartel=False, **kw):
    """Interior del banco: pared cálida, ventanales, carteles de hipotecas y suelo de baldosas."""
    capa(0.85)
    _rect(c, X0, Y0, X1, suelo, (246, 226, 196), degradado(Y0, suelo, (250, 236, 210), (236, 210, 172)))
    # ventanales con la ciudad
    for x in (40, 700):
        pieza(c, rrect(x, 330, x + 340, 900, 16), "cristal", 7, shader=degradado(330, 900, "cielo", "blanco"))
        for k in range(4):
            _rect(c, x + 20 + k * 80, 700 - (k * 47) % 160, x + 80 + k * 80, 890, (180, 196, 214))
        c.drawLine(x + 170, 330, x + 170, 900, trazo(7))
        c.drawLine(x, 615, x + 340, 615, trazo(7))
    # cartel de hipotecas (opcional: compite con los rótulos)
    if cartel:
        _cartel_hipoteca(c)
    _lamparas(c, t)
    capa(1.0)
    # zócalo de madera
    _zocalo(c, suelo)
    _suelo_baldosas(c, suelo, (236, 230, 220), (206, 196, 182))


def _cartel_hipoteca(c):
    pieza(c, rrect(440, 700, 640, 900, 12), "blanco", 6)
    f_tit = _f(34, "sub")
    for i, l in enumerate(("HIPOTECA", "FIJA", "3,01 %*")):
        c.drawString(l, 540 - f_tit.measureText(l) / 2, 758 + i * 46, f_tit, relleno("rojo" if i == 2 else "tinta"))
    c.drawString("*condiciones", 540 - _f(22).measureText("*condiciones") / 2, 884, _f(22), relleno("gris"))


def _lamparas(c, t, xs=(270, 810)):
    for i, x in enumerate(xs):
        a = 4 * math.sin(t * 1.4 + i)
        c.save(); c.translate(x, -260); c.rotate(a)
        c.drawLine(0, 0, 0, 470, trazo(4))
        pieza(c, poly([(-60, 520), (60, 520), (30, 470), (-30, 470)]), "verde_osc", 5)
        c.drawCircle(0, 526, 14, relleno("amarillo"))
        c.restore()


def _zocalo(c, suelo):
    _rect(c, X0, suelo - 260, X1, suelo, "madera", degradado(suelo - 260, suelo, (196, 140, 92), (150, 96, 56)))
    c.drawLine(X0, suelo - 260, X1, suelo - 260, trazo(6))
    for x in range(X0, X1, 180):
        c.drawPath(rrect(x + 20, suelo - 230, x + 160, suelo - 30, 8), trazo(4, (120, 76, 44)))


def oficina(c, t=0.0, capa=lambda d: None, suelo=SUELO, **kw):
    """Oficina de Hacienda: pared verde grisácea, archivadores, reloj y persianas."""
    capa(0.85)
    _rect(c, X0, Y0, X1, suelo, (206, 222, 208), degradado(Y0, suelo, (220, 232, 220), (186, 204, 190)))
    pieza(c, rrect(620, 300, 1000, 760, 12), "cristal", 7)
    for y in range(316, 760, 34):
        c.drawLine(626, y, 994, y, trazo(5, (150, 160, 170)))
    # reloj de pared
    pieza(c, elipse(260, 420, 90, 90), "blanco", 7)
    a = t * 2
    c.drawLine(260, 420, 260 + 60 * math.cos(a), 420 + 60 * math.sin(a), trazo(7))
    c.drawLine(260, 420, 260, 370, trazo(9))
    capa(1.0)
    # archivadores
    for i, x in enumerate((60, 260, 820)):
        pieza(c, rrect(x, suelo - 480, x + 180, suelo, 8), (150, 160, 170), 6)
        for k in range(3):
            pieza(c, rrect(x + 16, suelo - 460 + k * 150, x + 164, suelo - 330 + k * 150, 6), (176, 186, 196), 4)
            pieza(c, rrect(x + 70, suelo - 410 + k * 150, x + 110, suelo - 390 + k * 150, 4), "gris_claro", 3)
    _suelo_baldosas(c, suelo, (196, 196, 190), (170, 170, 164))


def salon(c, t=0.0, capa=lambda d: None, suelo=SUELO, **kw):
    """Salón de un piso pequeño (alquiler)."""
    capa(0.85)
    _rect(c, X0, Y0, X1, suelo, (240, 220, 200), degradado(Y0, suelo, (246, 230, 214), (226, 200, 176)))
    for x in range(X0, X1, 90):  # papel pintado
        c.drawLine(x, Y0, x, suelo, trazo(10, (236, 210, 188)))
    pieza(c, rrect(390, 660, 690, 1010, 14), "cristal", 7, shader=degradado(660, 1010, "cielo", "blanco"))
    c.drawLine(540, 660, 540, 1010, trazo(7))
    pieza(c, rrect(370, 630, 710, 664, 10), "rojo", 6)
    c.save()
    c.clipRect(skia.Rect(394, 664, 686, 1006))
    for i in range(2):  # nubes por la ventana
        _nube(c, 300 + ((t * 25 + i * 220) % 480), 760 + i * 110, 0.35, 220)
    c.restore()
    c.drawLine(540, 660, 540, 1010, trazo(7))
    for sx in (-1, 1):  # cortinas que se mecen
        cx = 540 + sx * 175
        sw = 10 * math.sin(t * 1.6 + sx)
        pieza(c, poly([(cx - 40, 650), (cx + 40, 650), (cx + 34 + sw, 1030), (cx - 46 + sw, 1030)]), (226, 80, 70), 5)
    capa(1.0)
    _rect(c, X0, suelo - 20, X1, Y1, (180, 128, 84), degradado(suelo, Y1, (190, 136, 90), (150, 100, 60)))
    c.drawLine(X0, suelo - 20, X1, suelo - 20, trazo(6))
    for y in range(int(suelo + 40), Y1, 90):
        c.drawLine(X0, y, X1, y, trazo(3, (140, 92, 54)))


def plano(c, t=0.0, capa=lambda d: None, color="amarillo", **kw):
    """Color plano con puntitos de trama (golpes de dato)."""
    capa(0.3)
    base = COL[color] if isinstance(color, str) else color
    _rect(c, X0, Y0, X1, Y1, base)
    p = relleno(mezcla(base, "blanco", 0.25))
    for y in range(Y0, Y1, 46):
        for x in range(X0 + (23 if (y // 46) % 2 else 0), X1, 46):
            c.drawCircle(x, y, 6, p)


def rayos(c, t=0.0, capa=lambda d: None, color="amarillo", color2=None, centro=(540, 760), **kw):
    """Fondo de rayos (sorpresa/impacto), gira despacio."""
    capa(0.3)
    base = COL[color] if isinstance(color, str) else color
    c2 = color2 or mezcla(base, "blanco", 0.35)
    _rect(c, X0, Y0, X1, Y1, base)
    cx, cy = centro
    n = 18
    for i in range(n):
        a0 = (i / n) * 2 * math.pi + t * 0.15
        a1 = a0 + math.pi / n
        r = 3000
        c.drawPath(poly([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))]),
                   relleno(c2))


def _suelo_baldosas(c, suelo, a, b):
    _rect(c, X0, suelo - 10, X1, Y1, a)
    c.drawLine(X0, suelo - 10, X1, suelo - 10, trazo(6))
    sz = 110
    for j, y in enumerate(range(int(suelo - 10), Y1, sz)):
        for i, x in enumerate(range(X0, X1, sz)):
            if (i + j) % 2:
                _rect(c, x, y, x + sz, y + sz, b)


def _f(size, cual="hand"):
    import wb
    return wb.font(cual, size)


TIPOS = {"calle": calle, "banco_dentro": banco_dentro, "oficina": oficina, "salon": salon, "plano": plano, "rayos": rayos}


def dibuja(c, fondo, t=0.0, cam=None):
    """cam = (cx, cy, z, inclina) de la cámara: cada capa se mueve según su profundidad (parallax)."""
    if isinstance(fondo, str):
        fondo = {"tipo": fondo}
    kw = dict(fondo)
    tipo = kw.pop("tipo")
    if cam is None:
        TIPOS[tipo](c, t=t, **kw)
        return
    cx, cy, z, inc = cam
    estado = {"abierta": False}

    def capa(d):
        if estado["abierta"]:
            c.restore()
        c.save()
        estado["abierta"] = True
        zd = 1 + (z - 1) * d
        c.translate(540, 820)
        if inc:
            c.rotate(inc * d)
        c.scale(zd, zd)
        c.translate(-(540 + (cx - 540) * d), -(820 + (cy - 820) * d))

    TIPOS[tipo](c, t=t, capa=capa, **kw)
    if estado["abierta"]:
        c.restore()
