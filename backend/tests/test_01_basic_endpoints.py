"""
TEST 1: Basic Endpoint Testing
================================

What we're testing: The root endpoint (GET /)
Why: To verify the FastAPI app is working and can handle HTTP requests

The test:
- Makes a GET request to the root endpoint
- Checks the response status code is 200 (OK)
- Verifies the response contains expected data
"""

def test_root_endpoint_returns_success(client):
    """
    TEST 1.1: Root endpoint returns 200 OK
    
    WHAT IT DOES:
    1. Makes a GET request to "/" using the test client
    2. Checks that the response status code is 200 (success)
    
    WHY:
    - Verifies the app is running and responds to requests
    - Confirms basic HTTP communication works
    
    EXPECTED RESULT:
    - Response status code should be 200
    """
    response = client.get("/")
    assert response.status_code == 200


def test_root_endpoint_returns_message(client):
    """
    TEST 1.2: Root endpoint returns correct message
    
    WHAT IT DOES:
    1. Makes a GET request to "/"
    2. Parses the JSON response
    3. Verifies the response contains "message" key with "LifeLine API" value
    
    WHY:
    - Ensures the endpoint returns the expected JSON structure
    - Confirms data integrity
    
    EXPECTED RESULT:
    - JSON response should have {"message": "LifeLine API", ...}
    """
    response = client.get("/")
    data = response.json()
    
    # Check that "message" key exists in response
    assert "message" in data
    
    # Check that the message value is correct
    assert data["message"] == "LifeLine API"
