#!/usr/bin/env python3
"""Prepara los contornos geográficos de los mapas dibujados (universo/mapas.py).

Fuente: Natural Earth (dominio público), https://www.naturalearthdata.com
  10m admin_0_map_subunits (estrecho: España, Ceuta, Melilla, Gibraltar, Marruecos…) y 50m admin_0_countries (atlántico).
Los contornos se simplifican (Douglas-Peucker) y se guardan en geo/<region>.json. Solo hay que volver a
ejecutarlo para añadir regiones: python3 universo/geo/preparar.py <carpeta con los .geojson>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OTAN = {"ALB", "BEL", "BGR", "CAN", "HRV", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "ISL", "ITA", "LVA",
        "LTU", "LUX", "MNE", "NLD", "MKD", "NOR", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE", "TUR", "GBR", "USA", "GRL"}


CAN_DX, CAN_DY = 5.6, 6.9  # Canarias en recuadro, al suroeste de la península
REG = {"Canary Is.": "Canarias", "Foral de Navarra": "Navarra", "Valenciana": "Comunitat Valenciana",
       "Islas Baleares": "Illes Balears"}


def dp(pts, tol):
    if len(pts) < 5 or tol <= 0:
        return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    n = (dx * dx + dy * dy) ** 0.5 or 1e-12
    dmax, idx = 0.0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x1 * y0 - y1 * x0) / n
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        return dp(pts[:idx + 1], tol)[:-1] + dp(pts[idx:], tol)
    return [pts[0], pts[-1]]


def anillo(r, tol):
    mid = len(r) // 2  # partir en dos para que el anillo cerrado no colapse
    out = dp(r[:mid + 1], tol)[:-1] + dp(r[mid:], tol)
    return [[round(x, 4), round(y, 4)] for x, y in out]


def region(fichero, bbox, tol, clave, nombre_de, min_pts=4):
    d = json.load(open(fichero))
    x0, y0, x1, y1 = bbox
    feats = []
    for f in d["features"]:
        p = f["properties"]
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        out = []
        for pl in polys:
            ext = pl[0]
            if not any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in ext):
                continue
            a = anillo(ext, tol)
            if len(a) >= min_pts:
                out.append(a)
        if out:
            feats.append({"id": nombre_de(p), "iso": p.get(clave), "polys": out})
    return feats


def main(src):
    sub = os.path.join(src, "ne_10m_admin_0_map_subunits.geojson")
    cou = os.path.join(src, "ne_50m_admin_0_countries.geojson")
    est = region(sub, (-11, 32.5, 6.5, 45), 0.006, "ADM0_A3", lambda p: p["SUBUNIT"])
    json.dump({"fuente": "Natural Earth 10m map subunits (dominio público)", "lat0": 37.0, "rasgos": est},
              open(os.path.join(HERE, "estrecho.json"), "w"), separators=(",", ":"))
    atl = region(cou, (-180, -5, 60, 84), 0.12, "ADM0_A3", lambda p: p["ADM0_A3"])
    for f in atl:
        f["otan"] = f["iso"] in OTAN
    # Ceuta y Melilla aparte (en el mapa del tratado se ven fuera del ámbito del artículo 6)
    for f in region(sub, (-6, 35, -2.8, 36.2), 0, "ADM0_A3", lambda p: p["SUBUNIT"]):
        if f["id"] in ("Ceuta", "Melilla"):
            atl.append({**f, "otan": True})
    json.dump({"fuente": "Natural Earth 50m admin 0 countries (dominio público)", "lat0": 40.0, "rasgos": atl},
              open(os.path.join(HERE, "atlantico.json"), "w"), separators=(",", ":"))
    # España por provincias (las 52 circunscripciones), con Canarias en recuadro y los vecinos alrededor
    pro = os.path.join(src, "ne_10m_admin_1_states_provinces.geojson")
    esp = []
    for f in json.load(open(pro))["features"]:
        p = f["properties"]
        if p["adm0_a3"] != "ESP":
            continue
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        canarias = p["region"] == "Canary Is."
        out = []
        for pl in polys:
            ext = pl[0]
            if canarias:  # recuadro: se acercan a la península (desplazamiento fijo, se dibuja un marco)
                ext = [[x + CAN_DX, y + CAN_DY] for x, y in ext]
            a = anillo(ext, 0.008)
            if len(a) >= 4:
                out.append(a)
        if out:
            esp.append({"id": p["name"], "grupo": REG.get(p["region"], p["region"]), "polys": out, "espana": True})
    for f in region(sub, (-10.5, 34.6, 4.6, 44.2), 0.01, "ADM0_A3", lambda p: p["SUBUNIT"]):
        if f["id"] in ("Portugal", "France", "Andorra", "Morocco", "Gibraltar", "Algeria"):
            esp.append(f)
    json.dump({"fuente": "Natural Earth 10m admin 1 (dominio público)", "lat0": 40.0,
               "canarias": [CAN_DX, CAN_DY], "rasgos": esp},
              open(os.path.join(HERE, "espana.json"), "w"), separators=(",", ":"))
    # el mundo entero (para viajes largos: España, América, África…)
    mun = region(cou, (-180, -60, 180, 84), 0.15, "ADM0_A3", lambda p: p["ADM0_A3"])
    json.dump({"fuente": "Natural Earth 50m admin 0 countries (dominio público)", "lat0": 0.0, "rasgos": mun},
              open(os.path.join(HERE, "mundo.json"), "w"), separators=(",", ":"))
    for n in ("estrecho", "atlantico", "espana", "mundo"):
        print(n, os.path.getsize(os.path.join(HERE, n + ".json")) // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
