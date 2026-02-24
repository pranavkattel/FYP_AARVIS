# Product Backlog Prioritization – AMMS
**Week 4 | Phase 1: Sprint Planning and Requirement Prioritization**
**Date Range:** 9 November – 10 November 2024

---

## 1. Introduction to Product Backlog Management

The **Product Backlog** is the single source of truth for all work that needs to be done on the AMMS project. It is an ordered list of everything that is known to be needed — features, bug fixes, technical tasks, knowledge acquisition — managed by the Product Owner.

Effective backlog prioritization ensures the team always works on the **most valuable items first**, maximizing return on investment and ensuring early risk mitigation.

---

## 2. AMMS Complete Product Backlog

### 2.1 Epic Breakdown

**Epic 1: Core Authentication System**
| Story ID | Title                                               | Priority | Story Points | Sprint  |
|----------|-----------------------------------------------------|----------|--------------|---------|
| US-001   | Face recognition login for registered users         | 1        | 8            | Sprint 1|
| US-010   | Multi-user profile management                       | 5        | 5            | Sprint 1|
| US-011   | Admin panel for user CRUD                           | 6        | 5            | Sprint 1|
| US-015   | OTP backup authentication                           | 10       | 3            | Sprint 1|
| US-016   | Face recognition confidence threshold setting       | 12       | 3            | Sprint 1|

**Epic 2: Information Display System**
| Story ID | Title                                               | Priority | Story Points | Sprint  |
|----------|-----------------------------------------------------|----------|--------------|---------|
| US-002   | Display real-time weather forecast                  | 2        | 3            | Sprint 2|
| US-003   | Display daily calendar events                       | 3        | 3            | Sprint 2|
| US-012   | Display curated news briefings                      | 7        | 3            | Sprint 2|
| US-017   | Display current time and date                       | 8        | 1            | Sprint 2|
| US-018   | Display stock/financial summary                     | 15       | 3            | Sprint 5|

**Epic 3: Emotion & Motivational System**
| Story ID | Title                                               | Priority | Story Points | Sprint  |
|----------|-----------------------------------------------------|----------|--------------|---------|
| US-004   | Real-time emotion detection from camera             | 4        | 8            | Sprint 2|
| US-005   | Display emotion-adaptive motivational messages      | 9        | 5            | Sprint 3|
| US-019   | Log emotion history per user                        | 13       | 3            | Sprint 3|

**Epic 4: AI Conversation System**
| Story ID | Title                                               | Priority | Story Points | Sprint  |
|----------|-----------------------------------------------------|----------|--------------|---------|
| US-006   | Voice-controlled interaction (STT + TTS)            | 11       | 8            | Sprint 3|
| US-009   | Local LLM for conversational AI                     | 14       | 13           | Sprint 3|
| US-020   | Multi-turn conversation context management          | 16       | 5            | Sprint 3|

**Epic 5: Communication Integration**
| Story ID | Title                                               | Priority | Story Points | Sprint  |
|----------|-----------------------------------------------------|----------|--------------|---------|
| US-007   | Read email summaries via voice                      | 17       | 5            | Sprint 6|
| US-008   | Draft and send email via voice                      | 18       | 8            | Sprint 6|
| US-013   | WhatsApp notification display                       | 19       | 8            | Sprint 4|
| US-021   | WhatsApp reply via voice                            | 20       | 8            | Sprint 4|

**Epic 6: Scheduling System**
| Story ID | Title                                               | Priority | Story Points | Sprint  |
|----------|-----------------------------------------------------|----------|--------------|---------|
| US-014   | Voice-controlled calendar event creation            | 21       | 8            | Sprint 5|
| US-022   | Event reminder notifications                        | 22       | 3            | Sprint 5|
| US-023   | Calendar conflict detection                         | 23       | 5            | Sprint 5|

---

## 3. Prioritization Methods Applied

### 3.1 WSJF – Weighted Shortest Job First (SAFe)

WSJF = (Business Value + Time Criticality + Risk Reduction) / Job Duration

| Story  | BV (1-10) | TC (1-10) | RR (1-10) | Size | WSJF Score | Priority |
|--------|-----------|-----------|-----------|------|------------|----------|
| US-001 | 9         | 8         | 9         | 8    | 3.25       | 1        |
| US-004 | 8         | 6         | 7         | 8    | 2.63       | 4        |
| US-009 | 9         | 8         | 9         | 13   | 2.00       | 6        |
| US-002 | 7         | 5         | 3         | 3    | 5.00       | 2        |
| US-003 | 7         | 5         | 3         | 3    | 5.00       | 3        |
| US-006 | 8         | 7         | 6         | 8    | 2.63       | 5        |

### 3.2 Value vs. Risk Matrix
- **High Value + High Risk → Sprint Early:** US-001 (Face Recognition), US-009 (Local LLM)
- **High Value + Low Risk → Sprint Mid:** US-002, US-003, US-012 (Widgets)
- **Low Value + High Risk → Deprioritize or Spike:** US-021 (WhatsApp voice reply)
- **Low Value + Low Risk → Fill-in:** US-017 (Clock display)

---

## 4. Sprint Allocation Summary

| Sprint   | Theme                              | Stories                      | Total Points |
|----------|------------------------------------|------------------------------|--------------|
| Sprint 1 | Facial Recognition Auth            | US-001, US-010, US-011, US-015, US-016 | 24 |
| Sprint 2 | Briefings & Emotion Detection      | US-002, US-003, US-004, US-012, US-017 | 18 |
| Sprint 3 | AI Communication                   | US-005, US-006, US-009, US-019, US-020 | 34 |
| Sprint 4 | WhatsApp Integration               | US-013, US-021              | 16           |
| Sprint 5 | Scheduling & Info Display          | US-014, US-018, US-022, US-023 | 19        |
| Sprint 6 | Email Assistant                    | US-007, US-008              | 13           |

**Total Story Points: 124**
**Velocity Target: ~21 points/sprint** (based on team size and 2-week sprints)

---

## 5. Backlog Refinement Process

### 5.1 Refinement Meeting Cadence
- **Frequency:** Weekly (mid-sprint)
- **Duration:** 1-2 hours
- **Participants:** Product Owner, Scrum Master, Development Team

### 5.2 Refinement Checklist
For each story to be sprint-ready (INVEST criteria):

| Criterion | Description                                          |
|-----------|------------------------------------------------------|
| **I**ndependent | Story can be developed independently           |
| **N**egotiable  | Details are open to discussion                 |
| **V**aluable    | Delivers value to user or business             |
| **E**stimable   | Team can size it in story points               |
| **S**mall       | Fits within a single sprint                   |
| **T**estable    | Has clear acceptance criteria                  |

### 5.3 Story Splitting Techniques

When a story is too large (>13 points), split by:
- **Workflow Steps:** Break the user journey into steps
- **Business Rules:** Separate for each business rule variation
- **Data Variations:** Different data types as separate stories
- **Interface Variations:** Desktop/mobile/voice as separate stories
- **Happy/Sad Path:** Core flow first; error handling later

---

## 6. Backlog Health Metrics

| Metric                        | Target  | AMMS Current Status |
|-------------------------------|---------|---------------------|
| Stories in Ready state        | Top 10  | 14 ready            |
| Stories with acceptance criteria | 100% | 86% (12/14)         |
| Stories sized > 13 (need split)| 0%    | 7% (1/14 - US-009)  |
| Sprint backlog change rate     | < 20%  | Tracking needed     |
| Team velocity                  | Stable | Establishing        |

---

## 7. AMMS Sprint Goal Statements

**Sprint 1:** *"By the end of Sprint 1, registered users can authenticate into the smart mirror using facial recognition, and an admin can manage user profiles."*

**Sprint 2:** *"By the end of Sprint 2, the mirror displays a personalized morning briefing (weather, calendar, news) triggered by face detection, along with real-time emotion analysis."*

**Sprint 3:** *"By the end of Sprint 3, users can have a multi-turn voice conversation with the mirror, powered by a locally running LLM."*

**Sprint 4:** *"By the end of Sprint 4, WhatsApp notifications are visible on the mirror display and can be replied to using voice commands."*

**Sprint 5:** *"By the end of Sprint 5, users can create, view, and receive reminders for calendar events using voice commands."*

**Sprint 6:** *"By the end of Sprint 6, users can dictate emails, receive email summaries, and send replies — all via voice commands."*

---

## 8. References

1. Wiegers, K. (1999). *First Things First: Prioritizing Requirements.* Software Development Magazine.
2. Leffingwell, D. (2020). *SAFe 5.0 Reference Guide: Scaled Agile Framework for Lean Enterprises.* Addison-Wesley.
3. Pichler, R. (2016). *Strategize: Product Strategy and Product Roadmap Practices.* Pichler Consulting.
4. Patton, J. (2014). *User Story Mapping.* O'Reilly Media.
5. Rubin, K.S. (2012). *Essential Scrum: A Practical Guide to the Most Popular Agile Process.* Addison-Wesley.

---
*Document prepared as part of AMMS Week 4 – Sprint Planning*
