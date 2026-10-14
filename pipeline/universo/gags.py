"""Plantillas de situaciones cómicas reutilizables (devuelven elementos y acciones para el storyboard).

Cada gag explica un dato: el humor ayuda a entenderlo, nunca cambia la cifra.
  cae_del_cielo     un precio gigante cae del cielo y aplasta al personaje (¡CHOF!), luego rebota a su sitio
  aparece_hacienda  la pizarra de Hacienda entra corriendo con una factura (¡KA-CHING!)
  lupa_letra_pequena  un banquero lee con lupa la letra pequeña del contrato
  casa_se_aleja     la casa sale corriendo cada vez que el personaje se acerca
  persecucion       un objeto con piernas (p. ej. el contrato de alquiler) persigue al personaje
  dinero_vuela      los billetes salen volando de la hucha
"""

SUELO = 1340


def _mas(at, dt):
    """'@palabra' + dt segundos (sin desplazamiento previo)."""
    import re
    if isinstance(at, (int, float)):
        return at + dt
    m = re.fullmatch(r"(@.+?(?:#\d+)?)([+-]\d*\.?\d+)?", at)
    return f"{m.group(1)}{float(m.group(2) or 0) + dt:+.2f}"


def cae_del_cielo(texto, at, x, y_final, victima=None, scale=1.3, color="amarillo", onomatopeya="¡CHOF!"):
    """Devuelve (elementos, acciones_para_la_victima). La etiqueta tarda 0,9 s en caer (aterriza a +0,63 s)."""
    llega = _mas(at, 0.63)
    els = [
        dict(type="objeto", objeto="etiqueta", id="precio_cae", x=x, y=SUELO - 300, scale=scale, at=at, dur=0.9,
             entra="cae", props={"texto": texto, "color": color}, rot=-3,
             acciones=[{"at": llega, "y": SUELO - 110, "dur": 0.06},
                       {"at": _mas(at, 1.25), "y": y_final, "x": x + 40, "dur": 0.45}]),
        dict(type="efecto", efecto="pum", text=onomatopeya, x=x + 120, y=SUELO - 330, at=llega, scale=0.9, vida=0.8),
    ]
    acc = [{"at": _mas(at, 0.15), "mira": "arriba", "cara": "susto"}, {"at": llega, "aplasta": True},
           {"at": _mas(at, 1.3), "cara": "confundido", "mira": None}]
    return els, acc


def aparece_hacienda(at, x, factura="IMPUESTOS", desde="der", scale=0.82):
    return dict(type="personaje", quien="hacienda", id="hacienda", x=x, y=SUELO, scale=scale, at=at, entra=desde,
                dur=0.4, cara="burla", pose="sostiene", objeto={"tipo": "contrato", "titulo": factura, "hojas": 1},
                sfx="kaching", acciones=[{"at": _mas(at, 0.45), "salta": True}])


def lupa_letra_pequena(at, x, y, clausula, quien_id=None, scale=1.0):
    """Contrato gigante + lupa que pasa por encima + la cláusula ampliada."""
    return [
        dict(type="objeto", objeto="contrato", id="contrato", x=x, y=y, scale=1.25 * scale, at=at, entra="pop",
             props={"titulo": "HIPOTECA", "hojas": 2}, sfx="papel"),
        dict(type="objeto", objeto="lupa", id="lupa", x=x - 180, y=y - 120, scale=0.9 * scale, at=_mas(at, 0.3),
             entra="izq", acciones=[{"at": _mas(at, 0.8), "x": x + 40, "y": y + 40, "dur": 0.8}]),
        dict(type="rotulo", text=clausula, x=540, y=1240, size=64, color="blanco", at=_mas(at, 1.0), hud=True),
    ]


def casa_se_aleja(casa_id, saltos):
    """saltos = [(at, x_nueva)]: la casa sale corriendo con sus piernas hasta x_nueva."""
    return [{"at": at, "x": x, "corre": True, "cara": "riendo"} for at, x in saltos]


def persecucion(at, objetivo, objeto="contrato", props=None, x=-300, scale=0.7, offset=-330, cara="enfado", id="persigue"):
    return dict(type="objeto", objeto=objeto, id=id, x=x, y=SUELO - 290 * scale, scale=scale, at=at, entra="nada",
                props=props or {}, piernas=True, cara=cara,
                acciones=[{"at": at, "sigue": objetivo, "offset": offset, "lag": 0.35}])


def dinero_vuela(at, x, y, n=7):
    return dict(type="efecto", efecto="vuelan", objeto="billete", n=n, x=x, y=y, at=at, vida=1.8)
