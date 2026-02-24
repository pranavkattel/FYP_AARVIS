# SDLC Methodology Comparison – AMMS Project Selection
**Week 2 | Phase 1: Sprint Planning and Requirement Prioritization**
**Subfolder:** Methodology/Considered methodology/
**Date Range:** 4 November – 6 November 2024

---

## 1. Introduction

Selecting the appropriate Software Development Life Cycle (SDLC) methodology is a critical project decision that impacts timeline, quality, flexibility, and team collaboration. This document evaluates four methodologies considered for the AMMS project:

1. **Waterfall**
2. **V-Model**
3. **Rapid Application Development (RAD)**
4. **Agile (Scrum)**

---

## 2. Methodology Overviews

### 2.1 Waterfall Methodology

The Waterfall model is a sequential, linear software development process where each phase must be completed before the next begins.

**Phases:**
```
Requirements → System Design → Implementation → Testing → Deployment → Maintenance
```

**Characteristics:**
- Rigid, well-documented phases
- Works well when requirements are stable and well-understood from the start
- Limited flexibility for change once a phase is complete
- Heavy upfront documentation

**Suitability for AMMS:**
| Factor                    | Assessment |
|---------------------------|------------|
| Requirements clarity       | ❌ Requirements evolving |
| Change frequency           | ❌ Expected high changes |
| Team size                  | ⚠️ Small team (suited) |
| Documentation need         | ✅ Academic project |
| Iteration need             | ❌ Multiple feedback loops needed |

**Verdict for AMMS:** ❌ **Not Recommended**
> AMMS requires user feedback loops, iterative AI model refinement, and sprint-based feature delivery. Waterfall's rigidity would prevent adaptation.

---

### 2.2 V-Model (Verification and Validation Model)

The V-Model extends Waterfall by pairing each development phase with a corresponding testing phase, creating a V-shaped process.

**Structure:**
```
Requirements ↔ Acceptance Testing
System Design ↔ System Testing
Architecture Design ↔ Integration Testing
Module Design ↔ Unit Testing
         ↓
      Coding
```

**Characteristics:**
- Each development phase has an explicit testing counterpart
- High emphasis on verification and validation
- Still sequential (not iterative)
- Better quality assurance than pure Waterfall

**Suitability for AMMS:**
| Factor                       | Assessment |
|------------------------------|------------|
| Testing emphasis              | ✅ Strong testing alignment |
| Iterative development         | ❌ Still sequential |
| AI/ML component uncertainty   | ❌ No room for model iteration |
| Academic rigor alignment      | ✅ Good documentation |
| Early defect detection        | ✅ Strong |

**Verdict for AMMS:** ⚠️ **Partial Consideration**
> Better test coverage than Waterfall, but still too rigid for AI component development where models require iterative tuning.

---

### 2.3 Rapid Application Development (RAD)

RAD emphasizes fast prototyping and user feedback over extensive planning. It uses iterative development cycles where prototype versions are rapidly built and refined.

**Phases:**
```
Requirements Planning → User Design → Construction → Cutover
        ↑__________________________________|
                  (iterative)
```

**Characteristics:**
- Fast development through component reuse
- Heavy user involvement in design phases
- Reduced planning overhead
- Best for smaller teams with experienced developers
- Time-boxing of development cycles

**Suitability for AMMS:**
| Factor                       | Assessment |
|------------------------------|------------|
| Speed of delivery             | ✅ Good for prototyping |
| User involvement              | ✅ Required for face recognition testing |
| Formal process structure      | ❌ Limited for academic documentation |
| Scalability                   | ⚠️ Works for small team |
| Sprint-based delivery         | ✅ Compatible concept |

**Verdict for AMMS:** ⚠️ **Considered but not fully adopted**
> RAD's fast prototyping is valuable, but its limited formal structure makes academic documentation challenging.

---

### 2.4 Agile (Scrum Framework) — **SELECTED**

Agile with Scrum is an iterative, incremental approach that delivers working software in short cycles (sprints), with continuous planning, feedback, and adaptation.

**Scrum Framework:**
```
Product Backlog → Sprint Planning → Sprint (1-4 weeks) → Sprint Review → Sprint Retrospective
                      ↑__________________________________________________|
                                    (continuous iteration)
```

**Scrum Roles:**
| Role            | Responsibility                                    |
|-----------------|---------------------------------------------------|
| Product Owner   | Maintains and prioritizes product backlog         |
| Scrum Master    | Facilitates process; removes impediments          |
| Development Team| Builds increment; self-organizes                  |

**Scrum Events:**
| Event                | Frequency   | Duration     | Purpose                               |
|----------------------|-------------|--------------|---------------------------------------|
| Sprint Planning      | Each sprint | 4 hours max  | Plan sprint work from backlog         |
| Daily Scrum          | Daily       | 15 minutes   | Sync progress; identify blockers      |
| Sprint Review        | End of sprint| 2-4 hours   | Demo increment to stakeholders        |
| Sprint Retrospective | End of sprint| 1.5-3 hours | Reflect on process; improve           |

**Suitability for AMMS:**
| Factor                       | Assessment |
|------------------------------|------------|
| Iterative AI/ML development   | ✅ Perfect fit |
| Frequent user feedback        | ✅ Regular sprint reviews |
| Evolving requirements         | ✅ Backlog can adapt |
| Team collaboration            | ✅ Daily standups |
| Deliverable tracking          | ✅ Sprint increments |
| Academic documentation        | ✅ Via sprint artifacts |
| Trello integration            | ✅ Kanban-style board |

**Verdict for AMMS:** ✅ **SELECTED METHODOLOGY**

---

## 3. Comparative Analysis Matrix

| Criterion               | Waterfall | V-Model | RAD   | Agile/Scrum |
|-------------------------|-----------|---------|-------|-------------|
| Flexibility to change   | Low       | Low     | High  | Very High   |
| Customer involvement    | Low       | Low     | High  | Very High   |
| Documentation           | High      | High    | Low   | Medium      |
| Risk management         | Low       | Medium  | Medium| High        |
| Testing integration     | Late      | Early   | Continuous | Continuous |
| Speed of delivery       | Slow      | Slow    | Fast  | Fast        |
| Suitability for AI/ML   | Poor      | Poor    | Fair  | Excellent   |
| Academic reporting      | Good      | Good    | Fair  | Good        |
| Team size fit           | Large     | Large   | Small | Any         |

---

## 4. Why Agile/Scrum for AMMS

### 4.1 Key Justifications

**1. AI Model Iterative Development**
Face recognition and emotion detection models require multiple training, testing, and refinement cycles. Agile's sprint structure naturally accommodates this.

**2. Incremental System Building**
AMMS is built from independent modules (face recognition, emotion detection, briefing system, voice interaction). Agile allows each module to be developed in its own sprint without blocking others.

**3. Early Risk Identification**
Hardware integration risks (Raspberry Pi camera, microphone latency) can be identified and mitigated in early sprints.

**4. Stakeholder Feedback**
Sprint reviews provide regular opportunities for supervisor and user feedback, improving both product quality and academic alignment.

**5. Trello as Agile Tool**
The team adopted Trello as their digital Kanban/Scrum board, aligning with Agile's visual workflow management philosophy.

---

## 5. Agile vs. Waterfall vs. V-Model: Literature Comparison

From *"WATERFALL Vs V-MODEL Vs AGILE: A Comparative Study on SDLC"* (Kumar & Bhatia, 2012):

> "Agile methodologies show 28% higher on-time delivery rates compared to Waterfall in projects with evolving requirements. V-Model provides superior defect detection but lacks the adaptability needed for innovative product development."

From *"Rapid Application Development"* research:

> "RAD reduces time-to-prototype by 40% but sacrifices long-term maintainability and formal documentation necessary for academic submissions."

---

## 6. AMMS Agile Implementation Plan

### 6.1 Sprint Structure for AMMS
- **Sprint Duration:** 2 weeks (aligned with academic calendar)
- **Total Sprints:** 6 major development sprints
- **Sprint Planning:** First day of each sprint
- **Sprint Review/Retro:** Last day of each sprint
- **Tools:** Trello (backlog + sprint board), GitHub (version control)

### 6.2 Definition of Done (DoD)
A task is considered complete when:
- [ ] Code is written and committed to repository
- [ ] Unit tests pass
- [ ] Feature demonstrated in sprint review
- [ ] Documentation updated
- [ ] Code reviewed by peer

---

## 7. References

1. Kumar, G., & Bhatia, P.K. (2012). *WATERFALL vs V-MODEL vs AGILE: A Comparative Study on SDLC.* International Journal of Information Technology and Knowledge Management.
2. Martin, J. (1991). *Rapid Application Development.* Macmillan Publishing.
3. Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide.* Scrum.org. Retrieved from https://scrumguides.org/
4. Forsberg, K., & Mooz, H. (1991). *The Relationship of Systems Engineering to the Project Cycle.* NCOSE.
5. Royce, W.W. (1970). *Managing the Development of Large Software Systems.* IEEE WESCON.
6. Beck, K., et al. (2001). *Manifesto for Agile Software Development.* https://agilemanifesto.org/

---
*Document prepared as part of AMMS Week 2 – Methodology Selection*
