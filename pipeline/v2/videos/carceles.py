"""Los datos que incomodan #4 · Cárceles, delitos, reincidentes y extranjeros.

Cifras (consultadas el 12/10/2026):
- Consejo de Europa, SPACE I 2025 (población a 31/01/2025, publicado 19/05/2026): España 59.279 presos; estancia media
  ≈ 20 meses frente a 8,8 de media europea; extranjeros 29 % (Administración del Estado) y 52 % (Cataluña), 17 % en Europa.
- InDret 1/2026 «El reciente incremento del encarcelamiento en España»: 61.175 presos en 2025 (124 por 100.000);
  la libertad condicional cae un 79 % entre 2014 y 2025.
- LO 1/2026 de multirreincidencia (BOE 09/04/2026, en vigor el 10/04/2026): hurto < 400 € = multa de 1 a 3 meses;
  con 3 condenas previas de la misma naturaleza, prisión de 6 a 18 meses.
- Ministerio del Interior, Balance de Criminalidad 2025: España 2.474.156 infracciones (+0,8 %), cibercriminalidad 489.248 (+5,3 %).
  Barcelona ciudad: 169.678 (−3,6 %), hurtos 76.713, robos con violencia 12.643 (+1,1 %), delitos sexuales 1.336 (+5 %).
  En 2016 Barcelona registró 169.984 (Junta Local de Seguridad). Madrid ciudad: −2,4 %, homicidios consumados de 10 a 17,
  delitos contra la libertad sexual de 1.751 a 1.850 (Delegación del Gobierno, 20/02/2026).
- INE, Estadística de la Población Condenada 2025: 306.237 adultos condenados; 6,1 por mil españoles y 15,3 por mil extranjeros (2,5 veces).
- Sánchez Barricarte, REIS 195 (CIS, 2026), 2007-2023: ratio bruto 2,7; estandarizado por edad y sexo 1,9 (la brecha se reduce un 48 %);
  por origen, de 0,6 (Asia y Pacífico) a 8,9 (Balcanes y Georgia).
- CEJFE (Generalitat), Tasa de reincidencia penitenciaria 2020: 21,2 % (40,3 % en 2008); españoles 20,4 %, extranjeros 22,2 %.
- Mossos d'Esquadra, primer semestre 2026: 2.190 delincuentes persistentes de alto riesgo identificados en Barcelona.
"""
VIDEO = {
    "slug": "di04_carceles",
    "titulo": "Cárceles llenas. Calles igual.",
    "serie": "LOS DATOS QUE INCOMODAN · #4",
    "acento": "orange",
    "claves": ["veinte", "nueve", "multa", "cárcel", "homicidios", "incómodo", "mitad", "igual", "siempre", "vuelvan"],
    "musica": {"bpm": 112, "tono": -2, "seed": 44},
    "portada": {"t": 1.2, "titulo": "20 MESES DE CÁRCEL.\n¿Y LOS DE SIEMPRE?"},
    "planos": [
        # GANCHO
        {"voz": [{"tts": "Veinte meses.", "text": "20 meses."}],
         "cam": "golpe", "fuente": "Consejo de Europa, SPACE I 2025", "min": 1.4,
         "el": [
             {"k": "icono", "n": "rejas", "x": 540, "y": 980, "tam": 1.8, "at": 0},
             {"k": "num", "val": 20, "desde": 0, "dur": 0.5, "golpe": True, "px": 170, "y": 560, "fondo": "yellow", "at": 0, "suf": " meses"},
         ]},
        {"voz": ["Lo que pasa de media un preso en una cárcel española."], "trans": "zoom", "cam": "empuja",
         "el": [
             {"k": "pers", "tipo": "preso", "x": 330, "y": 860, "tam": 1.5, "cara": "triste", "pose": "cabeza"},
             {"k": "icono", "n": "calendario", "x": 790, "y": 560, "tam": 1.3, "at": "@media", "rot": 8},
             {"k": "icono", "n": "rejas", "x": 790, "y": 950, "tam": 1.1, "at": "@cárcel"},
         ]},
        {"voz": [{"tts": "En Europa, menos de nueve.", "text": "En Europa, menos de 9."}], "trans": "barrido", "cam": "aleja",
         "fuente": "Consejo de Europa, SPACE I 2025",
         "el": [
             {"k": "barras", "y": 1050, "w": 700, "h": 560, "max": 22, "escalon": 0.5,
              "items": [{"label": "ESPAÑA", "val": 20, "color": "orange", "txt": "{v} meses"},
                        {"label": "EUROPA", "val": 8.8, "color": "blue", "txt": "{v} meses", "dec": 1}]},
         ]},
        {"voz": ["Y aun así, en la calle, siempre los mismos."], "trans": "tinta", "cam": "deriva",
         "el": [
             {"k": "pers", "tipo": "ciudadana", "x": 290, "y": 880, "tam": 1.3, "cara": "enfado", "pose": "jarras"},
             {"k": "pers", "tipo": "joven", "x": 790, "y": 880, "tam": 1.3, "cara": "listo", "pose": "normal", "mira": -1, "at": "@calle",
              "sostiene": None},
             {"k": "bocadillo", "t": "¿Otra vez\ntú?", "x": 300, "y": 480, "px": 64, "cola": [-10, 170], "at": "@mismos"},
         ]},
        # PROBLEMA
        {"voz": [{"tts": "¿Por qué? Un hurto de menos de cuatrocientos euros es un delito leve.", "text": "¿Por qué? Un hurto de menos de 400 € es un delito leve."}],
         "trans": "flash", "cam": "golpe", "fuente": "Código Penal, art. 234",
         "el": [
             {"k": "icono", "n": "movil", "x": 260, "y": 560, "tam": 1.1, "rot": -10, "at": "@hurto"},
             {"k": "icono", "n": "cartera", "x": 820, "y": 560, "tam": 1.0, "rot": 8, "at": "@hurto+0.2"},
             {"k": "num", "val": 400, "desde": 0, "dur": 0.6, "px": 190, "y": 860, "pre": "< ", "suf": " €", "at": "@400", "color": "red"},
             {"k": "sello", "t": "DELITO LEVE", "x": 540, "y": 1080, "px": 72, "at": "@leve", "rot": -8},
         ]},
        {"voz": ["Una multa. Te pillan, a casa… y vuelta a empezar."], "trans": "barrido", "cam": "empuja",
         "el": [
             {"k": "icono", "n": "billete", "x": 540, "y": 420, "tam": 1.1, "at": "@multa"},
             {"k": "pers", "tipo": "policia", "x": 290, "y": 900, "tam": 1.25, "cara": "listo", "pose": "señala", "at": "@pillan-0.2"},
             {"k": "icono", "n": "esposas", "x": 560, "y": 700, "tam": 0.9, "at": "@pillan"},
             {"k": "pers", "tipo": "joven", "x": 800, "y": 900, "tam": 1.25, "cara": "neutral", "mira": -1, "at": "@casa",
              "cambios": [["@empezar", {"cara": "listo", "pose": "saluda"}]]},
             {"k": "flecha", "de": [820, 640], "a": [620, 560], "at": "@vuelta", "color": "red"},
         ]},
        {"voz": [{"tts": "Desde abril, con tres condenas previas, ya es cárcel: de seis a dieciocho meses.",
                  "text": "Desde abril, con 3 condenas previas, ya es cárcel: de 6 a 18 meses."}],
         "trans": "zoom", "cam": "empuja", "fuente": "Ley Orgánica 1/2026, BOE 09/04/2026",
         "el": [
             {"k": "txt", "t": "LEY DE\nMULTIRREINCIDENCIA", "px": 76, "y": 400, "at": 0.1, "marca": "yellow"},
             {"k": "burbujas", "y": 680, "items": ["1ª", "2ª", "3ª"], "px": 80, "at": "@3", "escalon": 0.2},
             {"k": "icono", "n": "mazo", "x": 270, "y": 980, "tam": 1.1, "at": "@cárcel", "rot": -10},
             {"k": "txt", "t": "6-18 MESES\nDE PRISIÓN", "px": 84, "y": 990, "x": 680, "at": "@6", "color": "red"},
         ]},
        # DATOS: CIUDADES
        {"voz": [{"tts": "Barcelona: ciento sesenta y nueve mil delitos en un año.", "text": "Barcelona: 169.678 delitos en un año."}],
         "trans": "barrido", "cam": "golpe", "fuente": "Ministerio del Interior, 2025",
         "el": [
             {"k": "txt", "t": "BARCELONA", "px": 110, "y": 400, "at": 0, "color": "ink"},
             {"k": "num", "val": 169678, "desde": 0, "dur": 1.2, "golpe": True, "px": 190, "y": 700, "at": 0.15, "sub": "delitos en 2025"},
             {"k": "icono", "n": "edificio", "x": 540, "y": 1060, "tam": 1.1, "at": "@delitos"},
         ]},
        {"voz": ["Casi la mitad, hurtos."],
         "trans": "sube", "cam": "empuja", "fuente": "Ministerio del Interior, 2025",
         "el": [
             {"k": "gente", "n": 10, "cols": 5, "sep": 170, "y": 640, "destacar": [0, 1, 2, 3, 4], "apagar": "@hurtos", "color": "light",
              "color_dest": "orange"},
             {"k": "icono", "n": "movil", "x": 300, "y": 1030, "tam": 0.8, "rot": -14, "at": "@hurtos"},
             {"k": "num", "val": 76713, "desde": 0, "dur": 0.9, "px": 140, "y": 1060, "x": 640, "at": "@hurtos+0.2", "color": "orange"},
         ]},
        {"voz": [{"tts": "¿Más que nunca? No: la misma cifra que en dos mil dieciséis.", "text": "¿Más que nunca? No: la misma cifra que en 2016."}],
         "trans": "flash", "cam": "aleja", "pausa": 0.35, "fuente": "Junta Local de Seguridad de Barcelona",
         "el": [
             {"k": "barras", "y": 1050, "w": 700, "h": 520, "max": 190000, "escalon": 0.5, "px_val": 60,
              "items": [{"label": "2016", "val": 169984, "color": "gray", "txt": "{v}"},
                        {"label": "2025", "val": 169678, "color": "orange", "txt": "{v}"}]},
             {"k": "sello", "t": "=", "x": 540, "y": 420, "px": 120, "at": "@misma", "rot": 0},
         ]},
        {"voz": ["Pero algunos delitos graves sí suben."], "trans": "corte", "cam": "golpe",
         "el": [
             {"k": "estallido", "r": 330, "y": 700, "color": "red", "at": "@graves-0.2"},
             {"k": "txt", "t": "LOS GRAVES\nSUBEN", "px": 78, "y": 700, "at": "@graves-0.1", "color": "white"},
         ]},
        {"voz": [{"tts": "En Madrid, los delitos bajan… pero los homicidios pasan de diez a diecisiete.",
                  "text": "En Madrid, los delitos bajan… pero los homicidios pasan de 10 a 17."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Delegación del Gobierno en Madrid, 2025",
         "el": [
             {"k": "txt", "t": "MADRID", "px": 110, "y": 380, "at": 0},
             {"k": "icono", "n": "edificio", "x": 540, "y": 1060, "tam": 1.0, "at": 0.1, "hasta": "@homicidios"},
             {"k": "txt", "t": "DELITOS −2,4 %", "px": 70, "y": 540, "at": "@bajan", "color": "green"},
             {"k": "txt", "t": "HOMICIDIOS", "px": 80, "y": 760, "at": "@homicidios", "color": "red"},
             {"k": "num", "val": 17, "desde": 10, "dur": 0.8, "golpe": True, "px": 230, "y": 1080, "at": "@17-0.3", "color": "red"},
         ]},
        {"voz": [{"tts": "Y los delitos sexuales suben en las dos ciudades.", "text": "Y los delitos sexuales suben en las dos ciudades."}],
         "trans": "sube", "cam": "deriva", "fuente": "Interior y Delegación del Gobierno, 2025",
         "el": [
             {"k": "txt", "t": "BARCELONA  +5 %", "px": 76, "y": 560, "at": "@sexuales", "marca": "yellow"},
             {"k": "txt", "t": "MADRID  +5,7 %", "px": 76, "y": 760, "at": "@dos", "marca": "yellow"},
             {"k": "icono", "n": "grafica", "x": 540, "y": 1030, "tam": 1.0, "color": "red", "at": "@suben"},
         ]},
        # LO INCÓMODO
        {"voz": ["Ahora, lo incómodo."], "trans": "tinta", "cam": "golpe", "pausa": 0.5, "min": 1.3,
         "el": [
             {"k": "txt", "t": "LO\nINCÓMODO", "px": 150, "y": 700, "at": 0.05, "color": "red"},
         ]},
        {"voz": [{"tts": "Por cada mil adultos, condenan a seis españoles… y a quince extranjeros.",
                  "text": "Por cada 1.000 adultos, condenan a 6 españoles… y a 15 extranjeros."}],
         "trans": "barrido", "cam": "aleja", "fuente": "INE, Población condenada 2025",
         "el": [
             {"k": "barras", "y": 1050, "w": 700, "h": 560, "max": 17, "escalon": 1.4,
              "items": [{"label": "ESPAÑOLES", "val": 6.1, "color": "blue", "txt": "{v}", "dec": 1},
                        {"label": "EXTRANJEROS", "val": 15.3, "color": "orange", "txt": "{v}", "dec": 1}]},
             {"k": "sello", "t": "×2,5", "x": 540, "y": 400, "px": 100, "at": "fin-0.5", "rot": -10},
         ]},
        {"voz": [{"tts": "En prisión, tres de cada diez son extranjeros. En Cataluña, más de la mitad.",
                  "text": "En prisión, 3 de cada 10 son extranjeros. En Cataluña, más de la mitad."}],
         "trans": "zoom", "cam": "empuja", "fuente": "Consejo de Europa, SPACE I 2025",
         "el": [
             {"k": "gente", "n": 10, "cols": 5, "sep": 170, "y": 620, "destacar": [0, 1, 2], "apagar": "@extranjeros", "color": "blue",
              "color_dest": "orange"},
             {"k": "txt", "t": "ESPAÑA 29 %", "px": 80, "y": 950, "at": "@extranjeros", "color": "orange"},
             {"k": "txt", "t": "CATALUÑA 52 %", "px": 92, "y": 1090, "at": "@Cataluña", "marca": "yellow"},
         ]},
        # GIRO
        {"voz": [{"tts": "Pero son más jóvenes y más hombres: el perfil que más delinque.",
                  "text": "Pero son más jóvenes y más hombres: el perfil que más delinque."}],
         "trans": "flash", "cam": "deriva",
         "el": [
             {"k": "pers", "tipo": "joven", "x": 300, "y": 860, "tam": 1.4, "cara": "neutral", "at": "@jóvenes"},
             {"k": "pers", "tipo": "ciudadano", "x": 780, "y": 860, "tam": 1.4, "cara": "neutral", "mira": -1, "at": "@hombres"},
             {"k": "txt", "t": "18-30 AÑOS · HOMBRES", "px": 64, "y": 420, "at": "@perfil", "marca": "yellow"},
         ]},
        {"voz": [{"tts": "A igual edad y sexo, la diferencia baja a uno coma nueve.",
                  "text": "A igual edad y sexo, la diferencia baja a 1,9."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Sánchez Barricarte, REIS (CIS) 2026",
         "el": [
             {"k": "num", "val": 2.7, "desde": 2.7, "dur": 0, "px": 200, "y": 560, "pre": "×", "dec": 1, "color": "gray", "at": 0, "hasta": "@baja"},
             {"k": "num", "val": 1.9, "desde": 2.7, "dur": 0.8, "golpe": True, "px": 240, "y": 620, "pre": "×", "dec": 1, "color": "orange",
              "at": "@baja", "fondo": "yellow"},
             {"k": "txt", "t": "A IGUAL EDAD Y SEXO", "px": 64, "y": 900, "at": "@igual", "marca": "yellow"},
         ]},
        {"voz": ["Existe. Pero casi la mitad es edad y sexo."], "trans": "corte", "cam": "golpe",
         "fuente": "REIS (CIS) 2026: la brecha baja un 48 %",
         "el": [
             {"k": "txt", "t": "EXISTE", "px": 92, "y": 460, "at": 0.05, "color": "ink"},
             {"k": "num", "val": 48, "desde": 0, "dur": 0.7, "px": 200, "y": 830, "suf": " %", "at": "@mitad-0.2", "color": "orange", "golpe": True},
             {"k": "txt", "t": "ES EDAD Y SEXO", "px": 72, "y": 1020, "at": "@edad", "marca": "yellow"},
         ]},
        {"voz": [{"tts": "Y según el origen, va de cero coma seis en asiáticos a casi nueve en Balcanes y Georgia.",
                  "text": "Y según el origen, va de 0,6 en asiáticos a casi 9 en Balcanes y Georgia."}],
         "trans": "sube", "cam": "aleja", "fuente": "REIS (CIS) 2026, datos 2007-2023",
         "el": [
             {"k": "barras", "y": 1060, "w": 760, "h": 560, "max": 9.5, "escalon": 0.9, "px_label": 38,
              "items": [{"label": "ASIA", "val": 0.6, "color": "green", "txt": "×{v}", "dec": 1},
                        {"label": "UE OESTE", "val": 1.3, "color": "blue", "txt": "×{v}", "dec": 1},
                        {"label": "LATAM", "val": 2.5, "color": "purple", "txt": "×{v}", "dec": 1},
                        {"label": "BALCANES", "val": 8.9, "color": "red", "txt": "×{v}", "dec": 1}]},
         ]},
        # REINCIDENCIA
        {"voz": ["¿Reincidentes? En Cataluña, uno de cada cinco presos vuelve a prisión."],
         "trans": "barrido", "cam": "empuja", "fuente": "CEJFE, Generalitat, 2020",
         "el": [
             {"k": "gente", "n": 5, "cols": 5, "sep": 180, "y": 640, "destacar": [0], "apagar": "@vuelve", "color": "teal", "color_dest": "red"},
             {"k": "txt", "t": "21 % VUELVE", "px": 96, "y": 940, "at": "@vuelve", "marca": "yellow"},
             {"k": "icono", "n": "rejas", "x": 540, "y": 380, "tam": 0.7, "at": "@prisión"},
         ]},
        {"voz": [{"tts": "En dos mil ocho, eran cuatro de cada diez.", "text": "En 2008, eran 4 de cada 10."}],
         "trans": "zoom", "cam": "aleja", "fuente": "CEJFE, tasa de reincidencia 2008-2020",
         "el": [
             {"k": "linea", "y": 1000, "w": 660, "h": 460, "ymax": 45, "at": 0.1, "dur": 1.8, "color": "red",
              "datos": [[2008, 40.3], [2014, 30.2], [2020, 21.2]], "etiquetas": {"2008": "40 %", "2020": "21 %"}},
         ]},
        {"voz": [{"tts": "Lo que nadie cuenta: españoles, veinte por ciento. Extranjeros, veintidós.",
                  "text": "Lo que nadie cuenta: españoles, 20 %. Extranjeros, 22 %."}],
         "trans": "flash", "cam": "golpe", "pausa": 0.45, "fuente": "CEJFE, Generalitat, 2020",
         "el": [
             {"k": "medidor", "y": 560, "val": 20.4, "max": 40, "dur": 0.9, "etiqueta": "ESPAÑOLES", "txt": "20 %", "color": "blue",
              "at": "@españoles"},
             {"k": "medidor", "y": 900, "val": 22.2, "max": 40, "dur": 0.9, "etiqueta": "EXTRANJEROS", "txt": "22 %", "color": "orange",
              "at": "@Extranjeros"},
             {"k": "sello", "t": "CASI IGUAL", "x": 540, "y": 1120, "px": 76, "at": "fin-0.4", "rot": -8},
         ]},
        {"voz": [{"tts": "El problema: unos pocos que caen una y otra vez. En Barcelona, dos mil ciento noventa de alto riesgo en seis meses.",
                  "text": "El problema: unos pocos que caen una y otra vez. En Barcelona, 2.190 de alto riesgo en 6 meses."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Mossos d'Esquadra, 1er semestre 2026",
         "el": [
             {"k": "pers", "tipo": "joven", "x": 300, "y": 900, "tam": 1.3, "cara": "listo", "pose": "jarras", "at": "@pocos-0.3"},
             {"k": "burbujas", "y": 480, "items": ["1", "2", "3", "4", "5", "…"], "px": 66, "at": "@otra", "escalon": 0.15},
             {"k": "num", "val": 2190, "desde": 0, "dur": 0.9, "golpe": True, "px": 140, "y": 930, "x": 730, "at": "@2.190-0.1", "color": "red",
              "sub": "alto riesgo"},
         ]},
        # PREGUNTA FINAL
        {"voz": ["¿Más cárcel para los de siempre… o más medios para que no vuelvan?"],
         "trans": "zoom", "cam": "empuja", "min": 0,
         "el": [
             {"k": "estallido", "r": 330, "y": 700, "color": "yellow", "at": 0},
                          {"k": "txt", "t": "¿MÁS CÁRCEL", "px": 100, "y": 620, "at": "@cárcel", "color": "red"},
             {"k": "txt", "t": "O MÁS MEDIOS?", "px": 100, "y": 780, "at": "@medios", "color": "blue"},
             {"k": "txt", "t": "TE LEO EN COMENTARIOS", "px": 50, "y": 1080, "at": "fin-1.2", "fuente": "num"},
         ]},
    ],
}
