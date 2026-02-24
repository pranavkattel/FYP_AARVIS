# AMMS Technical Documentation
**Week 33 | Phase 6: Incremental and Final Deployment and Documentation**
**Document Version:** 1.0.0
**Date:** 5 May 2025

---

## 1. System Overview

AMMS (AI Mirror Management System), codenamed AURA, is a Raspberry Pi 4-based smart mirror that combines:

1. **Biometric authentication** — Face recognition login (face_recognition / dlib)
2. **Affective computing** — Emotion detection (DeepFace / FER+ CNN)
3. **Conversational AI** — Local LLM responses (Ollama + LLaMA 3 8B)
4. **Ambient information** — Weather, news, calendar widgets
5. **Messaging integration** — Voice-triggered WhatsApp/Gmail

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AMMS SYSTEM ARCHITECTURE                        │
├──────────────────┬──────────────────┬──────────────────────────────┤
│  INPUT LAYER     │  PROCESSING      │  OUTPUT LAYER               │
│                  │  LAYER           │                              │
│ ┌──────────────┐ │ ┌──────────────┐ │ ┌───────────────────────┐   │
│ │ USB Camera   │→│ │ FaceRecSvc   │ │ │ Mirror Display       │   │
│ └──────────────┘ │ │ EmotionSvc   │ │ │ (Flask + WebSocket)  │   │
│                  │ └──────────────┘ │ └───────────────────────┘   │
│ ┌──────────────┐ │                  │                              │
│ │ USB Mic      │→│ ┌──────────────┐ │ ┌───────────────────────┐   │
│ └──────────────┘ │ │ Whisper STT  │ │ │ Speaker (edge-tts)   │   │
│                  │ │ VoiceHandler │ │ └───────────────────────┘   │
│                  │ └──────────────┘ │                              │
│ ┌──────────────┐ │                  │ ┌───────────────────────┐   │
│ │ External APIs│ │ ┌──────────────┐ │ │ Messaging            │   │
│ │ (OWM, News,  │→│ │ DataCache    │ │ │ (Twilio/Gmail)       │   │
│ │  Gmail, Cal) │ │ │ Ollama LLM   │ │ └───────────────────────┘   │
│ └──────────────┘ │ └──────────────┘ │                              │
│                  │                  │                              │
│                  │ ┌──────────────┐ │                              │
│                  │ │ SQLite DB    │ │                              │
│                  │ │ (users,      │ │                              │
│                  │ │  emotions)   │ │                              │
│                  │ └──────────────┘ │                              │
└──────────────────┴──────────────────┴──────────────────────────────┘
```

---

## 3. Module Documentation

### 3.1 `services/face_recognition_service.py`

| Element | Detail |
|---------|--------|
| Class | `FaceRecognitionService` |
| Purpose | Enrol users, identify face from camera frame |
| Methods | `enroll(name, frames)`, `identify(frame)`, `remove_user(name)` |
| Config | `TOLERANCE=0.50`, `SCALE=0.25` |
| Storage | `face_encodings.pkl` (pickle, local) |
| Dependencies | `face_recognition`, `cv2`, `numpy`, `pickle` |

### 3.2 `services/emotion_detection_service.py`

| Element | Detail |
|---------|--------|
| Class | `EmotionDetectionService` |
| Purpose | Detect dominant emotion from frame; log to DB |
| Methods | `analyze_frame(frame, user_id)`, `get_weekly_summary(user_id)` |
| Config | `CONFIDENCE_THRESHOLD=40.0`, `SCAN_INTERVAL=2.5s`, `WINDOW=10` |
| Storage | `emotion_log` table in `amms.db` |
| Dependencies | `deepface`, `cv2`, `sqlite3` |

### 3.3 `services/feedback_engine.py`

| Element | Detail |
|---------|--------|
| Functions | `generate_aura_response(context)`, `_static_fallback(emotion, name)` |
| Purpose | Generate contextual LLM response or static fallback |
| LLM | Ollama API at `localhost:11434` |
| Model | `llama3:8b-q4_K_M` |
| Config | `temperature=0.7`, `num_predict=80` |
| Dependencies | `ollama` |

### 3.4 `services/gmail_service.py`

| Element | Detail |
|---------|--------|
| Functions | `get_gmail_service()`, `get_unread_emails(n)`, `send_email(to, subject, body)` |
| Auth | OAuth 2.0 (`credentials.json` + `token.json`) |
| Scopes | `gmail.modify`, `gmail.send` |
| Dependencies | `google-auth-oauthlib`, `google-api-python-client` |

### 3.5 `services/data_cache.py`

| Element | Detail |
|---------|--------|
| Class | `DataCache` |
| Purpose | Background-refreshed cache for external API data |
| Fields | `weather`, `forecast`, `events`, `headlines`, `email_count` |
| Refresh rates | Weather: 10m \| Calendar: 5m \| News: 30m \| Email: 3m |
| Dependencies | `requests`, `newsapi`, `googleapiclient` |

---

## 4. Database Schema

```sql
-- users
CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    role        TEXT DEFAULT 'user',
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login  DATETIME,
    login_count INTEGER DEFAULT 0,
    active      INTEGER DEFAULT 1
);

-- emotion_log
CREATE TABLE emotion_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    emotion    TEXT NOT NULL,
    confidence REAL,
    timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_emotion_user_time ON emotion_log(user_id, timestamp);
```

---

## 5. API Endpoints

| Method | Route | Description | Auth |
|--------|-------|-------------|------|
| POST | `/api/login` | Trigger face recognition login | None |
| GET | `/api/dashboard` | Get cached dashboard data | Session |
| GET | `/api/emotions/summary` | Get emotion weekly summary | Session |
| POST | `/api/command` | Submit voice command text | Session |
| POST | `/admin/users` | Add new user (admin) | Admin |
| DELETE | `/admin/users/<id>` | Remove user (admin) | Admin |
| GET | `/health` | System health check | None |

---

## 6. Configuration Reference

| Config Key | Default | Description |
|------------|---------|-------------|
| `FR_TOLERANCE` | 0.50 | Face match distance threshold |
| `FR_SCALE` | 0.25 | Frame downscale factor |
| `EMOTION_THRESHOLD` | 40.0 | Minimum confidence % to act |
| `EMOTION_INTERVAL` | 2.5 | Seconds between emotion scans |
| `EMOTION_WINDOW` | 10 | Temporal smoothing frames |
| `OLLAMA_MODEL` | llama3:8b-q4_K_M | LLM model identifier |
| `LLM_MAX_TOKENS` | 80 | Max response tokens |
| `WEATHER_REFRESH` | 600 | Weather cache refresh (seconds) |
| `CALENDAR_REFRESH` | 300 | Calendar cache refresh (seconds) |
| `NEWS_REFRESH` | 1800 | News cache refresh (seconds) |

---

## 7. Error Handling Guide

| Error | Module | Handling |
|-------|--------|---------|
| `FileNotFoundError` (no encodings) | FaceRecSvc | Logs warning; returns no match |
| `deepface` analysis fails | EmotionSvc | Logs warning; returns neutral |
| `ollama` connection refused | FeedbackEng | Returns static fallback quote |
| Gmail token expired | GmailSvc | Auto-refresh via `credentials.refresh()` |
| External API timeout | DataCache | Returns last cached value; logs |

---

## 8. Dependencies (requirements.txt snapshot)

```
face_recognition==1.3.0
deepface==0.0.79
opencv-python==4.9.0.80
numpy==1.26.4
flask==3.0.3
flask-socketio==5.3.6
ollama==0.2.0
edge-tts==6.1.9
pyttsx3==2.90
openai-whisper==20231117
google-auth-oauthlib==1.2.0
google-api-python-client==2.134.0
requests==2.31.0
newsapi-python==0.2.7
twilio==9.2.3
python-dotenv==1.0.1
scipy==1.13.0
dlib==19.24.4
```

---

## 9. References

1. PEP 8 – Style Guide for Python Code. python.org/dev/peps/pep-0008.
2. Flask Documentation (2024). flask.palletsprojects.com.
3. Brown, M. et al. (2022). *Software Architecture Patterns.* O'Reilly Media.
