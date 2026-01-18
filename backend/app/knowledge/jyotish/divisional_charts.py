"""
Divisional Charts (Varga Charts)
================================

The 16 divisional charts (Shodasha Varga) reveal different dimensions of life.
Navamsa (D9) is the most important after Rasi (D1).

"D1 shows the PROMISE, Vargas show the FULFILLMENT"
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

# =============================================================================
# THE 16 DIVISIONAL CHARTS (SHODASHA VARGA)
# =============================================================================


@dataclass
class VargaChart:
    division: int
    name: str
    sanskrit: str
    significations: List[str]
    calculation_method: str
    interpretation_notes: str


VARGA_CHARTS: Dict[int, VargaChart] = {
    1: VargaChart(
        1,
        "Rasi",
        "Rashi",
        ["Overall life", "Physical body", "General fortune", "All matters"],
        "Direct sign placement",
        """
        The foundation chart. All other vargas are derived from this.
        Shows the physical manifestation and general life themes.
        """,
    ),
    2: VargaChart(
        2,
        "Hora",
        "Hora",
        ["Wealth", "Financial prosperity", "Accumulation"],
        "Odd signs → Sun (Leo), Even signs → Moon (Cancer)",
        """
        HORA CHART (D2) - WEALTH ANALYSIS
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Only 2 signs used: Leo (Sun's hora) and Cancer (Moon's hora).
        
        Calculation:
        - Odd signs (Ari, Gem, Leo, Lib, Sag, Aqu): 0-15° = Leo, 15-30° = Cancer
        - Even signs (Tau, Can, Vir, Sco, Cap, Pis): 0-15° = Cancer, 15-30° = Leo
        
        Interpretation:
        - More planets in Sun's hora (Leo) = wealth through effort, authority
        - More planets in Moon's hora (Cancer) = wealth through public, inheritance
        - 2nd and 11th lords strong in D2 = good wealth
        - Benefics in Sun's hora = self-earned wealth
        """,
    ),
    3: VargaChart(
        3,
        "Drekkana",
        "Drekkana",
        ["Siblings", "Courage", "Short journeys", "Arms/shoulders"],
        "Each sign divided into 3 parts of 10°",
        """
        DREKKANA CHART (D3) - SIBLINGS & COURAGE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Calculation:
        - 0-10° → Same sign
        - 10-20° → 5th from sign
        - 20-30° → 9th from sign
        
        Interpretation:
        - 3rd house and its lord in D3 = younger siblings
        - 11th house in D3 = elder siblings
        - Mars strength in D3 = courage and initiative
        - Malefics in 3rd of D3 = sibling issues
        """,
    ),
    4: VargaChart(
        4,
        "Chaturthamsa",
        "Chaturthamsha",
        ["Fortune", "Property", "Fixed assets", "Happiness"],
        "Each sign divided into 4 parts of 7°30'",
        """
        CHATURTHAMSA (D4) - PROPERTY & FORTUNE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Calculation:
        - 0-7°30' → Same sign
        - 7°30'-15° → 4th from sign
        - 15°-22°30' → 7th from sign
        - 22°30'-30° → 10th from sign
        
        Interpretation:
        - 4th house in D4 = property and real estate
        - Moon and Venus in D4 = happiness and comfort
        - 4th lord strong = owns property
        - Malefics in 4th of D4 = property disputes
        """,
    ),
    7: VargaChart(
        7,
        "Saptamsa",
        "Saptamsha",
        ["Children", "Progeny", "Creative output"],
        "Each sign divided into 7 parts of 4°17'8\"",
        """
        SAPTAMSA (D7) - CHILDREN
        ━━━━━━━━━━━━━━━━━━━━━━━━
        Calculation:
        - Odd signs: Count from same sign
        - Even signs: Count from 7th sign
        - Each pada = 4°17'8\" (30/7 degrees)
        
        Interpretation:
        - 5th house in D7 = children fortune
        - Jupiter in D7 = blessings for progeny
        - 5th lord strong in D7 = healthy children
        - Afflicted 5th in D7 = difficulties with children
        """,
    ),
    9: VargaChart(
        9,
        "Navamsa",
        "Navamsha",
        ["Marriage", "Spouse", "Dharma", "Fortune", "Spiritual path"],
        "Each sign divided into 9 parts of 3°20'",
        """
        NAVAMSA (D9) - THE MOST IMPORTANT VARGA
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        CALCULATION:
        Starting sign for navamsa counting depends on element:
        - Fire signs (Ari, Leo, Sag): Start from Aries
        - Earth signs (Tau, Vir, Cap): Start from Capricorn
        - Air signs (Gem, Lib, Aqu): Start from Libra
        - Water signs (Can, Sco, Pis): Start from Cancer
        
        Each navamsa = 3°20' (3.333°)
        
        INTERPRETATION PRINCIPLES:
        
        1. NAVAMSA AS FRUIT OF RASI
           - D1 = Tree, D9 = Fruit
           - Strong in D1, weak in D9 = promise without fulfillment
           - Weak in D1, strong in D9 = eventual success after struggle
        
        2. VARGOTTAMA PLANETS
           - Same sign in D1 and D9
           - Extremely powerful - magnified results
           - Like having double confirmation
        
        3. PUSHKARA NAVAMSA
           - Especially auspicious navamsa positions
           - Planets here gain special strength
        
        4. MARRIAGE ANALYSIS IN D9
           - 7th house of D9 = spouse nature
           - D9 Lagna = your behavior in marriage
           - Venus (men) / Jupiter (women) = spouse significator
           - Planets in 7th = energies in marriage
        
        5. NAVAMSA LAGNA ANALYSIS
           - Shows inner self, dharmic path
           - Different from D1 Lagna = different inner/outer personality
           - Same as D1 = integrated personality
        
        6. 64TH NAVAMSA
           - The navamsa 64 positions from Moon's navamsa
           - Considered dangerous for health/longevity
           - Transit here can trigger health issues
        
        SPECIAL NAVAMSA COMBINATIONS:
        
        ★ Vargottama Lagna = Very fortunate life
        ★ Vargottama Moon = Emotional stability
        ★ Venus Vargottama = Happy marriage
        ★ Jupiter Vargottama = Dharmic success
        
        ⚠ Debilitated in D9 = Struggles in that area
        ⚠ 7th lord in 6/8/12 of D9 = Marriage challenges
        ⚠ Malefics in D9 7th = Spouse difficulties
        """,
    ),
    10: VargaChart(
        10,
        "Dasamsa",
        "Dashamsha",
        ["Career", "Profession", "Status", "Power", "Achievement"],
        "Each sign divided into 10 parts of 3°",
        """
        DASAMSA (D10) - CAREER & PROFESSION
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        CALCULATION:
        - Odd signs: Count from same sign
        - Even signs: Count from 9th sign
        - Each pada = 3°
        
        INTERPRETATION:
        
        1. D10 LAGNA
           - How you present professionally
           - Your work style and approach
        
        2. 10TH HOUSE IN D10
           - Type of career success
           - Professional achievements
        
        3. KEY PLANETS IN D10
           - Sun = Authority, government
           - Saturn = Service, hard work
           - Mercury = Business, communication
           - Jupiter = Teaching, consulting
        
        4. D1 10TH LORD IN D10
           - Where it falls shows career direction
           - Strong = professional success
           - Weak = career struggles
        
        5. YOGAS IN D10
           - Raja Yogas here = power and position
           - Dhana Yogas = wealth through career
        """,
    ),
    12: VargaChart(
        12,
        "Dwadasamsa",
        "Dwadashamsha",
        ["Parents", "Lineage", "Ancestry", "Karma from past"],
        "Each sign divided into 12 parts of 2°30'",
        """
        DWADASAMSA (D12) - PARENTS & ANCESTRY
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        CALCULATION:
        - Count from same sign
        - Each pada = 2°30'
        
        INTERPRETATION:
        - 4th house = Mother
        - 9th house = Father
        - Sun in D12 = Father's condition
        - Moon in D12 = Mother's condition
        - Malefics in 4th/9th = Parent difficulties
        """,
    ),
    16: VargaChart(
        16,
        "Shodasamsa",
        "Shodashamsha",
        ["Vehicles", "Conveyances", "Luxuries", "Comforts"],
        "Each sign divided into 16 parts of 1°52'30\"",
        """
        SHODASAMSA (D16) - VEHICLES & LUXURIES
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - 4th house = Vehicles owned
        - Venus = Luxury and comfort
        - Strong D16 = Material comforts
        """,
    ),
    20: VargaChart(
        20,
        "Vimshamsa",
        "Vimshamsha",
        ["Spiritual progress", "Upasana", "Religious pursuits"],
        "Each sign divided into 20 parts of 1°30'",
        """
        VIMSHAMSA (D20) - SPIRITUAL LIFE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - 9th house = Spiritual inclination
        - 12th house = Liberation path
        - Jupiter/Ketu = Spiritual progress
        """,
    ),
    24: VargaChart(
        24,
        "Chaturvimshamsa",
        "Chaturvimshamsha",
        ["Education", "Learning", "Academic success"],
        "Each sign divided into 24 parts of 1°15'",
        """
        CHATURVIMSHAMSA (D24) - EDUCATION
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - 4th house = Basic education
        - 5th house = Higher learning
        - Mercury/Jupiter = Educational success
        """,
    ),
    27: VargaChart(
        27,
        "Nakshatramsa",
        "Bhamsha",
        ["Strengths", "Weaknesses", "Inherent nature"],
        "Each sign divided into 27 parts (nakshatra-based)",
        """
        NAKSHATRAMSA (D27) - INHERENT NATURE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - Shows fundamental strengths/weaknesses
        - Based on nakshatra divisions
        """,
    ),
    30: VargaChart(
        30,
        "Trimshamsa",
        "Trimshamsha",
        ["Misfortunes", "Evils", "Difficulties"],
        "Unequal division based on malefic planets",
        """
        TRIMSHAMSA (D30) - MISFORTUNES
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - Used for identifying potential troubles
        - Different calculation for odd/even signs
        - Important for remedial measures
        """,
    ),
    40: VargaChart(
        40,
        "Khavedamsa",
        "Khavedamsha",
        ["Auspicious/Inauspicious effects", "Overall fortune"],
        "Each sign divided into 40 parts",
        """
        KHAVEDAMSA (D40) - MATRILINEAL LEGACY
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - Mother's side inheritance
        - Overall auspiciousness
        """,
    ),
    45: VargaChart(
        45,
        "Akshavedamsa",
        "Akshavedamsha",
        ["General indications", "Fine-tuning predictions"],
        "Each sign divided into 45 parts",
        """
        AKSHAVEDAMSA (D45) - PATRILINEAL LEGACY
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - Father's side inheritance
        - General well-being
        """,
    ),
    60: VargaChart(
        60,
        "Shashtyamsa",
        "Shashtiamsha",
        ["Past life karma", "Deepest karmic patterns", "Fine destiny"],
        "Each sign divided into 60 parts of 0°30'",
        """
        SHASHTYAMSA (D60) - PAST LIFE KARMA
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        The MOST SUBTLE divisional chart.
        
        - Each D60 portion has a specific deity
        - Shows deepest karmic patterns
        - Used by advanced astrologers
        - Explains "inexplicable" life patterns
        - Very sensitive to accurate birth time
        """,
    ),
}

# =============================================================================
# NAVAMSA CALCULATION FUNCTIONS
# =============================================================================


def calculate_navamsa_sign(longitude: float) -> int:
    """
    Calculate the Navamsa sign for a given longitude.

    Returns: Sign number (1-12)
    """
    sign_num = int(longitude / 30)  # 0-11
    deg_in_sign = longitude % 30
    navamsa_span = 30 / 9  # 3.333... degrees
    navamsa_num = int(deg_in_sign / navamsa_span)  # 0-8

    # Starting sign depends on element
    element = sign_num % 4
    if element == 0:  # Fire (Aries=0, Leo=4, Sag=8)
        start = 0  # Aries
    elif element == 1:  # Earth (Taurus=1, Virgo=5, Cap=9)
        start = 9  # Capricorn
    elif element == 2:  # Air (Gemini=2, Libra=6, Aqua=10)
        start = 6  # Libra
    else:  # Water (Cancer=3, Scorpio=7, Pisces=11)
        start = 3  # Cancer

    navamsa_sign = (start + navamsa_num) % 12
    return navamsa_sign + 1  # Return 1-12


def is_vargottama(rasi_longitude: float) -> bool:
    """Check if a planet is Vargottama (same sign in D1 and D9)"""
    rasi_sign = int(rasi_longitude / 30) % 12 + 1
    navamsa_sign = calculate_navamsa_sign(rasi_longitude)
    return rasi_sign == navamsa_sign


# =============================================================================
# VARGA STRENGTH (VIMSHOPAKA BALA)
# =============================================================================

VIMSHOPAKA_WEIGHTS = {
    # Shad Varga (6 charts)
    "shad_varga": {1: 6, 2: 2, 3: 4, 9: 5, 12: 2, 30: 1},  # Total = 20
    # Sapta Varga (7 charts)
    "sapta_varga": {1: 5, 2: 2, 3: 3, 9: 2.5, 12: 4.5, 30: 2, 7: 1},  # Total = 20
    # Dasa Varga (10 charts)
    "dasa_varga": {1: 3, 2: 1.5, 3: 1.5, 9: 1.5, 12: 1.5, 30: 1.5, 7: 1.5, 10: 1.5, 16: 1.5, 60: 5},
    # Shodasa Varga (16 charts) - Full scheme
    "shodasa_varga": {
        1: 3.5,
        2: 1,
        3: 1,
        4: 0.5,
        7: 0.5,
        9: 3,
        10: 0.5,
        12: 0.5,
        16: 2,
        20: 0.5,
        24: 0.5,
        27: 0.5,
        30: 1,
        40: 0.5,
        45: 0.5,
        60: 4,
    },
}


def get_varga_info(division: int) -> VargaChart:
    """Get information about a specific divisional chart"""
    return VARGA_CHARTS.get(division)


def get_interpretation_for_varga(division: int) -> str:
    """Get detailed interpretation notes for a varga"""
    varga = VARGA_CHARTS.get(division)
    if varga:
        return varga.interpretation_notes
    return "Varga chart information not available"
