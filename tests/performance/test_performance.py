"""
Performance Test Suite
PGF Protocol: TEST_003
Gate: GATE_4
Version: 1.0.0
"""

import pytest
import asyncio
import time
from typing import Dict, Any, List
import statistics
from datetime import datetime, timedelta
import logging
from locust import HttpUser, task, between
from prometheus_client import CollectorRegistry, Counter, Histogram, push_to_gateway

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REGISTRY = CollectorRegistry()
REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    ['endpoint'],
    registry=REGISTRY
)
REQUEST_COUNT = Counter(
    'request_count_total',
    'Total request count',
    ['endpoint', 'status'],
    registry=REGISTRY
)

class PerformanceTest:
    """Base class for performance testing."""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
    
    async def measure_latency(self, coroutine) -> float:
        """Measure execution time of a coroutine."""
        start_time = time.perf_counter()
        await coroutine
        end_time = time.perf_counter()
        return end_time - start_time
    
    def analyze_results(self) -> Dict[str, float]:
        """Analyze test results."""
        latencies = [r["latency"] for r in self.results]
        return {
            "min": min(latencies),
            "max": max(latencies),
            "avg": statistics.mean(latencies),
            "median": statistics.median(latencies),
            "p95": statistics.quantiles(latencies, n=20)[18],  # 95th percentile
            "p99": statistics.quantiles(latencies, n=100)[98]  # 99th percentile
        }
    
    def record_metrics(self, endpoint: str, latency: float, status: str = "success"):
        """Record metrics to Prometheus."""
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        REQUEST_COUNT.labels(endpoint=endpoint, status=status).inc()

class KundliPerformanceTest(PerformanceTest):
    """Performance tests for Kundli calculation endpoints."""
    
    def __init__(self, client):
        super().__init__()
        self.client = client
    
    async def test_calculate_kundli(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Test Kundli calculation performance."""
        try:
            latency = await self.measure_latency(
                self.client.post("/api/v1/kundli/calculate", json=data)
            )
            
            result = {
                "endpoint": "/kundli/calculate",
                "timestamp": datetime.utcnow(),
                "latency": latency,
                "status": "success"
            }
            
            self.results.append(result)
            self.record_metrics("/kundli/calculate", latency)
            
            return result
        
        except Exception as e:
            logger.error(f"Error in calculate_kundli: {str(e)}")
            self.record_metrics("/kundli/calculate", 0, "error")
            return {
                "endpoint": "/kundli/calculate",
                "timestamp": datetime.utcnow(),
                "error": str(e),
                "status": "error"
            }
    
    async def test_batch_calculate(self, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Test batch calculation performance."""
        try:
            latency = await self.measure_latency(
                self.client.post("/api/v1/kundli/batch", json={"calculations": data_list})
            )
            
            result = {
                "endpoint": "/kundli/batch",
                "timestamp": datetime.utcnow(),
                "latency": latency,
                "batch_size": len(data_list),
                "status": "success"
            }
            
            self.results.append(result)
            self.record_metrics("/kundli/batch", latency)
            
            return result
        
        except Exception as e:
            logger.error(f"Error in batch_calculate: {str(e)}")
            self.record_metrics("/kundli/batch", 0, "error")
            return {
                "endpoint": "/kundli/batch",
                "timestamp": datetime.utcnow(),
                "error": str(e),
                "status": "error"
            }

# Pytest test cases
@pytest.mark.performance
class TestKundliPerformance:
    """Performance test cases."""
    
    @pytest.fixture
    def perf_test(self, test_client):
        """Initialize performance test instance."""
        return KundliPerformanceTest(test_client)
    
    async def test_single_calculation_performance(self, perf_test, test_kundli_data):
        """Test single calculation performance."""
        # Run 100 sequential requests
        for _ in range(100):
            result = await perf_test.test_calculate_kundli(test_kundli_data)
            assert result["status"] == "success"
        
        # Analyze results
        analysis = perf_test.analyze_results()
        
        # Assert performance requirements
        assert analysis["p95"] < 1.0  # 95th percentile under 1 second
        assert analysis["p99"] < 2.0  # 99th percentile under 2 seconds
    
    async def test_concurrent_calculation_performance(self, perf_test, test_kundli_data):
        """Test concurrent calculation performance."""
        # Run 50 concurrent requests
        tasks = [
            perf_test.test_calculate_kundli(test_kundli_data)
            for _ in range(50)
        ]
        
        results = await asyncio.gather(*tasks)
        success_count = sum(1 for r in results if r["status"] == "success")
        
        # Assert all requests successful
        assert success_count == 50
        
        # Analyze results
        analysis = perf_test.analyze_results()
        
        # Assert performance under load
        assert analysis["p95"] < 2.0  # 95th percentile under 2 seconds
        assert analysis["p99"] < 3.0  # 99th percentile under 3 seconds
    
    async def test_batch_calculation_performance(self, perf_test, test_kundli_data):
        """Test batch calculation performance."""
        # Create batch of 10 calculations
        batch_data = [test_kundli_data.copy() for _ in range(10)]
        
        # Run 10 batch requests
        for _ in range(10):
            result = await perf_test.test_batch_calculate(batch_data)
            assert result["status"] == "success"
        
        # Analyze results
        analysis = perf_test.analyze_results()
        
        # Assert batch performance
        assert analysis["p95"] < 5.0  # 95th percentile under 5 seconds
        assert analysis["avg"] < 3.0  # Average under 3 seconds

# Locust load testing
class KundliUser(HttpUser):
    """Locust user for load testing."""
    
    wait_time = between(1, 3)
    
    @task(3)
    def calculate_kundli(self):
        """Test Kundli calculation endpoint."""
        self.client.post("/api/v1/kundli/calculate", json={
            "date": "2025-01-05",
            "time": "06:22:27",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata"
        })
    
    @task(1)
    def batch_calculate(self):
        """Test batch calculation endpoint."""
        calculations = [
            {
                "date": "2025-01-05",
                "time": "06:22:27",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "timezone": "Asia/Kolkata"
            }
            for _ in range(5)
        ]
        
        self.client.post("/api/v1/kundli/batch", json={
            "calculations": calculations
        })

if __name__ == "__main__":
    # Run load test
    import os
    os.system("locust -f test_performance.py --headless -u 100 -r 10 --run-time 1h")
