"""
Jyotish Fundamentals
====================

Core building blocks of Vedic astrology based on classical texts:
- Brihat Parashara Hora Shastra (BPHS)
- Brihat Jataka
- Phaladeepika
- Jataka Parijata
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# SIGNS (RASHIS)
# =============================================================================

class Element(Enum):
    FIRE = "fire"      # Agni tattva - action, initiative
    EARTH = "earth"    # Prithvi tattva - stability, material
    AIR = "air"        # Vayu tattva - intellect, movement
    WATER = "water"    # Jala tattva - emotion, intuition

class Modality(Enum):
    MOVABLE = "chara"      # Cardinal - initiating, active
    FIXED = "sthira"       # Fixed - stable, persistent
    DUAL = "dwiswabhava"   # Mutable - adaptable, flexible

@dataclass
class Sign:
    number: int           # 1-12
    name: str
    sanskrit: str
    symbol: str
    element: Element
    modality: Modality
    ruler: str
    body_part: str
    direction: str
    nature: str           # Benefic/Malefic/Neutral
    gender: str           # Male/Female

SIGNS: Dict[int, Sign] = {
    1: Sign(1, "Aries", "Mesha", "♈", Element.FIRE, Modality.MOVABLE, 
            "Mars", "Head", "East", "Malefic", "Male"),
    2: Sign(2, "Taurus", "Vrishabha", "♉", Element.EARTH, Modality.FIXED,
            "Venus", "Face/Throat", "South", "Benefic", "Female"),
    3: Sign(3, "Gemini", "Mithuna", "♊", Element.AIR, Modality.DUAL,
            "Mercury", "Arms/Shoulders", "West", "Neutral", "Male"),
    4: Sign(4, "Cancer", "Karka", "♋", Element.WATER, Modality.MOVABLE,
            "Moon", "Chest/Heart", "North", "Benefic", "Female"),
    5: Sign(5, "Leo", "Simha", "♌", Element.FIRE, Modality.FIXED,
            "Sun", "Stomach", "East", "Malefic", "Male"),
    6: Sign(6, "Virgo", "Kanya", "♍", Element.EARTH, Modality.DUAL,
            "Mercury", "Intestines", "South", "Neutral", "Female"),
    7: Sign(7, "Libra", "Tula", "♎", Element.AIR, Modality.MOVABLE,
            "Venus", "Lower Abdomen", "West", "Benefic", "Male"),
    8: Sign(8, "Scorpio", "Vrischika", "♏", Element.WATER, Modality.FIXED,
            "Mars", "Genitals", "North", "Malefic", "Female"),
    9: Sign(9, "Sagittarius", "Dhanu", "♐", Element.FIRE, Modality.DUAL,
            "Jupiter", "Thighs", "East", "Benefic", "Male"),
    10: Sign(10, "Capricorn", "Makara", "♑", Element.EARTH, Modality.MOVABLE,
             "Saturn", "Knees", "South", "Malefic", "Female"),
    11: Sign(11, "Aquarius", "Kumbha", "♒", Element.AIR, Modality.FIXED,
             "Saturn", "Calves/Ankles", "West", "Neutral", "Male"),
    12: Sign(12, "Pisces", "Meena", "♓", Element.WATER, Modality.DUAL,
             "Jupiter", "Feet", "North", "Benefic", "Female"),
}

# =============================================================================
# PLANETS (GRAHAS)
# =============================================================================

@dataclass
class Planet:
    name: str
    sanskrit: str
    symbol: str
    nature: str           # Natural benefic/malefic
    gender: str
    element: Element
    owns: List[int]       # Signs owned
    exaltation: int       # Sign of exaltation
    exalt_degree: float   # Exact degree of deep exaltation
    debilitation: int     # Sign of debilitation
    moolatrikona: int     # Moolatrikona sign
    mt_degrees: Tuple[float, float]  # Moolatrikona degree range
    friends: List[str]
    enemies: List[str]
    neutrals: List[str]
    karaka: List[str]     # Natural significations

PLANETS: Dict[str, Planet] = {
    "Sun": Planet(
        "Sun", "Surya", "☉", "Malefic", "Male", Element.FIRE,
        owns=[5], exaltation=1, exalt_degree=10, debilitation=7,
        moolatrikona=5, mt_degrees=(0, 20),
        friends=["Moon", "Mars", "Jupiter"],
        enemies=["Venus", "Saturn"],
        neutrals=["Mercury"],
        karaka=["Soul", "Father", "Authority", "Government", "Health", "Ego", "Vitality"]
    ),
    "Moon": Planet(
        "Moon", "Chandra", "☽", "Benefic", "Female", Element.WATER,
        owns=[4], exaltation=2, exalt_degree=3, debilitation=8,
        moolatrikona=2, mt_degrees=(3, 30),
        friends=["Sun", "Mercury"],
        enemies=[],
        neutrals=["Mars", "Jupiter", "Venus", "Saturn"],
        karaka=["Mind", "Mother", "Emotions", "Public", "Water", "Travel", "Fertility"]
    ),
    "Mars": Planet(
        "Mars", "Mangala", "♂", "Malefic", "Male", Element.FIRE,
        owns=[1, 8], exaltation=10, exalt_degree=28, debilitation=4,
        moolatrikona=1, mt_degrees=(0, 12),
        friends=["Sun", "Moon", "Jupiter"],
        enemies=["Mercury"],
        neutrals=["Venus", "Saturn"],
        karaka=["Energy", "Courage", "Brothers", "Property", "Surgery", "Police", "Competition"]
    ),
    "Mercury": Planet(
        "Mercury", "Budha", "☿", "Neutral", "Neutral", Element.EARTH,
        owns=[3, 6], exaltation=6, exalt_degree=15, debilitation=12,
        moolatrikona=6, mt_degrees=(15, 20),
        friends=["Sun", "Venus"],
        enemies=["Moon"],
        neutrals=["Mars", "Jupiter", "Saturn"],
        karaka=["Intelligence", "Speech", "Commerce", "Writing", "Mathematics", "Skin", "Nervous System"]
    ),
    "Jupiter": Planet(
        "Jupiter", "Guru", "♃", "Benefic", "Male", Element.AIR,
        owns=[9, 12], exaltation=4, exalt_degree=5, debilitation=10,
        moolatrikona=9, mt_degrees=(0, 10),
        friends=["Sun", "Moon", "Mars"],
        enemies=["Mercury", "Venus"],
        neutrals=["Saturn"],
        karaka=["Wisdom", "Children", "Guru", "Wealth", "Dharma", "Husband", "Fortune", "Expansion"]
    ),
    "Venus": Planet(
        "Venus", "Shukra", "♀", "Benefic", "Female", Element.WATER,
        owns=[2, 7], exaltation=12, exalt_degree=27, debilitation=6,
        moolatrikona=7, mt_degrees=(0, 15),
        friends=["Mercury", "Saturn"],
        enemies=["Sun", "Moon"],
        neutrals=["Mars", "Jupiter"],
        karaka=["Love", "Marriage", "Wife", "Beauty", "Art", "Luxury", "Vehicles", "Pleasure"]
    ),
    "Saturn": Planet(
        "Saturn", "Shani", "♄", "Malefic", "Neutral", Element.AIR,
        owns=[10, 11], exaltation=7, exalt_degree=20, debilitation=1,
        moolatrikona=11, mt_degrees=(0, 20),
        friends=["Mercury", "Venus"],
        enemies=["Sun", "Moon", "Mars"],
        neutrals=["Jupiter"],
        karaka=["Longevity", "Discipline", "Servants", "Delays", "Karma", "Old Age", "Death", "Sorrow"]
    ),
    "Rahu": Planet(
        "Rahu", "Rahu", "☊", "Malefic", "Male", Element.AIR,
        owns=[], exaltation=2, exalt_degree=20, debilitation=8,
        moolatrikona=0, mt_degrees=(0, 0),  # No MT for nodes
        friends=["Venus", "Saturn"],
        enemies=["Sun", "Moon", "Mars"],
        neutrals=["Mercury", "Jupiter"],
        karaka=["Illusion", "Foreign", "Obsession", "Technology", "Paternal Grandfather", "Poison"]
    ),
    "Ketu": Planet(
        "Ketu", "Ketu", "☋", "Malefic", "Neutral", Element.FIRE,
        owns=[], exaltation=8, exalt_degree=20, debilitation=2,
        moolatrikona=0, mt_degrees=(0, 0),
        friends=["Mars", "Venus", "Saturn"],
        enemies=["Sun", "Moon"],
        neutrals=["Mercury", "Jupiter"],
        karaka=["Liberation", "Spirituality", "Past Life", "Maternal Grandfather", "Mysticism", "Detachment"]
    ),
}

# =============================================================================
# HOUSES (BHAVAS)
# =============================================================================

@dataclass
class House:
    number: int
    name: str
    sanskrit: str
    trikona: bool         # 1, 5, 9 - Dharma trikona (fortune)
    kendra: bool          # 1, 4, 7, 10 - Angular (strength)
    dusthana: bool        # 6, 8, 12 - Difficult houses
    upachaya: bool        # 3, 6, 10, 11 - Growth houses
    maraka: bool          # 2, 7 - Death-inflicting
    significations: List[str]
    body_part: str
    karaka: str           # Natural significator planet

HOUSES: Dict[int, House] = {
    1: House(1, "Ascendant", "Lagna", True, True, False, False, False,
             ["Self", "Body", "Personality", "Health", "Beginning", "Head", "Fame", "Appearance"],
             "Head", "Sun"),
    2: House(2, "Wealth", "Dhana", False, False, False, False, True,
             ["Wealth", "Family", "Speech", "Food", "Face", "Right Eye", "Early Education", "Death"],
             "Face/Mouth", "Jupiter"),
    3: House(3, "Siblings", "Sahaja", False, False, False, True, False,
             ["Siblings", "Courage", "Short Travel", "Communication", "Arms", "Neighbors", "Efforts"],
             "Arms/Shoulders", "Mars"),
    4: House(4, "Mother", "Sukha", False, True, False, False, False,
             ["Mother", "Home", "Property", "Vehicles", "Education", "Peace", "Heart", "Happiness"],
             "Chest/Heart", "Moon"),
    5: House(5, "Children", "Putra", True, False, False, False, False,
             ["Children", "Intelligence", "Creativity", "Romance", "Speculation", "Past Merit", "Mantras"],
             "Stomach", "Jupiter"),
    6: House(6, "Enemies", "Ari", False, False, True, True, False,
             ["Enemies", "Disease", "Debts", "Service", "Obstacles", "Maternal Uncle", "Pets"],
             "Intestines", "Mars/Saturn"),
    7: House(7, "Spouse", "Kalatra", False, True, False, False, True,
             ["Marriage", "Partnership", "Business", "Public", "Foreign Travel", "Death"],
             "Lower Abdomen", "Venus"),
    8: House(8, "Longevity", "Ayu", False, False, True, False, False,
             ["Death", "Transformation", "Inheritance", "Occult", "Chronic Disease", "In-Laws", "Research"],
             "Genitals", "Saturn"),
    9: House(9, "Fortune", "Dharma", True, False, False, False, False,
             ["Father", "Guru", "Fortune", "Religion", "Higher Education", "Long Travel", "Dharma"],
             "Thighs", "Jupiter/Sun"),
    10: House(10, "Career", "Karma", False, True, False, True, False,
              ["Career", "Status", "Authority", "Government", "Fame", "Father", "Knee"],
              "Knees", "Sun/Saturn/Mercury"),
    11: House(11, "Gains", "Labha", False, False, False, True, False,
              ["Gains", "Income", "Elder Siblings", "Friends", "Hopes", "Ankles", "Networks"],
              "Calves/Ankles", "Jupiter"),
    12: House(12, "Loss", "Vyaya", False, False, True, False, False,
              ["Loss", "Expenses", "Liberation", "Foreign", "Sleep", "Hospital", "Isolation", "Bed Pleasures"],
              "Feet", "Saturn"),
}

# =============================================================================
# NAKSHATRAS (27 LUNAR MANSIONS)
# =============================================================================

@dataclass
class Nakshatra:
    number: int
    name: str
    deity: str
    symbol: str
    ruler: str            # Vimshottari dasha lord
    pada_signs: List[str] # Signs of 4 padas
    nature: str           # Deva/Manushya/Rakshasa
    gana: str
    animal: str           # Yoni (sexual compatibility)
    quality: str

NAKSHATRAS: Dict[int, Nakshatra] = {
    1: Nakshatra(1, "Ashwini", "Ashwini Kumaras", "Horse Head", "Ketu",
                 ["Aries", "Aries", "Aries", "Taurus"], "Deva", "Deva", "Horse", "Swift/Light"),
    2: Nakshatra(2, "Bharani", "Yama", "Yoni", "Venus",
                 ["Aries", "Aries", "Aries", "Aries"], "Manushya", "Manushya", "Elephant", "Fierce"),
    3: Nakshatra(3, "Krittika", "Agni", "Razor/Flame", "Sun",
                 ["Aries", "Taurus", "Taurus", "Taurus"], "Rakshasa", "Rakshasa", "Goat", "Mixed"),
    4: Nakshatra(4, "Rohini", "Brahma", "Chariot/Ox Cart", "Moon",
                 ["Taurus", "Taurus", "Taurus", "Taurus"], "Manushya", "Manushya", "Serpent", "Fixed"),
    5: Nakshatra(5, "Mrigashira", "Soma", "Deer Head", "Mars",
                 ["Taurus", "Gemini", "Gemini", "Gemini"], "Deva", "Deva", "Serpent", "Soft"),
    6: Nakshatra(6, "Ardra", "Rudra", "Teardrop", "Rahu",
                 ["Gemini", "Gemini", "Gemini", "Gemini"], "Manushya", "Manushya", "Dog", "Sharp"),
    7: Nakshatra(7, "Punarvasu", "Aditi", "Bow/Quiver", "Jupiter",
                 ["Gemini", "Cancer", "Cancer", "Cancer"], "Deva", "Deva", "Cat", "Movable"),
    8: Nakshatra(8, "Pushya", "Brihaspati", "Flower/Circle", "Saturn",
                 ["Cancer", "Cancer", "Cancer", "Cancer"], "Deva", "Deva", "Goat", "Light"),
    9: Nakshatra(9, "Ashlesha", "Nagas", "Coiled Serpent", "Mercury",
                 ["Cancer", "Cancer", "Cancer", "Cancer"], "Rakshasa", "Rakshasa", "Cat", "Sharp"),
    10: Nakshatra(10, "Magha", "Pitris", "Throne", "Ketu",
                  ["Leo", "Leo", "Leo", "Leo"], "Rakshasa", "Rakshasa", "Rat", "Fierce"),
    11: Nakshatra(11, "Purva Phalguni", "Bhaga", "Hammock/Bed", "Venus",
                  ["Leo", "Leo", "Leo", "Leo"], "Manushya", "Manushya", "Rat", "Fierce"),
    12: Nakshatra(12, "Uttara Phalguni", "Aryaman", "Bed/Legs", "Sun",
                  ["Leo", "Virgo", "Virgo", "Virgo"], "Manushya", "Manushya", "Cow", "Fixed"),
    13: Nakshatra(13, "Hasta", "Savitar", "Hand/Fist", "Moon",
                  ["Virgo", "Virgo", "Virgo", "Virgo"], "Deva", "Deva", "Buffalo", "Light"),
    14: Nakshatra(14, "Chitra", "Vishwakarma", "Pearl/Jewel", "Mars",
                  ["Virgo", "Libra", "Libra", "Libra"], "Rakshasa", "Rakshasa", "Tiger", "Soft"),
    15: Nakshatra(15, "Swati", "Vayu", "Coral/Sword", "Rahu",
                  ["Libra", "Libra", "Libra", "Libra"], "Deva", "Deva", "Buffalo", "Movable"),
    16: Nakshatra(16, "Vishakha", "Indra-Agni", "Archway/Potter", "Jupiter",
                  ["Libra", "Scorpio", "Scorpio", "Scorpio"], "Rakshasa", "Rakshasa", "Tiger", "Mixed"),
    17: Nakshatra(17, "Anuradha", "Mitra", "Lotus/Staff", "Saturn",
                  ["Scorpio", "Scorpio", "Scorpio", "Scorpio"], "Deva", "Deva", "Deer", "Soft"),
    18: Nakshatra(18, "Jyeshtha", "Indra", "Earring/Umbrella", "Mercury",
                  ["Scorpio", "Scorpio", "Scorpio", "Scorpio"], "Rakshasa", "Rakshasa", "Deer", "Sharp"),
    19: Nakshatra(19, "Mula", "Nirriti", "Roots/Tail", "Ketu",
                  ["Sagittarius", "Sagittarius", "Sagittarius", "Sagittarius"], "Rakshasa", "Rakshasa", "Dog", "Sharp"),
    20: Nakshatra(20, "Purva Ashadha", "Apas", "Fan/Tusk", "Venus",
                  ["Sagittarius", "Sagittarius", "Sagittarius", "Sagittarius"], "Manushya", "Manushya", "Monkey", "Fierce"),
    21: Nakshatra(21, "Uttara Ashadha", "Vishvadevas", "Elephant Tusk", "Sun",
                  ["Sagittarius", "Capricorn", "Capricorn", "Capricorn"], "Manushya", "Manushya", "Mongoose", "Fixed"),
    22: Nakshatra(22, "Shravana", "Vishnu", "Ear/Footprints", "Moon",
                  ["Capricorn", "Capricorn", "Capricorn", "Capricorn"], "Deva", "Deva", "Monkey", "Movable"),
    23: Nakshatra(23, "Dhanishta", "Vasus", "Drum/Flute", "Mars",
                  ["Capricorn", "Aquarius", "Aquarius", "Aquarius"], "Rakshasa", "Rakshasa", "Lion", "Movable"),
    24: Nakshatra(24, "Shatabhisha", "Varuna", "Circle/100 Stars", "Rahu",
                  ["Aquarius", "Aquarius", "Aquarius", "Aquarius"], "Rakshasa", "Rakshasa", "Horse", "Movable"),
    25: Nakshatra(25, "Purva Bhadrapada", "Aja Ekapada", "Sword/Bed", "Jupiter",
                  ["Aquarius", "Pisces", "Pisces", "Pisces"], "Manushya", "Manushya", "Lion", "Fierce"),
    26: Nakshatra(26, "Uttara Bhadrapada", "Ahir Budhnya", "Twins/Bed", "Saturn",
                  ["Pisces", "Pisces", "Pisces", "Pisces"], "Manushya", "Manushya", "Cow", "Fixed"),
    27: Nakshatra(27, "Revati", "Pushan", "Fish/Drum", "Mercury",
                  ["Pisces", "Pisces", "Pisces", "Pisces"], "Deva", "Deva", "Elephant", "Soft"),
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_sign_from_longitude(longitude: float) -> Sign:
    """Get sign data from absolute longitude"""
    sign_num = int(longitude / 30) % 12 + 1
    return SIGNS[sign_num]

def get_nakshatra_from_longitude(longitude: float) -> Tuple[Nakshatra, int]:
    """Get nakshatra and pada from longitude"""
    nak_span = 360 / 27  # 13.333...
    nak_idx = int(longitude / nak_span) % 27 + 1
    pada_span = nak_span / 4
    pada = int((longitude % nak_span) / pada_span) + 1
    return NAKSHATRAS[nak_idx], pada

def get_house_lord(house_num: int, asc_sign: int) -> str:
    """Get the lord of a house given ascendant sign"""
    house_sign = ((asc_sign - 1) + (house_num - 1)) % 12 + 1
    return SIGNS[house_sign].ruler

def is_benefic(planet: str, moon_sign: Optional[int] = None) -> bool:
    """
    Determine if planet is benefic.
    Moon is benefic when waxing (shukla paksha).
    Mercury is benefic when not conjunct malefics.
    """
    natural_benefics = ["Jupiter", "Venus"]
    if planet in natural_benefics:
        return True
    if planet == "Moon" and moon_sign:
        # Simplified - waxing moon is benefic
        return True  # Would need Sun position to calculate properly
    return False

def get_element(sign_num: int) -> Element:
    """Get element of a sign"""
    return SIGNS[sign_num].element

def get_modality(sign_num: int) -> Modality:
    """Get modality of a sign"""
    return SIGNS[sign_num].modality
