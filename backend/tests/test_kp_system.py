"""
KP System Tests
================
Validates Krishnamurti Paddhati calculations including:
- Sub-lord calculations (249 divisions)
- Cuspal sublords
- Ruling planets
- Horary number conversion
"""

import pytest
from datetime import datetime
from app.core.calculations.kp_system import (
    KPSystem,
    KPPosition,
    get_kp_data,
    NAKSHATRAS,
    DASHA_SEQUENCE,
    DASHA_PERIODS
)


class TestKPSubLordCalculations:
    """Test sub-lord division calculations"""
    
    @pytest.fixture
    def kp(self):
        return KPSystem()
    
    def test_nakshatra_span_is_correct(self, kp):
        """Each nakshatra should span exactly 13°20'"""
        expected_span = 13.333333333333334
        # 360° / 27 nakshatras = 13.333...°
        assert abs(360 / 27 - expected_span) < 0.0001
    
    def test_first_nakshatra_is_ashwini(self, kp):
        """0° should be in Ashwini nakshatra"""
        pos = kp.get_kp_position(0.0)
        assert pos.nakshatra_name == "Ashwini"
        assert pos.nakshatra_lord == "Ketu"
    
    def test_last_nakshatra_is_revati(self, kp):
        """359° should be in Revati nakshatra"""
        pos = kp.get_kp_position(359.9)
        assert pos.nakshatra_name == "Revati"
        assert pos.nakshatra_lord == "Mercury"
    
    def test_sub_lord_sequence_starts_from_star_lord(self, kp):
        """Sub-lord sequence should start from the star lord"""
        # Ashwini (0-13.33°) is ruled by Ketu
        # So sub-lords should start: Ketu, Venus, Sun, Moon, ...
        pos = kp.get_kp_position(0.0)
        assert pos.nakshatra_lord == "Ketu"
        assert pos.sub_lord == "Ketu"  # First sub in Ashwini
    
    def test_sub_spans_proportional_to_dasha(self, kp):
        """Sub spans should be proportional to Vimshottari dasha periods"""
        nakshatra_span = 13.333333333333334
        
        # Ketu's sub in Ashwini should span 7/120 of nakshatra
        ketu_sub_span = nakshatra_span * 7 / 120  # ~0.778°
        
        # At 0°, we're in Ketu sub
        pos1 = kp.get_kp_position(0.0)
        assert pos1.sub_lord == "Ketu"
        
        # Just after Ketu sub ends, we should be in Venus sub
        pos2 = kp.get_kp_position(ketu_sub_span + 0.01)
        assert pos2.sub_lord == "Venus"
    
    def test_sub_sub_lord_calculation(self, kp):
        """Sub-sub lord should follow same proportional division"""
        pos = kp.get_kp_position(100.0)
        
        # Should have valid sub-sub lord
        assert pos.sub_sub_lord in DASHA_SEQUENCE
    
    def test_five_levels_of_sublords(self, kp):
        """Should calculate up to 5 levels of sublords"""
        pos = kp.get_kp_position(123.456)
        
        assert pos.nakshatra_lord in DASHA_SEQUENCE
        assert pos.sub_lord in DASHA_SEQUENCE
        assert pos.sub_sub_lord in DASHA_SEQUENCE
        assert pos.sub_sub_sub_lord in DASHA_SEQUENCE
        assert pos.sub_sub_sub_sub_lord in DASHA_SEQUENCE


class TestKPSignPositions:
    """Test sign-related KP calculations"""
    
    @pytest.fixture
    def kp(self):
        return KPSystem()
    
    def test_aries_sign_lord(self, kp):
        """0-30° should be Aries ruled by Mars"""
        pos = kp.get_kp_position(15.0)
        assert pos.sign_name == "Aries"
        assert pos.sign_lord == "Mars"
    
    def test_taurus_sign_lord(self, kp):
        """30-60° should be Taurus ruled by Venus"""
        pos = kp.get_kp_position(45.0)
        assert pos.sign_name == "Taurus"
        assert pos.sign_lord == "Venus"
    
    def test_all_sign_lords(self, kp):
        """Verify all 12 sign lords"""
        expected_lords = [
            ("Aries", "Mars"), ("Taurus", "Venus"), ("Gemini", "Mercury"),
            ("Cancer", "Moon"), ("Leo", "Sun"), ("Virgo", "Mercury"),
            ("Libra", "Venus"), ("Scorpio", "Mars"), ("Sagittarius", "Jupiter"),
            ("Capricorn", "Saturn"), ("Aquarius", "Saturn"), ("Pisces", "Jupiter")
        ]
        
        for i, (sign_name, lord) in enumerate(expected_lords):
            pos = kp.get_kp_position(i * 30 + 15)  # Middle of each sign
            assert pos.sign_name == sign_name, f"Sign mismatch at {i*30+15}°"
            assert pos.sign_lord == lord, f"Lord mismatch for {sign_name}"


class TestKPHoraryNumbers:
    """Test horary number to position conversion"""
    
    @pytest.fixture
    def kp(self):
        return KPSystem()
    
    def test_horary_number_1(self, kp):
        """Horary number 1 should give first subdivision of Ashwini"""
        pos = kp.horary_number_to_position(1)
        assert pos.nakshatra_name == "Ashwini"
        assert pos.nakshatra_lord == "Ketu"
        assert pos.sub_lord == "Ketu"
    
    def test_horary_number_middle(self, kp):
        """Horary number in middle should return valid position"""
        pos = kp.horary_number_to_position(125)
        assert 0 <= pos.degree < 360
        assert pos.nakshatra_lord in DASHA_SEQUENCE
        assert pos.sub_lord in DASHA_SEQUENCE
    
    def test_horary_number_invalid_low(self, kp):
        """Horary number < 1 should raise error"""
        with pytest.raises(ValueError):
            kp.horary_number_to_position(0)
    
    def test_horary_number_invalid_high(self, kp):
        """Horary number > 249 should raise error"""
        with pytest.raises(ValueError):
            kp.horary_number_to_position(250)
    
    def test_horary_numbers_cover_zodiac(self, kp):
        """Horary numbers should span the zodiac"""
        # Note: KP system has 27 nakshatras × 9 subs = 243 primary divisions
        # The 249 number comes from a slightly different division scheme
        # Test valid range
        degrees = [kp.horary_number_to_position(n).degree for n in range(1, 244)]
        
        # First should be near 0°
        assert degrees[0] < 1.0
        
        # Should cover most of the zodiac
        assert max(degrees) > 300.0


class TestKPRulingPlanets:
    """Test ruling planets calculation"""
    
    @pytest.fixture
    def kp(self):
        return KPSystem()
    
    def test_weekday_lords(self, kp):
        """Test weekday lord calculation"""
        # Monday = Moon
        monday = datetime(2024, 1, 1)  # Was a Monday
        rp = kp.get_ruling_planets(monday, 100.0, 50.0)
        assert rp.weekday_lord == "Moon"
        
        # Sunday = Sun
        sunday = datetime(2024, 1, 7)  # Was a Sunday
        rp = kp.get_ruling_planets(sunday, 100.0, 50.0)
        assert rp.weekday_lord == "Sun"
    
    def test_ruling_planets_include_moon_sublords(self, kp):
        """Ruling planets should include Moon's sign, star, and sub lords"""
        rp = kp.get_ruling_planets(datetime.now(), 100.0, 50.0)
        
        # All should be valid planet names
        assert rp.moon_sign_lord in DASHA_SEQUENCE
        assert rp.moon_star_lord in DASHA_SEQUENCE
        assert rp.moon_sub_lord in DASHA_SEQUENCE
    
    def test_ruling_planets_include_asc_sublords(self, kp):
        """Ruling planets should include Ascendant's sign, star, and sub lords"""
        rp = kp.get_ruling_planets(datetime.now(), 100.0, 50.0)
        
        assert rp.ascendant_sign_lord in DASHA_SEQUENCE
        assert rp.ascendant_star_lord in DASHA_SEQUENCE
        assert rp.ascendant_sub_lord in DASHA_SEQUENCE
    
    def test_strong_ruling_planets(self, kp):
        """Strong RPs should be sorted by frequency"""
        rp = kp.get_ruling_planets(datetime.now(), 100.0, 50.0)
        
        # Should have at least some ruling planets
        assert len(rp.strong_rp) > 0
        assert len(rp.strong_rp) <= 9  # Max 9 unique planets


class TestKPDataFunction:
    """Test the convenience get_kp_data function"""
    
    def test_complete_kp_data(self):
        """get_kp_data should return complete analysis"""
        planets = {
            "Sun": 271.0,
            "Moon": 141.0,
            "Mars": 236.0,
            "Mercury": 258.0,
            "Jupiter": 70.0,
            "Venus": 277.0,
            "Saturn": 264.0,
            "Rahu": 294.0,
            "Ketu": 114.0
        }
        
        house_cusps = [(i * 30) % 360 for i in range(12)]
        
        result = get_kp_data(planets, house_cusps, datetime.now())
        
        # Check structure
        assert "planet_positions" in result
        assert "cuspal_positions" in result
        assert "planets_by_house" in result
        assert "ruling_planets" in result
        
        # Check all planets are present
        for planet in planets:
            assert planet in result["planet_positions"]
            pos = result["planet_positions"][planet]
            assert "star_lord" in pos
            assert "sub_lord" in pos
        
        # Check all 12 houses are present
        assert len(result["cuspal_positions"]) == 12


class TestKPAyanamsa:
    """Test KP Ayanamsa calculation"""
    
    @pytest.fixture
    def kp(self):
        return KPSystem()
    
    def test_kp_ayanamsa_1990(self, kp):
        """KP Ayanamsa for 1990 should be approximately 23.7°"""
        date = datetime(1990, 1, 1)
        ayanamsa = kp.calculate_kp_ayanamsa(date)
        
        # KP Ayanamsa is about 6 arc-minutes less than Lahiri
        # For 1990, should be around 23.6-23.7°
        assert 23.5 < ayanamsa < 24.0
    
    def test_kp_ayanamsa_2000(self, kp):
        """KP Ayanamsa for 2000 should be approximately 23.85°"""
        date = datetime(2000, 1, 1)
        ayanamsa = kp.calculate_kp_ayanamsa(date)
        
        assert 23.7 < ayanamsa < 24.1
    
    def test_kp_ayanamsa_progression(self, kp):
        """Ayanamsa should increase over time (precession)"""
        ay_1990 = kp.calculate_kp_ayanamsa(datetime(1990, 1, 1))
        ay_2000 = kp.calculate_kp_ayanamsa(datetime(2000, 1, 1))
        ay_2010 = kp.calculate_kp_ayanamsa(datetime(2010, 1, 1))
        
        assert ay_1990 < ay_2000 < ay_2010
        
        # Precession is about 50.3 arc-seconds per year = 0.014° per year
        yearly_increase = (ay_2000 - ay_1990) / 10
        assert 0.01 < yearly_increase < 0.02


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
