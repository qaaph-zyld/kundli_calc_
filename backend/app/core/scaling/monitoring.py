"""
Service Scaling Monitoring
PGF Protocol: SCAL_004
Gate: GATE_35
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union, Set
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio
import json
import logging
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    start_http_server
)

class MetricType(str, Enum):
    """Metric types"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"

class MetricScope(str, Enum):
    """Metric scopes"""
    RESOURCE = "resource"
    PERFORMANCE = "performance"
    OPERATION = "operation"
    BUSINESS = "business"

@dataclass
class MetricDefinition:
    """Metric definition"""
    
    name: str
    type: MetricType
    scope: MetricScope
    description: str
    labels: List[str]
    buckets: Optional[List[float]] = None

class ScalingMonitor:
    """Scaling monitor"""
    
    def __init__(
        self,
        metrics_port: int = 8000,
        collection_interval: int = 60,
        retention_days: int = 7
    ):
        """Initialize monitor"""
        self.metrics_port = metrics_port
        self.collection_interval = collection_interval
        self.retention_days = retention_days
        
        # Initialize metrics
        self._init_metrics()
        
        # Initialize logger
        self._init_logger()
        
        # Start metrics server
        self._start_metrics_server()
    
    def _init_metrics(self):
        """Initialize metrics"""
        # Define metrics
        self.metrics_definitions = [
            # Resource metrics
            MetricDefinition(
                name="scaling_cpu_usage",
                type=MetricType.GAUGE,
                scope=MetricScope.RESOURCE,
                description="CPU usage percentage",
                labels=["service", "instance"]
            ),
            MetricDefinition(
                name="scaling_memory_usage",
                type=MetricType.GAUGE,
                scope=MetricScope.RESOURCE,
                description="Memory usage percentage",
                labels=["service", "instance"]
            ),
            
            # Performance metrics
            MetricDefinition(
                name="scaling_request_latency",
                type=MetricType.HISTOGRAM,
                scope=MetricScope.PERFORMANCE,
                description="Request latency in seconds",
                labels=["service", "endpoint"],
                buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
            ),
            MetricDefinition(
                name="scaling_request_count",
                type=MetricType.COUNTER,
                scope=MetricScope.PERFORMANCE,
                description="Total request count",
                labels=["service", "endpoint"]
            ),
            
            # Operation metrics
            MetricDefinition(
                name="scaling_operations_total",
                type=MetricType.COUNTER,
                scope=MetricScope.OPERATION,
                description="Total scaling operations",
                labels=["service", "operation"]
            ),
            MetricDefinition(
                name="scaling_operation_duration",
                type=MetricType.HISTOGRAM,
                scope=MetricScope.OPERATION,
                description="Scaling operation duration",
                labels=["service", "operation"],
                buckets=[1.0, 5.0, 15.0, 30.0, 60.0]
            ),
            
            # Business metrics
            MetricDefinition(
                name="scaling_cost",
                type=MetricType.GAUGE,
                scope=MetricScope.BUSINESS,
                description="Scaling cost in dollars",
                labels=["service", "resource"]
            ),
            MetricDefinition(
                name="scaling_savings",
                type=MetricType.COUNTER,
                scope=MetricScope.BUSINESS,
                description="Cost savings in dollars",
                labels=["service", "resource"]
            )
        ]
        
        # Create metrics
        self.metrics = {}
        
        for definition in self.metrics_definitions:
            if definition.type == MetricType.COUNTER:
                self.metrics[definition.name] = Counter(
                    definition.name,
                    definition.description,
                    definition.labels
                )
            elif definition.type == MetricType.GAUGE:
                self.metrics[definition.name] = Gauge(
                    definition.name,
                    definition.description,
                    definition.labels
                )
            elif definition.type == MetricType.HISTOGRAM:
                self.metrics[definition.name] = Histogram(
                    definition.name,
                    definition.description,
                    definition.labels,
                    buckets=definition.buckets
                )
    
    def _init_logger(self):
        """Initialize logger"""
        self.logger = logging.getLogger("scaling_monitor")
        self.logger.setLevel(logging.INFO)
        
        # Add handlers if not already added
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            file_handler = logging.FileHandler(
                "scaling_monitor.log"
            )
            file_handler.setLevel(logging.DEBUG)
            
            # Create formatters
            console_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            
            # Add formatters
            console_handler.setFormatter(console_formatter)
            file_handler.setFormatter(file_formatter)
            
            # Add handlers
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def _start_metrics_server(self):
        """Start metrics server"""
        try:
            start_http_server(self.metrics_port)
            self.logger.info(
                f"Metrics server started on port {self.metrics_port}"
            )
        
        except Exception as e:
            self.logger.error(
                f"Failed to start metrics server: {str(e)}"
            )
            raise e
    
    async def start_monitoring(self):
        """Start monitoring"""
        self.logger.info("Starting scaling monitoring")
        
        try:
            while True:
                # Collect metrics
                await self._collect_metrics()
                
                # Clean old metrics
                await self._clean_metrics()
                
                # Wait for next interval
                await asyncio.sleep(self.collection_interval)
        
        except Exception as e:
            self.logger.error(f"Monitoring error: {str(e)}")
            raise e
    
    async def _collect_metrics(self):
        """Collect metrics"""
        try:
            # Collect resource metrics
            await self._collect_resource_metrics()
            
            # Collect performance metrics
            await self._collect_performance_metrics()
            
            # Collect operation metrics
            await self._collect_operation_metrics()
            
            # Collect business metrics
            await self._collect_business_metrics()
        
        except Exception as e:
            self.logger.error(f"Metrics collection error: {str(e)}")
            raise e
    
    async def _collect_resource_metrics(self):
        """Collect resource metrics"""
        try:
            # Mock resource metrics collection
            cpu_usage = 0.75
            memory_usage = 0.65
            
            # Update metrics
            self.metrics["scaling_cpu_usage"].labels(
                service="kundli",
                instance="prod-1"
            ).set(cpu_usage)
            
            self.metrics["scaling_memory_usage"].labels(
                service="kundli",
                instance="prod-1"
            ).set(memory_usage)
        
        except Exception as e:
            self.logger.error(
                f"Resource metrics collection error: {str(e)}"
            )
            raise e
    
    async def _collect_performance_metrics(self):
        """Collect performance metrics"""
        try:
            # Mock performance metrics collection
            latency = 0.2
            requests = 100
            
            # Update metrics
            self.metrics["scaling_request_latency"].labels(
                service="kundli",
                endpoint="/calculate"
            ).observe(latency)
            
            self.metrics["scaling_request_count"].labels(
                service="kundli",
                endpoint="/calculate"
            ).inc(requests)
        
        except Exception as e:
            self.logger.error(
                f"Performance metrics collection error: {str(e)}"
            )
            raise e
    
    async def _collect_operation_metrics(self):
        """Collect operation metrics"""
        try:
            # Mock operation metrics collection
            duration = 15.0
            
            # Update metrics
            self.metrics["scaling_operations_total"].labels(
                service="kundli",
                operation="scale_up"
            ).inc()
            
            self.metrics["scaling_operation_duration"].labels(
                service="kundli",
                operation="scale_up"
            ).observe(duration)
        
        except Exception as e:
            self.logger.error(
                f"Operation metrics collection error: {str(e)}"
            )
            raise e
    
    async def _collect_business_metrics(self):
        """Collect business metrics"""
        try:
            # Mock business metrics collection
            cost = 10.5
            savings = 5.25
            
            # Update metrics
            self.metrics["scaling_cost"].labels(
                service="kundli",
                resource="compute"
            ).set(cost)
            
            self.metrics["scaling_savings"].labels(
                service="kundli",
                resource="compute"
            ).inc(savings)
        
        except Exception as e:
            self.logger.error(
                f"Business metrics collection error: {str(e)}"
            )
            raise e
    
    async def _clean_metrics(self):
        """Clean old metrics"""
        try:
            # Calculate retention threshold
            threshold = datetime.utcnow() - timedelta(
                days=self.retention_days
            )
            
            # Clean metrics older than threshold
            # Note: This is a mock implementation
            # Real implementation would depend on storage backend
            pass
        
        except Exception as e:
            self.logger.error(f"Metrics cleaning error: {str(e)}")
            raise e
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        metrics = {}
        
        try:
            for name, metric in self.metrics.items():
                if isinstance(metric, Counter):
                    metrics[name] = metric._value.get()
                elif isinstance(metric, Gauge):
                    metrics[name] = metric._value.get()
                elif isinstance(metric, Histogram):
                    metrics[name] = {
                        "count": metric._count.get(),
                        "sum": metric._sum.get(),
                        "buckets": metric._buckets
                    }
            
            return metrics
        
        except Exception as e:
            self.logger.error(f"Failed to get metrics: {str(e)}")
            raise e
