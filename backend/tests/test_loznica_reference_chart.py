"""Loznica Reference Chart Regression Test

Locks in the user's provided D1 reference chart for:
- 1990-10-09 09:10 local (Europe/Belgrade), Loznica, Serbia
- Lahiri ayanamsa
- Whole Sign houses

This ensures the API calculation stays stable and never drifts.
"""

from fastapi.testclient import TestClient
from app.main import app


def _deg(sign: str, deg: int, minutes: int) -> float:
    signs = {
        "Aries": 0,
        "Taurus": 30,
        "Gemini": 60,
        "Cancer": 90,
        "Leo": 120,
        "Virgo": 150,
        "Libra": 180,
        "Scorpio": 210,
        "Sagittarius": 240,
        "Capricorn": 270,
        "Aquarius": 300,
        "Pisces": 330,
    }
    return (signs[sign] + deg + minutes / 60.0) % 360


def test_loznica_d1_reference_chart_positions_and_ascendant():
    client = TestClient(app)

    # User-provided D1 reference (Lahiri + Whole Sign)
    expected = {
        "Sun": _deg("Virgo", 22, 2),
        "Moon": _deg("Taurus", 28, 19),
        "Mercury": _deg("Virgo", 12, 34),
        "Venus": _deg("Virgo", 16, 2),
        "Mars": _deg("Taurus", 19, 54),
        "Jupiter": _deg("Cancer", 15, 50),
        "Saturn": _deg("Sagittarius", 25, 11),
        "Rahu": _deg("Capricorn", 9, 49),
        "Ascendant": _deg("Libra", 28, 55),
    }

    payload = {
        # IMPORTANT: Provide timezone-aware local datetime.
        # The backend must normalize to UTC and calculate identical to Z time.
        "date_time": "1990-10-09T09:10:00+01:00",
        "latitude": 44.5309221,
        "longitude": 19.2237478,
        "altitude": 0,
        "ayanamsa_type": "lahiri",
        "house_system": "W",
    }

    r = client.post("/api/v1/charts/calculate", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()

    tol = 0.2  # degrees (~12 arcminutes) - can tighten once we confirm rounding rules

    # Ascendant
    asc = float(data["houses"]["ascendant"])
    assert abs(asc - expected["Ascendant"]) < tol, f"ASC expected {expected['Ascendant']}, got {asc}"

    # Planets
    positions = data["planetary_positions"]
    for planet in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu"]:
        got = float(positions[planet]["longitude"])
        exp = expected[planet]
        diff = abs(got - exp)
        diff = min(diff, 360 - diff)
        assert diff < tol, f"{planet} expected {exp}, got {got} (diff {diff})"


def test_loznica_whole_sign_house_cusps_from_asc_sign():
    client = TestClient(app)

    payload = {
        "date_time": "1990-10-09T09:10:00+01:00",
        "latitude": 44.5309221,
        "longitude": 19.2237478,
        "altitude": 0,
        "ayanamsa_type": "lahiri",
        "house_system": "W",
    }

    r = client.post("/api/v1/charts/calculate", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()

    cusps = [float(x) for x in data["houses"]["cusps"]]
    asc = float(data["houses"]["ascendant"])

    asc_sign_start = int(asc / 30) * 30
    expected_cusps = [((asc_sign_start + i * 30) % 360) for i in range(12)]

    for i in range(12):
        assert abs(cusps[i] - expected_cusps[i]) < 0.01
