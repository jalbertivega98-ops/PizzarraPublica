"""Objetos de sucesos y emergencias (octubre de 2026), para vídeos de tono serio: sin caras ni gags.
Se registran en objetos.TIPOS como los de civico.py:

  lazo         lazo de luto (negro por defecto); props: color
  helicoptero  helicóptero sanitario blanco con cruz roja; el rotor gira siempre
  ambulancia   ambulancia blanca con franja roja y luces que parpadean; _mov la hace rodar
  gota         gota de sangre (donaciones); props: texto (debajo)
  via          tramo de vía de tren visto de lado (raíles y traviesas); props: ancho
"""
import math

from .estilo import degradado, elipse, pieza, poly, relleno, rrect, sombra_suelo, suave, trazo
from .civico import _rueda, _texto


def lazo(c, t=0.0, color=(34, 34, 40), **kw):
    """Lazo de luto: dos colas cruzadas y el nudo arriba."""
    claro = (90, 90, 100)
    for sx in (-1, 1):
        cola = suave([(0, -40), (sx * 40, 40), (sx * 120, 260), (sx * 60, 250), (sx * 30, 230), (sx * -10, 60)])
        pieza(c, cola, color, 7, shader=degradado(-40, 260, claro, color))
    for sx in (-1, 1):
        oreja = suave([(0, -40), (sx * 70, -170), (sx * 140, -150), (sx * 120, -60), (sx * 30, -10)])
        pieza(c, oreja, color, 7, shader=degradado(-170, -10, claro, color))
    pieza(c, elipse(0, -36, 34, 30), color, 7)


def helicoptero(c, t=0.0, **kw):
    """Helicóptero sanitario mirando a la derecha; (0, 0) = centro de la cabina."""
    bote = 6 * math.sin(t * 3)
    c.save(); c.translate(0, bote)
    pieza(c, rrect(-330, -40, -120, 10, 10), "blanco", 6)  # cola
    pieza(c, poly([(-350, -100), (-310, -100), (-300, -30), (-340, -30)]), "rojo", 6)
    pieza(c, suave([(-150, -110), (120, -120), (200, -40), (190, 70), (-140, 80), (-170, -10)]), "blanco", 7,
          shader=degradado(-120, 80, "blanco", (222, 228, 238)))
    pieza(c, suave([(70, -100), (130, -100), (185, -40), (70, -40)]), "cristal", 5)
    pieza(c, rrect(-90, -60, -20, 10, 6), "rojo", 0)  # cruz
    pieza(c, rrect(-125, -50, 15, 0, 6), "rojo", 0)
    for x in (-110, 110):  # patines
        c.drawLine(x, 80, x, 120, trazo(7))
    c.drawLine(-170, 120, 170, 120, trazo(8))
    c.drawLine(0, -120, 0, -150, trazo(9))
    a = abs(math.cos(t * 30))  # rotor visto de lado: se encoge y se estira
    c.drawLine(-300 * a, -152, 300 * a, -152, trazo(10, (60, 64, 76)))
    c.drawCircle(-340, -60, 30 + 10 * abs(math.sin(t * 30)), trazo(4, (60, 64, 76), 160))
    c.restore()


def ambulancia(c, t=0.0, _mov=False, **kw):
    """Ambulancia mirando a la derecha; (0, 0) = centro, ruedas en y = 110."""
    sombra_suelo(c, 0, 150, 330)
    pieza(c, rrect(-330, -230, 140, 90, 18), "blanco", 7, shader=degradado(-230, 90, "blanco", (226, 230, 238)))
    pieza(c, rrect(-326, 10, 136, 44, 0), "rojo", 0)
    pieza(c, rrect(-130, -180, -70, -60, 6), "rojo", 0)
    pieza(c, rrect(-160, -150, -40, -90, 6), "rojo", 0)
    pieza(c, suave([(140, 90), (140, -150), (230, -150), (320, -40), (330, 90)]), "blanco", 7,
          shader=degradado(-150, 90, "blanco", (226, 230, 238)))
    pieza(c, poly([(166, -128), (226, -128), (290, -46), (166, -46)]), "cristal", 5)
    encendida = int(t * 4) % 2 == 0
    for x, col in ((-60, "azul"), (20, "rojo")):
        pieza(c, rrect(x - 26, -262, x + 26, -230, 8), col if encendida else (120, 124, 140), 5)
    if encendida:
        c.drawCircle(-60, -246, 60, relleno("azul", 70))
    for x in (-230, 230):
        _rueda(c, x, 110, 44, t * (6 if _mov else 0))


def gota(c, t=0.0, texto="", **kw):
    """Gota de sangre."""
    pieza(c, suave([(0, -170), (60, -60), (110, 30), (90, 110), (0, 150), (-90, 110), (-110, 30), (-60, -60)]), "rojo", 7,
          shader=degradado(-170, 150, (240, 110, 100), "rojo"))
    c.drawPath(elipse(-50, 40, 14, 30), relleno("blanco", 170))
    if texto:
        _texto(c, texto, 0, 230, 44, "tinta", "sub", 420)


def via(c, t=0.0, ancho=1000, **kw):
    """Vía de lado; (0, 0) = centro, los raíles en y = 0 (las ruedas del tren van encima)."""
    for i in range(int(ancho // 70) + 1):
        x = -ancho / 2 + i * 70
        pieza(c, rrect(x - 22, 6, x + 22, 30, 5), "madera", 4)
    pieza(c, rrect(-ancho / 2, -6, ancho / 2, 8, 4), (150, 154, 162), 5)


TIPOS = {"via": via, "lazo": lazo, "helicoptero": helicoptero, "ambulancia": ambulancia, "gota": gota}
TAMANO = {"via": (1000, 40), "lazo": (300, 460), "helicoptero": (720, 300), "ambulancia": (700, 400), "gota": (240, 340)}
APOYADOS = set()
