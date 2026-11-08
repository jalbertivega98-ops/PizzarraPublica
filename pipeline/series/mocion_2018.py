#!/usr/bin/env python3
"""📜 Historia en la pizarra, cap. 3: «La única moción que ganó» (miércoles 11/11/2026, 20:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana).
Datos (Congreso de los Diputados, mociones de censura; BOE; Audiencia Nacional):
  Seis mociones de censura desde 1977: 1980 (PSOE contra Suárez), 1987 (AP contra González), 2017 (Podemos contra Rajoy),
    2018 (PSOE contra Rajoy), 2020 (Vox contra Sánchez), 2023 (Vox, candidato Tamames, contra Sánchez). Solo prosperó la de 2018.
  24/5/2018: sentencia de la Gürtel (Audiencia Nacional); el PP, condenado como partícipe a título lucrativo.
  25/5/2018: el PSOE registra la moción. Debate 31/5 y 1/6/2018.
  1/6/2018: 180 síes, 169 noes, 1 abstención. Sánchez presidente sin escaño de diputado (la Constitución no lo exige).
  El PNV, que días antes había apoyado los presupuestos de Rajoy, votó sí.
  Rajoy pasó la tarde del 31/5 fuera del hemiciclo, en un restaurante (ampliamente documentado en prensa).
"""
from _mundo import *  # noqa: F401,F403

F = "Congreso de los Diputados: mociones de censura"
NOCHE = (32, 30, 60)

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": NOCHE}, animo="tension", footnote=F, lines=[
        V("En España ha habido seis mociones de censura.", "intriga"),
        V("Cinco fracasaron. Solo una tumbó a un presidente.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Solo", "general", [540, 900], 0.4, zoom=1.08)],
       elements=[
        rot("HISTORIA EN LA PIZARRA", 540, 430, 0, 70, "blanco"),
        obj("contador", 540, 640, "@seis", 1.0, hud=True, entra="pop", sfx="kaching", props={"valor": 6, "ancho": 380}),
        rot("MOCIONES", 540, 840, "@mociones", 100, "amarillo", golpe=True),
        rot("5 FRACASOS", 540, 1000, "@Cinco", 90, "rojo", golpe=True),
        rot("1 GANÓ", 540, 1120, "@una", 110, "verde", golpe=True),
        quien("piz", 860, "@Cinco", 0.42, "sorpresa", y=1560, entra="der", acciones=[{"at": "@tumbó", "take": True, "cara": "susto"}]),
    ]),
    # 2 · LAS QUE FRACASARON
    dict(id="fracasos", fondo="carretera", animo="aventura", trans="barrido", footnote=F, lines=[
        V("1980, contra Suárez. 1987, contra González."),
        V("2017, contra Rajoy. Y 2020 y 2023, las dos contra Sánchez.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Sánchez", "general", [600, 980], 0.5, zoom=1.04)],
       elements=[
        etq("1980 · SUÁREZ", 540, 420, 0.1, "gris", 0.6, hud=True),
        etq("1987 · GONZÁLEZ", 540, 540, "@1987", "gris", 0.6, hud=True),
        etq("2017 · RAJOY", 540, 660, "@2017", "gris", 0.6, hud=True),
        etq("2020 · SÁNCHEZ", 540, 780, "@2020", "gris", 0.6, hud=True),
        etq("2023 · SÁNCHEZ", 540, 900, "@2023", "gris", 0.6, hud=True),
        sello("FRACASÓ", "rojo", 1080, "@Sánchez"),
        quien("piz", 220, 0, 0.5, "pensativo", entra="nada", acciones=[{"at": "@1987", "mira": "der"}, {"at": "@2017", "pose": "senala"}, {"at": "@dos", "pose": "encoge", "cara": "confundido"}]),
    ]),
    # 3 · LA GÜRTEL
    dict(id="gurtel", fondo="oficina", animo="tension", trans="papel", footnote="Audiencia Nacional, sentencia Gürtel (24/5/2018)", lines=[
        V("Mayo de 2018. Sale la sentencia de la Gürtel: el PP, condenado por beneficiarse de la trama."),
        V("Al día siguiente, el PSOE registra la moción contra Rajoy.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@siguiente", "general", [540, 960], 0.4, zoom=1.05)],
       elements=[
        obj("documento", 540, 700, "@sentencia", 0.75, hud=True, entra="nada", dibujo=0.6, sfx="papel", id="sent",
            props={"titulo": "SENTENCIA", "subtitulo": "CASO GÜRTEL · 24/5/2018", "ancho": 640, "articulos": []}, out="@siguiente"),
        sello("CONDENADO", "rojo", 1040, "@condenado", out="@siguiente"),
        quien("rajoy", 820, 0.2, 0.5, "normal", entra="der", acciones=[{"at": "@condenado", "cara": "preocupado"}, {"at": "@moción", "cara": "serio"}]),
        quien("sanchez", 240, "@PSOE-0.3", 0.5, "normal", entra="izq", acciones=[{"at": "@registra", "pose": "senala"}]),
        obj("documento", 540, 700, "@registra", 0.7, hud=True, entra="pop", dibujo=0.4, sfx="papel",
            props={"titulo": "MOCIÓN DE CENSURA", "subtitulo": "25/5/2018", "ancho": 600, "articulos": []}),
    ]),
    # 4 · LA VOTACIÓN
    dict(id="votacion", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="barrido", footnote=F, lines=[
        V("1 de junio. Hacen falta 176 votos. Salen 180."),
        V("La clave: el PNV, que una semana antes había apoyado los presupuestos de Rajoy.", "intriga", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@PNV", "general", [540, 920], 0.4, zoom=1.06)],
       elements=[
        edif("congreso", 540, 0, 0.5, entra="nada", dibuja=0.6, acciones=[{"at": "@180", "cara": "sorpresa"}]),
        obj("barras", 540, 560, "@176", 0.75, hud=True, entra="nada", dibujo=1.0,
            props={"tope": 200, "barras": [{"texto": "NECESARIOS", "valor": 176, "color": "gris"}, {"texto": "SÍ", "valor": 180, "color": "verde"}]},
            out="@PNV"),
        etq("PNV: SÍ", 540, 560, "@PNV", "verde", 0.75, hud=True),
        etq("UNA SEMANA ANTES: PRESUPUESTOS", 540, 700, "@presupuestos", "amarillo", 0.5, hud=True),
        quien("piz", 860, "@Salen", 0.4, "sorpresa", y=1620, entra="der", hud=True, acciones=[{"at": "@clave", "pose": "senala_arriba", "cara": "idea"}]),
    ]),
    # 5 · RESULTADO
    dict(id="resultado", fondo="calle", animo="curioso", trans="corte", footnote=F, lines=[
        V("Rajoy pasó la tarde anterior en un restaurante, fuera del hemiciclo."),
        V("Y Sánchez llegó a presidente sin ser diputado. La Constitución no lo exige.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Sánchez", "general", [540, 980], 0.5, zoom=1.04)],
       elements=[
        quien("rajoy", 260, 0, 0.5, "normal", entra="izq", out="@Sánchez", acciones=[{"at": "@restaurante", "pose": "encoge", "cara": "pensativo"}]),
        obj("reloj", 760, 760, "@tarde", 0.4, hud=True, entra="pop", sfx="pop", out="@Sánchez"),
        quien("sanchez", 540, "@Sánchez", 0.55, "ilusionado", entra="abajo", acciones=[{"at": "@presidente", "pose": "arriba", "cara": "riendo"}, {"at": "@Constitución", "pose": "senala_arriba"}]),
        sello("SIN ESCAÑO", "amarillo", 520, "@diputado"),
        obj("libro", 860, 760, "@Constitución", 0.4, hud=True, entra="pop", sfx="papel", props={"titulo": "CONSTITUCIÓN", "color": "rojo"}),
    ]),
    # 6 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Fue justa aquella moción? Te leo, con respeto."),
        V("Y sigue a Piz: el viernes, el PSOE cumple 147 años.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@justa", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("¿JUSTA?", 540, 420, 0, 120, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@147", "do": "latir"}]),
        etq("PRÓXIMO: 147 AÑOS DE PSOE", 540, 620, "@viernes", "blanco", 0.55, hud=True),
    ]),
]

if __name__ == "__main__":
    episodio("mocion_2018", "La única moción que ganó", scenes,
             {"t": 3.2, "titulo": "La única moción de censura que ganó", "capitulo": "📜 Historia en la pizarra · Cap. 3"},
             ["Congreso de los Diputados: mociones de censura (1980, 1987, 2017, 2018, 2020 y 2023)",
              "Audiencia Nacional: sentencia del caso Gürtel (24/5/2018)",
              "Congreso: votación del 1/6/2018 (180 sí, 169 no, 1 abstención)"],
             ("📜 Historia en la pizarra · Cap. 3\n"
              "🗳️ 6 mociones de censura en España… y solo 1 ganó\n"
              "⚖️ Mayo de 2018: sentencia Gürtel → el PSOE registra la moción contra Rajoy\n"
              "🔢 Hacían falta 176 votos: salieron 180 · el PNV, clave\n"
              "🪑 Sánchez, presidente sin ser diputado\n"
              "💬 ¿Fue justa? Te leo, con respeto 👇\n"
              "🔔 Sigue a Piz · Próximo: el PSOE cumple 147 años · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Congreso (mociones de censura y votación 1/6/2018) · Audiencia Nacional (sentencia Gürtel, 24/5/2018). ¿Ves un error? Dínoslo.",
             ["#MociónDeCensura", "#HistoriaDeEspaña", "#Rajoy", "#Sánchez", "#AprendeEnTikTok", "#pizarrapublica"],
             series_tag="HISTORIA EN LA PIZARRA")
