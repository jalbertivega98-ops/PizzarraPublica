# Pipeline whiteboard → Reel 1080×1920

Convierte un storyboard JSON en un MP4 vertical listo para Instagram: voz en español de España, dibujos que se trazan solos, texto letra a letra, subtítulos con palabra resaltada, música y sonido de rotulador.

```bash
pip install -r requirements.txt            # + ffmpeg; en Linux: apt-get install libegl1 libgl1
python3 make_video.py storyboards/reel01_presidente.json             # vídeo final (≈1,5 min de render en 4 CPU)
python3 make_video.py storyboards/reel01_presidente.json --preview   # borrador a 10 fps (≈40 s)
```

Salida en `../output/<slug>/`: `<slug>.mp4`, `<slug>.srt`, `<slug>_publicacion.txt` (texto + hashtags) y `<slug>_tiempos.json`.

## Archivos

| Archivo | Qué hace |
|---|---|
| `make_video.py` | Orquesta: voz (Piper) → línea de tiempo → fotogramas → audio → mezcla ffmpeg |
| `wb.py` | Motor de dibujo: paleta, fuentes, iconos, trazos con temblor de mano, rotulador, gráficos |
| `music.py` | Música de fondo y sonido de rotulador generados por código (sin licencias de terceros) |
| `storyboards/*.json` | Un archivo por vídeo |
| `voices/` | Voz Piper `es_ES-davefx-medium` (ver su MODEL_CARD) |
| `assets/fonts/` | Kalam, Patrick Hand, Caveat, Poppins (licencia OFL, incluida) |

## Formato del storyboard

Cada escena tiene `lines` (frases de narración; cada una se sintetiza por separado, así sabemos su tiempo exacto) y `elements` (lo que se dibuja).

- Una frase puede ser texto o `{"tts": "ciento setenta y seis", "text": "176"}` para que la voz lea una cosa y el subtítulo muestre otra.
- `at` decide cuándo empieza un elemento: `"L1"` (al empezar la frase 1), `"L1@0.5"` (a mitad de la frase 1), `"L1+0.3"`, `"+0"` (justo después del elemento anterior) o un número de segundos desde el inicio de la escena.
- `dur` es lo que tarda en dibujarse.
- Tipos: `text`, `icon` (`person`, `ballot_box`, `ballot`, `crown`, `bubble`, `lectern`, `document`, `clock`, `calendar`, `loop`, `question`, `handshake`), `arrow`, `line`, `rect`, `circle`, `cross`, `check`, `underline`, `highlight`, `hemicycle`, `bars`, `gauge`, `counter`.
- Colores: `ink`, `blue`, `red`, `yellow`, `green`, `gray`, `light`. Por neutralidad, los personajes políticos genéricos van en gris con corbata amarilla, nunca con colores de partido.
- Lienzo de 1080×1920. Zona útil para dibujos: y≈380–1380. Los subtítulos van en y≈1520 y la nota de fuente en y≈1395.

## Estilo «viva» (por defecto en todos los vídeos nuevos desde el 14/10/2026)

Estándar completo: [`../docs/enganche.md`](../docs/enganche.md). Ejemplo: `series/padres_viva.py`.
Se activa con `"estilo": "viva"` en el storyboard; los storyboards antiguos se renderizan igual que antes.

- **Frases** como `{"text": "...", "tono": "intriga|sorpresa|energia|remate|normal", "pausa": 0.5}`. La voz de ElevenLabs
  se genera con esos ajustes y con el tiempo de cada palabra (`voces_elevenlabs/<clave>.json`).
- **Anclas por palabra**: `"at": "@15,6"`, `"@euros#2"` (2.ª vez que se dice), `"@casa+0.2"`.
- **`fx`** en cualquier elemento: `[{"at": "@hoy", "do": "borrar"}]`; `do` = `tachar`, `rodear`, `subrayar`, `borrar`,
  `latir`, `temblar`, `mover` (con `x`, `y`, `scale`), `golpe`. `"golpe": true` en un elemento = aparece con impacto, zoom y sonido.
- **Personaje** `{"type": "tu", "x", "y", "scale", "etiqueta": "TÚ", "cara": "normal", "caras": [{"at": "@15", "cara": "susto"}]}`.
  Caras: `normal`, `sorpresa`, `susto`, `enfado`, `duda`, `risa`, `triste`, `vacio`. Los brazos acompañan a la cara.
  `{"type": "cara", ...}` pone ojos y boca a cualquier dibujo (una casa que se ríe).
- **Escena**: `"trans": "borrador|barrido|zoom|papel|corte"` (si no, rotan) y `"musica": "corte"` (silencio antes del giro).
- **Revisión**: `--maqueta` (sin voz, para montar antes de gastar ElevenLabs), `--ritmo` (solo el informe),
  `--hoja` (hoja de contactos). Cada render escribe `<slug>_ritmo.txt` con los avisos.

Voz: acción «Voces ElevenLabs» (`voces.yml`) en la rama, con `storyboards=storyboards/<slug>.json` y `motor=elevenlabs`.

## Limitaciones conocidas

- Los subtítulos se sincronizan exactamente por frase. Dentro de cada frase, el tiempo de cada palabra se estima por su número de letras.
- Piper no se puede escuchar desde aquí. Para revisar la voz se transcribió con Whisper, y las palabras que se entendían mal («investidura» pegada a otra frase, «pactos», «síes/noes») se reformularon.
- Aún no hay generación automática del storyboard: se escribe a mano o con un LLM (ver la propuesta técnica en `../entrega1.md`).
