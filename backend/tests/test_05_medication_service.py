"""
TEST 5: Medication Service
===========================

What we're testing: The MedicationService business logic
Why: This service has interesting logic - create_or_update checks if med exists

Key logic to test:
- If medication exists → increment quantity
- If medication doesn't exist → create new one
- This demonstrates conditional business logic

The tests:
- Create new medication
- Update existing medication (increment quantity)
- Get all medications
- Get specific medication
- Update medication
- Delete medication
"""

from unittest.mock import Mock, patch, MagicMock
from app.services.medication_service import MedicationService
from app.models.medication import MedicationCreate, MedicationUpdate


def test_create_new_medication_when_not_exists():
    """
    TEST 5.1: create_or_update creates new med when it doesn't exist
    
    WHAT IT DOES:
    1. Mock get_medication_by_name to return None (doesn't exist)
    2. Mock create_medication to return new med
    3. Call service.create_or_update_medication()
    4. Verify create_medication was called (not increment)
    
    WHY:
    - Service has conditional logic - need to test both paths
    - This path: medication doesn't exist, so CREATE it
    
    EXPECTED RESULT:
    - create_medication should be called
    - increment_medication_quantity should NOT be called
    - Should return newly created medication
    """
    med_data = MedicationCreate(name="Aspirin", quantity=100, expiration_date="2025-12-31")
    mock_new_med = {"id": 1, "user_id": 123, "name": "Aspirin", "quantity": 100}
    
    with patch('app.services.medication_service.MedicationDAO.get_medication_by_name') as mock_get:
        with patch('app.services.medication_service.MedicationDAO.create_medication') as mock_create:
            with patch('app.services.medication_service.db.get_connection'):
                mock_get.return_value = None  # Medication doesn't exist
                mock_create.return_value = mock_new_med
                
                result = MedicationService.create_or_update_medication(user_id=123, medication_data=med_data)
                
                # Verify create was called, not increment
                mock_create.assert_called_once()
                assert result["name"] == "Aspirin"


def test_update_existing_medication_increments_quantity():
    """
    TEST 5.2: create_or_update increments quantity if med exists
    
    WHAT IT DOES:
    1. Mock get_medication_by_name to return existing med
    2. Mock increment_medication_quantity to return updated med
    3. Call service.create_or_update_medication()
    4. Verify increment_medication_quantity was called (not create)
    
    WHY:
    - This tests the OTHER path - when medication ALREADY exists
    - Instead of creating new, we increment the quantity
    - This is smart inventory logic - don't create duplicates
    
    EXPECTED RESULT:
    - increment_medication_quantity should be called
    - create_medication should NOT be called
    - Should return medication with increased quantity
    """
    med_data = MedicationCreate(name="Aspirin", quantity=50, expiration_date="2025-12-31")
    existing_med = {"id": 1, "user_id": 123, "name": "Aspirin", "quantity": 100}
    updated_med = {"id": 1, "user_id": 123, "name": "Aspirin", "quantity": 150}
    
    with patch('app.services.medication_service.MedicationDAO.get_medication_by_name') as mock_get:
        with patch('app.services.medication_service.MedicationDAO.increment_medication_quantity') as mock_increment:
            with patch('app.services.medication_service.db.get_connection'):
                mock_get.return_value = existing_med  # Medication EXISTS
                mock_increment.return_value = updated_med
                
                result = MedicationService.create_or_update_medication(user_id=123, medication_data=med_data)
                
                # Verify increment was called
                mock_increment.assert_called_once()
                # Verify the quantity increased
                assert result["quantity"] == 150


def test_get_medications_returns_list():
    """
    TEST 5.3: get_medications returns list of all user's medications
    
    WHAT IT DOES:
    1. Mock DAO to return list of medications
    2. Call service.get_medications()
    3. Verify DAO called with correct user_id
    4. Verify returns list
    
    WHY:
    - Users need to view all their medications
    - Simple delegation to DAO
    
    EXPECTED RESULT:
    - Should return list of medications
    - List can be empty or have multiple items
    """
    mock_meds = [
        {"id": 1, "user_id": 123, "name": "Aspirin", "quantity": 100},
        {"id": 2, "user_id": 123, "name": "Ibuprofen", "quantity": 50},
    ]
    
    with patch('app.services.medication_service.MedicationDAO.get_medications_by_user_id') as mock_dao:
        mock_dao.return_value = mock_meds
        
        result = MedicationService.get_medications(user_id=123)
        
        mock_dao.assert_called_once_with(123)
        assert len(result) == 2
        assert result[0]["name"] == "Aspirin"


def test_get_medications_returns_empty_list_when_none():
    """
    TEST 5.4: get_medications returns empty list when user has no medications
    
    WHAT IT DOES:
    1. Mock DAO to return empty list
    2. Call service.get_medications()
    3. Verify returns empty list (not None)
    
    WHY:
    - Edge case: new user with no medications yet
    - Should return empty list, not crash
    
    EXPECTED RESULT:
    - Should return empty list []
    - Should not return None
    """
    with patch('app.services.medication_service.MedicationDAO.get_medications_by_user_id') as mock_dao:
        mock_dao.return_value = []
        
        result = MedicationService.get_medications(user_id=999)
        
        assert isinstance(result, list)
        assert len(result) == 0


def test_get_medication_returns_specific_med():
    """
    TEST 5.5: get_medication returns specific medication by ID
    
    WHAT IT DOES:
    1. Mock DAO to return specific med
    2. Call service.get_medication() with med_id
    3. Verify DAO called with med_id AND user_id (security)
    4. Verify returns the medication
    
    WHY:
    - Users need to view details of one medication
    - DAO checks both med_id and user_id (security - verify ownership)
    
    EXPECTED RESULT:
    - Should return one medication dict
    - Should have all medication fields
    """
    mock_med = {"id": 1, "user_id": 123, "name": "Aspirin", "quantity": 100}
    
    with patch('app.services.medication_service.MedicationDAO.get_medication_by_id') as mock_dao:
        mock_dao.return_value = mock_med
        
        result = MedicationService.get_medication(user_id=123, medication_id=1)
        
        # Verify DAO called with both IDs for security
        mock_dao.assert_called_once_with(1, 123)
        assert result["id"] == 1
        assert result["name"] == "Aspirin"


def test_update_medication_calls_dao():
    """
    TEST 5.6: update_medication updates med via DAO
    
    WHAT IT DOES:
    1. Create update data with new values
    2. Mock DAO.update_medication
    3. Call service.update_medication()
    4. Verify DAO called with all parameters
    
    WHY:
    - Users need to update medication details
    - Service passes update data to DAO
    
    EXPECTED RESULT:
    - DAO should be called with correct parameters
    - Should return updated medication
    """
    update_data = MedicationUpdate(name="Aspirin Extra", quantity=150, expiration_date="2026-12-31")
    updated_med = {"id": 1, "user_id": 123, "name": "Aspirin Extra", "quantity": 150}
    
    with patch('app.services.medication_service.MedicationDAO.update_medication') as mock_dao:
        mock_dao.return_value = updated_med
        
        result = MedicationService.update_medication(user_id=123, medication_id=1, medication_data=update_data)
        
        mock_dao.assert_called_once()
        assert result["name"] == "Aspirin Extra"


def test_delete_medication_calls_dao():
    """
    TEST 5.7: delete_medication deletes via DAO
    
    WHAT IT DOES:
    1. Mock DAO.delete_medication to return True
    2. Call service.delete_medication()
    3. Verify DAO called with med_id and user_id
    4. Verify returns True
    
    WHY:
    - Users need to remove medications
    - Service delegates deletion to DAO
    
    EXPECTED RESULT:
    - DAO called with med_id and user_id
    - Should return True (success)
    """
    with patch('app.services.medication_service.MedicationDAO.delete_medication') as mock_dao:
        mock_dao.return_value = True
        
        result = MedicationService.delete_medication(user_id=123, medication_id=1)
        
        mock_dao.assert_called_once_with(1, 123)
        assert result is True


def test_delete_medication_handles_not_found():
    """
    TEST 5.8: delete_medication returns False when med not found
    
    WHAT IT DOES:
    1. Mock DAO.delete_medication to return False
    2. Call service.delete_medication()
    3. Verify returns False
    
    WHY:
    - Edge case: med might not exist or already deleted
    - Should handle gracefully
    
    EXPECTED RESULT:
    - Should return False
    - No exception thrown
    """
    with patch('app.services.medication_service.MedicationDAO.delete_medication') as mock_dao:
        mock_dao.return_value = False
        
        result = MedicationService.delete_medication(user_id=123, medication_id=999)
        
        assert result is False
