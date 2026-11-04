#!/usr/bin/env python3
"""«¿Ha cambiado todo después de Urda?» (vie 6/11/2026, 15:00). Las primeras encuestas hechas tras el accidente.
Aprobado por joel el 4/11/2026 21:21 UTC (propuesta 2 de /mnt/project-files/insta/guiones/propuestas_5nov.md).
Tema político junto a una tragedia: tono serio, lazo, sin gags sobre el accidente.
Fuentes:
  Demócrata 2/11/2026: Target Point / El Debate, campo del 28/10 (18:00) al 30/10, 1.024 entrevistas.
    PP 32,0 → 31,8 %; PSOE 25,9 → 25,5 %; Vox 18,7 → 19,9 % (frente a su sondeo del 11/10). PP+Vox 199-207 escaños.
  UHN Plus / Infobae / Libertad Digital 2/11/2026: Sigma Dos / El Mundo, campo 29-30/10, 2.505 entrevistas.
    PSOE 24,6 % (−1,5 en una semana), 97-103 escaños (99); PP 31,1 % (+0,5), 133-139; Vox 19,3 %, 63-69.
  Libertad Digital 2/11: NC Report PP+Vox 204-208; SocioMétrica PP+Vox+UPN 203; Hamalgama PP+Vox 205.
  Infobae directo 4/11/2026: Narciso Michavila (GAD3, 31/10): «ahora es imposible que Pedro Sánchez sea el más votado».
"""
from _mundo import *  # noqa: F401,F403

AZUL = (28, 52, 110)
F_TP = "Target Point / El Debate, vía Demócrata 2/11/2026"
F_SD = "Sigma Dos / El Mundo, vía Infobae y UHN Plus 2/11/2026"


def barras(at, datos, y=1000, scale=1.1, tope=35, sufijo=" %", dec=1, **kw):
    return obj("barras", 540, y, at, scale, hud=True, entra="nada", dibujo=1.3,
               props={"sufijo": sufijo, "decimales": dec, "tope": tope, "barras": [
                   {"texto": t, "valor": v, "color": c} for t, v, c in datos]}, **kw)


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": AZUL}, animo="tension", footnote=F_SD, lines=[
        V("Antes de Urda, el PSOE remontaba en las encuestas.", "intriga"),
        V("Una semana después, una lo deja en 99 escaños. Por debajo de cien.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@99", "general", [540, 900], 0.5, zoom=1.08)],
       elements=[
        obj("grafica", 540, 760, 0, 0.9, hud=True, entra="crece", sfx="pop", out="@semana"),
        rot("PSOE: REMONTADA", 540, 460, 0.2, 90, "verde", out="@semana"),
        obj("contador", 540, 760, "@semana", 1.0, hud=True, entra="pop", sfx="kaching", dibujo=1.6,
            props={"valor": 99, "desde": 106, "sufijo": " ESCAÑOS", "ancho": 860}, acciones=[{"at": "@cien", "tiembla": True}]),
        rot("PSOE", 540, 520, "@semana", 110, "rojo", golpe=True),
        quien("sanchez", 540, "@99", 0.62, "preocupado", y=1560, entra="abajo", acciones=[{"at": "@cien", "pose": "encoge"}]),
        sello("SIGMA DOS", "azul", 1100, "@Por"),
        obj("lazo", 960, 220, 0, 0.3, hud=True, entra="pop"),
    ]),
    # 2 · MISMA EMPRESA, ANTES Y DESPUÉS
    dict(id="antes_despues", fondo={"tipo": "plano", "color": AZUL}, animo="curioso", trans="papel", footnote=F_TP, lines=[
        V("La forma limpia de verlo: misma empresa, antes y después. Target Point."),
        V("El PP, casi igual: 31,8. El PSOE baja cuatro décimas, al 25,5.", "normal", 0.1),
        V("Y quien más sube es Vox: del 18,7 al 19,9. A una décima del 20.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@Vox", "general", [540, 920], 0.4, zoom=1.05)],
       elements=[
        rot("ANTES 11/10 → DESPUÉS 30/10".replace("→", "·"), 540, 420, 0.2, 60, "blanco"),
        barras("@PP", [("PP", 31.8, "pp"), ("PSOE", 25.5, "psoe"), ("VOX", 19.9, "vox")]),
        etq("PP: −0,2", 230, 1330, "@igual", "blanco", 0.5, hud=True),
        etq("PSOE: −0,4", 540, 1430, "@décimas", "rojo", 0.5, hud=True),
        etq("VOX: +1,2", 850, 1330, "@sube", "verde", 0.55, hud=True),
        quien("abascal", 1250, "@Vox-0.5", 0.42, "normal", y=1660, entra="nada", acciones=[
            {"at": "@Vox-0.5", "x": 900, "dur": 0.5}, {"at": "@20", "pose": "punos", "cara": "riendo"}]),
    ]),
    # 3 · SIGMA DOS: el golpe al PSOE
    dict(id="sigma", fondo="oficina", animo="tension", trans="barrido", footnote=F_SD, lines=[
        V("Sigma Dos lo ve más fuerte: el PSOE cae punto y medio en una semana, hasta el 24,6."),
        V("El PP sube medio punto, al 31,1. Y Vox, 19,3.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@24,6", "general", [540, 900], 0.4, zoom=1.06)],
       elements=[
        obj("grafica", 540, 700, 0, 0.8, hud=True, entra="crece", sfx="pop", out="@PP"),
        etq("PSOE −1,5 EN 7 DÍAS", 540, 460, "@semana", "rojo", 0.7, hud=True, out="@PP"),
        barras("@PP", [("PP", 31.1, "pp"), ("PSOE", 24.6, "psoe"), ("VOX", 19.3, "vox")], y=900),
        quien("feijoo", 260, "@PP", 0.42, "normal", y=1560, entra="izq", acciones=[{"at": "@medio", "pose": "pulgar", "cara": "ilusionado"}]),
        quien("sanchez", 820, 0.2, 0.42, "serio", y=1560, entra="der", acciones=[{"at": "@cae", "cara": "preocupado"}]),
        sello("ENCUESTA", "azul", 1240, "@24,6"),
    ]),
    # 4 · LOS BLOQUES
    dict(id="bloques", fondo="calle", animo="curioso", trans="iris", footnote="Sigma Dos, NC Report, Target Point, SocioMétrica, Hamalgama · Libertad Digital 2/11", lines=[
        V("Cinco encuestas tras el accidente. En todas, PP y Vox suman mayoría absoluta."),
        V("Entre 196 y 208 escaños. Hacen falta 176.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@176", "general", [540, 900], 0.4, zoom=1.06)],
       elements=[
        edif("congreso", 540, 0, 0.55, entra="crece", sfx="pop", dibuja=0.7),
        rot("5 ENCUESTAS", 540, 420, 0.1, 100, "amarillo", golpe=True, out="@Entre"),
        rot("PP + VOX: 196-208", 540, 420, "@Entre", 90, "amarillo", golpe=True, out="@176"),
        rot("MAYORÍA: 176", 540, 420, "@176", 100, "blanco", golpe=True),
        quien("piz", 860, 0.2, 0.45, "pensativo", y=1560, entra="der", acciones=[{"at": "@todas", "pose": "senala_arriba", "cara": "sorpresa"}, {"at": "@176", "pose": "piensa"}]),
    ]),
    # 5 · LA FRASE DE MICHAVILA + OJO
    dict(id="michavila", fondo={"tipo": "plano", "color": AZUL}, animo="tension", trans="corte",
         footnote="Narciso Michavila (GAD3), 31/10/2026, vía Infobae", lines=[
        V("Y el presidente de GAD3, Narciso Michavila, va más lejos: «ahora es imposible que Pedro Sánchez sea el más votado»."),
        V("Ojo: son encuestas hechas en caliente. Y las encuestas no votan.", "normal", 0.2),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        obj("bocadillo", 540, 620, "@lejos", 0.85, hud=True, entra="pop", sfx="pop", out="@Ojo",
            props={"lineas": ["MICHAVILA (GAD3):", "«ahora es imposible", "que Sánchez sea", "el más votado»"], "cola": (0, 1)}),
        sello("OPINIÓN", "azul", 1100, "@imposible", out="@Ojo"),
        obj("calendario", 540, 820, "@Ojo", 0.7, hud=True, entra="pop", sfx="papel",
            props={"mes": "OCTUBRE 2026", "inicio": 3, "dias": 31, "marcados": [28, 29, 30], "colores": {28: "rojo", 29: "azul", 30: "azul"}}),
        sello("LAS ENCUESTAS NO VOTAN", "naranja", 1300, "@votan"),
    ]),
    # 6 · FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Urda ha cambiado tu voto? Sí o no, te leo."),
        V("Y sigue a Piz: hasta el 29N, cada encuesta con datos.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        edif("congreso", 540, 0, 0.5, entra="nada"),
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@voto", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        etq("SÍ", 300, 700, "@Sí", "verde", 0.7, hud=True, out="@sigue"),
        etq("NO", 780, 700, "@no", "rojo", 0.7, hud=True, out="@sigue"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@datos", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("tras_urda", "¿Ha cambiado todo después de Urda?", scenes,
             {"t": 3.0, "titulo": "¿Ha cambiado todo tras Urda?", "capitulo": None},
             ["Target Point / El Debate (campo 28-30/10/2026) vs su sondeo del 11/10, vía Demócrata 2/11",
              "Sigma Dos / El Mundo (campo 29-30/10/2026), vía Infobae y UHN Plus 2/11",
              "NC Report, SocioMétrica y Hamalgama, vía Libertad Digital 2/11/2026",
              "Narciso Michavila (GAD3), 31/10/2026, vía Infobae 4/11"],
             ("📊 ¿Ha cambiado todo después de Urda?\n"
              "🔴 Sigma Dos: PSOE 24,6 % (−1,5 en una semana) · 99 escaños\n"
              "🟢 Target Point: quien más sube es Vox, del 18,7 al 19,9 %\n"
              "🔵 PP, casi igual: 31-32 %\n"
              "🏛️ En las 5 encuestas, PP + Vox suman mayoría (196-208 · hacen falta 176)\n"
              "⚠️ Encuestas en caliente · las encuestas no votan\n"
              "💬 ¿Urda ha cambiado tu voto? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Target Point/El Debate y Sigma Dos/El Mundo (2/11/2026), NC Report, SocioMétrica y Hamalgama "
             "(vía Libertad Digital 2/11), Michavila/GAD3 vía Infobae. ¿Ves un error? Dínoslo.",
             ["#29N", "#encuestas", "#Urda", "#PSOE", "#PP", "#Vox", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
