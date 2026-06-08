import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS, GENERATED_DIR, VOICES_DIR
from app.routes import tts, voices
from app.services import xtts_service

os.environ.setdefault("COQUI_TOS_AGREED", "1")


@asynccontextmanager
async def lifespan(app: FastAPI):
    VOICES_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    if os.getenv("VOICEAI_WARMUP", "false").lower() == "true":
        xtts_service.warmup()
    yield


app = FastAPI(
    title="VoiceAI Studio API",
    description="XTTS v2 voice cloning and text-to-speech backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS if o.strip()],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voices.router)
app.include_router(tts.router)
