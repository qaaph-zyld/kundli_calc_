"""
Performance Middleware
PGF Protocol: PERF_003
Gate: GATE_4
Version: 1.0.0
"""

from fastapi import Request, Response
from ..middleware.base import BaseMiddleware, MiddlewarePriority
from .monitor import performance_monitor, MetricType
from .optimizer import performance_optimizer
import time
from datetime import datetime

class PerformanceMiddleware(BaseMiddleware):
    """Performance monitoring and optimization middleware"""
    
    def __init__(self):
        super().__init__(priority=MiddlewarePriority.HIGH)
        self._optimization_enabled = True
    
    async def process_request(self, request: Request) -> Request:
        """Process and monitor incoming requests"""
        # Start timing
        request.state.start_time = time.time()
        
        # Record request metrics
        await performance_monitor.record_metric(
            MetricType.THROUGHPUT,
            1.0  # Increment request count
        )
        
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Process and optimize outgoing responses"""
        # Calculate response time
        if hasattr(response.request.state, "start_time"):
            response_time = time.time() - response.request.state.start_time
            
            # Record latency
            await performance_monitor.record_metric(
                MetricType.LATENCY,
                response_time
            )
            
            # Record error rate if applicable
            if response.status_code >= 400:
                await performance_monitor.record_metric(
                    MetricType.ERROR_RATE,
                    1.0
                )
            
            # Add performance headers
            response.headers["X-Response-Time"] = f"{response_time:.3f}"
            
            # Check for performance optimization
            if self._optimization_enabled and response_time > 0.5:  # 500ms threshold
                await self._optimize_performance()
        
        return response
    
    async def _optimize_performance(self) -> None:
        """Trigger performance optimization"""
        # Check current metrics
        latency_stats = performance_monitor.get_statistics(MetricType.LATENCY)
        cpu_stats = performance_monitor.get_statistics(MetricType.CPU_USAGE)
        memory_stats = performance_monitor.get_statistics(MetricType.MEMORY_USAGE)
        
        # Determine which optimizations to apply
        if latency_stats.get("avg", 0) > 0.5:
            await performance_optimizer.optimize_performance(MetricType.LATENCY)
        
        if cpu_stats.get("avg", 0) > 70:
            await performance_optimizer.optimize_performance(MetricType.CPU_USAGE)
        
        if memory_stats.get("avg", 0) > 70:
            await performance_optimizer.optimize_performance(MetricType.MEMORY_USAGE)
