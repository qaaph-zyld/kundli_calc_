"""
Tests for Career Synthesis Engine
"""

import pytest
from backend.app.core.knowledge.engine.career_synthesis_engine import (
    CareerSynthesisEngine,
    CareerStrength
)


class TestCareerSynthesis:
    
    def test_career_engine_initialization(self):
        """Test career engine initializes"""
        engine = CareerSynthesisEngine()
        assert engine is not None
        assert engine.contextual_engine is not None
    
    def test_strong_career_chart(self):
        """Test chart with strong career indicators"""
        engine = CareerSynthesisEngine()
        
        chart_data = {
            "planets": {
                "Sun": {"house": 10, "sign": "Aries", "dignity": "exalted"},
                "Saturn": {"house": 6, "sign": "Capricorn", "dignity": "own_sign"},
                "Jupiter": {"house": 9, "sign": "Sagittarius", "dignity": "own_sign"}
            },
            "house_lords": {10: "Sun", 6: "Saturn", 2: "Mercury"},
            "active_yogas": ["Dharma_Karma_Adhipati_Yoga"]
        }
        
        result = engine.synthesize_career_analysis(chart_data, "Sun")
        
        assert result.strength_score > 70
        assert result.strength_level in [CareerStrength.VERY_STRONG, CareerStrength.EXCEPTIONAL]
        assert len(result.key_factors) >= 4
        assert result.confidence > 0.85
    
    def test_moderate_career_chart(self):
        """Test chart with moderate career indicators"""
        engine = CareerSynthesisEngine()
        
        chart_data = {
            "planets": {
                "Sun": {"house": 12, "sign": "Libra", "dignity": "debilitated"},
                "Saturn": {"house": 8, "sign": "Aquarius", "dignity": "own_sign"}
            },
            "house_lords": {10: "Venus", 6: "Mars", 2: "Moon"},
            "active_yogas": []
        }
        
        result = engine.synthesize_career_analysis(chart_data)
        
        assert result.strength_score < 70
        assert len(result.key_factors) >= 3
        assert len(result.recommendations) > 0
