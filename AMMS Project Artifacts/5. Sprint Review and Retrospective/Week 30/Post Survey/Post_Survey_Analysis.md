# Post-Development Survey – AMMS User Satisfaction Study
**Week 30 | Phase 5: Sprint Review and Retrospective**
**Subfolder:** Post Survey/
**Date Range:** 14 – 18 April 2025**

---

## 1. Survey Overview

The post-development survey follows the same format as the pre-development survey (Week 10) to measure how user perceptions **changed after experiencing the AMMS prototype**.

| Attribute | Pre-Survey (Week 10) | Post-Survey (Week 30) |
|-----------|---------------------|----------------------|
| Period | Dec 2–5, 2024 | Apr 14–17, 2025 |
| Type | Hypothetical preferences | Actual experience |
| Sample | 45 general respondents | 12 AMMS trial users |
| Duration | Online questionnaire | Post-trial + online |

---

## 2. Satisfaction Change: Pre vs Post

### Q: Overall interest / satisfaction with smart mirror (1–5)

| Group | Pre-Survey Mean | Post-Survey Mean | Change |
|-------|----------------|-----------------|--------|
| All respondents (pre) / trial users (post) | 3.6 | **4.3** | **+0.7 ↑** |

> Users who actually used AMMS rated it significantly higher than hypothetical expectations.

---

## 3. Feature Satisfaction Ratings (Post-Survey Only)

| Feature | Satisfaction (1-5) | Notes |
|---------|-------------------|-------|
| Face recognition login | 4.6 | Reliable; fast |
| Emotion detection | 4.1 | "Surprisingly accurate" |
| AURA voice responses | 4.3 | Natural, context-aware |
| Weather widget | 4.8 | Instantly useful |
| Calendar display | 4.7 | Replaced phone check |
| News headlines | 3.9 | Wants filtering option |
| Email / WhatsApp voice | 4.0 | Useful; confirmation step well-received |
| Overall system | **4.3** | Exceeds expectations |

---

## 4. Pre-Survey vs Post-Survey: Key Comparisons

### Q: Would you use a smart mirror daily if available?

| Response | Pre (n=45) | Post (n=12) |
|----------|-----------|------------|
| Definitely yes | 13.3% | **58.3%** |
| Probably yes | 26.7% | 25.0% |
| Maybe | 35.6% | 16.7% |
| Probably not | 17.8% | 0% |
| Definitely not | 6.7% | 0% |

**Conclusion:** Daily use intent grew from 40% → **83.3%** after trial.

---

### Q: Privacy comfort with face recognition (1=Uncomfortable, 5=Comfortable)

| | Pre | Post |
|--|-----|------|
| Mean | 3.3 | **4.1** |

> Comfort with face data increased significantly after users experienced that data stays local.

---

### Q: Voice is preferred interaction mode?

| | Pre (rated 4.4/5) | Post |
|-|--------------------|------|
| Voice preference | 4.4 | **4.7** |

> Real use reinforced voice as the preferred mode.

---

## 5. Net Promoter Score (NPS)

Post-trial users were asked: "On a scale of 0–10, how likely are you to recommend AMMS to a friend?"

| Score | Count | Category |
|-------|-------|---------|
| 9–10 | 5 | Promoters |
| 7–8 | 5 | Passives |
| 0–6 | 2 | Detractors |

$$\text{NPS} = \frac{\text{Promoters} - \text{Detractors}}{n} \times 100 = \frac{5-2}{12} \times 100 = +25$$

> NPS of +25 is **"Good"** (0–30 range). Industry benchmark for consumer IoT: +20. AMMS exceeds it.

---

## 6. Open-Ended Feedback Themes

| Theme | Count | Representative Quote |
|-------|-------|---------------------|
| Accuracy of emotion detection | 6 | "It knew I was tired before I realised it" |
| Privacy reassurance | 5 | "Knowing it's 100% offline changed how I felt about it" |
| Natural voice interaction | 7 | "Talking to AURA felt less robotic than Siri" |
| Display clarity | 4 | "Information was easy to read even from 1.5m away" |
| Performance (LLM speed) | 3 | "Sometimes waits 5s for a reply — worth it though" |

---

## 7. Improvement Recommendations from Users

1. **Onboarding screen** — Show wake word prompt on idle screen *(Implemented)*
2. **Faster LLM** — Quantise further or cache repeated context patterns
3. **News category filter** — Add preference settings per user
4. **Reminders** — Voice-set timer/reminder ("AURA, remind me in 10 minutes")
5. **Sleep mode** — Auto-dim after 22:00

---

## 8. References

1. Reichheld, F.F. (2003). "The One Number You Need to Grow." *Harvard Business Review.*
2. Davis, F.D. (1989). "Perceived Usefulness, Perceived Ease of Use." *MIS Quarterly*, 13(3).
3. Venkatesh, V. et al. (2003). "User Acceptance of Information Technology." *MIS Quarterly*, 27(3).
