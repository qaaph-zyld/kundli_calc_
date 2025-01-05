"""
Test Suite for Monitoring System
PGF Protocol: MON_001
Gate: GATE_4
Version: 1.0.0
"""

import pytest
from datetime import datetime, timedelta
import time
import json
from app.core.monitoring.monitor import (
    MonitoringSystem,
    Alert,
    AlertLevel,
    MetricCategory
)

@pytest.fixture
def monitor():
    """Create test monitoring system"""
    return MonitoringSystem(
        prometheus_port=8001,  # Use different port for tests
        alert_retention_days=1,
        metric_retention_hours=1
    )

def test_system_monitoring(monitor):
    """Test system monitoring"""
    # Wait for initial metrics
    time.sleep(2)
    
    metrics = monitor.get_system_metrics()
    assert "current" in metrics
    assert "history" in metrics
    
    current = metrics["current"]
    assert "cpu_percent" in current
    assert "memory_percent" in current
    assert "disk_percent" in current
    assert "timestamp" in current

def test_alert_creation(monitor):
    """Test alert creation and retrieval"""
    # Create test alert
    monitor.create_alert(
        AlertLevel.WARNING,
        "Test alert",
        "test",
        {"test_key": "test_value"}
    )
    
    # Get alerts
    alerts = monitor.get_alerts(level=AlertLevel.WARNING)
    assert len(alerts) > 0
    
    alert = alerts[0]
    assert alert.level == AlertLevel.WARNING
    assert alert.message == "Test alert"
    assert alert.category == "test"
    assert alert.metadata == {"test_key": "test_value"}
    assert not alert.acknowledged

def test_alert_filtering(monitor):
    """Test alert filtering"""
    # Create test alerts
    monitor.create_alert(
        AlertLevel.INFO,
        "Info alert",
        "test"
    )
    monitor.create_alert(
        AlertLevel.WARNING,
        "Warning alert",
        "test"
    )
    monitor.create_alert(
        AlertLevel.ERROR,
        "Error alert",
        "production"
    )
    
    # Test level filtering
    info_alerts = monitor.get_alerts(level=AlertLevel.INFO)
    assert len(info_alerts) == 1
    assert info_alerts[0].message == "Info alert"
    
    # Test category filtering
    prod_alerts = monitor.get_alerts(category="production")
    assert len(prod_alerts) == 1
    assert prod_alerts[0].message == "Error alert"

def test_alert_handlers(monitor):
    """Test alert handlers"""
    handled_alerts = []
    
    def test_handler(alert):
        handled_alerts.append(alert)
    
    # Register handler
    monitor.register_alert_handler(
        AlertLevel.CRITICAL,
        test_handler
    )
    
    # Create alert
    monitor.create_alert(
        AlertLevel.CRITICAL,
        "Critical alert",
        "test"
    )
    
    assert len(handled_alerts) == 1
    assert handled_alerts[0].level == AlertLevel.CRITICAL
    assert handled_alerts[0].message == "Critical alert"

def test_request_tracking(monitor):
    """Test request tracking"""
    # Track test request
    monitor.track_request(
        endpoint="/api/test",
        method="GET",
        duration=0.1
    )
    
    # Verify metrics
    metrics = monitor.export_metrics(format="dict")
    assert "performance_metrics" in metrics

def test_calculation_tracking(monitor):
    """Test calculation tracking"""
    # Track test calculation
    monitor.track_calculation(
        calc_type="natal",
        duration=0.5
    )
    
    # Verify metrics
    metrics = monitor.export_metrics(format="dict")
    assert "performance_metrics" in metrics

def test_error_tracking(monitor):
    """Test error tracking"""
    # Track test error
    monitor.track_error(
        error_type="validation",
        error_msg="Test error"
    )
    
    # Verify error alert
    alerts = monitor.get_alerts(level=AlertLevel.ERROR)
    assert len(alerts) > 0
    assert alerts[-1].message == "Test error"
    assert alerts[-1].metadata["error_type"] == "validation"

def test_metric_retention(monitor):
    """Test metric retention"""
    # Create old alert
    old_alert = Alert(
        level=AlertLevel.INFO,
        message="Old alert",
        timestamp=datetime.now() - timedelta(days=2),
        category="test"
    )
    monitor.alerts.append(old_alert)
    
    # Wait for cleanup
    time.sleep(2)
    
    # Verify old alert is removed
    alerts = monitor.get_alerts()
    assert old_alert not in alerts

def test_performance_metrics(monitor):
    """Test performance metrics calculation"""
    # Add test metrics
    test_metric = "test_metric"
    for i in range(5):
        monitor.metrics[test_metric].append({
            "value": i * 100,
            "timestamp": datetime.now()
        })
    
    # Get metrics
    metrics = monitor.get_performance_metrics(test_metric)
    assert metrics["count"] == 5
    assert metrics["min"] == 0
    assert metrics["max"] == 400
    assert metrics["avg"] == 200
    assert "p95" in metrics
    assert "p99" in metrics

def test_metric_export(monitor):
    """Test metric export"""
    # Create test data
    monitor.create_alert(
        AlertLevel.INFO,
        "Test alert",
        "test"
    )
    monitor.track_request(
        endpoint="/api/test",
        method="GET",
        duration=0.1
    )
    
    # Test JSON export
    json_export = monitor.export_metrics(format="json")
    assert isinstance(json_export, str)
    data = json.loads(json_export)
    assert "system_metrics" in data
    assert "alerts" in data
    assert "performance_metrics" in data
    
    # Test dict export
    dict_export = monitor.export_metrics(format="dict")
    assert isinstance(dict_export, dict)
    assert "system_metrics" in dict_export
    assert "alerts" in dict_export
    assert "performance_metrics" in dict_export

def test_system_alerts(monitor):
    """Test system alert generation"""
    # Wait for system monitoring
    time.sleep(2)
    
    # Get system alerts
    alerts = monitor.get_alerts(category="system")
    
    # System metrics should be collected
    metrics = monitor.get_system_metrics()
    assert metrics["current"]["cpu_percent"] >= 0
    assert metrics["current"]["memory_percent"] >= 0
    assert metrics["current"]["disk_percent"] >= 0

def test_concurrent_monitoring(monitor):
    """Test concurrent monitoring operations"""
    import threading
    
    def create_alerts():
        for i in range(10):
            monitor.create_alert(
                AlertLevel.INFO,
                f"Test alert {i}",
                "test"
            )
            time.sleep(0.1)
    
    def track_requests():
        for i in range(10):
            monitor.track_request(
                endpoint=f"/api/test/{i}",
                method="GET",
                duration=0.1
            )
            time.sleep(0.1)
    
    # Create threads
    alert_thread = threading.Thread(target=create_alerts)
    request_thread = threading.Thread(target=track_requests)
    
    # Start threads
    alert_thread.start()
    request_thread.start()
    
    # Wait for threads
    alert_thread.join()
    request_thread.join()
    
    # Verify data
    alerts = monitor.get_alerts()
    assert len(alerts) >= 10
    
    metrics = monitor.export_metrics(format="dict")
    assert "performance_metrics" in metrics
