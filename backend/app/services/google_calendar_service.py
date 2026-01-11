"""Google Calendar service."""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from app.dao.google_credentials_dao import GoogleCredentialsDAO
from app.config import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)

LIFELINE_CALENDAR_NAME = "LIFELINE"


class GoogleCalendarService:
    """
    Google Calendar service.
    
    TODO: Future MCP (Model Context Protocol) integration:
    1. Connect to MCP server for calendar event creation
    2. Use MCP to intelligently schedule medication reminders
    3. Integrate with N8N workflows for automated scheduling
    4. Support recurring events for medication schedules
    """
    
    @staticmethod
    def get_credentials(user_id: int) -> Credentials:
        """Get Google credentials for a user."""
        creds_data = GoogleCredentialsDAO.get_credentials_by_user_id(user_id)
        if not creds_data:
            raise ValueError("Google credentials not found. Please authenticate first.")
        
        return Credentials(
            token=creds_data["access_token"],
            refresh_token=creds_data["refresh_token"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            scopes=[
                "https://www.googleapis.com/auth/calendar",
            ],
            expiry=creds_data["token_expiry"],
        )
    
    @staticmethod
    def _refresh_credentials_if_needed(credentials: Credentials, user_id: int) -> Credentials:
        """Refresh credentials if expired and update in database."""
        if credentials.expired:
            from google.auth.transport.requests import Request
            credentials.refresh(Request())
            GoogleCredentialsDAO.create_or_update_credentials(
                user_id=user_id,
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                token_expiry=credentials.expiry if credentials.expiry else datetime.now(timezone.utc),
            )
        return credentials
    
    @staticmethod
    def find_or_create_lifeline_calendar(user_id: int, credentials: Optional[Credentials] = None) -> str:
        """
        Find or create the LIFELINE calendar for the user.
        Returns the calendar ID.
        """
        if credentials is None:
            credentials = GoogleCalendarService.get_credentials(user_id)
        
        credentials = GoogleCalendarService._refresh_credentials_if_needed(credentials, user_id)
        service = build("calendar", "v3", credentials=credentials)
        
        # Search for existing LIFELINE calendar
        calendar_list = service.calendarList().list().execute()
        for calendar in calendar_list.get("items", []):
            if calendar.get("summary") == LIFELINE_CALENDAR_NAME:
                logger.info(f"Found existing LIFELINE calendar for user {user_id}: {calendar['id']}")
                return calendar["id"]
        
        # Create new LIFELINE calendar
        new_calendar = {
            "summary": LIFELINE_CALENDAR_NAME,
            "description": "Medical appointments and medication reminders managed by Life-Line app",
            "timeZone": "UTC",
        }
        created_calendar = service.calendars().insert(body=new_calendar).execute()
        logger.info(f"Created new LIFELINE calendar for user {user_id}: {created_calendar['id']}")
        return created_calendar["id"]
    
    @staticmethod
    def get_upcoming_events(user_id: int, days: int = 7, max_per_day: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get upcoming events from the LIFELINE calendar for the next N days.
        Returns a dict with date strings as keys and lists of events as values.
        Maximum of max_per_day events per day.
        """
        credentials = GoogleCalendarService.get_credentials(user_id)
        credentials = GoogleCalendarService._refresh_credentials_if_needed(credentials, user_id)
        service = build("calendar", "v3", credentials=credentials)
        
        # Find LIFELINE calendar
        lifeline_calendar_id = GoogleCalendarService.find_or_create_lifeline_calendar(user_id, credentials)
        
        # Calculate time range
        now = datetime.now(timezone.utc)
        time_min = now.isoformat()
        time_max = (now + timedelta(days=days)).isoformat()
        
        # Fetch events
        events_result = service.events().list(
            calendarId=lifeline_calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        
        events = events_result.get("items", [])
        
        # Group events by date, limiting to max_per_day
        events_by_date: Dict[str, List[Dict[str, Any]]] = {}
        for event in events:
            start = event.get("start", {})
            # Handle all-day events (date) vs timed events (dateTime)
            event_datetime_str = start.get("dateTime", start.get("date", ""))
            if not event_datetime_str:
                continue
            
            # Extract date part
            event_date = event_datetime_str[:10]  # YYYY-MM-DD
            
            if event_date not in events_by_date:
                events_by_date[event_date] = []
            
            if len(events_by_date[event_date]) < max_per_day:
                events_by_date[event_date].append({
                    "id": event.get("id"),
                    "summary": event.get("summary", "No title"),
                    "description": event.get("description", ""),
                    "start": start,
                    "end": event.get("end", {}),
                    "location": event.get("location", ""),
                    "htmlLink": event.get("htmlLink", ""),
                })
        
        return events_by_date
    
    @staticmethod
    def create_event(user_id: int, summary: str, start_time: datetime, end_time: datetime, description: str = "") -> Dict[str, Any]:
        """
        Create a calendar event in the LIFELINE calendar.
        
        Future integration will include:
        - MCP server connection for intelligent scheduling
        - N8N workflow triggers
        - Automated medication reminders
        """
        credentials = GoogleCalendarService.get_credentials(user_id)
        credentials = GoogleCalendarService._refresh_credentials_if_needed(credentials, user_id)
        
        service = build("calendar", "v3", credentials=credentials)
        
        # Get or create LIFELINE calendar
        lifeline_calendar_id = GoogleCalendarService.find_or_create_lifeline_calendar(user_id, credentials)
        
        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "UTC",
            },
        }
        
        created_event = service.events().insert(calendarId=lifeline_calendar_id, body=event).execute()
        return created_event

