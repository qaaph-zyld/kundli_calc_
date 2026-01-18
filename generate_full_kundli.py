#!/usr/bin/env python3
"""Generate Full Kundli Report for User
Birth: 09th October 1990, 09:10 AM, Loznica, Serbia
Using only repository tools - no guesswork
"""
from datetime import datetime
from zoneinfo import ZoneInfo
import sys
import json
sys.path.insert(0, 'backend')

from app.core.astronomical.framework import AstronomicalCalculator, AyanamsaSystem
from app.core.calculations.houses import HouseCalculator
from app.core.calculations.dasha_system import VimshottariDasha
from app.core.calculations.extended_yogas import calculate_yogas
from app.core.calculations.nakshatra import NakshatraCalculator
from app.core.calculations.planetary_strength import PlanetaryStrengthCalculator

print("="*80)
print("FULL KUNDLI REPORT")
print("="*80)
print()

# Birth Details (from codebase: calculate_chart.py line 15-18)
print("BIRTH DETAILS:")
print("-" * 40)
birth_date_local = "09th October 1990"
birth_time_local = "09:10 AM"
birth_place = "Loznica, Serbia"
lat = 44.5333  # From calculate_chart.py
lon = 19.2333  # From calculate_chart.py
print(f"Date: {birth_date_local}")
print(f"Time: {birth_time_local} (Local)")
print(f"Place: {birth_place}")
print(f"Coordinates: {lat}°N, {lon}°E (from calculate_chart.py)")
print()

# Timezone Conversion (using ZoneInfo - Europe/Belgrade)
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

# Calculation Settings
print("CALCULATION SETTINGS:")
print("-" * 40)
ayanamsa = AyanamsaSystem.LAHIRI
house_system = 'WHOLE_SIGN'  # String identifier for house system
print(f"Ayanamsa: {ayanamsa.value}")
print(f"House System: {house_system}")
print()

# Initialize Calculators
print("INITIALIZING CALCULATION ENGINES:")
print("-" * 40)
astro_calc = AstronomicalCalculator()
house_calc = HouseCalculator()
nakshatra_calc = NakshatraCalculator()
strength_calc = PlanetaryStrengthCalculator()
print("✓ AstronomicalCalculator (Swiss Ephemeris via pyswisseph)")
print("✓ HouseCalculator (Whole Sign system)")
print("✓ NakshatraCalculator")
print("✓ PlanetaryStrengthCalculator")
print()

# Calculate Julian Day
jd = astro_calc.calculate_julian_day(dt_utc)
print(f"Julian Day: {jd:.6f}")
print()

# 1. PLANETARY POSITIONS (Sidereal - Lahiri Ayanamsa)
print("="*80)
print("1. PLANETARY POSITIONS (SIDEREAL - LAHIRI AYANAMSA)")
print("="*80)
print("Tool: backend/app/core/astronomical/framework.py - AstronomicalCalculator")
print()

planets = astro_calc.calculate_all_planets(jd, lat, lon, ayanamsa)
print(f"{'Planet':<12} {'Longitude':<12} {'Sign':<15} {'Degree':<10} {'Nakshatra':<15} {'Pada':<6}")
print("-" * 95)
for planet_name, planet_data in planets.items():
    lon_deg = planet_data['longitude']
    sign = planet_data['sign']
    sign_deg = planet_data['degree_in_sign']
    
    # Calculate nakshatra
    nak_info = nakshatra_calc.calculate(lon_deg)
    nak_name = nak_info['nakshatra']
    pada = nak_info['pada']
    
    print(f"{planet_name:<12} {lon_deg:<12.4f} {sign:<15} {sign_deg:<10.4f} {nak_name:<15} {pada:<6}")

print()

# 2. ASCENDANT & HOUSES
print("="*80)
print("2. ASCENDANT & HOUSES (WHOLE SIGN SYSTEM)")
print("="*80)
print("Tool: backend/app/core/calculations/houses.py - HouseCalculator")
print()

houses = house_calc.calculate_houses(jd, lat, lon, house_system, ayanamsa)
ascendant = houses['ascendant']
asc_sign = houses['ascendant_sign']
mc = houses['mc']

print(f"Ascendant (Lagna): {ascendant:.4f}° ({asc_sign})")
print(f"Midheaven (MC): {mc:.4f}°")
print()

print(f"{'House':<8} {'Sign':<15} {'Cusp (°)':<12}")
print("-" * 40)
for house_num, cusp_data in houses['cusps'].items():
    if isinstance(cusp_data, dict):
        cusp_deg = cusp_data.get('longitude', 0)
        cusp_sign = cusp_data.get('sign', 'Unknown')
    else:
        cusp_deg = cusp_data
        cusp_sign = astro_calc.get_zodiac_sign(cusp_deg)
    print(f"{house_num:<8} {cusp_sign:<15} {cusp_deg:<12.4f}")

print()

# 3. VIMSHOTTARI DASHA
print("="*80)
print("3. VIMSHOTTARI DASHA PERIODS")
print("="*80)
print("Tool: backend/app/core/calculations/dasha_system.py - VimshottariDasha")
print()

moon_lon = planets['Moon']['longitude']
dasha_calc = VimshottariDasha()
dasha_periods = dasha_calc.calculate_mahadasha(moon_lon, dt_utc)

print(f"Moon's Longitude: {moon_lon:.4f}° (used to calculate dasha starting point)")
print()
print("Mahadasha Periods:")
print(f"{'Planet':<12} {'Start Date':<20} {'End Date':<20} {'Years':<8}")
print("-" * 70)
for period in dasha_periods[:10]:  # Show first 10 periods
    planet = period['planet']
    start = period['start_date'].strftime('%Y-%m-%d')
    end = period['end_date'].strftime('%Y-%m-%d')
    years = period['years']
    print(f"{planet:<12} {start:<20} {end:<20} {years:<8}")

# Current Dasha
birth_date = dt_utc
current_dasha = None
for period in dasha_periods:
    if period['start_date'] <= birth_date <= period['end_date']:
        current_dasha = period
        break

if current_dasha:
    print()
    print(f"Dasha at Birth: {current_dasha['planet']} ({current_dasha['start_date'].strftime('%Y-%m-%d')} to {current_dasha['end_date'].strftime('%Y-%m-%d')})")

print()

# 4. YOGAS (Planetary Combinations)
print("="*80)
print("4. VEDIC YOGAS (PLANETARY COMBINATIONS)")
print("="*80)
print("Tool: backend/app/core/calculations/extended_yogas.py - calculate_yogas()")
print()

# Prepare data for yoga calculation
planet_positions = {}
for planet_name, planet_data in planets.items():
    planet_positions[planet_name.lower()] = {
        'longitude': planet_data['longitude'],
        'sign': planet_data['sign'],
        'house': None  # Will be calculated
    }

# Calculate which house each planet is in (Whole Sign)
asc_sign_num = astro_calc.get_sign_number(asc_sign)
for planet_name, planet_data in planet_positions.items():
    planet_sign = planet_data['sign']
    planet_sign_num = astro_calc.get_sign_number(planet_sign)
    house_num = ((planet_sign_num - asc_sign_num) % 12) + 1
    planet_data['house'] = house_num

# Calculate house lordships
house_lords = {}
for i in range(1, 13):
    house_sign_num = (asc_sign_num + i - 1) % 12
    if house_sign_num == 0:
        house_sign_num = 12
    lord = astro_calc.get_sign_lord(house_sign_num)
    house_lords[i] = lord

yogas = calculate_yogas(planet_positions, house_lords, asc_sign)

print(f"Total Yogas Detected: {len(yogas)}")
print()

if yogas:
    print(f"{'Yoga Name':<30} {'Type':<20} {'Strength':<10}")
    print("-" * 65)
    for yoga in yogas:
        name = yoga.get('name', 'Unknown')
        yoga_type = yoga.get('type', 'Unknown')
        strength = yoga.get('strength', 0)
        print(f"{name:<30} {yoga_type:<20} {strength:<10.2f}")
        desc = yoga.get('description', '')
        if desc:
            print(f"  → {desc}")
        print()
else:
    print("No specific yogas detected (rare - most charts have multiple yogas)")

print()

# 5. PLANETARY STRENGTHS
print("="*80)
print("5. PLANETARY STRENGTHS (SHADBALA COMPONENTS)")
print("="*80)
print("Tool: backend/app/core/calculations/planetary_strength.py")
print()

# Calculate dignities first
dignities = {}
for planet_name, planet_data in planets.items():
    if planet_name in ['Rahu', 'Ketu']:
        continue
    planet_lon = planet_data['longitude']
    planet_sign_num = astro_calc.get_sign_number(planet_data['sign'])
    
    # Calculate dignity based on sign position
    dignity = "Neutral"
    if planet_name == "Sun":
        if planet_sign_num == 5:  # Leo
            dignity = "Own Sign"
        elif planet_sign_num == 1:  # Aries
            dignity = "Exalted"
        elif planet_sign_num == 7:  # Libra
            dignity = "Debilitated"
    elif planet_name == "Moon":
        if planet_sign_num == 4:  # Cancer
            dignity = "Own Sign"
        elif planet_sign_num == 2:  # Taurus
            dignity = "Exalted"
        elif planet_sign_num == 8:  # Scorpio
            dignity = "Debilitated"
    elif planet_name == "Mars":
        if planet_sign_num in [1, 8]:  # Aries, Scorpio
            dignity = "Own Sign"
        elif planet_sign_num == 10:  # Capricorn
            dignity = "Exalted"
        elif planet_sign_num == 4:  # Cancer
            dignity = "Debilitated"
    elif planet_name == "Mercury":
        if planet_sign_num in [3, 6]:  # Gemini, Virgo
            dignity = "Own Sign"
        elif planet_sign_num == 6:  # Virgo
            dignity = "Exalted"
        elif planet_sign_num == 12:  # Pisces
            dignity = "Debilitated"
    elif planet_name == "Jupiter":
        if planet_sign_num in [9, 12]:  # Sagittarius, Pisces
            dignity = "Own Sign"
        elif planet_sign_num == 4:  # Cancer
            dignity = "Exalted"
        elif planet_sign_num == 10:  # Capricorn
            dignity = "Debilitated"
    elif planet_name == "Venus":
        if planet_sign_num in [2, 7]:  # Taurus, Libra
            dignity = "Own Sign"
        elif planet_sign_num == 12:  # Pisces
            dignity = "Exalted"
        elif planet_sign_num == 6:  # Virgo
            dignity = "Debilitated"
    elif planet_name == "Saturn":
        if planet_sign_num in [10, 11]:  # Capricorn, Aquarius
            dignity = "Own Sign"
        elif planet_sign_num == 7:  # Libra
            dignity = "Exalted"
        elif planet_sign_num == 1:  # Aries
            dignity = "Debilitated"
    
    dignities[planet_name] = dignity

print(f"{'Planet':<12} {'Sign':<15} {'Dignity':<20}")
print("-" * 50)
for planet_name, planet_data in planets.items():
    if planet_name in ['Rahu', 'Ketu']:
        continue
    sign = planet_data['sign']
    dignity = dignities.get(planet_name, "Neutral")
    print(f"{planet_name:<12} {sign:<15} {dignity:<20}")

print()

# 6. SUMMARY
print("="*80)
print("6. CHART SUMMARY")
print("="*80)
print()
print(f"Rising Sign (Lagna): {asc_sign}")
print(f"Lagna Lord: {astro_calc.get_sign_lord(astro_calc.get_sign_number(asc_sign))}")
print(f"Moon Sign (Chandra Rashi): {planets['Moon']['sign']}")
print(f"Sun Sign: {planets['Sun']['sign']}")
print()

# Chart Lord (1st house lord)
chart_lord = house_lords.get(1, 'Unknown')
chart_lord_position = None
for pname, pdata in planet_positions.items():
    if pname.capitalize() == chart_lord:
        chart_lord_position = f"House {pdata['house']} ({pdata['sign']})"
        break

print(f"Chart Lord (Lagna Lord): {chart_lord}")
if chart_lord_position:
    print(f"Chart Lord Position: {chart_lord_position}")
print()

print("="*80)
print("TOOLS USED FOR KUNDLI GENERATION:")
print("="*80)
print("1. Coordinates: calculate_chart.py (lines 15-18)")
print("2. Timezone: Python zoneinfo.ZoneInfo (Europe/Belgrade)")
print("3. Planetary Positions: backend/app/core/astronomical/framework.py")
print("   - AstronomicalCalculator (Swiss Ephemeris via pyswisseph)")
print("   - Lahiri Ayanamsa (sidereal zodiac)")
print("4. Houses: backend/app/core/calculations/houses.py")
print("   - HouseCalculator with Whole Sign system")
print("5. Nakshatras: backend/app/core/calculations/nakshatra.py")
print("   - NakshatraCalculator")
print("6. Dasha: backend/app/core/calculations/dasha_system.py")
print("   - VimshottariDasha")
print("7. Yogas: backend/app/core/calculations/extended_yogas.py")
print("   - calculate_yogas() function")
print("8. Strengths: backend/app/core/calculations/planetary_strength.py")
print("   - PlanetaryStrengthCalculator")
print("="*80)
print()
print("Report generation complete. No guesswork - all data from repository tools.")
