# Trello as an Agile Project Management Tool – Reference Guide
**Week 5 | Phase 1: Sprint Planning and Requirement Prioritization**
**Subfolder:** Trello/
**Date Range:** 11 November – 12 November 2024

---

## 1. Introduction to Trello

**Trello** is a visual, web-based project management tool that uses **boards, lists, and cards** to organize work. Developed by Atlassian, Trello is widely used in Agile teams due to its intuitive Kanban-style interface.

In the context of the AMMS project, Trello serves as the **digital Scrum board** for:
- Maintaining and prioritizing the Product Backlog
- Managing Sprint Boards (To Do → In Progress → Done)
- Tracking milestones and dependencies
- Team communication via card comments

---

## 2. Trello Core Concepts

### 2.1 Boards
A **Board** represents the entire project or a single sprint. It contains all Lists and Cards for that scope.

**AMMS Boards:**
1. **AMMS Product Backlog** – all user stories ordered by priority
2. **Sprint 1 Board** – Facial Recognition Auth sprint tasks
3. **Sprint 2 Board** – Morning Briefings sprint tasks
4. *(and so on for each sprint)*

### 2.2 Lists
**Lists** represent workflow stages (columns) in the board.

**Standard AMMS Sprint Board Lists:**
```
| Product Backlog | Sprint Backlog | In Progress | In Review | Done |
```

**AMMS Backlog Board Lists:**
```
| Icebox | Backlog | Sprint-Ready | Blocked |
```

### 2.3 Cards
A **Card** represents a single task, user story, or work item. Cards contain:
- Title (user story ID + summary)
- Description (full user story + acceptance criteria)
- Labels (by priority/category)
- Checklist (subtasks/acceptance criteria)
- Due date
- Assigned team members
- Attachments (wireframes, designs)
- Comments (discussion thread)

---

## 3. AMMS Trello Board Structure

### 3.1 Product Backlog Board

**Board Name:** AMMS – Product Backlog

| List: EPIC 1: Authentication | List: EPIC 2: Briefings | List: EPIC 3: Emotion | List: EPIC 4: AI | List: EPIC 5: Comms | List: EPIC 6: Schedule |
|------------------------------|-------------------------|-----------------------|------------------|---------------------|------------------------|
| US-001: Face Login ⭐⭐⭐⭐⭐ | US-002: Weather ⭐⭐⭐⭐⭐ | US-004: Emotion ⭐⭐⭐⭐ | US-006: Voice ⭐⭐⭐ | US-013: WhatsApp ⭐⭐ | US-014: Schedule ⭐⭐ |
| US-010: Multi-user ⭐⭐⭐⭐ | US-003: Calendar ⭐⭐⭐⭐ | US-005: Motivation ⭐⭐⭐ | US-009: LLM ⭐⭐⭐ | US-007: Email Read ⭐⭐ | US-022: Reminders ⭐ |
| US-011: Admin Panel ⭐⭐⭐ | US-012: News ⭐⭐⭐ | US-019: Emotion Log ⭐⭐ | US-020: Context ⭐⭐ | US-008: Email Draft ⭐⭐ | US-023: Conflicts ⭐ |

### 3.2 Sprint Board Layout (Example: Sprint 1)

**Board Name:** AMMS Sprint 1 – Facial Recognition Auth

```
┌─────────────────────────────────────────────────────────────────────────────┐
│   SPRINT 1 BOARD: Facial Recognition Authentication                         │
│   Sprint Duration: Dec 7–18, 2024 | Goal: Working face login + admin panel  │
├──────────────┬──────────────┬──────────────┬──────────────┬─────────────────┤
│ Sprint       │    To Do     │ In Progress  │  In Review   │      Done       │
│  Backlog     │              │              │              │                 │
├──────────────┼──────────────┼──────────────┼──────────────┼─────────────────┤
│ US-015: OTP  │ US-001:      │              │              │ ENV SETUP       │
│  Backup      │ Face Login   │              │              │ (prereq done)   │
│              │              │              │              │                 │
│ US-016:      │ US-010:      │              │              │                 │
│  Threshold   │ Multi-User   │              │              │                 │
│              │              │              │              │                 │
│              │ US-011:      │              │              │                 │
│              │ Admin Panel  │              │              │                 │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────────────┘
```

---

## 4. AMMS Trello Card Example (Detailed)

### Card: US-001 – Face Recognition Login

**Title:** `[US-001] Face Recognition Login (8 pts)`

**Labels:**
- 🔴 High Priority
- 🔵 Sprint 1
- 🟢 AI/Computer Vision

**Description:**
```
AS A registered user
I WANT the mirror to recognize my face when I approach
SO THAT I can access my personalized dashboard without manual input

ACCEPTANCE CRITERIA:
✅ Recognition within 2 seconds at 0.5–1.5m
✅ ≥95% confidence threshold
✅ Personalized dashboard loads on recognition
✅ OTP fallback on 3 failed attempts
✅ Unknown users shown "guest mode" or prompted to register
```

**Checklist – Implementation Tasks:**
- [ ] Set up OpenCV camera capture pipeline
- [ ] Implement face_recognition library encoding
- [ ] Create user database schema (SQLite)
- [ ] Build confidence threshold comparison logic
- [ ] Implement graceful fallback to OTP
- [ ] Write unit tests (≥80% coverage)
- [ ] Create face enrollment workflow
- [ ] Integration test with camera hardware

**Due Date:** December 11, 2024
**Assigned to:** [Developer 1], [Developer 2]
**Attachments:** `wireframes/login_flow.png`, `face_recognition_demo.ipynb`

---

## 5. Trello Labels System for AMMS

| Label Color | Category               | Examples                                |
|-------------|------------------------|-----------------------------------------|
| 🔴 Red      | High Priority          | US-001, US-004, US-009                  |
| 🟡 Yellow   | Medium Priority        | US-005, US-006, US-013                  |
| 🟢 Green    | Low Priority           | US-018, US-022, US-023                  |
| 🔵 Blue     | Sprint Number          | Sprint 1, Sprint 2, Sprint 3            |
| 🟣 Purple   | Feature Category       | AI/ML, Hardware, API Integration, UI    |
| ⚫ Black    | Blocker/Risk           | Hardware unavailable, API limits        |

---

## 6. Trello in Academic Context (Literature)

### 6.1 Trello Supporting Lifelong Learning

Research by Papastergiou et al. (2021) found that Visual project management tools like Trello significantly improve **task clarity** and **completion rates** in student-led software projects:
- Teams using Kanban boards (Trello) completed 23% more tasks on time
- Transparency of work in progress reduced missed handoffs by 37%
- Card-based requirements visible to all team members ensure shared understanding

### 6.2 Trello in Agile Development Education

Using Trello to Support Agile in Teacher Professional Development (Yilmaz, 2019):
> "The visual nature of Trello's Kanban board makes abstract Agile concepts concrete and navigable, particularly for teams new to Scrum methodology."

### 6.3 AMMS Team Trello Adoption Tips

1. **Update cards daily** during Daily Scrum
2. **Move cards** only when work state changes (don't skip columns)
3. **Add comments** for blockers or decisions — creates decision log
4. **Link wireframes and test results** as attachments to cards
5. **Use @mentions** to notify teammates of dependencies
6. **Sprint Retrospective:** Archive completed sprint board; start fresh for next

---

## 7. References

1. Papastergiou, M., et al. (2021). *Trello as a Tool for the Development of Lifelong Learning Skills of Senior Students.* Educational Technology & Society.
2. Yilmaz, Y. (2019). *Using Trello to Support Agile and Lean Learning with Scrum and Kanban in Teacher Professional Development.* Journal of Information Technology Education.
3. Atlassian (2024). *Trello Documentation and Guide.* https://trello.com/guide
4. Anderson, D.J. (2010). *Kanban: Successful Evolutionary Change for Your Technology Business.* Blue Hole Press.
5. Brechner, E. (2015). *Agile Project Management with Kanban.* Microsoft Press.

---
*Document prepared as part of AMMS Week 5 – Sprint Planning Tool Setup*
