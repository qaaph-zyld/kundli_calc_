"""
Test Suite for Pattern Detection System
PGF Protocol: PAT_001
Gate: GATE_3
Version: 1.0.0
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from app.core.analysis.pattern_detector import (
    PatternDetector,
    PatternType,
    PatternSignature,
    PatternMatch
)

@pytest.fixture
def detector():
    return PatternDetector()

@pytest.fixture
def sample_chart_data():
    return {
        "planets": {
            "Sun": {
                "sign": "Aries",
                "degree": 15,
                "rules": "Leo"
            },
            "Moon": {
                "sign": "Taurus",
                "degree": 20,
                "rules": "Cancer"
            },
            "Mars": {
                "sign": "Leo",
                "degree": 10,
                "rules": "Aries"
            },
            "Venus": {
                "sign": "Pisces",
                "degree": 5,
                "rules": "Taurus"
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
                "type": "trine",
                "planets": ["Sun", "Mars"],
                "orb": 2
            },
            {
                "type": "trine",
                "planets": ["Mars", "Jupiter"],
                "orb": 3
            }
        ],
        "temporal": {
            "hour_ruler": "Mars",
            "duration": 2.0
        }
    }

@pytest.mark.asyncio
async def test_pattern_initialization(detector):
    """Test pattern detector initialization"""
    assert detector.signatures
    assert "exaltation" in detector.signatures
    assert "mutual_reception" in detector.signatures
    assert "grand_trine" in detector.signatures

@pytest.mark.asyncio
async def test_planetary_pattern_detection(detector, sample_chart_data):
    """Test planetary pattern detection"""
    patterns = await detector.detect_patterns(sample_chart_data)
    
    # Should detect Sun in Aries (exaltation)
    exaltation_patterns = [
        p for p in patterns
        if p.name == "Exaltation"
    ]
    assert exaltation_patterns
    assert exaltation_patterns[0].confidence > 0
    assert any(
        comp["planet"] == "Sun" and comp["sign"] == "Aries"
        for comp in exaltation_patterns[0].components
    )

@pytest.mark.asyncio
async def test_house_pattern_detection(detector, sample_chart_data):
    """Test house pattern detection"""
    patterns = await detector.detect_patterns(sample_chart_data)
    
    # Should detect kendra (90-degree) pattern
    kendra_patterns = [
        p for p in patterns
        if p.name == "Kendra"
    ]
    assert kendra_patterns
    assert any(
        p.pattern_type == PatternType.HOUSE
        for p in patterns
    )

@pytest.mark.asyncio
async def test_aspect_pattern_detection(detector, sample_chart_data):
    """Test aspect pattern detection"""
    patterns = await detector.detect_patterns(sample_chart_data)
    
    # Should detect grand trine
    trine_patterns = [
        p for p in patterns
        if p.name == "Grand Trine"
    ]
    assert trine_patterns
    assert any(
        p.pattern_type == PatternType.ASPECT
        for p in patterns
    )

@pytest.mark.asyncio
async def test_temporal_pattern_detection(detector, sample_chart_data):
    """Test temporal pattern detection"""
    patterns = await detector.detect_patterns(sample_chart_data)
    
    # Should detect planetary hour
    hour_patterns = [
        p for p in patterns
        if p.name == "Planetary Hour"
    ]
    assert hour_patterns
    assert any(
        p.pattern_type == PatternType.TEMPORAL
        for p in patterns
    )

@pytest.mark.asyncio
async def test_pattern_strength_calculation(detector, sample_chart_data):
    """Test pattern strength calculations"""
    patterns = await detector.detect_patterns(sample_chart_data)
    
    for pattern in patterns:
        assert 0 <= pattern.strength <= 1
        assert 0 <= pattern.confidence <= 1
        assert pattern.effects

@pytest.mark.asyncio
async def test_multiple_pattern_detection(detector):
    """Test detection of multiple patterns"""
    chart_data = {
        "planets": {
            "Sun": {"sign": "Aries", "rules": "Leo"},
            "Moon": {"sign": "Cancer", "rules": "Cancer"},
            "Mars": {"sign": "Leo", "rules": "Aries"}
        },
        "houses": {
            1: {"degree": 0},
            5: {"degree": 120},
            9: {"degree": 240}
        },
        "aspects": [
            {
                "type": "trine",
                "planets": ["Sun", "Mars", "Jupiter"],
                "orb": 2
            }
        ],
        "temporal": {
            "hour_ruler": "Sun"
        }
    }
    
    patterns = await detector.detect_patterns(chart_data)
    pattern_types = {p.pattern_type for p in patterns}
    
    assert len(patterns) > 1
    assert len(pattern_types) > 1

@pytest.mark.asyncio
async def test_pattern_sequence_analysis(detector, sample_chart_data):
    """Test pattern sequence analysis"""
    # Generate patterns over time
    for i in range(3):
        patterns = await detector.detect_patterns(sample_chart_data)
        # Simulate time passage
        for pattern in patterns:
            pattern.timestamp = datetime.now() + timedelta(hours=i)
    
    analysis = await detector.analyze_pattern_sequence()
    
    assert analysis["total_patterns"] > 0
    assert analysis["pattern_types"]
    assert analysis["pattern_strengths"]
    assert analysis["temporal_distribution"]

@pytest.mark.asyncio
async def test_pattern_metrics(detector, sample_chart_data):
    """Test pattern metrics calculation"""
    await detector.detect_patterns(sample_chart_data)
    metrics = detector.get_pattern_metrics()
    
    assert metrics["total_detected"] > 0
    assert metrics["pattern_types"]
    assert 0 <= metrics["average_confidence"] <= 1
    assert metrics["latest_detection"]

@pytest.mark.asyncio
async def test_pattern_reset(detector, sample_chart_data):
    """Test pattern detector reset"""
    await detector.detect_patterns(sample_chart_data)
    assert detector.detected_patterns
    
    detector.reset()
    assert not detector.detected_patterns

@pytest.mark.asyncio
async def test_custom_pattern_signature(detector):
    """Test custom pattern signature detection"""
    # Add custom pattern
    detector.signatures["custom"] = PatternSignature(
        name="Custom Pattern",
        pattern_type=PatternType.PLANETARY,
        conditions=[{
            "type": "planet_sign",
            "relations": {
                "Sun": "Leo",
                "Moon": "Cancer"
            }
        }],
        effects={"custom_effect": 0.8}
    )
    
    chart_data = {
        "planets": {
            "Sun": {"sign": "Leo"},
            "Moon": {"sign": "Cancer"}
        }
    }
    
    patterns = await detector.detect_patterns(chart_data)
    custom_patterns = [
        p for p in patterns
        if p.name == "Custom Pattern"
    ]
    
    assert custom_patterns
    assert custom_patterns[0].effects["custom_effect"] == 0.8

@pytest.mark.asyncio
async def test_error_handling(detector):
    """Test error handling in pattern detection"""
    # Invalid chart data
    invalid_data = {
        "planets": None,
        "houses": None
    }
    
    patterns = await detector.detect_patterns(invalid_data)
    assert isinstance(patterns, list)
    assert len(patterns) == 0

@pytest.mark.asyncio
async def test_concurrent_pattern_detection(detector, sample_chart_data):
    """Test concurrent pattern detection"""
    # Create multiple detection tasks
    tasks = [
        detector.detect_patterns(sample_chart_data)
        for _ in range(5)
    ]
    
    results = await asyncio.gather(*tasks)
    
    assert all(isinstance(r, list) for r in results)
    assert all(len(r) > 0 for r in results)
