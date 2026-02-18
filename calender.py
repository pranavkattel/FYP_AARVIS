from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from datetime import datetime, timedelta

# Scopes define the level of access
# Use 'readonly' for read-only access, or 'calendar' for full access
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Authenticate and return Google Calendar service."""
    creds = None
    
    # Token file stores user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def get_upcoming_events(max_results=10):
    """Get upcoming events from Google Calendar."""
    try:
        service = authenticate_google_calendar()
        
        # Get current time in RFC3339 format
        now = datetime.utcnow().isoformat() + 'Z'
        
        print(f'Getting the upcoming {max_results} events...')
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
            return []
        
        print('\nUpcoming events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{start} - {event['summary']}")
        
        return events
        
    except Exception as e:
        print(f"Error fetching calendar events: {e}")
        return []

def get_todays_events():
    """Get today's events from Google Calendar."""
    try:
        import socket
        # Set socket timeout to 10 seconds
        socket.setdefaulttimeout(10)
        
        service = authenticate_google_calendar()
        
        # Get today's local date range as timezone-aware datetimes.
        # Do not append 'Z' to local time because that would reinterpret
        # local midnight as UTC midnight and can shift the query window.
        now_local = datetime.now().astimezone()
        today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=today_start.isoformat(),
            timeMax=today_end.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Return without printing when called from API
        return events
        
    except socket.timeout:
        print("⚠️ Google Calendar connection timed out - check your internet")
        return []
    except Exception as e:
        print(f"Error fetching today's events: {e}")
        return []

def add_event(summary, start_time, end_time, description='', location=''):
    """
    Add a new event to Google Calendar.
    
    Args:
        summary (str): Event title/name
        start_time (datetime): Event start time
        end_time (datetime): Event end time
        description (str): Event description (optional)
        location (str): Event location (optional)
    
    Returns:
        dict: Created event details or None if failed
    """
    try:
        service = authenticate_google_calendar()
        
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Kathmandu',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Kathmandu',
            },
        }
        
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")
        return created_event
        
    except Exception as e:
        print(f"Error creating event: {e}")
        return None

def add_event_simple(title, date_str, time_str, duration_minutes=60, description=''):
    """
    Add an event with simple string inputs.
    
    Args:
        title (str): Event title
        date_str (str): Date in format 'YYYY-MM-DD' (e.g., '2025-12-25')
        time_str (str): Time in format 'HH:MM' (e.g., '14:30')
        duration_minutes (int): Event duration in minutes (default: 60)
        description (str): Event description (optional)
    
    Returns:
        dict: Created event details or None if failed
    """
    try:
        # Parse date and time
        date_time_str = f"{date_str} {time_str}"
        start_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        return add_event(title, start_time, end_time, description)
        
    except Exception as e:
        print(f"Error creating event: {e}")
        return None

if __name__ == '__main__':
    # Test the calendar connection
    print("Connecting to Google Calendar...")
    get_todays_events()
    print("\n" + "="*50 + "\n")
    get_upcoming_events(5)
    
    # Example: Add a test event
    #add_event_simple("Test Meeting", "2025-12-25", "14:35", 60, "This is a test event")
