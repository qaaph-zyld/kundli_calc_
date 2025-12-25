#!/usr/bin/env python3
"""Debug Gajakesari yoga calculation"""

from app.core.calculations.complete_yogas import CompleteYogaCalculator

# Test data from the failing test
test_chart_positions = {
    "Sun": 172.5,      # Virgo
    "Moon": 58.32,     # Taurus  
    "Mars": 30.8,      # Taurus
    "Mercury": 186.2,  # Libra
    "Jupiter": 95.4,   # Cancer
    "Venus": 220.1,    # Scorpio
    "Saturn": 309.2,   # Capricorn
    "Rahu": 299.8,     # Capricorn
    "Ketu": 119.8      # Cancer
}

ascendant = 151.2  # Leo ascendant

print("=== Gajakesari Yoga Debug ===")
print(f"Moon: {test_chart_positions['Moon']}°")
print(f"Jupiter: {test_chart_positions['Jupiter']}°")

# Calculate signs
moon_sign = int(test_chart_positions["Moon"] / 30)
jup_sign = int(test_chart_positions["Jupiter"] / 30)

print(f"Moon sign: {moon_sign} (0=Aries)")
print(f"Jupiter sign: {jup_sign}")

# Calculate houses from Moon
houses_from_moon = ((jup_sign - moon_sign) % 12) + 1
print(f"Jupiter is {houses_from_moon}th house from Moon")

# Check conditions
kendras = [1, 4, 7, 10]
trines = [5, 9]
extended = kendras + trines

print(f"Kendras: {kendras}")
print(f"Trines: {trines}")
print(f"Extended (kendras+trines): {extended}")
print(f"Is kendra: {houses_from_moon in kendras}")
print(f"Is trine: {houses_from_moon in trines}")
print(f"Is extended: {houses_from_moon in extended}")

# Run actual calculation
calc = CompleteYogaCalculator()
result = calc.calculate_all_yogas(test_chart_positions, ascendant)

print(f"\nTotal yogas found: {len(result['yogas'])}")
gajakesari_yogas = [y for y in result['yogas'] if 'gajakesari' in y.get('name', '').lower()]
print(f"Gajakesari yogas: {len(gajakesari_yogas)}")

# Print all yoga names
print("\nAll yoga names:")
for yoga in result['yogas']:
    print(f"  - {yoga.get('name', 'Unknown')}")

if gajakesari_yogas:
    print(f"\nGajakesari details:")
    for yoga in gajakesari_yogas:
        print(f"  Name: {yoga.get('name')}")
        print(f"  Present: {yoga.get('present')}")
        print(f"  Description: {yoga.get('description')}")
else:
    print("\nGajakesari not detected")
