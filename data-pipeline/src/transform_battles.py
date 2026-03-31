import json
from pathlib import Path

from common import ensure_parent, get_config
from transform_logic import normalize_record


def transform(raw_path: Path, output_path: Path) -> int:
    count = 0

    with raw_path.open("r", encoding="utf-8") as inp, output_path.open("w", encoding="utf-8") as out:
        for line in inp:
            line = line.strip()
            if not line:
                continue
            raw_record = json.loads(line)
            normalized = normalize_record(raw_record)
            out.write(json.dumps(normalized, ensure_ascii=True) + "\n")
            count += 1

    return count


def main() -> None:
    cfg = get_config()
    raw_path = Path(cfg["RAW_OUTPUT"])
    output = ensure_parent(cfg["STAGING_OUTPUT"])

    if not raw_path.exists():
        raise FileNotFoundError(f"Raw input not found: {raw_path}")

    transformed = transform(raw_path, output)
    print(f"Transformed {transformed} records to {output}")


if __name__ == "__main__":
    main()

