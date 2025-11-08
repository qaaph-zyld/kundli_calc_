"""
Correct Chart Calculation - User's Actual Requirements
Whole Sign Houses + Lahiri Ayanamsa ONLY
"""

import requests
import json

API_BASE = "http://localhost:8000/api/v1"

def calculate_correct_chart():
    """Calculate with CORRECT settings: Whole Sign + Lahiri"""
    
    # CORRECT settings per user requirement
    birth_data = {
        "date_time": "1990-10-09T09:10:00",
        "latitude": 44.5333,
        "longitude": 19.2333,
        "altitude": 0,
        "ayanamsa_type": "LAHIRI",  # ONLY Lahiri
        "house_system": "W"  # W = Whole Sign (not Placidus)
    }
    
    print("=" * 60)
    print("CORRECT CHART CALCULATION")
    print("=" * 60)
    print("\nSettings:")
    print(f"  Ayanamsa: LAHIRI ONLY")
    print(f"  House System: WHOLE SIGN ONLY")
    print(f"  Date: October 9, 1990, 09:10 AM")
    print(f"  Location: Loznica, Serbia (44.53°N, 19.23°E)")
    print()
    
    response = requests.post(
        f"{API_BASE}/charts/calculate",
        json=birth_data,
        timeout=15
    )
    
    if response.status_code != 200:
        print(f"ERROR: {response.status_code}")
        print(response.text)
        return None
    
    chart = response.json()
    
    # Parse ascendant
    asc_deg = float(chart['houses']['ascendant'])
    asc_sign_num = int(asc_deg / 30)
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    asc_sign = signs[asc_sign_num]
    asc_in_sign = asc_deg % 30
    
    print("ASCENDANT (Lagna):")
    print(f"  {asc_sign} - {asc_in_sign:.2f}° (Total: {asc_deg:.2f}°)")
    print()
    
    # Calculate house positions with Whole Sign
    print("PLANETARY POSITIONS (Whole Sign Houses):")
    print("-" * 60)
    
    for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
        if planet in chart['planetary_positions']:
            pos = chart['planetary_positions'][planet]
            lon = float(pos['longitude'])
            sign_num = int(lon / 30)
            sign = signs[sign_num]
            deg = lon % 30
            
            # Whole Sign house = sign relative to ascendant sign
            house = ((sign_num - asc_sign_num) % 12) + 1
            
            speed = float(pos.get('speed', 0))
            retro = " (R)" if speed < 0 and planet not in ['Rahu', 'Ketu'] else ""
            
            print(f"{planet:10s}: {sign:12s} {deg:6.2f}° | House {house:2d}{retro}")
    
    # Save result
    with open('correct_chart.json', 'w') as f:
        json.dump(chart, f, indent=2, default=str)
    
    print()
    print("Full data saved to: correct_chart.json")
    
    return chart

if __name__ == "__main__":
    calculate_correct_chart()
