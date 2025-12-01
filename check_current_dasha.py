"""Check current running dasha for the user"""
import requests
from datetime import datetime

r = requests.post('http://127.0.0.1:8000/api/v1/dasha/vimshottari', 
                  json={'birth_date': '1990-10-09T07:10:00', 'moon_longitude': 57.73})
data = r.json()

now = datetime(2024, 12, 1)
periods = data.get('periods', [])

print("VIMSHOTTARI DASHA SEQUENCE:")
print("="*60)
for p in periods:
    planet = p['planet']
    start = p['start_date'][:10]
    end = p['end_date'][:10]
    duration = p['duration_years']
    print(f"  {planet:10} {start} to {end} ({duration:.1f} years)")

# Find current period
print("\n" + "="*60)
print("CURRENT RUNNING DASHA (December 2024):")
print("="*60)

for p in periods:
    start = datetime.fromisoformat(p['start_date'].replace('Z', ''))
    end = datetime.fromisoformat(p['end_date'].replace('Z', ''))
    if start <= now <= end:
        print(f"\n  MAHADASHA: {p['planet']}")
        print(f"    Period: {p['start_date'][:10]} to {p['end_date'][:10]}")
        
        for a in p.get('antardasha', []):
            a_start = datetime.fromisoformat(a['start_date'].replace('Z', ''))
            a_end = datetime.fromisoformat(a['end_date'].replace('Z', ''))
            if a_start <= now <= a_end:
                print(f"\n  ANTARDASHA: {a['planet']}")
                print(f"    Period: {a['start_date'][:10]} to {a['end_date'][:10]}")
                
                for pr in a.get('pratyantardasha', []):
                    pr_start = datetime.fromisoformat(pr['start_date'].replace('Z', ''))
                    pr_end = datetime.fromisoformat(pr['end_date'].replace('Z', ''))
                    if pr_start <= now <= pr_end:
                        print(f"\n  PRATYANTARDASHA: {pr['planet']}")
                        print(f"    Period: {pr['start_date'][:10]} to {pr['end_date'][:10]}")
                break
        break
