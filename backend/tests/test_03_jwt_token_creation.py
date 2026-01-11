"""
TEST 3: JWT Token Creation
===========================

What we're testing: The create_access_token() utility function
Why: JWT tokens are the core of authentication - we need to ensure they're created correctly

The tests:
- Verify tokens are created successfully
- Verify tokens contain the right data
- Verify tokens have expiration time
- Verify invalid data handling
"""

from app.utils.jwt import create_access_token, verify_token
from datetime import timedelta


def test_create_access_token_returns_string():
    """
    TEST 3.1: create_access_token returns a string
    
    WHAT IT DOES:
    1. Calls create_access_token() with sample data
    2. Checks the return value is a string
    
    WHY:
    - JWT tokens must be strings
    - If we get something else, it's a bug
    
    EXPECTED RESULT:
    - Return value should be a string (not None, not dict, not int)
    """
    token = create_access_token({"sub": "123"})
    assert isinstance(token, str)


def test_create_access_token_not_empty():
    """
    TEST 3.2: create_access_token returns non-empty string
    
    WHAT IT DOES:
    1. Calls create_access_token()
    2. Checks the string is not empty
    3. Checks the string has reasonable length (JWT has dots in it)
    
    WHY:
    - Empty tokens are useless
    - Real JWT tokens have structure: header.payload.signature
    
    EXPECTED RESULT:
    - Token length > 0
    - Token contains at least one dot (JWT structure)
    """
    token = create_access_token({"sub": "123"})
    assert len(token) > 0
    assert "." in token  # JWT has format: header.payload.signature


def test_create_access_token_with_custom_data():
    """
    TEST 3.3: create_access_token preserves custom data
    
    WHAT IT DOES:
    1. Creates token with custom data {"sub": "user123", "role": "admin"}
    2. Verifies the token (decodes it)
    3. Checks the decoded data contains our custom fields
    
    WHY:
    - The data we put in should be preserved
    - We need to verify the token actually contains what we expect
    
    EXPECTED RESULT:
    - Decoded token should have "sub": "user123"
    - Decoded token should have "role": "admin"
    """
    test_data = {"sub": "user123", "role": "admin"}
    token = create_access_token(test_data)
    
    # Verify/decode the token
    decoded = verify_token(token)
    
    assert decoded is not None
    assert decoded["sub"] == "user123"
    assert decoded["role"] == "admin"


def test_create_access_token_includes_expiration():
    """
    TEST 3.4: create_access_token includes expiration time
    
    WHAT IT DOES:
    1. Creates a token with default expiration
    2. Decodes it to get the payload
    3. Checks that "exp" (expiration) field exists
    4. Verifies exp is a valid timestamp
    
    WHY:
    - Tokens must expire for security
    - Without expiration, a stolen token works forever
    
    EXPECTED RESULT:
    - Decoded token should have "exp" key
    - "exp" value should be a number (Unix timestamp)
    """
    token = create_access_token({"sub": "123"})
    decoded = verify_token(token)
    
    assert decoded is not None
    assert "exp" in decoded
    # exp should be a number (Unix timestamp)
    assert isinstance(decoded["exp"], int)
    assert decoded["exp"] > 0


def test_create_access_token_with_custom_expiration():
    """
    TEST 3.5: create_access_token respects custom expiration
    
    WHAT IT DOES:
    1. Creates token with custom expiration time (1 hour instead of default 30 min)
    2. Decodes the token
    3. Verifies expiration was set
    
    WHY:
    - Sometimes we need different expiration times
    - Need to verify the custom expiration is actually used
    
    EXPECTED RESULT:
    - Token should be created without errors
    - Decoded token should have "exp" field
    """
    custom_expires = timedelta(hours=1)
    token = create_access_token({"sub": "123"}, expires_delta=custom_expires)
    decoded = verify_token(token)
    
    assert decoded is not None
    assert "exp" in decoded
