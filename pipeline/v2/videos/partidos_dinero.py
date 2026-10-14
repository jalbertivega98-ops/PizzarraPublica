"""Los datos que incomodan #11 · Lo que te cuestan PSOE, PP y Vox.

Cifras de 2025 de las cuentas anuales que cada partido presenta al Tribunal de Cuentas (vía EFE, 02/08/2026,
salvo indicación):
- Ingresos públicos sin subvenciones electorales: PSOE 46,7 M€, PP 45,8 M€, Vox ≈ 12,2 M€ (Europa Press /
  El Independiente, 24/06/2026). Suma: 104,7 M€.
- Ingresos privados: PSOE 26 M€, PP ≈ 9 M€, Vox 4,1 M€. Parte pública = públicos / (públicos + privados):
  PSOE 64 %, PP 84 %, Vox 75 % (cálculo nuestro).
- PSOE: venta de lotería 3,2 M€; aportaciones de sus cargos públicos ≈ 10,2 M€; cuotas 9,5 M€.
- PP: 807.792 afiliados; cuotas 3,5 M€ → ≈ 4,3 € por afiliado y año (cálculo nuestro). En 2024 (cuentas del PP en pp.es):
  804.914 afiliados y 3.261.907 € en cuotas (≈ 4 €).
- Vox: 71.194 afiliados, 33.609 al corriente de pago; cuotas ≈ 3,8 M€ (más que el PP con 11 veces menos afiliados).
  Préstamo de más de 9 M€ del banco húngaro MBH para las campañas de 2023, tras negarse los bancos españoles;
  lo confirmó su portavoz Pepa Millán (El Español, 30/09/2024). MBH es de Lőrinc Mészáros, amigo de la infancia de Orbán.
  Vox dice que lo devolvió.
- Las cuentas de 2025 del PSOE excluyen por primera vez a los grupos provinciales y autonómicos (El Cronista, 03/07/2026).
"""
VIDEO = {
    "slug": "di11_partidos",
    "titulo": "Aunque no les votes, les pagas.",
    "serie": "LOS DATOS QUE INCOMODAN · #11",
    "acento": "yellow",
    "voz": "elevenlabs:Pizarra Pública",
    "claves": ["104", "4", "lotería", "Hungría", "84", "cuotas"],
    "musica": {"bpm": 120, "tono": 0, "seed": 111},
    "portada": {"t": 2.4, "titulo": "AUNQUE NO LES VOTES,\nLES PAGAS"},
    "duro": True,
    "planos": [
        # GANCHO
        {"voz": ["Aunque no les votes… les pagas."],
         "cam": "golpe", "min": 1.6,
         "el": [
             {"k": "pers", "tipo": "joven", "x": 540, "y": 1000, "tam": 1.4, "cara": "shock", "pose": "cabeza", "at": 0.05},
             {"k": "sello", "t": "LES PAGAS", "x": 540, "y": 460, "px": 120, "at": "@pagas", "rot": -8},
         ]},
        {"voz": [{"tts": "PSOE, PP y Vox recibieron ciento cuatro millones de euros de dinero público en un solo año.",
                  "text": "PSOE, PP y Vox recibieron 104 millones de euros de dinero público en un solo año."}],
         "trans": "flash", "cam": "golpe", "fuente": "Cuentas anuales 2025 de los partidos",
         "el": [
             {"k": "txt", "t": "PSOE", "px": 80, "y": 1000, "x": 230, "color": "psoe", "at": "@PSOE-0.2"},
             {"k": "txt", "t": "PP", "px": 80, "y": 1000, "x": 540, "color": "pp", "at": "@PP-0.2"},
             {"k": "txt", "t": "VOX", "px": 80, "y": 1000, "x": 850, "color": "vox", "at": "@Vox-0.2"},
             {"k": "num", "val": 104, "desde": 0, "dur": 0.9, "golpe": True, "px": 170, "y": 600, "suf": " M€", "fondo": "estallido",
              "at": "@104-0.3"},
             {"k": "dinero", "modo": "lluvia", "n": 26, "at": "@público", "dur": 2.0, "z": -1},
             {"k": "txt", "t": "SALEN DE TUS IMPUESTOS", "px": 54, "y": 1130, "at": "@público", "marca": "yellow"},
         ]},
        # SÍGUENOS
        {"voz": ["Síguenos: esto casi nadie te lo cuenta."], "trans": "zoom", "cam": "golpe", "min": 1.6,
         "el": [
             {"k": "icono", "n": "movil", "x": 540, "y": 720, "tam": 1.4, "at": 0.05},
             {"k": "sello", "t": "SÍGUENOS", "x": 540, "y": 420, "px": 110, "at": "@Síguenos", "rot": -6, "color": "red"},
             {"k": "txt", "t": "+ DATOS QUE NO TE CUENTAN", "px": 52, "y": 1000, "at": "@nadie", "marca": "yellow"},
         ]},
        # PSOE
        {"voz": [{"tts": "El PSOE vende lotería de Navidad. El año pasado le dejó tres millones.",
                  "text": "El PSOE vende lotería de Navidad. El año pasado le dejó 3,2 millones."}],
         "trans": "barrido", "cam": "empuja", "fuente": "Cuentas PSOE 2025 (EFE)",
         "el": [
             {"k": "txt", "t": "PSOE", "px": 110, "y": 320, "color": "psoe", "at": 0.05},
             {"k": "icono", "n": "billete", "x": 540, "y": 620, "tam": 1.5, "at": "@lotería", "anim": "golpe"},
             {"k": "txt", "t": "LOTERÍA DE NAVIDAD", "px": 60, "y": 790, "at": "@Navidad", "fuente": "num"},
             {"k": "num", "val": 3.2, "desde": 0, "dur": 0.8, "dec": 1, "golpe": True, "px": 170, "y": 1020, "suf": " M€", "color": "psoe",
              "at": "@3,2-0.3"},
         ]},
        {"voz": [{"tts": "Y sus diputados y alcaldes le devuelven parte del sueldo: diez millones al año. Más que todas sus cuotas.",
                  "text": "Y sus diputados y alcaldes le devuelven parte del sueldo: 10 millones al año. Más que todas sus cuotas."}],
         "trans": "zoom", "cam": "deriva", "fuente": "Cuentas PSOE 2025 (EFE)",
         "el": [
             {"k": "pers", "tipo": "politico", "x": 270, "y": 900, "tam": 1.1, "cara": "neutral", "at": "@diputados-0.2"},
             {"k": "dinero", "modo": "fuga", "desde": [300, 800], "hacia": [800, 560], "n": 12, "at": "@sueldo", "dur": 1.3},
             {"k": "txt", "t": "PSOE", "px": 90, "y": 480, "x": 800, "color": "psoe", "at": "@sueldo"},
             {"k": "barras", "y": 1110, "x": 760, "w": 440, "h": 340, "max": 11, "escalon": 0.4, "px_val": 46,
              "at": "@10-0.2",
              "items": [{"label": "CARGOS", "val": 10.2, "color": "psoe", "txt": "{v} M€", "dec": 1},
                        {"label": "CUOTAS", "val": 9.5, "color": "gray", "txt": "{v} M€", "dec": 1}]},
         ]},
        {"voz": ["Aun así, de cada diez euros que ingresa, más de seis son públicos."],
         "trans": "flash", "cam": "golpe",
         "el": [
             {"k": "txt", "t": "PSOE", "px": 90, "y": 330, "color": "psoe", "at": 0.05},
             {"k": "gente", "n": 10, "cols": 5, "sep": 170, "y": 760, "color": "gray", "destacar": [0, 1, 2, 3, 4, 5],
              "color_dest": "yellow", "apagar": "@seis", "at": "@diez"},
             {"k": "txt", "t": "64 % DINERO PÚBLICO", "px": 66, "y": 1120, "at": "@públicos-0.2", "marca": "yellow"},
         ]},
        # PP
        {"voz": [{"tts": "El PP dice tener ochocientos siete mil afiliados.", "text": "El PP dice tener 807.792 afiliados."}],
         "trans": "barrido", "cam": "golpe", "fuente": "Cuentas PP 2025",
         "el": [
             {"k": "txt", "t": "PP", "px": 120, "y": 320, "color": "pp", "at": 0.05},
             {"k": "num", "val": 807792, "desde": 0, "dur": 1.1, "golpe": True, "px": 160, "y": 640, "at": "@807.792-0.4"},
             {"k": "txt", "t": "AFILIADOS", "px": 70, "y": 800, "at": "@afiliados", "fuente": "num"},
         ]},
        {"voz": [{"tts": "Pero en cuotas recauda tres millones y medio. Unos cuatro euros por afiliado… al año.",
                  "text": "Pero en cuotas recauda 3,5 millones. Unos 4 € por afiliado… al año."}],
         "trans": "corte", "cam": "golpe", "pausa": 0.3, "fuente": "Cuentas PP 2025 · cálculo nuestro",
         "el": [
             {"k": "pers", "tipo": "ciudadano", "x": 300, "y": 960, "tam": 1.2, "cara": "sorpresa", "at": 0.05},
             {"k": "icono", "n": "moneda", "x": 760, "y": 640, "tam": 1.6, "at": "@4", "anim": "cae"},
             {"k": "num", "val": 4, "desde": 0, "dur": 0.4, "golpe": True, "px": 230, "y": 980, "x": 760, "suf": " €", "color": "red",
              "at": "@4-0.2"},
             {"k": "txt", "t": "AL AÑO", "px": 80, "y": 1110, "x": 760, "at": "@año", "marca": "yellow"},
         ]},
        {"voz": [{"tts": "Y de cada diez euros que ingresa, más de ocho son públicos.",
                  "text": "Y de cada diez euros que ingresa, más de ocho son públicos."}],
         "trans": "flash", "cam": "golpe",
         "el": [
             {"k": "txt", "t": "PP", "px": 100, "y": 330, "color": "pp", "at": 0.05},
             {"k": "gente", "n": 10, "cols": 5, "sep": 170, "y": 760, "color": "gray", "destacar": [0, 1, 2, 3, 4, 5, 6, 7],
              "color_dest": "yellow", "apagar": "@ocho", "at": "@diez"},
             {"k": "txt", "t": "84 % DINERO PÚBLICO", "px": 66, "y": 1120, "at": "@públicos-0.2", "marca": "yellow"},
         ]},
        # VOX
        {"voz": ["¿Y Vox? Los bancos españoles no le prestaban."],
         "trans": "barrido", "cam": "empuja", "fuente": "El Español, 30/09/2024",
         "el": [
             {"k": "txt", "t": "VOX", "px": 120, "y": 320, "color": "vox", "at": 0.05},
             {"k": "icono", "n": "edificio", "x": 540, "y": 700, "tam": 1.4, "at": "@bancos"},
             {"k": "icono", "n": "cruz", "x": 540, "y": 700, "tam": 1.6, "at": "@prestaban"},
         ]},
        {"voz": [{"tts": "Así que pidió más de nueve millones a un banco de Hungría. Su dueño: un amigo de la infancia de Orbán.",
                  "text": "Así que pidió más de 9 millones a un banco de Hungría. Su dueño: un amigo de la infancia de Orbán."}],
         "trans": "zoom", "cam": "deriva", "fuente": "El Español, 30/09/2024 · Vox dice que lo devolvió",
         "el": [
             {"k": "icono", "n": "avion", "x": 300, "y": 560, "tam": 1.1, "at": "@Hungría-0.4"},
             {"k": "txt", "t": "HUNGRÍA", "px": 80, "y": 720, "x": 300, "at": "@Hungría", "marca": "yellow"},
             {"k": "num", "val": 9, "desde": 0, "dur": 0.5, "golpe": True, "px": 140, "y": 900, "x": 720, "pre": "+", "suf": " M€", "color": "red",
              "at": "@9-0.3"},
             {"k": "pers", "tipo": "politico", "x": 540, "y": 1060, "tam": 0.9, "cara": "listo", "pose": "jarras", "rotulo": "MBH",
              "color_rotulo": "ink", "px_rotulo": 50, "at": "@dueño"},
         ]},
        {"voz": [{"tts": "Y de cada diez euros que ingresa, siete y medio son públicos.",
                  "text": "Y de cada diez euros que ingresa, 7,5 son públicos."}],
         "trans": "flash", "cam": "golpe", "fuente": "Cuentas Vox 2025 · cálculo nuestro",
         "el": [
             {"k": "txt", "t": "VOX", "px": 100, "y": 330, "color": "vox", "at": 0.05},
             {"k": "gente", "n": 10, "cols": 5, "sep": 170, "y": 760, "color": "gray", "destacar": [0, 1, 2, 3, 4, 5, 6],
              "color_dest": "yellow", "apagar": "@7,5", "at": "@diez"},
             {"k": "txt", "t": "75 % DINERO PÚBLICO", "px": 66, "y": 1120, "at": "@públicos-0.2", "marca": "yellow"},
         ]},
        # GIRO
        {"voz": [{"tts": "Y el giro: Vox tiene once veces menos afiliados que el PP… y recauda más en cuotas.",
                  "text": "Y el giro: Vox tiene 11 veces menos afiliados que el PP… y recauda más en cuotas."}],
         "trans": "tinta", "cam": "golpe", "pausa": 0.5, "fuente": "Cuentas 2025 (EFE)",
         "el": [
             {"k": "barras", "y": 1150, "w": 720, "h": 560, "max": 4.2, "escalon": 0.6, "px_val": 58, "at": "@afiliados",
              "items": [{"label": "PP", "val": 3.5, "color": "pp", "txt": "{v} M€", "dec": 1},
                        {"label": "VOX", "val": 3.8, "color": "vox", "txt": "{v} M€", "dec": 1}]},
             {"k": "txt", "t": "×11 MENOS AFILIADOS", "px": 64, "y": 330, "at": "@11", "color": "red"},
             {"k": "txt", "t": "807.792\nAFILIADOS", "px": 44, "y": 470, "x": 360, "at": "@PP", "color": "pp"},
             {"k": "txt", "t": "71.194\nAFILIADOS", "px": 44, "y": 470, "x": 720, "at": "@Vox", "color": "vox"},
         ]},
        {"voz": ["Ojo: que los partidos reciban dinero público es legal. La pregunta es cuánto."],
         "trans": "flash", "cam": "deriva",
         "el": [
             {"k": "icono", "n": "mazo", "x": 300, "y": 700, "tam": 1.2, "at": "@legal-0.3"},
             {"k": "icono", "n": "check", "x": 300, "y": 960, "tam": 1.0, "at": "@legal"},
             {"k": "icono", "n": "interrogacion", "x": 780, "y": 800, "tam": 1.5, "at": "@cuánto-0.2"},
             {"k": "txt", "t": "¿CUÁNTO?", "px": 90, "y": 1060, "x": 780, "at": "@cuánto", "color": "red"},
         ]},
        # PREGUNTA
        {"voz": ["¿Los partidos deberían vivir solo de sus afiliados?", "Comenta A o B.", "Y síguenos para no perderte el siguiente."], "trans": "zoom", "cam": "quieta", "min": 0,
         "cola": 1.8,
         "el": [
             {"k": "encuesta", "pregunta": "¿SOLO DE SUS\nAFILIADOS?", "a": "SÍ, NI UN EURO PÚBLICO", "b": "NO, ES NECESARIO",
              "color_a": "green", "color_b": "red", "at": 0.05, "at_a": "@partidos", "at_b": "@afiliados", "at_c": "L1"},
         ]},
    ],
}
