"""Family member service."""
from typing import List, Dict, Any, Optional
from datetime import date
from app.dao.family_member_dao import FamilyMemberDAO
from app.models.family_member import FamilyMemberCreate, FamilyMemberUpdate, FamilyMemberResponse


class FamilyMemberService:
    """Business logic for family members."""
    
    @staticmethod
    def create_family_member(user_id: int, member_data: FamilyMemberCreate) -> Dict[str, Any]:
        """Create a new family member."""
        return FamilyMemberDAO.create_family_member(
            user_id=user_id,
            name=member_data.name,
            date_of_birth=member_data.date_of_birth,
            gender=member_data.gender,
            profession=member_data.profession,
            health_notes=member_data.health_notes,
        )
    
    @staticmethod
    def get_family_members(user_id: int) -> List[Dict[str, Any]]:
        """Get all family members for a user."""
        return FamilyMemberDAO.get_family_members_by_user_id(user_id)
    
    @staticmethod
    def get_family_member(user_id: int, member_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific family member."""
        return FamilyMemberDAO.get_family_member_by_id(member_id, user_id)
    
    @staticmethod
    def update_family_member(user_id: int, member_id: int, member_data: FamilyMemberUpdate) -> Optional[Dict[str, Any]]:
        """Update a family member."""
        return FamilyMemberDAO.update_family_member(
            family_member_id=member_id,
            user_id=user_id,
            name=member_data.name,
            date_of_birth=member_data.date_of_birth,
            gender=member_data.gender,
            profession=member_data.profession,
            health_notes=member_data.health_notes,
        )
    
    @staticmethod
    def delete_family_member(user_id: int, member_id: int) -> bool:
        """Delete a family member."""
        return FamilyMemberDAO.delete_family_member(member_id, user_id)

