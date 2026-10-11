"""Los datos que incomodan #2 · Bajas médicas: quien decide no paga.

Cifras: AIReF, estudio de incapacidad temporal (Spending Review 2022-2026), presentado el 04/02/2026, datos 2017-2024.
- Gasto de la Seguridad Social en IT: 16.500 M€ en 2024; el triple que en 2014; 2.º gasto tras pensiones.
- Bajas por contingencia común: 4,7 millones (2017) → casi 8,6 millones (2024).
- Duración media salud mental: 67 días (2017) → 98,5 (2024).
- El 25 % de quienes tienen bajas acumula el 55 % de los procesos.
- Pasar de temporal a fijo eleva un 30 % la probabilidad de iniciar una baja.
- La AIReF no cuantifica fraude; habla de deficiencias de gestión y control.
- Quién paga: días 4-15 la empresa, desde el 16 la Seguridad Social/mutua (LGSS).
"""
VIDEO = {
    "slug": "di02_bajas",
    "titulo": "Quien firma tu baja no la paga",
    "serie": "LOS DATOS QUE INCOMODAN · #2",
    "acento": "teal",
    "claves": ["triple", "firma", "paga", "decide", "fraude", "mental"],
    "musica": {"bpm": 100, "tono": -3, "seed": 22},
    "planos": [
        {"voz": ["Las bajas médicas ya cuestan el triple que hace diez años."], "cam": "golpe", "fuente": "AIReF, 2026",
         "el": [
             {"k": "estallido", "r": 270, "y": 640, "color": "yellow", "at": 0},
             {"k": "num", "val": 3, "desde": 3, "pre": "x", "px": 330, "y": 760, "golpe": True, "color": "teal", "at": 0},
             {"k": "icono", "n": "hospital", "x": 200, "y": 1020, "tam": 0.8, "at": "@médicas", "rot": -8},
             {"k": "dinero", "modo": "fuga", "desde": [200, 1000], "hacia": [700, -200], "n": 14, "at": "@cuestan", "dur": 1.4},
         ]},
        {"voz": ["Y quien las firma… no las paga."], "trans": "zoom", "cam": "empuja",
         "el": [
             {"k": "pers", "tipo": "medico", "x": 290, "y": 840, "tam": 1.35, "cara": "listo", "pose": "sostiene", "sostiene": "papel",
              "rotulo": "FIRMA", "px_rotulo": 64, "anim": "entra_izq"},
             {"k": "pers", "tipo": "hucha", "x": 790, "y": 860, "tam": 1.1, "cara": "nervioso", "rotulo": "", "at": "@paga-0.4",
              "anim": "cae"},
             {"k": "txt", "t": "PAGA", "px": 64, "x": 770, "y": 1090, "at": "@paga"},
         ]},
        {"voz": [{"tts": "La Seguridad Social pagó dieciséis mil quinientos millones de euros en 2024.",
                  "text": "La Seguridad Social pagó 16.500 millones de euros en 2024."}],
         "trans": "barrido", "cam": "golpe", "fuente": "AIReF, 2026 (datos de 2024)",
         "el": [
             {"k": "dinero", "modo": "lluvia", "n": 26, "at": "@pagó", "dur": 2.2, "z": -1},
             {"k": "num", "val": 16500, "desde": 0, "dur": 0.9, "golpe": True, "px": 200, "y": 680, "suf": " M€", "at": "@16.500-0.2",
              "fondo": "yellow"},
             {"k": "txt", "t": "EN BAJAS MÉDICAS", "px": 64, "y": 870, "at": "@euros"},
         ]},
        {"voz": ["El segundo mayor gasto de la Seguridad Social. Solo le ganan las pensiones."], "trans": "sube", "cam": "aleja",
         "el": [
             {"k": "panel", "x": 330, "y": 830, "w": 360, "h": 560, "color": "light", "t": "1.º", "px": 90, "at": "@pensiones-0.6"},
             {"k": "txt", "t": "PENSIONES", "px": 54, "x": 330, "y": 1150, "at": "@pensiones"},
             {"k": "panel", "x": 750, "y": 930, "w": 360, "h": 360, "color": "teal", "t": "2.º", "px": 90, "at": "@segundo"},
             {"k": "txt", "t": "BAJAS", "px": 70, "x": 750, "y": 1150, "at": "@segundo+0.2", "color": "teal"},
             {"k": "icono", "n": "hospital", "x": 750, "y": 960, "tam": 0.9, "at": "@gasto"},
         ]},
        {"voz": [{"tts": "En dos mil diecisiete hubo cuatro coma siete millones de bajas. En dos mil veinticuatro, casi ocho coma seis millones.",
                  "text": "En 2017 hubo 4,7 millones de bajas. En 2024, casi 8,6 millones."}],
         "trans": "barrido", "cam": "empuja", "fuente": "AIReF · bajas por enfermedad común",
         "el": [
             {"k": "barras", "y": 1020, "w": 700, "h": 560, "max": 9, "at": "@2017", "escalon": 1.7,
              "items": [{"label": "2017", "val": 4.7, "color": "light", "txt": "{v} M", "dec": 1},
                        {"label": "2024", "val": 8.6, "color": "teal", "txt": "{v} M", "dec": 1}]},
         ]},
        {"voz": [{"tts": "Y duran más: las de salud mental, de sesenta y siete días a casi cien.",
                  "text": "Y duran más: las de salud mental, de 67 días a casi 100."}],
         "trans": "tinta", "cam": "deriva", "fuente": "AIReF · duración media 2017 → 2024",
         "el": [
             {"k": "icono", "n": "cerebro", "x": 280, "y": 520, "tam": 1.2, "at": "@mental", "flota": True},
             {"k": "icono", "n": "reloj", "x": 800, "y": 520, "tam": 1.0, "at": "@duran", "flota": True},
             {"k": "num", "val": 98.5, "desde": 67, "dec": 1, "dur": 1.2, "suf": " días", "px": 170, "y": 900, "at": "@67", "golpe": True,
              "color": "teal"},
         ]},
        {"voz": ["Ahora, lo raro: la baja la firma tu médico, que depende de tu comunidad autónoma."],
         "pausa": 0.35, "trans": "flash", "cam": "golpe",
         "el": [
             {"k": "pers", "tipo": "medico", "x": 330, "y": 860, "tam": 1.4, "cara": "neutral", "pose": "sostiene", "sostiene": "papel",
              "anim": "pop", "cambios": [["@firma", {"cara": "feliz"}]]},
             {"k": "icono", "n": "edificio", "x": 790, "y": 560, "tam": 1.0, "at": "@comunidad-0.3"},
             {"k": "txt", "t": "COMUNIDAD\nAUTÓNOMA", "px": 56, "x": 790, "y": 780, "at": "@comunidad"},
             {"k": "flecha", "de": [700, 860], "a": [470, 760], "at": "@depende", "color": "ink"},
         ]},
        {"voz": ["Pero la pagan la Seguridad Social… y tu empresa."], "trans": "barrido", "cam": "empuja",
         "el": [
             {"k": "pers", "tipo": "hucha", "x": 300, "y": 840, "tam": 1.05, "cara": "triste", "anim": "cae", "at": "@Seguridad-0.3"},
             {"k": "pers", "tipo": "jefa", "x": 800, "y": 840, "tam": 1.25, "cara": "enfado", "pose": "jarras", "mira": -1, "at": "@empresa-0.2"},
             {"k": "dinero", "modo": "fuga", "desde": [300, 760], "hacia": [540, -300], "n": 8, "at": "@pagan", "dur": 1.2},
             {"k": "dinero", "modo": "fuga", "desde": [800, 760], "hacia": [540, -300], "n": 8, "at": "@empresa", "dur": 1.2},
         ]},
        {"voz": ["Quien decide no paga.", "Y quien paga, no decide."], "trans": "zoom", "cam": "empuja",
         "el": [
             {"k": "panel", "x": 290, "y": 760, "w": 440, "h": 720, "color": "teal", "t": "DECIDE", "px": 66},
             {"k": "pers", "tipo": "medico", "x": 290, "y": 820, "tam": 1.0, "cara": "listo", "anim": "pop", "at": 0.15},
             {"k": "panel", "x": 790, "y": 760, "w": 440, "h": 720, "color": "pink", "t": "PAGA", "px": 66, "at": "@paga"},
             {"k": "pers", "tipo": "hucha", "x": 780, "y": 840, "tam": 0.8, "cara": "nervioso", "anim": "pop", "at": "@paga+0.1"},
             {"k": "txt", "t": "≠", "px": 220, "x": 540, "y": 760, "color": "red", "at": "L1", "anim": "golpe"},
         ]},
        {"voz": ["Más: un cuarto de quienes se dan de baja acumula más de la mitad de todas las bajas."], "trans": "sube", "cam": "deriva",
         "fuente": "AIReF · 25 % de las personas, 55 % de las bajas",
         "el": [
             {"k": "gente", "n": 4, "cols": 4, "sep": 200, "y": 560, "destacar": [0], "apagar": "@acumula", "color": "teal", "color_dest": "red"},
             {"k": "num", "val": 55, "desde": 0, "suf": " %", "dur": 0.8, "px": 200, "y": 940, "at": "@mitad-0.2", "golpe": True, "color": "red",
              "sub": "de todas las bajas"},
         ]},
        {"voz": [{"tts": "Y al pasar de temporal a fijo, la probabilidad de coger una baja sube un treinta por ciento.",
                  "text": "Y al pasar de temporal a fijo, la probabilidad de coger una baja sube un 30 %."}],
         "trans": "barrido", "cam": "empuja", "fuente": "AIReF, junio 2026",
         "el": [
             {"k": "icono", "n": "documento", "x": 260, "y": 520, "tam": 1.0, "rot": -6, "at": "@temporal"},
             {"k": "txt", "t": "TEMPORAL", "px": 52, "x": 260, "y": 690, "at": "@temporal"},
             {"k": "flecha", "de": [380, 520], "a": [690, 520], "at": "@fijo-0.2"},
             {"k": "icono", "n": "documento", "x": 820, "y": 520, "tam": 1.0, "rot": 6, "at": "@fijo"},
             {"k": "txt", "t": "FIJO", "px": 60, "x": 820, "y": 690, "at": "@fijo"},
             {"k": "num", "val": 30, "desde": 0, "pre": "+", "suf": " %", "dur": 0.6, "px": 220, "y": 1010, "at": "@30-0.3", "golpe": True,
              "color": "red", "fondo": "yellow"},
         ]},
        {"voz": ["Pero ojo: esto no demuestra fraude. La AIReF no lo calcula."], "pausa": 0.55, "trans": "flash", "cam": "golpe",
         "el": [
             {"k": "txt", "t": "¿FRAUDE?", "px": 150, "y": 600, "at": "@fraude-0.3", "color": "ink"},
             {"k": "sello", "t": "NO DEMOSTRADO", "px": 80, "y": 820, "at": "@calcula-0.2", "color": "blue", "rot": -8},
         ]},
        {"voz": ["Habla de falta de control… y de más problemas de salud mental."], "trans": "tinta", "cam": "deriva",
         "el": [
             {"k": "icono", "n": "lupa", "x": 300, "y": 560, "tam": 1.2, "at": "@control-0.2", "flota": True},
             {"k": "txt", "t": "FALTA DE\nCONTROL", "px": 70, "x": 300, "y": 830, "at": "@control", "marca": "yellow"},
             {"k": "icono", "n": "cerebro", "x": 790, "y": 560, "tam": 1.2, "at": "@salud-0.3", "flota": True},
             {"k": "txt", "t": "SALUD\nMENTAL", "px": 70, "x": 790, "y": 830, "at": "@salud", "marca": "pink"},
         ]},
        {"voz": ["¿Quién debería revisar tu baja?", "¿Tu médico, tu empresa… o la Seguridad Social?"], "trans": "zoom", "cam": "empuja",
         "el": [
             {"k": "txt", "t": "¿QUIÉN REVISA TU BAJA?", "px": 72, "y": 400, "at": 0.05, "marca": "yellow"},
             {"k": "txt", "t": "1 · TU MÉDICO", "px": 80, "y": 600, "at": "@médico", "color": "teal"},
             {"k": "txt", "t": "2 · TU EMPRESA", "px": 80, "y": 760, "at": "@empresa", "color": "red"},
             {"k": "txt", "t": "3 · LA SEG. SOCIAL", "px": 80, "y": 920, "at": "@Seguridad", "color": "blue"},
             {"k": "txt", "t": "COMENTA 1, 2 O 3 ↓", "px": 54, "y": 1090, "at": "fin-1.0"},
         ]},
    ],
}
