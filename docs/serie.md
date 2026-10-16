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

## 8. Portada estándar (todas iguales)

Fotograma del momento más visual arriba y franja oscura fija abajo con la pastilla roja «CAPÍTULO N», el título en dos líneas
amarillas y @pizarrapublica (dentro del recorte 4:5 de Instagram). En el storyboard:
`"portada": {"t": <segundo del fotograma>, "titulo": "...", "capitulo": N}`. `make_video.py` la crea sola al terminar
(`videos/<slug>/portada_<slug>.png`); para rehacerla sin renderizar: `python3 portada.py storyboards/<slug>.json`.

## 9. Limitaciones reales

- Animación procedural (marionetas vectoriales con brazos de manguera, estirar y aplastar), no dibujo fotograma a fotograma.
- El giro de tres cuartos desplaza la cara; no hay perfil dibujado de verdad.
- Música y efectos sintetizados: suenan a dibujo animado sencillo, no a orquesta ni a librería profesional.
- Una sola voz (narrador). Para que Piz hable con voz propia hace falta una segunda voz de ElevenLabs.
- El arte vectorial es más limpio y menos texturizado que las ilustraciones de referencia.
- Render: unos 4 minutos por minuto de vídeo.

## 10. Mundo dibujado (desde el 15/10/2026, norma para todos los vídeos)

Los personajes siguen siendo protagonistas, pero ahora **viven en un mundo dibujado a mano** que cuenta la historia:
mapas que se trazan con rotulador, mares y barcos con estela, ciudades con murallas, banderas, tratados que se despliegan.
Episodios: `pipeline/series/ceuta_otan.py` y los cinco del 16/10 (`voto_nietos`, `coste_29n`, `cis_acierta`, `leyes_mueren`, `ceuta_marruecos`, ayudas en `series/_mundo.py`; guiones en `docs/series/cinco_mundo/`). Referencia: → «Si atacan Ceuta, ¿viene la OTAN?» (guion y fuentes en `docs/series/ceuta_otan/`).

**Reglas**: no repetir composición; cambiar de escenario cuando avanza la historia; cámara que se mueve con motivo;
los dibujos se **dibujan** (no aparecen sin más); humor y emoción con los personajes; continuidad entre escenas;
mapas geográficamente correctos; historia visual antes que pantallas de texto; recursos reutilizables; 9:16 y unos 60 s;
ninguna escena quieta más de 3 s. Datos históricos, jurídicos y de actualidad comprobados; lo discutido nunca como confirmado
(sellos `CONFIRMADO` / `DECLARACIÓN` / `SIN CONFIRMAR`).

| Pieza | Uso en el storyboard |
|---|---|
| `mapa` (objeto) | `props: region (estrecho, atlantico, espana: 52 provincias con Canarias en recuadro y colores por comunidad, mundo: países por ISO3), orden, colores, resalta, apaga, lineas, tropico, ambito6`; se traza en `dibujo` s. Contornos reales de Natural Earth (`universo/geo/`, nuevas regiones con `geo/preparar.py`). Líneas siempre del mismo grosor aunque la cámara haga zoom x10. |
| `mapas.punto(region, lon, lat, x, y, escala)` | coloca barcos, personajes, banderas y rótulos en su sitio real del mapa |
| `barco` | buque de perfil que se mece; al navegar (`acciones` con `x`, `dur`) deja estela y espuma. `props: bandera, numero, rumbo` |
| `bandera`, `chincheta` | ondean: `espana`, `marruecos`, `otan`, `ue`, `ceuta`, `portugal`, `castilla`, `argentina`, `uruguay`, `cuba`, `mexico`, `venezuela`, `brasil`, `onu` |
| `documento` | pergamino que se despliega; `articulos` y `resalta` (fosforito que se pinta) |
| `otan`, `atril`, `sello`, `prismaticos`, `faro`, `barquito` | símbolo de la OTAN, atril de partido, sello de verificación, prismáticos (pose `prismaticos`) |
| objetos cívicos (`universo/civico.py`) | `urna` (llena), `papeleta`, `mesa_electoral`, `camion` (rueda y echa humo), `senal` (tachada), `alcoholimetro`, `contador` (corre hasta el valor), `barras` (crecen; colores de partido), `bola`, `lapida`, `papelera`, `libro`, `pasaporte`, `maleta`, `carabela` (cruz portugal/castilla), `corona`, `pergamino` |
| fondos `carretera` (en perspectiva, `velocidad`), `colegio` (colegio electoral) | escenas de tráfico y de votación |
| fondos `ceuta`, `mar_mapa` | paseo junto a las Murallas Reales con el Monte Hacho y la península al fondo; mar infinito bajo los mapas |
| `"dibuja": s` en cualquier elemento | el rotulador lo traza de izquierda a derecha (con sonido) |
| acción `brinco` | `{"x", "y", "dur", "brinco": alto}`: salto en arco (p. ej. cruzar el Estrecho) |
| escena `"limites"` | hasta dónde puede ir la cámara (en los mapas, muy lejos); zoom grande = interpolación logarítmica |
