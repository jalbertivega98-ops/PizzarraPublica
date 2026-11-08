#!/usr/bin/env python3
"""📜 Historia en la pizarra, cap. 6: «Cómo nació Vox» (domingo 15/11/2026, 15:00).
Pedido por joel el 8/11/2026 («adelante» al plan de la semana). Trilogía de orígenes: PSOE (4), PP (5), Vox (6).
Datos (Ministerio del Interior, resultados electorales; Junta de Andalucía; prensa de la época):
  Diciembre de 2013: lo fundan antiguos miembros del PP; se presenta en enero de 2014 (Vidal-Quadras, Abascal, Ortega Lara…).
  Europeas de mayo de 2014: 1,57 %, sin escaño, por muy poco. Septiembre de 2014: Abascal, presidente.
  Generales de 2015: 0,23 %, cero escaños.
  Andaluzas de diciembre de 2018: 12 escaños, primera vez en un parlamento.
  Generales: abril de 2019, 24 escaños; noviembre de 2019, 52 (tercera fuerza); julio de 2023, 33.
"""
from _mundo import *  # noqa: F401,F403

F = "Ministerio del Interior: resultados electorales"
R = "espana"
SEV = P(R, -5.98, 37.39)


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": (24, 60, 40)}, animo="intriga", footnote=F, lines=[
        V("En 2015, Vox sacó cero escaños.", "intriga"),
        V("Cuatro años después tenía 52. ¿Cómo pasó?", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@52", "general", [540, 900], 0.4, zoom=1.08)],
       elements=[
        rot("HISTORIA EN LA PIZARRA", 540, 430, 0, 70, "blanco"),
        obj("contador", 540, 640, "@cero", 1.0, hud=True, entra="pop", sfx="kaching", props={"valor": 0, "sufijo": " ESCAÑOS", "ancho": 640}, out="@52"),
        obj("contador", 540, 640, "@52", 1.0, hud=True, entra="pop", sfx="kaching", props={"valor": 52, "sufijo": " ESCAÑOS", "ancho": 640}),
        quien("abascal", 760, 0.2, 0.48, "serio", entra="der", acciones=[{"at": "@52", "pose": "punos", "cara": "ilusionado"}]),
        quien("piz", 260, 0.3, 0.45, "pensativo", entra="izq", acciones=[{"at": "@52", "cara": "sorpresa", "take": True}, {"at": "@pasó", "pose": "piensa"}]),
    ]),
    # 2 · NACIMIENTO
    dict(id="nace", fondo="oficina", animo="curioso", trans="papel", footnote=F, lines=[
        V("Nace a finales de 2013, fundado por gente que se va del PP."),
        V("Entre ellos, Vidal-Quadras, Ortega Lara y un tal Santiago Abascal.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Abascal", "general", [540, 980], 0.4, zoom=1.04)],
       elements=[
        etq("DICIEMBRE 2013", 540, 440, 0.1, "verde", 0.7, hud=True),
        rot("PP", 260, 640, "@PP", 120, "azul", golpe=True),
        obj("flecha", 540, 640, "@PP+0.3", 0.5, hud=True, entra="pop", sfx="whoosh"),
        rot("VOX", 820, 640, "@PP+0.6", 120, "verde", golpe=True),
        etq("VIDAL-QUADRAS", 300, 820, "@Vidal-Quadras", "gris", 0.5, hud=True),
        etq("ORTEGA LARA", 780, 820, "@Ortega", "gris", 0.5, hud=True),
        quien("abascal", 540, "@Santiago-0.3", 0.5, "normal", y=1560, entra="abajo", acciones=[{"at": "@Abascal", "pose": "saluda"}]),
    ]),
    # 3 · LOS AÑOS EN BLANCO
    dict(id="blanco", fondo="carretera", animo="curioso", trans="barrido", footnote=F, lines=[
        V("En las europeas de 2014 se queda sin escaño por muy poco. En 2015, un 0,2 por ciento."),
        V("Casi nadie apostaba por él.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        obj("poste", 800, 1340, 0, 0.72, entra="nada", dibuja=0.7, sfx="rotulador", props={"texto": "SIN ESCAÑO", "numero": "2014", "color": "gris"}, out="@2015"),
        obj("poste", 800, 1340, "@2015", 0.72, entra="nada", dibuja=0.7, sfx="rotulador", props={"texto": "0,2 %", "numero": "2015", "color": "gris"}),
        quien("abascal", 380, 0, 0.5, "preocupado", entra="nada", acciones=[{"at": "@poco", "pose": "encoge"}, {"at": "@apostaba", "cara": "serio", "pose": "cruzados"}]),
        sello("0 ESCAÑOS", "rojo", 520, "@ciento"),
    ]),
    # 4 · ANDALUCÍA 2018
    dict(id="andalucia", fondo="mar_mapa", limites=LIM, animo="energia", trans="zoom", footnote="Junta de Andalucía: elecciones del 2/12/2018", lines=[
        V("Hasta diciembre de 2018. Andalucía: doce escaños de golpe."),
        V("Primera vez en un parlamento. Y de ahí, al Congreso.", "remate", 0.1),
    ], camara=[zoom(0, P(R, -3.7, 40), 1.0, 0), zoom("@Andalucía", SEV, 2.6, 0.9), zoom("@Congreso", P(R, -3.7, 40), 1.1, 0.8)],
       elements=[
        mapa(R, 0, 1.2, acciones=[{"at": "@Andalucía", "props": {"resalta": ["Sevilla", "Cádiz", "Málaga", "Granada", "Almería", "Jaén", "Córdoba", "Huelva"]}, "sfx": "pop"}]),
        rot("12 ESCAÑOS", 540, 430, "@doce", 120, "verde", golpe=True),
        sello("1.ª VEZ", "verde", 600, "@Primera"),
        quien("piz", 860, "@golpe", 0.4, "sorpresa", y=1600, entra="der", hud=True, acciones=[{"at": "@Congreso", "pose": "senala_arriba", "cara": "idea"}]),
    ]),
    # 5 · LA SUBIDA
    dict(id="subida", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", trans="corte", footnote=F, lines=[
        V("Abril de 2019: 24 diputados. Noviembre de 2019: 52, tercera fuerza."),
        V("En 2023 baja a 33. Y ahora, el 29N, vuelve a buscar su récord.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        obj("barras", 540, 640, "@Abril", 0.85, hud=True, entra="nada", dibujo=1.6,
            props={"tope": 60, "barras": [{"texto": "2015", "valor": 0, "color": "vox"}, {"texto": "ABR 2019", "valor": 24, "color": "vox"},
                                          {"texto": "NOV 2019", "valor": 52, "color": "vox"}, {"texto": "2023", "valor": 33, "color": "vox"}]}),
        sello("TERCERA FUERZA", "verde", 1080, "@tercera"),
        quien("abascal", 860, "@2023", 0.4, "pensativo", y=1620, entra="der", hud=True, acciones=[{"at": "@29N", "pose": "punos", "cara": "ilusionado"}]),
    ]),
    # 6 · CIERRE
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Crees que superará los 52? Te leo, con respeto."),
        V("Y sigue a Piz: esta noche, el último capítulo, el primer cara a cara de la historia.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@superará", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("¿MÁS DE 52?", 540, 420, 0, 110, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@cara", "do": "latir"}]),
        etq("ESTA NOCHE: EL PRIMER CARA A CARA", 540, 620, "@noche", "blanco", 0.5, hud=True),
    ]),
]

if __name__ == "__main__":
    episodio("nace_vox", "Cómo nació Vox", scenes,
             {"t": 3.0, "titulo": "De 0 a 52 escaños: cómo nació Vox", "capitulo": "📜 Historia en la pizarra · Cap. 6"},
             ["Ministerio del Interior: resultados de las europeas 2014 y las generales 2015, abril 2019, noviembre 2019 y 2023",
              "Junta de Andalucía: elecciones autonómicas del 2/12/2018 (12 escaños de Vox)",
              "Fundación de Vox: diciembre de 2013, presentación en enero de 2014"],
             ("📜 Historia en la pizarra · Cap. 6\n"
              "🟢 2015: Vox, 0 escaños · 2019: 52\n"
              "🧳 Nace a finales de 2013 con gente que sale del PP: Vidal-Quadras, Ortega Lara, Abascal…\n"
              "🗺️ Diciembre de 2018: 12 escaños en Andalucía, su primer parlamento\n"
              "📈 Abril 2019: 24 · noviembre 2019: 52 · 2023: 33\n"
              "💬 ¿Superará los 52 el 29N? Te leo 👇\n"
              "🔔 Sigue a Piz · Próximo: el primer cara a cara · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Ministerio del Interior (resultados 2014-2023) · Junta de Andalucía (2018). ¿Ves un error? Dínoslo.",
             ["#Vox", "#HistoriaDeEspaña", "#Abascal", "#29N", "#AprendeEnTikTok", "#pizarrapublica"],
             series_tag="HISTORIA EN LA PIZARRA")
