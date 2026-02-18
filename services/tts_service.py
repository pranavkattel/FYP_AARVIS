import numpy as np


# Cache the Kokoro pipeline so it's only loaded once
_kokoro_pipeline = None

def _get_pipeline():
    global _kokoro_pipeline
    if _kokoro_pipeline is None:
        from kokoro import KPipeline
        _kokoro_pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
    return _kokoro_pipeline


def speak(text: str, voice: str = 'af_heart', speed: float = 1.0) -> None:
    """
    Convert text to speech using Kokoro TTS and play it through speakers.
    Runs fully locally — no internet required.

    Args:
        text: The text to speak aloud
        voice: Kokoro voice ID. American English options: 'af_heart', 'af_sky', 'af_bella'
        speed: Speech speed multiplier (1.0 = normal, 1.2 = slightly faster)
    """
    try:
        import sounddevice as sd

        pipeline = _get_pipeline()
        generator = pipeline(text, voice=voice, speed=speed, split_pattern=r'\n+')

        for i, (gs, ps, audio) in enumerate(generator):
            # audio is a numpy float32 array, sample rate is 24000 Hz
            sd.play(audio, samplerate=24000)
            sd.wait()  # block until audio finishes before playing next chunk

    except ImportError as ie:
        print(f"[TTS] Missing dependency: {ie}. Run: pip install kokoro sounddevice")
    except Exception as e:
        print(f"[TTS] Error: {e}")


async def speak_async(text: str, voice: str = 'af_heart', speed: float = 1.0) -> None:
    """
    Async wrapper for speak() — use this from FastAPI/async contexts.
    Runs speak() in a thread pool to avoid blocking the event loop.
    """
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, speak, text, voice, speed)


def get_audio_bytes(text: str, voice: str = 'af_heart', speed: float = 1.0) -> bytes:
    """
    Generate TTS audio and return as raw bytes (WAV format).
    Use this if you need to stream audio to the frontend instead of playing locally.
    """
    import io
    import wave

    try:
        pipeline = _get_pipeline()
        all_audio = []

        for i, (gs, ps, audio) in enumerate(pipeline(text, voice=voice, speed=speed)):
            all_audio.append(audio)

        if not all_audio:
            return b""

        combined = np.concatenate(all_audio)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)      # 16-bit
            wf.setframerate(24000)
            wf.writeframes((combined * 32767).astype(np.int16).tobytes())
        return buf.getvalue()

    except Exception as e:
        print(f"[TTS] get_audio_bytes error: {e}")
        return b""
