import requests
import json

response = requests.post(
    "http://localhost:8000/api/v1/charts/calculate",
    json={
        "date_time": "1990-10-09T09:10:00",
        "latitude": 44.5333,
        "longitude": 19.2333,
        "altitude": 0,
        "ayanamsa_type": "LAHIRI",
        "house_system": "W"
    }
)

print("Status:", response.status_code)
print("\nRaw Response:")
print(json.dumps(response.json(), indent=2, default=str))

# Check Sun specifically
data = response.json()
if 'planetary_positions' in data and 'Sun' in data['planetary_positions']:
    print("\nSun data:")
    print(json.dumps(data['planetary_positions']['Sun'], indent=2, default=str))
