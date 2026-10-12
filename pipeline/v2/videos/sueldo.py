"""Los datos que incomodan #5 · Lo que cuesta tu sueldo y no ves.

Ejemplo propio (2026, soltero sin hijos, 12 pagas, contrato indefinido, régimen general):
- Neto 1.500 €/mes = 18.000 €/año  ⇐  bruto ≈ 22.300 €/año.
- Trabajador: cotiza 6,50 % (contingencias comunes 4,70 + desempleo 1,55 + FP 0,10 + MEI 0,15) = 1.450 €; IRPF ≈ 2.847 €
  (reducción por rendimientos del trabajo, mínimo personal 5.550 €, escala estatal + autonómica general).
- Empresa: cotiza ≈ 32,15 % (CC 23,60 + desempleo 5,50 + FOGASA 0,20 + FP 0,60 + MEI 0,75 + AT/EP ≈ 1,50) = 7.169 €.
- Coste total ≈ 29.469 €/año (2.456 €/mes). Estado: 11.466 € (38,9 %). Tipos: Orden de cotización 2026 (BOE); IRPF: Ley 35/2006.
- OCDE, Taxing Wages 2026 (datos 2025, soltero con salario medio): cuña fiscal España 41,4 %, media OCDE 35,1 %;
  la más alta en España desde 2000 (inicio de la serie); España, décima de la OCDE.
"""
VIDEO = {
    "slug": "di05_sueldo",
    "titulo": "Cobras 1.500. Cuestas 2.456.",
    "serie": "LOS DATOS QUE INCOMODAN · #5",
    "acento": "green",
    "voz": "elevenlabs:Pizarra Pública",
    "claves": ["2.456", "955", "39", "invisible", "41,4", "nómina"],
    "musica": {"bpm": 116, "tono": 2, "seed": 55},
    "portada": {"t": 1.3, "titulo": "COBRAS 1.500 €.\nTU EMPRESA PAGA 2.456 €."},
    "planos": [
        # GANCHO
        {"voz": [{"tts": "Cobras mil quinientos euros al mes.", "text": "Cobras 1.500 € al mes."}],
         "cam": "golpe", "min": 1.6, "fuente": "Ejemplo 2026: soltero, 12 pagas",
         "el": [
             {"k": "num", "val": 1500, "desde": 0, "dur": 0.7, "golpe": True, "px": 230, "y": 600, "suf": " €", "fondo": "yellow", "at": 0},
             {"k": "txt", "t": "LO QUE TE LLEGA", "px": 64, "y": 830, "at": "@1.500", "fuente": "num"},
             {"k": "pers", "tipo": "trabajador", "x": 540, "y": 1110, "tam": 0.95, "cara": "feliz", "pose": "brazos_arriba", "at": 0.2},
         ]},
        {"voz": [{"tts": "Tu empresa paga por ti dos mil cuatrocientos cincuenta y seis.", "text": "Tu empresa paga por ti 2.456."}],
         "trans": "flash", "cam": "golpe",
         "el": [
             {"k": "num", "val": 2456, "desde": 1500, "dur": 0.9, "golpe": True, "px": 190, "y": 640, "suf": " €", "color": "red", "fondo": "estallido",
              "at": "@paga"},
             {"k": "pers", "tipo": "jefa", "x": 540, "y": 1100, "tam": 0.95, "cara": "nervioso", "pose": "encoge", "at": "@empresa"},
         ]},
        {"voz": [{"tts": "¿Dónde están los novecientos cincuenta y cinco que faltan?", "text": "¿Dónde están los 955 que faltan?"}],
         "trans": "zoom", "cam": "empuja", "pausa": 0.3,
         "el": [
             {"k": "num", "val": 955, "desde": 0, "dur": 0.6, "px": 230, "y": 620, "suf": " €", "at": "@955-0.2", "color": "ink"},
             {"k": "icono", "n": "lupa", "x": 760, "y": 980, "tam": 1.4, "at": "@Dónde", "flota": True},
             {"k": "icono", "n": "interrogacion", "x": 300, "y": 980, "tam": 1.6, "at": "@faltan"},
         ]},
        # PROBLEMA
        {"voz": ["Antes de que lo veas, la empresa ingresa un tercio más en cotizaciones a la Seguridad Social."],
         "trans": "barrido", "cam": "empuja", "fuente": "Orden de cotización 2026",
         "el": [
             {"k": "pers", "tipo": "jefa", "x": 260, "y": 980, "tam": 1.0, "cara": "neutral", "pose": "sostiene", "at": 0.05},
             {"k": "pers", "tipo": "hucha", "x": 740, "y": 980, "tam": 0.9, "cara": "feliz", "at": "@empresa"},
             {"k": "dinero", "modo": "fuga", "desde": [300, 900], "hacia": [740, 960], "n": 12, "at": "@ingresa", "dur": 1.3},
             {"k": "txt", "t": "+32 %", "px": 160, "y": 470, "at": "@tercio", "color": "red"},
             {"k": "txt", "t": "LO PAGA LA EMPRESA", "px": 56, "y": 620, "at": "@tercio+0.2", "fuente": "num"},
         ]},
        {"voz": ["De tu bruto te quitan otro 6,5 %… y luego el IRPF."],
         "trans": "sube", "cam": "deriva",
         "el": [
             {"k": "icono", "n": "documento", "x": 300, "y": 800, "tam": 1.6, "at": 0.05, "rot": -6},
             {"k": "txt", "t": "NÓMINA", "px": 64, "y": 520, "x": 300, "at": 0.1, "fuente": "num"},
             {"k": "txt", "t": "−6,5 %", "px": 100, "y": 640, "x": 740, "at": "@6,5", "color": "red"},
             {"k": "txt", "t": "−IRPF", "px": 100, "y": 900, "x": 740, "at": "@IRPF", "color": "red"},
         ]},
        # DATOS
        {"voz": [{"tts": "Al año, tu trabajo cuesta casi veintinueve mil quinientos euros. A ti te llegan dieciocho mil.",
                  "text": "Al año, tu trabajo cuesta 29.469 €. A ti te llegan 18.000."}],
         "trans": "zoom", "cam": "aleja", "fuente": "Cálculo propio: Orden de cotización 2026 + IRPF",
         "el": [
             {"k": "barras", "y": 1060, "w": 700, "h": 560, "max": 31000, "escalon": 1.4, "px_val": 64,
              "items": [{"label": "CUESTAS", "val": 29469, "color": "red", "txt": "{v} €"},
                        {"label": "COBRAS", "val": 18000, "color": "green", "txt": "{v} €"}]},
         ]},
        {"voz": [{"tts": "Once mil cuatrocientos se quedan por el camino.", "text": "11.466 € se quedan por el camino."}],
         "trans": "barrido", "cam": "golpe",
         "el": [
             {"k": "num", "val": 11466, "desde": 0, "dur": 0.9, "golpe": True, "px": 200, "y": 620, "suf": " €", "color": "red", "at": 0.1},
             {"k": "dinero", "modo": "fuga", "desde": [540, 700], "hacia": [540, -300], "n": 16, "at": "@camino-0.4", "dur": 1.4},
             {"k": "txt", "t": "AL AÑO", "px": 70, "y": 860, "at": "@quedan", "marca": "yellow"},
         ]},
        {"voz": [{"tts": "De cada cien euros que cuestas, treinta y nueve no los tocas nunca.",
                  "text": "De cada 100 € que cuestas, 39 no los tocas nunca."}],
         "trans": "flash", "cam": "empuja",
         "el": [
             {"k": "gente", "n": 10, "cols": 5, "sep": 170, "y": 640, "destacar": [0, 1, 2, 3], "apagar": "@39", "color": "green", "color_dest": "red"},
             {"k": "txt", "t": "39 DE CADA 100 €", "px": 88, "y": 990, "at": "@39", "marca": "yellow"},
         ]},
        {"voz": [{"tts": "La OCDE lo confirma: en España, el cuarenta y uno coma cuatro por ciento. El nivel más alto en veinticinco años.",
                  "text": "La OCDE lo confirma: en España, el 41,4 %. El nivel más alto en 25 años."}],
         "trans": "zoom", "cam": "aleja", "fuente": "OCDE, Taxing Wages 2026",
         "el": [
             {"k": "barras", "y": 1000, "w": 700, "h": 520, "max": 45, "escalon": 1.0,
              "items": [{"label": "ESPAÑA", "val": 41.4, "color": "red", "txt": "{v} %", "dec": 1},
                        {"label": "MEDIA OCDE", "val": 35.1, "color": "blue", "txt": "{v} %", "dec": 1}]},
             {"k": "sello", "t": "RÉCORD", "x": 540, "y": 380, "px": 90, "at": "@alto", "rot": -8},
         ]},
        # GIRO
        {"voz": ["Ojo: ese dinero no desaparece."], "trans": "tinta", "cam": "golpe", "pausa": 0.5, "min": 1.4,
         "el": [
             {"k": "txt", "t": "NO\nDESAPARECE", "px": 130, "y": 700, "at": 0.05, "color": "ink"},
         ]},
        {"voz": ["Paga tu pensión, tu paro, tu baja… y la sanidad y los colegios con el IRPF."],
         "trans": "barrido", "cam": "deriva",
         "el": [
             {"k": "pers", "tipo": "hucha", "x": 270, "y": 560, "tam": 0.7, "cara": "feliz", "at": "@pensión"},
             {"k": "icono", "n": "maleta", "x": 800, "y": 560, "tam": 0.9, "at": "@paro"},
             {"k": "icono", "n": "calendario", "x": 270, "y": 950, "tam": 0.9, "at": "@baja"},
             {"k": "icono", "n": "hospital", "x": 800, "y": 950, "tam": 0.9, "at": "@sanidad"},
         ]},
        {"voz": ["Lo incómodo es otra cosa: casi nadie sabe que la mayor parte la paga su empresa. Porque no sale en la nómina."],
         "trans": "flash", "cam": "empuja",
         "el": [
             {"k": "icono", "n": "documento", "x": 540, "y": 800, "tam": 2.0, "at": 0.1},
             {"k": "icono", "n": "interrogacion", "x": 540, "y": 790, "tam": 1.2, "at": "@nómina"},
             {"k": "txt", "t": "INVISIBLE", "px": 110, "y": 430, "at": "@incómodo", "color": "red"},
         ]},
        # PREGUNTA
        {"voz": ["¿Quieres ver en tu nómina lo que cuesta de verdad tu trabajo?", "Comenta A o B."], "trans": "zoom", "cam": "quieta", "min": 0, "cola": 1.8,
         "el": [
             {"k": "encuesta", "pregunta": "¿LO QUIERES VER\nEN TU NÓMINA?", "a": "SÍ, QUIERO VERLO", "b": "ME DA IGUAL", "color_a": "green", "color_b": "gray",
              "at": 0.05, "at_a": "@cuesta", "at_b": "@trabajo", "at_c": "L1"},
         ]},
    ],
}
