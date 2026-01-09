"""
Tests for Relationship Synthesis Engine
"""

import pytest
from backend.app.core.knowledge.engine.relationship_synthesis_engine import (
    RelationshipSynthesisEngine,
    RelationshipStrength
)


class TestRelationshipSynthesis:
    
    def test_relationship_engine_initialization(self):
        """Test relationship engine initializes"""
        engine = RelationshipSynthesisEngine()
        assert engine is not None
        assert engine.contextual_engine is not None
    
    def test_strong_relationship_chart(self):
        """Test chart with strong relationship indicators"""
        engine = RelationshipSynthesisEngine()
        
        chart_data = {
            "planets": {
                "Venus": {"house": 7, "sign": "Pisces", "dignity": "exalted"},
                "Jupiter": {"house": 5, "sign": "Sagittarius", "dignity": "own_sign"},
                "Moon": {"house": 4, "sign": "Cancer", "dignity": "own_sign"}
            },
            "house_lords": {7: "Venus", 5: "Jupiter", 8: "Saturn"},
            "active_yogas": []
        }
        
        result = engine.synthesize_relationship_analysis(chart_data, "Venus")
        
        assert result.strength_score > 70
        assert result.strength_level in [RelationshipStrength.VERY_STRONG, RelationshipStrength.EXCEPTIONAL]
        assert len(result.key_factors) >= 4
        assert result.confidence > 0.85
    
    def test_moderate_relationship_chart(self):
        """Test chart with moderate relationship indicators"""
        engine = RelationshipSynthesisEngine()
        
        chart_data = {
            "planets": {
                "Venus": {"house": 12, "sign": "Virgo", "dignity": "debilitated"},
                "Saturn": {"house": 7, "sign": "Capricorn", "dignity": "own_sign"}
            },
            "house_lords": {7: "Saturn", 5: "Mars", 8: "Jupiter"},
            "active_yogas": []
        }
        
        result = engine.synthesize_relationship_analysis(chart_data)
        
        assert result.strength_score < 70
        assert len(result.key_factors) >= 3
        assert len(result.recommendations) > 0
        assert "marriage_windows" in result.timing
