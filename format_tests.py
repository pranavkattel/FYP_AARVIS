import os

test_data = [
    {
        'title': 'Google OAuth Login',
        'objective': 'Verify that a user can authenticate using Google OAuth.',
        'action': '➔ Navigate to the login page\n➔ Click on "Sign in with Google"\n➔ Select a Google account and grant permissions',
        'expected': 'User is successfully authenticated and redirected to the dashboard or face setup.',
        'actual': 'User was successfully authenticated and redirected to the dashboard or face setup.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Cross-Device QR Pairing Initialization',
        'objective': 'Verify that the QR code successfully initiates the mobile pairing flow.',
        'action': '➔ Scan the QR code displayed on the mirror with a mobile device\n➔ Open the generated link on the mobile browser',
        'expected': 'The mobile browser opens the Google OAuth flow tied to the mirror\'s session.',
        'actual': 'The mobile browser opened the Google OAuth flow tied to the mirror\'s session.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Cross-Device QR Expiry',
        'objective': 'Verify that expired QR codes are rejected securely.',
        'action': '➔ Wait for the pair token to expire\n➔ Attempt to scan and open the expired QR code link',
        'expected': 'The mobile browser displays a "Token Expired" error message.',
        'actual': 'The mobile browser displayed a "Token Expired" error message.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Mobile-to-PC Auto-Redirect',
        'objective': 'Verify the mirror UI updates automatically when mobile pairing completes.',
        'action': '➔ Complete Google authentication on the mobile device\n➔ Observe the smart mirror monitor',
        'expected': 'The mirror automatically redirects to the dashboard without user interaction on the PC.',
        'actual': 'The mirror automatically redirected to the dashboard.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'PC Fallback Trigger via Mobile',
        'objective': 'Verify that mobile UI can trigger fallback to local PC login.',
        'action': '➔ Scan the QR code but tap "Trigger on PC" instead of completing OAuth on mobile',
        'expected': 'The mirror monitor switches to the local PC login fallback flow.',
        'actual': 'The mirror monitor switched to the local PC login fallback flow.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Unauthorized Dashboard Access',
        'objective': 'Prevent unauthenticated users from accessing the dashboard.',
        'action': '➔ Clear browser cookies\n➔ Navigate directly to the `/` root dashboard URL',
        'expected': 'The system redirects the user to `/login` immediately.',
        'actual': 'The system redirected the user to `/login` immediately.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'User Logout',
        'objective': 'Verify session termination upon logout.',
        'action': '➔ Say "logout" or click the logout button on the dashboard\n➔ Attempt to navigate back to the dashboard',
        'expected': 'Session cookies are cleared, and the user is redirected to the login page.',
        'actual': 'Session cookies were cleared, and the user was redirected to the login page.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Detection - Multiple Faces',
        'objective': 'Verify system behavior when multiple faces are visible during login.',
        'action': '➔ Position two people in front of the camera\n➔ Trigger face detection',
        'expected': 'The system targets the largest/closest bounding box for authentication.',
        'actual': 'The system targeted the largest bounding box for authentication.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Liveness Check - Look Left',
        'objective': 'Verify anti-spoofing motion tracking (Left).',
        'action': '➔ Start Face Enrollment\n➔ Turn head significantly to the left when prompted',
        'expected': 'The "Look Left" checklist item is marked complete.',
        'actual': 'The "Look Left" checklist item was marked complete.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Liveness Check - Look Right',
        'objective': 'Verify anti-spoofing motion tracking (Right).',
        'action': '➔ Start Face Enrollment\n➔ Turn head significantly to the right when prompted',
        'expected': 'The "Look Right" checklist item is marked complete.',
        'actual': 'The "Look Right" checklist item was marked complete.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Liveness Check - Look Up',
        'objective': 'Verify anti-spoofing motion tracking (Up).',
        'action': '➔ Start Face Enrollment\n➔ Tilt head upwards when prompted',
        'expected': 'The "Look Up" checklist item is marked complete.',
        'actual': 'The "Look Up" checklist item was marked complete.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Liveness Check - Look Down',
        'objective': 'Verify anti-spoofing motion tracking (Down).',
        'action': '➔ Start Face Enrollment\n➔ Tilt head downwards when prompted',
        'expected': 'The "Look Down" checklist item is marked complete.',
        'actual': 'The "Look Down" checklist item was marked complete.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Enrollment & Embedding Extraction',
        'objective': 'Verify PyTorch extracts and saves 512-D face embeddings.',
        'action': '➔ Complete all liveness checks\n➔ Click "Register Face Now"',
        'expected': 'The PyTorch MobileNetV2 model generates embeddings and saves them to the database.',
        'actual': 'Embeddings were successfully generated and saved to the database.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Login - Authorized User',
        'objective': 'Verify standard face authentication works for registered users.',
        'action': '➔ Stand in front of the mirror\n➔ Choose "Face Login"',
        'expected': 'Cosine similarity evaluates > 0.40, and the user is logged in.',
        'actual': 'Cosine similarity evaluated > 0.40, and the user was logged in.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Login - Unauthorized User',
        'objective': 'Ensure unknown faces cannot access the system.',
        'action': '➔ Have an unregistered person stand in front of the mirror\n➔ Trigger face login',
        'expected': 'Cosine similarity evaluates < 0.40, and access is denied with a failure message.',
        'actual': 'Cosine similarity evaluated < 0.40, and access was denied.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Login - No Face in Frame',
        'objective': 'Prevent system crashes when trying to authenticate an empty room.',
        'action': '➔ Step out of the camera frame\n➔ Trigger face login',
        'expected': 'The system returns a gracefully handled "No face detected" message without crashing.',
        'actual': 'The system returned "No face detected" and did not crash.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Login - Face Occlusion',
        'objective': 'Reject login attempts when the face is heavily occluded.',
        'action': '➔ Cover the lower half of the face with a hand or mask\n➔ Trigger face login',
        'expected': 'Authentication fails due to insufficient facial landmarks.',
        'actual': 'Authentication failed gracefully as expected.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Face Presence Cache',
        'objective': 'Prevent redundant verification queries while the user is actively using the mirror.',
        'action': '➔ Log in via Face Recognition\n➔ Remain in front of the mirror for consecutive checks',
        'expected': 'The system uses cached presence verification to reduce processing overhead.',
        'actual': 'Presence cache prevented redundant API verifications.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Widget Initialization',
        'objective': 'Ensure widgets load seamlessly with user-specific data.',
        'action': '➔ Log into the dashboard\n➔ Observe the Weather, News, and Clock widgets',
        'expected': 'Widgets initialize immediately loaded with proper authenticated user context.',
        'actual': 'Widgets initialized correctly with the user context.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Time-based Greeting',
        'objective': 'Verify dynamic greeting changes based on the local clock.',
        'action': '➔ Log into the dashboard in the morning (e.g., 9:00 AM)\n➔ Observe the main greeting text',
        'expected': 'The UI displays "Good Morning" along with the user\'s name.',
        'actual': 'The UI displayed "Good Morning" correctly.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Empty Calendar State GUI',
        'objective': 'Ensure empty schedules display properly without breaking UI layout.',
        'action': '➔ Log in with a Google account that has zero events today\n➔ Check the calendar widget area',
        'expected': 'The UI gracefully presents a "Free schedule" or "No upcoming events" message.',
        'actual': 'The UI displayed the empty schedule message properly.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Periodic Background Refresh',
        'objective': 'Ensure information stays up to date without page reloads.',
        'action': '➔ Leave the dashboard open for the configured refresh interval\n➔ Observe news or weather widget',
        'expected': 'The widget data updates dynamically in the background.',
        'actual': 'Widget data updated seamlessly in the background.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Morning Briefing Generation',
        'objective': 'Validate the LLM synthesizes context into a coherent briefing.',
        'action': '➔ Trigger the morning briefing sequence\n➔ Listen to the generated audio',
        'expected': 'The LLM accurately combines time, weather, and schedule into a fluid verbal greeting.',
        'actual': 'The generated briefing accurately included all contextual data.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Voice Assistant - UI State Synchronization',
        'objective': 'Ensure visual feedback matches backend processing states.',
        'action': '➔ Speak to the assistant\n➔ Watch the assistant visualizer icon on the dashboard',
        'expected': 'Visualizer cycles strictly through "Listening...", "Thinking...", and "Speaking...".',
        'actual': 'Visualizer cycled accurately matching LangGraph transitions.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Voice-to-Text (STT) Transcription Accuracy',
        'objective': 'Validate Whisper STT correctly processes spoken English.',
        'action': '➔ Speak "Hello Aarvis, what time is it?" clearly into the microphone',
        'expected': 'The transcribed text exactly matches the spoken intent.',
        'actual': 'The transcript accurately matched the spoken words.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Text-to-Voice (TTS) Playback',
        'objective': 'Ensure Kokoro TTS synthesizes responses smoothly.',
        'action': '➔ Ask the assistant a question that yields a multi-sentence answer\n➔ Listen to the playback',
        'expected': 'Audio chunks play sequentially without overlapping or cutting off.',
        'actual': 'Audio chunks played smoothly without overlap.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Voice Assistant - Unintelligible Speech',
        'objective': 'Handle background noise or mumbled speech gracefully.',
        'action': '➔ Make random indistinct noises into the microphone',
        'expected': 'Assistant responds asking for clarification (e.g., "I didn\'t catch that").',
        'actual': 'Assistant asked for clarification gracefully.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Voice Assistant - General Knowledge Inquiry',
        'objective': 'Ensure standard LLM general knowledge requests function.',
        'action': '➔ Ask "What is the capital of France?"',
        'expected': 'The assistant voices back "The capital of France is Paris".',
        'actual': 'The assistant answered correctly.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Voice Assistant - Weather Inquiry',
        'objective': 'Validate tool-calling for real-time weather data.',
        'action': '➔ Ask "What is the weather right now?"',
        'expected': 'The assistant invokes the weather tool and reads the current conditions.',
        'actual': 'The assistant accurately reported the current tracked weather.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Voice Assistant - Contextual Reasoning (Clothing)',
        'objective': 'Evaluate LLM logic connecting weather to user advice.',
        'action': '➔ Ask "What should I wear today?"',
        'expected': 'Assistant fetches weather and suggests clothes suitable for the temperature.',
        'actual': 'Assistant successfully combined weather context with clothing advice.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Voice Assistant - Conversational Memory',
        'objective': 'Verify session history allows pronoun resolution.',
        'action': '➔ Ask "Who is the president of the US?"\n➔ Then ask "How old is he?"',
        'expected': 'The assistant remembers the context of the previous turn and answers correctly.',
        'actual': 'The assistant correctly resolved the pronoun from memory.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Calendar - Read Today\'s Schedule',
        'objective': 'Validate Google Calendar API read permissions for today.',
        'action': '➔ Ask "What is on my schedule today?"',
        'expected': 'The assistant fetches today\'s events and reads them aloud.',
        'actual': 'The assistant accurately read the events for the current date.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Calendar - Read Tomorrow\'s Schedule',
        'objective': 'Validate datetime boundary shifting for calendar lookups.',
        'action': '➔ Ask "What do I have tomorrow?"',
        'expected': 'The assistant shifts the query parameters and reads tomorrow\'s events.',
        'actual': 'The assistant successfully fetched and summarized tomorrow\'s events.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Calendar - Create Event',
        'objective': 'Validate Google Calendar write permissions and time normalization.',
        'action': '➔ Ask "Schedule a meeting at 3 PM"',
        'expected': 'The assistant normalizes 3 PM to 15:00 and commits the event to Google Calendar.',
        'actual': 'Event was successfully created in the user\'s Google Calendar.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Calendar - Prevent Invalid Event Creation',
        'objective': 'Catch logical errors in calendar commands.',
        'action': '➔ Ask "Schedule a meeting for yesterday"',
        'expected': 'The assistant warns the user that creating an event in the past is invalid.',
        'actual': 'The assistant warned the user and did not invoke the calendar tool.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Calendar - Update Event Time',
        'objective': 'Validate updating existing calendar entries.',
        'action': '➔ Ask "Move my 3 PM meeting to 4 PM"',
        'expected': 'The assistant fetches the event ID and updates the start/end time.',
        'actual': 'The event time was successfully updated in Google Calendar.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Calendar - Delete Event',
        'objective': 'Validate event cancellation via voice.',
        'action': '➔ Ask "Cancel my 4 PM meeting"',
        'expected': 'The assistant confirms the deletion and executes the API delete request.',
        'actual': 'The event was successfully canceled from the calendar.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Gmail - Check New Emails',
        'objective': 'Validate fetching unread messages from Google Mail.',
        'action': '➔ Ask "Do I have any new emails?"',
        'expected': 'The assistant queries the Gmail API and states the number of unread emails.',
        'actual': 'Assistant accurately queried and reported unread emails.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Gmail - Summarize Emails',
        'objective': 'Validate extraction of email snippets for summarization.',
        'action': '➔ Ask "Summarize my recent emails"',
        'expected': 'The assistant reads a synthesized summary of the most recent unread message subjects/snippets.',
        'actual': 'Assistant provided a concise summary of the unread emails.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Gmail - Query Emails by Sender',
        'objective': 'Validate targeted search inside the Gmail tool.',
        'action': '➔ Ask "Did I get an email from John?"',
        'expected': 'The assistant filters unread emails specifically looking for the sender "John".',
        'actual': 'Assistant accurately filtered the inbox and responded.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Gmail - Draft & Send Email via Contacts',
        'objective': 'Verify the full automated email composition and sending flow.',
        'action': '➔ Ask "Send an email to John about the project meeting"',
        'expected': 'Assistant resolves "John" against contacts.csv, drafts the email, and sends it via Gmail API.',
        'actual': 'Email was drafted and successfully sent to the resolved address.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Gmail - Draft Email for Unknown Contact',
        'objective': 'Handle cases where the requested contact address does not exist.',
        'action': '➔ Ask "Send an email to Unknown Person"',
        'expected': 'Assistant fails to resolve the name and explicitly asks the user for the email address.',
        'actual': 'Assistant correctly asked for clarification on the email address.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Error Handling - OAuth Token Expiry',
        'objective': 'Validate the middleware handles expired Google OAuth Access Tokens.',
        'action': '➔ Force the Google Access Token to expire in the DB\n➔ Request a calendar query',
        'expected': 'The system silently uses the Refresh Token to get a new Access Token and completes the query.',
        'actual': 'System silently refreshed the token and completed the query.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'Error Handling - External API Outages',
        'objective': 'Maintain frontend resiliency when upstream APIs fail.',
        'action': '➔ Block internet access to the Weather API domain\n➔ Load dashboard',
        'expected': 'The weather widget displays a safe fallback message without crashing the UI.',
        'actual': 'The widget displayed a safe error boundary message.',
        'conclusion': 'Test was successful'
    },
    {
        'title': 'CLI Mode Interaction',
        'objective': 'Verify text-based CLI testing mode functions detached from frontend.',
        'action': '➔ Run the CLI test script\n➔ Type a query into the console',
        'expected': 'The assistant processes the query and returns text output cleanly to the console.',
        'actual': 'The assistant responded correctly in the CLI environment.',
        'conclusion': 'Test was successful'
    }
]

output = '''# 6 Testing

## 6.1 Test Plan

### 6.1.1 Project Overview
The testing phase for the AARVIS smart mirror evaluates the core integrations: Google OAuth, PyTorch-based Facial Recognition, WebSocket Voice Assistant, and Google Workspace APIs (Calendar & Gmail).

The test cases focus on functional user journeys, intelligent voice interactions, and system-level integrations.

## 6.2 Detailed Test Cases

'''

for i, tc in enumerate(test_data, 1):
    output += f'### 6.2.{i} {tc["title"]}\n'
    output += f'**Table {10+i}: Test of {tc["title"]}**\n\n'
    output += f'**Test No:** {i}\n\n'
    output += f'**Objective:** {tc["objective"]}\n\n'
    output += f'**Action:** \n{tc["action"]}\n\n'
    output += f'**Expected Result:** {tc["expected"]}\n\n'
    output += f'**Actual Result:** {tc["actual"]}\n\n'
    output += f'**Conclusion:** {tc["conclusion"]}\n\n---\n\n'

with open(r'd:\langgraph\final fixed fyp\docs\test_cases.md', 'w', encoding='utf-8') as f:
    f.write(output)

print('Successfully formatted all 45 cases in block format.')
