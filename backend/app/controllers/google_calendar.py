"""Google Calendar controller."""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Any
from app.services.google_calendar_service import GoogleCalendarService
from app.utils.dependencies import get_current_user

router = APIRouter()


class CalendarEventCreate(BaseModel):
    """DTO for creating a calendar event."""
    summary: str
    start_time: datetime
    end_time: datetime
    description: str = ""


@router.get("/upcoming")
async def get_upcoming_events(
    current_user: dict = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get upcoming events from the LIFELINE calendar for the next 7 days.
    Returns events grouped by date, with a maximum of 3 events per day.
    """
    try:
        events = GoogleCalendarService.get_upcoming_events(
            user_id=current_user["id"],
            days=7,
            max_per_day=3,
        )
        return {"events": events, "message": "Events retrieved successfully"}
    except ValueError as e:
        # User hasn't granted calendar access
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Calendar access not granted. Please re-login and allow calendar access to use this feature.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching events: {str(e)}",
        )


@router.post("/events")
async def create_calendar_event(
    event_data: CalendarEventCreate,
    current_user: dict = Depends(get_current_user),
):
    """
    Create a calendar event.
    
    TODO: Future MCP integration - This will connect to MCP server for intelligent scheduling.
    TODO: Future N8N integration - Trigger N8N workflows for automated scheduling.
    """
    try:
        event = GoogleCalendarService.create_event(
            user_id=current_user["id"],
            summary=event_data.summary,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            description=event_data.description,
        )
        return {"event": event, "message": "Event created successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating event: {str(e)}",
        )

