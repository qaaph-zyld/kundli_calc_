"""
Whole Sign House Accuracy Validation
=====================================

Validates Whole Sign house calculations against expected behavior.

Whole Sign System Rules:
- House 1 starts at 0° of ascendant sign
- Each house = one complete sign (30°)
- House cusps are at sign boundaries (0° of each sign)
- No quadrant division - equal houses

Reference: Traditional Vedic astrology texts
"""

import pytest
from datetime import datetime
from app.core.calculations.houses import HouseCalculator


class TestWholeSignHouses:
    """Validate Whole Sign house calculations"""
    
    def test_house_cusps_at_sign_boundaries(self):
        """Test that Whole Sign house cusps are at sign boundaries"""
        
        # Test chart: Ascendant in Leo
        # Expected: House 1 = 120° (Leo starts), House 2 = 150° (Virgo starts), etc.
        
        calculator = HouseCalculator()
        
        # Birth data that produces Leo ascendant
        date = datetime(1990, 5, 15, 10, 30, 0)
        latitude = 28.6139  # New Delhi
        longitude = 77.2090
        
        houses = calculator.calculate_houses(date, latitude, longitude, house_system='W')
        
        # Verify house cusps are multiples of 30 (sign boundaries)
        for i, cusp in enumerate(houses.get('cusps', [])[:12], 1):
            remainder = cusp % 30
            assert remainder < 0.01 or remainder > 29.99, \
                f"House {i} cusp {cusp}° is not at sign boundary (remainder: {remainder}°)"
    
    def test_ascendant_determines_first_house(self):
        """Test that ascendant sign determines 1st house"""
        
        calculator = HouseCalculator()
        
        date = datetime(2000, 1, 1, 12, 0, 0)
        latitude = 28.6139
        longitude = 77.2090
        
        result = calculator.calculate_houses(date, latitude, longitude, house_system='W')
        
        ascendant = result['ascendant']
        first_house_cusp = result['cusps'][0]
        
        # In Whole Sign, 1st house cusp = start of ascendant sign
        asc_sign_start = (int(ascendant / 30)) * 30
        
        assert abs(first_house_cusp - asc_sign_start) < 0.01, \
            f"1st house cusp {first_house_cusp}° does not match ascendant sign start {asc_sign_start}°"
    
    def test_sequential_house_signs(self):
        """Test that houses follow sequential signs"""
        
        calculator = HouseCalculator()
        
        date = datetime(1985, 3, 20, 14, 30, 0)
        latitude = 28.6139
        longitude = 77.2090
        
        result = calculator.calculate_houses(date, latitude, longitude, house_system='W')
        cusps = result['cusps'][:12]
        
        # Each house should be exactly 30° after the previous
        for i in range(11):
            expected_diff = 30.0
            actual_diff = (cusps[i+1] - cusps[i]) % 360
            
            assert abs(actual_diff - expected_diff) < 0.01, \
                f"Houses {i+1} and {i+2} are not 30° apart (diff: {actual_diff}°)"
    
    def test_complete_zodiac_coverage(self):
        """Test that 12 houses cover complete zodiac"""
        
        calculator = HouseCalculator()
        
        date = datetime(1995, 7, 10, 8, 0, 0)
        latitude = 28.6139
        longitude = 77.2090
        
        result = calculator.calculate_houses(date, latitude, longitude, house_system='W')
        cusps = result['cusps'][:12]
        
        # 12 houses should span 360° total
        first_cusp = cusps[0]
        last_cusp = cusps[11]
        
        # Distance from last house to first house (wrapping around)
        total_span = (first_cusp - last_cusp) % 360
        
        # Should be 30° (one sign) since 12 houses × 30° = 360°
        assert abs(total_span - 30.0) < 0.01, \
            f"Houses don't span complete zodiac properly (gap: {total_span}°)"
    
    def test_house_system_independence(self):
        """Test that Whole Sign houses ignore time changes"""
        
        calculator = HouseCalculator()
        
        # Same date, different times
        date1 = datetime(2010, 12, 25, 6, 0, 0)
        date2 = datetime(2010, 12, 25, 18, 0, 0)  # 12 hours later
        
        latitude = 28.6139
        longitude = 77.2090
        
        result1 = calculator.calculate_houses(date1, latitude, longitude, house_system='W')
        result2 = calculator.calculate_houses(date2, latitude, longitude, house_system='W')
        
        # Whole Sign houses should be identical if ascendant is in same sign
        # (This test may fail if ascendant changes sign during the day - that's expected)
        
        asc1_sign = int(result1['ascendant'] / 30)
        asc2_sign = int(result2['ascendant'] / 30)
        
        if asc1_sign == asc2_sign:
            for i in range(12):
                assert abs(result1['cusps'][i] - result2['cusps'][i]) < 0.01, \
                    f"House {i+1} cusps differ despite same ascendant sign"
