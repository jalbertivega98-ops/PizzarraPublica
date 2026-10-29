#!/usr/bin/env python3
"""«Urda: ocho minutos y una orden» (29/10/2026). Segunda pieza del accidente de Urda: lo que cuentan los audios del centro
de control. Tono de luto (series/accidente_urda.py): sin gags ni caras en los trenes y el choque NO se dibuja. joel pidió
cerrar con «síguenos» también aquí: va en tono sobrio, sin pregunta de enganche.

Guion y fuentes: /mnt/project-files/insta/guiones/propuestas_29oct.md (aprobado por joel el 29/10/2026, 17:48 UTC)
  69 fallecidos: García-Page, 29/10 por la mañana, tras morir un herido crítico en el hospital (CMM 10:34; elDiario.es 10:43;
    Euronews 12:26 «al menos 69»).
  Audios (El País y elDiario.es, resumidos por Euronews 29/10): 8:31 el maquinista del AVE 2080 comunica la pérdida de
    transmisión del LZB; 8:36 Atocha le ordena desconectar y conectar el LZB y reanudar la marcha normal («¿Con marcha
    normal?» «Sí»); 8:41 la maquinista del Iryo 6076, detenida ante la señal de entrada de Urda, recibe la misma orden;
    8:48 avisa de que no puede reiniciar y sigue parada; nadie avisa al AVE; 8:54 impacto, a unos 25 km de distancia al
    reanudar. Protocolo según el Gobierno: «marcha a vista», máximo 40 km/h.
  Puente: «inexplicable» circular con un tren detenido y la señal en rojo (Euronews); comparece el 3/11 ante la Diputación
    Permanente (El Independiente 29/10). Sánchez: «esclarecer hasta el último detalle» (elDiario.es 10:57).
  Feijóo: «Las responsabilidades políticas no son opcionales» (CMM 13:14). Vox: querella por homicidio y lesiones
    imprudentes (Infobae 28/10). Rufián (ERC): «Una sola persona no puede ser responsable de la vida de centenares»
    (elDiario.es 10:31). Luto oficial del 29 al 31/10 (RD 949/2026).
"""
import json

from _mundo import *  # noqa: F401,F403
from _mundo import OUT  # noqa: E402

LUTO = (226, 224, 220)
NOCHE_AZUL = (28, 40, 70)
FA = "Audios del centro de control (El País, elDiario.es) vía Euronews 29/10/2026"


def S(text, pausa=None):
    return V(text, "sobrio", pausa)


def tren(x, at, color, id, acciones=(), y=1080, scale=0.8):
    return obj("tren", x, y, at, scale, id=id, entra="nada", props={"color": color, "cara": None, "vagones": 1},
               acciones=list(acciones))


def hora(txt, at, out=None):
    d = rot(txt, 540, 420, at, 130, "amarillo")
    if out:
        d["out"] = out
    return d


scenes = [
    # 1 · GANCHO: el reloj, las dos horas que importan
    dict(id="gancho", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="triste", footnote=FA, lines=[
        S("A las 8:36, desde Atocha, alguien le dijo a un AVE: «reanude con marcha normal»."),
        S("Dieciocho minutos después, chocó contra un tren parado.", 0.3),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@reanude", "general", [540, 900], 0.8, zoom=1.08),
               plano("@Dieciocho", "general", [540, 960], 0.6)],
       elements=[
        obj("reloj", 540, 860, 0, 1.1, hud=True, entra="crece", dibuja=0.8),
        hora("8:36", "@8:36", out="@Dieciocho"),
        obj("bocadillo", 540, 1320, "@reanude", 1.0, hud=True, entra="pop", sfx="pop", out="@Dieciocho",
            props={"lineas": ["ATOCHA:", "«reanude con", "marcha normal»"]}),
        hora("8:54", "@Dieciocho"),
        sello("AUDIOS DEL CONTROL", "naranja", 1500, "@chocó"),
    ]),
    # 2 · 8:31 – 8:36: cae el LZB y la orden al AVE
    dict(id="orden", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="triste", trans="corte", footnote=FA, lines=[
        S("8:31. Se cae el LZB, el sistema que vigila la distancia entre trenes. Seis trenes se paran."),
        S("8:36. Atocha le dice al AVE: desconecta el sistema, vuelve a conectarlo y sigue. «¿Con marcha normal?». «Sí».", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@AVE", "general", [540, 1040], 0.6, zoom=1.06)],
       elements=[
        obj("via", 540, 1184, 0, 1.0, entra="nada", props={"ancho": 1600}),
        tren(300, 0, "azul", "ave", acciones=[{"at": "@sigue+0.6", "x": 520, "dur": 2.4}]),
        etq("AVE 2080", 300, 760, 0.3, "azul", 0.7, hud=True),
        hora("8:31", "@8:31", out="@8:36"),
        sello("LZB CAÍDO", "rojo", 1500, "@LZB", out="@8:36"),
        hora("8:36", "@8:36"),
        obj("bocadillo", 540, 620, "@Sí-0.4", 0.95, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["«¿Con marcha normal?»", "«Sí»"]}),
    ]),
    # 3 · 8:41 – 8:48: el Iryo, parado delante; nadie avisa al AVE
    dict(id="iryo", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="triste", trans="corte", footnote=FA, lines=[
        S("8:41. Más adelante, el Iryo está parado ante la señal de Urda. Recibe la misma orden."),
        S("8:48. La maquinista avisa: no puede reiniciar, sigue parada."),
        S("Según los audios, nadie avisó al AVE.", 0.3),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@nadie", "general", [540, 1020], 0.8, zoom=1.06)],
       elements=[
        obj("via", 540, 1184, 0, 1.0, entra="nada", props={"ancho": 1600}),
        tren(760, 0, "rojo", "iryo"),
        tren(-900, "@nadie-1.0", "azul", "ave", acciones=[{"at": "@nadie-1.0", "x": -260, "dur": 2.6}]),
        etq("AVE 2080 · A 25 KM", 200, 760, "@nadie", "azul", 0.6, hud=True),
        etq("SEÑAL DE URDA", 900, 900, "@señal", "rojo", 0.6, hud=True),
        etq("IRYO 6076 · PARADO", 700, 760, 0.3, "rojo", 0.7, hud=True),
        hora("8:41", "@8:41", out="@8:48"),
        hora("8:48", "@8:48", out="@nadie"),
        obj("bocadillo", 540, 600, "@reiniciar", 0.95, hud=True, entra="pop", sfx="pop", out="@nadie",
            props={"lineas": ["IRYO:", "«no puedo reiniciar,", "sigo parada»"]}),
        rot("NADIE AVISÓ AL AVE", 540, 460, "@nadie", 80, "blanco"),
        sello("SEGÚN LOS AUDIOS", "naranja", 1500, "@audios"),
    ]),
    # 4 · LA NORMA: a la vista, 40 km/h; el reloj llega a las 8:54 y la pantalla se queda en negro
    dict(id="norma", fondo={"tipo": "plano", "color": LUTO}, animo="triste", trans="papel",
         footnote="Ministerio de Transportes vía Euronews 29/10/2026 · García-Page 29/10/2026", lines=[
        S("Con el sistema caído, la norma era ir a la vista y a 40 kilómetros por hora como máximo."),
        S("A las 8:54 llegó el choque. Hoy ya son 69 los fallecidos.", 0.3),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        obj("senal", 540, 760, 0.2, 1.1, hud=True, entra="pop", sfx="pop", props={"numero": "40"}, out="@8:54"),
        rot("A LA VISTA · MÁX. 40 KM/H", 540, 420, "@vista", 66, "tinta", out="@8:54"),
        obj("lazo", 540, 640, "@8:54", 0.9, hud=True, entra="crece", dibuja=1.0),
        obj("contador", 540, 1060, "@69", 0.8, hud=True, entra="pop", props={"valor": 69, "sufijo": " FALLECIDOS", "ancho": 860}),
        sello("CIFRA PROVISIONAL", "naranja", 1500, "@fallecidos"),
    ]),
    # 5 · RESPONSABILIDADES: el Gobierno y el ministro
    dict(id="gobierno", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="triste", trans="barrido",
         footnote="Euronews 29/10 · elDiario.es 29/10 · El Independiente 29/10/2026", lines=[
        S("El ministro Óscar Puente lo llama «inexplicable». Comparecerá en el Congreso el 3 de noviembre."),
        S("Sánchez promete aclarar hasta el último detalle.", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@Sánchez", "general", [540, 1000], 0.5)],
       elements=[
        quien("puente", 330, 0, 0.55, "serio", entra="izq", acciones=[{"at": "@inexplicable", "pose": "encoge"},
                                                                       {"at": "@Congreso", "pose": "manos_juntas"}]),
        obj("bocadillo", 540, 520, "@inexplicable", 0.72, hud=True, entra="pop", sfx="pop", out="@Sánchez",
            props={"lineas": ["PUENTE:", "«inexplicable»", "Congreso · 3 nov."]}),
        quien("sanchez", 1300, "@Sánchez", 0.55, "serio", entra="nada", acciones=[
            {"at": "@Sánchez", "x": 780, "dur": 0.6, "mira": "izq"}, {"at": "@detalle", "pose": "manos_juntas"}]),
        obj("bocadillo", 540, 520, "@Sánchez", 0.72, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["SÁNCHEZ:", "«esclarecer hasta", "el último detalle»"]}),
        sello("DECLARACIONES", "azul", 1500, "@Puente"),
    ]),
    # 6 · LA OPOSICIÓN Y LOS SOCIOS: PP, Vox y ERC, una frase cada uno
    dict(id="oposicion", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="triste", trans="corte",
         footnote="Feijóo (CMM 29/10) · Vox (Infobae 28/10) · Rufián (elDiario.es 29/10)", lines=[
        S("Feijóo: las responsabilidades políticas «no son opcionales». Vox se ha querellado por homicidio imprudente."),
        S("Y Rufián, socio del Gobierno: una sola persona no puede ser responsable de cientos de vidas.", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        quien("feijoo", 230, 0, 0.5, "serio", entra="pop", acciones=[{"at": "@opcionales", "pose": "senala"}]),
        quien("abascal", 540, "@Vox", 0.5, "serio", entra="pop", acciones=[{"at": "@querellado", "pose": "cruzados"}]),
        quien("diputado", 850, "@Rufián", 0.5, "serio", entra="pop", acciones=[{"at": "@persona", "pose": "encoge"}]),
        obj("bocadillo", 540, 520, "@Feijóo", 0.7, hud=True, entra="pop", sfx="pop", out="@Vox",
            props={"lineas": ["FEIJÓO (PP):", "«no son opcionales»"]}),
        obj("bocadillo", 540, 520, "@Vox", 0.7, hud=True, entra="pop", sfx="pop", out="@Rufián",
            props={"lineas": ["VOX:", "querella por", "homicidio imprudente"]}),
        obj("bocadillo", 540, 520, "@Rufián", 0.7, hud=True, entra="pop", sfx="pop",
            props={"lineas": ["RUFIÁN (ERC):", "«una sola persona", "no puede ser", "responsable»"]}),
    ]),
    # 7 · CIERRE: luto, la investigación y el «síguenos» sobrio
    dict(id="cierre", fondo={"tipo": "plano", "color": LUTO}, animo="triste", trans="iris", footnote="Luto oficial: RD 949/2026",
         lines=[
        S("Quién falló lo dirá la investigación. España está de luto hasta el sábado."),
        S("Síguenos para no perderte lo que se sepa. Nuestro recuerdo, para las víctimas.", 0.3),
    ], camara=[plano(0, "general", [540, 980], 0)],
       elements=[
        obj("lazo", 540, 640, 0, 0.8, hud=True, entra="nada"),
        quien("piz", 540, 0, 0.55, "triste", y=1500, entra="nada", acciones=[{"at": "@investigación", "mira": "camara"},
                                                                             {"at": "@recuerdo", "pose": "manos_juntas", "mira": "abajo"}]),
        sello("INVESTIGACIÓN ABIERTA", "naranja", 1180, "@investigación", out="@Síguenos"),
        rot("SÍGUENOS · @PIZARRAPUBLICA", 540, 430, "@Síguenos", 58, "tinta", out="@recuerdo"),
        rot("EN RECUERDO DE LAS VÍCTIMAS", 540, 430, "@recuerdo", 62, "tinta"),
    ]),
]

if __name__ == "__main__":
    SB = episodio("urda_audios", "Urda: ocho minutos y una orden", scenes,
                  {"t": 3.0, "titulo": "Urda: ocho minutos y una orden", "capitulo": None},
                  ["Euronews (29/10/2026): lo que revelan los audios del centro de control de Atocha",
                   "Castilla-La Mancha Media (29/10/2026): García-Page eleva a 69 los fallecidos; Feijóo",
                   "elDiario.es (29/10/2026, directo): Sánchez, Rufián, hospitalizados",
                   "El Independiente (29/10/2026): Puente comparecerá el 3 de noviembre",
                   "Infobae (28/10/2026): querella de Vox; RD 949/2026 de luto oficial",
                   "Tono de luto: sin gags ni caras en los trenes; el choque no se dibuja; el controlador no se nombra"],
                  ("🖤 Urda: ocho minutos y una orden\n"
                   "📻 8:36 · Atocha al AVE: «reanude con marcha normal»\n"
                   "🚆 8:48 · El Iryo avisa de que sigue parado. Según los audios, nadie avisa al AVE\n"
                   "⚠️ La norma con el sistema caído: a la vista y a 40 km/h\n"
                   "🕯️ 69 fallecidos (cifra provisional)\n"
                   "🗣️ Puente, Sánchez, Feijóo, Vox y Rufián: qué dice cada uno\n"
                   "⚖️ Quién falló lo dirá la investigación\n"
                   "🔔 Síguenos para no perderte lo que se sepa · 📚 Fuentes en comentarios"),
                  "📚 Fuentes: audios del centro de control (El País, elDiario.es, vía Euronews 29/10) · CMM 29/10 · "
                  "El Independiente 29/10 · Infobae 28/10. ¿Ves un error? Dínoslo.",
                  ["#Urda", "#Toledo", "#tren", "#accidente", "#OscarPuente", "#pizarrapublica"],
                  series_tag="EN DESARROLLO")
    SB.update(tono="sobrio", music_volume=0.12, sfx_volume=0.5)
    json.dump(SB, open(os.path.join(OUT, "urda_audios.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
