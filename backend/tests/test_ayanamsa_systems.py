"""
Ayanamsa Systems Tests
=====================
Tests for multiple ayanamsa calculation systems.
"""

import pytest
from datetime import datetime, timezone
from app.core.calculations.ayanamsa_systems import AyanamsaCalculator, get_ayanamsa_for_date


class TestAyanamsaSystems:
    """Test various ayanamsa calculation systems"""
    
    @pytest.fixture
    def calc(self):
        return AyanamsaCalculator()
    
    def test_lahiri_1990(self, calc):
        """Test Lahiri ayanamsa for 1990"""
        date = datetime(1990, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        ayanamsa = calc.calculate_ayanamsa(date, 'lahiri')
        
        # Expected ~23.7° for 1990
        assert 23.5 < ayanamsa < 24.0
    
    def test_lahiri_2000(self, calc):
        """Test Lahiri ayanamsa for 2000"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        ayanamsa = calc.calculate_ayanamsa(date, 'lahiri')
        
        # Expected ~23.85° for 2000
        assert 23.7 < ayanamsa < 24.0
    
    def test_kp_differs_from_lahiri(self, calc):
        """Test that KP ayanamsa differs from Lahiri"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        lahiri = calc.calculate_ayanamsa(date, 'lahiri')
        kp = calc.calculate_ayanamsa(date, 'kp')
        
        # KP should be slightly less than Lahiri (~6 arc minutes)
        assert kp < lahiri
        assert abs(lahiri - kp) < 0.2  # Less than 12 arc minutes difference
    
    def test_all_systems_available(self, calc):
        """Test all ayanamsa systems are available"""
        expected_systems = [
            'lahiri', 'raman', 'kp', 'yukteshwar',
            'true_chitra', 'fagan_bradley', 'deluce', 'sassanian'
        ]
        
        for system in expected_systems:
            assert system in calc.systems
    
    def test_all_systems_calculate(self, calc):
        """Test all systems can calculate for a date"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        all_values = calc.get_all_systems(date)
        
        # All systems should return values
        assert len(all_values) >= 8
        
        # All values should be reasonable (19-25 degrees for year 2000)
        for system, value in all_values.items():
            assert 18 < value < 26, f"{system} returned unreasonable value: {value}"
    
    def test_yukteshwar_different(self, calc):
        """Test Yukteshwar system has different base value"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        lahiri = calc.calculate_ayanamsa(date, 'lahiri')
        yukteshwar = calc.calculate_ayanamsa(date, 'yukteshwar')
        
        # Yukteshwar should be notably different (1.5-2.5 degrees less)
        assert abs(lahiri - yukteshwar) > 1.5
        assert yukteshwar < lahiri
    
    def test_tropical_to_sidereal_conversion(self, calc):
        """Test tropical to sidereal longitude conversion"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        tropical = 30.0  # 30° tropical (0° Taurus)
        
        sidereal = calc.tropical_to_sidereal(tropical, date, 'lahiri')
        
        # Sidereal should be less than tropical by ayanamsa amount
        assert sidereal < tropical
        assert 0 < sidereal < 10  # Should be in early Aries sidereal
    
    def test_sidereal_to_tropical_conversion(self, calc):
        """Test sidereal to tropical longitude conversion"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        sidereal = 0.0  # 0° sidereal (0° Aries)
        
        tropical = calc.sidereal_to_tropical(sidereal, date, 'lahiri')
        
        # Tropical should be greater than sidereal by ayanamsa amount
        assert tropical > sidereal
        assert 23 < tropical < 25  # Should be ~23-24° for year 2000
    
    def test_round_trip_conversion(self, calc):
        """Test tropical -> sidereal -> tropical gives same value"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        original_tropical = 100.0
        
        sidereal = calc.tropical_to_sidereal(original_tropical, date, 'lahiri')
        back_to_tropical = calc.sidereal_to_tropical(sidereal, date, 'lahiri')
        
        # Should get back to original value (within floating point precision)
        assert abs(back_to_tropical - original_tropical) < 0.001
    
    def test_compare_systems(self, calc):
        """Test system comparison functionality"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        comparison = calc.compare_systems(date)
        
        # Should have all systems
        assert len(comparison) >= 8
        
        # Each entry should have required fields
        for system_name, data in comparison.items():
            assert 'value_degrees' in data
            assert 'value_dms' in data
            assert 'diff_from_lahiri' in data
            assert 'system_name' in data
    
    def test_convenience_function(self):
        """Test convenience function works"""
        date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        ayanamsa = get_ayanamsa_for_date(date, 'lahiri')
        
        assert 23 < ayanamsa < 25


class TestAyanamsaProgression:
    """Test ayanamsa values increase over time"""
    
    @pytest.fixture
    def calc(self):
        return AyanamsaCalculator()
    
    def test_ayanamsa_increases_over_time(self, calc):
        """Test ayanamsa increases as years progress"""
        date_1950 = datetime(1950, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        date_2000 = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        date_2050 = datetime(2050, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        ayanamsa_1950 = calc.calculate_ayanamsa(date_1950, 'lahiri')
        ayanamsa_2000 = calc.calculate_ayanamsa(date_2000, 'lahiri')
        ayanamsa_2050 = calc.calculate_ayanamsa(date_2050, 'lahiri')
        
        # Each should be greater than previous
        assert ayanamsa_1950 < ayanamsa_2000 < ayanamsa_2050
    
    def test_annual_increase_rate(self, calc):
        """Test ayanamsa increases by approximately 50 arc seconds per year"""
        date_2000 = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        date_2001 = datetime(2001, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
        ayanamsa_2000 = calc.calculate_ayanamsa(date_2000, 'lahiri')
        ayanamsa_2001 = calc.calculate_ayanamsa(date_2001, 'lahiri')
        
        diff = ayanamsa_2001 - ayanamsa_2000
        
        # Should be approximately 50 arc seconds = 50/3600 degrees
        expected = 50.29 / 3600
        assert abs(diff - expected) < 0.001
