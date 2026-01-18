#!/usr/bin/env python3
"""Generate comprehensive Kundli report"""
import sys
sys.path.insert(0, 'app')

from datetime import datetime
from app.core.calculations.ayanamsa import EnhancedAyanamsaManager
from app.core.knowledge.sources.bphs_planets_in_houses import get_planet_in_house_interpretation
from app.core.knowledge.sources.saravali_planets_in_houses import get_saravali_interpretation
from app.core.knowledge.sources.phaladeepika_planets_in_houses import get_phaladeepika_interpretation
from app.core.knowledge.engine.multi_source_engine import MultiSourceEngine
import swisseph as swe

# Birth data
dt = datetime(1990, 10, 9, 9, 10, 0)
lat, lon = 44.5309221, 19.2237478
tz_offset = 1.0  # CET (UTC+1)

# Calculate JD (UTC time)
utc_dt = dt.replace(hour=dt.hour - int(tz_offset))
jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

# Set sidereal mode
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Calculate planets
planet_ids = {
    'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
    'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 'Venus': swe.VENUS,
    'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE, 'Ketu': swe.MEAN_NODE
}

planets = {}
for name, pid in planet_ids.items():
    if name == 'Ketu':
        # Ketu is 180 degrees from Rahu
        pos = (planets['Rahu']['longitude'] + 180) % 360
        planets[name] = {'longitude': pos, 'speed': planets['Rahu']['speed']}
    else:
        calc = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_NONUT)
        planets[name] = {'longitude': calc[0][0], 'speed': calc[0][3]}

# Calculate ayanamsa
ayanamsa_mgr = EnhancedAyanamsaManager()
ayanamsa = ayanamsa_mgr.calculate_precise_ayanamsa(utc_dt, 'LAHIRI')

# Planets are already in sidereal (we used FLG_SIDEREAL)
signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

sidereal_planets = {}
for planet, data in planets.items():
    sidereal_long = data['longitude'] % 360
    sign_num = int(sidereal_long / 30)
    degree_in_sign = sidereal_long % 30
    sidereal_planets[planet] = {
        'longitude': sidereal_long,
        'sign': signs[sign_num],
        'degree': degree_in_sign,
        'sign_num': sign_num + 1,
        'retrograde': data.get('speed', 1) < 0
    }

# Calculate ascendant (using houses calculation with geographic coords)
cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_SIDEREAL | swe.FLG_NONUT)
asc_sidereal = cusps[0]
asc_sign_num = int(asc_sidereal / 30)
asc_degree = asc_sidereal % 30

# Calculate house placements
house_placements = {}
for planet, data in sidereal_planets.items():
    house = ((data['sign_num'] - asc_sign_num - 1) % 12) + 1
    house_placements[planet] = house

print('=' * 80)
print('COMPREHENSIVE VEDIC ASTROLOGY BIRTH CHART REPORT')
print('=' * 80)
print()
print('Birth Information:')
print(f'  Date: October 9, 1990')
print(f'  Time: 9:10 AM (CET, UTC+1)')
print(f'  Place: Loznica, Serbia')
print(f'  Coordinates: 44.53°N, 19.22°E')
print(f'  Ayanamsa: Lahiri ({ayanamsa:.4f}°)')
print(f'  Calculation System: Swiss Ephemeris, Whole Sign Houses')
print()

print('-' * 80)
print('ASCENDANT (LAGNA)')
print('-' * 80)
print(f'  Rising Sign: {signs[asc_sign_num]} at {asc_degree:.2f}°')
print()

print('-' * 80)
print('PLANETARY POSITIONS (Sidereal)')
print('-' * 80)
print(f"{'Planet':<12} {'Sign':<15} {'Degree':<10} {'House':<8} {'Status':<12}")
print('-' * 80)
for planet, data in sidereal_planets.items():
    if planet not in ['Mean Node', 'True Node']:
        status = 'Retrograde' if data['retrograde'] else 'Direct'
        house = house_placements[planet]
        print(f"{planet:<12} {data['sign']:<15} {data['degree']:>6.2f}°   {house:<8} {status:<12}")
print()

# Birth Nakshatra
moon_long = sidereal_planets['Moon']['longitude']
birth_star = int(moon_long / (360/27))
nakshatras = ['Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu', 
              'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta',
              'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 
              'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishtha', 'Shatabhisha',
              'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati']

print('-' * 80)
print('BIRTH NAKSHATRA')
print('-' * 80)
print(f'  Moon Nakshatra: {nakshatras[birth_star]}')
pada = int((moon_long % (360/27)) / (360/27/4)) + 1
print(f'  Pada: {pada}')
print()

# Vimshottari Dasha at birth
dasha_lords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
nak_per_dasha = 3
dasha_ruler = dasha_lords[birth_star // nak_per_dasha]

print('-' * 80)
print('VIMSHOTTARI DASHA')
print('-' * 80)
print(f'  Birth Dasha Lord: {dasha_ruler}')
current_age = (datetime.now().year - 1990) + (datetime.now().month - 10) / 12.0
print(f'  Current Age: {current_age:.1f} years')
print()

# Multi-source interpretations
print('=' * 80)
print('DETAILED INTERPRETATIONS FROM CLASSICAL TEXTS')
print('=' * 80)
print()

multi_source = MultiSourceEngine()

# Key planets to interpret
key_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']

for planet in key_planets:
    house = house_placements[planet]
    sign = sidereal_planets[planet]['sign']
    
    print(f"\n{'*' * 80}")
    print(f"{planet.upper()} IN HOUSE {house} ({sign})")
    print('*' * 80)
    
    # Get multi-source comparison
    comparison = multi_source.compare_sources(planet, house)
    
    if comparison:
        print(f"\nAvailable Sources: {', '.join(comparison.sources_available)}")
        print(f"Agreement Level: {comparison.agreement_level.value.replace('_', ' ').title()}")
        print(f"Confidence Score: {comparison.confidence_score:.1%}")
        
        if comparison.common_themes:
            print("\nCommon Themes Across Sources:")
            for theme in comparison.common_themes:
                print(f"  • {theme}")
        
        print(f"\n{'-' * 80}")
        print("SYNTHESIZED INTERPRETATION:")
        print('-' * 80)
        print(comparison.synthesis)
        
        if comparison.unique_insights:
            print(f"\n{'-' * 80}")
            print("UNIQUE INSIGHTS FROM SPECIFIC TEXTS:")
            print('-' * 80)
            for source, insights in comparison.unique_insights.items():
                if insights:
                    print(f"\n{source}:")
                    for insight in insights:
                        print(f"  • {insight}")
        
        if comparison.contradictions:
            print(f"\n{'-' * 80}")
            print("NOTED CONTRADICTIONS:")
            print('-' * 80)
            for contra in comparison.contradictions:
                print(f"  • {contra.get('description', 'No description')}")

print("\n" + '=' * 80)
print('END OF REPORT')
print('=' * 80)
print()
print("Note: This report uses digitized classical texts with complete verse citations.")
print("Sources: BPHS (Brihat Parashara Hora Shastra), Saravali, Phaladeepika, Hora Sara")
print("Translation references provided for each interpretation.")
print()
