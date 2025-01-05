"""
Test Suite for House Analysis Validation Framework
PGF Protocol: VCI_002
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime
from app.core.validation.house_analysis_validator import (
    HouseAnalysisValidator,
    ValidationMetrics,
    ValidationThresholds
)

@pytest.fixture
def validator():
    return HouseAnalysisValidator()

@pytest.fixture
def test_cases():
    return [
        {
            'house': 1,
            'occupants': [{
                'name': 'Sun',
                'strength': 70,
                'dignity': 'own',
                'is_retrograde': False
            }],
            'aspects': [{
                'planet': 'Jupiter',
                'strength': 80,
                'type': 'trine',
                'is_applying': True
            }],
            'lord': {
                'planet': 'Mars',
                'strength': 75,
                'house': 1,
                'dignity': 'own'
            },
            'time_of_day': 'day',
            'expected_strength': 85.0,
            'tolerance': 5.0
        },
        {
            'house': 8,
            'occupants': [{
                'name': 'Saturn',
                'strength': 40,
                'dignity': 'debilitated',
                'is_retrograde': True,
                'is_combust': True
            }],
            'aspects': [{
                'planet': 'Mars',
                'strength': 60,
                'type': 'square',
                'is_applying': False
            }],
            'lord': {
                'planet': 'Mars',
                'strength': 45,
                'house': 12,
                'dignity': 'enemy'
            },
            'time_of_day': 'night',
            'expected_strength': 35.0,
            'tolerance': 5.0
        }
    ]

@pytest.mark.asyncio
async def test_validation_metrics(validator, test_cases):
    """Test validation metrics calculation"""
    metrics = await validator.validate_house_analysis(test_cases)
    
    assert metrics.accuracy > 0
    assert metrics.precision > 0
    assert metrics.recall > 0
    assert metrics.execution_time > 0
    assert metrics.resource_usage
    assert metrics.validation_status in ['PASSED', 'WARNING', 'FAILED']

@pytest.mark.asyncio
async def test_validation_thresholds(validator, test_cases):
    """Test validation threshold enforcement"""
    # Modify thresholds to force warning
    validator.thresholds = ValidationThresholds(
        min_accuracy=99.9,
        min_precision=99.9,
        min_recall=99.9,
        max_execution_time=1.0,
        max_memory_usage=1.0
    )
    
    metrics = await validator.validate_house_analysis(test_cases)
    assert metrics.validation_status in ['WARNING', 'FAILED']

@pytest.mark.asyncio
async def test_resource_monitoring(validator):
    """Test resource usage monitoring"""
    resource_usage = validator._get_resource_usage()
    
    assert 'memory_mb' in resource_usage
    assert 'cpu_percent' in resource_usage
    assert 'thread_count' in resource_usage
    assert 'open_files' in resource_usage
    
    assert resource_usage['memory_mb'] > 0
    assert resource_usage['thread_count'] > 0

@pytest.mark.asyncio
async def test_trend_analysis(validator, test_cases):
    """Test validation trend analysis"""
    # Run multiple validations
    for _ in range(3):
        await validator.validate_house_analysis(test_cases)
    
    trends = validator.get_trend_analysis()
    
    assert 'accuracy_trend' in trends
    assert 'precision_trend' in trends
    assert 'recall_trend' in trends
    assert 'performance_trend' in trends
    
    for metric in trends.values():
        assert 'mean' in metric
        assert 'std' in metric
        assert 'trend' in metric
        assert metric['trend'] in ['improving', 'declining']

@pytest.mark.asyncio
async def test_validation_history(validator, test_cases):
    """Test validation history tracking"""
    # Run multiple validations
    for _ in range(5):
        await validator.validate_house_analysis(test_cases)
    
    history = validator.get_validation_history()
    limited_history = validator.get_validation_history(limit=3)
    
    assert len(history) == 5
    assert len(limited_history) == 3
    assert all(isinstance(m, ValidationMetrics) for m in history)

@pytest.mark.asyncio
async def test_error_handling(validator):
    """Test error handling in validation"""
    # Test with invalid test case
    invalid_test_cases = [{
        'house': 1,
        'occupants': None,  # Invalid occupants
        'aspects': [],
        'lord': {},
        'expected_strength': 50.0
    }]
    
    metrics = await validator.validate_house_analysis(invalid_test_cases)
    
    assert metrics.validation_status == 'FAILED'
    assert metrics.error_details is not None
    assert len(metrics.error_details) > 0

@pytest.mark.asyncio
async def test_concurrent_validation(validator, test_cases):
    """Test concurrent validation handling"""
    # Run multiple validations concurrently
    tasks = [
        validator.validate_house_analysis(test_cases)
        for _ in range(5)
    ]
    
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 5
    assert all(isinstance(r, ValidationMetrics) for r in results)
    assert all(r.validation_status for r in results)
