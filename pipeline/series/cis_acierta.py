#!/usr/bin/env python3
"""«¿Acierta el CIS?» (16/10/2026). Mundo dibujado: Piz, hombre del tiempo de las encuestas, delante del mapa de España.

Guion y fuentes: docs/series/cinco_mundo/guiones.md · investigación: /mnt/project-files/insta/investigacion/temas5_mundo.md
  CIS, barómetro de octubre de 2026 (publicado 14/10): PSOE 34 / PP 22,2 / Vox 17,1 (CMM, El Debate 14/10).
  Media de encuestas privadas (Colmena de Datos, 3/10/2026): PP 32,6 / PSOE 25,7 / Vox 18,2.
  2023: barómetro CIS de julio (13/07/2023) PSOE 31 / PP 29,6 / Vox 11,7; preelectoral (05/07/2023) PP 31,4 / PSOE 31,2;
    resultado 23J: PP 33,05 / PSOE 31,70 / Vox 12,39 (Interior).
  Críticas: análisis de El País (junio de 2024): sobreestimó al bloque de izquierda en 41 de 42 elecciones desde 2018
    (Maldita 13/06/2025). Comisión del Senado impulsada por el PP con apoyo de Vox (17/07/2024); ley del PP para reformar
    el CIS tomada en consideración en 2025. Tezanos (Congreso, 09/2024): una sociedad «moderadamente de centro-izquierda».
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
MAD = P(R, -3.7, 40.4)
FCIS = "CIS, barómetro de octubre (14/10/2026) · Colmena de Datos, media de encuestas (3/10/2026)"
F23 = "CIS: barómetro 13/07/2023 y preelectoral 05/07/2023 · Interior: resultado del 23J"


def barras3(at, datos, y=1060, scale=1.2, **kw):
    return obj("barras", 540, y, at, scale, hud=True, entra="nada", dibujo=1.4,
               props={"sufijo": "", "decimales": 1, "tope": 40, "barras": [
                   {"texto": t, "valor": v, "color": c} for t, v, c in datos]}, **kw)


CIS26 = [("PSOE", 34, "psoe"), ("PP", 22.2, "pp"), ("VOX", 17.1, "vox")]
MEDIA = [("PSOE", 25.7, "psoe"), ("PP", 32.6, "pp"), ("VOX", 18.2, "vox")]
CIS23 = [("PSOE", 31, "psoe"), ("PP", 29.6, "pp"), ("VOX", 11.7, "vox")]
REAL23 = [("PSOE", 31.7, "psoe"), ("PP", 33.1, "pp"), ("VOX", 12.4, "vox")]  # 31,70 / 33,05 / 12,39 redondeados

scenes = [
    # 1 · GANCHO: Piz, hombre del tiempo, delante del mapa: dos pronósticos opuestos
    dict(id="gancho", fondo="mar_mapa", limites=LIM, animo="tension", footnote=FCIS, lines=[
        V("El CIS da ganador al PSOE por casi 12 puntos.", "energia"),
        V("La media de las demás encuestas, al PP por casi 7.", "energia", 0.1),
        V("¿Quién acierta?", "remate", 0.15),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@PSOE", P(R, -3, 39.6), 1.25, 0.8), zoom("@PP", P(R, -4.5, 40.2), 1.25, 0.8),
               zoom("@acierta", MAD, 1.0, 0.5)],
       elements=[
        mapa(R, 0, 1.4, colores={"espana": (240, 236, 226)}, acciones=[
            {"at": "@PSOE", "props": {"colores": {"espana": (246, 170, 168)}}, "sfx": "pop"},
            {"at": "@PP", "props": {"colores": {"espana": (150, 196, 238)}}, "sfx": "pop"},
            {"at": "@acierta", "props": {"colores": {"espana": (240, 236, 226)}}}]),
        quien("piz", 820, 0.3, 0.6, "ilusionado", y=1560, hud=True, entra="der", acciones=[
            {"at": "@CIS", "pose": "senala_izq", "cara": "ilusionado"},
            {"at": "@media", "pose": "senala_arriba", "cara": "confundido"},
            {"at": "@acierta", "pose": "encoge", "cara": "confundido", "mira": "camara"}]),
        obj("bola", 240, 1440, "@acierta-0.2", 0.6, hud=True, entra="crece", sfx="estrellitas", props={"texto": "?"}),
        rot("CIS: PSOE +11,8", 540, 400, "@PSOE", 90, "rojo", golpe=True, out="@media"),
        rot("ENCUESTAS: PP +6,9", 540, 400, "@media", 86, "azul", golpe=True, out="@acierta"),
        rot("¿QUIÉN ACIERTA?", 540, 400, "@acierta", 100, "amarillo", golpe=True),
    ]),
    # 2 · LOS DOS PRONÓSTICOS: barras del CIS y de la media
    dict(id="pronosticos", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel", footnote=FCIS, lines=[
        V("Barómetro del CIS de octubre: PSOE 34, PP 22,2 y Vox 17,1.", "normal"),
        V("Media de encuestas privadas: PP 32,6, PSOE 25,7 y Vox 18,2.", "normal", 0.2),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@Media", "general", [540, 900], 0.4, zoom=1.04)],
       elements=[
        rot("CIS · OCTUBRE 2026", 540, 420, 0.1, 76, "blanco", out="@Media"),
        barras3("@PSOE", CIS26, out="@Media"),
        rot("MEDIA DE ENCUESTAS", 540, 420, "@Media", 76, "blanco"),
        barras3("@PP#2", MEDIA),
        quien("piz", 1250, "@Vox-0.5", 0.4, "pensativo", y=1660, entra="nada", acciones=[
            {"at": "@Vox-0.5", "x": 930, "dur": 0.5}, {"at": "@Media", "cara": "sorpresa", "take": True},
            {"at": "@18,2", "pose": "cabeza", "cara": "confundido"}]),
    ]),
    # 3 · VIAJE A 2023: el mapa se repinta; lo que dijo el CIS y lo que votó la gente
    dict(id="2023", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote=F23, lines=[
        V("Viajemos a 2023. El barómetro de julio del CIS ponía al PSOE por delante.", "normal"),
        V("Ganó el PP, con el 33 por ciento.", "remate", 0.15),
        V("Eso sí: su gran encuesta preelectoral acertó quién quedaba primero… pero no por cuánto.", "normal", 0.2),
    ], camara=[zoom(0, MAD, 0.9, 0), zoom("@Ganó", MAD, 1.1, 0.6), zoom("@preelectoral", P(R, -3, 39.5), 1.0, 0.6)],
       elements=[
        mapa(R, 0, 0.01, progreso=1.0, colores={"espana": (240, 226, 196)}, acciones=[
            {"at": "@PSOE", "props": {"colores": {"espana": (246, 190, 186)}}},
            {"at": "@Ganó", "props": {"colores": {"espana": (150, 196, 238)}}, "sfx": "kaching"}]),
        rot("JULIO DE 2023", 540, 380, 0, 80, "amarillo", golpe=True),
        barras3("@barómetro", CIS23, y=1180, scale=0.75, out="@Ganó"),
        barras3("@Ganó", REAL23, y=1180, scale=0.75),
        sello("CIS DE JULIO", "rojo", 500, "@barómetro", out="@Ganó"),
        sello("RESULTADO REAL · 23J", "verde", 500, "@Ganó", out="@preelectoral"),
        sello("PREELECTORAL: PP 31,4 · PSOE 31,2", "azul", 500, "@preelectoral"),
        rot("PP: 33 %", 540, 640, "@33", 90, "azul", golpe=True, out="@preelectoral"),
        quien("piz", P(R, -1.5, 38.5)[0], 0, 0.26, "normal", y=P(R, -1.5, 38.5)[1], entra="nada", acciones=[
            {"at": "@Viajemos", "salta": True, "cara": "riendo"}, {"at": "@Ganó", "cara": "sorpresa", "take": True}, {"at": "@ciento", "salta": True, "cara": "riendo"}, {"at": "@gran", "pose": "senala_arriba", "cara": "pensativo"},
            {"at": "@cuánto", "pose": "encoge", "cara": "esceptica"}]),
    ]),
    # 4 · LA POLÉMICA: el dato de El País, la defensa de Tezanos y lo que hacen PP y Vox
    dict(id="polemica", fondo="calle", animo="curioso", trans="iris",
         footnote="El País (06/2024) vía Maldita 13/06/2025 · Tezanos en el Congreso (09/2024) · Senado 17/07/2024", lines=[
        V("Un análisis de El País vio que, desde 2018, el CIS sobreestimó a la izquierda en 41 de 42 elecciones.", "normal"),
        V("Su presidente, Tezanos, responde que refleja una sociedad «moderadamente de centro-izquierda».", "normal", 0.15),
        V("PP y Vox abrieron una comisión en el Senado, y el PP quiere reformarlo por ley.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@41", "general", [540, 760], 0.5, zoom=1.1),
               plano("@Tezanos", "medio", "profe", 0.5, aire=180), plano("@Senado", "general", [540, 1000], 0.6)],
       elements=[
        obj("contador", 540, 520, "@análisis", 0.85, hud=True, entra="pop", sfx="golpe", out="@Tezanos", dibujo=2.6,
            props={"valor": 41, "sufijo": " DE 42", "ancho": 640}),
        sello("ANÁLISIS DE EL PAÍS", "naranja", 700, "@País", out="@Tezanos"),
        quien("piz", -150, 0, 0.55, "pensativo", entra="nada", objeto="lupa", pose="sostiene", out="@Tezanos-0.2", acciones=[
            {"at": 0, "x": 540, "dur": 1.0}, {"at": "@izquierda", "cara": "sorpresa", "take": True},
            {"at": "@41", "objeto": None, "pose": "cabeza", "cara": "susto"}]),
        quien("profe", 300, "@Tezanos-0.3", 0.62, "serio", entra="izq", acciones=[
            {"at": "@responde", "pose": "senala_arriba", "cara": "serio"}, {"at": "@centro-izquierda", "pose": "manos_juntas"}]),
        sello("DECLARACIÓN", "azul", 520, "@responde", out="@PP"),
        rot("TEZANOS, PRESIDENTE DEL CIS", 540, 420, "@Tezanos", 56, "blanco", out="@PP"),
        quien("diputado", 650, "@PP-0.2", 0.55, "normal", id="p2", entra="pop", acciones=[{"at": "@comisión", "pose": "senala_arriba"}]),
        quien("diputado", 900, "@Vox-0.2", 0.55, "normal", id="p3", entra="pop", acciones=[{"at": "@comisión", "pose": "puno"}]),
        obj("atril", 650, SUELO_ATRIL, "@PP-0.2", 0.46, props={"texto": "PP", "color": "pp"}, entra="pop"),
        obj("atril", 900, SUELO_ATRIL, "@Vox-0.2", 0.46, props={"texto": "VOX", "color": "vox"}, entra="pop"),
        rot("COMISIÓN EN EL SENADO", 540, 450, "@comisión", 66, "blanco", golpe=True, out="@reformarlo"),
        rot("PP: REFORMAR EL CIS", 540, 560, "@reformarlo", 70, "blanco", golpe=True),
    ]),
    # 5 · FINAL: la única encuesta que no falla; la urna sobre el mapa
    dict(id="final", fondo="mar_mapa", limites=LIM, animo="final", trans="zoom", footnote="Te leemos en comentarios", lines=[
        V("La única encuesta que no falla se hace el 29 de noviembre.", "normal"),
        V("¿Tú te fías de las encuestas? Te leo.", "normal", 0.15),
        V("Y síguenos para el próximo viaje de Piz.", "energia", 0.15),
    ], camara=[zoom(0, MAD, 2.2, 0), zoom(0.3, MAD, 0.95, 2.0)],
       elements=[
        mapa(R, 0, 0.01, progreso=1.0),
        obj("urna", MAD[0], MAD[1] - 30, "@29", 0.65, entra="cae", sfx="golpe", props={"llena": 0.6, "texto": "29N"}),
        quien("piz", 790, "@fías-0.3", 0.6, "pensativo", y=1500, hud=True, entra="abajo", acciones=[
            {"at": "@encuestas", "pose": "piensa"}, {"at": "@leo", "mira": "camara", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@viaje", "salta": True}]),
        rot("¿TE FÍAS?", 540, 450, "@fías", 120, "amarillo", golpe=True, out="@síguenos-0.3"),
        rot("SÍGUENOS", 540, 450, "@síguenos", 110, "amarillo", fx=[{"at": "@Piz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("cis_acierta", "¿Acierta el CIS?", scenes,
             {"t": 2.4, "titulo": "¿Acierta el CIS?", "capitulo": None},
             ["CIS, barómetro de octubre de 2026 (publicado el 14/10/2026; CMM y El Debate)",
              "Colmena de Datos, media de encuestas de octubre de 2026 (3/10/2026)",
              "CIS: barómetro de julio de 2023 (13/07/2023) y estudio preelectoral (05/07/2023)",
              "Ministerio del Interior: resultados del 23J (2023)",
              "Maldita (13/06/2025): análisis de El País sobre los errores del CIS y la defensa de Tezanos",
              "Comisión del Senado sobre el CIS (Vozpópuli, 17/07/2024)",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("📊 El CIS da al PSOE ganando por casi 12 puntos; la media de encuestas, al PP por casi 7\n"
              "⏪ En julio de 2023, el barómetro del CIS ponía al PSOE delante… y ganó el PP\n"
              "🎯 Su preelectoral sí acertó quién ganaba, pero no por cuánto\n"
              "📰 El País: sobreestimó a la izquierda en 41 de 42 elecciones; Tezanos lo defiende\n"
              "🏛️ PP y Vox: comisión en el Senado; el PP quiere reformarlo\n"
              "💬 ¿Te fías de las encuestas?\n"
              "🔔 Síguenos · 📚 Fuentes en comentarios"),
             "📚 Fuentes: CIS oct. 2026 · Colmena de Datos 3/10 · CIS jul. 2023 y preelectoral · Interior 23J · "
             "Maldita 13/06/2025 · Vozpópuli 17/07/2024. ¿Ves un error? Dínoslo.",
             ["#CIS", "#encuestas", "#29N", "#elecciones", "#Tezanos", "#politica", "#España", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
