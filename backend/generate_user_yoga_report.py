"""
Generate comprehensive yoga report for user's birth chart
Birth Data: 09 October 1990, 09:10 AM, Loznica, Serbia
"""
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.astronomical.framework import AstronomicalCalculator
from app.core.calculations.houses import HouseCalculator
from app.core.calculations.extended_yogas import ExtendedYogaCalculator
from app.core.calculations.dasha_system import VimshottariDasha


def generate_yoga_report():
    """Generate comprehensive yoga report for user"""
    
    # Birth data
    birth_date = datetime(1990, 10, 9, 9, 10, 0)  # 09:10 AM
    latitude = 44.5333  # Loznica, Serbia
    longitude = 19.2333
    timezone_offset = 1.0  # CET (UTC+1)
    
    print("=" * 80)
    print("COMPREHENSIVE YOGA REPORT")
    print("=" * 80)
    print(f"\nBirth Details:")
    print(f"  Date: 09 October 1990")
    print(f"  Time: 09:10 AM (Local Time)")
    print(f"  Place: Loznica, Serbia")
    print(f"  Coordinates: {latitude}°N, {longitude}°E")
    print(f"  Timezone: UTC+{timezone_offset}")
    print("\n" + "=" * 80)
    
    # Initialize calculators
    from app.core.astronomical.framework import AyanamsaSystem, CelestialBody, GeoLocation
    
    location = GeoLocation(latitude=latitude, longitude=longitude, altitude=0.0)
    astro_calc = AstronomicalCalculator(ayanamsa_system=AyanamsaSystem.LAHIRI)
    house_calc = HouseCalculator()
    dasha_calc = VimshottariDasha()
    
    # Calculate planetary positions
    print("\n📍 PLANETARY POSITIONS (Sidereal, Lahiri Ayanamsa)")
    print("-" * 80)
    
    planet_positions = {}
    planet_map = {
        "Sun": CelestialBody.SUN,
        "Moon": CelestialBody.MOON,
        "Mars": CelestialBody.MARS,
        "Mercury": CelestialBody.MERCURY,
        "Jupiter": CelestialBody.JUPITER,
        "Venus": CelestialBody.VENUS,
        "Saturn": CelestialBody.SATURN,
        "Rahu": CelestialBody.RAHU,
        "Ketu": CelestialBody.KETU
    }
    
    for planet_name, planet_body in planet_map.items():
        pos_obj = astro_calc.calculate_planet_position(planet_body, birth_date, location)
        pos = {
            "longitude": pos_obj.longitude,
            "latitude": pos_obj.latitude,
            "speed": pos_obj.speed,
            "is_retrograde": pos_obj.is_retrograde
        }
        planet_positions[planet_name] = pos
        
        # Calculate sign
        sign_num = int(pos["longitude"] // 30)
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_name = signs[sign_num]
        
        degree_in_sign = pos["longitude"] % 30
        
        print(f"{planet_name:10s}: {pos['longitude']:7.2f}° | {sign_name:12s} {degree_in_sign:5.2f}° | "
              f"{'Retrograde' if pos.get('is_retrograde', False) else 'Direct':10s}")
    
    # Calculate houses (Whole Sign)
    print(f"\n🏠 HOUSE SYSTEM: Whole Sign")
    print("-" * 80)
    
    house_data = house_calc.calculate_houses(
        birth_date, latitude, longitude, house_system="WHOLE_SIGN"
    )
    
    ascendant_deg = house_data["ascendant"]
    ascendant_sign_num = int(ascendant_deg // 30)
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    ascendant_sign = signs[ascendant_sign_num]
    
    print(f"Ascendant (Lagna): {ascendant_deg:.2f}° ({ascendant_sign})")
    print(f"Midheaven (MC): {house_data['midheaven']:.2f}°")
    
    # Organize planets by house
    houses = {i: [] for i in range(1, 13)}
    for planet, pos in planet_positions.items():
        house_num = ((int(pos["longitude"] // 30) - ascendant_sign_num) % 12) + 1
        houses[house_num].append(planet)
        planet_positions[planet]["house"] = house_num
        planet_positions[planet]["sign"] = int(pos["longitude"] // 30)
    
    print(f"\nHouse Occupations:")
    for house_num in range(1, 13):
        planets_in_house = houses[house_num]
        if planets_in_house:
            print(f"  House {house_num:2d}: {', '.join(planets_in_house)}")
    
    # Calculate Moon Nakshatra for Dasha
    moon_long = planet_positions["Moon"]["longitude"]
    print(f"\n🌙 MOON DETAILS")
    print("-" * 80)
    print(f"Moon Longitude: {moon_long:.4f}°")
    
    # Calculate Vimshottari Dasha
    dasha_result = dasha_calc.calculate_dasha_at_birth(birth_date, moon_long)
    
    print(f"Birth Nakshatra: {dasha_result.get('birth_nakshatra', 'N/A')}")
    print(f"Balance at Birth: {dasha_result.get('balance_at_birth', 0):.2f} years")
    
    if 'periods' in dasha_result and dasha_result['periods']:
        print(f"\nCurrent Mahadasha (at birth): {dasha_result['periods'][0]['planet']}")
        print(f"Dasha ends: {dasha_result['periods'][0]['end_date']}")
    
    # YOGA DETECTION
    print(f"\n\n✨ YOGA ANALYSIS")
    print("=" * 80)
    print("Detecting all Vedic yogas using classical BPHS/Saravali definitions...")
    print()
    
    yoga_calc = ExtendedYogaCalculator()
    detected_yogas = yoga_calc.calculate_all_yogas(
        planets=planet_positions,
        houses=houses,
        ascendant_sign=ascendant_sign_num
    )
    
    if not detected_yogas:
        print("No major yogas detected in this chart.")
    else:
        # Sort yogas by strength
        detected_yogas.sort(key=lambda y: y.strength, reverse=True)
        
        print(f"Total Yogas Detected: {len(detected_yogas)}\n")
        
        # Group by category
        yoga_categories = {}
        for yoga in detected_yogas:
            cat = yoga.category.value
            if cat not in yoga_categories:
                yoga_categories[cat] = []
            yoga_categories[cat].append(yoga)
        
        print("Yogas by Category:")
        print("-" * 80)
        for category, yogas in sorted(yoga_categories.items()):
            print(f"\n{category.upper().replace('_', ' ')} ({len(yogas)} yogas)")
            print()
            
            for yoga in yogas:
                print(f"  🔹 {yoga.name} ({yoga.sanskrit_name})")
                print(f"     Strength: {yoga.strength}/100 {'🔥' if yoga.strength >= 80 else '⭐' if yoga.strength >= 70 else ''}")
                print(f"     Description: {yoga.description}")
                print(f"     Effects: {', '.join(yoga.effects[:3])}")
                print(f"     Planets: {', '.join(yoga.planets_involved)}")
                print(f"     Houses: {', '.join(map(str, yoga.houses_involved))}")
                if yoga.notes:
                    print(f"     Notes: {yoga.notes}")
                print()
        
        # Highlight top 5 strongest yogas
        print("\n" + "=" * 80)
        print("TOP 5 STRONGEST YOGAS IN YOUR CHART")
        print("=" * 80)
        
        for i, yoga in enumerate(detected_yogas[:5], 1):
            print(f"\n{i}. {yoga.name} (Strength: {yoga.strength}/100)")
            print(f"   Category: {yoga.category.value.title()}")
            print(f"   Description: {yoga.description}")
            print(f"   Classical Effects: {', '.join(yoga.effects)}")
            print(f"   Planets Involved: {', '.join(yoga.planets_involved)}")
            print(f"   Houses: {', '.join(map(str, yoga.houses_involved))}")
            
            # Add interpretation based on category
            if yoga.category.value == "raja":
                print(f"   💡 Interpretation: This Raja Yoga indicates authority and success.")
                print(f"      Peak activation during {yoga.planets_involved[0]} Mahadasha.")
            elif yoga.category.value == "dhana":
                print(f"   💡 Interpretation: This Dhana Yoga indicates wealth potential.")
                print(f"      Financial prosperity through the significations of involved planets.")
            elif yoga.category.value == "mahapurusha":
                print(f"   💡 Interpretation: This Mahapurusha Yoga indicates great personality traits.")
                print(f"      You embody the noble qualities of {yoga.planets_involved[0]}.")
            elif yoga.category.value == "chandra":
                print(f"   💡 Interpretation: This Chandra Yoga relates to emotional and material stability.")
                print(f"      Fixed after classical BPHS compliance (2026-01-17).")
        
        # Summary interpretation
        print("\n" + "=" * 80)
        print("CHART SUMMARY & INTERPRETATION")
        print("=" * 80)
        
        strong_yogas = [y for y in detected_yogas if y.strength >= 75]
        moderate_yogas = [y for y in detected_yogas if 60 <= y.strength < 75]
        
        print(f"\nYoga Strength Distribution:")
        print(f"  Strong Yogas (75-100): {len(strong_yogas)}")
        print(f"  Moderate Yogas (60-74): {len(moderate_yogas)}")
        print(f"  Total Significant: {len(strong_yogas) + len(moderate_yogas)}")
        
        # Check for key yoga types
        has_raja = any(y.category.value == "raja" for y in detected_yogas)
        has_dhana = any(y.category.value == "dhana" for y in detected_yogas)
        has_mahapurusha = any(y.category.value == "mahapurusha" for y in detected_yogas)
        
        print(f"\nKey Yoga Presence:")
        print(f"  Raja Yogas (Authority): {'✅ Present' if has_raja else '❌ Not detected'}")
        print(f"  Dhana Yogas (Wealth): {'✅ Present' if has_dhana else '❌ Not detected'}")
        print(f"  Mahapurusha Yogas: {'✅ Present' if has_mahapurusha else '❌ Not detected'}")
        
        print(f"\n📊 Overall Chart Assessment:")
        if len(strong_yogas) >= 3:
            print("  ⭐⭐⭐ Excellent - Multiple strong yogas indicate significant life blessings")
        elif len(strong_yogas) >= 1:
            print("  ⭐⭐ Good - Strong yogas present with good support")
        elif len(moderate_yogas) >= 3:
            print("  ⭐ Moderate - Several supportive yogas, steady progress")
        else:
            print("  Standard - Focus on overall chart strength and planetary periods")
    
    print("\n" + "=" * 80)
    print("Report generated using:")
    print("  - Lahiri Ayanamsa (standard for Vedic astrology)")
    print("  - Whole Sign House System")
    print("  - Extended Yoga Calculator v1.1.0 (BPHS-compliant)")
    print("  - Classical references: BPHS, Saravali, Phaladeepika")
    print("\nReport Date: 2026-01-17")
    print("=" * 80)


if __name__ == "__main__":
    try:
        generate_yoga_report()
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
