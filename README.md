# Lab 1 · Benchmarking de Serving Local y Cuantización

**Curso:** LLMOps, Serving Local y Arquitecturas RAG  
**Estudiante:** Juan José Gutiérrez Lasso

En este laboratorio se despliega Ollama en Docker (100 % CPU) y se compara `qwen2.5:1.5b-instruct` en dos cuantizaciones GGUF, **q4_K_M** y **q8_0**. Se miden memoria RAM, TTFT (latencia hasta el primer token) y TPS (tokens por segundo).

> 📄 **Entregable con las respuestas:** [`entrega/entregable_lab1.md`](entrega/entregable_lab1.md)

## Resultados clave

| Métrica | q4_K_M | q8_0 |
|:--|--:|--:|
| Tamaño en disco | 986 MB | 1.6 GB |
| Pico de RAM (`docker stats`) | 1.403 GiB | 1.952 GiB (+562 MiB) |
| KV Cache (`num_ctx` = 2048) | 56 MiB | 56 MiB |
| Velocidad media | **29.79 TPS** | 19.61 TPS |
| Aumento de velocidad de 8 → 4 bits | **+51.9 %** | — |

Hardware: Apple M1 con 8 GB, macOS 15.7.9. Docker Desktop corre una VM Linux arm64 con 4 vCPU y 2.83 GiB.

## Estructura

```
.
├── entrega/
│   └── entregable_lab1.md        # Entregable: análisis y respuestas a las 4 preguntas
├── resultados/
│   ├── resultados_benchmark.csv  # Métricas generadas por benchmark.py
│   ├── resultados_benchmark.md   # Las 6 respuestas completas de los modelos
│   ├── memoria_docker_stats.log  # Monitoreo de RAM durante la ejecución
│   ├── ttft_repeticiones.md      # Medición complementaria de TTFT
│   ├── ejecucion_benchmark.log
│   └── ollama_ps_final.txt
├── scripts/
│   ├── monitor_memoria.sh        # Registra docker stats + ollama ps cada ~1 s
│   └── ttft_repeticiones.py      # 5 repeticiones de TTFT por prompt
├── benchmark.py                  # Script del laboratorio (+ num_predict y seed)
├── docker-compose.yml
└── requirements.txt
```

## Cómo reproducirlo

```bash
docker compose up -d
docker exec -it ollama-local-lab ollama pull qwen2.5:1.5b-instruct-q4_K_M
docker exec -it ollama-local-lab ollama pull qwen2.5:1.5b-instruct-q8_0

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

./scripts/monitor_memoria.sh resultados/memoria_docker_stats.log &   # opcional
python benchmark.py            # genera resultados_benchmark.csv y .md en la raíz
python scripts/ttft_repeticiones.py

deactivate && docker compose down
```

> **Nota:** el contenedor necesita unos 2 GiB libres dentro de la VM de Docker para cargar q8_0. Si Ollama devuelve `signal: killed`, se quedó sin memoria (OOM): sube la memoria de Docker Desktop o detén otros contenedores.

## Cambios respecto a la guía

- `benchmark.py` incluye `num_predict: 1024` y `seed: 42`. Sin el tope, una generación entró en un bucle de repetición que no terminaba. La semilla hace los resultados reproducibles.
- Los resultados se movieron a `resultados/` para tener el repositorio ordenado.
