"""
Performance Monitoring Framework
PGF Protocol: PERF_001
Gate: GATE_4
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import time
import asyncio
import psutil
import statistics
from enum import Enum
from pydantic import BaseModel
from collections import deque

class MetricType(str, Enum):
    """Types of performance metrics"""
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DB_QUERIES = "db_queries"
    CACHE_HITS = "cache_hits"
    ERROR_RATE = "error_rate"

class PerformanceThreshold(BaseModel):
    """Performance threshold configuration"""
    warning: float
    critical: float
    duration: Optional[int] = None  # Duration in seconds to maintain threshold

class MetricData(BaseModel):
    """Performance metric data"""
    value: float
    timestamp: datetime
    threshold_exceeded: bool = False

class PerformanceMonitor:
    """Performance monitoring and analysis system"""
    
    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self._metrics: Dict[MetricType, deque] = {
            metric: deque(maxlen=window_size) for metric in MetricType
        }
        self._thresholds: Dict[MetricType, PerformanceThreshold] = {
            MetricType.LATENCY: PerformanceThreshold(warning=0.5, critical=1.0),
            MetricType.CPU_USAGE: PerformanceThreshold(warning=70, critical=90),
            MetricType.MEMORY_USAGE: PerformanceThreshold(warning=70, critical=85),
            MetricType.ERROR_RATE: PerformanceThreshold(warning=5, critical=10)
        }
        self._start_time = datetime.utcnow()
        self._last_cleanup = self._start_time
    
    async def record_metric(self, metric_type: MetricType, value: float) -> None:
        """Record a performance metric"""
        metric_data = MetricData(
            value=value,
            timestamp=datetime.utcnow(),
            threshold_exceeded=self._check_threshold(metric_type, value)
        )
        self._metrics[metric_type].append(metric_data)
        
        # Trigger analysis if threshold exceeded
        if metric_data.threshold_exceeded:
            await self._analyze_performance_degradation(metric_type)
    
    def get_metrics(self, metric_type: MetricType, duration: Optional[timedelta] = None) -> List[MetricData]:
        """Get metrics for specified duration"""
        if not duration:
            return list(self._metrics[metric_type])
            
        cutoff = datetime.utcnow() - duration
        return [m for m in self._metrics[metric_type] if m.timestamp >= cutoff]
    
    def get_statistics(self, metric_type: MetricType, duration: Optional[timedelta] = None) -> Dict[str, float]:
        """Calculate statistics for a metric"""
        metrics = self.get_metrics(metric_type, duration)
        values = [m.value for m in metrics]
        
        if not values:
            return {}
            
        return {
            "min": min(values),
            "max": max(values),
            "avg": statistics.mean(values),
            "median": statistics.median(values),
            "stddev": statistics.stdev(values) if len(values) > 1 else 0,
            "95th_percentile": statistics.quantiles(values, n=20)[-1],
            "threshold_violations": sum(1 for m in metrics if m.threshold_exceeded)
        }
    
    def _check_threshold(self, metric_type: MetricType, value: float) -> bool:
        """Check if metric exceeds threshold"""
        threshold = self._thresholds.get(metric_type)
        if not threshold:
            return False
            
        return value >= threshold.critical
    
    async def _analyze_performance_degradation(self, metric_type: MetricType) -> None:
        """Analyze performance degradation patterns"""
        metrics = self.get_metrics(metric_type, timedelta(minutes=5))
        if not metrics:
            return
            
        # Calculate trend
        values = [m.value for m in metrics]
        trend = statistics.linear_regression(range(len(values)), values) if len(values) > 1 else 0
        
        # Check for sustained degradation
        sustained_violation = all(m.threshold_exceeded for m in metrics[-5:]) if len(metrics) >= 5 else False
        
        if sustained_violation or trend > 0.1:
            await self._trigger_performance_alert(metric_type)
    
    async def _trigger_performance_alert(self, metric_type: MetricType) -> None:
        """Trigger performance degradation alert"""
        stats = self.get_statistics(metric_type, timedelta(minutes=5))
        alert = {
            "metric_type": metric_type,
            "timestamp": datetime.utcnow().isoformat(),
            "statistics": stats,
            "message": f"Performance degradation detected for {metric_type}"
        }
        # Alert handling logic here
        print(f"PERFORMANCE ALERT: {alert}")  # Replace with proper alerting

class ResourceMonitor:
    """System resource monitoring"""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self._process = psutil.Process()
    
    async def start_monitoring(self) -> None:
        """Start resource monitoring"""
        while True:
            await self._collect_metrics()
            await asyncio.sleep(1)
    
    async def _collect_metrics(self) -> None:
        """Collect system resource metrics"""
        # CPU Usage
        cpu_percent = self._process.cpu_percent()
        await self.monitor.record_metric(MetricType.CPU_USAGE, cpu_percent)
        
        # Memory Usage
        memory_info = self._process.memory_info()
        memory_percent = memory_info.rss / psutil.virtual_memory().total * 100
        await self.monitor.record_metric(MetricType.MEMORY_USAGE, memory_percent)

# Global performance monitor instance
performance_monitor = PerformanceMonitor()
resource_monitor = ResourceMonitor(performance_monitor)
