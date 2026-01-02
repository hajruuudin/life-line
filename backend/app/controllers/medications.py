"""Medications controller."""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.services.medication_service import MedicationService
from app.models.medication import MedicationCreate, MedicationUpdate, MedicationResponse
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=List[MedicationResponse])
async def get_medications(current_user: dict = Depends(get_current_user)):
    """Get all medications for the current user."""
    medications = MedicationService.get_medications(current_user["id"])
    return medications


@router.post("", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_medication(
    medication_data: MedicationCreate,
    current_user: dict = Depends(get_current_user),
):
    """Create a new medication or update quantity if it exists."""
    medication = MedicationService.create_or_update_medication(current_user["id"], medication_data)
    return medication


@router.get("/{medication_id}", response_model=MedicationResponse)
async def get_medication(
    medication_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Get a specific medication."""
    medication = MedicationService.get_medication(current_user["id"], medication_id)
    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found",
        )
    return medication


@router.put("/{medication_id}", response_model=MedicationResponse)
async def update_medication(
    medication_id: int,
    medication_data: MedicationUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update a medication."""
    medication = MedicationService.update_medication(current_user["id"], medication_id, medication_data)
    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found",
        )
    return medication


@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medication(
    medication_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Delete a medication."""
    success = MedicationService.delete_medication(current_user["id"], medication_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found",
        )

