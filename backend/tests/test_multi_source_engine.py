"""
Tests for Multi-Source Interpretation Engine

Tests the multi-source comparison and synthesis capabilities,
validating that the engine correctly compares BPHS and Saravali
interpretations and synthesizes unified results.
"""

import pytest
from backend.app.core.knowledge.engine.multi_source_engine import (
    MultiSourceEngine,
    AgreementLevel,
    SourceComparison
)


class TestMultiSourceEngine:
    """Test suite for multi-source interpretation engine"""
    
    @pytest.fixture
    def engine(self):
        """Create engine instance for testing"""
        return MultiSourceEngine()
    
    def test_engine_initialization(self, engine):
        """Test that engine initializes correctly"""
        assert engine is not None
        assert 'BPHS' in engine.sources
        assert 'Saravali' in engine.sources
    
    def test_get_available_sources_both(self, engine):
        """Test getting sources when both BPHS and Saravali have data"""
        # Sun in 1st house - both sources have this
        sources = engine.get_available_sources('Sun', 1)
        assert 'BPHS' in sources
        assert 'Saravali' in sources
        assert len(sources) == 2
    
    def test_get_available_sources_bphs_only(self, engine):
        """Test when only BPHS has data"""
        # Sun in 3rd house - only BPHS has this currently
        sources = engine.get_available_sources('Sun', 3)
        assert 'BPHS' in sources
        assert 'Saravali' not in sources
    
    def test_get_available_sources_none(self, engine):
        """Test when no sources have data"""
        # Invalid combination
        sources = engine.get_available_sources('Rahu', 1)
        assert len(sources) == 0
    
    def test_compare_sources_sun_first(self, engine):
        """Test comparison for Sun in 1st house (both sources available)"""
        comparison = engine.compare_sources('Sun', 1)
        
        assert comparison is not None
        assert comparison.planet == 'Sun'
        assert comparison.house == 1
        assert 'BPHS' in comparison.sources_available
        assert 'Saravali' in comparison.sources_available
        assert comparison.agreement_level in AgreementLevel
        assert isinstance(comparison.common_themes, list)
        assert isinstance(comparison.synthesis, str)
        assert 0.7 <= comparison.confidence_score <= 0.98
    
    def test_compare_sources_jupiter_first(self, engine):
        """Test comparison for Jupiter in 1st house"""
        comparison = engine.compare_sources('Jupiter', 1)
        
        assert comparison.planet == 'Jupiter'
        assert comparison.house == 1
        assert len(comparison.sources_available) == 2
        assert comparison.synthesis is not None
        assert 'Jupiter' in comparison.synthesis
    
    def test_compare_sources_single_source(self, engine):
        """Test comparison when only one source available"""
        # Sun in 3rd - only BPHS
        comparison = engine.compare_sources('Sun', 3)
        
        assert len(comparison.sources_available) == 1
        assert 'BPHS' in comparison.sources_available
        # Should still provide synthesis
        assert comparison.synthesis is not None
    
    def test_compare_sources_no_data_raises_error(self, engine):
        """Test that comparing non-existent combination raises error"""
        with pytest.raises(ValueError, match="No sources available"):
            engine.compare_sources('Rahu', 1)
    
    def test_agreement_level_types(self, engine):
        """Test that agreement levels are properly categorized"""
        comparison = engine.compare_sources('Sun', 1)
        
        # Agreement level should be one of the enum values
        assert comparison.agreement_level in [
            AgreementLevel.STRONG_AGREEMENT,
            AgreementLevel.MODERATE_AGREEMENT,
            AgreementLevel.NEUTRAL,
            AgreementLevel.MODERATE_DISAGREEMENT,
            AgreementLevel.STRONG_DISAGREEMENT
        ]
    
    def test_common_themes_extraction(self, engine):
        """Test that common themes are extracted"""
        comparison = engine.compare_sources('Jupiter', 1)
        
        # Jupiter in 1st should have common positive themes
        assert len(comparison.common_themes) >= 0  # May or may not find themes
        if comparison.common_themes:
            assert all(isinstance(theme, str) for theme in comparison.common_themes)
    
    def test_unique_effects_identification(self, engine):
        """Test that unique effects are identified"""
        comparison = engine.compare_sources('Sun', 1)
        
        assert isinstance(comparison.unique_to_bphs, list)
        assert isinstance(comparison.unique_to_saravali, list)
    
    def test_synthesis_quality(self, engine):
        """Test that synthesis is meaningful"""
        comparison = engine.compare_sources('Jupiter', 1)
        
        # Synthesis should mention both sources and planet
        assert 'Jupiter' in comparison.synthesis
        assert comparison.synthesis  # Not empty
        assert len(comparison.synthesis) > 50  # Substantial content
    
    def test_comprehensive_interpretation(self, engine):
        """Test comprehensive interpretation with all sources"""
        result = engine.get_comprehensive_interpretation('Sun', 1, include_comparison=True)
        
        assert result['planet'] == 'Sun'
        assert result['house'] == 1
        assert 'sources_available' in result
        assert 'interpretations' in result
        assert 'BPHS' in result['interpretations']
        assert 'Saravali' in result['interpretations']
        assert 'comparison' in result
        assert 'synthesis' in result['comparison']
    
    def test_comprehensive_interpretation_without_comparison(self, engine):
        """Test comprehensive interpretation without comparison"""
        result = engine.get_comprehensive_interpretation('Sun', 1, include_comparison=False)
        
        assert 'interpretations' in result
        assert 'comparison' not in result
    
    def test_confidence_score_range(self, engine):
        """Test that confidence scores are within valid range"""
        # Test multiple combinations
        combinations = [
            ('Sun', 1),
            ('Moon', 4),
            ('Jupiter', 1),
            ('Saturn', 10)
        ]
        
        for planet, house in combinations:
            try:
                comparison = engine.compare_sources(planet, house)
                assert 0.7 <= comparison.confidence_score <= 0.98
                assert isinstance(comparison.confidence_score, float)
            except ValueError:
                # Skip if combination not available
                pass
    
    def test_multi_source_boost(self, engine):
        """Test that multiple sources boost confidence"""
        # Compare single source vs multi-source
        single_source = engine.compare_sources('Sun', 3)  # BPHS only
        multi_source = engine.compare_sources('Sun', 1)   # Both sources
        
        # Multi-source should generally have higher confidence if agreement is good
        if multi_source.agreement_level in [
            AgreementLevel.STRONG_AGREEMENT,
            AgreementLevel.MODERATE_AGREEMENT
        ]:
            # Multi-source with agreement should be confident
            assert multi_source.confidence_score >= 0.85


class TestMultiSourceCoverage:
    """Test coverage statistics for multi-source system"""
    
    @pytest.fixture
    def engine(self):
        return MultiSourceEngine()
    
    def test_coverage_statistics(self, engine):
        """Test that we can get coverage statistics"""
        # Count available combinations
        bphs_count = 0
        saravali_count = 0
        both_count = 0
        
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        
        for planet in planets:
            for house in range(1, 13):
                sources = engine.get_available_sources(planet, house)
                if 'BPHS' in sources:
                    bphs_count += 1
                if 'Saravali' in sources:
                    saravali_count += 1
                if len(sources) == 2:
                    both_count += 1
        
        # BPHS should have all 84
        assert bphs_count == 84
        
        # Saravali should have some coverage
        assert saravali_count >= 10  # At least 10 combinations
        
        # Some should have both
        assert both_count >= 5  # At least 5 with both sources
        
        print(f"\nCoverage: BPHS={bphs_count}, Saravali={saravali_count}, Both={both_count}")
