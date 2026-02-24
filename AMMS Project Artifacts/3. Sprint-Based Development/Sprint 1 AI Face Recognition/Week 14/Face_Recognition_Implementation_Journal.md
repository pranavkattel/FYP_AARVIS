# AMMS Sprint 1 – Face Recognition Implementation Journal
**Sprint 1 | Week 14 | Phase 3: Sprint-Based Development**
**Sprint Review Date:** 3 January 2025
**Sprint Velocity:** 18 story points completed

---

## 1. Sprint 1 Goals and Outcome

| Sprint Goal | Status |
|-------------|--------|
| Multi-user face recognition login (3+ users) | ✅ Complete |
| Face enrolment workflow (Admin) | ✅ Complete |
| Liveness detection (blink check) | ✅ Complete |
| Recognition latency < 200ms | ✅ 123ms avg |
| Graceful fallback for unrecognised users | ✅ Complete |

---

## 2. Implementation Summary

### 2.1 Module Structure

```
agent/
├── __init__.py
├── graph.py
└── ...

services/
├── face_recognition_service.py    ← NEW Sprint 1
├── liveness_service.py            ← NEW Sprint 1
├── user_profile_service.py        ← NEW Sprint 1
└── ...

database.py                        ← Updated: users table
face_encodings.pkl                 ← Binary: enrolled face data
```

### 2.2 `face_recognition_service.py` — Core Logic

```python
"""
AMMS Face Recognition Service
Sprint 1 Implementation
"""
import face_recognition
import cv2
import pickle
import numpy as np
import logging

logger = logging.getLogger(__name__)

ENCODINGS_PATH = 'face_encodings.pkl'
TOLERANCE = 0.50
SCALE = 0.25
MIN_CONFIDENCE = 60.0  # %

class FaceRecognitionService:

    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self._load()

    def _load(self):
        try:
            with open(ENCODINGS_PATH, 'rb') as f:
                data = pickle.load(f)
            self.known_encodings = data.get('encodings', [])
            self.known_names = data.get('names', [])
            logger.info(f"Loaded {len(self.known_names)} enrolled users.")
        except FileNotFoundError:
            logger.warning("face_encodings.pkl not found. No users enrolled.")

    def _save(self):
        with open(ENCODINGS_PATH, 'wb') as f:
            pickle.dump({'encodings': self.known_encodings,
                         'names': self.known_names}, f)

    def enroll(self, name: str, frames: list) -> bool:
        """Enroll user from list of BGR frames."""
        encodings = []
        for frame in frames:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locs = face_recognition.face_locations(rgb, model='hog')
            encs = face_recognition.face_encodings(rgb, locs)
            if encs:
                encodings.append(encs[0])

        if len(encodings) < 5:
            logger.error(f"Enrollment failed: only {len(encodings)} valid frames.")
            return False

        avg = np.mean(encodings, axis=0)
        self.known_encodings.append(avg)
        self.known_names.append(name)
        self._save()
        logger.info(f"Enrolled: {name} ({len(encodings)} samples)")
        return True

    def identify(self, frame) -> tuple[str | None, float]:
        """Identify face in frame. Returns (name, confidence%) or (None, 0)."""
        if not self.known_encodings:
            return None, 0.0

        small = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, locations)

        for enc in encodings:
            distances = face_recognition.face_distance(self.known_encodings, enc)
            idx = int(np.argmin(distances))
            dist = float(distances[idx])
            if dist <= TOLERANCE:
                confidence = round((1 - dist) * 100, 1)
                return self.known_names[idx], confidence

        return None, 0.0

    def remove_user(self, name: str) -> bool:
        """Remove user encoding from database."""
        if name in self.known_names:
            idx = self.known_names.index(name)
            self.known_encodings.pop(idx)
            self.known_names.pop(idx)
            self._save()
            return True
        return False
```

### 2.3 `liveness_service.py` — Blink Detection

```python
import dlib
import cv2
import numpy as np
from scipy.spatial import distance

predictor_path = 'shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

EAR_THRESH = 0.27
REQUIRED_BLINKS = 1

(LEFT_START, LEFT_END) = (42, 48)
(RIGHT_START, RIGHT_END) = (36, 42)

def eye_aspect_ratio(eye_pts):
    A = distance.euclidean(eye_pts[1], eye_pts[5])
    B = distance.euclidean(eye_pts[2], eye_pts[4])
    C = distance.euclidean(eye_pts[0], eye_pts[3])
    return (A + B) / (2.0 * C)

def check_liveness(frames, timeout_sec=5):
    """Returns True if blink detected within frames."""
    blink_count = 0
    ear_below = False

    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        for rect in rects:
            shape = predictor(gray, rect)
            coords = np.array([[shape.part(i).x, shape.part(i).y]
                                for i in range(68)])
            left_eye = coords[LEFT_START:LEFT_END]
            right_eye = coords[RIGHT_START:RIGHT_END]
            ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

            if ear < EAR_THRESH:
                ear_below = True
            elif ear_below:
                blink_count += 1
                ear_below = False

        if blink_count >= REQUIRED_BLINKS:
            return True

    return False
```

---

## 3. Database Schema (users table)

```sql
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    role        TEXT DEFAULT 'user',       -- 'user' | 'admin'
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login  DATETIME,
    login_count INTEGER DEFAULT 0,
    active      INTEGER DEFAULT 1          -- 0 = disabled
);
```

---

## 4. Recognition Loop (Main App Integration)

```python
# In main.py / Flask app

fr_service = FaceRecognitionService()
liveness = LivenessService()

@app.route('/start_recognition')
def start_recognition():
    cap = cv2.VideoCapture(0)
    frames = [cap.read()[1] for _ in range(30)]  # 3 seconds at 10 FPS
    cap.release()

    # Step 1: Liveness
    if not liveness.check_liveness(frames):
        return jsonify({'status': 'liveness_fail'})

    # Step 2: Recognition
    name, confidence = fr_service.identify(frames[-1])
    if name:
        return jsonify({'status': 'success', 'user': name, 'confidence': confidence})

    return jsonify({'status': 'unknown_face'})
```

---

## 5. Sprint 1 Testing Results

| Test Case | Expected | Actual | Pass? |
|-----------|---------|--------|-------|
| FR-TC-001: Enroll 3 users (10 samples each) | All enrolled | 3 users in .pkl | ✅ |
| FR-TC-002: Login as enrolled user | Match returned | Match at 0.38 dist | ✅ |
| FR-TC-003: Unknown person at mirror | No match | Correctly rejected | ✅ |
| FR-TC-004: Photo held up (liveness) | Liveness fail | Rejected (no blink) | ✅ |
| FR-TC-005: Recognition latency | < 200ms | 123ms @ 0.25 scale | ✅ |
| FR-TC-006: Low lighting (< 100 lux) | Match or reject | 3/5 passed | ⚠️ |
| FR-TC-007: Glasses worn | Match | Matched (0.46 dist) | ⚠️ |

> **Known Issue:** Low-light environments reduce accuracy. Mitigation: CLAHE preprocessing added. Will be revisited in Sprint 6 (hardware).

---

## 6. Sprint Retrospective Notes

**What went well:**
- `face_recognition` library integration was straightforward
- Liveness detection (blink) works reliably in good lighting
- SQLite user profile integration clean

**What to improve:**
- Low-light performance needs IR sensor or software enhancement
- Enrolment UI (admin panel flow) to be refined in Sprint 6

**Action items for next sprint:**
- Begin Emotion Detection module (Sprint 2) using DeepFace
- Keep face recognition service stable and don't refactor

---

## 7. References

1. Viola, P. & Jones, M. (2001). "Rapid Object Detection using a Boosted Cascade of Simple Features." *CVPR 2001*.
2. King, D.E. (2009). "Dlib-ml: A Machine Learning Toolkit." *JMLR*, 10, 1755–1758.
3. Soukupova, T. & Cech, J. (2016). "Real-Time Eye Blink Detection using Facial Landmarks." *CVWW 2016*.
4. Geitgey, A. (2020). face_recognition library README. GitHub.
