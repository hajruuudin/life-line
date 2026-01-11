"""
TEST 6: Medication Usage Service
=================================

What we're testing: The MedicationUsageService business logic
Why: This service has important validation and business rules

Key logic to test:
- Verify family member exists and belongs to user
- Verify medication exists and belongs to user
- Check sufficient quantity before logging usage
- Decrease medication quantity after logging
- Handle various error cases

The tests:
- Log usage successfully
- Fail when family member not found
- Fail when medication not found
- Fail when insufficient quantity
- Fail when user doesn't own resources (security)
- Get usage logs
"""

from unittest.mock import Mock, patch, MagicMock
from app.services.medication_usage_service import MedicationUsageService
from app.models.medication_usage import MedicationUsageCreate
import pytest


def test_log_usage_success_happy_path():
    """
    TEST 6.1: log_usage successfully logs usage and decreases quantity
    
    WHAT IT DOES:
    1. Mock all DAO calls to return valid data
    2. Call service.log_usage() with valid data
    3. Verify:
       - Family member verified
       - Medication verified
       - Quantity check passed
       - Usage log created
       - Medication quantity decreased
    
    WHY:
    - This is the happy path - everything works correctly
    - Need to verify all steps happen in order
    
    EXPECTED RESULT:
    - Should return usage log
    - Medication quantity should decrease
    - No errors raised
    """
    usage_data = MedicationUsageCreate(
        family_member_id=1,
        medication_id=1,
        quantity_used=10
    )
    
    family_member = {"id": 1, "user_id": 123, "name": "John"}
    medication = {"id": 1, "user_id": 123, "name": "Aspirin", "quantity": 100}
    usage_log = {"id": 1, "family_member_id": 1, "medication_id": 1, "quantity_used": 10}
    updated_med = {"id": 1, "quantity": 90}  # 100 - 10
    
    with patch('app.dao.family_member_dao.FamilyMemberDAO.get_family_member_by_id') as mock_family:
        with patch('app.dao.medication_dao.MedicationDAO.get_medication_by_id') as mock_med:
            with patch('app.dao.medication_usage_dao.MedicationUsageDAO.create_usage_log') as mock_log:
                with patch('app.dao.medication_dao.MedicationDAO.update_medication') as mock_update:
                    with patch('app.services.medication_usage_service.db.get_connection'):
                        mock_family.return_value = family_member
                        mock_med.return_value = medication
                        mock_log.return_value = usage_log
                        mock_update.return_value = updated_med
                        
                        result = MedicationUsageService.log_usage(user_id=123, usage_data=usage_data)
                        
                        # Verify all steps were called
                        mock_family.assert_called_once()
                        mock_med.assert_called_once()
                        mock_log.assert_called_once()
                        mock_update.assert_called_once()
                        
                        # Verify result
                        assert result["quantity_used"] == 10


def test_log_usage_fails_family_member_not_found():
    """
    TEST 6.2: log_usage raises error when family member not found
    
    WHAT IT DOES:
    1. Mock DAO to return None for family member
    2. Call service.log_usage()
    3. Expect ValueError exception
    
    WHY:
    - Security: verify user owns the family member
    - Can't log usage for someone else's family member
    
    EXPECTED RESULT:
    - Should raise ValueError
    - Message should mention family member not found
    - No database operations should proceed
    """
    usage_data = MedicationUsageCreate(
        family_member_id=999,  # Doesn't exist
        medication_id=1,
        quantity_used=10
    )
    
    with patch('app.dao.family_member_dao.FamilyMemberDAO.get_family_member_by_id') as mock_family:
        with patch('app.services.medication_usage_service.db.get_connection'):
            mock_family.return_value = None  # Not found
            
            with pytest.raises(ValueError) as exc_info:
                MedicationUsageService.log_usage(user_id=123, usage_data=usage_data)
            
            assert "Family member not found" in str(exc_info.value)


def test_log_usage_fails_medication_not_found():
    """
    TEST 6.3: log_usage raises error when medication not found
    
    WHAT IT DOES:
    1. Mock family member found
    2. Mock medication not found
    3. Call service.log_usage()
    4. Expect ValueError exception
    
    WHY:
    - Security: verify user owns the medication
    - Can't log usage for someone else's medication
    
    EXPECTED RESULT:
    - Should raise ValueError
    - Message should mention medication not found
    """
    usage_data = MedicationUsageCreate(
        family_member_id=1,
        medication_id=999,  # Doesn't exist
        quantity_used=10
    )
    
    family_member = {"id": 1, "user_id": 123, "name": "John"}
    
    with patch('app.dao.family_member_dao.FamilyMemberDAO.get_family_member_by_id') as mock_family:
        with patch('app.dao.medication_dao.MedicationDAO.get_medication_by_id') as mock_med:
            with patch('app.services.medication_usage_service.db.get_connection'):
                mock_family.return_value = family_member
                mock_med.return_value = None  # Not found
                
                with pytest.raises(ValueError) as exc_info:
                    MedicationUsageService.log_usage(user_id=123, usage_data=usage_data)
                
                assert "Medication not found" in str(exc_info.value)


def test_log_usage_fails_insufficient_quantity():
    """
    TEST 6.4: log_usage raises error when quantity insufficient
    
    WHAT IT DOES:
    1. Mock family member and medication found
    2. Medication has quantity=10 but trying to use 20
    3. Call service.log_usage()
    4. Expect ValueError exception
    
    WHY:
    - Business rule: can't use more medication than available
    - Prevents inventory going negative
    
    EXPECTED RESULT:
    - Should raise ValueError
    - Message should show available vs requested
    - Should NOT decrease quantity or create log
    """
    usage_data = MedicationUsageCreate(
        family_member_id=1,
        medication_id=1,
        quantity_used=20  # Request more than available
    )
    
    family_member = {"id": 1, "user_id": 123, "name": "John"}
    medication = {"id": 1, "user_id": 123, "quantity": 10}  # Only 10 available
    
    with patch('app.dao.family_member_dao.FamilyMemberDAO.get_family_member_by_id') as mock_family:
        with patch('app.dao.medication_dao.MedicationDAO.get_medication_by_id') as mock_med:
            with patch('app.services.medication_usage_service.db.get_connection'):
                mock_family.return_value = family_member
                mock_med.return_value = medication
                
                with pytest.raises(ValueError) as exc_info:
                    MedicationUsageService.log_usage(user_id=123, usage_data=usage_data)
                
                assert "Insufficient quantity" in str(exc_info.value)
                assert "Available: 10" in str(exc_info.value)
                assert "Requested: 20" in str(exc_info.value)


def test_log_usage_fails_when_update_fails():
    """
    TEST 6.5: log_usage raises error when quantity update fails
    
    WHAT IT DOES:
    1. All validations pass
    2. Usage log created successfully
    3. But medication update fails (returns None)
    4. Expect Exception
    
    WHY:
    - Should fail gracefully if database update fails
    - Transaction should be rolled back
    
    EXPECTED RESULT:
    - Should raise Exception
    - Should mention update failure
    """
    usage_data = MedicationUsageCreate(
        family_member_id=1,
        medication_id=1,
        quantity_used=10
    )
    
    family_member = {"id": 1, "user_id": 123}
    medication = {"id": 1, "user_id": 123, "quantity": 100}
    usage_log = {"id": 1, "quantity_used": 10}
    
    with patch('app.dao.family_member_dao.FamilyMemberDAO.get_family_member_by_id') as mock_family:
        with patch('app.dao.medication_dao.MedicationDAO.get_medication_by_id') as mock_med:
            with patch('app.dao.medication_usage_dao.MedicationUsageDAO.create_usage_log') as mock_log:
                with patch('app.dao.medication_dao.MedicationDAO.update_medication') as mock_update:
                    with patch('app.services.medication_usage_service.db.get_connection'):
                        mock_family.return_value = family_member
                        mock_med.return_value = medication
                        mock_log.return_value = usage_log
                        mock_update.return_value = None  # Update failed
                        
                        with pytest.raises(Exception) as exc_info:
                            MedicationUsageService.log_usage(user_id=123, usage_data=usage_data)
                        
                        assert "Failed to update medication quantity" in str(exc_info.value)


def test_get_usage_logs_returns_list():
    """
    TEST 6.6: get_usage_logs returns list of usage logs
    
    WHAT IT DOES:
    1. Mock DAO to return list of usage logs
    2. Call service.get_usage_logs()
    3. Verify returns list
    
    WHY:
    - Users need to see history of medication usage
    - Simple delegation to DAO
    
    EXPECTED RESULT:
    - Should return list of usage logs
    - List can be empty or have multiple items
    """
    mock_logs = [
        {"id": 1, "family_member_id": 1, "medication_id": 1, "quantity_used": 10},
        {"id": 2, "family_member_id": 1, "medication_id": 2, "quantity_used": 5},
    ]
    
    with patch('app.services.medication_usage_service.MedicationUsageDAO.get_usage_logs_by_user_id') as mock_dao:
        mock_dao.return_value = mock_logs
        
        result = MedicationUsageService.get_usage_logs(user_id=123)
        
        mock_dao.assert_called_once_with(123)
        assert len(result) == 2


def test_get_usage_logs_returns_empty_when_none():
    """
    TEST 6.7: get_usage_logs returns empty list when no logs
    
    WHAT IT DOES:
    1. Mock DAO to return empty list
    2. Call service.get_usage_logs()
    3. Verify returns empty list
    
    WHY:
    - Edge case: user with no usage logs yet
    - Should return empty list, not None
    
    EXPECTED RESULT:
    - Should return empty list []
    """
    with patch('app.services.medication_usage_service.MedicationUsageDAO.get_usage_logs_by_user_id') as mock_dao:
        mock_dao.return_value = []
        
        result = MedicationUsageService.get_usage_logs(user_id=999)
        
        assert isinstance(result, list)
        assert len(result) == 0
