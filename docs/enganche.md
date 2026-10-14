# Pizarra Pública · Estándar de enganche (desde el 14/10/2026)

Se aplica por defecto a **todos** los vídeos nuevos del motor de pizarra (`pipeline/make_video.py`).
El motor avisa (informe `_ritmo.txt`) cuando un vídeo no lo cumple.

## 1. Qué hace el vídeo de referencia (Economía Ilustrada, «Así es comprar una casa con hipoteca»)

YouTube bloquea la descarga desde nuestras máquinas, así que se analizó con la transcripción, la portada y
fotogramas sueltos. Lo que lo hace adictivo no es el dibujo «bonito», es cómo cuenta:

| Recurso | Cómo lo usa | Qué copiamos (la técnica, no el contenido) |
|---|---|---|
| **Protagonista** | Todo le pasa a él (y a su pareja): el piso con fallos, el regateo, el banco. | Un personaje fijo: **«TÚ»**, un monigote a lápiz al que le pasan los datos (paga, se sorprende, suda). |
| **Cosas con cara** | Los bancos son triángulos de colores con ojos que compiten. | Hacienda, el banco, la casa o el sueldo pueden tener **dos ojos y una boca** a lápiz y reaccionar. |
| **Bucles abiertos** | «Y ahí empieza a correr el reloj», «aquí viene el momento crítico», «dun, dun». | Cada 6-8 s una frase que **promete** lo siguiente sin contarlo. |
| **Preguntas** | Unas 5 preguntas retóricas («¿cómo no lo vimos?»). | 2-3 preguntas por vídeo; la respuesta llega **después** de una pausa. |
| **Humor e ironía** | Exageración y autocrítica («deuda hasta el infinito»). | Un guiño irónico por vídeo, nunca contra un votante. |
| **Analogías** | Wallapop, «el jefe final», «saltar al vacío». | Cada cifra grande se traduce a algo físico (años de sueldo, nóminas, pisos, estadios…). |
| **Sonido como chiste** | Onomatopeyas y efectos que puntúan. | Efectos en cada aparición y golpe, y **silencio** justo antes del dato fuerte. |
| **Ritmo visual** | El dibujo cambia constantemente y reacciona a la voz. | Algo nuevo cada 1,5-2,5 s, sincronizado con la palabra exacta. |

## 2. Por qué los nuestros se sienten sosos (diagnóstico de «Tus padres a tu edad» y 29N)

1. **Estructura de diapositiva**: título arriba («¿Y HOY?»), gráfico, cifra. Cada escena es una lámina.
2. **Lo dibujado se queda quieto**: nada se tacha, se borra, se mueve ni reacciona. Hay tramos de 2-3 s idénticos.
3. **El primer fotograma está vacío**: el gancho empieza escribiendo letra a letra sobre papel en blanco.
4. **Cámara casi fija** (zoom del 3,5 % por escena) y una sola transición (deslizar papel).
5. **Voz plana**: cada frase se locuta con los mismos ajustes; no hay pausas con intención ni cambios de energía.
6. **Se cuenta todo de golpe**: dato → dato → dato, sin pregunta, sin giro, sin promesa.
7. **El sonido no ayuda**: música continua y rotulador; ningún efecto marca los momentos clave.

## 3. La fórmula de guion (obligatoria)

| Tramo | Tiempo | Regla |
|---|---|---|
| **Gancho** | 0-2 s | Pregunta incómoda, contradicción o dato que choca. La pantalla **ya tiene algo** en el fotograma 0. Prohibido: «Hoy vamos a hablar», «¿Sabías que…?», «Hola». |
| **Síguenos** | 2-4 s | Sello corto, sin parar la historia («Síguenos, que esto va contigo»). |
| **Problema con protagonista** | 4-12 s | Le pasa a «TÚ» o a alguien concreto. Un dato, una imagen física. |
| **Bucle abierto** | ~10 s | «Pero lo raro no es eso…», «Y aquí viene lo que nadie cuenta». |
| **Escalada** | 12-25 s | 2-3 datos, cada uno más fuerte, cada uno con reacción del personaje. |
| **Giro** | 25-35 s | La contradicción o la consecuencia poco conocida. Silencio de 0,4-0,6 s antes. |
| **Final** | últimos 4-6 s | Dato que remata o pregunta A/B para comentar + «síguenos». Si es posible, que enlace con la primera frase (bucle). |

- Duración objetivo: **25-45 s**. Una pizarra (escena) dura **≤ 9 s** y dentro pasa algo cada ≤ 2,5 s. Frases de **≤ 14 palabras**.
- Cada cifra: fuente en pantalla (nota pequeña) y en el comentario fijado. Nunca redondear para exagerar.
- Lado menos conocido: buscar la **consecuencia** (quién paga, cuánto tarda, qué no se cuenta), no la definición.

## 4. Animación (motor de pizarra, por defecto)

- **Sincronía por palabra**: los elementos aparecen en la palabra exacta (`"at": "@15,6"`), con tiempos reales de ElevenLabs.
- **Los dibujos viven**: `fx` en cualquier elemento → `tachar`, `rodear`, `borrar` (con borrador), `latir`, `temblar`, `mover` (la cifra se encoge y se va a una esquina para dejar sitio).
- **Personaje «TÚ»** (`type: "tu"`): monigote a lápiz con caras (`normal`, `sorpresa`, `susto`, `enfado`, `duda`, `risa`) y gotas de sudor; cambia de cara en una palabra.
- **Cámara viva**: sigue al elemento que se está dibujando (encuadre suave), da un **golpe de zoom** en los datos fuertes (`"golpe": true`) y nunca está quieta del todo.
- **Transiciones variadas**: `borrador` (se borra la pizarra), `zoom` (entramos en un dibujo), `barrido` (latigazo de cámara) y `papel`. Rotan solas si no se elige.
- **Subtítulos** más grandes; las cifras se resaltan en el color del vídeo.

## 5. Voz «Pizarra Pública» (ElevenLabs)

- Ajustes por frase con `tono`: `intriga` (más lenta, baja), `sorpresa`, `energia`, `remate` (lenta y firme), `normal`.
- `pausa` antes de una frase (p. ej. 0,5 s antes del giro). El silencio también corta la música.
- La voz genera los tiempos de cada palabra (`tts_elevenlabs.py --tiempos`), así los dibujos y subtítulos caen en la palabra.

## 6. Sonido

- Efectos generados por código: aparición (pop suave), golpe (impacto grave), sello, contador (tic-tac), borrador, latigazo.
- **Corte de música** en el giro (`"musica": "corte"`) y vuelta en el dato.
- La música baja sola bajo la voz (como antes).

## 7. Cómo se hace un vídeo nuevo

1. Copiar `pipeline/series/padres_viva.py` (estructura y ayudas `V()`, `T()`, `stamp()`), escribir guion y dibujos.
2. `python3 series/<serie>.py` → `python3 make_video.py storyboards/<slug>.json --maqueta --ritmo` hasta que no haya avisos.
3. Voz: acción «Voces ElevenLabs» en la rama. Render final con `--hoja`, revisar la hoja y entregar el enlace raw de `videos/`.

## 8. Control de calidad automático (`_ritmo.txt`)

El motor avisa si:
- el fotograma 0 está vacío o la primera palabra llega después de 0,4 s;
- hay más de **2,5 s** sin ningún cambio visual;
- una escena dura más de 9 s;
- el vídeo pasa de 60 s;
- la última escena no tiene pregunta ni «síguenos».
