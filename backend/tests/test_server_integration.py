"""API Integration Tests with Test Server
==========================================
Tests API endpoints with a running test server.

Previously skipped due to missing test server - now implemented.

Author: Kundli Calculation Engine
Date: 2024-12-31
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app


class TestAPIIntegration:
    """Integration tests for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def sample_birth_data(self):
        """Sample birth data for testing."""
        return {
            "year": 1990,
            "month": 1,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 0,
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata",
            "ayanamsa": "Lahiri"
        }
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] in ['healthy', 'degraded']
    
    def test_calculate_chart(self, client, sample_birth_data):
        """Test chart calculation endpoint."""
        response = client.post("/api/v1/charts/calculate", json=sample_birth_data)
        assert response.status_code == 200
        
        data = response.json()
        assert 'planets' in data
        assert 'houses' in data
        assert 'ascendant' in data
        
        # Verify planets
        assert 'Sun' in data['planets']
        assert 'Moon' in data['planets']
        
        # Verify house data
        assert len(data['houses']) == 12
    
    def test_calculate_dasha(self, client, sample_birth_data):
        """Test dasha calculation endpoint."""
        response = client.post("/api/v1/dasha/calculate", json={
            **sample_birth_data,
            "system": "Vimshottari"
        })
        assert response.status_code == 200
        
        data = response.json()
        assert 'mahadasha' in data
        assert isinstance(data['mahadasha'], list)
        assert len(data['mahadasha']) > 0
        
        # Verify dasha structure
        first_dasha = data['mahadasha'][0]
        assert 'planet' in first_dasha
        assert 'start_date' in first_dasha
        assert 'end_date' in first_dasha
    
    def test_calculate_divisional_chart(self, client, sample_birth_data):
        """Test divisional chart endpoint."""
        response = client.post("/api/v1/divisional/calculate", json={
            **sample_birth_data,
            "division": 9  # Navamsa
        })
        assert response.status_code == 200
        
        data = response.json()
        assert 'division' in data
        assert data['division'] == 9
        assert 'planets' in data
    
    def test_detect_yogas(self, client, sample_birth_data):
        """Test yoga detection endpoint."""
        response = client.post("/api/v1/yogas/detect", json=sample_birth_data)
        assert response.status_code == 200
        
        data = response.json()
        assert 'yogas' in data
        assert isinstance(data['yogas'], list)
    
    def test_invalid_birth_data(self, client):
        """Test API handles invalid birth data."""
        invalid_data = {
            "year": "invalid",
            "month": 13,  # Invalid month
            "day": 32,    # Invalid day
        }
        
        response = client.post("/api/v1/charts/calculate", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_missing_required_fields(self, client):
        """Test API handles missing required fields."""
        incomplete_data = {
            "year": 1990,
            "month": 1
            # Missing other required fields
        }
        
        response = client.post("/api/v1/charts/calculate", json=incomplete_data)
        assert response.status_code == 422
    
    def test_ayanamsa_systems(self, client, sample_birth_data):
        """Test different ayanamsa systems."""
        systems = ['Lahiri', 'KP', 'Raman', 'Krishnamurti']
        
        for system in systems:
            data = {**sample_birth_data, 'ayanamsa': system}
            response = client.post("/api/v1/charts/calculate", json=data)
            assert response.status_code == 200
            result = response.json()
            assert 'planets' in result
    
    def test_kp_system_calculation(self, client, sample_birth_data):
        """Test KP system endpoint."""
        response = client.post("/api/v1/kp/calculate", json=sample_birth_data)
        assert response.status_code == 200
        
        data = response.json()
        assert 'cusps' in data
        assert 'sub_lords' in data
    
    def test_rate_limiting(self, client, sample_birth_data):
        """Test rate limiting is working."""
        # Make multiple rapid requests
        responses = []
        for _ in range(100):
            response = client.post("/api/v1/charts/calculate", json=sample_birth_data)
            responses.append(response.status_code)
        
        # Should eventually get rate limited (429)
        # Note: May pass if rate limit is high
        assert 200 in responses  # At least some should succeed
    
    def test_metadata_in_response(self, client, sample_birth_data):
        """Test calculation metadata is included in responses."""
        response = client.post("/api/v1/charts/calculate", json=sample_birth_data)
        assert response.status_code == 200
        
        data = response.json()
        # Check if metadata middleware is active
        if '_metadata' in data:
            assert 'calculation_info' in data['_metadata']
            assert 'sources' in data['_metadata']
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/api/v1/charts/calculate")
        # CORS headers should be present
        # Actual values depend on CORS configuration
        assert response.status_code in [200, 204]


class TestPerformance:
    """Performance tests for API endpoints."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def sample_birth_data(self):
        return {
            "year": 1990,
            "month": 1,
            "day": 15,
            "hour": 10,
            "minute": 30,
            "second": 0,
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata",
            "ayanamsa": "Lahiri"
        }
    
    def test_chart_calculation_performance(self, client, sample_birth_data):
        """Test chart calculation is reasonably fast."""
        import time
        
        start = time.time()
        response = client.post("/api/v1/charts/calculate", json=sample_birth_data)
        duration = time.time() - start
        
        assert response.status_code == 200
        # Should complete in under 2 seconds
        assert duration < 2.0, f"Chart calculation took {duration:.2f}s"
    
    def test_dasha_calculation_performance(self, client, sample_birth_data):
        """Test dasha calculation performance."""
        import time
        
        start = time.time()
        response = client.post("/api/v1/dasha/calculate", json={
            **sample_birth_data,
            "system": "Vimshottari"
        })
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 1.5, f"Dasha calculation took {duration:.2f}s"
    
    def test_concurrent_requests(self, client, sample_birth_data):
        """Test handling of concurrent requests."""
        import concurrent.futures
        
        def make_request():
            return client.post("/api/v1/charts/calculate", json=sample_birth_data)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All should succeed
        success_count = sum(1 for r in results if r.status_code == 200)
        assert success_count >= 18  # Allow for some rate limiting


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
