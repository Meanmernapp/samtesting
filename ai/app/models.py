from typing import Optional

from pydantic import BaseModel, Field


class VoiceResponse(BaseModel):
    id: str
    name: str
    status: str
    language: str = "en"
    duration_seconds: Optional[float] = None
    created_at: str
    sample_filename: str


class TrainResponse(BaseModel):
    id: str
    name: str
    status: str
    message: str


class TTSRequest(BaseModel):
    voice_id: str
    text: str = Field(..., min_length=1, max_length=5000)
    language: str = "en"


class TTSResponse(BaseModel):
    id: str
    voice_id: str
    voice_name: str
    text_preview: str
    audio_url: str
    filename: str
    created_at: str


class HistoryItem(BaseModel):
    id: str
    voice_id: str
    voice_name: str
    text_preview: str
    audio_url: str
    filename: str
    created_at: str
