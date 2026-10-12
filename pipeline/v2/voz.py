#!/usr/bin/env python3
"""Voz de Álvaro (Microsoft, edge-tts) con el tiempo exacto de cada palabra.

Se ejecuta en GitHub Actions (acción «Voces v2»), porque desde los contenedores de Claude
no se llega al servicio de Microsoft. Por cada frase de un vídeo guarda:
  voces/<clave>.mp3   el audio
  voces/<clave>.json  [{"w": palabra, "t": inicio_s, "d": duración_s}, ...]

  python3 voz.py videos/bajas.py videos/expulsiones.py
"""
import asyncio
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "voces")
VOZ = "es-ES-AlvaroNeural"
VELOCIDAD = "+12%"


def cargar_video(path):
    spec = importlib.util.spec_from_file_location("video_" + os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.VIDEO


def frases(video):
    for plano in video["planos"]:
        for linea in plano.get("voz", []):
            yield linea


def texto_tts(linea):
    return linea["tts"] if isinstance(linea, dict) else linea


def clave(texto, voz=VOZ, vel=VELOCIDAD):
    return hashlib.sha1(f"{voz}|{vel}|{texto}".encode()).hexdigest()[:16]


# Microsoft rechaza a veces la versión de navegador que declara edge-tts (403). Se prueban otras.
VERSIONES = [None, "150.0.3480.0", "149.0.3440.0", "148.0.3390.0", "147.0.3340.0", "146.0.3300.0", "145.0.3250.0", "144.0.3200.0"]


def usa_version(v):
    import edge_tts.communicate as C
    import edge_tts.constants as K
    if not hasattr(K, "_ORIG"):
        K._ORIG = K.CHROMIUM_FULL_VERSION
    v = v or K._ORIG
    m = v.split(".")[0]
    gec = f"1-{v}"
    for mod in (K, C):
        for nombre, val in (("CHROMIUM_FULL_VERSION", v), ("CHROMIUM_MAJOR_VERSION", m), ("SEC_MS_GEC_VERSION", gec)):
            if hasattr(mod, nombre):
                setattr(mod, nombre, val)
        for hd in ("WSS_HEADERS", "BASE_HEADERS"):
            h = getattr(mod, hd, None)
            if isinstance(h, dict) and "User-Agent" in h:
                h["User-Agent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   f"Chrome/{m}.0.0.0 Safari/537.36 Edg/{m}.0.0.0")


async def sintetizar(texto, voz=VOZ, vel=VELOCIDAD):
    import edge_tts

    com = edge_tts.Communicate(texto, voz, rate=vel, boundary="WordBoundary")
    audio, palabras = b"", []
    async for ch in com.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            palabras.append({"w": ch["text"], "t": ch["offset"] / 1e7, "d": ch["duration"] / 1e7})
    return audio, palabras


def main(paths):
    os.makedirs(CACHE, exist_ok=True)
    nuevas = 0
    for p in paths:
        video = cargar_video(p)
        voz = video.get("voz", VOZ)
        vel = video.get("velocidad", VELOCIDAD)
        for linea in frases(video):
            txt = texto_tts(linea)
            k = clave(txt, voz, vel)
            mp3, js = os.path.join(CACHE, k + ".mp3"), os.path.join(CACHE, k + ".json")
            if os.path.exists(mp3) and os.path.exists(js):
                continue
            audio = None
            for intento in range(len(VERSIONES) + 3):
                try:
                    audio, palabras = asyncio.run(sintetizar(txt, voz, vel))
                    break
                except Exception as e:  # el servicio a veces corta la conexión o rechaza la versión
                    print("reintento", intento, e)
                    if "403" in str(e) and intento + 1 < len(VERSIONES):
                        usa_version(VERSIONES[intento + 1])
                        print("  probando versión", VERSIONES[intento + 1])
            if audio is None:
                sys.exit("No se pudo generar la voz")
            open(mp3, "wb").write(audio)
            json.dump(palabras, open(js, "w", encoding="utf-8"), ensure_ascii=False)
            nuevas += 1
            print("✓", txt[:70])
    print(f"{nuevas} frases nuevas")


if __name__ == "__main__":
    main(sys.argv[1:])
