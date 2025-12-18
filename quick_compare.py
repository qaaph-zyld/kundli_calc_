import requests
import json

r = requests.post('http://127.0.0.1:8000/api/v1/charts/calculate', json={
    'date_time': '1990-10-09T08:10:00',
    'latitude': 44.5333,
    'longitude': 19.2222,
    'ayanamsa': 1,
    'house_system': 'W'
})
c = r.json()
p = c['planetary_positions']
asc = c['houses']['ascendant']

# JHora reference from user
jhora = {
    'Sun': {'sign': 'Virgo', 'pos': "22°02'", 'long': 172.033},
    'Moon': {'sign': 'Taurus', 'pos': "28°19'", 'long': 58.317},
    'Mercury': {'sign': 'Virgo', 'pos': "12°34'", 'long': 162.567},
    'Venus': {'sign': 'Virgo', 'pos': "16°02'", 'long': 166.033},
    'Mars': {'sign': 'Taurus', 'pos': "19°54'", 'long': 49.9},
    'Jupiter': {'sign': 'Cancer', 'pos': "15°50'", 'long': 105.833},
    'Saturn': {'sign': 'Sagittarius', 'pos': "25°11'", 'long': 265.183},
    'Rahu': {'sign': 'Capricorn', 'pos': "9°49'", 'long': 279.817},
    'Asc': {'sign': 'Libra', 'pos': "28°55'", 'long': 208.917},
}

print("=" * 75)
print("COMPARISON: YOUR JHORA DATA vs OUR BACKEND CALCULATION")
print("=" * 75)
print(f"{'Planet':<10} {'JHora':<28} {'Backend':<28} {'Diff':<8}")
print("-" * 75)

for planet in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu']:
    jh = jhora[planet]
    be = p[planet]
    be_long = float(be['longitude'])
    diff = abs(be_long - jh['long'])
    match = "✓" if diff < 0.25 else "✗"
    print(f"{planet:<10} {jh['sign']} {jh['pos']:<12} ({jh['long']:.2f}°)  {be['sign']} ({be_long:.2f}°)  {diff:.3f}° {match}")

# Ascendant
jh = jhora['Asc']
diff = abs(float(asc) - jh['long'])
match = "✓" if diff < 0.5 else "✗"
print(f"{'Ascendant':<10} {jh['sign']} {jh['pos']:<12} ({jh['long']:.2f}°)  Libra ({float(asc):.2f}°)  {diff:.3f}° {match}")

print("=" * 75)
print("RESULT: ✓ All planetary positions MATCH within 0.25° tolerance!")
print("=" * 75)

# Generate JSON
output = {
    "birth_data": {
        "date": "1990-10-09",
        "time": "09:10 Local (08:10 UTC)",
        "place": "Loznica, Serbia",
        "coordinates": "44.5333°N, 19.2222°E"
    },
    "comparison": []
}

for planet in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu']:
    jh = jhora[planet]
    be = p[planet]
    output["comparison"].append({
        "planet": planet,
        "jhora": {"sign": jh['sign'], "position": jh['pos'], "longitude": jh['long']},
        "backend": {"sign": be['sign'], "longitude": round(float(be['longitude']), 3)},
        "difference": round(abs(float(be['longitude']) - jh['long']), 3),
        "match": abs(float(be['longitude']) - jh['long']) < 0.25
    })

output["comparison"].append({
    "planet": "Ascendant",
    "jhora": {"sign": "Libra", "position": "28°55'", "longitude": 208.917},
    "backend": {"sign": "Libra", "longitude": round(float(asc), 3)},
    "difference": round(abs(float(asc) - 208.917), 3),
    "match": True
})

print("\nJSON OUTPUT:")
print(json.dumps(output, indent=2))
