# AMMS UI Wireframe Descriptions
**Week 9 | Phase 2: Iterative System Design and Prototyping**
**Subfolder:** Wireframe/
**Date Range:** 29 November – 1 December 2024

---

## 1. Design Principles

The AMMS interface follows **ambient display** design principles:
- **Glanceability:** All critical information must be readable within 2 seconds
- **High contrast:** White text on dark/black background for mirror overlay readability
- **Minimal typography:** Maximum 2 font families; minimum 24pt for primary content
- **No touch required:** Interface designed primarily for voice + face interaction
- **Grid layout:** Consistent 12-column CSS grid for predictable widget placement

**Colour Palette:**
| Element         | Colour           | Hex       |
|-----------------|------------------|-----------|
| Background      | Deep Black       | #000000   |
| Primary Text    | Pure White       | #FFFFFF   |
| Secondary Text  | Light Gray       | #CCCCCC   |
| Accent/Highlight| Cyan/Teal        | #00BCD4   |
| Success         | Green            | #4CAF50   |
| Warning/Alert   | Amber            | #FFC107   |
| Emotion: Happy  | Yellow           | #FFD700   |
| Emotion: Sad    | Blue             | #2196F3   |
| Emotion: Angry  | Red              | #F44336   |

---

## 2. Screen 1: Idle / Guest Screen

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                                                             │
│                       [AMMS Logo / AURA]                                   │
│                                                                             │
│                    ┌─────────────────────┐                                 │
│                    │                     │                                 │
│                    │      07:42 AM       │  ← Large digital clock          │
│                    │   Monday, Nov 18    │  ← Date                         │
│                    │                     │                                 │
│                    └─────────────────────┘                                 │
│                                                                             │
│                                                                             │
│               ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐                         │
│                 Stand in front of mirror to login                           │
│               └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘                         │
│                                                                             │
│                          [Scanning animation]                               │
│                                                                             │
│                    ┌─────────────────────┐                                 │
│                    │   🌤 26°C  KL       │  ← Minimal weather              │
│                    └─────────────────────┘                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Notes:
- Background: Pure black
- No news/calendar shown for privacy until user logged in
- Gentle pulsing animation around mirror perimeter to indicate "ready"
- Weather widget only: no user-specific data
```

---

## 3. Screen 2: User Dashboard (Post-Login)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌──────────────────────────┐        ┌──────────────────────────────────┐  │
│  │  07:42 AM                │        │  📍 Kuala Lumpur                 │  │
│  │  Monday, 18 Nov 2024     │        │  🌤 26°C | Feels like 28°C      │  │
│  │                          │        │  Humidity: 72% | Wind: 12 km/h  │  │
│  │  Good morning, Ahmad!  ✨│        │  3-Day: Mon ☀ | Tue 🌧 | Wed ⛅ │  │
│  └──────────────────────────┘        └──────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  😊 You look energised today! "The secret of getting ahead is       │  │
│  │   getting started." — Mark Twain                                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────┐         ┌──────────────────────────────────┐  │
│  │  📅 TODAY'S SCHEDULE    │         │  📰 TOP NEWS                    │  │
│  │  ─────────────────────  │         │  ─────────────────────────────  │  │
│  │  09:00 Team Meeting     │         │  • KLSE up 1.2% on tech stocks  │  │
│  │        (Zoom)           │         │  • New AI model released by Meta │  │
│  │  13:00 Lunch with Ali   │         │  • Malaysia CPG GDP Q3 beat est  │  │
│  │  15:30 Project Review   │         │  • SpaceX Starship 5th test fly  │  │
│  │  18:00 Gym              │         │  • Local: Hari Raya prep begins  │  │
│  └─────────────────────────┘         └──────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  🔔 NOTIFICATIONS                                                   │  │
│  │  📧 3 unread emails (1 marked urgent) | 📱 2 new WhatsApp messages  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  🎙️ Say "AURA" to interact  |  Ahmad  [●] Active                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Notes:
- Top-left: Time, date, greeting + emotion icon
- Top-right: Weather widget with 3-day forecast
- Center banner: Emotion-adaptive quote with emotion emoji
- Bottom-left: Today's Google Calendar events (5 max)
- Bottom-right: Top 5 news headlines
- Bottom banner: Notification summary
- Status bar: Wake word prompt + user name + active indicator
```

---

## 4. Screen 3: Voice Interaction Mode (Active)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌──────────────────────────┐        ┌──────────────────────────────────┐  │
│  │  07:42 AM                │        │  🌤 26°C                        │  │
│  │  Good morning, Ahmad!    │        └──────────────────────────────────┘  │
│  └──────────────────────────┘                                              │
│                                                                             │
│           ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐              │
│                                                                             │
│           │         ┌───────────────────────────┐         │              │
│                     │         AURA 🎙️           │                         │
│           │         │   Listening...            │         │              │
│                     │   ░░░░░░░░░░░░░           │                         │
│           │         │   [audio waveform]        │         │              │
│                     └───────────────────────────┘                         │
│           │                                                 │              │
│                User: "What's on my calendar today?"                        │
│           │                                                 │              │
│                AURA: "You have 4 events today. First,                      │
│           │           Team Meeting at 9 AM on Zoom..."     │              │
│                                                                             │
│           └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘              │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  📅 09:00 Team Meeting (Zoom)  |  13:00 Lunch  |  +2 more            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  🎙️ Listening... Say a command or ask anything  [■ Stop]              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Notes:
- Dashboard fades to dark when voice mode activates
- Centre: AURA AI avatar/waveform animation
- Conversation history shows last 2 exchanges
- Dashboard context widgets persist in background
- Bottom: Live status indicator
```

---

## 5. Screen 4: Admin Panel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AURA – Admin Panel                              🔐 Admin: Razif | [Logout] │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  ┌────────────────┐  ┌──────────────────────────────────────────────────┐  │
│  │  NAVIGATION    │  │  USER MANAGEMENT                                │  │
│  │  ──────────── │  │  ──────────────────────────────────────────────  │  │
│  │  👥 Users      │  │  [+ Add New User]                               │  │
│  │  ⚙️ Settings   │  │                                                  │  │
│  │  📊 Logs       │  │  Name          Status   Last Login   Actions   │  │
│  │  🔔 Alerts     │  │  ─────────────────────────────────────────────  │  │
│  │                │  │  Ahmad Razifi  Active   Today 7:42   [Edit][Del]│  │
│  │                │  │  Siti Nabilah  Active   Yesterday    [Edit][Del]│  │
│  │                │  │  Amir Hassan   Inactive  3 days ago  [Edit][Del]│  │
│  │                │  │                                                  │  │
│  │                │  │  Total users: 3 | Active: 2 | Max: 10           │  │
│  └────────────────┘  └──────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  SYSTEM STATUS                                                      │  │
│  │  Camera: ✅ Active  |  Mic: ✅ Active  |  LLM: ✅ Running           │  │
│  │  Storage: 67% used (12GB/18GB)  |  Uptime: 14 days 3h              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Notes:
- Web-based admin panel (accessible on local network via browser)
- Also accessible directly on mirror via hidden touch/keyboard shortcut
- User enrollment requires: name, face capture (10 samples), API permissions
```

---
*Document prepared as part of AMMS Week 9 – Technical Diagrams (Wireframes)*
