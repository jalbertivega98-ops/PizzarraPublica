#!/usr/bin/env python3
"""📜 Historia en la pizarra, cap. 7: «El primer cara a cara» (domingo 15/11/2026, 20:00). Cierre de la serie, víspera del 16/11.
Pedido por joel el 8/11/2026 («adelante» al plan de la semana).
Datos (RTVE Archivo; Antena 3; Telecinco; Congreso, resultados de 1993):
  24/5/1993, Antena 3 (modera Manuel Campo Vidal): primer cara a cara televisado, Felipe González contra José María Aznar.
    La mayoría de encuestas de entonces dieron ganador a Aznar.
  31/5/1993, Telecinco (modera Luis Mariñas): segundo cara a cara; se dio ganador a González.
  6/6/1993: gana González, 159 escaños (pierde la mayoría absoluta).
  No hubo otro cara a cara hasta 2008 (Zapatero contra Rajoy, dos debates).
  16/11/2026: cara a cara Sánchez-Feijóo (RTVC y Euronews, 22/10/2026).
"""
from _mundo import *  # noqa: F401,F403

F = "RTVE Archivo · Antena 3 · Telecinco"
NOCHE = (32, 30, 60)

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plato", "rotulo": "CARA A CARA"}, animo="tension", footnote=F, lines=[
        V("Mañana, Sánchez y Feijóo, cara a cara.", "intriga"),
        V("Pero el primero de la historia fue en 1993. Y el que ganó el debate… no ganó las elecciones.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@1993", "general", [540, 960], 0.4, zoom=1.06)],
       elements=[
        quien("sanchez", 260, 0, 0.48, "normal", entra="izq", out="@1993", acciones=[{"at": "@cara", "pose": "senala"}]),
        quien("feijoo", 820, 0.1, 0.48, "normal", entra="der", out="@1993", acciones=[{"at": "@cara", "pose": "senala_izq"}]),
        rot("HISTORIA EN LA PIZARRA", 540, 430, "@1993", 70, "blanco"),
        rot("1993", 540, 580, "@1993", 150, "amarillo", golpe=True),
        quien("piz", 540, "@ganó", 0.5, "sorpresa", entra="abajo", acciones=[{"at": "@elecciones", "take": True, "cara": "susto"}]),
    ]),
    # 2 · EL PRIMER DEBATE
    dict(id="primero", fondo={"tipo": "plato", "rotulo": "ANTENA 3 · 1993"}, animo="curioso", trans="barrido", footnote=F, lines=[
        V("24 de mayo de 1993. Antena 3. Felipe González contra José María Aznar."),
        V("Aznar llega como aspirante. Y, según casi todas las encuestas, gana el debate.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@gana", "general", [700, 1000], 0.4, zoom=1.05)],
       elements=[
        etq("24/5/1993", 540, 440, 0.1, "amarillo", 0.7, hud=True),
        quien("gonzalez", 260, "@Felipe-0.3", 0.5, "normal", entra="izq", acciones=[{"at": "@gana", "cara": "preocupado"}]),
        quien("aznar", 820, "@José-0.3", 0.5, "serio", entra="der", acciones=[{"at": "@aspirante", "pose": "senala_izq"}, {"at": "@gana", "pose": "arriba", "cara": "ilusionado"}]),
        sello("GANA AZNAR", "azul", 640, "@debate"),
    ]),
    # 3 · LA REVANCHA
    dict(id="revancha", fondo={"tipo": "plato", "rotulo": "TELECINCO · 1993"}, animo="tension", trans="corte", footnote=F, lines=[
        V("Una semana después, revancha en Telecinco. González sale a por todas."),
        V("Esta vez, el que gana es él.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@él", "general", [360, 1000], 0.4, zoom=1.06)],
       elements=[
        etq("31/5/1993", 540, 440, 0, "amarillo", 0.7, hud=True),
        quien("gonzalez", 260, 0, 0.5, "serio", entra="nada", acciones=[{"at": "@todas", "pose": "punos", "cara": "enfado"}, {"at": "@él", "pose": "arriba", "cara": "ilusionado"}]),
        quien("aznar", 820, 0, 0.5, "normal", entra="nada", acciones=[{"at": "@él", "cara": "preocupado"}]),
        sello("GANA GONZÁLEZ", "rojo", 640, "@gana"),
        pum("1 · 1", 540, 800, "@revancha", 0.8),
    ]),
    # 4 · EL RESULTADO
    dict(id="resultado", fondo={"tipo": "plano", "color": NOCHE}, animo="curioso", trans="barrido", footnote="Congreso: elecciones del 6/6/1993", lines=[
        V("El 6 de junio gana González, con 159 escaños. Pierde la mayoría absoluta, pero sigue."),
        V("Y después, quince años sin un solo cara a cara. Hasta 2008: Zapatero contra Rajoy.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        edif("congreso", 540, 0, 0.45, entra="nada", dibuja=0.6, out="@quince"),
        obj("contador", 540, 520, "@159", 0.9, hud=True, entra="pop", sfx="kaching", props={"valor": 159, "sufijo": " ESCAÑOS", "ancho": 680}, out="@quince"),
        obj("contador", 540, 600, "@quince", 0.9, hud=True, entra="pop", sfx="kaching", props={"valor": 15, "sufijo": " AÑOS SIN DEBATE", "ancho": 860}),
        quien("zapatero", 260, "@2008", 0.45, "normal", y=1560, entra="izq", acciones=[{"at": "@Rajoy", "pose": "senala"}]),
        quien("rajoy", 820, "@Rajoy-0.3", 0.45, "normal", y=1560, entra="der", acciones=[{"at": "@Rajoy", "pose": "senala_izq"}]),
    ]),
    # 5 · CIERRE DE LA SERIE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("Y mañana, otro. ¿Crees que un debate puede cambiar tu voto? Te leo."),
        V("Fin de la serie. Sigue a Piz: mañana te contamos el cara a cara.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        obj("calendario", 540, 560, 0, 0.5, hud=True, entra="pop", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [16], "colores": {16: "azul"}}, out="@Fin"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@debate", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@Sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("FIN DE LA SERIE", 540, 420, "@Fin", 90, "amarillo", golpe=True, out="@Sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@Sigue", 110, "amarillo", fx=[{"at": "@cara", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("debate_1993", "El primer cara a cara", scenes,
             {"t": 3.0, "titulo": "El primer cara a cara de la historia", "capitulo": "📜 Historia en la pizarra · Cap. 7"},
             ["RTVE Archivo: debates González-Aznar en Antena 3 (24/5/1993) y Telecinco (31/5/1993)",
              "Congreso de los Diputados: elecciones del 6/6/1993 (PSOE, 159 escaños)",
              "Debates Zapatero-Rajoy (2008) · RTVC y Euronews (22/10/2026): cara a cara Sánchez-Feijóo el 16/11"],
             ("📜 Historia en la pizarra · Cap. 7 (final)\n"
              "📺 Mañana, cara a cara Sánchez-Feijóo… pero el primero fue en 1993\n"
              "🥊 24/5/1993, Antena 3: González vs Aznar · según las encuestas, gana Aznar\n"
              "🔁 31/5, Telecinco: revancha, y gana González\n"
              "🗳️ 6/6/1993: gana González (159 escaños) · luego, 15 años sin cara a cara\n"
              "💬 ¿Un debate puede cambiar tu voto? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: RTVE Archivo (debates de 1993) · Congreso (elecciones 6/6/1993) · RTVC 22/10/2026 (cara a cara 16/11). ¿Ves un error? Dínoslo.",
             ["#CaraACara", "#HistoriaDeEspaña", "#Debate", "#29N", "#AprendeEnTikTok", "#pizarrapublica"],
             series_tag="HISTORIA EN LA PIZARRA")
