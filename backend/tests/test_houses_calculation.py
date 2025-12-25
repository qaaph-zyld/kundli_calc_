"""
House Calculation Tests
======================
Tests for house system calculations including Whole Sign and Placidus.
"""

import pytest
from datetime import datetime, timezone
from app.core.calculations.houses import HouseCalculator


class TestWholeSignHouses:
    """Test Whole Sign house system"""
    
    @pytest.fixture
    def calc(self):
        return HouseCalculator()
    
    def test_whole_sign_basic(self, calc):
        """Test basic Whole Sign house calculation"""
        # Ascendant at 15° Aries (15°)
        houses = calc.calculate_whole_sign_houses(15.0)
        
        # 1st house should start at 0° Aries (0°)
        assert houses[1]['sign'] == 0  # Aries
        assert houses[1]['start_degree'] == 0
        
        # 2nd house should start at 0° Taurus (30°)
        assert houses[2]['sign'] == 1  # Taurus
        assert houses[2]['start_degree'] == 30
    
    def test_whole_sign_all_houses(self, calc):
        """Test all 12 houses are calculated"""
        houses = calc.calculate_whole_sign_houses(100.0)
        
        assert len(houses) == 12
        for i in range(1, 13):
            assert i in houses
    
    def test_whole_sign_house_sequence(self, calc):
        """Test houses follow proper sequence"""
        houses = calc.calculate_whole_sign_houses(45.0)  # Mid Taurus
        
        # Should start from Taurus (sign 1)
        for i in range(1, 13):
            expected_sign = (1 + i - 1) % 12
            assert houses[i]['sign'] == expected_sign
    
    def test_whole_sign_boundary_case(self, calc):
        """Test ascendant exactly at sign boundary"""
        houses = calc.calculate_whole_sign_houses(0.0)  # 0° Aries
        
        assert houses[1]['sign'] == 0
        assert houses[1]['start_degree'] == 0
    
    def test_whole_sign_end_of_zodiac(self, calc):
        """Test ascendant near end of zodiac"""
        houses = calc.calculate_whole_sign_houses(359.0)  # 29° Pisces
        
        # Should start from Pisces (sign 11)
        assert houses[1]['sign'] == 11
        assert houses[2]['sign'] == 0  # Wraps to Aries


class TestHouseOccupancy:
    """Test planet house occupancy determination"""
    
    @pytest.fixture
    def calc(self):
        return HouseCalculator()
    
    def test_planet_in_first_house(self, calc):
        """Test planet placement in 1st house"""
        houses = calc.calculate_whole_sign_houses(15.0)  # Asc at 15° Aries
        
        # Planet at 20° Aries should be in 1st house
        house_num = calc.get_house_for_planet(20.0, houses)
        assert house_num == 1
    
    def test_planet_in_seventh_house(self, calc):
        """Test planet placement in 7th house (opposite ascendant)"""
        houses = calc.calculate_whole_sign_houses(15.0)  # Asc at 15° Aries
        
        # Planet at 195° (15° Libra) should be in 7th house
        house_num = calc.get_house_for_planet(195.0, houses)
        assert house_num == 7
    
    def test_planet_at_house_boundary(self, calc):
        """Test planet exactly at house boundary"""
        houses = calc.calculate_whole_sign_houses(0.0)
        
        # Planet at 30° (boundary between Aries/Taurus)
        house_num = calc.get_house_for_planet(30.0, houses)
        assert house_num in [1, 2]  # Could be either depending on implementation


class TestPlacidusHouses:
    """Test Placidus house system"""
    
    @pytest.fixture
    def calc(self):
        return HouseCalculator()
    
    def test_placidus_basic(self, calc):
        """Test basic Placidus calculation"""
        # Test data: Standard location and time
        jd = 2448500.5  # Arbitrary Julian Day
        lat = 28.6139  # Delhi
        lon = 77.209
        
        houses = calc.calculate_placidus_houses(jd, lat, lon)
        
        # Should return 12 houses
        assert len(houses) >= 12
    
    def test_placidus_northern_hemisphere(self, calc):
        """Test Placidus for northern hemisphere"""
        jd = 2448500.5
        lat = 51.5074  # London
        lon = -0.1278
        
        houses = calc.calculate_placidus_houses(jd, lat, lon)
        assert houses is not None
    
    def test_placidus_southern_hemisphere(self, calc):
        """Test Placidus for southern hemisphere"""
        jd = 2448500.5
        lat = -33.8688  # Sydney
        lon = 151.2093
        
        houses = calc.calculate_placidus_houses(jd, lat, lon)
        assert houses is not None


class TestHouseAspects:
    """Test house-based aspects and relationships"""
    
    @pytest.fixture
    def calc(self):
        return HouseCalculator()
    
    def test_kendra_houses(self, calc):
        """Test kendra (angular) house identification"""
        kendras = calc.get_kendra_houses()
        assert kendras == [1, 4, 7, 10]
    
    def test_trikona_houses(self, calc):
        """Test trikona (trinal) house identification"""
        trikonas = calc.get_trikona_houses()
        assert trikonas == [1, 5, 9]
    
    def test_dusthana_houses(self, calc):
        """Test dusthana (difficult) house identification"""
        dusthanas = calc.get_dusthana_houses()
        assert dusthanas == [6, 8, 12]
    
    def test_upachaya_houses(self, calc):
        """Test upachaya (growing) house identification"""
        upachayas = calc.get_upachaya_houses()
        assert upachayas == [3, 6, 10, 11]


class TestHouseStrength:
    """Test house strength calculations"""
    
    @pytest.fixture
    def calc(self):
        return HouseCalculator()
    
    def test_house_strength_kendra(self, calc):
        """Test kendra houses have high strength"""
        strength_1 = calc.get_house_strength(1)
        strength_5 = calc.get_house_strength(5)
        
        # Kendra (1st) should be stronger than non-kendra (5th)
        assert strength_1 > strength_5
    
    def test_house_strength_all_positive(self, calc):
        """Test all houses have positive strength"""
        for house_num in range(1, 13):
            strength = calc.get_house_strength(house_num)
            assert strength > 0
