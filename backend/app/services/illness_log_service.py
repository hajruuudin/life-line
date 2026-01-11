"""Illness log service."""
from typing import List, Dict, Any, Optional
from app.dao.illness_log_dao import IllnessLogDAO
from app.dao.family_member_dao import FamilyMemberDAO
from app.models.illness_log import IllnessLogCreate, IllnessLogUpdate


class IllnessLogService:
    """Business logic for illness logs."""
    
    @staticmethod
    def create_illness_log(user_id: int, log_data: IllnessLogCreate) -> Dict[str, Any]:
        """Create a new illness log."""
        # Verify the family member belongs to the user
        family_member = FamilyMemberDAO.get_family_member_by_id(log_data.family_member_id, user_id)
        if not family_member:
            raise ValueError("Family member not found or does not belong to user")
        
        result = IllnessLogDAO.create_illness_log(
            family_member_id=log_data.family_member_id,
            illness_name=log_data.illness_name,
            start_date=log_data.start_date,
            end_date=log_data.end_date,
            notes=log_data.notes,
        )
        # Add family member name to response
        result["family_member_name"] = family_member["name"]
        return result
    
    @staticmethod
    def get_illness_logs(user_id: int, family_member_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all illness logs for a user, optionally filtered by family member."""
        return IllnessLogDAO.get_illness_logs_by_user_id(user_id, family_member_id)
    
    @staticmethod
    def get_illness_log(user_id: int, log_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific illness log."""
        return IllnessLogDAO.get_illness_log_by_id(log_id, user_id)
    
    @staticmethod
    def update_illness_log(user_id: int, log_id: int, log_data: IllnessLogUpdate) -> Optional[Dict[str, Any]]:
        """Update an illness log."""
        return IllnessLogDAO.update_illness_log(
            illness_log_id=log_id,
            user_id=user_id,
            illness_name=log_data.illness_name,
            start_date=log_data.start_date,
            end_date=log_data.end_date,
            notes=log_data.notes,
        )
    
    @staticmethod
    def delete_illness_log(user_id: int, log_id: int) -> bool:
        """Delete an illness log."""
        return IllnessLogDAO.delete_illness_log(log_id, user_id)
