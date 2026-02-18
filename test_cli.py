"""
AARVIS CLI Test — Test the agent pipeline from the command line.
Run: python test_cli.py

This lets you chat with AARVIS in your terminal without needing
the FastAPI server, browser, or WebSocket connection.
TTS is optional — it will speak responses if Kokoro is installed.
Voice mode: type 'voice on' to use microphone input (STT) + spoken output (TTS).
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent.graph import agent
from database import init_db, get_user_by_username, save_conversation, get_recent_context
import uuid


def clean_messages_for_history(messages):
    """Collapse tool interactions into the final AI response.
    Keeps tool results (like event_ids) in context so the model can
    reference them in follow-up turns, while removing raw tool_call
    structures that confuse the model."""
    cleaned = []
    pending_tool_results = []

    for m in messages:
        if isinstance(m, ToolMessage):
            # Collect tool results to fold into the next AI message
            tool_name = getattr(m, 'name', 'tool')
            pending_tool_results.append(f"[{tool_name} result: {m.content}]")
            continue
        if isinstance(m, AIMessage) and m.tool_calls:
            # Skip intermediate AI messages that triggered tool calls
            continue
        if isinstance(m, AIMessage):
            # Final AI response — attach any pending tool results so
            # the model remembers data like event_ids next turn
            if pending_tool_results:
                context = "\n".join(pending_tool_results)
                cleaned.append(AIMessage(content=f"{context}\n\n{m.content}"))
                pending_tool_results = []
            else:
                cleaned.append(m)
        elif isinstance(m, HumanMessage):
            cleaned.append(m)

    return cleaned


# ── Configuration ──────────────────────────────────────────────
TEST_USERNAME = None        # Set to a real username from your DB, or None to pick interactively
ENABLE_TTS = False          # Set True to hear responses via Kokoro
ENABLE_VOICE = False        # Set True for full voice mode (STT input + TTS output)
LOAD_HISTORY = True         # Load recent conversation history from DB
SAVE_HISTORY = True         # Persist this session to conversation_history table
# ───────────────────────────────────────────────────────────────


# ── STT (Speech-to-Text) via faster_whisper ────────────────────
_whisper_model = None

def _get_whisper_model():
    """Lazy-load faster_whisper model (base, CPU, int8)."""
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel
        print("⏳ Loading Whisper model (base, CPU, int8)...")
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        print("✅ Whisper model loaded.")
    return _whisper_model


def listen_from_mic() -> str | None:
    """Record from microphone until silence, then transcribe with faster_whisper.
    Returns transcribed text, or None on failure."""
    import pyaudio
    import wave
    import tempfile
    import struct
    import math

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    SILENCE_THRESHOLD = 500      # RMS amplitude below which = silence
    SILENCE_DURATION = 1.5       # seconds of silence to stop recording
    MAX_RECORD_SECONDS = 15      # hard cap

    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                            input=True, frames_per_buffer=CHUNK)
    except Exception as e:
        print(f"  [!] Microphone error: {e}")
        audio.terminate()
        return None

    print("\n🎤 Listening... (speak now, silence to stop)", flush=True)
    frames = []
    silent_chunks = 0
    chunks_per_sec = RATE // CHUNK
    silence_limit = int(SILENCE_DURATION * chunks_per_sec)
    max_chunks = int(MAX_RECORD_SECONDS * chunks_per_sec)
    started_speaking = False

    try:
        for _ in range(max_chunks):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            # Calculate RMS for voice activity detection
            samples = struct.unpack(f"<{CHUNK}h", data)
            rms = math.sqrt(sum(s * s for s in samples) / CHUNK)

            if rms > SILENCE_THRESHOLD:
                started_speaking = True
                silent_chunks = 0
            else:
                silent_chunks += 1

            # Stop after sustained silence (only if user already spoke)
            if started_speaking and silent_chunks >= silence_limit:
                break
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()

    if not started_speaking or len(frames) < chunks_per_sec * 0.3:
        print("\r[!] No speech detected.")
        audio.terminate()
        return None

    # Write to temp WAV and transcribe
    print("⏳ Transcribing...", end="", flush=True)
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            wf = wave.open(tmp_path, "wb")
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))
            wf.close()

        model = _get_whisper_model()
        segments, _ = model.transcribe(tmp_path, beam_size=5, language="en")
        text = " ".join(seg.text.strip() for seg in segments).strip()

        import os
        os.unlink(tmp_path)
    except Exception as e:
        print(f"\r[!] Transcription error: {e}")
        audio.terminate()
        return None
    finally:
        audio.terminate()

    if not text:
        print("\r[!] Could not understand audio.")
        return None

    print(f"\r🎤 You (voice): {text}")
    return text
# ────────────────────────────────────────────────────────────────


def get_test_user():
    """Get a user for testing — either from config or by prompting."""
    global TEST_USERNAME

    if TEST_USERNAME:
        user = get_user_by_username(TEST_USERNAME)
        if user:
            return user
        print(f"[!] User '{TEST_USERNAME}' not found in database.")

    # Try to list existing users
    import sqlite3
    from database import DB_PATH
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT username, full_name, location, interests FROM users")
        users = cursor.fetchall()
        conn.close()

        if users:
            print("\n📋 Available users in database:")
            for i, (uname, fname, loc, interests) in enumerate(users, 1):
                print(f"  {i}. {uname} ({fname}) — {loc}, interests: {interests or 'none'}")
            print()

            choice = input("Enter username (or number): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(users):
                chosen = users[int(choice) - 1][0]
            else:
                chosen = choice

            user = get_user_by_username(chosen)
            if user:
                return user
            print(f"[!] User '{chosen}' not found.")
        else:
            print("[!] No users in database. Register one via the web UI first,")
            print("    or run: python -c \"from database import create_user; create_user('test','test@test.com','pass123','Test User','Kathmandu','technology')\"")
    except Exception as e:
        print(f"[!] Could not query users: {e}")

    return None


def speak(text: str):
    """Optional TTS output."""
    if not ENABLE_TTS:
        return
    try:
        from services.tts_service import speak as tts_speak
        tts_speak(text)
    except Exception as e:
        print(f"  [TTS error: {e}]")


def run_cli():
    global ENABLE_TTS, ENABLE_VOICE

    print("=" * 60)
    print("  🤖 AARVIS CLI Test Mode")
    print("=" * 60)
    print()

    # Initialize DB
    init_db()

    # Get user
    user = get_test_user()
    if not user:
        print("\n[ERROR] No valid user. Exiting.")
        sys.exit(1)

    first_name = user['full_name'].split()[0]
    session_id = str(uuid.uuid4())

    print(f"\n✅ Logged in as: {user['full_name']} ({user['username']})")
    print(f"   Location: {user.get('location', 'N/A')}")
    print(f"   Interests: {user.get('interests', 'N/A')}")
    print(f"   Session: {session_id[:8]}...")
    print()

    # Seed message history from DB
    messages = []
    if LOAD_HISTORY:
        recent = get_recent_context(user['id'], limit=10)
        for m in recent:
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            else:
                messages.append(AIMessage(content=m["content"]))
        if recent:
            print(f"📜 Loaded {len(recent)} messages from conversation history\n")

    print(f"Hello {first_name}! Type your message below.")
    print("Commands: 'quit', 'clear', 'tts on/off', 'voice on/off', 'history'\n")
    print("-" * 60)

    while True:
        try:
            if ENABLE_VOICE:
                user_text = listen_from_mic()
                if user_text is None:
                    continue  # retry listening
            else:
                user_text = input(f"\n🧑 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if not user_text:
            continue

        # Handle special commands
        if user_text.lower() in ('quit', 'exit', 'q'):
            print("\nGoodbye! 👋")
            break

        if user_text.lower() == 'clear':
            messages = []
            print("🗑️  Conversation history cleared.\n")
            continue

        if user_text.lower() == 'tts on':
            ENABLE_TTS = True
            print("🔊 TTS enabled.\n")
            continue

        if user_text.lower() == 'tts off':
            ENABLE_TTS = False
            print("🔇 TTS disabled.\n")
            continue

        if user_text.lower() == 'voice on':
            ENABLE_VOICE = True
            ENABLE_TTS = True
            print("🎙️  Voice mode ON — mic input + spoken output. Say 'voice off' to stop.\n")
            continue

        if user_text.lower() == 'voice off':
            ENABLE_VOICE = False
            print("🎙️  Voice mode OFF — back to text input.\n")
            continue

        if user_text.lower() == 'history':
            print("\n📜 Current conversation:")
            for m in messages:
                role = "You" if isinstance(m, HumanMessage) else "AARVIS"
                print(f"  [{role}] {m.content[:100]}{'...' if len(m.content) > 100 else ''}")
            print()
            continue

        # Persist user message
        if SAVE_HISTORY:
            save_conversation(user['id'], session_id, "user", user_text)

        messages.append(HumanMessage(content=user_text))

        print("\n⏳ Thinking...", end="", flush=True)

        try:
            result = agent.invoke({
                "messages": messages,
                "current_user": user['username'],
                "user_id": user['id'],
                "session_id": session_id,
                "user_location": user.get('location', 'Kathmandu'),
                "user_interests": user.get('interests', 'technology'),
                "voice_state": "thinking",
                "pending_confirmation": None,
                "pending_action": None,
                "draft_email": None,
                "final_response": None,
                "error": None,
            })

            final_messages = result["messages"]
            response_text = final_messages[-1].content if final_messages else "No response."

            # Update in-memory history — keep only human/AI text, strip tool messages
            messages = clean_messages_for_history(result["messages"])

            # Persist assistant response
            if SAVE_HISTORY:
                save_conversation(
                    user['id'], session_id, "assistant", response_text,
                    agent_type="AARVIS"
                )

            # Show tool calls if any were made
            tool_msgs = [m for m in result["messages"] if hasattr(m, 'tool_calls') and m.tool_calls]
            if tool_msgs:
                for tm in tool_msgs:
                    for tc in tm.tool_calls:
                        print(f"\r🔧 Tool called: {tc['name']}({tc.get('args', {})})")

            print(f"\r🤖 AARVIS: {response_text}")

            # Optional TTS
            speak(response_text)

        except Exception as e:
            print(f"\r❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    run_cli()
