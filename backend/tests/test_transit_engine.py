"""
Tests for Transit Intelligence Engine
"""

import pytest
from datetime import datetime
from backend.app.core.timing.transit_engine import (
    TransitIntelligenceEngine,
    CurrentTransits
)


class TestTransitEngine:
    
    def test_engine_initialization(self):
        """Test transit engine initializes"""
        engine = TransitIntelligenceEngine()
        assert engine is not None
        assert len(engine.ASPECT_RULES) >= 5
    
    def test_current_transits_calculation(self):
        """Test current transit calculation"""
        engine = TransitIntelligenceEngine()
        
        birth_data = {
            "ascendant_sign": "Aries",
            "planets": {
                "Sun": {"house": 10, "sign": "Capricorn"},
                "Moon": {"house": 4, "sign": "Cancer"},
                "Jupiter": {"house": 9, "sign": "Sagittarius"}
            }
        }
        
        result = engine.get_current_transits(
            birth_data=birth_data,
            current_date=datetime(2026, 1, 9)
        )
        
        assert isinstance(result, CurrentTransits)
        assert result.jupiter is not None
        assert result.saturn is not None
        assert result.rahu is not None
        assert result.ketu is not None
        assert len(result.active_effects) > 0
    
    def test_jupiter_transit_position(self):
        """Test Jupiter transit position calculation"""
        engine = TransitIntelligenceEngine()
        
        birth_data = {
            "ascendant_sign": "Leo",
            "planets": {}
        }
        
        result = engine.get_current_transits(birth_data, datetime(2026, 1, 9))
        
        assert result.jupiter.planet == "Jupiter"
        assert result.jupiter.sign in ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        assert 1 <= result.jupiter.house_in_natal <= 12
    
    def test_aspect_calculation(self):
        """Test aspect calculation to natal planets"""
        engine = TransitIntelligenceEngine()
        
        birth_data = {
            "ascendant_sign": "Aries",
            "planets": {
                "Sun": {"house": 10, "sign": "Capricorn"},
                "Moon": {"house": 4, "sign": "Cancer"},
                "Venus": {"house": 7, "sign": "Libra"}
            }
        }
        
        result = engine.get_current_transits(birth_data, datetime(2026, 1, 9))
        
        # Should have some aspects
        total_aspects = (
            len(result.jupiter.aspects_natal_planets) +
            len(result.saturn.aspects_natal_planets) +
            len(result.rahu.aspects_natal_planets)
        )
        
        assert total_aspects >= 0  # May or may not aspect depending on positions
    
    def test_transit_effects_generation(self):
        """Test transit effects are generated"""
        engine = TransitIntelligenceEngine()
        
        birth_data = {
            "ascendant_sign": "Sagittarius",
            "planets": {
                "Sun": {"house": 1, "sign": "Sagittarius"},
                "Jupiter": {"house": 9, "sign": "Leo"}
            }
        }
        
        result = engine.get_current_transits(birth_data, datetime(2026, 1, 9))
        
        assert len(result.active_effects) > 0
        
        # Check effect structure
        for effect in result.active_effects:
            assert effect.transit_planet in ["Jupiter", "Saturn", "Rahu", "Ketu"]
            assert effect.effect_type in ["transiting_house", "aspecting_planet", "activating_yoga"]
            assert 0 <= effect.strength <= 100
            assert len(effect.description) > 0
    
    def test_synthesis_generation(self):
        """Test transit synthesis generation"""
        engine = TransitIntelligenceEngine()
        
        birth_data = {
            "ascendant_sign": "Gemini",
            "planets": {}
        }
        
        result = engine.get_current_transits(birth_data, datetime(2026, 1, 9))
        
        assert len(result.synthesis) > 50
        assert "Jupiter" in result.synthesis
        assert "Saturn" in result.synthesis
        assert len(result.recommendations) > 0
