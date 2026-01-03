"""Family members controller."""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.services.family_member_service import FamilyMemberService
from app.models.family_member import FamilyMemberCreate, FamilyMemberUpdate, FamilyMemberResponse
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=List[FamilyMemberResponse])
async def get_family_members(current_user: dict = Depends(get_current_user)):
    """Get all family members for the current user."""
    members = FamilyMemberService.get_family_members(current_user["id"])
    return members


@router.post("", response_model=FamilyMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_family_member(
    member_data: FamilyMemberCreate,
    current_user: dict = Depends(get_current_user),
):
    """Create a new family member."""
    member = FamilyMemberService.create_family_member(current_user["id"], member_data)
    return member


@router.get("/{member_id}", response_model=FamilyMemberResponse)
async def get_family_member(
    member_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Get a specific family member."""
    member = FamilyMemberService.get_family_member(current_user["id"], member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found",
        )
    return member


@router.put("/{member_id}", response_model=FamilyMemberResponse)
async def update_family_member(
    member_id: int,
    member_data: FamilyMemberUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update a family member."""
    member = FamilyMemberService.update_family_member(current_user["id"], member_id, member_data)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found",
        )
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_family_member(
    member_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Delete a family member."""
    success = FamilyMemberService.delete_family_member(current_user["id"], member_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found",
        )

