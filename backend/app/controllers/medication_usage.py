"""Medication usage controller."""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.services.medication_usage_service import MedicationUsageService
from app.models.medication_usage import MedicationUsageCreate, MedicationUsageResponse
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=MedicationUsageResponse, status_code=status.HTTP_201_CREATED)
async def log_medication_usage(
    usage_data: MedicationUsageCreate,
    current_user: dict = Depends(get_current_user),
):
    """Log medication usage by a family member."""
    try:
        usage_log = MedicationUsageService.log_usage(current_user["id"], usage_data)
        return usage_log
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("", response_model=List[MedicationUsageResponse])
async def get_usage_logs(current_user: dict = Depends(get_current_user)):
    """Get all medication usage logs for the current user."""
    logs = MedicationUsageService.get_usage_logs(current_user["id"])
    return logs

