#!/usr/bin/env python3
"""Genera la narración de cada episodio con edge-tts (se ejecuta en GitHub Actions).
uso: python3 terror/voz.py terror/guiones/ep00.json  -> terror/voz/<ep>/<id>.mp3"""
import asyncio, json, os, sys
import edge_tts

async def main(path):
    g = json.load(open(path)); out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(path))), 'voz', g['ep'])
    os.makedirs(out, exist_ok=True)
    for f in g['frases']:
        v = f.get('voz', g['voz']); rate = f.get('rate', g.get('rate', '+0%')); pitch = f.get('pitch', g.get('pitch', '+0Hz'))
        dst = os.path.join(out, f['id'] + '.mp3')
        await edge_tts.Communicate(f['t'], v, rate=rate, pitch=pitch).save(dst); print('ok', dst)

for p in sys.argv[1:]: asyncio.run(main(p))
