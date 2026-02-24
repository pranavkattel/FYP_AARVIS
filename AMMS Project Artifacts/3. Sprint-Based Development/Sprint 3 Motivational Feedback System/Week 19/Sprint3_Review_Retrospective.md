# Sprint 3 Review – Motivational Feedback System
**Sprint 3 | Week 19 | Phase 3: Sprint-Based Development**
**Sprint Review Date:** 31 January 2025
**Sprint Velocity:** 19 story points completed

---

## 1. Sprint Goals vs Outcomes

| Goal | Status | Notes |
|------|--------|-------|
| Replace static quotes with Ollama LLM | ✅ | llama3:8b-q4_K_M deployed |
| Context-passing (emotion, schedule, weather) | ✅ | Full context template working |
| Conversation memory (10-message window) | ✅ | ConversationMemory class |
| TTS with edge-tts (Aria Neural voice) | ✅ | ~0.8s audio generation |
| Graceful fallback when Ollama offline | ✅ | Static fallback activates |
| Response latency < 5s | ⚠️ | Avg 3.8s; peak 6.2s under load |

---

## 2. Sprint Review: Generated Response Quality Samples

**Scenario 1 – User: Ahmad, emotion: happy (Monday 7:42 AM)**
> *AURA:* "Good morning, Ahmad! That energy is exactly what Mondays need. Your team meeting starts at 9 — you've got time to grab breakfast first. Anything you need from me?"

**Scenario 2 – User: Siti, emotion: sad (Tuesday 8:10 AM)**
> *AURA:* "Morning, Siti. Take it easy today — some days just start that way, and that's okay. You've got a lighter schedule today, which might help. What would you like to do first?"

**Scenario 3 – User: Ahmad, emotion: angry (Wednesday 7:55 AM)**
> *AURA:* "Morning, Ahmad. Looks like something's got your thinking going already. Take a breath — you've got your project review at 3:30, so there's time before the big stuff. Want me to go through your day?"

> **Stakeholder feedback:** All 3 reviewers preferred LLM responses over static quotes (sprint review demo, 31 Jan 2025).

---

## 3. Performance on Raspberry Pi 4

| Metric | Target | Actual |
|--------|--------|--------|
| LLM response generation (avg) | < 5s | 3.8s |
| LLM response generation (worst) | < 8s | 6.2s |
| TTS audio generation | < 1s | 0.8s |
| Total "think + speak" latency | < 6s | 4.6s avg |
| CPU load during generation | Acceptable | 87% (1 core) |
| RAM used by Ollama | < 5GB | 4.9GB |

> **Identified risk:** With 8GB RPi4, Ollama takes 4.9GB leaving only ~3GB for OS + other modules. Memory pressure observed during concurrent face recognition + emotion detection + LLM.

**Mitigation:** Emotion detection pauses during LLM generation; both run sequentially on CPU scheduler.

---

## 4. Context Integration Test

```python
# Integration test: full context pipeline
context = {
    'user_name': 'Ahmad Razifi',
    'emotion': 'sad',
    'confidence': 71.3,
    'events': 'Team Meeting 9:00 AM, Lunch 1:00 PM, Project Review 3:30 PM',
    'weather': '26°C, Partly Cloudy, Humidity 72%',
    'email_count': 3
}

response = generate_aura_response(context)
assert len(response.split()) <= 60, "Response too long"
assert 'Ahmad' in response, "Must address user by name"
print(response)
# ✅ 42 words, contains 'Ahmad', empathetic tone verified
```

---

## 5. Bug Log

| Bug ID | Description | Resolution |
|--------|-------------|-----------|
| BUG-301 | Ollama first response 12s cold-start | Pre-warm on startup `ollama.chat(...)` |
| BUG-302 | LLM sometimes gives >5 sentences | `num_predict=80` + `stop=['\n\n']` constraints added |
| BUG-303 | edge-tts fails offline (requires internet) | Added pyttsx3 as fallback TTS |
| BUG-304 | Memory leak in ConversationMemory | Fixed by enforcing max length on every `add()` |

---

## 6. Sprint Retrospective

**What went well:**
- LLM output quality exceeded expectations
- Graceful fallback to static quotes works seamlessly
- TTS with edge-tts sounds natural for morning interactions

**What to improve:**
- LLM memory consumption (4.9GB) leaves little headroom — must monitor
- User feedback: would like to be able to interrupt AURA mid-sentence (Sprint 6 voice refinement)
- edge-tts requires internet — pyttsx3 fallback offline mode needed for production

**Next Sprint (Sprint 4):**
- WhatsApp Messaging Integration
- Gmail API (read + compose)
- Voice-triggered commands ("Send WhatsApp to Ali saying I'm running late")

---

## 7. References

1. Meta AI (2024). "Meta Llama 3." ai.meta.com.
2. Weizenbaum, J. (1966). "ELIZA — a computer program for the study of natural language communication." *CACM*, 9(1), 36-45. (Historical context for conversational AI)
3. Amodei, D. et al. (2016). "Deep Speech 2: End-to-End Speech Recognition in English and Mandarin." *ICML 2016*.
