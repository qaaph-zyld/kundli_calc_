"""
System Integration Tests
PGF Protocol: TEST_001
Gate: GATE_4
Version: 1.0.0
"""

import pytest
import asyncio
import httpx
from datetime import datetime
from prometheus_client import CollectorRegistry
from app.main import app
from app.core.monitoring.monitor import MonitoringSystem, AlertLevel

# Create a test client
@pytest.fixture
def test_client():
    """Create a test client"""
    return httpx.AsyncClient(app=app, base_url="http://test")

@pytest.fixture
def monitoring_system():
    """Create a monitoring system with custom registry"""
    registry = CollectorRegistry()
    return MonitoringSystem(prometheus_port=8001, registry=registry)

@pytest.mark.asyncio
async def test_health_check(test_client):
    """Test health check endpoint"""
    response = await test_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_calculate_kundli(test_client):
    """Test kundli calculation endpoint"""
    test_data = {
        "date": "1990-01-01",
        "time": "12:00:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }
    
    response = await test_client.post("/api/v1/kundli/calculate", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "planets" in data
    assert "houses" in data
    assert "ascendant" in data

@pytest.mark.asyncio
async def test_pattern_detection(test_client):
    """Test pattern detection endpoint"""
    test_data = {
        "kundli_data": {
            "planets": [
                {"name": "Sun", "sign": "Capricorn", "degree": 15},
                {"name": "Moon", "sign": "Taurus", "degree": 25},
                {"name": "Mars", "sign": "Aries", "degree": 10}
            ]
        }
    }
    
    response = await test_client.post("/api/v1/kundli/patterns", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "patterns" in data
    assert isinstance(data["patterns"], list)

@pytest.mark.asyncio
async def test_correlation_analysis(test_client):
    """Test correlation analysis endpoint"""
    test_data = {
        "kundli_1": {
            "planets": [
                {"name": "Sun", "sign": "Capricorn", "degree": 15},
                {"name": "Moon", "sign": "Taurus", "degree": 25}
            ]
        },
        "kundli_2": {
            "planets": [
                {"name": "Sun", "sign": "Leo", "degree": 20},
                {"name": "Moon", "sign": "Cancer", "degree": 15}
            ]
        }
    }
    
    response = await test_client.post("/api/v1/kundli/correlate", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "compatibility_score" in data
    assert "aspects" in data

@pytest.mark.asyncio
async def test_validation_error(test_client):
    """Test validation error handling"""
    invalid_data = {
        "date": "invalid-date",
        "time": "invalid-time",
        "latitude": "invalid",
        "longitude": "invalid",
        "timezone": "invalid"
    }
    
    response = await test_client.post("/api/v1/kundli/calculate", json=invalid_data)
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_concurrent_requests(test_client):
    """Test handling of concurrent requests"""
    test_data = {
        "date": "1990-01-01",
        "time": "12:00:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }
    
    # Create multiple concurrent requests
    async def make_request():
        response = await test_client.post("/api/v1/kundli/calculate", json=test_data)
        assert response.status_code == 200
        return response
    
    # Run 5 concurrent requests
    tasks = [make_request() for _ in range(5)]
    responses = await asyncio.gather(*tasks)
    
    # Verify all responses
    for response in responses:
        data = response.json()
        assert "planets" in data
        assert "houses" in data
        assert "ascendant" in data

@pytest.mark.asyncio
async def test_monitoring_system(monitoring_system):
    """Test monitoring system functionality"""
    # Test alert creation
    alert = monitoring_system.create_alert(
        level=AlertLevel.ERROR,
        message="Test error",
        category="test"
    )
    assert alert is not None
    assert alert.level == AlertLevel.ERROR
    assert alert.message == "Test error"
    
    # Test metric tracking
    monitoring_system.track_request(
        endpoint="/api/v1/kundli/calculate",
        method="POST",
        duration=0.5
    )
    
    monitoring_system.track_calculation(
        calc_type="kundli",
        duration=0.3
    )
    
    # Test system metrics
    metrics = monitoring_system.get_system_metrics()
    assert "current" in metrics
    assert "history" in metrics
    
    # Test performance metrics
    perf_metrics = monitoring_system.get_performance_metrics("calculations")
    assert isinstance(perf_metrics, dict)
    
    # Test metric export
    exported = monitoring_system.export_metrics(format="json")
    assert isinstance(exported, str)

@pytest.mark.asyncio
async def test_error_handling(test_client):
    """Test error handling for various scenarios"""
    # Test 404 error
    response = await test_client.get("/nonexistent")
    assert response.status_code == 404
    
    # Test method not allowed
    response = await test_client.post("/api/v1/health")
    assert response.status_code == 405
    
    # Test internal server error simulation
    response = await test_client.get("/api/v1/health/simulate-error")
    assert response.status_code == 500

if __name__ == "__main__":
    pytest.main(["-v", __file__])
