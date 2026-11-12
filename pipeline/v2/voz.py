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
            for intento in range(4):
                try:
                    audio, palabras = asyncio.run(sintetizar(txt, voz, vel))
                    break
                except Exception as e:  # el servicio a veces corta la conexión
                    print("reintento", intento, e)
            open(mp3, "wb").write(audio)
            json.dump(palabras, open(js, "w", encoding="utf-8"), ensure_ascii=False)
            nuevas += 1
            print("✓", txt[:70])
    print(f"{nuevas} frases nuevas")


if __name__ == "__main__":
    main(sys.argv[1:])
