"""
Enhanced Ashtakavarga System
PGF Protocol: ASHTAK_002
Gate: GATE_5
Version: 1.0.0

This module implements the complete Ashtakavarga system:
- Bhinnashtakavarga (BAV) - Individual planet contributions
- Sarvashtakavarga (SAV) - Combined totals
- Prastara Ashtakavarga - Detailed contribution tables
- Kaksha Analysis
- Trikona Shodhan (Reduction)
- Ekadhipatya Shodhan
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
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

# Ashtakavarga benefic point rules
# Format: For each planet, positions from various reference points that give benefic points
# Positions are 1-indexed house numbers

ASHTAKAVARGA_RULES = {
    "Sun": {
        "from_Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "from_Moon": [3, 6, 10, 11],
        "from_Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "from_Mercury": [3, 5, 6, 9, 10, 11, 12],
        "from_Jupiter": [5, 6, 9, 11],
        "from_Venus": [6, 7, 12],
        "from_Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "from_Lagna": [3, 4, 6, 10, 11, 12],
    },
    "Moon": {
        "from_Sun": [3, 6, 7, 8, 10, 11],
        "from_Moon": [1, 3, 6, 7, 10, 11],
        "from_Mars": [2, 3, 5, 6, 9, 10, 11],
        "from_Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "from_Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "from_Venus": [3, 4, 5, 7, 9, 10, 11],
        "from_Saturn": [3, 5, 6, 11],
        "from_Lagna": [3, 6, 10, 11],
    },
    "Mars": {
        "from_Sun": [3, 5, 6, 10, 11],
        "from_Moon": [3, 6, 11],
        "from_Mars": [1, 2, 4, 7, 8, 10, 11],
        "from_Mercury": [3, 5, 6, 11],
        "from_Jupiter": [6, 10, 11, 12],
        "from_Venus": [6, 8, 11, 12],
        "from_Saturn": [1, 4, 7, 8, 9, 10, 11],
        "from_Lagna": [1, 3, 6, 10, 11],
    },
    "Mercury": {
        "from_Sun": [5, 6, 9, 11, 12],
        "from_Moon": [2, 4, 6, 8, 10, 11],
        "from_Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "from_Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "from_Jupiter": [6, 8, 11, 12],
        "from_Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "from_Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "from_Lagna": [1, 2, 4, 6, 8, 10, 11],
    },
    "Jupiter": {
        "from_Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "from_Moon": [2, 5, 7, 9, 11],
        "from_Mars": [1, 2, 4, 7, 8, 10, 11],
        "from_Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "from_Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "from_Venus": [2, 5, 6, 9, 10, 11],
        "from_Saturn": [3, 5, 6, 12],
        "from_Lagna": [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "Venus": {
        "from_Sun": [8, 11, 12],
        "from_Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "from_Mars": [3, 5, 6, 9, 11, 12],
        "from_Mercury": [3, 5, 6, 9, 11],
        "from_Jupiter": [5, 8, 9, 10, 11],
        "from_Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "from_Saturn": [3, 4, 5, 8, 9, 10, 11],
        "from_Lagna": [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "Saturn": {
        "from_Sun": [1, 2, 4, 7, 8, 10, 11],
        "from_Moon": [3, 6, 11],
        "from_Mars": [3, 5, 6, 10, 11, 12],
        "from_Mercury": [6, 8, 9, 10, 11, 12],
        "from_Jupiter": [5, 6, 11, 12],
        "from_Venus": [6, 11, 12],
        "from_Saturn": [3, 5, 6, 11],
        "from_Lagna": [1, 3, 4, 6, 10, 11],
    },
}


@dataclass
class BAVResult:
    """Bhinnashtakavarga result for one planet"""

    planet: str
    bindus: List[int]  # 12 values, one per sign
    total: int
    strongest_signs: List[int]
    weakest_signs: List[int]


@dataclass
class SAVResult:
    """Sarvashtakavarga result"""

    bindus: List[int]  # 12 values combined
    total: int
    strongest_signs: List[int]
    weakest_signs: List[int]


@dataclass
class PrastaraResult:
    """Prastara (detailed contribution) result"""

    planet: str
    table: List[List[int]]  # 8x12 table (contributors x signs)
    contributors: List[str]
    signs: List[str]


class EnhancedAshtakavarga:
    """
    Complete Ashtakavarga System Implementation
    """

    def __init__(self):
        self.bav_results: Dict[str, BAVResult] = {}
        self.sav_result: Optional[SAVResult] = None
        self.prastara_results: Dict[str, PrastaraResult] = {}

    def calculate_complete(self, planet_positions: Dict[str, float], ascendant: float) -> Dict[str, Any]:
        """
        Calculate complete Ashtakavarga

        Args:
            planet_positions: Dictionary of planet name to longitude
            ascendant: Ascendant longitude

        Returns:
            Complete Ashtakavarga data
        """
        # Get sign positions
        positions = self._get_sign_positions(planet_positions, ascendant)

        # Calculate BAV for each planet
        for planet in PLANETS:
            self.bav_results[planet] = self._calculate_bav(planet, positions)

        # Calculate SAV
        self.sav_result = self._calculate_sav()

        # Calculate Prastara for each planet
        for planet in PLANETS:
            self.prastara_results[planet] = self._calculate_prastara(planet, positions)

        return self._format_results()

    def _get_sign_positions(self, planet_positions: Dict[str, float], ascendant: float) -> Dict[str, int]:
        """Convert longitudes to sign numbers (0-11)"""
        positions = {}
        for planet, lon in planet_positions.items():
            positions[planet] = int(lon / 30)
        positions["Lagna"] = int(ascendant / 30)
        return positions

    def _calculate_bav(self, planet: str, positions: Dict[str, int]) -> BAVResult:
        """
        Calculate Bhinnashtakavarga for a planet

        Counts benefic points for each sign based on positions
        of all contributing planets
        """
        bindus = [0] * 12
        rules = ASHTAKAVARGA_RULES.get(planet, {})

        contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]

        for contributor in contributors:
            if contributor not in positions:
                continue

            contributor_sign = positions[contributor]
            rule_key = f"from_{contributor}"

            if rule_key in rules:
                benefic_houses = rules[rule_key]
                for house in benefic_houses:
                    # House 1 from contributor is same sign as contributor
                    target_sign = (contributor_sign + house - 1) % 12
                    bindus[target_sign] += 1

        total = sum(bindus)

        # Find strongest and weakest signs
        sorted_signs = sorted(range(12), key=lambda x: bindus[x], reverse=True)
        strongest = [s for s in sorted_signs[:3] if bindus[s] >= 4]
        weakest = [s for s in sorted_signs[-3:] if bindus[s] <= 2]

        return BAVResult(planet=planet, bindus=bindus, total=total, strongest_signs=strongest, weakest_signs=weakest)

    def _calculate_sav(self) -> SAVResult:
        """
        Calculate Sarvashtakavarga (combined bindus)
        """
        combined = [0] * 12

        for planet, bav in self.bav_results.items():
            for i in range(12):
                combined[i] += bav.bindus[i]

        total = sum(combined)

        # Strongest and weakest
        sorted_signs = sorted(range(12), key=lambda x: combined[x], reverse=True)
        strongest = [s for s in sorted_signs[:3] if combined[s] >= 28]  # Good threshold
        weakest = [s for s in sorted_signs[-3:] if combined[s] <= 20]

        return SAVResult(bindus=combined, total=total, strongest_signs=strongest, weakest_signs=weakest)

    def _calculate_prastara(self, planet: str, positions: Dict[str, int]) -> PrastaraResult:
        """
        Calculate Prastara Ashtakavarga (detailed contribution table)

        Shows which contributor gives bindu to which sign
        """
        contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]
        table = [[0] * 12 for _ in range(8)]  # 8 contributors x 12 signs
        rules = ASHTAKAVARGA_RULES.get(planet, {})

        for i, contributor in enumerate(contributors):
            if contributor not in positions:
                continue

            contributor_sign = positions[contributor]
            rule_key = f"from_{contributor}"

            if rule_key in rules:
                benefic_houses = rules[rule_key]
                for house in benefic_houses:
                    target_sign = (contributor_sign + house - 1) % 12
                    table[i][target_sign] = 1

        return PrastaraResult(planet=planet, table=table, contributors=contributors, signs=SIGNS)

    def trikona_shodhan(self) -> Dict[str, List[int]]:
        """
        Trikona Shodhan (Reduction)

        Reduces bindus in trine houses based on certain rules
        Used for refined predictions
        """
        reduced = {}

        for planet, bav in self.bav_results.items():
            bindus = bav.bindus.copy()

            # Process each trine set (1-5-9, 2-6-10, 3-7-11, 4-8-12)
            for start in range(4):
                trine_signs = [start, (start + 4) % 12, (start + 8) % 12]
                trine_bindus = [bindus[s] for s in trine_signs]
                min_bindu = min(trine_bindus)

                # Reduce each trine sign by minimum
                for sign in trine_signs:
                    bindus[sign] -= min_bindu

            reduced[planet] = bindus

        return reduced

    def ekadhipatya_shodhan(self, planet_positions: Dict[str, float]) -> Dict[str, List[int]]:
        """
        Ekadhipatya Shodhan

        Reduction when same planet lords two signs
        """
        # Get positions
        positions = {p: int(lon / 30) for p, lon in planet_positions.items()}

        reduced = {}

        for planet, bav in self.bav_results.items():
            bindus = bav.bindus.copy()

            # Dual-ownership planets: Mercury, Venus, Mars, Jupiter, Saturn
            dual_lords = {
                "Mercury": [2, 5],  # Gemini, Virgo
                "Venus": [1, 6],  # Taurus, Libra
                "Mars": [0, 7],  # Aries, Scorpio
                "Jupiter": [8, 11],  # Sagittarius, Pisces
                "Saturn": [9, 10],  # Capricorn, Aquarius
            }

            for lord, signs in dual_lords.items():
                if lord in positions:
                    lord_sign = positions[lord]
                    # If lord is in one of its signs
                    if lord_sign in signs:
                        other_sign = signs[0] if lord_sign == signs[1] else signs[1]
                        # Reduce the other sign's bindu
                        bindus[other_sign] = max(0, bindus[other_sign] - 1)

            reduced[planet] = bindus

        return reduced

    def get_kaksha_analysis(self, planet: str, target_sign: int) -> Dict[str, Any]:
        """
        Kaksha Analysis

        Shows which sub-period (kaksha) of a sign is strong/weak
        Each sign is divided into 8 kakshas ruled by different planets
        """
        kaksha_lords = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Lagna"]

        if planet not in self.prastara_results:
            return {}

        prastara = self.prastara_results[planet]
        contributions = [prastara.table[i][target_sign] for i in range(8)]

        kakshas = []
        for i, (lord, bindu) in enumerate(zip(kaksha_lords, contributions)):
            kakshas.append(
                {
                    "kaksha": i + 1,
                    "lord": lord,
                    "has_bindu": bindu == 1,
                    "degrees": f"{(i * 3.75):.2f}° - {((i + 1) * 3.75):.2f}°",
                }
            )

        return {
            "planet": planet,
            "sign": SIGNS[target_sign],
            "kakshas": kakshas,
            "favorable_kakshas": sum(contributions),
            "interpretation": self._interpret_kaksha(sum(contributions)),
        }

    def _interpret_kaksha(self, favorable_count: int) -> str:
        """Interpret kaksha analysis"""
        if favorable_count >= 6:
            return "Very strong position. Planet gives excellent results through most of the sign."
        elif favorable_count >= 4:
            return "Good position. Planet gives favorable results in majority of the sign."
        elif favorable_count >= 2:
            return "Mixed position. Results vary depending on exact degree."
        else:
            return "Weak position. Planet struggles to give positive results in this sign."

    def _format_results(self) -> Dict[str, Any]:
        """Format all results for output"""
        return {
            "bhinnashtakavarga": {
                planet: {
                    "bindus": bav.bindus,
                    "total": bav.total,
                    "strongest_signs": [SIGNS[s] for s in bav.strongest_signs],
                    "weakest_signs": [SIGNS[s] for s in bav.weakest_signs],
                    "by_sign": {SIGNS[i]: bav.bindus[i] for i in range(12)},
                }
                for planet, bav in self.bav_results.items()
            },
            "sarvashtakavarga": {
                "bindus": self.sav_result.bindus if self.sav_result else [],
                "total": self.sav_result.total if self.sav_result else 0,
                "strongest_signs": [SIGNS[s] for s in self.sav_result.strongest_signs] if self.sav_result else [],
                "weakest_signs": [SIGNS[s] for s in self.sav_result.weakest_signs] if self.sav_result else [],
                "by_sign": {SIGNS[i]: self.sav_result.bindus[i] for i in range(12)} if self.sav_result else {},
            },
            "analysis": {
                "total_bindus": self.sav_result.total if self.sav_result else 0,
                "average_per_sign": (self.sav_result.total / 12) if self.sav_result else 0,
                "interpretation": self._get_overall_interpretation(),
            },
        }

    def _get_overall_interpretation(self) -> str:
        """Get overall interpretation"""
        if not self.sav_result:
            return ""

        avg = self.sav_result.total / 12
        if avg >= 30:
            return "Excellent overall chart strength. Most areas of life well-supported."
        elif avg >= 25:
            return "Good chart strength. Generally favorable life circumstances."
        elif avg >= 20:
            return "Average chart strength. Results depend on specific areas and dashas."
        else:
            return "Below average strength. Focus on strong areas and remedies for weak ones."


def calculate_complete_ashtakavarga(planet_positions: Dict[str, float], ascendant: float) -> Dict[str, Any]:
    """
    Convenience function for complete Ashtakavarga calculation

    Args:
        planet_positions: Dictionary of planet name to longitude
        ascendant: Ascendant longitude

    Returns:
        Complete Ashtakavarga data
    """
    calculator = EnhancedAshtakavarga()
    return calculator.calculate_complete(planet_positions, ascendant)
