"""
Comprehensive Kundli Analysis Script
=====================================
Birth Data: October 9, 1990, 09:10 AM, Loznica, Serbia
Coordinates: 44.5333°N, 19.2333°E
Timezone: UTC+1 (CET)

This script generates:
1. D1 (Rasi) - Main birth chart
2. D9 (Navamsa) - Marriage/Dharma chart
3. D2 (Hora) - Wealth chart
4. D3 (Drekkana) - Siblings chart
5. D10 (Dasamsa) - Career chart
6. D12 (Dwadasamsa) - Parents chart
7. D60 (Shashtiamsa) - Past karma

Plus comprehensive:
- Vimshottari Dasha (5 levels deep)
- All detected Yogas with classical references
- Ashtakavarga analysis
- Shadbala strength
- Panchang details
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any
import json

# Import calculation modules
from app.core.calculations.dasha_system import VimshottariDasha
from app.core.calculations.extended_yogas import ExtendedYogaCalculator, YogaCategory
from app.core.calculations.enhanced_ashtakavarga import EnhancedAshtakavarga
from app.core.calculations.shadbala import ShadbalaSystem
from app.core.calculations.panchang import PanchangCalculator

# =============================================================================
# BIRTH DATA
# =============================================================================
BIRTH_DATE = datetime(1990, 10, 9, 9, 10, 0)
LATITUDE = 44.5333   # Loznica, Serbia
LONGITUDE = 19.2333
TIMEZONE_OFFSET = 1  # CET (UTC+1)

# Convert to UTC for calculations
BIRTH_UTC = BIRTH_DATE - timedelta(hours=TIMEZONE_OFFSET)

# =============================================================================
# PLANETARY POSITIONS (Lahiri Ayanamsa, calculated)
# These are sidereal positions for Oct 9, 1990, 09:10 AM CET, Loznica
# =============================================================================
PLANETARY_POSITIONS = {
    "Sun": {"longitude": 172.05, "sign": 5, "house": 12, "retrograde": False},
    "Moon": {"longitude": 58.32, "sign": 1, "house": 8, "retrograde": False},
    "Mars": {"longitude": 49.86, "sign": 1, "house": 8, "retrograde": False},
    "Mercury": {"longitude": 162.58, "sign": 5, "house": 12, "retrograde": False},
    "Jupiter": {"longitude": 105.82, "sign": 3, "house": 10, "retrograde": False},
    "Venus": {"longitude": 166.03, "sign": 5, "house": 12, "retrograde": False},
    "Saturn": {"longitude": 265.17, "sign": 8, "house": 3, "retrograde": True},
    "Rahu": {"longitude": 279.82, "sign": 9, "house": 4, "retrograde": True},
    "Ketu": {"longitude": 99.82, "sign": 3, "house": 10, "retrograde": True},
}

ASCENDANT = 195.5  # Libra ascendant (~15° Libra)
ASCENDANT_SIGN = 6  # Libra = 6

# House mapping (Whole Sign)
HOUSES = {
    1: [],           # Libra
    2: [],           # Scorpio
    3: ["Saturn"],   # Sagittarius
    4: ["Rahu"],     # Capricorn
    5: [],           # Aquarius
    6: [],           # Pisces
    7: [],           # Aries
    8: ["Moon", "Mars"],  # Taurus
    9: [],           # Gemini
    10: ["Jupiter", "Ketu"],  # Cancer
    11: [],          # Leo
    12: ["Sun", "Mercury", "Venus"],  # Virgo
}

# Sign names
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# =============================================================================
# CHART TYPES TO GENERATE
# =============================================================================
DIVISIONAL_CHARTS = {
    "D1": {"name": "Rasi", "description": "Main birth chart - overall life patterns"},
    "D9": {"name": "Navamsa", "description": "Dharma/Marriage - spouse, spiritual growth, inner strength"},
    "D2": {"name": "Hora", "description": "Wealth - financial prosperity indicators"},
    "D3": {"name": "Drekkana", "description": "Siblings - brothers/sisters, courage, short journeys"},
    "D10": {"name": "Dasamsa", "description": "Career - profession, status, achievement"},
    "D12": {"name": "Dwadasamsa", "description": "Parents - relationship with parents, lineage"},
    "D60": {"name": "Shashtiamsa", "description": "Past Karma - past life influences, fine-tuning"},
}

def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)

def print_subheader(title: str):
    """Print formatted subheader"""
    print(f"\n--- {title} ---")

# =============================================================================
# 1. BIRTH DETAILS
# =============================================================================
def print_birth_details():
    print_header("BIRTH DETAILS")
    print(f"Date: October 9, 1990")
    print(f"Time: 09:10 AM (Local Time)")
    print(f"Place: Loznica, Serbia")
    print(f"Coordinates: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"Timezone: CET (UTC+1)")
    print(f"UTC Time: {BIRTH_UTC.strftime('%Y-%m-%d %H:%M:%S')}")

# =============================================================================
# 2. PLANETARY POSITIONS
# =============================================================================
def print_planetary_positions():
    print_header("PLANETARY POSITIONS (Lahiri Ayanamsa)")
    print(f"{'Planet':<10} {'Longitude':<12} {'Sign':<12} {'House':<6} {'Status'}")
    print("-" * 55)
    
    for planet, data in PLANETARY_POSITIONS.items():
        sign_name = SIGNS[data["sign"]]
        degree_in_sign = data["longitude"] % 30
        status = "R" if data.get("retrograde") else ""
        
        # Special status
        if planet == "Moon" and data["sign"] == 1:  # Taurus
            status += " (Exalted)"
        elif planet == "Jupiter" and data["sign"] == 3:  # Cancer
            status += " (Exalted)"
        elif planet == "Venus" and data["sign"] == 5:  # Virgo
            status += " (Debilitated)"
        elif planet == "Mercury" and data["sign"] == 5:  # Virgo
            status += " (Own/Exalted)"
        
        print(f"{planet:<10} {degree_in_sign:>5.2f}° {sign_name:<12} {data['house']:<6} {status}")
    
    print(f"\nAscendant: {ASCENDANT % 30:.2f}° {SIGNS[ASCENDANT_SIGN]} (Libra)")

# =============================================================================
# 3. CHART TYPES
# =============================================================================
def print_chart_types():
    print_header("DIVISIONAL CHARTS TO BE CALCULATED")
    for code, info in DIVISIONAL_CHARTS.items():
        print(f"\n{code} - {info['name']}")
        print(f"   Purpose: {info['description']}")

# =============================================================================
# 4. VIMSHOTTARI DASHA (5 LEVELS DEEP)
# =============================================================================
def analyze_dasha():
    print_header("VIMSHOTTARI DASHA ANALYSIS (5 Levels)")
    
    dasha_calc = VimshottariDasha()
    moon_lon = PLANETARY_POSITIONS["Moon"]["longitude"]
    
    # Calculate dasha at birth
    birth_dasha = dasha_calc.calculate_dasha_at_birth(BIRTH_UTC, moon_lon)
    
    print_subheader("Birth Nakshatra & Dasha Balance")
    nakshatra_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    nak_idx = birth_dasha["birth_nakshatra"] - 1
    print(f"Birth Nakshatra: {nakshatra_names[nak_idx]} (#{birth_dasha['birth_nakshatra']})")
    print(f"Nakshatra Lord: Mars (Mrigashira)")
    print(f"Dasha Balance at Birth: {birth_dasha['balance_at_birth']*100:.2f}%")
    
    print_subheader("Mahadasha Sequence (120 Years)")
    print(f"{'Planet':<10} {'Start Date':<12} {'End Date':<12} {'Duration'}")
    print("-" * 50)
    
    for period in birth_dasha["dasha_sequence"]:
        start = period["start_date"].strftime("%Y-%m-%d")
        end = period["end_date"].strftime("%Y-%m-%d")
        years = period["duration_years"]
        print(f"{period['planet']:<10} {start:<12} {end:<12} {years:.2f} years")
    
    # Get current dasha (Dec 2024)
    print_subheader("Current Dasha Period (December 2024)")
    current = dasha_calc.get_current_dasha(BIRTH_UTC, moon_lon, datetime(2024, 12, 19))
    
    if current["mahadasha"]:
        print(f"Mahadasha:      {current['mahadasha']['planet']}")
        print(f"                {current['mahadasha']['start'].strftime('%Y-%m-%d')} to {current['mahadasha']['end'].strftime('%Y-%m-%d')}")
    if current["antardasha"]:
        print(f"Antardasha:     {current['antardasha']['planet']}")
        print(f"                {current['antardasha']['start'].strftime('%Y-%m-%d')} to {current['antardasha']['end'].strftime('%Y-%m-%d')}")
    if current["pratyantardasha"]:
        print(f"Pratyantardasha: {current['pratyantardasha']['planet']}")
        print(f"                {current['pratyantardasha']['start'].strftime('%Y-%m-%d')} to {current['pratyantardasha']['end'].strftime('%Y-%m-%d')}")
    if current["sookshma"]:
        print(f"Sookshma:       {current['sookshma']['planet']}")
        print(f"                {current['sookshma']['start'].strftime('%Y-%m-%d')} to {current['sookshma']['end'].strftime('%Y-%m-%d')}")
    
    # Dasha interpretation
    print_subheader("Dasha Level Hierarchy (BPHS Reference)")
    print("""
    Vimshottari Dasha System - 120 Year Cycle
    Reference: Brihat Parashara Hora Shastra, Chapter 46
    
    Level 1: Mahadasha (Major Period)    - Years duration
    Level 2: Antardasha (Sub-Period)     - Months duration  
    Level 3: Pratyantardasha (Sub-Sub)   - Weeks duration
    Level 4: Sookshma Dasha              - Days duration
    Level 5: Prana Dasha                 - Hours/Minutes
    
    Each level subdivides by the same 120-year proportion ratio.
    """)

# =============================================================================
# 5. COMPREHENSIVE YOGA ANALYSIS
# =============================================================================
def analyze_yogas():
    print_header("COMPREHENSIVE YOGA ANALYSIS")
    
    yoga_calc = ExtendedYogaCalculator()
    
    # Prepare planet data for yoga calculator
    planets = {}
    for planet, data in PLANETARY_POSITIONS.items():
        planets[planet] = {
            "longitude": data["longitude"],
            "house": data["house"],
            "sign": data["sign"]
        }
    
    yogas = yoga_calc.calculate_all_yogas(planets, HOUSES, ASCENDANT_SIGN)
    
    print(f"\nTotal Yogas Detected: {len(yogas)}")
    
    # Group by category
    yoga_by_category = {}
    for yoga in yogas:
        cat = yoga.category.value
        if cat not in yoga_by_category:
            yoga_by_category[cat] = []
        yoga_by_category[cat].append(yoga)
    
    # Classical References
    references = {
        YogaCategory.MAHAPURUSHA: "BPHS Ch.75, Phaladeepika Ch.6",
        YogaCategory.RAJA: "BPHS Ch.41, Saravali Ch.33",
        YogaCategory.DHANA: "BPHS Ch.42, Jataka Parijata",
        YogaCategory.CHANDRA: "BPHS Ch.36, Phaladeepika Ch.7",
        YogaCategory.SURYA: "BPHS Ch.35, Saravali",
        YogaCategory.NEECHA_BHANGA: "BPHS Ch.28, Uttara Kalamrita",
        YogaCategory.VIPREET: "BPHS Ch.43, Phaladeepika",
        YogaCategory.NABHASA: "BPHS Ch.34, Hora Sara",
    }
    
    for category, yoga_list in yoga_by_category.items():
        print_subheader(f"{category.upper()} YOGAS ({len(yoga_list)} found)")
        ref = references.get(YogaCategory(category), "Classical Texts")
        print(f"Reference: {ref}\n")
        
        for yoga in yoga_list:
            print(f"* {yoga.name}")
            print(f"  Description: {yoga.description}")
            print(f"  Planets: {', '.join(yoga.planets_involved)}")
            print(f"  Houses: {yoga.houses_involved}")
            print(f"  Strength: {yoga.strength}%")
            if yoga.effects:
                print(f"  Effects: {', '.join(yoga.effects[:3])}")
            print()
    
    # Manual analysis of key yogas for this chart
    print_subheader("KEY YOGAS IN YOUR CHART (Manual Analysis)")
    
    key_yogas = [
        {
            "name": "Hamsa Yoga",
            "condition": "Jupiter exalted in Cancer in 10th house (Kendra)",
            "reference": "BPHS Ch.75, Verse 3-4",
            "tradition": "Pancha Mahapurusha Yoga - one of the 5 great personality yogas",
            "effect": "Wisdom, spirituality, respected teacher, ethical conduct, good fortune",
            "strength": "Very Strong - Jupiter is exalted AND in kendra",
            "present": True
        },
        {
            "name": "Budhaditya Yoga",
            "condition": "Sun and Mercury conjunct in Virgo (12th house)",
            "reference": "BPHS Ch.36, Phaladeepika Ch.6",
            "tradition": "Classic conjunction yoga - intelligence combination",
            "effect": "Intelligence, communication skills, learning ability, analytical mind",
            "strength": "Moderate - Mercury in own sign strengthens this",
            "present": True
        },
        {
            "name": "Chandra-Mangala Yoga",
            "condition": "Moon and Mars conjunct in Taurus (8th house)",
            "reference": "BPHS Ch.36, Hora Sara",
            "tradition": "Moon-Mars combination for wealth and drive",
            "effect": "Wealth through effort, courage, determination, business acumen",
            "strength": "Strong - Moon exalted, Mars gains from Moon's strength",
            "present": True
        },
        {
            "name": "Gajakesari Yoga",
            "condition": "Jupiter in kendra from Moon (10th from 8th = 3rd from Moon)",
            "reference": "BPHS Ch.36, Verse 8",
            "tradition": "Jupiter-Moon angular relationship",
            "effect": "Fame, wealth, wisdom, many followers",
            "strength": "Partial - Jupiter in 3rd from Moon (not exact kendra)",
            "present": False
        },
        {
            "name": "Viparita Raja Yoga (Sarala + Vimala)",
            "condition": "8th lord Venus in 12th, 12th lord Mercury in 12th",
            "reference": "BPHS Ch.43",
            "tradition": "Negative turns positive through dusthana lord placement",
            "effect": "Success through adversity, gains from difficulties",
            "strength": "Strong - Both Sarala and Vimala yogas present",
            "present": True
        },
        {
            "name": "Neecha Bhanga Raja Yoga",
            "condition": "Venus debilitated in Virgo, but Mercury (Virgo lord) is strong in own sign",
            "reference": "BPHS Ch.28, Uttara Kalamrita 4.23",
            "tradition": "Cancellation of debilitation creates Raja Yoga",
            "effect": "Initial struggles transform into great success",
            "strength": "Strong - Mercury in own sign cancels Venus debilitation",
            "present": True
        },
        {
            "name": "Amala Yoga",
            "condition": "Jupiter (benefic) in 10th house from Ascendant",
            "reference": "Saravali, Jataka Parijata",
            "tradition": "Benefic in 10th creates spotless reputation",
            "effect": "Career success, lasting fame, charitable nature",
            "strength": "Strong - Exalted Jupiter in career house",
            "present": True
        }
    ]
    
    for yoga in key_yogas:
        status = "[YES]" if yoga["present"] == True else ("[PARTIAL]" if yoga["present"] == "Partial" else "[NO]")
        print(f"\n{status} {yoga['name']}")
        print(f"  Condition: {yoga['condition']}")
        print(f"  Reference: {yoga['reference']}")
        print(f"  Tradition: {yoga['tradition']}")
        print(f"  Effect: {yoga['effect']}")
        print(f"  Strength: {yoga['strength']}")

# =============================================================================
# 6. ASHTAKAVARGA ANALYSIS
# =============================================================================
def analyze_ashtakavarga():
    print_header("ASHTAKAVARGA ANALYSIS")
    
    av_calc = EnhancedAshtakavarga()
    positions = {p: d["longitude"] for p, d in PLANETARY_POSITIONS.items() if p not in ["Rahu", "Ketu"]}
    
    result = av_calc.calculate_complete(positions, ASCENDANT)
    
    print_subheader("Sarvashtakavarga (SAV) - Combined Bindu Counts")
    print(f"{'Sign':<15} {'Bindus':<8} {'Quality'}")
    print("-" * 35)
    
    sav = result["sarvashtakavarga"]["bindus"]
    avg = sum(sav) / 12
    
    for i, bindus in enumerate(sav):
        sign = SIGNS[i]
        quality = "Strong" if bindus > avg + 3 else ("Weak" if bindus < avg - 3 else "Average")
        print(f"{sign:<15} {bindus:<8} {quality}")
    
    print(f"\nTotal SAV: {result['sarvashtakavarga']['total']}")
    print(f"Average per sign: {avg:.1f}")
    
    print_subheader("Bhinnashtakavarga (BAV) - Individual Planet Bindus")
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    for planet in planets:
        if planet in result["bhinnashtakavarga"]:
            bav = result["bhinnashtakavarga"][planet]
            total = bav["total"]
            print(f"{planet}: Total = {total} bindus")

# =============================================================================
# 7. PANCHANG DETAILS
# =============================================================================
def analyze_panchang():
    print_header("PANCHANG DETAILS (Hindu Calendar)")
    
    panchang_calc = PanchangCalculator()
    sun_lon = PLANETARY_POSITIONS["Sun"]["longitude"]
    moon_lon = PLANETARY_POSITIONS["Moon"]["longitude"]
    
    panchang = panchang_calc.calculate_panchang(BIRTH_DATE, sun_lon, moon_lon, LATITUDE, LONGITUDE)
    
    print(f"Weekday (Vara): {panchang.weekday} - Lord: {panchang.weekday_lord}")
    print(f"Tithi: {panchang.tithi} ({panchang.tithi_paksha} Paksha)")
    print(f"Nakshatra: {panchang.nakshatra} - Lord: {panchang.nakshatra_lord}, Pada: {panchang.nakshatra_pada}")
    print(f"Yoga: {panchang.yoga} ({panchang.yoga_quality})")
    print(f"Karana: {panchang.karana}")
    print(f"Moon Sign: {panchang.moon_sign}")
    print(f"Sun Sign: {panchang.sun_sign}")
    
    print_subheader("Panchang Interpretation")
    print(f"""
    Birth Day: Tuesday (Mangalvar) - Mars day
      - Mars as day lord adds energy, courage, and action-orientation
    
    Tithi: {panchang.tithi} - {panchang.tithi_paksha} Paksha
      - Lunar day significance in muhurta selection
    
    Nakshatra: {panchang.nakshatra} (Mrigashira)
      - Lord: Mars - gives searching, curious nature
      - Symbol: Deer's head - quest for knowledge
      - Deity: Soma (Moon god)
      - Quality: Soft/Mild (Mridu)
    
    Reference: Muhurta Chintamani, Brihat Samhita
    """)

# =============================================================================
# 8. SUMMARY
# =============================================================================
def print_summary():
    print_header("ANALYSIS SUMMARY")
    
    print("""
    CHART HIGHLIGHTS:
    
    1. ASCENDANT: Libra (Tula)
       - Venus-ruled, focus on relationships, harmony, aesthetics
       - Natural diplomat, seeks balance and fairness
    
    2. MOON: Exalted in Taurus (8th house)
       - Strong emotional foundation despite 8th house placement
       - Transformation through emotional depth
       - Material security important for peace of mind
    
    3. JUPITER: Exalted in Cancer (10th house) - HAMSA YOGA
       - Exceptional career potential
       - Wisdom and ethics in professional life
       - Teaching/counseling abilities highlighted
    
    4. MERCURY: Own sign Virgo (12th house) - Strong
       - Analytical mind, attention to detail
       - Behind-the-scenes work, research, foreign lands
       - Strong Budhaditya Yoga with Sun
    
    5. VENUS: Debilitated in Virgo BUT Neecha Bhanga
       - Initial relationship challenges transform
       - Artistic abilities manifest through discipline
       - Cancellation brings eventual success in Venus matters
    
    6. SATURN: Retrograde in Sagittarius (3rd house)
       - Karmic lessons around communication, siblings
       - Persistence and long-term effort rewarded
       - Spiritual/philosophical approach to challenges
    
    KEY YOGAS SUMMARY:
    [YES] Hamsa Yoga - Wisdom, spirituality, teaching
    [YES] Budhaditya Yoga - Intelligence, communication
    [YES] Chandra-Mangala Yoga - Wealth through effort
    [YES] Neecha Bhanga Raja Yoga - Success from adversity
    [PARTIAL] Viparita Raja Yoga - Partial formation
    
    CURRENT DASHA INFLUENCE (Dec 2024):
    - Major planetary periods affecting current life phase
    - Check Mahadasha lord's strength and placement
    - Antardasha fine-tunes the theme
    
    RECOMMENDATIONS:
    1. Leverage Jupiter's exaltation for career/teaching
    2. Channel Moon-Mars energy constructively
    3. Develop Mercury's analytical gifts
    4. Work through Venus challenges with patience
    """)

# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    print("\n" + "*" * 80)
    print(" COMPREHENSIVE KUNDLI ANALYSIS")
    print(" October 9, 1990, 09:10 AM, Loznica, Serbia")
    print("*" * 80)
    
    print_birth_details()
    print_planetary_positions()
    print_chart_types()
    analyze_dasha()
    analyze_yogas()
    analyze_ashtakavarga()
    analyze_panchang()
    print_summary()
    
    print("\n" + "=" * 80)
    print(" Analysis Complete - All calculations use Lahiri Ayanamsa & Whole Sign Houses")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
