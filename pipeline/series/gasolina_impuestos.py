#!/usr/bin/env python3
"""«¿Cuánto de tu gasolina son impuestos?» (octubre de 2026).

Fuente: Comisión Europea, Weekly Oil Bulletin del 05/10/2026 (España, gasolina 95: 1,849 €/l; sin impuestos 1,255; impuesto especial 0,273;
IVA 0,321 → 32,1 % de impuestos). Depósito de 60 €: 19,28 € de impuestos (cálculo propio). Francia 28,73 €, Portugal 28,14 €,
Alemania 27,68 € de cada 60 € (cálculo propio con el mismo boletín).
Rebaja temporal: RDL 25/2026 (BOE 30/09/2026): impuesto especial −20 cts/l en octubre, −13 en noviembre y −6 en diciembre.
Sin rebaja (tipo ordinario 0,473 €/l, mismo precio antes de impuestos): ≈ 40 % → ≈ 24 € de cada 60 (estimación).
El IVA (21 %) se aplica sobre el precio más el impuesto especial. Canarias, Ceuta y Melilla tienen otros tributos.
"""
from _tu_dinero import *  # noqa: F401,F403

FN = "Comisión Europea, Weekly Oil Bulletin 05/10/2026 · gasolina 95 · cálculo propio"

scenes = [
    dict(id="gancho", fondo="calle", animo="curioso", footnote=FN, lines=[
        V("Echas 60 euros de gasolina: 19 se los queda Hacienda.", "energia"),
        V("Y eso, con rebaja.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@Hacienda", "abierto", dur=0.4)],
       elements=[
        obj("coche", 330, 1230, 0, 0.9, id="coche", entra="izq"),
        quien("piz", 760, "@gasolina", 0.7, "ilusionado", entra="der", objeto="fajo", pose="sostiene", acciones=[
            {"at": "@Hacienda", "take": True, "cara": "susto", "objeto": None}, {"at": "@rebaja", "cara": "indignado", "pose": "jarras"}]),
        gags.dinero_vuela("@19", 760, 1000, 6),
        rot("60 €", 540, 500, "@60", 110, "amarillo", golpe=True, out="@19"),
        rot("19 € IMPUESTOS", 540, 500, "@19", 90, C, golpe=True),
        rot("¡CON REBAJA!", 540, 640, "@rebaja", 80, "amarillo", golpe=True),
    ]),
    dict(id="litro", fondo="oficina", animo="curioso", trans="pan", footnote=FN, lines=[
        V("El litro, 1,85. De eso, 27 céntimos son impuesto especial y 32, IVA.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@IVA", "medio", "profe", 0.3, aire=220)],
       elements=[
        quien("profe", 300, 0, 0.75, "normal", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@1,85", "pose": "senala"}, {"at": "@especial", "mira": "camara", "cara": "serio"}, {"at": "@IVA", "salta": True}]),
        obj("calculadora", 800, 860, "@litro", 0.8, id="calc", props={"texto": "1,85"}, entra="pop", sfx="calculadora",
            acciones=[{"at": "@27", "props": {"texto": "-0,27"}, "salta": True}, {"at": "@IVA", "props": {"texto": "-0,32"}, "salta": True}]),
        rot("1,85 €/LITRO", 600, 470, "@1,85", 90, "amarillo", golpe=True, out="@27"),
        rot("ESPECIAL: 0,27 €", 600, 470, "@27", 76, C, golpe=True),
        rot("IVA: 0,32 €", 600, 580, "@IVA", 76, C, golpe=True),
    ]),
    dict(id="doble", fondo="rayos", animo="comico", musica="corte", trans="iris", footnote="Ley del IVA: la base incluye los impuestos especiales", lines=[
        V("Y sí: el IVA se cobra también sobre el impuesto.", "sorpresa"),
        V("Impuesto sobre impuesto.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@Impuesto", "medio", "sarcastica", 0.3, aire=220)],
       elements=[
        quien("sarcastica", 540, 0, 0.8, "burla", entra="pop", acciones=[
            {"at": "@también", "take": True, "cara": "sorpresa"}, {"at": "@Impuesto", "pose": "jarras", "cara": "esceptica"},
            {"at": "@impuesto#2", "salta": True, "cara": "riendo"}]),
        rot("IVA SOBRE IMPUESTO", 540, 500, "@también", 80, C, golpe=True),
        pum("¡DOBLE!", 780, 800, "@impuesto#2"),
    ]),
    dict(id="rebaja", fondo="calle", animo="tension", trans="pan", footnote="RDL 25/2026: −20 cts/l en octubre · sin rebaja, estimación con el tipo ordinario", lines=[
        V("En octubre, el impuesto especial baja 20 céntimos.", "normal"),
        V("Sin esa rebaja, serían unos 24 euros de cada 60.", "sorpresa", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@24", "abierto", dur=0.4)],
       elements=[
        obj("coche", 780, 1230, 0, 0.8, id="coche", entra="nada"),
        quien("pizon", 300, 0, 0.72, "normal", entra="izq", acciones=[
            {"at": "@baja", "salta": True, "cara": "riendo"}, {"at": "@Sin", "cara": "preocupado"},
            {"at": "@24", "take": True, "cara": "susto"}]),
        rot("OCTUBRE: −20 CTS", 540, 480, "@20", 84, "verde", golpe=True, out="@Sin"),
        rot("SIN REBAJA: 24 €", 540, 480, "@24", 84, C, golpe=True),
    ]),
    dict(id="europa", fondo={"tipo": "playa", "variante": "montana"}, animo="alegre", trans="iris", footnote="Weekly Oil Bulletin 05/10/2026 · impuestos en 60 € de gasolina 95 · cálculo propio", lines=[
        V("En Francia, de esos 60, casi 29 son impuestos. En Alemania o Portugal, unos 28.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@Portugal", "abierto", dur=0.4)],
       elements=[
        obj("avion", 1300, 600, 0, 0.6, entra="nada", acciones=[{"at": "@Francia", "x": -300, "dur": 3.0}]),
        quien("piz", 300, 0, 0.72, "normal", entra="izq", acciones=[
            {"at": "@Francia", "mira": "arriba", "cara": "sorpresa"}, {"at": "@29", "take": True},
            {"at": "@Alemania", "mira": "camara", "cara": "pensativo"}]),
        etq("FRANCIA: 28,73 €", 760, 640, "@Francia", "blanco"),
        etq("ALEMANIA: 27,68 €", 760, 820, "@Alemania", "amarillo"),
        etq("PORTUGAL: 28,14 €", 760, 1000, "@Portugal", "verde"),
    ]),
    dict(id="matiz", fondo="oficina", animo="curioso", trans="pan", footnote="RDL 25/2026: −13 cts en noviembre y −6 en diciembre · Canarias, Ceuta y Melilla: otros tributos", lines=[
        V("Ojo: en noviembre la rebaja es de 13 céntimos, y en diciembre de 6.", "normal"),
        V("En Canarias, Ceuta y Melilla, el sistema es otro.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@Canarias", "medio", "profe", 0.3, aire=200)],
       elements=[
        quien("profe", 300, 0, 0.75, "normal", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@noviembre", "pose": "senala"}, {"at": "@diciembre", "mira": "camara"},
            {"at": "@Canarias", "pose": "pulgar", "cara": "ilusionado"}]),
        obj("grafica", 760, 800, "@noviembre", 0.8, entra="pop", props={"valores": [3.3, 2.2, 1.0], "color": "verde"}),
        rot("NOV: −13 · DIC: −6", 600, 480, "@noviembre", 76, "amarillo", golpe=True),
    ]),
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote=FN, lines=[
        V("¿Cuánto te gastas al mes? Te leemos.", "normal"),
        V("Y síguenos: la próxima, cuánto cuesta un hijo.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        obj("coche", 780, 1230, 0, 0.75, entra="nada"),
        quien("piz", 300, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@gastas", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@hijo", "salta": True}]),
        rot("¿CUÁNTO GASTAS?", 540, 470, "@gastas", 90, "amarillo", golpe=True, out="@síguenos-0.4"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@hijo", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("gasolina_impuestos", "¿Cuánto de tu gasolina son impuestos?", scenes,
             {"t": 3.4, "titulo": "De 60 € de gasolina, 19 son impuestos", "capitulo": None},
             ["Comisión Europea: Weekly Oil Bulletin, 05/10/2026", "Real Decreto-ley 25/2026 (BOE 30/09/2026)"],
             ("⛽ De 60 € de gasolina, 19 € son impuestos… y eso con rebaja\n"
              "🧾 Litro: 1,85 € · impuesto especial 0,27 € · IVA 0,32 €\n"
              "🔁 El IVA se cobra también sobre el impuesto\n"
              "📉 Octubre: −20 cts de rebaja · sin ella, unos 24 € de cada 60\n"
              "🇫🇷 Francia 28,73 € · 🇵🇹 Portugal 28,14 € · 🇩🇪 Alemania 27,68 €\n"
              "📅 Noviembre −13 cts, diciembre −6\n"
              "💬 ¿Cuánto te gastas al mes?\n"
              "➡️ Próximo: cuánto cuesta un hijo · 🔔 Síguenos · 📚 Fuentes en comentarios"),
             ("📚 Fuente: Comisión Europea, Weekly Oil Bulletin del 05/10/2026 (gasolina 95: 1,849 €/l; sin impuestos 1,255; impuesto especial 0,273; "
              "IVA 0,321). Cálculo propio para 60 € y para Francia, Alemania y Portugal con el mismo boletín. Rebaja: RDL 25/2026 (BOE 30/09/2026), "
              "−20 cts/l en octubre, −13 en noviembre y −6 en diciembre salvo salvaguarda. «Sin rebaja» es una estimación con el tipo ordinario y el "
              "mismo precio antes de impuestos. Media nacional; Canarias, Ceuta y Melilla tienen otros tributos. ¿Ves un error? Dínoslo."),
             ["#PizarraPública", "#Gasolina", "#Impuestos", "#Carburantes", "#IVA", "#TuDinero", "#Hacienda"])
