#!/usr/bin/env python3
"""«Esta noche empieza la campaña» (jueves 12/11/2026, 20:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana).
Fuentes:
  EFE (Infobae, 6/11/2026): la campaña empieza a las 00:00 del día 13.
  LOREG: la campaña dura 15 días y acaba a las 00:00 del día anterior a la votación (art. 51); el 28 es jornada de
    reflexión (art. 53); prohibido publicar encuestas los cinco días anteriores a la votación (art. 69.7: del 24 al 28).
  La Moncloa / Interior: voto por correo, solicitud hasta el 19/11; enviarlo antes del 25/11.
  RTVC / Euronews 22/10/2026: cara a cara Sánchez-Feijóo el lunes 16/11. Demócrata: debate a cuatro el 26/11.
"""
from _mundo import *  # noqa: F401,F403

F = "LOREG · EFE 6/11/2026"
NOCHE = (36, 34, 64)


def cal(at, marcados, colores, **kw):
    return obj("calendario", 540, 600, at, 0.62, hud=True, entra="pop", sfx="papel",
               props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": marcados, "colores": colores}, **kw)


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "calle", "hora": "noche"}, animo="tension", footnote=F, lines=[
        V("A las doce de esta noche empieza oficialmente la campaña.", "intriga"),
        V("Y con ella, cambian las reglas del juego.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@reglas", "general", [540, 940], 0.4, zoom=1.08)],
       elements=[
        obj("reloj", 540, 560, 0, 0.7, hud=True, entra="pop", sfx="pop"),
        rot("00:00", 540, 780, "@doce", 140, "amarillo", golpe=True),
        obj("cartel", 760, 1000, "@campaña", 0.6, entra="cae", sfx="golpe", props={"texto": "¡VÓTAME!", "color": "rojo", "tinta": "blanco"}),
        quien("piz", 280, 0.3, 0.5, "ilusionado", entra="izq", acciones=[{"at": "@campaña", "salta": True}, {"at": "@reglas", "pose": "senala_arriba", "cara": "idea"}]),
    ]),
    # 2 · PEGADA DE CARTELES
    dict(id="carteles", fondo="calle", animo="aventura", trans="barrido", footnote="EFE 6/11/2026", lines=[
        V("A medianoche, la pegada de carteles: el pistoletazo de salida."),
        V("Sánchez, Feijóo y Abascal ya pueden pedir el voto de forma directa. Quince días.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Quince", "general", [540, 960], 0.4, zoom=1.05)],
       elements=[
        obj("cartel", 540, 560, 0.2, 0.7, hud=True, entra="cae", sfx="golpe", props={"texto": "PEGADA DE CARTELES", "color": "amarillo", "tinta": "tinta"}, out="@Sánchez"),
        quien("sanchez", 230, "@Sánchez", 0.46, "ilusionado", entra="izq", acciones=[{"at": "@pedir", "pose": "saluda"}]),
        quien("feijoo", 540, "@Feijóo", 0.46, "ilusionado", entra="abajo", acciones=[{"at": "@voto", "pose": "pulgar"}]),
        quien("abascal", 850, "@Abascal", 0.46, "ilusionado", entra="der", acciones=[{"at": "@directa", "pose": "punos"}]),
        obj("contador", 540, 520, "@Quince", 0.8, hud=True, entra="pop", sfx="kaching", props={"valor": 15, "sufijo": " DÍAS", "ancho": 560}),
    ]),
    # 3 · EL CALENDARIO
    dict(id="calendario", fondo="oficina", animo="curioso", trans="papel", footnote="RTVC 22/10/2026 · Interior · Demócrata", lines=[
        V("Apunta: el lunes 16, cara a cara Sánchez-Feijóo."),
        V("El jueves 19, último día para pedir el voto por correo. Y el 26, debate a cuatro.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        cal(0.1, [16, 19, 26, 29], {16: "azul", 19: "amarillo", 26: "azul", 29: "rojo"}),
        etq("16 · CARA A CARA", 540, 1000, "@16", "azul", 0.6, hud=True, out="@jueves"),
        etq("19 · VOTO POR CORREO", 540, 1000, "@jueves", "amarillo", 0.6, hud=True, out="@26"),
        etq("26 · DEBATE A CUATRO", 540, 1000, "@26", "azul", 0.6, hud=True),
        quien("piz", 860, 0.2, 0.42, "normal", y=1600, entra="der", hud=True, acciones=[{"at": "@Apunta", "pose": "senala_izq"}, {"at": "@19", "cara": "idea"}, {"at": "@cuatro", "pose": "pulgar"}]),
    ]),
    # 4 · ENCUESTAS Y REFLEXIÓN
    dict(id="reglas", fondo={"tipo": "plano", "color": NOCHE}, animo="tension", trans="barrido", footnote="LOREG, arts. 53 y 69.7", lines=[
        V("Desde el martes 24, prohibido publicar encuestas en España."),
        V("El 28, jornada de reflexión: nadie puede pedir el voto. Y el 29, a las urnas.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@urnas", "general", [540, 920], 0.4, zoom=1.06)],
       elements=[
        obj("grafica", 540, 600, "@encuestas-0.3", 0.6, hud=True, entra="pop", sfx="pop", fx=[{"at": "@prohibido", "do": "temblar"}], out="@28"),
        sello("PROHIBIDO", "rojo", 860, "@prohibido", out="@28"),
        obj("cartel", 540, 640, "@28", 0.7, hud=True, entra="cae", sfx="golpe", props={"texto": "REFLEXIÓN", "color": "blanco", "tinta": "tinta"}, out="@29"),
        obj("urna", 540, 760, "@29", 0.6, entra="crece", sfx="pop", props={"llena": 0.6, "texto": "29N"}),
        quien("piz", 860, "@reflexión", 0.42, "pensativo", y=1600, entra="der", hud=True, acciones=[{"at": "@urnas", "salta": True, "cara": "ilusionado"}]),
    ]),
    # 5 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Ya sabes a quién vas a votar, o esperas a la campaña? Te leo."),
        V("Y sigue a Piz: te lo contamos todo, día a día.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        etq("YA LO SÉ", 300, 640, "@sabes", "verde", 0.65, hud=True, out="@sigue"),
        etq("ESPERO", 780, 640, "@esperas", "amarillo", 0.65, hud=True, out="@sigue"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@sabes", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@día", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("empieza_campana", "Esta noche empieza la campaña", scenes,
             {"t": 2.4, "titulo": "Esta noche empieza la campaña", "capitulo": None},
             ["EFE (Infobae, 6/11/2026): la campaña empieza a las 00:00 del 13/11",
              "LOREG: campaña de 15 días (art. 51), jornada de reflexión (art. 53), sin encuestas los 5 días previos (art. 69.7)",
              "La Moncloa / Interior: voto por correo, solicitud hasta el 19/11",
              "RTVC y Euronews (22/10/2026): cara a cara 16/11 · Demócrata: debate a cuatro 26/11"],
             ("📣 Esta noche, a las 00:00, empieza la campaña del 29N\n"
              "🖼️ Pegada de carteles y 15 días para pedir el voto\n"
              "📅 16: cara a cara · 19: último día voto por correo · 26: debate a cuatro\n"
              "🚫 Desde el 24, prohibido publicar encuestas · 28: jornada de reflexión\n"
              "💬 ¿Ya sabes a quién votar? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: LOREG (arts. 51, 53 y 69.7) · EFE 6/11/2026 · Interior (voto por correo) · RTVC 22/10/2026. ¿Ves un error? Dínoslo.",
             ["#29N", "#CampañaElectoral", "#Elecciones", "#VotoPorCorreo", "#PolíticaEspañola", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
