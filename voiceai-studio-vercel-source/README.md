# VoiceAI Studio Demo

ElevenLabs-style voice cloning SaaS demo UI.

## Features

- Text to Speech screen
- Voice Library screen
- Voice Lab screen
- Dubbing screen
- API Dashboard screen
- History screen
- Settings screen
- Functional sidebar navigation
- Static HTML/CSS/JS
- Vercel-ready deployment

## Deploy on Vercel

1. Create a new GitHub repository.
2. Upload `index.html`, `vercel.json`, and `README.md`.
3. Go to Vercel.
4. Click **Add New Project**.
5. Import your GitHub repository.
6. Framework preset: **Other**.
7. Click **Deploy**.

## Client Demo Note

This UI connects to the XTTS v2 backend in `../ai/`. Set the API URL in **Settings** (default: `http://localhost:8000`).

For local dev, run the backend (`cd ai && python run.py`) then open this folder with any static server or open `index.html` directly.
