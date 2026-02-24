# AMMS Project Gantt Chart – Reference and Documentation
**Week 6 | Phase 1: Sprint Planning and Requirement Prioritization**
**Subfolder:** Gantt Chart/
**Date Range:** 13 November – 14 November 2024

---

## 1. Introduction to Gantt Charts

A **Gantt chart** is a type of bar chart that illustrates a project schedule, showing the start and finish dates of the various elements (phases, tasks, milestones). Named after Henry Gantt who popularized it in the 1910s, it remains one of the most widely used project scheduling tools.

### 1.1 Key Elements
| Element        | Description                                                  |
|----------------|--------------------------------------------------------------|
| **Task Bars**  | Horizontal bars representing duration of each task           |
| **Milestones** | Diamond shapes representing key deliverable dates            |
| **Dependencies**| Arrows showing predecessor-successor relationships          |
| **Critical Path** | Longest sequence of dependent tasks; delay impacts deadline|
| **WBS Number** | Work Breakdown Structure numbering for task hierarchy        |

### 1.2 Modern Gantt Chart Criticisms
While Gantt charts are widely used, researchers have noted limitations:
- **Static nature** — doesn't reflect changing priorities well
- **Illusion of precision** — exact dates often not realistic
- **Dependency overload** — complex projects become unreadable
- **Agile conflict** — rigid scheduling conflicts with iterative development

**Reconciliation for AMMS:** Using Gantt for high-level phase planning while Trello handles sprint-level task management.

---

## 2. AMMS Gantt Chart – Full Project Schedule

### 2.1 Project Overview
| Field               | Details                                     |
|---------------------|---------------------------------------------|
| Project Name        | AMMS – AI Mirror Management System          |
| Project Start       | 2 November 2024                             |
| Project End         | 22 March 2025                               |
| Total Duration      | ~20 weeks                                   |
| Methodology         | Agile/Scrum with phase-based planning        |
| Milestones          | 11 major milestones (M1–M11)                |

### 2.2 Phase Timeline

```
AMMS Project Timeline (Nov 2024 – Mar 2025)

Week:  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20
       Nov─────────────────────Dec────────────────Jan─────────Feb────Mar
       
PHASE 1: PROJECT INITIATION [█████████████████]
  1.1 Requirements         [█████]
  1.2 User Needs Analysis       [█████]
  1.3 Product Backlog                [███]
  1.4 Sprint Planning                    [███]
  1.5 Sprint Goals                           [███]
  1.6 Team Roles                                 [███]
  M1: Req Complete                                   ◆

PHASE 2: DESIGN [████████████████████]
  2.1 Core Architecture                              [████]
       - Face Recognition Module                     [██]
       - Emotion Detection Module                       [█]
       - Motivational Feedback Module                    [█]
       - Email Messaging Module                           [█]
       - Data Integration Display                          [█]
  2.2 Prototype Subsystems                                  [███████]
  2.3 Technical Diagrams                                            [████]
  2.4 User Feedback                                                     [███]
  2.5 Refine Design                                                          [███]
  M2: Design Complete                                                             ◆

PHASE 3: SPRINT DEVELOPMENT [████████████████████████████████████████████]
  Sprint 1: Face Recognition Auth                                                  [████████████]
  Sprint 2: Morning Briefings                                                                   [████████████]
  Sprint 3: AI Communication                                                                                [████████████]
  Sprint 4: Hardware Setup                                                                                              [████████████]
  Sprint 5: Voice Scheduling                                                                                                          [████████████]
  Sprint 6: Email Assistant                                                                                                                        [████████████]
  M8: Dev Complete                                                                                                                                             ◆

PHASE 4: CONTINUOUS TESTING [██████████████]
  Unit Testing                                                                                                                                                   [█████]
  Integration Testing                                                                                                                                                 [████]
  User Feedback Testing                                                                                                                                                    [███]
  Bug Fixes                                                                                                                                                                    [███]
  M9: Testing Complete                                                                                                                                                            ◆

PHASE 5: DOCUMENTATION [████████████████]
  Project Report                                                                                                                                                                  [█████]
  Future Enhancements                                                                                                                                                                  [████]
  User Documentation                                                                                                                                                                      [████]
  User Manual                                                                                                                                                                                 [████]
  Feature Guide                                                                                                                                                                                    [████]
  M10/M11: Project Complete                                                                                                                                                                            ◆
```

---

## 3. Milestone Summary

| Milestone | Description                        | Target Date       |
|-----------|------------------------------------|-------------------|
| **M1**    | Requirements Complete              | 18 November 2024  |
| **M2**    | Design Complete                    | 6 December 2024   |
| **M3**    | Facial Recognition Complete        | 18 December 2024  |
| **M4**    | Morning Briefings Complete         | 31 December 2024  |
| **M5**    | AI Communication Ready             | 14 January 2025   |
| **M6**    | Hardware Ready                     | 27 January 2025   |
| **M7**    | Voice Scheduling Ready             | 8 February 2025   |
| **M8**    | Email Assistant Complete           | 20 February 2025  |
| **M9**    | Testing Complete                   | 7 March 2025      |
| **M10**   | Documentation Complete             | 22 March 2025     |
| **M11**   | Project Complete                   | 22 March 2025     |

---

## 4. Work Breakdown Structure (WBS)

```
1. AMMS (Project)
├── 1.1 Phase 1: Project Initiation (6 tasks)
│   ├── 1.1.1 Identify AI Assistant Requirements
│   ├── 1.1.2 Conduct User Needs Analysis
│   ├── 1.1.3 Create Product Backlog
│   ├── 1.1.4 Sprint Planning
│   ├── 1.1.5 Define Sprint Goals and Timeline
│   ├── 1.1.6 Assign Team Roles
│   └── M1: Requirements Complete
├── 1.2 Phase 2: Design and Development (5 tasks)
│   ├── 1.2.1 Define Core System Architecture
│   │   ├── 1.2.1.1 Facial Recognition Module
│   │   ├── 1.2.1.2 Emotion Detection Module
│   │   ├── 1.2.1.3 Motivational Feedback Module
│   │   ├── 1.2.1.4 Email Messaging Module
│   │   └── 1.2.1.5 Data Integration Display
│   ├── 1.2.2 Prototype Subsystems
│   ├── 1.2.3 Create Technical Diagrams
│   ├── 1.2.4 Collect User Feedback
│   ├── 1.2.5 Refine Design
│   └── M2: Design Complete
├── 1.3 Phase 3: Sprint Development (6 sprints × 5 tasks)
│   ├── Sprint 1: Facial Recognition (M3)
│   ├── Sprint 2: Morning Briefings (M4)
│   ├── Sprint 3: AI Communication (M5)
│   ├── Sprint 4: Hardware Setup (M6)
│   ├── Sprint 5: Voice Scheduling (M7)
│   └── Sprint 6: Email Assistant (M8)
├── 1.4 Phase 4: Continuous Testing (4 groups)
│   ├── 1.4.1 Unit Testing
│   ├── 1.4.2 Integration Testing
│   ├── 1.4.3 User Feedback Testing
│   ├── 1.4.4 Bug Fixes
│   └── M9: Testing Complete
└── 1.5 Phase 5: Documentation (6 tasks)
    ├── 1.5.1 Project Report
    ├── 1.5.2 Report Writing
    ├── 1.5.3 Future Enhancements Documentation
    ├── 1.5.4 User Documentation
    ├── 1.5.5 User Manual
    ├── 1.5.6 Feature Guide and FAQ
    ├── M10: Documentation Complete
    └── M11: Project Complete
```

---

## 5. Critical Path Analysis

The **Critical Path** identifies tasks where any delay will delay the project completion.

**AMMS Critical Path:**
```
Requirements (M1) → Design (M2) → Sprint 1 Face Recognition (M3) → Sprint 2 Briefings (M4) 
→ Sprint 3 AI Communication (M5) → Sprint 4 Hardware (M6) → Sprint 5 Scheduling (M7) 
→ Sprint 6 Email (M8) → Unit Testing → Integration Testing → Bug Fixes (M9) 
→ Report Writing → Documentation (M10/M11)
```

**Total Critical Path Duration:** 20 weeks (140 days)

**Parallel (Non-Critical) Activities:**
- Market research (can run during requirements phase)
- Literature review (can run throughout)
- Hardware procurement (can start during design)

---

## 6. References

1. Geraldi, J., & Lechler, T. (2012). *Gantt charts revisited: A critical analysis of its roots and implications to the management of projects today.* International Journal of Managing Projects in Business.
2. PMI (2021). *A Guide to the Project Management Body of Knowledge (PMBOK® Guide)* (7th ed.). Project Management Institute.
3. Gantt, H.L. (1919). *Organizing for Work.* Harcourt, Brace and Howe.
4. Kerzner, H. (2017). *Project Management: A Systems Approach to Planning, Scheduling, and Controlling.* Wiley.

---
*Document prepared as part of AMMS Week 6 – Assign Team Roles for Sprint*
