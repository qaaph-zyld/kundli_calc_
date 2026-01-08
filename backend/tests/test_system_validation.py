"""
System Validation Tests
========================

Comprehensive validation of the complete astrological interpretation system.
Tests integration, data integrity, performance, and production readiness.
"""

import pytest
import time
from backend.app.core.knowledge.sources.bphs_planets_in_houses import (
    BPHS_PLANETS_IN_HOUSES,
    get_planet_in_house_interpretation
)
from backend.app.core.knowledge.sources.saravali_planets_in_houses import (
    SARAVALI_PLANETS_IN_HOUSES,
    get_saravali_interpretation
)
from backend.app.core.knowledge.sources.bphs_yogas import get_all_yogas
from backend.app.core.knowledge.engine.interpretation_engine import KnowledgeInterpretationEngine
from backend.app.core.knowledge.engine.multi_source_engine import MultiSourceEngine


class TestDataIntegrity:
    """Validate data integrity across all sources"""
    
    def test_bphs_complete_coverage(self):
        """Verify BPHS has all 84 planet-house combinations"""
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        
        total_combinations = 0
        for planet in planets:
            assert planet in BPHS_PLANETS_IN_HOUSES
            houses = BPHS_PLANETS_IN_HOUSES[planet]
            assert len(houses) == 12, f"{planet} should have 12 houses, has {len(houses)}"
            total_combinations += len(houses)
        
        assert total_combinations == 84, f"Should have 84 total, has {total_combinations}"
    
    def test_all_interpretations_have_required_fields(self):
        """Verify all interpretations have required data fields"""
        required_fields = ['verses', 'translation', 'detailed_effects', 
                          'positive_effects', 'challenging_effects']
        
        for planet, houses in BPHS_PLANETS_IN_HOUSES.items():
            for house, data in houses.items():
                for field in required_fields:
                    assert field in data, f"{planet} in {house} missing {field}"
                
                # Verify arrays have content
                assert len(data['detailed_effects']) > 0
                assert len(data['positive_effects']) > 0
                assert len(data['challenging_effects']) > 0
    
    def test_saravali_data_integrity(self):
        """Verify Saravali interpretations have proper structure"""
        for planet, houses in SARAVALI_PLANETS_IN_HOUSES.items():
            for house, data in houses.items():
                assert 'verses' in data
                assert 'translation' in data
                assert 'detailed_effects' in data
                assert 'positive_effects' in data
                assert 'challenging_effects' in data
    
    def test_yoga_data_integrity(self):
        """Verify all yogas have complete data"""
        yogas = get_all_yogas()
        
        assert len(yogas) == 27, f"Should have 27 yogas, has {len(yogas)}"
        
        for yoga_name, yoga_data in yogas.items():
            assert 'chapter' in yoga_data
            assert 'verses' in yoga_data
            assert 'category' in yoga_data
            assert 'formation' in yoga_data
            assert 'effects' in yoga_data


class TestIntegrationValidation:
    """Test integration between system components"""
    
    def test_interpretation_engine_all_planets(self):
        """Test interpretation engine with all planets"""
        engine = KnowledgeInterpretationEngine()
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        
        for planet in planets:
            # Test with house 1
            result = engine.interpret_planet_in_house(
                planet=planet,
                house=1,
                sign='Aries',
                dignity='neutral'
            )
            
            assert result is not None
            assert result.planet == planet
            assert result.house == 1
            assert result.metadata.confidence_score > 0.9
    
    def test_multi_source_engine_all_overlaps(self):
        """Test multi-source engine for all overlapping combinations"""
        engine = MultiSourceEngine()
        
        overlap_count = 0
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            for house in range(1, 13):
                sources = engine.get_available_sources(planet, house)
                if len(sources) > 1:
                    overlap_count += 1
                    # Test comparison works
                    comparison = engine.compare_sources(planet, house)
                    assert comparison is not None
                    assert comparison.confidence_score > 0.8
        
        assert overlap_count >= 10, "Should have at least 10 multi-source combinations"
    
    def test_source_attribution_completeness(self):
        """Verify all interpretations have complete source attribution"""
        engine = KnowledgeInterpretationEngine()
        
        test_cases = [
            ('Sun', 1), ('Moon', 4), ('Mars', 10),
            ('Mercury', 1), ('Jupiter', 9), ('Venus', 7), ('Saturn', 10)
        ]
        
        for planet, house in test_cases:
            result = engine.interpret_planet_in_house(
                planet=planet,
                house=house,
                sign='Leo',
                dignity='neutral'
            )
            
            citations = result.sources.get_all_citations()
            assert len(citations) > 0, f"No citations for {planet} in {house}"
            assert all('BPHS' in c or 'Brihat' in c for c in citations)


class TestPerformance:
    """Performance and scalability tests"""
    
    def test_single_interpretation_performance(self):
        """Test single interpretation completes quickly"""
        engine = KnowledgeInterpretationEngine()
        
        start = time.time()
        result = engine.interpret_planet_in_house('Sun', 10, 'Aries', 'exalted')
        duration = time.time() - start
        
        assert duration < 0.1, f"Interpretation took {duration}s, should be <0.1s"
        assert result is not None
    
    def test_multi_source_comparison_performance(self):
        """Test multi-source comparison completes quickly"""
        engine = MultiSourceEngine()
        
        start = time.time()
        comparison = engine.compare_sources('Sun', 1)
        duration = time.time() - start
        
        assert duration < 0.2, f"Comparison took {duration}s, should be <0.2s"
        assert comparison is not None
    
    def test_full_chart_performance(self):
        """Test complete 7-planet chart interpretation performance"""
        engine = KnowledgeInterpretationEngine()
        planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        
        start = time.time()
        results = []
        for i, planet in enumerate(planets, 1):
            result = engine.interpret_planet_in_house(planet, i, 'Aries', 'neutral')
            results.append(result)
        duration = time.time() - start
        
        assert len(results) == 7
        assert duration < 1.0, f"Full chart took {duration}s, should be <1s"


class TestProductionReadiness:
    """Validate production readiness"""
    
    def test_error_handling_missing_planet(self):
        """Test graceful handling of invalid planet"""
        engine = KnowledgeInterpretationEngine()
        
        with pytest.raises(ValueError):
            engine.interpret_planet_in_house('InvalidPlanet', 1, 'Aries', 'neutral')
    
    def test_error_handling_invalid_house(self):
        """Test handling of invalid house number"""
        engine = KnowledgeInterpretationEngine()
        
        # Should raise error for house outside 1-12
        try:
            result = engine.interpret_planet_in_house('Sun', 13, 'Aries', 'neutral')
            # If it doesn't raise, check result is None or empty
            assert result is None or hasattr(result, 'error')
        except (ValueError, KeyError):
            # Expected behavior
            assert True
    
    def test_confidence_scores_valid_range(self):
        """Verify all confidence scores are in valid range"""
        engine = KnowledgeInterpretationEngine()
        
        test_cases = [
            ('Sun', 10), ('Moon', 4), ('Jupiter', 1),
            ('Venus', 7), ('Saturn', 10)
        ]
        
        for planet, house in test_cases:
            result = engine.interpret_planet_in_house(planet, house, 'Leo', 'neutral')
            assert 0.0 <= result.metadata.confidence_score <= 1.0
            assert isinstance(result.metadata.confidence_score, float)
    
    def test_no_empty_interpretations(self):
        """Verify no interpretations are empty"""
        for planet, houses in BPHS_PLANETS_IN_HOUSES.items():
            for house, data in houses.items():
                assert len(data['translation']) > 20, f"Empty translation for {planet}/{house}"
                assert len(data['detailed_effects']) > 0
                assert all(len(effect) > 0 for effect in data['detailed_effects'])


class TestCoverageStatistics:
    """Validate coverage statistics"""
    
    def test_total_interpretation_count(self):
        """Verify total interpretation count"""
        bphs_count = sum(len(houses) for houses in BPHS_PLANETS_IN_HOUSES.values())
        saravali_count = sum(len(houses) for houses in SARAVALI_PLANETS_IN_HOUSES.values())
        yoga_count = len(get_all_yogas())
        
        total = bphs_count + saravali_count + yoga_count
        
        assert bphs_count == 84
        assert saravali_count >= 10
        assert yoga_count == 27
        assert total >= 121  # At least 121 total interpretations
    
    def test_multi_source_coverage(self):
        """Verify multi-source coverage statistics"""
        engine = MultiSourceEngine()
        
        bphs_only = 0
        multi_source = 0
        
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            for house in range(1, 13):
                sources = engine.get_available_sources(planet, house)
                if len(sources) == 1:
                    bphs_only += 1
                elif len(sources) > 1:
                    multi_source += 1
        
        assert bphs_only + multi_source == 84  # Should cover all combinations
        assert multi_source >= 10  # At least 10 with multiple sources
    
    def test_category_distribution(self):
        """Test yoga category distribution"""
        yogas = get_all_yogas()
        categories = {}
        
        for yoga in yogas.values():
            category = yoga.get('category', 'Other')
            categories[category] = categories.get(category, 0) + 1
        
        # Should have multiple categories
        assert len(categories) >= 5
        
        # Should have some in each major category
        assert categories.get('Wealth Yoga', 0) > 0
        assert categories.get('Raja Yoga', 0) > 0
        assert categories.get('Mahapurusha Yoga', 0) > 0
