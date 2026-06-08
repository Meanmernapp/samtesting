import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models import TrainResponse, VoiceResponse
from app.services import audio_utils, voice_store, xtts_service

router = APIRouter(prefix="/api/voices", tags=["voices"])


def _to_response(voice: dict) -> VoiceResponse:
    return VoiceResponse(
        id=voice["id"],
        name=voice["name"],
        status=voice["status"],
        language=voice.get("language", "en"),
        duration_seconds=voice.get("duration_seconds"),
        created_at=voice["created_at"],
        sample_filename=voice["sample_filename"],
    )


@router.get("", response_model=list[VoiceResponse])
def list_voices(ready_only: bool = False):
    return [_to_response(v) for v in voice_store.list_voices(ready_only=ready_only)]


@router.get("/{voice_id}", response_model=VoiceResponse)
def get_voice(voice_id: str):
    voice = voice_store.get_voice(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    return _to_response(voice)


@router.post("", response_model=VoiceResponse)
async def upload_voice(
    name: str = Form(...),
    file: UploadFile = File(...),
):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Voice name is required")

    suffix = Path(file.filename or "sample.mp3").suffix or ".mp3"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        tmp.write(content)
        tmp_path = Path(tmp.name)

    wav_tmp = tmp_path.with_suffix(".wav")
    try:
        duration = audio_utils.to_wav(tmp_path, wav_tmp)
        voice = voice_store.create_voice(name=name, sample_path=wav_tmp, duration_seconds=duration)
        return _to_response(voice)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        tmp_path.unlink(missing_ok=True)
        wav_tmp.unlink(missing_ok=True)


@router.post("/{voice_id}/train", response_model=TrainResponse)
def train_voice(voice_id: str):
    voice = voice_store.get_voice(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")

    reference = Path(voice["sample_path"])
    conditioning = Path(voice["conditioning_path"])

    try:
        xtts_service.prepare_voice(reference, conditioning)
        voice_store.mark_ready(voice_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Voice training failed: {exc}") from exc

    return TrainResponse(
        id=voice_id,
        name=voice["name"],
        status="ready",
        message="Voice cloned and ready for text-to-speech.",
    )


@router.delete("/{voice_id}")
def delete_voice(voice_id: str):
    if not voice_store.delete_voice(voice_id):
        raise HTTPException(status_code=404, detail="Voice not found")
    return {"ok": True}
