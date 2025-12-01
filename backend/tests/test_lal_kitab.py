"""
Lal Kitab System Tests
=======================
Tests the Lal Kitab prediction system including:
- Planet analysis in houses
- Pakka Ghar calculations
- Karmic debt detection
- Remedy generation
"""

import pytest
from app.core.calculations.lal_kitab import (
    LalKitabCalculator,
    get_lal_kitab_analysis,
    get_planet_remedy,
    PAKKA_GHAR,
    EXALTED_HOUSES,
    DEBILITATED_HOUSES,
    PLANETS,
    LAL_KITAB_REMEDIES,
    KarmicDebt
)


class TestPakkaGhar:
    """Test Pakka Ghar (permanent house) concept"""
    
    def test_all_planets_have_pakka_ghar(self):
        """Each planet should have a defined Pakka Ghar"""
        for planet in PLANETS:
            assert planet in PAKKA_GHAR, f"{planet} missing Pakka Ghar"
            assert 1 <= PAKKA_GHAR[planet] <= 12
    
    def test_sun_pakka_ghar_is_first(self):
        """Sun's Pakka Ghar should be 1st house"""
        assert PAKKA_GHAR["Sun"] == 1
    
    def test_moon_pakka_ghar_is_fourth(self):
        """Moon's Pakka Ghar should be 4th house"""
        assert PAKKA_GHAR["Moon"] == 4
    
    def test_saturn_pakka_ghar_is_eighth(self):
        """Saturn's Pakka Ghar should be 8th house"""
        assert PAKKA_GHAR["Saturn"] == 8


class TestPlanetAnalysis:
    """Test individual planet analysis"""
    
    @pytest.fixture
    def calculator(self):
        return LalKitabCalculator()
    
    def test_sun_in_pakka_ghar_excellent(self, calculator):
        """Sun in 1st house (Pakka Ghar) should give excellent results"""
        positions = {"Sun": 1, "Moon": 4, "Mars": 3}
        chart = calculator.analyze_chart(positions)
        
        assert chart.planets["Sun"].is_in_pakka_ghar == True
        assert chart.planets["Sun"].result_type == "excellent"
        assert chart.planets["Sun"].strength_score > 70
    
    def test_sun_in_debilitated_house(self, calculator):
        """Sun in 7th house should give poor results"""
        positions = {"Sun": 7}
        chart = calculator.analyze_chart(positions)
        
        assert chart.planets["Sun"].result_type == "poor"
        assert chart.planets["Sun"].remedy_needed == True
    
    def test_planet_strength_calculation(self, calculator):
        """Strength score should be between 0 and 100"""
        positions = {planet: (i % 12) + 1 for i, planet in enumerate(PLANETS)}
        chart = calculator.analyze_chart(positions)
        
        for planet, analysis in chart.planets.items():
            assert 0 <= analysis.strength_score <= 100
    
    def test_remedies_generated_for_afflicted_planet(self, calculator):
        """Afflicted planets should have remedies"""
        positions = {"Sun": 12}  # Sun afflicted in 12th
        chart = calculator.analyze_chart(positions)
        
        assert len(chart.planets["Sun"].remedies_hindi) > 0
        assert len(chart.planets["Sun"].remedies_english) > 0


class TestKarmicDebts:
    """Test karmic debt (Rin) detection"""
    
    @pytest.fixture
    def calculator(self):
        return LalKitabCalculator()
    
    def test_pitra_rin_detection(self, calculator):
        """Pitra Rin should be detected when Jupiter and Ketu afflicted"""
        positions = {
            "Jupiter": 2,  # Jupiter in 2nd (condition met)
            "Ketu": 5,     # Ketu in 5th (condition met)
            "Sun": 5       # Sun in 5th (condition met)
        }
        chart = calculator.analyze_chart(positions)
        
        # Should detect Pitra Rin
        pitra_rin = [d for d in chart.karmic_debts 
                     if d.debt_type == KarmicDebt.PITRA_RIN]
        assert len(pitra_rin) > 0
    
    def test_karmic_debt_has_remedies(self, calculator):
        """Detected karmic debts should have remedies"""
        positions = {"Jupiter": 2, "Ketu": 5, "Sun": 5}
        chart = calculator.analyze_chart(positions)
        
        for debt in chart.karmic_debts:
            assert len(debt.remedies_hindi) > 0
            assert len(debt.remedies_english) > 0


class TestLalKitabAnalysis:
    """Test complete Lal Kitab analysis"""
    
    def test_complete_analysis_structure(self):
        """Analysis should contain all required fields"""
        positions = {
            "Sun": 10, "Moon": 4, "Mars": 6,
            "Mercury": 9, "Jupiter": 2, "Venus": 7,
            "Saturn": 11, "Rahu": 3, "Ketu": 9
        }
        
        result = get_lal_kitab_analysis(positions)
        
        # Check structure
        assert "planets" in result
        assert "karmic_debts" in result
        assert "overall_score" in result
        assert "lucky" in result
        assert "predictions" in result
        assert "priority_remedies" in result
    
    def test_all_planets_analyzed(self):
        """All provided planets should be analyzed"""
        positions = {
            "Sun": 1, "Moon": 4, "Mars": 3,
            "Mercury": 7, "Jupiter": 2
        }
        
        result = get_lal_kitab_analysis(positions)
        
        for planet in positions.keys():
            assert planet in result["planets"]
    
    def test_lucky_items_present(self):
        """Lucky numbers, colors, and directions should be present"""
        positions = {"Sun": 1, "Moon": 4}
        result = get_lal_kitab_analysis(positions)
        
        assert "numbers" in result["lucky"]
        assert "colors" in result["lucky"]
        assert "directions" in result["lucky"]
    
    def test_bilingual_predictions(self):
        """Predictions should be in both Hindi and English"""
        positions = {"Sun": 1, "Moon": 4}
        result = get_lal_kitab_analysis(positions)
        
        assert "hindi" in result["predictions"]
        assert "english" in result["predictions"]
        assert len(result["predictions"]["hindi"]) > 0
        assert len(result["predictions"]["english"]) > 0


class TestRemedies:
    """Test Lal Kitab remedies"""
    
    def test_all_planets_have_remedies(self):
        """Each planet should have defined remedies"""
        for planet in PLANETS:
            assert planet in LAL_KITAB_REMEDIES
            assert "general" in LAL_KITAB_REMEDIES[planet]
    
    def test_remedies_bilingual(self):
        """Remedies should be in Hindi and English"""
        for planet, remedies in LAL_KITAB_REMEDIES.items():
            general = remedies.get("general", {})
            assert "hindi" in general
            assert "english" in general
            assert len(general["hindi"]) > 0
            assert len(general["english"]) > 0
    
    def test_get_planet_remedy_function(self):
        """get_planet_remedy should return correct structure"""
        remedy = get_planet_remedy("Sun", 7)
        
        assert "planet" in remedy
        assert "house" in remedy
        assert "general_remedies" in remedy
        assert remedy["planet"] == "Sun"
        assert remedy["house"] == 7


class TestExaltedDebilitated:
    """Test exalted and debilitated house lists"""
    
    def test_all_planets_have_exalted_houses(self):
        """Each planet should have exalted houses defined"""
        for planet in PLANETS:
            assert planet in EXALTED_HOUSES
            assert len(EXALTED_HOUSES[planet]) > 0
    
    def test_all_planets_have_debilitated_houses(self):
        """Each planet should have debilitated houses defined"""
        for planet in PLANETS:
            assert planet in DEBILITATED_HOUSES
            assert len(DEBILITATED_HOUSES[planet]) > 0
    
    def test_no_overlap_exalted_debilitated(self):
        """A house should not be both exalted and debilitated for same planet"""
        for planet in PLANETS:
            exalted = set(EXALTED_HOUSES.get(planet, []))
            debilitated = set(DEBILITATED_HOUSES.get(planet, []))
            overlap = exalted.intersection(debilitated)
            assert len(overlap) == 0, f"{planet} has overlapping houses: {overlap}"


class TestOverallScore:
    """Test overall chart score calculation"""
    
    @pytest.fixture
    def calculator(self):
        return LalKitabCalculator()
    
    def test_good_chart_high_score(self, calculator):
        """Chart with planets in pakka ghar should have high score"""
        positions = {
            "Sun": 1,   # Pakka Ghar
            "Moon": 4,  # Pakka Ghar
            "Mars": 3,  # Pakka Ghar
        }
        chart = calculator.analyze_chart(positions)
        
        assert chart.overall_score > 60
    
    def test_afflicted_chart_lower_score(self, calculator):
        """Chart with many debilitated planets should have lower score"""
        positions = {
            "Sun": 7,   # Debilitated
            "Moon": 8,  # Debilitated
            "Saturn": 1,  # Debilitated
        }
        chart = calculator.analyze_chart(positions)
        
        assert chart.overall_score < 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
