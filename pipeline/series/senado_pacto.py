#!/usr/bin/env python3
"""«El pacto del Senado» (31/10/2026, 20:00). Segundo capítulo de «La guerra del Senado» (series/guerra_senado.py): el
pacto PP-Vox para las listas del Senado. Mundo dibujado: el mapa de provincias se ilumina según quién se retira.

Guion y fuentes: /mnt/project-files/insta/guiones/propuestas_31oct.md, propuesta B (joel: «Haz algún tema más», 31/10 16:53 UTC)
  Demócrata (26/10/2026, «Vox incorporates 20 independents in the PP lists…»): pacto hecho público el lunes 26/10; Vox no
    presenta lista en seis (Las Palmas, Santa Cruz de Tenerife, Cádiz, Valencia, Castellón, Baleares) e incorpora a 20
    personas, suplentes incluidos, como independientes en las listas del PP.
  Demócrata/agencias (26/10/2026, «PP and Vox aspire to up to 140 seats…»): el PP no presenta candidatura en Gipuzkoa, Girona y
    Tarragona; Vox presenta un solo candidato en 14 provincias; aspiran a 125-140 senadores (fuentes de la negociación,
    anónimas → sello «SEGÚN FUENTES DEL PACTO»); Vox no obtuvo ningún senador elegido en 2023.
  2023: PP 120 senadores elegidos (Infobae 17/10/2026, como en guerra_senado). PSOE y Frente Amplio: «Senado de Progreso».
  Veto del Senado por mayoría absoluta: art. 90 de la Constitución (el Congreso puede levantarlo).
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
CENTRO = P(R, -3.7, 40.0)
VOX_FUERA = ["Las Palmas", "Santa Cruz de Tenerife", "Cádiz", "Valencia", "Castellón", "Baleares"]
PP_FUERA = ["Gipuzkoa", "Gerona", "Tarragona"]
VOX_UNO = ["Sevilla", "Huelva", "Asturias", "Badajoz", "Álava", "Navarra", "Cáceres", "Huesca", "Zaragoza", "Alicante",
           "Granada", "Cuenca", "Pontevedra", "Jaén"]
FD = "Demócrata, 26/10/2026"
TODAS = ['Albacete', 'Alicante', 'Almería', 'Asturias', 'Badajoz', 'Baleares', 'Barcelona', 'Bizkaia', 'Burgos', 'Cantabria',
         'Castellón', 'Ceuta', 'Ciudad Real', 'Cuenca', 'Cáceres', 'Cádiz', 'Córdoba', 'Gerona', 'Gipuzkoa', 'Granada', 'Guadalajara',
         'Huelva', 'Huesca', 'Jaén', 'La Coruña', 'La Rioja', 'Las Palmas', 'León', 'Lugo', 'Lérida', 'Madrid', 'Melilla', 'Murcia',
         'Málaga', 'Navarra', 'Orense', 'Palencia', 'Pontevedra', 'Salamanca', 'Santa Cruz de Tenerife', 'Segovia', 'Sevilla', 'Soria',
         'Tarragona', 'Teruel', 'Toledo', 'Valencia', 'Valladolid', 'Zamora', 'Zaragoza', 'Álava', 'Ávila']


def resto(*grupos):
    dentro = {p for g in grupos for p in g}
    return [p for p in TODAS if p not in dentro]


def sillas(at, colores, x0=330, y=1420, s=0.32, paso=140):
    return [obj("silla", x0 + i * paso, y, f"{at}+{i * 0.15:.2f}", s, entra="cae", sfx="golpe", props={"color": col})
            for i, col in enumerate(colores)]


scenes = [
    # 1 · GANCHO: Feijóo y Abascal se dan la mano; Piz busca a Vox en su papeleta
    dict(id="gancho", fondo="calle", animo="tension", footnote=FD, lines=[
        V("En seis provincias, Vox desaparece de tu papeleta del Senado.", "intriga"),
        V("Y no es un error: es un pacto con el PP.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@pacto", "general", [540, 980], 0.5, zoom=1.06)],
       elements=[
        obj("papeleta", 540, 820, 0, 1.2, entra="crece", sfx="papel", props={"color": "sepia", "texto": "SENADO"}, out="@error"),
        obj("lupa", 700, 760, "@Vox", 0.7, entra="izq", out="@error"),
        rot("¿Y VOX?", 540, 430, "@desaparece", 110, "amarillo", golpe=True, out="@error"),
        quien("piz", 220, 0, 0.5, "confundido", y=1600, entra="abajo", acciones=[
            {"at": "@desaparece", "pose": "encoge", "cara": "sorpresa"}], out="@error"),
        quien("feijoo", -300, "@error", 0.5, "ilusionado", entra="nada", acciones=[
            {"at": "@error", "x": 380, "dur": 0.7}, {"at": "@pacto", "pose": "saluda", "mira": "der"}]),
        quien("abascal", 1380, "@error", 0.5, "ilusionado", entra="nada", acciones=[
            {"at": "@error", "x": 700, "dur": 0.7}, {"at": "@pacto", "pose": "saluda", "mira": "izq"}]),
        rot("PACTO PP + VOX", 540, 430, "@pacto", 96, "amarillo", golpe=True),
        sello("CONFIRMADO", "verde", 1290, "@PP"),
    ]),
    # 2 · RECUERDA: cuatro senadores por provincia, el primero se lleva tres
    dict(id="reglas", fondo="colegio", animo="curioso", trans="papel", footnote="Capítulo 1: «La guerra del Senado»", lines=[
        V("Recuerda: cada provincia elige cuatro senadores, y el que gana suele llevarse tres."),
        V("Si la derecha va dividida, la izquierda puede quedar primera.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@dividida", "general", [540, 1100], 0.6)],
       elements=[
        obj("contador", 540, 460, "@cuatro", 0.6, hud=True, entra="pop", sfx="kaching",
            props={"valor": 4, "sufijo": " SENADORES", "ancho": 760}, out="@dividida"),
        *sillas("@gana", ["azul", "azul", "azul", "rojo"]),
        rot("3 + 1", 540, 1180, "@tres", 120, "amarillo", golpe=True, out="@dividida"),
        rot("¿DIVIDIDOS? PIERDEN", 540, 460, "@dividida", 74, "amarillo", golpe=True),
        quien("piz", 160, 0, 0.5, "pensativo", y=1700, entra="nada", acciones=[
            {"at": "@cuatro", "pose": "senala"}, {"at": "@tres", "cara": "idea"}, {"at": "@izquierda", "cara": "sorpresa"}]),
    ]),
    # 3 · EL PACTO EN EL MAPA: dónde se retira Vox
    dict(id="vox_fuera", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote=FD, lines=[
        V("El lunes 26 lo cerraron. Vox no se presenta en Las Palmas, Tenerife, Cádiz, Valencia, Castellón y Baleares."),
        V("Mete a los suyos como independientes en las listas del PP: veinte nombres, contando suplentes.", "normal", 0.15),
    ], camara=[zoom(0, CENTRO, 1.0, 0), zoom("@Cádiz", P(R, -3.0, 38.5), 1.25, 0.8), zoom("@independientes", CENTRO, 1.0, 0.8)],
       elements=[
        mapa(R, 0, 1.2, acciones=[{"at": "@Palmas", "props": {"resalta": VOX_FUERA[:2], "apaga": resto(VOX_FUERA)}, "sfx": "pop"},
                                  {"at": "@Cádiz", "props": {"resalta": VOX_FUERA[:3], "apaga": resto(VOX_FUERA)}, "sfx": "pop"},
                                  {"at": "@Valencia", "props": {"resalta": VOX_FUERA[:4], "apaga": resto(VOX_FUERA)}, "sfx": "pop"},
                                  {"at": "@Castellón", "props": {"resalta": VOX_FUERA[:5], "apaga": resto(VOX_FUERA)}, "sfx": "pop"},
                                  {"at": "@Baleares", "props": {"resalta": VOX_FUERA, "apaga": resto(VOX_FUERA)}, "sfx": "pop"}]),
        rot("VOX SE RETIRA EN 6", 540, 330, "@presenta", 84, "amarillo", golpe=True, hud=True, out="@independientes"),
        etq("20 DE VOX EN LISTAS DEL PP", 540, 330, "@independientes", "verde", 0.8, hud=True),
        sello("CONFIRMADO", "verde", 1290, "@suplentes"),
    ]),
    # 4 · Y A CAMBIO: el PP se retira en tres; Vox con un solo candidato en catorce
    dict(id="pp_fuera", fondo="mar_mapa", limites=LIM, animo="aventura", trans="corte", footnote=FD, lines=[
        V("A cambio, el PP se retira en Guipúzcoa, Girona y Tarragona."),
        V("Y en otras catorce provincias, Vox lleva un solo candidato. Así a sus votantes les quedan cruces libres para el PP.", "normal", 0.15),
    ], camara=[zoom(0, P(R, -0.5, 42.0), 1.6, 0), zoom("@catorce", CENTRO, 1.0, 0.9), zoom("@candidato", P(R, -4.5, 39.0), 1.15, 1.2)],
       elements=[
        mapa(R, 0, 0.01, progreso=1.0, acciones=[{"at": "@Guipúzcoa", "props": {"resalta": PP_FUERA[:1], "apaga": resto(PP_FUERA)}, "sfx": "pop"},
                                                 {"at": "@Girona", "props": {"resalta": PP_FUERA, "apaga": resto(PP_FUERA)}, "sfx": "pop"},
                                                 {"at": "@catorce", "props": {"resalta": VOX_UNO, "apaga": resto(VOX_UNO)}, "sfx": "kaching"}]),
        rot("EL PP SE RETIRA EN 3", 540, 330, "@retira", 84, "amarillo", golpe=True, hud=True, out="@catorce"),
        rot("VOX: 1 CANDIDATO EN 14", 540, 330, "@catorce", 80, "amarillo", golpe=True, hud=True, out="@cruces"),
        etq("CRUCES LIBRES → PP", 540, 330, "@cruces", "azul", 0.8, hud=True),
    ]),
    # 5 · EL OBJETIVO: de 0 senadores a 125-140 entre los dos
    dict(id="objetivo", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="barrido",
         footnote="Infobae 17/10 (2023) · Demócrata 26/10/2026", lines=[
        V("¿Para qué? En 2023, Vox no sacó ni un senador elegido. El PP, 120."),
        V("Ahora, juntos, aspiran a entre 125 y 140.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@juntos", "general", [540, 900], 0.5, zoom=1.06)],
       elements=[
        obj("barras", 540, 980, "@2023", 1.0, entra="nada", dibuja=1.2, out="@juntos", props={"tope": 208, "decimales": 0, "barras": [
            {"texto": "PP", "valor": 120, "color": "pp"}, {"texto": "VOX", "valor": 0, "color": "vox"}]}),
        rot("2023", 540, 420, "@2023", 110, "amarillo", golpe=True, out="@juntos"),
        rot("125 – 140", 540, 820, "@125", 170, "amarillo", golpe=True),
        rot("SENADORES", 540, 990, "@140", 80, "blanco"),
        sello("SEGÚN FUENTES DEL PACTO", "naranja", 1290, "@aspiran"),
        quien("critica", 880, 0, 0.5, "esceptica", y=1700, entra="nada", acciones=[
            {"at": "@ni", "cara": "sorpresa"}, {"at": "@aspiran", "pose": "cruzados", "cara": "esceptica"}]),
    ]),
    # 6 · ENFRENTE Y QUÉ ESTÁ EN JUEGO: Senado de Progreso y el veto
    dict(id="enfrente", fondo="calle", animo="tension", trans="pan",
         footnote="Constitución, art. 90 · capítulo 1: «Senado de Progreso»", lines=[
        V("Enfrente, PSOE y Frente Amplio van juntos: el «Senado de Progreso»."),
        V("Y quien tenga mayoría absoluta puede vetar leyes y obligar al Congreso a votarlas otra vez.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@mayoría", "general", [540, 950], 0.5, zoom=1.05)],
       elements=[
        quien("sanchez", 300, 0, 0.5, "ilusionado", entra="izq", acciones=[{"at": "@juntos", "pose": "saluda", "mira": "der"}]),
        quien("pizon", 780, 0, 0.5, "ilusionado", entra="der", id="fa", acciones=[{"at": "@juntos", "pose": "saluda", "mira": "izq"}]),
        etq("FRENTE AMPLIO", 780, 900, "@Frente", "rojo", 0.6),
        rot("«SENADO DE PROGRESO»", 540, 430, "@Progreso", 78, "amarillo", golpe=True, out="@mayoría"),
        rot("VETO", 540, 430, "@vetar", 150, "rojo", golpe=True),
        obj("libro", 540, 640, "@leyes", 0.6, hud=True, entra="cae", sfx="golpe", props={"titulo": "LEY", "color": "azul"}),
        etq("VUELVE AL CONGRESO", 540, 820, "@Congreso", "amarillo", 0.7, hud=True),
    ]),
    # 7 · CIERRE: pregunta de debate y «sigue a Piz»
    dict(id="final", fondo="colegio", animo="final", trans="iris", footnote="Te leo en comentarios", lines=[
        V("¿Pacto inteligente o trampa al votante? Te leo en comentarios.", "energia"),
        V("Y sigue a Piz para no perderte nada antes del 29N.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        obj("papeleta", 820, 900, 0, 0.9, entra="nada", props={"color": "sepia", "texto": "SENADO"}, flota=True, out="@sigue"),
        quien("piz", 380, 0, 0.6, "pensativo", entra="abajo", acciones=[
            {"at": "@inteligente", "pose": "piensa", "mira": "camara"}, {"at": "@trampa", "pose": "senala", "mira": "der"},
            {"at": "@leo", "cara": "ilusionado"}, {"at": "@sigue", "pose": "saluda", "cara": "riendo", "salta": True}]),
        rot("¿INTELIGENTE O TRAMPA?", 540, 420, "@Pacto", 70, "amarillo", golpe=True, out="@sigue-0.3"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@29N", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("senado_pacto", "El pacto del Senado", scenes,
             {"t": 2.6, "titulo": "El pacto del Senado: PP y Vox", "capitulo": 2},
             ["Demócrata (26/10/2026): Vox incorpora 20 independientes en las listas del PP al Senado en seis provincias",
              "Demócrata/agencias (26/10/2026): PP y Vox aspiran a hasta 140 senadores; el PP no se presenta en Gipuzkoa, Girona y Tarragona",
              "Infobae (17/10/2026): resultados del Senado en 2023 y «Senado de Progreso»",
              "Constitución española, art. 90: veto del Senado por mayoría absoluta",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("🏛️ El pacto del Senado: PP y Vox (capítulo 2)\n"
              "❌ Vox no se presenta en Las Palmas, Tenerife, Cádiz, Valencia, Castellón y Baleares\n"
              "🤝 Mete a 20 de los suyos (con suplentes) en las listas del PP\n"
              "🔁 A cambio, el PP se retira en Guipúzcoa, Girona y Tarragona\n"
              "✏️ En 14 provincias Vox lleva un solo candidato\n"
              "🎯 Aspiran a 125-140 senadores (según fuentes del pacto). En 2023 Vox sacó 0\n"
              "💬 ¿Pacto inteligente o trampa al votante? Te leo 👇\n"
              "🔔 Sigue a Piz para no perderte nada antes del 29N · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Demócrata 26/10/2026 (dos piezas) · Infobae 17/10/2026 · Constitución, art. 90. ¿Ves un error? Dínoslo.",
             ["#29N", "#Senado", "#PP", "#Vox", "#elecciones", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
