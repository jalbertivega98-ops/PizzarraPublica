#!/usr/bin/env python3
"""«Pagado, prometido… ¿y sin cambiar?» (31/10/2026). El sistema de seguridad LZB que se cayó en Urda tenía contratada
su sustitución por el ERTMS desde 2021. Tema político, días después de un accidente con víctimas: sin gags sobre el
accidente, trenes sin cara, el choque no se dibuja. Pregunta de debate y «sigue a Piz» al final (petición de joel).

Guion y fuentes: /mnt/project-files/insta/guiones/propuestas_31oct.md, propuesta E (aprobada por joel el 31/10/2026, 09:37 UTC)
  16/09/2021: Adif adjudica a Thales 93.832.737,51 € (IVA incl.) la renovación de las instalaciones de seguridad y el ERTMS
    de la LAV Madrid-Sevilla, «con financiación europea», plazo 52 meses (~16/01/2026). Maldita 30/10/2026.
  Ministerio de Transportes, abril de 2025: la línea celebrará su 34 aniversario «completamente renovada… como el sistema
    ERTMS 2» (Maldita y Xataka 28-30/10/2026).
  Puente 28/10/2026 (EFE vía Infobae): el LZB «se está en proceso de reemplazar… porque ya no se fabrica».
  Artículo 14 (citado por Maldita 30/10): anexo enviado a Bruselas en mayo de 2026 para el sexto desembolso que confirma
    contratos «ejecutados» del objetivo 85. Maldita NO lo ha podido verificar → SIN CONFIRMAR.
  Puente 30/10/2026 (Maldita): «A la UE no se le engaña, se le aportan certificados de finalización de obra»; certificado
    provisional de la «colocación física del ERTMS» en junio de 2026.
  Adif, Declaración sobre la Red 2027 (Maldita): puesta en servicio en 2027.
  Feijóo: sistema «obsoleto», «Si no dimiten ellos, les dimitiremos en las urnas». Abascal: «un crimen» (HerQles 31/10).
  Puente no dimite; comparece el 3/11 ante la Diputación Permanente (El Independiente 29/10).
"""
import json

from _mundo import *  # noqa: F401,F403
from _mundo import OUT  # noqa: E402

R = "espana"
MAD = P(R, -3.70, 40.42)
URDA = P(R, -3.71, 39.41)
SEV = P(R, -5.98, 37.39)
LINEA = [(-3.70, 40.42), (-3.80, 39.85), (-3.71, 39.41), (-3.93, 38.98), (-4.10, 38.68), (-4.78, 37.89), (-5.98, 37.39)]
NOCHE_AZUL = (28, 40, 70)
MEDIO = [(MAD[0] + SEV[0]) / 2, (MAD[1] + SEV[1]) / 2]
FM = "Maldita, 30/10/2026: contrato Adif-Thales"


def tren(x, at, color, id, acciones=(), y=1080, scale=0.8, out=None):
    d = obj("tren", x, y, at, scale, id=id, entra="nada", props={"color": color, "cara": None, "vagones": 1},
            acciones=list(acciones))
    if out:
        d["out"] = out
    return d


def bocata(lineas, at, out=None, y=520, scale=0.72):
    d = obj("bocadillo", 540, y, at, scale, hud=True, entra="pop", sfx="pop", props={"lineas": lineas})
    if out:
        d["out"] = out
    return d


scenes = [
    # 1 · GANCHO: el dinero y el tren con el sistema viejo
    dict(id="gancho", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="tension", footnote=FM, lines=[
        V("En 2021 se pagaron 93,8 millones para cambiar el sistema de seguridad que falló en Urda.", "intriga"),
        V("El día del choque, seguía puesto el viejo.", "remate", 0.25),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@viejo", "general", [540, 1000], 0.8, zoom=1.08)],
       elements=[
        obj("fajo", 540, 760, 0, 1.1, hud=True, entra="cae", sfx="kaching", out="@día"),
        etq("93,8 MILLONES", 540, 1040, "@93,8", "amarillo", 0.95, hud=True, out="@día"),
        rot("PARA CAMBIARLO", 540, 420, "@cambiar", 90, "blanco", out="@día"),
        obj("via", 540, 1184, "@día", 1.0, entra="nada", props={"ancho": 1600}),
        tren(-700, "@día", "azul", "ave", acciones=[{"at": "@día", "x": 540, "dur": 1.4}]),
        etq("SISTEMA LZB · DE 1992", 540, 760, "@seguía", "rojo", 0.8, hud=True),
        sello("CONFIRMADO", "verde", 1290, "@viejo"),
    ]),
    # 2 · EL CONTRATO: el mapa con la línea Madrid-Sevilla; Thales, fondos europeos y el plazo en el calendario
    dict(id="contrato", fondo="mar_mapa", limites=LIM, animo="curioso", trans="iris", footnote=FM, lines=[
        V("Septiembre de 2021. Adif encarga a Thales cambiar el LZB de la Madrid-Sevilla por el ERTMS, con fondos europeos."),
        V("Plazo: 52 meses. O sea, hacia enero de 2026.", "normal", 0.2),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@Madrid-Sevilla", MEDIO, 2.0, 1.2), zoom("@Plazo", MEDIO, 1.6, 0.8)],
       elements=[
        mapa(R, 0, 1.4, acciones=[{"at": "@Madrid-Sevilla", "props": {"lineas": [linea("ave", LINEA, "azul", 1.2, ancho=8)]}, "sfx": "rotulador"}]),
        obj("chincheta", MAD[0] + 6, MAD[1], "@Madrid-Sevilla", 0.1, props={"diseno": "espana"}, entra="cae"),
        obj("chincheta", SEV[0] + 6, SEV[1], "@Madrid-Sevilla+0.6", 0.1, props={"diseno": "espana"}, entra="cae"),
        etq("ADIF → THALES · 93,8 M€", 540, 380, "@Thales", "amarillo", 0.75, hud=True, out="@Plazo"),
        obj("bandera", 860, 1520, "@europeos", 0.8, hud=True, entra="abajo", props={"diseno": "ue"}, out="@Plazo"),
        obj("calendario", 540, 920, "@Plazo", 0.75, hud=True, entra="crece", sfx="papel",
            props={"mes": "ENERO 2026", "inicio": 3, "dias": 31, "marcados": [16], "colores": {16: "rojo"}}),
        etq("52 MESES", 540, 380, "@Plazo", "rojo", 0.8, hud=True),
        sello("CONTRATO PÚBLICO", "verde", 1290, "@Plazo+0.4"),
    ]),
    # 3 · LA PROMESA: Transportes, abril de 2025
    dict(id="promesa", fondo="oficina", animo="curioso", trans="papel",
         footnote="Transportes, abril 2025 (vía Maldita y Xataka)", lines=[
        V("En abril de 2025, Transportes lo prometió: la línea, «completamente renovada», con el ERTMS 2."),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@renovada", "general", [540, 900], 0.6, zoom=1.06)],
       elements=[
        obj("documento", 600, 780, 0.1, 0.9, hud=True, id="doc", entra="nada", dibujo=1.0, sfx="papel", props={
            "titulo": "TRANSPORTES · ABRIL 2025", "ancho": 760,
            "articulos": [{"id": "a", "titulo": "LÍNEA MADRID-SEVILLA", "lineas": ["«completamente renovada»", "con el sistema ERTMS 2"]}]},
            acciones=[{"at": "@renovada", "props": {"resalta": ["a"]}}]),
        quien("piz", 220, 0, 0.5, "pensativo", y=1500, entra="izq", acciones=[
            {"at": "@prometió", "pose": "piensa", "mira": "der"}, {"at": "@renovada", "cara": "esceptica"}]),
        sello("DECLARACIÓN", "azul", 1290, "@ERTMS", x=700),
    ]),
    # 4 · EL 28 DE OCTUBRE: funcionaba el LZB, se cayó; Puente lo admite
    dict(id="urda", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="tension", trans="corte",
         footnote="Puente, 28/10/2026 (EFE vía Infobae)", lines=[
        V("El 28 de octubre, en Urda, el que funcionaba era el LZB. Y se cayó."),
        V("Puente lo admite: está «en proceso de reemplazar», porque ya no se fabrica.", "normal", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Puente", "general", [540, 1000], 0.5)],
       elements=[
        obj("via", 540, 1184, 0, 1.0, entra="nada", props={"ancho": 1600}, out="@Puente"),
        tren(540, 0, "azul", "ave", out="@Puente"),
        etq("LZB", 540, 760, "@LZB", "amarillo", 0.9, hud=True, out="@cayó"),
        sello("LZB CAÍDO", "rojo", 1290, "@cayó", out="@Puente"),
        obj("lazo", 960, 300, 0, 0.35, hud=True, entra="nada"),
        quien("puente", 540, "@Puente", 0.55, "serio", entra="abajo", acciones=[
            {"at": "@admite", "pose": "encoge"}, {"at": "@fabrica", "pose": "manos_juntas"}]),
        bocata(["PUENTE:", "«en proceso", "de reemplazar»"], "@admite"),
        sello("DECLARACIÓN", "azul", 1290, "@fabrica"),
    ]),
    # 5 · ¿SE LE DIJO A BRUSELAS QUE YA ESTABA HECHO? Sin confirmar, y la versión del ministro
    dict(id="bruselas", fondo={"tipo": "plano", "color": (30, 56, 120)}, animo="tension", trans="barrido",
         footnote="Artículo 14 y Maldita, 30/10/2026", lines=[
        V("¿Se le dijo a Bruselas que ya estaba hecho? Artículo 14 publica un documento de mayo que da los contratos por ejecutados.", "intriga"),
        V("Maldita no lo ha podido verificar. Y Puente lo niega: «A la UE no se le engaña». Solo certificaron que estaba colocado.", "normal", 0.2),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Puente", "general", [540, 1000], 0.6)],
       elements=[
        obj("bandera", 860, 1300, 0, 0.9, entra="abajo", props={"diseno": "ue"}),
        obj("documento", 470, 800, "@documento", 0.85, hud=True, id="anexo", entra="nada", dibujo=1.0, sfx="papel", props={
            "titulo": "ANEXO A BRUSELAS", "subtitulo": "MAYO 2026", "ancho": 720,
            "articulos": [{"id": "a", "titulo": "CONTRATOS", "lineas": ["«ejecutados»"]}]},
            acciones=[{"at": "@ejecutados", "props": {"resalta": ["a"]}}], out="@Puente"),
        sello("SIN CONFIRMAR", "naranja", 330, "@verificar"),
        quien("puente", 360, "@Puente", 0.55, "serio", entra="izq", acciones=[
            {"at": "@niega", "pose": "senala"}, {"at": "@colocado", "pose": "encoge"}]),
        bocata(["PUENTE:", "«A la UE", "no se le engaña»"], "@niega", out="@colocado"),
        bocata(["Certificado:", "equipo «colocado»", "(junio 2026)"], "@colocado"),
    ]),
    # 6 · LOS PARTIDOS: Feijóo, Abascal y el ministro que no dimite
    dict(id="partidos", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="tension", trans="corte",
         footnote="HerQles 31/10 · El Independiente 29/10/2026", lines=[
        V("Feijóo habla de un sistema «obsoleto»: «si no dimiten ellos, les dimitiremos en las urnas». Abascal lo llama «un crimen»."),
        V("Puente no dimite. Comparece el 3 de noviembre.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        quien("feijoo", 230, 0, 0.5, "serio", entra="pop", acciones=[{"at": "@dimitiremos", "pose": "senala"}]),
        quien("abascal", 540, "@Abascal", 0.5, "enfado", entra="pop", acciones=[{"at": "@crimen", "pose": "punos"}]),
        quien("puente", 850, "@Puente", 0.5, "serio", entra="pop", acciones=[{"at": "@dimite", "pose": "cruzados"}]),
        bocata(["FEIJÓO (PP):", "«les dimitiremos", "en las urnas»"], "@Feijóo", out="@Abascal"),
        bocata(["ABASCAL (VOX):", "«un crimen»"], "@Abascal", out="@Puente"),
        bocata(["PUENTE (PSOE):", "no dimite", "Congreso · 3 nov."], "@Puente"),
        sello("DECLARACIONES", "azul", 330, "@urnas"),
    ]),
    # 7 · CIERRE: 2027, la pregunta de debate y «sigue a Piz»
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Adif, Declaración sobre la Red 2027 (vía Maldita)",
         lines=[
        V("Ahora Adif habla de ponerlo en servicio en 2027."),
        V("¿Retraso normal de una obra así, o alguien tiene que dimitir? Te leo en comentarios.", "energia", 0.2),
        V("Y sigue a Piz para no perderte nada antes del 29N.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        obj("calendario", 800, 820, 0, 0.42, hud=True, entra="crece", sfx="papel", out="@Retraso",
            props={"mes": "¿2027?", "inicio": 4, "dias": 31, "tachados": [1, 2, 3, 4, 5, 6, 7, 8]}),
        quien("piz", 380, 0, 0.6, "esceptica", entra="abajo", acciones=[
            {"at": "@2027", "pose": "jarras", "mira": "der"}, {"at": "@Retraso", "pose": "piensa", "mira": "camara", "cara": "pensativo"},
            {"at": "@dimitir", "pose": "senala", "mira": "camara"}, {"at": "@leo", "cara": "ilusionado"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("¿RETRASO O DIMISIÓN?", 540, 420, "@Retraso", 70, "amarillo", golpe=True, out="@sigue-0.3"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@29N", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("lzb_pagado", "Pagado, prometido… ¿y sin cambiar?", scenes,
             {"t": 3.2, "titulo": "Pagado, prometido… ¿y sin cambiar?", "capitulo": None},
             ["Maldita (30/10/2026): Adif adjudicó a Thales en 2021 la sustitución del LZB por ERTMS en Madrid-Sevilla",
              "Maldita (30/10/2026): qué sabemos de la comunicación del Gobierno a Bruselas (anexo de Artículo 14, sin verificar)",
              "Infobae/EFE (28/10/2026): Puente, el LZB «en proceso de ser reemplazado»",
              "Vozpópuli (30/10/2026): la oferta de Thales, un 28,45 % por debajo del presupuesto",
              "Xataka (28/10/2026): el Ministerio prometió la línea renovada con ERTMS 2",
              "HerQles (31/10/2026): Feijóo y Abascal; El Independiente (29/10/2026): comparecencia del 3/11",
              "Tema político tras un accidente con víctimas: sin gags sobre el accidente, trenes sin cara, el choque no se dibuja"],
             ("🚆 Pagado, prometido… ¿y sin cambiar?\n"
              "💶 2021: Adif adjudica 93,8 M€ (fondos europeos) para cambiar el LZB por el ERTMS en la Madrid-Sevilla\n"
              "📅 Plazo: 52 meses, hacia enero de 2026\n"
              "🗣️ 2025: Transportes promete la línea «completamente renovada»\n"
              "⚠️ 28/10: en Urda seguía el LZB, y se cayó\n"
              "❓ ¿Se dijo a Bruselas que estaba hecho? Sin confirmar · Puente: «A la UE no se le engaña»\n"
              "💬 ¿Retraso normal o alguien tiene que dimitir? Te leo 👇\n"
              "🔔 Sigue a Piz para no perderte nada antes del 29N · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Maldita 30/10/2026 (contrato Adif-Thales y anexo a Bruselas, sin verificar) · EFE/Infobae 28/10 · "
             "Vozpópuli 30/10 · Xataka 28/10 · HerQles 31/10 · El Independiente 29/10. ¿Ves un error? Dínoslo.",
             ["#Urda", "#Adif", "#OscarPuente", "#ERTMS", "#29N", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
