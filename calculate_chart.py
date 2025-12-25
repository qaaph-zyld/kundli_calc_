#!/usr/bin/env python3
"""Direct chart calculation for analysis"""
from datetime import datetime
import sys
sys.path.insert(0, 'backend')

from app.core.calculations.astronomical import AstronomicalCalculator
from app.core.calculations.dasha_system import VimshottariDasha
from app.core.calculations.houses import HouseSystem
from app.core.calculations.dignities import PlanetaryDignities
from app.core.calculations.shadbala import ShadbalaSystem
from app.core.calculations.yoga_calculator import YogaCalculator
import json

# Birth details: 9th October 1990, 09:10 AM, Loznica Serbia
dt = datetime(1990, 10, 9, 9, 10)
lat, lon = 44.5333, 19.2333
timezone_offset = 1  # UTC+1 for Serbia

calc = AstronomicalCalculator()
jd = calc.calculate_julian_day(dt, timezone_offset)

# Calculate planetary positions (Lahiri ayanamsa)
planets = calc.calculate_planetary_positions(jd, 'lahiri')

# Calculate ascendant (Whole Sign houses)
asc_data = calc.calculate_ascendant(jd, lat, lon, 'W', 'lahiri')

# Calculate houses
house_system = HouseSystem()
houses = house_system.calculate_houses(asc_data['longitude'], 'W')

# Calculate Vimshottari Dasha
dasha_calc = VimshottariDasha()
dasha_info = dasha_calc.calculate_dasha_at_birth(dt, planets['Moon']['longitude'])

# Calculate dignities
dignity_calc = PlanetaryDignities()
dignities = {}
for planet, data in planets.items():
    if planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
        dignities[planet] = dignity_calc.calculate_dignity(planet, data['longitude'])

print("="*80)
print("BIRTH CHART: 9 October 1990, 09:10 AM, Loznica Serbia (44.53°N, 19.23°E)")
print("="*80)

print("\n### PLANETARY POSITIONS (Lahiri Ayanamsa) ###")
for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
    if planet in planets:
        p = planets[planet]
        deg_in_sign = p['longitude'] % 30
        print(f"{planet:10s}: {p['longitude']:7.2f}° | {p['sign']:12s} {deg_in_sign:5.2f}° | House {p.get('house', 'N/A')}")

print(f"\n### ASCENDANT (LAGNA) ###")
print(f"Ascendant: {asc_data['longitude']:.2f}° in {asc_data['sign']}")

print(f"\n### VIMSHOTTARI DASHA AT BIRTH ###")
print(f"Birth Nakshatra: {dasha_info['birth_nakshatra']} ({['Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra','Punarvasu','Pushya','Ashlesha','Magha','Purva Phalguni','Uttara Phalguni','Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha','Mula','Purva Ashadha','Uttara Ashadha','Shravana','Dhanishta','Shatabhisha','Purva Bhadrapada','Uttara Bhadrapada','Revati'][dasha_info['birth_nakshatra']-1]})")
print(f"Balance at Birth: {dasha_info['balance_at_birth']*100:.1f}% of {dasha_info['dasha_sequence'][0]['planet']} Mahadasha")
print(f"Current Mahadasha: {dasha_info['dasha_sequence'][0]['planet']} ({dasha_info['dasha_sequence'][0]['duration_years']:.2f} years remaining)")
print(f"Next Mahadasha: {dasha_info['dasha_sequence'][1]['planet']}")

print(f"\n### PLANETARY DIGNITIES ###")
for planet, dignity in dignities.items():
    status = dignity['status']
    print(f"{planet:10s}: {status:15s} (in {planets[planet]['sign']})")

print("\n" + "="*80)
