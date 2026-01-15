"""Illness log DTOs."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class IllnessLogCreate(BaseModel):
    """DTO for creating an illness log."""
    family_member_id: int
    illness_name: str
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None
    ai_suggestion: Optional[str] = None


class IllnessLogUpdate(BaseModel):
    """DTO for updating an illness log."""
    illness_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None
    ai_suggestion: Optional[str] = None


class IllnessLogResponse(BaseModel):
    """DTO for illness log response."""
    id: int
    family_member_id: int
    family_member_name: Optional[str] = None
    illness_name: str
    start_date: date
    end_date: Optional[date]
    notes: Optional[str]
    ai_suggestion: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
