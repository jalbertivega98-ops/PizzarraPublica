#!/usr/bin/env python3
"""📜 Historia en la pizarra, cap. 1: «Siete presidentes en 50 años» (lunes 9/11/2026, 20:00).
Pedido por joel el 8/11/2026; primer capítulo de la serie de historia del plan de la semana (9/11 20:00).
Datos (Moncloa, lista de presidentes del Gobierno; Congreso, mociones de censura):
  Suárez: nombrado por el Rey el 3/7/1976; gana las elecciones de 1977; dimite (efectiva 26/2/1981). ~4 años y 8 meses.
  Calvo-Sotelo: votación de investidura interrumpida por el golpe del 23-F (23/2/1981); investido el 25/2/1981,
    presidente hasta el 2/12/1982 (~1 año y 9 meses). No ganó unas generales.
  González: 2/12/1982 – 5/5/1996, el más largo (~13 años y 5 meses).
  Aznar: 5/5/1996 – 17/4/2004 (~8 años). Zapatero: 17/4/2004 – 21/12/2011 (~7 años y 8 meses).
  Rajoy: 21/12/2011 – 1/6/2018 (~6 años y 5 meses): el único desalojado por una moción de censura (1/6/2018, 180 síes).
  Sánchez: desde el 2/6/2018 por esa moción (~8 años y 5 meses a 9/11/2026).
  Llegaron sin ganar antes unas generales: Suárez (nombrado), Calvo-Sotelo (relevo) y Sánchez (moción).
"""
from _mundo import *  # noqa: F401,F403

SUELO = 1340
F = "La Moncloa: presidentes del Gobierno desde 1976"
CAMINO = {"tipo": "carretera", "velocidad": 0.6}


def poste(texto, ano, at, x=800, color="amarillo"):
    return obj("poste", x, SUELO, at, 0.72, entra="nada", dibuja=0.7, sfx="rotulador",
               props={"texto": texto, "numero": str(ano), "color": color})


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": (60, 40, 20)}, animo="tension", footnote=F, lines=[
        V("En 50 años, España solo ha tenido siete presidentes.", "intriga"),
        V("Y tres llegaron sin haber ganado unas elecciones.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@tres", "general", [540, 900], 0.5, zoom=1.08)],
       elements=[
        obj("contador", 540, 600, 0.2, 1.0, hud=True, entra="pop", sfx="kaching", props={"valor": 7, "ancho": 380}),
        rot("PRESIDENTES", 540, 800, 0.4, 110, "amarillo", golpe=True),
        rot("3 SIN GANAR", 540, 1000, "@tres", 110, "rojo", golpe=True),
        quien("piz", 540, "@tres-0.3", 0.5, "sorpresa", y=1600, entra="abajo", acciones=[{"at": "@elecciones", "take": True}]),
        rot("HISTORIA EN LA PIZARRA", 540, 430, 0, 70, "blanco"),
    ]),
    # 2 · SUÁREZ Y CALVO-SOTELO
    dict(id="suarez", fondo=CAMINO, animo="aventura", trans="barrido", footnote=F, lines=[
        V("1976: Suárez. Lo nombra el Rey; gana las elecciones después, en 1977.", "normal"),
        V("1981: Calvo-Sotelo. Su votación de investidura la interrumpió el golpe del 23-F. Duró un año y nueve meses.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Calvo-Sotelo", "general", [600, 980], 0.5, zoom=1.04)],
       elements=[
        poste("SUÁREZ", 1976, 0.1, 820),
        quien("piz", 220, 0, 0.55, "ilusionado", entra="nada", acciones=[
            {"at": "@nombra", "pose": "senala", "mira": "der"}, {"at": "@1981", "x": 330, "dur": 0.4},
            {"at": "@golpe", "cara": "susto", "take": True}, {"at": "@nueve", "cara": "pensativo"}]),
        obj("corona", 820, 760, "@Rey", 0.5, hud=True, entra="pop", sfx="pop", out="@1981"),
        poste("CALVO-SOTELO", 1981, "@1981", 820, "rojo"),
        pum("23-F", 700, 640, "@golpe", 1.0),
        etq("1 AÑO Y 9 MESES", 540, 480, "@Duró", "amarillo", 0.7, hud=True),
    ]),
    # 3 · GONZÁLEZ, EL RÉCORD
    dict(id="gonzalez", fondo=CAMINO, animo="curioso", trans="corte", footnote=F, lines=[
        V("1982: Felipe González. El récord: más de trece años en la Moncloa.", "energia"),
        V("Nadie lo ha superado.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@récord", "general", [700, 1000], 0.5, zoom=1.06)],
       elements=[
        poste("GONZÁLEZ", 1982, 0, 820, "rojo"),
        obj("contador", 540, 560, "@récord", 0.9, hud=True, entra="pop", sfx="kaching", props={"valor": 13, "prefijo": "+", "sufijo": " AÑOS", "ancho": 700}),
        obj("corona", 820, 760, "@superado", 0.45, hud=True, entra="cae", sfx="golpe"),
        quien("piz", 300, 0, 0.55, "sorpresa", entra="nada", acciones=[{"at": "@récord", "salta": True}, {"at": "@Nadie", "pose": "jarras", "mira": "camara"}]),
    ]),
    # 4 · AZNAR, ZAPATERO, RAJOY
    dict(id="tres", fondo=CAMINO, animo="aventura", trans="barrido", footnote=F, lines=[
        V("1996: Aznar, ocho años. 2004: Zapatero, casi ocho.", "normal"),
        V("2011: Rajoy. Y aquí viene lo raro: es el único al que echaron con una moción de censura.", "intriga", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Rajoy", "general", [600, 1000], 0.5, zoom=1.04),
               plano("@moción", "general", [700, 960], 0.4, zoom=1.08)],
       elements=[
        poste("AZNAR", 1996, 0, 820, "azul"),
        poste("ZAPATERO", 2004, "@2004", 820, "rojo"),
        quien("zapatero", 540, "@Zapatero", 0.5, "riendo", y=1560, entra="abajo", out="@2011", acciones=[{"at": "@ocho", "pose": "saluda"}]),
        poste("RAJOY", 2011, "@2011", 820, "azul"),
        quien("piz", 220, 0, 0.55, "pensativo", entra="nada", acciones=[
            {"at": "@raro", "cara": "idea", "pose": "senala_arriba"}, {"at": "@moción", "cara": "sorpresa", "take": True}]),
        sello("ÚNICA VEZ", "rojo", 600, "@moción"),
    ]),
    # 5 · SÁNCHEZ
    dict(id="sanchez", fondo=CAMINO, animo="tension", trans="corte", footnote=F, lines=[
        V("2018: Sánchez, que llegó justo con esa moción. Lleva casi ocho años y medio.", "normal"),
        V("Si gana el 29N, podría acercarse al récord de González.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@récord", "general", [540, 960], 0.4, zoom=1.04)],
       elements=[
        poste("SÁNCHEZ", 2018, 0, 820, "rojo"),
        quien("sanchez", 480, 0.1, 0.55, "ilusionado", y=1560, entra="abajo", acciones=[{"at": "@moción", "pose": "saluda"}]),
        obj("barras", 540, 760, "@gana", 0.85, hud=True, entra="nada", dibujo=1.0,
            props={"sufijo": " AÑOS", "decimales": 1, "tope": 14, "barras": [
                {"texto": "GONZÁLEZ", "valor": 13.4, "color": "psoe"}, {"texto": "SÁNCHEZ", "valor": 8.4, "color": "psoe"}]}),
    ]),
    # 6 · FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Cuál ha sido el mejor presidente? Te leo, con respeto."),
        V("Y sigue a Piz: próximo capítulo, la noche del 23-F.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@mejor", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("7 PRESIDENTES", 540, 420, 0, 110, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@23-F", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("siete_presidentes", "Siete presidentes en 50 años", scenes,
             {"t": 4.0, "titulo": "Siete presidentes en 50 años", "capitulo": "📜 Historia en la pizarra · Cap. 1"},
             ["La Moncloa: relación de presidentes del Gobierno desde 1976 (fechas de toma de posesión y cese)",
              "Congreso de los Diputados: moción de censura del 1/6/2018 (180 votos a favor), la única que ha prosperado",
              "23-F: el golpe interrumpió la votación de investidura de Calvo-Sotelo (23/2/1981)"],
             ("📜 Historia en la pizarra · Cap. 1\n"
              "🇪🇸 En 50 años, solo 7 presidentes… y 3 llegaron sin ganar unas elecciones\n"
              "👑 Suárez, nombrado por el Rey · ⚡ Calvo-Sotelo y el 23-F\n"
              "🏆 González, el récord: más de 13 años\n"
              "🗳️ Rajoy, el único echado por una moción · Sánchez llegó con ella\n"
              "💬 ¿El mejor presidente? Te leo, con respeto 👇\n"
              "🔔 Sigue a Piz · Próximo: el 23-F · 📚 Fuentes en comentarios"),
             "📚 Fuentes: La Moncloa (presidentes desde 1976) · Congreso (moción de censura 1/6/2018). ¿Ves un error? Dínoslo.",
             ["#HistoriaDeEspaña", "#Presidentes", "#Transición", "#29N", "#AprendeEnTikTok", "#pizarrapublica"],
             series_tag="HISTORIA EN LA PIZARRA")
