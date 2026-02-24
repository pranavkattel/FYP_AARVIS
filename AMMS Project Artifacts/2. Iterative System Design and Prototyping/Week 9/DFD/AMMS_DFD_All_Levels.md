# Data Flow Diagrams (DFD) – AMMS
**Week 9 | Phase 2: Iterative System Design and Prototyping**
**Subfolder:** DFD/
**Date Range:** 29 November – 1 December 2024

---

## DFD Level 0 – Context Diagram (AMMS System Overview)

The **Level 0 DFD** (Context Diagram) shows AMMS as a single process interacting with external entities.

```
                    ┌──────────────┐
                    │              │
    Face Image ────→│              │←──── Admin Commands
    Voice Input ───→│              │←──── User Voice/Commands
                    │     AMMS     │
    Recognition ←───│  AI Mirror   │────→ Display Output
    Briefing ←──────│   System     │────→ TTS Audio
    Calendar ←──────│              │────→ Notifications
                    │              │
                    └──────────────┘
                           ↑↓
               ┌───────────────────────┐
               │   External Services   │
               │  (Weather, Calendar,  │
               │   News, Gmail APIs)   │
               └───────────────────────┘

External Entities:
├── Registered User (primary actor)
├── System Administrator (admin panel)
├── Google Calendar API (external data source)
├── Gmail API (external communication)
├── OpenWeatherMap API (external data source)
├── NewsAPI (external data source)
└── WhatsApp Business API (external communication)
```

---

## DFD Level 1 – AMMS Main Processes

```
                        ┌─────────────────┐
                        │  Registered      │
                        │     User         │
                        └────────┬────────┘
                                 │ Face Image + Voice
                                 ↓
┌──────────┐  Face Data  ┌──────────────────┐  User Profile  ┌────────────┐
│  Camera  │────────────→│  1.0 Authenticate│───────────────→│  User DB   │
│ (Input)  │             │     User         │←───────────────│ (SQLite)   │
└──────────┘             └────────┬─────────┘                └────────────┘
                                  │ Authenticated User
                                  ↓
┌──────────┐  Frame Data  ┌──────────────────┐  Emotion Tag   ┌──────────────┐
│  Camera  │─────────────→│ 2.0 Detect       │───────────────→│  Emotion     │
│(continuous)│             │     Emotion      │←───────────────│  History DB  │
└──────────┘              └────────┬─────────┘                └──────────────┘
                                   │ Emotion + User Context
                                   ↓
┌──────────────┐  API Data  ┌──────────────────┐  Display Data  ┌──────────────┐
│External APIs │───────────→│ 3.0 Generate     │───────────────→│    Mirror    │
│(Weather, Cal,│            │     Briefing     │                │    Display   │
│ News, etc.)  │            └────────┬─────────┘                └──────────────┘
└──────────────┘                     │ Content + Motivation
                                     ↓
┌──────────┐  Voice Input  ┌──────────────────┐  LLM Response  ┌──────────────┐
│  Mic     │──────────────→│ 4.0 Process      │──────────────→ │  Speaker     │
│ (Input)  │               │   Voice Command  │                │  (Output)    │
└──────────┘               └────────┬─────────┘                └──────────────┘
                                    │ Command Actions
                                    ↓
┌──────────────┐  Auth Token  ┌──────────────────┐  Email Sent  ┌──────────────┐
│  Gmail API   │─────────────→│ 5.0 Email        │────────────→ │  User Inbox  │
│  WhatsApp    │              │   Assistant      │              │  (Notified)  │
└──────────────┘              └──────────────────┘              └──────────────┘
```

---

## DFD Level 2 – Process 1.0: Authenticate User / Admin

```
┌──────────────────────┐
│   Registered User    │──── Face Image ──→ [1.1 Capture Face Frame]
└──────────────────────┘                           │
                                                   │ Cropped Face ROI
                                                   ↓
                                          [1.2 Extract Face Encoding]
                                                   │
                                                   │ 128-d embedding
                                                   ↓
                              Stored Encodings ──→ [1.3 Match Identity]
                              (User Encoding DB)           │
                                                           │ confidence score
                                                   ┌───────┴──────┐
                                                   │              │
                                           ≥ 0.95 conf      < 0.95 (3x fail)
                                                   │              │
                                                   ↓              ↓
                                          [1.4 Load User    [1.5 OTP Login
                                            Profile]          Fallback]
                                                   │              │
                                                   ↓              ↓
                                          ┌─────────────────────────┐
                                          │    Authenticated Session  │
                                          └─────────────────────────┘

Admin Flow:
[Admin Login] → [Admin Face Verified] → [1.6 Admin Panel Access]
                                               │
                              ┌────────────────┼─────────────────┐
                              ↓                ↓                  ↓
                      [Add User]         [Edit User]        [Delete User]
                              │                │                  │
                              └───────────────→[User Database Update]
```

---

## DFD Level 2 – Process 2.0: Face Recognition and Emotion Detection

```
Continuous Camera Feed
         │
         ↓
[2.1 Pre-process Frame]
│   - Resize to 640×480
│   - Adjust brightness/contrast
│   - Grayscale (for emotion model)
         │
         ├──── Color Frame ──→ [2.2 Detect Face Region (MTCNN/HOG)]
         │                               │
         │                    ┌──────────┴──────────┐
         │                    │ Face Bounding Boxes  │
         │                    └──────────┬──────────┘
         │                               │
         │                    [2.3 Classify Emotion]
         │                    │   Input: 48×48 gray ROI
         │                    │   Model: DeepFace FER+
         │                    │   Output: 7 emotion probs
         │                               │
         │                    [2.4 Dominant Emotion]
         │                               │
         └────────────────────────────── → [2.5 Update Emotion State]
                                                    │
                                                    ↓
                                        ┌──────────────────────┐
                                        │  Emotion + Confidence │
                                        │  → Content Engine      │
                                        └──────────────────────┘
```

---

## DFD Level 2 – Process 3.0: Generate Briefing and Display

```
[User Profile Data]──────┐
[Emotion State]──────────┤
[Time/Date Context]──────┤
                         ↓
                [3.1 Determine Content Strategy]
                         │
        ┌────────────────┼───────────────────┐
        ↓                ↓                   ↓
[3.2 Fetch Weather] [3.3 Fetch Calendar] [3.4 Fetch News]
        │                │                   │
        └────────────────┴───────────────────┘
                         │ Aggregated Data
                         ↓
              [3.5 Select Motivational Content]
              │   Based on: emotion + history
              │   Source: quotes DB or LLM
                         │
                         ↓
              [3.6 Render Display Layout]
              │   Compose widgets: weather + calendar + news + quote
              │   Apply user theme/preferences
                         │
                         ↓
              [3.7 Push to Mirror Display]
              │   Flask WebSocket / HTTP refresh
                         │
                         ↓
                  [Mirror Screen Updated]
```

---

## DFD Level 2 – Process 4.0: Admin Panel Management

```
[Admin User]
      │
      ↓
[4.1 Admin Authentication]
      │ admin credentials verified
      ↓
[4.2 Admin Dashboard]
      │
      ├──→ [4.3 User Management]
      │         ├── Create User (name, face enrollment)
      │         ├── Edit User (update profile)
      │         └── Delete User (remove face + data)
      │
      ├──→ [4.4 System Settings]
      │         ├── Widget configuration
      │         ├── Wake word settings
      │         └── API key management
      │
      └──→ [4.5 System Logs]
                ├── Activity log (login history)
                ├── Emotion log (aggregated)
                └── Error log
```

---

## DFD Level 2 – Process 5.0: Send Alerts and Notifications

```
Event Sources:
├── [Calendar API] ──────────→ [Upcoming event] ──→ [5.1 Schedule Alert]
├── [Email Service] ─────────→ [New unread email] ─→ [5.2 Email Alert]
└── [WhatsApp API] ──────────→ [New message] ──────→ [5.3 WhatsApp Alert]

                                         │
                                         ↓
                              [5.4 Alert Priority Engine]
                              │   Priority: Urgent > Calendar > Email > WhatsApp
                                         │
                              ┌──────────┴──────────┐
                              ↓                     ↓
                       [Visual Alert]         [TTS Audio Alert]
                       (Banner on mirror)     ("You have a meeting in 10 min")
```

---
*Document prepared as part of AMMS Week 9 – Create Technical Diagrams*
