# Smart Mirror Emotion AI – Design and Architecture
**Sprint 2 | Week 16 | Phase 3: Sprint-Based Development**
**Date Range:** 13 – 17 January 2025

---

## 1. Emotion Detection Module Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                  AMMS EMOTION DETECTION MODULE                        │
│                                                                        │
│  ┌─────────────┐    ┌─────────────┐    ┌──────────────────────────┐   │
│  │ VideoCapture│ →  │ Face Detect │ →  │  DeepFace.analyze()      │   │
│  │ (OpenCV)    │    │ (HOG/MMOD)  │    │  action=['emotion']       │   │
│  └─────────────┘    └─────────────┘    └──────────┬───────────────┘   │
│                                                   ↓                   │
│                                     ┌─────────────────────────────┐   │
│                                     │  EmotionSmoother (10-frame) │   │
│                                     └──────────────┬──────────────┘   │
│                                                    ↓                  │
│                       ┌────────────────────────────────────────────┐  │
│                       │  EmotionHistoryDB (SQLite)                 │  │
│                       │  emotion_log(user_id, emotion, confidence, │  │
│                       │             timestamp)                     │  │
│                       └──────────────────┬─────────────────────────┘  │
│                                          ↓                            │
│                       ┌────────────────────────────────────────────┐  │
│                       │  FeedbackEngine                            │  │
│                       │  select_quote(emotion, time_of_day, user)  │  │
│                       └──────────────────┬─────────────────────────┘  │
│                                          ↓                            │
│                       ┌────────────────────────────────────────────┐  │
│                       │  Dashboard Render (Flask → WebSocket)      │  │
│                       │  + TTS (edge-tts) spoken feedback          │  │
│                       └────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. EmotionDetectionService Implementation

```python
"""
AMMS Emotion Detection Service
Sprint 2 Implementation
"""

import cv2
import time
import sqlite3
import logging
from collections import deque
from deepface import DeepFace

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 40.0   # Minimum confidence% to act
WINDOW_SIZE = 10               # Temporal smoothing frames
SCAN_INTERVAL = 2.5            # Seconds between emotion scans (battery/perf)
DB_PATH = 'amms.db'

class EmotionDetectionService:

    def __init__(self):
        self.smoother = deque(maxlen=WINDOW_SIZE)
        self._last_scan = 0
        self.current_emotion = 'neutral'
        self.current_confidence = 0.0
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS emotion_log (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER,
                emotion    TEXT NOT NULL,
                confidence REAL,
                timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        conn.close()

    def analyze_frame(self, frame, user_id: int | None = None):
        """
        Analyze a BGR frame for emotion.
        Throttles to SCAN_INTERVAL to save CPU.
        Returns (emotion_str, confidence_float)
        """
        now = time.time()
        if now - self._last_scan < SCAN_INTERVAL:
            return self.current_emotion, self.current_confidence

        self._last_scan = now

        try:
            results = DeepFace.analyze(
                img_path=frame,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            if not results:
                return 'neutral', 0.0

            result = results[0]
            dominant = result['dominant_emotion']
            confidence = result['emotion'][dominant]

            if confidence < CONFIDENCE_THRESHOLD:
                dominant = 'neutral'

            # Temporal smoothing
            self.smoother.append(dominant)
            from statistics import mode
            smoothed = mode(self.smoother)

            self.current_emotion = smoothed
            self.current_confidence = confidence

            if user_id:
                self._log_emotion(user_id, smoothed, confidence)

            return smoothed, confidence

        except Exception as e:
            logger.warning(f"Emotion analysis failed: {e}")
            return 'neutral', 0.0

    def _log_emotion(self, user_id: int, emotion: str, confidence: float):
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO emotion_log (user_id, emotion, confidence) VALUES (?,?,?)",
            (user_id, emotion, round(confidence, 2))
        )
        conn.commit()
        conn.close()

    def get_weekly_summary(self, user_id: int) -> dict:
        """Return emotion frequency for last 7 days."""
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute("""
            SELECT emotion, COUNT(*) as cnt
            FROM emotion_log
            WHERE user_id=? AND timestamp >= datetime('now', '-7 days')
            GROUP BY emotion ORDER BY cnt DESC
        """, (user_id,)).fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}
```

---

## 3. Feedback Engine

```python
"""
AMMS Motivational Feedback Engine
Selects appropriate quote/message based on detected emotion
"""

import random

QUOTES = {
    'happy': [
        "Keep that energy — you're unstoppable today! 🌟",
        "Happiness looks great on you. Make today count!",
        "That smile says it all. Let's make magic happen.",
    ],
    'sad': [
        "It's okay to feel low. Every storm runs out of rain. 💙",
        "Rest if you must, but don't you quit. — Unknown",
        "You are braver than you believe. — A.A. Milne",
        "One step at a time. You've got this.",
    ],
    'angry': [
        "Take a deep breath. This moment will pass.",
        "Respond, don't react. You're in control.",
        "Channel that energy — anger can be fuel.",
    ],
    'fearful': [
        "Courage is feeling the fear and doing it anyway.",
        "You are more capable than you think. 💪",
        "Whatever's worrying you — you've overcome things before.",
    ],
    'disgusted': [
        "Let's reset. Here's what's ahead today.",
        "A fresh perspective changes everything.",
    ],
    'surprised': [
        "Life is full of surprises — embrace them!",
        "Something interesting happening? I'm ready whenever you are.",
    ],
    'neutral': [
        "Good morning. Let's make today productive.",
        "A new day, a new opportunity.",
        "Ready when you are.",
    ],
}

def get_motivational_message(emotion: str, user_name: str = '') -> str:
    emotion = emotion.lower()
    pool = QUOTES.get(emotion, QUOTES['neutral'])
    message = random.choice(pool)
    if user_name:
        # Personalise first message
        message = f"{user_name.split()[0]}, {message[0].lower()}{message[1:]}"
    return message
```

---

## 4. Dashboard Integration (WebSocket Push)

AMMS uses Flask-SocketIO to push real-time emotion updates to the browser dashboard:

```python
# In main.py
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

def emotion_background_task():
    cap = cv2.VideoCapture(0)
    emotion_svc = EmotionDetectionService()
    while True:
        ret, frame = cap.read()
        if ret:
            emotion, conf = emotion_svc.analyze_frame(frame, user_id=current_user_id)
            quote = get_motivational_message(emotion, current_user_name)
            socketio.emit('emotion_update', {
                'emotion': emotion,
                'confidence': round(conf, 1),
                'quote': quote
            })
        socketio.sleep(2.5)

@socketio.on('connect')
def on_connect():
    socketio.start_background_task(emotion_background_task)
```

**Browser (JavaScript):**
```javascript
socket.on('emotion_update', (data) => {
    document.getElementById('emotion-icon').textContent = EMOJI_MAP[data.emotion];
    document.getElementById('quote-text').textContent = data.quote;
    document.getElementById('emotion-confidence').textContent = 
        `${data.emotion} (${data.confidence}%)`;
});
```

---

## 5. Emotion History Analytics (Admin Dashboard)

### 5.1 Weekly Emotion Report Format

```
AHMAD — Emotion Summary (Last 7 Days)
──────────────────────────────────────
happy      ████████████  58%
neutral    █████          22%
sad        ███            13%
angry      █              4%
fearful                   2%
surprised                 1%
```

### 5.2 Trend Analysis Feature
- If user shows 3+ consecutive sad/fearful readings → flag for "check-in mode"
- AURA proactively asks: *"You seem a bit down lately. Is there anything you'd like to talk about?"*

---

## 6. Performance Profile

| Metric | Value |
|--------|-------|
| DeepFace inference (FER+ backend) | ~180ms |
| Frame capture time | ~12ms |
| SQLite write | ~2ms |
| WebSocket broadcast | ~3ms |
| **Total pipeline** | **~197ms** |
| CPU load (RPi4, 4-core) | 35–45% per core during analysis |

---

## 7. References

1. Serengil, S.I. & Ozpinar, A. (2020). "LightFace: A Hybrid Deep Face Recognition Framework." *ASYU 2020*, Istanbul.
2. Barsoum, E. et al. (2016). "Training Deep Networks for Facial Expression Recognition with Crowd-Sourced Label Distribution." *ICMI 2016*. (FER+ dataset)
3. Picard, R.W. (1997). *Affective Computing.* MIT Press, Cambridge MA.
4. Geifman, Y. & El-Yaniv, R. (2019). "SelectiveNet: A Deep Neural Network with an Integrated Reject Option." *ICML 2019*.
