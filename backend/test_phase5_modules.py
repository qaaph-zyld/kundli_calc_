"""
Test Script for Phase 5 Modules
Tests all newly implemented features
"""

import sys
import os
from datetime import datetime

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test data (Oct 9, 1990, Loznica, Serbia)
TEST_DATA = {
    "name": "Test User",
    "day": 9,
    "month": 10,
    "year": 1990,
    "hour": 9,
    "minute": 10,
    "latitude": 44.5333,
    "longitude": 19.2261
}

# Sample planetary positions (sidereal/Lahiri)
SAMPLE_PLANETS = {
    "Sun": 171.8,
    "Moon": 314.3,
    "Mars": 44.3,
    "Mercury": 178.3,
    "Jupiter": 93.3,
    "Venus": 145.3,
    "Saturn": 265.3,
    "Rahu": 286.3,
    "Ketu": 106.3
}

SAMPLE_ASCENDANT = 200.0  # Libra

def print_result(name: str, success: bool, details: str = ""):
    """Print test result"""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"  {name}: {status}")
    if details and not success:
        print(f"    Details: {details}")


def test_birth_rectification():
    """Test Birth Time Rectification"""
    print("\n--- BIRTH TIME RECTIFICATION ---")
    try:
        from core.calculations.birth_rectification import rectify_birth_time
        
        birth_time = datetime(1990, 10, 9, 9, 10)
        
        result = rectify_birth_time(
            approximate_time=birth_time,
            latitude=TEST_DATA["latitude"],
            longitude=TEST_DATA["longitude"],
            moon_longitude=SAMPLE_PLANETS["Moon"],
            ascendant=SAMPLE_ASCENDANT
        )
        
        print(f"  Original time: {result['original_time']}")
        print(f"  Recommended time: {result['recommended_time']}")
        print(f"  Methods used: {list(result['methods'].keys())}")
        print(f"  Confidence: {result['overall_confidence']:.1%}")
        
        print_result("Birth Rectification", True)
        return True
    except Exception as e:
        print_result("Birth Rectification", False, str(e))
        return False


def test_sahamas():
    """Test Sahamas (Arabic Parts)"""
    print("\n--- SAHAMAS (36 Arabic Parts) ---")
    try:
        from core.calculations.sahamas import calculate_sahamas
        
        result = calculate_sahamas(
            planets=SAMPLE_PLANETS,
            ascendant=SAMPLE_ASCENDANT,
            sun_longitude=SAMPLE_PLANETS["Sun"]
        )
        
        print(f"  Total sahamas calculated: {result['total_count']}")
        print(f"  Is day birth: {result['is_day_birth']}")
        print(f"  Key sahamas:")
        for key, val in result['key_sahamas'].items():
            if val:
                print(f"    {key}: {val.get('sign', 'N/A')} {val.get('degree', 'N/A')}°")
        
        print_result("Sahamas", result['total_count'] == 36)
        return True
    except Exception as e:
        print_result("Sahamas", False, str(e))
        return False


def test_critical_points():
    """Test Critical Points (Mrityu Bhaga, etc.)"""
    print("\n--- CRITICAL POINTS ---")
    try:
        from core.calculations.critical_points import analyze_all_critical_points
        
        result = analyze_all_critical_points(
            planets=SAMPLE_PLANETS,
            moon_longitude=SAMPLE_PLANETS["Moon"]
        )
        
        print(f"  Mrityu Bhaga afflicted: {result['summary']['mrityu_bhaga_count']}")
        print(f"  Gandanta planets: {result['summary']['gandanta_count']}")
        print(f"  Vargottama planets: {result['summary']['vargottama_count']}")
        print(f"  64th Navamsa lord: {result['64th_navamsa']['64th_navamsa_lord']}")
        print(f"  22nd Drekkana lord: {result['22nd_drekkana']['22nd_drekkana_lord']}")
        
        print_result("Critical Points", True)
        return True
    except Exception as e:
        print_result("Critical Points", False, str(e))
        return False


def test_latta():
    """Test Latta System"""
    print("\n--- LATTA (Planetary Kick) ---")
    try:
        from core.calculations.latta_system import analyze_latta
        
        result = analyze_latta(
            planets=SAMPLE_PLANETS,
            moon_longitude=SAMPLE_PLANETS["Moon"]
        )
        
        birth_latta = result['birth_latta']
        print(f"  Birth nakshatra: {birth_latta['birth_nakshatra']}")
        print(f"  Afflicted by latta: {birth_latta['is_afflicted']}")
        if birth_latta['afflicting_planets']:
            print(f"  Afflicting planets: {[p['planet'] for p in birth_latta['afflicting_planets']]}")
        
        all_lattas = result['all_lattas']
        print(f"  Lattas calculated: {len(all_lattas['lattas_by_planet'])}")
        
        print_result("Latta System", True)
        return True
    except Exception as e:
        print_result("Latta System", False, str(e))
        return False


def test_transit_search():
    """Test Transit Search"""
    print("\n--- TRANSIT SEARCH ---")
    try:
        from core.calculations.transit_search import search_transits
        
        # Use current positions as transit
        transit_planets = {k: (v + 30) % 360 for k, v in SAMPLE_PLANETS.items()}
        
        result = search_transits(
            natal_planets=SAMPLE_PLANETS,
            transit_planets=transit_planets,
            natal_ascendant=SAMPLE_ASCENDANT,
            search_type="major",
            days_ahead=365
        )
        
        print(f"  Total events found: {result['total_events']}")
        if result['events']:
            print(f"  First event: {result['events'][0]}")
        
        print_result("Transit Search", True)
        return True
    except Exception as e:
        print_result("Transit Search", False, str(e))
        return False


def test_numerology():
    """Test Numerology"""
    print("\n--- NUMEROLOGY ---")
    try:
        from core.calculations.numerology import calculate_numerology
        
        result = calculate_numerology(
            name=TEST_DATA["name"],
            day=TEST_DATA["day"],
            month=TEST_DATA["month"],
            year=TEST_DATA["year"]
        )
        
        print(f"  Birth Number: {result['birth_number']['number']} ({result['birth_number']['name']})")
        print(f"  Destiny Number: {result['destiny_number']['number']} ({result['destiny_number']['name']})")
        print(f"  Name Number: {result['name_number']['number']} ({result['name_number']['name']})")
        print(f"  Soul Number: {result['soul_number']['number']}")
        print(f"  Lucky Numbers: {result['lucky_numbers']['primary']}")
        print(f"  Lucky Colors: {result['lucky_colors']}")
        
        print_result("Numerology", True)
        return True
    except Exception as e:
        print_result("Numerology", False, str(e))
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("  PHASE 5 MODULE TESTS")
    print("=" * 60)
    
    print(f"\nTest Data: {TEST_DATA['name']}")
    print(f"Birth: {TEST_DATA['day']}/{TEST_DATA['month']}/{TEST_DATA['year']}")
    
    results = {}
    
    results["Birth Rectification"] = test_birth_rectification()
    results["Sahamas"] = test_sahamas()
    results["Critical Points"] = test_critical_points()
    results["Latta System"] = test_latta()
    results["Transit Search"] = test_transit_search()
    results["Numerology"] = test_numerology()
    
    # Summary
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {name}: {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  ✓ ALL PHASE 5 MODULES VERIFIED")
    else:
        print(f"\n  ⚠ {total - passed} test(s) failed")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
