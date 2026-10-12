#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_CODEQL="$ROOT_DIR/scripts/codeql"
EXPERIMENTS_DIR="${EXPERIMENTS_DIR:-experiments}"
N="${N:-5}"
CONCURRENCY="${CONCURRENCY:-50}"
TEMPERATURE="${TEMPERATURE:-0.8}"

export OPENAI_API_KEY="${OPENAI_API_KEY:-lmstudio}"
BASE_URL="${BASE_URL:-http://localhost:1235/v1}"
MODEL="${MODEL:-openai/gpt-oss-20b}"
REASONING="${REASONING:-medium}"
if [[ -x "$LOCAL_CODEQL" ]]; then
  CODEQL="${CODEQL:-$LOCAL_CODEQL}"
else
  CODEQL="${CODEQL:-codeql}"
fi

MODEL_SLUG="${MODEL//[^A-Za-z0-9._-]/-}"
STARTED_AT="$(date -u +%Y-%m-%d_%H-%M-%S_UTC)"
RUN_NAME="${RUN_NAME:-${STARTED_AT}__${MODEL_SLUG}__reasoning-${REASONING}__n${N}-$$}"
OUTPUT="${OUTPUT:-${EXPERIMENTS_DIR}/${RUN_NAME}/results.parquet}"

: "${OPENAI_API_KEY:?Debes definir OPENAI_API_KEY}"
: "${BASE_URL:?Debes definir BASE_URL}"
: "${MODEL:?Debes definir MODEL}"
: "${TEMPERATURE:?Debes definir TEMPERATURE}"
: "${REASONING:?Debes definir REASONING}"

if [[ "$OUTPUT" != *.parquet ]]; then
  echo "error: OUTPUT debe terminar en .parquet" >&2
  exit 2
fi

if [[ ! "$RUN_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "error: RUN_NAME sólo puede contener letras, números, puntos, guiones y '_'" >&2
  exit 2
fi

if [[ ! "$N" =~ ^[1-9][0-9]*$ ]]; then
  echo "error: N debe ser un entero positivo" >&2
  exit 2
fi

if [[ ! "$CONCURRENCY" =~ ^[1-9][0-9]*$ ]]; then
  echo "error: CONCURRENCY debe ser un entero positivo" >&2
  exit 2
fi

if [[ ! "$TEMPERATURE" =~ ^([0-9]+([.][0-9]+)?|[.][0-9]+)$ ]]; then
  echo "error: TEMPERATURE debe ser un número no negativo" >&2
  exit 2
fi

case "$REASONING" in
  none|off|on|minimal|low|medium|high|xhigh) ;;
  *)
    echo "error: REASONING debe ser on/off o none/minimal/low/medium/high/xhigh" >&2
    exit 2
    ;;
esac

cd "$ROOT_DIR"
mkdir -p "$(dirname "$OUTPUT")"

echo "Experimento: $RUN_NAME" >&2
echo "Salida: $OUTPUT" >&2
echo "Modelo: $MODEL" >&2
echo "Reasoning: $REASONING" >&2
echo "N: $N generaciones por nivel" >&2
echo "Concurrencia: $CONCURRENCY peticiones" >&2
echo "Temperatura: $TEMPERATURE" >&2
echo "CodeQL: $CODEQL" >&2
echo >&2

uv run python experiment.py run \
  --output "$OUTPUT" \
  --base-url "$BASE_URL" \
  --model "$MODEL" \
  --n "$N" \
  --concurrency "$CONCURRENCY" \
  --temperature "$TEMPERATURE" \
  --reasoning "$REASONING" \
  --codeql "$CODEQL" \
  --include-cwe-description \
  --timeout 300 \
  "$@"
