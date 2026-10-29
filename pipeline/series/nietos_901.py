#!/usr/bin/env python3
"""«901 de 163.355» (29/10/2026). Segunda parte de «Los 163.020 que no podrán votar el 29N» (series/voto_nietos.py).
Mundo dibujado: la lista que llega al Supremo, el contador que cae hasta 901 y el viaje por el mapa del mundo.

Guion y fuentes: /mnt/project-files/insta/guiones/propuestas_29oct.md (aprobado por joel el 29/10/2026, 17:48 UTC)
  28/10/2026: la Abogacía del Estado entrega al Supremo (Sala 3ª, Sección 4ª) la lista nominal de 163.355 nacionalizados por
    la ley de nietos; plazo fijado por el Supremo hasta el 28/10, con multas coercitivas de 1.000 € a Bolaños y Albares
    (Infobae 28/10; Estrella Digital 29/10).
  Los consulados solo han certificado a 901 como descendientes de exiliados: «algo más del 0,5 %» (Estrella Digital).
    Son, por ahora, los únicos de la lista con el voto asegurado (Estrella Digital). 163.355 − 901 = 162.454.
  La suspensión (10/09, confirmada el 12/10 por 5 votos a 1) afecta al voto desde el extranjero (CERA); viene de los
    recursos de Vox e Iustitia Europa contra la presunción de exilio 1936-1955 sin prueba individual (Infobae 28/10).
  Pendiente (Estrella Digital): si la lista es reservada y si la suspensión alcanza a los hijos de los nacionalizados (lo
    piden Vox y Hazte Oír). La cifra inicial era 163.020: 335 de diferencia sin explicar.
  El Gobierno calcula que son menos de 14.000 votos, menos del 0,06 % del electorado de 2023 (Infobae, estimación propia).
"""
from _mundo import *  # noqa: F401,F403

R = "mundo"
MAD = P(R, -3.7, 40.4)
BSAS = P(R, -58.4, -34.6)
HABANA = P(R, -82.4, 23.1)
MEXICO = P(R, -99.1, 19.4)
ATL = P(R, -40, 8)
FL = "Abogacía del Estado y Exteriores · Infobae 28/10/2026 · Estrella Digital 29/10/2026"


def ruta(id, desde, dur=1.1):
    lon, lat = desde
    medio = ((lon + -3.7) / 2, (lat + 40.4) / 2 + 9)
    return linea(id, [(lon, lat), medio, (-3.7, 40.4)], "rojo", dur, discontinua=True, ancho=6)


RUTAS = [("arg", (-58.4, -34.6)), ("cub", (-82.4, 23.1)), ("mex", (-99.1, 19.4))]

scenes = [
    # 1 · GANCHO: el contador cae de 163.355 a 901 y Piz no se lo cree
    dict(id="gancho", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="tension", footnote=FL, lines=[
        V("163.355 nuevos españoles, gracias a la ley de nietos.", "energia"),
        V("¿Cuántos han demostrado que su familia huyó por la guerra o la dictadura?", "intriga", 0.1),
        V("901.", "remate", 0.35),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@demostrado", "general", [540, 900], 0.6, zoom=1.06),
               plano("@901.", "general", [540, 900], 0.3, zoom=1.12)],
       elements=[
        obj("contador", 540, 720, 0, 0.95, hud=True, entra="pop", sfx="kaching", out="@901.", dibujo=1.6,
            props={"valor": 163355, "ancho": 840}),
        obj("contador", 540, 720, "@901.", 0.95, hud=True, entra="pop", sfx="golpe", dibujo=0.8,
            props={"valor": 901, "desde": 163355, "ancho": 840, "color": (190, 40, 44)}),
        quien("piz", 540, 0.3, 0.8, "ilusionado", y=1520, entra="abajo", objeto="pasaporte", pose="sostiene", acciones=[
            {"at": "@demostrado", "cara": "pensativo", "pose": "piensa", "objeto": None},
            {"at": "@901.", "cara": "susto", "take": True, "pose": "cabeza"}]),
        rot("¿CUÁNTOS?", 540, 450, "@Cuántos", 100, "amarillo", golpe=True, out="@901."),
        rot("SOLO EL 0,5 %", 540, 450, "@901.+0.4", 100, "amarillo", golpe=True),
    ]),
    # 2 · DE DÓNDE VIENE: la ley de 2022 y la suspensión del Supremo
    dict(id="contexto", fondo="mar_mapa", limites=LIM, animo="curioso", trans="zoom",
         footnote="Ley 20/2022 · Tribunal Supremo, Sala 3ª (10/09 y 12/10/2026)", lines=[
        V("La ley de 2022 dio la nacionalidad a hijos y nietos de españoles nacidos fuera, sobre todo en América.", "normal"),
        V("Pero el Supremo, a petición de Vox y de Iustitia Europa, congeló su voto desde el extranjero para el 29N.", "normal", 0.15),
        V("Salvo para quien acredite que su familia se exilió.", "remate", 0.15),
    ], camara=[zoom(0, ATL, 1.0, 0), zoom("@América", P(R, -60, -5), 1.6, 1.0), zoom("@Supremo", P(R, -9, 44), 3.2, 1.0),
               zoom("@Salvo", P(R, -9, 44), 2.6, 0.6)],
       elements=[
        mapa(R, 0, 1.4, acciones=[
            {"at": "@América", "props": {"resalta": ["ARG", "CUB", "MEX"], "lineas": [ruta(i, p) for i, p in RUTAS]}, "sfx": "rotulador"},
            {"at": "@Supremo", "props": {"resalta": ["ESP", "ARG", "CUB", "MEX"]}}]),
        obj("chincheta", BSAS[0], BSAS[1], "@América", 0.3, props={"diseno": "argentina"}, entra="cae"),
        obj("chincheta", HABANA[0], HABANA[1], "@América+0.2", 0.3, props={"diseno": "cuba"}, entra="cae"),
        obj("chincheta", MEXICO[0], MEXICO[1], "@América+0.4", 0.3, props={"diseno": "mexico"}, entra="cae"),
        obj("urna", MAD[0] + 40, MAD[1] - 10, "@congeló-0.3", 0.18, entra="crece", sfx="pop",
            props={"llena": 0.3, "texto": "29N"}, acciones=[{"at": "@congeló", "tiembla": True}]),
        sello("VOTO CONGELADO", "rojo", 600, "@congeló", out="@Salvo"),
        sello("CON EXILIO ACREDITADO, SÍ VOTA", "verde", 600, "@exilió"),
    ]),
    # 3 · LA LISTA: el Supremo exige los nombres; multas si no llegan; el pergamino se despliega
    dict(id="lista", fondo={"tipo": "plano", "color": (110, 40, 52)}, animo="tension", trans="papel", footnote=FL, lines=[
        V("El Supremo exigió la lista con nombre y apellidos, con multas de mil euros a dos ministros si no llegaba.", "normal"),
        V("Llegó el 28 de octubre: 163.355 nombres.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 900], 0), plano("@Llegó", "general", [540, 860], 0.5, zoom=1.08)],
       elements=[
        quien("jueza", 250, 0, 0.85, "serio", y=1500, entra="pop", acciones=[{"at": "@exigió", "pose": "senala_arriba"},
                                                                     {"at": "@multas", "pose": "jarras"}]),
        obj("documento", 700, 860, "@lista", 0.95, hud=True, id="doc", entra="nada", dibujo=1.0, sfx="papel", props={
            "titulo": "LISTA AL SUPREMO", "ancho": 620,
            "articulos": [{"id": "a", "titulo": "NOMBRE Y APELLIDOS", "lineas": ["· · · · · · · ·", "· · · · · · · ·", "· · · · · · · ·"]}]},
            acciones=[{"at": "@Llegó", "props": {"resalta": ["a"]}, "salta": True}]),
        etq("MULTA: 1.000 €", 540, 420, "@multas", "rojo", 0.75, hud=True, out="@Llegó"),
        rot("163.355 NOMBRES", 540, 420, "@nombres", 90, "amarillo", golpe=True),
    ]),
    # 4 · EL DATO: barras 901 contra 162.454
    dict(id="dato", fondo={"tipo": "plano", "color": "amarillo"}, animo="tension", trans="barrido", footnote=FL, lines=[
        V("De todos ellos, los consulados solo han certificado a 901 como descendientes de exiliados.", "normal"),
        V("Son, por ahora, los únicos con el voto asegurado. Los otros 162.454, de momento, no votan desde fuera.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@162.454", "general", [540, 900], 0.5, zoom=1.06)],
       elements=[
        obj("barras", 540, 960, "@certificado", 1.15, hud=True, entra="nada", dibujo=1.4,
            props={"sufijo": "", "decimales": 0, "tope": 170000, "resalta": [0], "barras": [
                {"texto": "CERTIFICADOS", "valor": 901, "color": "verde"},
                {"texto": "SIN CERTIFICAR", "valor": 162454, "color": "rojo"}]}),
        quien("piz", 1300, "@únicos", 0.45, "pensativo", y=1660, entra="nada", hud=True, acciones=[
            {"at": "@únicos", "x": 930, "dur": 0.5}, {"at": "@162.454", "cara": "sorpresa", "take": True},
            {"at": "@momento", "pose": "encoge", "cara": "confundido", "mira": "camara"}]),
        rot("901", 540, 420, "@901", 130, "verde", golpe=True, out="@162.454"),
        rot("162.454 SIN VOTO", 540, 420, "@162.454", 90, "rojo", golpe=True),
    ]),
    # 5 · LO QUE FALTA: los hijos, la lista secreta y los 335 que nadie explica
    dict(id="pendiente", fondo={"tipo": "plano", "color": (28, 52, 110)}, animo="curioso", trans="iris",
         footnote="Estrella Digital 29/10/2026 · Infobae 28/10/2026 (estimación del Gobierno)", lines=[
        V("Y queda lo gordo: el Supremo debe decidir si la congelación alcanza también a sus hijos, como piden Vox y Hazte Oír.", "normal"),
        V("Detalle curioso: al principio eran 163.020. Hay 335 nombres más que nadie ha explicado.", "intriga", 0.2),
        V("El Gobierno calcula que, al final, serían menos de 14.000 votos.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 950], 0), plano("@335", "general", [540, 900], 0.5, zoom=1.08),
               plano("@14.000", "general", [540, 950], 0.5)],
       elements=[
        obj("checklist", 540, 760, 0.2, 0.85, hud=True, entra="pop", sfx="papel", out="@curioso",
            props={"titulo": "PENDIENTE DEL SUPREMO", "items": ["¿También sus hijos?", "¿Lista reservada?"]}),
        quien("critica", 820, 0, 0.55, "esceptica", y=1440, entra="der", acciones=[
            {"at": "@hijos", "pose": "senala_izq"}, {"at": "@335", "cara": "sorpresa", "take": True},
            {"at": "@explicado", "pose": "encoge", "cara": "confundido"}]),
        obj("lupa", 300, 1100, "@335", 0.7, hud=True, entra="pop", sfx="pop", out="@14.000"),
        rot("163.020 → 163.355", 540, 520, "@163.020", 80, "amarillo", golpe=True, out="@14.000"),
        sello("SIN EXPLICAR", "naranja", 760, "@explicado", out="@14.000"),
        rot("< 14.000 VOTOS", 540, 520, "@14.000", 100, "blanco", golpe=True),
        sello("ESTIMACIÓN DEL GOBIERNO", "azul", 760, "@calcula"),
    ]),
    # 6 · FINAL: pregunta y síguenos
    dict(id="final", fondo="mar_mapa", limites=LIM, animo="final", trans="zoom", footnote="Te leemos en comentarios", lines=[
        V("Si tu abuelo emigró, pero no huyó de la dictadura, ¿deberías poder votar? Te leo.", "normal"),
        V("Y sígueme para no perderte nada antes del 29N.", "energia", 0.15),
    ], camara=[zoom(0, MAD, 4.0, 0), zoom(0.2, ATL, 1.0, 2.2)],
       elements=[
        mapa(R, 0, 0.01, progreso=1.0, resalta=["ESP", "ARG", "CUB", "MEX"], lineas=[ruta(i, p, 0.01) for i, p in RUTAS]),
        quien("piz", 790, "@abuelo", 0.6, "pensativo", y=1500, hud=True, entra="abajo", acciones=[
            {"at": "@votar", "pose": "senala_izq"}, {"at": "@leo", "mira": "camara", "cara": "ilusionado"},
            {"at": "@sígueme", "pose": "saluda", "cara": "riendo"}, {"at": "@nada", "salta": True}]),
        rot("¿SÍ O NO?", 540, 450, "@votar", 120, "amarillo", golpe=True, out="@sígueme-0.3"),
        rot("SÍGUEME", 540, 450, "@sígueme", 110, "amarillo", fx=[{"at": "@29N", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("nietos_901", "901 de 163.355", scenes,
             {"t": 6.0, "titulo": "Ley de nietos: 901 de 163.355", "capitulo": None},
             ["Infobae (28/10/2026): Exteriores confirma que solo 901 personas certifican su condición de descendiente exiliado",
              "Estrella Digital (29/10/2026): la lista de 163.355 nombres llega al Supremo; decisiones pendientes",
              "Tribunal Supremo, Sala 3ª: suspensión cautelar (10/09/2026) confirmada el 12/10/2026",
              "Ley 20/2022 de Memoria Democrática, disposición adicional 8ª (BOE)",
              "Mapas dibujados sobre contornos de Natural Earth (dominio público)"],
             ("🌎 Ley de nietos: 163.355 nuevos españoles… y solo 901 han acreditado exilio\n"
              "⚖️ El Supremo congeló su voto desde el extranjero para el 29N (lo pidieron Vox e Iustitia Europa)\n"
              "📜 El Gobierno entregó la lista con nombres y apellidos, bajo amenaza de multa\n"
              "✅ 901 con voto asegurado · ❌ 162.454 sin voto desde fuera, de momento\n"
              "❓ Pendiente: ¿también sus hijos? Y 335 nombres de más sin explicar\n"
              "💬 ¿Deberían poder votar? Te leo 👇\n"
              "🔔 Sígueme para no perderte nada antes del 29N · 📚 Fuentes en comentarios"),
             "📚 Fuentes: Infobae 28/10/2026 · Estrella Digital 29/10/2026 · Tribunal Supremo (autos 10/09 y 12/10/2026) · "
             "Ley 20/2022 (BOE). ¿Ves un error? Dínoslo.",
             ["#leydenietos", "#29N", "#elecciones", "#Supremo", "#Argentina", "#Cuba", "#pizarrapublica"],
             series_tag="EXPLICADO FÁCIL")
