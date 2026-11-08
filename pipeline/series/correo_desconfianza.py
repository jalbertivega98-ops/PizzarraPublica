#!/usr/bin/env python3
"""«Abascal no se fía del voto por correo» (sábado 14/11/2026, 20:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana).
Fuentes:
  Infobae 6/11/2026 (directo 29N): Abascal en El gato al agua: no puede garantizar que el voto por correo «va a ser
    salvaguardado»; pide votar en persona con un «esfuerzo extraordinario»; lo admite para quien no tenga alternativa.
  Diario de León (Europa Press/EFE) 6/10/2026: Ayuso (5/10): «Pido a todo el mundo que ni se le ocurra votar por correo».
    Correos (Olga García, directora de Operaciones): «un proceso seguro, transparente y garantista»; «No hay posibilidad
    de manipulación». Envíos con código de barras, trazados y custodiados hasta la mesa.
  Xataka / Diario de León: Feijóo (7/10, Ceuta): «No confío en los directivos de Correos», sí en los carteros.
  Xataka 8/10/2026: el votante se identifica tres veces (al pedirlo, al recogerlo y al enviarlo).
  La Moncloa / Interior: solicitud hasta el 19/11; enviarlo antes del 25/11.
"""
from _mundo import *  # noqa: F401,F403

F = "Infobae 6/11/2026 · Diario de León 6/10/2026"

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo="calle", animo="tension", footnote=F, lines=[
        V("Abascal pide a los suyos que no voten por correo.", "intriga"),
        V("Y no es el único que desconfía.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@único", "general", [540, 960], 0.4, zoom=1.06)],
       elements=[
        obj("contrato", 540, 600, 0, 0.6, hud=True, entra="pop", sfx="papel", fx=[{"at": "@correo", "do": "tachar"}]),
        rot("VOTO POR CORREO", 540, 420, 0.1, 90, "amarillo", golpe=True),
        quien("abascal", 300, 0.2, 0.52, "serio", entra="izq", acciones=[{"at": "@voten", "pose": "senala"}, {"at": "@correo", "pose": "cruzados"}]),
        quien("piz", 820, "@único", 0.45, "sorpresa", y=1560, entra="der", acciones=[{"at": "@desconfía", "cara": "pensativo", "pose": "piensa"}]),
    ]),
    # 2 · QUÉ DIJO
    dict(id="dijo", fondo="plato", animo="curioso", trans="barrido", footnote="Infobae 6/11/2026", lines=[
        V("En El gato al agua dijo que no puede garantizar que el voto por correo vaya a estar salvaguardado."),
        V("Pide ir a votar en persona, con un esfuerzo extraordinario. Por correo, solo si no hay otra opción.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        quien("abascal", 540, 0, 0.52, "serio", entra="nada", acciones=[{"at": "@garantizar", "pose": "encoge"}, {"at": "@persona", "pose": "punos"}, {"at": "@opción", "pose": "senala"}]),
        obj("bocadillo", 540, 520, "@garantizar", 0.65, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["«NO PUEDO", "GARANTIZAR»"], "cola": (0, 1)}, out="@Pide"),
        obj("urna", 860, 760, "@persona", 0.4, hud=True, entra="pop", sfx="pop", props={"llena": 0.5, "texto": "29N"}),
        sello("DECLARACIÓN", "azul", 1240, "@extraordinario"),
    ]),
    # 3 · AYUSO Y FEIJÓO
    dict(id="pp", fondo="calle", animo="curioso", trans="corte", footnote="Diario de León 6/10/2026 · Xataka 8/10/2026", lines=[
        V("Ayuso fue más allá: «pido a todo el mundo que ni se le ocurra votar por correo»."),
        V("Y Feijóo: no confía en los directivos de Correos, pero sí en los carteros.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        etq("AYUSO (PP)", 540, 440, 0.1, "pp", 0.65, hud=True, out="@Feijóo"),
        obj("bocadillo", 540, 600, "@ocurra", 0.6, hud=True, entra="pop", sfx="pop", props={"lineas": ["«NI SE LE OCURRA", "VOTAR POR CORREO»"], "cola": (0, 1)}, out="@Feijóo"),
        quien("feijoo", 540, "@Feijóo-0.3", 0.52, "serio", entra="abajo", acciones=[{"at": "@directivos", "pose": "cruzados"}, {"at": "@carteros", "pose": "pulgar", "cara": "normal"}]),
        quien("piz", 860, 0.2, 0.4, "sorpresa", y=1600, entra="der", hud=True, acciones=[{"at": "@carteros", "cara": "riendo"}]),
    ]),
    # 4 · QUÉ DICE CORREOS
    dict(id="correos", fondo="oficina", animo="curioso", trans="papel", footnote="Diario de León 6/10/2026 · Xataka 8/10/2026", lines=[
        V("Correos responde: «es un proceso seguro, transparente y garantista». «No hay posibilidad de manipulación»."),
        V("Cada sobre va con código de barras y vigilado hasta la mesa. Y tú enseñas el DNI tres veces.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@tres", "general", [540, 960], 0.4, zoom=1.06)],
       elements=[
        etq("CORREOS", 540, 440, 0, "amarillo", 0.7, hud=True),
        sello("DECLARACIÓN", "azul", 620, "@manipulación", out="@código"),
        obj("contrato", 300, 720, "@sobre", 0.5, hud=True, entra="pop", sfx="papel"),
        obj("lupa", 780, 720, "@vigilado", 0.45, hud=True, entra="pop", sfx="pop"),
        obj("contador", 540, 980, "@tres", 0.75, hud=True, entra="pop", sfx="kaching", props={"valor": 3, "sufijo": " VECES DNI", "ancho": 640}),
        quien("piz", 860, "@DNI", 0.4, "normal", y=1620, entra="der", hud=True, acciones=[{"at": "@tres", "pose": "senala_arriba", "cara": "idea"}]),
    ]),
    # 5 · FECHAS
    dict(id="fechas", fondo="calle", animo="curioso", trans="barrido", footnote="La Moncloa / Ministerio del Interior", lines=[
        V("Si vas a votar por correo: pídelo hasta el jueves 19, y envíalo antes del 25."),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        obj("calendario", 540, 640, 0, 0.62, hud=True, entra="pop", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [19, 25, 29], "colores": {19: "amarillo", 25: "rojo", 29: "azul"}}),
        etq("19 · PEDIRLO", 300, 1040, "@19", "amarillo", 0.6, hud=True),
        etq("25 · ENVIARLO", 780, 1040, "@25", "rojo", 0.6, hud=True),
    ]),
    # 6 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Tú te fías del voto por correo? Sí o no, te leo."),
        V("Y sigue a Piz para no perderte nada antes del 29N.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        etq("SÍ", 300, 640, "@Sí", "verde", 0.7, hud=True, out="@sigue"),
        etq("NO", 780, 640, "@no", "rojo", 0.7, hud=True, out="@sigue"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@fías", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@29N", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("correo_desconfianza", "Abascal no se fía del voto por correo", scenes,
             {"t": 2.4, "titulo": "¿Te fías del voto por correo?", "capitulo": None},
             ["Infobae (6/11/2026): Abascal en El gato al agua sobre el voto por correo",
              "Diario de León / Europa Press (6/10/2026): Ayuso; Correos (Olga García) y garantías del proceso",
              "Xataka / Diario de León (oct. 2026): Feijóo (7/10), «no confío en los directivos de Correos»",
              "Xataka (8/10/2026): identificación en tres momentos · Interior: plazos (19/11 y 25/11)"],
             ("📮 Abascal pide no votar por correo: «no puedo garantizar» que esté salvaguardado\n"
              "🔵 Ayuso: «ni se le ocurra» · Feijóo: no se fía de los directivos de Correos, sí de los carteros\n"
              "📦 Correos: «seguro y garantista» · código de barras y DNI 3 veces\n"
              "📅 Si votas por correo: pídelo hasta el 19 y envíalo antes del 25\n"
              "💬 ¿Te fías? Sí o no, te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Infobae 6/11/2026 · Diario de León 6/10/2026 · Xataka 8/10/2026 · Interior. ¿Ves un error? Dínoslo.",
             ["#VotoPorCorreo", "#29N", "#Vox", "#PP", "#Correos", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
