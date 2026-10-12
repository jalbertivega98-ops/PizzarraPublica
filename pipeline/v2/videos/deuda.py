"""Los datos que incomodan #7 · La deuda pública.

- Banco de España (17/09/2026): deuda de las Administraciones Públicas (PDE) en julio de 2026 = 1,744 billones €, 99,9 % del PIB;
  +3,8 % interanual en euros, −2,4 puntos sobre el PIB; primera vez por debajo del 100 % desde febrero de 2020.
  Máximo en euros: junio de 2026, 1,762-1,763 billones (101,4-101,5 % del PIB).
- Por habitante: 1,744 billones / 49.801.559 habitantes (INE, 1/07/2026) ≈ 35.020 €.
- Ritmo: +3,8 % interanual ≈ +63.800 M€ en un año ≈ 175 M€ al día ≈ 2.000 € por segundo (cálculo propio, media del último año).
- 2007: 35,8 % del PIB (Eurostat / Banco de España, deuda PDE).
"""
VIDEO = {
    "slug": "di07_deuda",
    "titulo": "Debes 35.000 € y no lo sabías.",
    "serie": "LOS DATOS QUE INCOMODAN · #7",
    "acento": "blue",
    "voz": "elevenlabs:Pizarra Pública",
    "claves": ["35.000", "segundo", "2.000", "dos", "verdad", "honesto"],
    "musica": {"bpm": 114, "tono": 1, "seed": 77},
    "portada": {"t": 1.3, "titulo": "DEBES 35.000 €\nY NO LO SABÍAS"},
    "planos": [
        # GANCHO
        {"voz": [{"tts": "Debes treinta y cinco mil euros.", "text": "Debes 35.000 €."}],
         "cam": "golpe", "min": 1.6, "fuente": "Banco de España e INE, 2026",
         "el": [
             {"k": "num", "val": 35000, "desde": 0, "dur": 0.8, "golpe": True, "px": 180, "y": 640, "suf": " €", "color": "red", "fondo": "yellow", "at": 0},
             {"k": "pers", "tipo": "ciudadana", "x": 540, "y": 1080, "tam": 1.1, "cara": "shock", "pose": "cabeza", "at": 0.2},
         ]},
        {"voz": ["Tú, tu madre, y el bebé que nació ayer."], "trans": "zoom", "cam": "empuja",
         "el": [
             {"k": "pers", "tipo": "joven", "x": 220, "y": 900, "tam": 1.0, "cara": "duda", "at": "@Tú"},
             {"k": "pers", "tipo": "jefa", "x": 540, "y": 900, "tam": 1.0, "cara": "sorpresa", "at": "@madre"},
             {"k": "pers", "tipo": "ciudadano", "x": 860, "y": 980, "tam": 0.6, "cara": "feliz", "at": "@bebé"},
             {"k": "txt", "t": "35.000 € CADA UNO", "px": 72, "y": 420, "at": "@ayer", "marca": "yellow"},
         ]},
        {"voz": ["Es lo que toca por cabeza de la deuda pública."], "trans": "barrido", "cam": "deriva",
         "el": [
             {"k": "icono", "n": "documento", "x": 540, "y": 760, "tam": 1.8, "at": 0.05},
             {"k": "sello", "t": "DEUDA PÚBLICA", "x": 540, "y": 800, "px": 72, "at": "@deuda", "rot": -10},
         ]},
        # DATOS
        {"voz": [{"tts": "Un billón setecientos cuarenta y cuatro mil millones de euros.", "text": "1,744 billones de euros."}],
         "trans": "flash", "cam": "golpe", "fuente": "Banco de España, julio 2026",
         "el": [
             {"k": "txt", "t": "1.744.000.000.000 €", "px": 92, "y": 640, "at": 0.1, "color": "red"},
             {"k": "dinero", "modo": "lluvia", "n": 30, "at": 0.3, "dur": 2.2, "z": -1},
             {"k": "txt", "t": "BILLONES CON B", "px": 64, "y": 840, "at": "@billones", "marca": "yellow"},
         ]},
        {"voz": [{"tts": "Y sigue subiendo: unos dos mil euros cada segundo.", "text": "Y sigue subiendo: unos 2.000 € cada segundo."}],
         "trans": "zoom", "cam": "empuja", "fuente": "Cálculo propio: +3,8 % en el último año",
         "el": [
             {"k": "icono", "n": "reloj", "x": 540, "y": 520, "tam": 1.3, "at": 0.05},
             {"k": "num", "val": 2000, "desde": 0, "dur": 0.7, "golpe": True, "px": 200, "y": 900, "suf": " €", "color": "red", "at": "@2.000-0.3"},
             {"k": "txt", "t": "POR SEGUNDO", "px": 76, "y": 1080, "at": "@segundo", "fuente": "num"},
         ]},
        {"voz": [{"tts": "Mientras ves este vídeo, unos ochenta mil euros más.", "text": "Mientras ves este vídeo, unos 80.000 € más."}],
         "trans": "barrido", "cam": "golpe",
         "el": [
             {"k": "num", "val": 80000, "desde": 0, "dur": 1.6, "px": 170, "y": 660, "suf": " €", "color": "red", "at": "@vídeo", "pre": "+"},
             {"k": "icono", "n": "movil", "x": 540, "y": 1000, "tam": 1.0, "at": 0.05},
         ]},
        {"voz": [{"tts": "En dos mil siete era el treinta y seis por ciento del PIB. Hoy, casi el cien.", "text": "En 2007 era el 36 % del PIB. Hoy, casi el 100 %."}],
         "trans": "zoom", "cam": "aleja", "fuente": "Banco de España / Eurostat",
         "el": [
             {"k": "barras", "y": 1040, "w": 700, "h": 560, "max": 105, "escalon": 1.6,
              "items": [{"label": "2007", "val": 35.8, "color": "green", "txt": "{v} %", "dec": 1},
                        {"label": "JULIO 2026", "val": 99.9, "color": "red", "txt": "{v} %", "dec": 1}]},
         ]},
        {"voz": ["Es como deber un año entero de todo lo que produce el país."], "trans": "sube", "cam": "empuja",
         "el": [
             {"k": "icono", "n": "calendario", "x": 300, "y": 760, "tam": 1.5, "at": "@año"},
             {"k": "txt", "t": "= 1 AÑO\nDE PIB", "px": 100, "y": 760, "x": 760, "at": "@entero", "color": "blue"},
         ]},
        # GIRO
        {"voz": ["Y aquí viene el truco: el Gobierno dice que baja… y la oposición, que sube."], "trans": "flash", "cam": "deriva",
         "pausa": 0.4,
         "el": [
             {"k": "pers", "tipo": "politico", "x": 300, "y": 900, "tam": 1.2, "cara": "feliz", "pose": "señala", "at": "@Gobierno",
              "rotulo": "GOBIERNO", "px_rotulo": 40},
             {"k": "bocadillo", "t": "¡Baja!", "x": 290, "y": 520, "px": 70, "cola": [-10, 170], "at": "@baja"},
             {"k": "pers", "tipo": "politico", "x": 780, "y": 900, "tam": 1.2, "cara": "enfado", "pose": "jarras", "mira": -1, "at": "@oposición",
              "rotulo": "OPOSICIÓN", "px_rotulo": 40},
             {"k": "bocadillo", "t": "¡Sube!", "x": 790, "y": 520, "px": 70, "cola": [10, 170], "at": "@sube"},
         ]},
        {"voz": ["Los dos dicen la verdad."], "trans": "corte", "cam": "golpe", "min": 1.3,
         "el": [
             {"k": "estallido", "r": 320, "y": 700, "color": "yellow", "at": 0},
             {"k": "txt", "t": "LOS DOS\nTIENEN RAZÓN", "px": 96, "y": 700, "at": "@dos", "color": "ink"},
         ]},
        {"voz": [{"tts": "Sobre el PIB baja: ha caído del cien por cien por primera vez desde dos mil veinte. En euros sube: un tres coma ocho por ciento en un año.",
                  "text": "Sobre el PIB baja: ha caído del 100 % por primera vez desde 2020. En euros sube: un 3,8 % en un año."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Banco de España, julio 2026",
         "el": [
             {"k": "txt", "t": "% DEL PIB", "px": 64, "y": 470, "x": 300, "at": "@PIB"},
             {"k": "flecha", "de": [300, 560], "a": [300, 860], "at": "@baja", "color": "green"},
             {"k": "txt", "t": "BAJA", "px": 80, "y": 960, "x": 300, "at": "@baja", "color": "green"},
             {"k": "txt", "t": "EUROS", "px": 64, "y": 470, "x": 780, "at": "@euros"},
             {"k": "flecha", "de": [780, 860], "a": [780, 560], "at": "@sube", "color": "red"},
             {"k": "txt", "t": "+3,8 %", "px": 80, "y": 960, "x": 780, "at": "@3,8", "color": "red"},
         ]},
        {"voz": ["El país crece más rápido que su deuda… pero la deuda no deja de crecer."], "trans": "tinta", "cam": "deriva",
         "el": [
             {"k": "icono", "n": "grafica", "x": 300, "y": 760, "tam": 1.3, "color": "green", "at": "@crece"},
             {"k": "txt", "t": "PIB", "px": 70, "y": 1000, "x": 300, "at": "@crece", "color": "green"},
             {"k": "icono", "n": "grafica", "x": 780, "y": 760, "tam": 1.3, "color": "red", "at": "@deuda"},
             {"k": "txt", "t": "DEUDA", "px": 70, "y": 1000, "x": 780, "at": "@deuda", "color": "red"},
         ]},
        # PREGUNTA
        {"voz": ["¿Qué número te parece más honesto: el de los euros o el del porcentaje?", "Comenta A o B."], "trans": "zoom", "cam": "quieta", "min": 0, "cola": 1.8,
         "el": [
             {"k": "encuesta", "pregunta": "¿QUÉ NÚMERO ES\nMÁS HONESTO?", "a": "LOS EUROS", "b": "EL PORCENTAJE", "color_a": "red", "color_b": "blue",
              "at": 0.05, "at_a": "@euros", "at_b": "@porcentaje", "at_c": "L1"},
         ]},
    ],
}
