"""
Latta (Planetary Kick) System
PGF Protocol: LATTA_001
Gate: GATE_5
Version: 1.0.0

Latta = planetary affliction on nakshatras
Each planet kicks (afflicts) specific nakshatras counted from its position.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

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

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


@dataclass
class LattaResult:
    """Result of Latta analysis"""

    planet: str
    planet_nakshatra: str
    kicked_nakshatra: str
    kicked_nakshatra_index: int
    latta_count: int
    is_afflicting: bool


class LattaCalculator:
    """
    Latta (Planetary Kick) Calculator

    Each planet gives a "kick" (latta) to a specific nakshatra
    counted from its own nakshatra position.

    Traditional counts:
    - Sun: kicks 12th nakshatra from its position
    - Moon: kicks 22nd nakshatra
    - Mars: kicks 3rd nakshatra
    - Mercury: kicks 7th nakshatra
    - Jupiter: kicks 6th nakshatra
    - Venus: kicks 5th nakshatra
    - Saturn: kicks 8th nakshatra
    - Rahu: kicks 9th nakshatra
    - Ketu: kicks 19th nakshatra (some texts vary)
    """

    LATTA_COUNTS = {
        "Sun": 12,
        "Moon": 22,
        "Mars": 3,
        "Mercury": 7,
        "Jupiter": 6,
        "Venus": 5,
        "Saturn": 8,
        "Rahu": 9,
        "Ketu": 19,
    }

    def __init__(self):
        pass

    def get_nakshatra_index(self, longitude: float) -> int:
        """Get nakshatra index (0-26) from longitude"""
        return int(longitude / (360 / 27))

    def get_kicked_nakshatra(self, planet: str, planet_longitude: float) -> Dict[str, Any]:
        """
        Get the nakshatra kicked by a planet
        """
        if planet not in self.LATTA_COUNTS:
            return {"error": f"Unknown planet: {planet}"}

        planet_nak = self.get_nakshatra_index(planet_longitude)
        latta_count = self.LATTA_COUNTS[planet]

        # Kicked nakshatra = planet's nakshatra + latta_count - 1 (counted from planet's position)
        kicked_nak = (planet_nak + latta_count - 1) % 27

        return {
            "planet": planet,
            "planet_nakshatra": NAKSHATRAS[planet_nak],
            "planet_nakshatra_index": planet_nak,
            "latta_count": latta_count,
            "kicked_nakshatra": NAKSHATRAS[kicked_nak],
            "kicked_nakshatra_index": kicked_nak,
        }

    def check_latta_on_nakshatra(self, target_nakshatra_index: int, planets: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Check which planets are giving latta to a specific nakshatra
        """
        afflicting_planets = []

        for planet, longitude in planets.items():
            latta_info = self.get_kicked_nakshatra(planet, longitude)
            if latta_info.get("kicked_nakshatra_index") == target_nakshatra_index:
                afflicting_planets.append(
                    {
                        "planet": planet,
                        "planet_nakshatra": latta_info["planet_nakshatra"],
                        "latta_count": latta_info["latta_count"],
                    }
                )

        return afflicting_planets

    def analyze_birth_latta(self, birth_nakshatra_index: int, planets: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyze latta on birth nakshatra (janma nakshatra)

        Latta on birth nakshatra indicates obstacles and challenges.
        """
        afflicting = self.check_latta_on_nakshatra(birth_nakshatra_index, planets)

        interpretation = ""
        if afflicting:
            planet_names = [a["planet"] for a in afflicting]
            interpretation = (
                f"Latta on Janma Nakshatra from: {', '.join(planet_names)}. "
                "This indicates obstacles and challenges in life areas "
                "signified by these planets."
            )
        else:
            interpretation = "No planetary latta on Janma Nakshatra - favorable."

        return {
            "birth_nakshatra": NAKSHATRAS[birth_nakshatra_index],
            "birth_nakshatra_index": birth_nakshatra_index,
            "afflicting_planets": afflicting,
            "is_afflicted": len(afflicting) > 0,
            "interpretation": interpretation,
        }

    def analyze_all_lattas(self, planets: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate all lattas from all planets
        """
        all_lattas = {}
        latta_by_nakshatra = {i: [] for i in range(27)}

        for planet, longitude in planets.items():
            latta_info = self.get_kicked_nakshatra(planet, longitude)
            all_lattas[planet] = latta_info

            kicked_idx = latta_info.get("kicked_nakshatra_index")
            if kicked_idx is not None:
                latta_by_nakshatra[kicked_idx].append(planet)

        # Find nakshatras with multiple lattas
        heavily_afflicted = {
            NAKSHATRAS[idx]: planets_list for idx, planets_list in latta_by_nakshatra.items() if len(planets_list) >= 2
        }

        return {
            "lattas_by_planet": all_lattas,
            "lattas_by_nakshatra": {
                NAKSHATRAS[i]: planets_list for i, planets_list in latta_by_nakshatra.items() if planets_list
            },
            "heavily_afflicted_nakshatras": heavily_afflicted,
        }

    def analyze_transit_latta(
        self, natal_planets: Dict[str, float], transit_planets: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Analyze transit lattas on natal positions
        """
        transit_lattas = []

        for transit_planet, transit_lon in transit_planets.items():
            latta_info = self.get_kicked_nakshatra(transit_planet, transit_lon)
            kicked_nak = latta_info.get("kicked_nakshatra_index")

            # Check if any natal planet is in the kicked nakshatra
            for natal_planet, natal_lon in natal_planets.items():
                natal_nak = self.get_nakshatra_index(natal_lon)

                if natal_nak == kicked_nak:
                    transit_lattas.append(
                        {
                            "transit_planet": transit_planet,
                            "natal_planet": natal_planet,
                            "nakshatra": NAKSHATRAS[kicked_nak],
                            "interpretation": (
                                f"Transit {transit_planet} giving latta to natal {natal_planet}. "
                                "Challenges related to natal planet's significations."
                            ),
                        }
                    )

        return {
            "transit_lattas": transit_lattas,
            "total_count": len(transit_lattas),
            "summary": (
                f"{len(transit_lattas)} transit latta(s) active" if transit_lattas else "No transit lattas active"
            ),
        }


def analyze_latta(planets: Dict[str, float], moon_longitude: float) -> Dict[str, Any]:
    """
    Convenience function for complete Latta analysis
    """
    calculator = LattaCalculator()
    moon_nak = calculator.get_nakshatra_index(moon_longitude)

    return {
        "birth_latta": calculator.analyze_birth_latta(moon_nak, planets),
        "all_lattas": calculator.analyze_all_lattas(planets),
    }
