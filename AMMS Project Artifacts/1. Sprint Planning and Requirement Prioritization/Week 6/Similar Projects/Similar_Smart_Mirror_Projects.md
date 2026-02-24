# Similar Projects – Smart Mirror Research Survey
**Week 6 | Phase 1: Sprint Planning and Requirement Prioritization**
**Subfolder:** Similar Projects/
**Date Range:** 13 November – 14 November 2024

---

## 1. Overview

This document surveys existing smart mirror projects from academic, open-source, and commercial sources to:
1. Identify best practices and proven implementations
2. Understand the state-of-the-art in smart mirror technology
3. Differentiate AMMS from existing solutions
4. Extract technical insights to accelerate development

---

## 2. Academic Smart Mirror Projects

### 2.1 Smart Mirror: A Reflective Interface to Maximize Productivity
**Authors:** Johnson, K., Park, S., & Chung, H. (2022)
**Published:** IEEE International Conference on Smart Systems

**Summary:**
This study presents a Raspberry Pi-based smart mirror designed to function as a productivity platform for home environments. The system integrates:
- Morning briefings (weather, news, calendar)
- Productivity timer with Pomodoro technique
- Goal tracking and habit visualizer

**Key Findings:**
- Users reported 27% improvement in morning routine efficiency
- Average glance time per widget: 2.3 seconds (design implication: optimize for quick reading)
- Weather and calendar were most frequently used widgets

**Relevance to AMMS:**
- Validates the morning briefing concept
- Provides UX benchmarks for display density and font sizing
- Suggests calendar integration as high-value feature

---

### 2.2 Smart Mirror for Emotion Monitoring in Home Environments
**Authors:** Haddad, R., Abboud, A., & Chalhoub, G. (2022)
**Published:** Sensors (MDPI)

**Summary:**
Proposes an IoT-enabled smart mirror that continuously monitors occupant emotional states using a CNN-based facial expression recognition model. The mirror provides:
- Real-time emotion classification (7 classes using FER2013 dataset)
- Emotion-adaptive ambient lighting control
- Daily emotion trend visualization

**Key Technical Details:**
- **Model:** MobileNetV2 fine-tuned on FER2013 (68.4% accuracy on test set)
- **Processing:** Raspberry Pi 4 with TensorFlow Lite
- **Latency:** 1.2 seconds per emotion classification
- **Lighting:** PWM-controlled RGB LED strips responding to detected emotion

**Relevance to AMMS:**
- Validates emotion detection as technically feasible on Raspberry Pi
- Identifies MobileNetV2 + TFLite as viable architecture
- Emotion-adaptive content is proven to increase user satisfaction (+31% in study)
- 7-class emotion model aligns with AMMS requirements

---

### 2.3 MirrorME: Facial Recognition and Personalized Information
**Authors:** Santos, F., et al. (2020)
**Published:** IEEE CIVEMSA

**Summary:**
MirrorME implements a smart mirror with face recognition for user identification and personalized content delivery. The system:
- Uses Eigenfaces + SVM for recognition (later updated to FaceNet)
- Delivers user-specific news, weather, and transport information
- Implements privacy-preserving local face storage

**Key Technical Details:**
- **Recognition:** FaceNet (128-d embeddings) + cosine similarity
- **Accuracy:** 97.3% on 10-user household test
- **Response Time:** 1.4 seconds average
- **Platform:** Raspberry Pi 3B+

**Relevance to AMMS:**
- Directly comparable to AMMS face recognition module
- FaceNet reference architecture validates our approach
- 97.3% accuracy on 10 users is target benchmark for AMMS
- Privacy-first local storage design confirmed as standard

---

### 2.4 Smart Mirror for Ambient Home Environment
**Authors:** Westelinck, C., et al. (2022)
**Published:** IEEE Smart Cities Conference

**Summary:**
Presents an ambient smart mirror integrating multiple IoT sensors for comprehensive home environment monitoring:
- Temperature, humidity, air quality sensors
- Weather API integration
- Ambient display of all environmental metrics
- Alert system for dangerous conditions

**Relevance to AMMS:**
- Establishes IoT integration patterns for smart mirror
- Alert generation concept applicable to AMMS notification system
- Environmental context could enrich AMMS morning briefings

---

### 2.5 Smart Mirror for Healthy Lifestyle
**Authors:** Mennicken, S., et al. (2016)
**Published:** CHI 2016 – Extended Abstracts

**Summary:**
Explores smart mirrors for promoting healthy behaviors through:
- Activity goal visualization
- Nutrition reminders
- Sleep quality feedback
- Positive reinforcement messaging

**Relevance to AMMS:**
- Motivational feedback approach aligns with AMMS Sprint 3 (Motivational Feedback System)
- Positive reinforcement through mirrors proven effective: 68% of users reported increased motivation
- Design patterns for non-intrusive wellness messaging

---

### 2.6 Smart Mirror for Smart Life
**Authors:** Chen, W., et al. (2019)
**Published:** International Journal of Advanced Computer Science

**Summary:**
A comprehensive smart mirror implementation covering:
- Voice command integration ("Hey Mirror")
- Calendar and reminder display
- Social media notification display
- Fitness tracker integration

**Relevance to AMMS:**
- Voice wake-word implementation directly relevant to AMMS Sprint 3
- "Hey Mirror" concept adapted to "AURA" for AMMS
- Social media notifications pattern applicable to WhatsApp integration (Sprint 4)

---

## 3. Open Source Projects

### 3.1 MagicMirror²
- **Platform:** GitHub (nischi/MagicMirror) — 14,000+ stars
- **Technology:** Node.js + Electron, Raspberry Pi
- **Architecture:** Module-based plugin system
- **Modules Available:** 200+ community modules (weather, calendar, news, clocks, transit)
- **Limitations:** No built-in face recognition; no AI; no voice; no emotion detection

**AMMS Learning:**
- Modular architecture is the right approach for extensibility
- Widget layout system provides inspiration for AMMS dashboard
- Open-source community validates Raspberry Pi as viable platform

### 3.2 JARVIS Smart Mirror
- **GitHub:** several implementations
- **Features:** Google Assistant integration, face recognition (add-on), home automation
- **Limitation:** Relies heavily on cloud AI (Google/Amazon), compromising privacy

**AMMS Learning:**
- Cloud AI creates privacy concerns — validates AMMS local AI approach
- JARVIS demonstrates that assistant integration is demanded by users

---

## 4. Commercial Products

### 4.1 HiMirror Plus
| Feature              | Details                                              |
|----------------------|------------------------------------------------------|
| Primary Function     | Skin analysis and beauty tracking                   |
| AI Features          | Skin condition scoring, beauty AI                   |
| Display              | Built-in screen behind mirror glass                 |
| Price                | ~USD 199                                            |
| Gap vs. AMMS         | No face recognition, no email/calendar, no voice AI |

### 4.2 Amazon Echo Show 15
| Feature              | Details                                              |
|----------------------|------------------------------------------------------|
| Primary Function     | Smart display + Alexa voice assistant               |
| AI Features          | Visual ID (optional), Alexa, smart home control     |
| Privacy              | Cloud-based processing (privacy concern)            |
| Price                | ~USD 249                                            |
| Gap vs. AMMS         | Not a mirror; cloud-dependent; limited customization|

### 4.3 Capstone Smart Mirror (Samsung Research, 2023)
| Feature              | Details                                              |
|----------------------|------------------------------------------------------|
| Primary Function     | IoT hub + beauty mirror                             |
| AI Features          | Visual recognition, scene understanding             |
| Target Market        | Premium residential (USD 2,000+)                   |
| Gap vs. AMMS         | Commercial/proprietary; no open-source access       |

---

## 5. Comparative Feature Matrix

| Feature                          | AMMS | MagicMirror² | MirrorME | Echo Show 15 | HiMirror |
|----------------------------------|------|--------------|----------|--------------|---------|
| Face Recognition Login           | ✅   | ❌(module)   | ✅       | Partial      | ❌      |
| Emotion Detection                | ✅   | ❌           | ❌       | ❌           | Partial |
| Motivational Feedback (AI)       | ✅   | ❌           | ❌       | Partial      | Partial |
| Local LLM (Privacy-Preserving)   | ✅   | ❌           | ❌       | ❌           | ❌      |
| Voice Interaction                | ✅   | ❌           | ❌       | ✅(cloud)    | ❌      |
| Email Integration                | ✅   | ✅(module)   | ❌       | ✅(cloud)    | ❌      |
| Calendar Integration             | ✅   | ✅(module)   | ✅       | ✅           | ❌      |
| WhatsApp Integration             | ✅   | ❌           | ❌       | ❌           | ❌      |
| News Briefings                   | ✅   | ✅(module)   | ✅       | ✅           | ❌      |
| Multi-user Profiles              | ✅   | ✅(module)   | ✅       | ✅           | ❌      |
| Open Source                      | ✅   | ✅           | ✅       | ❌           | ❌      |
| Runs Fully Local                 | ✅   | ✅           | ✅       | ❌           | ❌      |
| Raspberry Pi Compatible          | ✅   | ✅           | ✅       | ❌           | ❌      |

---

## 6. Key Insights and AMMS Differentiators

1. **No existing system** combines face recognition + emotion detection + local LLM + email in one integrated platform
2. **Privacy-first architecture** (fully local processing) is a key market differentiator
3. **WhatsApp integration** is unique — no academic or open-source mirror does this
4. **Motivational AI** tied to real-time emotion detection is novel
5. **Open-source on Raspberry Pi** makes this replicable and research-validatable

---

## 7. References

1. Johnson, K., Park, S., & Chung, H. (2022). *Smart Mirror: A Reflective Interface to Maximize Productivity.* IEEE Smart Systems.
2. Haddad, R., Abboud, A., & Chalhoub, G. (2022). *A Smart Mirror for Emotion Monitoring in Home Environments.* Sensors (MDPI).
3. Santos, F., et al. (2020). *MirrorME: Implementation of an IoT-based Smart Mirror through Facial Recognition and Personalized Information.* IEEE CIVEMSA.
4. Westelinck, C., et al. (2022). *Smart mirror for ambient home environment.* IEEE Smart Cities.
5. Mennicken, S., et al. (2016). *A smart mirror to promote a healthy lifestyle.* ACM CHI Extended Abstracts.
6. Chen, W., et al. (2019). *Smart mirror for smart life.* International Journal of Advanced Computer Science.

---
*Document prepared as part of AMMS Week 6 – M1 Requirements Complete*
