# Smart Mirror – Overview & Background Research
**Week 1 | Phase 1: Project Initiation and Requirements Collection**
**Date Range:** 2 November – 3 November 2024

---

## 1. What is a Smart Mirror?

A **smart mirror** is a two-way reflective glass integrated with a display panel and computing hardware that overlays digital information on top of a person's reflection. Unlike a standard mirror, a smart mirror can display:

- Real-time data (time, weather, news, traffic)
- Personalized user content (calendar, emails, reminders)
- Interactive AI-driven features (voice assistant, face recognition, emotion detection)

Smart mirrors represent the convergence of **ambient computing**, **human-computer interaction (HCI)**, and **internet of things (IoT)** technologies.

---

## 2. Market Landscape

### 2.1 Industry Overview (2024–2032 Projections)

According to Precedence Research (2024):
- Global Smart Mirror Market Size: **USD 3.21 billion** (2024)
- Projected Market Size by 2032: **USD 11.74 billion**
- CAGR: **17.6%** (2024–2032)
- Key Segments: Automotive, Hospitality, Healthcare, Residential

### 2.2 Key Market Drivers
1. Rising demand for smart home devices and IoT integration
2. Increasing adoption in luxury hospitality (smart hotel rooms)
3. Growth in health and beauty sector (fitness tracking mirrors)
4. Advances in computer vision and edge AI computing

### 2.3 Market Challenges
- High initial cost of hardware components
- Privacy and data security concerns (biometric data)
- Limited standardization across platforms
- Consumer unfamiliarity with smart mirror technology

---

## 3. Existing Smart Mirror Solutions

### 3.1 Open Source: MagicMirror²
- **Platform:** Raspberry Pi / Node.js
- **Features:** Modular widget system, weather, clock, news, calendar
- **Limitations:** No built-in face recognition, no AI, no emotion detection
- **Community:** 14,000+ GitHub stars; extensive module ecosystem
- **Relevance to AMMS:** Core inspiration for display architecture

### 3.2 Commercial: Amazon Echo Show / Portal
- **Features:** Voice assistant, smart home control, video calls
- **Limitations:** No mirror form factor; privacy concerns (cloud processing)
- **Relevance to AMMS:** Voice interaction design patterns

### 3.3 Commercial: HiMirror
- **Features:** Skin analysis, beauty tracking, LED lighting
- **Target Market:** Beauty/cosmetic sector
- **Limitations:** Narrow use case; no general AI integration

### 3.4 Academic Prototypes
| Project                                                            | Institution       | Key Feature                          |
|--------------------------------------------------------------------|-------------------|--------------------------------------|
| AURA Smart Mirror (2023)                                           | Local University  | Emotion + Face Recognition           |
| Smart Mirror for Ambient Home Environment (Haddad et al., 2022)   | IEEE              | IoT sensor integration               |
| Smart Mirror for Healthy Lifestyle (Mennicken et al., 2016)        | ETH Zurich        | Wellness tracking                    |

---

## 4. AMMS Positioning

The **AI Mirror Management System (AMMS)** is designed to address gaps in existing solutions:

| Feature                        | MagicMirror² | Commercial Solutions | AMMS (Proposed) |
|--------------------------------|--------------|----------------------|-----------------|
| Facial Recognition Login       | ❌ (module)  | Partial              | ✅ (built-in)   |
| Emotion Detection              | ❌           | ❌                   | ✅              |
| Motivational Feedback Engine   | ❌           | Partial              | ✅              |
| Local LLM (Privacy-Preserving) | ❌           | ❌                   | ✅              |
| Email/Calendar Integration     | ✅ (module)  | ✅                   | ✅              |
| Multi-User Profiles            | ✅ (module)  | ✅                   | ✅              |
| Voice Command System           | ❌           | ✅                   | ✅              |
| WhatsApp Integration           | ❌           | ❌                   | ✅              |

---

## 5. Technical Components Overview

### 5.1 Hardware Platform
- **Computing Unit:** Raspberry Pi 4 Model B (8GB RAM)
- **Display:** 27-inch IPS monitor (1920×1080)
- **Mirror Glass:** Two-way acrylic or glass
- **Camera:** Logitech C920 (1080p, 30fps) mounted at top
- **Microphone:** USB omnidirectional microphone
- **Speaker:** Compact USB or Bluetooth speaker

### 5.2 Software Stack (Planned)
| Component             | Technology                       |
|-----------------------|----------------------------------|
| Operating System      | Raspberry Pi OS (64-bit)         |
| Face Recognition      | OpenCV + face_recognition lib    |
| Emotion Detection     | DeepFace / FER+ CNN model        |
| NLP / Voice           | Whisper (speech-to-text) + LLM   |
| Local LLM             | Ollama + LLama3 (local inference) |
| Calendar API          | Google Calendar API              |
| Email                 | Gmail API / IMAP                 |
| Weather API           | OpenWeatherMap API               |
| News API              | NewsAPI.org                      |
| Frontend Display      | Electron.js / Flask + HTML/CSS   |

---

## 6. Related Academic Research Summary

### 6.1 Smart Mirror as a Productivity Tool
**Lee et al. (2021)** demonstrated that smart mirrors in morning routines can reduce decision fatigue by 34% when displaying curated daily schedules, weather, and communication summaries.

### 6.2 Ambient Displays and Information Retrieval
**Weiser & Brown (1996)** introduced the concept of "calm technology" – devices that inform without demanding attention. Smart mirrors embody this design philosophy as they integrate into existing routines.

### 6.3 Face Recognition in Home Environments
**Turk & Pentland (1991)** pioneered eigenface-based recognition while modern CNNs (FaceNet, ArcFace) achieve 99%+ accuracy on benchmark datasets. For home environments, privacy-preserving local processing remains critical.

---

## 7. Project Scope Boundaries

### In Scope
- Face recognition for up to 10 users
- Emotion detection from facial expressions (7 basic emotions)
- Personalized dashboard widgets (weather, calendar, time, news)
- Voice-controlled email drafting and reading
- Motivational content delivery based on emotional state
- WhatsApp message notifications
- Admin panel for user profile management

### Out of Scope (v1.0)
- Mobile companion app
- Cloud synchronization
- 3D depth camera integration
- Full body gesture control
- Smart home device control (lights, thermostat)
- Multi-mirror networking

---

## 8. References

1. Haddad, R., et al. (2022). *Smart mirror for ambient home environment.* IEEE Smart Computing.
2. Mennicken, S., et al. (2016). *A smart mirror to promote a healthy lifestyle.* CHI 2016.
3. Precedence Research (2024). *Smart Mirror Market Size, Share and Trends 2024 to 2034.* Retrieved from https://www.precedenceresearch.com/
4. Fortune Business Insights (2024). *Smart Mirror Market Size – Global Industry Analysis 2024-2032.*
5. Weiser, M., & Brown, J.S. (1996). *Designing calm technology.* PowerGrid Journal.
6. Turk, M., & Pentland, A. (1991). *Eigenfaces for recognition.* Journal of Cognitive Neuroscience.

---
*Document prepared as part of AMMS Week 1 – Project Initiation and Requirements Collection*
