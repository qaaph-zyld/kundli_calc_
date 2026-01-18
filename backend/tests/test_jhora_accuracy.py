"""
JHora Accuracy Validation Tests

These tests ensure planetary calculations match JHora within defined tolerances.
Reference: JHora 8.0 with Lahiri ayanamsa, Whole Sign houses.

Tolerance Standards:
- Planetary longitude: ±0.01° (36 arc-seconds)
- Ayanamsa value: ±0.001°
- Nakshatra/Pada: Exact match
"""

import json
import pytest
from datetime import datetime, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.astronomical.framework import (
    AstronomicalCalculator,
    CelestialBody,
    GeoLocation,
    AyanamsaSystem,
    CoordinateSystem,
)
import swisseph as swe


# Tolerance thresholds
TOLERANCE_LONGITUDE = 0.01  # ±0.01° = 36 arc-seconds
TOLERANCE_AYANAMSA = 0.001  # ±0.001°


class TestJHoraAccuracy:
    """Test suite for JHora accuracy validation"""

    @pytest.fixture
    def calculator(self):
        """Create calculator with Lahiri ayanamsa"""
        calc = AstronomicalCalculator(
            coordinate_system=CoordinateSystem.GEOCENTRIC,
            ayanamsa_system=AyanamsaSystem.LAHIRI
        )
        yield calc

    @pytest.fixture
    def jhora_reference(self):
        """Load JHora reference data for chart_016"""
        ref_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "jhora_reference" / "chart_016_nikola_jelacic.json"
        if not ref_path.exists():
            pytest.skip("JHora reference file not found")
        with open(ref_path) as f:
            return json.load(f)

    def test_ayanamsa_matches_jhora(self, jhora_reference):
        """Verify ayanamsa value matches JHora within tolerance"""
        birth_data = jhora_reference["birth_data"]
        
        # Calculate Julian Day (UTC)
        dt_local = datetime(
            birth_data["year"], birth_data["month"], birth_data["day"],
            birth_data["hour"], birth_data["minute"], birth_data.get("second", 0)
        )
        dt_utc = dt_local - timedelta(hours=birth_data["timezone_offset"])
        
        jd = swe.julday(
            dt_utc.year, dt_utc.month, dt_utc.day,
            dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600
        )
        
        # Get ayanamsa with LAHIRI_1940 (matches JHora)
        swe.set_sid_mode(swe.SIDM_LAHIRI_1940)
        calculated = swe.get_ayanamsa_ut(jd)
        expected = jhora_reference["settings"]["ayanamsa_value"]
        
        deviation = abs(calculated - expected)
        assert deviation <= TOLERANCE_AYANAMSA, (
            f"Ayanamsa deviation {deviation:.6f}° exceeds tolerance {TOLERANCE_AYANAMSA}°. "
            f"Expected: {expected:.6f}°, Got: {calculated:.6f}°"
        )

    def test_all_planets_within_tolerance(self, calculator, jhora_reference):
        """Verify all 9 planetary positions match JHora within ±0.01°"""
        birth_data = jhora_reference["birth_data"]
        
        # Build datetime (UTC)
        dt_local = datetime(
            birth_data["year"], birth_data["month"], birth_data["day"],
            birth_data["hour"], birth_data["minute"], birth_data.get("second", 0)
        )
        dt_utc = dt_local - timedelta(hours=birth_data["timezone_offset"])
        
        location = GeoLocation(
            latitude=birth_data["latitude"],
            longitude=birth_data["longitude"],
            altitude=0.0
        )
        
        # Calculate all positions
        positions = calculator.calculate_all_positions(dt_utc, location)
        
        # Map our CelestialBody enum to JHora planet names
        planet_map = {
            CelestialBody.SUN: "Sun",
            CelestialBody.MOON: "Moon",
            CelestialBody.MARS: "Mars",
            CelestialBody.MERCURY: "Mercury",
            CelestialBody.JUPITER: "Jupiter",
            CelestialBody.VENUS: "Venus",
            CelestialBody.SATURN: "Saturn",
            CelestialBody.RAHU: "Rahu",
            CelestialBody.KETU: "Ketu",
        }
        
        # Build expected values lookup
        expected_positions = {
            p["planet"]: p["longitude"]
            for p in jhora_reference["planetary_positions"]
        }
        
        # Validate each planet
        failed = []
        for body, planet_name in planet_map.items():
            if planet_name not in expected_positions:
                continue
                
            calculated = positions[body].longitude
            expected = expected_positions[planet_name]
            
            deviation = abs(calculated - expected)
            # Handle 360° wrap-around
            if deviation > 180:
                deviation = 360 - deviation
            
            if deviation > TOLERANCE_LONGITUDE:
                failed.append(
                    f"{planet_name}: deviation {deviation:.4f}° "
                    f"(expected {expected:.4f}°, got {calculated:.4f}°)"
                )
        
        assert not failed, (
            f"Planets exceeding ±{TOLERANCE_LONGITUDE}° tolerance:\n" +
            "\n".join(f"  - {f}" for f in failed)
        )

    @pytest.mark.parametrize("planet_name,body", [
        ("Sun", CelestialBody.SUN),
        ("Moon", CelestialBody.MOON),
        ("Mars", CelestialBody.MARS),
        ("Mercury", CelestialBody.MERCURY),
        ("Jupiter", CelestialBody.JUPITER),
        ("Venus", CelestialBody.VENUS),
        ("Saturn", CelestialBody.SATURN),
        ("Rahu", CelestialBody.RAHU),
        ("Ketu", CelestialBody.KETU),
    ])
    def test_individual_planet_accuracy(self, calculator, jhora_reference, planet_name, body):
        """Test each planet individually for detailed failure messages"""
        birth_data = jhora_reference["birth_data"]
        
        dt_local = datetime(
            birth_data["year"], birth_data["month"], birth_data["day"],
            birth_data["hour"], birth_data["minute"], birth_data.get("second", 0)
        )
        dt_utc = dt_local - timedelta(hours=birth_data["timezone_offset"])
        
        location = GeoLocation(
            latitude=birth_data["latitude"],
            longitude=birth_data["longitude"],
            altitude=0.0
        )
        
        # Calculate position
        position = calculator.calculate_planet_position(body, dt_utc, location)
        
        # Find expected
        expected = None
        for p in jhora_reference["planetary_positions"]:
            if p["planet"] == planet_name:
                expected = p["longitude"]
                break
        
        assert expected is not None, f"No reference data for {planet_name}"
        
        deviation = abs(position.longitude - expected)
        if deviation > 180:
            deviation = 360 - deviation
        
        assert deviation <= TOLERANCE_LONGITUDE, (
            f"{planet_name} deviation {deviation:.6f}° exceeds tolerance. "
            f"Expected: {expected:.6f}°, Calculated: {position.longitude:.6f}°"
        )


class TestSampleChartCalculations:
    """Test calculations on sample charts (no JHora reference yet)"""

    @pytest.fixture
    def sample_charts(self):
        """Load sample birth data"""
        fixture_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "sample_birth_data.json"
        if not fixture_path.exists():
            pytest.skip("Sample birth data not found")
        with open(fixture_path) as f:
            return json.load(f)["charts"]

    def test_all_charts_calculate_successfully(self, sample_charts):
        """Verify all 15 sample charts calculate without errors"""
        calc = AstronomicalCalculator(
            coordinate_system=CoordinateSystem.GEOCENTRIC,
            ayanamsa_system=AyanamsaSystem.LAHIRI
        )
        
        for chart in sample_charts:
            birth_data = chart["birth_data"]
            
            dt = datetime(
                birth_data["year"], birth_data["month"], birth_data["day"],
                birth_data["hour"], birth_data["minute"], birth_data.get("second", 0)
            )
            dt_utc = dt - timedelta(hours=birth_data.get("timezone_offset", 0))
            
            location = GeoLocation(
                latitude=birth_data["latitude"],
                longitude=birth_data["longitude"],
                altitude=0.0
            )
            
            # Should not raise any exceptions
            positions = calc.calculate_all_positions(dt_utc, location)
            
            # Basic sanity checks
            assert len(positions) >= 9, f"Chart {chart['id']}: Expected at least 9 planets"
            
            for body, pos in positions.items():
                assert 0 <= pos.longitude < 360, (
                    f"Chart {chart['id']}, {body}: Invalid longitude {pos.longitude}"
                )

    def test_edge_case_midnight(self, sample_charts):
        """Test exact midnight calculation (chart_005)"""
        chart = next((c for c in sample_charts if c["id"] == "chart_005"), None)
        if not chart:
            pytest.skip("chart_005 not found")
        
        calc = AstronomicalCalculator()
        birth_data = chart["birth_data"]
        
        # Midnight exactly
        dt = datetime(1995, 8, 15, 0, 0, 0)
        dt_utc = dt - timedelta(hours=5.5)  # IST
        
        location = GeoLocation(latitude=13.0827, longitude=80.2707, altitude=0.0)
        positions = calc.calculate_all_positions(dt_utc, location)
        
        assert all(0 <= p.longitude < 360 for p in positions.values())

    def test_edge_case_polar_latitude(self, sample_charts):
        """Test high latitude calculation (chart_006 - Iceland 64°N)"""
        chart = next((c for c in sample_charts if c["id"] == "chart_006"), None)
        if not chart:
            pytest.skip("chart_006 not found")
        
        calc = AstronomicalCalculator()
        birth_data = chart["birth_data"]
        
        dt = datetime(2000, 6, 21, 12, 0, 0)  # Summer solstice
        location = GeoLocation(latitude=64.1466, longitude=-21.9426, altitude=0.0)
        
        positions = calc.calculate_all_positions(dt, location)
        assert all(0 <= p.longitude < 360 for p in positions.values())

    def test_edge_case_historical_date(self, sample_charts):
        """Test 19th century date (chart_012)"""
        chart = next((c for c in sample_charts if c["id"] == "chart_012"), None)
        if not chart:
            pytest.skip("chart_012 not found")
        
        calc = AstronomicalCalculator()
        
        dt = datetime(1879, 3, 14, 10, 30, 0)  # Einstein's birth
        location = GeoLocation(latitude=48.2082, longitude=16.3738, altitude=0.0)
        
        positions = calc.calculate_all_positions(dt, location)
        assert all(0 <= p.longitude < 360 for p in positions.values())


class TestLahiriAyanamsaConfiguration:
    """Test that Lahiri ayanamsa is correctly configured"""

    def test_uses_lahiri_1940_variant(self):
        """Verify SIDM_LAHIRI_1940 is used for JHora compatibility"""
        calc = AstronomicalCalculator(ayanamsa_system=AyanamsaSystem.LAHIRI)
        
        # Test date: Oct 9, 1990
        dt = datetime(1990, 10, 9, 8, 10, 0)
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60)
        
        # SIDM_LAHIRI_1940 should give ~23.713° for this date
        swe.set_sid_mode(swe.SIDM_LAHIRI_1940)
        expected = swe.get_ayanamsa_ut(jd)
        
        # Now verify our calculator uses the same
        location = GeoLocation(latitude=44.5333, longitude=19.2167, altitude=0.0)
        positions = calc.calculate_all_positions(dt, location)
        
        # The positions should match what SIDM_LAHIRI_1940 produces
        sun_pos = positions[CelestialBody.SUN].longitude
        
        # Calculate expected Sun position with SIDM_LAHIRI_1940
        swe.set_sid_mode(swe.SIDM_LAHIRI_1940)
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED | swe.FLG_TRUEPOS
        result = swe.calc_ut(jd, swe.SUN, flags)
        expected_sun = result[0][0]
        
        assert abs(sun_pos - expected_sun) < 0.001, (
            f"Sun position mismatch: expected {expected_sun:.4f}°, got {sun_pos:.4f}°"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
