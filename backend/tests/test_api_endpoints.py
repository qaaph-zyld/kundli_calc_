"""
Test Suite for API Endpoints
PGF Protocol: API_001
Gate: GATE_4
Version: 1.0.0
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import json
from app.api.v1.endpoints import (
    router,
    CalculationRequest,
    PatternRequest,
    CorrelationRequest,
    ValidationRequest
)
from fastapi import FastAPI

# Create test app
app = FastAPI()
app.include_router(router)
client = TestClient(app)

# Test Data
sample_calculation_request = {
    "datetime": "2024-01-01T12:00:00Z",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York",
    "calculation_type": "natal",
    "ayanamsa": 23.5,
    "house_system": "placidus"
}

sample_pattern_request = {
    "data": {
        "planets": {
            "Sun": {
                "longitude": 0,
                "latitude": 0,
                "speed": 1
            },
            "Moon": {
                "longitude": 120,
                "latitude": 0,
                "speed": 13
            }
        }
    },
    "pattern_type": "planetary",
    "parameters": {
        "orb": 5
    }
}

sample_correlation_request = {
    "data_series": [
        {
            "timestamp": "2024-01-01T00:00:00Z",
            "value": 100
        },
        {
            "timestamp": "2024-01-02T00:00:00Z",
            "value": 200
        }
    ],
    "correlation_type": "temporal",
    "parameters": {
        "window_size": 24
    }
}

sample_validation_request = {
    "data": {
        "planets": {
            "Sun": {
                "longitude": 0,
                "latitude": 0,
                "speed": 1
            }
        }
    },
    "validation_level": "STANDARD",
    "validation_scope": "INPUT"
}

def test_calculate_chart():
    """Test chart calculation endpoint"""
    response = client.post(
        "/api/v1/calculate",
        json=sample_calculation_request
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "request_id" in data
    assert "planets" in data
    assert "houses" in data
    assert "aspects" in data
    assert "metadata" in data

def test_calculate_chart_validation():
    """Test chart calculation input validation"""
    # Invalid latitude
    invalid_request = {
        **sample_calculation_request,
        "latitude": 100  # Invalid latitude
    }
    response = client.post(
        "/api/v1/calculate",
        json=invalid_request
    )
    assert response.status_code == 400
    
    # Invalid datetime
    invalid_request = {
        **sample_calculation_request,
        "datetime": "invalid"
    }
    response = client.post(
        "/api/v1/calculate",
        json=invalid_request
    )
    assert response.status_code == 400

def test_detect_patterns():
    """Test pattern detection endpoint"""
    response = client.post(
        "/api/v1/detect-patterns",
        json=sample_pattern_request
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "patterns" in data
    assert "metadata" in data
    assert data["metadata"]["pattern_type"] == "planetary"

def test_analyze_correlations():
    """Test correlation analysis endpoint"""
    response = client.post(
        "/api/v1/analyze-correlations",
        json=sample_correlation_request
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "correlations" in data
    assert "metadata" in data
    assert data["metadata"]["correlation_type"] == "temporal"

def test_validate_data():
    """Test data validation endpoint"""
    response = client.post(
        "/api/v1/validate",
        json=sample_validation_request
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "is_valid" in data
    assert "results" in data
    assert "metadata" in data
    assert isinstance(data["is_valid"], bool)

def test_get_metrics():
    """Test metrics endpoint"""
    # Make some requests to generate metrics
    client.post("/api/v1/calculate", json=sample_calculation_request)
    client.post("/api/v1/detect-patterns", json=sample_pattern_request)
    
    # Get metrics
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    
    data = response.json()
    assert "metrics" in data
    assert "metadata" in data

def test_get_metrics_with_timerange():
    """Test metrics endpoint with time range"""
    start_time = datetime.now() - timedelta(hours=1)
    end_time = datetime.now()
    
    response = client.get(
        "/api/v1/metrics",
        params={
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "metrics" in data
    assert "metadata" in data
    assert data["metadata"]["start_time"]
    assert data["metadata"]["end_time"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_error_handling():
    """Test error handling"""
    # Test non-existent endpoint
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    
    # Test method not allowed
    response = client.get("/api/v1/calculate")
    assert response.status_code == 405
    
    # Test invalid JSON
    response = client.post(
        "/api/v1/calculate",
        data="invalid json"
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test concurrent request handling"""
    import asyncio
    import httpx
    
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        # Make multiple concurrent requests
        tasks = [
            ac.post(
                "/api/v1/calculate",
                json=sample_calculation_request
            )
            for _ in range(5)
        ]
        
        responses = await asyncio.gather(*tasks)
        assert all(r.status_code == 200 for r in responses)

def test_request_tracking():
    """Test request tracking middleware"""
    # Make a request
    response = client.post(
        "/api/v1/calculate",
        json=sample_calculation_request
    )
    assert response.status_code == 200
    
    # Check metrics
    metrics_response = client.get("/api/v1/metrics")
    metrics_data = metrics_response.json()
    
    assert "request_latency" in str(metrics_data)
    assert "calculations_per_second" in str(metrics_data)

def test_validation_levels():
    """Test different validation levels"""
    levels = ["STRICT", "STANDARD", "RELAXED"]
    
    for level in levels:
        request = {
            **sample_validation_request,
            "validation_level": level
        }
        
        response = client.post(
            "/api/v1/validate",
            json=request
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["metadata"]["validation_level"] == level

def test_large_request_handling():
    """Test handling of large requests"""
    # Create a large request
    large_request = {
        **sample_calculation_request,
        "planets": {
            f"Planet_{i}": {
                "longitude": i,
                "latitude": 0,
                "speed": 1
            }
            for i in range(100)
        }
    }
    
    response = client.post(
        "/api/v1/calculate",
        json=large_request
    )
    assert response.status_code == 200
