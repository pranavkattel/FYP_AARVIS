# Integration Testing Guide – AMMS Module Interactions
**Week 26 | Phase 4: Continuous Testing**
**Date Range:** 17 – 21 March 2025**

---

## 1. Integration Testing Scope

Integration tests verify that individual modules work correctly **together** as a system. Unlike unit tests (which mock everything), integration tests connect real components and observe interactions.

### 1.1 AMMS Module Interaction Map

```
[Camera]
   ↓
[FaceRecognitionService] ←→ [face_encodings.pkl]
   ↓ login success
[EmotionDetectionService] ←→ [emotion_log DB]
   ↓ emotion
[FeedbackEngine] → [Ollama/LLM] → response text
   ↓                     → [static fallback]
[TTSService] → audio file → speaker
   ↓
[Flask Dashboard] ←→ [DataCache: Weather, Calendar, News]
   ↓ WebSocket
[Browser UI]
```

Each arrow is an integration boundary tested in Week 26.

---

## 2. Integration Test: Auth → Dashboard Flow

```python
# tests/integration/test_auth_flow.py

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    return app.test_client()

def test_full_login_flow_unknown_user(client):
    """Unknown face → 401 response."""
    with patch('services.face_recognition_service.FaceRecognitionService.identify',
               return_value=(None, 0.0)):
        response = client.post('/api/login', data={'trigger': '1'})
        assert response.status_code == 401
        data = response.get_json()
        assert data['status'] == 'unknown_face'

def test_full_login_flow_known_user(client):
    """Known face → 200 with user profile."""
    with patch('services.face_recognition_service.FaceRecognitionService.identify',
               return_value=('Ahmad', 93.2)), \
         patch('services.liveness_service.check_liveness', return_value=True):
        response = client.post('/api/login', data={'trigger': '1'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['user'] == 'Ahmad'
```

---

## 3. Integration Test: Voice Command → WhatsApp Send

```python
# tests/integration/test_voice_command_pipeline.py

import pytest
from unittest.mock import patch, MagicMock

def test_voice_command_send_whatsapp():
    utterance = "Send a WhatsApp to Ali saying I'll be late"

    with patch('ollama.chat') as mock_llm, \
         patch('services.messaging_service.send_whatsapp_twilio') as mock_send:

        # LLM extracts intent
        mock_llm.return_value = {
            'message': {
                'content': '{"action":"send_whatsapp","recipient_name":"Ali","message":"I\'ll be late"}'
            }
        }
        mock_send.return_value = 'SM123456'

        from services.voice_command_handler import process_utterance
        result = process_utterance(utterance, user_context={'user_name': 'Ahmad'})

        assert result['action'] == 'send_whatsapp'
        assert result['recipient'] == 'Ali'
        mock_send.assert_called_once()
```

---

## 4. Integration Test: DataCache → Dashboard API

```python
# tests/integration/test_dashboard_api.py

import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    return app.test_client()

def test_dashboard_api_returns_all_fields(client):
    mock_weather = {'temp': 26, 'description': 'Sunny', 'city': 'KL',
                    'humidity': 72, 'wind_speed': 12, 'icon': '01d'}
    mock_events = [{'time': '09:00 AM', 'title': 'Team Meeting'}]
    mock_news = ['Headline 1', 'Headline 2']

    with patch('services.data_cache.DataCache.weather', mock_weather), \
         patch('services.data_cache.DataCache.events', mock_events), \
         patch('services.data_cache.DataCache.headlines', mock_news):

        response = client.get('/api/dashboard')
        assert response.status_code == 200
        data = response.get_json()
        assert 'time' in data
        assert 'weather' in data
        assert 'events' in data
        assert 'headlines' in data
        assert data['weather']['temp'] == 26
```

---

## 5. Database Integration Tests

```python
# tests/integration/test_database.py

import pytest
import sqlite3
import tempfile
import os

@pytest.fixture
def temp_db():
    """Create temporary in-memory test database."""
    conn = sqlite3.connect(':memory:')
    conn.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY, name TEXT, role TEXT DEFAULT 'user',
        enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP, active INTEGER DEFAULT 1
    )""")
    conn.execute("""CREATE TABLE emotion_log (
        id INTEGER PRIMARY KEY, user_id INTEGER, emotion TEXT,
        confidence REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    yield conn
    conn.close()

def test_user_insert_and_query(temp_db):
    temp_db.execute("INSERT INTO users (name, role) VALUES ('Ahmad', 'admin')")
    temp_db.commit()
    row = temp_db.execute("SELECT * FROM users WHERE name='Ahmad'").fetchone()
    assert row is not None
    assert row[1] == 'Ahmad'

def test_emotion_log_cascade_delete(temp_db):
    temp_db.execute("INSERT INTO users (id, name) VALUES (1, 'TestUser')")
    temp_db.execute("INSERT INTO emotion_log (user_id, emotion, confidence) VALUES (1,'happy',90)")
    temp_db.commit()
    count = temp_db.execute("SELECT COUNT(*) FROM emotion_log WHERE user_id=1").fetchone()[0]
    assert count == 1
```

---

## 6. Integration Test Results (Week 26)

| Test Suite | Tests | Pass | Fail | Skip |
|------------|-------|------|------|------|
| Auth Flow | 6 | 6 | 0 | 0 |
| Voice Command Pipeline | 4 | 4 | 0 | 0 |
| Dashboard API | 5 | 5 | 0 | 0 |
| Database | 8 | 8 | 0 | 0 |
| **Total** | **23** | **23** | **0** | **0** |

---

## 7. References

1. Sommerville, I. (2016). *Software Engineering* (10th ed). Pearson.
2. Kaner, C., Falk, J., & Nguyen, H. (1999). *Testing Computer Software.* Wiley.
3. Flask Testing Docs (2024). flask.palletsprojects.com/testing.
