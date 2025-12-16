"""Test Yogini and Ashtottari Dasha endpoints"""
import requests
import json

base = 'http://127.0.0.1:8000/api/v1'
moon_lon = 58.33  # User's Moon at Mrigashira

# Test Yogini Dasha
print('=== YOGINI DASHA ===')
r = requests.post(f'{base}/dashas/yogini', json={
    'birth_datetime': '1990-10-09T08:10:00Z',
    'moon_longitude': moon_lon
}, timeout=30)
if r.status_code == 200:
    d = r.json()
    print('Success:', d.get('success'))
    data = d.get('data', {})
    print('Balance:', data.get('balance_at_birth', 'N/A'))
    periods = data.get('periods', data.get('dasha_sequence', []))[:3]
    for p in periods:
        yogini = p.get('yogini', p.get('planet', 'Unknown'))
        print(f"  {yogini}: {p.get('start', 'N/A')} to {p.get('end', 'N/A')}")
else:
    print('Error:', r.status_code, r.text[:200])

# Test Ashtottari Dasha
print('\n=== ASHTOTTARI DASHA ===')
r = requests.post(f'{base}/dashas/ashtottari', json={
    'birth_datetime': '1990-10-09T08:10:00Z',
    'moon_longitude': moon_lon
}, timeout=30)
if r.status_code == 200:
    d = r.json()
    print('Success:', d.get('success'))
    data = d.get('data', {})
    periods = data.get('periods', data.get('dasha_sequence', []))[:3]
    for p in periods:
        print(f"  {p.get('planet', 'Unknown')}: {p.get('start', 'N/A')} to {p.get('end', 'N/A')}")
else:
    print('Error:', r.status_code, r.text[:200])

# Test Ashtakavarga
print('\n=== ASHTAKAVARGA ===')
# Need planet house positions for Ashtakavarga
planet_houses = {
    'Sun': 12,
    'Moon': 8,
    'Mars': 8,
    'Mercury': 12,
    'Jupiter': 10,
    'Venus': 12,
    'Saturn': 3
}
r = requests.post(f'{base}/ashtakavarga/calculate', json={
    'planet_positions': planet_houses
}, timeout=30)
if r.status_code == 200:
    d = r.json()
    sav = d.get('sarvashtakavarga', {})
    print('Sarvashtakavarga totals by house:')
    for house, bindus in sorted(sav.items(), key=lambda x: int(x[0])):
        print(f"  House {house}: {bindus} bindus")
    print('Strong houses:', d.get('strong_houses', []))
else:
    print('Error:', r.status_code, r.text[:200])
