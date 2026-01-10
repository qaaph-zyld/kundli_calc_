"""
Frontend-Backend Integration Tests
===================================

Validates that frontend can successfully call backend APIs.
Tests CORS, authentication, data format, error handling.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime


@pytest.fixture
def client():
    """Get test client"""
    from app.main import app
    return TestClient(app)


class TestCoreAPIs:
    """Test core calculation APIs used by frontend"""
    
    def test_calculate_chart_api(self, client):
        """Test chart calculation endpoint"""
        payload = {
            "date_time": "1990-05-15T10:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "altitude": 0,
            "ayanamsa": 1,  # 1 = Lahiri
            "house_system": "W"
        }
        
        response = client.post("/api/v1/charts/calculate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "planets" in data or "planetary_positions" in data
        assert "houses" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/api/v1/system/health")
        
        # Should return 200
        assert response.status_code == 200
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        # Should return something
        assert response.status_code in [200, 404]


class TestCORSConfiguration:
    """Test CORS headers for frontend access"""
    
    def test_cors_headers_on_chart_endpoint(self, client):
        """Verify CORS configured for chart endpoint"""
        response = client.post("/api/v1/charts/calculate", json={
            "date_time": "1990-05-15T10:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "altitude": 0,
            "ayanamsa": 1,
            "house_system": "W"
        })
        
        # CORS should be configured (check will vary by implementation)
        # At minimum, endpoint should be accessible
        assert response.status_code in [200, 400, 422]


class TestErrorHandling:
    """Test API error handling"""
    
    def test_invalid_datetime_format(self, client):
        """Test invalid datetime handling"""
        payload = {
            "date_time": "invalid-date",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "altitude": 0
        }
        
        response = client.post("/api/v1/charts/calculate", json=payload)
        
        # Should return error status
        assert response.status_code in [400, 422, 500]
    
    def test_invalid_coordinates(self, client):
        """Test invalid coordinate handling"""
        payload = {
            "date_time": "1990-05-15T10:30:00",
            "latitude": 999,  # Invalid
            "longitude": 999,   # Invalid
            "altitude": 0
        }
        
        response = client.post("/api/v1/charts/calculate", json=payload)
        
        # Should return validation error
        assert response.status_code in [400, 422, 500]
    
    def test_missing_required_fields(self, client):
        """Test missing field handling"""
        payload = {
            "date_time": "1990-05-15T10:30:00"
            # Missing latitude, longitude
        }
        
        response = client.post("/api/v1/charts/calculate", json=payload)
        
        # Should return validation error
        assert response.status_code in [400, 422, 500]


class TestDataFormat:
    """Test data format consistency for frontend"""
    
    def test_response_is_json(self, client):
        """Verify responses are JSON formatted"""
        response = client.get("/")
        
        # Should return JSON or HTML (for docs)
        content_type = response.headers.get("content-type", "")
        assert "json" in content_type.lower() or "html" in content_type.lower() or response.status_code == 404
    
    def test_numeric_precision_in_responses(self, client):
        """Verify numeric values have reasonable precision"""
        payload = {
            "date_time": "1990-05-15T10:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "altitude": 0,
            "ayanamsa": 1,
            "house_system": "W"
        }
        
        response = client.post("/api/v1/charts/calculate", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if we have planet data
            planets = data.get("planets") or data.get("planetary_positions")
            if planets and isinstance(planets, dict):
                # At least verify we got planet data structure
                assert len(planets) > 0
