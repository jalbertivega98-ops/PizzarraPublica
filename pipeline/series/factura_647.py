#!/usr/bin/env python3
"""«647.000 €» (dom 8/11/2026, 20:00). El Supremo pasa la factura del caso mascarillas a Ábalos, Koldo y Aldama.
Aprobado por joel el 4/11/2026 21:21 UTC (propuesta 3 de /mnt/project-files/insta/guiones/propuestas_5nov.md).
Fuentes (auto de la Sala de lo Penal del Supremo, vía Europa Press/EFE, 4/11/2026): Infobae, Público, El Debate, Cronista.
  Total 647.000 € en multas, decomiso e indemnizaciones; plazo 15 días (dos semanas); si no, vía de apremio.
  Multas: Ábalos 52.500 €, Koldo 45.750 €, Aldama 75.000 € (= 173.250 €).
  Decomiso 430.298 €: beneficio del cohecho «del que Aldama era el encargado de repartirlo», solidario entre los tres.
  Indemnizaciones (Ábalos y Koldo): Ineco 34.450 €, Tragsatec 9.500 € (por el enchufe de Jéssica Rodríguez).
  Penas: Ábalos 24 años, Koldo 19; Aldama colaboró y su pena está suspendida (fuentes: 4 años o 4 y medio).
  Ábalos y Koldo en prisión. Ninguna fuente dice si la sentencia es firme: no lo decimos.
"""
from _mundo import *  # noqa: F401,F403

GRANATE = (70, 30, 40)
F = "Auto del Supremo vía Infobae, El Debate y Público, 4/11/2026"


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo={"tipo": "plano", "color": GRANATE}, animo="tension", footnote=F, lines=[
        V("El Supremo acaba de pasarles la factura: 647.000 euros.", "intriga"),
        V("A Ábalos, a Koldo y a Aldama. Y tienen quince días para pagar.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@quince", "general", [540, 900], 0.5, zoom=1.08)],
       elements=[
        obj("contador", 540, 700, 0.2, 1.0, hud=True, entra="pop", sfx="kaching", dibujo=1.8,
            props={"valor": 647000, "sufijo": " €", "ancho": 900}, acciones=[{"at": "@euros", "tiembla": True}]),
        rot("LA FACTURA", 540, 460, 0.1, 110, "amarillo", golpe=True),
        quien("abalos", 540, "@factura", 0.7, "susto", y=1480, entra="abajo", acciones=[{"at": "@pagar", "pose": "encoge", "cara": "preocupado"}]),
        etq("KOLDO", 230, 1180, "@Koldo", "blanco", 0.6, hud=True),
        etq("ALDAMA", 850, 1180, "@Aldama", "blanco", 0.6, hud=True),
        obj("calendario", 860, 420, "@quince", 0.28, hud=True, entra="crece", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [4], "colores": {4: "rojo"}}),
        sello("15 DÍAS", "rojo", 1000, "@días"),
    ]),
    # 2 · LAS MULTAS (y el gag: el que más paga no está en la cárcel)
    dict(id="multas", fondo="oficina", animo="curioso", trans="papel", footnote=F, lines=[
        V("Primero, las multas. Ábalos, 52.500. Koldo, 45.750."),
        V("Y el que más paga es Aldama: 75.000.", "sorpresa", 0.1),
        V("Lo curioso: es el único de los tres que no está en la cárcel. Colaboró con la justicia.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Aldama", "general", [540, 900], 0.4, zoom=1.06),
               plano("@curioso", "general", [540, 1000], 0.4)],
       elements=[
        obj("barras", 540, 880, "@Ábalos", 1.05, hud=True, entra="nada", dibujo=1.6,
            props={"sufijo": " MIL €", "decimales": 1, "tope": 80, "barras": [
                {"texto": "ÁBALOS", "valor": 52.5, "color": "psoe"}, {"texto": "KOLDO", "valor": 45.75, "color": "gris"},
                {"texto": "ALDAMA", "valor": 75.0, "color": "amarillo"}]}, out="@curioso"),
        rot("1 · MULTAS", 540, 420, 0, 100, "amarillo"),
        quien("abalos", 230, "@Ábalos", 0.4, "preocupado", y=1640, entra="izq", out="@curioso", acciones=[{"at": "@Koldo", "mira": "der"}, {"at": "@Aldama", "cara": "sorpresa"}]),
        quien("piz", 1250, "@Aldama-0.4", 0.45, "normal", y=1640, entra="nada", acciones=[
            {"at": "@Aldama-0.4", "x": 900, "dur": 0.5}, {"at": "@75.000", "cara": "sorpresa", "take": True},
            {"at": "@cárcel", "pose": "jarras", "cara": "esceptica", "mira": "camara"}]),
        obj("checklist", 480, 900, "@curioso", 0.75, hud=True, entra="pop", sfx="pop",
            props={"items": ["ÁBALOS: PRISIÓN", "KOLDO: PRISIÓN", "ALDAMA: CALLE"], "marcas": ["si", "si", "no"]}),
        sello("COLABORÓ", "azul", 1240, "@Colaboró"),
    ]),
    # 3 · EL DECOMISO: lo que se llevaron
    dict(id="decomiso", fondo={"tipo": "plano", "color": GRANATE}, animo="tension", trans="barrido", footnote=F, lines=[
        V("Segundo, el decomiso: 430.298 euros."),
        V("Es lo que, según la sentencia, ganaron con las mordidas. Y el que lo repartía era Aldama.", "normal", 0.1),
        V("Lo pagan entre los tres, hasta el último euro.", "remate", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@repartía", "general", [540, 900], 0.4, zoom=1.06)],
       elements=[
        rot("2 · DECOMISO", 540, 420, 0, 100, "amarillo"),
        obj("contador", 540, 640, "@decomiso", 0.95, hud=True, entra="pop", sfx="kaching", props={"valor": 430298, "sufijo": " €", "ancho": 900}),
        obj("saco", 540, 1000, "@Es", 0.8, hud=True, entra="cae", sfx="golpe"),
        dict(type="efecto", efecto="lluvia", objeto="moneda", n=12, x0=200, x1=880, at="@repartía", vida=1.8),
        etq("MORDIDAS", 540, 1240, "@mordidas", "rojo", 0.6, hud=True, out="@repartía"),
        etq("ALDAMA REPARTÍA", 540, 1240, "@repartía", "blanco", 0.6, hud=True, out="@pagan"),
        etq("ENTRE LOS TRES", 540, 1240, "@pagan", "amarillo", 0.65, hud=True),
        sello("SENTENCIA", "azul", 1400, "@sentencia"),
    ]),
    # 4 · LAS INDEMNIZACIONES: el enchufe
    dict(id="enchufe", fondo="oficina", animo="curioso", trans="corte", footnote=F, lines=[
        V("Y tercero: casi 44.000 euros para dos empresas públicas, Ineco y Tragsatec."),
        V("Por el enchufe de Jéssica Rodríguez. Esto lo pagan Ábalos y Koldo.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        rot("3 · INDEMNIZACIONES", 540, 420, 0, 84, "amarillo"),
        obj("cartel", 300, 820, "@Ineco", 0.8, hud=True, entra="cae", sfx="golpe", props={"texto": "INECO", "color": "azul", "tinta": "blanco"}),
        obj("cartel", 780, 820, "@Tragsatec", 0.8, hud=True, entra="cae", sfx="golpe", props={"texto": "TRAGSATEC", "color": "verde", "tinta": "blanco"}),
        etq("34.450 €", 300, 620, "@Ineco", "verde", 0.62, hud=True),
        etq("9.500 €", 780, 620, "@Tragsatec", "verde", 0.62, hud=True),
        quien("abalos", 540, "@empresas", 0.45, "serio", y=1600, entra="abajo", acciones=[{"at": "@pagan", "pose": "manos_juntas", "cara": "preocupado"}]),
    ]),
    # 5 · LAS CONDENAS Y QUÉ PASA SI NO PAGAN
    dict(id="condenas", fondo="oficina", animo="tension", trans="iris", footnote=F, lines=[
        V("Recuerda las condenas: 24 años para Ábalos, el que fue ministro y número tres del PSOE. 19 para Koldo."),
        V("¿Y si no pagan? El tribunal irá a por su dinero por la vía de apremio.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@pagan", "general", [540, 900], 0.4, zoom=1.06)],
       elements=[
        obj("barras", 540, 820, "@condenas", 0.95, hud=True, entra="nada", dibujo=1.2, out="@pagan",
            props={"sufijo": " AÑOS", "decimales": 0, "tope": 26, "barras": [
                {"texto": "ÁBALOS", "valor": 24, "color": "psoe"}, {"texto": "KOLDO", "valor": 19, "color": "gris"}]}),
        etq("EX MINISTRO", 300, 1250, "@ministro", "blanco", 0.55, hud=True, out="@pagan"),
        etq("Nº 3 DEL PSOE", 780, 1250, "@tres", "psoe", 0.55, hud=True, out="@pagan"),
        quien("abalos", 540, "@pagan", 0.55, "susto", y=1560, entra="abajo", acciones=[{"at": "@tribunal", "cara": "preocupado"}, {"at": "@apremio", "pose": "encoge"}]),
        obj("lupa", 820, 760, "@dinero", 0.7, hud=True, entra="crece", sfx="pop"),
        rot("VÍA DE APREMIO", 540, 440, "@apremio", 90, "rojo", golpe=True),
        sello("COBRO FORZOSO", "naranja", 1100, "@apremio+0.3"),
    ]),
    # 6 · FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Crees que van a pagar en quince días? Sí o no, te leo."),
        V("Y sigue a Piz: te contamos cómo acaba.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@pagar", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        etq("SÍ", 300, 700, "@Sí", "verde", 0.7, hud=True, out="@sigue"),
        etq("NO", 780, 700, "@no", "rojo", 0.7, hud=True, out="@sigue"),
        rot("647.000 €", 540, 420, 0, 110, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@acaba", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("factura_647", "647.000 €", scenes,
             {"t": 4.2, "titulo": "La factura de Ábalos: 647.000 €", "capitulo": None},
             ["Auto del Tribunal Supremo (ejecución de la sentencia del caso mascarillas), vía Europa Press/EFE 4/11/2026",
              "Infobae, El Debate, Público y Cronista, 4/11/2026: multas, decomiso, indemnizaciones, plazo y vía de apremio",
              "No afirmamos si la sentencia es firme (no consta en las fuentes)"],
             ("💸 El Supremo les pasa la factura: 647.000 €\n"
              "⚖️ Multas: Ábalos 52.500 € · Koldo 45.750 € · Aldama 75.000 €\n"
              "🤔 El que más paga, Aldama, es el único que no está en la cárcel\n"
              "💰 Decomiso: 430.298 € de las mordidas, entre los tres\n"
              "🏢 ~44.000 € a Ineco y Tragsatec por el enchufe de Jéssica\n"
              "⏳ 15 días para pagar · si no, vía de apremio\n"
              "💬 ¿Pagarán a tiempo? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuente: auto del Tribunal Supremo (4/11/2026) recogido por Europa Press/EFE: Infobae, El Debate, Público. "
             "¿Ves un error? Dínoslo.",
             ["#Abalos", "#Koldo", "#Aldama", "#CasoMascarillas", "#Supremo", "#29N", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
