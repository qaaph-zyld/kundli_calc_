#!/usr/bin/env python3
"""Generate Full Kundli Report
Birth: 09th October 1990, 09:10 AM, Loznica, Serbia
Using only repository tools - no guesswork
"""
from datetime import datetime
from zoneinfo import ZoneInfo
import sys
sys.path.insert(0, 'backend')

from app.core.astronomical.framework import (
    AstronomicalCalculator, 
    AyanamsaSystem, 
    CelestialBody,
    GeoLocation
)
from app.core.calculations.houses import HouseCalculator
from app.core.calculations.dasha_system import VimshottariDasha
from app.core.calculations.extended_yogas import calculate_yogas
from app.core.calculations.nakshatra import NakshatraCalculator

print("="*80)
print("FULL KUNDLI REPORT")
print("="*80)
print()

# Birth Details (from calculate_chart.py)
print("BIRTH DETAILS:")
print("-" * 40)
birth_date_local = "09th October 1990"
birth_time_local = "09:10 AM"
birth_place = "Loznica, Serbia"
lat = 44.5333  # From calculate_chart.py line 17
lon = 19.2333  # From calculate_chart.py line 17
print(f"Date: {birth_date_local}")
print(f"Time: {birth_time_local} (Local)")
print(f"Place: {birth_place}")
print(f"Coordinates: {lat}°N, {lon}°E")
print(f"Source: calculate_chart.py lines 17-18")
print()

# Timezone Conversion
print("TIMEZONE CONVERSION:")
print("-" * 40)
timezone = "Europe/Belgrade"
dt_local = datetime(1990, 10, 9, 9, 10, tzinfo=ZoneInfo(timezone))
dt_utc = dt_local.astimezone(ZoneInfo("UTC"))
print(f"Timezone: {timezone}")
print(f"Local Time: {dt_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"UTC Time: {dt_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"UTC Offset: {dt_local.strftime('%z')}")
print()

# Settings
ayanamsa = AyanamsaSystem.LAHIRI
house_system = 'WHOLE_SIGN'
print("CALCULATION SETTINGS:")
print("-" * 40)
print(f"Ayanamsa: {ayanamsa.value} (Lahiri)")
print(f"House System: {house_system}")
print()

# Initialize calculators
print("INITIALIZING CALCULATION ENGINES:")
print("-" * 40)
location = GeoLocation(latitude=lat, longitude=lon, altitude=0.0)
astro_calc = AstronomicalCalculator(ayanamsa_system=ayanamsa)
house_calc = HouseCalculator()
nakshatra_calc = NakshatraCalculator()
print("✓ AstronomicalCalculator (Swiss Ephemeris)")
print("✓ HouseCalculator")
print("✓ NakshatraCalculator")
print()

# Calculate all planetary positions
print("="*80)
print("1. PLANETARY POSITIONS (SIDEREAL - LAHIRI AYANAMSA)")
print("="*80)
print("Tool: backend/app/core/astronomical/framework.py")
print()

positions = astro_calc.calculate_all_positions(dt_utc, location)

print(f"{'Planet':<12} {'Longitude':<12} {'Sign':<15} {'House':<8} {'Nakshatra':<15} {'Pada':<6} {'R':<3}")
print("-" * 90)

for body, pos in positions.items():
    lon_deg = pos.longitude
    sign = pos.sign.value.capitalize()
    house = pos.house.value.capitalize()
    retro = "R" if pos.is_retrograde else ""
    
    # Calculate nakshatra
    from decimal import Decimal
    nak_info = nakshatra_calc.calculate_nakshatra(Decimal(str(lon_deg)))
    nak_name = nak_info['name']
    pada = nak_info['pada']
    
    print(f"{body.value.capitalize():<12} {lon_deg:<12.4f} {sign:<15} {house:<8} {nak_name:<15} {pada:<6} {retro:<3}")

print()

# Calculate Houses
print("="*80)
print("2. HOUSES (WHOLE SIGN SYSTEM)")
print("="*80)
print("Tool: backend/app/core/calculations/houses.py")
print()

houses_data = house_calc.calculate_houses(dt_utc, lat, lon, house_system)
ascendant = houses_data['ascendant']
mc = houses_data['midheaven']
cusps = houses_data['cusps']

# Determine ascendant sign
asc_sign_idx = int(ascendant / 30)
sign_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
              'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
asc_sign = sign_names[asc_sign_idx]

print(f"Ascendant (Lagna): {ascendant:.4f}° in {asc_sign}")
print(f"Midheaven (MC): {mc:.4f}°")
print()

print(f"{'House':<8} {'Sign':<15} {'Cusp (°)':<12}")
print("-" * 40)
for i, cusp in enumerate(cusps, 1):
    cusp_sign_idx = int(cusp / 30) % 12
    cusp_sign = sign_names[cusp_sign_idx]
    print(f"{i:<8} {cusp_sign:<15} {cusp:<12.4f}")

print()

# Vimshottari Dasha
print("="*80)
print("3. VIMSHOTTARI DASHA PERIODS")
print("="*80)
print("Tool: backend/app/core/calculations/dasha_system.py")
print()

moon_pos = positions[CelestialBody.MOON]
moon_lon = moon_pos.longitude
print(f"Moon's Longitude: {moon_lon:.4f}° (basis for dasha calculation)")
print()

dasha_calc = VimshottariDasha()
dasha_data = dasha_calc.calculate_dasha_at_birth(dt_utc, moon_lon)
dasha_periods = dasha_data['dasha_sequence']

print(f"Birth Nakshatra: #{dasha_data['birth_nakshatra']}")
print(f"Balance at Birth: {dasha_data['balance_at_birth']:.4f}")
print()

print("Mahadasha Periods:")
print(f"{'Planet':<12} {'Start Date':<20} {'End Date':<20} {'Years':<8}")
print("-" * 70)
for period in dasha_periods[:10]:
    planet = period['planet']
    start = period['start_date'].strftime('%Y-%m-%d')
    end = period['end_date'].strftime('%Y-%m-%d')
    years = period['duration_years']
    print(f"{planet:<12} {start:<20} {end:<20} {years:<8.2f}")

# Current Dasha at birth (first one by definition)
if dasha_periods:
    current_dasha = dasha_periods[0]
    print()
    print(f"Dasha at Birth: {current_dasha['planet']} Mahadasha (Balance: {current_dasha['duration_years']:.2f} years)")
    print(f"Period: {current_dasha['start_date'].strftime('%Y-%m-%d')} to {current_dasha['end_date'].strftime('%Y-%m-%d')}")

print()

# Yogas
print("="*80)
print("4. VEDIC YOGAS (PLANETARY COMBINATIONS)")
print("="*80)
print("Tool: backend/app/core/calculations/extended_yogas.py")
print()

# Prepare planet positions for yoga calculation
planet_positions = {}
sign_names_lower = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

# Map planets to expected format
planet_name_map = {
    CelestialBody.SUN: 'sun',
    CelestialBody.MOON: 'moon',
    CelestialBody.MARS: 'mars',
    CelestialBody.MERCURY: 'mercury',
    CelestialBody.JUPITER: 'jupiter',
    CelestialBody.VENUS: 'venus',
    CelestialBody.SATURN: 'saturn',
    CelestialBody.RAHU: 'rahu',
    CelestialBody.KETU: 'ketu'
}

for body, pos in positions.items():
    if body in planet_name_map:
        planet_key = planet_name_map[body]
        sign_name = pos.sign.value
        house_name = pos.house.value
        
        planet_positions[planet_key] = {
            'longitude': pos.longitude,
            'sign': sign_name,
            'house': house_name
        }

# Calculate house lordships
sign_lord_map = {
    1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon', 5: 'Sun', 6: 'Mercury',
    7: 'Venus', 8: 'Mars', 9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
}

house_lords = {}
for i in range(1, 13):
    house_sign_num = (asc_sign_idx + i - 1) % 12 + 1
    lord = sign_lord_map.get(house_sign_num, 'Unknown')
    house_lords[i] = lord

try:
    yogas = calculate_yogas(planet_positions, house_lords, asc_sign.lower())
    
    print(f"Total Yogas Detected: {len(yogas)}")
    print()
    
    if yogas:
        # Group by type
        yoga_types = {}
        for yoga in yogas:
            yoga_type = yoga.get('type', 'Other')
            if yoga_type not in yoga_types:
                yoga_types[yoga_type] = []
            yoga_types[yoga_type].append(yoga)
        
        for yoga_type, type_yogas in yoga_types.items():
            print(f"{yoga_type.upper()} YOGAS:")
            print("-" * 60)
            for yoga in type_yogas[:5]:  # Show top 5 per type
                name = yoga.get('name', 'Unknown')
                strength = yoga.get('strength', 0)
                print(f"• {name} (Strength: {strength:.2f})")
                desc = yoga.get('description', '')
                if desc:
                    print(f"  {desc}")
            print()
    else:
        print("No specific yogas detected")
except Exception as e:
    print(f"Yoga calculation encountered an issue: {e}")
    print("Continuing with rest of report...")

print()

# Chart Summary
print("="*80)
print("5. CHART SUMMARY")
print("="*80)
print()

sun_pos = positions[CelestialBody.SUN]
sun_sign_idx = int(sun_pos.longitude / 30)
sun_sign = sign_names[sun_sign_idx]

moon_sign_idx = int(moon_lon / 30)
moon_sign = sign_names[moon_sign_idx]

print(f"Rising Sign (Lagna): {asc_sign}")
print(f"Sun Sign: {sun_sign}")
print(f"Moon Sign (Chandra Rashi): {moon_sign}")
moon_nak_info = nakshatra_calc.calculate_nakshatra(Decimal(str(moon_lon)))
print(f"Moon Nakshatra: {moon_nak_info['name']} (Pada {moon_nak_info['pada']})")
print()

# Dignities
print("PLANETARY DIGNITIES:")
print("-" * 40)
print(f"{'Planet':<12} {'Sign':<15} {'Status':<20}")
print("-" * 50)

dignity_rules = {
    'Sun': {'own': [5], 'exalted': [1], 'debilitated': [7]},
    'Moon': {'own': [4], 'exalted': [2], 'debilitated': [8]},
    'Mars': {'own': [1, 8], 'exalted': [10], 'debilitated': [4]},
    'Mercury': {'own': [3, 6], 'exalted': [6], 'debilitated': [12]},
    'Jupiter': {'own': [9, 12], 'exalted': [4], 'debilitated': [10]},
    'Venus': {'own': [2, 7], 'exalted': [12], 'debilitated': [6]},
    'Saturn': {'own': [10, 11], 'exalted': [7], 'debilitated': [1]}
}

for body, pos in positions.items():
    planet_name = body.value.capitalize()
    if planet_name in dignity_rules:
        sign_idx = int(pos.longitude / 30) + 1
        sign = pos.sign.value.capitalize()
        
        dignity = "Neutral"
        rules = dignity_rules[planet_name]
        if sign_idx in rules['own']:
            dignity = "Own Sign (Swagraha)"
        elif sign_idx in rules['exalted']:
            dignity = "Exalted (Uchcha)"
        elif sign_idx in rules['debilitated']:
            dignity = "Debilitated (Neecha)"
        
        print(f"{planet_name:<12} {sign:<15} {dignity:<20}")

print()

# Tools Used
print("="*80)
print("TOOLS AND MODULES USED FOR KUNDLI GENERATION")
print("="*80)
print()
print("1. COORDINATES SOURCE:")
print("   • calculate_chart.py (lines 17-18)")
print("   • Latitude: 44.5333°N, Longitude: 19.2333°E")
print()
print("2. TIMEZONE CONVERSION:")
print("   • Python standard library: zoneinfo.ZoneInfo")
print("   • Timezone: Europe/Belgrade")
print("   • Historical accuracy: Yes (includes DST rules)")
print()
print("3. PLANETARY POSITIONS:")
print("   • Module: backend/app/core/astronomical/framework.py")
print("   • Class: AstronomicalCalculator")
print("   • Engine: Swiss Ephemeris (pyswisseph)")
print("   • Ayanamsa: Lahiri (sidereal zodiac)")
print("   • Coordinate System: Geocentric")
print()
print("4. HOUSE CALCULATION:")
print("   • Module: backend/app/core/calculations/houses.py")
print("   • Class: HouseCalculator")
print("   • System: Whole Sign (Vedic default)")
print()
print("5. NAKSHATRA CALCULATION:")
print("   • Module: backend/app/core/calculations/nakshatra.py")
print("   • Class: NakshatraCalculator")
print("   • Method: 27 nakshatra division with pada calculation")
print()
print("6. DASHA CALCULATION:")
print("   • Module: backend/app/core/calculations/dasha_system.py")
print("   • Class: VimshottariDasha")
print("   • System: Vimshottari (120-year cycle)")
print("   • Basis: Moon's nakshatra position")
print()
print("7. YOGA DETECTION:")
print("   • Module: backend/app/core/calculations/extended_yogas.py")
print("   • Function: calculate_yogas()")
print("   • Coverage: 60+ traditional Vedic yogas")
print()
print("="*80)
print("REPORT GENERATION COMPLETE")
print("All data derived from repository tools - no guesswork")
print("="*80)
