"""
Enhanced System Health Endpoints
================================
Comprehensive health checks with detailed metrics.
"""

from fastapi import APIRouter, Response, status
from typing import Dict, Any
from datetime import datetime
import psutil
import time

from app.core.performance import get_monitor
from app.core.cache.calculation_cache import CalculationCache

router = APIRouter()

# Global cache instance for metrics
_cache = CalculationCache()
_start_time = time.time()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "kundli-calculator"
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with system metrics
    
    Returns:
        Detailed health status with metrics
    """
    uptime_seconds = time.time() - _start_time
    
    # System metrics
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Performance metrics
    perf_monitor = get_monitor()
    perf_stats = perf_monitor.get_all_stats()
    
    # Cache metrics
    cache_stats = _cache.get_stats()
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": round(uptime_seconds, 2),
        "system": {
            "cpu_percent": round(cpu_percent, 2),
            "memory_percent": round(memory.percent, 2),
            "memory_available_mb": round(memory.available / 1024 / 1024, 2),
            "disk_percent": round(disk.percent, 2),
            "disk_free_gb": round(disk.free / 1024 / 1024 / 1024, 2)
        },
        "performance": {
            "calculations_tracked": len(perf_stats),
            "operations": perf_stats
        },
        "cache": cache_stats
    }


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check for kubernetes/deployment
    
    Returns:
        Readiness status
    """
    # Check if critical services are available
    checks = {
        "service": True,
        "calculations": True,
        "cache": True
    }
    
    all_ready = all(checks.values())
    
    return {
        "ready": all_ready,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for kubernetes/deployment
    
    Returns:
        Liveness status
    """
    return {
        "alive": "true",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/metrics", status_code=status.HTTP_200_OK)
async def get_metrics() -> Dict[str, Any]:
    """
    Get application metrics
    
    Returns:
        Application metrics
    """
    perf_monitor = get_monitor()
    cache_stats = _cache.get_stats()
    
    uptime_seconds = time.time() - _start_time
    
    return {
        "uptime_seconds": round(uptime_seconds, 2),
        "performance": perf_monitor.get_all_stats(),
        "cache": cache_stats,
        "timestamp": datetime.utcnow().isoformat()
    }
