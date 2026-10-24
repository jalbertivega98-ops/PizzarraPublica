"""Los datos que incomodan #10 · Okupación.

Cifras (consultadas el 13/10/2026):
- Ministerio del Interior, Portal Estadístico de Criminalidad (vía EFE, 29/04/2026): 14.875 hechos conocidos de
  allanamiento/usurpación de inmuebles en 2025 frente a 16.426 en 2024 (−9,4 %). Interior no separa allanamiento y usurpación.
  Cataluña 5.913 (≈40 %), Andalucía 1.909, C. Valenciana 1.805, C. de Madrid 1.269.
- Código Penal: art. 202 (allanamiento de morada: vivienda habitual o segunda residencia, prisión de 6 meses a 2 años)
  y art. 245.2 (usurpación de inmueble que no es morada: multa de 3 a 6 meses).
- LO 1/2025 (en vigor el 3/04/2025): allanamiento y usurpación pasan al juicio rápido (art. 795 LECrim).
- Ley 5/2018: desahucio exprés por la vía civil.
- Cortar suministros por tu cuenta puede ser delito de coacciones (art. 172 CP).
"""
VIDEO = {
    "slug": "di10_okupacion",
    "titulo": "Alguien vive en tu casa.",
    "serie": "LOS DATOS QUE INCOMODAN · #10",
    "acento": "purple",
    "voz": "elevenlabs:Pizarra Pública",
    "claves": ["dentro", "14.875", "9,4", "dos", "allanamiento", "usurpación", "rápido", "40", "sí", "no"],
    "musica": {"bpm": 120, "tono": -1, "seed": 110},
    "portada": {"t": 1.2, "titulo": "ALGUIEN VIVE\nEN TU CASA"},
    "duro": True,
    "planos": [
        # GANCHO
        {"voz": ["Llegas a casa. La llave no entra. Hay alguien dentro."],
         "cam": "golpe",
         "el": [
             {"k": "icono", "n": "casa", "x": 540, "y": 640, "tam": 1.8, "at": 0},
             {"k": "icono", "n": "llave", "x": 300, "y": 1040, "tam": 1.0, "rot": -20, "at": "@llave"},
             {"k": "icono", "n": "cruz", "x": 300, "y": 1040, "tam": 0.8, "at": "@entra"},
             {"k": "pers", "tipo": "ciudadana", "x": 780, "y": 1060, "tam": 1.0, "cara": "shock", "pose": "cabeza", "mira": -1,
              "at": "@dentro"},
         ]},
        {"voz": ["¿Qué pasa de verdad si te okupan la casa?"], "trans": "zoom", "cam": "empuja", "min": 1.4,
         "el": [
             {"k": "icono", "n": "interrogacion", "x": 540, "y": 620, "tam": 1.4, "at": 0.05},
             {"k": "txt", "t": "¿Y AHORA QUÉ?", "px": 96, "y": 960, "at": "@okupan", "marca": "yellow"},
         ]},
        # DATOS
        {"voz": [{"tts": "En dos mil veinticinco hubo catorce mil ochocientas setenta y cinco denuncias por allanamiento o usurpación.",
                  "text": "En 2025 hubo 14.875 denuncias por allanamiento o usurpación."}],
         "trans": "barrido", "cam": "golpe", "fuente": "Ministerio del Interior, 2025",
         "el": [
             {"k": "num", "val": 14875, "desde": 0, "dur": 1.1, "golpe": True, "px": 200, "y": 620, "at": "@14.875-0.2",
              "color": "red", "fondo": "yellow", "sub": "hechos conocidos"},
             {"k": "icono", "n": "documento", "x": 540, "y": 1020, "tam": 1.0, "at": "@denuncias"},
         ]},
        {"voz": [{"tts": "Un nueve coma cuatro por ciento menos que el año anterior.", "text": "Un 9,4 % menos que el año anterior."}],
         "trans": "sube", "cam": "aleja", "fuente": "Ministerio del Interior, 2024-2025",
         "el": [
             {"k": "barras", "y": 1060, "w": 700, "h": 560, "max": 17500, "escalon": 0.6, "px_val": 60,
              "items": [{"label": "2024", "val": 16426, "color": "gray", "txt": "{v}"},
                        {"label": "2025", "val": 14875, "color": "purple", "txt": "{v}"}]},
             {"k": "txt", "t": "−9,4 %", "px": 110, "y": 400, "at": "@menos", "color": "green"},
         ]},
        {"voz": [{"tts": "Y casi el cuarenta por ciento, en Cataluña.", "text": "Y casi el 40 %, en Cataluña."}], "trans": "barrido", "cam": "empuja",
         "fuente": "Interior: Cataluña 5.913 casos en 2025",
         "el": [
             {"k": "barras", "y": 1080, "w": 800, "h": 560, "max": 6400, "escalon": 0.4, "px_label": 30, "px_val": 46,
              "items": [{"label": "CATAL.", "val": 5913, "color": "red", "txt": "{v}"},
                        {"label": "ANDAL.", "val": 1909, "color": "gray", "txt": "{v}"},
                        {"label": "VALENC.", "val": 1805, "color": "gray", "txt": "{v}"},
                        {"label": "MADRID", "val": 1269, "color": "gray", "txt": "{v}"}]},
             {"k": "txt", "t": "≈ 40 %", "px": 100, "y": 380, "at": "@40", "marca": "yellow"},
         ]},
        # GIRO
        {"voz": ["Pero esa cifra mezcla dos delitos muy distintos."], "trans": "flash", "cam": "golpe", "pausa": 0.4,
         "el": [
             {"k": "estallido", "r": 330, "y": 700, "color": "yellow", "at": "@dos-0.2"},
             {"k": "txt", "t": "2 DELITOS\nDISTINTOS", "px": 96, "y": 700, "at": "@dos", "color": "ink"},
         ]},
        {"voz": ["Si es tu casa, la de siempre o tu segunda residencia, es allanamiento de morada. Cárcel de seis meses a dos años."],
         "trans": "barrido", "cam": "empuja", "fuente": "Código Penal, art. 202",
         "el": [
             {"k": "icono", "n": "casa", "x": 300, "y": 760, "tam": 1.3, "at": 0.05},
             {"k": "txt", "t": "ALLANAMIENTO DE MORADA", "px": 62, "y": 440, "at": "@allanamiento", "color": "red"},
             {"k": "icono", "n": "rejas", "x": 780, "y": 760, "tam": 1.0, "at": "@Cárcel"},
             {"k": "txt", "t": "6 MESES - 2 AÑOS", "px": 66, "y": 1100, "at": "@Cárcel+0.3", "marca": "yellow"},
         ]},
        {"voz": ["La policía puede actuar al momento."], "trans": "corte", "cam": "golpe", "min": 1.4,
         "el": [
             {"k": "pers", "tipo": "policia", "x": 540, "y": 900, "tam": 1.4, "cara": "listo", "pose": "señala", "at": 0.05},
             {"k": "sello", "t": "YA", "x": 540, "y": 440, "px": 130, "at": "@momento", "rot": -10},
         ]},
        {"voz": ["Si es un piso vacío, es usurpación. Se castiga con multa, y si ya llevan tiempo dentro, suele hacer falta un juez."],
         "trans": "barrido", "cam": "deriva", "fuente": "Código Penal, art. 245.2",
         "el": [
             {"k": "icono", "n": "edificio", "x": 300, "y": 720, "tam": 1.2, "at": 0.05},
             {"k": "txt", "t": "USURPACIÓN", "px": 90, "y": 440, "at": "@usurpación", "color": "purple"},
             {"k": "icono", "n": "billete", "x": 780, "y": 700, "tam": 0.9, "at": "@multa"},
             {"k": "pers", "tipo": "juez", "x": 780, "y": 1080, "tam": 0.8, "cara": "neutral", "mira": -1, "at": "@llevan"},
         ]},
        {"voz": ["Desde dos mil veinticinco, los dos van por juicio rápido."], "trans": "zoom", "cam": "empuja",
         "fuente": "Ley Orgánica 1/2025",
         "el": [
             {"k": "icono", "n": "reloj", "x": 540, "y": 620, "tam": 1.4, "at": 0.05},
             {"k": "icono", "n": "mazo", "x": 780, "y": 900, "tam": 1.0, "rot": -12, "at": "@dos"},
             {"k": "txt", "t": "JUICIO RÁPIDO", "px": 90, "y": 1060, "at": "@juicio", "marca": "yellow"},
         ]},
        # QUÉ HACER
        {"voz": ["Si te pasa: denuncia ya, y lleva escrituras o contrato."], "trans": "sube", "cam": "golpe",
         "el": [
             {"k": "txt", "t": "1 · DENUNCIA YA", "px": 76, "y": 520, "at": "@denuncia", "color": "green"},
             {"k": "icono", "n": "documento", "x": 300, "y": 900, "tam": 1.0, "at": "@escrituras"},
             {"k": "txt", "t": "2 · ESCRITURAS\nO CONTRATO", "px": 64, "y": 900, "x": 740, "at": "@escrituras", "color": "green"},
         ]},
        {"voz": ["Y no les cortes la luz ni el agua por tu cuenta: podrías acabar denunciado tú."], "trans": "flash", "cam": "golpe",
         "fuente": "Código Penal, art. 172: coacciones",
         "el": [
             {"k": "txt", "t": "3 · NO CORTES\nLUZ NI AGUA", "px": 76, "y": 520, "at": "@cortes", "color": "red"},
             {"k": "pers", "tipo": "ciudadano", "x": 540, "y": 1000, "tam": 1.1, "cara": "nervioso", "pose": "encoge", "at": "@cortes"},
             {"k": "sello", "t": "DENUNCIADO TÚ", "x": 540, "y": 760, "px": 64, "at": "@denunciado", "rot": -10},
         ]},
        # PREGUNTA
        {"voz": ["¿Crees que la ley protege lo suficiente a los propietarios? A: sí. B: no.", "Comenta A o B."],
         "trans": "zoom", "cam": "quieta", "min": 0, "cola": 1.8,
         "el": [
             {"k": "encuesta", "pregunta": "¿LA LEY PROTEGE\nAL PROPIETARIO?", "a": "SÍ", "b": "NO", "color_a": "green", "color_b": "red",
              "at": 0.05, "at_a": "@sí", "at_b": "@no", "at_c": "L1"},
         ]},
    ],
}
