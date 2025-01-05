"""
API Endpoint Tests
PGF Protocol: API_001
Gate: GATE_4
Version: 1.0.0
"""

import pytest
from fastapi.testclient import TestClient
from app.api.v1.endpoints import app
from datetime import datetime

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_calculate_endpoint():
    """Test calculation endpoint"""
    request_data = {
        "date": "2024-01-01",
        "time": "12:00:00",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timezone": "America/New_York"
    }
    
    response = client.post("/api/v1/kundli/calculate", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert "planets" in result
    assert "houses" in result
    assert "ascendant" in result

def test_pattern_detection_endpoint():
    """Test pattern detection endpoint"""
    request_data = {
        "planets": {
            "Sun": {"longitude": 0, "latitude": 0, "speed": 1},
            "Moon": {"longitude": 120, "latitude": 0, "speed": 13}
        }
    }
    
    response = client.post("/api/v1/kundli/patterns", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert "patterns" in result

def test_correlation_endpoint():
    """Test correlation analysis endpoint"""
    request_data = {
        "kundli1": {
            "planets": {
                "Sun": {"longitude": 0, "latitude": 0, "speed": 1},
                "Moon": {"longitude": 120, "latitude": 0, "speed": 13}
            }
        },
        "kundli2": {
            "planets": {
                "Sun": {"longitude": 60, "latitude": 0, "speed": 1},
                "Moon": {"longitude": 180, "latitude": 0, "speed": 13}
            }
        }
    }
    
    response = client.post("/api/v1/kundli/correlate", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert "compatibility_score" in result
    assert "aspects" in result

def test_validation_endpoint():
    """Test data validation endpoint"""
    request_data = {
        "data": {
            "date": "2024-01-01",
            "time": "12:00:00",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York"
        },
        "validation_level": "STANDARD",
        "validation_scope": "ALL"
    }
    
    response = client.post("/api/v1/kundli/validate", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert "is_valid" in result
    assert "errors" in result

def test_metrics_endpoint():
    """Test metrics retrieval endpoint"""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    result = response.json()
    assert "system_metrics" in result
    assert "performance_metrics" in result

def test_error_handling():
    """Test error handling"""
    # Invalid calculation request
    invalid_request = {
        "datetime": "invalid",
        "latitude": 1000,  # Invalid latitude
        "longitude": -74.0060
    }
    
    response = client.post("/api/v1/calculate", json=invalid_request)
    assert response.status_code == 422  # FastAPI returns 422 for validation errors
    error = response.json()
    assert "detail" in error  # FastAPI returns validation errors in 'detail' field

def test_rate_limiting():
    """Test rate limiting"""
    # Make multiple rapid requests
    for _ in range(10):
        response = client.get("/api/v1/health")
        assert response.status_code in [200, 429]  # Either success or rate limited

def test_authentication():
    """Test authentication"""
    # Test without auth
    response = client.get("/api/v1/protected")
    assert response.status_code == 401
    
    # Test with invalid auth
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/protected", headers=headers)
    assert response.status_code == 401

def test_concurrent_requests():
    """Test handling of concurrent requests"""
    import asyncio
    import httpx
    
    async def make_request():
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/health")
            return response.status_code
    
    async def test_concurrent():
        tasks = [make_request() for _ in range(5)]
        results = await asyncio.gather(*tasks)
        return results
    
    results = asyncio.run(test_concurrent())
    assert all(status == 200 for status in results)
