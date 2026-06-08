import os
import threading
from pathlib import Path
from typing import Optional

import torch

from app.config import XTTS_MODEL

_model = None
_model_lock = threading.Lock()
_device = "cuda" if torch.cuda.is_available() else "cpu"


def get_device() -> str:
    return _device


def _load_model():
    global _model
    if _model is not None:
        return _model

    with _model_lock:
        if _model is not None:
            return _model

        os.environ.setdefault("COQUI_TOS_AGREED", "1")
        from TTS.api import TTS

        _model = TTS(XTTS_MODEL).to(_device)
        return _model


def prepare_voice(reference_wav: Path, conditioning_path: Path) -> None:
    """Pre-compute speaker conditioning latents (Voice Lab 'training' step)."""
    tts = _load_model()
    model = tts.synthesizer.tts_model

    gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(
        audio_path=[str(reference_wav)]
    )
    payload = {
        "gpt_cond_latent": gpt_cond_latent.cpu(),
        "speaker_embedding": speaker_embedding.cpu(),
    }
    torch.save(payload, conditioning_path)


def synthesize(
    text: str,
    reference_wav: Path,
    output_path: Path,
    language: str = "en",
    conditioning_path: Optional[Path] = None,
) -> None:
    tts = _load_model()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if conditioning_path and conditioning_path.exists():
        payload = torch.load(conditioning_path, map_location=_device)
        model = tts.synthesizer.tts_model
        out = model.inference(
            text,
            language,
            gpt_cond_latent=payload["gpt_cond_latent"].to(_device),
            speaker_embedding=payload["speaker_embedding"].to(_device),
        )
        import torchaudio

        torchaudio.save(str(output_path), torch.tensor(out["wav"]).unsqueeze(0), 24000)
        return

    tts.tts_to_file(
        text=text,
        speaker_wav=str(reference_wav),
        language=language,
        file_path=str(output_path),
    )


def warmup() -> dict:
    """Load model into memory. Call on startup for faster first request."""
    tts = _load_model()
    return {"model": XTTS_MODEL, "device": _device, "loaded": tts is not None}
