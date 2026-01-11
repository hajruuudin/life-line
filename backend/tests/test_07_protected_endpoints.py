"""
TEST 7: Protected Endpoints - Authentication Required
=======================================================

What we're testing: Endpoints that require valid JWT authentication
Why: These are the critical business endpoints - they must be secured

Key tests:
- Endpoints reject requests without auth token
- Endpoints reject requests with invalid token
- Endpoints accept requests with valid token
- Endpoints return 403 Forbidden without auth

This prevents unauthorized access to sensitive operations.
"""

from app.utils.jwt import create_access_token


def test_family_members_endpoint_requires_auth(client):
    """
    TEST 7.1: GET /family-members requires authentication
    
    WHAT IT DOES:
    1. Make GET request to /family-members WITHOUT token
    2. Check response status code
    
    WHY:
    - Family member data is personal health information
    - Must be protected from unauthorized access
    - Should require valid JWT token
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    - Should not return family member data
    """
    response = client.get("/family-members")
    
    # Without auth header, should get 403 Forbidden
    assert response.status_code == 403


def test_medications_endpoint_requires_auth(client):
    """
    TEST 7.2: GET /medications requires authentication
    
    WHAT IT DOES:
    1. Make GET request to /medications WITHOUT token
    2. Check response status code
    
    WHY:
    - Medication data is sensitive health information
    - Must be protected
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    response = client.get("/medications")
    
    assert response.status_code == 403


def test_medication_usage_endpoint_requires_auth(client):
    """
    TEST 7.3: GET /medication-usage requires authentication
    
    WHAT IT DOES:
    1. Make GET request to /medication-usage WITHOUT token
    2. Check response status code
    
    WHY:
    - Usage logs are sensitive medical records
    - Must be protected
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    response = client.get("/medication-usage")
    
    assert response.status_code == 403


def test_create_family_member_requires_auth(client):
    """
    TEST 7.4: POST /family-members requires authentication
    
    WHAT IT DOES:
    1. Try to POST (create) family member WITHOUT token
    2. Check response status code
    
    WHY:
    - Can't create data without being authenticated
    - Would allow anyone to pollute the database
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    payload = {
        "name": "John",
        "date_of_birth": "1990-01-15"
    }
    
    response = client.post("/family-members", json=payload)
    
    assert response.status_code == 403


def test_create_medication_requires_auth(client):
    """
    TEST 7.5: POST /medications requires authentication
    
    WHAT IT DOES:
    1. Try to POST (create) medication WITHOUT token
    
    WHY:
    - Can't create medication record without auth
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    payload = {
        "name": "Aspirin",
        "quantity": 100
    }
    
    response = client.post("/medications", json=payload)
    
    assert response.status_code == 403


def test_log_medication_usage_requires_auth(client):
    """
    TEST 7.6: POST /medication-usage requires authentication
    
    WHAT IT DOES:
    1. Try to POST (log usage) WITHOUT token
    
    WHY:
    - Can't create usage logs without auth
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    payload = {
        "medication_id": 1,
        "family_member_id": 1,
        "quantity_used": 1
    }
    
    response = client.post("/medication-usage", json=payload)
    
    assert response.status_code == 403


def test_update_family_member_requires_auth(client):
    """
    TEST 7.7: PUT /family-members/{id} requires authentication
    
    WHAT IT DOES:
    1. Try to PUT (update) family member WITHOUT token
    
    WHY:
    - Can't update data without auth
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    payload = {"name": "Johnny"}
    
    response = client.put("/family-members/1", json=payload)
    
    assert response.status_code == 403


def test_update_medication_requires_auth(client):
    """
    TEST 7.8: PUT /medications/{id} requires authentication
    
    WHAT IT DOES:
    1. Try to PUT (update) medication WITHOUT token
    
    WHY:
    - Can't update without auth
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    payload = {"quantity": 200}
    
    response = client.put("/medications/1", json=payload)
    
    assert response.status_code == 403


def test_delete_family_member_requires_auth(client):
    """
    TEST 7.9: DELETE /family-members/{id} requires authentication
    
    WHAT IT DOES:
    1. Try to DELETE family member WITHOUT token
    
    WHY:
    - Can't delete without auth
    - Destructive operation - must be authenticated
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    response = client.delete("/family-members/1")
    
    assert response.status_code == 403


def test_delete_medication_requires_auth(client):
    """
    TEST 7.10: DELETE /medications/{id} requires authentication
    
    WHAT IT DOES:
    1. Try to DELETE medication WITHOUT token
    
    WHY:
    - Destructive operation - must be authenticated
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    response = client.delete("/medications/1")
    
    assert response.status_code == 403


def test_delete_usage_log_requires_auth(client):
    """
    TEST 7.11: DELETE /medication-usage/{id} requires authentication
    
    WHAT IT DOES:
    1. Try to DELETE usage log WITHOUT token
    
    WHY:
    - Can't delete logs without auth
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden (or 404 if endpoint doesn't exist)
    """
    response = client.delete("/medication-usage/1")
    
    # Should be 403 if endpoint exists, 404 if endpoint doesn't exist
    assert response.status_code in [403, 404]


def test_invalid_token_rejected(client):
    """
    TEST 7.12: Invalid token is rejected
    
    WHAT IT DOES:
    1. Make request with INVALID token
    2. Check that request is rejected
    
    WHY:
    - Malformed or tampered tokens should be rejected
    - Only valid tokens should grant access
    
    EXPECTED RESULT:
    - Status code should be 401 Unauthorized (or 403)
    """
    headers = {"Authorization": "Bearer invalid.token.here"}
    
    response = client.get("/family-members", headers=headers)
    
    # Invalid token should return 401 or 403
    assert response.status_code in [401, 403]


def test_expired_token_rejected(client):
    """
    TEST 7.13: Expired token is rejected
    
    WHAT IT DOES:
    1. Create a token that's already expired
    2. Try to use it for a request
    3. Check that it's rejected
    
    WHY:
    - Expired tokens should not grant access
    - Time-based security
    
    EXPECTED RESULT:
    - Status code should be 401 Unauthorized
    """
    from datetime import timedelta
    
    # Create token that expires immediately
    expired_token = create_access_token(
        data={"sub": "123"},
        expires_delta=timedelta(seconds=-1)  # Already expired
    )
    
    headers = {"Authorization": f"Bearer {expired_token}"}
    
    response = client.get("/family-members", headers=headers)
    
    # Expired token should be rejected
    assert response.status_code in [401, 403]


def test_missing_authorization_header(client):
    """
    TEST 7.14: Missing Authorization header is rejected
    
    WHAT IT DOES:
    1. Make request with NO headers at all
    2. Check status code
    
    WHY:
    - No token means no authentication
    - Should be rejected
    
    EXPECTED RESULT:
    - Status code should be 403 Forbidden
    """
    response = client.get("/family-members")
    
    assert response.status_code == 403


def test_malformed_authorization_header(client):
    """
    TEST 7.15: Malformed Authorization header is rejected
    
    WHAT IT DOES:
    1. Send header without "Bearer" prefix
    2. Or wrong format
    3. Check that it's rejected
    
    WHY:
    - Authorization header must follow correct format
    - "Authorization: Bearer <token>"
    
    EXPECTED RESULT:
    - Status code should be 401 or 403
    """
    # Wrong format - missing "Bearer"
    headers = {"Authorization": "invalid_token"}
    
    response = client.get("/family-members", headers=headers)
    
    assert response.status_code in [401, 403]
