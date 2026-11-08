#!/usr/bin/env python3
"""📜 Historia en la pizarra, cap. 5: «De Alianza Popular al PP» (sábado 14/11/2026, 15:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana). Trilogía de orígenes: PSOE (4), PP (5), Vox (6).
Datos (Partido Popular, historia; Congreso de los Diputados, resultados electorales):
  Octubre de 1976: Manuel Fraga funda Alianza Popular con otros exministros (los «siete magníficos»).
  1977: 16 escaños. 1982: 106 escaños, principal partido de la oposición.
  Enero de 1989 (IX Congreso): AP se refunda como Partido Popular. 1990: José María Aznar, presidente del partido.
  1996: Aznar gana las elecciones (156 escaños). 2000: mayoría absoluta, 183 escaños.
  2011: Rajoy, mayoría absoluta, 186 escaños (el mejor resultado del PP). 2022: Feijóo, presidente del partido.
"""
from _mundo import *  # noqa: F401,F403

F = "Partido Popular · Congreso de los Diputados"
SEPIA = (92, 64, 38)
CAMINO = {"tipo": "carretera", "velocidad": 0.6}


def poste(texto, ano, at, color="azul", **kw):
    return obj("poste", 800, 1340, at, 0.72, entra="nada", dibuja=0.7, sfx="rotulador",
               props={"texto": texto, "numero": str(ano), "color": color}, **kw)


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": SEPIA}, animo="intriga", footnote=F, lines=[
        V("El PP no siempre se llamó PP.", "intriga"),
        V("Nació con otro nombre, lo fundó un exministro de Franco y tardó veinte años en ganar.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@ganar", "general", [540, 920], 0.4, zoom=1.06)],
       elements=[
        rot("HISTORIA EN LA PIZARRA", 540, 430, 0, 70, "blanco"),
        rot("PP", 540, 640, 0.2, 200, "azul", golpe=True, fx=[{"at": "@siempre", "do": "tachar"}], out="@nombre"),
        rot("¿?", 540, 640, "@nombre", 200, "amarillo", golpe=True),
        obj("contador", 540, 860, "@veinte", 0.8, hud=True, entra="pop", sfx="kaching", props={"valor": 20, "sufijo": " AÑOS", "ancho": 560}),
        quien("piz", 860, 0.3, 0.42, "sorpresa", y=1580, entra="der", acciones=[{"at": "@nombre", "cara": "pensativo"}, {"at": "@Franco", "take": True, "cara": "sorpresa"}]),
    ]),
    # 2 · ALIANZA POPULAR
    dict(id="ap", fondo=CAMINO, animo="aventura", trans="barrido", footnote=F, lines=[
        V("1976: Manuel Fraga funda Alianza Popular, con otros exministros. Les llamaban los siete magníficos."),
        V("En 1977, solo 16 escaños. En 1982, ya 106: líder de la oposición.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@1982", "general", [600, 980], 0.5, zoom=1.04)],
       elements=[
        poste("ALIANZA POPULAR", 1976, 0.1, "verde", out="@1977"),
        quien("fraga", 400, "@Fraga-0.3", 0.55, "serio", entra="izq", acciones=[{"at": "@funda", "pose": "senala_arriba"}, {"at": "@magníficos", "cara": "riendo"}]),
        obj("contador", 540, 520, "@magníficos", 0.7, hud=True, entra="pop", sfx="kaching", props={"valor": 7, "sufijo": " MAGNÍFICOS", "ancho": 700}, out="@1977"),
        poste("16 ESCAÑOS", 1977, "@1977", "gris", out="@1982"),
        poste("106 ESCAÑOS", 1982, "@1982", "azul"),
        sello("OPOSICIÓN", "azul", 520, "@oposición"),
    ]),
    # 3 · LA REFUNDACIÓN
    dict(id="refundacion", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="papel", footnote=F, lines=[
        V("Pero no ganaba. Así que en 1989 se refunda: nace el Partido Popular."),
        V("Y en 1990, el presidente de Castilla y León toma el mando: José María Aznar.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Aznar", "general", [540, 1000], 0.5, zoom=1.04)],
       elements=[
        rot("AP", 540, 520, 0, 160, "verde", golpe=True, fx=[{"at": "@refunda", "do": "tachar"}], out="@Partido"),
        rot("PARTIDO POPULAR", 540, 560, "@Partido", 110, "azul", golpe=True),
        etq("1989", 540, 720, "@1989", "amarillo", 0.75, hud=True),
        quien("aznar", 540, "@1990", 0.55, "serio", y=1560, entra="abajo", acciones=[{"at": "@Aznar", "pose": "saluda", "cara": "normal"}]),
        quien("piz", 220, 0, 0.45, "pensativo", y=1560, entra="izq", acciones=[{"at": "@ganaba", "pose": "encoge"}, {"at": "@nace", "cara": "ilusionado"}]),
    ]),
    # 4 · LAS VICTORIAS
    dict(id="victorias", fondo=CAMINO, animo="energia", trans="corte", footnote="Congreso: resultados de 1996, 2000 y 2011", lines=[
        V("1996: por fin gana. En 2000, mayoría absoluta: 183 escaños."),
        V("Y en 2011, con Rajoy, su récord: 186.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@186", "general", [600, 960], 0.4, zoom=1.06)],
       elements=[
        poste("GANA", 1996, 0, "azul", out="@2000"),
        poste("183 ESCAÑOS", 2000, "@2000", "azul", out="@2011"),
        poste("186 ESCAÑOS", 2011, "@2011", "azul"),
        quien("aznar", 400, 0.1, 0.5, "ilusionado", entra="izq", out="@Rajoy", acciones=[{"at": "@gana", "pose": "arriba"}]),
        quien("rajoy", 400, "@Rajoy", 0.5, "ilusionado", entra="izq", acciones=[{"at": "@récord", "pose": "pulgar"}]),
        sello("RÉCORD", "verde", 520, "@186"),
    ]),
    # 5 · HOY
    dict(id="hoy", fondo="calle", animo="curioso", trans="barrido", footnote=F, lines=[
        V("Desde 2022, lo lidera Feijóo. Y el 29N busca lo que no consiguió en 2023: gobernar.", "normal"),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@gobernar", "general", [540, 960], 0.4, zoom=1.05)],
       elements=[
        quien("feijoo", 540, 0, 0.55, "ilusionado", entra="abajo", acciones=[{"at": "@29N", "pose": "senala_arriba"}, {"at": "@gobernar", "pose": "punos"}]),
        etq("DESDE 2022", 540, 520, "@2022", "pp", 0.7, hud=True),
        obj("urna", 860, 780, "@29N", 0.4, hud=True, entra="pop", sfx="pop", props={"llena": 0.5, "texto": "29N"}),
    ]),
    # 6 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Sabías que antes se llamaba Alianza Popular? Te leo."),
        V("Y sigue a Piz: mañana, cómo nació Vox.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@Sabías", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("DE AP A PP", 540, 420, 0, 120, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@Vox", "do": "latir"}]),
        etq("PRÓXIMO: CÓMO NACIÓ VOX", 540, 620, "@mañana", "blanco", 0.55, hud=True),
    ]),
]

if __name__ == "__main__":
    episodio("ap_pp", "De Alianza Popular al PP", scenes,
             {"t": 2.8, "titulo": "El PP no siempre se llamó PP", "capitulo": "📜 Historia en la pizarra · Cap. 5"},
             ["Partido Popular: historia (Alianza Popular 1976, refundación 1989)",
              "Congreso de los Diputados: resultados de 1977, 1982, 1996, 2000 y 2011"],
             ("📜 Historia en la pizarra · Cap. 5\n"
              "🔵 El PP no siempre se llamó PP: nació como Alianza Popular (1976)\n"
              "👔 Lo fundó Manuel Fraga con otros exministros, «los siete magníficos»\n"
              "🔄 1989: se refunda como Partido Popular · 1990: Aznar al mando\n"
              "🏆 2000: 183 escaños · 2011, con Rajoy: 186, su récord\n"
              "💬 ¿Lo sabías? Te leo 👇\n"
              "🔔 Sigue a Piz · Próximo: cómo nació Vox · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Partido Popular (historia) · Congreso de los Diputados (resultados 1977-2011). ¿Ves un error? Dínoslo.",
             ["#PP", "#HistoriaDeEspaña", "#Aznar", "#29N", "#AprendeEnTikTok", "#pizarrapublica"],
             series_tag="HISTORIA EN LA PIZARRA")
