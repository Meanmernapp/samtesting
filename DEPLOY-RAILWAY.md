# Deploy with Railway

Recommended setup:

| Service | Railway service | URL |
|---------|-----------------|-----|
| AI backend | `voiceai-api` | `https://voiceai-api-production.up.railway.app` |
| UI (optional) | `voiceai-ui` | `https://voiceai-ui-production.up.railway.app` |

You can also keep the UI on **Vercel** and only run the backend on Railway.

---

## Prerequisites

1. Code pushed to **GitHub**
2. Account at [railway.app](https://railway.app)
3. Credit card on Railway (required for volumes / sustained usage)

---

## Part 1 — Deploy the AI backend

### 1. Create project
- Railway dashboard → **New Project** → **Deploy from GitHub repo**
- Select your repository

### 2. Configure the backend service
Railway may auto-create a service. Click it → **Settings**:

| Setting | Value |
|---------|--------|
| **Root Directory** | `ai` |
| **Builder** | Dockerfile (auto-detected via `ai/railway.toml`) |

### 3. Environment variables
**Variables** tab → add:

| Variable | Value |
|----------|-------|
| `COQUI_TOS_AGREED` | `1` |
| `VOICEAI_DATA_DIR` | `/data` |
| `CORS_ORIGINS` | Your frontend URL (set after Part 2) |

Railway sets `PORT` automatically — no need to configure it.

### 4. Persistent volume (important)
Without this, uploaded voices are lost on redeploy.

- Service → **Volumes** → **Add Volume**
- Mount path: `/data`
- Attach to the `voiceai-api` service

### 5. Public URL
- **Settings** → **Networking** → **Generate Domain**
- Copy the URL, e.g. `https://voiceai-api-production.up.railway.app`

Test: `https://YOUR-URL/api/health` → `"status": "ok"`

### 6. Resources (recommended for XTTS)
- **Settings** → increase memory to **4–8 GB** if available on your plan
- CPU-only works but TTS is slow (30s–3min per generation)

---

## Part 2 — Deploy the UI

### Option A — UI also on Railway (all-in-one)

1. In the same Railway project → **New** → **GitHub Repo** → same repo
2. **Settings** → **Root Directory**: `voiceai-studio-vercel-source`
3. Edit `voiceai-studio-vercel-source/config.js` **before deploy**:

```javascript
window.VOICEAI_API_URL = 'https://voiceai-api-production.up.railway.app';
```

4. **Networking** → **Generate Domain** for the UI service
5. Back on the **backend** service → set `CORS_ORIGINS` to the UI Railway URL
6. Redeploy backend if needed

**Send your client the UI Railway URL.**

### Option B — UI on Vercel, backend on Railway

1. Edit `voiceai-studio-vercel-source/config.js`:

```javascript
window.VOICEAI_API_URL = 'https://voiceai-api-production.up.railway.app';
```

2. Deploy `voiceai-studio-vercel-source/` to Vercel (root directory = that folder)
3. Set backend `CORS_ORIGINS` = `https://your-app.vercel.app`

**Send your client the Vercel URL.**

---

## Part 3 — Verify

1. Open your UI URL
2. **API** tab → **Online**
3. **Voice Lab** → upload → train (first run downloads ~1.8 GB model)
4. **Text To Speech** → generate → download

---

## Railway vs local differences

| Item | Note |
|------|------|
| First deploy build | 10–20 minutes (PyTorch + deps) |
| First voice training | 5–15 minutes (XTTS model download) |
| Idle | Railway does not spin down like Render free tier, but costs accrue while running |
| Logs | Service → **Deployments** → view logs |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Build fails | Check **Deployments** logs; ensure Root Directory is `ai` |
| API Offline | Confirm domain generated; test `/api/health` directly |
| CORS error | `CORS_ORIGINS` must exactly match UI URL (https, no trailing slash) |
| OOM / crash during training | Increase service memory in Railway settings |
| Voices lost after redeploy | Volume must be mounted at `/data` |

---

## Cost ballpark

Railway bills by usage (CPU, RAM, disk). A small always-on backend with 4 GB RAM is typically **~$5–20/month** depending on traffic. Check [railway.app/pricing](https://railway.app/pricing).
