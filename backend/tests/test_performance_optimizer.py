"""
Test Suite for Performance Optimization Module
PGF Protocol: OPT_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
import time
import numpy as np
from app.core.optimization.performance_optimizer import (
    PerformanceOptimizer,
    OptimizationStrategy,
    optimized,
    PerformanceProfile
)

@pytest.fixture
def optimizer():
    return PerformanceOptimizer(
        strategy=OptimizationStrategy.BALANCED,
        max_workers=5
    )

@pytest.mark.asyncio
async def test_basic_optimization(optimizer):
    """Test basic function optimization"""
    
    @optimized(optimizer)
    async def test_function(x: int) -> int:
        await asyncio.sleep(0.1)
        return x * 2
    
    result = await test_function(5)
    assert result == 10
    
    metrics = optimizer.get_metrics()
    assert metrics["total_calls"] == 1
    assert metrics["execution_time"] >= 0.1
    assert "test_function" in metrics["profiles"]

@pytest.mark.asyncio
async def test_optimization_strategies(optimizer):
    """Test different optimization strategies"""
    
    # CPU-intensive function
    @optimized(optimizer, strategy=OptimizationStrategy.CPU)
    async def cpu_intensive(n: int) -> int:
        result = 0
        for i in range(n):
            result += i * i
        return result
    
    # Memory-intensive function
    @optimized(optimizer, strategy=OptimizationStrategy.MEMORY)
    async def memory_intensive(size: int) -> list:
        return [i * i for i in range(size)]
    
    # Test CPU optimization
    result = await cpu_intensive(1000)
    assert result == sum(i * i for i in range(1000))
    
    # Test memory optimization
    result = await memory_intensive(1000)
    assert len(result) == 1000
    assert result[0] == 0
    assert result[-1] == 999 * 999

@pytest.mark.asyncio
async def test_concurrent_optimization(optimizer):
    """Test optimization under concurrent load"""
    
    @optimized(optimizer)
    async def concurrent_task(x: int) -> int:
        await asyncio.sleep(0.1)
        return x * 2
    
    # Run multiple tasks concurrently
    tasks = [concurrent_task(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 10
    assert all(results[i] == i * 2 for i in range(10))
    
    metrics = optimizer.get_metrics()
    assert metrics["total_calls"] == 10

@pytest.mark.asyncio
async def test_aggressive_optimization(optimizer):
    """Test aggressive optimization mode"""
    
    class SplittableTask:
        @staticmethod
        def __split__(*args, **kwargs):
            # Split into chunks
            n = args[0]
            chunk_size = max(1, n // 4)
            return [
                range(i, min(i + chunk_size, n))
                for i in range(0, n, chunk_size)
            ]
        
        @staticmethod
        def __process_chunk__(chunk):
            return sum(i * i for i in chunk)
        
        @staticmethod
        def __merge__(results):
            return sum(results)
        
        def __call__(self, n):
            return sum(i * i for i in range(n))
    
    task = SplittableTask()
    
    @optimized(optimizer)
    async def optimized_task(n: int) -> int:
        return task(n)
    
    result = await optimized_task(1000)
    expected = sum(i * i for i in range(1000))
    assert result == expected

@pytest.mark.asyncio
async def test_performance_profiling(optimizer):
    """Test performance profiling functionality"""
    
    @optimized(optimizer)
    async def profiled_task(n: int) -> int:
        time.sleep(0.01)  # Simulate work
        return sum(i * i for i in range(n))
    
    # Run task multiple times
    for i in range(5):
        await profiled_task(100 * (i + 1))
    
    metrics = optimizer.get_metrics()
    profile = metrics["profiles"]["profiled_task"]
    
    assert profile["call_count"] == 5
    assert profile["avg_time"] > 0
    assert profile["min_time"] <= profile["max_time"]
    assert all(
        key in profile["memory_stats"]
        for key in ["mean", "std", "max"]
    )
    assert all(
        key in profile["cpu_stats"]
        for key in ["mean", "std", "max"]
    )

@pytest.mark.asyncio
async def test_optimization_levels(optimizer):
    """Test different optimization levels"""
    
    @optimized(optimizer)
    async def adaptive_task(n: int) -> int:
        # Task complexity increases with n
        time.sleep(0.01 * n)
        return sum(i * i for i in range(n))
    
    # Run with increasing load
    results = []
    for i in range(1, 4):
        result = await adaptive_task(i)
        results.append(result)
        metrics = optimizer.get_metrics()
        assert metrics["optimization_level"] >= 1
    
    assert len(results) == 3
    assert all(r >= 0 for r in results)

@pytest.mark.asyncio
async def test_metrics_reset(optimizer):
    """Test metrics reset functionality"""
    
    @optimized(optimizer)
    async def test_task() -> int:
        await asyncio.sleep(0.1)
        return 42
    
    # Run task
    await test_task()
    
    # Verify metrics
    metrics_before = optimizer.get_metrics()
    assert metrics_before["total_calls"] == 1
    
    # Reset metrics
    optimizer.reset_metrics()
    
    # Verify reset
    metrics_after = optimizer.get_metrics()
    assert metrics_after["total_calls"] == 0
    assert not metrics_after["profiles"]

@pytest.mark.asyncio
async def test_memory_optimization(optimizer):
    """Test memory usage optimization"""
    optimizer.context.strategy = OptimizationStrategy.MEMORY
    
    @optimized(optimizer)
    async def memory_task(size: int) -> list:
        # Allocate memory
        data = [i * i for i in range(size)]
        await asyncio.sleep(0.1)
        return data
    
    result = await memory_task(10000)
    assert len(result) == 10000
    
    metrics = optimizer.get_metrics()
    assert metrics["memory_usage"] >= 0
    assert "memory_task" in metrics["profiles"]

@pytest.mark.asyncio
async def test_cpu_optimization(optimizer):
    """Test CPU usage optimization"""
    optimizer.context.strategy = OptimizationStrategy.CPU
    
    @optimized(optimizer)
    async def cpu_task(n: int) -> int:
        # CPU-intensive operation
        result = 0
        for i in range(n):
            result += i * i
            for j in range(100):
                result += j
        return result
    
    result = await cpu_task(1000)
    assert result > 0
    
    metrics = optimizer.get_metrics()
    assert metrics["cpu_usage"] >= 0
    assert "cpu_task" in metrics["profiles"]

@pytest.mark.asyncio
async def test_latency_optimization(optimizer):
    """Test latency optimization"""
    optimizer.context.strategy = OptimizationStrategy.LATENCY
    
    @optimized(optimizer)
    async def latency_task(delay: float) -> float:
        await asyncio.sleep(delay)
        return delay
    
    start_time = time.time()
    result = await latency_task(0.1)
    execution_time = time.time() - start_time
    
    assert abs(result - 0.1) < 0.01
    assert execution_time >= 0.1
    
    metrics = optimizer.get_metrics()
    assert metrics["execution_time"] >= 0.1
