#!/usr/bin/env python3
"""Voces de ElevenLabs para los storyboards (se ejecuta en GitHub Actions con el secreto ELEVENLABS_API_KEY).

Genera un MP3 por frase en voces_elevenlabs/<clave>.mp3, donde la clave depende de la voz, el modelo
y el texto. make_video.py usa esos archivos cuando el storyboard tiene "voice": {"engine": "elevenlabs"}.

  python3 tts_elevenlabs.py storyboards/impuestos_*.json --voice <voice_id>   # vídeos completos
  python3 tts_elevenlabs.py --muestras "texto de prueba"                      # una muestra por voz en voces_elevenlabs/muestras/
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "voces_elevenlabs")
API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"
# voces de la biblioteca básica de ElevenLabs que hablan español con el modelo multilingüe
MUESTRAS = {"George": "JBFqnCBsd6RMkjVDRZzb", "Brian": "nPczCjzI2devNBz1zQrb", "Daniel": "onwK4e9ZLuTAKqWW03F9",
            "Liam": "TX3LPaxmHKxFdv7VOQHJ", "Sarah": "EXAVITQu4vr4xnSDxMaL", "Alice": "Xb7hH8MSUJpSbSDYk0k2"}
SETTINGS = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}


def line_text(line):
    """ElevenLabs lee bien siglas y cifras: usa el texto del subtítulo, no la variante fonética de Piper."""
    return line["text"] if isinstance(line, dict) else line


def key(voice, model, text):
    return hashlib.sha1(f"{voice}|{model}|{text}".encode()).hexdigest()[:16]


def synth(text, voice, model, api_key):
    req = urllib.request.Request(
        f"{API}/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": model, "language_code": "es", "voice_settings": SETTINGS}).encode(),
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def voces_espanol(api_key):
    """Voces de la cuenta con acento de España (añadidas desde la biblioteca de voces)."""
    req = urllib.request.Request(f"{API}/voices", headers={"xi-api-key": api_key})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    out = {}
    for v in data.get("voices", []):
        labels = " ".join(str(x) for x in (v.get("labels") or {}).values()).lower()
        if v.get("category") != "premade" and re.search(r"spain|castilian|españa|peninsular|spanish", labels + v.get("name", "").lower()):
            out[v["name"]] = v["voice_id"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboards", nargs="*")
    ap.add_argument("--voice")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--muestras")
    a = ap.parse_args()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        sys.exit("Falta el secreto ELEVENLABS_API_KEY")

    if a.muestras:
        os.makedirs(os.path.join(CACHE, "muestras"), exist_ok=True)
        voces = {**MUESTRAS, **voces_espanol(api_key)}
        for name, vid in voces.items():
            path = os.path.join(CACHE, "muestras", re.sub(r"\W+", "_", name).strip("_") + ".mp3")
            open(path, "wb").write(synth(a.muestras, vid, a.model, api_key))
            print("→", os.path.relpath(path, HERE), vid)
        return

    files = [f for pat in a.storyboards for f in sorted(glob.glob(pat))]
    n = 0
    for f in files:
        story = json.load(open(f, encoding="utf-8"))
        voice = a.voice or story.get("voice", {}).get("voice_id")
        os.makedirs(CACHE, exist_ok=True)
        for sc in story["scenes"]:
            for line in sc["lines"]:
                text = line_text(line)
                path = os.path.join(CACHE, key(voice, a.model, text) + ".mp3")
                if not os.path.exists(path):
                    open(path, "wb").write(synth(text, voice, a.model, api_key))
                    n += len(text)
        print("✓", os.path.relpath(f, HERE))
    print(f"{n} caracteres enviados a ElevenLabs")


if __name__ == "__main__":
    main()
