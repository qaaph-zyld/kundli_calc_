"""
Test Data Flow - Verify API Returns Complete Data for Frontend
"""

import requests
import json
import time

API_BASE = "http://localhost:8000/api/v1"

def test_api_data_structure():
    """Test if API returns house and sign_num for yoga detection"""
    
    print("="*60)
    print("DATA FLOW VERIFICATION TEST")
    print("="*60)
    print()
    
    birth_data = {
        "date_time": "1990-10-09T09:10:00",
        "latitude": 44.5333,
        "longitude": 19.2333,
        "altitude": 0,
        "ayanamsa_type": "LAHIRI",
        "house_system": "W"
    }
    
    print("⏱️  Testing API response time...")
    start = time.time()
    
    try:
        response = requests.post(
            f"{API_BASE}/charts/calculate",
            json=birth_data,
            timeout=15
        )
        
        elapsed = time.time() - start
        print(f"   Response time: {elapsed:.2f}s")
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return False
        
        chart = response.json()
        
        # Check data structure
        print("\n📊 Data Structure Check:")
        print("-"*60)
        
        if "planetary_positions" not in chart:
            print("❌ FAIL: No planetary_positions in response")
            return False
        
        # Check first planet
        planets = chart["planetary_positions"]
        first_planet = list(planets.keys())[0]
        planet_data = planets[first_planet]
        
        print(f"\n🔍 Checking {first_planet} data structure:")
        print(f"   Fields present: {list(planet_data.keys())}")
        
        required_fields = ["longitude", "sign_num", "sign", "house"]
        missing_fields = []
        
        for field in required_fields:
            if field in planet_data:
                print(f"   ✅ {field}: {planet_data[field]}")
            else:
                print(f"   ❌ MISSING: {field}")
                missing_fields.append(field)
        
        if missing_fields:
            print(f"\n❌ CRITICAL: Missing fields: {missing_fields}")
            print("   Yoga detection will NOT work without these fields")
            return False
        
        # Verify house numbers make sense
        print("\n🏠 House Number Verification:")
        print("-"*60)
        
        asc_deg = float(chart["houses"]["ascendant"])
        asc_sign = int(asc_deg / 30)
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        print(f"Ascendant: {signs[asc_sign]} (sign {asc_sign})")
        print()
        
        house_errors = []
        
        for pname in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            if pname in planets:
                pdata = planets[pname]
                sign_num = pdata["sign_num"]
                house = pdata["house"]
                
                # Calculate expected house (Whole Sign)
                expected_house = ((sign_num - asc_sign) % 12) + 1
                
                status = "✅" if house == expected_house else "❌"
                print(f"{status} {pname:10s}: {pdata['sign']:12s} | House {house} (expected {expected_house})")
                
                if house != expected_house:
                    house_errors.append(pname)
        
        if house_errors:
            print(f"\n❌ House calculation errors for: {house_errors}")
            return False
        
        # Test yoga detection readiness
        print("\n🎯 Yoga Detection Readiness:")
        print("-"*60)
        
        # Check if Budhaditya Yoga (Sun + Mercury same sign) can be detected
        sun_sign = planets.get("Sun", {}).get("sign_num")
        mercury_sign = planets.get("Mercury", {}).get("sign_num")
        
        if sun_sign == mercury_sign:
            print(f"✅ Can detect Budhaditya Yoga:")
            print(f"   Sun in {planets['Sun']['sign']} (sign {sun_sign})")
            print(f"   Mercury in {planets['Mercury']['sign']} (sign {mercury_sign})")
        
        # Check if Chandra-Mangal (Moon + Mars same sign) can be detected
        moon_sign = planets.get("Moon", {}).get("sign_num")
        mars_sign = planets.get("Mars", {}).get("sign_num")
        
        if moon_sign == mars_sign:
            print(f"✅ Can detect Chandra-Mangal Yoga:")
            print(f"   Moon in {planets['Moon']['sign']} (sign {moon_sign})")
            print(f"   Mars in {planets['Mars']['sign']} (sign {mars_sign})")
        
        # Check if Mangal Dosha (Mars in 7th) can be detected
        mars_house = planets.get("Mars", {}).get("house")
        if mars_house == 7:
            print(f"✅ Can detect Mangal Dosha:")
            print(f"   Mars in house {mars_house}")
        
        print("\n" + "="*60)
        print("✅ ALL DATA FLOW TESTS PASSED")
        print("="*60)
        print("\nConclusion:")
        print("  - API returns complete data structure ✓")
        print("  - House numbers calculated correctly ✓")
        print("  - Sign information included ✓")
        print("  - Frontend yoga detection will work ✓")
        print(f"  - Response time: {elapsed:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api_data_structure()
    
    if not success:
        print("\n⚠️  RESTART BACKEND SERVER AND RUN AGAIN")
        print("   cd backend")
        print("   uvicorn app.main:app --reload --port 8000")
    else:
        print("\n✅ Ready for frontend integration")
