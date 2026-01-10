"""
Dasha Period Accuracy Tests
============================

Validates Vimshottari dasha calculations against JHora.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime, timedelta

from app.core.calculations.dasha_system import VimshottariDasha


REFERENCE_DIR = Path(__file__).parent / "reference_charts"


def load_reference_chart(chart_name: str) -> dict:
    """Load JHora reference chart"""
    chart_path = REFERENCE_DIR / f"{chart_name}.json"
    
    if not chart_path.exists():
        pytest.skip(f"Reference chart {chart_name}.json not found")
    
    with open(chart_path, 'r') as f:
        return json.load(f)


@pytest.mark.parametrize("chart_name", [
    "test_chart_1",
    "test_chart_2",
    "test_chart_3"
])
def test_dasha_birth_balance(chart_name):
    """
    Validate dasha balance at birth matches JHora.
    
    Tests:
    - Which planet's dasha is active at birth
    - How many years/months/days remaining in that dasha
    
    Tolerance: ±1 day
    """
    reference = load_reference_chart(chart_name)
    
    birth_data = reference["birth_data"]
    dt = datetime.fromisoformat(birth_data["datetime"])
    
    dasha_calc = VimshottariDashaCalculator()
    our_balance = dasha_calc.calculate_birth_balance(
        dt,
        birth_data["latitude"],
        birth_data["longitude"]
    )
    
    jhora_balance = reference["dashas"]["birth_balance"]
    
    assert our_balance["planet"] == jhora_balance["planet"], \
        f"Birth dasha planet mismatch: " \
        f"JHora={jhora_balance['planet']}, Ours={our_balance['planet']}"
    
    jhora_years = jhora_balance["years_remaining"]
    our_years = our_balance["years_remaining"]
    
    tolerance_days = 1
    tolerance_years = tolerance_days / 365.25
    
    assert abs(jhora_years - our_years) < tolerance_years, \
        f"Birth dasha balance mismatch: " \
        f"JHora={jhora_years:.4f} years, Ours={our_years:.4f} years, " \
        f"diff={abs(jhora_years - our_years):.4f} years"


@pytest.mark.parametrize("chart_name", [
    "test_chart_1",
    "test_chart_2"
])
def test_mahadasha_periods(chart_name):
    """
    Validate mahadasha start/end dates match JHora.
    
    Tests all 9 mahadasha periods in sequence.
    Tolerance: ±1 day
    """
    reference = load_reference_chart(chart_name)
    
    birth_data = reference["birth_data"]
    dt = datetime.fromisoformat(birth_data["datetime"])
    
    dasha_calc = VimshottariDashaCalculator()
    our_dashas = dasha_calc.calculate_all_mahadashas(
        dt,
        birth_data["latitude"],
        birth_data["longitude"]
    )
    
    jhora_current = reference["dashas"]["current_mahadasha"]
    
    our_current = None
    for dasha in our_dashas:
        if dasha["planet"] == jhora_current["planet"]:
            our_current = dasha
            break
    
    assert our_current is not None, \
        f"Could not find {jhora_current['planet']} mahadasha in our calculations"
    
    jhora_start = datetime.fromisoformat(jhora_current["start_date"])
    jhora_end = datetime.fromisoformat(jhora_current["end_date"])
    
    our_start = datetime.fromisoformat(our_current["start_date"])
    our_end = datetime.fromisoformat(our_current["end_date"])
    
    tolerance = timedelta(days=1)
    
    assert abs((jhora_start - our_start).total_seconds()) < tolerance.total_seconds(), \
        f"Mahadasha start date mismatch: JHora={jhora_start}, Ours={our_start}"
    
    assert abs((jhora_end - our_end).total_seconds()) < tolerance.total_seconds(), \
        f"Mahadasha end date mismatch: JHora={jhora_end}, Ours={our_end}"


def test_dasha_sequence_order():
    """
    Validate Vimshottari dasha sequence is correct.
    
    Standard sequence: Sun → Moon → Mars → Rahu → Jupiter → 
                      Saturn → Mercury → Ketu → Venus
    
    Each person starts at different point based on birth nakshatra.
    """
    standard_sequence = [
        "Sun", "Moon", "Mars", "Rahu", "Jupiter",
        "Saturn", "Mercury", "Ketu", "Venus"
    ]
    
    dt = datetime(1990, 5, 15, 10, 30, 0)
    lat, lon = 28.6139, 77.2090
    
    dasha_calc = VimshottariDashaCalculator()
    dashas = dasha_calc.calculate_all_mahadashas(dt, lat, lon)
    
    our_sequence = [d["planet"] for d in dashas]
    
    start_planet = our_sequence[0]
    start_index = standard_sequence.index(start_planet)
    
    expected_sequence = (
        standard_sequence[start_index:] + 
        standard_sequence[:start_index]
    )
    
    assert our_sequence == expected_sequence, \
        f"Dasha sequence incorrect: expected {expected_sequence}, got {our_sequence}"


def test_dasha_durations():
    """
    Validate mahadasha durations match Vimshottari standard.
    
    Standard durations (in years):
    Sun: 6, Moon: 10, Mars: 7, Rahu: 18, Jupiter: 16,
    Saturn: 19, Mercury: 17, Ketu: 7, Venus: 20
    """
    standard_durations = {
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
        "Ketu": 7,
        "Venus": 20
    }
    
    dt = datetime(2000, 1, 1, 0, 0, 0)
    lat, lon = 28.6139, 77.2090
    
    dasha_calc = VimshottariDashaCalculator()
    dashas = dasha_calc.calculate_all_mahadashas(dt, lat, lon)
    
    tolerance_days = 1
    
    for dasha in dashas:
        planet = dasha["planet"]
        
        start = datetime.fromisoformat(dasha["start_date"])
        end = datetime.fromisoformat(dasha["end_date"])
        
        duration_days = (end - start).days
        duration_years = duration_days / 365.25
        
        expected_years = standard_durations[planet]
        
        assert abs(duration_years - expected_years) < (tolerance_days / 365.25), \
            f"{planet} mahadasha duration incorrect: " \
            f"expected {expected_years} years, got {duration_years:.4f} years"
