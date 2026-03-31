#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

rm -rf "$ROOT_DIR/data/raw" \
       "$ROOT_DIR/data/staging" \
       "$ROOT_DIR/data/duckdb/*.duckdb" \
       "$ROOT_DIR/data/duckdb/*.wal"

mkdir -p "$ROOT_DIR/data/raw" \
         "$ROOT_DIR/data/staging" \
         "$ROOT_DIR/data/duckdb"

echo "Cleaned ETL artifacts under data/"

