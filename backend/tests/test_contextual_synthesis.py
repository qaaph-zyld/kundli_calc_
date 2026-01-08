"""
Tests for Contextual Synthesis Engine

Validates multi-factor interpretation synthesis
"""

import pytest
from backend.app.core.knowledge.engine.contextual_synthesis_engine import (
    ContextualSynthesisEngine,
    StrengthLevel
)


class TestContextualSynthesis:
    """Test contextual synthesis engine"""
    
    def test_basic_synthesis(self):
        """Test basic contextual synthesis"""
        engine = ContextualSynthesisEngine()
        
        result = engine.synthesize_interpretation(
            planet="Sun",
            house=10,
            sign="Aries",
            dignity="exalted"
        )
        
        assert result.planet == "Sun"
        assert result.house == 10
        assert result.sign == "Aries"
        assert result.strength_assessment.overall_strength in [
            StrengthLevel.EXCEPTIONAL, StrengthLevel.VERY_STRONG
        ]
        assert result.confidence_score > 0.90
    
    def test_with_lordship(self):
        """Test synthesis with lordship"""
        engine = ContextualSynthesisEngine()
        
        result = engine.synthesize_interpretation(
            planet="Sun",
            house=10,
            sign="Aries",
            dignity="exalted",
            lordship_houses=[9]  # 9th lord
        )
        
        assert result.lordship_effects is not None
        assert 9 in result.lordship_effects["ruling_houses"]
        assert "trikona" in result.lordship_effects["strength_note"].lower()
    
    def test_with_aspects(self):
        """Test synthesis with aspects"""
        engine = ContextualSynthesisEngine()
        
        result = engine.synthesize_interpretation(
            planet="Sun",
            house=10,
            sign="Aries",
            aspects=[{"planet": "Jupiter", "type": "5th"}]
        )
        
        assert len(result.aspect_effects) == 1
        assert result.aspect_effects[0]["aspecting_planet"] == "Jupiter"
        assert result.aspect_effects[0]["influence"] == "positive"
    
    def test_with_yogas(self):
        """Test synthesis with yogas"""
        engine = ContextualSynthesisEngine()
        
        result = engine.synthesize_interpretation(
            planet="Sun",
            house=10,
            sign="Aries",
            active_yogas=["Dharma_Karma_Adhipati_Yoga"]
        )
        
        assert len(result.yoga_effects) >= 1
        assert result.yoga_effects[0]["yoga_name"] == "Dharma_Karma_Adhipati_Yoga"
        assert "key_effects" in result.yoga_effects[0]
    
    def test_strength_assessment(self):
        """Test strength assessment calculation"""
        engine = ContextualSynthesisEngine()
        
        # Exalted planet in good house should be very strong
        result = engine.synthesize_interpretation(
            planet="Sun",
            house=10,
            sign="Aries",
            dignity="exalted"
        )
        
        assert result.strength_assessment.strength_score >= 60
        assert result.strength_assessment.dignity_score >= 35
        assert len(result.strength_assessment.factors_contributing) > 0
    
    def test_full_contextual_synthesis(self):
        """Test complete synthesis with all factors"""
        engine = ContextualSynthesisEngine()
        
        result = engine.synthesize_interpretation(
            planet="Sun",
            house=10,
            sign="Aries",
            dignity="exalted",
            lordship_houses=[9],
            aspects=[{"planet": "Jupiter", "type": "5th"}],
            active_yogas=["Dharma_Karma_Adhipati_Yoga"],
            current_dasha="Sun"
        )
        
        # Should have exceptional strength
        assert result.strength_assessment.overall_strength == StrengthLevel.EXCEPTIONAL
        assert result.strength_assessment.strength_score >= 85
        
        # Should have all factor analyses
        assert result.lordship_effects is not None
        assert len(result.aspect_effects) > 0
        assert len(result.yoga_effects) > 0
        assert result.dasha_modulation is not None
        
        # Should have synthesis
        assert len(result.synthesized_interpretation) > 100
        assert len(result.key_themes) > 0
        assert len(result.timing_notes) > 0
        
        # High confidence
        assert result.confidence_score >= 0.92
    
    def test_weak_placement(self):
        """Test synthesis for weak placement"""
        engine = ContextualSynthesisEngine()
        
        result = engine.synthesize_interpretation(
            planet="Sun",
            house=12,  # Dusthana
            sign="Libra",
            dignity="debilitated"
        )
        
        # Should show weakness
        assert result.strength_assessment.overall_strength in [
            StrengthLevel.WEAK, StrengthLevel.DEBILITATED
        ]
        assert result.strength_assessment.strength_score < 40
        assert len(result.strength_assessment.factors_weakening) > 0
