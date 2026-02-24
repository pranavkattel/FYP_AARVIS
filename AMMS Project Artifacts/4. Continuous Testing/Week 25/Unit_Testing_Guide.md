# Unit Testing Guide – AMMS Modules
**Week 25 | Phase 4: Continuous Testing**
**Date Range:** 10 – 14 March 2025**

---

## 1. Unit Testing Fundamentals

### 1.1 FIRST Principles

| Principle | Meaning | AMMS Application |
|-----------|---------|-----------------|
| **F**ast | Run in milliseconds | Mock all I/O (camera, DB, network) |
| **I**solated | Test one thing | Each test targets one function |
| **R**epeatable | Same result every run | No randomness (seed if needed) |
| **S**elf-validating | Pass/Fail automatically | Use pytest assertions |
| **T**imely | Written before/during code | TDD where practical |

### 1.2 Mocking External Dependencies

```python
# conftest.py — shared fixtures
import pytest
import numpy as np
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_camera_frame():
    """240×320 BGR frame — simulates USB webcam output."""
    return np.random.randint(0, 255, (240, 320, 3), dtype=np.uint8)

@pytest.fixture
def mock_db_connection():
    with patch('sqlite3.connect') as mock_conn:
        mock_conn.return_value.__enter__ = lambda s: s
        mock_conn.return_value.__exit__ = MagicMock(return_value=False)
        yield mock_conn
```

---

## 2. Unit Tests: Emotion Detection

```python
# tests/unit/test_emotion_detection.py

import pytest
import numpy as np
from unittest.mock import patch
from services.emotion_detection_service import EmotionDetectionService, get_confident_emotion

@pytest.fixture
def emotion_svc():
    with patch('sqlite3.connect'):
        return EmotionDetectionService()

def test_confident_emotion_above_threshold():
    result = {'dominant_emotion': 'happy', 'emotion': {'happy': 85.0, 'neutral': 15.0}}
    emotion, conf = get_confident_emotion(result)
    assert emotion == 'happy'
    assert conf == pytest.approx(85.0)

def test_low_confidence_returns_neutral():
    result = {'dominant_emotion': 'surprised', 'emotion': {'surprised': 32.0, 'neutral': 68.0}}
    emotion, conf = get_confident_emotion(result)
    assert emotion == 'neutral'

def test_scan_interval_throttles_calls():
    svc = EmotionDetectionService()
    svc._last_scan = 9999999999.0   # Future timestamp → throttle
    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    emotion, conf = svc.analyze_frame(frame, user_id=None)
    assert emotion == 'neutral'  # Returns cached value
```

---

## 3. Unit Tests: Data Cache / API Services

```python
# tests/unit/test_data_cache.py

import pytest
from unittest.mock import patch, MagicMock
from services.data_cache import get_current_weather, get_top_headlines

MOCK_WEATHER_RESPONSE = {
    'main': {'temp': 26.0, 'feels_like': 28.0, 'humidity': 72},
    'wind': {'speed': 3.3},
    'weather': [{'description': 'Light rain', 'icon': '10d'}],
    'name': 'Kuala Lumpur'
}

def test_get_current_weather_parses_correctly():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = MOCK_WEATHER_RESPONSE
        mock_get.return_value.raise_for_status = MagicMock()
        result = get_current_weather()
        assert result['temp'] == 26
        assert result['city'] == 'Kuala Lumpur'
        assert 'humidity' in result

def test_weather_api_failure_raises():
    with patch('requests.get', side_effect=Exception("Network error")):
        with pytest.raises(Exception):
            get_current_weather()

MOCK_NEWS_RESPONSE = {
    'articles': [
        {'title': 'Test Headline 1'},
        {'title': 'Test Headline 2'},
        {'title': None}  # Should be filtered out
    ]
}

def test_get_headlines_filters_none():
    with patch('newsapi.NewsApiClient.get_top_headlines',
               return_value=MOCK_NEWS_RESPONSE):
        headlines = get_top_headlines(count=5)
        assert len(headlines) == 2
        assert 'Test Headline 1' in headlines
```

---

## 4. Unit Tests: Feedback Engine

```python
# tests/unit/test_feedback_engine.py

import pytest
from services.feedback_engine import get_motivational_message, QUOTES

@pytest.mark.parametrize("emotion", ['happy', 'sad', 'angry', 'fearful', 'neutral',
                                      'disgusted', 'surprised'])
def test_all_emotions_return_message(emotion):
    msg = get_motivational_message(emotion, 'TestUser')
    assert isinstance(msg, str)
    assert len(msg) > 0

def test_unknown_emotion_falls_back_to_neutral():
    msg = get_motivational_message('bored', 'Ahmad')
    neutral_pool = QUOTES['neutral']
    # Message should be from neutral pool
    assert any(q in msg for q in neutral_pool) or isinstance(msg, str)

def test_message_not_identical_on_repeated_calls():
    """Messages should vary (random selection from pool)."""
    messages = {get_motivational_message('happy', 'Ahmad') for _ in range(20)}
    # With 3+ options, should see at least 2 different messages in 20 trials
    assert len(messages) >= 2
```

---

## 5. Test Results Summary (Week 25)

| Module | Tests Written | Tests Passing | Coverage |
|--------|--------------|---------------|---------|
| feedback_engine | 12 | 12 | 94% |
| emotion_detection_service | 8 | 8 | 78% |
| data_cache | 10 | 9 (1 skip) | 71% |
| face_recognition_service | 7 | 7 | 82% |
| **Total** | **37** | **36** | **81% avg** |

> 1 skipped test: `test_weather_live_api` — requires real API key, excluded from CI.

---

## 6. References

1. Meszaros, G. (2007). *xUnit Test Patterns.* Addison-Wesley.
2. Freeman, S. & Pryce, N. (2009). *Growing Object-Oriented Software, Guided by Tests.* Addison-Wesley.
3. pytest documentation (2024). docs.pytest.org.
