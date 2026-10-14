# Pizarra Pública como serie animada · motor de producción (desde el 14/10/2026)

Cada vídeo es **un episodio**: Piz quiere algo, los datos son los obstáculos que le pasan, hay un giro y el final
deja una razón para volver («Síguenos para ver si Piz lo consigue»). Se apoya en la identidad
([identidad/README.md](identidad/README.md)) y en el estándar de enganche ([enganche.md](enganche.md)).
Episodio de referencia: `pipeline/series/compra2026_serie.py` → «Piz y la casa imposible».

## 1. Reglas de dirección

- **Nada arbitrario**: cada movimiento de cámara, gag o cambio de luz aporta información, humor, emoción o curiosidad.
  Si no, no se pone. Mejor una escena quieta con una cara expresiva que tres zooms sin motivo.
- **El dato le pasa al personaje**: el precio le cae encima, Hacienda entra con la factura, la casa sale corriendo cuando sube.
- **2-3 gags por vídeo como mínimo**, siempre al servicio de la cifra. Nunca parodia de personas reales ni de partidos, nunca cambia un dato.
- **Personajes de lado y en movimiento**: entran andando, corren, se giran, miran a otros personajes. No siempre centrados mirando a cámara.
- **Los datos van en el HUD** (`"hud": true`): se quedan fijos en pantalla aunque la cámara se mueva por el mundo.
- **CTA dentro de la historia**: Piz pide ayuda o anuncia el próximo capítulo; nunca una pantalla publicitaria suelta al final.
- **Un dato fuerte = una reacción física** (take, aplastado, tropiezo, tiembla) con su efecto de sonido.

## 2. Acciones de personaje (`acciones` / `caras`)

| Clave | Qué hace |
|---|---|
| `x`, `y`, `dur` | anda hasta ahí (brazos y piernas en balanceo, inclinación, polvo); `"corre": true` = carrera con zancada larga |
| `sigue: id`, `offset`, `lag` | persigue a otro elemento (p. ej. el contrato de alquiler persigue a Piz) |
| `salta` | anticipación, arco y aterrizaje con aplastamiento |
| `take` | «toma» cartoon: se estira, los ojos se le salen (silbato que sube) |
| `aplasta` | queda aplastado y rebota (¡CHOF!) |
| `tropieza` | cae de bruces, estrellitas en la cabeza y se levanta |
| `gira` (+`flip`) | se da la vuelta |
| `tiembla` | tiembla de miedo |
| `cara`, `pose`, `mira` | expresión, brazos (`anda1/2`, `corre1/2`, `cae`, `empuja`, `ruega`, …) y mirada (izq/der/arriba/abajo/camara o el id de otro elemento) |

Entradas: `pop`, `crece`, `izq`, `der`, `cae` (con estirado y aplastado al aterrizar), `abajo`. Salidas: `izq`, `der`, `abajo`, `arriba`, `pop`.
En reposo los personajes respiran y se balancean. Edificios y objetos aceptan `"piernas": true` y `cara`.

## 3. Cámara, luz y transiciones (por escena)

- `"camara": [{"at", "plano": general|abierto|medio|primero|detalle, "sobre": id o [x, y], "dur", "aire", "inclina"}]`.
  El primer plano de un personaje encuadra su cara; la cámara nunca sale del decorado.
- **Parallax** automático en los fondos (cielo, ciudad, árboles y suelo a distintas profundidades), con pájaros, coches, autobús, nubes, lámparas y cortinas animadas.
- `"luz": [{"at", "tipo": normal|oscuro|noche|foco|alarma|atardecer, "sobre": id, "r"}]` (fundido de 0,3 s).
- `"trans"`: `borrador`, `barrido`, `zoom`, `papel`, `corte`, `iris` (cierre circular de dibujo animado), `pan` (la cámara viaja a la escena siguiente).

## 4. Efectos (`"type": "efecto"`)

`pum` (estallido con onomatopeya), `estrellas`, `lineas` (de velocidad), `flash`, `polvo`, `lluvia` (monedas u objetos que caen con gravedad y rebotan),
`vuelan` (billetes que se escapan de la hucha).

## 5. Plantillas de gag (`pipeline/universo/gags.py`)

`cae_del_cielo` (un precio gigante aplasta al personaje), `aparece_hacienda` (entra con la factura, ¡ka-ching!),
`lupa_letra_pequena` (banquero leyendo la letra pequeña con lupa), `casa_se_aleja` (la casa con piernas huye),
`persecucion` (un objeto con piernas persigue al personaje), `dinero_vuela`.

## 6. Sonido

- **Banda sonora por momentos** (`"banda": true` en el storyboard; `"animo"` por escena): curioso, alegre, comico, tension, triste, final.
  `"musica": "corte"` = silencio dramático. Todo en la misma tonalidad para que los fundidos suenen naturales.
  La música baja sola cuando habla la voz (`"ducking"`, 0,6 por defecto).
- **Efectos automáticos**: pasos y carrera, golpes, aplastado, tropiezo, silbatos de sorpresa y de caída, monedas, calculadora, caja registradora,
  estrellitas, papel, iris y whoosh. Salen de las acciones; `"sfx"` en un elemento añade uno concreto (`puerta`, `redoble`, `scratch`, …).
- Todo se genera por código (sin licencias). Si se quiere más calidad: efectos y música de ElevenLabs (gasta créditos) o librerías CC0.

## 7. Flujo

1. Guion como episodio (objetivo, problema, obstáculos crecientes, giro, conclusión, próximo capítulo) con fuentes.
2. `python3 series/<episodio>.py` → storyboard. `python3 make_video.py storyboards/<slug>.json --maqueta --preview` para revisar encuadres sin voz.
3. Voz: workflow `voces.yml` (ElevenLabs «Pizarra Pública»).
4. `--ritmo` con la voz real: ningún hueco de más de 2,5 s; si lo hay, se rellena con una reacción que signifique algo.
5. Render final y revisión de fotogramas y volúmenes.

## 8. Limitaciones reales

- Animación procedural (marionetas vectoriales con brazos de manguera, estirar y aplastar), no dibujo fotograma a fotograma.
- El giro de tres cuartos desplaza la cara; no hay perfil dibujado de verdad.
- Música y efectos sintetizados: suenan a dibujo animado sencillo, no a orquesta ni a librería profesional.
- Una sola voz (narrador). Para que Piz hable con voz propia hace falta una segunda voz de ElevenLabs.
- El arte vectorial es más limpio y menos texturizado que las ilustraciones de referencia.
- Render: unos 4 minutos por minuto de vídeo.
