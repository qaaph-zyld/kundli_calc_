"""
Test Knowledge-Based Interpretation Engine
===========================================
Validates classical text interpretations and source attribution.
"""
import pytest
from backend.app.core.knowledge.engine.interpretation_engine import KnowledgeInterpretationEngine
from backend.app.core.knowledge.schemas.interpretation_schema import PlanetaryDignity
from backend.app.core.knowledge.sources.bphs_planets_in_houses import BPHS_PLANETS_IN_HOUSES


class TestKnowledgeEngine:
    """Test interpretation engine functionality"""
    
    @pytest.fixture
    def engine(self):
        """Create engine instance"""
        return KnowledgeInterpretationEngine()
    
    def test_engine_initialization(self, engine):
        """Test engine initializes correctly"""
        assert engine is not None
        assert len(engine.source_priority) > 0
    
    def test_available_interpretations(self, engine):
        """Test getting available interpretations"""
        available = engine.get_available_interpretations()
        assert len(available) >= 7  # Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
        assert 'Sun' in available
        assert 'Moon' in available
        assert 'Jupiter' in available
    
    def test_sun_in_tenth_interpretation(self, engine):
        """Test Sun in 10th house interpretation"""
        result = engine.interpret_planet_in_house(
            planet='Sun',
            house=10,
            sign='Aries',
            dignity=PlanetaryDignity.EXALTED
        )
        
        assert result.planet == 'Sun'
        assert result.house == 10
        assert result.dignity == PlanetaryDignity.EXALTED
        assert len(result.general_effects) > 100
        assert result.sources is not None
        assert len(result.sources.get_all_citations()) > 0
        assert 'Brihat Parashara Hora Shastra' in result.sources.get_all_citations()[0]
        assert result.metadata.confidence_score >= 0.9
    
    def test_moon_in_fourth_interpretation(self, engine):
        """Test Moon in 4th house - excellent placement"""
        result = engine.interpret_planet_in_house(
            planet='Moon',
            house=4,
            sign='Taurus',
            dignity='exalted'
        )
        
        assert result.planet == 'Moon'
        assert result.house == 4
        assert 'mother' in result.general_effects.lower()
        assert result.metadata.confidence_score > 0.8
    
    def test_venus_in_seventh_interpretation(self, engine):
        """Test Venus in 7th house - marriage placement"""
        result = engine.interpret_planet_in_house(
            planet='Venus',
            house=7,
            sign='Pisces',
            dignity=PlanetaryDignity.EXALTED
        )
        
        assert result.planet == 'Venus'
        assert result.house == 7
        assert 'marriage' in result.general_effects.lower() or 'spouse' in result.general_effects.lower()
        assert len(result.remedies) > 0
    
    def test_saturn_in_tenth_interpretation(self, engine):
        """Test Saturn in 10th house - excellent for career"""
        result = engine.interpret_planet_in_house(
            planet='Saturn',
            house=10,
            sign='Capricorn',
            dignity=PlanetaryDignity.OWN_SIGN
        )
        
        assert result.planet == 'Saturn'
        assert result.house == 10
        assert 'career' in result.general_effects.lower()
        assert result.strong_placement_effects is not None
    
    def test_jupiter_in_first_interpretation(self, engine):
        """Test Jupiter in 1st house"""
        result = engine.interpret_planet_in_house(
            planet='Jupiter',
            house=1,
            sign='Sagittarius',
            dignity=PlanetaryDignity.OWN_SIGN
        )
        
        assert result.planet == 'Jupiter'
        assert 'wisdom' in result.general_effects.lower() or 'fortune' in result.general_effects.lower()
    
    def test_source_attribution_complete(self, engine):
        """Test that all interpretations have proper source attribution"""
        result = engine.interpret_planet_in_house(
            planet='Sun',
            house=1,
            sign='Leo',
            dignity=PlanetaryDignity.OWN_SIGN
        )
        
        # Check source structure
        assert result.sources.primary_sources is not None
        assert len(result.sources.primary_sources) > 0
        
        primary = result.sources.primary_sources[0]
        assert primary.citation.text.value == "Brihat Parashara Hora Shastra"
        assert primary.citation.chapter == 24
        assert primary.citation.verses is not None
        assert primary.citation.translator is not None
        assert primary.confidence.value in ['direct_quote', 'direct_interpretation']
    
    def test_dignity_string_conversion(self, engine):
        """Test that dignity accepts both string and enum"""
        result1 = engine.interpret_planet_in_house('Sun', 10, 'Aries', 'exalted')
        result2 = engine.interpret_planet_in_house('Sun', 10, 'Aries', PlanetaryDignity.EXALTED)
        
        assert result1.dignity == result2.dignity
    
    def test_missing_interpretation_raises_error(self, engine):
        """Test that missing interpretations raise proper error"""
        with pytest.raises(ValueError, match="No BPHS interpretation found"):
            engine.interpret_planet_in_house('Sun', 8, 'Cancer', PlanetaryDignity.DEBILITATED)
    
    def test_metadata_tags(self, engine):
        """Test that metadata includes proper tags"""
        result = engine.interpret_planet_in_house('Venus', 7, 'Pisces', 'exalted')
        
        assert 'venus' in result.metadata.tags
        assert 'house_7' in result.metadata.tags
        assert 'pisces' in result.metadata.tags
        assert 'exalted' in result.metadata.tags
        assert 'bphs' in result.metadata.tags
    
    def test_life_areas_populated(self, engine):
        """Test that life areas are properly populated when available in source"""
        result = engine.interpret_planet_in_house('Sun', 10, 'Aries', 'exalted')
        
        # Life areas populated if in BPHS data, otherwise check timing or general effects mention life areas
        if len(result.life_areas) > 0:
            from backend.app.core.knowledge.schemas.interpretation_schema import LifeArea
            assert LifeArea.CAREER_STATUS in result.life_areas or 'career' in str(result.life_areas)
        else:
            # Check that career is mentioned in general effects or timing
            assert 'career' in result.general_effects.lower() or 'career' in (result.timing_notes or '').lower()


class TestBPHSDataIntegrity:
    """Test BPHS data structure integrity"""
    
    def test_all_planets_have_data(self):
        """Test that key planets are in knowledge base"""
        expected_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        for planet in expected_planets:
            assert planet in BPHS_PLANETS_IN_HOUSES
    
    def test_interpretation_structure(self):
        """Test that interpretations have required fields"""
        for planet, houses in BPHS_PLANETS_IN_HOUSES.items():
            for house, data in houses.items():
                assert 'verses' in data
                assert 'translation' in data
                assert isinstance(data['verses'], str)
                assert isinstance(data['translation'], str)
                assert len(data['translation']) > 20
    
    def test_coverage_statistics(self):
        """Test knowledge base coverage"""
        total_combinations = sum(len(houses) for houses in BPHS_PLANETS_IN_HOUSES.values())
        assert total_combinations >= 25  # Should have at least 25 interpretations
        
        # Check specific important combinations
        assert 10 in BPHS_PLANETS_IN_HOUSES['Sun']  # Sun in 10th
        assert 7 in BPHS_PLANETS_IN_HOUSES['Venus']  # Venus in 7th
        assert 10 in BPHS_PLANETS_IN_HOUSES['Saturn']  # Saturn in 10th
        assert 4 in BPHS_PLANETS_IN_HOUSES['Moon']  # Moon in 4th
