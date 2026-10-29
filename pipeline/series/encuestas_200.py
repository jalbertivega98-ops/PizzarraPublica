#!/usr/bin/env python3
"""«PP y Vox bajan de 200» (29/10/2026). Mundo dibujado: el Congreso, la línea de la mayoría absoluta y la balanza
de bloques con los tres candidatos.

Guion y fuentes: /mnt/project-files/insta/guiones/propuestas_29oct.md (aprobado por joel el 29/10/2026, 17:48 UTC)
  El Independiente (26/10/2026, Ángel Carreño): media de Sigma Dos (El Mundo), SocioMétrica (El Español) y El Ateneo del
    Dato (eldiario.es). PP unos 130 escaños (horquillas 119-135), pierde hasta siete de media en dos semanas; Vox 67 (antes
    65), a un par de décimas del 20 %; PP + Vox 197, primera vez por debajo de 200; PSOE media de 108 (antes desde 104);
    Frente Amplio 14 escaños y 6,8 %. Mayoría absoluta: 176 de 350.
  Son encuestas publicadas antes del accidente de Urda (28/10).
"""
from _mundo import *  # noqa: F401,F403

FE = "Media de Sigma Dos, SocioMétrica y El Ateneo del Dato · El Independiente 26/10/2026"
AZUL = (28, 52, 110)


def barras(at, datos, y=1000, scale=1.15, tope=210, **kw):
    return obj("barras", 540, y, at, scale, hud=True, entra="nada", dibujo=1.4,
               props={"sufijo": "", "decimales": 0, "tope": tope, "barras": [
                   {"texto": t, "valor": v, "color": c} for t, v, c in datos]}, **kw)


scenes = [
    # 1 · GANCHO: el contador de PP + Vox baja de 204 a 197 y cruza el 200
    dict(id="gancho", fondo={"tipo": "plano", "color": AZUL}, animo="tension", footnote=FE, lines=[
        V("PP y Vox siguen sumando mayoría absoluta.", "energia"),
        V("Pero, por primera vez en meses, bajan de 200 escaños.", "remate", 0.15),
        V("Y quedan 31 días.", "intriga", 0.2),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@primera", "general", [540, 900], 0.5, zoom=1.08),
               plano("@31", "general", [540, 960], 0.5)],
       elements=[
        obj("contador", 540, 760, 0, 1.0, hud=True, entra="pop", sfx="kaching", dibujo=2.0,
            props={"valor": 197, "desde": 200, "sufijo": " ESCAÑOS", "ancho": 860},
            acciones=[{"at": "@bajan", "tiembla": True}]),
        rot("PP + VOX", 540, 520, 0.2, 110, "amarillo", golpe=True),
        quien("feijoo", 260, 0.3, 0.7, "normal", y=1560, entra="izq", acciones=[{"at": "@bajan", "cara": "preocupado"}]),
        quien("abascal", 820, 0.4, 0.7, "normal", y=1560, entra="der", acciones=[{"at": "@bajan", "cara": "serio", "pose": "cruzados"}]),
        sello("POR DEBAJO DE 200", "rojo", 960, "@200"),
        etq("29N · QUEDAN 31 DÍAS", 540, 1110, "@31", "blanco", 0.7, hud=True),
    ]),
    # 2 · LA REGLA: el Congreso y la línea de los 176
    dict(id="regla", fondo="calle", animo="curioso", trans="iris", footnote="Constitución: 350 diputados · mayoría absoluta 176", lines=[
        V("Recuerda: el Congreso tiene 350 diputados. Para gobernar solo, hacen falta 176.", "normal"),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@176", "general", [540, 900], 0.5, zoom=1.06)],
       elements=[
        edif("congreso", 540, 0, 0.62, entra="crece", sfx="pop", dibuja=0.8),
        rot("350 ESCAÑOS", 540, 420, "@350", 100, "amarillo", golpe=True, out="@176"),
        rot("MAYORÍA: 176", 540, 420, "@176", 110, "amarillo", golpe=True),
        quien("piz", 860, 0.2, 0.45, "normal", y=1560, entra="der", acciones=[{"at": "@176", "pose": "senala_arriba", "cara": "idea"}]),
    ]),
    # 3 · CADA PARTIDO: barras PP, PSOE, Vox, Frente Amplio
    dict(id="partidos", fondo={"tipo": "plano", "color": AZUL}, animo="curioso", trans="papel", footnote=FE, lines=[
        V("La media de tres encuestas: el PP, unos 130 escaños; pierde hasta siete en dos semanas.", "normal"),
        V("El PSOE sube a 108. Vox, 67, rozando el 20 por ciento. Y el Frente Amplio, 14.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@PSOE", "general", [540, 920], 0.4, zoom=1.04)],
       elements=[
        barras("@PP", [("PP", 130, "pp"), ("PSOE", 108, "psoe"), ("VOX", 67, "vox"), ("F. AMPLIO", 14, "gris")], tope=150),
        etq("PP: −7", 300, 420, "@siete", "rojo", 0.75, hud=True),
        etq("PSOE: SUBE", 780, 420, "@sube", "verde", 0.75, hud=True),
        etq("VOX ≈ 20 %", 540, 540, "@rozando", "amarillo", 0.75, hud=True),
        quien("piz", 1250, "@Vox-0.5", 0.4, "pensativo", y=1660, entra="nada", acciones=[
            {"at": "@Vox-0.5", "x": 930, "dur": 0.5}, {"at": "@20", "cara": "sorpresa", "take": True}]),
    ]),
    # 4 · LOS BLOQUES: la balanza PP + Vox contra la línea de 176
    dict(id="bloques", fondo={"tipo": "plano", "color": "amarillo"}, animo="tension", trans="barrido", footnote=FE, lines=[
        V("Juntos, PP y Vox suman 197. Les sobran 21 para la mayoría.", "normal"),
        V("Hace dos semanas pasaban de 200. El colchón se está encogiendo.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@colchón", "general", [540, 900], 0.5, zoom=1.08)],
       elements=[
        barras("@Juntos", [("PP + VOX", 197, "pp"), ("MAYORÍA", 176, "gris")]),
        rot("197", 540, 420, "@197", 130, "amarillo", golpe=True, out="@sobran"),
        rot("+21", 540, 420, "@sobran", 130, "verde", golpe=True, out="@Hace"),
        rot("ANTES: MÁS DE 200", 540, 420, "@Hace", 100, "tinta", golpe=True, out="@colchón"),
        rot("EL COLCHÓN ENCOGE", 540, 420, "@colchón", 80, "rojo", golpe=True),
        quien("piz", 1250, "@colchón-0.5", 0.45, "preocupado", y=1660, entra="nada", hud=True, acciones=[
            {"at": "@colchón-0.5", "x": 900, "dur": 0.5}, {"at": "@encogiendo", "pose": "encoge", "mira": "camara"}]),
    ]),
    # 5 · OJO: antes de Urda; las encuestas no votan
    dict(id="ojo", fondo={"tipo": "plano", "color": AZUL}, animo="curioso", trans="corte",
         footnote="Encuestas publicadas el 26/10/2026, antes del accidente de Urda (28/10)", lines=[
        V("Ojo: estas encuestas se hicieron antes del accidente de Urda. Y las encuestas no votan.", "normal"),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        obj("calendario", 540, 820, 0, 0.8, hud=True, entra="pop", sfx="papel",
            props={"mes": "OCTUBRE", "inicio": 3, "dias": 31, "marcados": [26, 28], "colores": {26: "azul", 28: "rojo"}}),
        etq("26 · ENCUESTAS", 300, 1260, "@encuestas", "azul", 0.65, hud=True),
        etq("28 · URDA", 780, 1260, "@Urda", "rojo", 0.65, hud=True),
        sello("LAS ENCUESTAS NO VOTAN", "naranja", 1420, "@votan"),
    ]),
    # 6 · FINAL: pregunta y sígueme
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Crees que en un mes esto se da la vuelta? Te leo.", "normal"),
        V("Y sígueme: hasta el 29N te cuento cada encuesta con datos.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sígueme", "medio", "piz", 0.5, aire=300)],
       elements=[
        edif("congreso", 540, 0, 0.5, entra="nada"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@mes", "salta": True, "cara": "sorpresa"}, {"at": "@vuelta", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sígueme", "pose": "saluda", "cara": "riendo"}]),
        rot("¿SE DA LA VUELTA?", 540, 420, "@vuelta", 96, "amarillo", golpe=True, out="@sígueme-0.3"),
        rot("SÍGUEME", 540, 420, "@sígueme", 110, "amarillo", fx=[{"at": "@datos", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("encuestas_200", "PP y Vox bajan de 200", scenes,
             {"t": 3.2, "titulo": "PP y Vox bajan de 200 escaños", "capitulo": None},
             ["El Independiente (26/10/2026): media de Sigma Dos, SocioMétrica y El Ateneo del Dato",
              "Mayoría absoluta del Congreso: 176 de 350 diputados",
              "Encuestas publicadas antes del accidente de Urda (28/10/2026)"],
             ("📉 PP y Vox siguen sumando mayoría… pero bajan de 200 escaños por primera vez en meses\n"
              "🔵 PP ~130 (−7 en dos semanas) · 🟢 Vox 67, rozando el 20 %\n"
              "🔴 PSOE sube a 108 · Frente Amplio 14\n"
              "🏛️ Mayoría absoluta: 176. A PP + Vox les sobran 21\n"
              "⚠️ Encuestas hechas antes del accidente de Urda\n"
              "💬 ¿Se da la vuelta en un mes? Te leo 👇\n"
              "🔔 Sígueme para no perderte nada hasta el 29N · 📚 Fuentes en comentarios"),
             "📚 Fuente: media de Sigma Dos (El Mundo), SocioMétrica (El Español) y El Ateneo del Dato (eldiario.es), "
             "recogida por El Independiente 26/10/2026. ¿Ves un error? Dínoslo.",
             ["#29N", "#encuestas", "#elecciones", "#PP", "#PSOE", "#Vox", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
