"""
Monitoring Configuration
PGF Protocol: MON_002
Gate: GATE_10
Version: 1.0.0
"""

from typing import Dict
from .framework import (
    MonitoringConfig,
    MetricConfig,
    AlertRule,
    MetricType,
    AlertSeverity
)

def get_monitoring_config() -> MonitoringConfig:
    """Get monitoring configuration"""
    
    # Metric configurations
    metrics: Dict[str, MetricConfig] = {
        # HTTP metrics
        "http_requests_total": MetricConfig(
            name="http_requests_total",
            type=MetricType.COUNTER,
            description="Total HTTP requests",
            labels=["endpoint", "method", "status"]
        ),
        "http_request_duration_seconds": MetricConfig(
            name="http_request_duration_seconds",
            type=MetricType.HISTOGRAM,
            description="HTTP request duration in seconds",
            labels=["endpoint", "method", "status"],
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
        ),
        "http_request_errors_total": MetricConfig(
            name="http_request_errors_total",
            type=MetricType.COUNTER,
            description="Total HTTP request errors",
            labels=["endpoint", "method", "status", "error"]
        ),
        
        # Calculation metrics
        "calculations_total": MetricConfig(
            name="calculations_total",
            type=MetricType.COUNTER,
            description="Total calculations performed",
            labels=["type", "success"]
        ),
        "calculation_duration_seconds": MetricConfig(
            name="calculation_duration_seconds",
            type=MetricType.HISTOGRAM,
            description="Calculation duration in seconds",
            labels=["type", "success"],
            buckets=[0.1, 0.5, 1.0, 5.0, 10.0]
        ),
        
        # Cache metrics
        "cache_operations_total": MetricConfig(
            name="cache_operations_total",
            type=MetricType.COUNTER,
            description="Total cache operations",
            labels=["operation", "hit"]
        ),
        "cache_hits_total": MetricConfig(
            name="cache_hits_total",
            type=MetricType.COUNTER,
            description="Total cache hits"
        ),
        "cache_misses_total": MetricConfig(
            name="cache_misses_total",
            type=MetricType.COUNTER,
            description="Total cache misses"
        ),
        
        # System metrics
        "system_cpu_usage": MetricConfig(
            name="system_cpu_usage",
            type=MetricType.GAUGE,
            description="System CPU usage percentage"
        ),
        "system_memory_usage": MetricConfig(
            name="system_memory_usage",
            type=MetricType.GAUGE,
            description="System memory usage percentage"
        ),
        "system_disk_usage": MetricConfig(
            name="system_disk_usage",
            type=MetricType.GAUGE,
            description="System disk usage percentage",
            labels=["path"]
        ),
        "system_network_io": MetricConfig(
            name="system_network_io",
            type=MetricType.COUNTER,
            description="System network IO bytes",
            labels=["direction"]
        )
    }
    
    # Alert configurations
    alerts: Dict[str, AlertRule] = {
        # System alerts
        "high_cpu_usage": AlertRule(
            name="high_cpu_usage",
            description="High CPU usage detected",
            severity=AlertSeverity.HIGH,
            metric="system_cpu_usage",
            condition=">",
            threshold=80.0,
            duration=300,
            labels={"type": "system"},
            annotations={
                "summary": "High CPU usage",
                "description": "CPU usage is above 80%"
            }
        ),
        "high_memory_usage": AlertRule(
            name="high_memory_usage",
            description="High memory usage detected",
            severity=AlertSeverity.HIGH,
            metric="system_memory_usage",
            condition=">",
            threshold=80.0,
            duration=300,
            labels={"type": "system"},
            annotations={
                "summary": "High memory usage",
                "description": "Memory usage is above 80%"
            }
        ),
        "high_disk_usage": AlertRule(
            name="high_disk_usage",
            description="High disk usage detected",
            severity=AlertSeverity.HIGH,
            metric="system_disk_usage",
            condition=">",
            threshold=85.0,
            duration=3600,
            labels={"type": "system"},
            annotations={
                "summary": "High disk usage",
                "description": "Disk usage is above 85%"
            }
        ),
        
        # Application alerts
        "high_error_rate": AlertRule(
            name="high_error_rate",
            description="High error rate detected",
            severity=AlertSeverity.HIGH,
            metric="http_request_errors_total",
            condition=">",
            threshold=10.0,
            duration=300,
            labels={"type": "application"},
            annotations={
                "summary": "High error rate",
                "description": "Error rate is above 10 per 5 minutes"
            }
        ),
        "slow_response_time": AlertRule(
            name="slow_response_time",
            description="Slow response time detected",
            severity=AlertSeverity.MEDIUM,
            metric="http_request_duration_seconds",
            condition=">",
            threshold=5.0,
            duration=300,
            labels={"type": "application"},
            annotations={
                "summary": "Slow response time",
                "description": "Response time is above 5 seconds"
            }
        ),
        "high_cache_miss_rate": AlertRule(
            name="high_cache_miss_rate",
            description="High cache miss rate detected",
            severity=AlertSeverity.MEDIUM,
            metric="cache_misses_total",
            condition=">",
            threshold=100.0,
            duration=300,
            labels={"type": "cache"},
            annotations={
                "summary": "High cache miss rate",
                "description": "Cache miss rate is above 100 per 5 minutes"
            }
        )
    }
    
    return MonitoringConfig(
        metrics_port=9090,
        metrics_path="/metrics",
        collection_interval=15,
        retention_days=30,
        alert_check_interval=60,
        metrics=metrics,
        alerts=alerts
    )
