import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from app.config import VOICES_DB, VOICES_DIR


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_db() -> None:
    VOICES_DIR.mkdir(parents=True, exist_ok=True)
    if not VOICES_DB.exists():
        VOICES_DB.write_text("[]", encoding="utf-8")


def _read_all() -> list[dict[str, Any]]:
    _ensure_db()
    return json.loads(VOICES_DB.read_text(encoding="utf-8"))


def _write_all(voices: list[dict[str, Any]]) -> None:
    _ensure_db()
    VOICES_DB.write_text(json.dumps(voices, indent=2), encoding="utf-8")


def list_voices(ready_only: bool = False) -> list[dict[str, Any]]:
    voices = _read_all()
    if ready_only:
        return [v for v in voices if v.get("status") == "ready"]
    return voices


def get_voice(voice_id: str) -> Optional[dict[str, Any]]:
    for voice in _read_all():
        if voice["id"] == voice_id:
            return voice
    return None


def create_voice(name: str, sample_path: Path, duration_seconds: float) -> dict[str, Any]:
    voice_id = str(uuid.uuid4())
    voice_dir = VOICES_DIR / voice_id
    voice_dir.mkdir(parents=True, exist_ok=True)

    dest = voice_dir / "reference.wav"
    shutil.copy2(sample_path, dest)

    voice = {
        "id": voice_id,
        "name": name.strip(),
        "status": "uploaded",
        "language": "en",
        "duration_seconds": round(duration_seconds, 2),
        "created_at": _now(),
        "sample_filename": "reference.wav",
        "sample_path": str(dest),
        "conditioning_path": str(voice_dir / "conditioning.pth"),
    }
    voices = _read_all()
    voices.append(voice)
    _write_all(voices)
    return voice


def mark_ready(voice_id: str) -> Optional[dict[str, Any]]:
    voices = _read_all()
    for voice in voices:
        if voice["id"] == voice_id:
            voice["status"] = "ready"
            voice["trained_at"] = _now()
            _write_all(voices)
            return voice
    return None


def delete_voice(voice_id: str) -> bool:
    voices = _read_all()
    kept = [v for v in voices if v["id"] != voice_id]
    if len(kept) == len(voices):
        return False
    _write_all(kept)
    voice_dir = VOICES_DIR / voice_id
    if voice_dir.exists():
        shutil.rmtree(voice_dir)
    return True
