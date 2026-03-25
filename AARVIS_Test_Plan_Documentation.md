# 6 Testing

## 6.1 Test Plan

### 6.1.1 Authentication and Session Module

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC1 | Login with valid username and password | Redirect to mirror dashboard | Successful |
| TC2 | Login with incorrect password | Show invalid credentials error | Successful |
| TC3 | Login with non-existent username | Show invalid credentials error | Successful |
| TC4 | Login with empty fields | Prompt required fields | Successful |
| TC5 | Password field masking | Password hidden in UI | Successful |
| TC6 | Register with valid data | Account created and session started | Successful |
| TC7 | Register with duplicate username | Show username already exists error | Successful |
| TC8 | Register with duplicate email | Show email already exists error | Successful |
| TC9 | Logout from active session | Session cleared and redirect to login | Successful |
| TC10 | Access protected route without session | Return unauthorized/redirect login | Successful |

---

### 6.1.2 Google OAuth and Mobile Pairing Flow

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC11 | Start Google OAuth from register page | Redirect to Google consent page | Successful |
| TC12 | Start Google OAuth from login page | Redirect to Google consent page | Successful |
| TC13 | OAuth callback with valid code | User session created successfully | Successful |
| TC14 | OAuth callback with missing code | Redirect with no_code error | Successful |
| TC15 | OAuth callback with access denied | Redirect with access_denied error | Successful |
| TC16 | Phone QR scan opens mobile pairing page | Mobile connect page loads | Successful |
| TC17 | Pair status polling before completion | Status remains pending/triggered | Successful |
| TC18 | Pair completion syncs PC session | PC receives session token and destination | Successful |
| TC19 | Private IP callback blocked case | Proper fallback guidance shown | Successful |
| TC20 | PC fallback trigger from phone | PC opens OAuth flow correctly | Successful |

---

### 6.1.3 Face Recognition and Face Enrollment

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC21 | Enroll face with valid image set | Embeddings saved successfully | Successful |
| TC22 | Enroll face with empty image list | Show no images provided error | Successful |
| TC23 | Enroll face with no detectable face | Show no face detected error | Successful |
| TC24 | Face login with enrolled user | Login successful with confidence value | Successful |
| TC25 | Face login with unknown user | Authentication denied | Successful |
| TC26 | Face verification API with valid image | Detected user and confidence returned | Successful |
| TC27 | Face verification API with invalid payload | Return detected false/error message | Successful |
| TC28 | Face cache check within valid window | Return cached true with remaining time | Successful |
| TC29 | Face cache check after expiry | Return cached false and reverify needed | Successful |
| TC30 | Face engine unavailable scenario | Graceful fallback message shown | Successful |

---

### 6.1.4 Voice Assistant Pipeline (WebSocket, STT, TTS)

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC31 | WebSocket connect with valid session | Connection established | Successful |
| TC32 | WebSocket connect without session | Connection rejected with auth error | Successful |
| TC33 | Send text message over WebSocket | Assistant returns streamed response | Successful |
| TC34 | Send audio message for STT | Transcript generated and displayed | Successful |
| TC35 | Low-quality audio input | Graceful could-not-understand response | Successful |
| TC36 | TTS chunk streaming to browser | Audio chunks queued and played in order | Successful |
| TC37 | Voice state transition (listening-thinking-speaking-idle) | UI state changes correctly | Successful |
| TC38 | Continuous VAD mode with speech detection | Auto-capture starts and stops properly | Successful |
| TC39 | Say logout command (bye) | Session closed and redirect to login | Successful |
| TC40 | Assistant fallback on model exception | Friendly fallback response returned | Successful |

---

### 6.1.5 Calendar and Scheduling Module

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC41 | Fetch today's calendar events | Correct event list displayed | Successful |
| TC42 | Fetch upcoming events | Upcoming events returned with event IDs | Successful |
| TC43 | Create event with valid date/time | Event created successfully | Successful |
| TC44 | Create event with 12-hour time input | Time normalized to 24-hour and created | Successful |
| TC45 | Create event with missing title | Validation error returned | Successful |
| TC46 | Update event with valid event_id | Event updated successfully | Successful |
| TC47 | Delete event with valid event_id | Event deleted successfully | Successful |
| TC48 | Calendar API unavailable/network timeout | Graceful error and empty/fallback response | Successful |
| TC49 | Dashboard calendar endpoint formatting | Events include status/time for UI rendering | Successful |
| TC50 | Voice scheduling intent parsing | Correct tool called and result spoken | Successful |

---

### 6.1.6 Gmail and Intelligent Email Assistant Module

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC51 | Fetch unread emails | Sender, subject, and preview returned | Successful |
| TC52 | Summarize latest email by sender | Summary returned successfully | Successful |
| TC53 | Send email direct mode (subject/body provided) | Email sent via Gmail API | Successful |
| TC54 | Send email auto-compose mode (topic only) | Draft auto-generated and sent | Successful |
| TC55 | Send email with contact name lookup | Name resolved to contact email and sent | Successful |
| TC56 | Send email with unknown contact name | Prompt to provide direct email | Successful |
| TC57 | Gmail token expired with refresh token available | Token refreshed and request succeeds | Successful |
| TC58 | Gmail access unavailable for non-OAuth user | Graceful failure message shown | Successful |
| TC59 | Voice request to read emails | Correct email tool invoked and spoken output | Successful |
| TC60 | Voice request to send email | Send tool invoked with proper confirmation behavior | Successful |

---

### 6.1.7 Dashboard Content and Data Refresh

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC61 | Time display accuracy | Correct local time shown | Successful |
| TC62 | Date display accuracy | Correct local date shown | Successful |
| TC63 | Greeting based on time of day | Proper greeting displayed | Successful |
| TC64 | Weather API success | Weather widget populated | Successful |
| TC65 | Weather API failure | Fallback message/data shown | Successful |
| TC66 | News API success | Headlines rendered in news section | Successful |
| TC67 | News API failure | Graceful fallback message shown | Successful |
| TC68 | Periodic weather refresh | Data refreshes at configured interval | Successful |
| TC69 | Periodic news refresh | Data refreshes at configured interval | Successful |
| TC70 | Periodic calendar refresh | Schedule refreshes at configured interval | Successful |

---

### 6.1.8 Admin Panel and User Management

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC71 | Open admin page | Admin dashboard loads successfully | Successful |
| TC72 | List all users | User table populated correctly | Successful |
| TC73 | Search users by name/username/email | Filtered results shown correctly | Successful |
| TC74 | Edit user profile fields | User details updated successfully | Successful |
| TC75 | Delete user account | User removed from DB | Successful |
| TC76 | Delete user with face enrollment | Face embeddings removed from storage | Successful |
| TC77 | Admin face list endpoint | Enrolled face usernames returned | Successful |
| TC78 | Modal cancel/close behavior | No unwanted update occurs | Successful |
| TC79 | Invalid update target user ID | User not found error returned | Successful |
| TC80 | Admin UI responsiveness | Layout remains usable across screen sizes | Successful |

---

### 6.1.9 Database, Security, and Compatibility Testing

| TC No. | Test Case Description | Expected Result | Status |
|---|---|---|---|
| TC81 | Password storage validation | Passwords stored as hashes, not plain text | Successful |
| TC82 | Session cookie properties check | HttpOnly and proper expiry set | Successful |
| TC83 | Conversation history save and load | Messages persisted and loaded correctly | Successful |
| TC84 | Per-user OAuth token isolation | User A cannot access User B tokens/data | Successful |
| TC85 | Database migration on startup | Missing columns/indexes created safely | Successful |
| TC86 | Browser compatibility (Chrome) | Core features function correctly | Successful |
| TC87 | Browser compatibility (Edge) | Core features function correctly | Successful |
| TC88 | Browser compatibility (Firefox) | Core features function correctly | Successful |
| TC89 | Recovery after temporary network loss | App reconnects/retries without crash | Successful |
| TC90 | Long-running WebSocket stability | No memory leak/crash in normal session | Successful |

---

## 6.2 Overall Testing Outcome
- Authentication, face recognition, voice assistant, scheduling, and email workflows performed according to expected behavior.
- Dashboard data modules (weather, news, calendar) updated and rendered correctly with fallback handling for failure scenarios.
- Admin and database operations were validated for correctness and consistency.
- Security and compatibility checks confirmed readiness for controlled deployment and further user acceptance testing.
