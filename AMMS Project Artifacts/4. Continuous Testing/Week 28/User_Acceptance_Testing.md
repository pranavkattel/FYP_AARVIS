# User Acceptance Testing (UAT) – AMMS Smart Mirror
**Week 28 | Phase 4: Continuous Testing**
**Date Range:** 31 March – 4 April 2025**

---

## 1. UAT Purpose and Scope

User Acceptance Testing (UAT) validates the AMMS system from the **end-user's perspective** — ensuring the system meets real-world needs before final deployment. UAT cannot be replaced by automated tests because it evaluates subjective qualities like usability, satisfaction, and real-context appropriateness.

### 1.1 UAT Entry Criteria

- [x] All functional tests passed (Week 27)
- [x] No Severity-1 defects open
- [x] Hardware assembled and stable (Sprint 6)
- [x] System running on target hardware (Raspberry Pi 4)
- [x] 3 test users enrolled in system

---

## 2. UAT Participants

| Participant | Profile | Role in AMMS |
|-------------|---------|-------------|
| Ahmad (P1) | 23M, Engineering student, daily user | Primary user |
| Siti (P2) | 21F, Business student, occasional user | Secondary user |
| Razif (P3) | 35M, Lecturer, admin expertise | System admin |

---

## 3. UAT Test Scenarios

### Scenario 1: Morning Routine (Primary User)

**Task:** Simulate a typical weekday morning using AMMS for 10 minutes.

**Steps:**
1. Stand in front of mirror → observe face detection
2. Verify correct login and personalised greeting
3. Review dashboard (time, weather, calendar, news)
4. Ask AURA: "What's on my schedule today?"
5. Ask AURA: "What's the weather like?"
6. Ask AURA to send WhatsApp to contact
7. Ask AURA to read top emails

**Acceptance Criteria:**
- Login occurs without manual intervention ✅
- Greeting uses correct name ✅
- All dashboard widgets populated ✅
- Voice answers are accurate and concise ✅
- WhatsApp sent correctly ✅

**P1 Result:** All criteria met. Login in 1.4s. Ahmad rated experience 4/5.

---

### Scenario 2: Admin User Management

**Task:** Razif (admin) enrols a new user and then removes one.

**Steps:**
1. Access Admin Panel (via keyboard shortcut on mirror / browser at amms.local:5000/admin)
2. Add new user: "Farah" — capture 10 face samples
3. Verify Farah can log in
4. Delete user "Amir"
5. Verify Amir cannot log in

**P3 Result:** All steps completed. Registration took 2 minutes. Panel rated "easy to use" (4/5).

---

### Scenario 3: New User First Experience

**Task:** Siti uses AMMS for the first time (enrolled but never used independently).

**Observations:**
- Had to be shown the wake word ("AURA") — not intuitively discoverable
- Was confused by emotion icon at first ("Why does it show a face?")
- Successfully sent email after first explanation
- Found weather widget "immediately useful"

**Siti's Rating:** 3.5/5 — overall positive but wants better onboarding

---

## 4. UAT Questionnaire Results

**System Usability Scale (SUS) scoring (0–100):**

| SUS Item | P1 | P2 | P3 | Avg |
|----------|----|----|-----|-----|
| 1. I would use this frequently | 4 | 3 | 5 | 4.0 |
| 2. Unnecessary complexity | 2 | 3 | 2 | 2.3 |
| 3. Easy to use | 4 | 3 | 5 | 4.0 |
| 4. Needed technical help | 2 | 3 | 1 | 2.0 |
| 5. Well-integrated functions | 4 | 4 | 5 | 4.3 |
| 6. Too much inconsistency | 2 | 2 | 2 | 2.0 |
| 7. Most people learn quickly | 4 | 3 | 5 | 4.0 |
| 8. Cumbersome to use | 2 | 2 | 1 | 1.7 |
| 9. Felt confident using system | 4 | 3 | 5 | 4.0 |
| 10. Needed to learn a lot first | 2 | 3 | 2 | 2.3 |

**SUS Score Calculation:**
- Odd items (1,3,5,7,9): (sum − 5) × 2.5
- Even items (2,4,6,8,10): (25 − sum) × 2.5

| Participant | SUS Score | Grade |
|-------------|---------|-------|
| P1 (Ahmad) | 77.5 | C (Good) |
| P2 (Siti) | 62.5 | D (OK) |
| P3 (Razif) | 87.5 | B (Excellent) |
| **Average** | **75.8** | **C (Good)** |

> SUS score of 68 = industry acceptable. AMMS at 75.8 exceeds baseline. Target >80 for v2.

---

## 5. UAT Defects Found

| Defect | Reporter | Severity | Fix |
|--------|---------|---------|-----|
| Wake word not discovered by new user | Siti | Medium | Added "Say AURA to start" overlay on idle screen |
| Emotion icon unexplained | Siti | Low | Added tooltip/label under emotion icon |
| Admin panel accessible without HTTPS | Razif | Low | Noted for v2 (HTTPS cert) |
| Calendar showed events from yesterday | Ahmad | Medium | Fixed: timeMin uses current time, not midnight |

---

## 6. UAT Sign-Off

| Criteria | Result |
|---------|--------|
| All high-priority test scenarios passed | ✅ |
| No Severity-1 or unresolved Severity-2 defects | ✅ |
| SUS score ≥ 68 (industry baseline) | ✅ 75.8 |
| All 3 participant sign-offs obtained | ✅ |

**UAT Status: PASSED ✅**

---

## 7. References

1. Brooke, J. (1996). "SUS: A quick and dirty usability scale." In Jordan, Thomas, McClelland, Weerdmeester (Eds.), *Usability Evaluation in Industry.*
2. Nielsen, J. (1993). *Usability Engineering.* Academic Press.
3. Kaner, C. (1999). "Architectures of community for testing." *Star East Conference.*
