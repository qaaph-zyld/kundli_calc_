"""
Tests for Wealth Synthesis Engine
"""

import pytest
from backend.app.core.knowledge.engine.wealth_synthesis_engine import (
    WealthSynthesisEngine,
    WealthStrength
)


class TestWealthSynthesis:
    
    def test_wealth_engine_initialization(self):
        """Test wealth engine initializes"""
        engine = WealthSynthesisEngine()
        assert engine is not None
        assert engine.contextual_engine is not None
    
    def test_strong_wealth_chart(self):
        """Test chart with strong wealth indicators"""
        engine = WealthSynthesisEngine()
        
        chart_data = {
            "planets": {
                "Jupiter": {"house": 2, "sign": "Sagittarius", "dignity": "own_sign"},
                "Venus": {"house": 11, "sign": "Taurus", "dignity": "own_sign"},
                "Mercury": {"house": 5, "sign": "Gemini", "dignity": "own_sign"}
            },
            "house_lords": {2: "Jupiter", 11: "Venus", 5: "Mercury", 9: "Mars"},
            "active_yogas": ["Dhana_Yoga", "Gaja_Kesari_Yoga"]
        }
        
        result = engine.synthesize_wealth_analysis(chart_data, "Jupiter")
        
        assert result.strength_score >= 70
        assert result.strength_level in [WealthStrength.VERY_STRONG, WealthStrength.EXCEPTIONAL, WealthStrength.STRONG]
        assert len(result.key_factors) >= 5
        assert result.confidence >= 0.85
    
    def test_moderate_wealth_chart(self):
        """Test chart with moderate wealth indicators"""
        engine = WealthSynthesisEngine()
        
        chart_data = {
            "planets": {
                "Jupiter": {"house": 12, "sign": "Capricorn", "dignity": "debilitated"},
                "Saturn": {"house": 2, "sign": "Aquarius", "dignity": "own_sign"}
            },
            "house_lords": {2: "Saturn", 11: "Mars", 5: "Sun", 9: "Venus"},
            "active_yogas": []
        }
        
        result = engine.synthesize_wealth_analysis(chart_data)
        
        assert result.strength_score <= 75
        assert len(result.key_factors) >= 4
        assert len(result.recommendations) > 0
        assert "wealth_gain_windows" in result.timing
    
    def test_weak_wealth_chart(self):
        """Test chart with challenging wealth indicators"""
        engine = WealthSynthesisEngine()
        
        chart_data = {
            "planets": {
                "Jupiter": {"house": 8, "sign": "Capricorn", "dignity": "debilitated"},
                "Saturn": {"house": 11, "sign": "Aries", "dignity": "debilitated"}
            },
            "house_lords": {2: "Mars", 11: "Saturn", 5: "Sun", 9: "Venus"},
            "active_yogas": []
        }
        
        result = engine.synthesize_wealth_analysis(chart_data)
        
        assert result.strength_score < 60
        assert result.strength_level in [WealthStrength.MODERATE, WealthStrength.CHALLENGING, WealthStrength.DIFFICULT]
        assert len(result.recommendations) > 0
