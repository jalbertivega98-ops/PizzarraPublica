#!/usr/bin/env python3
"""«Tu voto vale 0,81 €» (domingo 8/11/2026, 15:00). Lo que cobra cada partido por tu voto el 29N.
Pedido por joel el 8/11/2026 («hazme dos por día… algún dato nuevo»), tema elegido por Claude.
Fuente primaria: Orden HAC/1062/2026, de 7 de octubre (BOE núm. 250, 8/10/2026, BOE-A-2026-20962):
  21.167,64 € por escaño (Congreso o Senado).
  0,81 € por voto al Congreso, solo si la candidatura saca al menos un diputado (en esa circunscripción).
  0,32 € por voto al Senado, solo los votos del candidato que sale senador.
  0,26 € por elector por el envío de sobres y papeletas, si logran grupo parlamentario (o los escaños/votos para tenerlo).
  Límite de gasto: 0,37 € por habitante.
Ejemplo del vídeo (cuenta propia, marcado EJEMPLO): 8 millones de votos × 0,81 = 6,48 M€; 130 escaños × 21.167,64 = 2,75 M€.
"""
from _mundo import *  # noqa: F401,F403

VERDE = (24, 92, 70)
F = "Orden HAC/1062/2026 · BOE 8/10/2026"

scenes = [
    # 1 · GANCHO: Piz vota y del sobre sale una moneda
    dict(id="gancho", fondo="colegio", animo="tension", footnote=F, lines=[
        V("Cuando metes tu voto en la urna, alguien cobra.", "intriga"),
        V("El partido al que votas: 81 céntimos por cada voto.", "remate", 0.15),
    ], camara=[plano(0, "medio", "piz", 0, aire=220), plano("@urna", "medio", "urna", 0.5, aire=180),
               plano("@partido", "general", [540, 900], 0.5), plano("@céntimos", "general", [540, 880], 0.4, zoom=1.06)],
       elements=[
        obj("mesa_electoral", 760, 1340, 0, 0.75, props={"texto": "MESA 1"}, entra="nada"),
        obj("urna", 760, 1020, 0, 0.55, id="urna", entra="nada", props={"llena": 0.35, "texto": "CONGRESO"}),
        quien("piz", 300, 0, 0.62, "ilusionado", entra="nada", objeto="papeleta", pose="sostiene", acciones=[
            {"at": "@metes", "x": 520, "dur": 0.8}, {"at": "@urna", "pose": "senala", "objeto": None, "cara": "riendo"},
            {"at": "@cobra", "cara": "sorpresa", "take": True, "mira": "camara"}, {"at": "@céntimos", "pose": "jarras", "cara": "esceptica"}]),
        dict(type="efecto", efecto="lluvia", objeto="moneda", n=6, x0=640, x1=880, at="@cobra", vida=1.4),
        obj("contador", 540, 520, "@partido", 1.0, hud=True, entra="cae", sfx="kaching", dibujo=1.4,
            props={"valor": 0.81, "decimales": 2, "sufijo": " €", "ancho": 700}),
        rot("POR CADA VOTO", 540, 700, "@cada", 80, "amarillo", golpe=True),
    ]),
    # 2 · EL ESCAÑO
    dict(id="escano", fondo={"tipo": "plano", "color": VERDE}, animo="curioso", trans="barrido", footnote=F, lines=[
        V("Y por cada escaño que gane, mucho más: 21.167 euros.", "sorpresa"),
        V("No me lo invento: lo publicó el BOE el 8 de octubre.", "normal", 0.15),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@21.167", "general", [540, 900], 0.4, zoom=1.06)],
       elements=[
        rot("1 ESCAÑO =", 540, 430, 0, 100, "amarillo"),
        obj("contador", 540, 640, "@escaño", 0.95, hud=True, entra="pop", sfx="kaching", dibujo=1.2,
            props={"valor": 21167.64, "decimales": 2, "sufijo": " €", "ancho": 900}),
        obj("silla", 540, 1330, "@gane", 0.7, hud=True, entra="cae", sfx="golpe", props={"color": "rojo", "texto": "ESCAÑO"}),
        monedas("@21.167", 200, 880, 10),
        obj("cartel", 820, 980, "@BOE", 0.7, hud=True, entra="cae", sfx="papel", props={"texto": "BOE 8/10", "color": "blanco", "tinta": "tinta"}),
        sello("OFICIAL", "azul", 1400, "@octubre"),
    ]),
    # 3 · EL TRUCO: sin diputado, tu voto vale cero
    dict(id="truco", fondo="colegio", animo="tension", trans="corte", footnote=F, lines=[
        V("Pero hay truco.", "intriga"),
        V("Esos 81 céntimos solo los cobra si saca al menos un diputado en tu provincia.", "normal", 0.1),
        V("Si no, tu voto, para su caja, vale cero.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@diputado", "general", [540, 950], 0.5, zoom=1.05),
               plano("@cero", "medio", "piz", 0.4, aire=260)],
       elements=[
        quien("piz", 540, 0, 0.62, "pensativo", entra="nada", acciones=[
            {"at": "@truco", "pose": "piensa", "cara": "esceptica"}, {"at": "@diputado", "pose": "senala_arriba", "cara": "idea"},
            {"at": "@cero", "cara": "susto", "take": True, "pose": "cabeza"}]),
        obj("checklist", 540, 640, "@solo", 0.75, hud=True, entra="pop", sfx="pop", out="@cero-0.2",
            props={"items": ["SACA DIPUTADO: 0,81 €", "NO SACA: 0 €"], "marcas": ["si", "no"]}),
        rot("0 €", 540, 600, "@cero", 200, "rojo", golpe=True),
    ]),
    # 4 · EJEMPLO: la cuenta de un partido grande
    dict(id="ejemplo", fondo={"tipo": "plano", "color": VERDE}, animo="curioso", trans="papel",
         footnote="Cuenta de Pizarra Pública con las cifras del BOE", lines=[
        V("Haz la cuenta con un partido grande: 8 millones de votos y 130 diputados.", "normal"),
        V("Más de 9 millones de euros. Solo por el Congreso.", "energia", 0.1),
    ], camara=[plano(0, "general", [540, 960], 0), plano("@Más", "general", [540, 900], 0.4, zoom=1.07)],
       elements=[
        obj("calculadora", 220, 1180, 0, 0.55, hud=True, entra="pop", sfx="pop"),
        obj("barras", 560, 860, "@votos", 1.0, hud=True, entra="nada", dibujo=1.4, out="@Más",
            props={"sufijo": " M€", "decimales": 2, "tope": 7, "barras": [
                {"texto": "VOTOS", "valor": 6.48, "color": "verde"}, {"texto": "ESCAÑOS", "valor": 2.75, "color": "amarillo"}]}),
        obj("contador", 540, 700, "@Más", 1.0, hud=True, entra="pop", sfx="kaching", props={"valor": 9.2, "decimales": 1, "prefijo": "+", "sufijo": " M€", "ancho": 760}),
        obj("saco", 540, 1050, "@millones-0.1", 0.8, hud=True, entra="cae", sfx="golpe"),
        sello("EJEMPLO", "naranja", 1300, "@cuenta"),
    ]),
    # 5 · EXTRAS: Senado y cartas
    dict(id="extras", fondo="calle", animo="comico", trans="barrido", footnote=F, lines=[
        V("En el Senado, 32 céntimos por voto. Y si te mandan las papeletas a casa, 26 céntimos más por elector.", "normal"),
        V("Eso sí: no pueden gastar sin límite. 37 céntimos por habitante.", "remate", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@casa", "general", [600, 980], 0.5, zoom=1.05),
               plano("@límite", "general", [540, 1000], 0.4)],
       elements=[
        etq("SENADO: 0,32 €", 540, 520, "@Senado", "amarillo", 0.75, hud=True, out="@límite"),
        obj("camion", -300, 1180, "@papeletas", 0.5, entra="nada", props={"texto": "PAPELETAS"},
            acciones=[{"at": "@papeletas", "x": 760, "dur": 1.0}]),
        etq("CARTAS: 0,26 €", 540, 680, "@céntimos", "verde", 0.7, hud=True, out="@límite"),
        quien("piz", 300, "@casa-0.3", 0.55, "sorpresa", entra="abajo", acciones=[
            {"at": "@límite", "pose": "jarras", "cara": "esceptica"}, {"at": "@habitante", "pose": "senala", "mira": "camara"}]),
        obj("senal", 760, 620, "@límite", 0.7, hud=True, entra="pop", sfx="golpe", props={"numero": "0,37"}),
        rot("TOPE DE GASTO", 540, 440, "@límite", 96, "rojo", golpe=True),
    ]),
    # 6 · FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Te leemos en comentarios", lines=[
        V("¿Sabías que tu voto valía dinero? Dímelo en comentarios."),
        V("Y sigue a Piz: esta noche, lo que pasa si votas en blanco.", "energia", 0.15),
    ], camara=[plano(0, "general", [540, 1000], 0), plano("@sigue", "medio", "piz", 0.5, aire=300)],
       elements=[
        quien("piz", 540, 0, 0.6, "pensativo", y=1500, entra="abajo", acciones=[
            {"at": "@dinero", "pose": "piensa", "mira": "camara"}, {"at": "@comentarios", "cara": "ilusionado", "pose": "senala"},
            {"at": "@sigue", "pose": "saluda", "cara": "riendo"}]),
        rot("0,81 €", 540, 420, 0, 130, "amarillo", golpe=True, out="@sigue-0.2"),
        rot("SIGUE A PIZ", 540, 420, "@sigue", 110, "amarillo", fx=[{"at": "@blanco", "do": "latir"}]),
    ]),
]

if __name__ == "__main__":
    episodio("voto_vale", "Tu voto vale 0,81 €", scenes,
             {"t": 4.0, "titulo": "Tu voto vale 0,81 €", "capitulo": None},
             ["Orden HAC/1062/2026, de 7 de octubre (BOE núm. 250, 8/10/2026): subvenciones de las generales del 29N",
              "Ejemplo de 8 millones de votos y 130 escaños: cuenta propia con esas cifras"],
             ("💶 Tu voto vale dinero: 0,81 € para el partido al que votas\n"
              "🪑 Cada escaño: 21.167 €\n"
              "⚠️ Truco: solo cobran tu voto si sacan diputado en tu provincia\n"
              "🧮 Un partido grande se lleva más de 9 millones solo por el Congreso\n"
              "📮 Senado 0,32 € · cartas a casa 0,26 € por elector · tope de gasto 0,37 €\n"
              "💬 ¿Lo sabías? Te leo 👇\n"
              "🔔 Sigue a Piz · 📚 Fuentes en comentarios"),
             "📚 Fuente: Orden HAC/1062/2026 (BOE 8/10/2026). El ejemplo de 9 M€ es una cuenta nuestra con esas cifras. "
             "¿Ves un error? Dínoslo.",
             ["#29N", "#EleccionesGenerales", "#TuVoto", "#BOE", "#PartidosPolíticos", "#pizarrapublica"],
             series_tag="DATOS QUE NO SABÍAS")
