# Sprint 4 Review – Messaging Integration & Voice Commands
**Sprint 4 | Week 21 | Phase 3: Sprint-Based Development**
**Sprint Review Date:** 14 February 2025

---

## 1. Sprint Goals vs Outcomes

| Goal | Status |
|------|--------|
| Send WhatsApp via voice command | ✅ Complete (Twilio sandbox) |
| Read top 5 Gmail subjects aloud | ✅ Complete |
| Compose and send email via voice dictation | ✅ Complete |
| Notification count on dashboard | ✅ Complete |
| Fuzzy contact name resolution | ✅ Complete (using `difflib`) |
| Message confirmation flow | ✅ Complete |

---

## 2. Sprint 4 Test Results

| Test ID | Scenario | Expected | Actual | Pass? |
|---------|---------|---------|--------|-------|
| MSG-TC-001 | "Send WhatsApp to Ali saying hi" | Message sent | ✅ Sent | ✅ |
| MSG-TC-002 | Contact not found ("John") | "No contact found" | Spoken correctly | ✅ |
| MSG-TC-003 | Read emails (5 unread) | 5 subjects read aloud | 5 read | ✅ |
| MSG-TC-004 | Compose email via dictation | Draft created | Created + sent | ✅ |
| MSG-TC-005 | Confirm → "No" → cancel | Message cancelled | Cancelled | ✅ |
| MSG-TC-006 | Ambiguous recipient: 2 contacts named "Ali" | List both options | Listed | ✅ |

---

## 3. Fuzzy Contact Matching

```python
import difflib

def fuzzy_find_contact(name: str, contacts: list[dict], threshold=0.6) -> list[dict]:
    matches = []
    for c in contacts:
        ratio = difflib.SequenceMatcher(None, name.lower(), c['Name'].lower()).ratio()
        if ratio >= threshold:
            matches.append((ratio, c))
    return [c for _, c in sorted(matches, reverse=True)]
```

---

## 4. Gmail Dashboard Widget Data

```python
def get_dashboard_email_summary():
    service = get_gmail_service()
    unread = service.users().messages().list(
        userId='me', q='is:unread', maxResults=1
    ).execute()
    total_unread = unread.get('resultSizeEstimate', 0)

    # Check for urgent (starred + unread)
    urgent = service.users().messages().list(
        userId='me', q='is:unread is:starred', maxResults=1
    ).execute()
    urgent_count = urgent.get('resultSizeEstimate', 0)

    return {
        'unread': total_unread,
        'urgent': urgent_count
    }
# → Dashboard shows: "📧 7 unread (2 urgent)"
```

---

## 5. Sprint Retrospective

**What went well:**
- Twilio WhatsApp sandbox integration was straightforward
- Gmail OAuth flow is reusable for Calendar (already integrated in Sprint 5)
- Voice-confirmation two-step prevents accidental sends

**Challenges:**
- Gmail API rate limits: 250 quota units/second; heavy use could trigger limits
- Twilio sandbox requires recipient to opt-in (production limitation)
- Google OAuth token occasionally expires mid-session — fixed with auto-refresh

**Backlog items deferred:**
- WhatsApp message reading (no official incoming message API for non-business accounts)
- Read receipts (not available via API without full META Business approval)

---

## 6. References

1. Twilio Inc. (2024). *Twilio WhatsApp API Docs.* twilio.com/docs.
2. Google Inc. (2024). *Gmail API Python Quickstart.* developers.google.com.
3. Navarro, M. (2022). "Building voice-first applications: lessons learned." *O'Reilly Media.*
