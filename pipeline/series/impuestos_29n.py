#!/usr/bin/env python3
"""«¿Quién te baja más los impuestos?» (lun 9/11/2026, 15:00). Lo que prometen PSOE, PP y Vox para tu bolsillo.
Aprobado por joel el 4/11/2026 21:21 UTC (propuesta 4 de /mnt/project-files/insta/guiones/propuestas_5nov.md).
Ningún partido ha publicado aún su programa completo del 29N: son anuncios y documentos previos (sellos).
Fuentes:
  Vox: Valencia Plaza / Demócrata / Infobae 4/11/2026 (Figaredo, Madrid Foro): IVA general del 21 al 18 %, revisar
    52.000 M€ en subvenciones; «No creo que saquemos el 100 %». IRPF: 0 € hasta 22.000 € y 15 % hasta 70.000 € (programa
    2025; descrito por Infobae 13/10/2026); Hacienda (Arcadi España) cifra el coste en 85.000 M€ (Infobae 13/10); Vox, 46.000 M€.
  PP: decálogo económico de septiembre de 2026 (Euro Weekly 24/09, Forbes 5/10, pp.es): IVA de alimentos básicos del 4 al 0 %;
    luz y gas del 21 al 10 %; mínimo por hijo de 2.400 a 4.800 € (primer hijo); deflactar el IRPF. Sin coste publicado.
  PSOE: no promete una bajada general. SMI de 1.221 € exento de IRPF (Hacienda 17/02/2026); decretos de vivienda del 6/10/2026
    (préstamos ICO hasta 50.000 € sin intereses). Forbes 5/10: defiende la «progresividad fiscal».
"""
from _mundo import *  # noqa: F401,F403

VERDE_OSC = (22, 60, 48)


def tarjeta(texto, x, y, at, color, out=None, scale=0.62):
    d = etq(texto, x, y, at, color, scale, hud=True)
    if out:
        d["out"] = out
    return d


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo="calle", animo="tension", footnote="Anuncios de PSOE, PP y Vox, sept.-nov. 2026", lines=[
        V("Los tres dicen que van a cuidar tu bolsillo. Pero no te prometen lo mismo.", "intriga"),
        V("Uno baja el IVA de todo. Otro, el de la comida. Y otro no promete bajarlo.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Uno", "general", [540, 960], 0.4, zoom=1.05)],
       elements=[
        quien("abascal", 230, 0, 0.46, "normal", entra="izq", acciones=[{"at": "@todo", "pose": "senala_arriba", "cara": "riendo"}]),
        quien("feijoo", 540, 0.1, 0.46, "normal", entra="abajo", acciones=[{"at": "@comida", "pose": "senala", "cara": "ilusionado"}]),
        quien("sanchez", 850, 0.2, 0.46, "normal", entra="der", acciones=[{"at": "@promete#2", "pose": "cruzados", "cara": "serio"}]),
        rot("¿QUIÉN TE BAJA MÁS?", 540, 420, 0, 90, "amarillo", golpe=True, out="@Uno", fx=[{"at": "@bolsillo", "do": "latir"}]),
        obj("hucha", 540, 640, "@bolsillo", 0.5, hud=True, entra="pop", sfx="kaching", out="@Uno"),
        tarjeta("IVA DE TODO", 300, 540, "@todo", "vox", scale=0.5),
        tarjeta("IVA DE LA COMIDA", 540, 640, "@comida", "pp", scale=0.5),
        tarjeta("NO PROMETE BAJARLO", 760, 740, "@bajarlo", "psoe", scale=0.5),
    ]),
    # 2 · VOX
    dict(id="vox", fondo={"tipo": "plano", "color": VERDE_OSC}, animo="curioso", trans="barrido",
         footnote="Figaredo 4/11 (Valencia Plaza, Infobae) · Infobae 13/10/2026", lines=[
        V("Vox: el IVA general, del 21 al 18. Algo de 121 euros pasaría a costar 118."),
        V("Y en el IRPF, nada hasta 22.000 euros al año, y un 15 por ciento hasta 70.000.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@IRPF", "general", [540, 900], 0.4, zoom=1.05)],
       elements=[
        rot("VOX", 540, 400, 0, 110, "verde"),
        obj("etiqueta", 540, 680, "@IVA", 1.0, hud=True, entra="pop", sfx="kaching", props={"texto": "IVA 21 %", "color": "amarillo"}, out="@18"),
        obj("etiqueta", 540, 680, "@18", 1.0, hud=True, entra="pop", sfx="kaching", props={"texto": "IVA 18 %", "color": "verde"}, out="@121"),
        obj("etiqueta", 540, 680, "@121", 1.0, hud=True, entra="pop", sfx="kaching", props={"texto": "121 € → 118 €".replace("→", "·"), "color": "verde"}, out="@IRPF"),
        obj("calculadora", 300, 900, "@IRPF", 0.7, hud=True, entra="crece", sfx="pop", props={"texto": "0 €"}),
        tarjeta("0 € HASTA 22.000", 680, 860, "@22.000", "verde"),
        tarjeta("15 % HASTA 70.000", 680, 1000, "@70.000", "verde"),
        quien("piz", 1250, "@118-0.4", 0.42, "normal", y=1660, entra="nada", acciones=[
            {"at": "@118-0.4", "x": 900, "dur": 0.5}, {"at": "@118", "cara": "ilusionado", "salta": True}]),
        sello("ANUNCIO + PROGRAMA 2025", "azul", 1240, "@IRPF"),
    ]),
    # 3 · PP
    dict(id="pp", fondo="calle", animo="curioso", trans="papel", footnote="Decálogo económico del PP, sept. 2026 (Forbes 5/10 · pp.es)", lines=[
        V("El PP: IVA cero en la comida básica, como el pan, la leche o los huevos."),
        V("La luz y el gas, del 21 al 10. Y el doble por cada hijo en la renta: de 2.400 a 4.800 euros.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@luz", "general", [540, 960], 0.4, zoom=1.05)],
       elements=[
        rot("PP", 540, 400, 0, 110, "azul"),
        edif("supermercado", 540, 0, 0.5, entra="nada", dibuja=0.6, out="@luz"),
        tarjeta("IVA 0 % COMIDA BÁSICA", 540, 600, "@cero", "pp", out="@luz"),
        obj("etiqueta", 300, 700, "@luz", 0.9, hud=True, entra="pop", sfx="kaching", props={"texto": "LUZ Y GAS: 10 %", "color": "amarillo"}),
        obj("etiqueta", 780, 840, "@hijo", 0.9, hud=True, entra="pop", sfx="kaching", props={"texto": "HIJO: 4.800 €", "color": "verde"}),
        quien("pizon", 780, "@luz", 0.45, "ilusionado", entra="der", acciones=[{"at": "@gas", "cara": "riendo"}, {"at": "@doble", "salta": True}, {"at": "@4.800", "pose": "arriba"}]),
        sello("DECÁLOGO", "azul", 1240, "@básica"),
    ]),
    # 4 · PSOE
    dict(id="psoe", fondo="oficina", animo="curioso", trans="barrido", footnote="Hacienda 17/02/2026 · decretos de vivienda 6/10/2026 · Forbes 5/10", lines=[
        V("El PSOE no promete una bajada general. Defiende que el que cobra el salario mínimo no pague IRPF."),
        V("Y préstamos sin intereses de hasta 50.000 euros para tu primera casa.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        rot("PSOE", 540, 400, 0, 110, "rojo"),
        obj("etiqueta", 540, 640, "@mínimo", 0.9, hud=True, entra="pop", sfx="kaching", props={"texto": "SMI: 0 € DE IRPF", "color": "rojo"}, out="@préstamos"),
        edif("casa", 540, "@préstamos", 0.5, entra="crece", sfx="pop", dibuja=0.5),
        tarjeta("HASTA 50.000 € AL 0 %", 540, 640, "@50.000", "psoe"),
        quien("piz", 860, 0.2, 0.42, "pensativo", entra="der", acciones=[{"at": "@general", "pose": "encoge"}, {"at": "@casa", "cara": "ilusionado"}]),
        sello("HECHO + DECRETO", "azul", 1240, "@IRPF"),
    ]),
    # 5 · OJO: ¿y quién lo paga?
    dict(id="ojo", fondo={"tipo": "plano", "color": VERDE_OSC}, animo="tension", trans="corte",
         footnote="Infobae 13/10 y 4/11/2026", lines=[
        V("Ojo: Vox dice que su rebaja cuesta 46.000 millones. Hacienda dice 85.000."),
        V("Y hasta su número dos en economía admite: «No creo que saquemos el 100 %». El PP no ha dicho cuánto cuesta la suya.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        obj("calculadora", 300, 760, 0, 0.7, hud=True, entra="crece", sfx="pop", props={"texto": "46"}),
        obj("calculadora", 780, 760, "@Hacienda", 0.7, hud=True, entra="crece", sfx="golpe", props={"texto": "85"}),
        tarjeta("VOX: 46.000 M", 300, 1020, "@46.000", "verde", scale=0.5),
        tarjeta("HACIENDA: 85.000 M", 780, 1120, "@85.000", "rojo", scale=0.5),
        obj("bocadillo", 540, 520, "@admite", 0.7, hud=True, entra="pop", sfx="pop", props={"lineas": ["«No creo que", "saquemos el 100 %»"], "cola": (0, 1)}, out="@PP"),
        tarjeta("PP: COSTE ¿?", 540, 520, "@PP", "azul"),
        quien("piz", 540, "@admite", 0.42, "esceptica", y=1600, entra="abajo", acciones=[{"at": "@100", "pose": "encoge"}, {"at": "@PP", "pose": "piensa", "cara": "confundido"}, {"at": "@cuesta", "mira": "camara"}]),
        sello("CIFRAS QUE NO CUADRAN", "naranja", 1300, "@85.000"),
    ]),
    # 6 · FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Cuál te convence más? A, Vox. B, PP. C, PSOE. Te leo."),
        V("Y sigue a Piz: te contamos qué cumple cada uno.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@convence", "pose": "piensa", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        tarjeta("A · VOX", 220, 700, "@Vox", "vox", out="@sigue", scale=0.55),
        tarjeta("B · PP", 540, 600, "@PP", "pp", out="@sigue"),
        tarjeta("C · PSOE", 860, 700, "@PSOE", "psoe", out="@sigue"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@cumple", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("impuestos_29n", "¿Quién te baja más los impuestos?", scenes,
             {"t": 5.5, "titulo": "¿Quién te baja más los impuestos?", "capitulo": None},
             ["Vox: Figaredo, Madrid Foro 4/11/2026 (Valencia Plaza, Demócrata, Infobae); IRPF del programa 2025 (Infobae 13/10)",
              "Hacienda: coste de 85.000 M€ de la rebaja de Vox (Infobae 13/10/2026)",
              "PP: decálogo económico de septiembre de 2026 (Euro Weekly 24/09, Forbes 5/10)",
              "PSOE: SMI exento de IRPF (Hacienda 17/02/2026), decretos de vivienda 6/10/2026, Forbes 5/10",
              "Ningún partido ha publicado aún su programa completo del 29N"],
             ("💶 ¿Quién te baja más los impuestos?\n"
              "🟢 Vox: IVA del 21 al 18 % · 0 € de IRPF hasta 22.000 €\n"
              "🔵 PP: IVA 0 % en comida básica · luz y gas al 10 % · el doble por hijo\n"
              "🔴 PSOE: sin bajada general · SMI sin IRPF · préstamos de hasta 50.000 € al 0 % para tu casa\n"
              "🧮 Ojo: Vox dice que cuesta 46.000 M · Hacienda, 85.000 M · el PP no da cifra\n"
              "💬 ¿Cuál te convence? A, B o C 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Valencia Plaza/Infobae 4/11/2026 (Vox), Infobae 13/10 (Hacienda), decálogo PP sept. 2026 (Forbes 5/10), "
             "Hacienda 17/02/2026 y decretos 6/10 (PSOE). Aún no hay programas completos. ¿Ves un error? Dínoslo.",
             ["#29N", "#impuestos", "#IVA", "#IRPF", "#PSOE", "#PP", "#Vox", "#pizarrapublica"],
             series_tag="TU DINERO, CON DATOS")
