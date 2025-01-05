"""
Test Suite for Validation Framework
PGF Protocol: VAL_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime
from app.core.validation.validation_framework import (
    ValidationFramework,
    ValidationRule,
    ValidationResult,
    ValidationError,
    ValidationLevel,
    ValidationScope,
    ValidationType,
    validate_input
)

@pytest.fixture
def framework():
    return ValidationFramework(default_level=ValidationLevel.STANDARD)

@pytest.fixture
def sample_data():
    return {
        "datetime": "2024-01-01T12:00:00Z",
        "planets": {
            "Sun": {
                "longitude": 280.5,
                "latitude": 0.0,
                "speed": 1.0
            },
            "Moon": {
                "longitude": 120.3,
                "latitude": 5.0,
                "speed": 13.2
            }
        },
        "calculations": {
            "houses": {
                1: {"angle": 30},
                2: {"angle": 60},
                3: {"angle": 90},
                4: {"angle": 120},
                5: {"angle": 150},
                6: {"angle": 180},
                7: {"angle": 210},
                8: {"angle": 240},
                9: {"angle": 270},
                10: {"angle": 300},
                11: {"angle": 330},
                12: {"angle": 360}
            },
            "aspects": [
                {
                    "planets": ["Sun", "Moon"],
                    "angle": 120,
                    "orb": 2
                }
            ]
        },
        "ayanamsa": 23.5,
        "system_resources": {
            "memory_usage": 60,
            "cpu_usage": 70
        }
    }

@pytest.mark.asyncio
async def test_validation_initialization(framework):
    """Test validation framework initialization"""
    assert framework.rules
    assert framework.default_level == ValidationLevel.STANDARD
    assert not framework.results

@pytest.mark.asyncio
async def test_planetary_coordinates_validation(framework, sample_data):
    """Test planetary coordinates validation"""
    results = await framework.validate(
        sample_data,
        scope=ValidationScope.INPUT
    )
    
    planetary_results = [
        r for r in results
        if r.rule_name == "planetary_coordinates"
    ]
    assert planetary_results
    assert planetary_results[0].is_valid

@pytest.mark.asyncio
async def test_datetime_validation(framework, sample_data):
    """Test datetime validation"""
    results = await framework.validate(
        sample_data,
        scope=ValidationScope.INPUT
    )
    
    datetime_results = [
        r for r in results
        if r.rule_name == "date_time_format"
    ]
    assert datetime_results
    assert datetime_results[0].is_valid

@pytest.mark.asyncio
async def test_calculation_consistency(framework, sample_data):
    """Test calculation consistency validation"""
    results = await framework.validate(
        sample_data,
        scope=ValidationScope.CALCULATION
    )
    
    consistency_results = [
        r for r in results
        if r.rule_name == "calculation_consistency"
    ]
    assert consistency_results
    assert consistency_results[0].is_valid

@pytest.mark.asyncio
async def test_ayanamsa_range(framework, sample_data):
    """Test ayanamsa range validation"""
    results = await framework.validate(
        sample_data,
        scope=ValidationScope.CALCULATION
    )
    
    ayanamsa_results = [
        r for r in results
        if r.rule_name == "ayanamsa_range"
    ]
    assert ayanamsa_results
    assert ayanamsa_results[0].is_valid

@pytest.mark.asyncio
async def test_output_completeness(framework, sample_data):
    """Test output completeness validation"""
    # Add required output sections
    complete_data = {
        **sample_data,
        "planets": {
            "Sun": {"position": {"longitude": 0}},
            "Moon": {"position": {"longitude": 180}}
        },
        "houses": {
            1: {"cusp": 0},
            7: {"cusp": 180}
        },
        "aspects": [],
        "calculations": {}
    }
    
    results = await framework.validate(
        complete_data,
        scope=ValidationScope.OUTPUT
    )
    
    completeness_results = [
        r for r in results
        if r.rule_name == "output_completeness"
    ]
    assert completeness_results
    assert completeness_results[0].is_valid

@pytest.mark.asyncio
async def test_system_resources(framework, sample_data):
    """Test system resources validation"""
    results = await framework.validate(
        sample_data,
        scope=ValidationScope.SYSTEM
    )
    
    resource_results = [
        r for r in results
        if r.rule_name == "system_resources"
    ]
    assert resource_results
    assert resource_results[0].is_valid

@pytest.mark.asyncio
async def test_validation_levels(framework, sample_data):
    """Test validation at different levels"""
    # Test strict validation
    strict_results = await framework.validate(
        sample_data,
        level=ValidationLevel.STRICT
    )
    assert strict_results
    
    # Test relaxed validation
    relaxed_results = await framework.validate(
        sample_data,
        level=ValidationLevel.RELAXED
    )
    assert len(relaxed_results) <= len(strict_results)

@pytest.mark.asyncio
async def test_custom_rule_addition(framework):
    """Test adding custom validation rule"""
    async def custom_validator(data: dict) -> bool:
        return "custom_field" in data
    
    framework.add_rule(ValidationRule(
        name="custom_rule",
        validation_type=ValidationType.CUSTOM,
        scope=ValidationScope.INPUT,
        level=ValidationLevel.STANDARD,
        validator=custom_validator,
        error_message="Custom validation failed"
    ))
    
    test_data = {"custom_field": "value"}
    results = await framework.validate(test_data)
    
    custom_results = [
        r for r in results
        if r.rule_name == "custom_rule"
    ]
    assert custom_results
    assert custom_results[0].is_valid

@pytest.mark.asyncio
async def test_validation_metrics(framework, sample_data):
    """Test validation metrics calculation"""
    await framework.validate(sample_data)
    metrics = framework.get_validation_metrics()
    
    assert metrics["total_validations"] > 0
    assert metrics["validation_scopes"]
    assert metrics["validation_levels"]
    assert 0 <= metrics["success_rate"] <= 1

@pytest.mark.asyncio
async def test_validation_reset(framework, sample_data):
    """Test validation framework reset"""
    await framework.validate(sample_data)
    assert framework.results
    
    framework.reset()
    assert not framework.results

@pytest.mark.asyncio
async def test_validation_error_handling(framework):
    """Test validation error handling"""
    # Invalid planetary data
    invalid_data = {
        "planets": {
            "Sun": {
                "longitude": 400,  # Invalid longitude
                "latitude": 0,
                "speed": 1
            }
        }
    }
    
    with pytest.raises(ValidationError) as exc_info:
        await framework.validate(
            invalid_data,
            level=ValidationLevel.STRICT
        )
    assert exc_info.value.scope == ValidationScope.INPUT

@pytest.mark.asyncio
async def test_input_validation_decorator():
    """Test input validation decorator"""
    class TestClass:
        @validate_input(level=ValidationLevel.STRICT)
        async def test_method(self, data: dict):
            return data
    
    test_instance = TestClass()
    valid_data = {
        "datetime": "2024-01-01T12:00:00Z",
        "planets": {
            "Sun": {
                "longitude": 280.5,
                "latitude": 0.0,
                "speed": 1.0
            }
        }
    }
    
    # Test with valid data
    result = await test_instance.test_method(valid_data)
    assert result == valid_data
    
    # Test with invalid data
    invalid_data = {"invalid": "data"}
    with pytest.raises(ValidationError):
        await test_instance.test_method(invalid_data)

@pytest.mark.asyncio
async def test_concurrent_validation(framework, sample_data):
    """Test concurrent validation execution"""
    # Create multiple validation tasks
    tasks = [
        framework.validate(sample_data)
        for _ in range(5)
    ]
    
    results = await asyncio.gather(*tasks)
    assert all(isinstance(r, list) for r in results)
    assert all(len(r) > 0 for r in results)
