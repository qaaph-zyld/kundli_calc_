"""
Test Suite for Load Balancing Module
PGF Protocol: LB_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
import time
from datetime import datetime
from app.core.balancing.load_balancer import (
    LoadBalancer,
    Worker,
    BalancingStrategy,
    WorkerMetrics
)

@pytest.fixture
def load_balancer():
    return LoadBalancer(
        strategy=BalancingStrategy.ADAPTIVE,
        max_workers=5,
        tasks_per_worker=5
    )

async def dummy_task(duration: float = 0.1) -> str:
    """Dummy task for testing"""
    await asyncio.sleep(duration)
    return "completed"

@pytest.mark.asyncio
async def test_worker_task_processing():
    """Test worker task processing"""
    worker = Worker("test_worker", max_concurrent_tasks=5)
    
    # Process task
    result = await worker.process_task(
        "task_1",
        dummy_task,
        0.1
    )
    
    assert result == "completed"
    metrics = worker.get_metrics()
    assert metrics["completed_tasks"] == 1
    assert metrics["active_tasks"] == 0
    assert metrics["failed_tasks"] == 0
    assert metrics["avg_response_time"] > 0

@pytest.mark.asyncio
async def test_worker_concurrent_tasks():
    """Test worker concurrent task handling"""
    worker = Worker("test_worker", max_concurrent_tasks=5)
    
    # Start multiple tasks
    tasks = [
        worker.process_task(f"task_{i}", dummy_task, 0.1)
        for i in range(3)
    ]
    
    results = await asyncio.gather(*tasks)
    
    assert all(r == "completed" for r in results)
    metrics = worker.get_metrics()
    assert metrics["completed_tasks"] == 3
    assert metrics["active_tasks"] == 0

@pytest.mark.asyncio
async def test_worker_error_handling():
    """Test worker error handling"""
    worker = Worker("test_worker", max_concurrent_tasks=5)
    
    async def failing_task():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        await worker.process_task("task_1", failing_task)
    
    metrics = worker.get_metrics()
    assert metrics["failed_tasks"] == 1
    assert metrics["active_tasks"] == 0

@pytest.mark.asyncio
async def test_round_robin_strategy(load_balancer):
    """Test round-robin load balancing"""
    load_balancer.strategy = BalancingStrategy.ROUND_ROBIN
    
    # Process multiple tasks
    tasks = [
        load_balancer.process_task(f"task_{i}", dummy_task, 0.1)
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    assert all(r == "completed" for r in results)
    
    metrics = await load_balancer.get_metrics()
    assert metrics["total_completed_tasks"] == 10
    
    # Verify distribution
    worker_tasks = [
        w.metrics.completed_tasks
        for w in load_balancer.workers.values()
    ]
    assert max(worker_tasks) - min(worker_tasks) <= 1

@pytest.mark.asyncio
async def test_least_connections_strategy(load_balancer):
    """Test least connections strategy"""
    load_balancer.strategy = BalancingStrategy.LEAST_CONNECTIONS
    
    # Process tasks with varying durations
    tasks = [
        load_balancer.process_task(f"task_{i}", dummy_task, 0.1 * (i % 3 + 1))
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    assert all(r == "completed" for r in results)
    
    metrics = await load_balancer.get_metrics()
    assert metrics["total_completed_tasks"] == 10

@pytest.mark.asyncio
async def test_resource_aware_strategy(load_balancer):
    """Test resource-aware strategy"""
    load_balancer.strategy = BalancingStrategy.RESOURCE_AWARE
    
    # Process resource-intensive tasks
    async def resource_task():
        # Simulate CPU usage
        start = time.time()
        while time.time() - start < 0.1:
            _ = [i * i for i in range(1000)]
        return "completed"
    
    tasks = [
        load_balancer.process_task(f"task_{i}", resource_task)
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    assert all(r == "completed" for r in results)
    
    metrics = await load_balancer.get_metrics()
    assert metrics["avg_cpu_usage"] > 0

@pytest.mark.asyncio
async def test_adaptive_strategy(load_balancer):
    """Test adaptive strategy"""
    load_balancer.strategy = BalancingStrategy.ADAPTIVE
    
    # Process mixed workload
    tasks = []
    
    # Fast tasks
    tasks.extend([
        load_balancer.process_task(f"fast_task_{i}", dummy_task, 0.1)
        for i in range(5)
    ])
    
    # Slow tasks
    tasks.extend([
        load_balancer.process_task(f"slow_task_{i}", dummy_task, 0.3)
        for i in range(5)
    ])
    
    results = await asyncio.gather(*tasks)
    assert all(r == "completed" for r in results)
    
    metrics = await load_balancer.get_metrics()
    assert metrics["total_completed_tasks"] == 10

@pytest.mark.asyncio
async def test_worker_overload_prevention(load_balancer):
    """Test worker overload prevention"""
    worker = list(load_balancer.workers.values())[0]
    
    # Create more tasks than worker capacity
    tasks = [
        worker.process_task(f"task_{i}", dummy_task, 0.1)
        for i in range(worker.max_concurrent_tasks + 5)
    ]
    
    results = await asyncio.gather(*tasks)
    assert all(r == "completed" for r in results)
    
    metrics = worker.get_metrics()
    assert metrics["active_tasks"] <= worker.max_concurrent_tasks

@pytest.mark.asyncio
async def test_metrics_accuracy(load_balancer):
    """Test metrics accuracy"""
    # Process some tasks
    tasks = [
        load_balancer.process_task(f"task_{i}", dummy_task, 0.1)
        for i in range(5)
    ]
    
    await asyncio.gather(*tasks)
    
    metrics = await load_balancer.get_metrics()
    
    assert metrics["total_completed_tasks"] == 5
    assert metrics["total_failed_tasks"] == 0
    assert metrics["avg_response_time"] > 0
    assert metrics["avg_cpu_usage"] >= 0
    assert metrics["avg_memory_usage"] >= 0
    assert metrics["active_workers"] >= 0

@pytest.mark.asyncio
async def test_worker_recovery(load_balancer):
    """Test worker recovery after errors"""
    async def failing_task():
        raise ValueError("Test error")
    
    # Process some failing tasks
    tasks = [
        load_balancer.process_task(f"fail_task_{i}", failing_task)
        for i in range(3)
    ]
    
    for task in tasks:
        with pytest.raises(ValueError):
            await task
    
    # Process successful tasks
    tasks = [
        load_balancer.process_task(f"task_{i}", dummy_task, 0.1)
        for i in range(3)
    ]
    
    results = await asyncio.gather(*tasks)
    assert all(r == "completed" for r in results)
    
    metrics = await load_balancer.get_metrics()
    assert metrics["total_completed_tasks"] == 3
    assert metrics["total_failed_tasks"] == 3
