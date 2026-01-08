"""Medication usage service."""
from typing import List, Dict, Any
from app.dao.medication_usage_dao import MedicationUsageDAO
from app.dao.medication_dao import MedicationDAO
from app.models.medication_usage import MedicationUsageCreate
from app.database import db


class MedicationUsageService:
    """Business logic for medication usage logs."""
    
    @staticmethod
    def log_usage(user_id: int, usage_data: MedicationUsageCreate) -> Dict[str, Any]:
        """Log medication usage and decrease inventory in a single transaction."""
        # Use a single transaction for all database operations
        with db.get_connection() as conn:
            # Verify that the family member belongs to the user
            from app.dao.family_member_dao import FamilyMemberDAO
            family_member = FamilyMemberDAO.get_family_member_by_id(usage_data.family_member_id, user_id, connection=conn)
            if not family_member:
                raise ValueError("Family member not found or does not belong to user")
            
            # Verify that the medication belongs to the user
            medication = MedicationDAO.get_medication_by_id(usage_data.medication_id, user_id, connection=conn)
            if not medication:
                raise ValueError("Medication not found or does not belong to user")
            
            # Check if quantity is sufficient
            if medication["quantity"] < usage_data.quantity_used:
                raise ValueError(f"Insufficient quantity. Available: {medication['quantity']}, Requested: {usage_data.quantity_used}")
            
            # Create usage log
            usage_log = MedicationUsageDAO.create_usage_log(
                family_member_id=usage_data.family_member_id,
                medication_id=usage_data.medication_id,
                quantity_used=usage_data.quantity_used,
                connection=conn,
            )
            
            # Decrease medication quantity
            updated_med = MedicationDAO.update_medication(
                medication_id=usage_data.medication_id,
                user_id=user_id,
                quantity=medication["quantity"] - usage_data.quantity_used,
                connection=conn,
            )
            
            if not updated_med:
                raise Exception("Failed to update medication quantity")
        
        return usage_log
    
    @staticmethod
    def get_usage_logs(user_id: int) -> List[Dict[str, Any]]:
        """Get all usage logs for a user."""
        return MedicationUsageDAO.get_usage_logs_by_user_id(user_id)

