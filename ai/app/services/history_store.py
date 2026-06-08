import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import DATA_DIR

HISTORY_DB = DATA_DIR / "history.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not HISTORY_DB.exists():
        HISTORY_DB.write_text("[]", encoding="utf-8")


def _read_all() -> list[dict[str, Any]]:
    _ensure_db()
    return json.loads(HISTORY_DB.read_text(encoding="utf-8"))


def _write_all(items: list[dict[str, Any]]) -> None:
    _ensure_db()
    HISTORY_DB.write_text(json.dumps(items, indent=2), encoding="utf-8")


def add_entry(
    voice_id: str,
    voice_name: str,
    text: str,
    filename: str,
) -> dict[str, Any]:
    entry = {
        "id": str(uuid.uuid4()),
        "voice_id": voice_id,
        "voice_name": voice_name,
        "text_preview": text[:120] + ("..." if len(text) > 120 else ""),
        "filename": filename,
        "created_at": _now(),
    }
    items = _read_all()
    items.insert(0, entry)
    _write_all(items)
    return entry


def list_history(limit: int = 50) -> list[dict[str, Any]]:
    return _read_all()[:limit]
