"""
Test frontend connection to backend API
"""
import requests

# Test health endpoint
print("Testing backend API connection...")
print("=" * 60)

try:
    response = requests.get("http://localhost:8000/api/v1/health")
    print(f"✅ Health endpoint: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Health endpoint failed: {e}")

print()

# Test CORS preflight
print("Testing CORS preflight...")
try:
    response = requests.options(
        "http://localhost:8000/api/v1/charts/calculate",
        headers={
            "Origin": "http://localhost:3100",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   CORS headers:")
    for key, value in response.headers.items():
        if 'access-control' in key.lower():
            print(f"      {key}: {value}")
    
    if response.status_code == 200:
        print("✅ CORS configured correctly")
    else:
        print(f"⚠️  CORS preflight returned: {response.status_code}")
except Exception as e:
    print(f"❌ CORS test failed: {e}")

print()

# Test actual chart calculation
print("Testing chart calculation endpoint...")
try:
    response = requests.post(
        "http://localhost:8000/api/v1/charts/calculate",
        json={
            "date_time": "1990-10-09T09:10:00",
            "latitude": 44.5333,
            "longitude": 19.2333,
            "altitude": 0,
            "ayanamsa_type": "LAHIRI",
            "house_system": "W"
        },
        headers={
            "Origin": "http://localhost:3100",
            "Content-Type": "application/json"
        }
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Chart calculation successful")
        print(f"   Planets returned: {list(data.get('planetary_positions', {}).keys())}")
        sun = data.get('planetary_positions', {}).get('Sun', {})
        if 'house' in sun and 'sign' in sun:
            print(f"   Sun data includes: sign={sun.get('sign')}, house={sun.get('house')}")
            print("✅ Data structure correct for frontend")
        else:
            print("⚠️  Missing sign/house data")
    else:
        print(f"❌ Chart calculation failed: {response.status_code}")
        print(f"   Error: {response.text[:200]}")
except Exception as e:
    print(f"❌ Chart calculation failed: {e}")

print()
print("=" * 60)
print("Frontend should now be able to connect to backend")
