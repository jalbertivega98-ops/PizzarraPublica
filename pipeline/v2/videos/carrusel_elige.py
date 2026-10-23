"""Carrusel de 3 fotos para TikTok: votación del próximo «Los datos que incomodan».

Se renderiza como vídeo mudo sin subtítulos y se extrae un fotograma por plano (ver la historia historia_elige.py).
"""
CARDS = [
    ("A", "hospital", "SANIDAD «GRATIS»:\n¿QUIÉN LA PAGA?", "teal"),
    ("B", "casa", "TOPAR EL ALQUILER:\n¿FUNCIONA?", "orange"),
    ("C", "documento", "PROMESAS:\nDICHO VS HECHO", "purple"),
    ("D", "pasaporte", "REGULARIZACIÓN:\nLA CIFRA QUE NADIE VIO", "red"),
]
_els = [{"k": "txt", "t": "4 TEMAS QUE\nINCOMODAN", "px": 80, "y": 410, "at": 0, "color": "ink"}]
for i, (letra, ico, txt, col) in enumerate(CARDS):
    y = 640 + 200 * i
    _els += [
        {"k": "panel", "w": 820, "h": 170, "x": 540, "y": y, "color": col, "at": 0},
        {"k": "txt", "t": letra, "px": 96, "x": 195, "y": y + 8, "at": 0, "color": "white"},
        {"k": "icono", "n": ico, "x": 315, "y": y, "tam": 0.6, "at": 0},
        {"k": "txt", "t": txt, "px": 44, "x": 650, "y": y - 2, "ancho": 520, "at": 0, "color": "ink"},
    ]
_els += [{"k": "txt", "t": "DESLIZA PARA VOTAR", "px": 60, "y": 1500, "at": 0, "marca": "yellow"}]

VIDEO = {
    "slug": "carrusel_elige",
    "titulo": "Tú eliges el próximo vídeo",
    "serie": "LOS DATOS QUE INCOMODAN",
    "acento": "yellow",
    "voz": "elevenlabs:Pizarra Pública",
    "sin_subs": True,
    "musica": {"bpm": 120, "tono": 0, "seed": 7},
    "portada": {"t": 1.5, "titulo": "TÚ ELIGES"},
    "planos": [
        {"voz": ["uno"], "cam": "quieta", "min": 3,
         "el": [
             {"k": "estallido", "r": 400, "y": 700, "color": "yellow", "at": 0},
             {"k": "txt", "t": "TÚ\nELIGES", "px": 180, "y": 680, "at": 0, "color": "ink"},
             {"k": "txt", "t": "EL PRÓXIMO VÍDEO", "px": 76, "y": 1080, "at": 0, "marca": "yellow"},
             {"k": "pers", "tipo": "ciudadana", "x": 260, "y": 1330, "tam": 0.8, "cara": "duda", "pose": "señala", "at": 0},
             {"k": "pers", "tipo": "joven", "x": 820, "y": 1330, "tam": 0.8, "cara": "feliz", "pose": "brazos_arriba", "mira": -1, "at": 0},
         ]},
        {"voz": ["dos"], "trans": "corte", "cam": "quieta", "min": 3, "el": _els},
        {"voz": ["tres"], "trans": "corte", "cam": "quieta", "min": 3,
         "el": [
             {"k": "txt", "t": "¿CUÁL QUIERES?", "px": 96, "y": 430, "at": 0, "color": "ink"},
             {"k": "txt", "t": "A  ·  B  ·  C  ·  D", "px": 120, "y": 700, "at": 0, "color": "red"},
             {"k": "icono", "n": "movil", "x": 540, "y": 990, "tam": 1.2, "at": 0},
             {"k": "sello", "t": "COMENTA TU LETRA", "x": 540, "y": 1260, "px": 72, "at": 0, "rot": -6},
             {"k": "txt", "t": "El más votado será el próximo vídeo", "px": 44, "y": 1440, "at": 0, "fuente": "ui", "color": "ink"},
         ]},
    ],
}
