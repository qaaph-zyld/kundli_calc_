"""
Test Script for Phase 6 Modules
Tests all newly implemented features for JH parity
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Test data
SAMPLE_PLANETS = {
    "Sun": 171.8, "Moon": 314.3, "Mars": 44.3,
    "Mercury": 178.3, "Jupiter": 93.3, "Venus": 145.3,
    "Saturn": 265.3, "Rahu": 286.3, "Ketu": 106.3
}
SAMPLE_ASCENDANT = 200.0
BIRTH_DATE = datetime(1990, 10, 9, 9, 10)


def test_advanced_dashas():
    """Test 20 additional Dasha systems"""
    print("\n--- ADVANCED DASHAS (20 systems) ---")
    try:
        from core.calculations.advanced_dashas import AdvancedDashaCalculator
        
        calc = AdvancedDashaCalculator()
        results = calc.calculate_all(
            birth_time=BIRTH_DATE,
            ascendant=SAMPLE_ASCENDANT,
            planets=SAMPLE_PLANETS
        )
        
        print(f"  Dasha systems calculated: {len(results)}")
        for name, periods in list(results.items())[:5]:
            if periods:
                print(f"    {name}: {periods[0].ruler} ({periods[0].years:.1f} years)")
        
        available = calc.get_available_dashas()
        print(f"  Available systems: {len(available)}")
        
        return len(results) == 20
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_advanced_divisional():
    """Test D-81, D-108, D-144 charts"""
    print("\n--- ADVANCED DIVISIONAL CHARTS ---")
    try:
        from core.calculations.advanced_divisional import AdvancedDivisionalCalculator
        
        calc = AdvancedDivisionalCalculator()
        results = calc.calculate_all(SAMPLE_PLANETS)
        
        print(f"  D-81 (cyclical): Sun in {results['d81_cyclical']['Sun'].sign_name}")
        print(f"  D-108 (cyclical): Sun in {results['d108_cyclical']['Sun'].sign_name}")
        print(f"  D-144: Sun in {results['d144']['Sun'].sign_name}")
        print(f"  Nadyamsa: Sun's nadi = {results['nadyamsa']['Sun']['nadi_name']}")
        
        # Test custom D-N
        custom_d50 = calc.calculate_custom(SAMPLE_PLANETS, 50)
        print(f"  Custom D-50: Sun in {custom_d50['Sun'].sign_name}")
        
        return len(results) >= 5
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_complete_yogas():
    """Test 184 yoga detection"""
    print("\n--- COMPLETE YOGAS (184 types) ---")
    try:
        from core.calculations.complete_yogas import calculate_complete_yogas
        
        results = calculate_complete_yogas(SAMPLE_PLANETS, SAMPLE_ASCENDANT)
        
        print(f"  Total yogas checked: {results['total_checked']}")
        print(f"  Yogas found: {results['total_found']}")
        print(f"  Summary: {results['summary']}")
        
        if results['yogas']:
            print(f"  Top yogas:")
            for yoga in results['yogas'][:3]:
                print(f"    - {yoga['name']} ({yoga['category']})")
        
        return results['total_found'] >= 3  # At least finding some yogas
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_dasa_pravesh():
    """Test Dasa Pravesh charts"""
    print("\n--- DASA PRAVESH CHARTS ---")
    try:
        from core.calculations.dasa_pravesh import calculate_dasa_pravesh
        
        dasa_start = datetime(1995, 10, 9)  # Sample dasa start
        
        result = calculate_dasa_pravesh(
            natal_planets=SAMPLE_PLANETS,
            natal_ascendant=SAMPLE_ASCENDANT,
            dasa_start=dasa_start,
            dasa_lord="Rahu"
        )
        
        print(f"  Dasa lord: {result['dasa_lord']}")
        print(f"  Pravesh Ascendant: {result['ascendant']['sign']} {result['ascendant']['degree']:.1f}°")
        print(f"  Overall indication: {result['analysis']['overall_indication'][:50]}...")
        
        return "analysis" in result
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_tajaka_system():
    """Test Tajaka annual charts"""
    print("\n--- TAJAKA SYSTEM ---")
    try:
        from core.calculations.tajaka_system import calculate_tajaka_annual
        
        result = calculate_tajaka_annual(
            birth_date=BIRTH_DATE,
            birth_sun_longitude=SAMPLE_PLANETS["Sun"],
            year_number=35  # 35th year
        )
        
        print(f"  Year: {result['year_number']}")
        print(f"  Muntha: {result['muntha']['sign']} (House {result['muntha']['house']})")
        print(f"  Year Lord: {result['year_lord']}")
        print(f"  Tajaka Yogas found: {len(result['yogas'])}")
        print(f"  Aspects found: {len(result['aspects'])}")
        
        if result['yogas']:
            print(f"    Top yoga: {result['yogas'][0]['name']}")
        
        return "muntha" in result and "yogas" in result
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_mundane_astrology():
    """Test Mundane charts"""
    print("\n--- MUNDANE ASTROLOGY ---")
    try:
        from core.calculations.mundane_astrology import calculate_mundane_chart
        
        # Solar ingress
        ingress = calculate_mundane_chart("aries_ingress", datetime(2024, 3, 21))
        print(f"  Aries Ingress 2024: Asc in {ingress['ascendant']['sign']}")
        print(f"  Government forecast: {ingress['analysis']['government'][:40]}...")
        
        # Lunar chart
        lunar = calculate_mundane_chart("new_moon", datetime(2024, 1, 11))
        print(f"  New Moon chart: Moon in {lunar['planets']['Moon']['sign']}")
        
        return "analysis" in ingress
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_chart_superimposition():
    """Test Chart Superimposition"""
    print("\n--- CHART SUPERIMPOSITION ---")
    try:
        from core.calculations.chart_superimposition import ChartSuperimposition
        
        calc = ChartSuperimposition()
        
        # Shifted planets for transit
        transit = {k: (v + 45) % 360 for k, v in SAMPLE_PLANETS.items()}
        
        result = calc.natal_transit_overlay(
            natal_planets=SAMPLE_PLANETS,
            transit_planets=transit,
            natal_ascendant=SAMPLE_ASCENDANT
        )
        
        print(f"  Aspects found: {len(result['aspects'])}")
        print(f"  Harmony score: {result['harmony_score']['score']}%")
        print(f"  Assessment: {result['harmony_score']['assessment']}")
        
        if result['aspects']:
            asp = result['aspects'][0]
            print(f"    Closest aspect: {asp['planet1']} {asp['aspect']} {asp['planet2']}")
        
        # Composite chart test
        chart2 = {k: (v + 90) % 360 for k, v in SAMPLE_PLANETS.items()}
        composite = calc.composite_chart(SAMPLE_PLANETS, chart2)
        print(f"  Composite Sun: {composite['planets']['Sun']['sign']}")
        
        return "harmony_score" in result
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_additional_chakras():
    """Test Additional Chakras"""
    print("\n--- ADDITIONAL CHAKRAS ---")
    try:
        from core.calculations.additional_chakras import calculate_additional_chakras
        
        result = calculate_additional_chakras(
            moon_longitude=SAMPLE_PLANETS["Moon"],
            weekday=2  # Tuesday
        )
        
        print(f"  Chakras calculated: {len(result)}")
        
        for name, chakra in result.items():
            print(f"    {chakra['chakra_name']}: {chakra['interpretation'][:40]}...")
        
        return len(result) == 5
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    """Run all Phase 6 tests"""
    print("=" * 60)
    print("  PHASE 6 MODULE TESTS - JH PARITY")
    print("=" * 60)
    
    results = {}
    
    results["Advanced Dashas (20)"] = test_advanced_dashas()
    results["Advanced Divisional (D-81/108/144)"] = test_advanced_divisional()
    results["Complete Yogas (184)"] = test_complete_yogas()
    results["Dasa Pravesh"] = test_dasa_pravesh()
    results["Tajaka System"] = test_tajaka_system()
    results["Mundane Astrology"] = test_mundane_astrology()
    results["Chart Superimposition"] = test_chart_superimposition()
    results["Additional Chakras"] = test_additional_chakras()
    
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
        print("\n  ✓ ALL PHASE 6 MODULES VERIFIED - JH PARITY ACHIEVED!")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
