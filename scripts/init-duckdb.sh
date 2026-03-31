#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB_PATH="$ROOT_DIR/data/duckdb/arena.duckdb"
SQL_PATH="$ROOT_DIR/data-pipeline/sql/init.sql"

mkdir -p "$(dirname "$DB_PATH")"

python3 - "$DB_PATH" "$SQL_PATH" << 'PY'
import duckdb
from pathlib import Path
import sys

db_path = Path(sys.argv[1])
sql_path = Path(sys.argv[2])

try:
    con = duckdb.connect(str(db_path))
    con.execute(sql_path.read_text(encoding="utf-8"))
    con.close()
    print(f"✓ DuckDB initialized at: {db_path}")
except Exception as e:
    print(f"✗ Error: {e}", file=sys.stderr)
    sys.exit(1)
PY


