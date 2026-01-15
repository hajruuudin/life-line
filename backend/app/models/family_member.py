"""Family member DTOs."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class FamilyMemberCreate(BaseModel):
    """DTO for creating a family member."""
    name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    profession: Optional[str] = None
    health_notes: Optional[str] = None


class FamilyMemberUpdate(BaseModel):
    """DTO for updating a family member."""
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    profession: Optional[str] = None
    health_notes: Optional[str] = None


class FamilyMemberResponse(BaseModel):
    """DTO for family member response."""
    id: int
    user_id: int
    name: str
    date_of_birth: Optional[date]
    gender: Optional[str] = None
    profession: Optional[str] = None
    health_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

