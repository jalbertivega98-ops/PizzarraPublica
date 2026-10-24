# Motor v2 · «Los datos que incomodan»

Sustituye la plantilla de la mano que escribe despacio por animación con cámara, personajes y ritmo de TikTok.

```bash
pip install skia-python numpy        # + ffmpeg; en Linux: apt-get install libegl1 libgl1
python3 motor.py videos/bajas.py              # vídeo final 1080×1920 a 30 fps (≈1,5 min en 4 CPU)
python3 motor.py videos/bajas.py --hoja       # hoja de contactos: 1 fotograma por segundo para revisar el ritmo
python3 motor.py videos/bajas.py --portada    # portada
```

La voz (Álvaro, Microsoft) se genera en GitHub Actions: acción **Voces ElevenLabs** con `motor = v2` y
`storyboards = pipeline/v2/videos/*.py`. Guarda en `voces/` el MP3 de cada frase y el tiempo exacto de cada
palabra, que sincroniza subtítulos y animaciones. Sin voces, el motor usa tiempos estimados y silencio.

## Qué cambia respecto al motor v1

| v1 | v2 |
|---|---|
| Plano fijo, sin cámara | Cámara por plano: `golpe` (entra cerca y se aleja), `empuja`, `aleja`, `deriva`, `inclina`, `foco` (zoom a un punto); sacudida automática con cada impacto |
| Corte o fundido | Transiciones: `barrido` (whip con desenfoque), `sube`, `zoom`, `flash`, `tinta`, `corte` |
| Mano que dibuja despacio | Elementos que entran con rebote, caen, golpean o se trazan rápido; todo «respira» mientras está en pantalla |
| Subtítulo por frase | Subtítulos de 1-3 palabras, palabra activa resaltada, cifras en color; sincronizados palabra a palabra con la voz |
| Iconos sueltos | Personajes con caras (neutral, feliz, sorpresa, shock, enfado, duda, triste, nervioso, listo) y poses; hucha de la Seguridad Social |
| Música plana | Base tensa por tema, silencios estratégicos antes del giro (`pausa`), efectos: golpe, sello, contador, billetes, rotulador, subida, glitch |
| Misma plantilla | Fondo por plano (rayos, mancha, liso), color de acento por vídeo |

## Guion (`videos/*.py`)

Un vídeo es una lista de `planos` de 2-4 s. Cada plano: `voz` (frases; `{"tts", "text"}` si la voz debe leer
otra cosa que el subtítulo), `cam`, `trans`, `pausa`, `fuente` (etiqueta visible), `sfx` y `el` (elementos).

`at` marca cuándo aparece un elemento: `"@palabra"` (cuando la voz la dice), `"@palabra+0.2"`, `"L1"`,
número de segundos o `"fin-0.5"`. `hasta` lo retira.

Elementos (`k`): `num` (cifra con contador), `txt`, `sello`, `gente` (pictograma «1 de cada 10»), `barras`,
`linea`, `icono`, `pers` (personaje), `dinero` (billetes volando), `circulo`/`tacha`/`subraya`/`flecha`
(rotulador), `estallido`, `bocadillo`, `medidor` (prometido vs cumplido), `panel`, `burbujas`.

Zona útil: y≈230-1230 (los subtítulos van en 1400, por encima de los botones de TikTok/Reels).
Regla de neutralidad: personajes políticos siempre en gris con corbata amarilla; el color del partido solo en su nombre.

## Revisión antes de publicar

1. `--hoja` y comprobar que cada plano cambia algo en 2-3 s y que nada se sale del encuadre.
2. Escuchar: voz por encima de la música, golpes en las cifras, silencio antes del giro.
3. Cifras: cada una con fuente y año en la etiqueta y en el texto de publicación.
