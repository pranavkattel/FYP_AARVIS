# Emotion Detection with AI – Research Survey
**Sprint 2 | Week 15 | Phase 3: Sprint-Based Development**
**Sprint Goal:** Detect 7 emotions from camera feed; trigger contextual motivational feedback
**Date Range:** 6 – 10 January 2025

---

## 1. Overview of Facial Emotion Recognition (FER)

Facial Emotion Recognition (FER) is the automated process of detecting and classifying human emotional states from facial images or video streams. The field is grounded in Ekman's theory of **Basic Universal Emotions** (1971):

| Emotion | Facial Action Units (approx.) | AMMS Response |
|---------|-------------------------------|---------------|
| Happy 😊 | Raised cheeks, lip corners up | Positive reinforcement |
| Sad 😢 | Lowered lip corners, raised brows | Encouragement quotes |
| Angry 😠 | Lowered brows, tensed lips | Calming reminders |
| Surprised 😲 | Raised brows, wide eyes, open mouth | Info display |
| Fearful 😨 | Wide eyes, raised brows, open mouth | Reassuring message |
| Disgusted 🤢 | Nose wrinkle, raised upper lip | Neutral redirect |
| Neutral 😐 | No significant expression | Standard briefing |

---

## 2. Methodological Evolution

### 2.1 Traditional Methods (Pre-2012)

| Method | Description | Limitation |
|--------|-------------|-----------|
| Gabor filters + SVM | Texture features + SVM classifier | Hand-crafted features |
| AAM (Active Appearance Model) | Fit face model; extract shape/texture params | Slow, requires initialisation |
| SIFT/HOG + SVM | Local feature descriptors + SVM | Sensitive to illumination |
| FACS + Rule system | Manual AU coding → emotion rules | Not real-time |

### 2.2 Deep Learning Methods (Post-2012)

| Method | Year | Accuracy (FER2013) | Notes |
|--------|------|--------------------|-------|
| Plain CNN | 2013 | 65.5% | Baseline |
| VGGNet-13 fine-tuned | 2015 | 71.2% | Overfits on small sets |
| Inception-v3 fine-tuned | 2016 | 72.4% | Heavy for edge |
| ResNet-50 | 2017 | 74.1% | Good balance |
| **DeepFace (FER+ model)** | 2018 | **84.2%** | **AMMS selected** |
| Vision Transformer (ViT) | 2022 | 87.8% | Too heavy for RPi |

---

## 3. FER2013 Dataset

The primary benchmark dataset for facial expression recognition:

| Property | Value |
|----------|-------|
| Total images | 35,887 |
| Training set | 28,709 |
| Validation set | 3,589 |
| Test set | 3,589 |
| Image size | 48×48 px (grayscale) |
| Classes | 7 (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral) |
| Source | Google Image Search, semi-automatic labelling |

**Class distribution (imbalanced):**
- Happy: 8,989 images (25.1%) ← most common
- Neutral: 6,198 (17.3%)
- Sad: 6,077 (17.0%)
- Fear: 5,121 (14.3%)
- Angry: 4,953 (13.8%)
- Surprise: 4,002 (11.2%)
- Disgust: 547 (1.5%) ← rarest

> **AMMS implication:** Disgust detection will have lower reliability. System treats Disgust + Angry similarly for feedback selection.

---

## 4. DeepFace Library

### 4.1 Overview

**DeepFace** (Serengil & Ozpinar, 2020) is a Python library that provides a unified wrapper for multiple face analysis backends:

```bash
pip install deepface
```

### 4.2 Emotion Analysis API

```python
from deepface import DeepFace

result = DeepFace.analyze(
    img_path=frame,          # BGR numpy array or file path
    actions=['emotion'],     # Only request emotion (faster)
    enforce_detection=False, # Don't fail if no face
    silent=True
)

emotions = result[0]['emotion']
# Returns: {'angry': 2.3, 'disgust': 0.1, 'fear': 1.8,
#           'happy': 85.4, 'sad': 4.2, 'surprise': 0.5, 'neutral': 5.7}
dominant = result[0]['dominant_emotion']
# Returns: 'happy'
```

### 4.3 Backend Models Available

| Backend | Accuracy | Inference Speed (RPi4) |
|---------|----------|----------------------|
| `VGG-Face` | High | Slow (~800ms) |
| `FER+` (default for emotion) | Good | **~180ms** ✅ |
| `OpenFace` | Medium | ~300ms |
| `DeepID` | Medium | ~400ms |

→ AMMS uses default FER+ model; satisfies < 200ms target.

---

## 5. Contextual Emotion Recognition

AMMS goes beyond single-frame classification by implementing **temporal smoothing** and **context fusion**:

### 5.1 Temporal Smoothing (Moving Average)

Single-frame FER is noisy. AMMS averages over a 10-frame window:

```python
from collections import deque
import statistics

class EmotionSmoother:
    def __init__(self, window=10):
        self.history = deque(maxlen=window)

    def update(self, emotion: str) -> str:
        self.history.append(emotion)
        # Return mode (most frequent in window)
        return statistics.mode(self.history)
```

### 5.2 Confidence Threshold

Only act on emotion if dominant score > 40%:

```python
CONFIDENCE_THRESHOLD = 0.40

def get_confident_emotion(result):
    dominant = result['dominant_emotion']
    confidence = result['emotion'][dominant] / 100.0
    if confidence >= CONFIDENCE_THRESHOLD:
        return dominant, confidence
    return 'neutral', confidence
```

---

## 6. Emotion–Feedback Mapping

| Detected Emotion | Motivation Category | Example AMMS Response |
|-----------------|--------------------|-----------------------|
| Happy | Celebration | "Keep that energy! What's got you smiling today?" |
| Sad | Encouragement | "It's okay to have tough days. You've got this 💙" |
| Angry | De-escalation | "Take a breath. This moment will pass." |
| Fearful | Reassurance | "Whatever's worrying you — you're stronger than it." |
| Neutral | Informational | [Standard morning briefing] |
| Surprised | Curiosity | "Something exciting happening? I'm ready to help!" |
| Disgusted | Redirect | "Let's shift focus — here's your schedule for today." |

---

## 7. Privacy Analysis for Emotion Detection

| Consideration | Decision |
|--------------|---------|
| Are emotion classifications stored? | Yes — in `emotion_history` table (for personalization) |
| Are raw frames stored? | No — only classification result |
| Can users opt out? | Yes — admin per-user toggle |
| Retention period | 30 days sliding window |
| Who can view history? | Admin only |

---

## 8. Related Research

### 8.1 Context-Aware Emotion Recognition

Kosti et al. (2017) showed that including **scene context** with facial features improved emotion classification by 8.2%:

```
Emotion = f(Face Features ⊕ Scene Features ⊕ Body Language)
```

AMMS v2 may incorporate time-of-day (morning vs evening) as contextual modulator.

### 8.2 Affective Computing Origins

Picard (1997) introduced the term **affective computing**: "computing that relates to, arises from, or deliberately influences emotions." AMMS is a direct application — sensing user affect and responding to optimise the morning routine experience.

---

## 9. References

1. Ekman, P. (1971). "Universals and cultural differences in facial expressions of emotion." *Nebraska Symposium on Motivation*, 19, 207-283.
2. Goodfellow, I. et al. (2013). "Challenges in Representation Learning: A Report on Three Machine Learning Contests." *ICANN 2013*.
3. Serengil, S.I. & Ozpinar, A. (2020). "LightFace: A Hybrid Deep Face Recognition Framework." *ASYU 2020*.
4. Kosti, R., Alvarez, J.M., Recasens, A., & Lapedriza, A. (2019). "Context Based Emotion Recognition using EMOTIC Dataset." *IEEE TPAMI*.
5. Picard, R.W. (1997). *Affective Computing.* MIT Press.
6. Zhang, K., Zhang, Z., Li, Z., & Qiao, Y. (2016). "Joint Face Detection and Alignment Using Multitask Cascaded Convolutional Networks." *IEEE SPL*, 23(10), 1499-1503.
