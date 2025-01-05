"""
Load Balancing Module
PGF Protocol: LB_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass
import asyncio
import logging
from datetime import datetime
import heapq
from concurrent.futures import ThreadPoolExecutor
import psutil
import threading
from enum import Enum

class BalancingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    RESOURCE_AWARE = "resource_aware"
    ADAPTIVE = "adaptive"

@dataclass
class WorkerMetrics:
    """Metrics for a worker node"""
    active_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    avg_response_time: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    last_heartbeat: Optional[datetime] = None

class Worker:
    """Represents a worker node for processing calculations"""
    
    def __init__(
        self,
        worker_id: str,
        max_concurrent_tasks: int = 10
    ):
        self.worker_id = worker_id
        self.max_concurrent_tasks = max_concurrent_tasks
        self.metrics = WorkerMetrics()
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
    
    async def process_task(
        self,
        task_id: str,
        task_func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Process a task with metrics tracking"""
        start_time = datetime.now()
        
        with self.lock:
            self.metrics.active_tasks += 1
            self.metrics.last_heartbeat = datetime.now()
        
        try:
            # Execute task in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                lambda: task_func(*args, **kwargs)
            )
            
            # Update success metrics
            with self.lock:
                self.metrics.completed_tasks += 1
                execution_time = (
                    datetime.now() - start_time
                ).total_seconds()
                
                # Update average response time
                if self.metrics.completed_tasks == 1:
                    self.metrics.avg_response_time = execution_time
                else:
                    self.metrics.avg_response_time = (
                        (self.metrics.avg_response_time *
                         (self.metrics.completed_tasks - 1) +
                         execution_time) /
                        self.metrics.completed_tasks
                    )
            
            return result
            
        except Exception as e:
            # Update failure metrics
            with self.lock:
                self.metrics.failed_tasks += 1
            self.logger.error(
                f"Task {task_id} failed on worker {self.worker_id}: {str(e)}"
            )
            raise
            
        finally:
            # Update resource metrics
            with self.lock:
                self.metrics.active_tasks -= 1
                self.metrics.cpu_usage = psutil.cpu_percent()
                self.metrics.memory_usage = psutil.Process().memory_info().rss / (
                    1024 * 1024
                )
    
    def get_load_factor(self) -> float:
        """Calculate worker load factor"""
        with self.lock:
            # Consider multiple factors with weights
            active_factor = self.metrics.active_tasks / self.max_concurrent_tasks
            cpu_factor = self.metrics.cpu_usage / 100
            memory_factor = min(self.metrics.memory_usage / 1000, 1.0)  # Cap at 1GB
            
            # Weighted average
            return (0.4 * active_factor +
                   0.3 * cpu_factor +
                   0.3 * memory_factor)
    
    def is_available(self) -> bool:
        """Check if worker can accept new tasks"""
        with self.lock:
            return (
                self.metrics.active_tasks < self.max_concurrent_tasks and
                self.metrics.cpu_usage < 80 and
                self.metrics.memory_usage < 800  # 800MB limit
            )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current worker metrics"""
        with self.lock:
            return {
                "worker_id": self.worker_id,
                "active_tasks": self.metrics.active_tasks,
                "completed_tasks": self.metrics.completed_tasks,
                "failed_tasks": self.metrics.failed_tasks,
                "avg_response_time": self.metrics.avg_response_time,
                "cpu_usage": self.metrics.cpu_usage,
                "memory_usage": self.metrics.memory_usage,
                "last_heartbeat": self.metrics.last_heartbeat
            }

class LoadBalancer:
    """Load balancer for distributing calculation tasks"""
    
    def __init__(
        self,
        strategy: BalancingStrategy = BalancingStrategy.ADAPTIVE,
        max_workers: int = 10,
        tasks_per_worker: int = 10
    ):
        self.strategy = strategy
        self.max_workers = max_workers
        self.tasks_per_worker = tasks_per_worker
        self.workers: Dict[str, Worker] = {}
        self.current_worker_idx = 0
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        
        # Initialize workers
        for i in range(max_workers):
            worker = Worker(
                f"worker_{i}",
                max_concurrent_tasks=tasks_per_worker
            )
            self.workers[worker.worker_id] = worker
    
    async def process_task(
        self,
        task_id: str,
        task_func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Process task using selected worker"""
        worker = await self._select_worker()
        if not worker:
            raise RuntimeError("No available workers")
        
        return await worker.process_task(task_id, task_func, *args, **kwargs)
    
    async def _select_worker(self) -> Optional[Worker]:
        """Select worker based on strategy"""
        with self.lock:
            if self.strategy == BalancingStrategy.ROUND_ROBIN:
                return self._select_round_robin()
            elif self.strategy == BalancingStrategy.LEAST_CONNECTIONS:
                return self._select_least_connections()
            elif self.strategy == BalancingStrategy.RESOURCE_AWARE:
                return self._select_resource_aware()
            else:  # ADAPTIVE
                return self._select_adaptive()
    
    def _select_round_robin(self) -> Optional[Worker]:
        """Select worker using round-robin"""
        start_idx = self.current_worker_idx
        
        while True:
            worker_id = f"worker_{self.current_worker_idx}"
            worker = self.workers[worker_id]
            
            self.current_worker_idx = (
                self.current_worker_idx + 1
            ) % self.max_workers
            
            if worker.is_available():
                return worker
            
            if self.current_worker_idx == start_idx:
                return None
    
    def _select_least_connections(self) -> Optional[Worker]:
        """Select worker with least active connections"""
        available_workers = [
            w for w in self.workers.values()
            if w.is_available()
        ]
        
        if not available_workers:
            return None
        
        return min(
            available_workers,
            key=lambda w: w.metrics.active_tasks
        )
    
    def _select_resource_aware(self) -> Optional[Worker]:
        """Select worker based on resource usage"""
        available_workers = [
            w for w in self.workers.values()
            if w.is_available()
        ]
        
        if not available_workers:
            return None
        
        return min(
            available_workers,
            key=lambda w: w.get_load_factor()
        )
    
    def _select_adaptive(self) -> Optional[Worker]:
        """Select worker using adaptive strategy"""
        available_workers = [
            w for w in self.workers.values()
            if w.is_available()
        ]
        
        if not available_workers:
            return None
        
        # Consider multiple factors
        scored_workers = [
            (w, self._calculate_worker_score(w))
            for w in available_workers
        ]
        
        return max(scored_workers, key=lambda x: x[1])[0]
    
    def _calculate_worker_score(self, worker: Worker) -> float:
        """Calculate worker score for adaptive selection"""
        metrics = worker.get_metrics()
        
        # Performance score
        perf_score = 1.0 / (1.0 + metrics["avg_response_time"])
        
        # Resource score
        resource_score = 1.0 - worker.get_load_factor()
        
        # Reliability score
        total_tasks = (
            metrics["completed_tasks"] +
            metrics["failed_tasks"]
        )
        reliability_score = (
            metrics["completed_tasks"] / total_tasks
            if total_tasks > 0
            else 1.0
        )
        
        # Weighted score
        return (0.4 * perf_score +
                0.4 * resource_score +
                0.2 * reliability_score)
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get load balancer metrics"""
        total_active = 0
        total_completed = 0
        total_failed = 0
        avg_response_times = []
        avg_cpu_usage = 0
        avg_memory_usage = 0
        
        for worker in self.workers.values():
            metrics = worker.get_metrics()
            total_active += metrics["active_tasks"]
            total_completed += metrics["completed_tasks"]
            total_failed += metrics["failed_tasks"]
            if metrics["avg_response_time"] > 0:
                avg_response_times.append(metrics["avg_response_time"])
            avg_cpu_usage += metrics["cpu_usage"]
            avg_memory_usage += metrics["memory_usage"]
        
        worker_count = len(self.workers)
        
        return {
            "total_active_tasks": total_active,
            "total_completed_tasks": total_completed,
            "total_failed_tasks": total_failed,
            "avg_response_time": (
                sum(avg_response_times) / len(avg_response_times)
                if avg_response_times
                else 0
            ),
            "avg_cpu_usage": avg_cpu_usage / worker_count,
            "avg_memory_usage": avg_memory_usage / worker_count,
            "active_workers": sum(
                1 for w in self.workers.values()
                if w.metrics.active_tasks > 0
            )
        }
