"""Objetos cívicos del mundo dibujado (octubre de 2026): elecciones, leyes, carreteras, viajes e historia.
Mismo estilo que los personajes pizarra (contorno negro, colores vivos, formas simpáticas). Se registran en
objetos.TIPOS como los de mundo.py:

  urna        urna transparente con ranura; props: llena (0-1), texto ("CONGRESO"), cara
  papeleta    sobre de votar; props: color ("blanco" Congreso, "sepia" Senado), texto
  camion      camión de reparto que rueda; props: texto del toldo, color; _mov lo pone el motor
  senal       señal de tráfico redonda de límite; props: numero, tachada (0-1: la cruza un aspa roja)
  alcoholimetro  aparato de soplar con pantalla; props: texto
  contador    marcador de dígitos que corre hasta un valor; props: valor, prefijo, sufijo, decimales, progreso,
              color (fondo), ancho
  barras      gráfica de barras con etiqueta y valor; props: barras [{texto, valor, color}], tope, progreso, sufijo,
              resalta [índices]
  lapida      lápida «R.I.P.» con texto (las leyes que mueren); props: texto, lineas
  papelera    papelera de rejilla (los papeles caen dentro)
  pasaporte   pasaporte español granate; props: abierto (bool)
  maleta      maleta con pegatinas
  mesa_electoral  mesa con mantel y cartel «MESA»; (0, 0) = suelo
  carabela    nave de vela del siglo XV (velas con cruz); props: cruz ("portugal" | "castilla"), _mov
  corona      corona dorada (la Corona, sin caras de personas reales)
  pergamino   hoja de tratado antigua con sello de lacre; props: titulo, fecha, lineas
  bola        bola de cristal de adivino (encuestas: «predecir»); props: texto
  libro       libro grueso cerrado con título en el lomo; props: titulo, color
"""
import math

import skia

from .estilo import COL, degradado, elipse, mezcla, pieza, poly, relleno, rrect, sombra_suelo, suave, texto_cartoon, trazo
from .mundo import _estrella5, tela


def _font(size, cual="hand"):
    import wb
    return wb.font(cual, size)


def _texto(c, txt, x, y, size, color="tinta", cual="hand", ancho=None):
    f = _font(size, cual)
    if ancho and f.measureText(txt) > ancho:
        size = size * ancho / f.measureText(txt)
        f = _font(size, cual)
    c.drawString(txt, x - f.measureText(txt) / 2, y, f, relleno(color))


def _eo(k):
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 3


def _cara(c, x, y, s, ex, t):
    if ex:
        from .objetos import _cara as cara
        cara(c, x, y, s, ex, t)


# ------------------------------------------------------------------ elecciones
def papeleta(c, t=0.0, color="blanco", texto="", **kw):
    col = {"blanco": (252, 252, 250), "sepia": (236, 214, 176)}.get(color, color)
    pieza(c, rrect(-120, -80, 120, 80, 10), col, 6)
    c.drawPath(poly([(-118, -78), (0, 10), (118, -78)], close=False), trazo(5, mezcla(col, "tinta", 0.35)))
    if texto:
        _texto(c, texto, 0, 60, 30, "tinta", "sub", 200)


def urna(c, t=0.0, llena=0.4, texto="", cara=None, **kw):
    """Urna de metacrilato; (0, 0) = centro."""
    sombra_suelo(c, 0, 200, 210)
    caja = rrect(-200, -150, 200, 190, 22)
    c.drawPath(caja, relleno((225, 240, 252), 150))
    # sobres dentro, apilados hasta "llena"
    c.save(); c.clipPath(caja, skia.ClipOp.kIntersect, True)
    n = int(26 * max(0.0, min(1.0, llena)))
    for i in range(n):
        fila, col = divmod(i, 5)
        x = -160 + col * 78 + (fila % 2) * 20
        y = 160 - fila * 52
        c.save(); c.translate(x, y); c.rotate(((i * 37) % 21) - 10); c.scale(0.32, 0.32)
        papeleta(c, t, "blanco" if i % 3 else "sepia")
        c.restore()
    c.restore()
    c.drawPath(caja, trazo(7))
    c.drawPath(elipse(-120, -60, 30, 90), relleno("blanco", 90))  # brillo del cristal
    pieza(c, rrect(-215, -190, 215, -140, 14), (60, 90, 170), 6)  # tapa azul
    pieza(c, rrect(-90, -176, 90, -158, 8), "tinta", 0)
    if texto:
        pieza(c, rrect(-150, 60, 150, 120, 10), "blanco", 5)
        _texto(c, texto, 0, 106, 46, (60, 90, 170), "sub", 270)
    _cara(c, 0, -40, 0.6, cara, t)


def mesa_electoral(c, t=0.0, texto="MESA 1", **kw):
    """Mesa con mantel; (0, 0) = suelo."""
    pieza(c, rrect(-330, -260, 330, -220, 10), "madera", 6)
    pieza(c, poly([(-340, -230), (340, -230), (360, 0), (-360, 0)]), (240, 244, 250), 6,
          shader=degradado(-230, 0, (255, 255, 255), (214, 222, 236)))
    pieza(c, rrect(-130, -170, 130, -80, 10), "blanco", 5)
    _texto(c, texto, 0, -108, 54, (60, 90, 170), "sub", 230)


def camion(c, t=0.0, texto="ELECCIONES", color="azul", _mov=False, cara=None, **kw):
    """Camión de reparto mirando a la derecha; (0, 0) = centro, ruedas en y = 110."""
    bote = 3 * math.sin(t * 18) if _mov else 0
    sombra_suelo(c, 0, 150, 330)
    c.save(); c.translate(0, bote)
    pieza(c, rrect(-330, -230, 130, 90, 18), "blanco", 7, shader=degradado(-230, 90, "blanco", (226, 230, 238)))
    _texto(c, texto, -100, -50, 64, color, "sub", 420)
    for i in range(3):  # sobres pintados en el toldo
        c.save(); c.translate(-240 + i * 140, 30); c.scale(0.34, 0.34); papeleta(c, t); c.restore()
    pieza(c, suave([(140, 90), (140, -130), (240, -130), (320, -30), (330, 90)]), color, 7,
          shader=degradado(-130, 90, mezcla(color, "blanco", 0.3), color))
    pieza(c, poly([(166, -108), (236, -108), (290, -36), (166, -36)]), "cristal", 5)
    pieza(c, elipse(318, 40, 14, 18), "amarillo", 4)
    _cara(c, 230, 20, 0.36, cara, t)
    c.restore()
    for x in (-230, -110, 230):
        _rueda(c, x, 110, 44, t * (6 if _mov else 0))
    if _mov:  # humo del tubo de escape
        for i in range(3):
            k = (t * 1.5 + i / 3) % 1
            c.drawCircle(-360 - 70 * k, 70 - 40 * k, 14 + 24 * k, relleno((200, 204, 212), int(200 * (1 - k))))


def _rueda(c, x, y, r, giro):
    pieza(c, elipse(x, y, r, r), (50, 52, 60), 6)
    c.drawCircle(x, y, r * 0.45, relleno((200, 204, 212)))
    for a in (0, 120, 240):
        aa = math.radians(a) + giro
        c.drawLine(x, y, x + math.cos(aa) * r * 0.42, y + math.sin(aa) * r * 0.42, trazo(5, (90, 94, 104)))


# ------------------------------------------------------------------ carretera
def senal(c, t=0.0, numero="50", tachada=0.0, poste=True, **kw):
    """Señal de límite de velocidad; (0, 0) = centro del disco."""
    if poste:
        pieza(c, rrect(-12, 120, 12, 520, 6), (180, 184, 192), 5)
    pieza(c, elipse(0, 0, 130, 130), "blanco", 7)
    c.drawCircle(0, 0, 104, trazo(34, (214, 30, 36)))
    _texto(c, str(numero), 0, 44, 120 if len(str(numero)) < 3 else 92, "tinta", "sub")
    k = _eo(tachada)
    if k > 0:  # aspa roja de rotulador
        for (x0, y0, x1, y1) in ((-150, -150, 150, 150), (150, -150, -150, 150)):
            c.drawLine(x0, y0, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, trazo(30, "blanco"))
            c.drawLine(x0, y0, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, trazo(20, "rojo"))


def alcoholimetro(c, t=0.0, texto="0,5", **kw):
    pieza(c, rrect(-90, -170, 90, 170, 40), (250, 200, 60), 7, shader=degradado(-170, 170, (255, 226, 120), (240, 180, 40)))
    pieza(c, rrect(-60, -120, 60, -10, 14), (40, 60, 50), 5)
    _texto(c, texto, 0, -45, 64, (120, 255, 150), "sub", 110)
    for i, y in enumerate((40, 90)):
        pieza(c, elipse(-30 + i * 60, y, 20, 20), "rojo" if i else "verde", 4)
    pieza(c, rrect(-18, -250, 18, -166, 8), "blanco", 5)  # boquilla


# ------------------------------------------------------------------ datos
def contador(c, t=0.0, valor=100, prefijo="", sufijo="", decimales=0, progreso=1.0, color=(40, 44, 56), ancho=760,
             miles=".", desde=0, **kw):
    """Marcador que corre desde «desde» hasta el valor (progreso 0-1, con frenada)."""
    v = desde + (valor - desde) * _eo(progreso) if progreso < 1 else valor
    s = f"{v:,.{decimales}f}".replace(",", "#").replace(".", ",").replace("#", miles)
    txt = f"{prefijo}{s}{sufijo}"
    pieza(c, rrect(-ancho / 2, -110, ancho / 2, 110, 30), color, 8)
    c.drawRect(skia.Rect(-ancho / 2 + 26, -84, ancho / 2 - 26, 84), relleno(mezcla(color, "tinta", 0.4)))
    for i in range(1, 6):  # rayitas de display
        y = -84 + i * 28
        c.drawLine(-ancho / 2 + 26, y, ancho / 2 - 26, y, trazo(2, mezcla(color, "blanco", 0.1), 120))
    _texto(c, txt, 0, 46, 130, (255, 226, 80), "sub", ancho - 90)


def barras(c, t=0.0, barras=(), tope=None, progreso=1.0, sufijo="", resalta=(), alto=520, ancho=840, decimales=1,
           **kw):
    """Gráfica de barras; (0, 0) = centro; las barras crecen una tras otra."""
    n = len(barras) or 1
    top = tope or (max(b["valor"] for b in barras) * 1.15 if barras else 1)
    paso = ancho / n
    base = alto / 2
    c.drawLine(-ancho / 2 - 20, base, ancho / 2 + 20, base, trazo(7))
    for i, b in enumerate(barras):
        k = _eo(progreso * n - i * 0.7)
        if k <= 0:
            continue
        x = -ancho / 2 + paso * (i + 0.5)
        h = alto * b["valor"] / top * k
        col = COL.get(b.get("color"), b.get("color")) if isinstance(b.get("color"), str) else b.get("color", (150, 150, 160))
        bw = paso * 0.62
        if i in resalta:
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - bw / 2 - 14, base - h - 14, x + bw / 2 + 14, base + 8), 22, 22),
                        relleno((255, 236, 90), 220))
        pieza(c, rrect(x - bw / 2, base - h, x + bw / 2, base, 16), col, 6,
              shader=degradado(base - h, base, mezcla(col, "blanco", 0.25), col))
        v = b["valor"] * k
        num = f"{v:.{decimales}f}".replace(".", ",") + sufijo
        _texto(c, num, x, base - h - 22, 62, "tinta", "sub", paso * 0.95)
        _texto(c, b.get("texto", ""), x, base + 70, 52, "tinta", "sub", paso * 0.95)


def bola(c, t=0.0, texto="", **kw):
    pieza(c, poly([(-120, 150), (120, 150), (90, 100), (-90, 100)]), "madera", 6)
    g = skia.GradientShader.MakeRadial(skia.Point(-40, -40), 220, [skia.Color(230, 210, 255), skia.Color(120, 80, 200)])
    pieza(c, elipse(0, 0, 150, 150), (160, 120, 230), 7, shader=g)
    for i in range(3):  # remolinos que giran dentro
        a = t * 1.5 + i * 2.1
        c.drawCircle(math.cos(a) * 60, math.sin(a) * 50, 26, relleno("blanco", 70))
    c.drawPath(elipse(-60, -70, 30, 18), relleno("blanco", 170))
    if texto:
        _texto(c, texto, 0, 22, 64, "blanco", "sub", 220)


# ------------------------------------------------------------------ leyes
def lapida(c, t=0.0, texto="R.I.P.", lineas=(), **kw):
    """Lápida de cómic; (0, 0) = suelo."""
    pieza(c, suave([(-170, 0), (-170, -300), (-120, -380), (0, -410), (120, -380), (170, -300), (170, 0)]),
          (200, 204, 212), 7, shader=degradado(-410, 0, (226, 228, 234), (170, 174, 184)))
    _texto(c, texto, 0, -300, 64, (90, 94, 104), "sub")
    for i, ln in enumerate(lineas):
        _texto(c, ln, 0, -220 + i * 52, 44, "tinta", "sub", 290)
    for x in (-150, -60, 70, 150):  # hierbajos
        c.drawPath(poly([(x - 16, 0), (x, -36), (x + 6, 0)]), relleno("hierba"))


def papelera(c, t=0.0, **kw):
    pieza(c, poly([(-130, -200), (130, -200), (100, 120), (-100, 120)]), (150, 160, 172), 7)
    for i in range(7):
        x = -110 + i * 36
        c.drawLine(x, -190, x * 0.78, 110, trazo(4, (110, 118, 130)))
    pieza(c, rrect(-150, -226, 150, -192, 12), (120, 128, 140), 6)
    for i, (x, r) in enumerate(((-60, -20), (10, 16), (60, -8))):  # bolas de papel asomando
        pieza(c, elipse(x, -228 - 10 * i % 20, 40, 34), "blanco", 4)


def libro(c, t=0.0, titulo="LEY", color="rojo", **kw):
    pieza(c, rrect(-150, -200, 150, 200, 14), "blanco", 6)
    pieza(c, rrect(-170, -210, 130, 210, 16), color, 7, shader=degradado(-210, 210, mezcla(color, "blanco", 0.2), color))
    c.drawLine(-140, -210, -140, 210, trazo(5, mezcla(color, "tinta", 0.4)))
    pieza(c, rrect(-110, -90, 100, 30, 10), (250, 236, 200), 4)
    _texto(c, titulo, -5, -10, 50, "tinta", "sub", 190)


# ------------------------------------------------------------------ viajes e historia
def pasaporte(c, t=0.0, abierto=False, **kw):
    gr = (128, 24, 40)
    pieza(c, rrect(-120, -170, 120, 170, 16), gr, 7, shader=degradado(-170, 170, (150, 36, 52), (108, 18, 32)))
    _texto(c, "UNIÓN EUROPEA", 0, -110, 26, (240, 200, 90), "sub")
    _texto(c, "ESPAÑA", 0, -70, 40, (240, 200, 90), "sub")
    c.drawCircle(0, 10, 44, trazo(5, (240, 200, 90)))
    c.drawPath(_estrella5(0, 10, 26), relleno((240, 200, 90)))
    _texto(c, "PASAPORTE", 0, 120, 40, (240, 200, 90), "sub")


def maleta(c, t=0.0, color="naranja", **kw):
    sombra_suelo(c, 0, 150, 160)
    pieza(c, rrect(-60, -200, 60, -140, 20), "tinta", 0)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-60, -200, 60, -150), 20, 20), trazo(14))
    pieza(c, rrect(-170, -150, 170, 140, 30), color, 7, shader=degradado(-150, 140, mezcla(color, "blanco", 0.25), color))
    for x in (-90, 90):
        c.drawLine(x, -150, x, 140, trazo(6, mezcla(color, "tinta", 0.35)))
    for (x, y, d) in ((-20, -40, "espana"), (60, 60, "argentina")):  # pegatinas
        c.save(); c.translate(x, y); c.rotate(-8); tela(c, d, 70, 46, 0, 0); c.restore()


def carabela(c, t=0.0, cruz="portugal", _mov=False, _dir=0, **kw):
    """Nave de vela del siglo XV mirando a la derecha; (0, 0) = centro, flotación y = 80."""
    bob = 7 * math.sin(t * 2)
    c.save()
    if (_dir or kw.get("rumbo", 1)) < 0:
        c.scale(-1, 1)
    c.translate(0, bob); c.rotate(2 * math.sin(t * 1.6))
    casco = suave([(-300, -10), (-230, 90), (210, 90), (300, -40), (180, 10), (-200, 10)])
    pieza(c, casco, (150, 98, 58), 7, shader=degradado(-40, 90, (186, 128, 80), (120, 76, 40)))
    for x in range(-200, 200, 60):
        c.drawLine(x, 20, x + 30, 80, trazo(3, (100, 62, 32)))
    c.drawLine(-40, 10, -40, -330, trazo(9, (110, 70, 40)))
    c.drawLine(130, 10, 130, -230, trazo(8, (110, 70, 40)))
    infla = 1 + 0.08 * math.sin(t * 3)
    for (mx, top, h, w) in ((-40, -310, 230, 220), (130, -210, 160, 150)):
        vela = suave([(mx - w / 2, top), (mx + w / 2, top), (mx + w / 2 + 20 * infla, top + h / 2), (mx + w / 2, top + h),
                      (mx - w / 2, top + h), (mx - w / 2 + 20 * infla, top + h / 2)])
        pieza(c, vela, (250, 244, 226), 6)
        cy = top + h / 2
        col = (214, 30, 36)
        c.drawRect(skia.Rect(mx - 14, cy - h * 0.32, mx + 14, cy + h * 0.32), relleno(col))
        c.drawRect(skia.Rect(mx - w * 0.3, cy - 14, mx + w * 0.3, cy + 14), relleno(col))
    c.save(); c.translate(-40, -360); tela(c, "portugal" if cruz == "portugal" else "castilla", 90, 56, t, 0.8); c.restore()
    c.restore()
    p = skia.Path()
    p.moveTo(-360, 88 + bob)
    for i in range(14):
        x = -360 + i * 54
        p.quadTo(x + 13, 78 + bob, x + 27, 88 + bob)
        p.quadTo(x + 40, 98 + bob, x + 54, 88 + bob)
    p.lineTo(400, 140); p.lineTo(-360, 140); p.close()
    c.drawPath(p, relleno((118, 190, 234), 240))
    c.drawPath(p, trazo(4, (60, 120, 175), 200))


def corona(c, t=0.0, **kw):
    brillo = 0.5 + 0.5 * math.sin(t * 4)
    base = poly([(-150, 60), (-170, -90), (-90, -20), (0, -130), (90, -20), (170, -90), (150, 60)])
    pieza(c, base, "oro", 7, shader=degradado(-130, 60, (255, 230, 120), (220, 160, 30)))
    pieza(c, rrect(-160, 40, 160, 100, 14), (230, 170, 40), 7)
    for x, col in ((-90, "rojo"), (0, "azul"), (90, "verde")):
        pieza(c, elipse(x, 70, 18, 18), col, 4)
    for x, y in ((-170, -90), (0, -130), (170, -90)):
        c.drawCircle(x, y - 14, 16, relleno((255, 250, 220)))
        c.drawCircle(x, y - 14, 16, trazo(4))
    c.drawPath(_estrella5(60, -60, 18 * brillo + 4), relleno("blanco", int(230 * brillo)))


def pergamino(c, t=0.0, titulo="TRATADO", fecha="", lineas=(), **kw):
    """Hoja de tratado antiguo con lacre rojo; (0, 0) = centro."""
    hoja = suave([(-280, -360), (0, -372), (280, -360), (290, 0), (280, 360), (0, 372), (-280, 360), (-290, 0)])
    pieza(c, hoja, (246, 232, 196), 7, shader=degradado(-370, 370, (252, 242, 214), (230, 210, 168)))
    _texto(c, titulo, 0, -250, 60, (90, 60, 30), "sub", 480)
    if fecha:
        _texto(c, fecha, 0, -180, 50, (150, 90, 40), "sub")
    for i in range(7):  # renglones de letra antigua (garabatos)
        y = -110 + i * 46
        c.drawPath(suave([(-200, y), (-100, y - 6), (0, y + 4), (100, y - 5), (200, y)], close=False), trazo(4, (150, 120, 90), 170))
    for i, ln in enumerate(lineas):
        _texto(c, ln, 0, -100 + i * 60, 44, (90, 60, 30), "hand", 480)
    pieza(c, elipse(170, 270, 56, 52), (190, 30, 40), 6)
    c.drawPath(_estrella5(170, 270, 26), relleno((230, 90, 90)))
    pieza(c, poly([(150, 310), (130, 380), (160, 360), (175, 390)]), (190, 30, 40), 4)


# ------------------------------------------------------------------ medios (podcast, tele, calendario)
def microfono(c, t=0.0, encendido=True, **kw):
    """Micro de podcast en brazo articulado; (0, 0) = cabeza del micro."""
    c.drawPath(poly([(30, 60), (150, 200), (150, 330)], close=False), trazo(16, (50, 50, 60)))
    c.drawPath(poly([(30, 60), (150, 200), (150, 330)], close=False), trazo(8, (120, 120, 135)))
    pieza(c, rrect(-60, -130, 60, 90, 56), (60, 60, 72), 7)
    for y in range(-100, 70, 22):
        c.drawLine(-44, y, 44, y, trazo(3, (140, 140, 155)))
    if encendido:
        a = int(160 + 90 * math.sin(t * 6))
        c.drawCircle(0, 112, 12, relleno((255, 60, 70), a))


def silla(c, t=0.0, color="gris", vacia=True, texto="", **kw):
    """Silla de estudio (respaldo alto); (0, 0) = suelo. color de la tapicería; texto en una chapa."""
    col = color if not isinstance(color, str) else color
    c.drawLine(-120, 0, 120, 0, trazo(10))
    for x in (-110, 110):
        c.drawLine(x * 0.8, 0, 0, -150, trazo(12, (60, 60, 70)))
    pieza(c, rrect(-20, -240, 20, -150, 6), (60, 60, 70), 5)
    pieza(c, rrect(-170, -300, 170, -230, 26), col, 7)  # asiento
    pieza(c, rrect(-150, -640, 150, -290, 60), col, 7)  # respaldo
    c.drawPath(elipse(-80, -540, 26, 70), relleno("blanco", 70))
    if texto:
        pieza(c, rrect(-120, -470, 120, -400, 12), "blanco", 5)
        _texto(c, texto, 0, -418, 46, "tinta", "sub", 220)


def tele(c, t=0.0, texto="", color="azul", pantalla=(30, 60, 140), **kw):
    """Televisor de dibujo con antena; (0, 0) = centro de la pantalla. texto = rótulo en pantalla."""
    for a in (-30, 30):
        c.drawLine(0, -250, a * 4, -360, trazo(8))
        c.drawCircle(a * 4, -360, 14, relleno("rojo"))
    pieza(c, rrect(-300, -250, 300, 230, 40), color, 8)
    pieza(c, rrect(-250, -200, 250, 170, 30), pantalla, 7)
    c.drawPath(elipse(-150, -120, 60, 30), relleno("blanco", 60))
    if texto:
        _texto(c, texto, 0, 20, 92, "blanco", "sub", 420)
    for x in (-120, 120):
        c.drawLine(x, 230, x * 1.3, 300, trazo(10))


def calendario(c, t=0.0, mes="NOVIEMBRE", inicio=6, dias=30, marcados=(), colores=None, tachados=(), **kw):
    """Hoja de calendario mensual; (0, 0) = centro. inicio = columna (0=lunes) del día 1. marcados = días con círculo
    (colores: {día: color}); tachados = días con aspa."""
    colores = colores or {}
    pieza(c, rrect(-380, -420, 380, 420, 26), "blanco", 8)
    pieza(c, rrect(-380, -420, 380, -280, 26), "rojo", 8)
    for x in (-200, 200):
        pieza(c, rrect(x - 16, -460, x + 16, -390, 10), (90, 90, 100), 5)
    _texto(c, mes, 0, -320, 76, "blanco", "sub", 600)
    for i, d in enumerate("LMXJVSD"):
        _texto(c, d, -300 + i * 100, -220, 40, (150, 150, 160), "sub")
    for d in range(1, dias + 1):
        k = inicio + d - 1
        x, y = -300 + (k % 7) * 100, -140 + (k // 7) * 100
        _texto(c, str(d), x, y, 46, "rojo" if k % 7 == 6 else "tinta", "sub")
        if d in marcados:
            col = colores.get(d, colores.get(str(d), "rojo"))
            c.drawPath(suave([(x - 44, y - 30), (x, y - 62), (x + 46, y - 26), (x + 34, y + 20), (x - 30, y + 22)]), trazo(8, col))
        if d in tachados:
            c.drawLine(x - 36, y - 56, x + 36, y + 14, trazo(8, "rojo"))
            c.drawLine(x + 36, y - 56, x - 36, y + 14, trazo(8, "rojo"))


def invitacion(c, t=0.0, texto="INVITACIÓN", color="amarillo", abierta=False, **kw):
    """Sobre de invitación con lacre; (0, 0) = centro."""
    pieza(c, rrect(-200, -130, 200, 130, 14), (252, 246, 228), 7)
    if abierta:
        pieza(c, poly([(-198, -128), (0, -260), (198, -128)]), (240, 230, 200), 6)
    else:
        c.drawPath(poly([(-198, -128), (0, 20), (198, -128)], close=False), trazo(6, (170, 150, 110)))
    pieza(c, elipse(0, 20, 40, 38), "rojo", 5)
    c.drawPath(_estrella5(0, 20, 18), relleno((255, 160, 160)))
    if texto:
        pieza(c, rrect(-170, 60, 170, 116, 10), color, 4)
        _texto(c, texto, 0, 104, 40, "tinta", "sub", 320)


def gorra(c, t=0.0, texto="", color="azul", **kw):
    """Gorra de visera con rótulo en el frontal (dos cargos = dos gorras); (0, 0) = centro."""
    pieza(c, suave([(-150, 30), (-140, -60), (-60, -110), (60, -110), (140, -60), (150, 30)]), color, 7)
    pieza(c, suave([(60, 26), (190, 20), (250, 44), (180, 62), (60, 54)]), mezcla(color, "tinta", 0.25), 6)
    c.drawCircle(0, -112, 14, relleno(mezcla(color, "tinta", 0.3))); c.drawCircle(0, -112, 14, trazo(4))
    if texto:
        pieza(c, rrect(-118, -60, 118, 4, 10), "blanco", 4)
        _texto(c, texto, 0, -14, 40, "tinta", "sub", 220)


TIPOS = {"papeleta": papeleta, "urna": urna, "mesa_electoral": mesa_electoral, "camion": camion, "senal": senal,
         "alcoholimetro": alcoholimetro, "contador": contador, "barras": barras, "bola": bola, "lapida": lapida,
         "papelera": papelera, "libro": libro, "pasaporte": pasaporte, "maleta": maleta, "carabela": carabela,
         "corona": corona, "pergamino": pergamino, "microfono": microfono, "silla": silla, "tele": tele,
         "calendario": calendario, "invitacion": invitacion, "gorra": gorra}
TAMANO = {"papeleta": (240, 160), "urna": (430, 400), "mesa_electoral": (720, 270), "camion": (700, 380),
          "senal": (300, 820), "alcoholimetro": (200, 440), "contador": (800, 240), "barras": (900, 700), "bola": (320, 320),
          "lapida": (360, 420), "papelera": (300, 340), "libro": (340, 420), "pasaporte": (240, 340), "maleta": (340, 360),
          "carabela": (680, 520), "corona": (360, 260), "pergamino": (600, 760), "microfono": (340, 480),
          "silla": (360, 660), "tele": (620, 680), "calendario": (780, 900), "invitacion": (420, 280), "gorra": (520, 200)}
APOYADOS = {"mesa_electoral", "lapida", "silla"}
