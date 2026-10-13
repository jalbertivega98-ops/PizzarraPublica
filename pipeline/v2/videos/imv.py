"""Los datos que incomodan #9 · Ingreso Mínimo Vital.

Cifras (consultadas el 13/10/2026):
- INSS vía Revista de la Seguridad Social (10/04/2026), nómina de marzo de 2026: 829.399 hogares, 2.532.284 personas,
  1.034.319 menores; 495,6 millones de euros; 543,1 € de media por hogar.
- Requisitos (seg-social.es, IMV): residencia legal y efectiva en España al menos el año anterior (excepciones: menores,
  víctimas de trata y de violencia de género); 23 años como mínimo (salvo excepciones); de 23 a 29 años, vida independiente
  2 años y 12 meses de alta en la Seguridad Social; ingresos por debajo de la renta garantizada (733,60 €/mes un adulto
  solo en 2026); patrimonio neto sin vivienda habitual < 3 veces la renta garantizada anual (26.409,60 €).
  No exige cotización previa salvo el alta de 12 meses del tramo 23-29. Compatible con rentas del trabajo.
- Ley 19/2021: lo cobrado indebidamente se reintegra.
"""
VIDEO = {
    "slug": "di09_imv",
    "titulo": "Cobrar sin haber cotizado.",
    "serie": "LOS DATOS QUE INCOMODAN · #9",
    "acento": "green",
    "voz": "elevenlabs:Pizarra Pública",
    "claves": ["ni", "829.000", "496", "543", "año", "733,60", "26.400", "23", "29", "fraude", "sí", "no"],
    "musica": {"bpm": 118, "tono": 2, "seed": 99},
    "portada": {"t": 1.2, "titulo": "COBRAR SIN\nHABER COTIZADO"},
    "duro": True,
    "planos": [
        # GANCHO
        {"voz": ["Hay una ayuda del Estado que no te pide haber trabajado ni un solo día."],
         "cam": "golpe", "fuente": "Seguridad Social, Ingreso Mínimo Vital",
         "el": [
             {"k": "dinero", "modo": "lluvia", "n": 24, "at": 0.1, "dur": 2.4, "z": -1},
             {"k": "pers", "tipo": "ciudadano", "x": 540, "y": 1060, "tam": 1.1, "cara": "sorpresa", "pose": "brazos_arriba", "at": 0.2},
             {"k": "sello", "t": "0 DÍAS COTIZADOS", "x": 540, "y": 560, "px": 80, "at": "@ni", "rot": -10},
         ]},
        {"voz": ["Se llama Ingreso Mínimo Vital."], "trans": "zoom", "cam": "empuja", "min": 1.4,
         "el": [
             {"k": "icono", "n": "documento", "x": 540, "y": 740, "tam": 1.7, "at": 0.05},
             {"k": "txt", "t": "INGRESO\nMÍNIMO VITAL", "px": 96, "y": 760, "at": "@Ingreso", "color": "green", "marca": "yellow"},
         ]},
        # DATOS
        {"voz": [{"tts": "En marzo lo cobraban más de ochocientos veintinueve mil hogares. Más de dos millones y medio de personas.",
                  "text": "En marzo lo cobraban más de 829.000 hogares. Más de 2,5 millones de personas."}],
         "trans": "barrido", "cam": "golpe", "fuente": "INSS, nómina de marzo 2026",
         "el": [
             {"k": "num", "val": 829399, "desde": 0, "dur": 1.2, "golpe": True, "px": 180, "y": 560, "at": "@829.000-0.2",
              "sub": "hogares"},
             {"k": "icono", "n": "casa", "x": 300, "y": 1000, "tam": 0.9, "at": "@hogares"},
             {"k": "txt", "t": "2,5 MILLONES\nDE PERSONAS", "px": 72, "y": 1000, "x": 740, "at": "@personas", "color": "green"},
         ]},
        {"voz": [{"tts": "Ese mes costó casi cuatrocientos noventa y seis millones de euros. Unos quinientos cuarenta y tres por hogar.",
                  "text": "Ese mes costó casi 496 millones de euros. Unos 543 € por hogar."}],
         "trans": "flash", "cam": "golpe", "fuente": "INSS, nómina de marzo 2026",
         "el": [
             {"k": "dinero", "modo": "lluvia", "n": 30, "at": 0.2, "dur": 2.0, "z": -1},
             {"k": "num", "val": 495.6, "desde": 0, "dur": 1.0, "golpe": True, "px": 150, "y": 600, "dec": 1, "suf": " M€",
              "color": "red", "fondo": "yellow", "at": "@496-0.2"},
             {"k": "num", "val": 543, "desde": 0, "dur": 0.6, "px": 130, "y": 960, "suf": " €/hogar", "color": "green",
              "at": "@543-0.2"},
         ]},
        # REQUISITOS
        {"voz": ["¿Quién puede cobrarlo? Tres requisitos."], "trans": "tinta", "cam": "golpe", "min": 1.4,
         "el": [
             {"k": "icono", "n": "lupa", "x": 540, "y": 640, "tam": 1.4, "at": 0.05},
             {"k": "txt", "t": "3 REQUISITOS", "px": 100, "y": 960, "at": "@Tres", "marca": "yellow"},
         ]},
        {"voz": [{"tts": "Uno: residencia legal en España, al menos un año.", "text": "Uno: residencia legal en España, al menos un año."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Seguridad Social, requisitos IMV",
         "el": [
             {"k": "icono", "n": "pasaporte", "x": 300, "y": 720, "tam": 1.2, "at": "@residencia"},
             {"k": "icono", "n": "calendario", "x": 780, "y": 720, "tam": 1.2, "at": "@año"},
             {"k": "txt", "t": "1 AÑO LEGAL", "px": 84, "y": 1020, "at": "@legal", "color": "green"},
         ]},
        {"voz": [{"tts": "Dos: ingresar menos de setecientos treinta y tres euros con sesenta al mes si vives solo.",
                  "text": "Dos: ingresar menos de 733,60 € al mes si vives solo."}],
         "trans": "sube", "cam": "golpe", "fuente": "Renta garantizada 2026, adulto solo",
         "el": [
             {"k": "icono", "n": "cartera", "x": 540, "y": 520, "tam": 1.1, "at": 0.05},
             {"k": "num", "val": 733.6, "desde": 0, "dur": 0.8, "px": 130, "y": 850, "pre": "< ", "suf": " €", "dec": 2,
              "color": "green", "at": "@733,60-0.2"},
             {"k": "txt", "t": "AL MES", "px": 64, "y": 1020, "at": "@mes"},
         ]},
        {"voz": [{"tts": "Y tres: patrimonio por debajo de unos veintiséis mil cuatrocientos euros, sin contar tu casa.",
                  "text": "Y tres: patrimonio por debajo de unos 26.400 €, sin contar tu casa."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Seguridad Social, requisitos IMV 2026",
         "el": [
             {"k": "num", "val": 26409, "desde": 0, "dur": 0.9, "px": 160, "y": 620, "pre": "< ", "suf": " €", "color": "green",
              "at": "@26.400-0.2"},
             {"k": "icono", "n": "casa", "x": 540, "y": 960, "tam": 1.0, "at": "@contar"},
             {"k": "tacha", "x": 540, "y": 960, "w": 260, "h": 200, "at": "@casa"},
         ]},
        # GIRO
        {"voz": ["Pero aquí está el matiz."], "trans": "flash", "cam": "golpe", "pausa": 0.4, "min": 1.2,
         "el": [
             {"k": "estallido", "r": 320, "y": 700, "color": "yellow", "at": 0},
             {"k": "txt", "t": "EL MATIZ", "px": 110, "y": 700, "at": "@matiz-0.1", "color": "ink"},
         ]},
        {"voz": [{"tts": "Si lo pides solo, con entre veintitrés y veintinueve años, sí te exigen un año de alta en la Seguridad Social.",
                  "text": "Si lo pides solo, con entre 23 y 29 años, sí te exigen un año de alta en la Seguridad Social."}],
         "trans": "zoom", "cam": "empuja", "fuente": "Seguridad Social, requisitos IMV",
         "el": [
             {"k": "pers", "tipo": "joven", "x": 290, "y": 960, "tam": 1.2, "cara": "duda", "at": "@solo"},
             {"k": "txt", "t": "23-29 AÑOS", "px": 84, "y": 480, "at": "@23", "marca": "yellow"},
             {"k": "sello", "t": "12 MESES\nDE ALTA", "x": 720, "y": 860, "px": 58, "at": "@alta", "rot": -8},
         ]},
        {"voz": ["Para el resto, y para las familias con hijos, no hace falta haber cotizado."],
         "trans": "barrido", "cam": "deriva", "fuente": "INSS: 1.034.319 menores viven en hogares con IMV",
         "el": [
             {"k": "pers", "tipo": "ciudadana", "x": 360, "y": 900, "tam": 1.1, "cara": "neutral", "at": "@familias"},
             {"k": "pers", "tipo": "ciudadano", "x": 600, "y": 990, "tam": 0.6, "cara": "feliz", "at": "@hijos"},
             {"k": "num", "val": 1034319, "desde": 0, "dur": 1.0, "px": 110, "y": 460, "sub": "menores", "color": "green",
              "at": "@hijos"},
             {"k": "sello", "t": "SIN COTIZAR", "x": 820, "y": 760, "px": 60, "at": "@cotizado", "rot": 10},
         ]},
        # FRAUDE VS PROTECCIÓN
        {"voz": ["Cobrarlo cumpliendo los requisitos no es fraude. Fraude es ocultar ingresos o patrimonio, y obliga a devolverlo."],
         "trans": "tinta", "cam": "empuja", "fuente": "Ley 19/2021 del Ingreso Mínimo Vital",
         "el": [
             {"k": "txt", "t": "CUMPLIR ≠ FRAUDE", "px": 76, "y": 440, "at": "@fraude", "color": "green"},
             {"k": "icono", "n": "lupa", "x": 540, "y": 760, "tam": 1.2, "at": "@ocultar"},
             {"k": "sello", "t": "A DEVOLVER", "x": 540, "y": 1040, "px": 80, "at": "@devolverlo", "rot": -10},
         ]},
        # PREGUNTA
        {"voz": ["¿Deberían exigirse años cotizados para cobrar ayudas como esta? A: sí. B: no.", "Comenta A o B."],
         "trans": "zoom", "cam": "quieta", "min": 0, "cola": 1.8,
         "el": [
             {"k": "encuesta", "pregunta": "¿EXIGIR AÑOS\nCOTIZADOS?", "a": "SÍ", "b": "NO", "color_a": "green", "color_b": "red",
              "at": 0.05, "at_a": "@sí", "at_b": "@no", "at_c": "L1"},
         ]},
    ],
}
