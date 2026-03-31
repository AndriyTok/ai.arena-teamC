#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
SAMPLES="${1:-10}"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install -r "$ROOT_DIR/data-pipeline/requirements.txt" >/dev/null

if [[ ! -f "$ROOT_DIR/data-pipeline/config/.env" ]]; then
  cp "$ROOT_DIR/data-pipeline/config/.env.example" "$ROOT_DIR/data-pipeline/config/.env"
fi

cd "$ROOT_DIR"
REPO_ROOT="$ROOT_DIR" python3 data-pipeline/src/run_pipeline.py --samples "$SAMPLES"

