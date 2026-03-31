# Data Pipeline

This folder contains a minimal ETL flow for battle data:

1. Extract battle results from backend API into newline-delimited JSON.
2. Transform raw JSON into normalized records.
3. Load records into DuckDB.

## Layout

- `src/` Python ETL modules
- `sql/` DuckDB schema SQL
- `tests/` unit tests for transform logic
- `config/.env.example` environment template
- `scripts/` shell helpers to run/clean pipeline artifacts

## Quick start

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
python3 -m venv .venv
source .venv/bin/activate
pip install -r data-pipeline/requirements.txt
cp data-pipeline/config/.env.example data-pipeline/config/.env
python3 data-pipeline/src/run_pipeline.py --samples 5
```

Alternative via helper script:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
./data-pipeline/scripts/run-etl.sh 5
```

## Output

By default the pipeline writes to the visible `data/` folder:

- `data/raw/battles_raw.ndjson`
- `data/staging/battles_transformed.ndjson`
- `data/duckdb/arena.duckdb`

## Run pieces separately

```bash
python3 data-pipeline/src/extract_battles.py --samples 10
python3 data-pipeline/src/transform_battles.py
python3 data-pipeline/src/load_to_duckdb.py
```

## Clean local ETL artifacts

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
./data-pipeline/scripts/clean-etl.sh
```

## Notes

- Start backend before extract phase (`http://localhost:5222` by default).
- All files gitignored (see `.gitignore`), so they won't be committed.
- Easy to browse in Finder and attach in Rider without enabling hidden files.

## Smoke test

```bash
python3 -m unittest discover -s data-pipeline/tests -p "test_*.py"
```

