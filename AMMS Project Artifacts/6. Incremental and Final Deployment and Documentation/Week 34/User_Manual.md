# AMMS (AURA Smart Mirror) – User Manual
**Week 34 | Phase 6: Incremental and Final Deployment and Documentation**
**Document Version:** 1.0 | Date: 12 May 2025
**Audience:** End users (daily users + administrators)

---

## 1. Welcome to AURA

AURA is your intelligent smart mirror assistant. It recognises your face, reads your emotions, and delivers a personalised morning briefing — all without connecting to the cloud.

**What AURA can do:**
- Log you in automatically using face recognition
- Show your calendar, weather, and news at a glance
- Detect your mood and offer a motivational message
- Answer questions and take voice commands
- Send WhatsApp messages and emails by voice
- Read your inbox aloud

---

## 2. Getting Started (Users)

### 2.1 First Time Use

1. An **administrator** must first enrol your face (see Admin section)
2. Stand in front of the mirror — AURA will begin scanning
3. The idle screen shows the clock and weather while scanning

### 2.2 Logging In

```
1. Stand 40–80 cm from mirror, looking directly at camera
2. Hold steady for 1–2 seconds
3. Blink naturally when prompted (anti-spoofing check)
4. Your dashboard appears with personalised content
```

**Troubleshooting login:**

| Problem | Solution |
|---------|---------|
| "Scanning…" stays on screen | Ensure face is fully visible; check lighting |
| "User not recognised" | Ask admin to re-enrol or update your face data |
| Login takes > 5 seconds | Step back slightly; avoid strong backlight |

---

## 3. Using AURA Voice Assistant

### 3.1 Waking Up AURA

Say the wake word: **"AURA"**

- You will see the AURA listening animation
- A soft chime will play
- You have 7 seconds to speak your command

### 3.2 Voice Commands Reference

| Command | Example |
|---------|---------|
| Ask about schedule | "What's on my calendar today?" |
| Ask about weather | "What's the weather today?" / "Will it rain this afternoon?" |
| Read news | "What are today's headlines?" |
| Read emails | "Read my emails" / "Any urgent emails?" |
| Send email | "Send an email to Ali with subject project update saying I've finished the report" |
| Send WhatsApp | "Send a WhatsApp to Siti saying I'm on my way" |
| General question | "What is the capital of Japan?" |
| Stop listening | "Stop" / "Cancel" / "Never mind" |

### 3.3 Sending Messages (Confirmation Flow)

When you ask AURA to send a message, it will always confirm first:

> **AURA:** "Sending to Ali Hasan (+60123456789): 'I'm on my way.' Shall I send it?"  
> **You:** "Yes" / "Send it" / "Go ahead"  
> **AURA:** "Message sent to Ali."

To cancel: say "No" / "Cancel" / "Don't send"

---

## 4. Dashboard Widgets Explained

```
┌────────────────────────────────────────────────────────────┐
│  ① TIME & GREETING   │  ② WEATHER + FORECAST             │
│  Good morning, Ahmad │  26°C KL | Mon ☀ Tue 🌧 Wed ⛅     │
├──────────────────────┴───────────────────────────────────  │
│  📣 "That smile says it all. Let's make magic today!"      │ ③
├────────────────────────┬───────────────────────────────────│
│  📅 SCHEDULE           │  📰 NEWS                         │
│  09:00 Team Meeting   │  • KLSE hits 5-year high          │ ④⑤
│  13:00 Lunch          │  • New AI model released          │
│  15:30 Project Review │  • Malaysia budget: highlights    │
├────────────────────────┴───────────────────────────────────│
│  🔔 3 emails (1 urgent) | 2 new WhatsApps                  │ ⑥
└────────────────────────────────────────────────────────────┘
```

| # | Widget | Updates |
|---|--------|---------|
| ① | Clock, date, greeting | Every second |
| ② | Weather + 3-day forecast | Every 10 minutes |
| ③ | Emotion-based motivational quote | Changes on emotion detection |
| ④ | Today's calendar events | Every 5 minutes |
| ⑤ | Top 5 news headlines | Every 30 minutes |
| ⑥ | Email/WhatsApp count | Every 3 minutes |

---

## 5. Emotion Icons Guide

| Icon | Detected Emotion | What AURA Does |
|------|-----------------|----------------|
| 😊 | Happy | Celebratory message |
| 😢 | Sad | Encouraging message |
| 😠 | Angry | Calming reminder |
| 😨 | Fearful | Reassuring message |
| 😲 | Surprised | Curious/engaging message |
| 😐 | Neutral | Standard briefing |

> Emotion detection is automatic. If you prefer privacy, ask your administrator to disable it for your profile.

---

## 6. For Administrators

### 6.1 Accessing the Admin Panel

Via browser on any device connected to the same Wi-Fi:
```
http://amms.local:5000/admin
```

Or directly on the mirror (keyboard shortcut if connected): **Ctrl+Shift+A**

### 6.2 Enrolling a New User

1. Go to **Admin Panel → Users → [+ Add New User]**
2. Enter the user's full name
3. Click **"Start Face Capture"**
4. Guide the user to stand in front of the mirror
5. System captures 10 sample frames automatically
6. Click **"Save User"** — enrolment complete

**Tips for good enrolment:**
- Ensure good, even lighting (no strong backlight)
- Capture at the normal standing distance (60–80 cm)
- Remove hat/sunglasses during enrolment
- Make sure the person looks directly at camera at least 5 of 10 captures

### 6.3 Managing Users

| Action | Steps |
|--------|-------|
| View users | Admin Panel → Users |
| Disable user (temporary) | Click user → Toggle "Active" off |
| Delete user permanently | Click user → Delete → Confirm |
| Update (re-enrol) | Delete → Re-enrol with new captures |

### 6.4 System Status

Admin Panel → System shows:
- Camera status, Mic status, LLM status
- Storage usage, uptime
- Today's login count

---

## 7. Privacy Information

- **Your face data** is stored as a mathematical vector only (not an image). It is never transmitted to the internet.
- **Emotion logs** are stored locally and viewable only by the system administrator. You can request deletion at any time.
- **Voice commands** are processed locally using Whisper AI. Audio is not recorded or stored.
- **Emails and WhatsApp** are only accessed when you request it. The system does not scan messages passively.

To request deletion of your data: Ask your administrator to remove your profile from the Admin Panel.

---

## 8. Troubleshooting

| Problem | Solution |
|---------|---------|
| Mirror display is blank | Check HDMI connection; `sudo systemctl status amms` |
| AURA doesn't respond to wake word | Move closer; speak clearly; check microphone connection |
| Calendar not showing | Google OAuth token may need refresh — ask admin |
| "LLM offline" | Ollama service may need restart: `sudo systemctl restart ollama` |
| Weather shows "Unavailable" | Check internet connection; OWM API key may be invalid |

---

## 9. Quick Reference Card

```
╔══════════════════════════════════════════╗
║         AURA SMART MIRROR                ║
║         Quick Reference                  ║
╠══════════════════════════════════════════╣
║  Wake word: "AURA"                       ║
║  Login: Stand 60-80cm, look at camera   ║
╠══════════════════════════════════════════╣
║  KEY COMMANDS:                           ║
║  "What's my schedule?"                  ║
║  "What's the weather?"                  ║
║  "Read my emails"                        ║
║  "Send WhatsApp to [Name] saying [msg]" ║
║  "Send email to [Name]..."              ║
╚══════════════════════════════════════════╝
```
