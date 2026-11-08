#!/usr/bin/env python3
"""Rellena los huecos de ritmo de un storyboard con pequeños movimientos de cámara (sin tocar el guion).

Uso: python3 rellenar_ritmo.py storyboards/<slug>.json [--max 2.5]
Para cada tramo sin cambios visuales de más de --max segundos (según el informe de ritmo de make_video.py), añade en
la escena un plano que repite el encuadre vigente con un zoom un 5 % distinto (alternando acercar y alejar). En los
mapas mantiene el punto de mira del último plano, así que no se pierde el encuadre geográfico.
Necesita las voces ya generadas (usa la misma caché que make_video.py).
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_video as mv  # noqa: E402
import viva  # noqa: E402


def eventos(story, scenes, elements):
    ev = []
    for sc, els in zip(scenes, elements):
        ev.append(sc["start"])
        for e in els:
            ev.append(e.t0)
            ev += [ch["t"] for ch in getattr(e, "cambios", [])]
            ev += [t0 for t0, d, f in e.fx]
        ev += [x["t"] for x in sc.get("camara", [])]
        ev += [x["t"] for x in sc.get("luz", [])]
    return sorted(ev)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--max", type=float, default=2.5)
    args = ap.parse_args()
    story = json.load(open(args.storyboard, encoding="utf-8"))
    work = os.path.join(HERE, "..", "output", story["slug"], "_work")
    os.makedirs(work, exist_ok=True)
    audio, sr = mv.tts_lines(story, work, False)
    for vuelta in range(4):
        sb = json.loads(json.dumps(story))
        scenes, clips, total = mv.build_timeline(sb, audio, sr)
        total += sb.get("end_hold", 1.2)
        scenes[-1]["end"] = total
        elements = mv.build_elements(sb, scenes)
        tiempos = eventos(sb, scenes, elements) + [total - sb.get("end_hold", 1.2)]
        huecos = [(a, b) for a, b in zip(tiempos[:-1], tiempos[1:]) if b - a > args.max]
        if not huecos:
            break
        for a, b in huecos:
            n = int((b - a) // args.max)
            for k in range(1, n + 1):
                t = a + (b - a) * k / (n + 1)
                si = max(i for i, s in enumerate(scenes) if s["start"] <= t)
                tl, spec = scenes[si], story["scenes"][si]
                previos = [x for x in tl.get("camara", []) if x["t"] <= t]
                base = dict(previos[-1]) if previos else {"plano": "general", "sobre": [540, 960], "zoom": 1.0}
                z = base.get("zoom", 1.0)
                nuevo = {"at": round(t - tl["start"], 2), "plano": base.get("plano", "general"), "sobre": base.get("sobre"),
                         "dur": 0.6, "zoom": round(z * (0.95 if (len(previos) % 2) else 1.05), 3)}
                if nuevo["sobre"] is None:
                    nuevo["sobre"] = [540, 960]
                for clave in ("aire",):
                    if clave in base:
                        nuevo[clave] = base[clave]
                spec.setdefault("camara", []).append(nuevo)
        print(f"   vuelta {vuelta + 1}: {len(huecos)} huecos rellenados")
    json.dump(story, open(args.storyboard, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sb = json.loads(json.dumps(story))
    scenes, clips, total = mv.build_timeline(sb, audio, sr)
    total += sb.get("end_hold", 1.2)
    scenes[-1]["end"] = total
    resumen, avisos = viva.informe_ritmo(sb, scenes, mv.build_elements(sb, scenes), total)
    print("   " + resumen + "".join("\n   ⚠ " + a for a in avisos))


if __name__ == "__main__":
    main()
