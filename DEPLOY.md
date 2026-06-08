# Deploy VoiceAI Studio (client demo link)

Split deployment: **Vercel** hosts the UI, **Render** hosts the AI backend.

```
Browser  →  https://your-app.vercel.app     (UI)
                ↓ API calls
           https://your-api.onrender.com     (XTTS backend)
```

---

## Before you start

1. Push the project to **GitHub** (whole `TTS Voice AI App` folder).
2. Expect **slow first run** on the server (downloads ~1.8 GB XTTS model).
3. CPU hosting: voice training and TTS can take **1–5 minutes** per action.
4. Uploaded voices need a **persistent disk** on the backend (Render Starter or above).

---

## Part 1 — Deploy the AI backend (Render)

### 1. Create a Render account
Go to [render.com](https://render.com) and sign in with GitHub.

### 2. New Web Service
- **New +** → **Web Service**
- Connect your GitHub repo
- Settings:

| Field | Value |
|-------|-------|
| Name | `voiceai-api` |
| Region | Closest to your client |
| Branch | `main` |
| Root Directory | `ai` |
| Runtime | **Docker** |
| Instance type | **Starter** ($7/mo) or higher — needed for disk + always-on |

### 3. Environment variables

| Key | Value |
|-----|-------|
| `COQUI_TOS_AGREED` | `1` |
| `CORS_ORIGINS` | `https://YOUR-APP.vercel.app` (fill in after Part 2) |
| `VOICEAI_DATA_DIR` | `/data` |

### 4. Persistent disk
- **Disks** → Add disk
- Mount path: `/data`
- Size: 5 GB (minimum)

### 5. Deploy
Click **Create Web Service**. Wait for the build (10–20 min first time).

### 6. Copy your backend URL
Example: `https://voiceai-api.onrender.com`

Test: open `https://voiceai-api.onrender.com/api/health` — should return `"status": "ok"`.

---

## Part 2 — Deploy the UI (Vercel)

### 1. Set production API URL
Edit `voiceai-studio-vercel-source/config.js`:

```javascript
window.VOICEAI_API_URL = 'https://voiceai-api.onrender.com';
```

Use your real Render URL (no trailing slash).

### 2. Deploy on Vercel
- Go to [vercel.com](https://vercel.com) → **Add New Project**
- Import the same GitHub repo
- Settings:

| Field | Value |
|-------|-------|
| Framework Preset | **Other** |
| Root Directory | `voiceai-studio-vercel-source` |
| Build Command | *(leave empty)* |
| Output Directory | `.` |

Click **Deploy**.

### 3. Copy your frontend URL
Example: `https://voiceai-studio.vercel.app`

### 4. Update backend CORS
Back on **Render** → your web service → **Environment**:
- Set `CORS_ORIGINS` to your Vercel URL, e.g. `https://voiceai-studio.vercel.app`
- Save (triggers redeploy)

---

## Part 3 — Verify end-to-end

1. Open your Vercel URL
2. **API** tab → should show **Online**
3. **Voice Lab** → upload 6–30s audio → train
4. **Text To Speech** → generate → play / download

**Send your client the Vercel URL only.**

---

## Client demo expectations

| Item | Note |
|------|------|
| First voice training | May take 5–15 min (model download) |
| TTS generation | 30s–3min on CPU |
| Free Render tier | Spins down when idle; first visit is slow |
| Voices | Lost if you skip persistent disk |

---

## Alternatives

| Platform | Use for |
|----------|---------|
| **Railway** | Backend (Docker + volume), similar to Render |
| **Fly.io** | Backend with volume |
| **RunPod / GPU VPS** | Faster TTS if client needs speed |

Railway: New Project → Deploy from GitHub → set root to `ai` → add volume at `/data`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| API shows Offline | Check Render service is running; `config.js` URL correct |
| CORS error in browser | `CORS_ORIGINS` on Render must match Vercel URL exactly |
| Training fails | Check Render logs; ensure disk mounted at `/data` |
| Very slow | Normal on CPU; upgrade to GPU instance for production |

Render logs: Dashboard → your service → **Logs**.
