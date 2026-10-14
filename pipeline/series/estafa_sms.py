#!/usr/bin/env python3
"""«El código que no tenías que dar» (2026): estafa del falso banco por SMS en Casas Ibáñez (Albacete).

Fuentes (noticia del 08/10/2026, Guardia Civil, operación «Corduro»):
  Cadena SER Radio Albacete (08/10/2026) · El Digital de Albacete (08/10/2026):
  https://www.eldigitaldealbacete.com/2026/10/08/creyo-que-evitaba-una-estafa-y-perdio-90-000-euros-guardia-civil-de-albacete-desarticula-una-red-criminal-con-un-detenido-de-valencia/
  SomosCLM: https://somosclm.com/ab/una-estafa-de-casi-90-000-euros-en-casas-ibanez-acaba-con-un-detenido-y-tres-investigados/590990/
  Hechos: un falso empleado de una entidad bancaria avisa de transferencias sospechosas; la víctima recibe SMS con
  códigos de validación y los facilita creyendo que cancela las operaciones; en realidad autoriza 4 transferencias
  (89.900 €). El dinero salta entre cuentas. Recuperados 57.600 €; faltan 32.300 €. 1 detenido (40 años, Valencia) y
  3 investigados (Asturias, Madrid, Las Palmas). Estafa, blanqueo y grupo criminal.
  Ministerio del Interior, nota 10/07/2026: 488.426 ciberdelitos en 2025, 429.677 estafas informáticas (casi 9 de cada 10).
  https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/interior/Paginas/2026/100726-interior-ciberdelitos.aspx
Los códigos que salen en el móvil son de ejemplo. La víctima se representa con Pizón (personaje).
Gags: el móvil que vibra y salta · el banquero se quita el disfraz (¡ZAS!) · el saco de dinero huye de banco en banco ·
el estafador tropieza al llegar la Guardia Civil.
Uso: python3 series/estafa_sms.py → storyboards/estafa_sms.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import compra2026 as base  # noqa: E402
from compra2026_serie import edif, obj, pj, plano, rot  # noqa: E402
from padres_viva import V  # noqa: E402
from universo import gags  # noqa: E402

C = "red"
SUELO = 1340
FUENTE = "Guardia Civil de Albacete, operación Corduro (08/10/2026)"


def pizon(x, at=0.0, scale=0.85, cara="normal", acciones=(), **kw):
    return dict(type="personaje", quien="pizon", id="pizon", x=x, y=SUELO, scale=scale, at=at, cara=cara,
                acciones=list(acciones), **kw)


def movil(x, y, at, pantalla, scale=1.0, acciones=(), **props):
    return obj("movil", x, y, at, scale, props={"pantalla": pantalla, **props}, acciones=acciones, id="movil", hud=True)


scenes = [
    # 1 · GANCHO: la paradoja (perdió el dinero intentando protegerlo)
    dict(id="gancho", fondo="salon", animo="tension", footnote=FUENTE, lines=[
        V("Una persona de Albacete perdió 89.900 euros…", "energia"),
        V("intentando proteger su dinero.", "remate", 0.2),
    ], camara=[plano(0, "medio", [470, 1000], 0), plano("@89.900", "general", dur=0.3),
               plano("@proteger", "medio", "pizon", 0.4, aire=160)],
       elements=[
        pizon(400, 0, 0.85, "preocupado", entra="nada", objeto="hucha", pose="sostiene", acciones=[
            {"at": "@perdió", "take": True, "cara": "susto"},
            {"at": "@89.900", "objeto": None, "pose": "cabeza", "cara": "susto", "tiembla": True},
            {"at": "@proteger", "cara": "confundido", "pose": "encoge", "mira": "camara"}]),
        gags.dinero_vuela("@perdió+0.2", 620, 1000, 8),
        rot("−89.900 €", 540, 560, "@89.900", 140, C, golpe=True, rot=-4),
    ]),
    # 2 · LA LLAMADA: un falso empleado del banco
    dict(id="llamada", fondo="salon", animo="tension", trans="pan", footnote=FUENTE, lines=[
        V("Le llama alguien «de su banco»: hay transferencias sospechosas en su cuenta.", "intriga"),
    ], camara=[plano(0, "general", dur=0), plano("@banco", "medio", "pizon", 0.35, aire=200),
               plano("@sospechosas", "general", dur=0.4)],
       luz=[{"at": "@sospechosas", "tipo": "alarma"}],
       elements=[
        pizon(260, 0, 0.8, "normal", entra="nada", acciones=[
            {"at": "@llama", "cara": "sorpresa", "mira": "movil"},
            {"at": "@banco", "cara": "preocupado", "mira": "banquero"},
            {"at": "@sospechosas", "take": True, "cara": "susto"}]),
        movil(300, 560, "@llama-0.3", "llamada", 0.7, remite="TU BANCO", suena=True, entra="pop", sfx="sorpresa",
              out="@transferencias"),
        pj("banquero", 830, "@transferencias-0.3", 0.8, "serio", id="banquero", entra="der", pose="senala",
           acciones=[{"at": "@sospechosas", "cara": "preocupado", "pose": "manos_juntas"}]),
        obj("bocadillo", 760, 500, "@transferencias", 0.8, props={"lineas": ["¡Transferencias", "sospechosas!"], "cola": [1, 1]},
            hud=True, out="@cuenta+0.6"),
    ]),
    # 3 · LOS CÓDIGOS: «para cancelarlas, dímelos»
    dict(id="codigos", fondo="salon", animo="tension", trans="corte", footnote="Guardia Civil de Albacete (08/10/2026) · códigos de ejemplo", lines=[
        V("Para cancelarlas, le llegan SMS con códigos… y se los pide.", "normal"),
        V("Uno. Otro. Y otro.", "intriga", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@Uno", "medio", "pizon", 0.3, aire=220)],
       elements=[
        pizon(260, 0, 0.8, "preocupado", entra="nada", acciones=[
            {"at": "@SMS", "mira": "movil", "cara": "pensativo"},
            {"at": "@pide", "cara": "preocupado", "habla": True, "pose": "manos_juntas"},
            {"at": "@Otro", "salta": True}, {"at": "@otro", "cara": "confundido"}]),
        pj("banquero", 830, 0, 0.8, "normal", id="banquero", entra="nada",
           acciones=[{"at": "@pide", "cara": "ilusionado", "pose": "ruega"}, {"at": "@otro", "cara": "riendo"}]),
        movil(540, 600, "@SMS-0.2", "codigo", 0.85, remite="BANCO", codigo="482719", entra="pop", sfx="calculadora",
              acciones=[{"at": "@Otro", "props": {"pantalla": "codigo", "remite": "BANCO", "codigo": "093561"}, "salta": True},
                        {"at": "@otro", "props": {"pantalla": "codigo", "remite": "BANCO", "codigo": "770248"}, "salta": True}]),
        obj("bocadillo", 230, 450, "@Uno", 0.65, props={"texto": "4… 8… 2…", "cola": [-1, 1]}, hud=True, out="@Otro"),
    ]),
    # 4 · GIRO: el banquero se quita el disfraz
    dict(id="giro", fondo="rayos", animo="comico", musica="corte", trans="iris", footnote=FUENTE, lines=[
        V("Pero esos códigos no cancelaban nada.", "remate"),
        V("Autorizaban las transferencias.", "sorpresa", 0.35),
    ], camara=[plano(0, "general", dur=0), plano("@Autorizaban", "medio", [540, 1000], 0.2)],
       elements=[
        pizon(250, 0, 0.75, "confundido", entra="nada", acciones=[
            {"at": "@nada", "cara": "pensativo", "mira": "banquero"},
            {"at": "@Autorizaban", "take": True, "cara": "susto", "pose": "cabeza", "mira": "estafador"}]),
        pj("banquero", 760, 0, 0.8, "riendo", id="banquero", entra="nada", acciones=[{"at": "@Autorizaban-0.05", "sale": "pop"}]),
        pj("estafador", 760, "@Autorizaban", 0.8, "burla", id="estafador", entra="pop",
           acciones=[{"at": "@transferencias", "salta": True, "pose": "punos"}]),
        dict(type="efecto", efecto="pum", text="¡ZAS!", x=760, y=820, at="@Autorizaban", scale=0.9, vida=0.8),
        rot("CANCELAR", 540, 400, "@cancelaban", 100, "verde", out="@Autorizaban"),
        rot("AUTORIZAR", 540, 400, "@Autorizaban", 120, C, golpe=True, rot=-5),
    ]),
    # 5 · EL DINERO HUYE: cuatro transferencias, de cuenta en cuenta
    dict(id="huye", fondo="calle", animo="comico", trans="pan", footnote=FUENTE, lines=[
        V("Cuatro transferencias. 89.900 euros.", "energia"),
        V("Y el dinero, saltando de cuenta en cuenta para no dejar rastro.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@saltando", "abierto", dur=0.5)],
       elements=[
        edif("banco", 190, 0, 0.3, entra="nada", cara="sorpresa"),
        edif("banco", 540, 0, 0.3, entra="nada", cara="esceptica"),
        edif("banco", 890, 0, 0.3, entra="nada", cara="confundido"),
        obj("saco", 190, SUELO - 130, "@Cuatro", 0.75, id="saco", entra="pop", piernas=True, cara="burla",
            acciones=[{"at": "@saltando", "x": 540, "corre": True, "dur": 0.7}, {"at": "@saltando+0.75", "salta": True},
                      {"at": "@cuenta#2", "x": 890, "corre": True, "dur": 0.7}, {"at": "@rastro", "sale": "der"}]),
        rot("4 TRANSFERENCIAS", 540, 470, "@Cuatro", 84, "amarillo", golpe=True),
        rot("89.900 €", 540, 600, "@89.900", 120, C, golpe=True),
        dict(type="efecto", efecto="lineas", x=700, y=1220, at="@saltando", vida=1.2),
    ]),
    # 6 · LA GUARDIA CIVIL: lo que se recuperó y lo que no
    dict(id="pillado", fondo="calle", animo="final", trans="iris", footnote=FUENTE, lines=[
        V("La Guardia Civil recuperó 57.600 euros. Faltan 32.300.", "normal"),
        V("Un detenido en Valencia y tres investigados.", "remate"),
    ], camara=[plano(0, "general", dur=0), plano("@detenido", "medio", "estafador", 0.3, aire=200)],
       elements=[
        pj("estafador", 150, 0, 0.75, "burla", id="estafador", entra="nada",
           acciones=[{"at": 0, "x": 520, "corre": True, "dur": 1.6}, {"at": "@Faltan", "x": 760, "corre": True, "dur": 0.8},
                     {"at": "@detenido", "tropieza": True, "cara": "susto"}, {"at": "@investigados", "cara": "triste"}]),
        obj("saco", 860, SUELO - 120, "@57.600", 0.55, entra="cae", cara="riendo"),
        rot("RECUPERADOS: 57.600 €", 540, 460, "@57.600", 70, "verde", golpe=True),
        rot("SIN RECUPERAR: 32.300 €", 540, 560, "@32.300", 70, C, golpe=True),
        rot("1 DETENIDO · 3 INVESTIGADOS", 540, 680, "@detenido", 60, "amarillo"),
    ]),
    # 7 · LA REGLA DE ORO: el código es una firma
    dict(id="regla", fondo="oficina", animo="curioso", trans="pan", footnote="Recomendaciones de la Guardia Civil", lines=[
        V("Regla de oro: un código que no has pedido es alguien intentando usar tu cuenta.", "intriga"),
        V("Tu banco nunca te lo pide. Cuelga y llama tú.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@Cuelga", "medio", "profe", 0.3, aire=200)],
       elements=[
        pj("profe", 300, 0, 0.82, "serio", id="profe", entra="izq", pose="senala_arriba",
           acciones=[{"at": "@pedido", "cara": "pensativo"}, {"at": "@alguien", "cara": "esceptica", "pose": "senala"},
                     {"at": "@usar", "take": True}, {"at": "@nunca", "cara": "serio", "pose": "jarras"},
                     {"at": "@Cuelga", "cara": "ilusionado", "pose": "pulgar"}]),
        movil(740, 640, "@código-0.2", "codigo", 0.8, remite="BANCO", codigo="482719", entra="pop",
              acciones=[{"at": "@alguien", "props": {"pantalla": "aviso"}, "tiembla": True}, {"at": "@cuenta", "salta": True}]),
        rot("CÓDIGO = FIRMA", 540, 460, "@alguien", 90, "amarillo", golpe=True),
        obj("checklist", 600, 900, "@nunca", 0.85, hud=True,
            props={"items": ["No dictes códigos", "Cuelga y llama tú", "Activa los avisos"], "marcas": ["si", "si", "si"]}),
    ]),
    # 8 · FINAL: dato general + llamada a compartir/seguir dentro de la historia
    dict(id="final", fondo="salon", animo="final", trans="iris", footnote="Ministerio del Interior, balance de cibercriminalidad 2025 (10/07/2026)",
         lines=[
        V("En España, casi nueve de cada diez ciberdelitos ya son estafas.", "normal"),
        V("Mándaselo a quien siempre coge el teléfono. Y síguenos para no picar.", "energia"),
    ], camara=[plano(0, "general", dur=0), plano("@Mándaselo", "medio", "pizon", 0.4, aire=200)],
       elements=[
        pizon(320, 0, 0.82, "triste", entra="nada", acciones=[
            {"at": "@ciberdelitos", "take": True, "cara": "susto", "mira": "camara"},
            {"at": "@estafas", "cara": "indignado", "pose": "punos"},
            {"at": "@teléfono", "salta": True},
            {"at": "@Mándaselo", "cara": "idea", "pose": "sostiene", "objeto": {"tipo": "movil", "pantalla": "sms",
                                                                            "lineas": ["¡Ojo con", "los códigos!"]}},
            {"at": "@síguenos", "cara": "riendo", "pose": "saluda", "objeto": None, "salta": True}]),
        rot("9 DE CADA 10", 540, 480, "@nueve", 120, C, golpe=True, out="@Mándaselo"),
        rot("de los ciberdelitos son estafas", 540, 600, "@ciberdelitos", 58, "blanco", out="@Mándaselo"),
        rot("SÍGUENOS", 540, 480, "@síguenos", 100, "amarillo", fx=[{"at": "@picar", "do": "latir"}]),
    ]),
]

SB = dict(base.SB)
SB.update(
    slug="estafa_sms", title="El código que no tenías que dar", series_tag="ESTAFAS: QUE NO TE PASE",
    scenes=scenes, banda=True, music_volume=0.2, scribble_volume=0.0, sfx_volume=1.0, end_hold=0.9,
    portada={"t": 2.0, "titulo": "El código que no tenías que dar", "capitulo": None},
    sources=[
        "Guardia Civil de Albacete, operación Corduro, vía El Digital de Albacete (08/10/2026): "
        "https://www.eldigitaldealbacete.com/2026/10/08/creyo-que-evitaba-una-estafa-y-perdio-90-000-euros-guardia-civil-de-albacete-desarticula-una-red-criminal-con-un-detenido-de-valencia/",
        "Cadena SER Radio Albacete (08/10/2026): https://cadenaser.com/castillalamancha/2026/10/08/se-hicieron-pasar-por-su-entidad-bancaria-para-estafarle-89900-con-sms-falsos-radio-albacete/",
        "Ministerio del Interior, ciberdelitos 2025 (10/07/2026): https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/interior/Paginas/2026/100726-interior-ciberdelitos.aspx",
    ],
    caption=("📱 Le llamó «su banco» por unas transferencias sospechosas… y perdió 89.900 €\n"
             "🔢 Los códigos SMS que dictó no cancelaban nada: las autorizaban\n"
             "🏃 4 transferencias saltando de cuenta en cuenta\n"
             "🚔 Recuperados 57.600 € · faltan 32.300 € · 1 detenido y 3 investigados\n"
             "💬 ¿Te han intentado algo parecido? Cuéntalo\n"
             "➡️ Mándaselo a quien siempre coge el teléfono · 🔔 Síguenos · 📚 Fuentes en comentarios"),
    pinned_comment=("📚 Fuentes: Guardia Civil de Albacete, operación Corduro (El Digital de Albacete y Cadena SER, 08/10/2026) · "
                    "Ministerio del Interior, ciberdelitos 2025 (10/07/2026): 429.677 de 488.426 son estafas informáticas. "
                    "Pizón representa a la víctima; los códigos del vídeo son de ejemplo. ¿Ves un error? Dínoslo."),
    hashtags=["#PizarraPública", "#Estafa", "#Phishing", "#SMS", "#Banco", "#GuardiaCivil", "#Albacete", "#Ciberseguridad"],
)

if __name__ == "__main__":
    path = os.path.join(OUT, f"{SB['slug']}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
