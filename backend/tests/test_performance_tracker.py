"""
Test Suite for Performance Metrics Tracker
PGF Protocol: MET_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime, timedelta
import time
from app.core.metrics.performance_tracker import (
    PerformanceTracker,
    MetricType,
    MetricUnit,
    MetricSeries,
    MetricValue,
    track_performance
)

@pytest.fixture
def tracker():
    return PerformanceTracker(
        retention_period=timedelta(hours=1)
    )

@pytest.mark.asyncio
async def test_metric_initialization(tracker):
    """Test metric initialization"""
    assert tracker.metrics
    assert "request_latency" in tracker.metrics
    assert "cpu_usage" in tracker.metrics
    assert "memory_usage" in tracker.metrics
    assert "error_rate" in tracker.metrics

@pytest.mark.asyncio
async def test_metric_tracking(tracker):
    """Test basic metric tracking"""
    tracker.track_metric(
        "request_latency",
        100.0,
        MetricUnit.MILLISECONDS,
        {"endpoint": "/api/v1/calculate"}
    )
    
    stats = tracker.get_metric_statistics("request_latency")
    assert stats["count"] == 1
    assert stats["avg"] == 100.0
    assert stats["unit"] == "ms"

@pytest.mark.asyncio
async def test_resource_monitoring(tracker):
    """Test resource monitoring"""
    # Wait for resource monitoring to collect some data
    await asyncio.sleep(2)
    
    cpu_stats = tracker.get_metric_statistics("cpu_usage")
    memory_stats = tracker.get_metric_statistics("memory_usage")
    
    assert cpu_stats["count"] > 0
    assert memory_stats["count"] > 0
    assert 0 <= cpu_stats["avg"] <= 100
    assert 0 <= memory_stats["avg"] <= 100

@pytest.mark.asyncio
async def test_metric_retention(tracker):
    """Test metric retention policy"""
    # Add metrics with different timestamps
    now = datetime.now()
    
    tracker.track_metric(
        "request_latency",
        100.0,
        MetricUnit.MILLISECONDS,
        {"timestamp": "old"}
    )
    tracker.metrics["request_latency"].values[-1].timestamp = (
        now - timedelta(hours=2)
    )
    
    tracker.track_metric(
        "request_latency",
        200.0,
        MetricUnit.MILLISECONDS,
        {"timestamp": "new"}
    )
    
    # Force retention check
    tracker._apply_retention("request_latency")
    
    stats = tracker.get_metric_statistics("request_latency")
    assert stats["count"] == 1
    assert stats["avg"] == 200.0

@pytest.mark.asyncio
async def test_metric_statistics(tracker):
    """Test metric statistics calculation"""
    # Add multiple values
    values = [100.0, 200.0, 300.0, 400.0, 500.0]
    for value in values:
        tracker.track_metric(
            "request_latency",
            value,
            MetricUnit.MILLISECONDS
        )
    
    stats = tracker.get_metric_statistics("request_latency")
    assert stats["count"] == 5
    assert stats["min"] == 100.0
    assert stats["max"] == 500.0
    assert stats["avg"] == 300.0
    assert stats["p95"] == 500.0

@pytest.mark.asyncio
async def test_custom_metric_series(tracker):
    """Test adding custom metric series"""
    tracker.add_metric_series(
        MetricSeries(
            metric_type=MetricType.CUSTOM,
            name="custom_metric",
            aggregation="sum"
        )
    )
    
    tracker.track_metric(
        "custom_metric",
        42.0,
        MetricUnit.CUSTOM,
        {"custom_tag": "test"}
    )
    
    stats = tracker.get_metric_statistics("custom_metric")
    assert stats["count"] == 1
    assert stats["avg"] == 42.0

@pytest.mark.asyncio
async def test_sla_compliance(tracker):
    """Test SLA compliance calculation"""
    # Add test data
    values = [90.0, 95.0, 100.0, 105.0, 110.0]
    for value in values:
        tracker.track_metric(
            "request_latency",
            value,
            MetricUnit.MILLISECONDS
        )
    
    sla_thresholds = {
        "request_latency": 100.0  # 100ms threshold
    }
    
    compliance = tracker.calculate_sla_compliance(sla_thresholds)
    assert "request_latency" in compliance
    assert compliance["request_latency"] == 60.0  # 3 out of 5 values are compliant

@pytest.mark.asyncio
async def test_metric_export(tracker):
    """Test metric export functionality"""
    tracker.track_metric(
        "request_latency",
        100.0,
        MetricUnit.MILLISECONDS
    )
    
    # Test JSON export
    json_export = tracker.export_metrics(format="json")
    assert isinstance(json_export, str)
    assert "request_latency" in json_export
    
    # Test dict export
    dict_export = tracker.export_metrics(format="dict")
    assert isinstance(dict_export, dict)
    assert "request_latency" in dict_export

@pytest.mark.asyncio
async def test_metric_reset(tracker):
    """Test metric reset functionality"""
    tracker.track_metric(
        "request_latency",
        100.0,
        MetricUnit.MILLISECONDS
    )
    
    assert tracker.get_metric_statistics("request_latency")["count"] > 0
    
    tracker.reset()
    assert tracker.get_metric_statistics("request_latency")["count"] == 0

@pytest.mark.asyncio
async def test_performance_decorator():
    """Test performance tracking decorator"""
    tracker = PerformanceTracker()
    
    class TestClass:
        def __init__(self):
            self._performance_tracker = tracker
        
        @track_performance("test_latency")
        async def async_test_method(self):
            await asyncio.sleep(0.1)
            return True
        
        @track_performance("test_latency")
        def sync_test_method(self):
            time.sleep(0.1)
            return True
    
    test_instance = TestClass()
    
    # Test async method
    result = await test_instance.async_test_method()
    assert result
    
    # Test sync method
    result = test_instance.sync_test_method()
    assert result
    
    stats = tracker.get_metric_statistics("test_latency")
    assert stats["count"] == 2
    assert stats["min"] >= 100  # At least 100ms

@pytest.mark.asyncio
async def test_error_tracking(tracker):
    """Test error tracking functionality"""
    class TestClass:
        def __init__(self):
            self._performance_tracker = tracker
        
        @track_performance("error_test")
        async def failing_method(self):
            raise ValueError("Test error")
    
    test_instance = TestClass()
    
    # Test error tracking
    with pytest.raises(ValueError):
        await test_instance.failing_method()
    
    error_stats = tracker.get_metric_statistics("error_rate")
    assert error_stats["count"] > 0

@pytest.mark.asyncio
async def test_concurrent_metric_tracking(tracker):
    """Test concurrent metric tracking"""
    async def track_metrics():
        for i in range(10):
            tracker.track_metric(
                "request_latency",
                float(i * 100),
                MetricUnit.MILLISECONDS
            )
            await asyncio.sleep(0.01)
    
    # Create multiple tracking tasks
    tasks = [track_metrics() for _ in range(5)]
    await asyncio.gather(*tasks)
    
    stats = tracker.get_metric_statistics("request_latency")
    assert stats["count"] == 50  # 5 tasks * 10 metrics each
