"""
Chart Superimposition - Phase 6
PGF Protocol: SUPER_001
Gate: GATE_6
Version: 1.0.0

Implements:
1. Two-chart overlay/superimposition
2. Synastry analysis
3. Transit overlay on natal
4. Divisional chart overlay
5. Composite charts
"""

import math
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


@dataclass
class SuperimposedAspect:
    """An aspect in superimposed charts"""

    planet1: str
    chart1: str
    planet2: str
    chart2: str
    aspect_type: str
    orb: float
    nature: str  # "harmonious" or "challenging"


class ChartSuperimposition:
    """
    Chart Superimposition Calculator

    Overlays two charts (natal-transit, natal-natal, natal-divisional)
    and analyzes interactions.
    """

    ASPECT_DEFINITIONS = {
        0: ("Conjunction", 10, "neutral"),
        60: ("Sextile", 6, "harmonious"),
        90: ("Square", 8, "challenging"),
        120: ("Trine", 8, "harmonious"),
        180: ("Opposition", 10, "challenging"),
    }

    def __init__(self):
        pass

    def superimpose_charts(
        self,
        chart1: Dict[str, float],
        chart1_name: str,
        chart2: Dict[str, float],
        chart2_name: str,
        chart1_ascendant: float = None,
        chart2_ascendant: float = None,
    ) -> Dict[str, Any]:
        """
        Superimpose two charts and analyze interactions

        Args:
            chart1: First chart's planetary positions {planet: longitude}
            chart1_name: Name/label for first chart (e.g., "Natal", "Transit")
            chart2: Second chart's planetary positions
            chart2_name: Name/label for second chart
        """
        # Find all inter-chart aspects
        aspects = self._find_all_aspects(chart1, chart1_name, chart2, chart2_name)

        # Analyze conjunctions (same sign placements)
        conjunctions = self._find_conjunctions(chart1, chart1_name, chart2, chart2_name)

        # House overlays (if ascendants provided)
        house_overlays = None
        if chart1_ascendant is not None:
            house_overlays = self._analyze_house_overlays(chart1, chart2, chart1_ascendant, chart2_name)

        # Calculate overall harmony
        harmony_score = self._calculate_harmony_score(aspects)

        return {
            "charts": {
                "chart1": {"name": chart1_name, "planets": chart1},
                "chart2": {"name": chart2_name, "planets": chart2},
            },
            "aspects": [self._aspect_to_dict(a) for a in aspects],
            "conjunctions": conjunctions,
            "house_overlays": house_overlays,
            "harmony_score": harmony_score,
            "summary": self._generate_summary(aspects, harmony_score),
        }

    def _find_all_aspects(
        self, chart1: Dict[str, float], name1: str, chart2: Dict[str, float], name2: str
    ) -> List[SuperimposedAspect]:
        """Find all aspects between two charts"""
        aspects = []

        for p1, lon1 in chart1.items():
            for p2, lon2 in chart2.items():
                aspect = self._check_aspect(p1, lon1, name1, p2, lon2, name2)
                if aspect:
                    aspects.append(aspect)

        # Sort by orb (tightest first)
        aspects.sort(key=lambda x: x.orb)

        return aspects

    def _check_aspect(
        self, planet1: str, lon1: float, name1: str, planet2: str, lon2: float, name2: str
    ) -> Optional[SuperimposedAspect]:
        """Check if two planets form an aspect"""
        diff = abs(lon1 - lon2)
        if diff > 180:
            diff = 360 - diff

        for angle, (aspect_name, orb, nature) in self.ASPECT_DEFINITIONS.items():
            if abs(diff - angle) <= orb:
                return SuperimposedAspect(
                    planet1=planet1,
                    chart1=name1,
                    planet2=planet2,
                    chart2=name2,
                    aspect_type=aspect_name,
                    orb=round(abs(diff - angle), 2),
                    nature=nature,
                )

        return None

    def _find_conjunctions(
        self, chart1: Dict[str, float], name1: str, chart2: Dict[str, float], name2: str
    ) -> List[Dict[str, Any]]:
        """Find same-sign placements between charts"""
        conjunctions = []

        for p1, lon1 in chart1.items():
            sign1 = int(lon1 / 30)
            for p2, lon2 in chart2.items():
                sign2 = int(lon2 / 30)
                if sign1 == sign2:
                    conjunctions.append(
                        {
                            "planet1": p1,
                            "chart1": name1,
                            "planet2": p2,
                            "chart2": name2,
                            "sign": SIGNS[sign1],
                            "degree_difference": abs(lon1 % 30 - lon2 % 30),
                        }
                    )

        return conjunctions

    def _analyze_house_overlays(
        self, chart1: Dict[str, float], chart2: Dict[str, float], ascendant: float, chart2_name: str
    ) -> Dict[str, Any]:
        """Analyze where chart2 planets fall in chart1 houses"""
        lagna_sign = int(ascendant / 30)

        overlays = {}
        for planet, lon in chart2.items():
            planet_sign = int(lon / 30)
            house = ((planet_sign - lagna_sign) % 12) + 1

            if house not in overlays:
                overlays[house] = []
            overlays[house].append(planet)

        interpretations = {}
        for house, planets in overlays.items():
            interpretations[f"house_{house}"] = {
                "planets": planets,
                "interpretation": self._interpret_house_overlay(house, planets, chart2_name),
            }

        return interpretations

    def _interpret_house_overlay(self, house: int, planets: List[str], chart_name: str) -> str:
        """Interpret planets overlaying a house"""
        house_meanings = {
            1: "Self, personality, vitality",
            2: "Wealth, family, speech",
            3: "Courage, siblings, communication",
            4: "Home, mother, happiness",
            5: "Children, creativity, romance",
            6: "Enemies, health, service",
            7: "Partnerships, marriage",
            8: "Longevity, transformation",
            9: "Fortune, dharma, father",
            10: "Career, status, authority",
            11: "Gains, wishes, friends",
            12: "Losses, spirituality, foreign",
        }

        meaning = house_meanings.get(house, "")
        planet_str = ", ".join(planets)

        return f"{chart_name} {planet_str} activates {house}th house matters: {meaning}"

    def _calculate_harmony_score(self, aspects: List[SuperimposedAspect]) -> Dict[str, Any]:
        """Calculate overall harmony between charts"""
        harmonious = sum(1 for a in aspects if a.nature == "harmonious")
        challenging = sum(1 for a in aspects if a.nature == "challenging")
        neutral = sum(1 for a in aspects if a.nature == "neutral")

        total = len(aspects) if aspects else 1
        score = ((harmonious * 2 + neutral) / (total * 2)) * 100

        return {
            "score": round(score, 1),
            "harmonious_aspects": harmonious,
            "challenging_aspects": challenging,
            "neutral_aspects": neutral,
            "assessment": self._get_harmony_assessment(score),
        }

    def _get_harmony_assessment(self, score: float) -> str:
        """Get harmony assessment based on score"""
        if score >= 70:
            return "Highly compatible/harmonious"
        elif score >= 50:
            return "Generally compatible with some challenges"
        elif score >= 30:
            return "Mixed compatibility; requires effort"
        else:
            return "Challenging interaction; significant differences"

    def _aspect_to_dict(self, aspect: SuperimposedAspect) -> Dict[str, Any]:
        """Convert aspect to dictionary"""
        return {
            "planet1": aspect.planet1,
            "chart1": aspect.chart1,
            "planet2": aspect.planet2,
            "chart2": aspect.chart2,
            "aspect": aspect.aspect_type,
            "orb": aspect.orb,
            "nature": aspect.nature,
            "interpretation": self._interpret_aspect(aspect),
        }

    def _interpret_aspect(self, aspect: SuperimposedAspect) -> str:
        """Interpret a specific aspect"""
        interpretations = {
            ("Sun", "Moon"): "Vitality meets emotions",
            ("Sun", "Mars"): "Will and action",
            ("Sun", "Venus"): "Self-expression and love",
            ("Sun", "Jupiter"): "Confidence and expansion",
            ("Sun", "Saturn"): "Ego and discipline",
            ("Moon", "Venus"): "Emotions and affection",
            ("Moon", "Mars"): "Feelings and passion",
            ("Moon", "Jupiter"): "Emotions and optimism",
            ("Moon", "Saturn"): "Feelings and responsibility",
            ("Venus", "Mars"): "Love and desire",
            ("Jupiter", "Saturn"): "Expansion and contraction",
        }

        key = (aspect.planet1, aspect.planet2)
        rev_key = (aspect.planet2, aspect.planet1)

        base = (
            interpretations.get(key) or interpretations.get(rev_key) or f"{aspect.planet1}-{aspect.planet2} interaction"
        )

        if aspect.nature == "harmonious":
            return f"{base} - flows easily"
        elif aspect.nature == "challenging":
            return f"{base} - requires conscious effort"
        else:
            return f"{base} - intensified energy"

    def _generate_summary(self, aspects: List[SuperimposedAspect], harmony: Dict[str, Any]) -> str:
        """Generate summary of chart interaction"""
        if not aspects:
            return "No significant aspects between the charts."

        # Find strongest aspects
        strongest = aspects[:3] if len(aspects) >= 3 else aspects

        summary = f"Harmony Score: {harmony['score']}% - {harmony['assessment']}. "
        summary += f"Key aspects: "

        for asp in strongest:
            summary += f"{asp.planet1}-{asp.planet2} {asp.aspect_type}, "

        return summary.rstrip(", ")

    # =========================================================================
    # SPECIALIZED SUPERIMPOSITIONS
    # =========================================================================
    def natal_transit_overlay(
        self, natal_planets: Dict[str, float], transit_planets: Dict[str, float], natal_ascendant: float
    ) -> Dict[str, Any]:
        """Overlay transit chart on natal chart"""
        result = self.superimpose_charts(natal_planets, "Natal", transit_planets, "Transit", natal_ascendant)

        # Add transit-specific analysis
        result["transit_analysis"] = self._analyze_transits(natal_planets, transit_planets, natal_ascendant)

        return result

    def _analyze_transits(self, natal: Dict[str, float], transit: Dict[str, float], ascendant: float) -> Dict[str, Any]:
        """Analyze transits specifically"""
        lagna_sign = int(ascendant / 30)

        # Key transits (Saturn, Jupiter, Rahu/Ketu)
        key_analysis = {}

        for planet in ["Jupiter", "Saturn", "Rahu", "Ketu"]:
            if planet in transit:
                transit_house = ((int(transit[planet] / 30) - lagna_sign) % 12) + 1

                # Check if transiting over natal planets
                transit_sign = int(transit[planet] / 30)
                conjunct_natal = [p for p, lon in natal.items() if int(lon / 30) == transit_sign]

                key_analysis[planet] = {
                    "transit_house": transit_house,
                    "conjunct_natal": conjunct_natal,
                    "interpretation": self._interpret_key_transit(planet, transit_house, conjunct_natal),
                }

        return key_analysis

    def _interpret_key_transit(self, planet: str, house: int, conjunct: List[str]) -> str:
        """Interpret key transit"""
        base = f"Transit {planet} in {house}th house"

        house_effects = {
            1: "Focus on self, new beginnings",
            4: "Home and emotional matters",
            7: "Relationships and partnerships",
            10: "Career and public status",
        }

        effect = house_effects.get(house, f"affects {house}th house matters")

        if conjunct:
            return f"{base} - {effect}. Activating natal {', '.join(conjunct)}"
        return f"{base} - {effect}"

    def divisional_overlay(
        self,
        rasi_planets: Dict[str, float],
        divisional_planets: Dict[str, float],
        divisional_name: str,
        ascendant: float,
    ) -> Dict[str, Any]:
        """Overlay divisional chart on Rasi"""
        result = self.superimpose_charts(rasi_planets, "Rasi (D-1)", divisional_planets, divisional_name, ascendant)

        # Add vargottama check
        vargottama = []
        for planet in rasi_planets:
            if planet in divisional_planets:
                rasi_sign = int(rasi_planets[planet] / 30)
                div_sign = int(divisional_planets[planet] / 30)
                if rasi_sign == div_sign:
                    vargottama.append(planet)

        result["vargottama_planets"] = vargottama

        return result

    def composite_chart(self, chart1: Dict[str, float], chart2: Dict[str, float]) -> Dict[str, Any]:
        """
        Create composite (midpoint) chart from two charts

        Each planet position is the midpoint of the two charts.
        """
        composite = {}

        for planet in set(chart1.keys()) & set(chart2.keys()):
            lon1 = chart1[planet]
            lon2 = chart2[planet]

            # Calculate midpoint
            if abs(lon1 - lon2) <= 180:
                midpoint = (lon1 + lon2) / 2
            else:
                midpoint = ((lon1 + lon2) / 2 + 180) % 360

            composite[planet] = {"longitude": midpoint, "sign": SIGNS[int(midpoint / 30)], "degree": midpoint % 30}

        return {
            "chart_type": "Composite (Midpoint)",
            "planets": composite,
            "interpretation": "Composite chart represents the relationship entity",
        }


def superimpose_charts(
    chart1: Dict[str, float], chart2: Dict[str, float], chart1_name: str = "Chart 1", chart2_name: str = "Chart 2"
) -> Dict[str, Any]:
    """Convenience function for chart superimposition"""
    calc = ChartSuperimposition()
    return calc.superimpose_charts(chart1, chart1_name, chart2, chart2_name)
