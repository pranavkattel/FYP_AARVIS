# AMMS Sprint 2 – Emotion Detection Implementation Journal
**Sprint 2 | Week 17 | Phase 3: Sprint-Based Development**
**Sprint Review Date:** 17 January 2025
**Sprint Velocity:** 21 story points completed

---

## 1. Sprint 2 Goals and Outcome

| Sprint Goal | Status |
|-------------|--------|
| Detect 7 emotions from live camera feed | ✅ Complete |
| Temporal smoothing (10-frame window) | ✅ Complete |
| Emotion–feedback message mapping | ✅ Complete |
| Log emotion history in SQLite | ✅ Complete |
| Real-time dashboard update via WebSocket | ✅ Complete |
| Admin emotion history view | ✅ Complete |

---

## 2. Integration Test Results

| Test ID | Description | Expected | Result | Status |
|---------|-------------|----------|--------|--------|
| ED-TC-001 | Happy face detected | `happy` returned | `happy` at 88.4% | ✅ |
| ED-TC-002 | Neutral face (rest state) | `neutral` returned | `neutral` at 72.1% | ✅ |
| ED-TC-003 | Sad expression | `sad` returned | `sad` at 63.2% | ✅ |
| ED-TC-004 | Angry expression | `angry` returned | `angry` at 51.7% | ✅ |
| ED-TC-005 | 10-frame smoothing | Consistent output | Mode across 10 = stable | ✅ |
| ED-TC-006 | No face in frame | `neutral` (graceful) | Returned `neutral` | ✅ |
| ED-TC-007 | Emotion log written to DB | SQLite entry created | Row inserted | ✅ |
| ED-TC-008 | Quote displayed on dashboard | Contextual quote shown | Correct quote displayed | ✅ |
| ED-TC-009 | Disgusted (hard case) | `disgusted` or close | `angry` (misclassified) | ⚠️ |
| ED-TC-010 | Pipeline latency | < 250ms | 197ms avg | ✅ |

> **Note on TC-009:** Disgust is chronically misclassified as Angry — known issue with FER2013 dataset imbalance (1.5% disgust samples). Mitigation: Merge disgust and angry into "tense" category for feedback purposes.

---

## 3. Sprint 2 Bug Log

| Bug ID | Description | Severity | Fix Applied |
|--------|-------------|----------|-------------|
| BUG-201 | DeepFace cold-start delay (~2s first call) | Medium | Pre-warm model on app init |
| BUG-202 | statistics.mode fails with all-different deque | Low | Added try/except, default to last value |
| BUG-203 | WebSocket emits emotion even when user logged out | Medium | Added auth check in background task |
| BUG-204 | RPi4 CPU spike to 98% during analysis | High | Added SCAN_INTERVAL throttle (2.5s) |

---

## 4. Model Warm-Up Fix (BUG-201)

```python
# In app startup: pre-warm DeepFace model to avoid 2s cold-start
import numpy as np
dummy_frame = np.zeros((48, 48, 3), dtype=np.uint8)
try:
    DeepFace.analyze(dummy_frame, actions=['emotion'],
                     enforce_detection=False, silent=True)
    logger.info("[INIT] DeepFace model pre-warmed.")
except Exception:
    pass
```

---

## 5. CPU Throttling Strategy

The RPi4 cannot sustain continuous emotion analysis at 10 FPS without thermal throttling. AMMS implements a tiered scan strategy:

| State | Scan Rate | Reason |
|-------|-----------|--------|
| User just logged in | Every 5 frames (~1.5s) | High attention period |
| Dashboard idle (2+ min) | Every 15 frames (~5s) | Conserve CPU |
| Voice interaction active | Suspended | Not needed during chat |
| System screensaver | Suspended | No user present |

---

## 6. Emotion Data Schema

```sql
CREATE TABLE emotion_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    emotion    TEXT NOT NULL CHECK(emotion IN
               ('happy','sad','angry','fearful','disgusted','surprised','neutral')),
    confidence REAL CHECK(confidence BETWEEN 0 AND 100),
    timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for analytics queries
CREATE INDEX idx_emotion_user_time ON emotion_log(user_id, timestamp);
```

---

## 7. Sample Analytics Query

```sql
-- Last 7 days emotion breakdown for user_id = 1
SELECT
    emotion,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
FROM emotion_log
WHERE user_id = 1
  AND timestamp >= datetime('now', '-7 days')
GROUP BY emotion
ORDER BY count DESC;
```

---

## 8. Sprint Retrospective

**What went well:**
- DeepFace library was easy to integrate
- Temporal smoothing significantly improved stability (jitter reduced from ~40% to <8%)
- SQLite logging and WebSocket push both worked cleanly

**What to improve:**
- Disgust classification unreliable — merge with Angry for UX purposes
- CPU management needed more upfront planning
- Quote database (static list) feels limited — next phase: route through LLM (Sprint 3)

**Sprint 3 Handoff:**
The Motivational Feedback System (Sprint 3) will replace static quote selection with dynamic LLM-generated responses from Ollama/LLaMA3, consuming the emotion output from this module.

---

## 9. References

1. Serengil, S. & Ozpinar, A. (2020). "LightFace." *ASYU 2020.*
2. Barsoum et al. (2016). "Training Deep Networks for Facial Expression Recognition with Crowd-Sourced Label Distribution." *ICMI 2016.*
3. McKinney, W. (2010). "Data Structures for Statistical Computing in Python." *Scipy 2010.*
