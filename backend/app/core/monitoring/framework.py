"""
Monitoring Framework
PGF Protocol: MON_001
Gate: GATE_10
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, Type
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import time
import psutil
import logging
import json
from pathlib import Path
import asyncio
from collections import deque
from statistics import mean, median, stdev
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Summary,
    start_http_server
)

class MetricType(str, Enum):
    """Metric types"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class MetricLabel(str, Enum):
    """Metric labels"""
    SERVICE = "service"
    ENDPOINT = "endpoint"
    METHOD = "method"
    STATUS = "status"
    ERROR = "error"

class AlertSeverity(str, Enum):
    """Alert severities"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class AlertStatus(str, Enum):
    """Alert statuses"""
    FIRING = "firing"
    RESOLVED = "resolved"
    ACKNOWLEDGED = "acknowledged"

class MetricConfig(BaseModel):
    """Metric configuration"""
    
    name: str
    type: MetricType
    description: str
    labels: List[str] = Field(default_factory=list)
    buckets: Optional[List[float]] = None
    quantiles: Optional[List[float]] = None

class AlertRule(BaseModel):
    """Alert rule"""
    
    name: str
    description: str
    severity: AlertSeverity
    metric: str
    condition: str
    threshold: float
    duration: int
    labels: Dict[str, str] = Field(default_factory=dict)
    annotations: Dict[str, str] = Field(default_factory=dict)

class Alert(BaseModel):
    """Alert"""
    
    name: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    metric: str
    value: float
    threshold: float
    labels: Dict[str, str]
    annotations: Dict[str, str]
    started_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

class MonitoringConfig(BaseModel):
    """Monitoring configuration"""
    
    metrics_port: int = 9090
    metrics_path: str = "/metrics"
    collection_interval: int = 15
    retention_days: int = 30
    alert_check_interval: int = 60
    metrics: Dict[str, MetricConfig]
    alerts: Dict[str, AlertRule]

class MetricsManager:
    """Metrics manager"""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
    
    def create_metric(self, config: MetricConfig) -> None:
        """Create metric based on configuration"""
        if config.name in self.metrics:
            return
            
        if config.type == MetricType.COUNTER:
            metric = Counter(
                config.name,
                config.description,
                config.labels
            )
        elif config.type == MetricType.GAUGE:
            metric = Gauge(
                config.name,
                config.description,
                config.labels
            )
        elif config.type == MetricType.HISTOGRAM:
            metric = Histogram(
                config.name,
                config.description,
                config.labels,
                buckets=config.buckets or Histogram.DEFAULT_BUCKETS
            )
        else:  # SUMMARY
            metric = Summary(
                config.name,
                config.description,
                config.labels,
                quantiles=config.quantiles or [0.5, 0.9, 0.99]
            )
        
        self.metrics[config.name] = metric
    
    def get_metric(self, name: str) -> Optional[Any]:
        """Get metric by name"""
        return self.metrics.get(name)
    
    def increment_counter(
        self,
        name: str,
        value: float = 1,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Increment counter metric"""
        metric = self.get_metric(name)
        if metric and isinstance(metric, Counter):
            if labels:
                metric.labels(**labels).inc(value)
            else:
                metric.inc(value)
    
    def set_gauge(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Set gauge metric"""
        metric = self.get_metric(name)
        if metric and isinstance(metric, Gauge):
            if labels:
                metric.labels(**labels).set(value)
            else:
                metric.set(value)
    
    def observe_histogram(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Observe histogram metric"""
        metric = self.get_metric(name)
        if metric and isinstance(metric, Histogram):
            if labels:
                metric.labels(**labels).observe(value)
            else:
                metric.observe(value)
    
    def observe_summary(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Observe summary metric"""
        metric = self.get_metric(name)
        if metric and isinstance(metric, Summary):
            if labels:
                metric.labels(**labels).observe(value)
            else:
                metric.observe(value)

class AlertManager:
    """Alert manager"""
    
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.history: deque = deque(maxlen=1000)
    
    def check_alert(
        self,
        rule: AlertRule,
        value: float,
        current_time: datetime
    ) -> Optional[Alert]:
        """Check if alert should be fired"""
        alert_key = f"{rule.name}:{rule.labels}"
        
        # Check if alert condition is met
        is_firing = eval(
            f"{value} {rule.condition} {rule.threshold}",
            {"__builtins__": None},
            {"value": value, "threshold": rule.threshold}
        )
        
        if is_firing:
            if alert_key not in self.alerts:
                # Create new alert
                alert = Alert(
                    name=rule.name,
                    description=rule.description,
                    severity=rule.severity,
                    status=AlertStatus.FIRING,
                    metric=rule.metric,
                    value=value,
                    threshold=rule.threshold,
                    labels=rule.labels,
                    annotations=rule.annotations,
                    started_at=current_time,
                    updated_at=current_time
                )
                self.alerts[alert_key] = alert
                self.history.append(alert)
                return alert
            else:
                # Update existing alert
                alert = self.alerts[alert_key]
                alert.value = value
                alert.updated_at = current_time
                return alert
        else:
            if alert_key in self.alerts:
                # Resolve alert
                alert = self.alerts[alert_key]
                alert.status = AlertStatus.RESOLVED
                alert.resolved_at = current_time
                self.history.append(alert)
                del self.alerts[alert_key]
                return alert
        
        return None
    
    def get_active_alerts(
        self,
        severity: Optional[AlertSeverity] = None
    ) -> List[Alert]:
        """Get active alerts"""
        alerts = list(self.alerts.values())
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return sorted(alerts, key=lambda x: x.started_at, reverse=True)
    
    def get_alert_history(
        self,
        limit: int = 100,
        severity: Optional[AlertSeverity] = None
    ) -> List[Alert]:
        """Get alert history"""
        alerts = list(self.history)
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return sorted(alerts, key=lambda x: x.started_at, reverse=True)[:limit]
    
    def acknowledge_alert(self, alert_key: str) -> Optional[Alert]:
        """Acknowledge alert"""
        if alert_key in self.alerts:
            alert = self.alerts[alert_key]
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.updated_at = datetime.utcnow()
            return alert
        return None

class SystemMetricsCollector:
    """System metrics collector"""
    
    def __init__(self, metrics_manager: MetricsManager):
        self.metrics = metrics_manager
        self._setup_metrics()
    
    def _setup_metrics(self) -> None:
        """Setup system metrics"""
        metrics = {
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
        
        for config in metrics.values():
            self.metrics.create_metric(config)
    
    async def collect_metrics(self) -> None:
        """Collect system metrics"""
        # CPU usage
        self.metrics.set_gauge(
            "system_cpu_usage",
            psutil.cpu_percent()
        )
        
        # Memory usage
        memory = psutil.virtual_memory()
        self.metrics.set_gauge(
            "system_memory_usage",
            memory.percent
        )
        
        # Disk usage
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.metrics.set_gauge(
                    "system_disk_usage",
                    usage.percent,
                    {"path": partition.mountpoint}
                )
            except Exception:
                continue
        
        # Network IO
        net_io = psutil.net_io_counters()
        self.metrics.increment_counter(
            "system_network_io",
            net_io.bytes_sent,
            {"direction": "sent"}
        )
        self.metrics.increment_counter(
            "system_network_io",
            net_io.bytes_recv,
            {"direction": "received"}
        )

class MonitoringManager:
    """Monitoring manager"""
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.metrics = MetricsManager()
        self.alerts = AlertManager()
        self.system_collector = SystemMetricsCollector(self.metrics)
        self._setup_metrics()
        self._setup_logging()
    
    def _setup_metrics(self) -> None:
        """Setup metrics from configuration"""
        for config in self.config.metrics.values():
            self.metrics.create_metric(config)
    
    def _setup_logging(self) -> None:
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("monitoring.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def start(self) -> None:
        """Start monitoring"""
        self.logger.info("Starting monitoring")
        
        # Start Prometheus metrics server
        start_http_server(
            self.config.metrics_port,
            addr="0.0.0.0"
        )
        
        # Start collection and alert checking tasks
        await asyncio.gather(
            self._collect_metrics(),
            self._check_alerts()
        )
    
    async def _collect_metrics(self) -> None:
        """Collect metrics periodically"""
        while True:
            try:
                await self.system_collector.collect_metrics()
            except Exception as e:
                self.logger.error(f"Error collecting metrics: {str(e)}")
            
            await asyncio.sleep(self.config.collection_interval)
    
    async def _check_alerts(self) -> None:
        """Check alert rules periodically"""
        while True:
            try:
                current_time = datetime.utcnow()
                
                for rule in self.config.alerts.values():
                    metric = self.metrics.get_metric(rule.metric)
                    if metric:
                        # Get current metric value
                        if isinstance(metric, (Counter, Gauge)):
                            value = metric._value.get()
                        else:
                            value = metric._sum.get()
                        
                        # Check alert rule
                        alert = self.alerts.check_alert(
                            rule,
                            value,
                            current_time
                        )
                        
                        if alert:
                            self.logger.info(
                                f"Alert {alert.status}: {alert.name} "
                                f"(value={alert.value}, threshold={alert.threshold})"
                            )
            
            except Exception as e:
                self.logger.error(f"Error checking alerts: {str(e)}")
            
            await asyncio.sleep(self.config.alert_check_interval)
    
    def record_request(
        self,
        endpoint: str,
        method: str,
        duration: float,
        status: int,
        error: Optional[str] = None
    ) -> None:
        """Record API request metrics"""
        labels = {
            "endpoint": endpoint,
            "method": method,
            "status": str(status)
        }
        
        # Increment request counter
        self.metrics.increment_counter(
            "http_requests_total",
            1,
            labels
        )
        
        # Record request duration
        self.metrics.observe_histogram(
            "http_request_duration_seconds",
            duration,
            labels
        )
        
        # Record errors if any
        if error:
            self.metrics.increment_counter(
                "http_request_errors_total",
                1,
                {**labels, "error": error}
            )
    
    def record_calculation(
        self,
        type: str,
        duration: float,
        success: bool
    ) -> None:
        """Record calculation metrics"""
        labels = {
            "type": type,
            "success": str(success).lower()
        }
        
        # Increment calculation counter
        self.metrics.increment_counter(
            "calculations_total",
            1,
            labels
        )
        
        # Record calculation duration
        self.metrics.observe_histogram(
            "calculation_duration_seconds",
            duration,
            labels
        )
    
    def record_cache(
        self,
        operation: str,
        hit: bool
    ) -> None:
        """Record cache metrics"""
        labels = {
            "operation": operation,
            "hit": str(hit).lower()
        }
        
        # Increment cache operation counter
        self.metrics.increment_counter(
            "cache_operations_total",
            1,
            labels
        )
        
        # Update cache hit ratio
        if operation == "get":
            self.metrics.increment_counter(
                "cache_hits_total" if hit else "cache_misses_total",
                1
            )
