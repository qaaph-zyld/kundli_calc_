"""
Tests for Yoga Activation Engine
"""

import pytest
from backend.app.core.timing.yoga_activation_engine import (
    YogaActivationEngine,
    YogaActivationWindow
)


class TestYogaActivation:
    
    def test_engine_initialization(self):
        """Test yoga activation engine initializes"""
        engine = YogaActivationEngine()
        assert engine is not None
        assert len(engine.dasha_durations) == 9
    
    def test_gaja_kesari_yoga_timing(self):
        """Test Gaja Kesari Yoga activation timing"""
        engine = YogaActivationEngine()
        
        result = engine.calculate_activation_windows(
            yoga_name="Gaja_Kesari_Yoga",
            involved_planets=["Jupiter", "Moon"],
            formation_strength=85.0
        )
        
        assert result.yoga_name == "Gaja_Kesari_Yoga"
        assert result.formation_strength == 85.0
        assert len(result.involved_planets) == 2
        assert len(result.primary_periods) == 2
        assert result.confidence > 0.85
        
        # Check primary periods include Jupiter and Moon
        planet_names = [p.planet for p in result.primary_periods]
        assert "Jupiter" in planet_names
        assert "Moon" in planet_names
    
    def test_raja_yoga_timing(self):
        """Test Raja Yoga activation timing"""
        engine = YogaActivationEngine()
        
        result = engine.calculate_activation_windows(
            yoga_name="Dharma_Karma_Adhipati_Yoga",
            involved_planets=["Jupiter", "Saturn"],
            formation_strength=90.0
        )
        
        assert result.formation_strength == 90.0
        assert len(result.primary_periods) == 2
        assert len(result.peak_activation) > 0
        assert len(result.transit_triggers) > 0
        
        # High formation strength should give high confidence
        assert result.confidence >= 0.90
    
    def test_weak_formation_timing(self):
        """Test yoga with weak formation"""
        engine = YogaActivationEngine()
        
        result = engine.calculate_activation_windows(
            yoga_name="Test_Yoga",
            involved_planets=["Mars"],
            formation_strength=45.0
        )
        
        assert result.formation_strength == 45.0
        assert len(result.primary_periods) == 1
        assert result.confidence < 0.90
    
    def test_peak_antardasha_calculation(self):
        """Test peak antardasha combinations"""
        engine = YogaActivationEngine()
        
        result = engine.calculate_activation_windows(
            yoga_name="Test_Yoga",
            involved_planets=["Jupiter", "Venus", "Mercury"],
            formation_strength=80.0
        )
        
        # Should have peak activation periods
        assert len(result.peak_activation) > 0
        
        # Peak activation should have higher strength
        for peak in result.peak_activation:
            assert peak["activation_strength"] >= result.formation_strength
    
    def test_manifestation_timeline(self):
        """Test manifestation timeline generation"""
        engine = YogaActivationEngine()
        
        result = engine.calculate_activation_windows(
            yoga_name="Test_Yoga",
            involved_planets=["Sun", "Moon"],
            formation_strength=75.0
        )
        
        assert "primary_manifestation" in result.manifestation_timeline
        assert "strength_note" in result.manifestation_timeline
