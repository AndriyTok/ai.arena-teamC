from __future__ import annotations

from typing import Any


def normalize_record(raw_record: dict[str, Any]) -> dict[str, Any]:
    payload = raw_record.get("payload") or {}
    actions = payload.get("actions") or []

    return {
        "battle_id": payload.get("battleId") or payload.get("battleID") or "",
        "winner": payload.get("winner") or "",
        "actions_count": len(actions) if isinstance(actions, list) else 0,
        "extracted_at": raw_record.get("extracted_at") or "",
        "raw_json": payload,
    }

