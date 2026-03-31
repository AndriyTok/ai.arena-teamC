import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transform_logic import normalize_record


class TestTransformLogic(unittest.TestCase):
    def test_normalize_record_basic(self) -> None:
        raw = {
            "extracted_at": "2026-01-01T00:00:00Z",
            "payload": {
                "battleId": "b1",
                "winner": "teamA",
                "actions": [{"actionType": "Appears"}, {"actionType": "Moves"}],
            },
        }

        out = normalize_record(raw)

        self.assertEqual(out["battle_id"], "b1")
        self.assertEqual(out["winner"], "teamA")
        self.assertEqual(out["actions_count"], 2)
        self.assertEqual(out["extracted_at"], "2026-01-01T00:00:00Z")
        self.assertIsInstance(out["raw_json"], dict)

    def test_normalize_record_missing_fields(self) -> None:
        out = normalize_record({})
        self.assertEqual(out["battle_id"], "")
        self.assertEqual(out["winner"], "")
        self.assertEqual(out["actions_count"], 0)


if __name__ == "__main__":
    unittest.main()

