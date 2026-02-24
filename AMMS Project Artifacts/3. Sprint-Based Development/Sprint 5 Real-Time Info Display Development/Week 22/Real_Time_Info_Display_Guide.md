# Real-Time Information Display – API Integration Guide
**Sprint 5 | Week 22 | Phase 3: Sprint-Based Development**
**Sprint Goal:** Persistent real-time widget display (weather, news, calendar)
**Date Range:** 17 – 21 February 2025

---

## 1. Sprint 5 Scope

| Widget | Data Source | Update Interval |
|--------|------------|----------------|
| Clock & Date | System | Every second |
| Live Weather | OpenWeatherMap API | Every 10 minutes |
| 3-Day Forecast | OpenWeatherMap One Call | Every 10 minutes |
| Google Calendar Events | Google Calendar API | Every 5 minutes |
| Top News Headlines | NewsAPI.org | Every 30 minutes |
| Email/WhatsApp count | Gmail API (Sprint 4) | Every 3 minutes |

---

## 2. OpenWeatherMap API

### 2.1 Setup

```bash
pip install requests python-dotenv
# Register at openweathermap.org → get free API key (1000 calls/day limit)
```

### 2.2 Current Weather

```python
import requests
import os

OWM_KEY = os.getenv('OWM_API_KEY')
CITY = 'Kuala Lumpur,MY'

def get_current_weather() -> dict:
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': CITY, 'appid': OWM_KEY, 'units': 'metric'}
    r = requests.get(url, params=params, timeout=5)
    r.raise_for_status()
    data = r.json()
    return {
        'temp': round(data['main']['temp']),
        'feels_like': round(data['main']['feels_like']),
        'humidity': data['main']['humidity'],
        'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s to km/h
        'description': data['weather'][0]['description'].title(),
        'icon': data['weather'][0]['icon'],
        'city': data['name']
    }
```

### 2.3 3-Day Forecast (One Call API 3.0)

```python
LAT, LON = 3.1390, 101.6869  # Kuala Lumpur

def get_forecast() -> list:
    url = 'https://api.openweathermap.org/data/3.0/onecall'
    params = {
        'lat': LAT, 'lon': LON,
        'appid': OWM_KEY, 'units': 'metric',
        'exclude': 'minutely,hourly,alerts'
    }
    r = requests.get(url, params=params, timeout=5)
    data = r.json()
    forecast = []
    for day in data['daily'][:3]:
        forecast.append({
            'day': datetime.fromtimestamp(day['dt']).strftime('%a'),
            'max': round(day['temp']['max']),
            'min': round(day['temp']['min']),
            'icon': day['weather'][0]['icon'],
            'desc': day['weather'][0]['main']
        })
    return forecast
```

---

## 3. Google Calendar API

### 3.1 Authentication (reuses Gmail OAuth)

```python
from googleapiclient.discovery import build

CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    creds = get_google_credentials(CALENDAR_SCOPES)
    return build('calendar', 'v3', credentials=creds)
```

### 3.2 Fetch Today's Events

```python
from datetime import datetime, timezone

def get_todays_events(service, max_events=5) -> list:
    now = datetime.now(timezone.utc).isoformat()
    end_of_day = datetime.now(timezone.utc).replace(
        hour=23, minute=59, second=59).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end_of_day,
        maxResults=max_events,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    result = []
    for e in events:
        start = e['start'].get('dateTime', e['start'].get('date'))
        if 'T' in start:
            time_str = datetime.fromisoformat(start).strftime('%I:%M %p')
        else:
            time_str = 'All day'
        result.append({'time': time_str, 'title': e.get('summary', 'Untitled')})
    return result
```

---

## 4. NewsAPI Integration

```bash
pip install newsapi-python
# Register at newsapi.org → Developer plan (100 req/day free)
```

```python
from newsapi import NewsApiClient
import os

newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

def get_top_headlines(country='my', count=5) -> list:
    result = newsapi.get_top_headlines(country=country, page_size=count)
    articles = result.get('articles', [])
    return [a['title'] for a in articles if a.get('title')]
```

---

## 5. Real-Time Update Architecture

AMMS uses a **background refresh scheduler** with Flask + threading:

```python
import threading
import time

class DataCache:
    """Cached data refreshed in background threads."""
    weather = {}
    forecast = []
    events = []
    headlines = []
    email_count = 0

    def __init__(self):
        self._start_refresh_threads()

    def _start_refresh_threads(self):
        specs = [
            (self._refresh_weather, 600),     # 10 min
            (self._refresh_calendar, 300),    # 5 min
            (self._refresh_news, 1800),       # 30 min
            (self._refresh_email, 180),       # 3 min
        ]
        for func, interval in specs:
            t = threading.Thread(target=self._loop, args=(func, interval), daemon=True)
            t.start()

    def _loop(self, func, interval):
        while True:
            try:
                func()
            except Exception as e:
                logger.warning(f"Refresh error {func.__name__}: {e}")
            time.sleep(interval)

    def _refresh_weather(self):
        DataCache.weather = get_current_weather()
        DataCache.forecast = get_forecast()

    def _refresh_calendar(self):
        svc = get_calendar_service()
        DataCache.events = get_todays_events(svc)

    def _refresh_news(self):
        DataCache.headlines = get_top_headlines()

    def _refresh_email(self):
        svc = get_gmail_service()
        DataCache.email_count = get_dashboard_email_summary()
```

---

## 6. Dashboard API Endpoint (Flask)

```python
@app.route('/api/dashboard')
def api_dashboard():
    return jsonify({
        'time': datetime.now().strftime('%I:%M %p'),
        'date': datetime.now().strftime('%A, %d %B %Y'),
        'weather': DataCache.weather,
        'forecast': DataCache.forecast,
        'events': DataCache.events,
        'headlines': DataCache.headlines,
        'email': DataCache.email_count
    })
```

Browser polls this every 30 seconds via `setInterval`.

---

## 7. Sprint 5 Test Results

| Test | Expected | Actual | Status |
|------|---------|--------|--------|
| Weather widget loads | 26°C, KL shown | ✅ Correct | ✅ |
| Forecast shows 3 days | Mon/Tue/Wed tiles | ✅ Shown | ✅ |
| Calendar shows 5 events | 5 events | ✅ 4 events (only 4 today) | ✅ |
| News headlines (5) | 5 shown | ✅ 5 shown | ✅ |
| No API key → graceful | Shows "Unavailable" | ✅ Handled | ✅ |
| Widget refresh (10 min) | Background refresh | ✅ Confirmed | ✅ |

---

## 8. References

1. OpenWeatherMap (2024). *API Documentation v3.0.* openweathermap.org/api.
2. Google (2024). *Google Calendar API Python Quickstart.* developers.google.com/calendar.
3. NewsAPI.org (2024). *Developer Documentation.* newsapi.org/docs.
4. Atzori, L., Iera, A., & Morabito, G. (2010). "The Internet of Things: A survey." *Computer Networks*, 54(15).
