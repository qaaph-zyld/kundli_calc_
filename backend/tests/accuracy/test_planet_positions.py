"""
Planet Position Accuracy Tests
===============================

Validates planet calculations against JHora reference charts.
Requires: Reference charts in reference_charts/ directory
"""

import pytest
import json
from pathlib import Path
from datetime import datetime
import swisseph as swe

from app.core.calculations.engine_core import VedicChartEngine
from app.core.calculations.ayanamsa import EnhancedAyanamsaManager


REFERENCE_DIR = Path(__file__).parent / "reference_charts"


def load_reference_chart(chart_name: str) -> dict:
    """Load JHora reference chart data"""
    chart_path = REFERENCE_DIR / f"{chart_name}.json"
    
    if not chart_path.exists():
        pytest.skip(f"Reference chart {chart_name}.json not found. "
                   f"Generate it using JHora following reference_charts/README.md")
    
    with open(chart_path, 'r') as f:
        return json.load(f)


@pytest.mark.parametrize("chart_name", [
    "test_chart_1",
    "test_chart_2",
    "test_chart_3",
    "celebrity_chart_1",
    "celebrity_chart_2"
])
def test_planet_positions_match_jhora(chart_name):
    """
    Validate planet positions match JHora for reference charts.
    
    Tolerance: ±0.01 degrees (36 arcseconds)
    This accounts for minor ephemeris precision differences.
    """
    reference = load_reference_chart(chart_name)
    
    birth_data = reference["birth_data"]
    dt = datetime.fromisoformat(birth_data["datetime"])
    
    jd = swe.julday(dt.year, dt.month, dt.day, 
                    dt.hour + dt.minute/60.0 + dt.second/3600.0)
    
    engine = VedicChartEngine()
    chart_data = engine.calculate(
        jd,
        birth_data['latitude'],
        birth_data['longitude'],
        ayanamsa_id=1
    )
    our_planets = chart_data['planets']
    
    ayanamsa_mgr = EnhancedAyanamsaManager()
    ayanamsa = ayanamsa_mgr.get_ayanamsa(jd, ayanamsa_id=1)
    
    planets_to_test = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", 
                       "Venus", "Saturn", "Rahu", "Ketu"]
    
    tolerance = 0.01
    results = []
    
    for planet in planets_to_test:
        jhora_data = reference["planets"][planet]
        jhora_sidereal = jhora_data["sidereal_longitude"]
        
        our_tropical = our_planets[planet]["longitude"]
        our_sidereal = (our_tropical - ayanamsa) % 360
        
        diff = abs(jhora_sidereal - our_sidereal)
        
        if diff > 180:
            diff = 360 - diff
        
        results.append({
            "planet": planet,
            "jhora": jhora_sidereal,
            "ours": our_sidereal,
            "diff": diff,
            "pass": diff < tolerance
        })
        
        assert diff < tolerance, \
            f"{planet} position mismatch in {chart_name}: " \
            f"JHora={jhora_sidereal:.4f}°, Ours={our_sidereal:.4f}°, " \
            f"Diff={diff:.4f}° (tolerance={tolerance}°)"
    
    passed = sum(1 for r in results if r["pass"])
    print(f"\n{chart_name}: {passed}/{len(planets_to_test)} planets within tolerance")


def test_tropical_to_sidereal_conversion():
    """
    Test tropical → sidereal conversion accuracy.
    
    Verifies that:
    1. Tropical positions are calculated correctly from Swiss Ephemeris
    2. Lahiri ayanamsa is applied correctly
    3. Sidereal positions match expected values
    """
    jd = swe.julday(2000, 1, 1, 0.0)
    
    engine = VedicChartEngine()
    chart_data = engine.calculate(
        jd,
        28.6139,
        77.2090,
        ayanamsa_id=1
    )
    planets = chart_data['planets']
    
    ayanamsa_mgr = EnhancedAyanamsaManager()
    ayanamsa = ayanamsa_mgr.get_ayanamsa(jd, ayanamsa_id=1)
    
    sun_tropical = planets["Sun"]["longitude"]
    sun_sidereal = (sun_tropical - ayanamsa) % 360
    
    assert 275 < sun_tropical < 285, \
        f"Sun tropical position unexpected: {sun_tropical}° (expected ~280°)"
    
    assert 23.8 < ayanamsa < 23.9, \
        f"Lahiri ayanamsa unexpected: {ayanamsa}° (expected ~23.85°)"
    
    assert 251 < sun_sidereal < 261, \
        f"Sun sidereal position unexpected: {sun_sidereal}° (expected ~256°)"


def test_rahu_ketu_opposition():
    """
    Validate Rahu and Ketu are always 180° apart (exact opposition).
    
    Tests multiple dates to ensure the opposition is maintained.
    """
    test_dates = [
        (1990, 5, 15, 10.5),
        (2000, 1, 1, 0.0),
        (2010, 12, 25, 18.0),
        (2020, 7, 4, 12.0),
        (2026, 1, 10, 0.0)
    ]
    
    engine = VedicChartEngine()
    
    for year, month, day, hour in test_dates:
        jd = swe.julday(year, month, day, hour)
        chart_data = engine.calculate(
            jd,
            28.6139,
            77.2090,
            ayanamsa_id=1
        )
        planets = chart_data['planets']
        
        rahu_long = planets["Rahu"]["longitude"]
        ketu_long = planets["Ketu"]["longitude"]
        
        diff = abs(rahu_long - ketu_long)
        
        if diff > 180:
            diff = 360 - diff
        
        assert abs(diff - 180.0) < 0.001, \
            f"Rahu-Ketu not in opposition on {year}-{month:02d}-{day:02d}: " \
            f"Rahu={rahu_long:.4f}°, Ketu={ketu_long:.4f}°, diff={diff:.4f}°"


def test_retrograde_detection():
    """
    Test retrograde motion detection for planets.
    
    Validates that retrograde status is correctly calculated
    for planets that can go retrograde.
    """
    test_cases = [
    ]
    
    if not test_cases:
        pytest.skip("Retrograde test cases need to be populated with verified dates")
    
    engine = VedicChartEngine()
    
    for case in test_cases:
        year, month, day, hour = case["date"]
        jd = swe.julday(year, month, day, hour)
        
        chart_data = engine.calculate(
            jd,
            28.6139,
            77.2090,
            ayanamsa_id=1
        )
        planets = chart_data['planets']
        planet_data = planets[case["planet"]]
        
        is_retrograde = planet_data.get("is_retrograde", False)
        expected = case["expected_retrograde"]
        
        assert is_retrograde == expected, \
            f"{case['planet']} retrograde mismatch on {year}-{month:02d}-{day:02d}: " \
            f"expected {expected}, got {is_retrograde}"


def generate_reference_chart_template():
    """
    Generate template for JHora reference chart JSON.
    
    Use this to create the structure, then fill in actual values from JHora.
    """
    template = {
        "chart_name": "Test Chart 1",
        "description": "Birth chart for accuracy validation",
        "birth_data": {
            "datetime": "1990-05-15T10:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata",
            "place": "New Delhi, India",
            "ayanamsa": "Lahiri",
            "ayanamsa_value": 23.65
        },
        "planets": {
            "Sun": {
                "tropical_longitude": 0.0,
                "sidereal_longitude": 0.0,
                "sign": "Taurus",
                "degree": 0.0,
                "house": 10,
                "nakshatra": "Rohini",
                "pada": 1
            }
        },
        "houses": {
            "1": {"sign": "Leo", "cusp": 120.0}
        },
        "dashas": {
            "birth_balance": {
                "planet": "Sun",
                "years_remaining": 3.5
            },
            "current_mahadasha": {
                "planet": "Sun",
                "start_date": "1989-03-15",
                "end_date": "1995-03-15"
            }
        },
        "yogas_detected": [
            "Gaja Kesari",
            "Budha Aditya"
        ]
    }
    
    return template


if __name__ == "__main__":
    template = generate_reference_chart_template()
    import json
    print(json.dumps(template, indent=2))
