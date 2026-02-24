# AMMS Use Case Diagram
**Week 9 | Phase 2: Iterative System Design and Prototyping**
**Subfolder:** Use Case Diagram/
**Date Range:** 29 November – 1 December 2024

---

## 1. Use Case Diagram (Textual Representation)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AMMS USE CASE DIAGRAM                           │
│                                                                         │
│    ┌─────────────┐                                    ┌───────────────┐ │
│    │             │                                    │ External APIs │ │
│    │  REGISTERED │                                    │ (Weather/Cal/ │ │
│    │    USER     │                                    │  News/Gmail)  │ │
│    │             │                                    └───────────────┘ │
│    └──────┬──────┘                                           │          │
│           │                          ┌────────────────────── ↓──────┐   │
│           ├──────────────────────────→  (UC-01) Face Recognition    │   │
│           │                          │  Login                       │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           ├──────────────────────────→  (UC-02) View Morning       │   │
│           │                          │  Briefing Dashboard         │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           ├──────────────────────────→  (UC-03) Receive Emotion-   │   │
│           │                          │  Adaptive Motivation        │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           ├──────────────────────────→  (UC-04) Voice Interaction  │   │
│           │                          │  (Wake "AURA")              │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           ├──────────────────────────→  (UC-05) Ask AI Questions   │   │
│           │                          │  (Local LLM)                │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           ├──────────────────────────→  (UC-06) Read Email Summary │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           ├──────────────────────────→  (UC-07) Draft & Send Email │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           ├──────────────────────────→  (UC-08) View Calendar      │   │
│           │                          │  Events                     │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           ├──────────────────────────→  (UC-09) Schedule Events    │   │
│           │                          │  via Voice                  │   │
│           │                          └──────────────────────────────┘   │
│           │                          ┌──────────────────────────────┐   │
│           └──────────────────────────→  (UC-10) View WhatsApp      │   │
│                                      │  Notifications              │   │
│                                      └──────────────────────────────┘   │
│                                                                         │
│    ┌─────────────────┐                                                  │
│    │                 │               ┌──────────────────────────────┐   │
│    │  ADMINISTRATOR  ├───────────────→  (UC-11) Manage User Profiles│   │
│    │                 │               │  (Add/Edit/Delete)          │   │
│    │                 │               └──────────────────────────────┘   │
│    │                 │               ┌──────────────────────────────┐   │
│    │                 ├───────────────→  (UC-12) Enroll New User    │   │
│    │                 │               │  (Face Capture)             │   │
│    │                 │               └──────────────────────────────┘   │
│    │                 │               ┌──────────────────────────────┐   │
│    │                 ├───────────────→  (UC-13) Configure System   │   │
│    │                 │               │  Settings                   │   │
│    │                 │               └──────────────────────────────┘   │
│    │                 │               ┌──────────────────────────────┐   │
│    │                 └───────────────→  (UC-14) View System Logs   │   │
│    └─────────────────┘               └──────────────────────────────┘   │
│                                                                         │
│    ┌─────────────────┐               ┌──────────────────────────────┐   │
│    │   GUEST USER    ├───────────────→  (UC-15) Register / Request  │   │
│    │  (Unrecognized) │               │  Profile Creation            │   │
│    └─────────────────┘               └──────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

«include» relationships:
UC-02 «include» UC-01  (briefing requires login)
UC-03 «include» UC-01  (motivation requires login + emotion)
UC-06 «include» UC-04  (email reading uses voice)
UC-07 «include» UC-04  (email drafting uses voice)
UC-09 «include» UC-04  (scheduling uses voice)

«extend» relationships:
UC-12 «extend» UC-11  (face enrollment extends user management)
UC-04 «extend» UC-05  (voice command can trigger AI conversation)
```

---

## 2. Use Case Descriptions

### UC-01: Face Recognition Login
| Field | Details |
|-------|---------|
| **Actor** | Registered User |
| **Preconditions** | User face enrolled in system; camera active |
| **Basic Flow** | User approaches mirror → camera captures frame → system detects face → extracts encoding → matches against DB → loads profile |
| **Alternate Flow** | Low confidence → retry up to 3 times → offer OTP login |
| **Postconditions** | User session active; personalized dashboard displayed |
| **Exception** | Camera offline → display error; request admin |

---

### UC-03: Receive Emotion-Adaptive Motivation
| Field | Details |
|-------|---------|
| **Actor** | Registered User |
| **Preconditions** | UC-01 complete; emotion detection enabled |
| **Basic Flow** | Face recognized → emotion detected → content engine selects appropriate quote/message → displayed on mirror + spoken via TTS |
| **Alternate Flow** | Emotion neutral → display standard motivational content |
| **Postconditions** | Motivational content displayed; logged to emotion history |
| **Exception** | Emotion model unavailable → display default content |

---

### UC-07: Draft & Send Email via Voice
| Field | Details |
|-------|---------|
| **Actor** | Registered User |
| **Preconditions** | Gmail OAuth token valid; voice system active |
| **Basic Flow** | User says "Send email to [name]" → system confirms recipient → asks for subject → asks for body → shows draft → confirms → sends via Gmail API |
| **Alternate Flow** | Recipient not found → ask for email address directly |
| **Postconditions** | Email sent and confirmed; display shows confirmation |
| **Exception** | Gmail API error → notify user; offer retry |

---

### UC-11: Manage User Profiles
| Field | Details |
|-------|---------|
| **Actor** | Administrator |
| **Preconditions** | Admin authenticated via face recognition |
| **Basic Flow** | Admin views user list → selects action (add/edit/delete) → confirms action → system updates DB |
| **Alternate Flow** | Delete user → GDPR-compliant data removal (face encodings + profile) |
| **Postconditions** | User DB updated; changes reflected immediately |
| **Exception** | Cannot delete admin account; minimum 1 admin required |

---

## 3. Use Case Priority Matrix

| Use Case | Frequency | Complexity | Business Value | Sprint |
|----------|-----------|------------|----------------|--------|
| UC-01 Face Login | Very High | High | Critical | 1 |
| UC-02 View Briefing | Very High | Medium | High | 2 |
| UC-03 Motivation | High | Medium | High | 2-3 |
| UC-04 Voice | High | High | High | 3 |
| UC-05 Ask AI | Medium | High | Medium | 3 |
| UC-07 Send Email | Medium | High | High | 6 |
| UC-11 Admin | Low | Medium | Critical | 1 |

---
*Document prepared as part of AMMS Week 9 – Technical Diagrams (Use Case)*
