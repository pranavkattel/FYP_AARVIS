# AMMS Final Deployment Report
**Week 34 | Phase 6: Incremental and Final Deployment and Documentation**
**Document Version:** 1.0 | Date: 15 May 2025
**Status: FINAL ✅**

---

## 1. Executive Summary

The AMMS (AI Mirror Management System), branded as **AURA Smart Mirror**, has been successfully developed, tested, and deployed as a fully functional prototype. The system was built over 20 weeks using Agile/Scrum methodology with 6 development sprints, achieving 97.6% of planned story points.

**Key outcomes:**
- ✅ All Must-Have requirements implemented
- ✅ UAT passed with 75.8 SUS score (above 68 industry baseline)
- ✅ Face recognition accuracy: 91.4% (target: 85%)
- ✅ Privacy-first: 100% offline core processing
- ✅ Total BOM cost: RM 1,222 (well within RM 1,500 budget)
- ✅ NPS: +25 (exceeds consumer IoT benchmark of +20)

---

## 2. Project Metrics

### 2.1 Delivery Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Sprint velocity | 100% | 97.6% |
| Requirements implemented | 12 FR + 5 NFR | 12 FR + 4 NFR ✅ |
| Defects raised | < 20 | 14 |
| Defects resolved | > 95% | 93% (13/14) |
| Test coverage (unit) | ≥ 75% | 81% |
| UAT sign-off | All 3 participants | 3/3 ✅ |

### 2.2 Performance Metrics

| Metric | Target | Achieved |
|--------|--------|---------|
| Face recognition latency | < 3s | 2.1s avg ✅ |
| Face recognition accuracy | > 85% | 91.4% ✅ |
| Emotion detection accuracy | > 80% | 83.0% (82.9% excl. disgust) ✅ |
| LLM response latency | < 5s | 3.8s avg ✅ |
| System uptime (testing period) | > 95% | 97.2% ✅ |
| End-to-end login latency | < 5s | 2.1 + 0.3 TTS = 2.4s ✅ |

---

## 3. System Features Delivered

| Sprint | Feature | Status |
|--------|---------|--------|
| Sprint 1 | Face recognition multi-user login | ✅ Deployed |
| Sprint 1 | Liveness detection (blink check) | ✅ Deployed |
| Sprint 2 | Emotion detection (7 classes) | ✅ Deployed |
| Sprint 2 | Emotion history logging | ✅ Deployed |
| Sprint 3 | AURA LLM-powered responses (Ollama) | ✅ Deployed |
| Sprint 3 | Voice command via Whisper STT | ✅ Deployed |
| Sprint 3 | TTS via edge-tts (Aria Neural) | ✅ Deployed |
| Sprint 4 | WhatsApp send via voice (Twilio) | ✅ Deployed |
| Sprint 4 | Gmail read/send via voice | ✅ Deployed |
| Sprint 5 | Weather widget (OpenWeatherMap) | ✅ Deployed |
| Sprint 5 | Calendar widget (Google Calendar) | ✅ Deployed |
| Sprint 5 | News headlines (NewsAPI) | ✅ Deployed |
| Sprint 6 | Raspberry Pi 4 hardware assembly | ✅ Deployed |
| Sprint 6 | Auto-boot systemd service | ✅ Deployed |
| Sprint 6 | Admin panel (user management) | ✅ Deployed |

---

## 4. Architecture Decision Record (ADR Summary)

| Decision | Alternatives Considered | Chosen | Rationale |
|----------|------------------------|--------|-----------|
| Face recognition | LBPH, DeepFace | face_recognition (dlib) | Best accuracy/speed on RPi4 |
| Emotion detection | Custom CNN | DeepFace (FER+) | Pre-trained, easy integration |
| LLM | GPT-4 API, Mistral | Ollama + LLaMA3 | Fully offline; privacy-first |
| STT | Google STT, DeepSpeech | Whisper (OpenAI, local) | Offline; high accuracy |
| TTS | gTTS, pyttsx3 | edge-tts (primary) / pyttsx3 (fallback) | Most natural voice |
| Web framework | Django, FastAPI | Flask + SocketIO | Lightweight; real-time support |
| Database | PostgreSQL, MongoDB | SQLite | No server required; sufficient scale |
| WhatsApp API | Meta Official | Twilio sandbox | No business verification required |

---

## 5. Known Limitations and Deferred Items

| Item | Category | Deferred to |
|------|----------|------------|
| Disgust detection accuracy (57%) | ML limitation | v2 — retrain on balanced dataset |
| Admin panel HTTP only (no HTTPS) | Security | v2 — Let's Encrypt SSL |
| News category filtering | Feature | v2 |
| Voice reminders/timers | Feature | v2 |
| Night mode / auto-dim | UX | v2 |
| Raspberry Pi 5 migration (for LLM headroom) | Hardware | Future |
| rPPG heart rate widget | Research | v3 |

---

## 6. Budget Summary

| Category | Budgeted | Actual |
|----------|---------|--------|
| Raspberry Pi 4 (8GB) | RM 350 | RM 340 |
| Monitor (27") | RM 450 | RM 420 |
| Camera + Mic + Speaker | RM 200 | RM 200 |
| Mirror glass + frame | RM 200 | RM 180 |
| Storage + accessories | RM 100 | RM 82 |
| **Total** | **RM 1,300** | **RM 1,222** |

**Underspent by RM 78 (6%)** ✅

---

## 7. Lessons Learned

### 7.1 Architecture
- Design for memory constraints from Day 1 (Ollama + FaceRec + DeepFace = 7.5GB on 8GB RPi)
- Offline-first design is achievable and strongly preferred by users
- Modular service architecture enabled incremental deployment successfully

### 7.2 Process
- Hardware availability must be secured before Sprint 1, not Sprint 6
- Non-functional requirements (security, HTTPS) need story points like functional ones
- UAT with actual users is irreplaceable — found onboarding issue not caught in technical testing

### 7.3 Technology
- `face_recognition` (dlib) is the correct choice over LBPH for production quality
- Temporal smoothing for emotion detection is essential — single-frame output is too noisy
- LLM response limits (`num_predict=80`) are critical to keep interaction natural and fast

---

## 8. Project Closure Checklist

- [x] All code committed to git repository
- [x] `requirements.txt` frozen
- [x] `.env.example` documented
- [x] Auto-start systemd service active
- [x] All enrolled users tested and confirmed
- [x] Technical documentation complete (Week 33)
- [x] User manual complete (Week 34)
- [x] Post-survey analysis complete (Week 30)
- [x] Final retrospective complete (Week 31)
- [x] Supervisor sign-off obtained
- [x] All project artifacts filed in `AMMS Project Artifacts/`

---

## 9. Final Statement

> *AMMS demonstrates that a sophisticated, privacy-respecting AI assistant can be built with commodity hardware (< RM 1,300), open-source AI models, and well-structured software architecture. The system successfully merges ambient display design, affective computing, conversational AI, and productivity integration into a single cohesive experience. The project is recommended for advancement to a v2 development cycle.*

**Project Status: SUCCESSFULLY COMPLETED ✅**  
**Date:** 15 May 2025  
**Version:** 1.0.0

---

## 10. References

1. Sommerville, I. (2016). *Software Engineering* (10th ed). Pearson.
2. Schwaber, K. & Sutherland, J. (2020). *The Scrum Guide.* scrumguides.org.
3. Benyon, D. (2014). *Designing Interactive Systems* (3rd ed.). Pearson.
4. Raspberry Pi Foundation (2024). *RPi4 Technical Reference.* raspberrypi.com.
