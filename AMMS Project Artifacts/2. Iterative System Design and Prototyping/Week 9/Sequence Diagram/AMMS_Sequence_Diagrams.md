# AMMS Sequence Diagrams
**Week 9 | Phase 2: Iterative System Design and Prototyping**
**Subfolder:** Sequence Diagram/
**Date Range:** 29 November – 1 December 2024

---

## 1. Sequence Diagram: User Login via Face Recognition

```
User        Camera     FaceRecog   ProfileDB   EmotionDet  DisplayEngine
  │            │          │            │           │              │
  │ approaches │          │            │           │              │
  │────────────→          │            │           │              │
  │            │ capture  │            │           │              │
  │            │ frame    │            │           │              │
  │            │──────────→            │           │              │
  │            │          │ detect()   │           │              │
  │            │          │────────────→           │              │
  │            │          │ [faces found]          │              │
  │            │          │            │           │              │
  │            │          │ encode()   │           │              │
  │            │          │ [128-d embedding]      │              │
  │            │          │            │           │              │
  │            │          │ match_identity()       │              │
  │            │          │────────────→           │              │
  │            │          │ [user_id, confidence]  │              │
  │            │          │            │           │              │
  │            │          │ load_profile(user_id)  │              │
  │            │          │──────────────────────→ │              │
  │            │          │ [profile data]         │              │
  │            │          │──────────────────────→ │              │
  │            │          │            │           │              │
  │            │          │ detect_emotion(frame)  │              │
  │            │          │──────────────────────────────────────→│
  │            │          │            │       [emotion: "happy"] │
  │            │          │            │                          │
  │            │          │            │ render_dashboard()       │
  │            │          │──────────────────────────────────────→│
  │            │          │            │ [briefing + emotion content]
  │            │          │            │                          │
  │ ←──────────────────────────────────────────────────────────── │
  │ (welcome message displayed + voice greeting)                  │
  │            │          │            │           │              │
```

---

## 2. Sequence Diagram: Voice Email Drafting and Sending

```
User     WakeWord   WhisperSTT   LLM       Gmail     Display   Speaker
  │         │           │         │          │          │          │
  │"AURA"   │           │         │          │          │          │
  │─────────→           │         │          │          │          │
  │         │ triggered │         │          │          │          │
  │         │───────────→         │          │          │          │
  │         │           │ record  │          │          │          │
  │"Send    │           │ audio   │          │          │          │
  │ email   │           │         │          │          │          │
  │ to Ali" │           │ stt()   │          │          │          │
  │         │           │ [text]  │          │          │          │
  │         │           │─────────→          │          │          │
  │         │           │         │ classify_intent()  │          │
  │         │           │         │ ["send_email", "Ali"]         │
  │         │           │         │          │ speak("What is the │
  │         │           │         │          │ subject?")         │
  │         │           │         │──────────────────────────────→│
  │ (says subject)      │         │          │          │          │
  │─────────────────────→         │          │          │          │
  │         │           │ stt()   │          │          │          │
  │         │           │[subject]│          │          │          │
  │         │           │─────────→          │          │          │
  │         │           │         │ speak("What would you │       │
  │         │           │         │ like to say?")         │      │
  │         │           │         │──────────────────────────────→│
  │ (says body)         │         │          │          │          │
  │─────────────────────→         │          │          │          │
  │         │           │ stt()   │          │          │          │
  │         │           │ [body]  │          │          │          │
  │         │           │─────────→          │          │          │
  │         │           │         │ display_draft()     │          │
  │         │           │         │────────────────────→│          │
  │         │           │         │ speak("Shall I send it?")     │
  │         │           │         │──────────────────────────────→│
  │ "Send"  │           │         │          │          │          │
  │─────────────────────→         │          │          │          │
  │         │           │ stt()   │          │          │          │
  │         │           │["send"] │          │          │          │
  │         │           │─────────→          │          │          │
  │         │           │         │ gmail.send_email()  │          │
  │         │           │         │──────────→          │          │
  │         │           │         │ [success]           │          │
  │         │           │         │ speak("Email sent!") │         │
  │         │           │         │──────────────────────────────→│
  │ ←───────────────────────────────────────────────── (audio)    │
  │         │           │         │          │ display_ │          │
  │         │           │         │          │confirmation        │
  │         │           │         │          │──────────→          │
```

---

## 3. Sequence Diagram: Admin Panel – Add New User

```
Admin     AdminUI    FaceRecog    UserDB     Display
  │           │          │           │          │
  │ login as  │          │           │          │
  │ admin     │          │           │          │
  │───────────→          │           │          │
  │           │ verify_admin()       │          │
  │           │──────────→           │          │
  │           │ [admin verified]     │          │
  │           │          │ load_admin_panel()   │
  │           │──────────────────────────────── →│
  │           │          │           │ [admin UI shown]
  │           │          │           │          │
  │ click "Add User"     │           │          │
  │───────────→          │           │          │
  │           │ show enrollment form │          │
  │           │───────────────────────────────── →│
  │           │          │           │          │
  │ enter user │          │           │          │
  │ details   │          │           │          │
  │───────────→          │           │          │
  │           │ start_face_enrollment()          │
  │           │──────────→           │          │
  │           │          │ capture 10 face samples │
  │           │          │           │          │
  │ faces     │          │           │          │
  │ captured  │          │           │          │
  │           │          │ encode_face_samples() │
  │           │          │ [average embedding]  │
  │           │          │──────────→           │
  │           │          │           │ store profile + encoding │
  │           │          │           │          │
  │           │          │           │[success] │
  │           │ show "User added successfully!"  │
  │           │───────────────────────────────── →│
  │ ←─────────────────────────────────────────── │
```

---

## 4. Sequence Diagram: Morning Briefing Delivery

```
FaceRecog  Profile   Weather  Calendar  NewsAPI  Emotion  Display  Speaker
    │          │        │          │        │       │        │         │
    │ user_id  │        │          │        │       │        │         │
    │──────────→        │          │        │       │        │         │
    │          │load_user_prefs()  │        │       │        │         │
    │          │        │          │        │       │        │         │
    │ [prefs]  │        │          │        │       │        │         │
    │──────────→ fetch_weather(location)    │       │        │         │
    │          │        │          │        │       │        │         │
    │          │        │[weather data]     │       │        │         │
    │          │        │──────────→        │       │        │         │
    │          │        │  fetch_events()   │       │        │         │
    │          │        │          │        │       │        │         │
    │          │        │          │[events]│       │        │         │
    │          │        │          │────────→       │        │         │
    │          │        │          │  fetch_news(categories) │         │
    │          │        │          │        │       │        │         │
    │          │        │          │        │[news] │        │         │
    │          │        │          │        │───────────────→│         │
    │          │        │          │        │ emotion_tag ───────────→ │
    │          │        │          │        │       │ select_quote(emotion)
    │          │        │          │        │       │        │         │
    │          │        │          │        │       │[quote] │         │
    │          │        │──────────────────────────────────→ │         │
    │          │        │ [all data aggregated]             │         │
    │          │        │          render_dashboard()        │         │
    │          │        │──────────────────────────────────→ │         │
    │          │        │          │        │       │ [display updated]│
    │          │        │          │        │       │        │speak_greeting()
    │          │        │          │        │       │        │─────────→
    │          │        │          │        │       │        │ (audio)  │
```

---
*Document prepared as part of AMMS Week 9 – Technical Diagrams (Sequence Diagram)*
