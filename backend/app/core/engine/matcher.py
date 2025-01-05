from typing import List, Dict, Any, Tuple
from app.models.kundli import (
    KundliChart,
    Planet,
    House,
    MatchingResponse,
    KundliResponse,
)

class KundliMatcher:
    GUNAS = {
        "Varna": 1,
        "Vashya": 2,
        "Tara": 3,
        "Yoni": 4,
        "Graha Maitri": 5,
        "Gana": 6,
        "Bhakut": 7,
        "Nadi": 8,
    }

    MOON_SIGNS_COMPATIBILITY = {
        ("Aries", "Leo"): 0.9,
        ("Aries", "Sagittarius"): 0.9,
        ("Taurus", "Virgo"): 0.85,
        ("Taurus", "Capricorn"): 0.85,
        # Add more combinations
    }

    def __init__(self):
        self.total_points = 36  # Traditional Ashtakoot system

    def _calculate_varna_kuta(
        self, moon1: Planet, moon2: Planet
    ) -> Tuple[float, str]:
        # Simplified varna calculation
        varna_map = {
            "Aries": "Kshatriya",
            "Taurus": "Vaishya",
            "Gemini": "Shudra",
            "Cancer": "Brahmin",
            # Add more mappings
        }

        varna1 = varna_map.get(moon1.sign, "Unknown")
        varna2 = varna_map.get(moon2.sign, "Unknown")

        if varna1 == varna2:
            return 1.0, "Perfect varna compatibility"
        elif varna1 == "Brahmin" and varna2 == "Kshatriya":
            return 0.8, "Good varna compatibility"
        # Add more conditions

        return 0.5, "Average varna compatibility"

    def _calculate_vashya_kuta(
        self, moon1: Planet, moon2: Planet
    ) -> Tuple[float, str]:
        # Simplified vashya calculation
        vashya_groups = {
            "Chatushpad": ["Aries", "Taurus", "Leo", "Sagittarius"],
            "Manav": ["Gemini", "Virgo", "Libra", "Aquarius"],
            "Jalachar": ["Cancer", "Scorpio", "Pisces"],
            # Add more groups
        }

        for group_name, signs in vashya_groups.items():
            if moon1.sign in signs and moon2.sign in signs:
                return 1.0, f"Both belong to {group_name} vashya"

        return 0.5, "Different vashya groups"

    def _calculate_tara_kuta(
        self, moon1: Planet, moon2: Planet
    ) -> Tuple[float, str]:
        # Calculate birth star (nakshatra) compatibility
        nakshatra1_num = self.NAKSHATRAS.index(moon1.nakshatra)
        nakshatra2_num = self.NAKSHATRAS.index(moon2.nakshatra)

        # Calculate tara (birth star compatibility)
        tara = (nakshatra2_num - nakshatra1_num) % 9
        
        tara_scores = {
            1: (1.0, "Excellent - Janma Tara"),
            2: (0.5, "Poor - Sampat Tara"),
            3: (0.75, "Good - Vipat Tara"),
            4: (0.5, "Mixed - Kshema Tara"),
            5: (0.25, "Poor - Pratyak Tara"),
            6: (0.6, "Medium - Sadhaka Tara"),
            7: (0.4, "Challenging - Vadha Tara"),
            8: (0.8, "Good - Mitra Tara"),
            9: (0.3, "Difficult - Ati-Mitra Tara"),
        }

        return tara_scores.get(tara, (0.5, "Unknown Tara"))

    def calculate_compatibility(
        self, kundli1: KundliResponse, kundli2: KundliResponse
    ) -> MatchingResponse:
        # Get Moon positions from both charts
        moon1 = next(p for p in kundli1.charts[0].planets if p.name == "Moon")
        moon2 = next(p for p in kundli2.charts[0].planets if p.name == "Moon")

        # Calculate individual compatibility scores
        varna_score, varna_desc = self._calculate_varna_kuta(moon1, moon2)
        vashya_score, vashya_desc = self._calculate_vashya_kuta(moon1, moon2)
        tara_score, tara_desc = self._calculate_tara_kuta(moon1, moon2)

        # Calculate weighted scores
        factor_scores = {
            "Varna": varna_score * self.GUNAS["Varna"],
            "Vashya": vashya_score * self.GUNAS["Vashya"],
            "Tara": tara_score * self.GUNAS["Tara"],
            # Add other guna calculations
        }

        # Calculate total score
        total_score = sum(factor_scores.values())
        max_score = sum(self.GUNAS.values())
        normalized_score = (total_score / max_score) * 36  # Convert to 36-point scale

        # Generate detailed compatibility report
        compatibility_report = [
            {
                "factor": "Varna Kuta",
                "score": varna_score * self.GUNAS["Varna"],
                "max_score": self.GUNAS["Varna"],
                "description": varna_desc,
            },
            {
                "factor": "Vashya Kuta",
                "score": vashya_score * self.GUNAS["Vashya"],
                "max_score": self.GUNAS["Vashya"],
                "description": vashya_desc,
            },
            {
                "factor": "Tara Kuta",
                "score": tara_score * self.GUNAS["Tara"],
                "max_score": self.GUNAS["Tara"],
                "description": tara_desc,
            },
            # Add other factors
        ]

        # Generate recommendations based on scores
        recommendations = self._generate_recommendations(
            factor_scores, normalized_score
        )

        return MatchingResponse(
            kundli1=kundli1,
            kundli2=kundli2,
            total_score=normalized_score,
            factor_scores=factor_scores,
            compatibility_report=compatibility_report,
            recommendations=recommendations,
        )

    def _generate_recommendations(
        self, factor_scores: Dict[str, float], total_score: float
    ) -> List[str]:
        recommendations = []

        if total_score >= 25:
            recommendations.append(
                "This is a highly compatible match with strong spiritual and practical harmony."
            )
        elif total_score >= 18:
            recommendations.append(
                "This match shows good compatibility but may need work in some areas."
            )
        else:
            recommendations.append(
                "This match shows some challenges. Careful consideration is advised."
            )

        # Add specific recommendations based on factor scores
        for factor, score in factor_scores.items():
            if score < (self.GUNAS[factor] * 0.6):
                recommendations.append(
                    f"Consider working on {factor} compatibility through appropriate remedies."
                )

        return recommendations
