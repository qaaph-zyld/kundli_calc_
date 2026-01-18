"""
Synastry (Chart Comparison) System
===================================
Analyzes compatibility and relationship dynamics between two charts.
"""

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class SynastryAspect:
    """Represents an aspect between two charts"""

    person1_planet: str
    person2_planet: str
    aspect_type: str
    orb: float
    is_applying: bool
    strength: float
    interpretation: str


class SynastryAnalyzer:
    """Analyzes relationship compatibility between two birth charts"""

    # Aspect definitions (in degrees)
    ASPECTS = {
        "conjunction": {"angle": 0, "orb": 8, "nature": "neutral"},
        "sextile": {"angle": 60, "orb": 6, "nature": "harmonious"},
        "square": {"angle": 90, "orb": 8, "nature": "challenging"},
        "trine": {"angle": 120, "orb": 8, "nature": "harmonious"},
        "opposition": {"angle": 180, "orb": 8, "nature": "challenging"},
    }

    # Relationship significators
    RELATIONSHIP_PLANETS = ["Sun", "Moon", "Venus", "Mars", "Mercury"]

    @staticmethod
    def normalize_longitude(lon: float) -> float:
        """Normalize longitude to 0-360 range"""
        return lon % 360

    @classmethod
    def calculate_aspect(cls, lon1: float, lon2: float) -> Tuple[str, float]:
        """
        Calculate aspect between two planetary positions

        Args:
            lon1: First planet longitude
            lon2: Second planet longitude

        Returns:
            Tuple of (aspect_type, orb) or (None, None) if no aspect
        """
        diff = abs(cls.normalize_longitude(lon1) - cls.normalize_longitude(lon2))
        if diff > 180:
            diff = 360 - diff

        for aspect_name, aspect_data in cls.ASPECTS.items():
            angle = aspect_data["angle"]
            orb = aspect_data["orb"]

            if abs(diff - angle) <= orb:
                return aspect_name, abs(diff - angle)

        return None, None

    @classmethod
    def analyze_synastry(
        cls,
        chart1_planets: Dict[str, float],
        chart2_planets: Dict[str, float],
        person1_name: str = "Person 1",
        person2_name: str = "Person 2",
    ) -> Dict[str, Any]:
        """
        Complete synastry analysis between two charts

        Args:
            chart1_planets: Planet positions for person 1 (degrees)
            chart2_planets: Planet positions for person 2 (degrees)
            person1_name: Name of first person
            person2_name: Name of second person

        Returns:
            Comprehensive synastry report
        """
        aspects = []

        # Find all inter-chart aspects
        for p1_name, p1_lon in chart1_planets.items():
            for p2_name, p2_lon in chart2_planets.items():
                aspect_type, orb = cls.calculate_aspect(p1_lon, p2_lon)

                if aspect_type:
                    aspect_data = cls.ASPECTS[aspect_type]
                    strength = 100 * (1 - orb / aspect_data["orb"])

                    aspects.append(
                        SynastryAspect(
                            person1_planet=p1_name,
                            person2_planet=p2_name,
                            aspect_type=aspect_type,
                            orb=round(orb, 2),
                            is_applying=True,  # Simplified
                            strength=round(strength, 2),
                            interpretation=cls._get_aspect_interpretation(p1_name, p2_name, aspect_type),
                        )
                    )

        # Categorize aspects
        harmonious = [a for a in aspects if cls.ASPECTS[a.aspect_type]["nature"] == "harmonious"]
        challenging = [a for a in aspects if cls.ASPECTS[a.aspect_type]["nature"] == "challenging"]
        neutral = [a for a in aspects if cls.ASPECTS[a.aspect_type]["nature"] == "neutral"]

        # Calculate compatibility score
        compatibility_score = cls._calculate_compatibility_score(aspects, chart1_planets, chart2_planets)

        # Relationship themes
        themes = cls._identify_relationship_themes(aspects)

        return {
            "person1": person1_name,
            "person2": person2_name,
            "compatibility_score": compatibility_score,
            "overall_assessment": cls._get_overall_assessment(compatibility_score),
            "total_aspects": len(aspects),
            "harmonious_aspects": len(harmonious),
            "challenging_aspects": len(challenging),
            "neutral_aspects": len(neutral),
            "key_aspects": [
                cls._aspect_to_dict(a) for a in sorted(aspects, key=lambda x: x.strength, reverse=True)[:10]
            ],
            "relationship_themes": themes,
            "strengths": cls._identify_strengths(harmonious),
            "challenges": cls._identify_challenges(challenging),
            "advice": cls._generate_relationship_advice(compatibility_score, themes),
        }

    @classmethod
    def _calculate_compatibility_score(
        cls, aspects: List[SynastryAspect], chart1: Dict[str, float], chart2: Dict[str, float]
    ) -> int:
        """Calculate overall compatibility score (0-100)"""
        if not aspects:
            return 50

        # Weight aspects by nature
        score = 50  # Base score

        for aspect in aspects:
            nature = cls.ASPECTS[aspect.aspect_type]["nature"]
            weight = aspect.strength / 100

            # Relationship planets carry more weight
            if aspect.person1_planet in cls.RELATIONSHIP_PLANETS and aspect.person2_planet in cls.RELATIONSHIP_PLANETS:
                weight *= 1.5

            if nature == "harmonious":
                score += weight * 3
            elif nature == "challenging":
                score -= weight * 2

        # Normalize to 0-100
        score = max(0, min(100, score))
        return round(score)

    @classmethod
    def _get_aspect_interpretation(cls, planet1: str, planet2: str, aspect: str) -> str:
        """Get interpretation for specific planetary aspect"""
        interpretations = {
            ("Sun", "Moon", "conjunction"): "Deep emotional connection and mutual understanding",
            ("Sun", "Moon", "trine"): "Natural harmony between ego and emotions",
            ("Sun", "Moon", "opposition"): "Complementary but potentially polarizing energies",
            ("Venus", "Mars", "conjunction"): "Strong romantic and sexual attraction",
            ("Venus", "Mars", "square"): "Passionate but potentially conflictual attraction",
            ("Moon", "Venus", "trine"): "Emotional nurturing and affection flow easily",
            ("Mercury", "Mercury", "conjunction"): "Excellent communication and mental rapport",
            ("Sun", "Sun", "conjunction"): "Similar life paths and core identities",
            ("Jupiter", "Sun", "trine"): "Growth, optimism, and mutual support",
            ("Saturn", "Sun", "conjunction"): "Karmic connection with lessons to learn",
        }

        key = (planet1, planet2, aspect)
        if key in interpretations:
            return interpretations[key]

        # Generic interpretation
        nature = cls.ASPECTS[aspect]["nature"]
        if nature == "harmonious":
            return f"{planet1} harmonizes with {planet2}, creating ease and flow"
        elif nature == "challenging":
            return f"{planet1} challenges {planet2}, requiring growth and adjustment"
        else:
            return f"{planet1} connects with {planet2}, intensifying both energies"

    @classmethod
    def _identify_relationship_themes(cls, aspects: List[SynastryAspect]) -> List[str]:
        """Identify major relationship themes"""
        themes = []

        # Check for specific planetary combinations
        planet_pairs = [(a.person1_planet, a.person2_planet) for a in aspects]

        if any(("Sun", "Moon") in pair or ("Moon", "Sun") in pair for pair in planet_pairs):
            themes.append("Emotional Connection")

        if any(("Venus", "Mars") in pair or ("Mars", "Venus") in pair for pair in planet_pairs):
            themes.append("Romantic Attraction")

        if any(("Mercury", "Mercury") in pair for pair in planet_pairs):
            themes.append("Communication")

        if any(("Jupiter", p) in pair or (p, "Jupiter") in pair for pair in planet_pairs for p in ["Sun", "Moon"]):
            themes.append("Growth & Expansion")

        if any(
            ("Saturn", p) in pair or (p, "Saturn") in pair for pair in planet_pairs for p in ["Sun", "Moon", "Venus"]
        ):
            themes.append("Commitment & Karma")

        return themes if themes else ["General Compatibility"]

    @classmethod
    def _identify_strengths(cls, harmonious_aspects: List[SynastryAspect]) -> List[str]:
        """Identify relationship strengths"""
        strengths = []

        for aspect in harmonious_aspects[:5]:
            if aspect.person1_planet in ["Sun", "Moon"] and aspect.person2_planet in ["Sun", "Moon"]:
                strengths.append("Strong emotional and personal compatibility")
            elif "Venus" in [aspect.person1_planet, aspect.person2_planet]:
                strengths.append("Natural affection and appreciation for each other")
            elif "Jupiter" in [aspect.person1_planet, aspect.person2_planet]:
                strengths.append("Mutual growth and positive outlook together")
            elif "Mercury" in [aspect.person1_planet, aspect.person2_planet]:
                strengths.append("Good communication and intellectual connection")

        return strengths if strengths else ["General positive rapport"]

    @classmethod
    def _identify_challenges(cls, challenging_aspects: List[SynastryAspect]) -> List[str]:
        """Identify potential relationship challenges"""
        challenges = []

        for aspect in challenging_aspects[:5]:
            if aspect.person1_planet == "Saturn" or aspect.person2_planet == "Saturn":
                challenges.append("Need for patience and working through limitations")
            elif aspect.person1_planet == "Mars" or aspect.person2_planet == "Mars":
                challenges.append("Potential for conflicts and need to manage anger")
            elif aspect.aspect_type == "square":
                challenges.append(
                    f"Tension between {aspect.person1_planet} and {aspect.person2_planet} requiring compromise"
                )

        return challenges if challenges else ["Minor adjustments needed"]

    @classmethod
    def _get_overall_assessment(cls, score: int) -> str:
        """Get overall compatibility assessment"""
        if score >= 80:
            return "Excellent compatibility with strong natural harmony"
        elif score >= 65:
            return "Good compatibility with more strengths than challenges"
        elif score >= 50:
            return "Moderate compatibility requiring effort and understanding"
        elif score >= 35:
            return "Challenging compatibility requiring significant work"
        else:
            return "Difficult compatibility with major obstacles to overcome"

    @classmethod
    def _generate_relationship_advice(cls, score: int, themes: List[str]) -> List[str]:
        """Generate actionable relationship advice"""
        advice = []

        if score >= 65:
            advice.append("Build on your natural harmony and mutual understanding")
            advice.append("Continue open communication to maintain connection")
        else:
            advice.append("Focus on developing patience and understanding")
            advice.append("Work consciously on communication and compromise")

        if "Emotional Connection" in themes:
            advice.append("Honor each other's emotional needs and vulnerabilities")

        if "Communication" in themes:
            advice.append("Maintain regular, honest dialogue about feelings and goals")

        if "Commitment & Karma" in themes:
            advice.append("View challenges as opportunities for growth together")

        return advice

    @staticmethod
    def _aspect_to_dict(aspect: SynastryAspect) -> Dict[str, Any]:
        """Convert aspect to dictionary"""
        return {
            "person1_planet": aspect.person1_planet,
            "person2_planet": aspect.person2_planet,
            "aspect": aspect.aspect_type,
            "orb": aspect.orb,
            "strength": aspect.strength,
            "interpretation": aspect.interpretation,
        }
