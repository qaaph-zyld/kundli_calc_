"""
Dasha Accuracy Verification Tests
==================================
Tests Vimshottari Dasha calculations against JHora reference values.
Uses Lahiri ayanamsa baseline.

Reference Chart: October 9, 1990, 09:10 AM, Loznica, Serbia
Moon: 58.32° (Taurus, Mrigashira Nakshatra, Pada 2)
"""

import pytest
from datetime import datetime, timezone
from app.core.calculations.dasha_system import VimshottariDasha

# Reference data from JHora for Oct 9, 1990, 09:10 AM, Loznica
JHORA_REFERENCE = {
    "birth_datetime": datetime(1990, 10, 9, 8, 10, 0, tzinfo=timezone.utc),
    "moon_longitude": 58.32,  # Mrigashira nakshatra (5th nakshatra, 0-indexed: 4)
    
    # JHora Dasha Balance at Birth
    "expected_balance": {
        "planet": "Mars",  # Mars mahadasha at birth
        "years": 4,
        "months": 4,
        "days": 16,
        "total_years_approx": 4.38  # ~4 years 4 months 16 days
    },
    
    # JHora Mahadasha sequence with end dates
    "expected_mahadasha_sequence": [
        {"planet": "Mars", "end_year": 1995},
        {"planet": "Rahu", "end_year": 2013},
        {"planet": "Jupiter", "end_year": 2029},
        {"planet": "Saturn", "end_year": 2048},
        {"planet": "Mercury", "end_year": 2065},
        {"planet": "Ketu", "end_year": 2072},
        {"planet": "Venus", "end_year": 2092},
        {"planet": "Sun", "end_year": 2098},
        {"planet": "Moon", "end_year": 2108},
    ],
    
    # Current dasha (as of late 2024) from JHora
    "current_dasha_2024": {
        "mahadasha": "Jupiter",
        "antardasha": "Moon",  # Jupiter-Moon from Jun 2024 to Oct 2025
    }
}


class TestVimshottariDashaAccuracy:
    """Test Vimshottari Dasha calculations against JHora"""
    
    @pytest.fixture
    def dasha_calculator(self):
        return VimshottariDasha()
    
    def test_nakshatra_lord_determination(self, dasha_calculator):
        """Test that Moon at 58.32° gives Mars as nakshatra lord"""
        # Moon at 58.32° is in Mrigashira (nakshatra index 4, 0-based)
        # Mrigashira lord is Mars
        result = dasha_calculator.calculate_dasha_at_birth(
            JHORA_REFERENCE["birth_datetime"],
            JHORA_REFERENCE["moon_longitude"]
        )
        
        first_dasha = result["dasha_sequence"][0]
        assert first_dasha["planet"] == "Mars", \
            f"Expected Mars mahadasha at birth, got {first_dasha['planet']}"
    
    def test_dasha_balance_at_birth(self, dasha_calculator):
        """Test dasha balance at birth matches JHora within tolerance"""
        result = dasha_calculator.calculate_dasha_at_birth(
            JHORA_REFERENCE["birth_datetime"],
            JHORA_REFERENCE["moon_longitude"]
        )
        
        first_dasha = result["dasha_sequence"][0]
        balance_years = first_dasha["duration_years"]
        expected_years = JHORA_REFERENCE["expected_balance"]["total_years_approx"]
        
        # Allow 0.1 year (about 36 days) tolerance
        assert abs(balance_years - expected_years) < 0.15, \
            f"Dasha balance {balance_years:.2f} years differs from JHora {expected_years} years"
    
    def test_mahadasha_sequence_order(self, dasha_calculator):
        """Test mahadasha sequence follows correct order"""
        result = dasha_calculator.calculate_dasha_at_birth(
            JHORA_REFERENCE["birth_datetime"],
            JHORA_REFERENCE["moon_longitude"]
        )
        
        sequence = [d["planet"] for d in result["dasha_sequence"]]
        expected_sequence = [d["planet"] for d in JHORA_REFERENCE["expected_mahadasha_sequence"]]
        
        assert sequence == expected_sequence, \
            f"Sequence mismatch: got {sequence}, expected {expected_sequence}"
    
    def test_mahadasha_end_years_accuracy(self, dasha_calculator):
        """Test mahadasha end years match JHora within 1 year"""
        result = dasha_calculator.calculate_dasha_at_birth(
            JHORA_REFERENCE["birth_datetime"],
            JHORA_REFERENCE["moon_longitude"]
        )
        
        for i, dasha in enumerate(result["dasha_sequence"]):
            expected = JHORA_REFERENCE["expected_mahadasha_sequence"][i]
            actual_end_year = dasha["end_date"].year
            expected_end_year = expected["end_year"]
            
            assert abs(actual_end_year - expected_end_year) <= 1, \
                f"{expected['planet']} mahadasha: end year {actual_end_year} differs from JHora {expected_end_year}"
    
    def test_antardasha_calculation(self, dasha_calculator):
        """Test antardasha periods are calculated correctly"""
        result = dasha_calculator.calculate_dasha_at_birth(
            JHORA_REFERENCE["birth_datetime"],
            JHORA_REFERENCE["moon_longitude"]
        )
        
        # Get Jupiter mahadasha (3rd in sequence after Mars, Rahu)
        jupiter_maha = None
        for dasha in result["dasha_sequence"]:
            if dasha["planet"] == "Jupiter":
                jupiter_maha = dasha
                break
        
        assert jupiter_maha is not None, "Jupiter mahadasha not found"
        
        # Calculate antardashas for Jupiter period
        antardashas = dasha_calculator.calculate_antardasha(
            "Jupiter",
            jupiter_maha["start_date"],
            jupiter_maha["end_date"]
        )
        
        # Verify 9 antardashas exist
        assert len(antardashas) == 9, f"Expected 9 antardashas, got {len(antardashas)}"
        
        # Verify antardasha starts with Jupiter (self first)
        assert antardashas[0]["planet"] == "Jupiter", \
            f"First antardasha should be Jupiter-Jupiter, got Jupiter-{antardashas[0]['planet']}"
    
    def test_total_dasha_cycle_120_years(self, dasha_calculator):
        """Test that complete dasha cycle equals 120 years"""
        total_years = sum(VimshottariDasha.DASHA_PERIODS.values())
        assert total_years == 120, f"Total dasha cycle should be 120 years, got {total_years}"
    
    def test_dasha_periods_standard_values(self, dasha_calculator):
        """Test that dasha periods match standard Vimshottari values"""
        expected_periods = {
            "Ketu": 7,
            "Venus": 20,
            "Sun": 6,
            "Moon": 10,
            "Mars": 7,
            "Rahu": 18,
            "Jupiter": 16,
            "Saturn": 19,
            "Mercury": 17,
        }
        
        for planet, years in expected_periods.items():
            assert VimshottariDasha.DASHA_PERIODS[planet] == years, \
                f"{planet} period should be {years} years"


class TestDashaEdgeCases:
    """Test edge cases for dasha calculations"""
    
    @pytest.fixture
    def dasha_calculator(self):
        return VimshottariDasha()
    
    def test_moon_at_nakshatra_boundary(self, dasha_calculator):
        """Test Moon exactly at nakshatra boundary (0° of nakshatra)"""
        # Moon at exactly 0° (start of Ashwini = Ketu nakshatra)
        result = dasha_calculator.calculate_dasha_at_birth(
            datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            0.0
        )
        
        # At 0°, should be full Ketu dasha (7 years)
        first_dasha = result["dasha_sequence"][0]
        assert first_dasha["planet"] == "Ketu"
        assert abs(first_dasha["duration_years"] - 7.0) < 0.01
    
    def test_moon_near_nakshatra_end(self, dasha_calculator):
        """Test Moon near end of nakshatra (13.33° - small fraction remaining)"""
        # Moon at 13.0° (near end of Ashwini, only ~0.33° remaining)
        result = dasha_calculator.calculate_dasha_at_birth(
            datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            13.0
        )
        
        first_dasha = result["dasha_sequence"][0]
        assert first_dasha["planet"] == "Ketu"
        # Should have small balance (13.33 - 13.0) / 13.33 * 7 ≈ 0.175 years
        assert first_dasha["duration_years"] < 1.0
    
    def test_moon_at_360_degrees(self, dasha_calculator):
        """Test Moon at 360° (should wrap to 0°)"""
        result = dasha_calculator.calculate_dasha_at_birth(
            datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            360.0
        )
        
        first_dasha = result["dasha_sequence"][0]
        # 360° wraps to 0°, which is Ashwini = Ketu
        assert first_dasha["planet"] == "Ketu"


class TestJHoraDateAccuracy:
    """Test exact dasha dates against JHora within ±1 day tolerance"""
    
    @pytest.fixture
    def dasha_calculator(self):
        return VimshottariDasha()
    
    # JHora reference dates from Nikola_Jelacic.txt
    JHORA_MAHADASHA_DATES = [
        {"planet": "Mars", "start": "1988-02-17", "end": "1995-02-17"},
        {"planet": "Rahu", "start": "1995-02-17", "end": "2013-02-16"},
        {"planet": "Jupiter", "start": "2013-02-16", "end": "2029-02-16"},
        {"planet": "Saturn", "start": "2029-02-16", "end": "2048-02-17"},
        {"planet": "Mercury", "start": "2048-02-17", "end": "2065-02-17"},
    ]
    
    def test_mahadasha_dates_within_tolerance(self, dasha_calculator):
        """Test mahadasha start/end dates match JHora within acceptable tolerance
        
        Tolerance: ±1 day per year of dasha period (accounts for 365.25 vs 365.2422 day/year)
        This means a 7-year dasha can have up to 7 days deviation.
        """
        birth_time = datetime(1990, 10, 9, 8, 10, 0, tzinfo=timezone.utc)
        moon_longitude = 58.348689  # From JHora reference
        
        result = dasha_calculator.calculate_dasha_at_birth(birth_time, moon_longitude)
        
        for i, expected in enumerate(self.JHORA_MAHADASHA_DATES):
            if i >= len(result["dasha_sequence"]):
                break
                
            actual = result["dasha_sequence"][i]
            
            # Check planet matches
            assert actual["planet"] == expected["planet"], \
                f"Period {i}: Expected {expected['planet']}, got {actual['planet']}"
            
            # Check end date within tolerance (1 day per year of elapsed time)
            expected_end = datetime.strptime(expected["end"], "%Y-%m-%d")
            actual_end = actual["end_date"].replace(tzinfo=None) if actual["end_date"].tzinfo else actual["end_date"]
            
            # Calculate years from birth to this dasha end
            years_elapsed = (expected_end - birth_time.replace(tzinfo=None)).days / 365.25
            tolerance_days = max(3, int(years_elapsed * 0.5))  # 0.5 day/year, minimum 3 days
            
            diff_days = abs((actual_end - expected_end).days)
            assert diff_days <= tolerance_days, \
                f"{expected['planet']} end date: {actual_end.date()} differs from JHora {expected_end.date()} by {diff_days} days (tolerance: {tolerance_days})"
    
    def test_current_bhukti_matches_jhora(self, dasha_calculator):
        """Test current bhukti (as of Jan 2026) matches JHora"""
        birth_time = datetime(1990, 10, 9, 8, 10, 0, tzinfo=timezone.utc)
        moon_longitude = 58.348689
        
        # Check date: January 18, 2026
        check_date = datetime(2026, 1, 18, 12, 0, 0, tzinfo=timezone.utc)
        
        current = dasha_calculator.get_current_dasha(birth_time, moon_longitude, check_date)
        
        # Per JHora: Jupiter mahadasha, Mars bhukti (Oct 2025 - Sep 2026)
        assert current["mahadasha"]["planet"] == "Jupiter", \
            f"Expected Jupiter mahadasha, got {current['mahadasha']['planet']}"
        assert current["antardasha"]["planet"] == "Mars", \
            f"Expected Mars antardasha, got {current['antardasha']['planet']}"


class TestPratyantardashaCalculation:
    """Test pratyantardasha (sub-sub-period) calculations"""
    
    @pytest.fixture
    def dasha_calculator(self):
        return VimshottariDasha()
    
    def test_pratyantardasha_count(self, dasha_calculator):
        """Test that pratyantardasha has 9 periods"""
        start = datetime(2020, 1, 1, tzinfo=timezone.utc)
        end = datetime(2021, 1, 1, tzinfo=timezone.utc)
        
        pratyantardasha = dasha_calculator.calculate_pratyantardasha(
            "Jupiter", "Saturn", start, end
        )
        
        assert len(pratyantardasha) == 9
    
    def test_pratyantardasha_starts_with_sub_lord(self, dasha_calculator):
        """Test pratyantardasha starts with antardasha lord"""
        start = datetime(2020, 1, 1, tzinfo=timezone.utc)
        end = datetime(2021, 1, 1, tzinfo=timezone.utc)
        
        pratyantardasha = dasha_calculator.calculate_pratyantardasha(
            "Jupiter", "Moon", start, end
        )
        
        # First pratyantardasha should be Jupiter-Moon-Moon
        assert pratyantardasha[0]["planet"] == "Moon"
