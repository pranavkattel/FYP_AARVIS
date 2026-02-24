# Role of Needs Analysis in Agile Projects
**Week 3 | Phase 1: Sprint Planning and Requirement Prioritization**
**Date Range:** 7 November – 8 November 2024

---

## 1. Introduction

In Agile software development, **needs analysis** is not a one-time activity confined to the beginning of a project — it is a continuous process woven into every sprint. This document explores how needs analysis supports agile delivery, particularly in the context of the AMMS project.

---

## 2. Agile Needs Analysis vs. Traditional Needs Analysis

### 2.1 Traditional (Plan-Driven) Approach
In Waterfall or V-Model, needs analysis is conducted upfront, resulting in a **Software Requirements Specification (SRS)** document that is agreed upon before development begins. Changes after sign-off are expensive and disruptive.

### 2.2 Agile Approach
In Agile, needs analysis is **incremental and iterative**:
- Requirements are captured as User Stories and placed in the **Product Backlog**
- The backlog is continuously refined (Backlog Grooming/Refinement)
- New needs can be added or re-prioritized at any time
- Acceptance criteria are defined just-in-time (before each sprint)

---

## 3. Business Analysis Activities in Each Scrum Event

### 3.1 Sprint Planning
**BA Activities:**
- Present user stories from top of backlog
- Clarify acceptance criteria
- Break epics into sprint-sized stories
- Assist team in estimating story points

**AMMS Application:**
At Sprint 1 planning, the BA (team member) clarified:
- What "face recognition" means in terms of matching accuracy
- What constitutes a "successful login" (95% confidence threshold)
- Error handling for unknown faces (graceful fallback to OTP)

### 3.2 Daily Scrum (Stand-up)
**BA Activities:**
- Listen for emerging requirements or scope creep
- Clarify ambiguities that arise during development
- Update acceptance criteria if needed

### 3.3 Sprint Review
**BA Activities:**
- Facilitate stakeholder feedback session
- Document new requirements emerging from demo
- Update backlog with new/revised items

### 3.4 Sprint Retrospective
**BA Activities:**
- Reflect on requirements quality for the completed sprint
- Identify requirement-related impediments
- Improve requirements process for next sprint

### 3.5 Backlog Refinement (Grooming)
**BA Activities:**
- Write/refine user stories for upcoming sprints
- Add/revise acceptance criteria
- Re-prioritize backlog items based on business value
- Decompose large epics into smaller stories

---

## 4. Needs Analysis Artifacts in Agile

### 4.1 Product Vision Statement
```
FOR morning routine users
WHO need personalized real-time information without device dependency
THE AMMS is an AI-powered smart mirror
THAT recognizes users, detects emotions, and delivers context-aware content
UNLIKE generic digital assistants
OUR PRODUCT delivers fully local, privacy-preserving, multimodal interaction.
```

### 4.2 User Personas

#### Persona 1: Ahmad (Primary User)
- **Age:** 28 | **Occupation:** Software Engineer
- **Morning Routine:** Wakes 7AM; checks phone for weather, email, news in 15 minutes
- **Goals:** Want updates without touching a device while getting ready
- **Pain Points:** Phone notifications are disruptive; worried about privacy
- **AMMS Needs:** Face login, calendar overview, voice email, local processing

#### Persona 2: Siti (Secondary User)
- **Age:** 25 | **Occupation:** Marketing Executive
- **Morning Routine:** Wakes 6:30AM; skincare routine takes 20 minutes
- **Goals:** Motivation to start the day; quick news update
- **Pain Points:** Feeling rushed; forgetting appointments
- **AMMS Needs:** Emotion-aware motivation, daily schedule display

#### Persona 3: Razif (Admin)
- **Age:** 35 | **Occupation:** Household administrator
- **Goals:** Manage family profiles on the mirror
- **AMMS Needs:** Admin panel, easy user add/remove, privacy controls

---

## 5. Needs Prioritization Techniques

### 5.1 MoSCoW Method
| Priority     | Definition                                    | AMMS Examples                          |
|--------------|-----------------------------------------------|----------------------------------------|
| **Must Have**    | Critical – system fails without it         | Face recognition, dashboard display    |
| **Should Have**  | Important – significant value              | Emotion detection, voice control       |
| **Could Have**   | Desirable – nice to have                   | WhatsApp integration, news feed        |
| **Won't Have**   | Not in this version                         | Mobile app, smart home control         |

### 5.2 Value vs. Effort Matrix
```
High Value, Low Effort (Quick Wins):
  - Display time/date
  - Weather widget
  - Basic face recognition

High Value, High Effort (Strategic):
  - Voice-controlled email
  - Local LLM integration
  - Emotion detection system

Low Value, Low Effort (Fill-ins):
  - Custom themes
  - Startup animation

Low Value, High Effort (Avoid):
  - Hardware gesture control
  - Full natural language query parsing
```

### 5.3 Kano Model Analysis
| Feature                     | Category    | User Satisfaction Impact |
|-----------------------------|-------------|--------------------------|
| Clock/time display          | Basic       | Expected, no delight      |
| Face recognition login      | Performance | Proportional to quality   |
| Emotion-aware motivation    | Excitement  | High delight if present   |
| Local AI processing         | Excitement  | High delight if present   |
| Voice email drafting        | Performance | Proportional to accuracy  |

---

## 6. Traceability in Agile

Each need must be traceable through the system:

```
Business Need → User Story → Acceptance Criteria → Sprint Task → Test Case → Feature
```

**AMMS Traceability Example:**
| Level              | Item                                                    |
|--------------------|---------------------------------------------------------|
| Business Need      | User wants to start their day with information          |
| User Story         | US-002: Display weather on dashboard                    |
| Acceptance Criteria| Weather shown within 3s; location-accurate; refreshes hourly |
| Sprint Task        | Integrate OpenWeatherMap API; cache responses           |
| Test Case          | TC-002: Weather widget renders with correct location    |
| Feature            | Weather Widget (Sprint 2)                               |

---

## 7. Common Needs Analysis Pitfalls in Agile

| Pitfall                   | Description                                           | Mitigation                                  |
|---------------------------|-------------------------------------------------------|---------------------------------------------|
| Gold Plating              | Developers add unrequested features                   | Strict DoD; backlog ownership               |
| Scope Creep               | Uncontrolled requirement growth                       | Sprint boundaries; Product Owner approval   |
| Ambiguous Stories         | Stories open to multiple interpretations              | Acceptance criteria; definition of "done"   |
| Missing Non-Functional Req| Focus only on features; ignore quality                | NFR checklist in backlog refinement         |
| No Stakeholder Buy-In     | Stakeholders not engaged throughout                   | Regular sprint reviews; feedback sessions   |

---

## 8. AMMS Needs Analysis Outcomes

After conducting needs analysis in Weeks 1–3:

✅ **14 User Stories** documented in product backlog
✅ **12 Functional Requirements** with acceptance criteria
✅ **8 Non-Functional Requirements** with measurable criteria
✅ **3 User Personas** created for design reference
✅ **MoSCoW prioritization** applied to all requirements
✅ **Sprint assignments** determined for all Must/Should features
✅ **Product Vision** statement authored

---

## 9. References

1. Brohl, C., Nelles, J., & Brandl, C. (2019). *What is the role of needs analysis in agile projects for Business Analysis.* International Journal of Agile Systems and Management.
2. Begel, A., & Nagappan, N. (2007). *Usage and perceptions of Agile software development in an industrial context.* IEEE ESEM.
3. Leffingwell, D. (2011). *Agile Software Requirements.* Addison-Wesley.
4. Cohn, M. (2009). *Succeeding with Agile.* Addison-Wesley Professional.
5. Kano, N., et al. (1984). *Attractive Quality and Must-Be Quality.* Journal of the Japanese Society for Quality Control.

---
*Document prepared as part of AMMS Week 3 – Product Backlog Creation*
