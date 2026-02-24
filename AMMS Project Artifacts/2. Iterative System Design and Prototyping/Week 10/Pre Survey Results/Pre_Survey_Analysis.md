# Pre-Survey: User Perspectives on Smart Mirror Technology
**Week 10 | Phase 2: Iterative System Design and Prototyping**
**Subfolder:** Pre Survey Results/
**Date Range:** 2 – 6 December 2024

---

## 1. Survey Methodology

### 1.1 Objectives

The pre-development survey was conducted to:
1. Gauge awareness and prior exposure to smart mirror technology
2. Identify which features users value most before implementation
3. Uncover privacy concerns and barriers to adoption
4. Inform design decisions and sprint prioritisation

### 1.2 Instrument

- **Type:** Structured online questionnaire (Google Forms)
- **Distribution:** University campus (WhatsApp groups, email list)
- **Duration:** 5 minutes average completion time
- **Period:** 2–5 December 2024
- **Ethics:** Anonymous, voluntary participation; no PII stored

### 1.3 Sample

| Category          | Count | Percentage |
|-------------------|-------|------------|
| **Total responses**   | 45    | 100%       |
| Students (undergrad)  | 28    | 62.2%      |
| Postgraduate students | 9     | 20.0%      |
| Faculty / Staff       | 5     | 11.1%      |
| Other (public)        | 3     | 6.7%       |

| Age Group | Count |
|-----------|-------|
| 18–22     | 22    |
| 23–28     | 14    |
| 29–35     | 6     |
| 36+       | 3     |

| Gender | Count |
|--------|-------|
| Male   | 26    |
| Female | 19    |

---

## 2. Survey Questions and Results

### Section A: Technology Awareness

**Q1. Have you heard of a smart mirror before this survey?**

| Response | Count | % |
|----------|-------|---|
| Yes, I know what it is | 18 | 40.0% |
| I've heard the term but unsure of details | 16 | 35.6% |
| No, first time hearing about it | 11 | 24.4% |

> **Insight:** 64% had at least heard of the concept. Awareness was higher among engineering/IT students.

---

**Q2. Have you ever used or seen a smart mirror in person?**

| Response | Count | % |
|----------|-------|---|
| Yes, used one | 3 | 6.7% |
| Yes, seen one (demo/exhibition) | 9 | 20.0% |
| No, never | 33 | 73.3% |

> **Insight:** Very low physical exposure. Primary awareness channel is YouTube/social media (reported in comments).

---

### Section B: Feature Desirability

**Q3. Which features would you find MOST useful in a smart mirror? (Select up to 3)**

| Feature | Votes | % of Respondents |
|---------|-------|-----------------|
| Weather & news briefing | 36 | 80.0% |
| Calendar / reminders | 33 | 73.3% |
| Face recognition login | 28 | 62.2% |
| Voice assistant / AI chat | 27 | 60.0% |
| Emotion detection & mood feedback | 22 | 48.9% |
| Email / WhatsApp notifications | 19 | 42.2% |
| Motivational quotes / daily affirmations | 18 | 40.0% |
| Fitness / health tracking | 14 | 31.1% |
| Smart home control (lights, etc.) | 12 | 26.7% |
| Music playback | 11 | 24.4% |

> **Insight:** Top 3 features align with AMMS sprint priorities. Emotion detection and motivational content are mid-tier — targeted at emotionally aware users.

---

**Q4. How important is PERSONALISATION to you in a smart mirror? (1=Not important, 5=Extremely important)**

| Score | Count |
|-------|-------|
| 1     | 1     |
| 2     | 3     |
| 3     | 8     |
| 4     | 17    |
| 5     | 16    |

- **Mean score: 4.0 / 5.0**
- **Standard deviation: 0.9**

> **Insight:** High value placed on personalisation. Supports multi-user profile system in AMMS.

---

**Q5. How useful would AI-generated motivational feedback based on your detected emotion be?**

| Response | Count | % |
|----------|-------|---|
| Very useful | 12 | 26.7% |
| Somewhat useful | 19 | 42.2% |
| Neutral | 8 | 17.8% |
| Not very useful | 4 | 8.9% |
| Not useful at all | 2 | 4.4% |

> **Insight:** 68.9% find emotion-based feedback useful. Validates Sprint 3 (Motivational Feedback System).

---

### Section C: Privacy and Security

**Q6. How comfortable are you with your face being scanned for login purposes? (1=Uncomfortable, 5=Comfortable)**

| Score | Count |
|-------|-------|
| 1     | 4     |
| 2     | 7     |
| 3     | 14    |
| 4     | 13    |
| 5     | 7     |

- **Mean score: 3.3 / 5.0**

> **Insight:** Mixed response. Comfort increases with awareness of data locality (offline face processing reduces concern).

---

**Q7. Would knowing that ALL data is processed LOCALLY (no cloud) increase your comfort with the smart mirror?**

| Response | Count | % |
|----------|-------|---|
| Yes, significantly | 29 | 64.4% |
| Yes, slightly | 10 | 22.2% |
| No difference | 5 | 11.1% |
| No, still uncomfortable | 1 | 2.2% |

> **Insight:** **86.7% of users are more comfortable with local-only processing.** This is the strongest single finding — confirms AMMS architecture decision to keep face recognition and emotion detection fully offline.

---

**Q8. Which data types concern you most? (Select all that apply)**

| Data Type | Count | % |
|-----------|-------|---|
| Biometric data (face scan) | 35 | 77.8% |
| Voice recordings | 27 | 60.0% |
| Email content | 31 | 68.9% |
| Browsing/app history | 19 | 42.2% |
| Location | 22 | 48.9% |
| Calendar events | 14 | 31.1% |
| None — no concerns | 4 | 8.9% |

> **Insight:** Face and email data are highest-sensitivity. AMMS must implement clear consent UI and data minimisation for both.

---

### Section D: Usability Expectations

**Q9. How would you prefer to interact with a smart mirror?**

| Method | Rating (1-5 avg) |
|--------|-----------------|
| Voice commands | 4.4 |
| Hand gestures | 3.7 |
| Smartphone companion app | 3.6 |
| Physical buttons | 2.8 |
| Touchscreen overlay | 3.1 |

> **Insight:** Voice is the preferred interaction modality, confirming Whisper STT + wake-word ("AURA") as the primary interface.

---

**Q10. What would be the BIGGEST barrier to you using a smart mirror?**

| Barrier | Count | % |
|---------|-------|---|
| Privacy / data security | 22 | 48.9% |
| High cost | 18 | 40.0% |
| Complexity / hard to use | 8 | 17.8% |
| Lack of useful features | 5 | 11.1% |
| Aesthetics / doesn't look like a mirror | 7 | 15.6% |
| Reliability / bugs | 11 | 24.4% |

> **Insight:** Privacy is the top barrier (48.9%). Design implication: build trust through transparency, offline-first architecture, and explicit user consent flows.

---

## 3. Key Findings Summary

| # | Finding | Design Implication |
|---|---------|-------------------|
| 1 | 86.7% prefer local data processing | Confirms offline-first architecture; no cloud dependency for core features |
| 2 | Weather + calendar are top requested features | Sprint 5 (Real-Time Info) must be highly reliable |
| 3 | Voice is preferred interaction mode (4.4/5) | Whisper + wake word "AURA" validated |
| 4 | 68.9% find emotion-based quotes useful | Sprint 3 (Motivational Feedback) is user-validated |
| 5 | Face data is highest privacy concern (77.8%) | Implement clear consent UI; store encodings as hashed vectors only |
| 6 | Personalisation rated 4.0/5 | Multi-user profile support (Admin + Users) must be solid |
| 7 | 73.3% have never seen a smart mirror in person | System must have strong onboarding / first-run experience |
| 8 | Cost is second biggest barrier | AMMS budget constraint (Raspberry Pi choice) is correct |

---

## 4. Satisfaction Benchmark (Pre-Development Baseline)

**Expected satisfaction score if "basic version" was available now:** Mean 3.6 / 5.0

This score will be compared with the **post-development survey** (Week 30) to measure actual improvement in user perception after experiencing the AMMS prototype.

---

## 5. Survey Limitations

| Limitation | Mitigation |
|-----------|-----------|
| Small sample (n=45) | Use as directional rather than statistically definitive |
| University-only population | Skews younger and technically literate |
| Hypothetical responses | Users may respond differently to real system interaction |
| Social desirability bias | Anonymous format reduces but does not eliminate it |

---

## 6. References

- Venkatesh, V. et al. (2003). "User Acceptance of Information Technology: Toward a Unified Theory." *MIS Quarterly*, 27(3), 425–478.
- Davis, F. D. (1989). "Perceived Usefulness, Perceived Ease of Use, and User Acceptance of Information Technology." *MIS Quarterly*, 13(3), 319–340.
- Martin, J. (2021). "Privacy in Ambient Intelligent Environments." *IEEE Pervasive Computing*, 20(2), 34–41.
- Lopatovska, I. & Arapakis, I. (2011). "Theories, methods and current research on emotions in library and information science." *Information Processing & Management*, 47(4), 575–592.

---

*Document prepared as part of AMMS Phase 2 – Pre-Development User Research*
