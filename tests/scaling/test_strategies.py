"""
Service Scaling Strategy Tests
PGF Protocol: SCAL_007
Gate: GATE_38
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime
from app.core.scaling.strategies import (
    ScalingMode,
    HorizontalScaling,
    VerticalScaling,
    HybridScaling
)

@pytest.fixture
def horizontal_scaling():
    """Horizontal scaling fixture"""
    return HorizontalScaling()

@pytest.fixture
def vertical_scaling():
    """Vertical scaling fixture"""
    return VerticalScaling()

@pytest.fixture
def hybrid_scaling():
    """Hybrid scaling fixture"""
    return HybridScaling()

@pytest.mark.asyncio
async def test_horizontal_scaling_up(horizontal_scaling):
    """Test horizontal scaling up"""
    # Arrange
    current_replicas = 2
    target_replicas = 4
    
    # Act
    result = await horizontal_scaling.scale_up(
        current_replicas,
        target_replicas
    )
    
    # Assert
    assert result["status"] == "success"
    assert result["replicas"] == target_replicas
    assert result["timestamp"] <= datetime.utcnow()

@pytest.mark.asyncio
async def test_horizontal_scaling_down(horizontal_scaling):
    """Test horizontal scaling down"""
    # Arrange
    current_replicas = 4
    target_replicas = 2
    
    # Act
    result = await horizontal_scaling.scale_down(
        current_replicas,
        target_replicas
    )
    
    # Assert
    assert result["status"] == "success"
    assert result["replicas"] == target_replicas
    assert result["timestamp"] <= datetime.utcnow()

@pytest.mark.asyncio
async def test_vertical_scaling_up(vertical_scaling):
    """Test vertical scaling up"""
    # Arrange
    current_resources = {
        "cpu": 1.0,
        "memory": 1024
    }
    target_resources = {
        "cpu": 2.0,
        "memory": 2048
    }
    
    # Act
    result = await vertical_scaling.scale_up(
        current_resources,
        target_resources
    )
    
    # Assert
    assert result["status"] == "success"
    assert result["resources"] == target_resources
    assert result["timestamp"] <= datetime.utcnow()

@pytest.mark.asyncio
async def test_vertical_scaling_down(vertical_scaling):
    """Test vertical scaling down"""
    # Arrange
    current_resources = {
        "cpu": 2.0,
        "memory": 2048
    }
    target_resources = {
        "cpu": 1.0,
        "memory": 1024
    }
    
    # Act
    result = await vertical_scaling.scale_down(
        current_resources,
        target_resources
    )
    
    # Assert
    assert result["status"] == "success"
    assert result["resources"] == target_resources
    assert result["timestamp"] <= datetime.utcnow()

@pytest.mark.asyncio
async def test_hybrid_scaling_up(hybrid_scaling):
    """Test hybrid scaling up"""
    # Arrange
    current_state = {
        "replicas": 2,
        "resources": {
            "cpu": 1.0,
            "memory": 1024
        }
    }
    target_state = {
        "replicas": 4,
        "resources": {
            "cpu": 2.0,
            "memory": 2048
        }
    }
    
    # Act
    result = await hybrid_scaling.scale_up(
        current_state,
        target_state
    )
    
    # Assert
    assert result["status"] == "success"
    assert result["replicas"] == target_state["replicas"]
    assert result["resources"] == target_state["resources"]
    assert result["timestamp"] <= datetime.utcnow()

@pytest.mark.asyncio
async def test_hybrid_scaling_down(hybrid_scaling):
    """Test hybrid scaling down"""
    # Arrange
    current_state = {
        "replicas": 4,
        "resources": {
            "cpu": 2.0,
            "memory": 2048
        }
    }
    target_state = {
        "replicas": 2,
        "resources": {
            "cpu": 1.0,
            "memory": 1024
        }
    }
    
    # Act
    result = await hybrid_scaling.scale_down(
        current_state,
        target_state
    )
    
    # Assert
    assert result["status"] == "success"
    assert result["replicas"] == target_state["replicas"]
    assert result["resources"] == target_state["resources"]
    assert result["timestamp"] <= datetime.utcnow()

@pytest.mark.asyncio
async def test_invalid_scaling_mode():
    """Test invalid scaling mode"""
    # Arrange
    mode = "invalid"
    
    # Act & Assert
    with pytest.raises(ValueError):
        ScalingMode(mode)

@pytest.mark.asyncio
async def test_horizontal_scaling_invalid_replicas(horizontal_scaling):
    """Test horizontal scaling with invalid replicas"""
    # Arrange
    current_replicas = 2
    target_replicas = -1
    
    # Act & Assert
    with pytest.raises(ValueError):
        await horizontal_scaling.scale_up(
            current_replicas,
            target_replicas
        )

@pytest.mark.asyncio
async def test_vertical_scaling_invalid_resources(vertical_scaling):
    """Test vertical scaling with invalid resources"""
    # Arrange
    current_resources = {
        "cpu": 1.0,
        "memory": 1024
    }
    target_resources = {
        "cpu": -1.0,
        "memory": -1024
    }
    
    # Act & Assert
    with pytest.raises(ValueError):
        await vertical_scaling.scale_up(
            current_resources,
            target_resources
        )

@pytest.mark.asyncio
async def test_hybrid_scaling_invalid_state(hybrid_scaling):
    """Test hybrid scaling with invalid state"""
    # Arrange
    current_state = {
        "replicas": 2,
        "resources": {
            "cpu": 1.0,
            "memory": 1024
        }
    }
    target_state = {
        "replicas": -1,
        "resources": {
            "cpu": -1.0,
            "memory": -1024
        }
    }
    
    # Act & Assert
    with pytest.raises(ValueError):
        await hybrid_scaling.scale_up(
            current_state,
            target_state
        )
