"""
Verify chart calculation with correct timezone
October 9, 1990, 09:10 AM Local = 08:10 UTC
"""
import requests
import json

API_BASE = "http://127.0.0.1:8000/api/v1"

# CORRECTED: 09:10 AM local = 08:10 UTC (CET = UTC+1)
CORRECT_UTC = "1990-10-09T08:10:00"

# Also test October 24, 1990, 10:15 AM local = 09:15 UTC
OCT24_UTC = "1990-10-24T09:15:00"

def get_sign_degree(longitude):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign_num = int(longitude / 30)
    degree = longitude % 30
    minutes = (degree % 1) * 60
    return signs[sign_num], int(degree), int(minutes)

def format_degree(longitude):
    sign, deg, mins = get_sign_degree(longitude)
    return f"{sign} {deg:02d}°{mins:02d}'"

def test_chart(datetime_utc, label):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  UTC Time: {datetime_utc}")
    print(f"{'='*60}")
    
    payload = {
        "date_time": datetime_utc,
        "latitude": 44.5333,
        "longitude": 19.2222,
        "ayanamsa": 1,  # Lahiri
        "house_system": "W"  # Whole Sign
    }
    
    r = requests.post(f"{API_BASE}/charts/calculate", json=payload)
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        return
    
    data = r.json()
    planets = data.get("planetary_positions", {})
    houses = data.get("houses", {})
    
    # Ascendant
    asc = float(houses.get("ascendant", 0))
    mc = float(houses.get("midheaven", 0))
    
    print(f"\n  ASC:  {format_degree(asc)}")
    print(f"  MC:   {format_degree(mc)}")
    
    print(f"\n  {'Planet':<10} {'Sign':<12} {'Degree':>8}")
    print(f"  {'-'*35}")
    
    order = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Rahu", "Ketu"]
    for planet in order:
        if planet in planets:
            info = planets[planet]
            longitude = float(info.get("longitude", 0))
            sign, deg, mins = get_sign_degree(longitude)
            retro = " R" if planet in ["Rahu", "Ketu"] else ""
            print(f"  {planet:<10} {sign:<12} {deg:02d}°{mins:02d}'{retro}")
    
    return data

# Test with corrected time
print("\n" + "#"*60)
print("#  CHART VERIFICATION")
print("#"*60)

# October 9, 1990 - CORRECTED
chart1 = test_chart(CORRECT_UTC, "OCTOBER 9, 1990 - 09:10 AM Local (08:10 UTC)")

# October 24, 1990
chart2 = test_chart(OCT24_UTC, "OCTOBER 24, 1990 - 10:15 AM Local (09:15 UTC)")

# Reference comparison
print("\n" + "="*60)
print("  REFERENCE COMPARISON (Oct 9)")
print("="*60)
print("""
  Your Reference:           My Calculation:
  ASC: Libra 28°55'         ASC: [see above]
  Sun: Virgo 22°02'         Sun: [see above]
  Moon: Taurus 28°19'       Moon: [see above]
  Mercury: Virgo 12°34'     Mercury: [see above]
  Venus: Virgo 16°02'       Venus: [see above]
  Mars: Taurus 19°54'       Mars: [see above]
  Jupiter: Cancer 15°50'    Jupiter: [see above]
  Saturn: Sag 25°11'        Saturn: [see above]
  Rahu: Cap 9°49' R         Rahu: [see above]
""")
