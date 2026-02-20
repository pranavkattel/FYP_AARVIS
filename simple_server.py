from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Cookie, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import Request
from datetime import datetime, timedelta
import json
import asyncio
import uuid
from pydantic import BaseModel
from typing import Optional
import secrets
import cv2
import numpy as np
import base64
import pickle
import os
from database import create_user, verify_user, get_user_by_username, save_conversation, get_recent_context
from langchain_core.messages import HumanMessage, AIMessage

# ── Server-side STT via faster_whisper (shared with CLI) ──
_whisper_model = None

def _get_whisper_model():
    """Lazy-load faster_whisper model (base, CPU, int8)."""
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel
        print("[STT] Loading Whisper model (base, CPU, int8)...")
        _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        print("[STT] ✅ Whisper model loaded.")
    return _whisper_model

def transcribe_audio_bytes(audio_bytes: bytes) -> str | None:
    """Transcribe raw audio bytes (WAV or webm) using faster_whisper. Returns text or None."""
    import tempfile, wave, io

    try:
        model = _get_whisper_model()

        # Browser MediaRecorder sends webm/opus — write to temp file for ffmpeg decode
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        segments, info = model.transcribe(tmp_path, beam_size=5, language="en")
        seg_list = list(segments)
        text = " ".join(seg.text.strip() for seg in seg_list).strip()

        os.unlink(tmp_path)
        return text if text else None
    except Exception as e:
        print(f"[STT] Error: {e}")
        return None

# Import calendar functions
try:
    from calender import get_todays_events, get_upcoming_events
    CALENDAR_AVAILABLE = True
    print("[DEBUG] ✅ Calendar integration loaded successfully")
except Exception as e:
    CALENDAR_AVAILABLE = False
    print(f"[DEBUG] ❌ Calendar integration not available: {e}")

# Initialize face recognition
try:
    from insightface.app import FaceAnalysis
    print("[DEBUG] Initializing InsightFace...")
    face_app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
    face_app.prepare(ctx_id=-1, det_size=(640, 640))
    FACE_RECOGNITION_AVAILABLE = True
    print("[DEBUG] ✅ Face recognition ready!")
except Exception as e:
    FACE_RECOGNITION_AVAILABLE = False
    face_app = None
    print(f"[DEBUG] ❌ Face recognition not available: {e}")

# Face database
FACE_DB_FILE = "face_database.pkl"

def load_face_database():
    if os.path.exists(FACE_DB_FILE):
        try:
            with open(FACE_DB_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            return {}
    return {}

def save_face_database(db):
    with open(FACE_DB_FILE, 'wb') as f:
        pickle.dump(db, f)

face_users_db = load_face_database()

# Face detection cache (username -> last_seen_time)
face_detection_cache = {}

app = FastAPI()
print(f"[DEBUG] Calendar available: {CALENDAR_AVAILABLE}")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Session storage (in production, use Redis or database)
sessions = {}

# Pydantic models for request validation
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    location: str
    interests: str = ""
    face_embeddings: Optional[list] = None  # Face embeddings for registration

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session_token: Optional[str] = Cookie(None)):
    # Check if user is logged in
    if not session_token or session_token not in sessions:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/api/register")
async def register(user: RegisterRequest, response: Response):
    try:
        user_id = create_user(
            username=user.username,
            email=user.email,
            password=user.password,
            full_name=user.full_name,
            location=user.location,
            interests=user.interests
        )
        
        # Save face embeddings if provided
        if user.face_embeddings and FACE_RECOGNITION_AVAILABLE:
            face_users_db[user.username] = user.face_embeddings
            save_face_database(face_users_db)
            print(f"[DEBUG] Saved {len(user.face_embeddings)} face embeddings for {user.username}")
        
        # Create session
        token = secrets.token_urlsafe(32)
        sessions[token] = user.username
        
        # Set cookie in response
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            max_age=86400,  # 24 hours
            samesite="lax"
        )
        
        return {
            "message": "User created successfully",
            "token": token,
            "username": user.username
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[DEBUG] Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/api/login")
async def login(credentials: LoginRequest, response: Response):
    user = verify_user(credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create session
    token = secrets.token_urlsafe(32)
    sessions[token] = credentials.username
    
    # Set cookie in response
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=86400,  # 24 hours
        samesite="lax"
    )
    
    return {
        "message": "Login successful",
        "token": token,
        "username": user['username'],
        "full_name": user['full_name']
    }

@app.post("/api/logout")
async def logout(session_token: Optional[str] = Cookie(None)):
    if session_token and session_token in sessions:
        del sessions[session_token]
    return {"message": "Logged out successfully"}

@app.get("/api/user")
async def get_current_user(session_token: Optional[str] = Cookie(None)):
    if not session_token or session_token not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    username = sessions[session_token]
    user = get_user_by_username(username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@app.post("/api/face/verify")
async def verify_face(request: Request):
    """Verify if a user is in front of the mirror using face recognition"""
    if not FACE_RECOGNITION_AVAILABLE:
        return {"detected": False, "message": "Face recognition not available"}
    
    try:
        data = await request.json()
        image_data = data.get('image')
        
        if not image_data:
            return {"detected": False, "message": "No image provided"}
        
        # Decode base64 image
        img_data = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect faces
        faces = face_app.get(frame)
        
        if len(faces) == 0:
            return {"detected": False, "message": "No face detected"}
        
        # Get face embedding
        test_emb = faces[0].embedding / np.linalg.norm(faces[0].embedding)
        
        # Check against all registered users
        best_match = None
        best_similarity = 0
        
        for username, embeddings in face_users_db.items():
            similarities = [np.dot(emb, test_emb) for emb in embeddings]
            avg_similarity = np.mean(similarities)
            
            if avg_similarity > best_similarity:
                best_similarity = avg_similarity
                best_match = username
        
        # Threshold for face recognition (40% similarity)
        if best_similarity > 0.4:
            # Update detection cache
            face_detection_cache[best_match] = datetime.now()
            
            return {
                "detected": True,
                "username": best_match,
                "confidence": round(float(best_similarity) * 100, 1),
                "cache_duration": 240  # 4 minutes in seconds
            }
        else:
            return {
                "detected": False,
                "message": "Unknown face",
                "confidence": round(float(best_similarity) * 100, 1)
            }
    
    except Exception as e:
        print(f"[DEBUG] Face verification error: {e}")
        return {"detected": False, "message": str(e)}

@app.post("/api/face/process")
async def process_face(request: Request):
    """Process face image and return embedding for registration"""
    if not FACE_RECOGNITION_AVAILABLE:
        return {"error": "Face recognition not available"}
    
    try:
        data = await request.json()
        image_data = data.get('image')
        
        if not image_data:
            return {"error": "No image provided"}
        
        # Decode base64 image
        img_data = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect faces
        faces = face_app.get(frame)
        
        if len(faces) == 0:
            return {"error": "No face detected"}
        
        # Get normalized embedding
        embedding = faces[0].embedding / np.linalg.norm(faces[0].embedding)
        
        return {"embedding": embedding.tolist()}
    
    except Exception as e:
        print(f"[DEBUG] Face processing error: {e}")
        return {"error": str(e)}

@app.post("/api/face/login")
async def face_login(request: Request, response: Response):
    """Login using face recognition without credentials"""
    if not FACE_RECOGNITION_AVAILABLE:
        return {"success": False, "message": "Face recognition not available"}
    
    try:
        data = await request.json()
        image_data = data.get('image')
        
        if not image_data:
            return {"success": False, "message": "No image provided"}
        
        # Decode base64 image
        img_data = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect faces
        faces = face_app.get(frame)
        
        if len(faces) == 0:
            return {"success": False, "message": "No face detected"}
        
        # Get face embedding
        test_emb = faces[0].embedding / np.linalg.norm(faces[0].embedding)
        
        # Check against all registered users
        best_match = None
        best_similarity = 0
        
        for username, embeddings in face_users_db.items():
            if not embeddings:
                continue
            similarities = [np.dot(emb, test_emb) for emb in embeddings]
            avg_similarity = np.mean(similarities)
            
            if avg_similarity > best_similarity:
                best_similarity = avg_similarity
                best_match = username
        
        # Threshold for face recognition (40% similarity)
        if best_similarity > 0.4:
            # Get user from database
            user = get_user_by_username(best_match)
            
            if not user:
                return {"success": False, "message": "User not found in database"}
            
            # Create session (same as normal login)
            token = secrets.token_urlsafe(32)
            sessions[token] = best_match
            
            # Set cookie in response
            response.set_cookie(
                key="session_token",
                value=token,
                httponly=True,
                max_age=86400,  # 24 hours
                samesite="lax"
            )
            
            # Update face detection cache
            face_detection_cache[best_match] = datetime.now()
            
            print(f"[DEBUG] Face login successful: {best_match} ({best_similarity*100:.1f}% confidence)")
            
            return {
                "success": True,
                "token": token,
                "username": user['username'],
                "full_name": user['full_name'],
                "confidence": round(float(best_similarity) * 100, 1),
                "message": f"Welcome back, {user['full_name'].split()[0]}!"
            }
        else:
            return {
                "success": False,
                "message": f"Face not recognized (confidence: {best_similarity*100:.1f}%)",
                "confidence": round(float(best_similarity) * 100, 1)
            }
    
    except Exception as e:
        print(f"[DEBUG] Face login error: {e}")
        
        return {"success": False, "message": str(e)}

@app.get("/api/face/check-cache")
async def check_face_cache(session_token: Optional[str] = Cookie(None)):
    """Check if user was recently detected (within last 4 minutes)"""
    if not session_token or session_token not in sessions:
        return {"cached": False, "message": "Not authenticated"}
    
    username = sessions[session_token]
    
    if username in face_detection_cache:
        last_seen = face_detection_cache[username]
        time_diff = (datetime.now() - last_seen).total_seconds()
        
        # Cache valid for 4 minutes (240 seconds)
        if time_diff < 240:
            return {
                "cached": True,
                "username": username,
                "seconds_remaining": int(240 - time_diff)
            }
    
    return {"cached": False, "message": "Face verification needed"}

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session_token: Optional[str] = Cookie(None),
    token: Optional[str] = None,
):
    await websocket.accept()

    # Resolve authenticated user from existing sessions dict
    auth_token = session_token or token
    if not auth_token or auth_token not in sessions:
        await websocket.send_json({"type": "error", "text": "Not authenticated"})
        await websocket.close()
        return

    username = sessions[auth_token]
    user = get_user_by_username(username)  # from database.py
    if not user:
        await websocket.send_json({"type": "error", "text": "User not found"})
        await websocket.close()
        return

    session_id = str(uuid.uuid4())

    # Import agent lazily to avoid circular imports and slow startup blocking
    from agent.graph import agent

    # Seed message history from DB — mirrors agent2_memory.py conversation_history pattern
    recent = get_recent_context(user['id'], limit=10)
    messages = []
    for m in recent:
        if m["role"] == "user":
            messages.append(HumanMessage(content=m["content"]))
        else:
            messages.append(AIMessage(content=m["content"]))

    first_name = user['full_name'].split()[0]
    await websocket.send_json({
        "type": "status",
        "state": "ready",
        "text": f"Welcome back, {first_name}!"
    })

    # ── Speak a welcome greeting via TTS ──
    try:
        from services.tts_service import get_sentence_audio_bytes
        welcome_text = f"Welcome, {first_name}!"
        welcome_wav = await asyncio.to_thread(get_sentence_audio_bytes, welcome_text)
        if welcome_wav:
            import base64 as _b64
            await websocket.send_json({"type": "tts_audio", "data": _b64.b64encode(welcome_wav).decode('ascii')})
    except Exception as e:
        print(f"[WS] Welcome TTS error (non-fatal): {e}")

    try:
        while True:
            # Accept both text (JSON) and binary (audio) messages
            ws_message = await websocket.receive()

            if ws_message.get("type") == "websocket.disconnect":
                break

            user_text = None

            if "text" in ws_message:
                data = json.loads(ws_message["text"])
                if data.get("type") == "message":
                    user_text = data.get("text", "").strip()
                elif data.get("type") == "audio":
                    # Base64-encoded audio from browser
                    audio_b64 = data.get("data", "")
                    if audio_b64:
                        await websocket.send_json({"type": "voice_state", "state": "thinking"})
                        audio_bytes = base64.b64decode(audio_b64)
                        transcript = await asyncio.to_thread(transcribe_audio_bytes, audio_bytes)
                        if transcript:
                            print(f"[VOICE] \"{transcript}\"")
                            await websocket.send_json({"type": "transcript", "text": transcript})
                            user_text = transcript
                        else:
                            await websocket.send_json({"type": "voice_state", "state": "idle"})
                            await websocket.send_json({"type": "status", "text": "Could not understand audio", "state": "ready"})
                            continue

            elif "bytes" in ws_message:
                # Raw binary audio
                audio_bytes = ws_message["bytes"]
                await websocket.send_json({"type": "voice_state", "state": "thinking"})
                transcript = await asyncio.to_thread(transcribe_audio_bytes, audio_bytes)
                if transcript:
                    print(f"[VOICE] \"{transcript}\"")
                    await websocket.send_json({"type": "transcript", "text": transcript})
                    user_text = transcript
                else:
                    await websocket.send_json({"type": "voice_state", "state": "idle"})
                    await websocket.send_json({"type": "status", "text": "Could not understand audio", "state": "ready"})
                    continue

            if not user_text:
                continue

            # ── "bye bye" → logout ──
            _bye_normalised = user_text.lower().strip().rstrip('.!?,')
            if _bye_normalised in ('bye bye', 'bye-bye', 'byebye', 'bye', 'goodbye', 'good bye', 'log out', 'logout', 'sign out'):
                try:
                    from services.tts_service import get_sentence_audio_bytes as _bye_tts
                    bye_text = f"Goodbye, {first_name}. See you later!"
                    bye_wav = await asyncio.to_thread(_bye_tts, bye_text)
                    if bye_wav:
                        await websocket.send_json({"type": "tts_audio", "data": base64.b64encode(bye_wav).decode('ascii')})
                except Exception:
                    pass
                await websocket.send_json({"type": "logout"})
                # Clean up server session
                if auth_token and auth_token in sessions:
                    del sessions[auth_token]
                break

            # Push thinking state to UI
            await websocket.send_json({"type": "voice_state", "state": "thinking"})
            await websocket.send_json({"type": "animation_start"})

            # Persist user message to conversation_history table
            save_conversation(user['id'], session_id, "user", user_text)

            # Append to in-memory history (same as agent2_memory.py pattern)
            messages.append(HumanMessage(content=user_text))

            try:
                # ── Streaming agent invocation ──────────────────────────
                # Stream tokens from the LLM and pipe completed sentences
                # to TTS immediately, so the user hears the first sentence
                # while the model is still generating the rest.
                import re as _re
                from services.tts_service import get_sentence_audio_bytes

                full_response = ""
                sentence_buffer = ""
                tts_tasks = []  # background TTS tasks (now produce audio bytes)
                sent_first_chunk = False
                final_result = None  # to capture tool messages for history
                _inside_think = False  # track <think> block state for streaming

                async for event in agent.astream_events(
                    {
                        "messages": messages,
                        "current_user": username,
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
                    },
                    version="v2",
                ):
                    kind = event.get("event")

                    # Capture token-by-token output from the LLM node
                    if kind == "on_chat_model_stream":
                        chunk = event.get("data", {}).get("chunk")
                        if chunk and hasattr(chunk, "content") and chunk.content:
                            token = chunk.content

                            # Track whether we're inside a <think> block
                            if "<think>" in token:
                                _inside_think = True
                            if _inside_think:
                                if "</think>" in token:
                                    # Extract any text after </think>
                                    token = token.split("</think>", 1)[1]
                                    _inside_think = False
                                else:
                                    continue  # skip tokens inside think block
                            if not token:
                                continue

                            full_response += token
                            sentence_buffer += token

                            # Send every token to frontend for instant display
                            await websocket.send_json({
                                "type": "response_chunk",
                                "token": token,
                                "first": not sent_first_chunk,
                            })
                            sent_first_chunk = True

                            # When a sentence boundary is hit, dispatch to TTS
                            # immediately so speech starts while LLM continues
                            sentence_match = _re.search(r'[.!?]\s', sentence_buffer)
                            if sentence_match:
                                sentence_end = sentence_match.end()
                                sentence = sentence_buffer[:sentence_end].strip()
                                sentence_buffer = sentence_buffer[sentence_end:]
                                if sentence:
                                    await websocket.send_json({"type": "voice_state", "state": "speaking"})
                                    audio_wav = await asyncio.to_thread(get_sentence_audio_bytes, sentence)
                                    if audio_wav:
                                        audio_b64 = base64.b64encode(audio_wav).decode('ascii')
                                        await websocket.send_json({"type": "tts_audio", "data": audio_b64})

                    # Capture the final state after the graph finishes
                    if kind == "on_chain_end" and event.get("name") == "LangGraph":
                        final_result = event.get("data", {}).get("output")

                # Flush any remaining text in the sentence buffer
                remaining = sentence_buffer.strip()
                # Also strip any lingering <think> blocks from full response
                full_response = _re.sub(r"<think>[\s\S]*?</think>", "", full_response).strip()
                if remaining:
                    remaining = _re.sub(r"<think>[\s\S]*?</think>", "", remaining).strip()
                    if remaining:
                        audio_wav = await asyncio.to_thread(get_sentence_audio_bytes, remaining)
                        if audio_wav:
                            audio_b64 = base64.b64encode(audio_wav).decode('ascii')
                            await websocket.send_json({"type": "tts_audio", "data": audio_b64})

                response_text = full_response if full_response else "I didn't get a response."

                # Persist assistant response
                save_conversation(
                    user['id'], session_id, "assistant", response_text,
                    agent_type="AARVIS"
                )

                # Update in-memory history for next turn
                from langchain_core.messages import ToolMessage
                result_messages = final_result.get("messages", messages) if final_result and isinstance(final_result, dict) else messages + [AIMessage(content=response_text)]
                cleaned_messages = []
                pending_tool_results = []
                for m in result_messages:
                    if isinstance(m, ToolMessage):
                        tool_name = getattr(m, 'name', 'tool')
                        pending_tool_results.append(f"[{tool_name} result: {m.content}]")
                        continue
                    if isinstance(m, AIMessage) and getattr(m, 'tool_calls', None):
                        continue
                    if isinstance(m, AIMessage):
                        if pending_tool_results:
                            context = "\n".join(pending_tool_results)
                            cleaned_messages.append(AIMessage(content=f"{context}\n\n{m.content}"))
                            pending_tool_results = []
                        else:
                            cleaned_messages.append(m)
                    elif isinstance(m, HumanMessage):
                        cleaned_messages.append(m)
                messages = cleaned_messages

            except Exception as agent_err:
                print(f"[WS] Agent error: {agent_err}")
                response_text = "I'm sorry, I encountered an error processing your request. Please try again."

            # Send final complete response + state reset
            await websocket.send_json({"type": "animation_stop"})
            await websocket.send_json({"type": "response", "text": response_text})
            await websocket.send_json({"type": "voice_state", "state": "idle"})
            await websocket.send_json({"type": "status", "text": "Ready", "state": "ready"})

    except WebSocketDisconnect:
        print(f"[WS] {username} disconnected")

@app.get("/api/weather")
async def get_weather(session_token: Optional[str] = Cookie(None)):
    """Get weather data from WeatherAPI.com based on user's location"""
    import httpx
    
    # Get user's location preference
    location = "Kathmandu"  # Default
    if session_token and session_token in sessions:
        username = sessions[session_token]
        user = get_user_by_username(username)
        if user and user.get('location'):
            location = user['location']
    
    API_KEY = "10428bba45b34ba8b4543622252612"
    # Use forecast endpoint to get min/max temps
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=1"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            data = response.json()
            
            if response.status_code == 200:
                if 'forecast' in data and 'forecastday' in data['forecast']:
                    forecast_day = data['forecast']['forecastday'][0]['day']
                    return {
                        "temp": data['current']['temp_c'],
                        "condition": data['current']['condition']['text'],
                        "location": location,
                        "temp_min": forecast_day['mintemp_c'],
                        "temp_max": forecast_day['maxtemp_c']
                    }
                else:
                    return {
                        "temp": data['current']['temp_c'],
                        "condition": data['current']['condition']['text'],
                        "location": location,
                        "temp_min": 5,
                        "temp_max": 12
                    }
            else:
                return {
                    "temp": 8,
                    "condition": "Unable to fetch weather",
                    "location": location,
                    "temp_min": 5,
                    "temp_max": 12
                }
    except Exception as e:
        print(f"[Weather] Error: {e}")
        return {
            "temp": 8,
            "condition": "Connection timeout - check internet",
            "location": location,
            "temp_min": 5,
            "temp_max": 12
        }

@app.get("/api/news")
async def get_news(session_token: Optional[str] = Cookie(None)):
    """Get top headlines from NewsAPI.org based on user interests"""
    import httpx
    
    # Get user's interests
    interests = None
    if session_token and session_token in sessions:
        username = sessions[session_token]
        user = get_user_by_username(username)
        if user and user.get('interests'):
            interests = user['interests']
    
    API_KEY = "b47750eb5d3a45cda2f4542d117a42e8"
    
    # Build URL based on interests
    if interests:
        # Use first interest as category or search query
        interest_list = [i.strip().lower() for i in interests.split(',')]
        # Try category first (business, entertainment, health, science, sports, technology)
        category = interest_list[0] if interest_list[0] in ['business', 'entertainment', 'health', 'science', 'sports', 'technology'] else None
        if category:
            url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={API_KEY}"
        else:
            # Use as search query
            url = f"https://newsapi.org/v2/everything?q={interest_list[0]}&sortBy=publishedAt&apiKey={API_KEY}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            data = response.json()
            
            if data.get("status") == "ok" and data.get("articles"):
                articles = [{"title": article["title"]} for article in data["articles"][:5]]
                return articles
            else:
                return [{"title": "Unable to fetch news at this time"}]
    except Exception as e:
        print(f"[News] Error: {e}")
        return [
            {"title": "⚠️ Unable to connect to news service"},
            {"title": "Check your internet connection or firewall settings"},
            {"title": "The application will retry automatically"}
        ]

@app.get("/api/calendar")
async def get_calendar():
    """Get today's events from Google Calendar"""
    if not CALENDAR_AVAILABLE:
        return {
            "events": [
                {"time": "09:00 AM", "endTime": "10:00 AM", "title": "Team Standup", "status": "upcoming", "startHour": 9.0, "endHour": 10.0},
                {"time": "02:00 PM", "endTime": "04:00 PM", "title": "Client Meeting", "status": "upcoming", "startHour": 14.0, "endHour": 16.0},
                {"time": "05:30 PM", "endTime": "06:30 PM", "title": "Gym Session", "status": "upcoming", "startHour": 17.5, "endHour": 18.5}
            ]
        }

    try:
        events = get_todays_events()

        if not events:
            return {"events": []}

        sorted_events = sorted(events, key=lambda e: e['start'].get('dateTime', e['start'].get('date')))

        formatted_events = []
        local_tz = datetime.now().astimezone().tzinfo
        now_local = datetime.now().astimezone()

        for event in sorted_events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            summary = event.get('summary', 'Untitled Event')

            try:
                if 'T' in start:  # dateTime format
                    start_clean = start.replace('Z', '+00:00')
                    end_clean = end.replace('Z', '+00:00')

                    try:
                        import re
                        event_time = datetime.fromisoformat(start_clean)
                        event_end_time = datetime.fromisoformat(end_clean)
                    except Exception:
                        start_naive = re.sub(r'[+-]\\d{2}:\\d{2}$', '', start)
                        end_naive = re.sub(r'[+-]\\d{2}:\\d{2}$', '', end)
                        event_time = datetime.fromisoformat(start_naive.replace('Z', ''))
                        event_end_time = datetime.fromisoformat(end_naive.replace('Z', ''))

                    if event_time.tzinfo is not None:
                        event_time_local = event_time.astimezone(local_tz)
                    else:
                        event_time_local = event_time.replace(tzinfo=local_tz)

                    if event_end_time.tzinfo is not None:
                        event_end_time_local = event_end_time.astimezone(local_tz)
                    else:
                        event_end_time_local = event_end_time.replace(tzinfo=local_tz)

                    time_str = event_time_local.strftime("%I:%M %p")
                    end_time_str = event_end_time_local.strftime("%I:%M %p")
                    status = "upcoming" if event_time_local > now_local else "past"

                    formatted_events.append({
                        "time": time_str,
                        "endTime": end_time_str,
                        "title": summary,
                        "status": status,
                        "startHour": event_time_local.hour + event_time_local.minute / 60,
                        "endHour": event_end_time_local.hour + event_end_time_local.minute / 60
                    })
                else:  # all-day event
                    formatted_events.append({
                        "time": "All Day",
                        "endTime": "All Day",
                        "title": summary,
                        "status": "all-day",
                        "startHour": 0,
                        "endHour": 24
                    })
            except Exception as e:
                print(f"[Calendar] Error parsing event '{summary}': {e}")
                formatted_events.append({
                    "time": "Unknown",
                    "endTime": "Unknown",
                    "title": summary,
                    "status": "unknown",
                    "startHour": 0,
                    "endHour": 1
                })

        return {"events": formatted_events}

    except Exception as e:
        print(f"[Calendar] Error: {e}")
        return {"error": str(e), "events": []}


@app.post("/api/briefing/trigger")
async def trigger_briefing(session_token: Optional[str] = Cookie(None)):
    """
    Called by the frontend after successful face login.
    Generates a personalized morning briefing using Ollama + existing data sources.
    """
    if not session_token or session_token not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")

    username = sessions[session_token]
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    first_name = user['full_name'].split()[0]

    # Fetch calendar events using existing function
    from calender import get_todays_events as briefing_get_events
    import httpx

    events = []
    try:
        events = briefing_get_events()
    except Exception:
        pass

    events_text = (
        "\n".join([
            f"- {e.get('summary', 'Untitled')} at {e['start'].get('dateTime', 'All day')}"
            for e in events
        ])
        if events else "No events today."
    )

    # Fetch weather
    weather_text = "Weather unavailable."
    try:
        API_KEY = "10428bba45b34ba8b4543622252612"
        location = user.get('location', 'Kathmandu')
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=1"
            )
            wd = resp.json()
            weather_text = f"{wd['current']['temp_c']}°C, {wd['current']['condition']['text']}"
    except Exception:
        pass

    # Fetch news
    news_text = "News unavailable."
    try:
        interests = user.get('interests', 'technology')
        category = interests.split(',')[0].strip().lower()
        API_KEY_NEWS = "b47750eb5d3a45cda2f4542d117a42e8"
        valid_cats = ['business', 'entertainment', 'health', 'science', 'sports', 'technology']
        if category in valid_cats:
            news_url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={API_KEY_NEWS}"
        else:
            news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY_NEWS}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(news_url)
            nd = resp.json()
            if nd.get("status") == "ok":
                news_text = "; ".join([a["title"] for a in nd.get("articles", [])[:3]])
    except Exception:
        pass

    # Generate spoken briefing with Ollama
    from langchain_ollama import ChatOllama

    llm = ChatOllama(model="llama3:latest", temperature=0.5)
    prompt = (
        f"Generate a concise, friendly good morning briefing for {first_name}. "
        f"Keep it under 5 sentences — it will be read aloud.\n"
        f"Calendar today: {events_text}\n"
        f"Weather: {weather_text}\n"
        f"Top news: {news_text}"
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    briefing_text = response.content

    # Speak it via Kokoro TTS
    try:
        from services.tts_service import speak_async
        await speak_async(briefing_text)
    except Exception as tts_err:
        print(f"[Briefing] TTS error (non-fatal): {tts_err}")

    return {"briefing": briefing_text}


if __name__ == "__main__":
    import uvicorn
    import logging

    # Show INFO for our app, silence noisy library debug logs
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for _noisy in (
        "httpcore", "httpx", "httpcore.connection", "httpcore.http11",
        "asyncio", "faster_whisper", "websockets", "uvicorn.error",
    ):
        logging.getLogger(_noisy).setLevel(logging.WARNING)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
