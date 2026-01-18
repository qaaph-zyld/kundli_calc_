"""
Yoga Interpretation Engine
===========================
Generates natural language interpretations for detected yogas.
"""

from enum import Enum
from typing import Any, Dict, List


class YogaStrength(Enum):
    """Yoga strength classifications"""

    VERY_STRONG = "very_strong"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    VERY_WEAK = "very_weak"


class YogaInterpreter:
    """Generates interpretations for yogas"""

    # Yoga interpretation templates
    YOGA_INTERPRETATIONS = {
        "Gajakesari Yoga": {
            "description": "The Elephant-Lion Yoga forms when Jupiter occupies a kendra (1st, 4th, 7th, or 10th house) from the Moon.",
            "effects": {
                "very_strong": "Exceptional wisdom, fame, and prosperity. Strong leadership qualities and influence in society. Material and spiritual abundance.",
                "strong": "Good reputation, intelligence, and wealth. Respected position in society. Success through ethical means.",
                "moderate": "Balanced personality with good judgment. Comfortable life with periods of recognition.",
                "weak": "Subtle positive influence. Some wisdom and good fortune during favorable periods.",
            },
            "timing": "Effects most pronounced during Jupiter and Moon dashas/bhuktis",
            "remedies": "Strengthen by honoring teachers, practicing charity, and maintaining ethical conduct",
        },
        "Budhaditya Yoga": {
            "description": "Sun-Mercury conjunction yoga. Forms when Sun and Mercury are within 12 degrees.",
            "effects": {
                "very_strong": "Exceptional intelligence, communication skills, and analytical abilities. Success in education and intellectual pursuits.",
                "strong": "Sharp intellect and business acumen. Good at mathematics, writing, and strategic thinking.",
                "moderate": "Intelligent and articulate. Good problem-solving abilities.",
                "weak": "Enhanced mental capabilities during favorable periods.",
            },
            "timing": "Effects prominent during Sun and Mercury periods",
            "remedies": "Strengthen through study, teaching, and intellectual pursuits",
        },
        "Hamsa Yoga": {
            "description": "One of the Pancha Mahapurusha yogas. Jupiter in own sign or exaltation in a kendra.",
            "effects": {
                "very_strong": "Exceptional spiritual wisdom, righteousness, and humanitarian qualities. Natural teacher and guide.",
                "strong": "High morality, wisdom, and spiritual inclination. Respected for knowledge and character.",
                "moderate": "Good ethical foundation and spiritual understanding. Interest in philosophy.",
                "weak": "Subtle spiritual influence and moral compass.",
            },
            "timing": "Strongest during Jupiter mahadasha",
            "remedies": "Practice meditation, study sacred texts, and engage in spiritual practices",
        },
        "Sasa Yoga": {
            "description": "Saturn in own sign or exaltation in a kendra. One of Pancha Mahapurusha yogas.",
            "effects": {
                "very_strong": "Exceptional discipline, perseverance, and organizational abilities. Leadership in structured fields.",
                "strong": "Strong work ethic, responsibility, and patience. Success through persistent effort.",
                "moderate": "Good organizational skills and steady progress. Reliable and dutiful.",
                "weak": "Disciplined approach during favorable Saturn periods.",
            },
            "timing": "Most pronounced during Saturn mahadasha",
            "remedies": "Develop discipline, serve the elderly, and practice patience",
        },
        "Malavya Yoga": {
            "description": "Venus in own sign or exaltation in a kendra. Pancha Mahapurusha yoga.",
            "effects": {
                "very_strong": "Exceptional beauty, charm, and artistic talents. Luxury and refined tastes. Success in arts.",
                "strong": "Attractive personality, creative abilities, and appreciation for beauty. Material comforts.",
                "moderate": "Pleasant demeanor and artistic inclinations. Comfortable lifestyle.",
                "weak": "Enhanced aesthetic sense during Venus periods.",
            },
            "timing": "Effects peak during Venus mahadasha",
            "remedies": "Cultivate arts, maintain harmonious relationships, and appreciate beauty",
        },
    }

    @classmethod
    def interpret_yoga(cls, yoga_name: str, strength: float) -> Dict[str, str]:
        """
        Generate interpretation for a specific yoga

        Args:
            yoga_name: Name of the yoga
            strength: Strength value (0-100)

        Returns:
            Dictionary with interpretation fields
        """
        # Classify strength
        if strength >= 90:
            strength_class = YogaStrength.VERY_STRONG
        elif strength >= 75:
            strength_class = YogaStrength.STRONG
        elif strength >= 50:
            strength_class = YogaStrength.MODERATE
        elif strength >= 25:
            strength_class = YogaStrength.WEAK
        else:
            strength_class = YogaStrength.VERY_WEAK

        # Get yoga template
        template = cls.YOGA_INTERPRETATIONS.get(yoga_name, {})

        if not template:
            return {
                "description": f"{yoga_name} is present in the chart",
                "effects": "This yoga influences the native's life in accordance with classical texts",
                "timing": "Effects manifest during relevant planetary periods",
                "strength_assessment": strength_class.value,
                "remedies": "Consult classical texts for specific remedies",
            }

        return {
            "description": template.get("description", ""),
            "effects": template["effects"].get(strength_class.value, template["effects"].get("moderate", "")),
            "timing": template.get("timing", ""),
            "strength_assessment": strength_class.value,
            "strength_percentage": strength,
            "remedies": template.get("remedies", ""),
        }

    @classmethod
    def interpret_multiple_yogas(cls, yogas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive interpretation for multiple yogas

        Args:
            yogas: List of yoga dictionaries with name, category, strength

        Returns:
            Comprehensive interpretation
        """
        if not yogas:
            return {
                "summary": "No significant yogas detected in this chart.",
                "overall_assessment": "Standard chart configuration",
                "recommendations": ["Focus on strengthening planetary positions through remedies"],
            }

        # Categorize yogas
        raja_yogas = [y for y in yogas if y.get("category") == "raja"]
        dhana_yogas = [y for y in yogas if y.get("category") == "dhana"]
        special_yogas = [y for y in yogas if y.get("category") == "special"]

        # Generate summary
        summary_parts = []
        if raja_yogas:
            summary_parts.append(f"{len(raja_yogas)} Raja Yoga(s) for power and status")
        if dhana_yogas:
            summary_parts.append(f"{len(dhana_yogas)} Dhana Yoga(s) for wealth")
        if special_yogas:
            summary_parts.append(f"{len(special_yogas)} Special Yoga(s)")

        summary = (
            f"Chart contains {len(yogas)} yoga(s): " + ", ".join(summary_parts)
            if summary_parts
            else "Multiple yogas present"
        )

        # Overall assessment
        avg_strength = sum(y.get("strength", 50) for y in yogas) / len(yogas)
        if avg_strength >= 75:
            assessment = "Excellent yoga combinations indicating strong potential for success"
        elif avg_strength >= 60:
            assessment = "Good yoga strength with favorable life outcomes expected"
        elif avg_strength >= 40:
            assessment = "Moderate yoga influence with mixed results"
        else:
            assessment = "Weak yoga formations requiring remedial measures"

        # Top 3 strongest yogas
        sorted_yogas = sorted(yogas, key=lambda y: y.get("strength", 0), reverse=True)[:3]
        highlighted_yogas = [
            {
                "name": y.get("name", "Unknown"),
                "strength": y.get("strength", 0),
                "interpretation": cls.interpret_yoga(y.get("name", ""), y.get("strength", 0)),
            }
            for y in sorted_yogas
        ]

        # General recommendations
        recommendations = [
            "Strengthen beneficial yoga effects through appropriate planetary remedies",
            "Time important activities during favorable dashas of yoga-forming planets",
            "Practice ethical living to maximize raja yoga benefits",
            "Maintain spiritual practices for overall chart enhancement",
        ]

        return {
            "summary": summary,
            "total_yogas": len(yogas),
            "average_strength": round(avg_strength, 2),
            "overall_assessment": assessment,
            "highlighted_yogas": highlighted_yogas,
            "by_category": {
                "raja_yogas": len(raja_yogas),
                "dhana_yogas": len(dhana_yogas),
                "special_yogas": len(special_yogas),
            },
            "recommendations": recommendations,
        }

    @classmethod
    def get_yoga_timing_advice(cls, yoga_name: str, current_dasha: str) -> str:
        """
        Get timing-specific advice for yoga manifestation

        Args:
            yoga_name: Name of the yoga
            current_dasha: Current mahadasha planet

        Returns:
            Timing advice string
        """
        # Map yogas to relevant planets
        yoga_planets = {
            "Gajakesari Yoga": ["Jupiter", "Moon"],
            "Budhaditya Yoga": ["Sun", "Mercury"],
            "Hamsa Yoga": ["Jupiter"],
            "Sasa Yoga": ["Saturn"],
            "Malavya Yoga": ["Venus"],
            "Ruchaka Yoga": ["Mars"],
            "Bhadra Yoga": ["Mercury"],
        }

        relevant_planets = yoga_planets.get(yoga_name, [])

        if current_dasha in relevant_planets:
            return f"Excellent! Current {current_dasha} mahadasha is ideal for {yoga_name} manifestation. This is a favorable period."
        elif relevant_planets:
            return f"{yoga_name} effects will be strongest during {', '.join(relevant_planets)} dasha periods."
        else:
            return f"This yoga's effects depend on the overall planetary strength and dasha periods."
