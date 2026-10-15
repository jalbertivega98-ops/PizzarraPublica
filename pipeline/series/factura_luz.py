#!/usr/bin/env python3
"""«La hora a la que pones la lavadora» (v2, 15/10/2026): la factura de la luz con datos que sorprenden.

Investigación con fuentes: /mnt/project-files/insta/investigacion/luz_datos_llamativos.md
  PVPC del martes 13/10/2026 (REE/OMIE, sin impuestos): 0,3818 €/kWh de 20 a 21 h; 0,0338 €/kWh de 15 a 16 h (× 11).
    Con IVA 21 % e impuesto eléctrico (cálculo propio): lavadora 1 kWh 0,49 € vs 0,04 €; horno 2 kWh 0,97 € vs 0,09 €;
    aire 4 h 1,74 € vs 0,31 €. Madrugada ≈ 0,20 €/kWh: unas 6 veces la hora de la siesta.
  PVPC negativo el domingo 11/10/2026 de 12 a 17 h (REE). Horas negativas en el mercado mayorista: récord en 2026 (Montel).
  Vertidos de renovables 1.er semestre 2026: 2,5 TWh, el triple que un año antes (Aurora) ≈ 570.000 hogares un año (cálculo propio).
  FACUA, usuario medio PVPC (4,4 kW, 366 kWh): septiembre 2026 104,31 € vs septiembre 2021 102,71 €.
"""
from _tu_dinero import *  # noqa: F401,F403

PV = "PVPC 13/10/2026 (REE/OMIE) · con impuestos, cálculo propio"

scenes = [
    dict(id="gancho", fondo="salon", animo="curioso", footnote=PV, lines=[
        V("Poner la lavadora a las ocho de la tarde te cuesta once veces más que a las tres.", "energia"),
        V("Mismo día. Misma lavadora.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@once", "medio", "piz", 0.3, aire=220)],
       elements=[
        quien("piz", 320, 0, 0.75, "ilusionado", entra="izq", objeto="saco", pose="sostiene", acciones=[
            {"at": "@lavadora", "mira": "reloj"}, {"at": "@once", "take": True, "cara": "susto", "objeto": None},
            {"at": "@tres", "mira": "camara", "cara": "indignado"}, {"at": "@Misma", "pose": "jarras"}]),
        obj("reloj", 790, 760, "@ocho", 0.75, id="reloj", entra="pop", velocidad=5),
        rot("× 11", 600, 480, "@once", 160, C, golpe=True),
    ]),
    dict(id="precios", fondo="salon", animo="tension", trans="pan", footnote=PV, lines=[
        V("El martes: una lavadora a las ocho, 49 céntimos. A las tres, 4.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@4", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 300, 0, 0.72, "normal", entra="izq", acciones=[
            {"at": "@martes", "mira": "camara"}, {"at": "@49", "take": True, "cara": "susto"},
            {"at": "@4", "salta": True, "cara": "riendo"}]),
        obj("moneda", 780, 700, "@49", 0.9, entra="cae"),
        rot("20:00 → 0,49 €", 600, 470, "@49", 90, C, golpe=True),
        rot("15:00 → 0,04 €", 600, 590, "@4", 90, "verde", golpe=True),
    ]),
    dict(id="mas", fondo="salon", animo="comico", trans="iris", footnote=PV + " · horno 2 kWh · aire 4 h", lines=[
        V("El horno: 97 céntimos o 9. Cuatro horas de aire: 1,74 euros o 31 céntimos.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@aire", "medio", "sarcastica", 0.3, aire=200)],
       elements=[
        quien("sarcastica", 300, 0, 0.75, "burla", entra="izq", acciones=[
            {"at": "@horno", "cara": "sorpresa"}, {"at": "@97", "take": True}, {"at": "@aire", "pose": "jarras"},
            {"at": "@1,74", "tiembla": True}, {"at": "@31", "cara": "riendo", "salta": True}]),
        rot("HORNO: 0,97 € / 0,09 €", 600, 470, "@97", 70, "amarillo", golpe=True),
        rot("AIRE 4 H: 1,74 € / 0,31 €", 600, 580, "@1,74", 66, "amarillo", golpe=True),
    ]),
    dict(id="noche", fondo="rayos", animo="tension", musica="corte", trans="iris", footnote=PV + " · madrugada ≈ 0,20 €/kWh", lines=[
        V("Y lo de que de noche es barato ya no vale.", "sorpresa"),
        V("La madrugada cuesta seis veces más que la siesta.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@siesta", "medio", "piz", 0.3, aire=220)],
       elements=[
        quien("piz", 540, 0, 0.8, "normal", entra="pop", acciones=[
            {"at": "@noche", "cara": "pensativo", "pose": "encoge"}, {"at": "@vale", "take": True, "cara": "susto"},
            {"at": "@seis", "tropieza": True}]),
        rot("NOCHE ≠ BARATO", 540, 480, "@vale", 96, C, golpe=True, out="@seis"),
        rot("MADRUGADA × 6", 540, 480, "@seis", 110, C, golpe=True),
    ]),
    dict(id="negativo", fondo="calle", animo="comico", trans="pan", footnote="PVPC negativo el domingo 11/10/2026 de 12 a 17 h (REE) · vertidos: Aurora, 1.er semestre 2026", lines=[
        V("Pero el domingo, de doce a cinco de la tarde, la luz costó menos que cero.", "sorpresa"),
        V("Sobra tanta solar que en seis meses se tiraron 2,5 teravatios: la luz de 570.000 casas durante un año.", "normal", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@570.000", "abierto", dur=0.4)],
       elements=[
        obj("sol", 790, 560, "@domingo", 0.7, entra="pop"),
        quien("piz", 300, 0, 0.72, "normal", entra="nada", acciones=[
            {"at": "@domingo", "mira": "arriba"}, {"at": "@cero", "salta": True, "cara": "riendo", "pose": "arriba"},
            {"at": "@solar", "mira": "camara"}, {"at": "@tiraron", "take": True, "cara": "indignado"},
            {"at": "@570.000", "pose": "jarras"}]),
        rot("< 0 €", 540, 480, "@cero", 150, "verde", golpe=True, out="@tiraron"),
        rot("2,5 TWh TIRADOS", 540, 480, "@tiraron", 90, C, golpe=True, out="@570.000"),
        rot("= 570.000 CASAS", 540, 480, "@570.000", 90, "amarillo", golpe=True),
        monedas("@cero", 200, 900, 8),
    ]),
    dict(id="factura", fondo="oficina", animo="tension", trans="iris", footnote="FACUA, usuario medio PVPC (4,4 kW, 366 kWh): sep 2026 104,31 € · sep 2021 102,71 €", lines=[
        V("Y aun así, la factura media de septiembre fue más cara que en 2021: 104 euros.", "remate"),
    ], camara=[plano(0, "general", dur=0), plano("@104", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 300, 0, 0.75, "normal", entra="izq", objeto={"tipo": "contrato", "titulo": "FACTURA LUZ", "hojas": 1}, pose="sostiene",
              acciones=[{"at": "@septiembre", "mira": "camara"}, {"at": "@2021", "cara": "sorpresa"},
                        {"at": "@104", "take": True, "cara": "susto", "objeto": None}]),
        gags.dinero_vuela("@104", 360, 1000, 6),
        rot("SEP 2021: 102,71 €", 600, 470, "@2021", 72, "blanco", golpe=True),
        rot("SEP 2026: 104,31 €", 600, 580, "@104", 72, C, golpe=True),
    ]),
    dict(id="final", fondo="salon", animo="final", trans="iris", footnote="Precios PVPC por horas: ree.es", lines=[
        V("¿A qué hora pones tú la lavadora? Te leemos.", "normal"),
        V("Y síguenos: la próxima, la gasolina.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        quien("piz", 300, 0, 0.72, "normal", entra="nada", objeto="saco", pose="sostiene", acciones=[
            {"at": "@hora", "mira": "camara", "cara": "pensativo"}, {"at": "@leemos", "pose": "senala", "cara": "ilusionado", "objeto": None},
            {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}, {"at": "@gasolina", "salta": True}]),
        quien("pizon", 790, 0, 0.72, "normal", entra="nada", acciones=[{"at": "@lavadora", "cara": "pensativo"}, {"at": "@gasolina", "take": True}]),
        rot("¿A QUÉ HORA LA PONES?", 540, 470, "@hora", 80, "amarillo", golpe=True, out="@síguenos-0.4"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@gasolina", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("factura_luz", "La hora de la lavadora", scenes, {"t": 3.0, "titulo": "La lavadora: 11 veces más cara a las 20:00", "capitulo": None},
             ["REE/OMIE: precios PVPC por horas (13/10/2026 y 11/10/2026)", "Aurora Energy Research: vertidos 1.er semestre 2026",
              "FACUA: factura media PVPC septiembre 2026"],
             ("🧺 Poner la lavadora a las 20:00 cuesta 11 veces más que a las 15:00\n"
              "💶 Martes 13/10: 0,49 € frente a 0,04 €\n"
              "🔥 Horno: 0,97 € o 0,09 € · ❄️ 4 h de aire: 1,74 € o 0,31 €\n"
              "🌙 De noche ya no es barato: la madrugada, 6 veces más que la siesta\n"
              "☀️ El domingo, de 12 a 17 h, la luz costó menos que cero\n"
              "🗑️ En seis meses se tiraron 2,5 TWh de renovables: la luz de 570.000 casas un año\n"
              "🧾 Aun así, septiembre (104 €) fue más caro que en 2021\n"
              "💬 ¿A qué hora pones la lavadora?\n"
              "➡️ Próximo: la gasolina · 🔔 Síguenos · 📚 Fuentes en comentarios"),
             ("📚 Precios PVPC por horas de REE/OMIE: martes 13/10/2026, 0,3818 €/kWh de 20 a 21 h y 0,0338 €/kWh de 15 a 16 h; domingo "
              "11/10/2026, negativo de 12 a 17 h. Consumos (lavadora 1 kWh, horno 2 kWh, aire 4 h) e impuestos (IVA 21 % e impuesto eléctrico): "
              "cálculo propio. Vertidos de renovables del 1.er semestre de 2026: Aurora Energy Research. Factura media: FACUA (4,4 kW, 366 kWh). "
              "Los precios cambian cada hora y cada día. ¿Ves un error? Dínoslo."),
             ["#PizarraPública", "#FacturaDeLaLuz", "#PrecioLuz", "#PVPC", "#Ahorro", "#TuDinero", "#Energía"])
