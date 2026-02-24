# WhatsApp Business API & Gmail Integration Guide
**Sprint 4 | Week 20 | Phase 3: Sprint-Based Development**
**Sprint Goal:** Voice-triggered WhatsApp/Gmail send and read-aloud inbox
**Date Range:** 3 – 7 February 2025

---

## 1. Sprint 4 Scope

| Feature | Platform |
|---------|---------|
| Send WhatsApp message via voice | WhatsApp Business API / Twilio |
| Read unread WhatsApp messages | (limited — see section 3) |
| Read top emails aloud | Gmail API |
| Compose and send email via voice | Gmail API |
| Notification count on dashboard | Gmail API |

---

## 2. Gmail API Integration

### 2.1 Setup (OAuth 2.0)

```bash
pip install google-auth-oauthlib google-api-python-client

# credentials.json: downloaded from Google Cloud Console
# Project: AMMS-Gmail
# Scopes: gmail.readonly, gmail.send, gmail.modify
```

### 2.2 Authentication Flow

```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)
```

### 2.3 Read Unread Emails

```python
import base64
from email import message_from_bytes

def get_unread_emails(service, max_results=5):
    results = service.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        raw = service.users().messages().get(
            userId='me', id=msg['id'], format='full').execute()
        headers = raw['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        emails.append({'id': msg['id'], 'subject': subject, 'from': sender})

    return emails
```

### 2.4 Send Email

```python
import base64
from email.mime.text import MIMEText

def send_email(service, to: str, subject: str, body: str):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()
```

---

## 3. WhatsApp Integration Options

### 3.1 Option A: WhatsApp Business API (Meta Official)

- **Requires:** Meta-verified business account, approved templates
- **AMMS Limitation:** Requires a real business with Meta approval
- **Use case:** Production / commercial deployment

```python
import requests

WA_TOKEN = 'YOUR_WA_ACCESS_TOKEN'
PHONE_ID = 'YOUR_PHONE_NUMBER_ID'

def send_whatsapp(to: str, message: str):
    url = f'https://graph.facebook.com/v17.0/{PHONE_ID}/messages'
    headers = {'Authorization': f'Bearer {WA_TOKEN}',
               'Content-Type': 'application/json'}
    payload = {
        'messaging_product': 'whatsapp',
        'to': to,
        'type': 'text',
        'text': {'body': message}
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
```

### 3.2 Option B: Twilio (Recommended for Development)

Twilio provides a WhatsApp sandbox for testing without Meta approval:

```python
from twilio.rest import Client

ACCOUNT_SID = 'ACxxxxxxxxxxxxxxxx'
AUTH_TOKEN  = 'your_auth_token'
FROM_NUM    = 'whatsapp:+14155238886'   # Twilio sandbox

def send_whatsapp_twilio(to_number: str, body: str):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        from_=FROM_NUM,
        body=body,
        to=f'whatsapp:{to_number}'
    )
    return message.sid
```

### 3.3 Comparison

| | Meta Official API | Twilio Sandbox | pywhatkit |
|--|---|---|---|
| Approval needed | Yes (business) | Sandbox only | WhatsApp Web session |
| Reliability | High | High | Medium |
| Cost | Per message | Per message | Free |
| AMMS use | Production | ✅ Development | Prototype only |

---

## 4. Voice-Triggered Send Flow

```
User says: "AURA, send a WhatsApp to Ali saying I'll be 10 minutes late"
    ↓
Whisper STT transcribes: "send a WhatsApp to Ali saying I'll be 10 minutes late"
    ↓
LLM extracts intent:
{
    "action": "send_whatsapp",
    "recipient_name": "Ali",
    "message": "I'll be 10 minutes late"
}
    ↓
AMMS looks up Ali's number in contacts.csv
    ↓
Confirmation: "Sending to Ali (+60123456789): I'll be 10 minutes late. Confirm?"
    ↓
User: "Yes" / "Send it"
    ↓
WhatsApp API call → sent ✅
    ↓
AURA: "Message sent to Ali."
```

### 4.1 Intent Extraction Prompt

```
You are a command parser. Extract from user utterance:
- action: send_whatsapp | send_email | read_emails | read_whatsapp
- recipient_name: string or null
- message: string or null

User utterance: "{utterance}"

Return valid JSON only. No explanation.
```

---

## 5. Contacts Management

AMMS uses a local `contacts.csv` for contact lookup:

```csv
Name,Phone,Email,WhatsApp
Ali Hassan,+60123456789,ali@example.com,+60123456789
Siti Nabilah,+60198765432,siti@example.com,+60198765432
```

```python
import csv

def find_contact(name: str) -> dict | None:
    with open('contacts.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if name.lower() in row['Name'].lower():
                return row
    return None
```

---

## 6. Security Considerations

| Risk | Mitigation |
|------|-----------|
| Unintended message sending | Always confirm before sending |
| Contact name ambiguity ("send to Ali" if 3 Alis) | List matching contacts for user to choose |
| API tokens in config | Store in `.env` (python-dotenv); never commit |
| Replay attack on voice confirmation | One-time session token per send operation |

---

## 7. References

1. Meta (2024). *WhatsApp Business Platform Documentation.* developers.facebook.com/docs/whatsapp.
2. Twilio (2024). *WhatsApp API for Developers.* twilio.com/docs/whatsapp.
3. Google (2024). *Gmail API Reference.* developers.google.com/gmail/api.
4. Ratadiya, P. (2019). "Natural Language Understanding: The Future of AI." *Towards Data Science.*
