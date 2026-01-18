"""
Planetary Dignities & Strengths
===============================

Classical dignity system from Brihat Parashara Hora Shastra (BPHS).
Understanding planetary strength is FUNDAMENTAL to chart interpretation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

# =============================================================================
# DIGNITY HIERARCHY (Most to Least Powerful)
# =============================================================================


class Dignity(Enum):
    """
    Planetary dignity levels from strongest to weakest.

    EXALTATION (Uchcha): Planet at peak power, like a king in his glory
    MOOLATRIKONA: Planet in its office, doing its best work
    OWN_SIGN (Swakshetra): Planet at home, comfortable and strong
    FRIENDLY: Planet in friend's house, supported
    NEUTRAL: Planet in neutral territory
    ENEMY: Planet in enemy's house, challenged
    DEBILITATION (Neecha): Planet at weakest, like a king in exile
    """

    EXALTED = "exalted"
    MOOLATRIKONA = "moolatrikona"
    OWN_SIGN = "own_sign"
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"
    ENEMY = "enemy"
    DEBILITATED = "debilitated"


# =============================================================================
# EXALTATION & DEBILITATION TABLE
# =============================================================================

EXALTATION_TABLE = {
    # Planet: (exaltation_sign, exact_degree, debilitation_sign)
    "Sun": (1, 10, 7),  # Aries 10°, Debilitated in Libra
    "Moon": (2, 3, 8),  # Taurus 3°, Debilitated in Scorpio
    "Mars": (10, 28, 4),  # Capricorn 28°, Debilitated in Cancer
    "Mercury": (6, 15, 12),  # Virgo 15°, Debilitated in Pisces
    "Jupiter": (4, 5, 10),  # Cancer 5°, Debilitated in Capricorn
    "Venus": (12, 27, 6),  # Pisces 27°, Debilitated in Virgo
    "Saturn": (7, 20, 1),  # Libra 20°, Debilitated in Aries
    "Rahu": (2, 20, 8),  # Taurus 20°, Debilitated in Scorpio (disputed)
    "Ketu": (8, 20, 2),  # Scorpio 20°, Debilitated in Taurus (disputed)
}

# =============================================================================
# MOOLATRIKONA POSITIONS
# =============================================================================

MOOLATRIKONA_TABLE = {
    # Planet: (sign, start_degree, end_degree)
    "Sun": (5, 0, 20),  # Leo 0-20°
    "Moon": (2, 3, 30),  # Taurus 3-30° (after exaltation point)
    "Mars": (1, 0, 12),  # Aries 0-12°
    "Mercury": (6, 15, 20),  # Virgo 15-20°
    "Jupiter": (9, 0, 10),  # Sagittarius 0-10°
    "Venus": (7, 0, 15),  # Libra 0-15°
    "Saturn": (11, 0, 20),  # Aquarius 0-20°
}

# =============================================================================
# OWNERSHIP TABLE
# =============================================================================

OWNERSHIP_TABLE = {
    "Sun": [5],  # Leo
    "Moon": [4],  # Cancer
    "Mars": [1, 8],  # Aries, Scorpio
    "Mercury": [3, 6],  # Gemini, Virgo
    "Jupiter": [9, 12],  # Sagittarius, Pisces
    "Venus": [2, 7],  # Taurus, Libra
    "Saturn": [10, 11],  # Capricorn, Aquarius
}

# =============================================================================
# NATURAL FRIENDSHIP TABLE (Naisargika Maitri)
# =============================================================================

FRIENDSHIP_TABLE = {
    "Sun": {"friends": ["Moon", "Mars", "Jupiter"], "enemies": ["Venus", "Saturn"], "neutrals": ["Mercury"]},
    "Moon": {"friends": ["Sun", "Mercury"], "enemies": [], "neutrals": ["Mars", "Jupiter", "Venus", "Saturn"]},
    "Mars": {"friends": ["Sun", "Moon", "Jupiter"], "enemies": ["Mercury"], "neutrals": ["Venus", "Saturn"]},
    "Mercury": {"friends": ["Sun", "Venus"], "enemies": ["Moon"], "neutrals": ["Mars", "Jupiter", "Saturn"]},
    "Jupiter": {"friends": ["Sun", "Moon", "Mars"], "enemies": ["Mercury", "Venus"], "neutrals": ["Saturn"]},
    "Venus": {"friends": ["Mercury", "Saturn"], "enemies": ["Sun", "Moon"], "neutrals": ["Mars", "Jupiter"]},
    "Saturn": {"friends": ["Mercury", "Venus"], "enemies": ["Sun", "Moon", "Mars"], "neutrals": ["Jupiter"]},
}

# =============================================================================
# DIGNITY CALCULATION FUNCTIONS
# =============================================================================


def get_dignity(planet: str, sign: int, degree: float = 15.0) -> Dignity:
    """
    Calculate the dignity of a planet in a sign.

    Order of checking:
    1. Is it exalted?
    2. Is it in moolatrikona?
    3. Is it in own sign?
    4. Is it debilitated?
    5. Check friendship with sign lord
    """
    # Check exaltation
    if planet in EXALTATION_TABLE:
        exalt_sign, exalt_deg, debil_sign = EXALTATION_TABLE[planet]
        if sign == exalt_sign:
            return Dignity.EXALTED
        if sign == debil_sign:
            return Dignity.DEBILITATED

    # Check moolatrikona
    if planet in MOOLATRIKONA_TABLE:
        mt_sign, mt_start, mt_end = MOOLATRIKONA_TABLE[planet]
        if sign == mt_sign and mt_start <= degree <= mt_end:
            return Dignity.MOOLATRIKONA

    # Check own sign
    if planet in OWNERSHIP_TABLE:
        if sign in OWNERSHIP_TABLE[planet]:
            return Dignity.OWN_SIGN

    # Check friendship with sign lord
    sign_lords = {
        1: "Mars",
        2: "Venus",
        3: "Mercury",
        4: "Moon",
        5: "Sun",
        6: "Mercury",
        7: "Venus",
        8: "Mars",
        9: "Jupiter",
        10: "Saturn",
        11: "Saturn",
        12: "Jupiter",
    }
    sign_lord = sign_lords[sign]

    if planet in FRIENDSHIP_TABLE:
        if sign_lord in FRIENDSHIP_TABLE[planet]["friends"]:
            return Dignity.FRIENDLY
        elif sign_lord in FRIENDSHIP_TABLE[planet]["enemies"]:
            return Dignity.ENEMY

    return Dignity.NEUTRAL


# =============================================================================
# SPECIAL DIGNITY CONDITIONS
# =============================================================================


def is_vargottama(rasi_sign: int, navamsa_sign: int) -> bool:
    """
    Vargottama: Planet in same sign in D1 and D9.
    This is considered very auspicious - the planet's results are magnified.
    """
    return rasi_sign == navamsa_sign


def is_pushkara_navamsa(longitude: float) -> bool:
    """
    Pushkara Navamsas are specially auspicious navamsa positions.
    These are specific degrees that confer great strength.

    Pushkara Navamsas (per sign):
    - Fire signs (Ari, Leo, Sag): 21°-23°20' and 26°40'-30°
    - Earth signs (Tau, Vir, Cap): 14°-16°40' and 21°-23°20'
    - Air signs (Gem, Lib, Aqu): 6°40'-10° and 16°40'-20°
    - Water signs (Can, Sco, Pis): 0°-3°20' and 10°-13°20'
    """
    sign = int(longitude / 30)
    deg_in_sign = longitude % 30
    element = sign % 4

    pushkara_ranges = {
        0: [(21, 23.333), (26.667, 30)],  # Fire
        1: [(14, 16.667), (21, 23.333)],  # Earth
        2: [(6.667, 10), (16.667, 20)],  # Air
        3: [(0, 3.333), (10, 13.333)],  # Water
    }

    for start, end in pushkara_ranges[element]:
        if start <= deg_in_sign <= end:
            return True
    return False


def is_gandanta(longitude: float) -> bool:
    """
    Gandanta: Junction points between water and fire signs.
    These are considered inauspicious - planets here face obstacles.

    Gandanta zones (last 3°20' of water signs, first 3°20' of fire signs):
    - Pisces/Aries junction: 356°40' - 3°20'
    - Cancer/Leo junction: 116°40' - 123°20'
    - Scorpio/Sagittarius junction: 236°40' - 243°20'
    """
    gandanta_zones = [
        (356.667, 360),
        (0, 3.333),  # Pisces-Aries
        (116.667, 123.333),  # Cancer-Leo
        (236.667, 243.333),  # Scorpio-Sagittarius
    ]

    for start, end in gandanta_zones:
        if start <= longitude <= end:
            return True
    return False


def get_combustion_status(planet_long: float, sun_long: float, planet: str) -> bool:
    """
    Combustion (Asta): Planet too close to Sun loses power.

    Combustion orbs:
    - Moon: 12°
    - Mars: 17°
    - Mercury: 14° (12° if retrograde)
    - Jupiter: 11°
    - Venus: 10° (8° if retrograde)
    - Saturn: 15°
    """
    if planet == "Sun":
        return False

    combustion_orbs = {"Moon": 12, "Mars": 17, "Mercury": 14, "Jupiter": 11, "Venus": 10, "Saturn": 15}

    if planet not in combustion_orbs:
        return False

    orb = combustion_orbs[planet]
    diff = abs(planet_long - sun_long)
    if diff > 180:
        diff = 360 - diff

    return diff <= orb


# =============================================================================
# NEECHABHANGA RAJA YOGA (Cancellation of Debilitation)
# =============================================================================


def check_neechabhanga(debilitated_planet: str, debil_sign: int, chart_data: Dict) -> List[str]:
    """
    Check for cancellation of debilitation (Neechabhanga).

    A debilitated planet's weakness is cancelled if:
    1. Lord of debilitation sign is in kendra from Lagna or Moon
    2. Lord of exaltation sign is in kendra from Lagna or Moon
    3. Planet that gets exalted in debilitation sign is in kendra
    4. Debilitated planet is conjunct or aspected by its exaltation lord
    5. Debilitated planet is in kendra (1,4,7,10)

    When Neechabhanga occurs, it forms RAJA YOGA - giving rise
    after initial struggles.
    """
    cancellations = []

    # This would need full chart data to implement
    # Placeholder for the logic

    return cancellations


# =============================================================================
# DIGNITY INTERPRETATION GUIDE
# =============================================================================

DIGNITY_INTERPRETATIONS = {
    Dignity.EXALTED: """
EXALTED PLANET (Uchcha)
━━━━━━━━━━━━━━━━━━━━━━━
The planet is at PEAK STRENGTH. Like a king sitting on his throne in full glory.

Effects:
• Planet's significations flourish abundantly
• Natural karakas (significations) are enhanced
• House rulership matters handled with excellence
• Confidence, authority, and success in planet's domain
• Can overcome obstacles easily

Caution:
• Over-confidence possible if afflicted
• Can become dominating or excessive
• Pride related to planet's significations
""",
    Dignity.MOOLATRIKONA: """
MOOLATRIKONA PLANET
━━━━━━━━━━━━━━━━━━━
The planet is in its "office" - doing its best professional work.
Slightly less than exaltation but more productive.

Effects:
• Planet performs its duties excellently
• Professional success in planet's domain
• Strong but balanced expression
• Good for career/dharma related to planet
""",
    Dignity.OWN_SIGN: """
OWN SIGN PLANET (Swakshetra)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Planet is "at home" - comfortable, secure, and natural.

Effects:
• Natural expression of planet's energy
• Stability in planet's significations
• Self-sufficiency in related matters
• Good foundation for growth
• Reliable and consistent results
""",
    Dignity.DEBILITATED: """
DEBILITATED PLANET (Neecha)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Planet is at its weakest - like a king in exile.

Effects:
• Planet's significations face obstacles
• Delays and frustrations in related areas
• Self-doubt or lack of confidence
• Results require extra effort
• May indicate karmic lessons

Remedies:
• Strengthen the planet through its gemstone
• Worship the deity associated with planet
• Charity related to planet's significations
• Check for Neechabhanga (cancellation)

IMPORTANT: Debilitation is NOT always bad!
• Creates determination through struggle
• Can indicate deep transformation
• Often found in charts of successful people
• Check for Neechabhanga Raja Yoga
""",
}
