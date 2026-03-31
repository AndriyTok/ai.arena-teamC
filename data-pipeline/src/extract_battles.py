import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib import request

from common import ensure_parent, get_config


def fetch_battle(base_url: str, endpoint: str) -> dict:
    url = f"{base_url.rstrip('/')}{endpoint}"
    req = request.Request(url, data=b"{}", method="POST")
    req.add_header("Content-Type", "application/json")

    with request.urlopen(req, timeout=10) as resp:  # nosec B310
        payload = resp.read().decode("utf-8")
    return json.loads(payload)


def extract(samples: int, output_path: Path) -> int:
    cfg = get_config()
    base_url = cfg["API_BASE_URL"]
    endpoint = cfg["API_BATTLE_ENDPOINT"]

    count = 0
    with output_path.open("w", encoding="utf-8") as out:
        for _ in range(samples):
            battle = fetch_battle(base_url, endpoint)
            record = {
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "payload": battle,
            }
            out.write(json.dumps(record, ensure_ascii=True) + "\n")
            count += 1

    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract random battle samples from API")
    parser.add_argument("--samples", type=int, default=10, help="Number of API calls")
    args = parser.parse_args()

    cfg = get_config()
    output = ensure_parent(cfg["RAW_OUTPUT"])
    written = extract(args.samples, output)
    print(f"Extracted {written} records to {output}")


if __name__ == "__main__":
    main()

