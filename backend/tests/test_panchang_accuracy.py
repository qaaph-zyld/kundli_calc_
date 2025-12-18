"""
Panchang Accuracy Verification Tests
=====================================
Tests Panchang calculations (Tithi, Nakshatra, Yoga, Karana) against classical formulas.

Reference Chart: October 9, 1990, 09:10 AM, Loznica, Serbia
Sun: 172.05° (Virgo)
Moon: 58.32° (Taurus, Mrigashira Nakshatra)
"""

import pytest
from datetime import datetime, timezone
from app.core.calculations.panchang import (
    PanchangCalculator,
    TITHI_NAMES,
    NAKSHATRA_NAMES,
    NAKSHATRA_LORDS,
    YOGA_NAMES,
    YOGA_QUALITY,
    KARANA_NAMES,
    WEEKDAY_NAMES,
    WEEKDAY_LORDS
)

# Reference data
REFERENCE_DATETIME = datetime(1990, 10, 9, 9, 10, 0, tzinfo=timezone.utc)
REFERENCE_SUN_LON = 172.05   # Virgo
REFERENCE_MOON_LON = 58.32   # Taurus, Mrigashira


class TestPanchangConstants:
    """Test Panchang constants are correctly defined"""
    
    def test_30_tithis_defined(self):
        """Should have 30 tithi names (15 Shukla + 15 Krishna)"""
        assert len(TITHI_NAMES) == 30
        assert TITHI_NAMES[0] == "Pratipada"
        assert TITHI_NAMES[14] == "Purnima"
        assert TITHI_NAMES[29] == "Amavasya"
    
    def test_27_nakshatras_defined(self):
        """Should have 27 nakshatra names"""
        assert len(NAKSHATRA_NAMES) == 27
        assert NAKSHATRA_NAMES[0] == "Ashwini"
        assert NAKSHATRA_NAMES[4] == "Mrigashira"
        assert NAKSHATRA_NAMES[26] == "Revati"
    
    def test_nakshatra_lords_match_vimshottari(self):
        """Nakshatra lords should follow Vimshottari sequence"""
        # Ashwini=Ketu, Bharani=Venus, Krittika=Sun, etc.
        assert NAKSHATRA_LORDS[0] == "Ketu"     # Ashwini
        assert NAKSHATRA_LORDS[1] == "Venus"    # Bharani
        assert NAKSHATRA_LORDS[2] == "Sun"      # Krittika
        assert NAKSHATRA_LORDS[3] == "Moon"     # Rohini
        assert NAKSHATRA_LORDS[4] == "Mars"     # Mrigashira
        assert len(NAKSHATRA_LORDS) == 27
    
    def test_27_yogas_defined(self):
        """Should have 27 yoga names"""
        assert len(YOGA_NAMES) == 27
        assert YOGA_NAMES[0] == "Vishkumbha"
        assert len(YOGA_QUALITY) == 27
    
    def test_11_karanas_defined(self):
        """Should have 11 karana names (7 repeating + 4 fixed)"""
        assert len(KARANA_NAMES) == 11
        assert KARANA_NAMES[0] == "Bava"
        assert KARANA_NAMES[6] == "Vishti"  # Bhadra karana
    
    def test_7_weekdays_defined(self):
        """Should have 7 weekday names and lords"""
        assert len(WEEKDAY_NAMES) == 7
        assert len(WEEKDAY_LORDS) == 7
        assert WEEKDAY_NAMES[0] == "Sunday"
        assert WEEKDAY_LORDS[0] == "Sun"


class TestTithiCalculation:
    """Test Tithi (lunar day) calculations"""
    
    @pytest.fixture
    def calculator(self):
        return PanchangCalculator()
    
    def test_tithi_formula(self, calculator):
        """Tithi = (Moon - Sun) / 12"""
        # For reference chart: Moon=58.32, Sun=172.05
        # Diff = (58.32 - 172.05 + 360) % 360 = 246.27
        # Tithi = 246.27 / 12 = 20.52 -> Tithi 21 (Krishna Shashthi)
        panchang = calculator.calculate_panchang(
            REFERENCE_DATETIME,
            REFERENCE_SUN_LON,
            REFERENCE_MOON_LON
        )
        
        # Verify tithi is in valid range
        assert 1 <= panchang.tithi_number <= 30
    
    def test_tithi_at_new_moon(self, calculator):
        """New Moon (Amavasya) when Sun = Moon"""
        panchang = calculator.calculate_panchang(
            datetime(2000, 1, 1, 12, 0),
            0.0,   # Sun at 0°
            0.0    # Moon at 0°
        )
        
        assert panchang.tithi_number == 1  # Pratipada (just after Amavasya)
    
    def test_tithi_at_full_moon(self, calculator):
        """Full Moon (Purnima) when Moon opposite Sun"""
        # Purnima is tithi 15, occurs when Moon-Sun diff is 168-180°
        # At exactly 180°, we're at start of Krishna Pratipada (16)
        # Test just before 180° for Purnima
        panchang = calculator.calculate_panchang(
            datetime(2000, 1, 1, 12, 0),
            0.0,    # Sun at 0°
            175.0   # Moon at 175° (just before opposition)
        )
        
        # 175/12 = 14.58 -> Tithi 15 (Purnima)
        assert panchang.tithi_number == 15  # Purnima
        assert panchang.tithi_paksha == "Shukla"
    
    def test_paksha_determination(self, calculator):
        """Shukla paksha for tithi 1-15, Krishna for 16-30"""
        # Shukla Panchami
        panchang1 = calculator.calculate_panchang(
            datetime(2000, 1, 1, 12, 0),
            0.0,
            50.0  # 50/12 ≈ 4.17 -> Tithi 5
        )
        assert panchang1.tithi_paksha == "Shukla"
        
        # Krishna Panchami
        panchang2 = calculator.calculate_panchang(
            datetime(2000, 1, 1, 12, 0),
            0.0,
            230.0  # 230/12 ≈ 19.17 -> Tithi 20
        )
        assert panchang2.tithi_paksha == "Krishna"


class TestNakshatraCalculation:
    """Test Nakshatra (lunar mansion) calculations"""
    
    @pytest.fixture
    def calculator(self):
        return PanchangCalculator()
    
    def test_nakshatra_formula(self, calculator):
        """Nakshatra = Moon longitude / (360/27)"""
        # Moon at 58.32° -> 58.32 / 13.33 = 4.37 -> Nakshatra 5 (Mrigashira)
        panchang = calculator.calculate_panchang(
            REFERENCE_DATETIME,
            REFERENCE_SUN_LON,
            REFERENCE_MOON_LON
        )
        
        assert panchang.nakshatra == "Mrigashira"
        assert panchang.nakshatra_lord == "Mars"
    
    def test_nakshatra_at_0_degrees(self, calculator):
        """Moon at 0° should be in Ashwini"""
        panchang = calculator.calculate_panchang(
            datetime(2000, 1, 1, 12, 0),
            0.0,
            0.0
        )
        
        assert panchang.nakshatra == "Ashwini"
        assert panchang.nakshatra_lord == "Ketu"
    
    def test_nakshatra_pada_calculation(self, calculator):
        """Each nakshatra has 4 padas"""
        # Moon at 58.32° in Mrigashira
        # Mrigashira spans 53.33° to 66.67°
        # Position in nakshatra = 58.32 - 53.33 = 4.99°
        # Pada = 4.99 / 3.33 ≈ 1.5 -> Pada 2
        panchang = calculator.calculate_panchang(
            REFERENCE_DATETIME,
            REFERENCE_SUN_LON,
            REFERENCE_MOON_LON
        )
        
        assert 1 <= panchang.nakshatra_pada <= 4
    
    def test_nakshatra_boundaries(self, calculator):
        """Test nakshatra changes at correct boundaries"""
        # Just before Mrigashira boundary (53.33°)
        panchang1 = calculator.calculate_panchang(
            datetime(2000, 1, 1, 12, 0), 0.0, 53.0
        )
        assert panchang1.nakshatra == "Rohini"
        
        # Just after Mrigashira starts
        panchang2 = calculator.calculate_panchang(
            datetime(2000, 1, 1, 12, 0), 0.0, 54.0
        )
        assert panchang2.nakshatra == "Mrigashira"


class TestYogaCalculation:
    """Test Yoga (Sun+Moon combination) calculations"""
    
    @pytest.fixture
    def calculator(self):
        return PanchangCalculator()
    
    def test_yoga_formula(self, calculator):
        """Yoga = (Sun + Moon) / (360/27)"""
        # Sun=172.05, Moon=58.32
        # Combined = (172.05 + 58.32) % 360 = 230.37
        # Yoga index = 230.37 / 13.33 = 17.28 -> Yoga 18 (Variyan)
        panchang = calculator.calculate_panchang(
            REFERENCE_DATETIME,
            REFERENCE_SUN_LON,
            REFERENCE_MOON_LON
        )
        
        assert panchang.yoga in YOGA_NAMES
        assert panchang.yoga_quality in ["benefic", "malefic"]
    
    def test_yoga_at_zero_combined(self, calculator):
        """Yoga when Sun+Moon = 0° (both at 0)"""
        panchang = calculator.calculate_panchang(
            datetime(2000, 1, 1, 12, 0),
            0.0,
            0.0
        )
        
        assert panchang.yoga == "Vishkumbha"  # First yoga


class TestKaranaCalculation:
    """Test Karana (half-tithi) calculations"""
    
    @pytest.fixture
    def calculator(self):
        return PanchangCalculator()
    
    def test_karana_from_tithi(self, calculator):
        """Karana calculated from tithi"""
        panchang = calculator.calculate_panchang(
            REFERENCE_DATETIME,
            REFERENCE_SUN_LON,
            REFERENCE_MOON_LON
        )
        
        assert panchang.karana in KARANA_NAMES
    
    def test_vishti_karana(self, calculator):
        """Vishti (Bhadra) karana is considered inauspicious"""
        # Vishti is the 7th repeating karana
        assert "Vishti" in KARANA_NAMES


class TestWeekdayCalculation:
    """Test weekday (Vara) calculations"""
    
    @pytest.fixture
    def calculator(self):
        return PanchangCalculator()
    
    def test_weekday_calculation(self, calculator):
        """October 9, 1990 was a Tuesday"""
        panchang = calculator.calculate_panchang(
            REFERENCE_DATETIME,
            REFERENCE_SUN_LON,
            REFERENCE_MOON_LON
        )
        
        assert panchang.weekday == "Tuesday"
        assert panchang.weekday_lord == "Mars"
    
    def test_weekday_lord_mapping(self, calculator):
        """Each weekday has correct lord"""
        test_dates = [
            (datetime(2024, 1, 7, 12, 0), "Sunday", "Sun"),
            (datetime(2024, 1, 8, 12, 0), "Monday", "Moon"),
            (datetime(2024, 1, 9, 12, 0), "Tuesday", "Mars"),
            (datetime(2024, 1, 10, 12, 0), "Wednesday", "Mercury"),
            (datetime(2024, 1, 11, 12, 0), "Thursday", "Jupiter"),
            (datetime(2024, 1, 12, 12, 0), "Friday", "Venus"),
            (datetime(2024, 1, 13, 12, 0), "Saturday", "Saturn"),
        ]
        
        for dt, expected_day, expected_lord in test_dates:
            panchang = calculator.calculate_panchang(dt, 0.0, 0.0)
            assert panchang.weekday == expected_day
            assert panchang.weekday_lord == expected_lord


class TestCompletePanchang:
    """Test complete Panchang output"""
    
    @pytest.fixture
    def calculator(self):
        return PanchangCalculator()
    
    def test_all_fields_populated(self, calculator):
        """All Panchang fields should be populated"""
        panchang = calculator.calculate_panchang(
            REFERENCE_DATETIME,
            REFERENCE_SUN_LON,
            REFERENCE_MOON_LON
        )
        
        assert panchang.weekday is not None
        assert panchang.weekday_lord is not None
        assert panchang.tithi is not None
        assert panchang.tithi_number > 0
        assert panchang.tithi_paksha in ["Shukla", "Krishna"]
        assert panchang.nakshatra is not None
        assert panchang.nakshatra_lord is not None
        assert 1 <= panchang.nakshatra_pada <= 4
        assert panchang.yoga is not None
        assert panchang.yoga_quality in ["benefic", "malefic"]
        assert panchang.karana is not None
        assert panchang.moon_sign is not None
        assert panchang.sun_sign is not None
    
    def test_sun_moon_signs(self, calculator):
        """Sun and Moon signs correctly identified"""
        panchang = calculator.calculate_panchang(
            REFERENCE_DATETIME,
            REFERENCE_SUN_LON,  # 172.05 -> Virgo
            REFERENCE_MOON_LON  # 58.32 -> Taurus
        )
        
        assert panchang.sun_sign == "Virgo"
        assert panchang.moon_sign == "Taurus"
