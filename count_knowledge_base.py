"""
Knowledge Base Coverage Counter
Analyzes all classical text sources and counts interpretations
"""
import sys
sys.path.insert(0, 'backend')

from app.core.knowledge.sources.bphs_planets_in_houses import BPHS_PLANETS_IN_HOUSES
from app.core.knowledge.sources.saravali_planets_in_houses import SARAVALI_PLANETS_IN_HOUSES
from app.core.knowledge.sources.phaladeepika_planets_in_houses import PHALADEEPIKA_PLANETS_IN_HOUSES
from app.core.knowledge.sources.hora_sara_planets_in_houses import HORA_SARA_PLANETS_IN_HOUSES
from app.core.knowledge.sources.bphs_yogas import BPHS_RAJA_YOGAS, BPHS_DHANA_YOGAS, BPHS_PANCHA_MAHAPURUSHA_YOGAS
from app.core.knowledge.sources.bphs_dasha_effects import BPHS_MAHADASHA_EFFECTS
from app.core.knowledge.sources.bphs_antardasha_effects import BPHS_ANTARDASHA_EFFECTS
from app.core.knowledge.sources.jataka_parijata_dashas import JATAKA_PARIJATA_DASHAS
from app.core.knowledge.sources.retrograde_effects import RETROGRADE_EFFECTS

print("=" * 80)
print("KNOWLEDGE BASE COVERAGE ANALYSIS")
print("=" * 80)

# Planets in Houses
print("\n1. PLANETS IN HOUSES INTERPRETATIONS")
print("-" * 80)

bphs_total = sum(len(houses) for houses in BPHS_PLANETS_IN_HOUSES.values())
print(f"BPHS (Chapter 24):")
for planet, houses in BPHS_PLANETS_IN_HOUSES.items():
    print(f"  {planet}: {len(houses)} houses")
print(f"  TOTAL: {bphs_total} interpretations")

saravali_total = sum(len(houses) for houses in SARAVALI_PLANETS_IN_HOUSES.values())
print(f"\nSaravali:")
for planet, houses in SARAVALI_PLANETS_IN_HOUSES.items():
    print(f"  {planet}: {len(houses)} houses")
print(f"  TOTAL: {saravali_total} interpretations")

phaladeepika_total = sum(len(houses) for houses in PHALADEEPIKA_PLANETS_IN_HOUSES.values())
print(f"\nPhaladeepika:")
for planet, houses in PHALADEEPIKA_PLANETS_IN_HOUSES.items():
    print(f"  {planet}: {len(houses)} houses")
print(f"  TOTAL: {phaladeepika_total} interpretations")

hora_sara_total = sum(len(houses) for houses in HORA_SARA_PLANETS_IN_HOUSES.values())
print(f"\nHora Sara:")
for planet, houses in HORA_SARA_PLANETS_IN_HOUSES.items():
    print(f"  {planet}: {len(houses)} houses")
print(f"  TOTAL: {hora_sara_total} interpretations")

planets_in_houses_total = bphs_total + saravali_total + phaladeepika_total + hora_sara_total
print(f"\n>>> PLANETS IN HOUSES GRAND TOTAL: {planets_in_houses_total}")

# Yogas
print("\n2. YOGAS (PLANETARY COMBINATIONS)")
print("-" * 80)
raja_count = len(BPHS_RAJA_YOGAS)
dhana_count = len(BPHS_DHANA_YOGAS)
mahapurusha_count = len(BPHS_PANCHA_MAHAPURUSHA_YOGAS)
yogas_total = raja_count + dhana_count + mahapurusha_count

print(f"BPHS Raja Yogas: {raja_count}")
print(f"BPHS Dhana Yogas: {dhana_count}")
print(f"BPHS Pancha Mahapurusha Yogas: {mahapurusha_count}")
print(f"\n>>> YOGAS TOTAL: {yogas_total}")

# Dashas
print("\n3. DASHA PERIOD INTERPRETATIONS")
print("-" * 80)
mahadasha_count = len(BPHS_MAHADASHA_EFFECTS)
print(f"BPHS Mahadasha Effects: {mahadasha_count} planets")

antardasha_count = sum(len(antardashas) for antardashas in BPHS_ANTARDASHA_EFFECTS.values())
print(f"BPHS Antardasha Effects: {antardasha_count} combinations")

jataka_dasha_count = len(JATAKA_PARIJATA_DASHAS)
print(f"Jataka Parijata Dashas: {jataka_dasha_count} planets")

dasha_total = mahadasha_count + antardasha_count + jataka_dasha_count
print(f"\n>>> DASHA TOTAL: {dasha_total}")

# Retrograde
print("\n4. RETROGRADE EFFECTS")
print("-" * 80)
retrograde_count = len(RETROGRADE_EFFECTS)
print(f"Retrograde Planets: {retrograde_count}")

# Grand Total
print("\n" + "=" * 80)
print("GRAND TOTAL KNOWLEDGE BASE")
print("=" * 80)
grand_total = planets_in_houses_total + yogas_total + dasha_total + retrograde_count
print(f"Total Interpretations: {grand_total}")
print(f"  - Planets in Houses: {planets_in_houses_total}")
print(f"  - Yogas: {yogas_total}")
print(f"  - Dashas: {dasha_total}")
print(f"  - Retrograde: {retrograde_count}")

# Coverage Analysis
print("\n" + "=" * 80)
print("COVERAGE GAPS ANALYSIS")
print("=" * 80)

all_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
all_houses = list(range(1, 13))

print("\nPlanets in Houses Coverage (84 combinations per source):")
for source_name, source_data in [
    ("BPHS", BPHS_PLANETS_IN_HOUSES),
    ("Saravali", SARAVALI_PLANETS_IN_HOUSES),
    ("Phaladeepika", PHALADEEPIKA_PLANETS_IN_HOUSES),
    ("Hora Sara", HORA_SARA_PLANETS_IN_HOUSES)
]:
    coverage = sum(len(houses) for houses in source_data.values())
    max_coverage = 7 * 12  # 7 planets (excluding Rahu/Ketu) * 12 houses
    percentage = (coverage / max_coverage) * 100
    print(f"  {source_name}: {coverage}/84 ({percentage:.1f}%)")

# Multi-source coverage
print("\nMulti-Source Coverage (same planet-house in multiple texts):")
multi_source_count = 0
for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
    for house in all_houses:
        sources = 0
        if planet in BPHS_PLANETS_IN_HOUSES and house in BPHS_PLANETS_IN_HOUSES[planet]:
            sources += 1
        if planet in SARAVALI_PLANETS_IN_HOUSES and house in SARAVALI_PLANETS_IN_HOUSES[planet]:
            sources += 1
        if planet in PHALADEEPIKA_PLANETS_IN_HOUSES and house in PHALADEEPIKA_PLANETS_IN_HOUSES[planet]:
            sources += 1
        if planet in HORA_SARA_PLANETS_IN_HOUSES and house in HORA_SARA_PLANETS_IN_HOUSES[planet]:
            sources += 1
        
        if sources >= 2:
            multi_source_count += 1

print(f"  Combinations with 2+ sources: {multi_source_count}/84 ({(multi_source_count/84)*100:.1f}%)")

print("\n" + "=" * 80)
