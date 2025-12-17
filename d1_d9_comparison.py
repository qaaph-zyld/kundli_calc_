"""
D1 + D9 Comparison Script
Birth: October 9, 1990, 09:10 AM, Loznica, Serbia (44.5333°N, 19.2222°E)
Reference: Jagannatha Hora with Lahiri Ayanamsa
"""

import requests
import json
from datetime import datetime

API_BASE_URL = "http://127.0.0.1:8000/api/v1"
TOLERANCE = 0.25  # degrees

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# Birth data
BIRTH_DATA = {
    "date_time": "1990-10-09T08:10:00Z",  # 09:10 Local = 08:10 UTC
    "latitude": 44.5333,
    "longitude": 19.2222,
    "altitude": 0,
    "ayanamsa": 1,  # Lahiri
    "house_system": "W"  # Whole Sign
}

# JHora D1 Reference (from test_accuracy_verification.py)
JHORA_D1 = {
    "Ascendant": {"longitude": 209.17, "sign": "Libra"},
    "Sun": {"longitude": 172.05, "sign": "Virgo"},
    "Moon": {"longitude": 58.32, "sign": "Taurus"},
    "Mars": {"longitude": 49.86, "sign": "Taurus"},
    "Mercury": {"longitude": 162.58, "sign": "Virgo"},
    "Jupiter": {"longitude": 105.82, "sign": "Cancer"},
    "Venus": {"longitude": 166.03, "sign": "Virgo"},
    "Saturn": {"longitude": 265.17, "sign": "Sagittarius"},
    "Rahu": {"longitude": 279.82, "sign": "Capricorn"},
    "Ketu": {"longitude": 99.82, "sign": "Cancer"},
}

def calc_navamsa_sign(longitude):
    """Calculate Navamsa sign using classical Parashara method"""
    sign_num = int(longitude / 30)
    deg_in_sign = longitude % 30
    navamsa_span = 30 / 9  # 3.333...°
    navamsa_num = int(deg_in_sign / navamsa_span)
    
    # Starting sign depends on element
    element = sign_num % 4
    if element == 0:    # Fire (Aries=0, Leo=4, Sag=8)
        start = 0       # Aries
    elif element == 1:  # Earth (Taurus=1, Virgo=5, Cap=9)
        start = 9       # Capricorn
    elif element == 2:  # Air (Gemini=2, Libra=6, Aqua=10)
        start = 6       # Libra
    else:               # Water (Cancer=3, Scorpio=7, Pisces=11)
        start = 3       # Cancer
    
    navamsa_sign_num = (start + navamsa_num) % 12
    return navamsa_sign_num, SIGNS[navamsa_sign_num]

# Calculate expected D9 from D1 longitudes
JHORA_D9 = {}
for planet, data in JHORA_D1.items():
    nav_num, nav_sign = calc_navamsa_sign(data["longitude"])
    JHORA_D9[planet] = {"sign_num": nav_num, "sign": nav_sign}

print("=" * 70)
print("EXPECTED D9 (Navamsa) from JHora D1 longitudes:")
print("-" * 70)
for planet, data in JHORA_D9.items():
    d1_sign = JHORA_D1[planet]["sign"]
    d1_lon = JHORA_D1[planet]["longitude"]
    d9_sign = data["sign"]
    vargottama = " ★ VARGOTTAMA" if d1_sign == d9_sign else ""
    print(f"{planet:<10} D1: {d1_sign:<12} ({d1_lon:>7.2f}°)  →  D9: {d9_sign}{vargottama}")
print("=" * 70)

def get_chart():
    """Get chart from backend API"""
    try:
        r = requests.post(f"{API_BASE_URL}/charts/calculate", json=BIRTH_DATA, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"API Error: {e}")
        return None

def get_d9_chart():
    """Get D9 chart from backend API"""
    try:
        d9_request = {
            "date_time": BIRTH_DATA["date_time"],
            "latitude": BIRTH_DATA["latitude"],
            "longitude": BIRTH_DATA["longitude"],
            "altitude": BIRTH_DATA["altitude"],
            "division": 9
        }
        r = requests.post(f"{API_BASE_URL}/divisional/calculate", json=d9_request, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"D9 API Error: {e}")
        return None

def compare_d1(chart):
    """Compare D1 positions with JHora"""
    print("\n" + "=" * 70)
    print("D1 (RASI) COMPARISON - Backend vs JHora")
    print("=" * 70)
    print(f"{'Planet':<10} {'JHora':<20} {'Backend':<20} {'Diff':<8} {'Match'}")
    print("-" * 70)
    
    results = {"matches": 0, "total": 0, "details": []}
    
    for planet, jhora in JHORA_D1.items():
        results["total"] += 1
        
        if planet == "Ascendant":
            backend_lon = float(chart.get("houses", {}).get("ascendant", 0))
        else:
            backend_lon = float(chart.get("planetary_positions", {}).get(planet, {}).get("longitude", 0))
        
        jhora_lon = jhora["longitude"]
        diff = abs(jhora_lon - backend_lon)
        if diff > 180:
            diff = 360 - diff
        
        match = "✓" if diff < TOLERANCE else "✗"
        if diff < TOLERANCE:
            results["matches"] += 1
        
        backend_sign = SIGNS[int(backend_lon / 30) % 12]
        
        detail = {
            "planet": planet,
            "jhora_longitude": jhora_lon,
            "jhora_sign": jhora["sign"],
            "backend_longitude": round(backend_lon, 2),
            "backend_sign": backend_sign,
            "difference": round(diff, 3),
            "match": diff < TOLERANCE
        }
        results["details"].append(detail)
        
        print(f"{planet:<10} {jhora['sign']:<8} {jhora_lon:>7.2f}°  {backend_sign:<8} {backend_lon:>7.2f}°  {diff:>6.3f}°  {match}")
    
    print("-" * 70)
    print(f"D1 Accuracy: {results['matches']}/{results['total']} planets match within {TOLERANCE}°")
    return results

def compare_d9(d9_chart, d1_chart):
    """Compare D9 positions with expected Navamsa from JHora D1"""
    print("\n" + "=" * 70)
    print("D9 (NAVAMSA) COMPARISON - Backend vs Expected from JHora D1")
    print("=" * 70)
    print(f"{'Planet':<10} {'Expected D9':<15} {'Backend D9':<15} {'Match'}")
    print("-" * 70)
    
    results = {"matches": 0, "total": 0, "details": []}
    
    for planet, expected in JHORA_D9.items():
        results["total"] += 1
        backend_lon = 0
        
        if planet == "Ascendant":
            # Try various response structures for ascendant
            backend_lon = d9_chart.get("ascendant_longitude", 0)
            if backend_lon == 0:
                houses = d9_chart.get("house_cusps", {})
                if isinstance(houses, dict):
                    backend_lon = houses.get("1", houses.get(0, 0))
                elif isinstance(houses, list) and len(houses) > 0:
                    backend_lon = houses[0]
            if backend_lon == 0:
                # Calculate from D1 ascendant using navamsa formula
                d1_asc = float(d1_chart.get("houses", {}).get("ascendant", 0))
                nav_num, _ = calc_navamsa_sign(d1_asc)
                backend_lon = nav_num * 30  # Start of the sign
        else:
            positions = d9_chart.get("planetary_positions", {})
            if planet in positions:
                pos = positions[planet]
                if isinstance(pos, (int, float)):
                    backend_lon = pos
                elif isinstance(pos, dict):
                    backend_lon = pos.get("longitude", pos.get("position", 0))
        
        backend_sign_num = int(float(backend_lon) / 30) % 12
        backend_sign = SIGNS[backend_sign_num]
        
        match = "✓" if expected["sign"] == backend_sign else "✗"
        if expected["sign"] == backend_sign:
            results["matches"] += 1
        
        detail = {
            "planet": planet,
            "expected_sign": expected["sign"],
            "backend_sign": backend_sign,
            "backend_longitude": round(float(backend_lon), 2),
            "match": expected["sign"] == backend_sign
        }
        results["details"].append(detail)
        
        # Check vargottama
        d1_sign = JHORA_D1[planet]["sign"]
        vargottama = " (Vargottama)" if d1_sign == expected["sign"] else ""
        
        print(f"{planet:<10} {expected['sign']:<15} {backend_sign:<15} {match}{vargottama}")
    
    print("-" * 70)
    print(f"D9 Accuracy: {results['matches']}/{results['total']} signs match")
    return results

def main():
    print("\n" + "=" * 70)
    print("KUNDLI D1 + D9 VERIFICATION")
    print("Birth: October 9, 1990, 09:10 AM, Loznica, Serbia")
    print("Reference: Jagannatha Hora (Lahiri Ayanamsa, Whole Sign)")
    print("=" * 70)
    
    # Get D1 chart
    print("\nFetching D1 chart from backend...")
    d1_chart = get_chart()
    if not d1_chart:
        print("Failed to get D1 chart. Is the backend running?")
        return
    
    # Get D9 chart
    print("Fetching D9 chart from backend...")
    d9_chart = get_d9_chart()
    if not d9_chart:
        print("Failed to get D9 chart.")
        return
    
    # Compare
    d1_results = compare_d1(d1_chart)
    d9_results = compare_d9(d9_chart, d1_chart)
    
    # Generate JSON output
    output = {
        "birth_data": {
            "date": "1990-10-09",
            "time": "09:10:00",
            "place": "Loznica, Serbia",
            "coordinates": {"lat": 44.5333, "lon": 19.2222},
            "timezone": "UTC+1 (no DST in Oct 1990)"
        },
        "settings": {
            "ayanamsa": "Lahiri",
            "house_system": "Whole Sign"
        },
        "d1_comparison": d1_results,
        "d9_comparison": d9_results,
        "summary": {
            "d1_accuracy": f"{d1_results['matches']}/{d1_results['total']}",
            "d9_accuracy": f"{d9_results['matches']}/{d9_results['total']}",
            "vargottama_planets": [p for p in JHORA_D1 if JHORA_D1[p]["sign"] == JHORA_D9[p]["sign"]]
        }
    }
    
    # Save to JSON
    with open("d1_d9_comparison_result.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"D1 Accuracy: {d1_results['matches']}/{d1_results['total']} planets")
    print(f"D9 Accuracy: {d9_results['matches']}/{d9_results['total']} signs")
    print(f"Vargottama: {output['summary']['vargottama_planets']}")
    print(f"\nFull results saved to: d1_d9_comparison_result.json")

if __name__ == "__main__":
    main()
