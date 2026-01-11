"""
Pytest configuration and shared fixtures for LifeLine backend tests.

This file contains:
- Global pytest configuration
- Shared fixtures used across all tests
- Mock setup for database and external services
"""
import os
import sys
import pytest
import warnings

# Add backend to Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from app.main import app

# Suppress deprecation warnings for cleaner test output
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)


@pytest.fixture
def client():
    """
    FIXTURE: FastAPI Test Client
    
    This creates a test client that can make HTTP requests to the FastAPI app
    without running an actual server. It's used for testing API endpoints.
    
    Example usage in a test:
        def test_health(client):
            response = client.get("/health")
            assert response.status_code == 200
    """
    return TestClient(app)
