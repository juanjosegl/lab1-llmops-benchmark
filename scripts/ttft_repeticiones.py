"""Medición complementaria de TTFT: 5 repeticiones por prompt y modelo (uso: python scripts/ttft_repeticiones.py)."""
import os, sys, time, json, statistics, requests
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from benchmark import PROMPTS, MODELS
out = ["| Modelo | Prompt | Tokens entrada | TTFT mediana (ms) | TTFT min–max (ms) | Prefill mediana (ms) |", "|---|---|---:|---:|---:|---:|"]
for m in MODELS:
    requests.post("http://localhost:11434/api/generate", json={"model": m, "prompt": "Hola", "stream": False, "options": {"num_ctx": 2048, "num_predict": 1}})
    res = {p["tipo"]: [] for p in PROMPTS}
    for _ in range(5):
        for p in PROMPTS:  # rotación: cada prompt difiere del anterior (sin reuso total de caché)
            t0 = time.perf_counter(); ttft = None
            with requests.post("http://localhost:11434/api/generate", stream=True, json={"model": m, "prompt": p["texto"], "stream": True,
                    "options": {"temperature": 0.1, "num_ctx": 2048, "num_predict": 2, "seed": 42}}) as r:
                for line in r.iter_lines():
                    if not line: continue
                    c = json.loads(line)
                    if ttft is None and c.get("response"): ttft = (time.perf_counter() - t0) * 1000
                    if c.get("done"): pe, pd = c["prompt_eval_count"], c["prompt_eval_duration"] / 1e6
            res[p["tipo"]].append((ttft, pe, pd))
    for t, v in res.items():
        tt = [x[0] for x in v]
        out.append(f"| {m.split(':')[1]} | {t} | {v[0][1]} | {statistics.median(tt):.1f} | {min(tt):.0f}–{max(tt):.0f} | {statistics.median([x[2] for x in v]):.1f} |")
print("\n".join(out))
