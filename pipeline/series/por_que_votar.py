#!/usr/bin/env python3
"""«¿Por qué votar a…?» (3/11/2026): tres episodios gemelos (PSOE, PP, Vox) antes del 29N.

Misma plantilla y duración para los tres: gancho «con todo lo que ha pasado», 4 razones del propio partido (con sello
HECHO / DOCUMENTO / ANUNCIO / PENDIENTE), un único «Ojo» y cierre «¿Te convence?» + sigue a Piz. Piz no pide el voto:
presenta las razones «las suyas, no las mías».

Aprobado por joel el 3/11/2026 19:49 UTC («Haz los videos»).
Guion y fuentes: /mnt/project-files/insta/guiones/por_que_votar_29n.md (copia en docs/series/por_que_votar/).
Uso: python3 series/por_que_votar.py [psoe|pp|vox]  (sin argumento, los tres)
"""
import sys

from _mundo import *  # noqa: F401,F403
from _mundo import quien as _quien


def quien(q, x, at=0.0, scale=0.75, *a, **kw):
    """Personajes un 18 % más grandes que en la plantilla (salvo los diminutos sobre el mapa)."""
    return _quien(q, x, at, scale * 1.18 if scale > 0.3 else scale, *a, **kw)

PARTIDO = {
    "psoe": dict(nombre="PSOE", art="al PSOE", color=(225, 30, 40), fondo=(70, 16, 22), lider="sanchez", col="psoe"),
    "pp": dict(nombre="PP", art="al PP", color=(0, 104, 180), fondo=(14, 36, 78), lider="feijoo", col="pp"),
    "vox": dict(nombre="VOX", art="a Vox", color=(90, 175, 40), fondo=(22, 56, 20), lider="abascal", col="vox"),
}
OSCURO = (34, 36, 46)
SELLOS = {"hecho": ("✔ HECHO", "verde"), "doc": ("DOCUMENTO", "azul"), "anuncio": ("ANUNCIO", "amarillo"),
          "pendiente": ("PENDIENTE · SE VOTA EL 12/11", "naranja")}
F_ENC = "SocioMétrica y Sigma Dos, 26/10/2026"


def bocata(lineas, at, out=None, x=540, y=520, scale=0.72, cola=(-1, 1)):
    d = obj("bocadillo", x, y, at, scale, hud=True, entra="pop", sfx="pop", props={"lineas": lineas, "cola": cola})
    if out:
        d["out"] = out
    return d


def tit(n, tema, at=0.0):
    """Rótulo fijo arriba: «RAZÓN 2/4 · LA PENSIÓN»."""
    return rot(f"RAZÓN {n}/4 · {tema}", 540, 400, at, 66, "amarillo", golpe=True)


def marca(tipo, at, texto=None):
    t, c = SELLOS[tipo]
    return sello(texto or t, c, 1240, at)


def gancho(p, extra=()):
    P_ = PARTIDO[p]
    return dict(id="gancho", fondo={"tipo": "plano", "color": P_["fondo"]}, animo="tension", footnote="Elecciones generales · 29 de noviembre de 2026",
                lines=[V(f"¿Por qué votaría alguien {P_['art']}, con todo lo que ha pasado?", "intriga"),
                       V("Te doy sus cuatro razones. Las suyas, no las mías.", "remate", 0.15)],
                camara=[plano(0, "general", [540, 960], 0), plano("@pasado", "general", [540, 900], 0.5, zoom=1.08),
                        plano("@cuatro", "general", [540, 980], 0.4)],
                elements=[
                    rot("¿POR QUÉ VOTAR", 540, 380, 0, 100, "blanco", golpe=True),
                    rot(f"{P_['art'].upper()}?", 540, 500, 0.25, 130, "amarillo", golpe=True),
                    obj("urna", 540, 1080, 0, 0.75, entra="nada", props={"texto": "29N", "llena": 0.3}),
                    obj("papeleta", 540, 620, 0.1, 0.8, entra="cae", sfx="papel", props={"color": P_["col"], "texto": P_["nombre"]},
                        acciones=[{"at": "@alguien", "y": 1000, "dur": 0.6}, {"at": "@todo", "sale": True}]),
                    quien(P_["lider"], 900, "@alguien", 0.48, "normal", entra="der", acciones=[
                        {"at": "@pasado", "cara": "preocupado", "pose": "encoge"}, {"at": "@razones", "cara": "ilusionado", "pose": "arriba"}]),
                    quien("piz", 190, 0, 0.48, "pensativo", entra="izq", acciones=[
                        {"at": "@pasado", "pose": "piensa", "mira": "der"}, {"at": "@cuatro", "pose": "senala", "cara": "ilusionado"},
                        {"at": "@suyas", "pose": "manos_juntas", "cara": "normal", "mira": "camara"}]),
                    obj("contador", 540, 760, "@cuatro", 0.5, hud=True, entra="pop", sfx="kaching",
                        props={"valor": 4, "desde": 0, "sufijo": " RAZONES", "ancho": 700}),
                    quien("critica", 540, "@suyas", 0.42, "esceptica", entra="abajo", acciones=[{"at": "@mías", "pose": "cruzados"}]),
                    *extra,
                ])


def ojo(p, lines, footnote, elements, camara):
    return dict(id="ojo", fondo={"tipo": "plano", "color": OSCURO}, animo="tension", trans="corte", footnote=footnote, lines=lines,
                camara=camara,
                elements=[rot("OJO", 540, 380, 0, 140, "rojo", golpe=True),
                          quien("critica", 860, 0, 0.42, "esceptica", entra="der", acciones=[{"at": "@Ojo", "pose": "senala_izq", "mira": "izq"},
                                                                                {"at": "@Ojo+2.2", "pose": "jarras", "cara": "indignado"}]),
                          *elements])


def cierre(p, siguiente=None):
    P_ = PARTIDO[p]
    if siguiente:
        S_ = PARTIDO[siguiente]
        lines = [V("¿Te convence? Comenta sí o no.", "energia"),
                 V(f"Y sigue a Piz: mañana, por qué votar {S_['art']}.", "energia", 0.15)]
        extra = [obj("atril", 830, SUELO_ATRIL, "@mañana", 0.5, entra="der", sfx="whoosh", props={"texto": S_["nombre"], "color": S_["col"]}),
                 rot("MAÑANA:", 540, 560, "@mañana", 70, "blanco", golpe=True),
                 rot(f"¿POR QUÉ {S_['nombre']}?", 540, 650, "@votar", 80, "amarillo", golpe=True)]
        piz_acc = [{"at": "@mañana", "pose": "senala", "mira": "der", "cara": "ilusionado"}]
    else:
        lines = [V("¿Te convence? Comenta sí o no.", "energia"),
                 V("¿Y tú, con cuál de los tres te quedas? Sigue a Piz.", "energia", 0.15)]
        extra = [*atriles(t=("@tres", "@tres+0.15", "@tres+0.3"))]
        piz_acc = [{"at": "@tres", "pose": "arriba", "cara": "ilusionado", "mira": "camara"}]
    return dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Fuentes en el comentario fijado", lines=lines,
                camara=[plano(0, "general", [540, 1000], 0), plano("@Piz", "medio", "piz", 0.5, aire=320)],
                elements=[
                    etq("SÍ", 300, 760, "@sí", "verde", 0.9, hud=True, out="@Piz-0.2" if not siguiente else "@mañana-0.2"),
                    etq("NO", 780, 760, "@no", "rojo", 0.9, hud=True, out="@Piz-0.2" if not siguiente else "@mañana-0.2"),
                    rot("¿TE CONVENCE?", 540, 420, 0, 110, "amarillo", golpe=True, out="@Piz-0.2"),
                    quien("piz", 540 if not siguiente else 300, 0, 0.55, "normal", entra="abajo", acciones=[
                        {"at": "@sí", "pose": "senala_izq", "mira": "izq"}, {"at": "@no", "pose": "senala", "mira": "der"},
                        *piz_acc, {"at": "@Piz", "pose": "saluda", "cara": "riendo", "mira": "camara"}]),
                    rot("SIGUE A PIZ", 540, 420, "@Piz", 110, "amarillo", fx=[{"at": "@Piz+0.4", "do": "latir"}]),
                    *extra,
                ])


# ───────────────────────────── PSOE ─────────────────────────────
F_SMI = "SMI 2018: 735,90 € · 2026: 1.221 € (14 pagas) · Hacienda 17/02/2026"


def psoe():
    return [
        gancho("psoe"),
        dict(id="sueldo", fondo="oficina", animo="curioso", trans="barrido", footnote=F_SMI, lines=[
            V("Una, el sueldo: el salario mínimo ha subido un 66 por ciento desde 2018,", "normal"),
            V("y quien lo cobra ya no paga IRPF.", "remate", 0.1),
        ], camara=[plano(0, "general", [540, 960], 0), plano("@66", "general", [540, 820], 0.5, zoom=1.08),
                   plano("@IRPF", "general", [540, 980], 0.5)],
           elements=[
            tit(1, "EL SUELDO"),
            obj("contador", 540, 600, "@salario", 0.62, hud=True, entra="pop", sfx="kaching", id="smi",
                props={"valor": 1221, "desde": 736, "sufijo": " €/MES", "ancho": 820}),
            etq("+66 % DESDE 2018", 540, 790, "@66", "verde", 0.75, hud=True),
            obj("contrato", 300, 1050, "@sueldo", 0.8, entra="cae", sfx="papel", props={"titulo": "NÓMINA"}),
            quien("piz", 800, 0, 0.45, "normal", entra="der", acciones=[
                {"at": "@66", "cara": "ilusionado", "salta": True}, {"at": "@desde", "pose": "senala_arriba", "mira": "izq"},
                {"at": "@2018", "pose": "arriba", "cara": "riendo"}, {"at": "@IRPF", "pose": "jarras", "cara": "riendo"}]),
            quien("hacienda", 300, "@cobra", 0.42, "normal", entra="izq", acciones=[
                {"at": "@paga", "cara": "confundido", "pose": "encoge"}, {"at": "@IRPF+0.3", "x": -300, "dur": 0.9}]),
            etq("IRPF: 0 €", 540, 940, "@IRPF", "amarillo", 0.75, hud=True),
            marca("hecho", "@IRPF+0.2"),
        ]),
        dict(id="pension", fondo="salon", animo="alegre", trans="papel", footnote="Mitin de Zaragoza, 14/10/2026 (politicaelectoral.com)", lines=[
            V("Dos, la pensión: promete cuatro años más subiéndola con el IPC,", "normal"),
            V("y dejar 20.000 millones en la hucha de las pensiones.", "normal", 0.1),
        ], camara=[plano(0, "general", [540, 980], 0), plano("@hucha", "general", [540, 1080], 0.5, zoom=1.1)],
           elements=[
            tit(2, "LA PENSIÓN"),
            quien("sanchez", 820, 0, 0.45, "normal", entra="der", acciones=[{"at": "@promete", "pose": "senala_arriba", "cara": "ilusionado"}]),
            etq("PENSIÓN = IPC", 420, 600, "@IPC", "amarillo", 0.7, hud=True),
            etq("+4 AÑOS", 420, 740, "@cuatro", "blanco", 0.65, hud=True),
            obj("hucha", 380, 1180, "@millones", 0.85, entra="crece", sfx="pop", props={"cara": "ilusionado"}),
            monedas("@hucha", 220, 560, 10),
            obj("contador", 540, 900, "@20.000", 0.55, hud=True, entra="pop", sfx="kaching",
                props={"valor": 20000, "desde": 0, "sufijo": " M€", "ancho": 700}),
            quien("piz", 160, 0.2, 0.36, "normal", entra="izq", acciones=[{"at": "@hucha", "cara": "sorpresa", "take": True}]),
            marca("anuncio", "@pensiones"),
        ]),
        dict(id="casa", fondo="calle", animo="curioso", trans="barrido", footnote="Decretos del 6/10/2026 · se votan el 12/11", lines=[
            V("Tres, la casa: por decreto, el alquiler solo podría subir un 2 por ciento,", "normal"),
            V("y préstamos sin intereses para pagar la entrada.", "normal", 0.1),
        ], camara=[plano(0, "general", [540, 1000], 0), plano("@2", "general", [600, 900], 0.5, zoom=1.08),
                   plano("@préstamos", "general", [540, 1000], 0.5)],
           elements=[
            tit(3, "LA CASA"),
            edif("piso", 760, 0, 0.62, entra="crece", sfx="pop", dibuja=0.6),
            obj("contrato", 300, 900, "@alquiler", 0.75, entra="cae", sfx="papel", props={"titulo": "ALQUILER"}),
            etq("MÁX. +2 %", 300, 640, "@2", "verde", 0.75, hud=True),
            obj("llave", 760, 760, "@entrada", 0.9, entra="cae", sfx="kaching"),
            etq("0 % INTERÉS", 760, 600, "@intereses", "amarillo", 0.65, hud=True),
            quien("piz", 520, "@préstamos", 0.42, "ilusionado", entra="abajo", acciones=[{"at": "@entrada", "pose": "arriba", "salta": True}]),
            marca("pendiente", "@decreto"),
        ]),
        dict(id="derechos", fondo={"tipo": "plano", "color": (236, 226, 204)}, animo="tension", trans="papel",
             footnote="Mitin de Granada, 24/10/2026 (Vozpópuli)", lines=[
            V("Cuatro, los derechos: blindar el aborto en la Constitución,", "normal"),
            V("y frenar lo que llama «la motosierra» de PP y Vox.", "remate", 0.1),
        ], camara=[plano(0, "general", [540, 960], 0), plano("@Constitución", "general", [460, 820], 0.5, zoom=1.1),
                   plano("@motosierra", "general", [540, 960], 0.4)],
           elements=[
            tit(4, "LOS DERECHOS"),
            obj("documento", 420, 800, "@Cuatro", 1.0, hud=True, id="ce", entra="nada", dibujo=0.9, sfx="papel", props={
                "titulo": "CONSTITUCIÓN", "subtitulo": "REFORMA", "ancho": 640,
                "articulos": [{"id": "a", "titulo": "ABORTO", "lineas": ["derecho blindado"]}]},
                acciones=[{"at": "@Constitución", "props": {"resalta": ["a"]}}], out="@frenar"),
            quien("sanchez", 830, 0, 0.45, "normal", entra="der", acciones=[
                {"at": "@aborto", "pose": "senala_izq", "mira": "izq"}, {"at": "@frenar", "pose": "punos", "cara": "serio", "mira": "camara"}]),
            obj("cartel", 420, 760, "@frenar", 0.95, hud=True, entra="cae", sfx="golpe", props={"lineas": ["«LA MOTOSIERRA»", "DE PP Y VOX"], "color": "gris_claro"}).__or__({"scale": 1.25}),
            pum("¡STOP!", 420, 980, "@motosierra", 0.8),
            sello("DECLARACIÓN", "azul", 1240, "@Vox"),
        ]),
        ojo("psoe", [V("Ojo: llega tocado. La tragedia de Urda tiene a su ministro Puente contra las cuerdas,", "sobrio"),
                     V("y las encuestas le dejan por debajo de 110 escaños.", "normal", 0.15)],
            "Infobae 03/11/2026 · SocioMétrica y Sigma Dos 26/10",
            [obj("lazo", 300, 640, "@Urda", 0.6, hud=True, entra="crece"),
             quien("puente", 300, "@Puente", 0.42, "serio", entra="izq", acciones=[{"at": "@cuerdas", "pose": "encoge", "cara": "preocupado"}],
                   out="@encuestas"),
             edif("congreso", 330, "@encuestas", 0.5, entra="crece", sfx="pop"),
             obj("contador", 540, 820, "@110", 0.55, hud=True, entra="pop", sfx="golpe",
                 props={"valor": 108, "desde": 121, "sufijo": " ESCAÑOS", "ancho": 760}),
             etq("2023: 121", 540, 640, "@encuestas", "blanco", 0.6, hud=True)],
            camara=[plano(0, "general", [540, 960], 0), plano("@Urda", "general", [460, 900], 0.5, zoom=1.06),
                    plano("@encuestas", "general", [540, 960], 0.5)]),
        cierre("psoe", "pp"),
    ]


# ───────────────────────────── PP ─────────────────────────────
F_DEC = "Decálogo económico del PP, 27/09/2026 (pp.es)"
F_CON = "«Mi contrato con España», 19/10/2026"


def pp():
    galicia = mapa("espana", "@Galicia-0.3", 1.0, id="mapa_es",
                   acciones=[{"at": "@Galicia", "props": {"colores": {"Galicia": "pp"},
                                                         "resalta": ["La Coruña", "Lugo", "Orense", "Pontevedra"]}, "sfx": "pop"}])
    return [
        gancho("pp"),
        dict(id="bolsillo", fondo="calle", animo="curioso", trans="barrido", footnote=F_DEC, lines=[
            V("Una, el bolsillo: IVA cero en alimentos básicos, la luz del 21 al 10,", "normal"),
            V("y el doble de desgravación por cada hijo.", "normal", 0.1),
        ], camara=[plano(0, "general", [540, 1000], 0), plano("@luz", "general", [540, 880], 0.5, zoom=1.06),
                   plano("@doble", "general", [540, 1000], 0.5)],
           elements=[
            tit(1, "EL BOLSILLO"),
            edif("supermercado", 300, 0, 0.55, entra="crece", sfx="pop", dibuja=0.6),
            etq("IVA 0 %", 230, 600, "@cero", "verde", 0.75, hud=True),
            etq("LUZ: DEL 21 AL 10 %", 700, 600, "@luz", "amarillo", 0.65, hud=True),
            etq("POR HIJO ×2", 540, 790, "@doble", "amarillo", 0.7, hud=True),
            quien("piz", 800, 0, 0.45, "normal", entra="der", acciones=[
                {"at": "@cero", "cara": "ilusionado"}, {"at": "@luz", "cara": "sorpresa", "take": True},
                {"at": "@hijo", "pose": "arriba", "cara": "riendo"}]),
            quien("hacienda", 560, "@doble", 0.36, "confundido", entra="abajo", acciones=[{"at": "@hijo", "pose": "encoge"}]),
            marca("doc", "@hijo"),
        ]),
        dict(id="casa", fondo="calle", animo="alegre", trans="papel", footnote=F_CON, lines=[
            V("Dos, la casa: al menos un millón de viviendas nuevas, prioridad para los jóvenes,", "normal"),
            V("y echar a los okupas en 48 horas.", "remate", 0.1),
        ], camara=[plano(0, "general", [540, 1000], 0), plano("@millón", "general", [540, 960], 0.5, zoom=0.92),
                   plano("@okupas", "general", [540, 1000], 0.5)],
           elements=[
            tit(2, "LA CASA"),
            edif("piso", 200, "@viviendas", 0.42, entra="crece", sfx="pop"),
            edif("casa", 440, "@viviendas+0.2", 0.38, entra="crece", sfx="pop"),
            edif("piso", 680, "@viviendas+0.4", 0.42, entra="crece", sfx="pop"),
            edif("casa", 900, "@viviendas+0.6", 0.38, entra="crece", sfx="pop"),
            obj("contador", 540, 620, "@millón", 0.6, hud=True, entra="pop", sfx="kaching",
                props={"valor": 1000000, "desde": 0, "sufijo": "", "ancho": 760}),
            etq("JÓVENES PRIMERO", 540, 800, "@jóvenes", "amarillo", 0.65, hud=True, out="@okupas"),
            obj("reloj", 540, 820, "@okupas", 0.6, hud=True, entra="pop", sfx="redoble", props={"velocidad": 4.0}),
            etq("OKUPAS: 48 H", 540, 1000, "@48", "rojo", 0.7, hud=True),
            quien("piz", 540, "@jóvenes", 0.36, "ilusionado", entra="abajo", y=1560),
            marca("doc", "@horas"),
        ]),
        dict(id="palabra", fondo={"tipo": "plano", "color": (236, 226, 204)}, animo="curioso", trans="barrido",
             footnote="Contrato con España 19/10 · Galicia 2009-2020", lines=[
            V("Tres, la palabra: Feijóo ha firmado un «Contrato con España» de doce compromisos.", "normal"),
            V("Lo mismo que hizo en Galicia, donde ganó cuatro mayorías absolutas.", "normal", 0.15),
        ], camara=[plano(0, "general", [540, 960], 0), plano("@compromisos", "general", [460, 820], 0.5, zoom=1.08),
                   plano("@Galicia", "general", [540, 900], 0.6)],
           elements=[
            tit(3, "LA PALABRA"),
            obj("pergamino", 420, 780, "@firmado", 0.9, entra="crece", sfx="papel", dibuja=0.7,
                props={"titulo": "CONTRATO CON ESPAÑA", "fecha": "19 OCT 2026", "lineas": ["12 COMPROMISOS"]}, out="@Galicia-0.3"),
            quien("feijoo", 830, 0, 0.45, "normal", entra="der", acciones=[
                {"at": "@firmado", "pose": "senala_izq", "mira": "izq"}, {"at": "@doce", "cara": "ilusionado", "pose": "manos_juntas"},
                {"at": "@absolutas", "pose": "arriba", "cara": "riendo"}], out="@Galicia-0.3"),
            galicia,
            obj("contador", 540, 1120, "@cuatro", 0.5, hud=True, entra="pop", sfx="kaching",
                props={"valor": 4, "desde": 0, "sufijo": " MAYORÍAS", "ancho": 700}),
            marca("doc", "@compromisos"),
        ]),
        dict(id="cambio", fondo={"tipo": "plano", "color": PARTIDO["pp"]["fondo"]}, animo="tension", trans="corte",
             footnote="Sigma Dos 26/10 · Infobae 03/11/2026", lines=[
            V("Cuatro, el cambio: va primero en las encuestas,", "energia"),
            V("y, tras Urda, exige la dimisión del ministro Puente.", "sobrio", 0.15),
        ], camara=[plano(0, "general", [540, 940], 0), plano("@Urda", "general", [540, 1000], 0.5)],
           elements=[
            tit(4, "EL CAMBIO"),
            obj("barras", 540, 900, "@Cuatro", 1.0, hud=True, entra="nada", dibujo=1.2, out="@dimisión-0.1",
                props={"sufijo": " %", "decimales": 1, "tope": 35, "barras": [
                    {"texto": "PP", "valor": 30.6, "color": "pp"}, {"texto": "PSOE", "valor": 26.1, "color": "psoe"},
                    {"texto": "VOX", "valor": 19.9, "color": "vox"}]}),
            etq("SIGMA DOS · 26/10", 540, 1000, "@primero", "blanco", 0.55, hud=True, out="@dimisión-0.1"),
            quien("feijoo", 250, "@Urda", 0.48, "serio", entra="izq", acciones=[{"at": "@exige", "pose": "senala", "mira": "der"}]),
            quien("puente", 830, "@ministro", 0.45, "serio", entra="der", acciones=[{"at": "@Puente", "pose": "encoge", "cara": "preocupado"}]),
            bocata(["PP:", "«¡DIMISIÓN!»"], "@dimisión", x=380, y=640),
            sello("DECLARACIÓN", "azul", 1240, "@Puente"),
        ]),
        ojo("pp", [V("Ojo: no ha dicho cuánto cuestan sus rebajas de impuestos.", "normal"),
                   V("Y para gobernar, casi seguro necesita a Vox: ya han pactado el Senado.", "remate", 0.15)],
            "politicaelectoral.com (PP) · pacto del Senado, 26/10/2026",
            [obj("calculadora", 300, 760, "@cuestan", 0.85, entra="cae", sfx="calculadora", props={"texto": "¿?"}, out="@Vox-0.3",
                  acciones=[{"at": "@rebajas", "tiembla": True}]),
             pum("¿CUÁNTO?", 360, 560, "@impuestos", 0.75),
             quien("feijoo", 190, "@gobernar", 0.4, "normal", entra="izq", acciones=[{"at": "@pactado", "pose": "senala", "mira": "der"}]),
             quien("abascal", 680, "@Vox+0.2", 0.4, "normal", entra="der", acciones=[{"at": "@pactado", "pose": "senala_izq", "mira": "izq"}]),
             edif("congreso", 435, "@Senado-0.2", 0.3, entra="crece", sfx="pop", texto="SENADO")],
            camara=[plano(0, "general", [540, 960], 0), plano("@cuestan", "general", [400, 820], 0.4, zoom=1.08),
                    plano("@Vox", "general", [540, 1000], 0.5)]),
        cierre("pp", "vox"),
    ]


# ───────────────────────────── VOX ─────────────────────────────
F_VOX = "Programa económico y de vivienda de Vox (voxespana.es, 2025)"


def vox():
    R = "estrecho"
    CEUTA = P(R, -5.335, 35.895)
    MELILLA = P(R, -2.94, 35.29)
    return [
        gancho("vox"),
        dict(id="impuestos", fondo="calle", animo="curioso", trans="barrido", footnote="Programa de Vox 2025 · Palma 24/10/2026", lines=[
            V("Una, los impuestos: nada de IRPF hasta 22.000 euros, el IVA del 21 al 18,", "normal"),
            V("y sin impuestos sobre las propinas.", "remate", 0.1),
        ], camara=[plano(0, "general", [540, 1000], 0), plano("@IVA", "general", [540, 900], 0.5, zoom=1.06),
                   plano("@propinas", "general", [540, 1000], 0.5)],
           elements=[
            tit(1, "LOS IMPUESTOS"),
            edif("hacienda", 280, 0, 0.5, entra="crece", sfx="pop", dibuja=0.6),
            etq("IRPF 0 € HASTA 22.000 €", 540, 600, "@IRPF", "verde", 0.62, hud=True),
            etq("IVA: DEL 21 AL 18 %", 540, 770, "@IVA", "amarillo", 0.68, hud=True),
            obj("hucha", 780, 1180, "@propinas", 0.6, entra="crece", sfx="kaching", props={"cara": "ilusionado"}),
            monedas("@propinas", 640, 920, 8),
            quien("piz", 780, 0, 0.42, "normal", entra="der", acciones=[
                {"at": "@IRPF", "pose": "senala_arriba", "mira": "izq"}, {"at": "@22.000", "cara": "sorpresa", "take": True},
                {"at": "@euros", "pose": "arriba", "cara": "ilusionado"}, {"at": "@21", "pose": "piensa", "cara": "pensativo"},
                {"at": "@propinas", "x": 560, "dur": 0.6, "cara": "riendo"}]),
            marca("doc", "@propinas"),
        ]),
        dict(id="casa", fondo="calle", animo="alegre", trans="papel", footnote=F_VOX, lines=[
            V("Dos, la casa: sin IVA al comprar tu primera vivienda, okupas fuera en 24 horas,", "normal"),
            V("y «prioridad nacional» en la vivienda protegida.", "remate", 0.1),
        ], camara=[plano(0, "general", [540, 1000], 0), plano("@okupas", "general", [540, 900], 0.5, zoom=1.06),
                   plano("@prioridad", "general", [540, 1000], 0.5)],
           elements=[
            tit(2, "LA CASA"),
            edif("casa", 300, 0, 0.55, entra="crece", sfx="pop", dibuja=0.6),
            etq("1.ª VIVIENDA: IVA 0 %", 540, 600, "@IVA", "verde", 0.62, hud=True),
            obj("reloj", 780, 820, "@okupas", 0.55, hud=True, entra="pop", sfx="redoble", props={"velocidad": 4.0}),
            etq("OKUPAS: 24 H", 780, 1000, "@24", "rojo", 0.65, hud=True),
            obj("cartel", 540, 780, "@prioridad", 0.85, hud=True, entra="cae", sfx="golpe",
                props={"lineas": ["«PRIORIDAD", "NACIONAL»"], "color": "amarillo"}),
            quien("piz", 760, 0, 0.42, "normal", entra="der", acciones=[
                {"at": "@vivienda", "cara": "ilusionado"}, {"at": "@24", "cara": "sorpresa", "take": True},
                {"at": "@prioridad", "pose": "piensa", "cara": "pensativo"}]),
            marca("doc", "@protegida"),
        ]),
        dict(id="fronteras", fondo="mar_mapa", limites=LIM, animo="tension", trans="iris",
             footnote="Mitin de Estepona 11/10 · Abascal 18/10/2026", lines=[
            V("Tres, las fronteras: lo que llama «remigración»: devolver a quien entra ilegalmente", "normal"),
            V("y expulsar al extranjero que delinque. Y militares en Ceuta y Melilla.", "normal", 0.1),
        ], camara=[zoom(0, P(R, -4.4, 37.6), 1.0, 0), zoom("@Ceuta", P(R, -4.2, 35.8), 2.0, 0.9)],
           elements=[
            tit(3, "LAS FRONTERAS"),
            mapa(R, 0, 1.2, orden=["Spain", "Portugal", "Gibraltar", "Ceuta", "Morocco", "Melilla", "Balearic Islands", "France", "Andorra", "Algeria"],
                 acciones=[{"at": "@Ceuta", "props": {"resalta": ["Ceuta", "Melilla"]}, "sfx": "pop"}]),
            obj("cartel", 540, 620, "@remigración", 0.85, hud=True, entra="cae", sfx="golpe",
                props={"lineas": ["«REMIGRACIÓN»"], "color": "amarillo"}, out="@Ceuta-0.2"),
            obj("avion", 540, 820, "@devolver", 0.6, hud=True, entra="izq", sfx="whoosh", out="@Ceuta-0.2"),
            obj("chincheta", CEUTA[0] + 4, CEUTA[1], "@Ceuta", 0.22, props={"diseno": "espana"}, entra="cae"),
            obj("chincheta", MELILLA[0] + 4, MELILLA[1], "@Melilla", 0.2, props={"diseno": "espana"}, entra="cae"),
            quien("piz", MELILLA[0] + 70, 0.4, 0.2, "pensativo", y=MELILLA[1] + 30, entra="cae", acciones=[
                {"at": "@expulsar", "cara": "sorpresa", "mira": "izq"}, {"at": "@militares", "pose": "encoge", "cara": "pensativo"}]),
            marca("anuncio", "@militares"),
        ]),
        dict(id="momento", fondo={"tipo": "plano", "color": PARTIDO["vox"]["fondo"]}, animo="tension", trans="corte",
             footnote="Sigma Dos 26/10 · Palma 24/10/2026", lines=[
            V("Cuatro, el momento: está en máximos en las encuestas, cerca del 20 por ciento,", "energia"),
            V("y Abascal pide una «gran mayoría» para ser presidente.", "remate", 0.15),
        ], camara=[plano(0, "general", [540, 940], 0), plano("@Abascal", "general", [540, 1000], 0.5)],
           elements=[
            tit(4, "EL MOMENTO"),
            pum("¡RÉCORD!", 540, 960, "@momento", 0.8),
            obj("contador", 540, 640, "@momento", 0.6, hud=True, entra="pop", sfx="kaching",
                props={"valor": 19.9, "desde": 12.4, "decimales": 1, "sufijo": " %", "ancho": 700}, out="@Abascal-0.2"),
            etq("SIGMA DOS · 26/10 · RÉCORD", 540, 830, "@20", "blanco", 0.55, hud=True, out="@Abascal-0.2"),
            obj("atril", 540, SUELO_ATRIL, "@Abascal", 0.5, entra="crece", props={"texto": "VOX", "color": "vox"}),
            quien("abascal", 540, "@Abascal", 0.5, "normal", entra="abajo", y=1200, acciones=[
                {"at": "@mayoría", "pose": "arriba", "cara": "ilusionado"}]),
            bocata(["ABASCAL:", "«no nos votéis", "a medias»"], "@presidente", x=540, y=560),
            sello("DECLARACIÓN", "azul", 1240, "@presidente"),
        ]),
        ojo("vox", [V("Ojo: Vox calcula que su bajada de impuestos cuesta 46.000 millones; Hacienda dice 85.000.", "normal"),
                    V("Y la «remigración» es su propuesta más polémica.", "remate", 0.15)],
            "Figaredo (Vox) · ministro Arcadi España (Hacienda)",
            [obj("calculadora", 300, 760, "@46.000", 0.8, entra="cae", sfx="calculadora", props={"texto": "46"}),
             etq("46.000 M€", 300, 960, "@46.000", "verde", 0.55, hud=True),
             etq("VOX", 300, 560, "@46.000", "verde", 0.55, hud=True),
             obj("calculadora", 700, 760, "@85.000", 0.8, entra="cae", sfx="calculadora", props={"texto": "85"}),
             etq("85.000 M€", 700, 960, "@85.000", "blanco", 0.55, hud=True),
             etq("HACIENDA", 700, 560, "@Hacienda", "blanco", 0.55, hud=True),
             pum("¿?", 500, 640, "@85.000+0.3", 0.8),
             obj("cartel", 540, 1110, "@remigración", 0.75, hud=True, entra="cae", sfx="golpe",
                 props={"lineas": ["«REMIGRACIÓN»"], "color": "naranja"}),
             sello("LA MÁS POLÉMICA", "rojo", 1260, "@polémica")],
            camara=[plano(0, "general", [540, 960], 0), plano("@46.000", "general", [540, 820], 0.4, zoom=1.06),
                    plano("@remigración", "general", [540, 980], 0.5)]),
        cierre("vox"),
    ]


EP = {
    "psoe": (psoe, "Por qué votar al PSOE", 1,
             ["SMI: 735,90 € (2018) y 1.221 € en 14 pagas (2026); deducción para que quien cobra el SMI no pague IRPF (Hacienda 17/02/2026)",
              "Pensiones con el IPC 4 años más y 20.000 M€ en el Fondo de Reserva: mitin de Zaragoza, 14/10/2026",
              "Decretos de vivienda del 6/10/2026 (tope del 2 %, préstamos ICO): pendientes de la Diputación Permanente (12/11)",
              "Aborto en la Constitución y «club de la motosierra»: Vozpópuli 24/10/2026",
              "Urda: 69 fallecidos (provisional), Infobae 03/11/2026; encuestas SocioMétrica y Sigma Dos 26/10 (Qué! 01/11/2026)"],
             ("🤔 ¿Por qué votar al PSOE el 29N? Sus 4 razones\n"
              "💶 Salario mínimo +66 % y sin IRPF ✅\n"
              "👵 Pensiones con el IPC 4 años más 🎤\n"
              "🏠 Alquiler: subida máxima del 2 % ⏳\n"
              "⚠️ Ojo: Urda y las encuestas\n"
              "💬 ¿Te convence? Sí o no\n"
              "➡️ ¿Por qué votar a…? Ep. 1/3 · Próximo: PP · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Hacienda 17/02/2026 (SMI) · mitin de Zaragoza 14/10 · decretos de vivienda 6/10 (se votan el 12/11) · "
             "Vozpópuli 24/10 · Infobae 03/11 · SocioMétrica y Sigma Dos 26/10. Las razones son las del partido; ¿ves un error? Dínoslo.",
             ["#PSOE", "#PedroSanchez", "#Elecciones29N", "#QuéVotar", "#PolíticaEspañola", "#pizarrapublica"]),
    "pp": (pp, "Por qué votar al PP", 2,
           ["IVA 0 % alimentos, luz 21 → 10 %, mínimo por hijo doble: decálogo económico del PP (27/09/2026)",
            "Un millón de viviendas, prioridad joven, okupas en 48 h: «Mi contrato con España» (19/10/2026)",
            "Galicia: mayorías absolutas de Feijóo en 2009, 2012, 2016 y 2020 (Moncloa.com 19/10/2026)",
            "Sigma Dos 26/10/2026: PP 30,6 %, PSOE 26,1 %, Vox 19,9 % (Qué! 01/11/2026); dimisión de Puente: Infobae 03/11/2026",
            "Coste de las rebajas sin cifrar (politicaelectoral.com); pacto PP-Vox en el Senado (26/10/2026)"],
           ("🤔 ¿Por qué votar al PP el 29N? Sus 4 razones\n"
            "🛒 IVA 0 % en alimentos básicos 📝\n"
            "🏠 Un millón de viviendas y okupas fuera en 48 h 📝\n"
            "✍️ «Contrato con España»: 12 compromisos 📝\n"
            "⚠️ Ojo: ¿cuánto cuesta? y ¿con Vox?\n"
            "💬 ¿Te convence? Sí o no\n"
            "➡️ ¿Por qué votar a…? Ep. 2/3 · Próximo: Vox · 📚 Fuentes en comentarios"),
           "📚 Fuentes: decálogo económico del PP 27/09 · «Mi contrato con España» 19/10 · Sigma Dos 26/10 · Infobae 03/11 · "
           "pacto del Senado 26/10. Las razones son las del partido; ¿ves un error? Dínoslo.",
           ["#PP", "#Feijoo", "#Elecciones29N", "#QuéVotar", "#PolíticaEspañola", "#pizarrapublica"]),
    "vox": (vox, "Por qué votar a Vox", 3,
            ["IRPF 0 hasta 22.000 €, IVA 18 %, IVA 0 % en la primera vivienda, desalojo en 24 h, prioridad nacional: programa de Vox (2025)",
             "Propinas sin impuestos y «gran mayoría»: mitin de Palma, 24/10/2026 (Infobae/Europa Press)",
             "«Remigración»: mitin de Estepona, 11/10/2026 (Qué! 12/10); militares en Ceuta y Melilla: Abascal, 18/10/2026",
             "Sigma Dos 26/10/2026: Vox 19,9 % y 68 escaños, nuevo máximo (Qué! 01/11/2026)",
             "Coste: 46.000 M€ según Figaredo (Vox); 85.000 M€ según el ministro de Hacienda Arcadi España"],
            ("🤔 ¿Por qué votar a Vox el 29N? Sus 4 razones\n"
             "💶 0 € de IRPF hasta 22.000 € 📝\n"
             "🏠 Sin IVA en tu primera vivienda 📝\n"
             "🛂 «Remigración» y «prioridad nacional» 🎤\n"
             "⚠️ Ojo: 46.000 o 85.000 millones\n"
             "💬 ¿Te convence? Sí o no · ¿Con cuál de los tres te quedas?\n"
             "➡️ ¿Por qué votar a…? Ep. 3/3 · 📚 Fuentes en comentarios"),
            "📚 Fuentes: programa económico y de vivienda de Vox (2025) · mitin de Palma 24/10 · Qué! 12/10 · Sigma Dos 26/10 · "
            "coste: Figaredo (Vox) y Arcadi España (Hacienda). Las razones son las del partido; ¿ves un error? Dínoslo.",
            ["#Vox", "#Abascal", "#Elecciones29N", "#QuéVotar", "#PolíticaEspañola", "#pizarrapublica"]),
}

if __name__ == "__main__":
    for p in (sys.argv[1:] or ["psoe", "pp", "vox"]):
        fn, titulo, n, fuentes, caption, pinned, tags = EP[p]
        episodio(f"porque_{p}", f"¿{titulo}?", fn(), {"t": 2.2, "titulo": f"¿{titulo}?", "capitulo": n},
                 fuentes, caption, pinned, tags, series_tag="¿POR QUÉ VOTAR A…? 29N")
