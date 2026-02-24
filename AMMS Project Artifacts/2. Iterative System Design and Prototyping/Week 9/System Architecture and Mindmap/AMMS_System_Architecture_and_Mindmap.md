# AMMS System Architecture and Mind Map
**Week 9 | Phase 2: Iterative System Design and Prototyping**
**Subfolder:** System Architecture and Mindmap/
**Date Range:** 29 November – 1 December 2024

---

## 1. System Architecture Diagram

### 1.1 High-Level Component Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         AMMS — System Architecture                          ║
╠═══════════════════╦═════════════════════════╦════════════════════════════════╣
║  HARDWARE LAYER   ║    APPLICATION LAYER    ║        EXTERNAL SERVICES       ║
║                   ║                         ║                                ║
║  ┌─────────────┐  ║  ┌───────────────────┐  ║  ┌────────────────────────┐   ║
║  │ USB Camera  │──╬─→│ Face Recognition  │  ║  │  Google Calendar API   │   ║
║  │ (1080p)     │  ║  │ Module            │  ║  │  (REST, OAuth 2.0)     │   ║
║  └─────────────┘  ║  └─────────┬─────────┘  ║  └────────────────────────┘   ║
║                   ║            │             ║                                ║
║  ┌─────────────┐  ║  ┌─────────▼─────────┐  ║  ┌────────────────────────┐   ║
║  │USB Mic      │──╬─→│ Emotion Detection │  ║  │  Gmail API              │   ║
║  │(Omnidirect.)│  ║  │ Module (DeepFace) │  ║  │  (REST, OAuth 2.0)     │   ║
║  └─────────────┘  ║  └─────────┬─────────┘  ║  └────────────────────────┘   ║
║                   ║            │             ║                                ║
║  ┌─────────────┐  ║  ┌─────────▼─────────┐  ║  ┌────────────────────────┐   ║
║  │USB Speaker  │←─╬──│ Voice Interaction │  ║  │  OpenWeatherMap API    │   ║
║  │(or BT)      │  ║  │ (Whisper + TTS)   │  ║  │  (REST, API Key)       │   ║
║  └─────────────┘  ║  └─────────┬─────────┘  ║  └────────────────────────┘   ║
║                   ║            │             ║                                ║
║  ┌─────────────┐  ║  ┌─────────▼─────────┐  ║  ┌────────────────────────┐   ║
║  │27" Monitor  │←─╬──│ Display Engine    │  ║  │  NewsAPI.org            │   ║
║  │(HDMI)       │  ║  │ (Flask/HTML/CSS)  │  ║  │  (REST, API Key)       │   ║
║  └─────────────┘  ║  └─────────┬─────────┘  ║  └────────────────────────┘   ║
║                   ║            │             ║                                ║
║  ┌─────────────┐  ║  ┌─────────▼─────────┐  ║  ┌────────────────────────┐   ║
║  │ Wi-Fi       │  ║  │   Local LLM       │  ║  │  WhatsApp Business API │   ║
║  │ (RPi onboard│  ║  │ (Ollama+LLaMA 3)  │  ║  │  (or Twilio)           │   ║
║  └─────────────┘  ║  └─────────┬─────────┘  ║  └────────────────────────┘   ║
║                   ║            │             ║                                ║
║  ┌─────────────┐  ║  ┌─────────▼─────────┐  ║                                ║
║  │Raspberry Pi │  ║  │    Data Layer     │  ║                                ║
║  │ 4 (8GB RAM) │  ║  │  SQLite + Files   │  ║                                ║
║  └─────────────┘  ║  └───────────────────┘  ║                                ║
║                   ║                         ║                                ║
╚═══════════════════╩═════════════════════════╩════════════════════════════════╝
```

---

### 1.2 Detailed Software Architecture

```
AMMS Software Stack
│
├── OS: Raspberry Pi OS 64-bit (Debian Bookworm)
│
├── Runtime: Python 3.10 (venv)
│   │
│   ├── Face Recognition
│   │   ├── face_recognition (dlib wrapper)
│   │   ├── OpenCV (cv2)
│   │   └── numpy / scipy
│   │
│   ├── Emotion Detection
│   │   ├── deepface
│   │   ├── tensorflow-lite
│   │   └── PIL / Pillow
│   │
│   ├── Speech Processing
│   │   ├── whisper (STT)
│   │   ├── pyaudio (mic capture)
│   │   ├── pyttsx3 / edge-tts (TTS)
│   │   └── sounddevice
│   │
│   ├── AI / LLM
│   │   ├── ollama (API client)
│   │   ├── LangChain (optional orchestration)
│   │   └── transformers (backup models)
│   │
│   ├── APIs & Integration
│   │   ├── google-auth / google-api-python-client
│   │   ├── requests (HTTP)
│   │   ├── schedule (task scheduling)
│   │   └── twilio (WhatsApp)
│   │
│   ├── Web Framework
│   │   ├── Flask (web server)
│   │   ├── flask-socketio (real-time updates)
│   │   └── Jinja2 (templates)
│   │
│   └── Data
│       ├── sqlite3 (user DB, emotion history)
│       ├── pickle (face encodings)
│       └── json (config files)
│
├── Frontend: HTML5 + CSS3 + JavaScript
│   ├── Mirror display (full-screen Chromium)
│   ├── Admin panel (responsive web UI)
│   └── Widget system (modular CSS grid)
│
└── AI Services (Local)
    └── Ollama Server (localhost:11434)
        └── LLaMA 3 8B Q4_K_M (4-bit quantized, ~4GB)
```

---

### 1.3 Module Interaction Diagram

```
                    ┌──────────────────────────────────────────┐
                    │              EVENT BUS                    │
                    │  (face_detected, emotion_updated,         │
                    │   widget_refresh, voice_command,          │
                    │   alert_triggered)                        │
                    └──────────────────────────────────────────┘
                              ↑ ↓  (publish/subscribe)
    ┌───────────────┐         │         ┌───────────────────┐
    │  Face Recog   │──publish:────────→│  Profile Manager  │
    │  Module       │  face_detected    │  (loads user data) │
    └───────────────┘                  └───────────────────┘
                                                │ user_loaded
    ┌───────────────┐                           ↓
    │  Emotion Det. │──publish:────────→ ┌───────────────────┐
    │  Module       │  emotion_updated   │  Content Engine   │
    └───────────────┘                   │  (selects content)│
                                        └───────────────────┘
    ┌───────────────┐                           │ content_ready
    │  API Manager  │──publish:─────────────────↓
    │  (Weather/Cal)│  data_fetched      ┌───────────────────┐
    └───────────────┘                   │  Display Engine   │
                                        │  (renders mirror) │
    ┌───────────────┐                   └───────────────────┘
    │  Voice Module │──publish:────────────────→ ↑
    │  (Whisper+LLM)│  command_received  ┌───────────────────┐
    └───────────────┘                   │  Admin Panel      │
                                        │  (user management)│
                                        └───────────────────┘
```

---

## 2. Mind Map – AMMS System Overview

```
                              ┌──────────────┐
                              │     AMMS     │
                              │ AI Mirror    │
                              │ Management   │
                              │   System     │
                              └──────┬───────┘
                ┌─────────────┬──────┴──────┬─────────────┬──────────────┐
                ↓             ↓             ↓             ↓              ↓
          ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
          │  USERS   │  │ HARDWARE │  │ MODULES  │  │  DATA    │  │EXTERNAL  │
          └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
               │             │             │             │             │
          ┌────┤        ┌────┤        ┌────┤        ┌────┤        ┌────┤
          │Reg.│        │RPi │        │Face│        │SQLite    │Weather │
          │User│        │ 4  │        │Recog        │DB        │API    │
          ├────┤        ├────┤        ├────┤        ├────┤        ├────┤
          │Admin        │Cam │        │Emotion      │Face      │Calendar
          │    │        │USB │        │Detect│      │Enc.│      │API    │
          ├────┤        ├────┤        ├────┤        ├────┤        ├────┤
          │Guest        │Mic │        │Voice│       │Log │        │Gmail │
          │    │        │USB │        │+LLM│        │DB  │        │API   │
               │        ├────┤        ├────┤        └────┘        ├────┤
               │        │Mon.│        │Brief│                     │News │
               │        │27" │        │ing  │                     │API  │
                        ├────┤        ├────┤                      ├────┤
                        │Spkr│        │Email│                     │WA   │
                        │    │        │Asst.│                     │API  │
                        └────┘        ├────┤                      └────┘
                                      │Admin│
                                      │Panel│
                                      └────┘

KEY FEATURES MIND MAP:

AMMS
├── Authentication
│   ├── Face Recognition (primary)
│   ├── OTP (fallback)
│   └── Admin access
│
├── AI Intelligence
│   ├── Emotion Detection
│   │   ├── 7 emotion categories
│   │   └── Real-time (1s latency)
│   ├── Local LLM (Ollama/LLaMA3)
│   │   ├── Conversation
│   │   └── Email summarization
│   └── Motivational Engine
│       ├── Emotion-adaptive quotes
│       └── 500+ quote database
│
├── Information Display
│   ├── Weather (OpenWeatherMap)
│   ├── Calendar (Google Calendar)
│   ├── News (NewsAPI)
│   ├── Clock/Date (system)
│   └── Notifications
│       ├── Email alerts
│       └── WhatsApp
│
├── Voice Control
│   ├── Wake word: "AURA"
│   ├── STT: Whisper base.en
│   ├── NLU: LLaMA 3
│   └── TTS: edge-tts / pyttsx3
│
├── Communication
│   ├── Email (Gmail API)
│   │   ├── Read summaries
│   │   └── Draft + send
│   └── WhatsApp (Twilio API)
│       ├── Notifications
│       └── Voice reply
│
└── Administration
    ├── User management (CRUD)
    ├── System settings
    └── Activity logs
```

---
*Document prepared as part of AMMS Week 9 – Technical Diagrams*
