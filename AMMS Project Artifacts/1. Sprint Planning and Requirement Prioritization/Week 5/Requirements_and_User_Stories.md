# Requirements and User Stories – Complete Reference
**Week 5 | Phase 1: Sprint Planning and Requirement Prioritization**
**Date Range:** 11 November – 12 November 2024

---

## 1. Introduction

This document provides the complete set of refined **requirements** and **user stories** for the AMMS project, incorporating feedback from Week 1–4 analysis. All stories follow the standard Agile format with full acceptance criteria.

---

## 2. Core Principles for Writing Effective User Stories

### 2.1 The 3 Cs of User Stories (Ron Jeffries)
- **Card:** Brief written description of the story (fits on an index card)
- **Conversation:** Ongoing dialogue between team and stakeholder about the story
- **Confirmation:** Acceptance criteria that confirm the story is complete

### 2.2 INVEST Criteria
All AMMS stories must satisfy INVEST before being sprint-ready:
- **I**ndependent — Can be built separately from other stories
- **N**egotiable — Implementation details are flexible
- **V**aluable — Provides user or business value
- **E**stimable — Can be sized in story points
- **S**mall — Can be completed within one sprint
- **T**estable — Has measurable acceptance criteria

---

## 3. Full User Story Catalog

### EPIC 1: AUTHENTICATION

---
**US-001: Face Recognition Login**
```
AS A registered user
I WANT the mirror to recognize my face when I approach
SO THAT I can access my personalized dashboard without manual input

ACCEPTANCE CRITERIA:
GIVEN I am standing 0.5–1.5m from the mirror
WHEN my face is captured by the camera
THEN the system identifies me within 2 seconds with ≥95% confidence
AND my personalized dashboard loads automatically
AND a welcome message with my name appears

GIVEN an unrecognized face is detected
WHEN the system fails to match after 3 attempts
THEN an OTP-based login option is offered

STORY POINTS: 8 | SPRINT: 1 | PRIORITY: 1
```

---
**US-010: Multi-User Profile Management**
```
AS AN administrator
I WANT to create, edit, and delete user profiles
SO THAT multiple household members can use the mirror

ACCEPTANCE CRITERIA:
GIVEN I am logged in as admin
WHEN I navigate to the admin panel
THEN I can add a new user with name and face enrollment
AND I can update existing user information
AND I can delete a user and remove their face data

STORY POINTS: 5 | SPRINT: 1 | PRIORITY: 5
```

---
**US-011: Admin Panel**
```
AS AN administrator
I WANT a dedicated admin interface on the mirror
SO THAT I can manage system settings and users

ACCEPTANCE CRITERIA:
GIVEN I authenticate as admin via face recognition
WHEN I access the admin panel
THEN I see user management, system settings, and logs

STORY POINTS: 5 | SPRINT: 1 | PRIORITY: 6
```

---

### EPIC 2: MORNING BRIEFINGS

---
**US-002: Weather Display**
```
AS A user
I WANT to see the current weather and 3-day forecast on the mirror
SO THAT I can plan my outfit and commute accordingly

ACCEPTANCE CRITERIA:
GIVEN my profile is loaded
WHEN the morning briefing starts
THEN weather for my saved location is displayed
AND it includes: temperature, humidity, conditions, and 3-day forecast
AND data refreshes every 30 minutes

STORY POINTS: 3 | SPRINT: 2 | PRIORITY: 2
```

---
**US-003: Calendar Display**
```
AS A user
I WANT to see today's and tomorrow's calendar events
SO THAT I don't miss appointments while getting ready

ACCEPTANCE CRITERIA:
GIVEN my Google Calendar is linked
WHEN my briefing loads
THEN today's events are shown in chronological order
AND event names, times, and locations are displayed
AND "No events today" is shown if calendar is empty

STORY POINTS: 3 | SPRINT: 2 | PRIORITY: 3
```

---
**US-012: News Briefing**
```
AS A user
I WANT to see top 5 news headlines relevant to my interests
SO THAT I stay informed without checking my phone

ACCEPTANCE CRITERIA:
GIVEN my topic preferences are configured
WHEN the briefing loads
THEN 5 relevant headlines are displayed, categorized by topic
AND articles are less than 24 hours old
AND I can ask the mirror to read a headline aloud

STORY POINTS: 3 | SPRINT: 2 | PRIORITY: 7
```

---

### EPIC 3: EMOTION & MOTIVATION

---
**US-004: Emotion Detection**
```
AS A user
I WANT the mirror to detect my facial emotion
SO THAT it can provide context-aware content

ACCEPTANCE CRITERIA:
GIVEN I am standing in front of the mirror with adequate lighting
WHEN the camera captures my face
THEN one of 7 emotions is detected: Happy, Sad, Angry, Fearful, Disgusted, Surprised, Neutral
AND emotion detection completes within 1 second
AND result is used to personalize displayed content

STORY POINTS: 8 | SPRINT: 2 | PRIORITY: 4
```

---
**US-005: Motivational Feedback**
```
AS A user
I WANT to receive motivational messages tailored to my detected emotion
SO THAT I feel supported and positive before starting my day

ACCEPTANCE CRITERIA:
GIVEN my emotion has been detected
WHEN the emotion is Sad, Angry, or Fearful
THEN a motivational quote/message is displayed
AND the message is relevant to the detected emotion
AND messages rotate each session (no repeats within 7 days)

GIVEN emotion is Happy or Neutral
THEN an encouraging or informational message is shown

STORY POINTS: 5 | SPRINT: 3 | PRIORITY: 9
```

---

### EPIC 4: VOICE & AI CONVERSATION

---
**US-006: Voice Interaction**
```
AS A user
I WANT to control the mirror using voice commands
SO THAT I can interact hands-free while getting ready

ACCEPTANCE CRITERIA:
GIVEN I say the wake word "AURA"
WHEN I speak a command
THEN the system transcribes speech to text within 1 second
AND responds with audible text-to-speech output within 2 seconds
AND executes the requested action (if valid command)

GIVEN ambient noise ≤ 60dB
THEN voice recognition accuracy ≥ 90%

STORY POINTS: 8 | SPRINT: 3 | PRIORITY: 11
```

---
**US-009: Local LLM Integration**
```
AS A user
I WANT to have a natural conversation with the mirror's AI
SO THAT I can ask questions and get intelligent responses without internet

ACCEPTANCE CRITERIA:
GIVEN the local LLM is running (Ollama + LLaMA 3)
WHEN I ask a question verbally
THEN the LLM generates a relevant, coherent response
AND response time is ≤ 5 seconds on Raspberry Pi 4
AND no data is sent to external AI services
AND multi-turn conversation context is maintained for 5+ turns

STORY POINTS: 13 | SPRINT: 3 | PRIORITY: 14
```

---

### EPIC 5: COMMUNICATION

---
**US-007: Email Summary Reading**
```
AS A user
I WANT the mirror to read my unread email summaries aloud
SO THAT I can stay on top of important emails hands-free

ACCEPTANCE CRITERIA:
GIVEN my Gmail account is authorized
WHEN I say "Read my emails"
THEN the system fetches and summarizes the top 5 unread emails
AND reads them aloud using TTS
AND can navigate to next/previous email on voice command

STORY POINTS: 5 | SPRINT: 6 | PRIORITY: 17
```

---
**US-008: Voice Email Drafting**
```
AS A user
I WANT to draft and send emails using voice dictation
SO THAT I can communicate without using my phone

ACCEPTANCE CRITERIA:
GIVEN I say "Send email to [name]"
WHEN I dictate the subject and body
THEN the mirror displays the drafted email for confirmation
AND I can say "Send" or "Cancel"
AND sent emails appear in Gmail Sent folder
AND email is sent via Gmail API

STORY POINTS: 8 | SPRINT: 6 | PRIORITY: 18
```

---

### EPIC 6: SCHEDULING

---
**US-014: Voice Calendar Scheduling**
```
AS A user
I WANT to create calendar events using voice commands
SO THAT I can schedule appointments without typing

ACCEPTANCE CRITERIA:
GIVEN I say "Schedule a meeting"
WHEN I provide event details verbally (title, date, time, location)
THEN the event is created in my Google Calendar
AND a confirmation is displayed and read aloud
AND conflicts with existing events are flagged

STORY POINTS: 8 | SPRINT: 5 | PRIORITY: 21
```

---

## 4. Story Map Overview

```
USER JOURNEY: Morning Routine

[Arrive at Mirror]
    ↓
[Face Recognition Login: US-001]
    ↓
[Emotion Detection: US-004]
    ↓
[Morning Briefing Dashboard: US-002, US-003, US-012, US-017]
    ↓
[Motivational Feedback: US-005]
    ↓
[Voice Interaction: US-006]
    ├─→ [Ask AI questions: US-009]
    ├─→ [Check/Send Email: US-007, US-008]
    ├─→ [Schedule Events: US-014]
    └─→ [See WhatsApp notifications: US-013]
```

---

## 5. Definition of Ready (DoR)

A user story is **Ready** for sprint planning when:
- [ ] Written in correct user story format
- [ ] Story points estimated by team
- [ ] Acceptance criteria defined and agreed
- [ ] Dependencies identified
- [ ] UI mockup/wireframe linked (if applicable)
- [ ] API or technical requirements noted
- [ ] Fits within one sprint

---

## 6. Definition of Done (DoD)

A user story is **Done** when:
- [ ] All acceptance criteria met
- [ ] Code committed to Git repository
- [ ] Unit tests written and passing (≥80% coverage)
- [ ] Integration tested with connected components
- [ ] Demonstrated in Sprint Review
- [ ] No critical bugs remaining
- [ ] Documentation updated

---

## 7. References

1. Cohn, M. (2004). *User Stories Applied: For Agile Software Development.* Addison-Wesley.
2. Wiegers, K., & Beatty, J. (2013). *Software Requirements* (3rd ed.). Microsoft Press.
3. Wake, B. (2003). *INVEST in Good Stories, and SMART Tasks.* XP123. https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
4. Jeffries, R. (2001). *Essential XP: Card, Conversation, Confirmation.* XProgramming.com
5. Patton, J. (2014). *User Story Mapping.* O'Reilly Media.

---
*Document prepared as part of AMMS Week 5 – Define Sprint Goals and Timeline*
