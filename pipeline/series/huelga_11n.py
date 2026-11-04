#!/usr/bin/env python3
"""«Mañana España para» (mar 10/11/2026, 20:00). La huelga general del 11N por la vivienda, a 18 días del 29N.
Aprobado por joel el 4/11/2026 21:21 UTC (propuesta 5 de /mnt/project-files/insta/guiones/propuestas_5nov.md).
Fuentes:
  Moncloa.com 8/10/2026: CCOO, UGT y el Sindicato de Inquilinas; 24 horas; primera gran huelga general de jornada completa
    desde 2012; piden contratos indefinidos, bajadas de precios, impuesto a la riqueza para vivienda pública y expropiar
    pisos vacíos; la CEOE la tacha de «política».
  Ara 7/10/2026: CCOO, UGT, Sindicato de Inquilinas y CGT; Unai Sordo (CCOO): «La vivienda se está comiendo la mitad de los
    salarios de muchas familias».
  Naiz 2/10 y 6/10/2026: el Congreso tumba los decretos de vivienda el 2/10 (PP, Vox, Junts y UPN en contra; 172-178);
    el Gobierno los aprueba otra vez el 6/10 y van a la Diputación Permanente (vota el 12/11 según el guion del 3/11).
  Propuestas: PSOE decretos 6/10 (prórroga de alquileres hasta 2 años, ICO hasta 50.000 €); PP «un millón de viviendas»
    (Contrato con España 19/10, Bendodo 16/10); Vox, sin IVA en la primera vivienda (programa 2025).
"""
from _mundo import *  # noqa: F401,F403

NOCHE = (36, 34, 64)
F_M = "Moncloa.com 8/10/2026 · Ara 7/10/2026"


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo="calle", animo="tension", footnote=F_M, lines=[
        V("Mañana, España para. Veinticuatro horas.", "intriga"),
        V("La primera gran huelga general desde 2012. Y el motivo no es solo el sueldo: es la casa.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@casa", "general", [540, 960], 0.4, zoom=1.06)],
       elements=[
        obj("cartel", 540, 620, 0, 0.9, hud=True, entra="cae", sfx="golpe", props={"texto": "HUELGA GENERAL · 11N", "color": "rojo", "tinta": "blanco"}),
        obj("reloj", 860, 420, "@Veinticuatro", 0.4, hud=True, entra="pop", sfx="pop"),
        quien("piz", 540, 0.2, 0.55, "sorpresa", entra="abajo", acciones=[{"at": "@2012", "take": True}, {"at": "@casa", "pose": "senala", "mira": "casa", "cara": "pensativo"}]),
        edif("piso", 200, "@casa", 0.45, entra="crece", sfx="pop", id="casa"),
        rot("DESDE 2012", 540, 420, "@2012", 90, "amarillo", golpe=True),
    ]),
    # 2 · QUIÉN LA CONVOCA
    dict(id="quien", fondo={"tipo": "plano", "color": NOCHE}, animo="curioso", trans="barrido", footnote=F_M, lines=[
        V("La convocan el Sindicato de Inquilinas, con CCOO, UGT y otros sindicatos."),
        V("El líder de CCOO lo resume así: «la vivienda se está comiendo la mitad de los salarios de muchas familias».", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        etq("INQUILINAS", 540, 520, "@Inquilinas", "amarillo", 0.75, hud=True),
        etq("CCOO", 300, 680, "@CCOO", "rojo", 0.7, hud=True),
        etq("UGT", 780, 680, "@UGT", "rojo", 0.7, hud=True),
        etq("+ OTROS", 540, 820, "@otros", "blanco", 0.6, hud=True, out="@líder"),
        obj("bocadillo", 540, 960, "@líder", 0.75, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["SORDO (CCOO):", "«se come la mitad", "de los salarios»"], "cola": (0, 1)}),
        obj("billete", 540, 1300, "@mitad", 0.8, hud=True, entra="pop", sfx="kaching", fx=[{"at": "@salarios", "do": "temblar"}]),
        sello("DECLARACIÓN", "azul", 1440, "@familias"),
    ]),
    # 3 · QUÉ PIDEN
    dict(id="piden", fondo="calle", animo="curioso", trans="papel", footnote="Moncloa.com 8/10/2026", lines=[
        V("¿Qué piden? Alquileres indefinidos y que bajen los precios."),
        V("Un impuesto a los ricos para hacer vivienda pública. Y expropiar pisos vacíos.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        obj("checklist", 540, 720, 0.2, 0.85, hud=True, entra="pop", sfx="papel",
            props={"items": ["ALQUILER INDEFINIDO", "BAJAR PRECIOS", "IMPUESTO A LA RIQUEZA", "EXPROPIAR VACÍOS"], "marcas": []}),
        quien("pizon", 860, 0.3, 0.45, "pensativo", entra="der", acciones=[{"at": "@ricos", "cara": "sorpresa"}, {"at": "@vacíos", "pose": "piensa"}]),
        edif("abandonado", 220, "@vacíos", 0.4, texto="VACÍO", entra="crece", sfx="pop"),
    ]),
    # 4 · LA POLÍTICA: los decretos
    dict(id="decretos", fondo="oficina", animo="tension", trans="barrido", footnote="Naiz 2/10 y 6/10/2026", lines=[
        V("Y llega en plena pelea por los decretos de vivienda del Gobierno."),
        V("El Congreso los tumbó el 2 de octubre, con PP, Vox y Junts en contra. El Gobierno los volvió a aprobar.", "normal", 0.1),
        V("Y el jueves 12, el día después de la huelga, se votan otra vez.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@jueves", "general", [540, 960], 0.4, zoom=1.06)],
       elements=[
        obj("documento", 540, 720, 0.2, 0.75, hud=True, id="dec", entra="nada", dibujo=0.6, sfx="papel",
            props={"titulo": "DECRETOS", "subtitulo": "VIVIENDA", "ancho": 640, "articulos": []},
            out="@aprobar"),
        rot("172 SÍ · 178 NO", 540, 420, "@tumbó", 80, "rojo", golpe=True, out="@aprobar"),
        rot("APROBADOS OTRA VEZ", 540, 420, "@aprobar", 80, "verde", golpe=True, out="@jueves"),
        obj("calendario", 540, 760, "@jueves", 0.7, hud=True, entra="pop", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [11, 12], "colores": {11: "rojo", 12: "azul"}}),
        etq("11 · HUELGA", 300, 1220, "@huelga", "rojo", 0.6, hud=True),
        etq("12 · VOTACIÓN", 780, 1220, "@votan", "azul", 0.6, hud=True),
    ]),
    # 5 · QUÉ PROPONE CADA PARTIDO
    dict(id="partidos", fondo="calle", animo="curioso", trans="corte",
         footnote="Decretos 6/10 · Contrato con España 19/10 · programa de Vox 2025", lines=[
        V("¿Y los partidos? El PSOE: alargar los alquileres hasta dos años y préstamos para la entrada."),
        V("El PP: un millón de viviendas. Y Vox: quitar el IVA al comprar tu primera casa.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        quien("sanchez", 230, 0, 0.46, "normal", entra="izq", acciones=[{"at": "@alquileres", "pose": "senala"}]),
        etq("ALQUILER +2 AÑOS", 230, 640, "@alquileres", "psoe", 0.55, hud=True),
        quien("feijoo", 540, "@PP", 0.46, "normal", entra="abajo", acciones=[{"at": "@millón", "pose": "senala_arriba"}]),
        etq("1.000.000 DE CASAS", 540, 540, "@millón", "pp", 0.55, hud=True),
        quien("abascal", 850, "@Vox", 0.46, "normal", entra="der", acciones=[{"at": "@IVA", "pose": "punos"}]),
        etq("SIN IVA 1.ª CASA", 850, 640, "@IVA", "vox", 0.55, hud=True),
        sello("PROPUESTAS", "azul", 1240, "@PSOE"),
    ]),
    # 6 · FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("La patronal dice que es una huelga política. Los sindicatos, que es por la casa."),
        V("¿Tú vas a hacer huelga mañana? Sí o no, te leo. Y sigue a Piz.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        etq("CEOE: «POLÍTICA»", 300, 600, "@patronal", "gris", 0.6, hud=True, out="@Tú"),
        etq("SINDICATOS: LA CASA", 780, 600, "@sindicatos", "rojo", 0.6, hud=True, out="@Tú"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@huelga", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        etq("SÍ", 300, 700, "@Sí", "verde", 0.7, hud=True, out="@sigue"),
        etq("NO", 780, 700, "@no", "rojo", 0.7, hud=True, out="@sigue"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@Piz", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("huelga_11n", "Mañana España para", scenes,
             {"t": 1.2, "titulo": "Huelga general: mañana España para", "capitulo": None},
             ["Moncloa.com (8/10/2026): convocantes, 24 h, primera desde 2012, reivindicaciones, CEOE",
              "Ara (7/10/2026): Unai Sordo (CCOO), «la mitad de los salarios»",
              "Naiz (2/10 y 6/10/2026): decretos de vivienda tumbados y aprobados de nuevo",
              "Decretos 6/10/2026 (PSOE) · Contrato con España 19/10/2026 (PP) · programa de Vox 2025"],
             ("✊ Mañana, huelga general · 11N · 24 horas\n"
              "🏠 La primera gran huelga general desde 2012, y el motivo es la vivienda\n"
              "📋 Piden alquileres indefinidos, bajar precios, impuesto a la riqueza y expropiar pisos vacíos\n"
              "🏛️ El jueves 12 se vuelven a votar los decretos de vivienda\n"
              "🔴 PSOE: alquileres +2 años · 🔵 PP: un millón de casas · 🟢 Vox: sin IVA en la 1.ª casa\n"
              "💬 ¿Vas a hacer huelga? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Moncloa.com 8/10/2026 · Ara 7/10 · Naiz 2/10 y 6/10 · decretos 6/10 · Contrato con España (PP) · "
             "programa de Vox 2025. ¿Ves un error? Dínoslo.",
             ["#HuelgaGeneral", "#11N", "#vivienda", "#alquiler", "#29N", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
