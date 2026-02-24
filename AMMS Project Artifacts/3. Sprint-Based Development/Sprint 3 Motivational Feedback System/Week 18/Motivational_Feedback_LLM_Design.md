# Motivational Feedback System – LLM Integration with Ollama
**Sprint 3 | Week 18 | Phase 3: Sprint-Based Development**
**Sprint Goal:** Replace static quotes with dynamic LLM-generated motivational responses
**Date Range:** 20 – 24 January 2025

---

## 1. Sprint 3 Overview

Sprint 3 upgrades the static quote system from Sprint 2 into a dynamic, context-aware motivational feedback engine powered by a locally running Large Language Model (LLM) via Ollama.

### 1.1 Motivation for LLM Integration

| Static Quotes (Sprint 2) | Dynamic LLM (Sprint 3) |
|--------------------------|------------------------|
| Fixed 5-10 quotes per emotion | Unlimited unique responses |
| No personalisation beyond name | Knows user's schedule, weather, history |
| No conversation flow | Can respond to follow-up questions |
| Zero compute overhead | ~2–4s generation time |

---

## 2. Ollama and LLaMA 3

### 2.1 What is Ollama?

Ollama is an open-source tool for running LLMs locally on a machine:

```bash
# Install Ollama (Linux/macOS/Windows)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull LLaMA 3 8B model (quantised, 4.7GB)
ollama pull llama3

# Start Ollama server (runs on http://localhost:11434)
ollama serve
```

### 2.2 LLaMA 3 Model Specs (Quantised)

| Variant | Params | Disk | RAM (loaded) | RPi4 Performance |
|---------|--------|------|--------------|-----------------|
| llama3:8b-q4_K_M | 8B | 4.7GB | ~5GB | ~2.8 tokens/sec |
| llama3:8b-q2_K | 8B | 2.7GB | ~4GB | ~4.1 tokens/sec |
| llama3:70b (any) | 70B | 40GB+ | 40GB+ | ❌ Not feasible |

**AMMS Selection:** `llama3:8b-q4_K_M` — balance of quality and speed on 8GB RPi4.

### 2.3 Ollama Python API

```python
import ollama

response = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_message}
    ],
    options={'temperature': 0.7, 'top_p': 0.9}
)
text = response['message']['content']
```

---

## 3. AURA System Prompt (Full)

```
You are AURA (Adaptive User-Responsive Assistant), the AI personality of a smart mirror.
You are warm, encouraging, brief, and professional.

CONTEXT:
- User name: {user_name}
- Current time: {current_time}
- Day: {day_of_week}
- Detected emotion: {emotion} (confidence: {confidence}%)
- Today's events: {calendar_summary}
- Weather: {weather_summary}
- Unread emails: {email_count}

RULES:
1. Response must be 1-3 sentences maximum (user is standing at a mirror)
2. Address the user by first name
3. Acknowledge their detected emotion naturally (do NOT say "I detect you are X")
4. If emotion is sad/fearful/angry: be empathetic before anything else
5. If emotion is happy/neutral: be energetic and forward-looking
6. Optionally mention one calendar event or weather point if relevant
7. Never be preachy or give unsolicited life advice
8. Never make medical/health claims
9. End with a simple call to action ("Ask me anything" or similar)
```

### 3.1 Filled Example

```
You are AURA...
CONTEXT:
- User name: Ahmad Razifi
- Current time: 7:42 AM
- Day: Monday
- Detected emotion: sad (confidence: 71%)
- Today's events: Team meeting 9 AM, Lunch 1 PM
- Weather: 26°C, partly cloudy
- Unread emails: 3

→ AURA response:
"Good morning, Ahmad. Mondays can feel heavy sometimes — take it one hour at a time. 
You've got your team meeting at 9, so let's get you ready for that. 
What do you need from me today?"
```

---

## 4. Feedback Engine v2 Code

```python
"""
AMMS Motivational Feedback Engine v2 - LLM-powered
Sprint 3
"""

import ollama
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

SYSTEM_TEMPLATE = """You are AURA (Adaptive User-Responsive Assistant), the AI personality of a smart mirror.
You are warm, encouraging, brief, and professional.

CONTEXT:
- User: {user_name}
- Time: {time}
- Day: {day}
- Emotion: {emotion} ({confidence}% confidence)
- Schedule: {events}
- Weather: {weather}
- Emails: {email_count} unread

RULES: 1-3 sentences max. Address user by name. Acknowledge emotion naturally. 
No preachiness. End with a simple question or offer."""


def generate_aura_response(context: dict) -> str:
    """Generate contextual motivational response via Ollama."""

    system = SYSTEM_TEMPLATE.format(
        user_name=context.get('user_name', 'User'),
        time=datetime.now().strftime('%I:%M %p'),
        day=datetime.now().strftime('%A'),
        emotion=context.get('emotion', 'neutral'),
        confidence=context.get('confidence', 0),
        events=context.get('events', 'No events today'),
        weather=context.get('weather', 'Unknown'),
        email_count=context.get('email_count', 0)
    )

    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': 'Good morning.'}
            ],
            options={
                'temperature': 0.7,
                'top_p': 0.9,
                'num_predict': 80,      # Max tokens (keep short)
                'stop': ['\n\n', '---']
            }
        )
        return response['message']['content'].strip()

    except Exception as e:
        logger.error(f"Ollama error: {e}")
        # Fallback to static
        return _static_fallback(context.get('emotion', 'neutral'),
                                 context.get('user_name', ''))


def _static_fallback(emotion: str, name: str) -> str:
    fallbacks = {
        'happy': f"Good morning, {name}! You're doing great — keep going!",
        'sad': f"Hang in there, {name}. Every day is a new chance.",
        'angry': f"Take a breath, {name}. You've got this.",
        'neutral': f"Good morning, {name}. Let's make today count."
    }
    return fallbacks.get(emotion, fallbacks['neutral'])
```

---

## 5. Conversation Memory

AMMS implements a **10-message sliding window** for conversational context:

```python
class ConversationMemory:
    def __init__(self, max_messages=10):
        self.history = []
        self.max = max_messages

    def add(self, role: str, content: str):
        self.history.append({'role': role, 'content': content})
        if len(self.history) > self.max:
            # Keep system prompt + trim oldest
            self.history = self.history[:1] + self.history[-(self.max-1):]

    def get_messages(self, system_prompt: str) -> list:
        return [{'role': 'system', 'content': system_prompt}] + self.history
```

---

## 6. TTS Integration (Text-to-Speech)

AURA's responses are spoken aloud using `edge-tts`:

```python
import asyncio
import edge_tts

async def speak(text: str, voice='en-US-AriaNeural'):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save('/tmp/aura_response.mp3')

# In sync context:
asyncio.run(speak(aura_response))
os.system('mpg123 -q /tmp/aura_response.mp3')
```

**Voice options evaluated:**

| Voice | Style | Quality | Verdict |
|-------|-------|---------|---------|
| en-US-AriaNeural | Conversational, warm | Excellent | ✅ Selected |
| en-US-JennyNeural | Professional | Good | Backup |
| en-GB-SoniaNeural | British, formal | Good | Alternative |

---

## 7. References

1. Touvron, H. et al. (2023). "Llama 2: Open Foundation and Fine-Tuned Chat Models." arXiv:2307.09288.
2. Meta AI (2024). "Introducing Meta Llama 3." ai.meta.com/blog.
3. Ollama (2024). *Ollama Documentation*. ollama.ai.
4. Chen, L., Lu, H., et al. (2021). "Dimensional Emotion Recognition." *IEEE Trans. Affective Computing*.
5. edge-tts (2024). *Microsoft Edge TTS Python wrapper*. GitHub: rany2/edge-tts.
