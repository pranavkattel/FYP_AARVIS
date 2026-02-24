# AMMS System Flowchart
**Week 9 | Phase 2: Iterative System Design and Prototyping**
**Subfolder:** Flowchart/
**Date Range:** 29 November – 1 December 2024

---

## 1. Main System Flowchart – AMMS Startup and Recognition Loop

```
                        ┌─────────────────┐
                        │  SYSTEM STARTUP │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │ Load Config &   │
                        │ Initialize DBs  │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │ Load Face       │
                        │ Encodings DB    │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │ Start Camera    │
                        │ & Mic Streams   │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │ Start Flask     │
                        │ Web Server      │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  Display Guest  │
                        │  / Idle Screen  │◄─────────────────────┐
                        └────────┬────────┘                      │
                                 │                               │
                        ┌────────▼────────┐                      │
                        │ Capture Camera  │                      │
                        │     Frame       │                      │
                        └────────┬────────┘                      │
                                 │                               │
                        ┌────────▼────────┐                      │
                        │  Face Detected? │                      │
                        └───┬───────┬─────┘                      │
                            │NO     │YES                         │
                            │       ↓                            │
                            │  ┌────────────────┐               │
                            │  │ Extract Face   │               │
                            │  │ Encoding       │               │
                            │  └────────┬───────┘               │
                            │           │                        │
                            │  ┌────────▼───────┐               │
                            │  │ Match Against  │               │
                            │  │ Registered DB  │               │
                            │  └────────┬───────┘               │
                            │           │                        │
                            │  ┌────────▼───────┐               │
                            │  │ Confidence     │               │
                            │  │   ≥ 0.95?      │               │
                            │  └──┬──────┬──────┘               │
                            │     │YES   │NO                     │
                            │     │      ↓                       │
                            │     │  ┌───────────────────┐      │
                            │     │  │ Attempt 3 or more?│      │
                            │     │  └──┬──────────┬─────┘      │
                            │     │     │NO        │YES          │
                            │     │     │          ↓             │
                            │     │     │  ┌──────────────────┐  │
                            │     │     │  │  Offer OTP Login │  │
                            │     │     │  └──────────────────┘  │
                            │     │     │                        │
                            └─────→(retry frame)                  │
                                  │                              │
                                  (no face after 30s)──────────→┘
                                  │
                                  ↓
                              ┌────────────────────┐
                              │  Load User Profile  │
                              │  & Preferences      │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │  Detect Emotion      │
                              │  (DeepFace)          │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │  Fetch API Data     │
                              │  (Weather/Cal/News) │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │  Select Motivational│
                              │  Content by Emotion │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │  Render & Display   │
                              │  Dashboard          │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │  Listen for Wake    │◄─────────────┐
                              │  Word "AURA"        │              │
                              └──────────┬──────────┘              │
                                         │ Wake word detected       │
                              ┌──────────▼──────────┐              │
                              │  Record Voice Input │              │
                              └──────────┬──────────┘              │
                                         │                         │
                              ┌──────────▼──────────┐              │
                              │  Whisper STT        │              │
                              └──────────┬──────────┘              │
                                         │                         │
                              ┌──────────▼──────────┐              │
                              │  NLU: Intent Class. │              │
                              └──┬───────┬───────┬──┘              │
                                 │       │       │                 │
                        COMMAND  │       │QUERY  │CONVERSATION     │
                                 │       │       │                 │
                    ┌────────────┘  ┌────┘  ┌───┘                 │
                    │               │       │                     │
                    ↓               ↓       ↓                     │
             ┌──────────┐  ┌───────────┐ ┌─────────────┐         │
             │ Execute  │  │ API Query │ │ LLM Dialogue│         │
             │ Action   │  │ Response  │ │ (Ollama)    │         │
             └──────────┘  └───────────┘ └─────────────┘         │
                    │               │             │               │
                    └───────────────┴─────────────┘               │
                                    │                             │
                           ┌────────▼──────────┐                 │
                           │  TTS Response +   │                 │
                           │  Display Update   │                 │
                           └────────┬──────────┘                 │
                                    │                             │
                                    └─────────────────────────────┘
                            (continue listening until face leaves)
```

---

## 2. Feature-Specific Flowcharts

### 2.1 Email Assistant Flowchart

```
┌──────────────────────┐
│ User: "Send email to │
│ [name]"              │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│ Search contacts DB   │
│ for [name]           │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│ Contact found?       │
└──────┬───────┬───────┘
       │NO     │YES
       ↓       ↓
┌───────────┐ ┌────────────────────┐
│ "I don't  │ │ "What is the       │
│ recognise │ │ subject?"          │
│ that name"│ └────────┬───────────┘
└───────────┘          │ (voice input)
                       ↓
              ┌────────────────────┐
              │ Record subject      │
              │ (Whisper STT)       │
              └────────┬───────────┘
                       │
              ┌────────▼───────────┐
              │ "What would you    │
              │ like to say?"      │
              └────────┬───────────┘
                       │ (voice input)
                       ↓
              ┌────────────────────┐
              │ Record body        │
              │ (Whisper STT)      │
              └────────┬───────────┘
                       │
              ┌────────▼───────────┐
              │ Display draft on   │
              │ mirror for review  │
              └────────┬───────────┘
                       │
              ┌────────▼───────────┐
              │ "Shall I send it?" │
              └──┬──────────┬──────┘
                 │"Send"    │"Cancel"
                 ↓          ↓
         ┌──────────┐  ┌─────────────┐
         │Gmail API │  │Discard draft│
         │Send email│  │Return to    │
         └────┬─────┘  │dashboard    │
              │        └─────────────┘
         ┌────▼─────┐
         │"Email    │
         │sent!"    │
         │(TTS+disp)│
         └──────────┘
```

---
*Document prepared as part of AMMS Week 9 – Technical Diagrams (Flowchart)*
