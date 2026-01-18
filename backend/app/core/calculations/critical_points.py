"""
Critical Points Calculator
PGF Protocol: CRITICAL_001
Gate: GATE_5
Version: 1.0.0

Implements:
1. Mrityu Bhaga (Fatal Degrees)
2. 64th Navamsa Lord
3. 22nd Drekkana Lord
4. Pushkara Bhaga (Auspicious Degrees)
5. Pushkara Navamsa
6. Gandanta Points
7. Vargottama Detection
"""

from dataclasses import dataclass
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

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

SIGN_LORDS = [
    "Mars",
    "Venus",
    "Mercury",
    "Moon",
    "Sun",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Saturn",
    "Jupiter",
]


@dataclass
class CriticalPointResult:
    """Result of critical point analysis"""

    planet: str
    point_type: str
    is_afflicted: bool
    degree: float
    critical_degree: float
    orb: float
    interpretation: str


class MrityuBhaga:
    """
    Mrityu Bhaga (Fatal Degrees)

    Specific degrees in each sign that are considered fatal/dangerous
    for each planet. A planet within 1° of its Mrityu Bhaga is afflicted.

    Two systems are commonly used:
    1. Saravali system
    2. Phala Deepika system
    """

    # Mrityu Bhaga degrees for each planet in each sign (Saravali)
    # Format: {planet: [deg_in_aries, deg_in_taurus, ..., deg_in_pisces]}
    MRITYU_BHAGA_SARAVALI = {
        "Sun": [20, 9, 12, 6, 8, 24, 16, 17, 22, 2, 3, 23],
        "Moon": [26, 12, 13, 25, 24, 11, 26, 14, 13, 25, 5, 12],
        "Mars": [19, 28, 25, 23, 29, 28, 14, 21, 2, 15, 11, 6],
        "Mercury": [15, 14, 13, 12, 8, 18, 20, 10, 21, 22, 7, 5],
        "Jupiter": [19, 29, 12, 27, 6, 4, 13, 10, 17, 11, 15, 28],
        "Venus": [28, 15, 11, 17, 10, 13, 4, 6, 27, 12, 29, 19],
        "Saturn": [10, 4, 7, 9, 12, 16, 3, 18, 28, 14, 13, 15],
        "Rahu": [14, 13, 12, 11, 24, 23, 22, 21, 10, 20, 18, 8],
        "Ketu": [8, 18, 20, 10, 21, 22, 11, 12, 13, 14, 23, 24],
    }

    # Phala Deepika system (alternative)
    MRITYU_BHAGA_PHALA_DEEPIKA = {
        "Sun": [20, 9, 12, 6, 8, 24, 16, 17, 22, 2, 3, 23],
        "Moon": [26, 12, 13, 25, 24, 11, 26, 14, 13, 25, 5, 12],
        "Mars": [19, 28, 25, 23, 29, 28, 14, 21, 2, 15, 11, 6],
        "Mercury": [15, 14, 13, 12, 8, 18, 20, 10, 21, 22, 7, 5],
        "Jupiter": [19, 29, 12, 27, 6, 4, 13, 10, 17, 11, 15, 28],
        "Venus": [28, 15, 11, 17, 10, 13, 4, 6, 27, 12, 29, 19],
        "Saturn": [10, 4, 7, 9, 12, 16, 3, 18, 28, 14, 13, 15],
    }

    def __init__(self, system: str = "saravali"):
        self.system = system
        self.mrityu_table = self.MRITYU_BHAGA_SARAVALI if system == "saravali" else self.MRITYU_BHAGA_PHALA_DEEPIKA

    def check_planet(self, planet: str, longitude: float, orb: float = 1.0) -> CriticalPointResult:
        """Check if a planet is in Mrityu Bhaga"""
        sign = int(longitude / 30)
        degree = longitude % 30

        if planet not in self.mrityu_table:
            return CriticalPointResult(
                planet=planet,
                point_type="mrityu_bhaga",
                is_afflicted=False,
                degree=degree,
                critical_degree=0,
                orb=0,
                interpretation="No Mrityu Bhaga defined for this planet",
            )

        mrityu_deg = self.mrityu_table[planet][sign]
        actual_orb = abs(degree - mrityu_deg)

        is_afflicted = actual_orb <= orb

        interpretation = ""
        if is_afflicted:
            interpretation = (
                f"{planet} is in Mrityu Bhaga at {degree:.1f}° (critical: {mrityu_deg}°). "
                "This indicates potential danger related to the planet's significations. "
                "Remedial measures are recommended."
            )
        else:
            interpretation = f"{planet} is not in Mrityu Bhaga. Distance: {actual_orb:.1f}°"

        return CriticalPointResult(
            planet=planet,
            point_type="mrityu_bhaga",
            is_afflicted=is_afflicted,
            degree=degree,
            critical_degree=mrityu_deg,
            orb=actual_orb,
            interpretation=interpretation,
        )

    def check_all_planets(self, planets: Dict[str, float], orb: float = 1.0) -> Dict[str, Any]:
        """Check Mrityu Bhaga for all planets"""
        results = {}
        afflicted = []

        for planet, longitude in planets.items():
            result = self.check_planet(planet, longitude, orb)
            results[planet] = {
                "is_afflicted": result.is_afflicted,
                "degree": result.degree,
                "critical_degree": result.critical_degree,
                "orb": result.orb,
                "sign": SIGNS[int(longitude / 30)],
                "interpretation": result.interpretation,
            }
            if result.is_afflicted:
                afflicted.append(planet)

        return {
            "system": self.system,
            "orb_used": orb,
            "results": results,
            "afflicted_planets": afflicted,
            "summary": f"{len(afflicted)} planet(s) in Mrityu Bhaga" if afflicted else "No planets in Mrityu Bhaga",
        }


class PushkaraBhaga:
    """
    Pushkara Bhaga (Auspicious Degrees)

    Specific degrees in each sign that are highly auspicious.
    Planets in Pushkara Bhaga gain strength.
    """

    # Pushkara Bhaga degrees for each sign
    PUSHKARA_DEGREES = {
        0: [21],  # Aries
        1: [14],  # Taurus
        2: [18],  # Gemini
        3: [8, 20],  # Cancer (two degrees)
        4: [19],  # Leo
        5: [9],  # Virgo
        6: [24],  # Libra
        7: [11, 23],  # Scorpio
        8: [5],  # Sagittarius
        9: [14],  # Capricorn
        10: [9],  # Aquarius
        11: [19],  # Pisces
    }

    def check_planet(self, planet: str, longitude: float, orb: float = 1.0) -> CriticalPointResult:
        """Check if a planet is in Pushkara Bhaga"""
        sign = int(longitude / 30)
        degree = longitude % 30

        pushkara_degrees = self.PUSHKARA_DEGREES.get(sign, [])

        for pd in pushkara_degrees:
            actual_orb = abs(degree - pd)
            if actual_orb <= orb:
                return CriticalPointResult(
                    planet=planet,
                    point_type="pushkara_bhaga",
                    is_afflicted=False,  # Positive!
                    degree=degree,
                    critical_degree=pd,
                    orb=actual_orb,
                    interpretation=f"{planet} is in Pushkara Bhaga - highly auspicious placement!",
                )

        return CriticalPointResult(
            planet=planet,
            point_type="pushkara_bhaga",
            is_afflicted=True,  # Not in Pushkara
            degree=degree,
            critical_degree=0,
            orb=0,
            interpretation=f"{planet} is not in Pushkara Bhaga",
        )


class SixtyFourthNavamsa:
    """
    64th Navamsa (Khara Navamsa)

    Counted from Moon's navamsa. The lord of 64th navamsa
    is a maraka (death-inflicting) planet.

    Also: 22nd Drekkana from Moon's drekkana
    """

    def calculate_64th_navamsa(self, moon_longitude: float) -> Dict[str, Any]:
        """
        Calculate 64th Navamsa from Moon

        64th = 63 navamsas from Moon's navamsa = 7 signs ahead
        """
        # Moon's navamsa
        moon_navamsa = int((moon_longitude % 30) / (30 / 9))
        moon_sign = int(moon_longitude / 30)

        # Starting navamsa sign depends on element
        element = moon_sign % 4
        start_signs = [0, 9, 5, 1]  # Fire, Earth, Air, Water
        moon_navamsa_sign = (start_signs[element] + moon_navamsa) % 12

        # 64th navamsa = 63 navamsas ahead = 7 signs ahead
        sixty_fourth_sign = (moon_navamsa_sign + 7) % 12
        lord = SIGN_LORDS[sixty_fourth_sign]

        return {
            "moon_navamsa_sign": SIGNS[moon_navamsa_sign],
            "64th_navamsa_sign": SIGNS[sixty_fourth_sign],
            "64th_navamsa_lord": lord,
            "interpretation": (
                f"The 64th Navamsa is {SIGNS[sixty_fourth_sign]}, lorded by {lord}. "
                f"{lord}'s dasha/antardasha and transits may trigger health crises."
            ),
        }

    def calculate_22nd_drekkana(self, moon_longitude: float) -> Dict[str, Any]:
        """
        Calculate 22nd Drekkana from Moon

        22nd = 21 drekkanas from Moon's drekkana = 7 signs ahead
        """
        # Moon's drekkana (1st, 2nd, or 3rd in sign)
        moon_sign = int(moon_longitude / 30)
        degree_in_sign = moon_longitude % 30
        moon_drekkana = int(degree_in_sign / 10)  # 0, 1, or 2

        # Drekkana lords cycle through trine signs
        drekkana_sign = (moon_sign + moon_drekkana * 4) % 12

        # 22nd drekkana = 21 drekkanas ahead = 7 signs ahead
        twentysecond_sign = (drekkana_sign + 7) % 12
        lord = SIGN_LORDS[twentysecond_sign]

        return {
            "moon_drekkana_sign": SIGNS[drekkana_sign],
            "22nd_drekkana_sign": SIGNS[twentysecond_sign],
            "22nd_drekkana_lord": lord,
            "interpretation": (
                f"The 22nd Drekkana is {SIGNS[twentysecond_sign]}, lorded by {lord}. "
                f"This is another maraka point related to dangers."
            ),
        }


class Gandanta:
    """
    Gandanta Points

    Junction points between water and fire signs:
    - End of Cancer / Start of Leo
    - End of Scorpio / Start of Sagittarius
    - End of Pisces / Start of Aries

    Planets within 3°20' of these points are in Gandanta.
    """

    GANDANTA_POINTS = [
        (120, "Cancer-Leo"),  # 120° = end of Cancer
        (240, "Scorpio-Sagittarius"),  # 240° = end of Scorpio
        (0, "Pisces-Aries"),  # 0° = end of Pisces/start of Aries
    ]

    GANDANTA_ORB = 3.33  # 3°20'

    def check_planet(self, planet: str, longitude: float) -> Dict[str, Any]:
        """Check if planet is in Gandanta"""
        for point, name in self.GANDANTA_POINTS:
            # Check distance from junction point
            distance = min(abs(longitude - point), abs(longitude - point + 360), abs(longitude - point - 360))

            if distance <= self.GANDANTA_ORB:
                return {
                    "planet": planet,
                    "is_gandanta": True,
                    "junction": name,
                    "distance": round(distance, 2),
                    "interpretation": (
                        f"{planet} is in Gandanta at {name} junction. "
                        "This indicates karmic knots and potential difficulties. "
                        "Special remedies may be needed."
                    ),
                }

        return {"planet": planet, "is_gandanta": False, "interpretation": f"{planet} is not in Gandanta"}

    def check_all_planets(self, planets: Dict[str, float]) -> Dict[str, Any]:
        """Check Gandanta for all planets"""
        results = {}
        gandanta_planets = []

        for planet, lon in planets.items():
            result = self.check_planet(planet, lon)
            results[planet] = result
            if result["is_gandanta"]:
                gandanta_planets.append(planet)

        return {
            "results": results,
            "gandanta_planets": gandanta_planets,
            "summary": (
                f"{len(gandanta_planets)} planet(s) in Gandanta" if gandanta_planets else "No planets in Gandanta"
            ),
        }


class Vargottama:
    """
    Vargottama Detection

    A planet in the same sign in Rasi and Navamsa is Vargottama.
    This gives the planet extra strength.
    """

    def check_planet(self, planet: str, rasi_longitude: float, navamsa_longitude: float = None) -> Dict[str, Any]:
        """Check if planet is Vargottama"""
        rasi_sign = int(rasi_longitude / 30)

        # Calculate navamsa if not provided
        if navamsa_longitude is None:
            degree_in_sign = rasi_longitude % 30
            navamsa_num = int(degree_in_sign / (30 / 9))
            element = rasi_sign % 4
            start_signs = [0, 9, 5, 1]
            navamsa_sign = (start_signs[element] + navamsa_num) % 12
        else:
            navamsa_sign = int(navamsa_longitude / 30)

        is_vargottama = rasi_sign == navamsa_sign

        return {
            "planet": planet,
            "rasi_sign": SIGNS[rasi_sign],
            "navamsa_sign": SIGNS[navamsa_sign],
            "is_vargottama": is_vargottama,
            "interpretation": (
                f"{planet} is Vargottama in {SIGNS[rasi_sign]} - gains extra strength!"
                if is_vargottama
                else f"{planet} is not Vargottama"
            ),
        }


def analyze_all_critical_points(planets: Dict[str, float], moon_longitude: float) -> Dict[str, Any]:
    """
    Comprehensive critical points analysis
    """
    mrityu = MrityuBhaga()
    pushkara = PushkaraBhaga()
    navamsa_64 = SixtyFourthNavamsa()
    gandanta = Gandanta()
    vargottama = Vargottama()

    results = {
        "mrityu_bhaga": mrityu.check_all_planets(planets),
        "pushkara_bhaga": {planet: pushkara.check_planet(planet, lon).__dict__ for planet, lon in planets.items()},
        "64th_navamsa": navamsa_64.calculate_64th_navamsa(moon_longitude),
        "22nd_drekkana": navamsa_64.calculate_22nd_drekkana(moon_longitude),
        "gandanta": gandanta.check_all_planets(planets),
        "vargottama": {planet: vargottama.check_planet(planet, lon) for planet, lon in planets.items()},
    }

    # Summary
    afflicted = results["mrityu_bhaga"]["afflicted_planets"]
    gandanta_list = results["gandanta"]["gandanta_planets"]
    vargottama_list = [p for p, r in results["vargottama"].items() if r["is_vargottama"]]

    results["summary"] = {
        "mrityu_bhaga_count": len(afflicted),
        "gandanta_count": len(gandanta_list),
        "vargottama_count": len(vargottama_list),
        "critical_planets": list(set(afflicted + gandanta_list)),
        "strong_planets": vargottama_list,
    }

    return results
