"""
Comprehensive Kundli Calculation Test V2
Date: October 9, 1990
Time: 09:10 AM
Location: Loznica, Serbia (44.5333°N, 19.2222°E)
Timezone: Europe/Belgrade (UTC+1, with DST UTC+2 in October 1990)
"""

import requests
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000/api/v1"

# Birth Details - October 9, 1990 was in DST (CEST = UTC+2)
# 09:10 AM local time = 07:10 UTC
BIRTH_DATETIME_UTC = "1990-10-09T07:10:00"
LATITUDE = 44.5333
LONGITUDE = 19.2222

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_main_chart():
    """Test 1: Main Chart Calculation"""
    print_section("TEST 1: MAIN CHART CALCULATION (Rasi Chart)")
    
    payload = {
        "date_time": BIRTH_DATETIME_UTC,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "ayanamsa": 1,  # 1=Lahiri, 2=Raman, 3=KP
        "house_system": "W"  # W=Whole Sign
    }
    
    response = requests.post(f"{API_BASE}/charts/calculate", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✓ Chart calculated successfully")
        
        # Planets
        planets = data.get("planets", {})
        print("\n--- PLANETARY POSITIONS (Sidereal/Lahiri) ---")
        
        sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        planet_houses = {}
        
        for planet, info in planets.items():
            if isinstance(info, dict):
                longitude = info.get("longitude", 0)
                sign_num = int(longitude // 30)
                sign = sign_names[sign_num] if 0 <= sign_num < 12 else "Unknown"
                degree_in_sign = longitude % 30
                retro = " (R)" if info.get("is_retrograde", False) else ""
                nakshatra = info.get("nakshatra", "")
                
                # Store house position (1-indexed)
                planet_houses[planet] = sign_num + 1
                
                print(f"  {planet:12}: {sign:12} {degree_in_sign:6.2f}°{retro:4} | Nakshatra: {nakshatra}")
        
        # Houses/Ascendant
        houses = data.get("houses", {})
        print("\n--- ASCENDANT & HOUSES ---")
        
        asc = houses.get("ascendant", 0)
        if isinstance(asc, dict):
            asc_deg = asc.get("longitude", asc.get("degree", 0))
        else:
            asc_deg = float(asc) if asc else 0
            
        asc_sign_num = int(asc_deg // 30)
        asc_sign = sign_names[asc_sign_num] if 0 <= asc_sign_num < 12 else "Unknown"
        asc_deg_in_sign = asc_deg % 30
        
        print(f"  Ascendant: {asc_sign} {asc_deg_in_sign:.2f}° (House 1)")
        
        # Calculate planet houses from ascendant
        print("\n--- PLANETS IN HOUSES (from Ascendant) ---")
        for planet, info in planets.items():
            if isinstance(info, dict):
                longitude = info.get("longitude", 0)
                planet_sign = int(longitude // 30)
                house = ((planet_sign - asc_sign_num) % 12) + 1
                planet_houses[planet] = house
                print(f"  {planet:12}: House {house}")
        
        return data, planet_houses, asc_sign
    else:
        print(f"✗ Error: {response.status_code} - {response.text[:200]}")
        return None, {}, None

def test_panchang():
    """Test 2: Panchang (Tithi, Nakshatra, Yoga, Karana)"""
    print_section("TEST 2: PANCHANG / BIRTH TITHI")
    
    payload = {
        "date_time": BIRTH_DATETIME_UTC
    }
    
    response = requests.post(f"{API_BASE}/panchang/calculate", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✓ Panchang calculated")
        
        # Tithi
        tithi_num = data.get("tithi_number", 0)
        tithi_names = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
        ]
        paksha = "Shukla" if tithi_num <= 15 else "Krishna"
        tithi_idx = (tithi_num - 1) % 15
        tithi_name = tithi_names[tithi_idx] if 0 <= tithi_idx < 15 else f"Tithi {tithi_num}"
        
        print(f"\n  Tithi: {paksha} {tithi_name} ({tithi_num})")
        print(f"  Nakshatra: {data.get('nakshatra_name', 'N/A')} (Pada {data.get('nakshatra_pada', 'N/A')})")
        print(f"  Yoga: {data.get('yoga_name', 'N/A')}")
        print(f"  Karana: {data.get('karana_number', 'N/A')}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_dasha():
    """Test 3: Vimshottari Dasha"""
    print_section("TEST 3: VIMSHOTTARI DASHA")
    
    # Need Moon longitude for dasha calculation
    chart_payload = {
        "date_time": BIRTH_DATETIME_UTC,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "ayanamsa": 1,
        "house_system": "W"
    }
    
    chart_response = requests.post(f"{API_BASE}/charts/calculate", json=chart_payload)
    if chart_response.status_code != 200:
        print("✗ Could not get chart for dasha")
        return None
    
    chart_data = chart_response.json()
    moon_long = chart_data.get("planets", {}).get("Moon", {}).get("longitude", 0)
    
    payload = {
        "birth_datetime": BIRTH_DATETIME_UTC,
        "moon_longitude": moon_long,
        "planet_longitudes": {
            p: info.get("longitude", 0) 
            for p, info in chart_data.get("planets", {}).items() 
            if isinstance(info, dict)
        }
    }
    
    response = requests.post(f"{API_BASE}/dasha/vimshottari", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✓ Dasha calculated")
        
        print("\n--- MAHADASHA SEQUENCE ---")
        for md in data.get("mahadasha_periods", [])[:6]:
            planet = md.get("planet", "N/A")
            start = md.get("start", "")[:10] if md.get("start") else "N/A"
            end = md.get("end", "")[:10] if md.get("end") else "N/A"
            print(f"  {planet:10}: {start} to {end}")
        
        # Current dasha
        current = data.get("current_period", {})
        if current:
            print(f"\n--- CURRENT DASHA (as of today) ---")
            print(f"  Mahadasha: {current.get('mahadasha', 'N/A')}")
            print(f"  Antardasha: {current.get('antardasha', 'N/A')}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code} - {response.text[:200]}")
        return None

def test_lal_kitab(planet_houses):
    """Test 4: Lal Kitab Analysis"""
    print_section("TEST 4: LAL KITAB ANALYSIS")
    
    if not planet_houses:
        print("✗ No planet houses data available")
        return None
    
    # Lal Kitab expects planet names with specific format
    lk_houses = {}
    for planet, house in planet_houses.items():
        # Map planet names
        name_map = {
            "Sun": "Sun", "Moon": "Moon", "Mars": "Mars", 
            "Mercury": "Mercury", "Jupiter": "Jupiter", "Venus": "Venus",
            "Saturn": "Saturn", "Rahu": "Rahu", "Ketu": "Ketu",
            "Mean Node": "Rahu", "True Node": "Rahu"
        }
        if planet in name_map:
            lk_houses[name_map[planet]] = house
    
    # Make sure we have Ketu if we have Rahu
    if "Rahu" in lk_houses and "Ketu" not in lk_houses:
        lk_houses["Ketu"] = ((lk_houses["Rahu"] + 5) % 12) + 1
    
    payload = {"planet_houses": lk_houses}
    
    response = requests.post(f"{API_BASE}/lal-kitab/analyze", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✓ Lal Kitab analysis completed")
        
        # Planet effects
        if "planet_analysis" in data:
            print("\n--- LAL KITAB PLANET EFFECTS ---")
            for planet, analysis in list(data["planet_analysis"].items())[:5]:
                effect = analysis.get("effect", "N/A")
                print(f"  {planet}: {effect[:60]}...")
        
        # Karmic Debts
        if "karmic_debts" in data:
            print("\n--- KARMIC DEBTS (Rin) ---")
            for debt in data["karmic_debts"][:3]:
                print(f"  • {debt.get('type', 'N/A')}: {debt.get('description', 'N/A')[:50]}...")
        
        # Remedies
        if "priority_remedies" in data:
            print("\n--- PRIORITY REMEDIES (Upay) ---")
            for i, remedy in enumerate(data["priority_remedies"][:5], 1):
                planet = remedy.get("planet", "N/A")
                upay = remedy.get("remedy", "N/A")[:50]
                print(f"  {i}. [{planet}] {upay}...")
        
        return data
    else:
        print(f"✗ Error: {response.status_code} - {response.text[:200]}")
        return None

def test_divisional_d9():
    """Test 5: Navamsa (D9) Chart"""
    print_section("TEST 5: NAVAMSA (D9) CHART")
    
    # First get main chart
    chart_payload = {
        "date_time": BIRTH_DATETIME_UTC,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "ayanamsa": 1,
        "house_system": "W"
    }
    
    chart_response = requests.post(f"{API_BASE}/charts/calculate", json=chart_payload)
    if chart_response.status_code != 200:
        print(f"✗ Could not get chart: {chart_response.status_code}")
        return None
    
    chart_data = chart_response.json()
    asc = chart_data.get("houses", {}).get("ascendant", 0)
    asc_long = float(asc) if isinstance(asc, (int, float)) else asc.get("longitude", 0)
    
    planet_longitudes = {
        p: info.get("longitude", 0) 
        for p, info in chart_data.get("planets", {}).items() 
        if isinstance(info, dict)
    }
    
    payload = {
        "division": 9,
        "planet_longitudes": planet_longitudes,
        "ascendant_longitude": asc_long,
        "ayanamsa_value": 23.72  # Approximate Lahiri for 1990
    }
    
    response = requests.post(f"{API_BASE}/divisional/calculate", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✓ Navamsa calculated")
        
        sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        print("\n--- NAVAMSA POSITIONS ---")
        planets = data.get("planets", {})
        for planet, info in planets.items():
            if isinstance(info, dict):
                sign_num = info.get("sign", 0)
                sign = sign_names[sign_num] if 0 <= sign_num < 12 else "N/A"
                print(f"  {planet:12}: {sign}")
        
        # Navamsa ascendant
        nav_asc = data.get("ascendant", {})
        if nav_asc:
            nav_sign = nav_asc.get("sign", 0)
            print(f"\n  Navamsa Lagna: {sign_names[nav_sign] if 0 <= nav_sign < 12 else 'N/A'}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code} - {response.text[:200]}")
        return None

def test_debug_full_chart():
    """Test 6: Debug endpoint for full chart analysis"""
    print_section("TEST 6: FULL CHART DEBUG (Yogas, Aspects, Strength)")
    
    response = requests.get(f"{API_BASE}/debug/verify")
    if response.status_code == 200:
        data = response.json()
        print("✓ Debug data retrieved")
        
        # Show yogas if available
        yogas = data.get("yogas", [])
        if yogas:
            print(f"\n--- YOGAS ({len(yogas)} detected) ---")
            for yoga in yogas[:5]:
                print(f"  • {yoga.get('name', 'N/A')}: {yoga.get('description', 'N/A')[:40]}...")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def calculate_full_analysis(chart_data, planet_houses, asc_sign):
    """Generate complete Kundli interpretation"""
    print_section("COMPLETE KUNDLI INTERPRETATION")
    
    if not chart_data:
        print("No chart data available for interpretation")
        return
    
    sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    planets = chart_data.get("planets", {})
    
    # Ascendant Lord
    asc_lords = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    
    print(f"\n🔮 ASCENDANT: {asc_sign}")
    print(f"   Lagna Lord: {asc_lords.get(asc_sign, 'N/A')}")
    
    # Key planets
    print(f"\n🌞 SUN (Soul, Father, Authority)")
    sun = planets.get("Sun", {})
    if sun:
        sun_long = sun.get("longitude", 0)
        sun_sign = sign_names[int(sun_long // 30)]
        sun_house = planet_houses.get("Sun", "N/A")
        print(f"   Position: {sun_sign} in House {sun_house}")
    
    print(f"\n🌙 MOON (Mind, Mother, Emotions)")
    moon = planets.get("Moon", {})
    if moon:
        moon_long = moon.get("longitude", 0)
        moon_sign = sign_names[int(moon_long // 30)]
        moon_house = planet_houses.get("Moon", "N/A")
        moon_nak = moon.get("nakshatra", "N/A")
        print(f"   Position: {moon_sign} in House {moon_house}")
        print(f"   Nakshatra: {moon_nak}")
    
    print(f"\n♂️ MARS (Energy, Courage, Siblings)")
    mars = planets.get("Mars", {})
    if mars:
        mars_long = mars.get("longitude", 0)
        mars_sign = sign_names[int(mars_long // 30)]
        mars_house = planet_houses.get("Mars", "N/A")
        print(f"   Position: {mars_sign} in House {mars_house}")
    
    print(f"\n☿ MERCURY (Intelligence, Communication)")
    merc = planets.get("Mercury", {})
    if merc:
        merc_long = merc.get("longitude", 0)
        merc_sign = sign_names[int(merc_long // 30)]
        merc_house = planet_houses.get("Mercury", "N/A")
        print(f"   Position: {merc_sign} in House {merc_house}")
    
    print(f"\n♃ JUPITER (Wisdom, Fortune, Guru)")
    jup = planets.get("Jupiter", {})
    if jup:
        jup_long = jup.get("longitude", 0)
        jup_sign = sign_names[int(jup_long // 30)]
        jup_house = planet_houses.get("Jupiter", "N/A")
        print(f"   Position: {jup_sign} in House {jup_house}")
    
    print(f"\n♀ VENUS (Love, Beauty, Luxury)")
    ven = planets.get("Venus", {})
    if ven:
        ven_long = ven.get("longitude", 0)
        ven_sign = sign_names[int(ven_long // 30)]
        ven_house = planet_houses.get("Venus", "N/A")
        print(f"   Position: {ven_sign} in House {ven_house}")
    
    print(f"\n♄ SATURN (Discipline, Karma, Delays)")
    sat = planets.get("Saturn", {})
    if sat:
        sat_long = sat.get("longitude", 0)
        sat_sign = sign_names[int(sat_long // 30)]
        sat_house = planet_houses.get("Saturn", "N/A")
        retro = " (Retrograde)" if sat.get("is_retrograde") else ""
        print(f"   Position: {sat_sign} in House {sat_house}{retro}")
    
    print(f"\n☊ RAHU (Obsession, Material Desires)")
    rahu = planets.get("Rahu", planets.get("Mean Node", planets.get("True Node", {})))
    if rahu:
        rahu_long = rahu.get("longitude", 0)
        rahu_sign = sign_names[int(rahu_long // 30)]
        rahu_house = planet_houses.get("Rahu", planet_houses.get("Mean Node", "N/A"))
        print(f"   Position: {rahu_sign} in House {rahu_house}")
    
    print(f"\n☋ KETU (Spirituality, Past Life)")
    ketu = planets.get("Ketu", {})
    if ketu:
        ketu_long = ketu.get("longitude", 0)
        ketu_sign = sign_names[int(ketu_long // 30)]
        ketu_house = planet_houses.get("Ketu", "N/A")
        print(f"   Position: {ketu_sign} in House {ketu_house}")


def main():
    print("\n" + "#"*70)
    print("#  COMPREHENSIVE KUNDLI CALCULATION")
    print("#  Birth: October 9, 1990, 09:10 AM Local Time")
    print("#  Location: Loznica, Serbia (44.5333°N, 19.2222°E)")
    print("#  Ayanamsa: Lahiri | House System: Whole Sign")
    print("#"*70)
    
    results = {}
    
    # Test 1: Main Chart
    chart_data, planet_houses, asc_sign = test_main_chart()
    results["chart"] = chart_data
    
    # Test 2: Panchang
    results["panchang"] = test_panchang()
    
    # Test 3: Dasha
    results["dasha"] = test_dasha()
    
    # Test 4: Lal Kitab
    results["lal_kitab"] = test_lal_kitab(planet_houses)
    
    # Test 5: Navamsa
    results["navamsa"] = test_divisional_d9()
    
    # Test 6: Debug
    results["debug"] = test_debug_full_chart()
    
    # Full Interpretation
    calculate_full_analysis(chart_data, planet_houses, asc_sign)
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v is not None)
    total = len(results)
    print(f"\n  Backend Tests Passed: {passed}/{total}")
    
    # Save full results
    with open("user_kundli_complete.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"  Full results saved to: user_kundli_complete.json")
    
    return results


if __name__ == "__main__":
    main()
