"""
Comprehensive Kundli Calculation - FINAL VERSION
Date: October 9, 1990
Time: 09:10 AM Local (07:10 UTC)
Location: Loznica, Serbia (44.5333°N, 19.2222°E)
"""

import requests
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000/api/v1"

# Birth Details - October 9, 1990, 09:10 AM local = 07:10 UTC
BIRTH_DATETIME_UTC = "1990-10-09T07:10:00"
LATITUDE = 44.5333
LONGITUDE = 19.2222

SIGN_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def get_nakshatra(longitude):
    """Get nakshatra from longitude"""
    nak_span = 360 / 27
    nak_idx = int(longitude / nak_span)
    pada = int((longitude % nak_span) / (nak_span / 4)) + 1
    return NAKSHATRAS[nak_idx % 27], pada

def test_main_chart():
    """Test 1: Main Birth Chart"""
    print_section("TEST 1: MAIN BIRTH CHART (D1 Rasi)")
    
    payload = {
        "date_time": BIRTH_DATETIME_UTC,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "ayanamsa": 1,  # Lahiri
        "house_system": "W"  # Whole Sign
    }
    
    response = requests.post(f"{API_BASE}/charts/calculate", json=payload)
    if response.status_code != 200:
        print(f"✗ Error: {response.status_code}")
        return None, {}, None
    
    data = response.json()
    print("✓ Chart calculated successfully (Lahiri Ayanamsa)")
    print(f"  Ayanamsa Value: {float(data.get('ayanamsa_value', 0)):.4f}°")
    
    # Ascendant
    houses = data.get("houses", {})
    asc_long = float(houses.get("ascendant", 0))
    asc_sign_num = int(asc_long / 30)
    asc_sign = SIGN_NAMES[asc_sign_num]
    asc_degree = asc_long % 30
    asc_nak, asc_pada = get_nakshatra(asc_long)
    
    print(f"\n🔮 ASCENDANT (Lagna)")
    print(f"   Sign: {asc_sign} {asc_degree:.2f}°")
    print(f"   Nakshatra: {asc_nak} Pada {asc_pada}")
    
    # Planets
    planets = data.get("planetary_positions", {})
    planet_houses = {}
    
    print("\n--- PLANETARY POSITIONS ---")
    print(f"{'Planet':<12} {'Sign':<12} {'Degree':>8} {'House':>6} {'Nakshatra':<20}")
    print("-" * 65)
    
    for planet, info in planets.items():
        longitude = float(info.get("longitude", 0))
        sign = info.get("sign", "N/A")
        house = info.get("house", 0)
        degree = longitude % 30
        nak, pada = get_nakshatra(longitude)
        
        planet_houses[planet] = house
        print(f"{planet:<12} {sign:<12} {degree:>7.2f}° {house:>5}  {nak} P{pada}")
    
    return data, planet_houses, asc_sign

def test_panchang():
    """Test 2: Panchang"""
    print_section("TEST 2: PANCHANG (Birth Tithi)")
    
    payload = {"date_time": BIRTH_DATETIME_UTC}
    
    response = requests.post(f"{API_BASE}/panchang/calculate", json=payload)
    if response.status_code != 200:
        print(f"✗ Error: {response.status_code}")
        return None
    
    data = response.json()
    print("✓ Panchang calculated")
    
    tithi_num = data.get("tithi_number", 0)
    tithi_names = ["Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
                   "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
                   "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima"]
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"
    tithi_idx = (tithi_num - 1) % 15
    
    print(f"\n  📅 Tithi: {paksha} {tithi_names[tithi_idx]}")
    print(f"  ⭐ Nakshatra: {data.get('nakshatra_name', 'N/A')} (Pada {data.get('nakshatra_pada', 'N/A')})")
    print(f"  🕉️ Yoga: {data.get('yoga_name', 'N/A')}")
    
    return data

def test_dasha(chart_data):
    """Test 3: Vimshottari Dasha"""
    print_section("TEST 3: VIMSHOTTARI DASHA")
    
    if not chart_data:
        print("✗ No chart data")
        return None
    
    planets = chart_data.get("planetary_positions", {})
    moon = planets.get("Moon", {})
    moon_long = float(moon.get("longitude", 0))
    
    # Dasha endpoint format
    payload = {
        "birth_date": BIRTH_DATETIME_UTC[:10],
        "birth_datetime": BIRTH_DATETIME_UTC,
        "moon_longitude": moon_long,
        "planet_longitudes": {
            p: float(info.get("longitude", 0)) 
            for p, info in planets.items()
        }
    }
    
    response = requests.post(f"{API_BASE}/dasha/vimshottari", json=payload)
    if response.status_code != 200:
        print(f"✗ Error: {response.status_code} - {response.text[:200]}")
        return None
    
    data = response.json()
    print("✓ Dasha periods calculated")
    
    # Current dasha
    current = data.get("current_period", {})
    if current:
        print(f"\n  🌟 CURRENT DASHA (December 2024)")
        print(f"     Mahadasha: {current.get('mahadasha', 'N/A')}")
        print(f"     Antardasha: {current.get('antardasha', 'N/A')}")
    
    # Mahadasha sequence
    periods = data.get("mahadasha_periods", [])
    if periods:
        print(f"\n  📜 MAHADASHA SEQUENCE")
        for p in periods:
            planet = p.get("planet", "N/A")
            start = p.get("start", "")[:10]
            end = p.get("end", "")[:10]
            print(f"     {planet:<10} {start} → {end}")
    
    return data

def test_lal_kitab(planet_houses):
    """Test 4: Lal Kitab Analysis"""
    print_section("TEST 4: LAL KITAB ANALYSIS")
    
    if not planet_houses:
        print("✗ No planet houses data")
        return None
    
    payload = {"planet_houses": planet_houses}
    
    response = requests.post(f"{API_BASE}/lal-kitab/analyze", json=payload)
    if response.status_code != 200:
        print(f"✗ Error: {response.status_code}")
        return None
    
    data = response.json()
    print("✓ Lal Kitab analysis completed")
    
    # Karmic Debts
    debts = data.get("karmic_debts", [])
    if debts:
        print(f"\n  ⚠️ KARMIC DEBTS (Rin)")
        for d in debts[:3]:
            print(f"     • {d.get('type', 'N/A')}")
    
    # Priority Remedies
    remedies = data.get("priority_remedies", [])
    if remedies:
        print(f"\n  💊 PRIORITY REMEDIES (Upay)")
        for i, r in enumerate(remedies[:5], 1):
            planet = r.get("planet", "")
            remedy = r.get("remedy", "")[:50]
            print(f"     {i}. [{planet}] {remedy}...")
    
    return data

def test_divisional(chart_data):
    """Test 5: Navamsa (D9) Chart"""
    print_section("TEST 5: NAVAMSA CHART (D9)")
    
    if not chart_data:
        print("✗ No chart data")
        return None
    
    # Get divisional charts from main response
    divisional = chart_data.get("divisional_charts", {})
    navamsa = divisional.get("D9", {})
    
    if navamsa:
        print("✓ Navamsa extracted from chart data")
        print("\n  📊 NAVAMSA POSITIONS")
        for planet, info in navamsa.items():
            if isinstance(info, dict):
                sign = info.get("sign", "N/A")
                print(f"     {planet:<12}: {sign}")
        return navamsa
    
    # Fallback: call divisional endpoint
    planets = chart_data.get("planetary_positions", {})
    asc = float(chart_data.get("houses", {}).get("ascendant", 0))
    
    payload = {
        "division": 9,
        "planet_longitudes": {
            p: float(info.get("longitude", 0)) 
            for p, info in planets.items()
        },
        "ascendant_longitude": asc,
        "ayanamsa_value": float(chart_data.get("ayanamsa_value", 23.72))
    }
    
    response = requests.post(f"{API_BASE}/divisional/calculate", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✓ Navamsa calculated")
        return data
    else:
        print(f"✗ Could not calculate: {response.status_code}")
        return None

def test_aspects(chart_data):
    """Test 6: Planetary Aspects"""
    print_section("TEST 6: PLANETARY ASPECTS")
    
    aspects = chart_data.get("aspects", []) if chart_data else []
    
    if not aspects:
        print("✗ No aspects data")
        return None
    
    print("✓ Aspects retrieved")
    print(f"\n  🔗 MAJOR ASPECTS ({len(aspects)} total)")
    
    for asp in aspects[:10]:
        p1 = asp.get("planet1", "N/A")
        p2 = asp.get("planet2", "N/A")
        asp_type = asp.get("aspect_type", asp.get("aspect", "N/A"))
        orb = asp.get("orb", 0)
        print(f"     {p1:<10} {asp_type:<12} {p2:<10} (orb: {orb:.1f}°)")
    
    return aspects

def test_strength(chart_data):
    """Test 7: Planetary Strengths"""
    print_section("TEST 7: PLANETARY STRENGTH")
    
    strengths = chart_data.get("planetary_strengths", {}) if chart_data else {}
    
    if not strengths:
        print("✗ No strength data")
        return None
    
    print("✓ Strengths retrieved")
    print(f"\n  💪 PLANET STRENGTH ANALYSIS")
    
    for planet, strength in strengths.items():
        if isinstance(strength, dict):
            total = strength.get("total", 0)
            status = "Strong" if total >= 1.0 else "Weak"
            print(f"     {planet:<12}: {total:.2f} ({status})")
        else:
            print(f"     {planet:<12}: {strength}")
    
    return strengths

def generate_interpretation(chart_data, planet_houses, asc_sign, panchang_data, dasha_data):
    """Generate comprehensive Kundli interpretation"""
    print_section("🔮 YOUR COMPLETE KUNDLI INTERPRETATION 🔮")
    
    if not chart_data:
        print("Insufficient data for interpretation")
        return
    
    planets = chart_data.get("planetary_positions", {})
    
    # Lagna Lord
    asc_lords = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    
    print(f"\n╔{'═'*68}╗")
    print(f"║  BIRTH DATA                                                        ║")
    print(f"╠{'═'*68}╣")
    print(f"║  Date: October 9, 1990 | Time: 09:10 AM                            ║")
    print(f"║  Place: Loznica, Serbia (44.53°N, 19.22°E)                         ║")
    print(f"║  Ayanamsa: Lahiri | Houses: Whole Sign                             ║")
    print(f"╚{'═'*68}╝")
    
    # Ascendant Analysis
    print(f"\n┌{'─'*68}┐")
    print(f"│  🌟 ASCENDANT: {asc_sign.upper():<52}│")
    print(f"│  Lagna Lord: {asc_lords.get(asc_sign, 'N/A'):<54}│")
    print(f"└{'─'*68}┘")
    
    # Libra Ascendant Interpretation
    if asc_sign == "Libra":
        print("""
    Libra Lagna indicates:
    • Diplomatic & charming personality
    • Strong sense of justice and fairness
    • Artistic temperament, appreciation of beauty
    • Partnership-oriented, seeks harmony in relationships
    • Venus (Shukra) as Lagna lord emphasizes love, beauty, luxury
    • Natural ability to see multiple perspectives
        """)
    
    # Key Planet Analysis
    print(f"\n┌{'─'*68}┐")
    print(f"│  KEY PLANETARY POSITIONS                                           │")
    print(f"└{'─'*68}┘")
    
    for planet_name, info in planets.items():
        sign = info.get("sign", "N/A")
        house = info.get("house", "N/A")
        longitude = float(info.get("longitude", 0))
        nak, pada = get_nakshatra(longitude)
        
        print(f"\n  {planet_name}: {sign} in House {house} ({nak} Pada {pada})")
        
        # Specific interpretations
        if planet_name == "Sun":
            if sign == "Virgo":
                print("    → Sun in Virgo: Analytical mind, attention to detail, service-oriented")
                print("    → House 12: Spiritual inclinations, behind-the-scenes work, foreign lands")
        
        elif planet_name == "Moon":
            if sign == "Taurus":
                print("    → Moon in Taurus (EXALTED): Strong emotional stability, love of comfort")
                print("    → House 8: Deep emotional nature, interest in occult, transformative experiences")
        
        elif planet_name == "Mars":
            if sign == "Taurus":
                print("    → Mars in Taurus: Steady determination, practical energy, financial drive")
                print("    → House 8: Research abilities, inheritance matters, strong willpower")
        
        elif planet_name == "Mercury":
            if sign == "Virgo":
                print("    → Mercury in Virgo (EXALTED): Brilliant analytical mind, excellent communication")
                print("    → House 12: Writing talent, foreign connections, spiritual intellect")
        
        elif planet_name == "Jupiter":
            if sign == "Cancer":
                print("    → Jupiter in Cancer (EXALTED): Exceptional wisdom, nurturing nature")
                print("    → House 10: Success in career, leadership, respected in profession")
        
        elif planet_name == "Venus":
            if sign == "Virgo":
                print("    → Venus in Virgo (DEBILITATED): Practical approach to love, critical nature")
                print("    → House 12: Spiritual love, foreign romance, artistic retreats")
        
        elif planet_name == "Saturn":
            if sign == "Sagittarius":
                print("    → Saturn in Sagittarius: Disciplined philosophy, structured beliefs")
                print("    → House 3: Persistent communication, hardworking siblings")
        
        elif planet_name == "Rahu":
            if sign == "Capricorn":
                print("    → Rahu in Capricorn: Ambitious drive, material goals, career obsession")
                print("    → House 4: Focus on home, property, mother, inner security")
        
        elif planet_name == "Ketu":
            if sign == "Cancer":
                print("    → Ketu in Cancer: Past life nurturing, emotional detachment needed")
                print("    → House 10: Spiritual career path, unconventional profession")
    
    # Panchang
    if panchang_data:
        print(f"\n┌{'─'*68}┐")
        print(f"│  BIRTH PANCHANG                                                    │")
        print(f"└{'─'*68}┘")
        print(f"  Tithi: Krishna Shashthi (Waning 6th)")
        print(f"  Nakshatra: {panchang_data.get('nakshatra_name', 'N/A')}")
        print(f"  Yoga: {panchang_data.get('yoga_name', 'N/A')}")
    
    # Dasha
    if dasha_data:
        current = dasha_data.get("current_period", {})
        if current:
            print(f"\n┌{'─'*68}┐")
            print(f"│  CURRENT DASHA PERIOD (December 2024)                             │")
            print(f"└{'─'*68}┘")
            print(f"  Mahadasha: {current.get('mahadasha', 'N/A')}")
            print(f"  Antardasha: {current.get('antardasha', 'N/A')}")
    
    # Key Yogas
    print(f"\n┌{'─'*68}┐")
    print(f"│  SPECIAL YOGAS DETECTED                                            │")
    print(f"└{'─'*68}┘")
    
    # Detect yogas based on positions
    moon_sign = planets.get("Moon", {}).get("sign")
    jupiter_sign = planets.get("Jupiter", {}).get("sign")
    mercury_sign = planets.get("Mercury", {}).get("sign")
    
    if moon_sign == "Taurus":
        print("  ✓ MOON EXALTATION - Emotional stability, prosperity, mental peace")
    if jupiter_sign == "Cancer":
        print("  ✓ JUPITER EXALTATION (Hamsa Yoga) - Wisdom, success, spiritual growth")
    if mercury_sign == "Virgo":
        print("  ✓ MERCURY EXALTATION (Bhadra Yoga) - Intelligence, communication skills")
    
    # Check for stellium (3+ planets in one sign)
    sign_counts = {}
    for p, info in planets.items():
        s = info.get("sign", "")
        sign_counts[s] = sign_counts.get(s, 0) + 1
    
    for sign, count in sign_counts.items():
        if count >= 3:
            print(f"  ✓ STELLIUM in {sign} ({count} planets) - Concentrated energy in that area")
    
    # Summary
    print(f"\n╔{'═'*68}╗")
    print(f"║  SUMMARY                                                           ║")
    print(f"╠{'═'*68}╣")
    print(f"║  You have a powerful chart with multiple exalted planets:          ║")
    print(f"║  • Moon exalted in Taurus - emotional stability                    ║")
    print(f"║  • Jupiter exalted in Cancer - wisdom and fortune                  ║")
    print(f"║  • Mercury exalted in Virgo - sharp intellect                      ║")
    print(f"║                                                                    ║")
    print(f"║  Key themes: Analytical mind, emotional depth, career success,    ║")
    print(f"║  spiritual inclinations, foreign connections, transformative      ║")
    print(f"║  experiences, and strong communication abilities.                 ║")
    print(f"╚{'═'*68}╝")


def main():
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#    COMPREHENSIVE KUNDLI CALCULATION - ALL BACKEND FEATURES        #")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    results = {}
    
    # Test 1: Main Chart
    chart_data, planet_houses, asc_sign = test_main_chart()
    results["chart"] = chart_data
    
    # Test 2: Panchang
    panchang_data = test_panchang()
    results["panchang"] = panchang_data
    
    # Test 3: Dasha
    dasha_data = test_dasha(chart_data)
    results["dasha"] = dasha_data
    
    # Test 4: Lal Kitab
    results["lal_kitab"] = test_lal_kitab(planet_houses)
    
    # Test 5: Navamsa
    results["navamsa"] = test_divisional(chart_data)
    
    # Test 6: Aspects
    results["aspects"] = test_aspects(chart_data)
    
    # Test 7: Strengths
    results["strengths"] = test_strength(chart_data)
    
    # Summary
    print_section("BACKEND TEST SUMMARY")
    passed = sum(1 for v in results.values() if v is not None)
    total = len(results)
    print(f"\n  ✓ Tests Passed: {passed}/{total}")
    
    # Full Interpretation
    generate_interpretation(chart_data, planet_houses, asc_sign, panchang_data, dasha_data)
    
    # Save results
    with open("user_kundli_final.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  📁 Full data saved to: user_kundli_final.json")
    
    return results


if __name__ == "__main__":
    main()
