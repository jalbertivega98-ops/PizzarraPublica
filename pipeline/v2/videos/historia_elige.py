"""Historia para Instagram y TikTok: la gente elige el próximo «Los datos que incomodan».

Sin voz ni subtítulos (VIDEO["sin_subs"]); las frases de "voz" solo marcan el ritmo y no se locutan.
Temas pendientes de 15_temas_incomodos.md: 8 (sanidad), 13 (topar el alquiler), 14 (promesas), 1 (regularización).
Sin cifras en pantalla: se verifican al escribir el guion del tema ganador.
"""
CARDS = [
    ("A", "hospital", "SANIDAD «GRATIS»:\n¿QUIÉN LA PAGA?", "teal"),
    ("B", "casa", "TOPAR EL ALQUILER:\n¿FUNCIONA?", "orange"),
    ("C", "documento", "PROMESAS:\nDICHO VS HECHO", "purple"),
    ("D", "pasaporte", "REGULARIZACIÓN:\nLA CIFRA QUE NADIE VIO", "red"),
]
_els = [{"k": "txt", "t": "¿QUÉ VÍDEO\nHACEMOS AHORA?", "px": 80, "y": 410, "at": 0.05, "color": "ink"}]
for i, (letra, ico, txt, col) in enumerate(CARDS):
    y = 640 + 200 * i
    t0 = 0.5 + 0.55 * i
    _els += [
        {"k": "panel", "w": 820, "h": 170, "x": 540, "y": y, "color": col, "at": t0},
        {"k": "txt", "t": letra, "px": 96, "x": 195, "y": y + 8, "at": t0 + 0.08, "color": "white"},
        {"k": "icono", "n": ico, "x": 315, "y": y, "tam": 0.6, "at": t0 + 0.12},
        {"k": "txt", "t": txt, "px": 44, "x": 650, "y": y - 2, "ancho": 520, "at": t0 + 0.16, "color": "ink"},
    ]
_els += [{"k": "sello", "t": "VOTA AQUÍ ABAJO", "x": 540, "y": 1520, "px": 60, "at": 3.0, "rot": -4}]

VIDEO = {
    "slug": "historia_elige",
    "titulo": "Tú eliges el próximo vídeo",
    "serie": "LOS DATOS QUE INCOMODAN",
    "acento": "yellow",
    "voz": "elevenlabs:Pizarra Pública",
    "sin_subs": True,
    "musica": {"bpm": 124, "tono": 0, "seed": 131},
    "portada": {"t": 9.5, "titulo": "TÚ ELIGES"},
    "duro": True,
    "planos": [
        {"voz": ["Tú eliges"], "cam": "golpe", "min": 2.2,
         "el": [
             {"k": "estallido", "r": 380, "y": 760, "color": "yellow", "at": 0},
             {"k": "txt", "t": "TÚ\nELIGES", "px": 170, "y": 700, "at": 0.1, "color": "ink"},
             {"k": "txt", "t": "EL PRÓXIMO VÍDEO", "px": 70, "y": 1080, "at": 0.6, "marca": "yellow"},
         ]},
        {"voz": ["opciones"], "trans": "barrido", "cam": "quieta", "min": 8.0, "el": _els},
    ],
}
