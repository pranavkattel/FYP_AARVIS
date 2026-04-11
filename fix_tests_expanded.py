import os

content = """# 6 Testing

## 6.1 Test Plan

### 6.1.1 Project Overview
The testing phase for the AARVIS smart mirror evaluates the core integrations: Google OAuth, PyTorch-based Facial Recognition, WebSocket Voice Assistant, and Google Workspace APIs (Calendar & Gmail).

The test cases focus on functional user journeys, intelligent voice interactions, system-level integrations, and robust error handling.

### 6.1.2 Authentication & Device Pairing
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC01 | Google OAuth Login | User successfully authenticates via Google consent screen and session is created. | Planned |
| TC02 | Cross-Device QR Pairing Initialization | Scanning the QR on mobile correctly opens the mobile auth flow. | Planned |
| TC03 | Cross-Device QR Expiry | Attempting to use an expired QR code presents a `Token Expired` error. | Planned |
| TC04 | Mobile-to-PC Auto-Redirect | PC mirror UI automatically updates to the face setup/dashboard once the mobile flow completes. | Planned |
| TC05 | PC Fallback Trigger via Mobile | Tapping `Trigger on PC` from the mobile UI forces the mirror to continue via the local monitor. | Planned |
| TC06 | Unauthorized Dashboard Access | Attempting to access the dashboard `/` without an active session redirects to `/login`. | Planned |
| TC07 | User Logout | Triggering logout clears session cookies and correctly returns the UI to the login screen. | Planned |

### 6.1.3 Facial Recognition (PyTorch MobileNetV2)
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC08 | Multi-Face Handling | If multiple faces are in frame, the system dynamically locks onto the largest/closest face. | Planned |
| TC09 | Face Liveness & Motion Checks | System successfully tracks user motion (look left, right, up, down) sequentially during enrollment. | Planned |
| TC10 | Face Registration & Embedding | System successfully extracts 512-D embeddings from captured frames and saves to DB. | Planned |
| TC11 | Distance Verification Reject | System rejects enrollment captures if the user is too far away or face bounding box is too small. | Planned |
| TC12 | Lighting & Environment Tolerance | Model successfully recognizes faces in both well-lit and dim environments. | Planned |
| TC13 | Face Login (Authorized) | Registered user is recognized (cosine similarity > 0.40) and logged into the dashboard. | Planned |
| TC14 | Face Login (Unauthorized) | Unregistered face is rejected and access is denied. | Planned |
| TC15 | Edge Cases (No Face) | System handles empty frames without crashing, maintaining a scanning loop. | Planned |
| TC16 | Edge Cases (Occlusion) | System gracefully rejects logins where the face is heavily occluded (e.g., masks, hands covering face). | Planned |
| TC17 | Face Presence Cache | Once verified, the dashboard caches the presence temporarily to avoid constant re-verification spam. | Planned |

### 6.1.4 Smart Dashboard & GUI
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC18 | Widget Initialization | Weather, News, and Clock widgets load immediately with data related to the logged-in user. | Planned |
| TC19 | Time-based Greeting | UI displays `Good Morning`, `Good Afternoon`, or `Good Evening` matching the local clock. | Planned |
| TC20 | Empty Calendar State | UI elegantly handles and displays a `Free schedule` message if no events exist today. | Planned |
| TC21 | Multi-line News Truncation | Excessively long news headlines are truncated via CSS to prevent UI layout breakage. | Planned |
| TC22 | Periodic Background Refresh | Widgets auto-refresh in the background at set intervals without a full browser page reload. | Planned |
| TC23 | Morning Briefing Generation | LLM synthesizes current time, weather, news, and calendar into a concise, personalized welcome message. | Planned |

### 6.1.5 Voice Assistant & Conversational AI
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC24 | UI State Synchronization | UI correctly cycles between `Listening...`, `Thinking...`, and `Speaking...` matching the WebSocket state. | Planned |
| TC25 | STT Transcription Accuracy | Spoken audio is correctly transcribed with punctuation via the integrated Whisper pipeline. | Planned |
| TC26 | TTS Playback Queue | AI responses are synthesized and played back without overlapping audio chunks. | Planned |
| TC27 | Unintelligible Speech Handling | Assistant gracefully responds (e.g., `I didn't catch that`) when background noise or silence is sent. | Planned |
| TC28 | Date & Time Inquiry | User asks `What time is it?` and receives an accurate, formatted voice response. | Planned |
| TC29 | General Knowledge Inquiry | User asks a normal question (e.g., `What is the capital of France?`) and receives an accurate voice response. | Planned |
| TC30 | Weather Inquiry | User asks about current weather; assistant triggers weather API tool and speaks the result. | Planned |
| TC31 | Contextual Reasoning (Clothing) | User asks `What should I wear today?`; assistant checks weather and suggests appropriate clothing logically. | Planned |
| TC32 | Conversational Memory | The assistant correctly answers follow-up questions referencing pronouns (e.g., `How about tomorrow?`). | Planned |

### 6.1.6 Intelligent Google Services (Calendar & Gmail)
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC33 | Read Today's Schedule | Asking `What's my schedule today?` fetches and reads today's Google Calendar events accurately. | Planned |
| TC34 | Read Tomorrow's Schedule | Asking `What do I have tomorrow?` correctly shifts the datetime query and fetches the future schedule. | Planned |
| TC35 | Create Calendar Event | Asking to `Schedule a meeting at 3 PM` creates the event using a normalized 24-hour time format. | Planned |
| TC36 | Prevent Invalid Event Creation | Attempting to schedule an event in the past throws a logical warning to the user rather than processing blindly. | Planned |
| TC37 | Update Calendar Event | Asking to `Move my 3 PM meeting to 4 PM` successfully updates the existing event time. | Planned |
| TC38 | Delete/Cancel Calendar Event | Asking to `Cancel my 4 PM meeting` removes it from Google Calendar after confirmation. | Planned |
| TC39 | Check New Emails | Asking `Do I have any new emails?` fetches the list of unread emails from the connected Gmail account. | Planned |
| TC40 | Summarize Emails | Asking `Summarize my recent emails` provides a concise voice summary of the latest messages. | Planned |
| TC41 | Query Emails by Sender | Asking `Did I get an email from John?` filters unread emails by the sender's alias. | Planned |
| TC42 | Draft & Send Email via Contacts | Asking `Send an email to John about the project` resolves 'John' using `contacts.csv`, drafts content, and sends via Gmail. | Planned |
| TC43 | Draft Email for Unknown Contact | Asking to send an email to a name not in `contacts.csv` prompts the AI to explicitly ask the user for the email address. | Planned |

### 6.1.7 System Resiliency & Error Handling
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC44 | OAuth Token Expiry | The system intelligently handles expired Google Access tokens under the hood by swapping the Refresh token. | Planned |
| TC45 | External API Outage Fallbacks | If a third-party API (e.g., Weather API) is down or times out, the mirror UI remains stable with fallback text. | Planned |

## 6.2 Testing Summary
This expanded test plan now encompasses 45 explicit test cases validating the critical pathways of the AARVIS smart mirror. By focusing on detailed integration steps, edge cases, intelligent voice logic, and complete Google Workspace coverage, it ensures robust hardware-to-software execution behavior.
"""

file_path = r'd:\langgraph\final fixed fyp\docs\test_cases.md'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated test cases successfully!')