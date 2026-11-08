#!/usr/bin/env python3
"""«Koldo dice que el PP le ofreció un millón» (viernes 13/11/2026, 20:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana).
Fuentes:
  Demócrata 5/11/2026 (11:35 y 18:02, agencias): Koldo García, en prisión, cuenta en la Cadena SER y luego en TVE
    (Mañaneros 360) que un abogado vinculado al PP, Alberto Durán, le ofreció pagar su defensa, ayudar a reducir su
    condena y un millón de euros a cambio de información contra Sánchez, su mujer y Zapatero, «incluso si tenía que mentir».
    Dice que lo rechazó. No ha aportado pruebas públicas.
  PSOE: Rebeca Torró exige explicaciones «de inmediato» a Feijóo: «pura guerra sucia de una gravedad extrema».
  PP (Génova): «absolutamente falso». Ester Muñoz: «Está mintiendo». Lo vincula a la operación de la UCO del mismo día.
  Infobae 6/11/2026 (directo): «Koldo García, en prisión».
Regla: no presentar como hecho lo que es una declaración (sellos DECLARACIÓN / SIN PRUEBAS).
"""
from _mundo import *  # noqa: F401,F403

F = "Demócrata 5/11/2026 (Cadena SER, TVE)"
NOCHE = (34, 30, 58)

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": NOCHE}, animo="tension", footnote=F, lines=[
        V("Un millón de euros por hablar contra Sánchez.", "intriga"),
        V("Eso dice Koldo que le ofrecieron. El PP dice que es mentira.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Koldo", "general", [540, 1000], 0.4, zoom=1.06)],
       elements=[
        obj("fajo", 540, 560, 0, 0.7, hud=True, entra="pop", sfx="kaching"),
        rot("1.000.000 €", 540, 760, 0.3, 130, "amarillo", golpe=True),
        quien("koldo", 260, "@Koldo-0.3", 0.5, "serio", entra="izq", acciones=[{"at": "@ofrecieron", "pose": "senala", "mira": "der"}]),
        etq("PP: «MENTIRA»", 800, 980, "@mentira", "pp", 0.6, hud=True),
        quien("piz", 820, "@PP-0.3", 0.42, "sorpresa", y=1560, entra="der", acciones=[{"at": "@mentira", "pose": "encoge", "cara": "pensativo"}]),
        sello("DECLARACIÓN", "azul", 1100, "@dice"),
    ]),
    # 2 · QUÉ CUENTA KOLDO
    dict(id="cuenta", fondo="oficina", animo="curioso", trans="papel", footnote=F, lines=[
        V("Koldo, en prisión, lo contó en la SER y en TVE."),
        V("Según él, un abogado del PP le ofreció pagar su defensa, rebajar su condena y un millón."),
        V("A cambio de información contra Sánchez, su mujer y Zapatero. «Incluso si tenía que mentir».", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Incluso", "general", [540, 940], 0.4, zoom=1.06)],
       elements=[
        obj("microfono", 220, 720, 0.2, 0.45, hud=True, entra="pop", sfx="pop", out="@abogado"),
        obj("tele", 820, 740, "@TVE", 0.45, hud=True, entra="pop", sfx="pop", props={"texto": "TVE"}, out="@abogado"),
        quien("koldo", 540, 0, 0.5, "serio", entra="nada", acciones=[{"at": "@abogado", "pose": "senala_arriba"}, {"at": "@mentir", "cara": "indignado"}]),
        obj("checklist", 540, 520, "@defensa", 0.75, hud=True, entra="pop", sfx="papel",
            props={"items": ["PAGAR SU DEFENSA", "REBAJAR CONDENA", "1 MILLÓN"], "marcas": []}, out="@cambio"),
        etq("CONTRA SÁNCHEZ · SU MUJER · ZAPATERO", 540, 520, "@cambio", "rojo", 0.5, hud=True),
        rot("«INCLUSO MINTIENDO»", 540, 660, "@Incluso", 90, "amarillo", golpe=True),
    ]),
    # 3 · LO RECHAZÓ, Y SIN PRUEBAS
    dict(id="pruebas", fondo="calle", animo="tension", trans="barrido", footnote=F, lines=[
        V("Dice que lo rechazó. Pero de momento no ha enseñado ninguna prueba."),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@prueba", "general", [540, 960], 0.4, zoom=1.08)],
       elements=[
        quien("koldo", 540, 0, 0.55, "serio", entra="abajo", acciones=[{"at": "@rechazó", "pose": "cruzados"}, {"at": "@prueba", "pose": "encoge", "cara": "pensativo"}]),
        obj("lupa", 820, 620, "@momento", 0.5, hud=True, entra="pop", sfx="pop"),
        sello("SIN PRUEBAS", "rojo", 520, "@prueba"),
    ]),
    # 4 · LAS REACCIONES
    dict(id="reacciones", fondo="plato", animo="tension", trans="corte", footnote=F, lines=[
        V("El PSOE pide explicaciones a Feijóo: «guerra sucia de una gravedad extrema»."),
        V("El PP: «absolutamente falso». Y Ester Muñoz: «está mintiendo».", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        etq("PSOE · REBECA TORRÓ", 300, 420, 0.1, "psoe", 0.5, hud=True),
        obj("bocadillo", 300, 560, "@guerra", 0.6, hud=True, entra="pop", sfx="pop", props={"lineas": ["«GUERRA SUCIA»"], "cola": (0, 1)}, out="@PP"),
        etq("PP · GÉNOVA Y ESTER MUÑOZ", 780, 420, "@PP", "pp", 0.45, hud=True),
        quien("piz", 540, 0, 0.5, "pensativo", y=1500, entra="abajo", acciones=[{"at": "@Feijóo", "mira": "izq"}, {"at": "@PP", "mira": "der", "cara": "sorpresa"}, {"at": "@mintiendo", "pose": "encoge", "mira": "camara"}]),
        obj("bocadillo", 780, 560, "@falso", 0.6, hud=True, entra="pop", sfx="pop", props={"lineas": ["«ABSOLUTAMENTE", "FALSO»"], "cola": (0, 1)}),
        sello("DECLARACIONES", "azul", 1240, "@mintiendo"),
    ]),
    # 5 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("Palabra de Koldo contra palabra del PP. ¿A quién crees? Te leo."),
        V("Y sigue a Piz: aquí, siempre con fuentes.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        etq("KOLDO", 300, 640, "@Koldo", "gris", 0.7, hud=True, out="@sigue"),
        etq("PP", 780, 640, "@PP", "pp", 0.7, hud=True, out="@sigue"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@Koldo", "mira": "izq"}, {"at": "@PP", "mira": "der"}, {"at": "@crees", "pose": "piensa", "mira": "camara"},
            {"at": "@leo", "cara": "ilusionado", "pose": "senala"}, {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@fuentes", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("koldo_millon", "Koldo: «el PP me ofreció un millón»", scenes,
             {"t": 2.6, "titulo": "Koldo: «el PP me ofreció un millón»", "capitulo": None},
             ["Demócrata (5/11/2026, agencias): declaraciones de Koldo García en la Cadena SER y TVE; respuesta del PSOE (Torró) y del PP (Génova, Ester Muñoz)",
              "Infobae (6/11/2026): Koldo García, en prisión"],
             ("💶 Koldo dice que el PP le ofreció 1 millón por hablar contra Sánchez\n"
              "🎙️ Lo contó en la SER y en TVE: defensa pagada, rebaja de condena y un millón\n"
              "🗣️ «Incluso si tenía que mentir» · dice que lo rechazó\n"
              "🔍 De momento, sin pruebas públicas\n"
              "🔴 PSOE: «guerra sucia» · 🔵 PP: «absolutamente falso»\n"
              "💬 ¿A quién crees? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Demócrata 5/11/2026 (Cadena SER, TVE, agencias) · Infobae 6/11/2026. Son declaraciones, no hechos probados. ¿Ves un error? Dínoslo.",
             ["#Koldo", "#PP", "#PSOE", "#29N", "#PolíticaEspañola", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
