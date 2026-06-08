# VoiceAI Studio MVP

ElevenLabs-style voice cloning app with **XTTS v2** backend.

## What's included

| Part | Folder | Purpose |
|------|--------|---------|
| UI | `voiceai-studio-vercel-source/` | Static web app (Vercel-ready) |
| AI API | `ai/` | FastAPI + XTTS v2 voice clone & TTS |

## Quick start (local)

### 1. Start the AI backend

```powershell
cd ai
.\install.ps1      # one-time setup
.\run-server.ps1   # start API every time
```

Install FFmpeg first if you plan to upload MP3 files.

### 2. Open the UI

Open `voiceai-studio-vercel-source/index.html` in a browser, or serve it:

```powershell
cd voiceai-studio-vercel-source
python -m http.server 5500
```

Go to **Settings** and set API URL to `http://localhost:8000`.

### 3. Use the app

1. **Voice Lab** — upload a 6–30s voice sample (MP3/WAV), name it, click **Start Voice Training**
2. **Text To Speech** — pick your cloned voice, enter text, **Generate Voice**, then play/download
3. **Voice Library** / **History** — view saved voices and past generations

## Deploy for your client

```
┌─────────────────┐      HTTPS       ┌──────────────────┐
│  Vercel (UI)    │ ───────────────► │  Railway/Render  │
│  static HTML    │   API calls      │  Docker + XTTS   │
└─────────────────┘                  └──────────────────┘
```

1. Deploy `voiceai-studio-vercel-source/` to Vercel (framework: **Other**)
2. Deploy `ai/` via Docker on Railway or Render
3. Set `CORS_ORIGINS` on backend to your Vercel URL
4. In the app **Settings**, set the production API URL

See `DEPLOY-RAILWAY.md` for Railway deployment (recommended) or `DEPLOY.md` for Render.

See `ai/README.md` for backend details and GPU options.

## Model choice: XTTS v2

XTTS v2 is a strong MVP choice:

- Small enough for self-hosting (~1.8 GB)
- Clones from a short audio sample (no dataset training)
- 17 languages
- Open source (Coqui TTS)

Alternatives if you outgrow MVP: OpenVoice, StyleTTS2, or commercial APIs (ElevenLabs, PlayHT).
