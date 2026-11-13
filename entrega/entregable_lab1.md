# Entregable Laboratorio 1: Benchmarking de Serving Local y Cuantización

- **Curso:** LLMOps, Serving Local y Arquitecturas RAG
- **Estudiante:** Juan José Gutiérrez Lasso
- **Hardware Utilizado:** Apple M1 (8 núcleos) / 8 GB RAM unificada / macOS 15.7.9 — Ollama en Docker Desktop (VM Linux arm64 con 4 vCPU y 2.83 GiB de RAM), inferencia **100 % CPU** (sin GPU dentro del contenedor)
- **Fecha:** 13 de noviembre de 2026

---

## Resumen de resultados

Modelo: `qwen2.5:1.5b-instruct` en dos cuantizaciones GGUF, con `num_ctx = 2048` y `temperature = 0.1`.

| Modelo | Prompt | TTFT (ms) | Velocidad (TPS) | Tokens | Total (s) |
|:--|:--|--:|--:|--:|--:|
| q4_K_M | Corto (Definición) | 254.79 | 30.54 | 552 | 18.09 |
| q4_K_M | Medio (Razonamiento) | 842.65 | 28.92 | 556 | 19.81 |
| q4_K_M | Largo (Generación de Código) | 401.82 | 29.91 | 664 | 22.27 |
| q8_0 | Corto (Definición) | 258.25 | 19.92 | 280 | 14.10 |
| q8_0 | Medio (Razonamiento) | 407.28 | 19.58 | 424 | 21.74 |
| q8_0 | Largo (Generación de Código) | 471.93 | 19.33 | 678 | 34.98 |

| Métrica | q4_K_M | q8_0 | Diferencia |
|:--|--:|--:|--:|
| Tamaño en disco (`ollama list`) | 986 MB (941 MiB) | 1.6 GB (1,571 MiB) | +630 MiB |
| Memoria según `ollama ps` | 1.3 GB | 2.0 GB | +0.7 GB |
| Pico de `MEM USAGE` (`docker stats`) | 1.403 GiB (≈1,437 MiB) | 1.952 GiB (≈1,999 MiB) | **+0.549 GiB (≈562 MiB)** |
| TPS promedio | 29.79 | 19.61 | **+51.9 % a favor de q4** |
| Procesador (`ollama ps`) | 100 % CPU | 100 % CPU | — |

---

## Análisis Técnico de Resultados

### 1. Impacto en Memoria (MEM USAGE y KV Cache)
> ¿Cuál fue la diferencia exacta en MB/GB de RAM consumida entre `q4_K_M` y `q8_0` al ejecutar `docker stats`? ¿Por qué el consumo en ejecución supera el tamaño del archivo en disco? (Relacionar con el tamaño de contexto `num_ctx: 2048` y el KV Cache).

**Respuesta:**

Con el modelo cargado y generando, `docker stats` llegó a un pico de **1.403 GiB con q4_K_M** y **1.952 GiB con q8_0**. La diferencia es de **0.549 GiB (≈562 MiB)**: q8_0 consume un 39 % más de RAM. `ollama ps` muestra lo mismo (1.3 GB frente a 2.0 GB). El dato cuadra con la teoría: q8_0 guarda unos 8.5 bits por peso y Q4_K_M unos 4.8, así que con ~1.5 B parámetros la diferencia en pesos ronda los 630 MiB, que es justo la diferencia entre los archivos en disco.

En ejecución se consume más que el archivo en disco (+496 MiB en q4 y +428 MiB en q8). El log de `llama.cpp` permite desglosar esa memoria:

| Componente (log de llama.cpp) | q4_K_M | q8_0 |
|:--|--:|--:|
| Pesos en RAM (`CPU model buffer` + `CPU_REPACK buffer`) | 183 + 934 = 1,117 MiB | 237 + 1,564 = 1,801 MiB |
| **KV Cache** (`num_ctx = 2048`, K y V en f16) | **56 MiB** | **56 MiB** |
| Buffer de cómputo (activaciones y logits) | 69.5 MiB | 69.5 MiB |
| Resto: servidor Ollama, runtime de `llama-server` y *page cache* del GGUF | ≈190 MiB | ≈70 MiB |
| **Total medido (`docker stats`)** | **≈1,437 MiB** | **≈1,999 MiB** |

1. **KV Cache.** En la inferencia se guardan las matrices K y V de cada token del contexto para no recalcularlas. La memoria se reserva completa para `num_ctx` al cargar el modelo:
   `2 (K,V) × 28 capas × 2048 tokens × 2 KV-heads × 128 dim × 2 bytes (f16) = 58,720,256 B = 56 MiB`.
   El KV cache **no depende de la cuantización de los pesos** (es f16 en ambos casos), por eso mide lo mismo en los dos modelos. Es pequeño porque Qwen2.5 usa *Grouped-Query Attention* (2 KV-heads en lugar de 12). Con atención multi-head clásica ocuparía unos 336 MiB. Además crece linealmente con `num_ctx`: con 8192 tokens serían 224 MiB.
2. **Repacking de pesos.** En CPU ARM, llama.cpp reordena los pesos a un formato intercalado optimizado para NEON y dot-product (`CPU_REPACK`). Por eso los copia a memoria anónima en lugar de mapearlos desde el archivo (`load_mode = none`), y el resultado ocupa algo más que el GGUF (1,117 MiB frente a 941 MiB en q4).
3. **Buffers de cómputo y runtime.** Están las activaciones intermedias y el vector de logits de 151,936 entradas (el vocabulario), más el proceso del servidor de Ollama. `docker stats` también cuenta la *page cache* del archivo leído, que varía entre cargas.

---

### 2. Ancho de Banda de Memoria y Velocidad (TPS)
> En inferencia sobre CPU, el cuello de botella suele ser el ancho de banda de la memoria RAM. ¿En qué porcentaje aumentó la velocidad (TPS) al pasar de 8 bits a 4 bits según tus resultados?

**Respuesta:**

La velocidad **aumentó un 51.9 %** de media al pasar de q8_0 (19.61 TPS) a q4_K_M (29.79 TPS):

| Prompt | q8_0 | q4_K_M | Aumento |
|:--|--:|--:|--:|
| Corto | 19.92 | 30.54 | +53.3 % |
| Medio | 19.58 | 28.92 | +47.7 % |
| Largo | 19.33 | 29.91 | +54.7 % |
| **Promedio** | **19.61** | **29.79** | **+51.9 %** |

**Por qué.** En la fase de decodificación se genera un token cada vez, y para cada uno hay que leer de RAM **todos** los pesos del modelo. Es una multiplicación matriz-vector con muy poca reutilización de datos, así que el CPU pasa la mayor parte del tiempo esperando a la memoria. Con menos bytes por token, salen más tokens por segundo.

**Comprobación con los datos.** Si multiplicamos los TPS por los bytes de pesos leídos en cada token, obtenemos el ancho de banda efectivo:
- q4_K_M: 29.79 tok/s × 1,117 MiB ≈ **34.9 GB/s**
- q8_0: 19.61 tok/s × 1,801 MiB ≈ **37.0 GB/s**

Los dos modelos llegan prácticamente **al mismo techo de ~35–37 GB/s**, aunque uno tiene el doble de bits por peso. Eso indica que el límite es el ancho de banda y no el cómputo. El M1 tiene 68 GB/s nominales, y la VM de Docker con 4 vCPU aprovecha más o menos la mitad.

**Por qué no llega al +61 % teórico.** Los bytes de pesos de q8 son 1.61 veces los de q4, y aun así la mejora fue del 52 %. Influyen dos cosas:
- **Coste fijo por token:** atención sobre el KV cache, *sampling* sobre 151 K logits y *streaming* HTTP. Este coste no se reduce al cuantizar.
- **Más cómputo en Q4_K:** desempaquetar sus super-bloques con escalas de 6 bits cuesta más que en Q8_0. Con 4 hilos, q4 empieza a acercarse al límite de cómputo.

---

### 3. Latencia Inicial (TTFT) y Fase Prefill
> ¿Por qué el `TTFT (ms)` es significativamente más alto en el Prompt Largo (Generación de Código) que en el Prompt Corto (Definición)?

**Respuesta:**

El TTFT es casi todo **prefill**: el modelo tiene que procesar **todos los tokens de entrada** y llenar el KV cache antes de emitir el primer token. A diferencia de la decodificación, el prefill procesa los tokens en paralelo con multiplicaciones matriz-matriz, de modo que está **limitado por cómputo (FLOPs)**. Su coste crece con el número de tokens de entrada (≈ 2 × parámetros × tokens), más un término cuadrático de la atención. A más tokens que pre-procesar, más TTFT.

En mis resultados, el prompt largo tuvo **un 58 % más de TTFT en q4** (402 ms frente a 255 ms) y **un 83 % más en q8** (472 ms frente a 258 ms). Hay matices que conviene señalar con datos:

- **Los prompts son cortos en entrada.** Con la plantilla de chat ocupan 52 tokens (corto), 79 (medio) y 65 (largo). El prompt "Largo" es largo sobre todo en **salida** (código). La longitud de salida no afecta al TTFT sino al tiempo total, que es donde se ve la diferencia grande: 22–35 s frente a 14–18 s. El prompt con más tokens de entrada (el medio, 79) fue el que tuvo el TTFT más alto en q4 (843 ms).
- **El TTFT incluye costes fijos** que no son prefill: HTTP, tokenización, planificación del *runner* y el primer paso de decodificación. Con tan pocos tokens de entrada, esos costes y la variabilidad del sistema pesan mucho, y por eso hay valores atípicos como esos 843 ms.
- **Prueba de que el coste es el prefill.** Repetí cada prompt 5 veces ([`resultados/ttft_repeticiones.md`](../resultados/ttft_repeticiones.md)). Al reutilizar el KV cache de un prompt ya visto (*prompt caching* de llama.cpp), el TTFT cae a **~30 ms en q4 y ~40–55 ms en q8**: al saltarse el prefill, la latencia inicial casi desaparece. También se ve que el prefill es más lento en q8 que en q4, porque mueve más bytes por cada capa.

Implicación para LLMOps: en RAG, donde el prompt lleva miles de tokens de contexto recuperado, el TTFT crecerá mucho más que aquí. Por eso conviene controlar el tamaño del contexto (`num_ctx`, *chunking*) y aprovechar el prompt caching de los prefijos comunes, como el *system prompt*.

---

### 4. Calidad vs. Eficiencia en `resultados_benchmark.md`
> Revisando las 6 respuestas completas generadas en `resultados_benchmark.md`, ¿hubo alguna degradación perceptible en la lógica del código Python o en el razonamiento arquitectónico generado por el modelo de 4 bits frente al de 8 bits?

**Respuesta:**

**No se observa una degradación clara atribuible a los 4 bits.** Los dos modelos comparten los mismos errores de fondo, que vienen de un modelo de solo 1.5 B parámetros y no de la cuantización. Hay diferencias menores de estilo y de seguimiento de instrucciones. Ejecuté el código generado para no evaluarlo "a ojo":

| Prompt | q4_K_M | q8_0 |
|:--|:--|:--|
| **Corto:** "exactamente 3 viñetas" | Da 3 viñetas, pero cada una con 3 sub-viñetas (552 tokens): **cumple peor el formato**. **Error conceptual:** confunde la cuantización con reducción de dimensionalidad y discretizar caracteres. | Exactamente 3 viñetas, más conciso (280 tokens): **mejor seguimiento de la instrucción**. **También es un error conceptual:** la describe como "eliminar información no esencial del texto". |
| **Medio:** arquitectura para 16 GB sin GPU | Recomienda un modelo de ~150 M y **se contradice**: propone desplegar en la nube (HF, Anthropic) cuando el servidor es local. Inventa requisitos (1–2 TB SSD). | Recomienda 124 M–350 M. Es **repetitivo y circular** (repite la cifra "124M a 350M" 5 veces, 3 de ellas como "sería una buena opción") y confunde entrenamiento con inferencia. |
| **Largo:** búsqueda binaria en Python | El algoritmo **es correcto** en listas ordenadas (lo probé con casos extra: inicio, medio y final). Fallos: da 5 pruebas, 3 de ellas idénticas, en lugar de 3. El docstring promete `ValueError` si la lista no está ordenada y `TypeError` explícito, y no implementa ninguno de los dos. **El script se cae** en la 3ª prueba con un `TypeError` no controlado. | El algoritmo **es correcto** (mismo núcleo). Usa `doctest`, que es más estructurado. Fallos: da 4 pruebas en vez de 3, **una de ellas falla** (documenta `[] → -1`, pero el código lanza `ValueError`) y tampoco valida que la lista esté ordenada. |

**Conclusiones:**
- **El razonamiento arquitectónico es pobre en ambos.** Ninguno da una respuesta útil, que sería algo como un modelo de 7–8 B en Q4_K_M (~5 GB) servido con llama.cpp/Ollama, más RAG, dentro de 16 GB. Esto es una limitación de capacidad del modelo de 1.5 B, no de la cuantización.
- **En código, el núcleo algorítmico es idéntico y correcto en ambos.** Los errores están en pruebas y manejo de excepciones, con una ligera ventaja de q8 en estructura.
- **q8_0 sigue algo mejor las restricciones de formato** (las "exactamente 3 viñetas"). Esto encaja con lo que se sabe: la pérdida de calidad de Q4_K_M es pequeña, pero se nota más en modelos pequeños.
- **Limitación del análisis:** hay una sola muestra por prompt (n = 1), así que las diferencias no son estadísticamente concluyentes. Para afirmarlo con rigor haría falta un conjunto de evaluación más grande con métricas automáticas (p. ej. *pass@k* con tests unitarios para el código, o LLM-as-judge).

**Recomendación:** para este hardware, **q4_K_M es la mejor opción**. Es un 52 % más rápido, usa ~562 MiB menos de RAM y, en esta muestra, su calidad es equivalente a q8_0.

---

## Anexo: notas de ejecución y ajustes

1. **Límite de memoria de Docker.** La VM de Docker Desktop tiene 2.83 GiB. Con otros contenedores activos, el primer intento terminó con `llama-server process has terminated: signal: killed` (OOM). `docker pause` no libera RAM, así que detuve temporalmente los demás contenedores mientras corría el benchmark. Esto mismo demuestra en la práctica el *sizing* de memoria que trata el laboratorio.
2. **Ajuste del script ([`benchmark.py`](../benchmark.py)).** Agregué `"num_predict": 1024` y `"seed": 42` a `options`. En la primera ejecución, el prompt medio con q4 estuvo más de 10 minutos generando sin terminar: con temperatura baja y sin límite de tokens, el modelo entró en un bucle de repetición y Ollama siguió generando con *context shift*. El tope se usa como protección (ninguna respuesta lo alcanzó: el máximo fue 678 tokens) y la semilla hace los resultados reproducibles.
3. **Formato de [`resultados_benchmark.md`](../resultados/resultados_benchmark.md).** Las respuestas de código contienen bloques ```` ```python ```` dentro del bloque ```` ```text ```` que crea el script, y eso rompía el renderizado. Cambié solo los delimitadores externos por `~~~~`; el contenido no se modificó.
4. **Monitoreo de memoria.** [`scripts/monitor_memoria.sh`](../scripts/monitor_memoria.sh) registró `docker stats` y `ollama ps` durante la ejecución ([`resultados/memoria_docker_stats.log`](../resultados/memoria_docker_stats.log)).

---
### Archivos de evidencia (en este repositorio)

| Archivo | Contenido |
|:--|:--|
| [`resultados/resultados_benchmark.csv`](../resultados/resultados_benchmark.csv) | Métricas tabuladas (TTFT, TPS, tokens, tiempo total) |
| [`resultados/resultados_benchmark.md`](../resultados/resultados_benchmark.md) | Las 6 respuestas completas con sus métricas |
| [`resultados/memoria_docker_stats.log`](../resultados/memoria_docker_stats.log) | Muestras de `docker stats` y `ollama ps` durante la ejecución |
| [`resultados/ttft_repeticiones.md`](../resultados/ttft_repeticiones.md) | Medición complementaria de TTFT (5 repeticiones) |
| [`benchmark.py`](../benchmark.py) · [`docker-compose.yml`](../docker-compose.yml) | Script y despliegue usados |
