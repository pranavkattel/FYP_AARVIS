# Continuous Testing Principles for Embedded AI Systems
**Week 24 | Phase 4: Continuous Testing**
**Date Range:** 3 – 7 March 2025**

---

## 1. Continuous Testing in Agile

Continuous Testing (CT) is the practice of executing automated tests as part of the software delivery pipeline to obtain immediate feedback on business risks associated with a software release.

### 1.1 Testing Pyramid for AMMS

```
                    ▲
                   /E\
                  / 2E\       E2E Tests (5%)
                 /─────\      – Full system tests
                /  INT  \     Integration Tests (25%)
               /─────────\    – Module interaction
              / UNIT TESTS \  Unit Tests (70%)
             /───────────────\ – Individual functions
```

| Level | Scope | Tools | Frequency |
|-------|-------|-------|-----------|
| Unit | Single function/class | pytest | Every commit |
| Integration | Module-to-module | pytest + mocks | Daily |
| System/Functional | End-to-end workflow | Manual + script | Per sprint |
| UAT | User validation | Human testers | End of sprint |

### 1.2 Why Continuous Testing for AMMS

| AMMS Risk | CT Mitigation |
|-----------|--------------|
| Face recognition breaks after model update | Automated regression tests with sample faces |
| Emotion detection latency drift | Performance assertions in test suite |
| Gmail API changes break integration | Mock-based tests decouple from live API |
| LLM output changes format unexpectedly | Response format validators |

---

## 2. AMMS Test Infrastructure

### 2.1 Tools

```bash
pip install pytest pytest-cov pytest-mock coverage
```

### 2.2 Directory Structure

```
tests/
├── unit/
│   ├── test_face_recognition.py
│   ├── test_emotion_detection.py
│   ├── test_feedback_engine.py
│   ├── test_gmail_service.py
│   └── test_data_cache.py
├── integration/
│   ├── test_auth_flow.py
│   ├── test_voice_command_pipeline.py
│   └── test_dashboard_api.py
├── fixtures/
│   ├── sample_face.jpg
│   ├── sample_encodings.pkl
│   └── mock_gmail_response.json
└── conftest.py
```

---

## 3. Sample Unit Tests

### 3.1 Face Recognition

```python
# tests/unit/test_face_recognition.py
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from services.face_recognition_service import FaceRecognitionService

@pytest.fixture
def fr_service():
    with patch('services.face_recognition_service.open'), \
         patch('pickle.load', return_value={'encodings': [], 'names': []}):
        return FaceRecognitionService()

def test_no_encodings_returns_none(fr_service):
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    name, conf = fr_service.identify(dummy_frame)
    assert name is None
    assert conf == 0.0

def test_enroll_requires_minimum_frames(fr_service):
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Only 2 frames provided (< 5 minimum)
    result = fr_service.enroll('TestUser', [dummy_frame, dummy_frame])
    assert result is False
```

### 3.2 Feedback Engine

```python
# tests/unit/test_feedback_engine.py
from services.feedback_engine import get_motivational_message

def test_happy_returns_positive_message():
    msg = get_motivational_message('happy', 'Ahmad')
    assert len(msg) > 0
    assert isinstance(msg, str)

def test_unknown_emotion_uses_neutral_pool():
    msg = get_motivational_message('confused', 'Siti')
    assert msg  # Should not raise, should return something

def test_name_personalisation():
    msg = get_motivational_message('happy', 'Ahmad')
    # Message should contain user's first name
    assert 'Ahmad' in msg or 'ahmad' in msg.lower()
```

---

## 4. Coverage Requirements

| Module | Target Coverage |
|--------|----------------|
| face_recognition_service | ≥ 80% |
| emotion_detection_service | ≥ 75% |
| feedback_engine | ≥ 90% |
| gmail_service | ≥ 70% |
| data_cache | ≥ 75% |

```bash
# Run with coverage
pytest tests/ --cov=services --cov-report=html
open htmlcov/index.html
```

---

## 5. CI/CD Pipeline (Local)

AMMS uses a simple `Makefile` as pseudo-pipeline on the Raspberry Pi:

```makefile
.PHONY: test lint check

test:
	pytest tests/ -v --tb=short

lint:
	flake8 services/ --max-line-length=100 --ignore=E501

check: lint test
	@echo "All checks passed."
```

---

## 6. Testing Challenges for AMMS

| Challenge | Mitigation Strategy |
|-----------|-------------------|
| Camera-dependent tests | Use pre-recorded sample frames in fixtures |
| LLM non-determinism | Test format/length constraints, not exact content |
| GPIO/hardware tests (RPi) | Abstract behind interfaces; mock in unit tests |
| Real API calls (Gmail, OWM) | Mock all external HTTP with `pytest-mock` |

---

## 7. References

1. Humble, J. & Farley, D. (2010). *Continuous Delivery.* Addison-Wesley.
2. Fowler, M. (2012). "TestPyramid." martinfowler.com.
3. Crispin, L. & Gregory, J. (2009). *Agile Testing.* Addison-Wesley.
4. Beizer, B. (1990). *Software Testing Techniques.* Thomson Computer Press.
