# Sprint-Wise Development Documentation (Excluding Hardware Sprint)

## 5.5.1 Sprint 1: Facial Recognition Authentication Development
The objective of this sprint was to implement real-time multi-user facial recognition so the mirror can identify authorized users and support face-based login.

### Steps:
- Develop Real-Time Face Recognition Pipeline:
  - Used InsightFace FaceAnalysis for face detection and embedding extraction.
  - Captured camera frames from browser and sent them to backend APIs.
  - Normalized embeddings for similarity matching.
  - Implemented recognition logic by comparing live embedding with enrolled user embeddings.

- Integrate Face Login with Authentication Flow:
  - Added face-based login endpoint to create authenticated sessions when confidence threshold is met.
  - Integrated face setup and enrollment pages for collecting multiple facial samples.
  - Stored enrolled embeddings for each user and linked them with account identity.

- Implement Presence Cache and Re-Verification:
  - Added face detection cache so recently verified users do not require repeated checks every second.
  - Configured periodic re-verification logic for secure but smooth user experience.

- Testing on Sample Users:
  - Collected multiple captures per user under different angles.
  - Tested recognition under varied indoor lighting conditions.
  - Verified unknown-face rejection behavior using non-enrolled faces.

### Sample Implementation
```python
from insightface.app import FaceAnalysis
import numpy as np

face_app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=-1, det_size=(640, 640))

faces = face_app.get(frame)
test_emb = faces[0].embedding / np.linalg.norm(faces[0].embedding)

best_match = None
best_similarity = 0
for username, embeddings in face_users_db.items():
    similarities = [np.dot(emb, test_emb) for emb in embeddings]
    avg_similarity = np.mean(similarities)
    if avg_similarity > best_similarity:
        best_similarity = avg_similarity
        best_match = username

if best_similarity > 0.4:
    # recognized user
    pass
```

---

## 5.5.2 Sprint 2: Morning Briefings and News Development
The goal of this sprint was to deliver personalized daily briefing and live information display by integrating weather, news, and calendar data sources.

### Steps:
- Integrate Data APIs and Services:
  - Connected Weather API for current conditions and min/max temperature.
  - Connected News API for latest headline retrieval based on user interests.
  - Integrated Google Calendar service for today and upcoming events.

- Build Personalized Briefing Logic:
  - Combined user profile (name, interests, location) with calendar, weather, and top news.
  - Generated concise spoken briefing text through LLM prompt orchestration.
  - Triggered briefing flow after successful authenticated session.

- Display Live Information on Mirror UI:
  - Rendered weather widget in top-right section.
  - Rendered latest news list in footer section.
  - Rendered schedule/events list on the mirror timeline area.

- Real-Time Refresh Strategy:
  - Scheduled periodic weather refresh.
  - Scheduled periodic news refresh.
  - Scheduled periodic calendar refresh.

### Sample Implementation
```python
# Weather endpoint logic
API_KEY = "<weather_api_key>"
url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=1"

# News endpoint logic
API_KEY_NEWS = "<news_api_key>"
news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY_NEWS}"

# Briefing generation prompt (server-side)
prompt = (
    f"Generate a concise, friendly good morning briefing for {first_name}. "
    f"Keep it under 5 sentences.\n"
    f"Calendar today: {events_text}\n"
    f"Weather: {weather_text}\n"
    f"Top news: {news_text}"
)
```

---

## 5.5.3 Sprint 3: Natural AI Communication Development
This sprint focused on implementing natural multi-turn communication with streaming responses, speech-to-text input, and text-to-speech output.

### Steps:
- Develop Multi-Turn Conversation Engine:
  - Built agent workflow using LangGraph StateGraph.
  - Added system rules for safe and controlled tool usage.
  - Preserved context through conversation history and session-level message state.

- Integrate STT and TTS for Voice Interaction:
  - Added faster-whisper transcription pipeline for browser audio input.
  - Added Kokoro-based TTS for spoken responses.
  - Streamed sentence-level audio chunks for faster perceived responsiveness.

- Implement Real-Time Streaming via WebSocket:
  - Used token-level response streaming from model to frontend.
  - Added thinking/speaking/listening state transitions in UI.
  - Added auto-listening VAD logic in frontend for continuous interaction.

- Refine Conversational Context:
  - Loaded recent conversation records from database at session start.
  - Saved user and assistant messages for continuity across sessions.
  - Cleaned tool call artifacts from stored history to improve follow-up turns.

### Sample Implementation
```python
# Graph loop: agent -> tools -> agent
graph = StateGraph(AgentState)
graph.add_node("aarvis_agent", model_call)
graph.add_node("tools", ToolNode(tools=tools))
graph.set_entry_point("aarvis_agent")
graph.add_conditional_edges("aarvis_agent", should_continue, {
    "continue": "tools",
    "end": END,
})
graph.add_edge("tools", "aarvis_agent")

# STT usage in websocket
transcript = await asyncio.to_thread(transcribe_audio_bytes, audio_bytes)
```

---

## 5.5.4 Sprint 5: Voice-Controlled Scheduling Development
The purpose of this sprint was to enable users to create, update, read, and delete calendar events using natural voice commands.

### Steps:
- Integrate Calendar APIs with Per-User OAuth Tokens:
  - Connected Google Calendar service to authenticated user accounts.
  - Implemented token loading, refresh, and update mechanisms.
  - Added support for both read and write calendar operations.

- Implement Scheduling Tools for Agent:
  - Added tools for today’s events and upcoming events.
  - Added create event with duration support.
  - Added update and delete event flows requiring explicit confirmation.

- Add Input Normalization and Guardrails:
  - Normalized time values into 24-hour format.
  - Enforced explicit confirmation before destructive operations.
  - Returned event_id values to support follow-up edits and deletions.

- Validate Voice-Based Event Management:
  - Tested event creation from spoken requests.
  - Tested schedule retrieval and follow-up updates.
  - Tested error handling for invalid date/time formats.

### Sample Implementation
```python
@tool
def create_calendar_event(title: str, date: str, time: str, duration_minutes: int = 60):
    # Normalize to HH:MM 24-hour format
    for fmt in ("%H:%M", "%I:%M %p", "%I:%M%p", "%I %p", "%I%p"):
        try:
            parsed = dt.strptime(time.strip(), fmt)
            time = parsed.strftime("%H:%M")
            break
        except ValueError:
            continue

    result = add_event_simple(title.strip(), date.strip(), time, duration_minutes, "")
    return f"Event created. event_id: {result.get('id', 'unknown')}"
```

---

## 5.5.5 Sprint 6: Intelligent Email Assistant Development
This sprint aimed to provide voice-driven email reading, summarization, drafting, and sending with personalization and contact lookup.

### Steps:
- Integrate Gmail API with LLM Workflow:
  - Added per-user Gmail service access from stored OAuth credentials.
  - Implemented unread email retrieval with sender, subject, and snippet preview.
  - Added sender-specific email summarization support.

- Develop Voice-Driven Email Composition:
  - Implemented dual-mode email sending:
    - Direct send (user provides full subject/body).
    - Auto-compose (user gives topic and assistant drafts the email).
  - Added contact name-to-email lookup via contacts CSV.

- Implement Drafting and Sending Flow:
  - Generated professional email body from topic/context when needed.
  - Encoded and sent MIME messages through Gmail API.
  - Returned sent confirmation with final subject/body summary.

- Validate Privacy and Functional Accuracy:
  - Verified user-specific token usage for mailbox isolation.
  - Tested missing-contact handling and fallback prompts.
  - Tested send failures and graceful error reporting.

### Sample Implementation
```python
@tool
def send_email(to: str, topic: str, subject: str = "", body: str = ""):
    if '@' not in to:
        found = lookup_contact(to)
        if not found:
            return f"Could not find an email address for '{to}'."
        recipient_email = found
    else:
        recipient_email = to

    # Auto-compose if body is empty
    if not body.strip():
        composed = composer.invoke([...])
        # parse Subject: ... and final body

    message = MIMEText(final_body)
    message['to'] = recipient_email
    message['subject'] = final_subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw}).execute()
```

---

## Sprint Outcome Summary (Excluding Hardware)
- Sprint 1 delivered secure face-based user identification and login.
- Sprint 2 delivered personalized morning briefing and live info widgets.
- Sprint 3 delivered natural multi-turn voice communication with streaming AI responses.
- Sprint 5 delivered voice-controlled calendar scheduling and event management.
- Sprint 6 delivered intelligent Gmail reading, summarization, drafting, and sending.

These sprints collectively formed the functional core of the AARVIS smart mirror assistant while excluding the separate hardware setup sprint.
