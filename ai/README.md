# VoiceAI AI Backend (XTTS v2)

FastAPI service for voice upload, cloning, and text-to-speech using **Coqui XTTS v2**.

## Model

- **Model:** `tts_models/multilingual/multi-dataset/xtts_v2`
- **Size:** ~1.8 GB (downloaded automatically on first use)
- **Cloning:** Few-shot — upload 6–30 seconds of clear speech (MP3/WAV). No fine-tuning required.
- **"Training"** in Voice Lab pre-computes speaker embeddings for faster TTS.

## Prerequisites

- Python 3.11
- **FFmpeg** (required for MP3 conversion)
- Optional: NVIDIA GPU + CUDA for faster inference

### Windows FFmpeg

```powershell
winget install Gyan.FFmpeg
```

## Local setup

```powershell
cd ai
.\install.ps1      # one-time: creates venv, installs torch + coqui-tts
.\run-server.ps1   # start API (no Activate.ps1 needed)
```

Uses **coqui-tts** (community fork) which supports Python 3.12. The old `TTS` package only works on Python 3.11 and below.

API runs at `http://localhost:8000`. Docs: `http://localhost:8000/docs`

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/voices` | Upload voice sample + name |
| POST | `/api/voices/{id}/train` | Clone / prepare voice |
| GET | `/api/voices` | List all voices |
| POST | `/api/tts/generate` | Generate speech |
| GET | `/api/audio/{filename}` | Download generated WAV |
| GET | `/api/history` | Generation history |
| GET | `/api/health` | Health check |

## Docker

```bash
docker compose up --build
```

## Deployment (share with client)

Recommended split:

1. **Frontend** → [Vercel](https://vercel.com) (static `voiceai-studio-vercel-source/`)
2. **Backend** → [Railway](https://railway.app), [Render](https://render.com), or a VPS with Docker

### Railway / Render steps

1. Push this repo to GitHub
2. Create a new service from `ai/Dockerfile`
3. Set env vars: `COQUI_TOS_AGREED=1`, `CORS_ORIGINS=https://your-app.vercel.app`
4. Add a persistent volume mounted at `/data`
5. Deploy Vercel frontend; in **Settings** tab set API URL to your backend URL

### GPU hosting (faster)

For production-quality speed, deploy the Docker image on:

- [RunPod](https://runpod.io)
- [Baseten](https://baseten.co)
- Any VPS with NVIDIA GPU

CPU works for MVP demos but first generation can take 30–90 seconds.
