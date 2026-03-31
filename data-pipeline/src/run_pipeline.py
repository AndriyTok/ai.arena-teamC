import argparse
from pathlib import Path

from common import get_config
from extract_battles import extract
from load_to_duckdb import load_records
from transform_battles import transform


def run(samples: int) -> None:
    cfg = get_config()

    raw_path = Path(cfg["RAW_OUTPUT"])
    staging_path = Path(cfg["STAGING_OUTPUT"])
    db_path = Path(cfg["DUCKDB_PATH"])
    sql_path = Path(cfg["REPO_ROOT"]) / "data-pipeline" / "sql" / "init.sql"

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    staging_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    extracted = extract(samples, raw_path)
    transformed = transform(raw_path, staging_path)
    loaded = load_records(staging_path, db_path, sql_path)

    print(f"Extracted: {extracted}")
    print(f"Transformed: {transformed}")
    print(f"Loaded: {loaded}")
    print(f"DuckDB: {db_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full ETL pipeline")
    parser.add_argument("--samples", type=int, default=10, help="Number of API samples")
    args = parser.parse_args()

    run(args.samples)


if __name__ == "__main__":
    main()

