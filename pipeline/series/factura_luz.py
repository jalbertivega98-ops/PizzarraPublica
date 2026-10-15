#!/usr/bin/env python3
"""«¿Qué pagas en la factura de la luz?» (2026): de cada 100 € de una factura PVPC tipo, cuánto es energía.

Cálculo propio sobre la factura tipo PVPC de septiembre de 2026 (FACUA, 104,31 €: 4,4 kW, 366 kWh) con los peajes y cargos 2.0TD
vigentes desde el 01/01/2026 (IDAE, «Tarifas reguladas julio 2026»), IVA 21 % e impuesto eléctrico 5,11269632 %:
  energía (con margen y bono social) 55 € · peajes 13 € · cargos 10 € · IVA 17 € · impuesto eléctrico 4 € · contador 1 € (de cada 100).
Impuestos 2026: RDL 7/2026 (BOE 21/03/2026) bajó el IVA al 10 % y el IEE al 0,5 % de marzo a mayo; desde junio, 21 % y 5,11 %
(nota de Hacienda del 29/06/2026). Estimación, no dato oficial de la CNMC; cambia cada mes.
"""
from _tu_dinero import *  # noqa: F401,F403

FN = "Cálculo propio: factura tipo PVPC sep 2026 (FACUA, 104,31 €)"

scenes = [
    dict(id="gancho", fondo="salon", animo="curioso", footnote=FN, lines=[
        V("De cada 100 euros de tu factura de la luz, unos 45 no son luz.", "energia"),
        V("¿Adónde van?", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@45", "medio", "piz", 0.3, aire=220)],
       elements=[
        quien("piz", 320, 0, 0.75, "ilusionado", entra="izq", objeto={"tipo": "contrato", "titulo": "FACTURA LUZ", "hojas": 1},
              pose="sostiene", acciones=[{"at": "@factura", "mira": "camara"}, {"at": "@45", "take": True, "cara": "susto"},
                                         {"at": "@van", "pose": "encoge", "cara": "confundido", "objeto": None}]),
        obj("billete", 780, 760, "@100", 0.9, id="billete", entra="pop", acciones=[{"at": "@van", "sale": "der"}]),
        rot("100 €", 700, 520, "@100", 110, "amarillo", golpe=True, out="@45"),
        rot("45 € NO SON LUZ", 600, 520, "@45", 84, C, golpe=True),
    ]),
    dict(id="energia", fondo="calle", animo="alegre", trans="pan", footnote=FN, lines=[
        V("La energía que gastas, con el margen de la comercializadora: unos 55.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@55", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@energía", "pose": "senala_arriba", "mira": "arriba"}, {"at": "@margen", "cara": "pensativo"},
            {"at": "@55", "salta": True, "cara": "ilusionado"}]),
        obj("sol", 780, 600, "@energía", 0.6, entra="pop"),
        rot("ENERGÍA: 55 €", 600, 480, "@55", 96, "verde", golpe=True),
    ]),
    dict(id="redes", fondo="oficina", animo="tension", trans="iris", footnote="Peajes (CNMC) y cargos 2.0TD 2026 · reparto estimado", lines=[
        V("Los cables que la traen a casa: 13.", "normal"),
        V("Los cargos del sistema, como las renovables o la deuda de años pasados: 10.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@10", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 300, 0, 0.75, "normal", entra="izq", acciones=[
            {"at": "@cables", "mira": "der"}, {"at": "@13", "salta": True, "cara": "sorpresa"},
            {"at": "@renovables", "cara": "pensativo"}, {"at": "@deuda", "take": True, "cara": "susto"},
            {"at": "@10", "pose": "encoge", "cara": "confundido"}]),
        rot("PEAJES: 13 €", 600, 470, "@13", 84, "amarillo", golpe=True),
        rot("CARGOS: 10 €", 600, 580, "@10", 84, "blanco", golpe=True),
    ]),
    dict(id="impuestos", fondo="oficina", animo="comico", trans="pan", footnote="IVA 21 % · impuesto eléctrico 5,11 % · contador 0,81 €/mes", lines=[
        V("Y Hacienda: 17 de IVA y 4 del impuesto eléctrico.", "sorpresa"),
        V("El euro que falta, el alquiler del contador.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@contador", "medio", "hacienda", 0.3, aire=200)],
       elements=[
        quien("piz", 290, 0, 0.75, "normal", entra="nada", acciones=[
            {"at": "@Hacienda", "take": True, "cara": "susto", "mira": "hacienda"}, {"at": "@17", "tiembla": True},
            {"at": "@eléctrico", "cara": "indignado", "pose": "jarras"}, {"at": "@contador", "cara": "confundido", "pose": "encoge"}]),
        gags.aparece_hacienda("@Hacienda-0.2", 800, factura="IVA + IEE"),
        gags.dinero_vuela("@17", 380, 1000, 6),
        rot("IVA: 17 €", 600, 470, "@17", 84, C, golpe=True),
        rot("IMPUESTO ELÉCTRICO: 4 €", 600, 580, "@4", 62, "amarillo", golpe=True),
        rot("CONTADOR: 1 €", 600, 690, "@contador", 62, "blanco", golpe=True),
    ]),
    dict(id="primavera", fondo="rayos", animo="comico", musica="corte", trans="iris", footnote="RDL 7/2026: IVA 10 % de marzo a mayo · desde junio, 21 %", lines=[
        V("En primavera pagabas menos: el IVA de la luz bajó al 10 %.", "normal"),
        V("Desde junio, otra vez al 21.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@21", "medio", "sarcastica", 0.3, aire=220)],
       elements=[
        quien("sarcastica", 540, 0, 0.8, "riendo", entra="pop", acciones=[
            {"at": 1.1, "mira": "camara", "pose": "senala_arriba"}, {"at": 2.2, "cara": "burla", "pose": "jarras"}, {"at": "@10", "salta": True, "pose": "arriba"}, {"at": "@junio", "cara": "burla"},
            {"at": "@21", "pose": "jarras", "cara": "esceptica"}]),
        rot("MAR-MAY: IVA 10 %", 540, 480, "@10", 80, "verde", golpe=True, out="@junio"),
        rot("DESDE JUNIO: 21 %", 540, 480, "@21", 80, C, golpe=True),
        pum("¡ZAS!", 760, 820, "@21+0.2"),
    ]),
    dict(id="matiz", fondo="oficina", animo="curioso", trans="pan", footnote="Estimación propia, no dato oficial de la CNMC", lines=[
        V("Ojo: es una factura tipo de septiembre. Cada mes cambia, porque la energía sigue al mercado.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@mercado", "medio", "profe", 0.3, aire=200)],
       elements=[
        quien("profe", 300, 0, 0.75, "normal", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@septiembre", "pose": "senala"}, {"at": "@cambia", "mira": "grafica"},
            {"at": "@mercado", "pose": "pulgar", "mira": "camara"}]),
        obj("grafica", 760, 800, "@cambia", 0.8, id="grafica", entra="pop", props={"valores": [2, 1.2, 2.6, 1.6, 2.2], "color": "azul"}),
        rot("CAMBIA CADA MES", 600, 480, "@Ojo", 76, "amarillo", golpe=True),
    ]),
    dict(id="final", fondo="salon", animo="final", trans="iris", footnote=FN, lines=[
        V("¿Miras tu factura? Te leemos.", "normal"),
        V("Y síguenos: la próxima, la gasolina.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@Miras", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@gasolina", "salta": True}]),
        quien("pizon", 790, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@factura", "cara": "sorpresa"}, {"at": "@gasolina", "take": True}]),
        rot("¿MIRAS TU FACTURA?", 540, 470, "@Miras", 84, "amarillo", golpe=True, out="@síguenos-0.4"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@gasolina", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("factura_luz", "¿Qué pagas en la luz?", scenes, {"t": 3.2, "titulo": "45 de cada 100 € no son luz", "capitulo": None},
             ["Peajes y cargos 2.0TD 2026: IDAE, Tarifas reguladas julio 2026", "RDL 7/2026 (BOE 21/03/2026) y nota de Hacienda 29/06/2026",
              "Factura tipo PVPC septiembre 2026: FACUA"],
             ("💡 De cada 100 € de tu factura de la luz, unos 45 no son luz\n"
              "⚡ Energía (con margen): 55 € · cables (peajes): 13 € · cargos del sistema: 10 €\n"
              "🧾 IVA: 17 € · impuesto eléctrico: 4 € · contador: 1 €\n"
              "🌸 De marzo a mayo el IVA bajó al 10 %; desde junio, otra vez al 21 %\n"
              "📈 Es una factura tipo de septiembre: cada mes cambia\n"
              "💬 ¿Miras tu factura?\n"
              "➡️ Próximo: la gasolina · 🔔 Síguenos · 📚 Fuentes en comentarios"),
             ("📚 Cálculo propio sobre la factura tipo PVPC de septiembre de 2026 de FACUA (104,31 €; 4,4 kW; 366 kWh) con los peajes y cargos 2.0TD "
              "vigentes desde el 01/01/2026 (IDAE, Tarifas reguladas julio 2026), IVA 21 % e impuesto eléctrico 5,11 %. «Energía» incluye el margen "
              "de comercialización y la financiación del bono social. Impuestos: RDL 7/2026 (IVA 10 % e IEE 0,5 % de marzo a mayo) y nota de Hacienda "
              "del 29/06/2026. Estimación, no dato oficial de la CNMC; cambia cada mes y en el mercado libre es distinto. ¿Ves un error? Dínoslo."),
             ["#PizarraPública", "#FacturaDeLaLuz", "#Luz", "#PVPC", "#IVA", "#TuDinero", "#Energía"])
