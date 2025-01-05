"""
Test Suite for Correlation Engine
PGF Protocol: COR_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime, timedelta
import numpy as np
from app.core.analysis.correlation_engine import (
    CorrelationAnalyzer,
    CorrelationType,
    CorrelationResult
)

@pytest.fixture
def analyzer():
    return CorrelationAnalyzer(significance_threshold=0.05)

@pytest.fixture
def sample_data():
    return {
        "planets": {
            "Sun": {
                "degree": 15,
                "strength": 0.8,
                "dignity": 0.7
            },
            "Moon": {
                "degree": 135,
                "strength": 0.6,
                "dignity": 0.5
            },
            "Mars": {
                "degree": 255,
                "strength": 0.9,
                "dignity": 0.8
            }
        },
        "houses": {
            1: {"degree": 0},
            4: {"degree": 90},
            7: {"degree": 180},
            10: {"degree": 270}
        },
        "aspects": [
            {
                "planets": ["Sun", "Moon"],
                "type": "trine",
                "strength": 0.7
            },
            {
                "planets": ["Moon", "Mars"],
                "type": "square",
                "strength": 0.6
            }
        ],
        "temporal": {
            "hour_series": [0.1, 0.3, 0.6, 0.8, 0.9, 0.7, 0.4, 0.2],
            "day_factor": [0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5]
        }
    }

@pytest.mark.asyncio
async def test_direct_correlation_analysis(analyzer, sample_data):
    """Test direct correlation analysis"""
    correlations = await analyzer._analyze_direct_correlation(sample_data)
    
    assert correlations
    assert all(c.correlation_type == CorrelationType.DIRECT
              for c in correlations)
    assert all(0 <= c.strength <= 1 for c in correlations)
    assert all(0 <= c.confidence <= 1 for c in correlations)

@pytest.mark.asyncio
async def test_inverse_correlation_analysis(analyzer, sample_data):
    """Test inverse correlation analysis"""
    correlations = await analyzer._analyze_inverse_correlation(sample_data)
    
    assert correlations
    assert all(c.correlation_type == CorrelationType.INVERSE
              for c in correlations)
    assert all(0 <= c.strength <= 1 for c in correlations)

@pytest.mark.asyncio
async def test_cyclic_correlation_analysis(analyzer, sample_data):
    """Test cyclic correlation analysis"""
    correlations = await analyzer._analyze_cyclic_correlation(sample_data)
    
    assert correlations
    assert all(c.correlation_type == CorrelationType.CYCLIC
              for c in correlations)
    assert all(0 <= c.strength <= 1 for c in correlations)
    assert all("period" in c.details for c in correlations)

@pytest.mark.asyncio
async def test_compound_correlation_analysis(analyzer, sample_data):
    """Test compound correlation analysis"""
    correlations = await analyzer._analyze_compound_correlation(sample_data)
    
    assert correlations
    assert all(c.correlation_type == CorrelationType.COMPOUND
              for c in correlations)
    assert all("components" in c.details for c in correlations)

@pytest.mark.asyncio
async def test_temporal_correlation_analysis(analyzer, sample_data):
    """Test temporal correlation analysis"""
    correlations = await analyzer._analyze_temporal_correlation(sample_data)
    
    assert correlations
    assert all(c.correlation_type == CorrelationType.TEMPORAL
              for c in correlations)
    assert all("cycle_length" in c.details for c in correlations)

@pytest.mark.asyncio
async def test_full_correlation_analysis(analyzer, sample_data):
    """Test full correlation analysis"""
    correlations = await analyzer.analyze_correlations(sample_data)
    
    assert correlations
    assert len(correlations) > 0
    assert len(set(c.correlation_type for c in correlations)) > 1

@pytest.mark.asyncio
async def test_correlation_metrics(analyzer, sample_data):
    """Test correlation metrics calculation"""
    await analyzer.analyze_correlations(sample_data)
    metrics = analyzer.get_correlation_metrics()
    
    assert metrics["total_correlations"] > 0
    assert metrics["correlation_types"]
    assert 0 <= metrics["average_strength"] <= 1
    assert 0 <= metrics["average_confidence"] <= 1

@pytest.mark.asyncio
async def test_correlation_reset(analyzer, sample_data):
    """Test correlation analyzer reset"""
    await analyzer.analyze_correlations(sample_data)
    assert len(analyzer.correlations) > 0
    
    analyzer.reset()
    assert len(analyzer.correlations) == 0

@pytest.mark.asyncio
async def test_selective_correlation_analysis(analyzer, sample_data):
    """Test selective correlation type analysis"""
    selected_types = [CorrelationType.DIRECT, CorrelationType.INVERSE]
    correlations = await analyzer.analyze_correlations(
        sample_data,
        correlation_types=selected_types
    )
    
    assert correlations
    assert all(c.correlation_type in selected_types for c in correlations)

@pytest.mark.asyncio
async def test_correlation_significance(analyzer, sample_data):
    """Test correlation significance calculation"""
    correlations = await analyzer.analyze_correlations(sample_data)
    
    assert all(hasattr(c, "significance") for c in correlations)
    assert all(0 <= c.significance <= 1 for c in correlations)

@pytest.mark.asyncio
async def test_error_handling(analyzer):
    """Test error handling in correlation analysis"""
    # Invalid data
    invalid_data = {
        "planets": None,
        "houses": None
    }
    
    correlations = await analyzer.analyze_correlations(invalid_data)
    assert isinstance(correlations, list)
    assert len(correlations) == 0

@pytest.mark.asyncio
async def test_temporal_pattern_detection(analyzer):
    """Test temporal pattern detection"""
    # Create synthetic time series
    t = np.linspace(0, 4*np.pi, 100)
    signal = np.sin(t) + 0.1*np.random.randn(100)
    
    data = {
        "temporal": {
            "test_series": signal
        }
    }
    
    correlations = await analyzer._analyze_temporal_correlation(data)
    assert correlations
    assert all("cycle_length" in c.details for c in correlations)
    assert all(c.strength > 0 for c in correlations)

@pytest.mark.asyncio
async def test_compound_pattern_detection(analyzer):
    """Test compound pattern detection"""
    # Create test data with known compound patterns
    data = {
        "planets": {
            "Sun": {"strength": 0.8},
            "Moon": {"strength": 0.7},
            "Mars": {"strength": 0.9}
        },
        "houses": {
            1: {"strength": 0.6},
            7: {"strength": 0.8}
        },
        "aspects": [
            {
                "planets": ["Sun", "Moon"],
                "strength": 0.9
            },
            {
                "planets": ["Moon", "Mars"],
                "strength": 0.8
            }
        ]
    }
    
    correlations = await analyzer._analyze_compound_correlation(data)
    assert correlations
    assert all("components" in c.details for c in correlations)
    assert all(len(c.details["components"]) >= 2 for c in correlations)
