#!/usr/bin/env python3
"""📜 Historia en la pizarra, cap. 4: «El PSOE tiene 147 años» (viernes 13/11/2026, 15:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana). Trilogía de orígenes: PSOE (cap. 4), PP (cap. 5), Vox (cap. 6).
Datos (Fundación Pablo Iglesias; Congreso de los Diputados, histórico de diputados y resultados):
  2/5/1879: 25 personas, en su mayoría tipógrafos, fundan el partido en la Casa Labra (Madrid), con Pablo Iglesias Posse.
  1888: nace el sindicato UGT. 1910: Pablo Iglesias, primer diputado socialista.
  Franquismo: prohibido; congreso de Suresnes (Francia), 1974: Felipe González, secretario general.
  1979: congreso extraordinario, abandona el marxismo como definición oficial.
  28/10/1982: 202 escaños, récord de la democracia; más de 10 millones de votos.
  2026 − 1879 = 147 años: el partido más antiguo de los que se presentan.
"""
from _mundo import *  # noqa: F401,F403

F = "Fundación Pablo Iglesias · Congreso de los Diputados"
SEPIA = (92, 64, 38)
R = "espana"
MAD = P(R, -3.7, 40.4)

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": SEPIA}, animo="intriga", footnote=F, lines=[
        V("El partido que hoy gobierna España nació en una taberna.", "intriga"),
        V("Y de eso hace 147 años.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@147", "general", [540, 900], 0.4, zoom=1.08)],
       elements=[
        rot("HISTORIA EN LA PIZARRA", 540, 430, 0, 70, "blanco"),
        edif("casa", 540, "@taberna-0.4", 0.5, entra="crece", sfx="pop", dibuja=0.8, id="taberna"),
        etq("CASA LABRA · MADRID", 540, 860, "@taberna", "amarillo", 0.6, hud=True, out="@147"),
        obj("contador", 540, 600, "@147", 1.0, hud=True, entra="pop", sfx="kaching", props={"valor": 147, "sufijo": " AÑOS", "ancho": 620}),
        quien("piz", 860, 0.2, 0.42, "sorpresa", y=1580, entra="der", acciones=[{"at": "@taberna", "mira": "taberna", "take": True}, {"at": "@147", "cara": "ilusionado"}]),
    ]),
    # 2 · LA FUNDACIÓN
    dict(id="fundacion", fondo="mar_mapa", limites=LIM, animo="aventura", trans="zoom", footnote=F, lines=[
        V("2 de mayo de 1879. Madrid, Casa Labra. Veinticinco personas, casi todas tipógrafos."),
        V("Las lidera un tal Pablo Iglesias. Sí, el original.", "remate", 0.15),
    ], camara=[zoom(0, P(R, -3.7, 40), 1.0, 0), zoom("@Madrid", MAD, 4.0, 0.9)],
       elements=[
        mapa(R, 0, 1.2),
        obj("chincheta", MAD[0], MAD[1], "@Madrid", 0.5, entra="cae", sfx="pop", props={"diseno": "espana"}),
        etq("2/5/1879", 540, 480, "@1879", "amarillo", 0.75, hud=True),
        obj("contador", 540, 620, "@Veinticinco", 0.7, hud=True, entra="pop", sfx="kaching", props={"valor": 25, "sufijo": " FUNDADORES", "ancho": 720}, out="@lidera"),
        quien("iglesias_posse", 540, "@lidera-0.2", 0.55, "serio", y=1560, entra="abajo", hud=True, acciones=[{"at": "@original", "pose": "saluda", "cara": "normal"}]),
        quien("piz", 880, "@original-0.3", 0.36, "riendo", y=1640, entra="der", hud=True),
    ]),
    # 3 · UGT, DIPUTADO Y PROHIBICIÓN
    dict(id="siglo", fondo="carretera", animo="curioso", trans="barrido", footnote=F, lines=[
        V("1888: crea el sindicato UGT. 1910: Iglesias, primer diputado socialista."),
        V("Con Franco, prohibido. Y en 1974, en Francia, un joven sevillano toma el mando: Felipe González.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Felipe", "general", [600, 980], 0.5, zoom=1.05)],
       elements=[
        obj("poste", 800, 1340, 0.1, 0.72, entra="nada", dibuja=0.7, sfx="rotulador", props={"texto": "UGT", "numero": "1888", "color": "rojo"}, out="@1910"),
        obj("poste", 800, 1340, "@1910", 0.72, entra="nada", dibuja=0.7, sfx="rotulador", props={"texto": "1.er DIPUTADO", "numero": "1910", "color": "amarillo"}, out="@Franco"),
        sello("PROHIBIDO", "rojo", 600, "@prohibido", out="@1974"),
        obj("poste", 800, 1340, "@1974", 0.72, entra="nada", dibuja=0.7, sfx="rotulador", props={"texto": "SURESNES", "numero": "1974", "color": "rojo"}),
        quien("gonzalez", 480, "@Felipe-0.3", 0.5, "ilusionado", y=1560, entra="abajo", acciones=[{"at": "@González", "pose": "saluda"}]),
        quien("piz", 220, 0, 0.5, "pensativo", entra="nada", acciones=[{"at": "@UGT", "pose": "senala"}, {"at": "@prohibido", "cara": "preocupado"}, {"at": "@joven", "cara": "sorpresa"}]),
    ]),
    # 4 · 1982
    dict(id="record", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="energia", trans="corte", footnote="Congreso: elecciones del 28/10/1982", lines=[
        V("En 1979 deja de definirse como marxista. Y en 1982, la gran explosión:"),
        V("202 escaños y más de diez millones de votos. Un récord que nadie ha vuelto a tocar.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@202", "general", [540, 900], 0.4, zoom=1.08)],
       elements=[
        etq("1979 · ADIÓS AL MARXISMO", 540, 500, "@1979", "amarillo", 0.6, hud=True, out="@1982"),
        edif("congreso", 540, "@1982", 0.45, entra="crece", sfx="pop", dibuja=0.6, acciones=[{"at": "@202", "cara": "sorpresa"}]),
        obj("contador", 540, 520, "@202", 1.0, hud=True, entra="pop", sfx="kaching", props={"valor": 202, "sufijo": " ESCAÑOS", "ancho": 700}),
        rot("+10 MILLONES DE VOTOS", 540, 700, "@millones", 80, "blanco", golpe=True),
        sello("RÉCORD", "verde", 860, "@récord"),
    ]),
    # 5 · HOY
    dict(id="hoy", fondo="calle", animo="curioso", trans="barrido", footnote=F, lines=[
        V("En democracia, tres presidentes socialistas: González, Zapatero y Sánchez."),
        V("Entre los tres, casi treinta años en la Moncloa.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@treinta", "general", [540, 960], 0.4, zoom=1.05)],
       elements=[
        quien("gonzalez", 230, "@González-0.3", 0.45, "normal", entra="izq", acciones=[{"at": "@González", "pose": "saluda"}]),
        quien("zapatero", 540, "@Zapatero-0.3", 0.45, "riendo", entra="abajo", acciones=[{"at": "@Zapatero", "pose": "saluda"}]),
        quien("sanchez", 850, "@Sánchez-0.3", 0.45, "ilusionado", entra="der", acciones=[{"at": "@Sánchez", "pose": "saluda"}]),
        rot("3 PRESIDENTES", 540, 460, "@tres", 110, "amarillo", golpe=True, out="@treinta"),
        obj("contador", 540, 520, "@treinta", 0.9, hud=True, entra="pop", sfx="kaching", props={"valor": 29, "prefijo": "CASI ", "sufijo": " AÑOS", "ancho": 700}),
    ]),
    # 6 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Sabías que nació en una taberna? Te leo."),
        V("Y sigue a Piz: mañana, cómo nació el PP.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@taberna", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("147 AÑOS", 540, 420, 0, 120, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@PP", "do": "latir"}]),
        etq("PRÓXIMO: CÓMO NACIÓ EL PP", 540, 620, "@mañana", "blanco", 0.55, hud=True),
    ]),
]

if __name__ == "__main__":
    episodio("psoe_147", "El PSOE tiene 147 años", scenes,
             {"t": 3.0, "titulo": "El PSOE nació en una taberna", "capitulo": "📜 Historia en la pizarra · Cap. 4"},
             ["Fundación Pablo Iglesias: fundación del PSOE (Casa Labra, Madrid, 2/5/1879), UGT (1888)",
              "Congreso de los Diputados: Pablo Iglesias, diputado en 1910; elecciones del 28/10/1982 (202 escaños)",
              "Congreso de Suresnes (1974) y congreso extraordinario de 1979"],
             ("📜 Historia en la pizarra · Cap. 4\n"
              "🍷 El PSOE nació en una taberna de Madrid: Casa Labra, 2 de mayo de 1879\n"
              "✍️ 25 fundadores, casi todos tipógrafos, con Pablo Iglesias (el original)\n"
              "🚫 Prohibido con Franco · 1974: Felipe González toma el mando\n"
              "🏆 1982: 202 escaños, récord que nadie ha tocado\n"
              "💬 ¿Lo sabías? Te leo 👇\n"
              "🔔 Sigue a Piz · Próximo: cómo nació el PP · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Fundación Pablo Iglesias · Congreso de los Diputados (elecciones de 1982). ¿Ves un error? Dínoslo.",
             ["#PSOE", "#HistoriaDeEspaña", "#FelipeGonzález", "#29N", "#AprendeEnTikTok", "#pizarrapublica"],
             series_tag="HISTORIA EN LA PIZARRA")
