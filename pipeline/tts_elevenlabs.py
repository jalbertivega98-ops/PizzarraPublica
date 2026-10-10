#!/usr/bin/env python3
"""Voces de ElevenLabs para los storyboards (se ejecuta en GitHub Actions con el secreto ELEVENLABS_API_KEY).

Genera un MP3 por frase en voces_elevenlabs/<clave>.mp3, donde la clave depende de la voz, el modelo
y el texto. make_video.py usa esos archivos cuando el storyboard tiene "voice": {"engine": "elevenlabs"}.

  python3 tts_elevenlabs.py storyboards/impuestos_*.json --voice <voice_id>   # vídeos completos
  python3 tts_elevenlabs.py --muestras "texto de prueba"                      # una muestra por voz en voces_elevenlabs/muestras/
  python3 tts_elevenlabs.py --muestras "texto" --biblioteca 8                 # voces de España de la biblioteca en muestras_es/
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
import urllib.error
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


def get_json(url, api_key, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"xi-api-key": api_key, "Content-Type": "application/json"},
                                 method="POST" if data is not None else "GET")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"{}")


def biblioteca(texto, n, model, api_key):
    """Busca en la biblioteca pública voces con acento de España, las añade a la cuenta y genera una muestra de cada una."""
    out_dir = os.path.join(CACHE, "muestras_es")
    os.makedirs(out_dir, exist_ok=True)
    vistas, cands = set(), []
    for q in ("language=es&accent=peninsular", "language=es&locale=es-ES", "language=es&search=spain", "language=es&search=castellano"):
        try:
            data = get_json(f"{API}/shared-voices?page_size=100&sort=cloned_by_count&{q}", api_key)
        except urllib.error.HTTPError as e:
            print(f"shared-voices {q}: HTTP {e.code} {e.read().decode()[:300]}")
            continue
        for v in data.get("voices", []):
            txt = " ".join(str(v.get(k) or "") for k in ("accent", "locale", "description", "name")).lower()
            if v["voice_id"] in vistas or not re.search(r"peninsular|castilian|es-es|spain|españa|castellano|madrid|españ", txt):
                continue
            if re.search(r"latin|mexic|argentin|colombi|venezol|chile|peru|caribe", txt):
                continue
            vistas.add(v["voice_id"])
            cands.append(v)
    cands.sort(key=lambda v: -(v.get("cloned_by_count") or 0))
    # mitad hombres, mitad mujeres
    elegidas = [v for v in cands if v.get("gender") == "male"][: (n + 1) // 2] + [v for v in cands if v.get("gender") == "female"][: n // 2]
    resumen = []
    for v in elegidas:
        name = re.sub(r"\W+", "_", v.get("name", v["voice_id"])).strip("_")[:40]
        info = {k: v.get(k) for k in ("name", "voice_id", "public_owner_id", "gender", "age", "accent", "locale",
                                     "description", "use_case", "cloned_by_count", "preview_url")}
        vid = v["voice_id"]
        try:
            added = get_json(f"{API}/voices/add/{v['public_owner_id']}/{v['voice_id']}", api_key, {"new_name": v.get("name", "es")})
            vid = added.get("voice_id", vid)
        except urllib.error.HTTPError as e:
            info["error_add"] = f"HTTP {e.code} {e.read().decode()[:300]}"
        info["voice_id_cuenta"] = vid
        try:
            open(os.path.join(out_dir, name + ".mp3"), "wb").write(synth(texto, vid, model, api_key, salir=False))
            info["muestra"] = f"voces_elevenlabs/muestras_es/{name}.mp3"
        except urllib.error.HTTPError as e:
            info["error_tts"] = f"HTTP {e.code} {e.read().decode()[:300]}"
        print(json.dumps(info, ensure_ascii=False))
        resumen.append(info)
    json.dump({"candidatas": len(cands), "voces": resumen}, open(os.path.join(out_dir, "voces.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


def synth(text, voice, model, api_key, salir=True):
    req = urllib.request.Request(
        f"{API}/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps({"text": text, "model_id": model, "language_code": "es", "voice_settings": SETTINGS}).encode(),
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if not salir:
            raise
        sys.exit(f"ElevenLabs respondió HTTP {e.code}: {e.read().decode()[:500]}")


def voces_espanol(api_key):
    """Voces de la cuenta con acento de España (añadidas desde la biblioteca de voces)."""
    req = urllib.request.Request(f"{API}/voices", headers={"xi-api-key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:  # la clave puede no tener permiso de lectura de voces
        print(f"No se pudieron listar las voces de la cuenta (HTTP {e.code}): {e.read().decode()[:300]}")
        return {}
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
    ap.add_argument("--biblioteca", type=int, default=0, help="con --muestras: probar N voces de España de la biblioteca")
    a = ap.parse_args()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        sys.exit("Falta el secreto ELEVENLABS_API_KEY")

    if a.muestras and a.biblioteca:
        return biblioteca(a.muestras, a.biblioteca, a.model, api_key)
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
