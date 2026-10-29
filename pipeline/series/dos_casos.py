#!/usr/bin/env python3
"""«Una condena y una citación» (29/10/2026). Dos casos judiciales que llegan al 29N: la condena firme de Ábalos (caso
mascarillas) y la citación de las hijas de Zapatero (caso Plus Ultra) el 30/11, al día siguiente de votar. Presunción de
inocencia en todo lo que no es sentencia; personajes como pizarras con chapa, sin caricatura; las hijas no se dibujan.

Guion y fuentes: /mnt/project-files/insta/guiones/propuestas_29oct.md (aprobado por joel el 29/10/2026, 17:48 UTC)
  Ábalos: Supremo, 22/06/2026, unanimidad de siete magistrados, sentencia firme: 24 años y 3 meses por organización
    criminal, cohecho, tráfico de influencias y malversación; Koldo García 19 años y 8 meses; Aldama 4 años y medio
    (suspendida). 10.000 € al mes durante 34 meses (oct. 2019 - jun. 2022). Su entorno la llama «desproporcionada» y
    estudia el amparo en el Constitucional (Ara 22/06/2026; El Independiente 22/06/2026).
  Plus Ultra: rescate público de 53 M€ en 2021. Laura y Alba Rodríguez Espinosa, administradoras de Whathefav,
    investigadas desde junio por presunto blanqueo (Anticorrupción ve también tráfico de influencias); declaran el 30/11
    (Euronews 21/09/2026; CGPJ 18/06/2026; Vozpópuli 19/06/2026). Whathefav cobró 239.755 € de Análisis Relevante, que pagó
    490.780 € a Zapatero (Vozpópuli). Zapatero sostiene que eran trabajos de marketing de sus hijas (Euronews).
    Peritos tasan en un millón de euros las joyas del despacho de Zapatero (titular de El Independiente, 29/10/2026).
  Equilibrio: Vox lleva de n.º 6 por Murcia a Aida Peñalver, investigada por presunta falsedad documental (Diario de
    Avisos 24/10/2026).
"""
from _mundo import *  # noqa: F401,F403

GRANATE = (110, 40, 52)
AZUL = (28, 52, 110)
FA = "Tribunal Supremo, sentencia 22/06/2026 · Ara y El Independiente 22/06/2026"
FZ = "Audiencia Nacional (CGPJ 18/06/2026) · Euronews 21/09/2026 · Vozpópuli 19/06/2026"


def nov(at, marcados, colores, **kw):
    return obj("calendario", 540, 800, at, 0.8, hud=True, entra="pop", sfx="papel",
               props={"mes": "NOVIEMBRE", "inicio": 6, "dias": 30, "marcados": marcados, "colores": colores}, **kw)


scenes = [
    # 1 · GANCHO: el calendario de noviembre: el 29 se vota, el 30 al juzgado
    dict(id="gancho", fondo={"tipo": "plano", "color": AZUL}, animo="tension", footnote=FA + " · " + FZ, lines=[
        V("Un exministro de Sánchez ya tiene condena firme: 24 años de cárcel.", "energia"),
        V("Y las hijas de Zapatero declaran ante el juez… el día después de votar.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@hijas", "general", [540, 860], 0.6, zoom=1.1)],
       elements=[
        rot("24 AÑOS", 540, 520, "@24", 150, "amarillo", golpe=True, out="@hijas"),
        quien("abalos", 540, 0.2, 0.6, "serio", y=1300, entra="abajo", out="@hijas"),
        nov("@hijas", [29, 30], {29: "azul", 30: "rojo"}),
        etq("29 · VOTAS", 300, 1260, "@votar-0.4", "azul", 0.7, hud=True),
        etq("30 · AL JUZGADO", 780, 1260, "@votar", "rojo", 0.7, hud=True),
        sello("CASO PLUS ULTRA", "naranja", 1420, "@votar+0.3"),
    ]),
    # 2 · ÁBALOS: la sentencia se despliega
    dict(id="abalos", fondo={"tipo": "plano", "color": GRANATE}, animo="tension", trans="papel", footnote=FA, lines=[
        V("Caso mascarillas. El Supremo, por unanimidad, condenó a José Luis Ábalos a 24 años y 3 meses.", "normal"),
        V("Organización criminal, cohecho, tráfico de influencias y malversación.", "normal", 0.1),
        V("Koldo García, casi 20 años. Y Aldama, cuatro y medio.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@Koldo", "general", [540, 900], 0.5)],
       elements=[
        quien("abalos", 230, 0, 0.55, "serio", y=1450, entra="izq", acciones=[{"at": "@condenó", "cara": "triste", "pose": "caidos"}]),
        obj("documento", 640, 820, 0.2, 0.85, hud=True, id="doc", entra="nada", dibujo=1.1, sfx="papel", props={
            "titulo": "SENTENCIA · SUPREMO", "ancho": 700,
            "articulos": [
                {"id": "a", "titulo": "ÁBALOS · 24 AÑOS Y 3 MESES", "lineas": ["Organización criminal, cohecho,", "tráfico de influencias, malversación"]},
                {"id": "b", "titulo": "KOLDO · 19 AÑOS Y 8 MESES", "lineas": []},
                {"id": "c", "titulo": "ALDAMA · 4 AÑOS Y MEDIO", "lineas": []}]},
            acciones=[{"at": "@condenó", "props": {"resalta": ["a"]}}, {"at": "@Koldo", "props": {"resalta": ["a", "b"]}},
                      {"at": "@Aldama", "props": {"resalta": ["a", "b", "c"]}}]),
        sello("FIRME", "rojo", 1500, "@unanimidad"),
    ]),
    # 3 · EL DINERO: 10.000 € al mes durante 34 meses
    dict(id="dinero", fondo={"tipo": "plano", "color": "amarillo"}, animo="tension", trans="barrido", footnote=FA, lines=[
        V("Según la sentencia, cobraba 10.000 euros al mes. Durante 34 meses.", "normal"),
        V("Su entorno la llama «desproporcionada» y estudia ir al Constitucional.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@34", "general", [540, 900], 0.5, zoom=1.08)],
       elements=[
        obj("contador", 540, 600, "@10.000", 0.9, hud=True, entra="pop", sfx="kaching", dibujo=1.0,
            props={"valor": 10000, "sufijo": " €/MES", "ancho": 820}, out="@34"),
        obj("contador", 540, 600, "@34", 0.9, hud=True, entra="pop", sfx="kaching", dibujo=1.4,
            props={"valor": 340000, "sufijo": " €", "ancho": 820, "color": (190, 40, 44)}),
        etq("× 34 MESES", 540, 780, "@34", "tinta", 0.8, hud=True),
        dict(type="efecto", efecto="lluvia", objeto="billete", n=12, x0=150, x1=930, at="@mes", vida=1.8),
        quien("piz", 1300, "@entorno-0.4", 0.5, "esceptica", y=1500, entra="nada", acciones=[
            {"at": "@entorno-0.4", "x": 820, "dur": 0.5}, {"at": "@desproporcionada", "pose": "cruzados"},
            {"at": "@Constitucional", "pose": "encoge", "cara": "pensativo"}]),
        sello("SU DEFENSA", "azul", 1180, "@entorno"),
    ]),
    # 4 · PLUS ULTRA: el avión, el rescate y la empresa de las hijas
    dict(id="plusultra", fondo={"tipo": "plano", "color": AZUL}, animo="curioso", trans="iris", footnote=FZ, lines=[
        V("Segundo caso. En 2021, el Gobierno rescató a la aerolínea Plus Ultra con 53 millones de euros.", "normal"),
        V("El juez investiga a las hijas de Zapatero por presunto blanqueo.", "normal", 0.15),
        V("Su empresa cobró casi 240.000 euros de una consultora que, a su vez, pagó a Zapatero casi medio millón.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@hijas", "general", [540, 900], 0.5),
               plano("@empresa", "general", [540, 950], 0.5)],
       elements=[
        obj("avion", -300, 700, 0, 0.8, entra="nada", acciones=[{"at": 0.1, "x": 540, "dur": 1.6}], out="@hijas"),
        etq("RESCATE · 53 M€", 540, 980, "@53", "amarillo", 0.85, hud=True, out="@hijas"),
        obj("pergamino", 540, 800, "@hijas", 0.62, entra="abajo", sfx="papel", out="@empresa",
            props={"titulo": "AUDIENCIA NACIONAL", "fecha": "Caso Plus Ultra", "lineas": ["Laura y Alba", "Rodríguez Espinosa:", "investigadas"]}),
        sello("PRESUNTO BLANQUEO", "naranja", 1300, "@blanqueo", out="@empresa"),
        obj("flecha", 540, 820, "@empresa", 0.8, hud=True, entra="pop"),
        etq("CONSULTORA → HIJAS · 239.755 €", 540, 640, "@empresa", "azul", 0.7, hud=True),
        etq("CONSULTORA → ZAPATERO · 490.780 €", 540, 1000, "@pagó", "rojo", 0.7, hud=True),
    ]),
    # 5 · LA DEFENSA y las joyas
    dict(id="zapatero", fondo={"tipo": "plano", "color": GRANATE}, animo="curioso", trans="corte",
         footnote="Euronews 21/09/2026 · El Independiente 29/10/2026", lines=[
        V("Zapatero defiende que eran trabajos de marketing de sus hijas.", "normal"),
        V("Y hoy se ha publicado que los peritos tasan en un millón de euros las joyas de su despacho.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@peritos", "general", [540, 900], 0.5, zoom=1.06)],
       elements=[
        quien("zapatero", 330, 0, 0.6, "normal", entra="izq", acciones=[{"at": "@marketing", "pose": "manos_juntas"},
                                                                         {"at": "@joyas", "cara": "serio"}]),
        obj("bocadillo", 700, 560, "@defiende", 0.72, hud=True, entra="pop", sfx="pop", out="@peritos",
            props={"lineas": ["ZAPATERO:", "trabajos de", "marketing"]}),
        sello("SU DEFENSA", "azul", 1500, "@defiende", out="@peritos"),
        obj("corona", 760, 760, "@joyas-0.3", 0.5, entra="crece", sfx="estrellitas"),
        rot("1.000.000 €", 540, 420, "@millón", 110, "amarillo", golpe=True),
        sello("SEGÚN LA PRENSA", "naranja", 1500, "@peritos"),
    ]),
    # 6 · EQUILIBRIO: no es cosa de un solo partido; presunción de inocencia
    dict(id="equilibrio", fondo={"tipo": "plano", "color": AZUL}, animo="curioso", trans="barrido",
         footnote="Diario de Avisos 24/10/2026", lines=[
        V("Ojo, no es cosa de un solo partido: Vox lleva en sus listas por Murcia a una candidata investigada por presunta falsedad documental.", "normal"),
        V("Y recuerda: investigado no es culpable.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0)],
       elements=[
        quien("diputado", 850, 0, 0.55, "normal", id="p3", entra="pop", acciones=[{"at": "@investigada", "cara": "serio"}]),
        *atriles(),
        etq("VOX · N.º 6 POR MURCIA", 540, 460, "@Murcia", "verde", 0.7, hud=True, out="@recuerda"),
        sello("INVESTIGADO ≠ CULPABLE", "verde", 600, "@recuerda"),
    ]),
    # 7 · FINAL: pregunta y sígueme
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Te influyen estos casos en tu voto? Te leo.", "normal"),
        V("Y sígueme para no perderte nada antes del 29N.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sígueme", "medio", "piz", 0.5, aire=300)],
       elements=[
        obj("urna", 820, 1200, 0, 0.6, entra="nada", props={"llena": 0.5, "texto": "29N"}),
        quien("piz", 420, 0, 0.6, "pensativo", entra="abajo", acciones=[
            {"at": "@influyen", "pose": "piensa", "mira": "camara"}, {"at": "@voto", "pose": "senala", "mira": "der"},
            {"at": "@leo", "cara": "ilusionado"}, {"at": "@sígueme", "pose": "saluda", "cara": "riendo"}]),
        rot("¿TE INFLUYE?", 540, 420, "@influyen", 110, "amarillo", golpe=True, out="@sígueme-0.3"),
        rot("SÍGUEME", 540, 420, "@sígueme", 110, "amarillo", fx=[{"at": "@29N", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("dos_casos", "Una condena y una citación", scenes,
             {"t": 5.2, "titulo": "Ábalos condenado y las hijas de Zapatero, al juez", "capitulo": None},
             ["Ara (22/06/2026) y El Independiente (22/06/2026): sentencia del Supremo del caso mascarillas",
              "Poder Judicial (18/06/2026): el juez del caso Plus Ultra acuerda investigar a las hijas de Zapatero",
              "Euronews (21/09/2026): declaran como investigadas el 30 de noviembre; defensa de Zapatero",
              "Vozpópuli (19/06/2026): pagos de Análisis Relevante a Whathefav y a Zapatero",
              "El Independiente (29/10/2026, titular): los peritos tasan en un millón las joyas de Zapatero",
              "Diario de Avisos (24/10/2026): candidata de Vox por Murcia investigada",
              "Personajes dibujados como pizarras, sin caricatura; las hijas no se dibujan"],
             ("⚖️ Una condena y una citación antes del 29N\n"
              "🔒 Ábalos: 24 años y 3 meses, firme (caso mascarillas)\n"
              "💶 Según la sentencia, 10.000 € al mes durante 34 meses\n"
              "✈️ Plus Ultra: las hijas de Zapatero, investigadas, declaran el 30/11… el día después de votar\n"
              "🗣️ Zapatero: «trabajos de marketing»\n"
              "🟢 Vox también lleva una candidata investigada en Murcia · investigado ≠ culpable\n"
              "💬 ¿Te influyen en tu voto? Te leo 👇\n"
              "🔔 Sígueme para no perderte nada antes del 29N · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Supremo (Ara y El Independiente 22/06/2026) · CGPJ 18/06/2026 · Euronews 21/09/2026 · "
             "Vozpópuli 19/06/2026 · El Independiente 29/10/2026 · Diario de Avisos 24/10/2026. ¿Ves un error? Dínoslo.",
             ["#Abalos", "#Zapatero", "#PlusUltra", "#29N", "#elecciones", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
