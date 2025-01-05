"""
Enhanced Monitoring System
Implements comprehensive monitoring for the Kundli Calculation Service
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import time
import psutil
import logging
from pydantic import BaseModel, Field
from app.core.cache import cache

class MetricType(str):
    """Metric types"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class Metric(BaseModel):
    """Metric model"""
    name: str
    type: str
    value: float
    labels: Dict[str, str] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PerformanceMetrics(BaseModel):
    """Performance metrics model"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    process_metrics: Dict[str, float]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class EndpointMetrics(BaseModel):
    """Endpoint metrics model"""
    path: str
    method: str
    status_code: int
    response_time: float
    error_count: int = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MonitoringSystem:
    """Enhanced monitoring system with comprehensive metrics collection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics: Dict[str, List[Metric]] = {}
        self.performance_metrics: List[PerformanceMetrics] = []
        self.endpoint_metrics: Dict[str, List[EndpointMetrics]] = {}
        
    async def track_metric(
        self,
        name: str,
        value: float,
        metric_type: str = MetricType.GAUGE,
        labels: Optional[Dict[str, str]] = None
    ):
        """Track a metric"""
        metric = Metric(
            name=name,
            type=metric_type,
            value=value,
            labels=labels or {}
        )
        
        if name not in self.metrics:
            self.metrics[name] = []
            
        self.metrics[name].append(metric)
        
        # Cache recent metrics
        await self._cache_metric(metric)
        
    async def track_endpoint(
        self,
        path: str,
        method: str,
        status_code: int,
        response_time: float
    ):
        """Track endpoint metrics"""
        metric = EndpointMetrics(
            path=path,
            method=method,
            status_code=status_code,
            response_time=response_time
        )
        
        endpoint_key = f"{method}:{path}"
        if endpoint_key not in self.endpoint_metrics:
            self.endpoint_metrics[endpoint_key] = []
            
        self.endpoint_metrics[endpoint_key].append(metric)
        
        # Cache endpoint metrics
        await self._cache_endpoint_metric(endpoint_key, metric)
        
        # Track error if status code >= 400
        if status_code >= 400:
            await self.track_metric(
                f"errors_{endpoint_key}",
                1,
                MetricType.COUNTER,
                {
                    "path": path,
                    "method": method,
                    "status_code": str(status_code)
                }
            )
            
    async def collect_performance_metrics(self):
        """Collect system performance metrics"""
        try:
            # System metrics
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Process metrics
            process = psutil.Process()
            process_metrics = {
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "threads": process.num_threads(),
                "handles": process.num_handles() if hasattr(process, 'num_handles') else 0
            }
            
            metrics = PerformanceMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                network_io={
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv
                },
                process_metrics=process_metrics
            )
            
            self.performance_metrics.append(metrics)
            
            # Cache performance metrics
            await self._cache_performance_metrics(metrics)
            
            # Track individual metrics
            await self.track_metric("cpu_usage", cpu_usage)
            await self.track_metric("memory_usage", memory.percent)
            await self.track_metric("disk_usage", disk.percent)
            
        except Exception as e:
            self.logger.error(f"Error collecting performance metrics: {str(e)}")
            
    async def get_metrics_summary(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get metrics summary"""
        end_time = end_time or datetime.utcnow()
        start_time = start_time or (end_time - timedelta(hours=1))
        
        summary = {
            "metrics": {},
            "endpoints": {},
            "performance": {
                "cpu_usage": [],
                "memory_usage": [],
                "disk_usage": [],
                "network_io": []
            },
            "timerange": {
                "start": start_time,
                "end": end_time
            }
        }
        
        # Get cached metrics
        for name, metrics in self.metrics.items():
            filtered_metrics = [
                m for m in metrics
                if start_time <= m.timestamp <= end_time
            ]
            
            if filtered_metrics:
                summary["metrics"][name] = {
                    "current": filtered_metrics[-1].value,
                    "min": min(m.value for m in filtered_metrics),
                    "max": max(m.value for m in filtered_metrics),
                    "avg": sum(m.value for m in filtered_metrics) / len(filtered_metrics)
                }
                
        # Get endpoint metrics
        for endpoint, metrics in self.endpoint_metrics.items():
            filtered_metrics = [
                m for m in metrics
                if start_time <= m.timestamp <= end_time
            ]
            
            if filtered_metrics:
                summary["endpoints"][endpoint] = {
                    "requests": len(filtered_metrics),
                    "errors": sum(1 for m in filtered_metrics if m.status_code >= 400),
                    "avg_response_time": sum(m.response_time for m in filtered_metrics) / len(filtered_metrics),
                    "p95_response_time": self._calculate_percentile(
                        [m.response_time for m in filtered_metrics],
                        95
                    )
                }
                
        # Get performance metrics
        filtered_perf_metrics = [
            m for m in self.performance_metrics
            if start_time <= m.timestamp <= end_time
        ]
        
        if filtered_perf_metrics:
            summary["performance"] = {
                "cpu_usage": {
                    "current": filtered_perf_metrics[-1].cpu_usage,
                    "avg": sum(m.cpu_usage for m in filtered_perf_metrics) / len(filtered_perf_metrics)
                },
                "memory_usage": {
                    "current": filtered_perf_metrics[-1].memory_usage,
                    "avg": sum(m.memory_usage for m in filtered_perf_metrics) / len(filtered_perf_metrics)
                },
                "disk_usage": {
                    "current": filtered_perf_metrics[-1].disk_usage,
                    "avg": sum(m.disk_usage for m in filtered_perf_metrics) / len(filtered_perf_metrics)
                },
                "network_io": {
                    "bytes_sent": filtered_perf_metrics[-1].network_io["bytes_sent"],
                    "bytes_recv": filtered_perf_metrics[-1].network_io["bytes_recv"]
                }
            }
            
        return summary
        
    async def _cache_metric(self, metric: Metric):
        """Cache metric"""
        key = f"metric:{metric.name}:{metric.timestamp.timestamp()}"
        await cache.set(key, metric.dict(), expire=3600)
        
    async def _cache_endpoint_metric(self, endpoint_key: str, metric: EndpointMetrics):
        """Cache endpoint metric"""
        key = f"endpoint:{endpoint_key}:{metric.timestamp.timestamp()}"
        await cache.set(key, metric.dict(), expire=3600)
        
    async def _cache_performance_metrics(self, metrics: PerformanceMetrics):
        """Cache performance metrics"""
        key = f"performance:{metrics.timestamp.timestamp()}"
        await cache.set(key, metrics.dict(), expire=3600)
        
    def _calculate_percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile value"""
        if not values:
            return 0.0
            
        sorted_values = sorted(values)
        index = int(len(sorted_values) * (percentile / 100))
        return sorted_values[index]


# Global monitoring system instance
monitoring_system = MonitoringSystem()
