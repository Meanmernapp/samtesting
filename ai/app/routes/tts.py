import re
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import GENERATED_DIR
from app.models import HistoryItem, TTSRequest, TTSResponse
from app.services import history_store, voice_store, xtts_service

router = APIRouter(prefix="/api", tags=["tts"])


def _safe_filename(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text[:40]).strip("_").lower() or "output"
    return f"{slug}.wav"


@router.post("/tts/generate", response_model=TTSResponse)
def generate_speech(body: TTSRequest):
    voice = voice_store.get_voice(body.voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    if voice.get("status") != "ready":
        raise HTTPException(
            status_code=400,
            detail="Voice is not trained yet. Complete training in Voice Lab first.",
        )

    gen_id = str(uuid.uuid4())
    filename = f"{gen_id}_{_safe_filename(body.text)}"
    output_path = GENERATED_DIR / filename

    reference = Path(voice["sample_path"])
    conditioning = Path(voice.get("conditioning_path", ""))

    try:
        xtts_service.synthesize(
            text=body.text,
            reference_wav=reference,
            output_path=output_path,
            language=body.language,
            conditioning_path=conditioning if conditioning.exists() else None,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {exc}") from exc

    entry = history_store.add_entry(
        voice_id=voice["id"],
        voice_name=voice["name"],
        text=body.text,
        filename=filename,
    )

    return TTSResponse(
        id=entry["id"],
        voice_id=voice["id"],
        voice_name=voice["name"],
        text_preview=entry["text_preview"],
        audio_url=f"/api/audio/{filename}",
        filename=filename,
        created_at=entry["created_at"],
    )


@router.get("/history", response_model=list[HistoryItem])
def get_history():
    items = history_store.list_history()
    return [
        HistoryItem(
            id=item["id"],
            voice_id=item["voice_id"],
            voice_name=item["voice_name"],
            text_preview=item["text_preview"],
            audio_url=f"/api/audio/{item['filename']}",
            filename=item["filename"],
            created_at=item["created_at"],
        )
        for item in items
    ]


@router.get("/audio/{filename}")
def get_audio(filename: str):
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    path = GENERATED_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(path, media_type="audio/wav", filename=filename)


@router.get("/health")
def health():
    return {
        "status": "ok",
        "device": xtts_service.get_device(),
        "model": "xtts_v2",
    }
