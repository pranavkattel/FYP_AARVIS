# User Requirements Analysis – AMMS (AI Mirror Management System)
**Week 1 | Phase 1: Project Initiation and Requirements Collection**
**Date Range:** 2 November – 3 November 2024

---

## 1. Overview

This document captures the comprehensive user requirements analysis for the **AI Mirror Management System (AMMS)** – an intelligent smart mirror platform that integrates facial recognition, emotion detection, motivational feedback, email/messaging integration, and real-time information display.

The purpose of this analysis is to:
- Identify functional and non-functional requirements
- Understand end-user expectations and pain points
- Establish a baseline for sprint planning and backlog creation

---

## 2. Stakeholder Identification

| Stakeholder         | Role                              | Interest                                    |
|---------------------|-----------------------------------|---------------------------------------------|
| End Users           | Primary users of smart mirror     | Seamless morning routine, personalization   |
| System Administrator| Manages mirror profiles/users     | Easy user management, security controls     |
| Developer Team      | Implements the system             | Clear requirements, feasible architecture   |
| Project Supervisor  | Academic oversight                | Research value, methodology compliance      |

---

## 3. User Needs Elicitation Methods

### 3.1 Online Review Analysis
Based on the methodology of Zheng et al. (2019), user requirements were extracted by analyzing:
- Product reviews from smart home devices (Amazon Echo, Google Nest Hub)
- Smart mirror community forums (Reddit r/SmartMirror, MagicMirror² community)
- Academic publications on user experience with ambient computing devices

### 3.2 Interviews and Surveys (Pre-Development)
A pre-development survey was designed to capture:
- Current morning routine pain points
- Desired smart mirror features
- Privacy concerns regarding facial recognition
- Preferred interaction modalities (voice, touch, gesture)

---

## 4. Functional Requirements

### 4.1 Core Features

| ID    | Requirement                                          | Priority | MoSCoW |
|-------|------------------------------------------------------|----------|--------|
| FR-01 | System shall recognize registered users via camera   | High     | Must   |
| FR-02 | System shall detect user emotional state             | High     | Must   |
| FR-03 | System shall deliver personalized morning briefings  | High     | Must   |
| FR-04 | System shall support voice-based interaction         | High     | Must   |
| FR-05 | System shall display real-time weather information   | Medium   | Should |
| FR-06 | System shall display calendar events                 | Medium   | Should |
| FR-07 | System shall send/read emails via voice command      | Medium   | Should |
| FR-08 | System shall provide motivational quotes/feedback    | Medium   | Should |
| FR-09 | System shall support multi-user profiles             | High     | Must   |
| FR-10 | System shall integrate WhatsApp messaging            | Low      | Could  |
| FR-11 | System shall support admin panel for user management | Medium   | Should |
| FR-12 | System shall function with local LLM for privacy     | High     | Must   |

### 4.2 Authentication Features

| ID    | Requirement                                              | Priority |
|-------|----------------------------------------------------------|----------|
| FR-13 | System shall authenticate users via facial recognition   | High     |
| FR-14 | System shall support OTP-based backup login              | Medium   |
| FR-15 | System shall lock after N failed recognition attempts    | High     |
| FR-16 | System shall maintain separate data per user profile     | High     |

---

## 5. Non-Functional Requirements

| ID     | Requirement                                              | Category         |
|--------|----------------------------------------------------------|------------------|
| NFR-01 | Face recognition response time < 2 seconds              | Performance      |
| NFR-02 | System accuracy ≥ 95% for registered users               | Accuracy         |
| NFR-03 | All processing done locally (no cloud for biometrics)    | Privacy/Security |
| NFR-04 | System uptime ≥ 99% during active hours                  | Reliability      |
| NFR-05 | UI must be readable at 0.5m–1.5m distance                | Usability        |
| NFR-06 | Boot time ≤ 30 seconds on Raspberry Pi                   | Performance      |
| NFR-07 | Voice recognition under ambient noise (up to 60dB)       | Robustness       |
| NFR-08 | System shall support minimum 5 simultaneous user profiles| Scalability      |

---

## 6. User Stories

### Epic 1: Facial Recognition & Authentication
```
As a registered user,
I want the mirror to recognize my face when I stand in front of it,
So that it can automatically load my personalized dashboard.

As an administrator,
I want to add/remove user profiles,
So that I can manage who has access to the smart mirror.
```

### Epic 2: Morning Briefings
```
As a user,
I want to see my calendar events, weather forecast, and top news
when I am identified in the morning,
So that I can plan my day without using my phone.
```

### Epic 3: Emotional Feedback
```
As a user,
I want the mirror to detect if I look stressed or unhappy,
So that it can display motivational messages tailored to my emotional state.
```

### Epic 4: Voice-Controlled Communication
```
As a user,
I want to dictate and send emails using voice commands,
So that I can communicate hands-free while getting ready.
```

---

## 7. Constraints and Assumptions

### Constraints
- Hardware limited to Raspberry Pi 4 (8GB RAM) or equivalent
- Display: 27-inch monitor with two-way mirror overlay
- Camera: USB webcam with minimum 720p resolution
- Network: Requires stable Wi-Fi for API calls (news, weather, calendar)
- All biometric data must be stored locally

### Assumptions
- Users are adults (18+) with basic familiarity with digital assistants
- Primary use case is the morning routine (6AM – 9AM)
- One mirror unit per household during prototype phase
- Internet connection available for non-biometric API services

---

## 8. Influencing Factors from Related Research

Based on analysis of academic literature on smart home requirements:

| Factor                  | Impact on AMMS Design                                    | Source           |
|-------------------------|----------------------------------------------------------|------------------|
| Privacy Concerns        | All facial data stored locally; no cloud upload          | Zheng et al., 2019|
| Usability at Distance   | UI elements min 24pt font; high contrast design          | Nielsen (2021)   |
| Wake-up Context         | Gentle briefings preferred; no alarming notifications    | Kim et al., 2020 |
| Hands-free Preference   | Voice-primary interaction model                          | Porcheron (2018) |
| Personalization Demand  | User-specific profiles for content, reminders, metrics  | Lee et al., 2021 |

---

## 9. Requirements Traceability Matrix (RTM) – Preview

| Req ID | Description                     | Sprint | Status      |
|--------|---------------------------------|--------|-------------|
| FR-01  | Face recognition login          | 1      | Planned     |
| FR-02  | Emotion detection               | 2      | Planned     |
| FR-03  | Morning briefing                | 2      | Planned     |
| FR-04  | Voice interaction               | 3      | Planned     |
| FR-07  | Email via voice                 | 6      | Planned     |
| FR-12  | Local LLM integration           | 3      | Planned     |

---

## 10. References

1. Zheng, S., et al. (2019). *Identification of User Requirements and their Influencing Factors Based on Online Reviews and Operational Data.* IEEE Access.
2. Lee, M., & Kwon, O. (2021). *Smart Mirror: A smart home solution for increased productivity during those busy mornings.* International Journal of Smart Home.
3. Nielsen Norman Group (2021). *User Experience in Ambient Computing Environments.* Retrieved from https://www.nngroup.com/
4. Porcheron, M., et al. (2018). *Voice Interfaces in Everyday Life.* ACM CHI 2018.
5. Kim, J., et al. (2020). *Morning Routines and Digital Assistants: A User Study.* UbiComp 2020.

---
*Document prepared as part of AMMS Week 1 – Project Initiation and Requirements Collection*
