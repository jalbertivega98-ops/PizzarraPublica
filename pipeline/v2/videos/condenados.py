"""Los datos que incomodan #8 · Condenados extranjeros y españoles.

Cifras (consultadas el 13/10/2026):
- INE, Estadística de la Población Condenada 2025 (nota de prensa 14/07/2026): 306.237 adultos condenados (−0,2 %);
  7,4 por 1.000 habitantes de 18 y más años; 15,3 por mil extranjeros y 6,1 por mil españoles (2,5 veces);
  70,2 % de los condenados con nacionalidad española; 80 % hombres; delitos más frecuentes: seguridad vial (22,4 %),
  lesiones (17,3 %) y hurtos (16,4 %).
- Sánchez Barricarte, REIS 195 (CIS, 2026), 2007-2023: ratio bruto 2,7; estandarizado por edad y sexo 1,9
  (la brecha se reduce un 48 %). Ya usado en di04.
"""
VIDEO = {
    "slug": "di08_condenados",
    "titulo": "2,5 veces más condenados.",
    "serie": "LOS DATOS QUE INCOMODAN · #8",
    "acento": "red",
    "voz": "elevenlabs:Pizarra Pública",
    "claves": ["2,5", "15,3", "6,1", "siete", "70,2", "1,9", "mitad", "irregular", "integración", "control"],
    "musica": {"bpm": 124, "tono": -3, "seed": 88},
    "portada": {"t": 1.2, "titulo": "2,5 VECES MÁS\nCONDENADOS"},
    "duro": True,
    "planos": [
        # GANCHO
        {"voz": [{"tts": "Dos coma cinco veces. Es lo que dice el INE de los condenados extranjeros.",
                  "text": "2,5 veces. Es lo que dice el INE de los condenados extranjeros."}],
         "cam": "golpe", "fuente": "INE, Población condenada 2025",
         "el": [
             {"k": "num", "val": 2.5, "desde": 0, "dur": 0.6, "golpe": True, "px": 240, "y": 620, "pre": "×", "dec": 1,
              "color": "red", "fondo": "yellow", "at": 0},
             {"k": "icono", "n": "mazo", "x": 300, "y": 1020, "tam": 1.1, "rot": -12, "at": "@INE"},
             {"k": "icono", "n": "pasaporte", "x": 780, "y": 1020, "tam": 1.0, "rot": 8, "at": "@extranjeros"},
         ]},
        {"voz": [{"tts": "En dos mil veinticinco condenaron a más de trescientos seis mil adultos en España.",
                  "text": "En 2025 condenaron a más de 306.000 adultos en España."}],
         "trans": "flash", "cam": "empuja", "fuente": "INE, Población condenada 2025",
         "el": [
             {"k": "num", "val": 306237, "desde": 0, "dur": 1.2, "golpe": True, "px": 180, "y": 640, "at": 0.3,
              "sub": "adultos condenados"},
             {"k": "pers", "tipo": "juez", "x": 540, "y": 1060, "tam": 1.0, "cara": "listo", "pose": "señala", "at": "@condenaron"},
         ]},
        # DATOS
        {"voz": [{"tts": "Por cada mil habitantes: seis coma uno españoles… y quince coma tres extranjeros.",
                  "text": "Por cada 1.000 habitantes: 6,1 españoles… y 15,3 extranjeros."}],
         "trans": "barrido", "cam": "aleja", "fuente": "INE, tasa por 1.000 habitantes de 18+ años",
         "el": [
             {"k": "barras", "y": 1060, "w": 700, "h": 580, "max": 17, "escalon": 1.6,
              "items": [{"label": "ESPAÑOLES", "val": 6.1, "color": "blue", "txt": "{v}", "dec": 1},
                        {"label": "EXTRANJEROS", "val": 15.3, "color": "red", "txt": "{v}", "dec": 1}]},
             {"k": "txt", "t": "POR CADA 1.000", "px": 60, "y": 380, "at": 0.1, "marca": "yellow"},
         ]},
        # GIRO 1
        {"voz": ["Pero ojo: siete de cada diez condenados son españoles."], "trans": "flash", "cam": "golpe", "pausa": 0.4,
         "fuente": "INE: 70,2 % de nacionalidad española",
         "el": [
             {"k": "gente", "n": 10, "cols": 5, "sep": 170, "y": 640, "destacar": [0, 1, 2, 3, 4, 5, 6], "apagar": "@siete",
              "color": "light", "color_dest": "blue"},
             {"k": "num", "val": 70.2, "desde": 0, "dur": 0.7, "golpe": True, "px": 170, "y": 1030, "suf": " %", "dec": 1,
              "color": "blue", "at": "@siete+0.3"},
         ]},
        {"voz": ["Hay más condenados españoles. Pero, en proporción, los extranjeros salen más."], "trans": "zoom", "cam": "deriva",
         "el": [
             {"k": "txt", "t": "EN NÚMERO: ESPAÑOLES", "px": 64, "y": 440, "at": "@condenados", "color": "blue"},
             {"k": "txt", "t": "EN PROPORCIÓN: EXTRANJEROS", "px": 56, "y": 600, "at": "@proporción", "color": "red"},
             {"k": "pers", "tipo": "ciudadano", "x": 300, "y": 1000, "tam": 1.0, "cara": "duda", "at": "@condenados"},
             {"k": "pers", "tipo": "viajero", "x": 780, "y": 1000, "tam": 1.0, "cara": "sorpresa", "mira": -1, "at": "@extranjeros"},
         ]},
        # POR QUÉ
        {"voz": ["¿Por qué? Primero: edad y sexo."], "trans": "tinta", "cam": "golpe", "min": 1.4,
         "el": [
             {"k": "icono", "n": "interrogacion", "x": 540, "y": 560, "tam": 1.4, "at": 0.05},
             {"k": "txt", "t": "1 · EDAD Y SEXO", "px": 84, "y": 900, "at": "@edad", "marca": "yellow"},
         ]},
        {"voz": ["Ocho de cada diez condenados son hombres. Y la población extranjera es más joven y más masculina."],
         "trans": "barrido", "cam": "empuja", "fuente": "INE: 80 % de los condenados son hombres",
         "el": [
             {"k": "gente", "n": 10, "cols": 5, "sep": 170, "y": 560, "destacar": [0, 1, 2, 3, 4, 5, 6, 7], "apagar": "@hombres",
              "color": "light", "color_dest": "teal"},
             {"k": "pers", "tipo": "joven", "x": 300, "y": 1080, "tam": 0.9, "cara": "neutral", "at": "@joven"},
             {"k": "txt", "t": "+ JÓVENES\n+ HOMBRES", "px": 70, "y": 1060, "x": 760, "at": "@masculina", "color": "red"},
         ]},
        {"voz": [{"tts": "Comparando a igual edad y sexo, la diferencia baja de dos coma siete a uno coma nueve.",
                  "text": "Comparando a igual edad y sexo, la diferencia baja de 2,7 a 1,9."}],
         "trans": "zoom", "cam": "empuja", "fuente": "Sánchez Barricarte, REIS (CIS) 2026, datos 2007-2023",
         "el": [
             {"k": "num", "val": 2.7, "desde": 2.7, "dur": 0, "px": 200, "y": 560, "pre": "×", "dec": 1, "color": "gray", "at": 0,
              "hasta": "@1,9-0.3"},
             {"k": "num", "val": 1.9, "desde": 2.7, "dur": 0.8, "golpe": True, "px": 240, "y": 620, "pre": "×", "dec": 1,
              "color": "red", "fondo": "yellow", "at": "@1,9-0.3"},
             {"k": "txt", "t": "A IGUAL EDAD Y SEXO", "px": 64, "y": 920, "at": "@igual", "marca": "yellow"},
         ]},
        {"voz": ["La brecha existe. Pero casi la mitad se explica por eso."], "trans": "corte", "cam": "golpe",
         "fuente": "REIS (CIS) 2026: la brecha baja un 48 %",
         "el": [
             {"k": "txt", "t": "EXISTE", "px": 100, "y": 460, "at": 0.05, "color": "ink"},
             {"k": "num", "val": 48, "desde": 0, "dur": 0.7, "golpe": True, "px": 200, "y": 820, "suf": " %", "color": "red",
              "at": "@mitad-0.2"},
             {"k": "txt", "t": "ES EDAD Y SEXO", "px": 72, "y": 1010, "at": "@eso", "marca": "yellow"},
         ]},
        # GIRO 2
        {"voz": ["Segundo: extranjero no significa irregular."], "trans": "flash", "cam": "golpe", "pausa": 0.3,
         "el": [
             {"k": "txt", "t": "2 · EXTRANJERO", "px": 84, "y": 480, "at": 0.05, "marca": "yellow"},
             {"k": "sello", "t": "≠ IRREGULAR", "x": 540, "y": 800, "px": 96, "at": "@irregular", "rot": -10},
         ]},
        {"voz": ["Un alemán, un residente legal o un turista también cuentan como extranjeros."],
         "trans": "barrido", "cam": "deriva", "fuente": "INE: solo distingue nacionalidad española o extranjera",
         "el": [
             {"k": "icono", "n": "bandera_ue", "x": 220, "y": 720, "tam": 1.0, "at": "@alemán"},
             {"k": "icono", "n": "documento", "x": 540, "y": 720, "tam": 1.0, "at": "@legal"},
             {"k": "icono", "n": "maleta", "x": 860, "y": 720, "tam": 1.0, "at": "@turista"},
             {"k": "txt", "t": "TODOS «EXTRANJEROS»", "px": 66, "y": 1010, "at": "@cuentan", "color": "red"},
         ]},
        {"voz": ["¿Y qué delitos? Sobre todo seguridad vial, lesiones y hurtos."],
         "trans": "sube", "cam": "empuja", "fuente": "INE, Población condenada 2025",
         "el": [
             {"k": "txt", "t": "TRÁFICO 22,4 %", "px": 70, "y": 520, "at": "@vial", "marca": "yellow"},
             {"k": "txt", "t": "LESIONES 17,3 %", "px": 70, "y": 740, "at": "@lesiones", "marca": "yellow"},
             {"k": "txt", "t": "HURTOS 16,4 %", "px": 70, "y": 960, "at": "@hurtos", "marca": "yellow"},
         ]},
        # PREGUNTA
        {"voz": ["¿Qué debería hacer España para bajar estas cifras? A: más integración y empleo. B: más control y expulsiones.",
                 "Comenta A o B."], "trans": "zoom", "cam": "quieta", "min": 0, "cola": 1.8,
         "el": [
             {"k": "encuesta", "pregunta": "¿QUÉ DEBERÍA\nHACER ESPAÑA?", "a": "INTEGRACIÓN", "b": "CONTROL", "color_a": "green",
              "color_b": "red", "at": 0.05, "at_a": "@integración", "at_b": "@control", "at_c": "L1"},
         ]},
    ],
}
