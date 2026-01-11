"""
TEST 4: Family Member Service
==============================

What we're testing: The FamilyMemberService business logic
Why: Services coordinate between controllers and DAOs - critical for business logic

Key concept: MOCKING
- We mock the DAO layer (database) so we don't need a real database
- We only test the Service layer logic
- This is called "unit testing" (test in isolation)

The tests:
- Create family member
- Get family members
- Get specific family member
- Update family member
- Delete family member
"""

from unittest.mock import Mock, patch, MagicMock
from app.services.family_member_service import FamilyMemberService
from app.models.family_member import FamilyMemberCreate, FamilyMemberUpdate


def test_create_family_member_calls_dao():
    """
    TEST 4.1: create_family_member calls FamilyMemberDAO
    
    WHAT IT DOES:
    1. Mock the FamilyMemberDAO.create_family_member method
    2. Call FamilyMemberService.create_family_member()
    3. Verify the DAO was called with correct parameters
    4. Verify the service returns what the DAO returned
    
    WHY:
    - Service delegates to DAO - we verify this delegation works
    - Mocking DAO means we don't need a database
    
    EXPECTED RESULT:
    - DAO's create_family_member should be called once
    - It should receive correct user_id, name, date_of_birth
    - Service should return what DAO returns
    """
    # Create mock data
    mock_result = {
        "id": 1,
        "user_id": 123,
        "name": "John",
        "date_of_birth": "1990-01-15"
    }
    
    # Create the Pydantic model for input
    member_data = FamilyMemberCreate(
        name="John",
        date_of_birth="1990-01-15"
    )
    
    # Mock the DAO method
    with patch('app.services.family_member_service.FamilyMemberDAO.create_family_member') as mock_dao:
        mock_dao.return_value = mock_result
        
        # Call the service
        result = FamilyMemberService.create_family_member(
            user_id=123,
            member_data=member_data
        )
        
        # Verify DAO was called
        mock_dao.assert_called_once()
        
        # Verify the result
        assert result == mock_result
        assert result["name"] == "John"
        assert result["user_id"] == 123


def test_get_family_members_calls_dao():
    """
    TEST 4.2: get_family_members retrieves from DAO
    
    WHAT IT DOES:
    1. Mock DAO.get_family_members_by_user_id
    2. Call FamilyMemberService.get_family_members()
    3. Verify DAO is called with correct user_id
    4. Verify returns list of family members
    
    WHY:
    - Services retrieve data through DAOs
    - Need to verify correct data flows through
    
    EXPECTED RESULT:
    - Should return a list of family members
    - DAO should be called with user_id
    """
    # Mock data - a list of family members
    mock_members = [
        {"id": 1, "user_id": 123, "name": "John", "date_of_birth": "1990-01-15"},
        {"id": 2, "user_id": 123, "name": "Jane", "date_of_birth": "1992-03-20"},
    ]
    
    with patch('app.services.family_member_service.FamilyMemberDAO.get_family_members_by_user_id') as mock_dao:
        mock_dao.return_value = mock_members
        
        # Call the service
        result = FamilyMemberService.get_family_members(user_id=123)
        
        # Verify DAO was called with correct user_id
        mock_dao.assert_called_once_with(123)
        
        # Verify result
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["name"] == "John"
        assert result[1]["name"] == "Jane"


def test_get_family_member_calls_dao():
    """
    TEST 4.3: get_family_member retrieves specific member
    
    WHAT IT DOES:
    1. Mock DAO.get_family_member_by_id
    2. Call FamilyMemberService.get_family_member()
    3. Verify DAO called with both member_id and user_id (security check)
    4. Verify returns single family member
    
    WHY:
    - Need to verify we're fetching the right member
    - Passing both user_id and member_id is a security measure
    
    EXPECTED RESULT:
    - Should return one family member dict
    - DAO should verify ownership (user_id check)
    """
    mock_member = {"id": 1, "user_id": 123, "name": "John", "date_of_birth": "1990-01-15"}
    
    with patch('app.services.family_member_service.FamilyMemberDAO.get_family_member_by_id') as mock_dao:
        mock_dao.return_value = mock_member
        
        result = FamilyMemberService.get_family_member(user_id=123, member_id=1)
        
        # Verify DAO was called with both IDs (security: verifies user owns this member)
        mock_dao.assert_called_once_with(1, 123)
        
        assert result["id"] == 1
        assert result["name"] == "John"


def test_update_family_member_calls_dao():
    """
    TEST 4.4: update_family_member updates in DAO
    
    WHAT IT DOES:
    1. Mock DAO.update_family_member
    2. Create update data with new name
    3. Call FamilyMemberService.update_family_member()
    4. Verify DAO called with correct parameters
    
    WHY:
    - Service must pass updates to DAO correctly
    - Need to verify the update parameters are passed through
    
    EXPECTED RESULT:
    - DAO should be called with member_id, user_id, and update data
    - Should return updated member
    """
    mock_updated = {"id": 1, "user_id": 123, "name": "Johnny", "date_of_birth": "1990-01-15"}
    
    update_data = FamilyMemberUpdate(name="Johnny", date_of_birth="1990-01-15")
    
    with patch('app.services.family_member_service.FamilyMemberDAO.update_family_member') as mock_dao:
        mock_dao.return_value = mock_updated
        
        result = FamilyMemberService.update_family_member(
            user_id=123,
            member_id=1,
            member_data=update_data
        )
        
        # Verify DAO was called
        mock_dao.assert_called_once()
        
        assert result["name"] == "Johnny"


def test_delete_family_member_calls_dao():
    """
    TEST 4.5: delete_family_member deletes via DAO
    
    WHAT IT DOES:
    1. Mock DAO.delete_family_member
    2. Call FamilyMemberService.delete_family_member()
    3. Verify DAO called with correct IDs
    4. Verify returns boolean success status
    
    WHY:
    - Service must delegate deletion to DAO
    - DAO performs the actual database deletion
    
    EXPECTED RESULT:
    - DAO called with member_id and user_id
    - Should return True (success) or False (failure)
    """
    with patch('app.services.family_member_service.FamilyMemberDAO.delete_family_member') as mock_dao:
        mock_dao.return_value = True  # Deletion successful
        
        result = FamilyMemberService.delete_family_member(user_id=123, member_id=1)
        
        # Verify DAO was called with correct parameters
        mock_dao.assert_called_once_with(1, 123)
        
        # Verify result
        assert result is True


def test_delete_family_member_handles_failure():
    """
    TEST 4.6: delete_family_member handles deletion failure
    
    WHAT IT DOES:
    1. Mock DAO.delete_family_member to return False
    2. Call FamilyMemberService.delete_family_member()
    3. Verify service returns False
    
    WHY:
    - DAO might fail (member not found, permission denied, etc)
    - Service should properly return failure status
    
    EXPECTED RESULT:
    - When DAO returns False, service should return False
    - No exception should be raised
    """
    with patch('app.services.family_member_service.FamilyMemberDAO.delete_family_member') as mock_dao:
        mock_dao.return_value = False  # Deletion failed
        
        result = FamilyMemberService.delete_family_member(user_id=123, member_id=999)
        
        assert result is False
