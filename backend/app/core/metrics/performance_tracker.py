"""
Performance Metrics Tracker
PGF Protocol: MET_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass, field
import asyncio
import logging
from datetime import datetime, timedelta
import numpy as np
from enum import Enum
from collections import defaultdict
import psutil
import time
import threading
from functools import wraps
import json

class MetricType(Enum):
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    RESOURCE = "resource"
    ERROR = "error"
    CUSTOM = "custom"

class MetricUnit(Enum):
    MILLISECONDS = "ms"
    REQUESTS = "req"
    PERCENTAGE = "%"
    BYTES = "bytes"
    COUNT = "count"
    CUSTOM = "custom"

@dataclass
class MetricValue:
    """Represents a metric measurement"""
    value: float
    unit: MetricUnit
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class MetricSeries:
    """Represents a time series of metric values"""
    metric_type: MetricType
    name: str
    values: List[MetricValue] = field(default_factory=list)
    aggregation: str = "avg"  # avg, sum, min, max
    retention_period: Optional[timedelta] = None

class PerformanceTracker:
    """Advanced performance metrics tracking system"""
    
    def __init__(
        self,
        retention_period: Optional[timedelta] = timedelta(hours=24)
    ):
        self.retention_period = retention_period
        self.metrics: Dict[str, MetricSeries] = {}
        self.logger = logging.getLogger(__name__)
        self._lock = threading.Lock()
        
        # Initialize standard metrics
        self._initialize_metrics()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _initialize_metrics(self) -> None:
        """Initialize standard performance metrics"""
        # Latency Metrics
        self.add_metric_series(
            MetricSeries(
                metric_type=MetricType.LATENCY,
                name="request_latency",
                aggregation="avg",
                retention_period=self.retention_period
            )
        )
        
        self.add_metric_series(
            MetricSeries(
                metric_type=MetricType.LATENCY,
                name="calculation_time",
                aggregation="avg",
                retention_period=self.retention_period
            )
        )
        
        # Throughput Metrics
        self.add_metric_series(
            MetricSeries(
                metric_type=MetricType.THROUGHPUT,
                name="requests_per_second",
                aggregation="sum",
                retention_period=self.retention_period
            )
        )
        
        self.add_metric_series(
            MetricSeries(
                metric_type=MetricType.THROUGHPUT,
                name="calculations_per_second",
                aggregation="sum",
                retention_period=self.retention_period
            )
        )
        
        # Resource Metrics
        self.add_metric_series(
            MetricSeries(
                metric_type=MetricType.RESOURCE,
                name="cpu_usage",
                aggregation="avg",
                retention_period=self.retention_period
            )
        )
        
        self.add_metric_series(
            MetricSeries(
                metric_type=MetricType.RESOURCE,
                name="memory_usage",
                aggregation="avg",
                retention_period=self.retention_period
            )
        )
        
        # Error Metrics
        self.add_metric_series(
            MetricSeries(
                metric_type=MetricType.ERROR,
                name="error_rate",
                aggregation="avg",
                retention_period=self.retention_period
            )
        )
    
    def _start_background_tasks(self) -> None:
        """Start background monitoring tasks"""
        self._resource_monitor_thread = threading.Thread(
            target=self._monitor_resources,
            daemon=True
        )
        self._resource_monitor_thread.start()
    
    def add_metric_series(self, series: MetricSeries) -> None:
        """Add a new metric series"""
        with self._lock:
            self.metrics[series.name] = series
    
    def track_metric(
        self,
        name: str,
        value: float,
        unit: MetricUnit,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Track a metric value"""
        with self._lock:
            if name not in self.metrics:
                self.logger.warning(f"Metric series '{name}' not found")
                return
            
            metric_value = MetricValue(
                value=value,
                unit=unit,
                tags=tags or {}
            )
            
            self.metrics[name].values.append(metric_value)
            
            # Apply retention policy
            self._apply_retention(name)
    
    def _apply_retention(self, metric_name: str) -> None:
        """Apply retention policy to metric series"""
        series = self.metrics[metric_name]
        if not series.retention_period:
            return
        
        cutoff_time = datetime.now() - series.retention_period
        series.values = [
            v for v in series.values
            if v.timestamp >= cutoff_time
        ]
    
    def _monitor_resources(self) -> None:
        """Background resource monitoring"""
        while True:
            try:
                # Monitor CPU usage
                cpu_percent = psutil.cpu_percent()
                self.track_metric(
                    "cpu_usage",
                    cpu_percent,
                    MetricUnit.PERCENTAGE
                )
                
                # Monitor memory usage
                memory = psutil.Process().memory_info()
                memory_percent = memory.rss / psutil.virtual_memory().total * 100
                self.track_metric(
                    "memory_usage",
                    memory_percent,
                    MetricUnit.PERCENTAGE
                )
                
                time.sleep(1)  # Sample every second
                
            except Exception as e:
                self.logger.error(
                    f"Error monitoring resources: {str(e)}"
                )
                time.sleep(5)  # Back off on error
    
    def get_metric_statistics(
        self,
        metric_name: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        aggregation: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get statistics for a metric series"""
        with self._lock:
            if metric_name not in self.metrics:
                return {}
            
            series = self.metrics[metric_name]
            values = series.values
            
            # Apply time filter
            if start_time:
                values = [v for v in values if v.timestamp >= start_time]
            if end_time:
                values = [v for v in values if v.timestamp <= end_time]
            
            if not values:
                return {
                    "metric_type": series.metric_type.value,
                    "name": metric_name,
                    "count": 0
                }
            
            # Extract raw values
            raw_values = [v.value for v in values]
            
            # Calculate statistics
            stats = {
                "metric_type": series.metric_type.value,
                "name": metric_name,
                "count": len(values),
                "unit": values[0].unit.value,
                "min": min(raw_values),
                "max": max(raw_values),
                "avg": np.mean(raw_values),
                "std": np.std(raw_values),
                "p50": np.percentile(raw_values, 50),
                "p95": np.percentile(raw_values, 95),
                "p99": np.percentile(raw_values, 99),
                "first_timestamp": min(v.timestamp for v in values),
                "last_timestamp": max(v.timestamp for v in values)
            }
            
            # Apply custom aggregation if specified
            if aggregation:
                if aggregation == "sum":
                    stats["aggregated_value"] = sum(raw_values)
                elif aggregation == "min":
                    stats["aggregated_value"] = min(raw_values)
                elif aggregation == "max":
                    stats["aggregated_value"] = max(raw_values)
                else:  # default to avg
                    stats["aggregated_value"] = np.mean(raw_values)
            
            return stats
    
    def get_all_metrics(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all metrics"""
        return {
            name: self.get_metric_statistics(
                name, start_time, end_time
            )
            for name in self.metrics
        }
    
    def calculate_sla_compliance(
        self,
        sla_thresholds: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate SLA compliance percentages"""
        compliance = {}
        
        for metric_name, threshold in sla_thresholds.items():
            if metric_name not in self.metrics:
                continue
            
            series = self.metrics[metric_name]
            if not series.values:
                continue
            
            # Calculate compliance percentage
            total_samples = len(series.values)
            compliant_samples = sum(
                1 for v in series.values
                if v.value <= threshold
            )
            
            compliance[metric_name] = (
                compliant_samples / total_samples * 100
            )
        
        return compliance
    
    def export_metrics(
        self,
        format: str = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Export metrics data"""
        data = {}
        
        for name, series in self.metrics.items():
            data[name] = {
                "metric_type": series.metric_type.value,
                "values": [
                    {
                        "value": v.value,
                        "unit": v.unit.value,
                        "timestamp": v.timestamp.isoformat(),
                        "tags": v.tags
                    }
                    for v in series.values
                ]
            }
        
        if format == "json":
            return json.dumps(data, indent=2)
        return data
    
    def reset(self) -> None:
        """Reset all metrics"""
        with self._lock:
            for series in self.metrics.values():
                series.values.clear()

def track_performance(
    metric_name: str,
    unit: MetricUnit = MetricUnit.MILLISECONDS
):
    """Decorator for tracking function performance"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            start_time = time.time()
            try:
                result = await func(self, *args, **kwargs)
                duration = (time.time() - start_time) * 1000  # ms
                
                # Track metric if tracker exists
                if hasattr(self, '_performance_tracker'):
                    self._performance_tracker.track_metric(
                        metric_name,
                        duration,
                        unit
                    )
                
                return result
            except Exception as e:
                # Track error if tracker exists
                if hasattr(self, '_performance_tracker'):
                    self._performance_tracker.track_metric(
                        "error_rate",
                        1.0,
                        MetricUnit.COUNT
                    )
                raise e
        
        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            start_time = time.time()
            try:
                result = func(self, *args, **kwargs)
                duration = (time.time() - start_time) * 1000  # ms
                
                # Track metric if tracker exists
                if hasattr(self, '_performance_tracker'):
                    self._performance_tracker.track_metric(
                        metric_name,
                        duration,
                        unit
                    )
                
                return result
            except Exception as e:
                # Track error if tracker exists
                if hasattr(self, '_performance_tracker'):
                    self._performance_tracker.track_metric(
                        "error_rate",
                        1.0,
                        MetricUnit.COUNT
                    )
                raise e
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator
