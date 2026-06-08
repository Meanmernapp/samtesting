import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("VOICEAI_DATA_DIR", BASE_DIR / "data"))
VOICES_DIR = DATA_DIR / "voices"
GENERATED_DIR = DATA_DIR / "generated"
VOICES_DB = DATA_DIR / "voices.json"

XTTS_MODEL = os.getenv("XTTS_MODEL", "tts_models/multilingual/multi-dataset/xtts_v2")
DEFAULT_LANGUAGE = os.getenv("XTTS_DEFAULT_LANGUAGE", "en")
HOST = os.getenv("VOICEAI_HOST", "0.0.0.0")
# Render/Railway inject PORT; VOICEAI_PORT is the local override.
PORT = int(os.getenv("PORT", os.getenv("VOICEAI_PORT", "8000")))
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500,https://*.vercel.app",
).split(",")

MIN_SAMPLE_SECONDS = 3
MAX_SAMPLE_SECONDS = 60
IDEAL_SAMPLE_SECONDS = (6, 30)
