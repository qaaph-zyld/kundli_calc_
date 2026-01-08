import os
from datetime import datetime

# Must be set at import-time (before autouse fixture setup) to disable swisseph mocking
os.environ["MOCK_SWISSEPH"] = "0"
os.environ["ENV"] = "test"

from fastapi.testclient import TestClient

from app.main import app


def test_traditional_report_real_birth_chart_smoke() -> None:
    client = TestClient(app)

    payload = {
        "date": "1990-10-09",
        "time": "09:10",
        "timezone": "Europe/Belgrade",
        "latitude": 44.5333,
        "longitude": 19.2333,
        "ayanamsa": "lahiri",
        "house_system": "W",
        "include_ashtakavarga_reductions": True,
        "include_current_transits": True,
        # Freeze transit snapshot for deterministic-ish results
        "transit_datetime_utc": "2025-12-25T00:00:00Z",
    }

    r = client.post("/api/v1/traditional/report", json=payload)
    assert r.status_code == 200, r.text

    data = r.json()

    assert data["birth"]["timezone"] == "Europe/Belgrade"
    assert data["birth"]["ayanamsa"] == "lahiri"

    # Ascendant should be Libra for this birth data in our current Swiss Ephemeris setup
    assert data["ascendant"]["sign"] == "Libra"

    # Ensure core sections exist
    assert "ashtakavarga" in data
    assert "jaimini" in data
    assert "bhava" in data
    assert "remedies" in data
    assert "transits" in data and data["transits"] is not None

    # Ensure Atmakaraka computed
    assert data["jaimini"]["chara_karakas"]["Atmakaraka"]["planet"] in {
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
    }

    # Ashtakavarga sanity
    sarva_house = data["ashtakavarga"]["sarvashtakavarga_by_house"]
    assert isinstance(sarva_house, list)
    assert len(sarva_house) == 12

    # Transit sanity
    assert "transits_from_moon" in data["transits"]
    assert "transits_from_lagna" in data["transits"]
    assert len(data["transits"]["transits_from_moon"]) == 7
    assert len(data["transits"]["transits_from_lagna"]) == 7
