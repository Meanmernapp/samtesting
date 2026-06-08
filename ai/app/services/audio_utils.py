from pathlib import Path

from pydub import AudioSegment

from app.config import MAX_SAMPLE_SECONDS, MIN_SAMPLE_SECONDS


def to_wav(source_path: Path, dest_path: Path) -> float:
    """Convert uploaded audio to mono 24kHz WAV. Returns duration in seconds."""
    audio = AudioSegment.from_file(str(source_path))
    duration = len(audio) / 1000.0

    if duration < MIN_SAMPLE_SECONDS:
        raise ValueError(
            f"Audio too short ({duration:.1f}s). Provide at least {MIN_SAMPLE_SECONDS}s of clear speech."
        )
    if duration > MAX_SAMPLE_SECONDS:
        raise ValueError(
            f"Audio too long ({duration:.1f}s). Trim to under {MAX_SAMPLE_SECONDS}s for MVP."
        )

    audio = audio.set_channels(1).set_frame_rate(24000)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    audio.export(str(dest_path), format="wav")
    return duration


def wav_duration(path: Path) -> float:
    audio = AudioSegment.from_file(str(path))
    return len(audio) / 1000.0
