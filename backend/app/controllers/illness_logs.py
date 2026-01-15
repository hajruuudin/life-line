"""Illness logs controller."""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.services.illness_log_service import IllnessLogService
from app.models.illness_log import IllnessLogCreate, IllnessLogUpdate, IllnessLogResponse
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=List[IllnessLogResponse])
async def get_illness_logs(
    family_member_id: Optional[int] = Query(None, description="Filter by family member ID"),
    current_user: dict = Depends(get_current_user),
):
    """Get all illness logs for the current user, optionally filtered by family member."""
    logs = IllnessLogService.get_illness_logs(current_user["id"], family_member_id)
    return logs


@router.post("", response_model=IllnessLogResponse, status_code=status.HTTP_201_CREATED)
async def create_illness_log(
    log_data: IllnessLogCreate,
    current_user: dict = Depends(get_current_user),
):
    """Create a new illness log."""
    try:
        log = await IllnessLogService.create_illness_log(current_user["id"], log_data)
        return log
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{log_id}", response_model=IllnessLogResponse)
async def get_illness_log(
    log_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Get a specific illness log."""
    log = IllnessLogService.get_illness_log(current_user["id"], log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Illness log not found",
        )
    return log


@router.put("/{log_id}", response_model=IllnessLogResponse)
async def update_illness_log(
    log_id: int,
    log_data: IllnessLogUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update an illness log."""
    log = IllnessLogService.update_illness_log(current_user["id"], log_id, log_data)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Illness log not found",
        )
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_illness_log(
    log_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Delete an illness log."""
    success = IllnessLogService.delete_illness_log(current_user["id"], log_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Illness log not found",
        )
