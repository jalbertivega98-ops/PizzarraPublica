#!/usr/bin/env python3
"""«Accidente de tren en Urda: lo que se sabe» (28/10/2026). Suceso con víctimas: tono serio y de luto, sin gags ni
caras en los trenes; el choque NO se dibuja. Mundo dibujado: la línea Madrid-Andalucía, los dos trenes en esquema,
los equipos de rescate y el lazo negro.

Guion y fuentes: /mnt/project-files/insta/guiones/accidente_tren_urda.md (aprobado por joel el 28/10/2026, 14:33 UTC;
cifras actualizadas a las 15:30 hora peninsular)
  8:54, entre Los Yébenes y Urda (PK 118, Adif): un AVE de Renfe alcanza a un Iryo parado en la línea Madrid-Andalucía;
    vagones descarrilados y caídos por un terraplén (112 CLM vía EFE/RTVC y Europa Press/The Objective, 28/10).
  Al menos 64 fallecidos (García-Page desde el puesto de mando; Óscar Puente en su comparecencia, Canal Sur 28/10 15:05).
  Heridos: 112 CLM daba «cerca de un centenar» a las 12:43 (Libertad Digital); Protección Civil, más de 179 (El Diario de
    Madrid 14:27, sin fuente precisa): decimos «más de un centenar».
  Viajeros: 147 en el Iryo y 397 en el AVE (Libertad Digital 11:21): decimos «más de 500».
  Puente (El Salto 28/10 15:19): cae el sistema LZB en el tramo; «se autoriza al AVE siniestrado que reanude la marcha
    a las 8:36» aunque tenía que detenerse; «No he atribuido responsabilidades a nadie, eso lo tendrá que establecer la
    investigación».
  UME con unos 100 efectivos (Defensa, 12:33); Guardia Civil, bomberos de Alcázar de San Juan y Orgaz, helicópteros
    sanitarios; hospitales de Madrid activados (Libertad Digital / RTVC).
  Línea Madrid-Andalucía cortada; familias: Renfe 900 10 10 20 y punto de atención 24 h en Atocha (El Diario de Madrid).
"""
import json

from _mundo import *  # noqa: F401,F403
from _mundo import OUT  # noqa: E402

R = "espana"
MAD = P(R, -3.70, 40.42)
URDA = P(R, -3.71, 39.41)
SEV = P(R, -5.98, 37.39)
LINEA = [(-3.70, 40.42), (-3.80, 39.85), (-3.71, 39.41), (-3.93, 38.98), (-4.10, 38.68), (-4.78, 37.89), (-5.98, 37.39)]
LUTO = (226, 224, 220)  # papel gris claro: el lazo negro se lee bien encima
NOCHE_AZUL = (28, 40, 70)


def S(text, pausa=None):
    """Toda la locución va en tono sobrio."""
    return V(text, "sobrio", pausa)


def tren(x, at, color, id, acciones=(), y=1080, scale=0.8):
    return obj("tren", x, y, at, scale, id=id, entra="nada", props={"color": color, "cara": None, "vagones": 1},
               acciones=list(acciones))


scenes = [
    # 1 · GANCHO: el mapa de España se dibuja, la línea Madrid-Andalucía y la chincheta en Urda
    dict(id="gancho", fondo="mar_mapa", limites=LIM, animo="triste", footnote="112 Castilla-La Mancha vía EFE · 28/10/2026",
         lines=[
        S("Esta mañana, dos trenes de alta velocidad han chocado en Urda, en Toledo."),
        S("Esto es lo que se sabe hasta ahora.", 0.25),
    ], camara=[zoom(0, MAD, 1.0, 0), zoom("@Urda", URDA, 2.6, 1.2), zoom("@sabe", URDA, 3.0, 1.0)],
       elements=[
        mapa(R, 0, 1.4, acciones=[{"at": "@trenes", "props": {"lineas": [linea("ave", LINEA, "azul", 1.2, ancho=8)]}},
                                  {"at": "@Toledo", "props": {"resalta": ["Toledo"]}, "sfx": "pop"}]),
        obj("chincheta", URDA[0] + 6, URDA[1], "@Urda", 0.12, props={"diseno": "espana"}, entra="cae"),
        rot("URDA (TOLEDO)", 540, 400, "@Urda", 96, "blanco"),
        sello("EN DESARROLLO", "naranja", 1500, "@sabe"),
    ]),
    # 2 · QUÉ PASÓ: los dos trenes en esquema; el AVE se acerca y la escena se oscurece antes del choque
    dict(id="que_paso", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="triste", trans="iris",
         footnote="Adif, Renfe y 112 CLM · 28/10/2026", luz=[{"at": "@alcanzó+0.6", "tipo": "oscuro"}], lines=[
        S("Eran las 8:54. Un tren de Iryo estaba parado en la línea Madrid-Andalucía."),
        S("Un AVE de Renfe lo alcanzó por detrás. Varios vagones descarrilaron y cayeron por un terraplén.", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@alcanzó", "general", [540, 1040], 0.8, zoom=1.06)],
       elements=[
        obj("via", 540, 1080 + 104, 0, 1.0, entra="nada", props={"ancho": 1600}),
        tren(820, 0, "rojo", "iryo"),
        etq("IRYO · PARADO", 760, 720, "@Iryo", "rojo", 0.7, hud=True),
        tren(-700, "@AVE-0.3", "azul", "ave", acciones=[{"at": "@AVE-0.3", "x": 40, "dur": 1.6}]),
        etq("AVE · RENFE", 150, 720, "@AVE", "azul", 0.7, hud=True),
        rot("8:54", 540, 420, "@8:54", 130, "amarillo"),
        etq("PK 118 · LOS YÉBENES-URDA", 540, 560, "@Madrid-Andalucía", "blanco", 0.6, hud=True),
        sello("CONFIRMADO", "verde", 1500, "@descarrilaron"),
    ]),
    # 3 · LAS VÍCTIMAS: lazo negro y las cifras, provisionales
    dict(id="victimas", fondo={"tipo": "plano", "color": LUTO}, animo="triste", trans="corte",
         footnote="García-Page y Ministerio de Transportes · 112 CLM · 28/10/2026", lines=[
        S("Hay al menos 64 fallecidos y más de un centenar de heridos."),
        S("En los dos trenes viajaban más de 500 personas. Las cifras todavía pueden cambiar.", 0.25),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        obj("lazo", 540, 600, 0, 1.0, hud=True, entra="crece", dibuja=1.2),
        obj("contador", 540, 1000, "@64", 0.8, hud=True, entra="pop", props={"valor": 64, "sufijo": " FALLECIDOS", "ancho": 860}),
        etq("+100 HERIDOS", 540, 1170, "@heridos", "rojo", 0.75, hud=True),
        etq("+500 VIAJEROS", 540, 1300, "@500", "azul", 0.7, hud=True),
        sello("CIFRAS PROVISIONALES", "naranja", 1500, "@cifras"),
    ]),
    # 4 · LO QUE HA EXPLICADO EL MINISTRO: documento que se despliega; nadie es culpable hasta que lo diga la investigación
    dict(id="ministro", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="triste", trans="papel",
         footnote="Óscar Puente, comparecencia 28/10/2026 (El Salto, Canal Sur)", lines=[
        S("El ministro de Transportes, Óscar Puente, ha explicado que falló el sistema de señales de ese tramo."),
        S("Y que, aun así, a las 8:36 se autorizó al AVE a seguir, cuando debía quedarse parado.", 0.15),
        S("Quién es el responsable lo decidirá la investigación.", 0.25),
    ], camara=[plano(0, "general", [540, 900], 0)],
       elements=[
        obj("documento", 540, 820, 0.2, 1.0, hud=True, id="doc", entra="nada", dibujo=1.1, sfx="papel", props={
            "titulo": "LO QUE DICE EL MINISTRO", "ancho": 860,
            "articulos": [
                {"id": "a", "titulo": "FALLA LA SEÑALIZACIÓN", "lineas": ["Cae el sistema que controla", "los trenes en el tramo"]},
                {"id": "b", "titulo": "8:36 · EL AVE SIGUE", "lineas": ["Se le autoriza a reanudar la marcha", "aunque debía seguir parado"]},
                {"id": "c", "titulo": "¿RESPONSABLES?", "lineas": ["Lo establecerá la investigación"]}]},
            acciones=[{"at": "@señales", "props": {"resalta": ["a"]}}, {"at": "@8:36", "props": {"resalta": ["a", "b"]}},
                      {"at": "@responsable", "props": {"resalta": ["a", "b", "c"]}}]),
        sello("DECLARACIÓN", "azul", 1500, "@Puente", out="@responsable"),
        etq("DEBÍA SEGUIR PARADO", 540, 1330, "@parado", "rojo", 0.7, hud=True, out="@responsable"),
        sello("INVESTIGACIÓN ABIERTA", "naranja", 1500, "@responsable"),
    ]),
    # 5 · EL RESCATE: ambulancia y helicóptero llegan; quién está trabajando
    dict(id="rescate", fondo={"tipo": "carretera", "velocidad": 0.0}, animo="triste", trans="barrido",
         footnote="Ministerio de Defensa, Guardia Civil y 112 CLM · 28/10/2026", lines=[
        S("En la zona trabajan bomberos, sanitarios, Guardia Civil y unos cien militares de la UME."),
        S("Y los hospitales de Madrid y de Castilla-La Mancha se han preparado para atender a los heridos.", 0.2),
    ], camara=[plano(0, "general", [540, 1000], 0)],
       elements=[
        obj("helicoptero", 1400, 760, 0, 0.6, entra="nada", acciones=[{"at": 0, "x": 720, "dur": 2.4}]),
        obj("ambulancia", -500, 1230, "@sanitarios-0.6", 0.6, entra="nada", acciones=[{"at": "@sanitarios-0.6", "x": 360, "dur": 1.6}, {"at": "@preparado", "x": 1500, "dur": 1.8}]),
        etq("BOMBEROS", 540, 330, "@bomberos", "rojo", 0.6, hud=True),
        etq("GUARDIA CIVIL", 540, 430, "@Guardia", "verde", 0.6, hud=True),
        etq("UME · 100 MILITARES", 540, 530, "@UME", "amarillo", 0.6, hud=True),
        etq("HOSPITALES EN ALERTA", 540, 630, "@hospitales", "azul", 0.65, hud=True),
    ]),
    # 6 · AYUDA: línea cortada y el teléfono para las familias
    dict(id="ayuda", fondo={"tipo": "plano", "color": NOCHE_AZUL}, animo="triste", trans="corte",
         footnote="Renfe y Protección Civil de Madrid · 28/10/2026", lines=[
        S("La línea entre Madrid y Andalucía sigue cortada."),
        S("Si buscas a un familiar, Renfe atiende en el 900 10 10 20. Y en la estación de Atocha hay un punto de atención.", 0.2),
    ], camara=[plano(0, "general", [540, 960], 0)],
       elements=[
        obj("via", 540, 1104, 0, 1.0, entra="nada", props={"ancho": 1600}, out="@familiar"),
        tren(640, 0, "azul", "parado", acciones=[]) | {"out": "@familiar"},
        sello("LÍNEA CORTADA", "rojo", 700, 0.8, out="@familiar"),
        etq("MADRID — ANDALUCÍA", 540, 520, "@Madrid", "blanco", 0.7, hud=True, out="@familiar"),
        obj("movil", 540, 880, "@familiar", 1.35, hud=True, entra="pop",
            props={"pantalla": "sms", "remite": "FAMILIAS", "lineas": ["RENFE", "900 10 10 20", "ATOCHA 24 H"]}),
        rot("900 10 10 20", 540, 420, "@familiar", 110, "amarillo"),
        etq("ATOCHA · ATENCIÓN 24 H", 540, 1290, "@Atocha", "blanco", 0.65, hud=True),
    ]),
    # 7 · CIERRE: Piz, en silencio, junto al lazo
    dict(id="cierre", fondo={"tipo": "plano", "color": LUTO}, animo="triste", trans="iris", footnote="Información en desarrollo",
         lines=[
        S("La información sigue en desarrollo."),
        S("Nuestro recuerdo, para las víctimas y sus familias.", 0.3),
    ], camara=[plano(0, "general", [540, 980], 0)],
       elements=[
        obj("lazo", 540, 640, 0, 0.8, hud=True, entra="nada"),
        quien("piz", 540, 0, 0.55, "triste", y=1500, entra="nada", acciones=[{"at": "@desarrollo", "mira": "camara"}, {"at": "@recuerdo", "pose": "manos_juntas", "mira": "abajo"}]),
        rot("EN RECUERDO DE LAS VÍCTIMAS", 540, 430, "@recuerdo", 62, "blanco"),
    ]),
]

if __name__ == "__main__":
    SB = episodio("accidente_urda", "Accidente de tren en Urda: lo que se sabe", scenes,
                  {"t": 19.5, "titulo": "Accidente de tren en Urda: lo que se sabe", "capitulo": None},
                  ["EFE vía RTVC (28/10/2026): colisión a las 8:54 cerca de la estación de Urda, vagones por un terraplén",
                   "El Español (28/10/2026): Adif y Renfe, alcance entre dos trenes entre Los Yébenes y Urda",
                   "Libertad Digital (28/10/2026, directo): PK 118, viajeros 147 + 397, UME, 112 CLM",
                   "El Diario de Madrid (28/10/2026): 64 fallecidos según García-Page, Atocha 24 h, línea cortada",
                   "Canal Sur y El Salto (28/10/2026): comparecencia de Óscar Puente",
                   "Tono de luto: sin gags ni caras en los trenes; el choque no se dibuja"],
                  ("🖤 Accidente de tren en Urda (Toledo): lo que se sabe\n"
                   "🚆 Un AVE de Renfe alcanzó a un Iryo parado en la línea Madrid-Andalucía (8:54)\n"
                   "🕯️ Al menos 64 fallecidos y más de un centenar de heridos (cifras provisionales)\n"
                   "🗣️ El ministro Puente: falló la señalización y se autorizó al AVE a seguir; responsables, los dirá la investigación\n"
                   "📞 Familias: Renfe 900 10 10 20 · punto de atención 24 h en Atocha\n"
                   "⚠️ Información en desarrollo\n"
                   "🖤 Nuestro recuerdo para las víctimas y sus familias · 📚 Fuentes en comentarios"),
                  "📚 Fuentes: 112 Castilla-La Mancha (vía EFE) · Adif · Renfe · Gobierno de Castilla-La Mancha · comparecencia de Óscar Puente (28/10/2026). ¿Ves un error? Dínoslo.",
                  ["#Urda", "#Toledo", "#accidente", "#tren", "#ultimahora", "#pizarrapublica"],
                  series_tag="EN DESARROLLO")
    SB.update(tono="sobrio", music_volume=0.12, sfx_volume=0.5)
    json.dump(SB, open(os.path.join(OUT, "accidente_urda.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
