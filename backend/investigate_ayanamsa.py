#!/usr/bin/env python3
"""
Investigate Ayanamsa Deviation between Swiss Ephemeris and JHora

JHora uses Lahiri ayanamsa but may use a slightly different reference point
or calculation method than Swiss Ephemeris default.

Key Facts:
- JHora's Lahiri is based on the Lahiri Ephemeris Commission standard
- Swiss Ephemeris has multiple Lahiri variants
- The difference we see is ~0.0156° which is systematic
"""

import swisseph as swe
from datetime import datetime

# Test date: October 9, 1990, 9:10:00 AM, UTC+1
# This is the user's birth data
test_date = datetime(1990, 10, 9, 8, 10, 0)  # Converted to UTC

# Calculate Julian Day
jd = swe.julday(
    test_date.year, 
    test_date.month, 
    test_date.day,
    test_date.hour + test_date.minute/60 + test_date.second/3600
)

print("=" * 70)
print("AYANAMSA INVESTIGATION")
print("=" * 70)
print(f"Test Date: {test_date} UTC")
print(f"Julian Day: {jd}")
print()

# JHora reference value from user's chart
jhora_ayanamsa = 23.712542  # 23°42'45.15"
print(f"JHora Ayanamsa (reference): {jhora_ayanamsa:.6f}° = 23°42'45.15\"")
print()

# Test all relevant Lahiri variants in Swiss Ephemeris
lahiri_variants = [
    (swe.SIDM_LAHIRI, "SIDM_LAHIRI (default)"),
    (swe.SIDM_LAHIRI_1940, "SIDM_LAHIRI_1940"),
    (swe.SIDM_LAHIRI_VP285, "SIDM_LAHIRI_VP285"),
]

# Also test True Chitrapaksha which some JHora versions use
other_variants = [
    (swe.SIDM_TRUE_CITRA, "SIDM_TRUE_CITRA (Chitrapaksha)"),
    (swe.SIDM_KRISHNAMURTI, "SIDM_KRISHNAMURTI"),
    (swe.SIDM_RAMAN, "SIDM_RAMAN"),
]

print("Swiss Ephemeris Ayanamsa Variants:")
print("-" * 70)
print(f"{'Variant':<35} {'Value (°)':<15} {'Diff from JHora':<15}")
print("-" * 70)

best_match = None
best_diff = float('inf')

for sid_mode, name in lahiri_variants + other_variants:
    swe.set_sid_mode(sid_mode)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    diff = ayanamsa - jhora_ayanamsa
    
    if abs(diff) < abs(best_diff):
        best_diff = diff
        best_match = (sid_mode, name, ayanamsa)
    
    match_indicator = "← BEST" if abs(diff) < 0.001 else ""
    print(f"{name:<35} {ayanamsa:<15.6f} {diff:+.6f}° {match_indicator}")

print()
print("=" * 70)
print("ANALYSIS")
print("=" * 70)

if best_match:
    print(f"Best matching variant: {best_match[1]}")
    print(f"  Value: {best_match[2]:.6f}°")
    print(f"  Difference: {best_diff:+.6f}°")
    print()

# The issue: Swiss Ephemeris SIDM_LAHIRI uses a different reference
# JHora likely uses SIDM_LAHIRI_1940 or a custom calculation

# Check what SIDM_LAHIRI_1940 gives us
swe.set_sid_mode(swe.SIDM_LAHIRI_1940)
ayanamsa_1940 = swe.get_ayanamsa_ut(jd)
diff_1940 = ayanamsa_1940 - jhora_ayanamsa

print("Detailed Check - SIDM_LAHIRI_1940:")
print(f"  Swiss Ephemeris: {ayanamsa_1940:.6f}°")
print(f"  JHora:           {jhora_ayanamsa:.6f}°")
print(f"  Difference:      {diff_1940:+.6f}°")
print()

# Convert to arc-seconds for clarity
diff_arcsec = abs(diff_1940) * 3600
print(f"  Difference in arc-seconds: {diff_arcsec:.2f}\"")
print(f"  Tolerance (0.01°):         36.00\"")
print()

if abs(diff_1940) <= 0.0001:
    print("✓ SIDM_LAHIRI_1940 matches JHora within tolerance!")
    print()
    print("RECOMMENDATION:")
    print("  Change from SIDM_LAHIRI to SIDM_LAHIRI_1940 in AstronomicalCalculator")
else:
    print("Checking if JHora uses True Chitrapaksha...")
    swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
    ayanamsa_citra = swe.get_ayanamsa_ut(jd)
    diff_citra = ayanamsa_citra - jhora_ayanamsa
    print(f"  TRUE_CITRA difference: {diff_citra:+.6f}°")

# Test with custom offset
print()
print("=" * 70)
print("TESTING CUSTOM AYANAMSA OFFSET")
print("=" * 70)

# Calculate the exact offset needed
swe.set_sid_mode(swe.SIDM_LAHIRI)
default_ayanamsa = swe.get_ayanamsa_ut(jd)
needed_offset = jhora_ayanamsa - default_ayanamsa

print(f"Default SIDM_LAHIRI:    {default_ayanamsa:.6f}°")
print(f"JHora Lahiri:           {jhora_ayanamsa:.6f}°")
print(f"Offset needed:          {needed_offset:+.6f}°")
print()

# Swiss Ephemeris allows custom ayanamsa with swe.set_sid_mode with offset
# Using SIDM_USER with reference date

# The standard Lahiri reference: Spica at 0° Libra on Sep 21, 1944
# But JHora might use a slightly different reference

print("JHora Lahiri Reference Info:")
print("  - Based on Indian Astronomical Ephemeris")
print("  - Reference: Spica at 180° sidereal on specific epoch")
print("  - JHora 8.0 uses 'Lahiri' (sometimes called 'Chitrapaksha')")
print()

# Let's verify by calculating what the planetary positions would be
# if we apply the offset
print("=" * 70)
print("VERIFICATION: Planetary positions with corrected ayanamsa")
print("=" * 70)

# User's chart data
lat = 44.5333
lon = 19.2167

# Calculate Sun position with both methods
from app.core.astronomical.framework import CelestialBody

def calc_planet_with_ayanamsa(planet_id, jd, sid_mode):
    swe.set_sid_mode(sid_mode)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    result = swe.calc_ut(jd, planet_id, flags)
    return result[0][0]

print(f"{'Planet':<10} {'Default Lahiri':<15} {'Lahiri 1940':<15} {'JHora Expected':<15}")
print("-" * 60)

jhora_expected = {
    "Sun": 172.068494,
    "Moon": 58.348689,
    "Mars": 49.917178,
    "Mercury": 162.604600,
    "Jupiter": 105.858014,
    "Venus": 166.069264,
    "Saturn": 265.204447,
}

planets = [
    (swe.SUN, "Sun"),
    (swe.MOON, "Moon"),
    (swe.MARS, "Mars"),
    (swe.MERCURY, "Mercury"),
    (swe.JUPITER, "Jupiter"),
    (swe.VENUS, "Venus"),
    (swe.SATURN, "Saturn"),
]

for planet_id, name in planets:
    pos_default = calc_planet_with_ayanamsa(planet_id, jd, swe.SIDM_LAHIRI)
    pos_1940 = calc_planet_with_ayanamsa(planet_id, jd, swe.SIDM_LAHIRI_1940)
    expected = jhora_expected.get(name, 0)
    
    diff_default = abs(pos_default - expected)
    diff_1940 = abs(pos_1940 - expected)
    
    better = "1940 ✓" if diff_1940 < diff_default else "default"
    
    print(f"{name:<10} {pos_default:<15.4f} {pos_1940:<15.4f} {expected:<15.4f} {better}")

print()
print("=" * 70)
print("CONCLUSION")
print("=" * 70)

# Final verification
swe.set_sid_mode(swe.SIDM_LAHIRI_1940)
sun_1940 = calc_planet_with_ayanamsa(swe.SUN, jd, swe.SIDM_LAHIRI_1940)
sun_diff = abs(sun_1940 - 172.068494)

if sun_diff <= 0.01:
    print("✓ SIDM_LAHIRI_1940 brings Sun within ±0.01° tolerance")
    print()
    print("ACTION REQUIRED:")
    print("  Update AstronomicalCalculator to use SIDM_LAHIRI_1940 instead of SIDM_LAHIRI")
    print()
    print("  In app/core/astronomical/framework.py, change:")
    print("    swe.set_sid_mode(swe.SIDM_LAHIRI)")
    print("  To:")
    print("    swe.set_sid_mode(swe.SIDM_LAHIRI_1940)")
else:
    print(f"✗ SIDM_LAHIRI_1940 still has {sun_diff:.4f}° deviation")
    print("  Need to investigate further or use custom ayanamsa")

swe.close()
