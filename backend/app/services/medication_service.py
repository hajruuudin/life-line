"""Medication service."""
from typing import List, Dict, Any, Optional
from app.dao.medication_dao import MedicationDAO
from app.models.medication import MedicationCreate, MedicationUpdate
from app.database import db


class MedicationService:
    """Business logic for medications."""
    
    @staticmethod
    def create_or_update_medication(user_id: int, medication_data: MedicationCreate) -> Dict[str, Any]:
        """Create a new medication or update quantity if it exists in a single transaction."""
        with db.get_connection() as conn:
            # Check if medication with same name exists
            existing = MedicationDAO.get_medication_by_name(user_id, medication_data.name, connection=conn)
            
            if existing:
                # Update quantity (increment)
                return MedicationDAO.increment_medication_quantity(
                    medication_id=existing["id"],
                    user_id=user_id,
                    quantity_to_add=medication_data.quantity,
                    connection=conn,
                )
            else:
                # Create new medication
                return MedicationDAO.create_medication(
                    user_id=user_id,
                    name=medication_data.name,
                    quantity=medication_data.quantity,
                    expiration_date=medication_data.expiration_date,
                    connection=conn,
                )
    
    @staticmethod
    def get_medications(user_id: int) -> List[Dict[str, Any]]:
        """Get all medications for a user."""
        return MedicationDAO.get_medications_by_user_id(user_id)
    
    @staticmethod
    def get_medication(user_id: int, medication_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific medication."""
        return MedicationDAO.get_medication_by_id(medication_id, user_id)
    
    @staticmethod
    def update_medication(user_id: int, medication_id: int, medication_data: MedicationUpdate) -> Optional[Dict[str, Any]]:
        """Update a medication."""
        return MedicationDAO.update_medication(
            medication_id=medication_id,
            user_id=user_id,
            name=medication_data.name,
            quantity=medication_data.quantity,
            expiration_date=medication_data.expiration_date,
        )
    
    @staticmethod
    def delete_medication(user_id: int, medication_id: int) -> bool:
        """Delete a medication."""
        return MedicationDAO.delete_medication(medication_id, user_id)

