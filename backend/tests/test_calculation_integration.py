"""
Test Suite for Calculation Integration Layer
PGF Protocol: INT_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime
from app.core.integration.calculation_integration import (
    CalculationIntegrationLayer,
    IntegrationMetrics
)

@pytest.fixture
def integration_layer():
    return CalculationIntegrationLayer()

@pytest.fixture
def sample_calculation_input():
    return {
        "house": 1,
        "occupants": [{
            "name": "Sun",
            "strength": 70,
            "dignity": "own",
            "is_retrograde": False
        }],
        "aspects": [{
            "planet": "Jupiter",
            "strength": 80,
            "type": "trine",
            "is_applying": True
        }],
        "lord": {
            "planet": "Mars",
            "strength": 75,
            "house": 1,
            "dignity": "own"
        },
        "time_of_day": "day"
    }

@pytest.mark.asyncio
async def test_successful_calculation(integration_layer, sample_calculation_input):
    """Test successful calculation processing"""
    calculation_id = "test_calc_001"
    
    result = await integration_layer.process_calculation_request(
        calculation_id,
        sample_calculation_input
    )
    
    assert result["calculation_id"] == calculation_id
    assert result["status"] == "completed"
    assert "result" in result
    assert "validation" in result
    
    metrics = await integration_layer.get_metrics()
    assert metrics["request_count"] == 1
    assert metrics["success_rate"] == 1.0
    assert metrics["error_rate"] == 0.0

@pytest.mark.asyncio
async def test_error_handling(integration_layer):
    """Test error handling in calculation processing"""
    calculation_id = "test_calc_002"
    invalid_input = {"house": 1}  # Missing required fields
    
    with pytest.raises(ValueError):
        await integration_layer.process_calculation_request(
            calculation_id,
            invalid_input
        )
    
    metrics = await integration_layer.get_metrics()
    assert metrics["error_rate"] > 0

@pytest.mark.asyncio
async def test_concurrent_calculations(
    integration_layer,
    sample_calculation_input
):
    """Test concurrent calculation processing"""
    async def run_calculation(calc_id: str):
        return await integration_layer.process_calculation_request(
            calc_id,
            sample_calculation_input
        )
    
    # Run multiple calculations concurrently
    tasks = [
        run_calculation(f"concurrent_calc_{i}")
        for i in range(5)
    ]
    
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 5
    assert all(r["status"] == "completed" for r in results)
    
    metrics = await integration_layer.get_metrics()
    assert metrics["request_count"] == 5
    assert metrics["success_rate"] == 1.0

@pytest.mark.asyncio
async def test_metrics_tracking(integration_layer, sample_calculation_input):
    """Test metrics tracking functionality"""
    # Reset metrics
    await integration_layer.reset_metrics()
    
    # Process multiple calculations
    for i in range(3):
        await integration_layer.process_calculation_request(
            f"test_calc_{i+1}",
            sample_calculation_input
        )
    
    metrics = await integration_layer.get_metrics()
    
    assert metrics["request_count"] == 3
    assert metrics["success_rate"] == 1.0
    assert metrics["avg_response_time"] > 0
    assert metrics["peak_memory_usage"] > 0
    assert metrics["active_calculations"] == 0

@pytest.mark.asyncio
async def test_recovery_mechanism(integration_layer, sample_calculation_input):
    """Test recovery mechanism during calculation"""
    calculation_id = "test_calc_003"
    
    # Modify input to trigger recovery
    modified_input = {
        **sample_calculation_input,
        "trigger_recovery": True  # This should trigger recovery path
    }
    
    result = await integration_layer.process_calculation_request(
        calculation_id,
        modified_input
    )
    
    assert result["calculation_id"] == calculation_id
    assert result["status"] == "completed"
    
    metrics = await integration_layer.get_metrics()
    assert metrics["success_rate"] > 0

@pytest.mark.asyncio
async def test_validation_integration(
    integration_layer,
    sample_calculation_input
):
    """Test validation integration"""
    calculation_id = "test_calc_004"
    
    result = await integration_layer.process_calculation_request(
        calculation_id,
        sample_calculation_input
    )
    
    assert "validation" in result
    assert result["validation"]["validation_status"] == "PASSED"

@pytest.mark.asyncio
async def test_performance_metrics(integration_layer, sample_calculation_input):
    """Test performance metrics tracking"""
    # Reset metrics
    await integration_layer.reset_metrics()
    
    start_time = datetime.now()
    
    # Process calculation
    await integration_layer.process_calculation_request(
        "test_calc_005",
        sample_calculation_input
    )
    
    metrics = await integration_layer.get_metrics()
    
    assert metrics["avg_response_time"] > 0
    assert metrics["avg_response_time"] < 1.0  # Should complete within 1 second
    assert metrics["peak_memory_usage"] > 0

@pytest.mark.asyncio
async def test_metrics_reset(integration_layer, sample_calculation_input):
    """Test metrics reset functionality"""
    # Process a calculation
    await integration_layer.process_calculation_request(
        "test_calc_006",
        sample_calculation_input
    )
    
    # Reset metrics
    await integration_layer.reset_metrics()
    
    metrics = await integration_layer.get_metrics()
    assert metrics["request_count"] == 0
    assert metrics["success_rate"] == 0
    assert metrics["error_rate"] == 0
    assert metrics["avg_response_time"] == 0.0
    assert metrics["active_calculations"] == 0
