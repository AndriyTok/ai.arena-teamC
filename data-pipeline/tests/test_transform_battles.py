import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transform_battles import transform


class TestTransformBattles(unittest.TestCase):
    def test_transform_writes_normalized_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw.ndjson"
            out = Path(tmp) / "out.ndjson"

            payload = {
                "extracted_at": "2026-01-01T00:00:00Z",
                "payload": {
                    "battleId": "battle-1",
                    "winner": "teamA",
                    "actions": [{"actionType": "Moves"}],
                },
            }
            raw.write_text(json.dumps(payload, ensure_ascii=True) + "\n", encoding="utf-8")

            count = transform(raw, out)
            self.assertEqual(count, 1)

            lines = out.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            row = json.loads(lines[0])
            self.assertEqual(row["battle_id"], "battle-1")
            self.assertEqual(row["actions_count"], 1)


if __name__ == "__main__":
    unittest.main()

