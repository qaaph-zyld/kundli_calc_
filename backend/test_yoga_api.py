"""Quick API test for Chandra yoga improvements"""
import requests
import json

# Test chart with potential Chandra yogas
test_data = {
    "date_time": "1990-10-09T08:10:00Z",
    "latitude": 44.5333,
    "longitude": 19.2333,
    "ayanamsa": 1,  # Lahiri
    "house_system": "W"  # Whole Sign
}

print("Testing Kundli calculation with Chandra yoga improvements...")
print(f"Request: {json.dumps(test_data, indent=2)}\n")

try:
    response = requests.post(
        "http://localhost:8000/api/v1/charts/calculate",
        json=test_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ API Response successful!")
        print(f"Status: {response.status_code}\n")
        
        # Check if yogas are present
        if "yogas" in result:
            yogas = result["yogas"]
            print(f"Total yogas detected: {len(yogas)}\n")
            
            # Look for Chandra yogas specifically
            chandra_yogas = [y for y in yogas if "Chandra" in y.get("category", "") or 
                            any(name in y.get("name", "") for name in ["Sunapha", "Anapha", "Durudhara"])]
            
            if chandra_yogas:
                print(f"Chandra yogas found: {len(chandra_yogas)}")
                for yoga in chandra_yogas:
                    print(f"\n  - {yoga.get('name', 'Unknown')}")
                    print(f"    Description: {yoga.get('description', 'N/A')}")
                    print(f"    Strength: {yoga.get('strength', 0)}")
                    print(f"    Planets: {yoga.get('planets_involved', [])}")
            else:
                print("No Chandra yogas detected in this chart.")
            
            # Sample a few other yogas
            print(f"\n\nSample of other yogas detected:")
            for yoga in yogas[:5]:
                print(f"  - {yoga.get('name', 'Unknown')} (strength: {yoga.get('strength', 0)})")
        else:
            print("⚠️ No yogas in response")
            print(f"Response keys: {list(result.keys())}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error: API server not running on localhost:8000")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
