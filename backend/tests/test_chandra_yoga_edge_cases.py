"""
Edge case tests for Chandra (Moon-based) yogas after classical compliance fixes.

Tests verify that Sunapha, Anapha, and Durudhara yogas now correctly detect:
- All planets except Sun (not just benefics)
- Proper strength variation based on planet types
- Mixed planet scenarios

Reference: BPHS Chapter 41, Verses 47-49
"""
import pytest
from app.core.calculations.extended_yogas import ExtendedYogaCalculator


class TestChandraYogasEdgeCases:
    """Test edge cases for fixed Chandra yoga detection"""
    
    def test_sunapha_with_benefic_jupiter(self):
        """Sunapha: Jupiter (benefic) in 2nd from Moon"""
        # Moon in house 5, Jupiter in house 6 (2nd from Moon)
        planets = {
            "Moon": {"house": 5, "sign": 4, "longitude": 135.0},
            "Jupiter": {"house": 6, "sign": 5, "longitude": 165.0},
            "Sun": {"house": 3, "sign": 2, "longitude": 75.0}
        }
        houses = {
            5: ["Moon"],
            6: ["Jupiter"],
            3: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        sunapha_yogas = [y for y in yogas if y.name == "Sunapha Yoga"]
        assert len(sunapha_yogas) == 1, "Should detect Sunapha with Jupiter"
        assert sunapha_yogas[0].strength == 80, "Pure benefic should have strength 80"
        assert "Jupiter" in sunapha_yogas[0].planets_involved
    
    def test_sunapha_with_malefic_mars(self):
        """Sunapha: Mars (malefic) in 2nd from Moon - NEW after fix"""
        # Moon in house 5, Mars in house 6
        planets = {
            "Moon": {"house": 5, "sign": 4, "longitude": 135.0},
            "Mars": {"house": 6, "sign": 5, "longitude": 165.0},
            "Sun": {"house": 3, "sign": 2, "longitude": 75.0}
        }
        houses = {
            5: ["Moon"],
            6: ["Mars"],
            3: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        sunapha_yogas = [y for y in yogas if y.name == "Sunapha Yoga"]
        assert len(sunapha_yogas) == 1, "Should detect Sunapha with Mars (post-fix)"
        assert sunapha_yogas[0].strength == 65, "Pure malefic should have strength 65"
        assert "Mars" in sunapha_yogas[0].planets_involved
    
    def test_sunapha_with_saturn_malefic(self):
        """Sunapha: Saturn (malefic) in 2nd from Moon - NEW after fix"""
        planets = {
            "Moon": {"house": 2, "sign": 1, "longitude": 45.0},
            "Saturn": {"house": 3, "sign": 2, "longitude": 75.0},
            "Sun": {"house": 1, "sign": 0, "longitude": 15.0}
        }
        houses = {
            2: ["Moon"],
            3: ["Saturn"],
            1: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        sunapha_yogas = [y for y in yogas if y.name == "Sunapha Yoga"]
        assert len(sunapha_yogas) == 1, "Should detect Sunapha with Saturn"
        assert sunapha_yogas[0].strength == 65, "Saturn malefic should have strength 65"
    
    def test_sunapha_with_node_rahu(self):
        """Sunapha: Rahu (node) in 2nd from Moon - NEW after fix"""
        planets = {
            "Moon": {"house": 4, "sign": 3, "longitude": 105.0},
            "Rahu": {"house": 5, "sign": 4, "longitude": 135.0},
            "Sun": {"house": 2, "sign": 1, "longitude": 45.0}
        }
        houses = {
            4: ["Moon"],
            5: ["Rahu"],
            2: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        sunapha_yogas = [y for y in yogas if y.name == "Sunapha Yoga"]
        assert len(sunapha_yogas) == 1, "Should detect Sunapha with Rahu"
        assert sunapha_yogas[0].strength == 60, "Pure nodes should have strength 60"
    
    def test_sunapha_excludes_sun(self):
        """Sunapha: Should NOT detect when only Sun in 2nd from Moon"""
        planets = {
            "Moon": {"house": 3, "sign": 2, "longitude": 75.0},
            "Sun": {"house": 4, "sign": 3, "longitude": 105.0},
            "Jupiter": {"house": 1, "sign": 0, "longitude": 15.0}
        }
        houses = {
            3: ["Moon"],
            4: ["Sun"],
            1: ["Jupiter"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        sunapha_yogas = [y for y in yogas if y.name == "Sunapha Yoga"]
        assert len(sunapha_yogas) == 0, "Should NOT detect Sunapha with only Sun"
    
    def test_sunapha_mixed_benefic_malefic(self):
        """Sunapha: Mixed benefic + malefic in 2nd from Moon"""
        planets = {
            "Moon": {"house": 1, "sign": 0, "longitude": 15.0},
            "Jupiter": {"house": 2, "sign": 1, "longitude": 45.0},
            "Mars": {"house": 2, "sign": 1, "longitude": 48.0},
            "Sun": {"house": 5, "sign": 4, "longitude": 135.0}
        }
        houses = {
            1: ["Moon"],
            2: ["Jupiter", "Mars"],
            5: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        sunapha_yogas = [y for y in yogas if y.name == "Sunapha Yoga"]
        assert len(sunapha_yogas) == 1, "Should detect Sunapha with mixed planets"
        assert sunapha_yogas[0].strength == 70, "Mixed should have strength 70"
        assert "Jupiter" in sunapha_yogas[0].planets_involved
        assert "Mars" in sunapha_yogas[0].planets_involved
    
    def test_anapha_with_malefic_saturn(self):
        """Anapha: Saturn (malefic) in 12th from Moon - NEW after fix"""
        # Moon in house 5, Saturn in house 4 (12th from Moon)
        planets = {
            "Moon": {"house": 5, "sign": 4, "longitude": 135.0},
            "Saturn": {"house": 4, "sign": 3, "longitude": 105.0},
            "Sun": {"house": 1, "sign": 0, "longitude": 15.0}
        }
        houses = {
            5: ["Moon"],
            4: ["Saturn"],
            1: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        anapha_yogas = [y for y in yogas if y.name == "Anapha Yoga"]
        assert len(anapha_yogas) == 1, "Should detect Anapha with Saturn"
        assert anapha_yogas[0].strength == 65, "Malefic should have strength 65"
        assert "Saturn" in anapha_yogas[0].planets_involved
    
    def test_anapha_with_node_ketu(self):
        """Anapha: Ketu (node) in 12th from Moon - NEW after fix"""
        planets = {
            "Moon": {"house": 8, "sign": 7, "longitude": 225.0},
            "Ketu": {"house": 7, "sign": 6, "longitude": 195.0},
            "Sun": {"house": 2, "sign": 1, "longitude": 45.0}
        }
        houses = {
            8: ["Moon"],
            7: ["Ketu"],
            2: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        anapha_yogas = [y for y in yogas if y.name == "Anapha Yoga"]
        assert len(anapha_yogas) == 1, "Should detect Anapha with Ketu"
        assert anapha_yogas[0].strength == 60, "Node should have strength 60"
    
    def test_durudhara_benefic_and_malefic(self):
        """Durudhara: Benefic in 2nd, Malefic in 12th from Moon"""
        planets = {
            "Moon": {"house": 6, "sign": 5, "longitude": 165.0},
            "Venus": {"house": 7, "sign": 6, "longitude": 195.0},  # 2nd
            "Mars": {"house": 5, "sign": 4, "longitude": 135.0},   # 12th
            "Sun": {"house": 1, "sign": 0, "longitude": 15.0}
        }
        houses = {
            6: ["Moon"],
            7: ["Venus"],
            5: ["Mars"],
            1: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        durudhara_yogas = [y for y in yogas if y.name == "Durudhara Yoga"]
        assert len(durudhara_yogas) == 1, "Should detect Durudhara with mixed"
        assert durudhara_yogas[0].strength == 80, "Mixed Durudhara has strength 80 (stronger than individual yogas)"
        assert "Venus" in durudhara_yogas[0].planets_involved
        assert "Mars" in durudhara_yogas[0].planets_involved
    
    def test_durudhara_both_malefics(self):
        """Durudhara: Both malefics on each side - NEW after fix"""
        planets = {
            "Moon": {"house": 3, "sign": 2, "longitude": 75.0},
            "Mars": {"house": 4, "sign": 3, "longitude": 105.0},     # 2nd
            "Saturn": {"house": 2, "sign": 1, "longitude": 45.0},     # 12th
            "Sun": {"house": 8, "sign": 7, "longitude": 225.0}
        }
        houses = {
            3: ["Moon"],
            4: ["Mars"],
            2: ["Saturn"],
            8: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        durudhara_yogas = [y for y in yogas if y.name == "Durudhara Yoga"]
        assert len(durudhara_yogas) == 1, "Should detect Durudhara with malefics"
        assert durudhara_yogas[0].strength == 70, "Pure malefics Durudhara has strength 70"
    
    def test_durudhara_nodes_on_both_sides(self):
        """Durudhara: Rahu in 2nd, Ketu in 12th - NEW after fix"""
        planets = {
            "Moon": {"house": 10, "sign": 9, "longitude": 285.0},
            "Rahu": {"house": 11, "sign": 10, "longitude": 315.0},  # 2nd
            "Ketu": {"house": 9, "sign": 8, "longitude": 255.0},    # 12th
            "Sun": {"house": 4, "sign": 3, "longitude": 105.0}
        }
        houses = {
            10: ["Moon"],
            11: ["Rahu"],
            9: ["Ketu"],
            4: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        durudhara_yogas = [y for y in yogas if y.name == "Durudhara Yoga"]
        assert len(durudhara_yogas) == 1, "Should detect Durudhara with nodes"
        assert durudhara_yogas[0].strength == 65, "Pure nodes Durudhara has strength 65"
    
    def test_no_chandra_yoga_when_sun_only(self):
        """No Chandra yoga when only Sun present (classical compliance)"""
        planets = {
            "Moon": {"house": 7, "sign": 6, "longitude": 195.0},
            "Sun": {"house": 8, "sign": 7, "longitude": 225.0},     # 2nd
            "Jupiter": {"house": 3, "sign": 2, "longitude": 75.0}
        }
        houses = {
            7: ["Moon"],
            8: ["Sun"],
            3: ["Jupiter"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        chandra_yogas = [y for y in yogas if y.name in ["Sunapha Yoga", "Anapha Yoga", "Durudhara Yoga"]]
        assert len(chandra_yogas) == 0, "Should not detect any Chandra yoga with only Sun"
    
    def test_complex_scenario_multiple_planets(self):
        """Complex: Multiple planets in 2nd and 12th from Moon"""
        planets = {
            "Moon": {"house": 6, "sign": 5, "longitude": 165.0},
            "Jupiter": {"house": 7, "sign": 6, "longitude": 195.0},   # 2nd (benefic)
            "Mercury": {"house": 7, "sign": 6, "longitude": 198.0},   # 2nd (benefic)
            "Mars": {"house": 5, "sign": 4, "longitude": 135.0},      # 12th (malefic)
            "Saturn": {"house": 5, "sign": 4, "longitude": 138.0},    # 12th (malefic)
            "Sun": {"house": 1, "sign": 0, "longitude": 15.0}
        }
        houses = {
            6: ["Moon"],
            7: ["Jupiter", "Mercury"],
            5: ["Mars", "Saturn"],
            1: ["Sun"]
        }
        
        calc = ExtendedYogaCalculator()
        yogas = calc.calculate_all_yogas(planets, houses, ascendant_sign=0)
        
        # Should detect Durudhara (both sides have planets)
        durudhara_yogas = [y for y in yogas if y.name == "Durudhara Yoga"]
        assert len(durudhara_yogas) == 1, "Should detect Durudhara with multiple planets"
        
        # Strength should be 80 (mixed benefics and malefics - Durudhara is stronger)
        assert durudhara_yogas[0].strength == 80, "Mixed Durudhara should have strength 80"
        
        # All planets except Sun should be involved
        involved = durudhara_yogas[0].planets_involved
        assert "Jupiter" in involved
        assert "Mercury" in involved
        assert "Mars" in involved
        assert "Saturn" in involved
        assert "Sun" not in involved


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
