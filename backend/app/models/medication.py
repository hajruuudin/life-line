"""Medication DTOs."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class MedicationCreate(BaseModel):
    """DTO for creating/updating medication inventory."""
    name: str
    quantity: int
    expiration_date: Optional[date] = None


class MedicationUpdate(BaseModel):
    """DTO for updating medication."""
    name: Optional[str] = None
    quantity: Optional[int] = None
    expiration_date: Optional[date] = None


class MedicationResponse(BaseModel):
    """DTO for medication response."""
    id: int
    user_id: int
    name: str
    quantity: int
    expiration_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

