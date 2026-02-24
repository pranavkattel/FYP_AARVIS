# IoT Smart Mirror – Design and Architecture Research
**Week 7 | Phase 2: Iterative System Design and Prototyping**
**Date Range:** 18 November – 21 November 2024

---

## 1. Introduction

Week 7 marks the transition from requirements collection to **system design**. This document covers foundational design research for the AMMS, focusing on IoT smart mirror architecture, core system design patterns, and the definition of each major module.

---

## 2. Core System Architecture

### 2.1 Three-Tier Architecture Overview

AMMS follows a **three-tier architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Mirror Display (HTML/CSS/JS + Electron/Flask)         │ │
│  │  Widgets: Clock, Weather, Calendar, News, Emotion      │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
                           │ ↑
                    API/Events
                           │ ↑
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐│
│  │  Face Recog │  │   Emotion    │  │   Voice Assistant   ││
│  │   Module    │  │  Detection   │  │  (STT + LLM + TTS)  ││
│  └─────────────┘  └──────────────┘  └─────────────────────┘│
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐│
│  │  Calendar   │  │    Email     │  │     WhatsApp        ││
│  │    API      │  │   Module     │  │    Notification     ││
│  └─────────────┘  └──────────────┘  └─────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │            Notification & Event Engine                  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                           │ ↑
                    Data Access
                           │ ↑
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐ │
│  │ User Profiles│  │ Face Encodings│  │  Emotion History │ │
│  │  (SQLite DB) │  │  (Local File) │  │    (SQLite)      │ │
│  └──────────────┘  └──────────────┘  └───────────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐ │
│  │  Config &    │  │  LLM Models  │  │    API Cache      │ │
│  │  Settings    │  │  (Ollama)    │  │   (Redis/File)    │ │
│  └──────────────┘  └──────────────┘  └───────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Module Architecture Specifications

### 3.1 Facial Recognition Module

**Purpose:** Authenticate users and load personalized profiles

**Architecture:**
```
Camera Feed (OpenCV)
      ↓
Face Detection (HOG + SVM or MTCNN)
      ↓
Face Alignment (Dlib 68-point landmarks)
      ↓
Feature Extraction (FaceNet 128-d embedding)
      ↓
Identity Matching (Cosine similarity vs. stored embeddings)
      ↓
User Profile Loaded (confidence ≥ 0.95)
      OR
Fallback: OTP Login (confidence < 0.95 after 3 attempts)
```

**Technology Stack:**
| Component         | Technology                          | Reason                               |
|-------------------|-------------------------------------|--------------------------------------|
| Camera access     | OpenCV (cv2)                        | Cross-platform, extensive Python API |
| Face detection    | face_recognition library (dlib)     | Easy API, fast on Pi 4               |
| Face encoding     | FaceNet / face_recognition.face_encodings() | 99%+ accuracy on LFW dataset |
| Matching          | scipy.spatial.distance.cosine       | Fast, accurate comparison            |
| Storage           | Pickle file + SQLite                | Simple, local, no dependencies       |

**Data Flow Diagram (Textual):**
```
INPUT: Camera frame (640×480 @ 30fps)
PROCESS: Detect faces → Encode → Compare vs. registered users
OUTPUT: {user_id, name, confidence, profile_data} OR {unknown, fallback_request}
LATENCY TARGET: < 2 seconds end-to-end
```

---

### 3.2 Emotion Detection Module

**Purpose:** Detect user's emotional state to personalize content

**Architecture:**
```
Camera Frame (from Facial Recognition pipeline)
      ↓
Face ROI Extraction (bounding box from FR module)
      ↓
Preprocessing (resize to 48×48, grayscale, normalize)
      ↓
CNN Inference (DeepFace / FER+ model)
      ↓
Softmax Output (7 emotion probabilities)
      ↓
Dominant Emotion Selection (argmax)
      ↓
Content Personalization Engine
```

**Emotion Categories:**
| Code | Emotion   | Mirror Response                                      |
|------|-----------|------------------------------------------------------|
| 0    | Angry     | Calming message: "Take a breath; it's going to be a great day" |
| 1    | Disgust   | Neutral redirect; ask if everything is okay         |
| 2    | Fear      | Reassuring message; highlight positive news          |
| 3    | Happy     | Energetic message; upbeat news selection             |
| 4    | Sad       | Empathetic message; motivational quote               |
| 5    | Surprise  | Curious response; interesting facts                  |
| 6    | Neutral   | Standard morning briefing                           |

---

### 3.3 Motivational Feedback Module

**Purpose:** Generate emotion-adaptive motivational content

**Architecture:**
```
Emotion Input (from Emotion Detection Module)
      ↓
Content Selection Engine
      ├── Quote Database (SQLite: 500+ quotes by emotion tag)
      ├── LLM Generation (if local LLM available)
      └── API Fallback (quote APIs if network available)
      ↓
Text-to-Speech (TTS) Output + Visual Display
      ↓
Usage Log (prevent repeat within 7 days)
```

**Quote Database Schema:**
```sql
CREATE TABLE motivational_quotes (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    emotion_tags TEXT,  -- comma-separated: "sad,fearful"
    author TEXT,
    category TEXT,      -- "motivation", "humor", "wisdom"
    last_shown DATE,
    usage_count INTEGER DEFAULT 0
);
```

---

### 3.4 Email Messaging Module

**Purpose:** Enable voice-controlled email reading and drafting

**Architecture:**
```
Voice Command: "Read emails" OR "Send email to [name]"
      ↓
NLP Intent Recognition (LLM)
      ↓
Gmail API Call (OAuth 2.0 authenticated)
      ├── READ: Fetch + Summarize top N unread emails (LLM summarization)
      └── COMPOSE: Collect recipient, subject, body via voice dialogue
      ↓
TTS Output (reading) OR Email Send (composing)
      ↓
Confirmation Display on Mirror
```

---

### 3.5 Data Integration Display Module

**Purpose:** Aggregate and display real-time information widgets

**Widget Architecture:**
```
Widget Manager (central orchestrator)
      ├── Weather Widget → OpenWeatherMap API (cache: 30 min)
      ├── Calendar Widget → Google Calendar API (cache: 5 min)
      ├── News Widget → NewsAPI.org (cache: 1 hour)
      ├── Clock Widget → System time (real-time)
      ├── Date Widget → System date (real-time)
      └── User Welcome Widget → Profile DB (on login)
```

**Widget Layout Grid:**
```
┌─────────────────────────────────────────────────────┐
│  TIME & DATE                    WEATHER              │
│   07:42 AM                      🌤 26°C              │
│   Monday, Nov 18                72% humidity          │
│                                                     │
│  GREETING                       CALENDAR             │
│  Good morning, Ahmad!           09:00 Team Meeting   │
│  You look focused today.        13:00 Lunch with Ali │
│                                                     │
│  NEWS BRIEFINGS                                     │
│  • Malaysia stock market up 1.2%                    │
│  • New AI model released by Google                  │
│                                                     │
│  MOTIVATIONAL                   NOTIFICATIONS        │
│  "Success is not final..."      📧 3 unread emails  │
│  – Winston Churchill            📱 2 WhatsApp msgs  │
└─────────────────────────────────────────────────────┘
```

---

## 4. Hardware Architecture

### 4.1 Component Diagram

```
┌────────────────────────────────────────────────────┐
│                  AMMS Hardware                      │
│                                                    │
│  ┌─────────────┐     ┌──────────────────────────┐  │
│  │  Camera     │────→│   Raspberry Pi 4 (8GB)   │  │
│  │ (720p-1080p)│     │   - Ubuntu / Pi OS 64-bit│  │
│  └─────────────┘     │   - Python 3.10+         │  │
│                      │   - OpenCV, face_rec      │  │
│  ┌─────────────┐     │   - DeepFace, Whisper     │  │
│  │ Microphone  │────→│   - Ollama + LLaMA3      │  │
│  │  (USB Omni) │     │   - Flask web server      │  │
│  └─────────────┘     └──────────────────────────┘  │
│                                │ ↑                  │
│  ┌─────────────┐               │ HDMI               │
│  │  Speaker    │←─────────────┤                    │
│  │  (USB/BT)   │               │                    │
│  └─────────────┘     ┌────────▼──────────────────┐  │
│                      │  27" Monitor (1920×1080)  │  │
│  ┌─────────────┐     │  Behind Two-Way Mirror    │  │
│  │   Wi-Fi     │────→│                           │  │
│  │(RPi onboard)│     └───────────────────────────┘  │
│  └─────────────┘                                   │
└────────────────────────────────────────────────────┘
```

---

## 5. Design Patterns Applied

| Pattern                  | Applied In                              | Benefit                                |
|--------------------------|-----------------------------------------|----------------------------------------|
| Observer                 | Event emission between modules          | Decoupled module communication         |
| Strategy                 | Different LLM backends (Ollama/API)     | Flexible AI backend selection          |
| Singleton                | Camera manager, Database connection     | Resource efficiency                    |
| Factory                  | Widget instantiation                    | Easy widget addition                   |
| Repository               | User profile data access                | Data access abstraction                |
| Pub/Sub                  | Face detection → content update         | Real-time reactive updates             |

---

## 6. Technology Justifications

| Component     | Chosen Tech       | Alternatives Considered | Justification                               |
|---------------|-------------------|-------------------------|---------------------------------------------|
| Face Recog    | face_recognition  | OpenFace, DeepFace      | Best Python API; dlib accuracy              |
| Emotion       | DeepFace/FER+     | MediaPipe, OpenCV       | Easiest API; multi-model support            |
| Voice STT     | OpenAI Whisper    | Google STT, Vosk        | Best offline accuracy; free                 |
| Local LLM     | Ollama + LLaMA3   | GPT4All, llama.cpp      | Easy API; excellent Pi 4 performance        |
| Display       | Flask + HTML/CSS  | Electron, Qt            | Web dev skills reuse; easy widget system    |
| Database      | SQLite            | PostgreSQL, MongoDB      | Local; no server; sufficient for use case   |

---

## 7. References

1. Raj, P., & Raman, A. (2017). *Designing Usable IoT Intelligent Systems: An Architectural Perspective.* CRC Press.
2. Gamma, E., et al. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software.* Addison-Wesley.
3. Taivalsaari, A., & Mikkonen, T. (2017). *On the Development of IoT Systems.* IEEE CCNC.
4. Garg, D., et al. (2022). *Design and Development of IoT-Smart Mirror Information Display System for Organizational Efficiency.* IEEE Transactions on IoT.
5. Kuanar, S., et al. (2023). *Reflecting the Future: A Comprehensive Prototype of Smart Mirrors.* ACM Computing Surveys.

---
*Document prepared as part of AMMS Week 7 – Define Core System Architecture*
