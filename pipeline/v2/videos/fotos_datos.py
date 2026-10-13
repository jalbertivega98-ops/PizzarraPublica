"""Tres fotos con datos para TikTok (un plano = una foto), con las cifras ya verificadas en di08, di09 y di10.

- INE, Población condenada 2025: 15,3 ‰ extranjeros, 6,1 ‰ españoles; 70,2 % de los condenados, españoles.
  REIS (CIS) 2026: a igual edad y sexo, ×1,9.
- INSS, marzo 2026: 829.399 hogares, 495,6 M€, 543 €/hogar; 1 año de residencia legal.
- Interior 2025: 14.875 hechos conocidos (−9,4 %); Cataluña 5.913 (≈40 %).
"""
VIDEO = {
    "slug": "fotos_datos",
    "titulo": "Fotos con datos",
    "serie": "LOS DATOS QUE INCOMODAN",
    "acento": "red",
    "voz": "elevenlabs:Pizarra Pública",
    "sin_subs": True,
    "musica": {"bpm": 120, "tono": 0, "seed": 3},
    "portada": {"t": 1.5, "titulo": "DATOS"},
    "planos": [
        {"voz": ["uno"], "cam": "quieta", "min": 3, "fuente": "INE 2025 · REIS (CIS) 2026",
         "el": [
             {"k": "txt", "t": "Fuente: INE, Población condenada 2025 · REIS (CIS) 2026", "px": 30, "y": 1290, "at": 0, "fuente": "ui", "color": "gray"},
             {"k": "txt", "t": "CONDENADOS POR\nCADA 1.000 ADULTOS", "px": 64, "y": 380, "at": 0, "color": "ink"},
             {"k": "barras", "y": 960, "w": 700, "h": 440, "max": 17, "escalon": 0, "at": 0,
              "items": [{"label": "ESPAÑOLES", "val": 6.1, "color": "blue", "txt": "{v}", "dec": 1},
                        {"label": "EXTRANJEROS", "val": 15.3, "color": "red", "txt": "{v}", "dec": 1}]},
             {"k": "txt", "t": "PERO 7 DE CADA 10\nCONDENADOS SON ESPAÑOLES", "px": 50, "y": 1100, "at": 0, "marca": "yellow"},
             {"k": "txt", "t": "Comparando a igual edad y sexo, la brecha se reduce casi a la mitad", "px": 36, "y": 1210, "at": 0,
              "fuente": "ui", "color": "ink"},
         ]},
        {"voz": ["dos"], "trans": "corte", "cam": "quieta", "min": 3, "fuente": "INSS, nómina de marzo 2026", "acento": "green",
         "el": [
             {"k": "txt", "t": "Fuente: INSS, nómina del IMV de marzo de 2026", "px": 30, "y": 1290, "at": 0, "fuente": "ui", "color": "gray"},
             {"k": "txt", "t": "INGRESO MÍNIMO VITAL", "px": 70, "y": 360, "at": 0, "color": "green"},
             {"k": "txt", "t": "829.399", "px": 170, "y": 560, "at": 0, "color": "ink"},
             {"k": "txt", "t": "HOGARES EN MARZO DE 2026", "px": 46, "y": 670, "at": 0, "marca": "yellow"},
             {"k": "txt", "t": "495,6 M€", "px": 130, "y": 860, "at": 0, "color": "red"},
             {"k": "txt", "t": "EN UN SOLO MES · 543 € POR HOGAR", "px": 40, "y": 960, "at": 0, "color": "ink"},
             {"k": "sello", "t": "NO EXIGE HABER COTIZADO*", "x": 540, "y": 1110, "px": 52, "at": 0, "rot": -5},
             {"k": "txt", "t": "*Salvo 23-29 años: 12 meses de alta. Exige 1 año de residencia legal.", "px": 30, "y": 1215, "at": 0,
              "fuente": "ui", "color": "ink"},
         ]},
        {"voz": ["tres"], "trans": "corte", "cam": "quieta", "min": 3, "fuente": "Ministerio del Interior, 2025",
         "el": [
             {"k": "txt", "t": "Fuente: Ministerio del Interior, Portal Estadístico de Criminalidad 2025", "px": 30, "y": 1290, "at": 0, "fuente": "ui", "color": "gray"},
             {"k": "txt", "t": "OKUPACIÓN EN 2025", "px": 74, "y": 360, "at": 0, "color": "purple"},
             {"k": "txt", "t": "14.875", "px": 190, "y": 570, "at": 0, "color": "ink"},
             {"k": "txt", "t": "DENUNCIAS POR ALLANAMIENTO\nO USURPACIÓN", "px": 44, "y": 700, "at": 0, "marca": "yellow"},
             {"k": "txt", "t": "−9,4 % vs 2024", "px": 80, "y": 860, "at": 0, "color": "green"},
             {"k": "txt", "t": "CASI EL 40 %, EN CATALUÑA", "px": 58, "y": 1000, "at": 0, "color": "red"},
             {"k": "icono", "n": "casa", "x": 540, "y": 1150, "tam": 0.7, "at": 0},
         ]},
    ],
}
