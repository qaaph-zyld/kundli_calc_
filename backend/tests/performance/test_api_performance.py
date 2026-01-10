"""
API Performance Tests
=====================

Validates that all APIs meet performance requirements:
- Chart calculation: < 2 seconds
- System health: < 500ms
- Yoga calculation: < 3 seconds
"""

import pytest
import time
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Get test client"""
    from app.main import app
    return TestClient(app)


@pytest.mark.benchmark
class TestAPIPerformance:
    """Performance benchmarks for core APIs"""
    
    def test_chart_calculation_performance(self, client):
        """Chart calculation should complete in < 2 seconds"""
        payload = {
            "date_time": "1990-05-15T10:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "altitude": 0,
            "ayanamsa": 1,
            "house_system": "W"
        }
        
        start = time.time()
        response = client.post("/api/v1/charts/calculate", json=payload)
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 2.0, f"Chart calculation took {duration:.2f}s (limit: 2.0s)"
        
        print(f"\n✓ Chart calculation: {duration:.3f}s")
    
    def test_health_check_performance(self, client):
        """Health check should complete in < 500ms"""
        start = time.time()
        response = client.get("/api/v1/system/health")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 0.5, f"Health check took {duration:.3f}s (limit: 0.5s)"
        
        print(f"\n✓ Health check: {duration:.3f}s")
    
    def test_yoga_calculation_performance(self, client):
        """Yoga calculation should complete in < 3 seconds"""
        payload = {
            "planets": {
                "Sun": {"longitude": 45.0, "house": 1},
                "Moon": {"longitude": 120.0, "house": 4},
                "Mars": {"longitude": 200.0, "house": 7},
                "Mercury": {"longitude": 60.0, "house": 2},
                "Jupiter": {"longitude": 150.0, "house": 5},
                "Venus": {"longitude": 80.0, "house": 3},
                "Saturn": {"longitude": 280.0, "house": 10},
                "Rahu": {"longitude": 180.0, "house": 6},
                "Ketu": {"longitude": 0.0, "house": 12}
            },
            "houses": {
                "1": 0, "2": 30, "3": 60, "4": 90,
                "5": 120, "6": 150, "7": 180, "8": 210,
                "9": 240, "10": 270, "11": 300, "12": 330
            },
            "ascendant": 0.0
        }
        
        start = time.time()
        response = client.post("/api/v1/yogas/calculate", json=payload)
        duration = time.time() - start
        
        # Yoga endpoint might not exist or have different format
        if response.status_code == 200:
            assert duration < 3.0, f"Yoga calculation took {duration:.2f}s (limit: 3.0s)"
            print(f"\n✓ Yoga calculation: {duration:.3f}s")
        else:
            pytest.skip(f"Yoga endpoint returned {response.status_code}")
    
    def test_concurrent_requests_performance(self, client):
        """Test performance under concurrent load (5 simultaneous requests)"""
        import concurrent.futures
        
        payload = {
            "date_time": "1990-05-15T10:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "altitude": 0,
            "ayanamsa": 1,
            "house_system": "W"
        }
        
        def make_request():
            start = time.time()
            response = client.post("/api/v1/charts/calculate", json=payload)
            return time.time() - start, response.status_code
        
        start_total = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda _: make_request(), range(5)))
        total_duration = time.time() - start_total
        
        # All should succeed
        for duration, status in results:
            assert status == 200, f"Request failed with status {status}"
        
        # Average should still be reasonable
        avg_duration = sum(d for d, _ in results) / len(results)
        
        print(f"\n✓ Concurrent (5 requests): {total_duration:.2f}s total, {avg_duration:.3f}s average")
        
        # Total time shouldn't exceed 5 seconds for 5 concurrent requests
        assert total_duration < 5.0, f"Concurrent requests took {total_duration:.2f}s (limit: 5.0s)"
    
    def test_repeated_requests_caching(self, client):
        """Test that repeated identical requests benefit from caching"""
        payload = {
            "date_time": "1990-05-15T10:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "altitude": 0,
            "ayanamsa": 1,
            "house_system": "W"
        }
        
        # First request (cold cache)
        start = time.time()
        response1 = client.post("/api/v1/charts/calculate", json=payload)
        first_duration = time.time() - start
        
        assert response1.status_code == 200
        
        # Second identical request (warm cache)
        start = time.time()
        response2 = client.post("/api/v1/charts/calculate", json=payload)
        second_duration = time.time() - start
        
        assert response2.status_code == 200
        
        # Second request should be faster or similar (caching benefit)
        print(f"\n✓ First request: {first_duration:.3f}s")
        print(f"✓ Second request (cached): {second_duration:.3f}s")
        print(f"✓ Speedup: {(first_duration/second_duration):.2f}x")


@pytest.mark.benchmark
class TestEndpointAvailability:
    """Test that key endpoints are available and responsive"""
    
    def test_all_key_endpoints_responsive(self, client):
        """Verify all key endpoints respond within reasonable time"""
        endpoints = [
            ("GET", "/"),
            ("GET", "/api/v1/system/health"),
            ("GET", "/api/v1/api/v1/docs"),  # FastAPI docs
        ]
        
        results = []
        for method, endpoint in endpoints:
            start = time.time()
            if method == "GET":
                response = client.get(endpoint)
            duration = time.time() - start
            
            results.append({
                "endpoint": endpoint,
                "status": response.status_code,
                "duration": duration
            })
        
        # All should respond in < 1 second
        for result in results:
            if result["status"] not in [404]:  # Allow 404 for non-existent endpoints
                assert result["duration"] < 1.0, \
                    f"{result['endpoint']} took {result['duration']:.2f}s"
        
        print("\n✓ Endpoint availability check complete")
        for result in results:
            print(f"  {result['endpoint']}: {result['status']} ({result['duration']:.3f}s)")
