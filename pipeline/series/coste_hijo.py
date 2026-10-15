#!/usr/bin/env python3
"""«¿Cuánto cuesta un hijo?» (2026): coste de criar frente a las ayudas en dinero.

Coste: Save the Children, «El coste de la crianza 2024» (dic. 2024, precios de 2024): 758 €/mes de media (0-17);
  0-3 años 604 €, 7-12 años 812 €.
Ayudas 2026: deducción por maternidad 100 €/mes hasta los 3 años (art. 81 LIRPF; madres trabajadoras o en paro),
  CAPI (Ley 19/2021): 115 €/mes (<3 años), 80,50 € (3-6), 57,50 € (6-18), solo hogares con rentas bajas.
  Prestación por hijo a cargo: ya no se pide para hijos sin discapacidad.
Cálculo propio: bebé, renta media 604 − 100 = 504 €; renta baja 604 − 215 = 389 €; 7-12 años, renta media 812 − 0;
  renta baja 57,50 / 812 ≈ 7 %.
Matiz: ayudas autonómicas, escuelas 0-3 gratuitas, cheque guardería y mínimos del IRPF no son pagos mensuales o no se incluyen.
"""
from _tu_dinero import *  # noqa: F401,F403

STC = "Save the Children, «El coste de la crianza 2024» (precios de 2024)"


def peque(x, at=0.0, cara="ilusionado", acciones=(), scale=0.42, **kw):
    return pj("pizon", x, at, scale, cara, acciones, id="peque", **kw)


scenes = [
    dict(id="gancho", fondo="salon", animo="curioso", footnote=STC, lines=[
        V("Criar a un hijo cuesta 758 euros al mes, según Save the Children.", "energia"),
        V("¿Cuánto pone el Estado?", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@Estado", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.75, "ilusionado", entra="izq", acciones=[
            {"at": "@hijo", "mira": "peque", "cara": "riendo"}, {"at": 2.4, "pose": "senala"}, {"at": "@758", "take": True, "cara": "susto"},
            {"at": "@Estado", "mira": "camara", "pose": "encoge", "cara": "pensativo"}]),
        peque(760, "@hijo", entra="pop", acciones=[{"at": 3.4, "salta": True, "mira": "piz"}, {"at": "@758", "take": True}]),
        rot("758 €/MES", 540, 500, "@758", 110, C, golpe=True),
        rot("¿Y EL ESTADO?", 540, 640, "@Estado", 84, "amarillo", golpe=True),
    ]),
    dict(id="bebe", fondo="salon", animo="alegre", trans="pan", footnote=STC + " · deducción por maternidad (art. 81 LIRPF)", lines=[
        V("Un bebé: 604 al mes.", "normal"),
        V("Si la madre trabaja, Hacienda le da 100: la deducción por maternidad.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@maternidad", "medio", "hacienda", 0.3, aire=200)],
       elements=[
        peque(300, 0, "riendo", entra="nada", acciones=[{"at": "@604", "salta": True}, {"at": "@100", "mira": "hacienda"}]),
        quien("hacienda", 1300, "@Hacienda-0.3", 0.75, "normal", entra="nada", pose="sostiene", objeto="billete", acciones=[
            {"at": "@Hacienda", "x": 780, "dur": 0.7}, {"at": "@100", "salta": True, "cara": "riendo"},
            {"at": "@maternidad", "pose": "pulgar", "objeto": None}]),
        rot("BEBÉ: 604 €/MES", 600, 480, "@604", 84, C, golpe=True, out="@100"),
        rot("− 100 €", 600, 480, "@100", 110, "verde", golpe=True),
    ]),
    dict(id="capi", fondo="oficina", animo="curioso", trans="iris", footnote="CAPI (Ley 19/2021): 115 €/mes a menores de 3 años, solo rentas bajas · cálculo propio", lines=[
        V("Si la familia tiene poca renta, suma el complemento de infancia: 115 euros.", "normal"),
        V("Aun así, le quedan 389 por pagar.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@389", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 300, 0, 0.75, "preocupado", entra="izq", acciones=[
            {"at": "@renta", "cara": "triste"}, {"at": "@115", "salta": True, "cara": "ilusionado"},
            {"at": "@389", "tiembla": True, "cara": "preocupado"}]),
        obj("calculadora", 800, 860, "@complemento", 0.85, id="calc", props={"texto": "604"}, entra="pop", sfx="calculadora",
            acciones=[{"at": "@115", "props": {"texto": "-215"}, "salta": True}, {"at": "@389", "props": {"texto": "389"}, "salta": True}]),
        rot("+ 115 € (CAPI)", 600, 480, "@115", 84, "verde", golpe=True, out="@389"),
        rot("QUEDAN 389 €", 600, 480, "@389", 96, C, golpe=True),
    ]),
    dict(id="giro", fondo="rayos", animo="tension", musica="corte", trans="iris", footnote=STC + " · 7-12 años: 812 €/mes", lines=[
        V("Pero a los tres años, la deducción se acaba.", "sorpresa"),
        V("Con siete, cuesta 812. Y una familia de renta media no recibe ni un euro al mes.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@euro", "medio", "piz", 0.3, aire=220)],
       elements=[
        quien("piz", 320, 0, 0.78, "normal", entra="pop", acciones=[
            {"at": "@acaba", "take": True, "cara": "susto"}, {"at": "@812", "tiembla": True}, {"at": "@familia", "mira": "camara", "cara": "preocupado"},
            {"at": "@euro", "tropieza": True}]),
        peque(780, "@siete", "riendo", entra="pop", scale=0.55, acciones=[{"at": "@812", "salta": True}, {"at": "@media", "mira": "piz", "cara": "sorpresa"}]),
        rot("DEDUCCIÓN: FIN", 540, 480, "@acaba", 84, C, golpe=True, out="@812"),
        rot("7 AÑOS: 812 €/MES", 540, 480, "@812", 84, "amarillo", golpe=True, out="@euro"),
        rot("AYUDA: 0 €", 540, 480, "@euro", 110, C, golpe=True),
    ]),
    dict(id="baja", fondo="oficina", animo="triste", trans="pan", footnote="CAPI 6-18 años: 57,50 €/mes · cálculo propio sobre 812 €", lines=[
        V("Con renta baja, 57,50. Un 7 % de lo que cuesta.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@7", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 300, 0, 0.75, "normal", entra="nada", acciones=[
            {"at": "@57,50", "salta": True, "cara": "ilusionado"}, {"at": "@7", "cara": "triste", "pose": "caidos"}]),
        obj("moneda", 780, 820, "@57,50", 0.7, entra="cae"),
        rot("57,50 € = 7 %", 600, 480, "@57,50", 96, "amarillo", golpe=True),
    ]),
    dict(id="matiz", fondo="oficina", animo="curioso", trans="pan", footnote="No incluye ayudas autonómicas, guarderías gratuitas ni mínimos del IRPF", lines=[
        V("Ojo: hay ayudas de cada comunidad, guarderías gratis y rebajas en la renta que no son un pago al mes.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@mes", "medio", "profe", 0.3, aire=200)],
       elements=[
        quien("profe", 300, 0, 0.75, "normal", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@comunidad", "pose": "senala"}, {"at": "@guarderías", "mira": "camara", "cara": "ilusionado"},
            {"at": "@renta", "pose": "pulgar"}, {"at": "@mes", "cara": "pensativo"}]),
        obj("checklist", 760, 760, "@ayudas", 0.6, entra="pop",
            props={"items": ["AYUDAS AUTONÓMICAS", "GUARDERÍA GRATIS", "IRPF"], "marcas": ["si", "si", "si"]}),
        rot("NO ENTRAN EN LA CUENTA", 600, 480, "@Ojo", 64, "amarillo", golpe=True),
    ]),
    dict(id="final", fondo="salon", animo="final", trans="iris", footnote=STC, lines=[
        V("¿Cuánto te cuesta a ti? Te leemos.", "normal"),
        V("Y síguenos: la próxima, lo que tarda la justicia.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@cuesta", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado"},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@justicia", "salta": True}]),
        peque(760, 0, "riendo", entra="nada", acciones=[{"at": "@leemos", "salta": True}, {"at": "@justicia", "take": True}]),
        rot("¿CUÁNTO TE CUESTA?", 540, 470, "@cuesta", 84, "amarillo", golpe=True, out="@síguenos-0.4"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@justicia", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("coste_hijo", "¿Cuánto cuesta un hijo?", scenes, {"t": 3.3, "titulo": "Un hijo: 758 € al mes", "capitulo": None},
             ["Save the Children: «El coste de la crianza 2024»", "Deducción por maternidad: art. 81 Ley 35/2006 del IRPF",
              "Complemento de Ayuda para la Infancia: Ley 19/2021"],
             ("👶 Criar a un hijo cuesta 758 € al mes (Save the Children, precios de 2024)\n"
              "🍼 Bebé: 604 € · deducción por maternidad: 100 €/mes si la madre trabaja\n"
              "🤝 Rentas bajas: + 115 € de complemento de infancia → quedan 389 €\n"
              "🎂 A los 3 años se acaba la deducción · con 7 años cuesta 812 €\n"
              "📉 Renta media: 0 € al mes · renta baja: 57,50 € (un 7 %)\n"
              "⚖️ Sin contar ayudas autonómicas, guarderías gratis ni el IRPF\n"
              "💬 ¿Cuánto te cuesta a ti?\n"
              "➡️ Próximo: lo que tarda la justicia · 🔔 Síguenos · 📚 Fuentes en comentarios"),
             ("📚 Coste: Save the Children, «El coste de la crianza 2024» (diciembre de 2024, precios de 2024): 758 €/mes de media; 604 € de 0 a 3 años; "
              "812 € de 7 a 12. Ayudas 2026: deducción por maternidad de 100 €/mes hasta los 3 años (art. 81 LIRPF) y Complemento de Ayuda para la "
              "Infancia (Ley 19/2021): 115 € (<3), 80,50 € (3-6) y 57,50 € (6-18) en hogares con rentas bajas. Cálculo propio. No incluye ayudas "
              "autonómicas, educación 0-3 gratuita, cheque guardería ni mínimos del IRPF. ¿Ves un error? Dínoslo."),
             ["#PizarraPública", "#Crianza", "#Hijos", "#Familia", "#Ayudas", "#TuDinero", "#Maternidad"])
