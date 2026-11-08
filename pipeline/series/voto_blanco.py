#!/usr/bin/env python3
"""«Votar en blanco no es lo que crees» (domingo 8/11/2026, 20:00).
Pedido por joel el 8/11/2026 («algún dato nuevo… que la gente no sepa»), tema elegido por Claude.
Fuente: Ley Orgánica 5/1985 del Régimen Electoral General (LOREG):
  art. 96: nulos = papeletas no oficiales, sobres con papeletas de candidaturas distintas, papeletas alteradas o tachadas.
           Varias papeletas de la misma candidatura en un sobre = un solo voto válido.
           Sobre sin papeleta = voto en blanco, pero válido (Congreso).
  art. 163.1.a: no entran en el reparto las candidaturas que no llegan al 3 % de los votos válidos emitidos en la
           circunscripción (los votos válidos incluyen los votos en blanco; los nulos no).
Dato de contexto: en provincias pequeñas hace falta mucho más del 3 % para sacar escaño; la barrera solo pesa de verdad
en las circunscripciones grandes (Madrid 37 escaños, Barcelona 32). Lo decimos como «sobre todo», sin cifra.
"""
from _mundo import *  # noqa: F401,F403

AZUL = (28, 52, 110)
F = "LOREG (Ley Orgánica 5/1985), arts. 96 y 163"

scenes = [
    # 1 · GANCHO: Piz mete un sobre vacío
    dict(id="gancho", fondo="colegio", animo="tension", footnote=F, lines=[
        V("¿Votar en blanco es no votar a nadie?", "intriga"),
        V("No exactamente. Tu voto en blanco sí cuenta… y casi nadie sabe a quién perjudica.", "remate", 0.15),
    ], camara=[plano(0, "medio", "piz", 0, aire=220), plano("@exactamente", "medio", "urna", 0.5, aire=180),
               plano("@perjudica", "general", [540, 900], 0.4, zoom=1.06)],
       elements=[
        obj("mesa_electoral", 760, 1340, 0, 0.75, props={"texto": "MESA 1"}, entra="nada"),
        obj("urna", 760, 1020, 0, 0.55, id="urna", entra="nada", props={"llena": 0.35, "texto": "CONGRESO"}),
        quien("piz", 300, 0, 0.62, "pensativo", entra="nada", objeto="papeleta", pose="sostiene", acciones=[
            {"at": "@nadie", "cara": "esceptica"}, {"at": "@exactamente", "x": 520, "dur": 0.7},
            {"at": "@cuenta", "pose": "senala", "objeto": None, "cara": "ilusionado"},
            {"at": "@perjudica", "cara": "sorpresa", "take": True, "mira": "camara"}]),
        rot("EN BLANCO", 540, 470, 0.2, 120, "blanco", golpe=True, out="@perjudica-0.2"),
        rot("¿A QUIÉN PERJUDICA?", 540, 470, "@perjudica", 90, "amarillo", golpe=True),
    ]),
    # 2 · VÁLIDO: entra en la cuenta del 3 %
    dict(id="valido", fondo={"tipo": "plano", "color": AZUL}, animo="curioso", trans="barrido", footnote=F, lines=[
        V("El voto en blanco es un voto válido. Y la ley dice que un partido necesita el 3 % de los votos válidos de tu provincia para entrar en el reparto.", "normal"),
        V("El que no llega, se queda fuera.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@3", "general", [540, 900], 0.5, zoom=1.06)],
       elements=[
        sello("VÁLIDO", "verde", 560, "@válido"),
        obj("senal", 540, 760, "@3", 0.8, hud=True, entra="pop", sfx="golpe", props={"numero": "3 %", "poste": False}),
        rot("BARRERA DEL 3 %", 540, 440, "@3", 96, "amarillo", golpe=True),
        quien("pizon", 300, "@reparto", 0.5, "confundido", y=1560, entra="abajo", acciones=[
            {"at": "@fuera", "cara": "triste", "pose": "caidos"}]),
        etq("FUERA", 780, 1200, "@fuera", "rojo", 0.7, hud=True),
    ]),
    # 3 · EL EJEMPLO: la barrera sube
    dict(id="ejemplo", fondo={"tipo": "plano", "color": AZUL}, animo="tension", trans="papel",
         footnote="Ejemplo sencillo · LOREG art. 163", lines=[
        V("Mira: con 100 votos, la barrera son 3.", "normal"),
        V("Si llegan 10 votos en blanco, ya son 110 válidos, y la barrera sube a 3,3.", "normal", 0.1),
        V("Cada voto en blanco pone el listón un poco más alto a los partidos pequeños.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@blanco", "general", [540, 900], 0.5, zoom=1.05),
               plano("@listón", "general", [540, 960], 0.4)],
       elements=[
        obj("contador", 540, 560, "@100", 0.9, hud=True, entra="pop", sfx="pop", out="@llegan",
            props={"valor": 3, "prefijo": "BARRERA: ", "ancho": 820}),
        obj("contador", 540, 560, "@llegan", 0.9, hud=True, entra="pop", sfx="kaching",
            props={"valor": 3.3, "decimales": 1, "prefijo": "BARRERA: ", "ancho": 820, "desde": 3}),
        obj("papeleta", 300, 900, "@blanco", 0.8, hud=True, entra="cae", sfx="papel"),
        obj("papeleta", 540, 880, "@blanco+0.15", 0.8, hud=True, entra="cae", sfx="papel"),
        obj("papeleta", 780, 900, "@blanco+0.3", 0.8, hud=True, entra="cae", sfx="papel"),
        quien("critica", 540, "@listón-0.4", 0.5, "esceptica", y=1560, entra="abajo", acciones=[
            {"at": "@pequeños", "pose": "senala_arriba", "cara": "sorpresa"}]),
        rot("SUBE EL LISTÓN", 540, 1120, "@listón", 90, "amarillo", golpe=True),
    ]),
    # 4 · EL NULO
    dict(id="nulo", fondo="colegio", animo="comico", trans="corte", footnote=F, lines=[
        V("¿Y el voto nulo? Ese no cuenta para nada. Ni para la barrera, ni para nadie.", "normal"),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@nada", "medio", "piz", 0.4, aire=260)],
       elements=[
        quien("piz", 540, 0, 0.62, "pensativo", entra="nada", acciones=[
            {"at": "@nulo", "pose": "piensa"}, {"at": "@nada", "cara": "vacio", "pose": "encoge"}]),
        obj("papelera", 820, 1250, "@nulo", 0.7, entra="pop", sfx="pop"),
        rot("NULO = NADA", 540, 460, "@nada", 110, "rojo", golpe=True),
    ]),
    # 5 · TRUCOS DEL SOBRE
    dict(id="sobre", fondo={"tipo": "plano", "color": AZUL}, animo="curioso", trans="barrido", footnote=F, lines=[
        V("Y tres cosas que casi nadie sabe. Sobre vacío: voto en blanco.", "normal"),
        V("Dos papeletas iguales en el sobre: vale como una. Dos de partidos distintos, o una tachada: nulo.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@iguales", "general", [540, 920], 0.4, zoom=1.04),
               plano("@como", "general", [540, 960], 0.4)],
       elements=[
        etq("SOBRE VACÍO = BLANCO", 540, 640, "@vacío", "blanco", 0.7, hud=True),
        etq("2 IGUALES = VALE 1", 540, 820, "@iguales", "verde", 0.7, hud=True),
        etq("2 DISTINTAS = NULO", 540, 1000, "@distintos", "rojo", 0.7, hud=True),
        etq("TACHADA = NULO", 540, 1180, "@tachada", "rojo", 0.7, hud=True),
        obj("papeleta", 860, 1380, "@Sobre", 0.6, hud=True, entra="cae", sfx="papel"),
        quien("pizon", 200, "@sabe", 0.45, "confundido", y=1600, entra="abajo", acciones=[
            {"at": "@una", "cara": "sorpresa", "take": True}, {"at": "@nulo", "cara": "idea", "pose": "senala_arriba"}]),
        rot("3 COSAS QUE NO SABÍAS", 540, 420, 0, 84, "amarillo"),
    ]),
    # 6 · EL DATO FINAL: dónde importa
    dict(id="donde", fondo="calle", animo="tension", trans="zoom", footnote="LOREG art. 163 · escaños 2026: Madrid 37, Barcelona 32", lines=[
        V("Eso sí: esa barrera del 3 % pesa sobre todo en provincias grandes, como Madrid o Barcelona.", "normal"),
        V("En las pequeñas, para sacar escaño hace falta mucho más.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@pequeñas", "general", [540, 980], 0.5, zoom=1.04)],
       elements=[
        etq("MADRID · 37", 300, 600, "@Madrid", "amarillo", 0.65, hud=True),
        etq("BARCELONA · 32", 780, 600, "@Barcelona", "amarillo", 0.65, hud=True),
        quien("profe", 540, 0, 0.6, "normal", entra="abajo", acciones=[
            {"at": "@grandes", "pose": "senala_arriba"}, {"at": "@pequeñas", "pose": "jarras", "cara": "serio", "mira": "camara"}]),
        rot("MUCHO MÁS DEL 3 %", 540, 440, "@más", 90, "rojo", golpe=True),
    ]),
    # 7 · FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Tú has votado alguna vez en blanco? Te leo."),
        V("Y sigue a Piz: mañana, Abascal en La Revuelta.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@blanco", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("EN BLANCO", 540, 420, 0, 120, "blanco", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@Revuelta", "do": "latir"}]),
    ]),
]

# Ritmo: cambios extra para que no haya tramos quietos de más de 3 s
EXTRA = {
    "valido": {"el": [obj("libro", 820, 1000, "@ley", 0.6, hud=True, entra="cae", sfx="golpe", props={"titulo": "LEY ELECTORAL", "color": "azul"})],
               "cam": [plano("@provincia", "general", [540, 900], 0.5, zoom=1.08)]},
    "ejemplo": {"el": [etq("110 VÁLIDOS", 540, 1300, "@110", "blanco", 0.6, hud=True, out="@listón")],
                "cam": [plano("@sube", "general", [540, 760], 0.5, zoom=1.1)]},
    "nulo": {"acc": {"piz": [{"at": "@barrera", "pose": "cruzados", "mira": "der"}, {"at": "@nadie", "cara": "burla", "mira": "camara"}]}},
    "donde": {"cam": [plano("@pesa", "general", [540, 900], 0.5, zoom=1.06)]},
    "final": {"acc": {"piz": [{"at": "@votado", "salta": True}]}},
}

for _sc in scenes:
    _ex = EXTRA.get(_sc["id"], {})
    _sc["elements"] += _ex.get("el", [])
    _sc["camara"] += _ex.get("cam", [])
    for _q, _acc in _ex.get("acc", {}).items():
        next(e for e in _sc["elements"] if e.get("id") == _q)["acciones"] += _acc

if __name__ == "__main__":
    episodio("voto_blanco", "Votar en blanco no es lo que crees", scenes,
             {"t": 4.0, "titulo": "Votar en blanco no es lo que crees", "capitulo": None},
             ["Ley Orgánica 5/1985 del Régimen Electoral General, art. 96 (votos nulos y en blanco) y art. 163 (barrera del 3 %)",
              "Reparto de escaños 2026: Madrid 37, Barcelona 32 (Real Decreto de convocatoria)"],
             ("🗳️ Votar en blanco SÍ cuenta… y no como crees\n"
              "✅ Es un voto válido: entra en la cuenta del 3 %\n"
              "📈 Cada voto en blanco sube el listón a los partidos pequeños\n"
              "🗑️ El nulo no cuenta para nada\n"
              "✉️ Sobre vacío = blanco · 2 papeletas iguales = 1 voto · 2 distintas o tachada = nulo\n"
              "💬 ¿Has votado alguna vez en blanco? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuente: Ley Orgánica 5/1985 del Régimen Electoral General (LOREG), arts. 96 y 163. ¿Ves un error? Dínoslo.",
             ["#29N", "#VotoEnBlanco", "#EleccionesGenerales", "#LeyElectoral", "#AprendeEnTikTok", "#pizarrapublica"],
             series_tag="DATOS QUE NO SABÍAS")
