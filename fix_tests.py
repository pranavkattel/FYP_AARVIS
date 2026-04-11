import os

content = """# 6 Testing

## 6.1 Test Plan

### 6.1.1 Project Overview
The testing phase for the AARVIS smart mirror evaluates the core integrations: Google OAuth, PyTorch-based Facial Recognition, WebSocket Voice Assistant, and Google Workspace APIs (Calendar & Gmail).

The test cases focus on functional user journeys, intelligent voice interactions, and system-level integrations.

### 6.1.2 Authentication & Device Pairing
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC01 | Google OAuth Login | User successfully authenticates via Google consent screen and session is created. | Planned |
| TC02 | Cross-Device QR Pairing | Scanning the QR on mobile logs the user in via Google and signals the mirror to proceed. | Planned |
| TC03 | Unauthorized Access | Attempting to access the dashboard `/` without a session redirects to `/login`. | Planned |

### 6.1.3 Facial Recognition (PyTorch MobileNetV2)
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC04 | Face Liveness & Motion Checks | System successfully tracks user motion (look left/right/up/down) during enrollment. | Planned |
| TC05 | Face Registration & Embedding | System successfully extracts 512-D embeddings from captured frames and saves to DB. | Planned |
| TC06 | Lighting & Environment Tolerance | Model successfully recognizes faces in both well-lit and dim environments. | Planned |
| TC07 | Face Login (Authorized) | Registered user is recognized (cosine similarity > 0.40) and logged into the dashboard. | Planned |
| TC08 | Face Login (Unauthorized) | Unregistered face is rejected and access is denied. | Planned |
| TC09 | Edge Cases (No Face & Occlusion) | System handles empty frames without crashing and rejects partially covered faces appropriately. | Planned |

### 6.1.4 Smart Dashboard & Background Services
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC10 | Widget Initialization | Weather, News, and Clock widgets load immediately with user-specific preferences. | Planned |
| TC11 | Morning Briefing | LLM synthesizes current time, weather, news, and calendar into a concise welcome message. | Planned |
| TC12 | Periodic Refresh | Widgets auto-refresh in the background without refreshing the browser page. | Planned |

### 6.1.5 Voice Assistant & Conversational AI
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC13 | General Knowledge Inquiry | User asks a normal question (e.g., "What is the capital of France?") and receives an accurate voice response. | Planned |
| TC14 | Weather Inquiry | User asks about the current weather; assistant queries weather tool and speaks the result. | Planned |
| TC15 | Contextual Reasoning (Clothing) | User asks "What should I wear today?"; assistant checks weather and suggests appropriate clothing. | Planned |
| TC16 | Voice-to-Text & Text-to-Voice | Spoken audio is correctly transcribed (STT), and AI responses are smoothly played back (TTS). | Planned |
| TC17 | Conversational Memory | The assistant correctly answers follow-up questions referencing previous conversational turns. | Planned |

### 6.1.6 Intelligent Google Services (Calendar & Gmail)
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC18 | Read Schedule | Asking "What's my schedule today?" fetches and reads today's events accurately. | Planned |
| TC19 | Create Calendar Event | Asking to "Schedule a meeting at 3 PM" creates the event in Google Calendar. | Planned |
| TC20 | Update Calendar Event | Asking to "Move my 3 PM meeting to 4 PM" successfully updates the existing event time. | Planned |
| TC21 | Delete/Cancel Calendar Event | Asking to "Cancel my 4 PM meeting" removes it from Google Calendar after confirmation. | Planned |
| TC22 | Check New Emails | Asking "Do I have any new emails?" fetches the list of unread emails from Gmail. | Planned |
| TC23 | Summarize Emails | Asking "Summarize my recent emails" provides a concise voice summary of the latest messages. | Planned |
| TC24 | Draft & Send Email via Contacts | Asking "Send an email to John about the project" resolves 'John' using `contacts.csv`, drafts the content, and sends via Gmail API. | Planned |

### 6.1.7 System Resiliency
| TC No. | Description | Expected Result | Status |
|---|---|---|---|
| TC25 | OAuth Token Expiry | The system intelligently handles expired Google Access tokens by using the Refresh token. | Planned |
| TC26 | System Fallbacks | If a third-party API (e.g., Weather) is down, the mirror UI remains stable with fallback text. | Planned |

## 6.2 Testing Summary
This refined test plan validates the critical pathways of the AARVIS smart mirror. By focusing on integration and system-level behavior, it ensures that the hardware components (camera, mic) interact flawlessly with the AI pipelines (PyTorch, LangGraph, STT/TTS) and external APIs (Google Workspace).
"""

with open(r'd:\langgraph\final fixed fyp\docs\test_cases.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated')