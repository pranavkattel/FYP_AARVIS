# OpenCV Face Recognition – Comprehensive Implementation Guide
**Sprint 1 | Week 11 | Phase 3: Sprint-Based Development**
**Sprint Goal:** Implement reliable face recognition-based login for 3+ concurrent users
**Date Range:** 9 – 13 December 2024

---

## 1. Introduction to Face Recognition

Face recognition is a biometric identification method that involves detecting a human face in an image/frame and comparing it to a database of known identities. The process follows a pipeline:

```
Image Input → Face Detection → Face Alignment → Feature Extraction → Face Matching → Identity Decision
```

### 1.1 Core Tasks

| Task | Description |
|------|-------------|
| **Face Detection** | Locate bounding boxes of faces in image |
| **Face Alignment** | Normalize face to standard pose/size |
| **Feature Extraction** | Convert face to numerical embedding vector |
| **Face Matching** | Compare vector against enrolled database |

---

## 2. OpenCV Foundations

### 2.1 OpenCV Overview

OpenCV (Open Source Computer Vision Library) is an open-source computer vision and ML library:
- Core language: C++ (with Python bindings `cv2`)
- First release: 2000 (Intel Research)
- Current version: 4.9.x
- License: Apache 2.0

### 2.2 Key Modules Relevant to AMMS

| Module | Purpose |
|--------|---------|
| `cv2.VideoCapture` | Capture frames from webcam |
| `cv2.CascadeClassifier` | Haar-cascade face detection |
| `cv2.dnn` | DNN inference (faster detection alternatives) |
| `cv2.resize`, `cv2.cvtColor` | Image preprocessing |
| `cv2.rectangle`, `cv2.putText` | Overlay UI elements on frame |

---

## 3. Face Detection Algorithms

### 3.1 Haar Cascade (OpenCV Built-in)

```python
import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def detect_faces_haar(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )
    return faces  # List of (x, y, w, h)
```

**Pros:** Fast (CPU), simple  
**Cons:** High false positives; sensitive to lighting, angle

### 3.2 HOG + SVM (dlib approach)

```python
import dlib

detector = dlib.get_frontal_face_detector()

def detect_faces_hog(rgb_frame):
    detections = detector(rgb_frame, 1)  # 1 = upsample once
    return detections
```

**Pros:** More accurate than Haar; good for frontal faces  
**Cons:** Slower; struggles with tilted faces

### 3.3 CNN-Based Detection (dlib MMOD)

```python
cnn_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')

def detect_faces_cnn(rgb_frame):
    dets = cnn_detector(rgb_frame, 1)
    return [(d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom())
            for d in dets]
```

**Pros:** Highest accuracy; works with tilted/partial faces  
**Cons:** Requires GPU for real-time; ~5 FPS on Raspberry Pi CPU

### 3.4 Algorithm Comparison for AMMS

| Method | Accuracy | Speed (RPi4) | Recommended |
|--------|----------|-------------|-------------|
| Haar Cascade | Medium | ~25 FPS | Detection-only pass |
| HOG + SVM | Medium-High | ~8 FPS | Fallback |
| CNN MMOD | High | ~4 FPS | Verification only |
| **face_recognition lib (HOG)** | **High** | **~6 FPS** | **✅ Selected** |

### 3.5 AMMS Decision: `face_recognition` Library

The `face_recognition` library (by Adam Geitgey) wraps dlib's models and provides a clean API:

```bash
pip install face_recognition
```

---

## 4. Face Recognition Pipeline (AMMS)

### 4.1 Full Pipeline Code

```python
import face_recognition
import cv2
import pickle
import numpy as np

class FaceRecognitionSystem:
    def __init__(self, encodings_path='face_encodings.pkl'):
        self.known_encodings = []
        self.known_names = []
        self.load_encodings(encodings_path)
        self.capture = cv2.VideoCapture(0)
        self.tolerance = 0.5        # Lower = stricter match
        self.scale_factor = 0.25   # Downscale for speed

    def load_encodings(self, path):
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.known_encodings = data['encodings']
                self.known_names = data['names']
        except FileNotFoundError:
            print("[WARN] No encodings file found. Enroll users first.")

    def enroll_user(self, name, num_samples=10):
        """Capture face samples and save encoding."""
        samples = []
        count = 0
        while count < num_samples:
            ret, frame = self.capture.read()
            if not ret:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model='hog')
            encodings = face_recognition.face_encodings(rgb, boxes)
            if encodings:
                samples.append(encodings[0])
                count += 1
        # Average encoding for robustness
        avg_encoding = np.mean(samples, axis=0)
        self.known_encodings.append(avg_encoding)
        self.known_names.append(name)
        self._save_encodings()
        print(f"[INFO] Enrolled {name} with {num_samples} samples.")

    def _save_encodings(self, path='face_encodings.pkl'):
        with open(path, 'wb') as f:
            pickle.dump({'encodings': self.known_encodings,
                         'names': self.known_names}, f)

    def recognize(self):
        """Run recognition loop. Returns (name, confidence) or None."""
        ret, frame = self.capture.read()
        if not ret:
            return None

        # Downscale for speed
        small = cv2.resize(frame, (0, 0), fx=self.scale_factor,
                           fy=self.scale_factor)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb_small, model='hog')
        encodings = face_recognition.face_encodings(rgb_small, locations)

        for encoding in encodings:
            distances = face_recognition.face_distance(
                self.known_encodings, encoding)
            if len(distances) == 0:
                continue
            best_idx = np.argmin(distances)
            best_dist = distances[best_idx]
            if best_dist <= self.tolerance:
                confidence = (1 - best_dist) * 100
                return self.known_names[best_idx], round(confidence, 1)

        return None  # No match found

    def release(self):
        self.capture.release()
```

---

## 5. Face Encoding: How It Works

### 5.1 128-Dimensional Embedding

The `face_recognition` library encodes each face as a **128-dimensional float vector** using a deep neural network pre-trained on ~3.3 million face images.

The matching distance formula (Euclidean):

$$d = \sqrt{\sum_{i=1}^{128}(e_1^i - e_2^i)^2}$$

Where:
- $e_1$, $e_2$ are the two face encodings
- $d < 0.5$ is considered a match (AMMS threshold)
- $d < 0.4$ is high-confidence match

### 5.2 Encode Multiple Sample Averaging

Averaging N samples of the same person improves robustness against lighting/expression variation:

$$\bar{e} = \frac{1}{N}\sum_{j=1}^{N} e_j$$

---

## 6. Liveness Detection (Anti-Spoofing)

To prevent photo attacks, AMMS implements a simple liveness check:

### 6.1 Eye Blink Detection (dlib landmark method)

```python
def eye_aspect_ratio(eye):
    # Distance vertical landmarks
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    # Distance horizontal landmark
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

EAR_THRESHOLD = 0.3
BLINK_FRAMES = 2

# Prompt: "Please blink twice to confirm"
```

If no blink detected within 5 seconds → reject login attempt.

---

## 7. Performance on Raspberry Pi 4 (Benchmarks)

| Configuration | FPS | Latency | Notes |
|---------------|-----|---------|-------|
| Full-res (1080p), HOG | 1.2 | 830ms | Too slow |
| 720p, HOG | 2.8 | 357ms | Marginal |
| 480p, HOG (AMMS default) | 5.3 | 189ms | ✅ Acceptable |
| 480p, HOG, 0.25 scale | 8.1 | 123ms | ✅ Selected |
| SSD MobileNet detect + dlib encode | 6.7 | 149ms | Alternative |

**AMMS target:** < 200ms recognition latency at 0.25 scale factor ✅

---

## 8. Integration with AMMS Login Flow

```
Camera frame
    ↓
Face detected? ──No──→ "Scanning..." overlay (keep trying)
    ↓ Yes
Liveness check (blink) ──Fail──→ "Liveness check failed"
    ↓ Pass
Face encoding generated
    ↓
match_face(encoding, db) ──No match──→ "User not recognised. Try again."
    ↓ Match (d < 0.5)
Load user profile (name, prefs, API tokens)
    ↓
Render personalised dashboard
```

---

## 9. References

- Bradski, G. (2000). "The OpenCV Library." *Dr. Dobb's Journal*, 25(11), 120-125.
- Geitgey, A. (2020). *face_recognition Python Library*. GitHub: ageitgey/face_recognition.
- King, D.E. (2009). "Dlib-ml: A Machine Learning Toolkit." *JMLR*, 10, 1755-1758.
- Amos, B., Ludwiczuk, B., Satyanarayanan, M. (2016). "OpenFace: A general-purpose face recognition library." CMU Tech Report CMU-CS-16-118.
- Schroff, F., Kalenichenko, D., Philbin, J. (2015). "FaceNet: A Unified Embedding for Face Recognition and Clustering." *CVPR 2015*.
