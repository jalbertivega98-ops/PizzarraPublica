"""Los datos que incomodan #6 · Pensiones y jóvenes.

- Pensión media de jubilación: 1.576,1 €/mes en septiembre de 2026 (Ministerio de Inclusión, nómina de septiembre); 14 pagas = 22.065 €/año.
- Salario más frecuente (moda): 16.520,18 €/año brutos en 2024 (INE, Encuesta Anual de Estructura Salarial, 28/05/2026).
- Nómina de pensiones de septiembre de 2026: 14.498,2 M€; 10.547.417 pensiones (Ministerio de Inclusión).
- Fedea (22/01/2026): en 2025 el Estado transfirió 61.342 M€ a la Seguridad Social; sin ellas, déficit de 69.783 M€.
  Hasta 2011 las cotizaciones cubrían el gasto contributivo.
- Deuda de la Seguridad Social con el Estado: 136.176 M€ en julio de 2026 (Banco de España).
- Instituto Santalucía/Fedea/UAH con la EFF del Banco de España (29/04/2026): los menores de 35 pasan del 8,2 % (2002)
  al 2,1 % (2022) de la riqueza neta de los hogares; los mayores de 75, del 8,3 % al 18,3 %; la riqueza mediana de los
  menores de 35 cae un 76,7 % desde 2008.
"""
VIDEO = {
    "slug": "di06_pensiones",
    "titulo": "Tu abuelo cobra más que tú.",
    "serie": "LOS DATOS QUE INCOMODAN · #6",
    "acento": "purple",
    "voz": "elevenlabs:Pizarra Pública",
    "claves": ["1.576", "más", "61.342", "2,1", "impuestos", "padres"],
    "musica": {"bpm": 110, "tono": -1, "seed": 66},
    "portada": {"t": 2.6, "titulo": "LA PENSIÓN MEDIA\nGANA AL SUELDO MÁS COMÚN"},
    "planos": [
        # GANCHO
        {"voz": [{"tts": "Pensión media de jubilación: mil quinientos setenta y seis euros.", "text": "Pensión media de jubilación: 1.576 €."}],
         "cam": "golpe", "fuente": "Seguridad Social, septiembre 2026",
         "el": [
             {"k": "pers", "tipo": "ciudadano", "x": 280, "y": 1040, "tam": 1.2, "cara": "feliz", "pose": "saluda", "at": 0.05},
             {"k": "num", "val": 1576, "desde": 0, "dur": 0.8, "golpe": True, "px": 220, "y": 600, "suf": " €", "fondo": "yellow", "at": "@1.576-0.3"},
             {"k": "txt", "t": "AL MES · 14 PAGAS", "px": 56, "y": 810, "at": "@1.576", "fuente": "num"},
         ]},
        {"voz": [{"tts": "El sueldo más común en España: dieciséis mil quinientos al año. Mil ciento ochenta al mes.",
                  "text": "El sueldo más común en España: 16.520 € al año. 1.180 al mes."}],
         "trans": "flash", "cam": "golpe", "fuente": "INE, Estructura Salarial 2024",
         "el": [
             {"k": "pers", "tipo": "joven", "x": 800, "y": 1040, "tam": 1.2, "cara": "triste", "pose": "encoge", "mira": -1, "at": 0.05},
             {"k": "num", "val": 1180, "desde": 0, "dur": 0.7, "golpe": True, "px": 220, "y": 600, "suf": " €", "color": "red", "at": "@1.180-0.3"},
             {"k": "txt", "t": "SUELDO MÁS FRECUENTE", "px": 56, "y": 810, "at": "@común", "fuente": "num"},
         ]},
        {"voz": ["Sí: la pensión media ya supera al sueldo más frecuente."], "trans": "zoom", "cam": "aleja", "pausa": 0.3,
         "el": [
             {"k": "barras", "y": 1060, "w": 700, "h": 560, "max": 24000, "escalon": 0.5, "px_val": 62,
              "items": [{"label": "PENSIÓN/AÑO", "val": 22065, "color": "purple", "txt": "{v} €"},
                        {"label": "SUELDO/AÑO", "val": 16520, "color": "red", "txt": "{v} €"}]},
         ]},
        # PROBLEMA
        {"voz": [{"tts": "Cada mes, España paga catorce mil quinientos millones en pensiones.", "text": "Cada mes, España paga 14.498 millones en pensiones."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Seguridad Social, septiembre 2026",
         "el": [
             {"k": "num", "val": 14498, "desde": 0, "dur": 1.0, "golpe": True, "px": 190, "y": 600, "suf": " M€", "at": "@paga"},
             {"k": "dinero", "modo": "lluvia", "n": 24, "at": "@millones", "dur": 2.0, "z": -1},
             {"k": "txt", "t": "10,5 MILLONES DE PENSIONES", "px": 54, "y": 820, "at": "@pensiones", "fuente": "num"},
         ]},
        {"voz": ["Y las cotizaciones ya no llegan."], "trans": "tinta", "cam": "golpe",
         "el": [
             {"k": "pers", "tipo": "hucha", "x": 540, "y": 820, "tam": 1.4, "cara": "shock", "anim": "cae", "at": 0.05, "tiembla": True},
             {"k": "txt", "t": "NO LLEGAN", "px": 110, "y": 430, "at": "@llegan", "color": "red"},
         ]},
        {"voz": [{"tts": "En dos mil veinticinco, el Estado tuvo que meter sesenta y un mil millones de impuestos.",
                  "text": "En 2025, el Estado tuvo que meter 61.342 millones de impuestos."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Fedea, enero 2026",
         "el": [
             {"k": "icono", "n": "edificio", "x": 260, "y": 620, "tam": 1.0, "at": "@Estado"},
             {"k": "dinero", "modo": "fuga", "desde": [260, 640], "hacia": [800, 900], "n": 14, "at": "@meter", "dur": 1.4},
             {"k": "pers", "tipo": "hucha", "x": 800, "y": 940, "tam": 0.9, "cara": "nervioso", "at": "@meter"},
             {"k": "num", "val": 61342, "desde": 0, "dur": 1.0, "golpe": True, "px": 150, "y": 1180, "suf": " M€", "color": "red", "at": "@61.342-0.3"},
         ]},
        {"voz": ["Hasta 2011, las cotizaciones bastaban. Desde entonces, no."], "trans": "zoom", "cam": "deriva",
         "el": [
             {"k": "txt", "t": "HASTA 2011", "px": 90, "y": 520, "at": 0.05, "color": "green"},
             {"k": "icono", "n": "check", "x": 540, "y": 690, "tam": 1.2, "at": "@bastaban"},
             {"k": "txt", "t": "DESDE 2012", "px": 90, "y": 930, "at": "@entonces", "color": "red"},
             {"k": "icono", "n": "cruz", "x": 540, "y": 1090, "tam": 1.1, "at": "@no"},
         ]},
        {"voz": [{"tts": "Y la Seguridad Social ya le debe al Estado ciento treinta y seis mil millones.",
                  "text": "Y la Seguridad Social ya le debe al Estado 136.176 millones."}],
         "trans": "flash", "cam": "golpe", "fuente": "Banco de España, julio 2026",
         "el": [
             {"k": "num", "val": 136176, "desde": 0, "dur": 1.1, "golpe": True, "px": 170, "y": 640, "suf": " M€", "color": "red", "fondo": "estallido",
              "at": "@debe"},
             {"k": "txt", "t": "DE DEUDA", "px": 80, "y": 860, "at": "@Estado", "marca": "yellow"},
         ]},
        # GIRO
        {"voz": ["Mientras, los jóvenes tienen cada vez menos."], "trans": "tinta", "cam": "golpe", "pausa": 0.5,
         "el": [
             {"k": "pers", "tipo": "joven", "x": 540, "y": 880, "tam": 1.5, "cara": "triste", "pose": "cabeza", "at": 0.05},
         ]},
        {"voz": [{"tts": "En dos mil dos, los menores de treinta y cinco tenían el ocho por ciento de la riqueza. En dos mil veintidós, el dos.",
                  "text": "En 2002, los menores de 35 tenían el 8,2 % de la riqueza. En 2022, el 2,1 %."}],
         "trans": "barrido", "cam": "aleja", "fuente": "Instituto Santalucía con datos del Banco de España",
         "el": [
             {"k": "barras", "y": 1040, "w": 700, "h": 520, "max": 10, "escalon": 1.6,
              "items": [{"label": "2002", "val": 8.2, "color": "purple", "txt": "{v} %", "dec": 1},
                        {"label": "2022", "val": 2.1, "color": "red", "txt": "{v} %", "dec": 1}]},
             {"k": "txt", "t": "RIQUEZA DE LOS MENORES DE 35", "px": 48, "y": 360, "at": 0.1, "fuente": "num"},
         ]},
        {"voz": [{"tts": "Los mayores de setenta y cinco pasaron del ocho al dieciocho.", "text": "Los mayores de 75 pasaron del 8,3 % al 18,3 %."}],
         "trans": "sube", "cam": "empuja", "fuente": "Instituto Santalucía, 2026",
         "el": [
             {"k": "pers", "tipo": "ciudadano", "x": 300, "y": 900, "tam": 1.3, "cara": "listo", "pose": "jarras", "at": "@mayores-0.3"},
             {"k": "num", "val": 18.3, "desde": 8.3, "dur": 1.0, "golpe": True, "px": 200, "y": 700, "x": 760, "suf": " %", "dec": 1, "color": "purple",
              "at": "@18,3-0.6"},
         ]},
        {"voz": ["Ojo: los jubilados cotizaron toda su vida. El problema no es su pensión, es quién la va a pagar."],
         "trans": "flash", "cam": "deriva",
         "el": [
             {"k": "pers", "tipo": "ciudadano", "x": 280, "y": 900, "tam": 1.2, "cara": "neutral", "at": 0.05},
             {"k": "txt", "t": "COTIZARON", "px": 80, "y": 470, "x": 280, "at": "@cotizaron", "color": "green"},
             {"k": "pers", "tipo": "joven", "x": 800, "y": 900, "tam": 1.2, "cara": "duda", "mira": -1, "at": "@quién"},
             {"k": "txt", "t": "¿Y QUIÉN\nPAGA?", "px": 80, "y": 470, "x": 800, "at": "@pagar", "color": "red"},
         ]},
        # PREGUNTA
        {"voz": ["¿Crees que cobrarás una pensión como la de tus padres?"], "trans": "zoom", "cam": "empuja", "min": 0,
         "el": [
             {"k": "estallido", "r": 330, "y": 700, "color": "yellow", "at": 0},
             {"k": "txt", "t": "¿COBRARÁS\nCOMO ELLOS?", "px": 96, "y": 700, "at": "@cobrarás", "color": "ink"},
             {"k": "txt", "t": "TE LEO EN COMENTARIOS", "px": 50, "y": 1080, "at": "fin-1.2", "fuente": "num"},
         ]},
    ],
}
