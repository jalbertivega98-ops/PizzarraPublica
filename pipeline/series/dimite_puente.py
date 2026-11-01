#!/usr/bin/env python3
"""«¿Debe dimitir Puente?» (2/11/2026). Pregunta de debate antes de la comparecencia del ministro de Transportes
por el accidente de Urda (martes 3/11, 17:00, Diputación Permanente). Tema político tras una tragedia: tono sobrio,
sin gags sobre el accidente ni las víctimas, trenes sin cara, el choque no se dibuja, lazo de luto. Los dos lados.

Aprobado por joel el 1/11/2026 (20:47 UTC, propuesta 4 de /mnt/project-files/insta/guiones/propuestas_2nov.md).
Fuentes:
  El Independiente 29/10/2026: comparecencia martes 3/11 a las 17:00 ante la Diputación Permanente; choque de un AVE
    y un Iryo entre Urda y Los Yébenes el 28/10; Feijóo: las responsabilidades políticas «no son opcionales».
  Nuevaradio 31/10/2026: «saldo provisional de 69 fallecidos y más de cien heridos» (El Español 1/11 también 69);
    Puente «descarta por el momento una dimisión».
  Malagaes 2026: primer informe de la AITAT, alcance a 160-200 km/h; el Gobierno apunta a un posible error humano tras
    la caída del LZB (un responsable de Adif autorizó al AVE a seguir); conclusiones preliminares; Vox presentó la
    primera querella contra el ministro; el PNV exigió la dimisión.
  HerQles 31/10/2026: Colau pide su dimisión «lo antes posible».
"""
from _mundo import *  # noqa: F401,F403

R = "espana"
MAD = P(R, -3.70, 40.42)
URDA = P(R, -3.71, 39.41)
LINEA = [(-3.70, 40.42), (-3.80, 39.85), (-3.71, 39.41), (-3.93, 38.98), (-4.10, 38.68), (-4.78, 37.89), (-5.98, 37.39)]
NOCHE_AZUL = (28, 40, 70)
GRIS_LUTO = (210, 212, 218)
F_IND = "El Independiente, 29/10/2026"


def bocata(lineas, at, out=None, x=540, y=520, scale=0.7, cola=(-1, 1)):
    d = obj("bocadillo", x, y, at, scale, hud=True, entra="pop", sfx="pop", props={"lineas": lineas, "cola": cola})
    if out:
        d["out"] = out
    return d


def pancarta(texto, x, y, at, out=None):
    d = obj("cartel", x, y, at, 0.8, hud=True, entra="abajo", sfx="golpe", props={"texto": texto, "color": "rojo", "tinta": "blanco"})
    if out:
        d["out"] = out
    return d


scenes = [
    # 1 · GANCHO: le piden que se vaya, y él dice que no
    dict(id="gancho", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="tension", footnote="Nuevaradio 31/10 · HerQles 31/10/2026",
         lines=[
        V("Hasta socios del Gobierno le piden que dimita. Y él, de momento, dice que no.", "intriga"),
        V("El martes, Óscar Puente da la cara por Urda.", "remate", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@no", "medio", "puente", 0.4, aire=260),
               plano("@martes", "general", [540, 1000], 0.5)],
       elements=[
        quien("puente", 540, 0, 0.6, "serio", entra="nada", acciones=[
            {"at": "@socios", "mira": "izq"}, {"at": "@dimita", "mira": "der", "cara": "preocupado"},
            {"at": "@no", "pose": "cruzados", "cara": "serio", "mira": "camara"}, {"at": "@cara", "pose": "manos_juntas"}]),
        rot("¿DIMISIÓN?", 540, 440, 0, 120, "amarillo", golpe=True, out="@martes"),
        pancarta("DIMISIÓN", 220, 700, "@socios"),
        pancarta("DIMISIÓN", 860, 760, "@dimita"),
        pancarta("RESPONSABILIDADES", 540, 560, "@dimita+0.4", out="@martes"),
        obj("calendario", 820, 560, "@martes", 0.34, hud=True, entra="crece", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [3], "colores": {3: "rojo"}}),
        rot("MARTES 3 · CONGRESO", 540, 440, "@martes", 70, "blanco"),
        obj("lazo", 960, 220, "@Urda", 0.3, hud=True, entra="pop"),
    ]),
    # 2 · QUÉ PASÓ: el mapa, Urda, las víctimas (sobrio)
    dict(id="urda", fondo="mar_mapa", limites=LIM, animo="triste", trans="iris", footnote="El Independiente 29/10 · Nuevaradio 31/10/2026",
         lines=[
        V("28 de octubre. Un AVE alcanza a un Iryo parado entre Urda y Los Yébenes.", "sobrio"),
        V("69 muertos, según el último balance provisional.", "sobrio", 0.25),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@AVE", URDA, 2.4, 1.0), zoom("@69", URDA, 1.6, 0.8)],
       elements=[
        mapa(R, 0, 1.2, acciones=[{"at": "@AVE", "props": {"lineas": [linea("ave", LINEA, "azul", 1.0, ancho=8)]}, "sfx": "rotulador"},
                                  {"at": "@Urda", "props": {"resalta": ["Toledo"]}}]),
        rot("28 OCTUBRE", 540, 440, 0.1, 90, "blanco", out="@69"),
        obj("chincheta", URDA[0] + 6, URDA[1], "@Urda", 0.12, props={"diseno": "espana"}, entra="cae"),
        etq("URDA · LOS YÉBENES", 540, 520, "@Yébenes", "blanco", 0.6, hud=True, out="@69"),
        obj("lazo", 960, 220, 0, 0.3, hud=True, entra="nada"),
        obj("contador", 540, 520, "@69", 0.75, hud=True, entra="pop", props={"valor": 69, "sufijo": " FALLECIDOS", "ancho": 860}),
        sello("PROVISIONAL", "naranja", 1240, "@provisional"),
    ]),
    # 3 · QUÉ SE SABE: el informe preliminar
    dict(id="informe", fondo={"tipo": "plano", "color": GRIS_LUTO}, animo="tension", trans="papel",
         footnote="Primer informe AITAT, vía Malagaes", lines=[
        V("Primer informe: se cae el sistema LZB, Adif autoriza al AVE a seguir… y alcanza al Iryo a entre 160 y 200 por hora."),
        V("Es preliminar. La investigación sigue abierta.", "normal", 0.2),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Adif", "general", [540, 820], 0.6, zoom=1.08),
               plano("@preliminar", "general", [540, 960], 0.4)],
       elements=[
        obj("documento", 540, 760, 0, 0.82, hud=True, id="inf", entra="nada", dibujo=0.9, sfx="papel", props={
            "titulo": "PRIMER INFORME", "subtitulo": "AITAT", "ancho": 760,
            "articulos": [{"id": "a", "titulo": "1 · SE CAE EL LZB", "lineas": []},
                          {"id": "b", "titulo": "2 · ADIF: «SIGA»", "lineas": []},
                          {"id": "c", "titulo": "3 · 160-200 KM/H", "lineas": []}]},
            acciones=[{"at": "@LZB", "props": {"resalta": ["a"]}}, {"at": "@autoriza", "props": {"resalta": ["b"]}},
                      {"at": "@160", "props": {"resalta": ["c"]}}]),
        quien("piz", 880, "@Primer", 0.42, "serio", entra="der", acciones=[
            {"at": "@LZB", "pose": "piensa", "mira": "inf"}, {"at": "@autoriza", "cara": "preocupado"}, {"at": "@alcanza", "pose": "manos_juntas", "cara": "triste"}, {"at": "@Iryo", "mira": "camara"},
            {"at": "@200", "cara": "triste"}, {"at": "@abierta", "pose": "normal", "mira": "camara", "cara": "serio"}]),
        etq("LZB CAÍDO", 260, 1320, "@cae", "rojo", 0.6, hud=True, out="@preliminar"),
        etq("160-200 KM/H", 540, 1460, "@160", "amarillo", 0.65, hud=True, out="@preliminar"),
        etq("EL AVE ALCANZA AL IRYO", 540, 1200, "@alcanza", "blanco", 0.6, hud=True, out="@160"),
        sello("PRELIMINAR", "naranja", 1400, "@preliminar"),
        rot("INVESTIGACIÓN ABIERTA", 540, 440, "@investigación", 66, "rojo"),
    ]),
    # 4 · A FAVOR DE LA DIMISIÓN
    dict(id="si", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="tension", trans="corte",
         footnote=F_IND + " · Malagaes · HerQles 31/10", lines=[
        V("Feijóo: las responsabilidades políticas «no son opcionales». Vox se querella contra él."),
        V("Y Colau y el PNV piden su salida.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Colau", "general", [540, 1000], 0.4)],
       elements=[
        rot("PIDEN QUE SE VAYA", 540, 440, 0, 80, "rojo"),
        quien("feijoo", 230, 0.1, 0.48, "serio", entra="pop", acciones=[{"at": "@opcionales", "pose": "senala"}]),
        bocata(["FEIJÓO (PP):", "«no son", "opcionales»"], "@responsabilidades", x=430, y=560, out="@Vox"),
        quien("abascal", 540, "@Vox", 0.48, "enfado", entra="pop", acciones=[{"at": "@querella", "pose": "punos"}]),
        obj("documento", 560, 600, "@querella", 0.6, hud=True, entra="nada", dibujo=0.6, sfx="papel",
            props={"titulo": "QUERELLA", "subtitulo": "VOX", "ancho": 520, "articulos": []}, out="@Colau"),
        quien("colau", 850, "@Colau", 0.48, "serio", entra="pop", acciones=[{"at": "@salida", "pose": "senala_izq"}]),
        etq("PNV", 850, 640, "@PNV", "verde", 0.7, hud=True),
        bocata(["COLAU Y PNV:", "dimisión"], "@piden", x=640, y=440, cola=(1, 1)),
    ]),
    # 5 · SU VERSIÓN
    dict(id="no", fondo="oficina", animo="curioso", trans="barrido", footnote="Nuevaradio 31/10 · Malagaes", lines=[
        V("Puente descarta dimitir por ahora. El Gobierno apunta a un posible error humano."),
        V("Y la investigación aún no ha terminado.", "normal", 0.1),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@error", "general", [540, 900], 0.5, zoom=1.06)],
       elements=[
        quien("puente", 500, 0, 0.55, "serio", entra="izq", acciones=[
            {"at": "@descarta", "pose": "cruzados"}, {"at": "@Gobierno", "pose": "manos_juntas"},
            {"at": "@error", "pose": "senala", "mira": "der"}, {"at": "@terminado", "pose": "encoge"}]),
        bocata(["PUENTE:", "por ahora,", "no dimite"], "@descarta", x=560, y=460, out="@Gobierno"),
        bocata(["GOBIERNO:", "posible", "error humano"], "@Gobierno", x=640, y=460, cola=(1, 1), out="@investigación"),
        obj("lupa", 820, 900, "@investigación", 0.7, hud=True, entra="crece", sfx="pop"),
        obj("reloj", 820, 1250, "@aún", 0.5, hud=True, entra="pop", sfx="pop"),
        sello("DECLARACIÓN", "azul", 1240, "@humano"),
    ]),
    # 6 · CIERRE: cuándo, la pregunta A/B y «sigue a Piz»
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote=F_IND, lines=[
        V("Martes, a las cinco, en el Congreso."),
        V("¿Dimitir ya, o esperar a la investigación? A o B, te leo.", "energia", 0.15),
        V("Y sigue a Piz: el martes te contamos qué dice.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        edif("congreso", 540, 0, 0.5, entra="nada", dibuja=0.6, out="@Dimitir"),
        obj("reloj", 860, 520, "@cinco", 0.45, hud=True, entra="pop", sfx="pop", out="@Dimitir"),
        rot("MARTES 3 · 17:00", 540, 440, "@Martes", 80, "amarillo", out="@Dimitir"),
        quien("piz", 540, "@Dimitir-0.4", 0.62, "pensativo", entra="abajo", acciones=[
            {"at": "@ya", "pose": "senala_izq", "mira": "izq"}, {"at": "@esperar", "pose": "senala", "mira": "der"},
            {"at": "@leo", "pose": "piensa", "mira": "camara", "cara": "normal"},
            {"at": "@sigue", "pose": "saluda", "cara": "ilusionado"}, {"at": "@martes#2", "pose": "senala_arriba"}, {"at": "@contamos", "pose": "jarras", "cara": "riendo"}]),
        etq("A · DIMITIR YA", 260, 700, "@ya", "rojo", 0.58, hud=True, out="@sigue"),
        etq("B · ESPERAR", 820, 700, "@esperar", "azul", 0.58, hud=True, out="@sigue"),
        rot("¿A O B?", 540, 360, "@leo", 110, "amarillo", golpe=True, out="@sigue-0.2"),
        obj("calendario", 830, 760, "@martes#2", 0.3, hud=True, entra="crece", sfx="papel",
            props={"mes": "NOVIEMBRE 2026", "inicio": 6, "dias": 30, "marcados": [3], "colores": {3: "rojo"}}),
        rot("SIGUE A PIZ", 540, 440, "@sigue", 110, "amarillo", fx=[{"at": "@dice", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("dimite_puente", "¿Debe dimitir Puente?", scenes,
             {"t": 1.2, "titulo": "¿Debe dimitir Puente?", "capitulo": None},
             ["El Independiente (29/10/2026): comparecencia de Puente el martes 3/11 a las 17:00; Feijóo",
              "Nuevaradio (31/10/2026): 69 fallecidos (balance provisional); Puente descarta dimitir por ahora",
              "Malagaes: primer informe AITAT (160-200 km/h), posible error humano, querella de Vox, PNV",
              "HerQles (31/10/2026): Colau pide su dimisión",
              "Tema político tras una tragedia: tono sobrio, sin gags sobre el accidente, el choque no se dibuja"],
             ("🚆 ¿Debe dimitir Puente?\n"
              "🖤 28/10: el accidente de Urda · 69 fallecidos (balance provisional)\n"
              "📄 Primer informe: cae el LZB, Adif autoriza a seguir, alcance a 160-200 km/h (preliminar)\n"
              "🗣️ PP, Vox, Colau y PNV piden responsabilidades · Puente no dimite por ahora\n"
              "🏛️ Comparece el martes 3/11 a las 17:00 en el Congreso\n"
              "💬 ¿Dimitir ya (A) o esperar a la investigación (B)? Te leo 👇\n"
              "🔔 Sigue a Piz: el martes te contamos qué dice · 📚 Fuentes en comentarios"),
             "📚 Fuentes: El Independiente 29/10/2026 · Nuevaradio 31/10 · Malagaes (informe AITAT) · HerQles 31/10. "
             "Cifras provisionales. ¿Ves un error? Dínoslo.",
             ["#OscarPuente", "#Urda", "#Adif", "#29N", "#EleccionesGenerales", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
