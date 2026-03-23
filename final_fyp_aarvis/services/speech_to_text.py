"""Speech to text helpers."""

from __future__ import annotations

import os
import tempfile

_whisper_model = None


def _get_whisper_model():
    """Load and cache Whisper model."""
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel

        print("[STT] Loading Whisper model (base, CPU, int8)...")
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        print("[STT] Whisper model loaded.")
    return _whisper_model


def transcribe_audio_bytes(audio_bytes: bytes) -> str | None:
    """Transcribe audio bytes to text."""
    try:
        model = _get_whisper_model()
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        segments, _ = model.transcribe(temp_path, beam_size=5, language="en")
        text = " ".join(segment.text.strip() for segment in segments).strip()
        os.unlink(temp_path)
        return text if text else None
    except Exception as exc:
        print(f"[STT] Error: {exc}")
        return None
