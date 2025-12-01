"""
Comprehensive Kundli Calculation Test
Date: October 9, 1990
Time: 09:10 AM
Location: Loznica, Serbia (44.5333°N, 19.2222°E)
"""

import requests
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000/api/v1"

# Birth Details
BIRTH_DATA = {
    "datetime": "1990-10-09T09:10:00Z",
    "latitude": 44.5333,
    "longitude": 19.2222,
    "timezone": "Europe/Belgrade",
    "ayanamsa": "lahiri",
    "house_system": "whole_sign"
}

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_chart_calculation():
    """Test 1: Main Chart Calculation"""
    print_section("TEST 1: MAIN CHART CALCULATION")
    
    response = requests.post(f"{API_BASE}/calculate", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Chart calculated successfully")
        
        # Planets
        if "planets" in data:
            print("\n--- PLANETARY POSITIONS ---")
            for planet, info in data["planets"].items():
                if isinstance(info, dict):
                    sign = info.get("sign", "N/A")
                    degree = info.get("longitude", info.get("degree", 0))
                    retro = " (R)" if info.get("retrograde", False) else ""
                    nakshatra = info.get("nakshatra", {})
                    nak_name = nakshatra.get("name", "N/A") if isinstance(nakshatra, dict) else "N/A"
                    print(f"  {planet:12}: {sign:12} {degree:6.2f}°{retro:4} | Nakshatra: {nak_name}")
        
        # Houses
        if "houses" in data:
            print("\n--- HOUSE CUSPS ---")
            houses = data["houses"]
            if isinstance(houses, dict):
                for key, value in houses.items():
                    if key == "ascendant":
                        asc_deg = value if isinstance(value, (int, float)) else value.get("degree", 0)
                        asc_sign_num = int(asc_deg // 30) + 1
                        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
                        asc_sign = signs[asc_sign_num - 1] if 1 <= asc_sign_num <= 12 else "N/A"
                        print(f"  Ascendant: {asc_sign} ({asc_deg:.2f}°)")
                    elif key == "cusps" and isinstance(value, list):
                        print("  House Cusps:", [f"{c:.1f}°" for c in value[:12]])
        
        return data
    else:
        print(f"✗ Error: {response.status_code} - {response.text}")
        return None

def test_lal_kitab(chart_data):
    """Test 2: Lal Kitab Analysis"""
    print_section("TEST 2: LAL KITAB ANALYSIS")
    
    response = requests.post(f"{API_BASE}/lal-kitab/analyze", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Lal Kitab analysis calculated")
        
        # Planet placements
        if "planet_placements" in data:
            print("\n--- LAL KITAB PLANET PLACEMENTS ---")
            for planet, info in data["planet_placements"].items():
                house = info.get("house", "N/A")
                strength = info.get("strength", "N/A")
                print(f"  {planet:12}: House {house:2} | Strength: {strength}")
        
        # Remedies
        if "remedies" in data:
            print("\n--- LAL KITAB REMEDIES ---")
            for i, remedy in enumerate(data["remedies"][:5], 1):
                planet = remedy.get("planet", "N/A")
                remedy_text = remedy.get("remedy", "N/A")[:60]
                print(f"  {i}. [{planet}] {remedy_text}...")
        
        # Debts
        if "debts" in data:
            print("\n--- ANCESTRAL DEBTS (Rin) ---")
            for debt in data["debts"]:
                print(f"  - {debt.get('type', 'N/A')}: {debt.get('description', 'N/A')[:50]}...")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_kp_system():
    """Test 3: KP System Analysis"""
    print_section("TEST 3: KP SYSTEM (KRISHNAMURTI PADDHATI)")
    
    response = requests.post(f"{API_BASE}/kp/analyze", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ KP System analysis calculated")
        
        # Sub-lord table
        if "sub_lords" in data:
            print("\n--- KP SUB-LORD TABLE ---")
            for cusp, info in list(data["sub_lords"].items())[:6]:
                sign_lord = info.get("sign_lord", "N/A")
                star_lord = info.get("star_lord", "N/A")
                sub_lord = info.get("sub_lord", "N/A")
                print(f"  Cusp {cusp:3}: Sign Lord: {sign_lord:8} Star Lord: {star_lord:8} Sub Lord: {sub_lord:8}")
        
        # Significators
        if "significators" in data:
            print("\n--- HOUSE SIGNIFICATORS ---")
            for house, planets in list(data["significators"].items())[:6]:
                print(f"  House {house:2}: {', '.join(planets) if planets else 'None'}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_dashas():
    """Test 4: Vimshottari Dasha"""
    print_section("TEST 4: VIMSHOTTARI DASHA PERIODS")
    
    dasha_request = {
        **BIRTH_DATA,
        "years_ahead": 10
    }
    
    response = requests.post(f"{API_BASE}/dashas/vimshottari", json=dasha_request)
    if response.status_code == 200:
        data = response.json()
        print("✓ Dasha periods calculated")
        
        if "current_dasha" in data:
            cd = data["current_dasha"]
            print(f"\n--- CURRENT DASHA ---")
            print(f"  Mahadasha: {cd.get('mahadasha', 'N/A')}")
            print(f"  Antardasha: {cd.get('antardasha', 'N/A')}")
            print(f"  Pratyantardasha: {cd.get('pratyantardasha', 'N/A')}")
        
        if "mahadasha_sequence" in data:
            print("\n--- MAHADASHA SEQUENCE ---")
            for md in data["mahadasha_sequence"][:5]:
                planet = md.get("planet", "N/A")
                start = md.get("start_date", "N/A")[:10]
                end = md.get("end_date", "N/A")[:10]
                print(f"  {planet:8}: {start} to {end}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_yogas(chart_data):
    """Test 5: Yoga Detection"""
    print_section("TEST 5: YOGA DETECTION")
    
    response = requests.post(f"{API_BASE}/yogas/analyze", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Yogas analyzed")
        
        yogas = data.get("yogas", [])
        print(f"\n--- YOGAS DETECTED ({len(yogas)}) ---")
        
        beneficial = [y for y in yogas if y.get("type") == "beneficial"]
        malefic = [y for y in yogas if y.get("type") == "malefic"]
        
        print(f"\n  BENEFICIAL YOGAS ({len(beneficial)}):")
        for yoga in beneficial[:5]:
            name = yoga.get("name", "N/A")
            strength = yoga.get("strength", "N/A")
            print(f"    ✓ {name} ({strength})")
        
        print(f"\n  CHALLENGING YOGAS ({len(malefic)}):")
        for yoga in malefic[:5]:
            name = yoga.get("name", "N/A")
            strength = yoga.get("strength", "N/A")
            print(f"    ✗ {name} ({strength})")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_doshas():
    """Test 6: Dosha Analysis"""
    print_section("TEST 6: DOSHA ANALYSIS")
    
    response = requests.post(f"{API_BASE}/doshas/analyze", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Doshas analyzed")
        
        # Manglik
        if "manglik" in data:
            m = data["manglik"]
            print(f"\n--- MANGLIK DOSHA ---")
            print(f"  Present: {m.get('is_manglik', False)}")
            print(f"  Intensity: {m.get('intensity', 'N/A')}")
            if m.get("cancellation"):
                print(f"  Cancellation: {m.get('cancellation_reason', 'N/A')}")
        
        # Kaal Sarp
        if "kaal_sarp" in data:
            ks = data["kaal_sarp"]
            print(f"\n--- KAAL SARP DOSHA ---")
            print(f"  Present: {ks.get('is_present', False)}")
            if ks.get("is_present"):
                print(f"  Type: {ks.get('type', 'N/A')}")
        
        # Pitra Dosha
        if "pitra" in data:
            p = data["pitra"]
            print(f"\n--- PITRA DOSHA ---")
            print(f"  Present: {p.get('is_present', False)}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_shadbala():
    """Test 7: Shadbala (Planetary Strength)"""
    print_section("TEST 7: SHADBALA (PLANETARY STRENGTH)")
    
    response = requests.post(f"{API_BASE}/shadbala/calculate", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Shadbala calculated")
        
        if "strengths" in data:
            print("\n--- PLANETARY STRENGTH (Rupas) ---")
            for planet, strength in data["strengths"].items():
                total = strength.get("total", 0) if isinstance(strength, dict) else strength
                required = strength.get("required", 1) if isinstance(strength, dict) else 1
                ratio = total / required if required > 0 else 0
                status = "Strong" if ratio >= 1 else "Weak"
                print(f"  {planet:10}: {total:.2f} Rupas ({status})")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_transits():
    """Test 8: Current Transits"""
    print_section("TEST 8: CURRENT TRANSITS")
    
    transit_request = {
        **BIRTH_DATA,
        "transit_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    response = requests.post(f"{API_BASE}/transits/current", json=transit_request)
    if response.status_code == 200:
        data = response.json()
        print("✓ Transit positions calculated")
        
        if "transits" in data:
            print("\n--- CURRENT PLANETARY TRANSITS ---")
            for planet, info in data["transits"].items():
                sign = info.get("sign", "N/A")
                degree = info.get("longitude", 0)
                house = info.get("natal_house", "N/A")
                print(f"  {planet:10}: {sign:12} {degree:6.2f}° (transiting House {house})")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_muhurta():
    """Test 9: Muhurta Analysis"""
    print_section("TEST 9: PANCHANG / MUHURTA")
    
    response = requests.post(f"{API_BASE}/muhurta/panchang", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Panchang calculated")
        
        print("\n--- BIRTH PANCHANG ---")
        print(f"  Tithi: {data.get('tithi', {}).get('name', 'N/A')}")
        print(f"  Nakshatra: {data.get('nakshatra', {}).get('name', 'N/A')}")
        print(f"  Yoga: {data.get('yoga', {}).get('name', 'N/A')}")
        print(f"  Karana: {data.get('karana', {}).get('name', 'N/A')}")
        print(f"  Vara (Day): {data.get('vara', 'N/A')}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_ashtakavarga():
    """Test 10: Ashtakavarga"""
    print_section("TEST 10: ASHTAKAVARGA")
    
    response = requests.post(f"{API_BASE}/ashtakavarga/calculate", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Ashtakavarga calculated")
        
        if "sarvashtakavarga" in data:
            sav = data["sarvashtakavarga"]
            print("\n--- SARVASHTAKAVARGA (Total Points per Sign) ---")
            signs = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
            if isinstance(sav, list):
                for i, points in enumerate(sav[:12]):
                    print(f"  {signs[i]:3}: {points} points")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_divisional_charts():
    """Test 11: Divisional Charts"""
    print_section("TEST 11: DIVISIONAL CHARTS (D9 NAVAMSA)")
    
    div_request = {
        **BIRTH_DATA,
        "division": 9
    }
    
    response = requests.post(f"{API_BASE}/divisional/calculate", json=div_request)
    if response.status_code == 200:
        data = response.json()
        print("✓ Navamsa (D9) calculated")
        
        if "planets" in data:
            print("\n--- NAVAMSA POSITIONS ---")
            for planet, info in data["planets"].items():
                sign = info.get("sign", "N/A")
                print(f"  {planet:12}: {sign}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_aspects():
    """Test 12: Planetary Aspects"""
    print_section("TEST 12: PLANETARY ASPECTS")
    
    response = requests.post(f"{API_BASE}/aspects/calculate", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Aspects calculated")
        
        if "aspects" in data:
            print("\n--- MAJOR ASPECTS ---")
            for aspect in data["aspects"][:10]:
                p1 = aspect.get("planet1", "N/A")
                p2 = aspect.get("planet2", "N/A")
                asp_type = aspect.get("aspect", "N/A")
                orb = aspect.get("orb", 0)
                print(f"  {p1:10} {asp_type:12} {p2:10} (orb: {orb:.1f}°)")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None

def test_special_lagnas():
    """Test 13: Special Lagnas"""
    print_section("TEST 13: SPECIAL LAGNAS")
    
    response = requests.post(f"{API_BASE}/lagnas/special", json=BIRTH_DATA)
    if response.status_code == 200:
        data = response.json()
        print("✓ Special Lagnas calculated")
        
        print("\n--- SPECIAL ASCENDANTS ---")
        for lagna_type, info in data.items():
            if isinstance(info, dict):
                sign = info.get("sign", "N/A")
                degree = info.get("degree", 0)
                print(f"  {lagna_type:20}: {sign:12} ({degree:.2f}°)")
            else:
                print(f"  {lagna_type:20}: {info}")
        
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        return None


def main():
    print("\n" + "#"*70)
    print("#  COMPREHENSIVE KUNDLI CALCULATION TEST")
    print("#  Birth: October 9, 1990, 09:10 AM")
    print("#  Location: Loznica, Serbia (44.5333°N, 19.2222°E)")
    print("#  Ayanamsa: Lahiri | House System: Whole Sign")
    print("#"*70)
    
    results = {}
    
    # Test 1: Main Chart
    chart_data = test_chart_calculation()
    results["chart"] = chart_data
    
    # Test 2: Lal Kitab
    results["lal_kitab"] = test_lal_kitab(chart_data)
    
    # Test 3: KP System
    results["kp"] = test_kp_system()
    
    # Test 4: Dashas
    results["dashas"] = test_dashas()
    
    # Test 5: Yogas
    results["yogas"] = test_yogas(chart_data)
    
    # Test 6: Doshas
    results["doshas"] = test_doshas()
    
    # Test 7: Shadbala
    results["shadbala"] = test_shadbala()
    
    # Test 8: Transits
    results["transits"] = test_transits()
    
    # Test 9: Muhurta
    results["muhurta"] = test_muhurta()
    
    # Test 10: Ashtakavarga
    results["ashtakavarga"] = test_ashtakavarga()
    
    # Test 11: Divisional Charts
    results["divisional"] = test_divisional_charts()
    
    # Test 12: Aspects
    results["aspects"] = test_aspects()
    
    # Test 13: Special Lagnas
    results["lagnas"] = test_special_lagnas()
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v is not None)
    total = len(results)
    print(f"\n  Tests Passed: {passed}/{total}")
    print(f"  Tests Failed: {total - passed}/{total}")
    
    # Save full results
    with open("user_kundli_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Full results saved to: user_kundli_results.json")
    
    return results


if __name__ == "__main__":
    main()
