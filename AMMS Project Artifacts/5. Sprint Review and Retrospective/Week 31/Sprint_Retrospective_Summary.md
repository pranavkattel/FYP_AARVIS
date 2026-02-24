# AMMS Sprint Retrospective – Full Project Review
**Week 31 | Phase 5: Sprint Review and Retrospective**
**Date:** 22 April 2025
**Format:** Team retrospective (4 team members + supervisor)

---

## 1. Project Summary

| Attribute | Value |
|-----------|-------|
| Project | AMMS – AI Mirror Management System (AURA) |
| Duration | 2 November 2024 – 22 March 2025 (20 weeks) |
| Methodology | Agile/Scrum (6 sprints × 2 weeks) |
| Total story points | 124 planned / 121 completed |
| Total defects | 14 raised / 13 resolved / 1 deferred |
| Team size | 4 (developer, UI, tester, PM) |

---

## 2. Sprint-by-Sprint Velocity

| Sprint | Goal | Points Planned | Points Completed | Velocity |
|--------|------|---------------|-----------------|---------|
| Sprint 1 | Face Recognition | 20 | 18 | 90% |
| Sprint 2 | Emotion Detection | 22 | 21 | 95% |
| Sprint 3 | Motivational Feedback | 21 | 19 | 90% |
| Sprint 4 | WhatsApp/Gmail | 24 | 24 | 100% |
| Sprint 5 | Real-Time Info | 20 | 20 | 100% |
| Sprint 6 | Hardware + Integration | 17 | 19 | 112% (pulled backlog) |
| **Total** | **All Goals** | **124** | **121** | **97.6%** |

---

## 3. What Went Well (Project-Wide Retrospective)

### 3.1 Technical Successes

| Area | Achievement |
|------|------------|
| Face recognition | 91.4% accuracy; 2.1s avg login latency |
| Offline-first architecture | 100% core features work without internet |
| LLM integration | Contextual, natural responses exceeded expectations |
| Modular design | Each sprint module can be enabled/disabled independently |
| Voice pipeline | Whisper STT + edge-TTS worked reliably together |

### 3.2 Process Successes

- **Agile choice validated:** Iterative delivery allowed emotion detection (Sprint 2) to inform motivational feedback (Sprint 3) design
- **Daily stand-ups (async):** 5-minute text updates in team WhatsApp group worked well for a small team
- **Sprint demos:** End-of-sprint demos to supervisor caught UX issues early (e.g., missing wake word prompt)
- **Definition of Done:** clear DoD prevented scope creep between sprints

---

## 4. What Could Be Improved

### 4.1 Technical Challenges

| Issue | Impact | Lesson Learned |
|-------|--------|---------------|
| RPi memory pressure with Ollama (7.2GB) | System instability risk | Quantise aggressively (Q2_K vs Q4_K_M) for production |
| Disgust emotion (57% accuracy) | Feedback mismatch | Dataset limitation — merge with angry earlier in design |
| edge-tts requires internet | Production offline mode unavailable | Ship pyttsx3 as primary fallback from the start |
| Google OAuth token expiry | Calendar failed mid-session | Auto-refresh should be designed as a requirement, not a fix |

### 4.2 Process Challenges

| Issue | Impact | Lesson Learned |
|-------|--------|---------------|
| Hardware arrived Week 22 (Sprint 6) | Late integration testing | Order hardware at project start; don't wait for final sprint |
| Functional requirements not formally tracked until Week 27 | Traceability gaps | Build RTM (requirements traceability matrix) at Week 1 |
| Admin HTTPS not implemented | Security gap in demo | Non-functional security requirements need story points |

---

## 5. Burndown Chart (Sprint 6)

```
Story Points
20|█
  |██
15|███
  |████
10|█████
  |██████
 5|███████
  |████████
 0└──────────
  Day1     Day10
  (Sprint 6 - all stories completed by Day 10)
```

---

## 6. Final Sprint Demos – Stakeholder Ratings

| Feature Demo | Supervisor | External Reviewer | Team |
|-------------|-----------|------------------|------|
| Face recognition login | 5 | 5 | 4 |
| Emotion-based feedback | 4 | 5 | 4 |
| AURA voice interaction | 5 | 5 | 5 |
| Dashboard widgets | 4 | 4 | 5 |
| WhatsApp/Gmail voice | 4 | 4 | 4 |
| Hardware assembly | 5 | 4 | 5 |
| **Average** | **4.5** | **4.5** | **4.5** |

---

## 7. Kaizen Items (Continuous Improvement Backlog)

For AMMS v2:

| # | Item | Priority |
|---|------|---------|
| 1 | HTTPS for admin panel (Let's Encrypt) | High |
| 2 | News category preferences per user | Medium |
| 3 | Voice reminders/timers | Medium |
| 4 | Dimmer / night mode schedule | Low |
| 5 | rPPG heart rate widget | Low |
| 6 | Calendar event voice creation | Medium |
| 7 | Sleep/snooze alarm clock | Low |
| 8 | Upgrade to LLaMA 3.1 when RPi 5 available | Medium |

---

## 8. Project Outcome Statement

AMMS was successfully designed, developed, and deployed as a functioning AI-powered smart mirror prototype meeting all **Must Have** and **Should Have** requirements from the original product backlog. The system demonstrates that a privacy-respecting, offline-first ambient AI assistant is achievable on affordable consumer hardware (< RM 1,300).

**Final evaluation: PROJECT SUCCESS ✅**

---

## 9. References

1. Schwaber, K. & Sutherland, J. (2020). *The Scrum Guide.* scrumguides.org.
2. Anderson, D.J. (2010). *Kanban: Successful Evolutionary Change for Your Technology Business.* Blue Hole Press.
3. Beck, K. et al. (2001). *Manifesto for Agile Software Development.* agilemanifesto.org.
