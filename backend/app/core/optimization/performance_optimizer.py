"""
Performance Optimization Module
PGF Protocol: OPT_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass
import asyncio
import logging
import time
from datetime import datetime
import threading
from enum import Enum
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import psutil
from functools import wraps

T = TypeVar('T')

class OptimizationStrategy(Enum):
    MEMORY = "memory"
    CPU = "cpu"
    LATENCY = "latency"
    BALANCED = "balanced"

@dataclass
class OptimizationMetrics:
    """Performance optimization metrics"""
    execution_time: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    optimized_calls: int = 0
    total_calls: int = 0

class PerformanceProfile:
    """Performance profiling for function calls"""
    
    def __init__(self, name: str):
        self.name = name
        self.call_count = 0
        self.total_time = 0.0
        self.min_time = float('inf')
        self.max_time = 0.0
        self.memory_samples: List[float] = []
        self.cpu_samples: List[float] = []
    
    def update(
        self,
        execution_time: float,
        memory_usage: float,
        cpu_usage: float
    ) -> None:
        """Update profile with new measurement"""
        self.call_count += 1
        self.total_time += execution_time
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)
        self.memory_samples.append(memory_usage)
        self.cpu_samples.append(cpu_usage)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistical analysis of profile"""
        if not self.call_count:
            return {}
        
        return {
            "name": self.name,
            "call_count": self.call_count,
            "avg_time": self.total_time / self.call_count,
            "min_time": self.min_time,
            "max_time": self.max_time,
            "memory_stats": {
                "mean": np.mean(self.memory_samples),
                "std": np.std(self.memory_samples),
                "max": max(self.memory_samples)
            },
            "cpu_stats": {
                "mean": np.mean(self.cpu_samples),
                "std": np.std(self.cpu_samples),
                "max": max(self.cpu_samples)
            }
        }

class OptimizationContext:
    """Context for optimization decisions"""
    
    def __init__(
        self,
        strategy: OptimizationStrategy,
        max_memory_mb: float = 1000.0,
        max_cpu_percent: float = 80.0,
        target_latency_ms: float = 100.0
    ):
        self.strategy = strategy
        self.max_memory_mb = max_memory_mb
        self.max_cpu_percent = max_cpu_percent
        self.target_latency_ms = target_latency_ms
        self.profiles: Dict[str, PerformanceProfile] = {}
        self.lock = threading.Lock()
    
    def get_optimization_level(self) -> int:
        """Determine optimization level based on current metrics"""
        memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)
        cpu_usage = psutil.cpu_percent()
        
        if self.strategy == OptimizationStrategy.MEMORY:
            if memory_usage > self.max_memory_mb * 0.9:
                return 3  # Aggressive optimization
            elif memory_usage > self.max_memory_mb * 0.7:
                return 2  # Moderate optimization
            return 1  # Light optimization
            
        elif self.strategy == OptimizationStrategy.CPU:
            if cpu_usage > self.max_cpu_percent * 0.9:
                return 3
            elif cpu_usage > self.max_cpu_percent * 0.7:
                return 2
            return 1
            
        elif self.strategy == OptimizationStrategy.LATENCY:
            # Use profile data to determine latency optimization
            avg_latencies = [
                p.total_time / p.call_count
                for p in self.profiles.values()
                if p.call_count > 0
            ]
            if not avg_latencies:
                return 1
                
            avg_latency = sum(avg_latencies) / len(avg_latencies)
            if avg_latency > self.target_latency_ms * 0.001 * 1.5:
                return 3
            elif avg_latency > self.target_latency_ms * 0.001:
                return 2
            return 1
            
        else:  # BALANCED
            memory_level = self.get_optimization_level(
                OptimizationStrategy.MEMORY
            )
            cpu_level = self.get_optimization_level(
                OptimizationStrategy.CPU
            )
            latency_level = self.get_optimization_level(
                OptimizationStrategy.LATENCY
            )
            return max(memory_level, cpu_level, latency_level)

class PerformanceOptimizer:
    """Performance optimization engine"""
    
    def __init__(
        self,
        strategy: OptimizationStrategy = OptimizationStrategy.BALANCED,
        max_workers: int = 10
    ):
        self.context = OptimizationContext(strategy)
        self.metrics = OptimizationMetrics()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
    
    def optimize(self, func: Callable) -> Callable:
        """Decorator for optimizing function execution"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            start_cpu = psutil.cpu_percent()
            
            try:
                # Get optimization level
                opt_level = self.context.get_optimization_level()
                
                # Apply optimizations based on level
                if opt_level >= 3:
                    result = await self._optimize_aggressive(
                        func, *args, **kwargs
                    )
                elif opt_level >= 2:
                    result = await self._optimize_moderate(
                        func, *args, **kwargs
                    )
                else:
                    result = await self._optimize_light(
                        func, *args, **kwargs
                    )
                
                return result
                
            finally:
                # Update metrics
                execution_time = time.time() - start_time
                end_memory = psutil.Process().memory_info().rss
                end_cpu = psutil.cpu_percent()
                
                memory_used = (end_memory - start_memory) / (1024 * 1024)
                cpu_used = (end_cpu - start_cpu)
                
                with self.lock:
                    self.metrics.execution_time += execution_time
                    self.metrics.memory_usage += memory_used
                    self.metrics.cpu_usage += cpu_used
                    self.metrics.total_calls += 1
                    
                    # Update profile
                    profile_name = func.__name__
                    if profile_name not in self.context.profiles:
                        self.context.profiles[profile_name] = PerformanceProfile(
                            profile_name
                        )
                    
                    self.context.profiles[profile_name].update(
                        execution_time,
                        memory_used,
                        cpu_used
                    )
        
        return wrapper
    
    async def _optimize_aggressive(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Aggressive optimization strategy"""
        # Use thread pool for CPU-bound operations
        loop = asyncio.get_event_loop()
        
        # Split operation if possible
        if hasattr(func, '__split__'):
            chunks = func.__split__(*args, **kwargs)
            tasks = [
                loop.run_in_executor(
                    self.executor,
                    lambda c=chunk: func.__process_chunk__(c)
                )
                for chunk in chunks
            ]
            results = await asyncio.gather(*tasks)
            return func.__merge__(results)
        
        # Fallback to regular execution in thread pool
        return await loop.run_in_executor(
            self.executor,
            lambda: func(*args, **kwargs)
        )
    
    async def _optimize_moderate(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Moderate optimization strategy"""
        # Use basic parallelization
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            lambda: func(*args, **kwargs)
        )
    
    async def _optimize_light(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Light optimization strategy"""
        # Direct execution with monitoring
        return await func(*args, **kwargs)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current optimization metrics"""
        with self.lock:
            metrics = {
                "execution_time": self.metrics.execution_time,
                "memory_usage": self.metrics.memory_usage,
                "cpu_usage": self.metrics.cpu_usage,
                "total_calls": self.metrics.total_calls,
                "optimization_level": self.context.get_optimization_level(),
                "profiles": {
                    name: profile.get_stats()
                    for name, profile in self.context.profiles.items()
                }
            }
            
            if self.metrics.total_calls > 0:
                metrics.update({
                    "avg_execution_time": (
                        self.metrics.execution_time /
                        self.metrics.total_calls
                    ),
                    "avg_memory_usage": (
                        self.metrics.memory_usage /
                        self.metrics.total_calls
                    ),
                    "avg_cpu_usage": (
                        self.metrics.cpu_usage /
                        self.metrics.total_calls
                    )
                })
            
            return metrics
    
    def reset_metrics(self) -> None:
        """Reset optimization metrics"""
        with self.lock:
            self.metrics = OptimizationMetrics()
            self.context.profiles.clear()

def optimized(
    optimizer: Optional[PerformanceOptimizer] = None,
    strategy: OptimizationStrategy = OptimizationStrategy.BALANCED
):
    """Decorator for applying optimization"""
    if optimizer is None:
        optimizer = PerformanceOptimizer(strategy=strategy)
    
    def decorator(func: Callable) -> Callable:
        return optimizer.optimize(func)
    
    return decorator
