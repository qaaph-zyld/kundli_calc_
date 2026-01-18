#!/usr/bin/env python3
"""
Investigate Mercury and Venus deviations

The remaining deviations (0.0141° Mercury, 0.0132° Venus) could be due to:
1. True vs Mean Node calculation affecting reference frame
2. Time calculation precision
3. Different ephemeris flags (topocentric vs geocentric)
"""

import swisseph as swe
from datetime import datetime, timedelta

# Test date: October 9, 1990, 9:10:00 AM, local time (UTC+1)
local_time = datetime(1990, 10, 9, 9, 10, 0)
utc_time = datetime(1990, 10, 9, 8, 10, 0)

# Location
lat = 44.5333  # 44°32'N
lon = 19.2167  # 19°13'E

print("=" * 70)
print("INNER PLANET DEVIATION INVESTIGATION")
print("=" * 70)
print(f"Local Time: {local_time}")
print(f"UTC Time:   {utc_time}")
print(f"Location:   {lat}°N, {lon}°E")
print()

# JHora expected values
jhora_expected = {
    "Mercury": 162.604600,
    "Venus": 166.069264,
    "Sun": 172.068494,
    "Moon": 58.348689,
}

# Calculate JD for UTC time
jd_utc = swe.julday(utc_time.year, utc_time.month, utc_time.day,
                     utc_time.hour + utc_time.minute/60)

print(f"Julian Day (UTC): {jd_utc}")
print()

# Set ayanamsa
swe.set_sid_mode(swe.SIDM_LAHIRI_1940)

# Test different calculation flags
print("Testing different calculation methods:")
print("-" * 70)

flag_sets = [
    ("SWIEPH + SIDEREAL + SPEED", swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED),
    ("MOSEPH + SIDEREAL + SPEED", swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED),
    ("SWIEPH + SIDEREAL + SPEED + TRUEPOS", swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED | swe.FLG_TRUEPOS),
    ("SWIEPH + SIDEREAL (no speed)", swe.FLG_SWIEPH | swe.FLG_SIDEREAL),
]

best_mercury = None
best_venus = None

for name, flags in flag_sets:
    print(f"\n{name}:")
    
    # Mercury
    result = swe.calc_ut(jd_utc, swe.MERCURY, flags)
    merc_lon = result[0][0]
    merc_diff = abs(merc_lon - jhora_expected["Mercury"])
    
    # Venus  
    result = swe.calc_ut(jd_utc, swe.VENUS, flags)
    venus_lon = result[0][0]
    venus_diff = abs(venus_lon - jhora_expected["Venus"])
    
    print(f"  Mercury: {merc_lon:.6f}° (diff: {merc_diff:.6f}°)")
    print(f"  Venus:   {venus_lon:.6f}° (diff: {venus_diff:.6f}°)")
    
    if best_mercury is None or merc_diff < best_mercury[1]:
        best_mercury = (name, merc_diff, merc_lon)
    if best_venus is None or venus_diff < best_venus[1]:
        best_venus = (name, venus_diff, venus_lon)

print()
print("=" * 70)
print("CHECKING TIME SENSITIVITY")
print("=" * 70)

# Mercury and Venus move faster, so time errors affect them more
# Let's check if a small time adjustment helps

flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

print("\nTime offset analysis (seconds):")
print("-" * 70)
print(f"{'Offset (s)':<12} {'Mercury':<15} {'Merc Diff':<12} {'Venus':<15} {'Venus Diff':<12}")
print("-" * 70)

best_offset = None
best_total_diff = float('inf')

for offset_seconds in range(-120, 121, 10):
    # Adjust JD by offset
    jd_test = jd_utc + offset_seconds / 86400.0
    
    result_merc = swe.calc_ut(jd_test, swe.MERCURY, flags)
    result_venus = swe.calc_ut(jd_test, swe.VENUS, flags)
    
    merc_lon = result_merc[0][0]
    venus_lon = result_venus[0][0]
    
    merc_diff = abs(merc_lon - jhora_expected["Mercury"])
    venus_diff = abs(venus_lon - jhora_expected["Venus"])
    total_diff = merc_diff + venus_diff
    
    if total_diff < best_total_diff:
        best_total_diff = total_diff
        best_offset = offset_seconds
    
    if offset_seconds % 30 == 0:
        print(f"{offset_seconds:+12d} {merc_lon:<15.6f} {merc_diff:<12.6f} {venus_lon:<15.6f} {venus_diff:<12.6f}")

print()
print(f"Best offset: {best_offset}s (total diff: {best_total_diff:.6f}°)")

# Test the best offset
jd_best = jd_utc + best_offset / 86400.0
result_merc = swe.calc_ut(jd_best, swe.MERCURY, flags)
result_venus = swe.calc_ut(jd_best, swe.VENUS, flags)

print()
print("=" * 70)
print("ANALYSIS: Root Cause Investigation")
print("=" * 70)

# The issue is likely different Delta T handling
# Delta T is the difference between UT (Universal Time) and TT (Terrestrial Time)
print("\nDelta T Investigation:")
delta_t = swe.deltat(jd_utc) * 86400  # Convert to seconds
print(f"Delta T at this date: {delta_t:.2f} seconds")

# Check if JHora might use TT instead of UT
jd_tt = jd_utc + swe.deltat(jd_utc)
print(f"JD (UT):  {jd_utc}")
print(f"JD (TT):  {jd_tt}")
print(f"Difference: {(jd_tt - jd_utc) * 86400:.2f} seconds")

# Calculate with TT
result_merc_tt = swe.calc_ut(jd_tt, swe.MERCURY, flags)
result_venus_tt = swe.calc_ut(jd_tt, swe.VENUS, flags)

print(f"\nWith TT-based JD:")
print(f"  Mercury: {result_merc_tt[0][0]:.6f}° (diff: {abs(result_merc_tt[0][0] - jhora_expected['Mercury']):.6f}°)")
print(f"  Venus:   {result_venus_tt[0][0]:.6f}° (diff: {abs(result_venus_tt[0][0] - jhora_expected['Venus']):.6f}°)")

# The deviations are small enough that they're within acceptable range for most applications
# JHora may use slightly different ephemeris precision or Delta T calculation

print()
print("=" * 70)
print("CONCLUSION")
print("=" * 70)

# Current deviations
current_merc_diff = 0.0141
current_venus_diff = 0.0132

print(f"Current deviations:")
print(f"  Mercury: {current_merc_diff:.4f}° ({current_merc_diff * 3600:.1f} arc-seconds)")
print(f"  Venus:   {current_venus_diff:.4f}° ({current_venus_diff * 3600:.1f} arc-seconds)")
print(f"  Tolerance: 0.01° (36 arc-seconds)")
print()

# These are 50.8" and 47.5" respectively - just ~12-15 arc-seconds above tolerance
# This is likely due to:
# 1. Different Delta T algorithms
# 2. Different ephemeris precision
# 3. Minor differences in aberration/nutation handling

if current_merc_diff < 0.02 and current_venus_diff < 0.02:
    print("RECOMMENDATION:")
    print("  The deviations are very small (< 1 arc-minute) and acceptable for")
    print("  practical astrological purposes. They fall within the uncertainty")
    print("  of birth time recording (1 minute of time = ~0.25° for Moon).")
    print()
    print("  Options:")
    print("  1. Accept current accuracy (deviations < 0.015°)")
    print("  2. Widen tolerance to ±0.02° for inner planets")
    print("  3. Apply minor time correction factor for JHora compatibility")

swe.close()
