"""
Chakra (Wheel) Calculations for Vedic Astrology
PGF Protocol: CHAKRA_001
Gate: GATE_5
Version: 1.0.0

This module implements various chakra systems:
- Sudarshana Chakra (Three-fold wheel)
- Sarvatobhadra Chakra (Auspicious from all sides)
- Kota Chakra (Fortress chart)
- Shoola Dasha timing
"""

import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

TITHIS = [
    "Pratipada",
    "Dwitiya",
    "Tritiya",
    "Chaturthi",
    "Panchami",
    "Shashthi",
    "Saptami",
    "Ashtami",
    "Navami",
    "Dashami",
    "Ekadashi",
    "Dwadashi",
    "Trayodashi",
    "Chaturdashi",
    "Purnima/Amavasya",
]

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


@dataclass
class SudarshanaPosition:
    """Position in Sudarshana Chakra"""

    house: int
    from_lagna: int
    from_moon: int
    from_sun: int
    planets: List[str]


@dataclass
class SarvatobhadraCell:
    """Cell in Sarvatobhadra Chakra"""

    row: int
    col: int
    content_type: str  # 'nakshatra', 'tithi', 'weekday', 'vowel', 'corner'
    content: str
    is_occupied: bool
    occupant: Optional[str]
    vedha_from: List[str]  # Planets causing vedha


class SudarshanaChakra:
    """
    Sudarshana Chakra (Three-fold Wheel)

    Combines houses from Lagna, Moon, and Sun for comprehensive analysis.
    Transit through any of the three triggers events.
    """

    def __init__(self):
        self.positions: Dict[int, SudarshanaPosition] = {}

    def calculate(self, ascendant: float, moon: float, sun: float, planets: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate Sudarshana Chakra

        Args:
            ascendant: Ascendant longitude
            moon: Moon longitude
            sun: Sun longitude
            planets: All planet longitudes

        Returns:
            Complete Sudarshana data
        """
        asc_sign = int(ascendant / 30)
        moon_sign = int(moon / 30)
        sun_sign = int(sun / 30)

        # Calculate planet placements
        planet_signs = {p: int(lon / 30) for p, lon in planets.items()}

        # Build 12 houses from each reference
        houses = {}
        for house in range(1, 13):
            # House from Lagna
            sign_from_lagna = (asc_sign + house - 1) % 12
            # House from Moon
            sign_from_moon = (moon_sign + house - 1) % 12
            # House from Sun
            sign_from_sun = (sun_sign + house - 1) % 12

            # Find planets in this house from each perspective
            planets_in_house = []
            for planet, sign in planet_signs.items():
                if sign == sign_from_lagna:
                    planets_in_house.append(planet)

            houses[house] = {
                "house_number": house,
                "from_lagna": {"sign": SIGNS[sign_from_lagna], "sign_number": sign_from_lagna},
                "from_moon": {"sign": SIGNS[sign_from_moon], "sign_number": sign_from_moon},
                "from_sun": {"sign": SIGNS[sign_from_sun], "sign_number": sign_from_sun},
                "planets": planets_in_house,
            }

        # Analysis
        analysis = self._analyze_sudarshana(houses, planet_signs, asc_sign, moon_sign, sun_sign)

        return {
            "houses": houses,
            "analysis": analysis,
            "reference_points": {"lagna": SIGNS[asc_sign], "moon": SIGNS[moon_sign], "sun": SIGNS[sun_sign]},
        }

    def _analyze_sudarshana(
        self, houses: Dict, planet_signs: Dict, asc_sign: int, moon_sign: int, sun_sign: int
    ) -> Dict[str, Any]:
        """Analyze Sudarshana positions"""

        # Find strong houses (same sign from all three)
        strong_houses = []
        for house in range(1, 13):
            h = houses[house]
            if h["from_lagna"]["sign_number"] == h["from_moon"]["sign_number"] == h["from_sun"]["sign_number"]:
                strong_houses.append(house)

        # Count planets in kendras from each
        kendras = [1, 4, 7, 10]
        kendra_strength = {
            "from_lagna": sum(1 for p, s in planet_signs.items() if ((s - asc_sign + 12) % 12) + 1 in kendras),
            "from_moon": sum(1 for p, s in planet_signs.items() if ((s - moon_sign + 12) % 12) + 1 in kendras),
            "from_sun": sum(1 for p, s in planet_signs.items() if ((s - sun_sign + 12) % 12) + 1 in kendras),
        }

        return {
            "strong_houses": strong_houses,
            "kendra_strength": kendra_strength,
            "interpretation": self._get_interpretation(kendra_strength),
        }

    def _get_interpretation(self, kendra_strength: Dict) -> str:
        """Generate interpretation"""
        total = sum(kendra_strength.values())
        if total >= 9:
            return "Very strong chart with excellent angular strength from all three lagnas."
        elif total >= 6:
            return "Good angular strength. Life events supported by planetary positions."
        elif total >= 3:
            return "Moderate angular strength. Mixed results depending on dasha periods."
        else:
            return "Weak angular positions. Focus on strengthening key areas."


class SarvatobhadraChakra:
    """
    Sarvatobhadra Chakra (Auspicious from All Sides)

    A 9x9 grid combining nakshatras, tithis, weekdays, and vowels.
    Used for muhurta (electional) and transit analysis.
    """

    # Layout of the 9x9 grid
    # Outer ring: Nakshatras (arranged in specific pattern)
    # Inner elements: Tithis, Weekdays, Vowels

    def __init__(self):
        self.grid = [[None for _ in range(9)] for _ in range(9)]
        self._initialize_grid()

    def _initialize_grid(self):
        """Initialize the Sarvatobhadra grid"""
        # This is a simplified representation
        # Full implementation would have the complete 9x9 layout

        # Nakshatra positions (simplified - outer ring)
        nakshatra_positions = [
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, 8),  # Top
            (1, 8),
            (2, 8),
            (3, 8),
            (4, 8),  # Right
            (5, 8),
            (6, 8),
            (7, 8),
            (8, 8),  # Right continued
            (8, 7),
            (8, 6),
            (8, 5),
            (8, 4),  # Bottom
            (8, 3),
            (8, 2),
            (8, 1),
            (8, 0),  # Bottom continued
            (7, 0),
            (6, 0),
            (5, 0),
            (4, 0),  # Left
            (3, 0),
            (2, 0),
            (1, 0),  # Left continued
        ]

        for i, (row, col) in enumerate(nakshatra_positions):
            if i < 27:
                self.grid[row][col] = ("nakshatra", NAKSHATRAS[i])

        # Weekdays (in center area)
        weekday_positions = [(4, 4)]  # Center and surrounding
        for i, (row, col) in enumerate(weekday_positions):
            if i < len(WEEKDAYS):
                self.grid[row][col] = ("weekday", WEEKDAYS[i])

    def calculate_vedha(self, transit_planets: Dict[str, float], natal_moon_nakshatra: int) -> Dict[str, Any]:
        """
        Calculate Vedha (obstruction) in Sarvatobhadra

        Args:
            transit_planets: Current planetary positions
            natal_moon_nakshatra: Natal Moon's nakshatra index

        Returns:
            Vedha analysis
        """
        vedhas = []

        # Get transit nakshatras
        transit_nakshatras = {}
        for planet, lon in transit_planets.items():
            nak_idx = int(lon / (360 / 27))
            transit_nakshatras[planet] = nak_idx

        # Check for vedha from each planet
        # Vedha occurs when transit planet is at specific angular distance
        vedha_angles = [(1, "adjacent"), (9, "trine"), (18, "opposite")]

        for planet, transit_nak in transit_nakshatras.items():
            for angle, vedha_type in vedha_angles:
                # Forward vedha
                target = (natal_moon_nakshatra + angle) % 27
                if transit_nak == target:
                    vedhas.append(
                        {
                            "planet": planet,
                            "type": vedha_type,
                            "direction": "forward",
                            "from_nakshatra": NAKSHATRAS[transit_nak],
                            "to_nakshatra": NAKSHATRAS[natal_moon_nakshatra],
                        }
                    )

                # Backward vedha
                target = (natal_moon_nakshatra - angle + 27) % 27
                if transit_nak == target:
                    vedhas.append(
                        {
                            "planet": planet,
                            "type": vedha_type,
                            "direction": "backward",
                            "from_nakshatra": NAKSHATRAS[transit_nak],
                            "to_nakshatra": NAKSHATRAS[natal_moon_nakshatra],
                        }
                    )

        # Determine overall impact
        malefics = ["Saturn", "Mars", "Rahu", "Ketu"]
        malefic_vedhas = [v for v in vedhas if v["planet"] in malefics]
        benefic_vedhas = [v for v in vedhas if v["planet"] not in malefics]

        return {
            "natal_nakshatra": NAKSHATRAS[natal_moon_nakshatra],
            "vedhas": vedhas,
            "malefic_vedhas": len(malefic_vedhas),
            "benefic_vedhas": len(benefic_vedhas),
            "overall": self._assess_vedha_impact(malefic_vedhas, benefic_vedhas),
        }

    def _assess_vedha_impact(self, malefic_vedhas: List, benefic_vedhas: List) -> str:
        """Assess overall vedha impact"""
        if len(malefic_vedhas) >= 2:
            return "Caution advised - multiple malefic vedhas active"
        elif len(malefic_vedhas) == 1 and len(benefic_vedhas) == 0:
            return "Some challenges indicated by transit vedha"
        elif len(benefic_vedhas) >= 2:
            return "Favorable period - benefic vedhas supportive"
        else:
            return "Mixed influences - results depend on specific activities"


class KotaChakra:
    """
    Kota Chakra (Fortress Chart)

    Maps planets into a fortress structure for analyzing
    strength and vulnerability.
    """

    # Fortress structure
    # Stambha (Pillar): Strong position
    # Swami (Lord): Very strong
    # Prakar (Wall): Protected
    # Vahya (Outside): Vulnerable

    def __init__(self):
        self.positions = {}

    def calculate(self, moon_nakshatra: int, planet_nakshatras: Dict[str, int]) -> Dict[str, Any]:
        """
        Calculate Kota Chakra positions

        Args:
            moon_nakshatra: Moon's nakshatra index
            planet_nakshatras: All planets' nakshatra indices

        Returns:
            Kota Chakra analysis
        """
        # Starting point is Moon's nakshatra
        start = moon_nakshatra

        # Define fortress zones (nakshatras from Moon)
        zones = {
            "swami": [1],  # Lord position - very strong
            "stambha": [2, 3],  # Pillar - strong support
            "prakar": [4, 5, 6],  # Wall - protection
            "vahya": [7, 8, 9],  # Outside - vulnerable
        }

        planet_positions = {}
        for planet, nak in planet_nakshatras.items():
            distance = (nak - start + 27) % 27

            position = "vahya"  # Default
            for zone, distances in zones.items():
                if distance in distances or (27 - distance) in distances:
                    position = zone
                    break

            planet_positions[planet] = {"nakshatra": NAKSHATRAS[nak], "zone": position, "distance_from_moon": distance}

        # Analysis
        swami_planets = [p for p, d in planet_positions.items() if d["zone"] == "swami"]
        stambha_planets = [p for p, d in planet_positions.items() if d["zone"] == "stambha"]
        vahya_planets = [p for p, d in planet_positions.items() if d["zone"] == "vahya"]

        return {
            "moon_nakshatra": NAKSHATRAS[moon_nakshatra],
            "planet_positions": planet_positions,
            "summary": {"swami": swami_planets, "stambha": stambha_planets, "vahya": vahya_planets},
            "interpretation": self._interpret_kota(swami_planets, stambha_planets, vahya_planets),
        }

    def _interpret_kota(self, swami: List, stambha: List, vahya: List) -> str:
        """Interpret Kota Chakra"""
        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]

        benefics_strong = sum(1 for p in swami + stambha if p in benefics)
        malefics_weak = sum(1 for p in vahya if p not in benefics)

        if benefics_strong >= 2 and malefics_weak >= 2:
            return "Excellent fortress - benefics protect, malefics contained"
        elif benefics_strong >= 2:
            return "Good protection from benefics in strong positions"
        elif malefics_weak >= 2:
            return "Malefics weakened - reduced negative influences"
        else:
            return "Mixed fortress strength - focus on strengthening key areas"


def calculate_all_chakras(ascendant: float, moon: float, sun: float, planets: Dict[str, float]) -> Dict[str, Any]:
    """
    Calculate all chakra systems

    Args:
        ascendant: Ascendant longitude
        moon: Moon longitude
        sun: Sun longitude
        planets: All planet longitudes

    Returns:
        All chakra data
    """
    # Calculate nakshatras
    moon_nak = int(moon / (360 / 27))
    planet_naks = {p: int(lon / (360 / 27)) for p, lon in planets.items()}

    # Sudarshana
    sudarshana = SudarshanaChakra()
    sudarshana_data = sudarshana.calculate(ascendant, moon, sun, planets)

    # Sarvatobhadra vedha
    sarvatobhadra = SarvatobhadraChakra()
    sarvatobhadra_data = sarvatobhadra.calculate_vedha(planets, moon_nak)

    # Kota Chakra
    kota = KotaChakra()
    kota_data = kota.calculate(moon_nak, planet_naks)

    return {"sudarshana_chakra": sudarshana_data, "sarvatobhadra_chakra": sarvatobhadra_data, "kota_chakra": kota_data}
