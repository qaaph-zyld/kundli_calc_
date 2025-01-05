"""
Service Scaling Integration Tests
PGF Protocol: SCAL_007
Gate: GATE_38
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime
from fastapi.testclient import TestClient
from app.core.scaling.integration import (
    ScalingIntegration,
    IntegrationMode,
    IntegrationStatus
)

@pytest.fixture
def integration():
    """Integration fixture"""
    return ScalingIntegration(
        mode=IntegrationMode.STANDALONE,
        config_path="tests/scaling/config/test_config.json"
    )

@pytest.fixture
def client(integration):
    """Test client fixture"""
    return TestClient(integration.api)

@pytest.mark.asyncio
async def test_integration_initialization(integration):
    """Test integration initialization"""
    # Assert
    assert integration.mode == IntegrationMode.STANDALONE
    assert integration.status == IntegrationStatus.INITIALIZING
    assert integration.metrics is not None

@pytest.mark.asyncio
async def test_integration_start(integration):
    """Test integration start"""
    # Act
    await integration.start()
    
    # Assert
    assert integration.status == IntegrationStatus.READY
    assert integration.metrics.current_status == IntegrationStatus.READY

@pytest.mark.asyncio
async def test_integration_scale(integration):
    """Test integration scale"""
    # Arrange
    await integration.start()
    request = {
        "mode": "horizontal",
        "replicas": 3
    }
    
    # Act
    result = await integration.scale(request)
    
    # Assert
    assert result["status"] == "success"
    assert result["platform"] == "standalone"
    assert result["timestamp"] <= datetime.utcnow()

def test_health_check(client):
    """Test health check endpoint"""
    # Act
    response = client.get("/health")
    
    # Assert
    assert response.status_code == 200
    assert "status" in response.json()
    assert "timestamp" in response.json()

def test_get_metrics(client):
    """Test get metrics endpoint"""
    # Act
    response = client.get("/metrics")
    
    # Assert
    assert response.status_code == 200
    assert "integration" in response.json()
    assert "monitoring" in response.json()

def test_trigger_scaling(client):
    """Test trigger scaling endpoint"""
    # Arrange
    request = {
        "mode": "horizontal",
        "replicas": 3
    }
    
    # Act
    response = client.post("/scale", json=request)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_config(client):
    """Test get configuration endpoint"""
    # Act
    response = client.get("/config")
    
    # Assert
    assert response.status_code == 200
    assert "mode" in response.json()
    assert "resources" in response.json()
    assert "replicas" in response.json()

def test_update_config(client):
    """Test update configuration endpoint"""
    # Arrange
    config = {
        "mode": "hybrid",
        "resources": {
            "min_cpu": 0.1,
            "max_cpu": 4.0
        }
    }
    
    # Act
    response = client.post("/config", json=config)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_get_validation(client):
    """Test get validation endpoint"""
    # Act
    response = client.get("/validation")
    
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_invalid_scaling_request(client):
    """Test invalid scaling request"""
    # Arrange
    request = {
        "mode": "invalid",
        "replicas": -1
    }
    
    # Act
    response = client.post("/scale", json=request)
    
    # Assert
    assert response.status_code == 500
    assert "detail" in response.json()

def test_invalid_config_update(client):
    """Test invalid configuration update"""
    # Arrange
    config = {
        "mode": "invalid",
        "resources": {
            "min_cpu": -1,
            "max_cpu": -4.0
        }
    }
    
    # Act
    response = client.post("/config", json=config)
    
    # Assert
    assert response.status_code == 500
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_integration_error_handling(integration):
    """Test integration error handling"""
    # Arrange
    await integration.start()
    request = {
        "mode": "invalid",
        "replicas": -1
    }
    
    # Act & Assert
    with pytest.raises(ValueError):
        await integration.scale(request)
    
    assert integration.status == IntegrationStatus.ERROR
    assert integration.metrics.current_status == IntegrationStatus.ERROR

@pytest.mark.asyncio
async def test_integration_metrics_update(integration):
    """Test integration metrics update"""
    # Arrange
    await integration.start()
    request = {
        "mode": "horizontal",
        "replicas": 3
    }
    
    # Act
    await integration.scale(request)
    
    # Assert
    assert integration.metrics.total_operations == 1
    assert integration.metrics.successful_operations == 1
    assert integration.metrics.failed_operations == 0
    assert integration.metrics.average_latency >= 0.0
    assert integration.metrics.last_operation_time <= datetime.utcnow()
