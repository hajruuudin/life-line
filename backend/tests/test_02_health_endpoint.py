"""
TEST 2: Health Check Endpoint
==============================

What we're testing: The health check endpoint (GET /health)
Why: Health checks are crucial in production to verify the app is running

The tests:
- Verify the endpoint returns 200 (success)
- Verify the response contains status "healthy"
- This simulates what monitoring tools like Kubernetes do
"""

def test_health_endpoint_returns_success(client):
    """
    TEST 2.1: Health endpoint returns 200 OK
    
    WHAT IT DOES:
    1. Makes a GET request to "/health"
    2. Checks the response status code is 200
    
    WHY:
    - Monitoring systems use health checks to ensure app is up
    - If this fails, the app may be down or crashed
    
    EXPECTED RESULT:
    - Status code should be 200 (OK)
    """
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_returns_healthy_status(client):
    """
    TEST 2.2: Health endpoint returns correct status
    
    WHAT IT DOES:
    1. Makes a GET request to "/health"
    2. Parses the JSON response
    3. Verifies the response contains {"status": "healthy"}
    
    WHY:
    - Confirms the app is not just responding, but actually healthy
    - Allows detailed health monitoring
    
    EXPECTED RESULT:
    - JSON response should have {"status": "healthy"}
    """
    response = client.get("/health")
    data = response.json()
    
    # Check that "status" key exists
    assert "status" in data
    
    # Check that status is "healthy"
    assert data["status"] == "healthy"


def test_health_endpoint_response_is_json(client):
    """
    TEST 2.3: Health endpoint returns valid JSON
    
    WHAT IT DOES:
    1. Makes a GET request to "/health"
    2. Verifies the response can be parsed as JSON
    3. Checks the content-type header
    
    WHY:
    - Ensures we're returning the right format
    - Prevents returning HTML or plain text by mistake
    
    EXPECTED RESULT:
    - Response should be valid JSON
    - Content-Type header should contain "application/json"
    """
    response = client.get("/health")
    
    # response.json() will throw an error if not valid JSON
    # This is an implicit test that JSON parsing works
    data = response.json()
    assert isinstance(data, dict)
    
    # Check content type header
    assert "application/json" in response.headers.get("content-type", "")
