"""Medication usage DTOs."""
from pydantic import BaseModel
from datetime import datetime


class MedicationUsageCreate(BaseModel):
    """DTO for creating medication usage log."""
    family_member_id: int
    medication_id: int
    quantity_used: int = 1


class MedicationUsageResponse(BaseModel):
    """DTO for medication usage response."""
    id: int
    family_member_id: int
    medication_id: int
    used_at: datetime
    quantity_used: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

