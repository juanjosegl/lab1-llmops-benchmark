#!/usr/bin/env bash
# Registra cada ~1 s el uso de memoria del contenedor (docker stats) y el modelo residente (ollama ps).
# Uso: ./monitor_memoria.sh &   (detener con kill al terminar el benchmark)
OUT="${1:-memoria_docker_stats.log}"
: > "$OUT"
while true; do
  ts=$(date +%H:%M:%S)
  mem=$(docker stats --no-stream --format '{{.MemUsage}} | CPU {{.CPUPerc}}' ollama-local-lab)
  ps=$(docker exec ollama-local-lab ollama ps 2>/dev/null | tail -n +2 | awk '{print $1, $3, $4, $5, $6}' | tr '\n' ';')
  echo "$ts | $mem | ollama ps: ${ps:-<ninguno>}" >> "$OUT"
  sleep 1
done
