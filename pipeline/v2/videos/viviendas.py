"""Los datos que incomodan #3 · 184.000 viviendas prometidas: ¿cuántas hay?

Cifras:
- Promesa: 184.000 viviendas públicas y asequibles (Pedro Sánchez, 18/12/2023; antes 183.000 el 25/04/2023).
- Anuncios de vivienda del Gobierno desde 2018: al menos 14 (Maldita.es, 30/04/2026).
- 120.479 viviendas «movilizadas» = fondos transferidos (Ministerio de Vivienda, 30/04/2026).
- El Ministerio no facilitó, ni por Transparencia, cuántas se han entregado (Maldita.es, 30/04/2026).
- 10.206 entregadas = 5,5 % de 184.000, cálculo de El Debate (04/10/2024).
- 14.317 viviendas protegidas terminadas en toda España entre el 4.º trim. 2024 y el 3.º trim. 2025 (datos del Gobierno vía Maldita).
- Competencias: la vivienda es competencia autonómica (art. 148.1.3.ª de la Constitución); los ayuntamientos gestionan suelo.
"""
VIDEO = {
    "slug": "di03_viviendas",
    "titulo": "184.000 viviendas prometidas. ¿Cuántas hay?",
    "serie": "LOS DATOS QUE INCOMODAN · #3",
    "acento": "orange",
    "claves": ["prometidas", "nadie", "movilizadas", "dinero", "exista", "colores"],
    "musica": {"bpm": 96, "tono": 2, "seed": 33},
    "portada": {"t": 4.4, "titulo": "¿DÓNDE ESTÁN\nLAS 184.000 CASAS?"},
    "planos": [
        {"voz": [{"tts": "Ciento ochenta y cuatro mil viviendas prometidas.", "text": "184.000 viviendas prometidas."}],
         "cam": "golpe", "fuente": "Pedro Sánchez, 18/12/2023",
         "el": [
             {"k": "num", "val": 184000, "desde": 0, "dur": 0.8, "golpe": True, "px": 220, "y": 560, "fondo": "yellow", "at": 0},
             {"k": "icono", "n": "casa", "x": 200, "y": 900, "tam": 0.8, "at": "@viviendas", "anim": "cae"},
             {"k": "icono", "n": "casa", "x": 420, "y": 920, "tam": 0.8, "at": "@viviendas+0.08", "anim": "cae", "color": "yellow"},
             {"k": "icono", "n": "casa", "x": 650, "y": 920, "tam": 0.8, "at": "@viviendas+0.16", "anim": "cae", "color": "teal"},
             {"k": "icono", "n": "casa", "x": 870, "y": 900, "tam": 0.8, "at": "@viviendas+0.24", "anim": "cae", "color": "pink"},
             {"k": "txt", "t": "PROMETIDAS", "px": 70, "y": 1110, "at": "@prometidas", "color": "orange"},
         ]},
        {"voz": ["¿Cuántas tienen ya a alguien viviendo dentro?"], "trans": "zoom", "cam": "empuja",
         "foco": [540, 760, 1.25, "@dentro"],
         "el": [
             {"k": "icono", "n": "casa", "x": 540, "y": 760, "tam": 2.6, "anim": "pop"},
             {"k": "icono", "n": "interrogacion", "x": 540, "y": 380, "tam": 1.5, "at": "@alguien", "flota": True},
         ]},
        {"voz": ["Nadie lo sabe.", "El Gobierno no publica esa cifra."], "trans": "corte", "cam": "golpe",
         "el": [
             {"k": "pers", "tipo": "politico", "x": 540, "y": 820, "tam": 1.6, "cara": "nervioso", "pose": "encoge", "anim": "pop", "tiembla": False,
              "cambios": [["@Gobierno", {"cara": "nervioso", "tiembla": True}]]},
             {"k": "sello", "t": "SIN DATOS", "x": 540, "y": 430, "px": 90, "at": "@cifra-0.2"},
         ]},
        {"voz": ["Desde 2018, el Gobierno de Pedro Sánchez ha anunciado planes de vivienda al menos catorce veces."],
         "trans": "barrido", "cam": "aleja", "fuente": "Maldita.es, 30/04/2026",
         "el": [
             {"k": "burbujas", "y": 720, "at": "@anunciado-0.3", "escalon": 0.16, "px": 50,
              "items": ["20.000", "26.000", "100.000", "30.000", "50.000", "43.000", "20.000", "43.000", "180.000", "40.000",
                        "15.000/año", "10.700", "184.000", "15.000/año"]},
             {"k": "num", "val": 14, "desde": 0, "dur": 0.5, "px": 230, "y": 760, "at": "@catorce-0.4", "golpe": True, "color": "orange",
              "fondo": "estallido", "suf": " veces", "z": 2},
         ]},
        {"voz": [{"tts": "En abril de 2026, Vivienda habló de ciento veinte mil viviendas movilizadas.",
                  "text": "En abril de 2026, Vivienda habló de 120.479 viviendas «movilizadas»."}],
         "trans": "sube", "cam": "empuja", "fuente": "Ministerio de Vivienda, 30/04/2026",
         "el": [
             {"k": "num", "val": 120479, "desde": 0, "dur": 0.9, "px": 200, "y": 620, "at": "@120.479-0.3", "golpe": True},
             {"k": "txt", "t": "«MOVILIZADAS»", "px": 96, "y": 830, "at": "@«movilizadas»", "marca": "yellow"},
         ]},
        {"voz": ["Suena bien. Pero movilizada significa que se ha enviado el dinero.", "No que la casa exista."],
         "trans": "tinta", "cam": "deriva",
         "el": [
             {"k": "icono", "n": "edificio", "x": 230, "y": 560, "tam": 1.0, "at": 0.05},
             {"k": "txt", "t": "SUENA BIEN…", "px": 90, "y": 1050, "at": 0.05, "hasta": "@movilizada-0.1", "marca": "yellow"},
             {"k": "dinero", "modo": "fuga", "desde": [230, 560], "hacia": [820, 760], "n": 12, "at": "@enviado", "dur": 1.3},
             {"k": "icono", "n": "casa", "x": 820, "y": 800, "tam": 1.4, "anim": "traza", "dur": 1.0, "at": "@movilizada", "color": "light"},
             {"k": "icono", "n": "interrogacion", "x": 820, "y": 470, "tam": 1.1, "at": "@exista-0.2"},
             {"k": "txt", "t": "DINERO ≠ CASA", "px": 92, "y": 1080, "at": "@No", "color": "red"},
         ]},
        {"voz": ["Maldita.es pidió cuántas se han entregado. También por Transparencia.", "El Ministerio no ha dado la cifra."],
         "trans": "barrido", "cam": "empuja", "fuente": "Maldita.es, 30/04/2026",
         "el": [
             {"k": "icono", "n": "documento", "x": 540, "y": 640, "tam": 1.6, "at": "@pidió-0.2"},
             {"k": "txt", "t": "SOLICITUD", "px": 60, "y": 420, "at": "@pidió"},
             {"k": "icono", "n": "reloj", "x": 860, "y": 420, "tam": 0.7, "at": "@Transparencia", "flota": True},
             {"k": "sello", "t": "SIN CIFRA", "y": 700, "px": 96, "at": "@cifra-0.25"},
         ]},
        {"voz": [{"tts": "En 2024, un recuento de prensa llegó a diez mil doscientas seis: el cinco coma cinco por ciento.",
                  "text": "En 2024, un recuento de prensa llegó a 10.206: el 5,5 %."}],
         "trans": "zoom", "cam": "empuja", "fuente": "El Debate, 04/10/2024",
         "el": [
             {"k": "medidor", "y": 700, "w": 700, "px": 100, "val": 5.5, "max": 100, "amago": True, "dur": 2.2, "etiqueta": "ENTREGADAS / 184.000",
              "txt": "5,5 %", "at": "@recuento", "color": "orange"},
             {"k": "num", "val": 10206, "desde": 0, "dur": 0.7, "px": 130, "y": 470, "at": "@10.206-0.3"},
         ]},
        {"voz": [{"tts": "Y en toda España, en un año, se terminaron catorce mil trescientas diecisiete viviendas protegidas.",
                  "text": "Y en toda España, en un año, se terminaron 14.317 viviendas protegidas."}],
         "trans": "barrido", "cam": "deriva", "fuente": "Gobierno: 4.º trim. 2024 – 3.º trim. 2025",
         "el": [
             {"k": "icono", "n": "casa", "x": 300, "y": 560, "tam": 0.9, "at": "@terminaron-0.3", "anim": "cae", "color": "teal"},
             {"k": "icono", "n": "casa", "x": 540, "y": 540, "tam": 1.0, "at": "@terminaron-0.15", "anim": "cae"},
             {"k": "icono", "n": "casa", "x": 780, "y": 560, "tam": 0.9, "at": "@terminaron", "anim": "cae", "color": "yellow"},
             {"k": "icono", "n": "check", "x": 860, "y": 420, "tam": 0.9, "at": "@protegidas"},
             {"k": "num", "val": 14317, "desde": 0, "dur": 0.8, "px": 190, "y": 880, "at": "@14.317-0.3", "golpe": True, "color": "orange"},
             {"k": "txt", "t": "SUMANDO TODAS\nLAS ADMINISTRACIONES", "px": 48, "y": 1060, "at": "@protegidas"},
         ]},
        {"voz": ["Pero ojo: construir y adjudicar vivienda depende sobre todo de comunidades y ayuntamientos."],
         "pausa": 0.55, "trans": "flash", "cam": "aleja",
         "el": [
             {"k": "icono", "n": "edificio", "x": 230, "y": 650, "tam": 0.75, "at": 0.1, "color": "light"},
             {"k": "txt", "t": "ESTADO", "px": 40, "x": 230, "y": 820, "at": 0.1, "color": "gray"},
             {"k": "icono", "n": "edificio", "x": 540, "y": 650, "tam": 0.85, "at": "@comunidades", "color": "yellow"},
             {"k": "txt", "t": "COMUNIDADES", "px": 42, "x": 540, "y": 840, "at": "@comunidades"},
             {"k": "icono", "n": "edificio", "x": 850, "y": 650, "tam": 0.85, "at": "@ayuntamientos", "color": "yellow"},
             {"k": "txt", "t": "AYUNTAM.", "px": 42, "x": 850, "y": 840, "at": "@ayuntamientos"},
             {"k": "circulo", "x": 695, "y": 720, "rx": 330, "ry": 200, "at": "@ayuntamientos+0.3"},
         ]},
        {"voz": ["Y ahí gobiernan partidos de todos los colores."], "trans": "barrido", "cam": "empuja",
         "el": [
             {"k": "pers", "tipo": "politico", "x": 220, "y": 840, "tam": 1.0, "cara": "duda", "pose": "encoge", "rotulo": "PP", "color_rotulo": "pp",
              "px_rotulo": 60, "anim": "pop", "at": 0.05},
             {"k": "pers", "tipo": "politico", "x": 540, "y": 840, "tam": 1.0, "cara": "duda", "pose": "encoge", "rotulo": "PSOE",
              "color_rotulo": "psoe", "px_rotulo": 60, "anim": "pop", "at": 0.25},
             {"k": "pers", "tipo": "politico", "x": 860, "y": 840, "tam": 1.0, "cara": "duda", "pose": "encoge", "rotulo": "OTROS",
              "color_rotulo": "gray", "px_rotulo": 60, "anim": "pop", "at": 0.45},
             {"k": "txt", "t": "TODOS LOS COLORES", "px": 70, "y": 450, "at": "@colores", "marca": "yellow"},
         ]},
        {"voz": ["Si un Gobierno promete viviendas…", "¿debería estar obligado a publicar cuántas entrega?"], "trans": "zoom", "cam": "empuja",
         "el": [
             {"k": "icono", "n": "casa", "y": 720, "tam": 2.0, "at": 0.05, "hasta": "@obligado-0.2"},
             {"k": "estallido", "r": 340, "y": 700, "color": "yellow", "at": "@obligado-0.15"},
             {"k": "txt", "t": "¿OBLIGADO A\nPUBLICAR\nCUÁNTAS ENTREGA?", "px": 86, "y": 700, "at": "@obligado"},
             {"k": "txt", "t": "SÍ O NO · COMENTA", "px": 60, "y": 1090, "marca": "yellow", "at": "fin-1.1"},
         ]},
    ],
}
