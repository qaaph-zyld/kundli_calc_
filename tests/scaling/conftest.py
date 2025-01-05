"""
Service Scaling Test Configuration
PGF Protocol: SCAL_007
Gate: GATE_38
Version: 1.0.0
"""

import pytest
import asyncio
import json
import os
from datetime import datetime

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def test_config():
    """Create test configuration"""
    config = {
        "mode": "hybrid",
        "resources": {
            "min_cpu": 0.1,
            "max_cpu": 4.0,
            "min_memory": 128,
            "max_memory": 8192,
            "cpu_request": 0.5,
            "memory_request": 512,
            "cpu_limit": 2.0,
            "memory_limit": 4096
        },
        "replicas": {
            "min_replicas": 1,
            "max_replicas": 10,
            "target_replicas": 2,
            "scale_up_threshold": 0.8,
            "scale_down_threshold": 0.2
        }
    }
    
    # Create config directory if not exists
    os.makedirs("tests/scaling/config", exist_ok=True)
    
    # Write config file
    with open("tests/scaling/config/test_config.json", "w") as f:
        json.dump(config, f, indent=4)
    
    yield config
    
    # Cleanup
    os.remove("tests/scaling/config/test_config.json")
    os.rmdir("tests/scaling/config")

@pytest.fixture(scope="session")
def test_metrics():
    """Create test metrics"""
    return {
        "cpu_usage": 0.6,
        "memory_usage": 0.4,
        "request_count": 1000,
        "average_latency": 0.2,
        "timestamp": datetime.utcnow()
    }

@pytest.fixture(scope="session")
def test_validation_results():
    """Create test validation results"""
    return [
        {
            "scope": "configuration",
            "status": "passed",
            "message": "Configuration validation passed",
            "timestamp": datetime.utcnow(),
            "details": {}
        },
        {
            "scope": "resources",
            "status": "warning",
            "message": "CPU usage outside limits",
            "timestamp": datetime.utcnow(),
            "details": {
                "component": "cpu"
            }
        }
    ]
