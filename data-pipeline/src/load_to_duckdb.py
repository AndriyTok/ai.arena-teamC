from __future__ import annotations

import json
from pathlib import Path

from common import ensure_parent, get_config


def load_records(staging_path: Path, db_path: Path, sql_path: Path) -> int:
    try:
        import duckdb
    except ImportError as exc:
        raise RuntimeError(
            "duckdb is required. Install with: pip install -r data-pipeline/requirements.txt"
        ) from exc

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(db_path))

    schema_sql = sql_path.read_text(encoding="utf-8")
    conn.execute(schema_sql)

    inserted = 0
    with staging_path.open("r", encoding="utf-8") as inp:
        for line in inp:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            conn.execute(
                """
                INSERT INTO battles (battle_id, winner, actions_count, extracted_at, raw_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    row.get("battle_id", ""),
                    row.get("winner", ""),
                    int(row.get("actions_count", 0)),
                    row.get("extracted_at", ""),
                    json.dumps(row.get("raw_json", {}), ensure_ascii=True),
                ],
            )
            inserted += 1

    conn.close()
    return inserted


def main() -> None:
    cfg = get_config()
    staging_path = Path(cfg["STAGING_OUTPUT"])
    db_path = ensure_parent(cfg["DUCKDB_PATH"])
    sql_path = Path(cfg["REPO_ROOT"]) / "data-pipeline" / "sql" / "init.sql"

    if not staging_path.exists():
        raise FileNotFoundError(f"Staging input not found: {staging_path}")

    inserted = load_records(staging_path, db_path, sql_path)
    print(f"Loaded {inserted} rows into {db_path}")


if __name__ == "__main__":
    main()

