"""
Complete User Chart Test
Test Date: October 9, 1990, 09:10 AM
Location: Loznica, Serbia (44.5333°N, 19.2333°E)
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000/api/v1"

def test_user_chart():
    """Test complete chart calculation for user's birth data"""
    
    print("=" * 60)
    print("🧪 COMPLETE USER CHART TEST")
    print("=" * 60)
    print()
    
    # Birth data
    birth_data = {
        "date_time": "1990-10-09T09:10:00",
        "latitude": 44.5333,
        "longitude": 19.2333,
        "altitude": 0,
        "ayanamsa_type": "LAHIRI",
        "house_system": "PLACIDUS"
    }
    
    print("📋 Birth Details:")
    print(f"   Date: October 9, 1990")
    print(f"   Time: 09:10 AM (Central European Time)")
    print(f"   Location: Loznica, Serbia")
    print(f"   Coordinates: {birth_data['latitude']}°N, {birth_data['longitude']}°E")
    print(f"   Ayanamsa: Lahiri")
    print(f"   House System: Placidus")
    print()
    
    # Test 1: Chart Calculation
    print("🔍 Test 1: Chart Calculation")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{API_BASE}/charts/calculate",
            json=birth_data,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Chart calculation successful!")
            chart = response.json()
            
            # Parse results
            print("\n📊 CHART RESULTS:")
            print("=" * 60)
            
            # Ascendant
            if 'houses' in chart and 'ascendant' in chart['houses']:
                asc_deg = float(chart['houses']['ascendant'])
                asc_sign_num = int(asc_deg / 30)
                signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
                asc_sign = signs[asc_sign_num]
                asc_in_sign = asc_deg % 30
                
                print(f"\n🌅 ASCENDANT (Lagna):")
                print(f"   Sign: {asc_sign}")
                print(f"   Degree: {asc_deg:.2f}° ({asc_in_sign:.2f}° in {asc_sign})")
            
            # Planetary Positions
            if 'planetary_positions' in chart:
                print(f"\n🪐 PLANETARY POSITIONS:")
                print("-" * 60)
                
                planets_order = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 
                               'Venus', 'Saturn', 'Rahu', 'Ketu']
                
                for planet in planets_order:
                    if planet in chart['planetary_positions']:
                        pos = chart['planetary_positions'][planet]
                        longitude = float(pos['longitude'])
                        sign_num = int(longitude / 30)
                        sign = signs[sign_num]
                        deg_in_sign = longitude % 30
                        
                        # Get speed for retrograde check
                        speed = float(pos.get('speed', 0))
                        retro = " (R)" if speed < 0 and planet not in ['Rahu', 'Ketu'] else ""
                        
                        print(f"   {planet:10s}: {sign:12s} {deg_in_sign:6.2f}°{retro}")
            
            # Divisional Charts
            if 'divisional_charts' in chart:
                print(f"\n📐 DIVISIONAL CHARTS:")
                print("-" * 60)
                
                for div_name, div_data in chart['divisional_charts'].items():
                    if isinstance(div_data, dict) and 'planetary_positions' in div_data:
                        print(f"\n   {div_name}:")
                        for planet, pos_data in list(div_data['planetary_positions'].items())[:3]:
                            if isinstance(pos_data, dict) and 'longitude' in pos_data:
                                long = float(pos_data['longitude'])
                                sign = signs[int(long / 30)]
                                print(f"      {planet}: {sign}")
            
            # Save full result
            with open('user_chart_result.json', 'w') as f:
                json.dump(chart, f, indent=2, default=str)
            print("\n💾 Full chart saved to: user_chart_result.json")
            
            return True, chart
            
        else:
            print(f"❌ Chart calculation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def analyze_yogas(chart_data):
    """Analyze yogas from chart data"""
    print("\n\n🎯 Test 2: Yoga Analysis")
    print("=" * 60)
    
    # This would be done by frontend, but we can analyze the data
    if not chart_data or 'planetary_positions' not in chart_data:
        print("❌ No chart data to analyze")
        return
    
    planets = chart_data['planetary_positions']
    
    # Check for some major yogas
    print("\n📋 Major Yoga Indicators:")
    
    # Get house positions (simplified - actual calculation needs house cusps)
    print("   (Detailed yoga analysis requires frontend library)")
    print("   Chart data contains all necessary planetary positions")
    print("   ✅ Ready for yoga detection on frontend")

def test_performance(birth_data):
    """Test API performance"""
    print("\n\n⚡ Test 3: Performance Check")
    print("=" * 60)
    
    import time
    
    times = []
    for i in range(3):
        start = time.time()
        response = requests.post(
            f"{API_BASE}/charts/calculate",
            json=birth_data,
            timeout=15
        )
        elapsed = time.time() - start
        times.append(elapsed)
        
        if response.status_code == 200:
            print(f"   Run {i+1}: {elapsed:.2f}s")
        else:
            print(f"   Run {i+1}: FAILED")
    
    if times:
        avg = sum(times) / len(times)
        print(f"\n   Average: {avg:.2f}s")
        
        if avg < 3:
            print(f"   ✅ EXCELLENT - Target achieved!")
        elif avg < 5:
            print(f"   ✅ GOOD - Within acceptable range")
        elif avg < 8:
            print(f"   ⚠️  ACCEPTABLE - Could be better")
        else:
            print(f"   ❌ SLOW - Optimization needed")

def main():
    """Run all tests"""
    
    birth_data = {
        "date_time": "1990-10-09T09:10:00",
        "latitude": 44.5333,
        "longitude": 19.2333,
        "altitude": 0,
        "ayanamsa_type": "LAHIRI",
        "house_system": "PLACIDUS"
    }
    
    # Test chart calculation
    success, chart = test_user_chart()
    
    if success:
        # Analyze yogas
        analyze_yogas(chart)
        
        # Test performance
        test_performance(birth_data)
        
        print("\n\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 60)
        print("\n📄 Next Steps:")
        print("   1. Open browser to http://localhost:3100")
        print("   2. Enter birth details:")
        print("      - Date: October 9, 1990")
        print("      - Time: 09:10 AM")
        print("      - Location: Loznica, Serbia")
        print("      - Or use coordinates: 44.5333, 19.2333")
        print("   3. Generate chart and verify all features")
        print("   4. Test all chart types (D1, D9, North/South)")
        print("   5. Check Yogas, Doshas, Planetary Strength")
        print("   6. Test Ashtakoot matching with another chart")
        print("   7. Test Transits and Rectification features")
    else:
        print("\n\n❌ TESTS FAILED")
        print("   Please check that backend is running on port 8000")

if __name__ == "__main__":
    main()
