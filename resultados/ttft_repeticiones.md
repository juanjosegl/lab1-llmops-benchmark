> Medición complementaria: 5 repeticiones por prompt (rotando prompts), `num_predict: 2`. Las repeticiones reutilizan el KV cache de prompts ya vistos (prompt caching de llama.cpp), por eso el TTFT cae a ~30–55 ms frente a los 250–850 ms del benchmark en frío.

| Modelo | Prompt | Tokens entrada | TTFT mediana (ms) | TTFT min–max (ms) | Prefill mediana (ms) |
|---|---|---:|---:|---:|---:|
| 1.5b-instruct-q4_K_M | Corto (Definición) | 52 | 34.3 | 27–152 | 25.0 |
| 1.5b-instruct-q4_K_M | Medio (Razonamiento) | 79 | 29.2 | 28–40 | 21.6 |
| 1.5b-instruct-q4_K_M | Largo (Generación de Código) | 65 | 30.1 | 29–42 | 21.6 |
| 1.5b-instruct-q8_0 | Corto (Definición) | 52 | 55.4 | 40–146 | 45.8 |
| 1.5b-instruct-q8_0 | Medio (Razonamiento) | 79 | 45.3 | 41–249 | 36.3 |
| 1.5b-instruct-q8_0 | Largo (Generación de Código) | 65 | 40.6 | 39–195 | 33.5 |
