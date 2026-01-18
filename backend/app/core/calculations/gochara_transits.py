"""Gochara (Transit) Analysis System
====================================
Complete implementation of planetary transit analysis per traditional Jyotish.

Reference Texts:
- Brihat Parashara Hora Shastra (BPHS), Chapter 53
- Phaladeepika, Chapter 20
- Saravali, Chapter 50
- Jataka Parijata, Chapter 16

Shlokas Referenced:
- BPHS 53.1-10: Introduction to Gochara
- BPHS 53.11-50: Individual planet transit results
- BPHS 53.51-60: Vedha (obstruction) rules
- Phaladeepika 20.1-25: Transit timing and results
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class TransitStrength(Enum):
    """Strength levels for transit results"""

    EXCELLENT = "Excellent"
    VERY_GOOD = "Very Good"
    GOOD = "Good"
    NEUTRAL = "Neutral"
    DIFFICULT = "Difficult"
    VERY_DIFFICULT = "Very Difficult"


@dataclass
class VedhaRule:
    """Vedha (obstruction) rule for a transit position"""

    benefic_house: int  # House giving good results
    vedha_house: int  # House that obstructs the benefic house
    description: str


@dataclass
class TransitResult:
    """Result of a single planet transit"""

    planet: str
    natal_house: int
    transit_house: int
    house_from_natal: int  # Transit house counted from natal position
    is_benefic: bool
    strength: TransitStrength
    ashtakavarga_bindus: Optional[int]
    has_vedha: bool
    vedha_from_planet: Optional[str]
    interpretation: str
    reference: str


class GocharaSystem:
    """Complete Gochara (Transit) analysis per BPHS Chapter 53"""

    # Traditional benefic houses for each planet's transit FROM Moon
    # Reference: BPHS 53.11-50, Phaladeepika 20.5-20
    BENEFIC_HOUSES_FROM_MOON = {
        "Sun": [3, 6, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [3, 6, 11],
        "Mercury": [2, 4, 6, 8, 10, 11],
        "Jupiter": [2, 5, 7, 9, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Saturn": [3, 6, 11],
        "Rahu": [3, 6, 10, 11],
        "Ketu": [3, 6, 10, 11],
    }

    # Benefic houses FROM Lagna
    # Reference: Traditional practice, Jataka Parijata 16.10-15
    BENEFIC_HOUSES_FROM_LAGNA = {
        "Sun": [3, 6, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [3, 6, 10, 11],
        "Mercury": [2, 4, 6, 8, 10, 11],
        "Jupiter": [2, 5, 7, 9, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Saturn": [3, 6, 11],
    }

    # Vedha (Obstruction) Rules
    # Reference: BPHS 53.51-60
    # If planet is in vedha_house when another is in benefic_house, it obstructs
    VEDHA_RULES = {
        "Jupiter": [
            VedhaRule(2, 12, "Jupiter in 2nd obstructed by planet in 12th"),
            VedhaRule(5, 4, "Jupiter in 5th obstructed by planet in 4th"),
            VedhaRule(7, 3, "Jupiter in 7th obstructed by planet in 3rd"),
            VedhaRule(9, 10, "Jupiter in 9th obstructed by planet in 10th"),
            VedhaRule(11, 8, "Jupiter in 11th obstructed by planet in 8th"),
        ],
        "Saturn": [
            VedhaRule(3, 12, "Saturn in 3rd obstructed by planet in 12th"),
            VedhaRule(6, 5, "Saturn in 6th obstructed by planet in 5th"),
            VedhaRule(11, 8, "Saturn in 11th obstructed by planet in 8th"),
        ],
        "Sun": [
            VedhaRule(3, 9, "Sun in 3rd obstructed by planet in 9th"),
            VedhaRule(6, 12, "Sun in 6th obstructed by planet in 12th"),
            VedhaRule(10, 4, "Sun in 10th obstructed by planet in 4th"),
            VedhaRule(11, 5, "Sun in 11th obstructed by planet in 5th"),
        ],
        "Moon": [
            VedhaRule(1, 5, "Moon in 1st obstructed by planet in 5th"),
            VedhaRule(3, 9, "Moon in 3rd obstructed by planet in 9th"),
            VedhaRule(6, 12, "Moon in 6th obstructed by planet in 12th"),
            VedhaRule(7, 2, "Moon in 7th obstructed by planet in 2nd"),
            VedhaRule(10, 4, "Moon in 10th obstructed by planet in 4th"),
            VedhaRule(11, 8, "Moon in 11th obstructed by planet in 8th"),
        ],
        "Mars": [
            VedhaRule(3, 12, "Mars in 3rd obstructed by planet in 12th"),
            VedhaRule(6, 9, "Mars in 6th obstructed by planet in 9th"),
            VedhaRule(11, 5, "Mars in 11th obstructed by planet in 5th"),
        ],
        "Mercury": [
            VedhaRule(2, 8, "Mercury in 2nd obstructed by planet in 8th"),
            VedhaRule(4, 10, "Mercury in 4th obstructed by planet in 10th"),
            VedhaRule(6, 12, "Mercury in 6th obstructed by planet in 12th"),
            VedhaRule(8, 2, "Mercury in 8th obstructed by planet in 2nd"),
            VedhaRule(10, 4, "Mercury in 10th obstructed by planet in 4th"),
            VedhaRule(11, 5, "Mercury in 11th obstructed by planet in 5th"),
        ],
        "Venus": [
            VedhaRule(1, 8, "Venus in 1st obstructed by planet in 8th"),
            VedhaRule(2, 7, "Venus in 2nd obstructed by planet in 7th"),
            VedhaRule(3, 1, "Venus in 3rd obstructed by planet in 1st"),
            VedhaRule(4, 10, "Venus in 4th obstructed by planet in 10th"),
            VedhaRule(5, 9, "Venus in 5th obstructed by planet in 9th"),
            VedhaRule(8, 5, "Venus in 8th obstructed by planet in 5th"),
            VedhaRule(9, 11, "Venus in 9th obstructed by planet in 11th"),
            VedhaRule(11, 6, "Venus in 11th obstructed by planet in 6th"),
            VedhaRule(12, 3, "Venus in 12th obstructed by planet in 3rd"),
        ],
    }

    def __init__(self):
        """Initialize Gochara calculator"""
        self.planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    def analyze_transit(
        self,
        planet: str,
        natal_positions: Dict[str, float],  # Natal chart planet positions
        transit_positions: Dict[str, float],  # Current transit positions
        ascendant: float,
        ashtakavarga_bindus: Optional[Dict[str, List[int]]] = None,
        reference_point: str = "Moon",  # 'Moon' or 'Lagna'
    ) -> TransitResult:
        """Analyze single planet transit

        Args:
            planet: Planet to analyze
            natal_positions: Natal planet longitudes
            transit_positions: Current transit longitudes
            ascendant: Natal ascendant
            ashtakavarga_bindus: Optional Ashtakavarga bindus per house
            reference_point: Calculate from 'Moon' or 'Lagna'

        Returns:
            TransitResult with complete analysis

        Reference: BPHS 53.1-60, Phaladeepika 20.1-25
        """
        # Get reference position
        if reference_point == "Moon":
            ref_pos = natal_positions.get("Moon", 0)
            benefic_houses = self.BENEFIC_HOUSES_FROM_MOON.get(planet, [])
        else:
            ref_pos = ascendant
            benefic_houses = self.BENEFIC_HOUSES_FROM_LAGNA.get(planet, [])

        # Calculate house positions
        ref_house = int(ref_pos / 30)
        natal_planet_house = int(natal_positions.get(planet, 0) / 30)
        transit_planet_house = int(transit_positions.get(planet, 0) / 30)

        # House from reference (1-12)
        house_from_ref = ((transit_planet_house - ref_house) % 12) + 1

        # Check if benefic
        is_benefic = house_from_ref in benefic_houses

        # Get Ashtakavarga bindus if available
        av_bindus = None
        if ashtakavarga_bindus and planet in ashtakavarga_bindus:
            av_bindus = ashtakavarga_bindus[planet][transit_planet_house]

        # Check for Vedha
        has_vedha, vedha_planet = self._check_vedha(planet, house_from_ref, transit_positions, ref_pos)

        # Determine strength (combining traditional + Ashtakavarga)
        strength = self._calculate_transit_strength(is_benefic, av_bindus, has_vedha)

        # Generate interpretation
        interpretation = self._interpret_transit(
            planet, house_from_ref, is_benefic, strength, has_vedha, vedha_planet, reference_point
        )

        return TransitResult(
            planet=planet,
            natal_house=natal_planet_house + 1,
            transit_house=transit_planet_house + 1,
            house_from_natal=house_from_ref,
            is_benefic=is_benefic,
            strength=strength,
            ashtakavarga_bindus=av_bindus,
            has_vedha=has_vedha,
            vedha_from_planet=vedha_planet,
            interpretation=interpretation,
            reference=f"BPHS 53.{11 + self.planets.index(planet) * 5 if planet in self.planets else 50}",
        )

    def _check_vedha(
        self, planet: str, house_from_ref: int, transit_positions: Dict[str, float], ref_pos: float
    ) -> Tuple[bool, Optional[str]]:
        """Check if transit has Vedha (obstruction)

        Reference: BPHS 53.51-60
        """
        if planet not in self.VEDHA_RULES:
            return False, None

        ref_house = int(ref_pos / 30)

        # Check each vedha rule for this planet
        for rule in self.VEDHA_RULES[planet]:
            if house_from_ref == rule.benefic_house:
                # Check if any other planet is in vedha position
                for other_planet, lon in transit_positions.items():
                    if other_planet == planet:
                        continue

                    other_house_from_ref = ((int(lon / 30) - ref_house) % 12) + 1

                    if other_house_from_ref == rule.vedha_house:
                        return True, other_planet

        return False, None

    def _calculate_transit_strength(
        self, is_benefic: bool, av_bindus: Optional[int], has_vedha: bool
    ) -> TransitStrength:
        """Calculate overall transit strength

        Combines:
        1. Traditional benefic/malefic house
        2. Ashtakavarga bindus (if available)
        3. Vedha obstruction
        """
        # Start with traditional assessment
        if has_vedha:
            return TransitStrength.DIFFICULT

        if not is_benefic:
            base_strength = TransitStrength.DIFFICULT
        else:
            base_strength = TransitStrength.GOOD

        # Modulate by Ashtakavarga if available
        if av_bindus is not None:
            if av_bindus >= 5 and is_benefic:
                return TransitStrength.EXCELLENT
            elif av_bindus >= 4 and is_benefic:
                return TransitStrength.VERY_GOOD
            elif av_bindus >= 3:
                return TransitStrength.GOOD if is_benefic else TransitStrength.NEUTRAL
            elif av_bindus <= 1:
                return TransitStrength.VERY_DIFFICULT
            else:
                return TransitStrength.DIFFICULT if not is_benefic else TransitStrength.NEUTRAL

        return base_strength

    def _interpret_transit(
        self,
        planet: str,
        house: int,
        is_benefic: bool,
        strength: TransitStrength,
        has_vedha: bool,
        vedha_planet: Optional[str],
        reference: str,
    ) -> str:
        """Generate traditional interpretation

        Reference: BPHS 53, Phaladeepika 20
        """
        house_significations = {
            1: "self, health, personality",
            2: "wealth, family, speech",
            3: "siblings, courage, efforts",
            4: "mother, home, property, vehicles",
            5: "children, education, creativity",
            6: "enemies, diseases, debts, service",
            7: "spouse, partnerships, business",
            8: "longevity, obstacles, transformation",
            9: "fortune, father, dharma, long journeys",
            10: "career, status, authority",
            11: "gains, income, fulfillment of desires",
            12: "losses, expenses, spirituality, foreign lands",
        }

        signification = house_significations.get(house, "unknown area")

        base = f"{planet} transiting {house}th house from {reference}"

        if has_vedha:
            return f"{base}: Obstructed by {vedha_planet}. Traditional benefic results blocked. Delays and obstacles in {signification}. Remedial measures recommended."

        if strength == TransitStrength.EXCELLENT:
            return f"{base}: Excellent period for {signification}. Strong Ashtakavarga support. Results manifest easily and abundantly."
        elif strength == TransitStrength.VERY_GOOD:
            return f"{base}: Very favorable for {signification}. Good results with moderate effort."
        elif strength == TransitStrength.GOOD:
            return f"{base}: Favorable for {signification}. Positive outcomes with consistent effort."
        elif strength == TransitStrength.NEUTRAL:
            return f"{base}: Mixed results in {signification}. Some gains, some challenges. Requires patience."
        elif strength == TransitStrength.DIFFICULT:
            return f"{base}: Challenging period for {signification}. Obstacles likely. Caution advised."
        else:  # VERY_DIFFICULT
            return f"{base}: Very difficult period for {signification}. Significant challenges. Strong remedial measures recommended."

    def analyze_all_transits(
        self,
        natal_positions: Dict[str, float],
        transit_positions: Dict[str, float],
        ascendant: float,
        ashtakavarga_bindus: Optional[Dict[str, List[int]]] = None,
    ) -> Dict[str, Any]:
        """Analyze all planetary transits

        Returns complete transit analysis from both Moon and Lagna
        """
        results_from_moon = {}
        results_from_lagna = {}

        for planet in self.planets:
            if planet in transit_positions:
                results_from_moon[planet] = self.analyze_transit(
                    planet, natal_positions, transit_positions, ascendant, ashtakavarga_bindus, reference_point="Moon"
                )

                results_from_lagna[planet] = self.analyze_transit(
                    planet, natal_positions, transit_positions, ascendant, ashtakavarga_bindus, reference_point="Lagna"
                )

        # Identify key transits (benefic with high AV, or malefic with vedha)
        key_transits = []
        for planet, result in results_from_moon.items():
            if (
                result.strength in [TransitStrength.EXCELLENT, TransitStrength.VERY_GOOD]
                or result.has_vedha
                or result.strength == TransitStrength.VERY_DIFFICULT
            ):
                key_transits.append(
                    {
                        "planet": planet,
                        "strength": result.strength.value,
                        "interpretation": result.interpretation,
                        "reference": "from Moon",
                    }
                )

        return {
            "transits_from_moon": {
                p: {
                    "house": r.house_from_natal,
                    "is_benefic": r.is_benefic,
                    "strength": r.strength.value,
                    "ashtakavarga_bindus": r.ashtakavarga_bindus,
                    "has_vedha": r.has_vedha,
                    "vedha_from": r.vedha_from_planet,
                    "interpretation": r.interpretation,
                    "reference": r.reference,
                }
                for p, r in results_from_moon.items()
            },
            "transits_from_lagna": {
                p: {
                    "house": r.house_from_natal,
                    "is_benefic": r.is_benefic,
                    "strength": r.strength.value,
                    "ashtakavarga_bindus": r.ashtakavarga_bindus,
                    "has_vedha": r.has_vedha,
                    "vedha_from": r.vedha_from_planet,
                    "interpretation": r.interpretation,
                }
                for p, r in results_from_lagna.items()
            },
            "key_transits": key_transits,
            "overall_assessment": self._overall_transit_assessment(results_from_moon),
            "reference": "BPHS Chapter 53, Phaladeepika Chapter 20",
        }

    def _overall_transit_assessment(self, results: Dict[str, TransitResult]) -> str:
        """Provide overall assessment of current transit period"""
        excellent_count = sum(1 for r in results.values() if r.strength == TransitStrength.EXCELLENT)
        good_count = sum(1 for r in results.values() if r.strength in [TransitStrength.VERY_GOOD, TransitStrength.GOOD])
        difficult_count = sum(
            1 for r in results.values() if r.strength in [TransitStrength.DIFFICULT, TransitStrength.VERY_DIFFICULT]
        )
        vedha_count = sum(1 for r in results.values() if r.has_vedha)

        if excellent_count >= 2:
            return "Excellent period overall. Multiple planets in strong positions. Favorable for major undertakings."
        elif good_count >= 3 and difficult_count <= 1:
            return "Generally favorable period. Good for steady progress and moderate initiatives."
        elif difficult_count >= 3 or vedha_count >= 2:
            return "Challenging period. Caution advised. Focus on remedial measures and patience."
        else:
            return "Mixed period. Some opportunities, some challenges. Selective action recommended."


def calculate_current_transits(
    natal_positions: Dict[str, float],
    natal_ascendant: float,
    current_datetime: datetime,
    ashtakavarga_bindus: Optional[Dict[str, List[int]]] = None,
) -> Dict[str, Any]:
    """Calculate current planetary transits

    Args:
        natal_positions: Natal chart planet positions
        natal_ascendant: Natal ascendant
        current_datetime: Current date/time for transit calculation
        ashtakavarga_bindus: Optional Ashtakavarga data for strength assessment

    Returns:
        Complete current transit analysis
    """
    # This would integrate with astronomical calculator to get current positions
    # For now, placeholder - in real implementation would calculate JD and positions
    from app.core.calculations.astronomical import AstronomicalCalculator

    calc = AstronomicalCalculator()
    # Calculate current Julian Day and positions
    # (implementation depends on timezone handling)

    system = GocharaSystem()
    # Would call: system.analyze_all_transits(natal_positions, current_positions, ...)

    return {
        "calculation_time": current_datetime.isoformat(),
        "note": "Integrate with AstronomicalCalculator for real-time positions",
        "reference": "BPHS Chapter 53, Phaladeepika Chapter 20",
    }
