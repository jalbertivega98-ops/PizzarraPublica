#!/usr/bin/env python3
"""«¿Compensa cobrar más?» (2026): Pizón (SMI + IMV) frente a Piz (24.500 € brutos, sin ayuda).

Fuentes y cálculo:
  SMI 2026: 1.221 € × 14 = 17.094 € brutos (Real Decreto 126/2026, BOE 19/02/2026); deducción IRPF de 590,89 € que
    deja la cuota a 0 (RDL 5/2026). Cotización del trabajador ≈ 6,5 % (contingencias comunes, desempleo, FP y MEI).
    Neto ≈ 15.983 €/año ≈ 1.330 €/mes (12 meses).
  IMV 2026: 733,60 €/mes para un adulto solo (subida del 11,4 %).
  Incentivo al empleo: Real Decreto 240/2026 (BOE 26/03/2026, en vigor el 27/03): del aumento de rentas del trabajo se
    excluyen los primeros 6.000 € y el 50 % del resto (55 % en hogares monoparentales o con discapacidad).
    Pizón (sin ingresos el año anterior): IMV que conserva ≈ 270-400 €/mes según cómo se compute su renta
    (íntegra, neta de cotizaciones o rendimiento neto IRPF) → en el vídeo «unos 300». Total ≈ 1.630 €/mes.
  Piz: bruto necesario para 1.630 €/mes netos (escala general IRPF 2026, mínimo personal, 6,5 % SS) ≈ 24.500 €/año.
  Pegas: solo si ya se cobraba el IMV; se revisa cada año.
Uso: python3 series/compensa_cobrar.py → storyboards/compensa_cobrar.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "storyboards")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import compra2026 as base  # noqa: E402
from compra2026_serie import obj, pj, plano, rot  # noqa: E402
from padres_viva import V  # noqa: E402

C = "red"
SUELO = 1340
BOE = "SMI: RD 126/2026 · IMV: RD 240/2026 · cálculo propio (IRPF y SS aprox.)"


def quien(q, x, at=0.0, scale=0.75, cara="normal", acciones=(), **kw):
    return pj(q, x, at, scale, cara, acciones, id=q, **kw)


scenes = [
    # 1 · GANCHO
    dict(id="gancho", fondo="calle", animo="curioso", footnote=BOE, lines=[
        V("Pizón cobra el sueldo mínimo. Piz, 7.000 euros más al año.", "energia"),
        V("Y a final de mes… tienen casi lo mismo.", "remate", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@mes", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 280, 0, 0.72, "normal", entra="pop", acciones=[{"at": "@Piz", "mira": "piz"}, {"at": "@mismo", "take": True, "cara": "sorpresa"}]),
        quien("piz", 800, "@Piz-0.2", 0.72, "ilusionado", entra="der", acciones=[{"at": "@7.000", "salta": True, "pose": "arriba"},
                                                                                {"at": "@mismo", "take": True, "cara": "susto", "pose": "cabeza"}]),
        rot("SMI", 280, 560, "@mínimo", 100, "amarillo", golpe=True),
        rot("+7.000 €", 800, 560, "@7.000", 100, "verde", golpe=True),
        rot("=", 540, 760, "@mismo", 200, C, golpe=True),
    ]),
    # 2 · PIZÓN: el sueldo mínimo
    dict(id="pizon", fondo="salon", animo="curioso", trans="pan", footnote="SMI 2026: RD 126/2026 · neto con cotización ≈ 6,5 % e IRPF 0 €", lines=[
        V("Pizón: 1.221 euros en 14 pagas. Neto, unos 1.330 al mes.", "normal"),
    ], camara=[plano(0, "general", dur=0), plano("@1.330", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 360, 0, 0.8, "normal", entra="nada", pose="sostiene", objeto="hucha",
              acciones=[{"at": "@1.221", "salta": True}, {"at": "@Neto", "cara": "pensativo"}, {"at": "@1.330", "cara": "ilusionado"}]),
        obj("calculadora", 800, 860, "@pagas", 0.85, id="calc", props={"texto": "1.221"}, entra="pop", sfx="calculadora",
            acciones=[{"at": "@1.330", "props": {"texto": "1.330"}, "salta": True}]),
        rot("1.221 € × 14", 540, 470, "@1.221", 100, "amarillo", golpe=True, out="@Neto"),
        rot("1.330 €", 540, 470, "@1.330", 110, "verde", golpe=True),
    ]),
    # 3 · LA AYUDA QUE NO PIERDE
    dict(id="ayuda", fondo="oficina", animo="tension", trans="iris", footnote="IMV 2026: 733,60 €/mes (1 adulto) · RD 240/2026 · estimación 270-400 €", lines=[
        V("Pero antes cobraba el Ingreso Mínimo Vital. Y al ponerse a trabajar, no lo pierde entero:", "intriga"),
        V("conserva unos 300 euros al mes.", "sorpresa", 0.2),
    ], camara=[plano(0, "general", dur=0), plano("@conserva", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 300, 0, 0.78, "pensativo", entra="izq", acciones=[
            {"at": "@Vital", "mira": "der"}, {"at": "@trabajar", "cara": "preocupado", "pose": "manos_juntas"},
            {"at": "@entero", "take": True}, {"at": "@300", "cara": "riendo", "pose": "arriba", "salta": True}]),
        pj("hacienda", 800, "@Vital-0.3", 0.75, "serio", id="hacienda", entra="der", pose="sostiene",
           objeto={"tipo": "contrato", "titulo": "IMV", "hojas": 1},
           acciones=[{"at": "@entero", "cara": "riendo", "pose": "pulgar"}]),
        rot("IMV: 733,60 €", 600, 600, "@Vital", 90, "amarillo", golpe=True, out="@conserva"),
        rot("+300 €/mes", 600, 600, "@300", 120, "verde", golpe=True),
        dict(type="efecto", efecto="lluvia", objeto="moneda", n=10, x0=200, x1=500, at="@300", vida=1.8),
    ]),
    # 4 · TOTAL PIZÓN vs PIZ
    dict(id="piz", fondo="calle", animo="comico", trans="pan", footnote=BOE, lines=[
        V("Total: unos 1.630. Piz cobra 24.500 brutos, sin ayuda.", "normal"),
        V("Tras IRPF y Seguridad Social: unos 1.630 al mes.", "remate", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@IRPF", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 260, 0, 0.72, "riendo", entra="nada", acciones=[{"at": "@Total", "salta": True}, {"at": "@IRPF", "mira": "piz"},
                                                                       {"at": "@1.630#2", "cara": "burla", "pose": "jarras"}]),
        quien("piz", 1300, "@Piz", 0.72, "ilusionado", entra="nada", objeto="fajo", pose="sostiene", acciones=[
            {"at": "@Piz", "x": 800, "dur": 0.9}, {"at": "@24.500", "salta": True},
            {"at": "@IRPF", "objeto": None, "pose": "cabeza", "cara": "susto", "tiembla": True},
            {"at": "@1.630#2", "take": True, "cara": "confundido"}]),
        dict(type="efecto", efecto="vuelan", objeto="billete", n=7, x=820, y=1000, at="@IRPF", vida=1.8),
        rot("1.630 €", 260, 560, "@Total", 90, "verde", golpe=True),
        rot("24.500 € brutos", 700, 470, "@24.500", 70, "amarillo", golpe=True, out="@1.630#2"),
        rot("1.630 €", 800, 560, "@1.630#2", 90, "verde", golpe=True),
    ]),
    # 5 · GIRO: es a propósito
    dict(id="giro", fondo="rayos", animo="comico", musica="corte", trans="iris", footnote="Real Decreto 240/2026 (BOE 26/03/2026)", lines=[
        V("¿Un error? No: es a propósito.", "remate"),
        V("Desde marzo, al empezar a trabajar, los primeros 6.000 euros de sueldo no cuentan para el IMV. Y del resto, solo la mitad.", "normal", 0.25),
    ], camara=[plano(0, "general", dur=0), plano("@6.000", "medio", "profe", 0.3, aire=220)],
       elements=[
        pj("sarcastica", 800, 0, 0.72, "burla", id="sarcastica", entra="pop", acciones=[{"at": "@propósito", "take": True, "cara": "sorpresa"},
                                                                                       {"at": "@marzo", "sale": "der"}]),
        pj("profe", 300, "@propósito-0.2", 0.78, "serio", id="profe", entra="izq", pose="senala_arriba", acciones=[
            {"at": "@6.000", "pose": "senala", "cara": "normal"}, {"at": "@cuentan", "salta": True, "cara": "riendo"}, {"at": "@resto", "mira": "camara", "pose": "senala_arriba"}, {"at": "@mitad", "pose": "pulgar", "cara": "ilusionado"}]),
        rot("6.000 €: NO CUENTAN", 600, 480, "@6.000", 72, "amarillo", golpe=True),
        dict(type="efecto", efecto="pum", text="¡0 €!", x=760, y=820, at="@cuentan", scale=0.8, vida=0.8),
        rot("EL RESTO: SOLO LA MITAD", 600, 600, "@mitad", 64, "blanco", golpe=True),
    ]),
    # 6 · POR QUÉ
    dict(id="porque", fondo="oficina", animo="curioso", trans="pan", footnote="El IMV completa la renta hasta un mínimo garantizado", lines=[
        V("Sin esta regla, cada euro que ganas te quitaría un euro de ayuda. Y trabajar no compensaría.", "intriga"),
    ], camara=[plano(0, "general", dur=0), plano("@compensaría", "medio", "pizon", 0.3, aire=200)],
       elements=[
        quien("pizon", 300, 0, 0.78, "pensativo", entra="nada", acciones=[
            {"at": "@ganas", "pose": "sostiene", "objeto": "billete", "cara": "ilusionado"},
            {"at": "@quitaría", "objeto": None, "take": True, "cara": "susto"},
            {"at": "@compensaría", "cara": "triste", "pose": "caidos"}]),
        obj("billete", 760, 760, "@ganas", 0.9, entra="pop", acciones=[{"at": "@quitaría", "sale": "der"}]),
        rot("+1 € SUELDO", 600, 600, "@ganas", 90, "verde", golpe=True, out="@quitaría"),
        rot("-1 € AYUDA", 600, 600, "@quitaría", 90, C, golpe=True),
    ]),
    # 7 · PEGAS + FINAL
    dict(id="final", fondo="calle", animo="final", trans="iris", footnote="Solo si ya se cobraba el IMV · se revisa cada año", lines=[
        V("Ojo: solo vale si ya cobrabas el IMV, y se revisa cada año.", "normal"),
        V("¿Te parece justo? Te leemos. Y síguenos: la próxima, lo que cobra un diputado.", "energia", 0.15),
    ], camara=[plano(0, "general", dur=0), plano("@síguenos", "abierto", dur=0.4)],
       elements=[
        quien("pizon", 300, 0, 0.72, "normal", entra="nada", acciones=[{"at": "@Ojo", "pose": "senala_arriba", "cara": "serio"}, {"at": "@cobrabas", "mira": "piz"},
                                                                      {"at": "@justo", "mira": "camara", "cara": "pensativo"},
                                                                      {"at": "@síguenos", "pose": "saluda", "cara": "riendo"}]),
        quien("piz", 780, 0, 0.72, "normal", entra="nada", acciones=[{"at": "@cobrabas", "mira": "pizon", "cara": "pensativo"}, {"at": "@revisa", "tiembla": True, "cara": "preocupado"}, {"at": "@año", "pose": "encoge"},
                                                                    {"at": "@leemos", "pose": "senala", "cara": "ilusionado"},
                                                                    {"at": "@diputado", "salta": True, "cara": "sorpresa"}]),
        rot("SOLO SI YA COBRABAS EL IMV", 540, 470, "@Ojo", 64, "amarillo", golpe=True, out="@justo"),
        rot("¿JUSTO?", 540, 470, "@justo", 120, "amarillo", golpe=True, out="@síguenos"),
        rot("SÍGUENOS", 540, 470, "@síguenos", 110, "amarillo", fx=[{"at": "@diputado", "do": "latir"}]),
    ]),
]

SB = dict(base.SB)
SB.update(
    slug="compensa_cobrar", title="¿Compensa cobrar más?", series_tag="TU DINERO, CON DATOS",
    scenes=scenes, banda=True, music_volume=0.2, scribble_volume=0.0, sfx_volume=1.0, end_hold=0.9,
    portada={"t": 3.2, "titulo": "¿Compensa cobrar más?", "capitulo": None},
    sources=["SMI 2026: Real Decreto 126/2026 (BOE 19/02/2026)", "IMV: Real Decreto 240/2026 (BOE 26/03/2026)",
             "Cuantías IMV 2026: 733,60 €/mes un adulto"],
    caption=("💶 Pizón cobra el SMI. Piz, 7.000 € más al año. A final de mes: casi lo mismo\n"
             "🧾 SMI 2026: 1.221 € × 14 → unos 1.330 € netos al mes\n"
             "🤝 Si ya cobrabas el IMV y empiezas a trabajar, conservas parte: unos 300 €/mes\n"
             "📜 Desde marzo, los primeros 6.000 € de sueldo no cuentan y del resto, solo la mitad\n"
             "💬 ¿Te parece justo?\n"
             "➡️ Próximo: lo que cobra un diputado · 🔔 Síguenos · 📚 Fuentes en comentarios"),
    pinned_comment=("📚 Fuentes: SMI 2026 (RD 126/2026, BOE 19/02/2026) · IMV 2026 733,60 €/mes un adulto · incentivo al empleo "
                    "(RD 240/2026, BOE 26/03/2026). Cálculo propio y aproximado: cotización ≈ 6,5 %, escala general de IRPF; "
                    "el IMV que se conserva va de unos 270 a 400 €/mes según cómo se compute la renta. Solo si ya se cobraba el IMV. "
                    "¿Ves un error? Dínoslo."),
    hashtags=["#PizarraPública", "#SMI", "#IngresoMínimoVital", "#Sueldo", "#IRPF", "#TuDinero", "#Economía"],
)

if __name__ == "__main__":
    path = os.path.join(OUT, f"{SB['slug']}.json")
    json.dump(SB, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
