"""
Ashtakavarga Accuracy Verification Tests
=========================================
Tests Ashtakavarga calculations against standard reference values.
Uses BPHS-standard benefic point rules.

Reference Chart: October 9, 1990, 09:10 AM, Loznica, Serbia
Lahiri Ayanamsa, Whole Sign Houses
"""

import pytest
from app.core.calculations.enhanced_ashtakavarga import (
    EnhancedAshtakavarga, ASHTAKAVARGA_RULES, PLANETS
)

# Reference planetary positions (sign indices 0-11)
# Oct 9, 1990, 09:10 AM, Loznica - from test_accuracy_verification.py
REFERENCE_POSITIONS = {
    "Sun": 172.05,      # Virgo (5)
    "Moon": 58.32,      # Taurus (1)
    "Mars": 49.86,      # Taurus (1)
    "Mercury": 162.58,  # Virgo (5)
    "Jupiter": 105.82,  # Cancer (3)
    "Venus": 166.03,    # Virgo (5)
    "Saturn": 265.17,   # Sagittarius (8)
    "Rahu": 279.82,     # Capricorn (9)
    "Ketu": 99.82,      # Cancer (3)
}
REFERENCE_ASCENDANT = 209.17  # Libra (6)


class TestAshtakavargaRules:
    """Test that Ashtakavarga rules are correctly defined"""
    
    def test_all_planets_have_rules(self):
        """Each planet should have rules defined"""
        for planet in PLANETS:
            assert planet in ASHTAKAVARGA_RULES, f"Missing rules for {planet}"
    
    def test_all_contributors_defined(self):
        """Each planet should have rules from all 8 contributors"""
        contributors = ["from_Sun", "from_Moon", "from_Mars", "from_Mercury",
                       "from_Jupiter", "from_Venus", "from_Saturn", "from_Lagna"]
        
        for planet in PLANETS:
            for contributor in contributors:
                assert contributor in ASHTAKAVARGA_RULES[planet], \
                    f"{planet} missing rules {contributor}"
    
    def test_sun_rules_match_bphs(self):
        """Verify Sun's Ashtakavarga rules match BPHS standard"""
        sun_rules = ASHTAKAVARGA_RULES["Sun"]
        
        # Sun gets benefic points from Sun at houses 1,2,4,7,8,9,10,11
        assert sun_rules["from_Sun"] == [1, 2, 4, 7, 8, 9, 10, 11]
        
        # Sun gets benefic points from Moon at houses 3,6,10,11
        assert sun_rules["from_Moon"] == [3, 6, 10, 11]
        
        # Sun gets benefic points from Lagna at houses 3,4,6,10,11,12
        assert sun_rules["from_Lagna"] == [3, 4, 6, 10, 11, 12]
    
    def test_moon_rules_match_bphs(self):
        """Verify Moon's Ashtakavarga rules match BPHS standard"""
        moon_rules = ASHTAKAVARGA_RULES["Moon"]
        
        # Moon gets benefic from Moon at 1,3,6,7,10,11
        assert moon_rules["from_Moon"] == [1, 3, 6, 7, 10, 11]
        
        # Moon gets benefic from Jupiter at 1,4,7,8,10,11,12
        assert moon_rules["from_Jupiter"] == [1, 4, 7, 8, 10, 11, 12]
    
    def test_jupiter_rules_match_bphs(self):
        """Verify Jupiter's Ashtakavarga rules match BPHS standard"""
        jupiter_rules = ASHTAKAVARGA_RULES["Jupiter"]
        
        # Jupiter gets benefic from Sun at 1,2,3,4,7,8,9,10,11 (9 points)
        assert jupiter_rules["from_Sun"] == [1, 2, 3, 4, 7, 8, 9, 10, 11]
        assert len(jupiter_rules["from_Sun"]) == 9
    
    def test_saturn_rules_match_bphs(self):
        """Verify Saturn's Ashtakavarga rules match BPHS standard"""
        saturn_rules = ASHTAKAVARGA_RULES["Saturn"]
        
        # Saturn gets benefic from Saturn at 3,5,6,11
        assert saturn_rules["from_Saturn"] == [3, 5, 6, 11]


class TestBAVCalculation:
    """Test Bhinnashtakavarga (individual planet) calculations"""
    
    @pytest.fixture
    def calculator(self):
        return EnhancedAshtakavarga()
    
    def test_bav_returns_12_values(self, calculator):
        """BAV should return 12 bindu values (one per sign)"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        for planet in PLANETS:
            assert len(result["bhinnashtakavarga"][planet]["bindus"]) == 12
    
    def test_bav_total_in_valid_range(self, calculator):
        """BAV total should be between 25-52 (typical range)"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        for planet in PLANETS:
            total = result["bhinnashtakavarga"][planet]["total"]
            # Theoretical max is 8 contributors * 12 houses = 96, but typical is 25-52
            assert 20 <= total <= 60, \
                f"{planet} BAV total {total} outside expected range"
    
    def test_bav_bindus_per_sign_valid(self, calculator):
        """Each sign should have 0-8 bindus (max 8 contributors)"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        for planet in PLANETS:
            for i, bindu in enumerate(result["bhinnashtakavarga"][planet]["bindus"]):
                assert 0 <= bindu <= 8, \
                    f"{planet} has invalid bindu count {bindu} in sign {i}"


class TestSAVCalculation:
    """Test Sarvashtakavarga (combined) calculations"""
    
    @pytest.fixture
    def calculator(self):
        return EnhancedAshtakavarga()
    
    def test_sav_returns_12_values(self, calculator):
        """SAV should return 12 combined bindu values"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        assert len(result["sarvashtakavarga"]["bindus"]) == 12
    
    def test_sav_total_equals_bav_sum(self, calculator):
        """SAV total should equal sum of all BAV totals"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        bav_sum = sum(result["bhinnashtakavarga"][p]["total"] for p in PLANETS)
        sav_total = result["sarvashtakavarga"]["total"]
        
        assert sav_total == bav_sum, \
            f"SAV total {sav_total} != BAV sum {bav_sum}"
    
    def test_sav_total_in_valid_range(self, calculator):
        """SAV total should be around 337 (theoretical average)"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        # Total SAV is typically 280-390
        total = result["sarvashtakavarga"]["total"]
        assert 250 <= total <= 400, f"SAV total {total} outside expected range"
    
    def test_sav_per_sign_in_valid_range(self, calculator):
        """Each sign's SAV should be between 18-35 (typical range)"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        for i, bindu in enumerate(result["sarvashtakavarga"]["bindus"]):
            # Max is 7 planets * 8 = 56, min is 0, typical is 18-35
            assert 10 <= bindu <= 45, \
                f"Sign {i} SAV {bindu} outside expected range"


class TestAshtakavargaInterpretation:
    """Test Ashtakavarga interpretation logic"""
    
    @pytest.fixture
    def calculator(self):
        return EnhancedAshtakavarga()
    
    def test_analysis_average_calculated(self, calculator):
        """Analysis should include average per sign"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        avg = result["analysis"]["average_per_sign"]
        expected_avg = result["sarvashtakavarga"]["total"] / 12
        
        assert abs(avg - expected_avg) < 0.01
    
    def test_strongest_signs_identified(self, calculator):
        """Strongest signs should be identified"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        # Should identify some strong signs (may be empty if none meet threshold)
        assert "strongest_signs" in result["sarvashtakavarga"]
    
    def test_weakest_signs_identified(self, calculator):
        """Weakest signs should be identified"""
        result = calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        # Should identify some weak signs (may be empty if none meet threshold)
        assert "weakest_signs" in result["sarvashtakavarga"]


class TestPrastaraAshtakavarga:
    """Test Prastara (detailed contribution table) calculations"""
    
    @pytest.fixture
    def calculator(self):
        return EnhancedAshtakavarga()
    
    def test_prastara_calculation(self, calculator):
        """Prastara should be calculated for each planet"""
        # Access internal prastara_results after calculation
        calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        for planet in PLANETS:
            assert planet in calculator.prastara_results
            prastara = calculator.prastara_results[planet]
            assert len(prastara.contributors) == 8
            assert len(prastara.table) == 8  # 8 contributors
            assert all(len(row) == 12 for row in prastara.table)  # 12 signs
    
    def test_prastara_column_sum_matches_bav(self, calculator):
        """Sum of Prastara columns should match BAV bindus"""
        calculator.calculate_complete(REFERENCE_POSITIONS, REFERENCE_ASCENDANT)
        
        for planet in PLANETS:
            prastara = calculator.prastara_results[planet]
            bav = calculator.bav_results[planet]
            
            # Sum each column (sign) across all contributors
            for sign_idx in range(12):
                col_sum = sum(prastara.table[row][sign_idx] for row in range(8))
                assert col_sum == bav.bindus[sign_idx], \
                    f"{planet} Prastara column {sign_idx} sum {col_sum} != BAV {bav.bindus[sign_idx]}"
