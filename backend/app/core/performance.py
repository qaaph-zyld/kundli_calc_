"""
Performance Monitoring and Timing Decorators
============================================
Tools for tracking calculation performance and timing.
"""

import time
import functools
from typing import Callable, Any, Dict
from datetime import datetime
from .logging_config import get_calculation_logger


class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, list] = {}
        self.logger = get_calculation_logger("performance")
    
    def record_timing(self, operation: str, duration_ms: float) -> None:
        """Record timing for an operation"""
        if operation not in self.metrics:
            self.metrics[operation] = []
        self.metrics[operation].append(duration_ms)
        
        self.logger.log_calculation_end(operation, duration_ms, success=True)
    
    def get_stats(self, operation: str) -> Dict[str, float]:
        """Get statistics for an operation"""
        if operation not in self.metrics or not self.metrics[operation]:
            return {}
        
        timings = self.metrics[operation]
        return {
            "count": len(timings),
            "min_ms": min(timings),
            "max_ms": max(timings),
            "avg_ms": sum(timings) / len(timings),
            "total_ms": sum(timings)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all operations"""
        return {op: self.get_stats(op) for op in self.metrics.keys()}


# Global performance monitor instance
_monitor = PerformanceMonitor()


def get_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance"""
    return _monitor


def timing_decorator(operation_name: str = None):
    """
    Decorator to time function execution
    
    Usage:
        @timing_decorator("dasha_calculation")
        def calculate_dasha(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        op_name = operation_name or func.__name__
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start_time) * 1000
                _monitor.record_timing(op_name, duration_ms)
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000
                _monitor.logger.log_calculation_error(
                    op_name, 
                    e, 
                    {"args": str(args)[:100], "kwargs": str(kwargs)[:100]}
                )
                raise
        
        return wrapper
    return decorator


def async_timing_decorator(operation_name: str = None):
    """
    Decorator to time async function execution
    
    Usage:
        @async_timing_decorator("async_chart_calc")
        async def calculate_chart_async(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        op_name = operation_name or func.__name__
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start_time) * 1000
                _monitor.record_timing(op_name, duration_ms)
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000
                _monitor.logger.log_calculation_error(
                    op_name, 
                    e, 
                    {"args": str(args)[:100], "kwargs": str(kwargs)[:100]}
                )
                raise
        
        return wrapper
    return decorator
