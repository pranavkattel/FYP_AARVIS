# Requirements Analysis in Software Development – Research Reference
**Week 3 | Phase 1: Sprint Planning and Requirement Prioritization**
**Date Range:** 7 November – 8 November 2024

---

## 1. What is Requirements Analysis?

**Requirements analysis** is the process of determining user expectations for a new or modified software product. It is a critical phase in the Software Development Life Cycle (SDLC) that bridges the gap between end-user needs and technical specifications.

According to IEEE Standard 830-1998, requirements must be:
- **Complete** – all requirements are documented
- **Consistent** – no contradictions between requirements
- **Unambiguous** – single interpretation possible
- **Verifiable** – can be tested or measured
- **Traceable** – linked to source and to design/testing

---

## 2. Types of Requirements

### 2.1 Functional Requirements (FR)
Define what the system **should do** — specific behaviors, functions, and features.

**Examples for AMMS:**
- The system shall recognize registered users through the camera
- The system shall display weather information on the mirror dashboard
- The system shall allow voice-commanded email drafting

### 2.2 Non-Functional Requirements (NFR)
Define **how well** the system performs — quality attributes and constraints.

| Category      | Example for AMMS                                          |
|---------------|-----------------------------------------------------------|
| Performance   | Face recognition must complete in < 2 seconds             |
| Security      | All biometric data must be encrypted at rest              |
| Usability     | UI must be readable at 0.5–1.5m distance                  |
| Reliability   | System uptime ≥ 99% during 6AM–9AM usage window           |
| Portability   | System must run on Raspberry Pi 4 (8GB RAM)               |
| Privacy       | No biometric data transmitted to external services        |

### 2.3 Domain Requirements
Constraints arising from the domain the system operates in.

**For AMMS:**
- Compliance with Malaysia Personal Data Protection Act (PDPA 2010)
- Following IEEE standards for biometric system design
- Hardware constraints of Raspberry Pi platform

---

## 3. Requirements Elicitation Techniques

### 3.1 Interviews
- One-on-one sessions with potential users
- Structured, semi-structured, or unstructured
- Best for: deep understanding of individual needs

### 3.2 Questionnaires/Surveys
- Large-scale data collection
- Pre-development survey conducted for AMMS (see Week 10 Pre-Survey Results)
- Best for: quantitative data from many respondents

### 3.3 Observation
- Watching users in their natural environment
- Applied to observe morning routines in AMMS context
- Best for: discovering unstated or habitual needs

### 3.4 Prototyping
- Build rough version; collect feedback
- Applied in AMMS design phase (Week 9 wireframes)
- Best for: visual/UX requirements validation

### 3.5 Document Analysis
- Review existing systems, research papers, market reports
- Applied to analyze MagicMirror², commercial solutions
- Best for: benchmarking and gap analysis

### 3.6 Brainstorming
- Group ideation sessions for feature identification
- Applied in AMMS Sprint Planning sessions
- Best for: creative alternative generation

---

## 4. Requirements Analysis Process

```
     ┌─────────────────┐
     │  Stakeholder     │
     │  Identification  │
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │  Requirements   │
     │  Elicitation    │
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │  Requirements   │
     │  Analysis &     │
     │  Negotiation    │
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │  Requirements   │
     │  Specification  │
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │  Requirements   │
     │  Validation     │
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │  Requirements   │
     │  Management     │
     └─────────────────┘
```

---

## 5. Role of Needs Analysis in Agile Projects

### 5.1 Agile vs. Traditional Requirements Analysis

| Aspect                     | Traditional                     | Agile                              |
|----------------------------|---------------------------------|------------------------------------|
| Timing                     | Upfront, before development     | Continuous, just-in-time           |
| Documentation              | Comprehensive, formal           | Lightweight, user stories          |
| Stakeholder involvement    | Initial phase only              | Throughout all sprints             |
| Change accommodation       | Costly and difficult            | Expected and welcomed              |
| Requirements form          | Formal specification document   | Product backlog + acceptance criteria |

### 5.2 User Stories as Agile Requirements

The standard format:
```
As a [role],
I want [capability],
So that [business value/outcome].
```

**Acceptance Criteria:**
Each user story must have defined acceptance criteria using **Given-When-Then** (Gherkin) format:
```
GIVEN [initial context]
WHEN [action performed]
THEN [expected outcome]
```

**Example for AMMS:**
```
Story: Face Recognition Login
As a registered user,
I want the mirror to recognize my face automatically,
So that my personalized dashboard loads without manual login.

Acceptance Criteria:
GIVEN I am registered in the system
WHEN I stand 0.5–1.5m in front of the mirror
THEN my dashboard loads within 2 seconds with 95% accuracy
```

### 5.3 Business Analysis in Agile (Scrum)

The **Business Analyst (BA)** role in Agile:
- Bridges the gap between Product Owner and Development Team
- Responsible for backlog refinement and story decomposition
- Facilitates requirements workshops and sprint planning
- Creates acceptance criteria for user stories

---

## 6. Requirements Documentation for AMMS

### 6.1 Product Backlog (Top Items)

| Story ID | User Story                                              | Priority | Story Points |
|----------|---------------------------------------------------------|----------|--------------|
| US-001   | Face recognition login                                  | 1        | 8            |
| US-002   | Display weather on dashboard                            | 2        | 3            |
| US-003   | Display calendar events                                 | 3        | 3            |
| US-004   | Emotion detection from camera                           | 4        | 8            |
| US-005   | Display motivational messages by emotion                | 5        | 5            |
| US-006   | Voice-controlled interaction                            | 6        | 8            |
| US-007   | Read email summaries aloud                              | 7        | 5            |
| US-008   | Draft and send email by voice                           | 8        | 8            |
| US-009   | Local LLM for conversational AI                         | 9        | 13           |
| US-010   | Multi-user profile management                           | 10       | 5            |
| US-011   | Admin panel for user CRUD operations                    | 11       | 5            |
| US-012   | Display news briefings                                  | 12       | 3            |
| US-013   | WhatsApp notification integration                       | 13       | 8            |
| US-014   | Voice-controlled calendar scheduling                    | 14       | 8            |

### 6.2 Story Point Scale (Fibonacci)
| Points | Effort Level        |
|--------|---------------------|
| 1      | Trivial             |
| 2      | Very Small          |
| 3      | Small               |
| 5      | Medium              |
| 8      | Large               |
| 13     | Very Large          |
| 21     | Huge (must split)   |

---

## 7. Requirements Validation Checklist

- [ ] Each requirement is testable
- [ ] No duplicate or conflicting requirements
- [ ] All functional requirements tied to a user story
- [ ] Non-functional requirements have measurable criteria
- [ ] All stakeholders have reviewed and signed off
- [ ] Requirements traced to sprint/milestone
- [ ] Edge cases and error scenarios documented

---

## 8. References

1. Sommerville, I. (2015). *Software Engineering* (10th ed.). Pearson Education.
2. Cohn, M. (2004). *User Stories Applied: For Agile Software Development.* Addison-Wesley.
3. Wiegers, K., & Beatty, J. (2013). *Software Requirements* (3rd ed.). Microsoft Press.
4. IEEE (1998). *IEEE Recommended Practice for Software Requirements Specifications (IEEE Std 830-1998).*
5. Racheva, Z., et al. (2010). *Do We Know Enough About Requirements Prioritization in Agile Projects?* IEEE REFSQ.
6. Inayat, I., et al. (2015). *A Systematic Literature Review on Agile Requirements Engineering Practices and Challenges.* Computers in Human Behavior.

---
*Document prepared as part of AMMS Week 3 – Product Backlog Creation*
