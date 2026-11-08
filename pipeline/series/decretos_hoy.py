#!/usr/bin/env python3
"""«Mañana se votan los decretos de vivienda» (miércoles 11/11/2026, 20:00; la votación es el jueves 12 y su hora no se conoce).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana).
Fuentes:
  ESdiario 5/11/2026: la Diputación Permanente vota el jueves 12/11, víspera de la campaña. Dos reales decretos-ley
    (aprobados 6/10, BOE 7/10). Decreto 1: freno a desahucios de personas vulnerables, ventajas fiscales a inquilinos y
    algunos propietarios, créditos ICO para la primera vivienda. Decreto 2: prórroga de los alquileres.
  Moncloa.com 17/10/2026: Diputación Permanente de 69: PP 27, PSOE 25, Vox 6, Sumar 6, ERC, PNV, Junts, Bildu y Podemos 1.
    Gobierno y socios 35 (con el PNV) frente a PP, Vox y Junts 34. El PNV puede votar no al de alquileres: lo decide un voto.
  Pleno del 2/10/2026: tumbó dos textos parecidos (PP, Vox, Junts y UPN en contra; el PNV también contra el de alquileres).
"""
from _mundo import *  # noqa: F401,F403

F = "ESdiario 5/11/2026 · Moncloa.com 17/10/2026"

scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo="calle", animo="tension", footnote=F, lines=[
        V("Mañana se decide si tu alquiler se alarga o no.", "intriga"),
        V("Y puede depender de un solo voto.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@solo", "general", [540, 920], 0.4, zoom=1.1)],
       elements=[
        edif("piso", 260, 0, 0.45, entra="crece", sfx="pop", id="casa"),
        obj("contrato", 760, 700, "@alquiler", 0.6, hud=True, entra="pop", sfx="papel"),
        quien("piz", 700, 0.2, 0.5, "pensativo", entra="der", acciones=[{"at": "@alarga", "pose": "senala_izq", "mira": "casa"}, {"at": "@solo", "cara": "sorpresa", "take": True}]),
        rot("1 VOTO", 540, 430, "@voto", 140, "amarillo", golpe=True),
    ]),
    # 2 · QUÉ SE VOTA
    dict(id="que", fondo="oficina", animo="curioso", trans="papel", footnote="ESdiario 5/11/2026 · BOE 7/10/2026", lines=[
        V("Son dos decretos del Gobierno. El primero: frenar desahucios de familias vulnerables, ventajas fiscales y créditos para tu primera casa."),
        V("El segundo: prorrogar los alquileres.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@segundo", "general", [540, 960], 0.4, zoom=1.05)],
       elements=[
        obj("checklist", 540, 720, "@primero", 1.0, hud=True, entra="pop", sfx="papel",
            props={"items": ["FRENO A DESAHUCIOS", "VENTAJAS FISCALES", "CRÉDITOS 1.ª CASA"], "marcas": []}, out="@segundo"),
        obj("documento", 540, 760, "@segundo", 1.1, hud=True, entra="pop", dibujo=0.5, sfx="papel",
            props={"titulo": "DECRETO 2", "subtitulo": "PRÓRROGA DE ALQUILERES", "ancho": 640, "articulos": []}),
        quien("sanchez", 860, 0.2, 0.42, "normal", y=1580, entra="der", acciones=[{"at": "@desahucios", "pose": "senala_izq"}, {"at": "@segundo", "pose": "pulgar"}]),
        etq("YA TUMBADOS EL 2/10", 540, 1180, "@prorrogar", "rojo", 0.55, hud=True),
    ]),
    # 3 · LAS CUENTAS
    dict(id="cuentas", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="barrido", footnote="Moncloa.com 17/10/2026", lines=[
        V("No vota el pleno: vota la Diputación Permanente, 69 diputados."),
        V("PSOE y sus socios suman 34. PP, Vox y Junts, otros 34.", "normal", 0.1),
        V("Y en medio, un voto: el del PNV.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@PNV", "general", [540, 900], 0.4, zoom=1.08)],
       elements=[
        edif("congreso", 540, 0, 0.45, entra="nada", dibuja=0.6, id="cong"),
        obj("contador", 540, 520, "@69", 0.8, hud=True, entra="pop", sfx="kaching", props={"valor": 69, "sufijo": " DIPUTADOS", "ancho": 720}, out="@socios"),
        obj("barras", 540, 560, "@socios", 0.75, hud=True, entra="nada", dibujo=0.8,
            props={"tope": 40, "barras": [{"texto": "PSOE Y SOCIOS", "valor": 34, "color": "psoe"}, {"texto": "PP + VOX + JUNTS", "valor": 34, "color": "pp"}]},
            out="@PNV"),
        rot("34 · 34", 540, 820, "@Junts", 110, "amarillo", golpe=True, out="@PNV"),
        rot("PNV", 540, 560, "@PNV", 160, "verde", golpe=True),
        quien("piz", 860, "@medio", 0.4, "sorpresa", y=1620, entra="der", hud=True, acciones=[{"at": "@PNV", "take": True}]),
    ]),
    # 4 · QUÉ PUEDE PASAR
    dict(id="pasar", fondo="calle", animo="curioso", trans="corte", footnote="Moncloa.com 17/10/2026 · ESdiario 5/11/2026", lines=[
        V("El PNV ya votó no al de alquileres en octubre. Si repite, ese decreto cae."),
        V("El de los desahucios y los créditos lo tiene más fácil.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        etq("ALQUILERES: EN EL AIRE", 540, 520, "@cae", "rojo", 0.65, hud=True),
        etq("DESAHUCIOS Y CRÉDITOS: MÁS FÁCIL", 540, 660, "@desahucios", "verde", 0.55, hud=True),
        obj("contrato", 300, 900, "@alquileres", 0.55, hud=True, entra="pop", sfx="papel", fx=[{"at": "@cae", "do": "temblar"}]),
        quien("piz", 760, 0, 0.5, "pensativo", entra="der", acciones=[{"at": "@octubre", "pose": "senala_izq"}, {"at": "@cae", "cara": "preocupado"}, {"at": "@fácil", "cara": "normal", "pose": "pulgar"}]),
        sello("SE VOTA MAÑANA", "azul", 1240, "@créditos"),
    ]),
    # 5 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Tú alargarías los alquileres por decreto? Sí o no, te leo."),
        V("Y sigue a Piz para no perderte nada antes del 29N.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        etq("SÍ", 300, 640, "@Sí", "verde", 0.7, hud=True, out="@sigue"),
        etq("NO", 780, 640, "@no", "rojo", 0.7, hud=True, out="@sigue"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@alargarías", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@Piz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("decretos_hoy", "Mañana se votan los decretos de vivienda", scenes,
             {"t": 2.6, "titulo": "Mañana se decide tu alquiler", "capitulo": None},
             ["ESdiario (5/11/2026): votación en la Diputación Permanente el 12/11; contenido de los dos decretos",
              "Moncloa.com (17/10/2026): composición de la Diputación Permanente (69) y aritmética; el PNV, clave",
              "BOE 7/10/2026: reales decretos-ley de vivienda"],
             ("🏠 Mañana, jueves 12, se decide si tu alquiler se alarga\n"
              "📜 Dos decretos: freno a desahucios + créditos 1.ª casa · y prórroga de alquileres\n"
              "🏛️ Vota la Diputación Permanente: 69 diputados\n"
              "⚖️ PSOE y socios 34 · PP, Vox y Junts 34 · el PNV decide\n"
              "💬 ¿Alargarías los alquileres por decreto? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: ESdiario 5/11/2026 · Moncloa.com 17/10/2026 · BOE 7/10/2026. ¿Ves un error? Dínoslo.",
             ["#Vivienda", "#Alquiler", "#Decretos", "#Congreso", "#29N", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
