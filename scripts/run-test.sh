#!/usr/bin/env bash
# Executa o teste de carga completo: mock -> JMeter -> dashboard + relatorios
# Uso: ./scripts/run-test.sh [threads] [rampup] [loops]
set -euo pipefail

THREADS="${1:-25}"
RAMPUP="${2:-10}"
LOOPS="${3:-2}"
PORT="${PORT:-8099}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/results"

command -v jmeter >/dev/null || { echo "ERRO: jmeter nao encontrado no PATH"; exit 1; }

echo ">> Subindo mock API na porta $PORT..."
python3 "$ROOT/mock-api/app.py" "$PORT" & MOCK_PID=$!
trap 'kill $MOCK_PID 2>/dev/null || true' EXIT
sleep 1
curl -sf "http://localhost:$PORT/health" >/dev/null || { echo "ERRO: mock nao respondeu"; exit 1; }

echo ">> Executando JMeter: $THREADS VUs, ramp-up ${RAMPUP}s, $LOOPS loops"
rm -rf "$OUT/dashboard" "$OUT/results.jtl"
jmeter -n -t "$ROOT/test-plan/immigration-api-load-test.jmx" \
  -Jhost=localhost -Jport="$PORT" \
  -Jthreads="$THREADS" -Jrampup="$RAMPUP" -Jloops="$LOOPS" \
  -l "$OUT/results.jtl" -j "$OUT/jmeter.log"

echo ">> Gerando dashboard HTML..."
jmeter -g "$OUT/results.jtl" -o "$OUT/dashboard" -j "$OUT/report.log"

echo ">> Concluido. Abra results/dashboard/index.html"
