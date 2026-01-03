"""Google Calendar service."""
from typing import Dict, Any
from datetime import datetime
from app.dao.google_credentials_dao import GoogleCredentialsDAO
from app.config import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


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
    def create_event(user_id: int, summary: str, start_time: datetime, end_time: datetime, description: str = "") -> Dict[str, Any]:
        """
        Create a calendar event.
        
        This is a placeholder implementation. Future integration will include:
        - MCP server connection for intelligent scheduling
        - N8N workflow triggers
        - Automated medication reminders
        """
        credentials = GoogleCalendarService.get_credentials(user_id)
        
        # Refresh token if expired
        if credentials.expired:
            from google.auth.transport.requests import Request
            credentials.refresh(Request())
            from datetime import timezone
            GoogleCredentialsDAO.create_or_update_credentials(
                user_id=user_id,
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                token_expiry=credentials.expiry if credentials.expiry else datetime.now(timezone.utc),
            )
        
        service = build("calendar", "v3", credentials=credentials)
        
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
        
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        return created_event

