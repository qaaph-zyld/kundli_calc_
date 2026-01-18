"""
Dasa Pravesh (Period Commencement Charts) - Phase 6
PGF Protocol: PRAVESH_001
Gate: GATE_6
Version: 1.0.0

Implements:
1. Dasa Pravesh Chart calculation
2. Antardasa Pravesh Chart
3. Pratyantardasa Pravesh Chart
4. Analysis of period commencement charts
"""

import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

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
class PraveshChart:
    """Dasa Pravesh Chart"""

    dasa_lord: str
    level: str  # "mahadasa", "antardasa", "pratyantardasa"
    start_time: datetime
    ascendant: float
    planets: Dict[str, float]
    houses: Dict[int, float]
    analysis: Dict[str, Any]


class DasaPraveshCalculator:
    """
    Dasa Pravesh Calculator

    Calculates charts for the moment when a dasha period begins.
    These charts are analyzed similarly to birth charts to predict
    events during the dasha period.
    """

    def __init__(self):
        pass

    def calculate_pravesh_chart(
        self,
        natal_planets: Dict[str, float],
        natal_ascendant: float,
        dasa_start_time: datetime,
        dasa_lord: str,
        level: str = "mahadasa",
        birth_latitude: float = 0.0,
        birth_longitude: float = 0.0,
    ) -> PraveshChart:
        """
        Calculate Dasa Pravesh Chart

        Args:
            natal_planets: Natal planetary positions
            natal_ascendant: Natal ascendant
            dasa_start_time: When the dasha period begins
            dasa_lord: Planet or sign ruling the dasha
            level: "mahadasa", "antardasa", or "pratyantardasa"
            birth_latitude: Birth location latitude
            birth_longitude: Birth location longitude
        """
        # Calculate approximate positions at dasa start
        # (In production, this would use Swiss Ephemeris)
        transit_planets = self._calculate_transit_positions(natal_planets, dasa_start_time)

        # Calculate ascendant for dasa start time
        pravesh_ascendant = self._calculate_pravesh_ascendant(dasa_start_time, birth_latitude, birth_longitude)

        # Calculate houses
        houses = self._calculate_houses(pravesh_ascendant)

        # Analyze the pravesh chart
        analysis = self._analyze_pravesh_chart(
            transit_planets, pravesh_ascendant, natal_planets, natal_ascendant, dasa_lord
        )

        return PraveshChart(
            dasa_lord=dasa_lord,
            level=level,
            start_time=dasa_start_time,
            ascendant=pravesh_ascendant,
            planets=transit_planets,
            houses=houses,
            analysis=analysis,
        )

    def _calculate_transit_positions(self, natal_planets: Dict[str, float], target_time: datetime) -> Dict[str, float]:
        """
        Calculate approximate planetary positions at target time
        Uses average daily motion
        """
        # Average daily motion
        daily_motion = {
            "Sun": 0.9856,
            "Moon": 13.1764,
            "Mars": 0.524,
            "Mercury": 1.383,
            "Jupiter": 0.083,
            "Venus": 1.2,
            "Saturn": 0.034,
            "Rahu": -0.053,
            "Ketu": -0.053,
        }

        # Assume natal_planets is for J2000 epoch for simplicity
        # Calculate days from epoch
        reference = datetime(2000, 1, 1, 12, 0, 0)
        days = (target_time - reference).days

        transit = {}
        for planet, natal_lon in natal_planets.items():
            motion = daily_motion.get(planet, 0)
            transit[planet] = (natal_lon + motion * days) % 360

        return transit

    def _calculate_pravesh_ascendant(self, time: datetime, latitude: float, longitude: float) -> float:
        """Calculate ascendant for given time and location"""
        # Simplified ascendant calculation
        # (In production, use full astronomical calculation)

        # Local sidereal time approximation
        hours = time.hour + time.minute / 60
        day_of_year = time.timetuple().tm_yday

        # Rough LST
        lst = (hours + longitude / 15 + day_of_year * 0.0657) % 24

        # Convert to degrees (rough approximation)
        asc_degree = (lst / 24 * 360 + latitude / 3) % 360

        return asc_degree

    def _calculate_houses(self, ascendant: float) -> Dict[int, float]:
        """Calculate house cusps (whole sign)"""
        lagna_sign = int(ascendant / 30)
        return {i + 1: ((lagna_sign + i) % 12) * 30 for i in range(12)}

    def _analyze_pravesh_chart(
        self,
        transit_planets: Dict[str, float],
        pravesh_asc: float,
        natal_planets: Dict[str, float],
        natal_asc: float,
        dasa_lord: str,
    ) -> Dict[str, Any]:
        """Analyze the Dasa Pravesh chart"""
        pravesh_lagna = int(pravesh_asc / 30)
        natal_lagna = int(natal_asc / 30)

        # Get planet houses in pravesh chart
        pravesh_houses = {planet: ((int(lon / 30) - pravesh_lagna) % 12) + 1 for planet, lon in transit_planets.items()}

        # Dasa lord analysis
        dasa_lord_house = pravesh_houses.get(dasa_lord, 1)
        dasa_lord_sign = int(transit_planets.get(dasa_lord, 0) / 30)

        # Key factors
        analysis = {
            "pravesh_ascendant": {
                "sign": SIGNS[pravesh_lagna],
                "degree": pravesh_asc % 30,
                "relation_to_natal": self._get_house_relation(pravesh_lagna, natal_lagna),
            },
            "dasa_lord_position": {
                "house": dasa_lord_house,
                "sign": SIGNS[dasa_lord_sign],
                "interpretation": self._interpret_dasa_lord_house(dasa_lord, dasa_lord_house),
            },
            "benefic_positions": self._analyze_benefic_positions(pravesh_houses),
            "malefic_positions": self._analyze_malefic_positions(pravesh_houses),
            "key_transits": self._analyze_key_transits(transit_planets, natal_planets),
            "overall_indication": self._get_overall_indication(pravesh_houses, dasa_lord_house),
        }

        return analysis

    def _get_house_relation(self, sign1: int, sign2: int) -> str:
        """Get relationship between two signs"""
        diff = (sign1 - sign2) % 12
        relations = {
            0: "Same (1st)",
            1: "2nd",
            2: "3rd",
            3: "4th (Kendra)",
            4: "5th (Trikona)",
            5: "6th (Dusthana)",
            6: "7th (Kendra)",
            7: "8th (Dusthana)",
            8: "9th (Trikona)",
            9: "10th (Kendra)",
            10: "11th",
            11: "12th (Dusthana)",
        }
        return relations.get(diff, "Unknown")

    def _interpret_dasa_lord_house(self, dasa_lord: str, house: int) -> str:
        """Interpret dasa lord's house position"""
        interpretations = {
            1: f"{dasa_lord} in 1st - Strong self-expression, new beginnings",
            2: f"{dasa_lord} in 2nd - Focus on wealth, family, speech",
            3: f"{dasa_lord} in 3rd - Courage, communication, short travels",
            4: f"{dasa_lord} in 4th - Home, mother, property, happiness",
            5: f"{dasa_lord} in 5th - Children, creativity, speculation",
            6: f"{dasa_lord} in 6th - Obstacles, health issues, service",
            7: f"{dasa_lord} in 7th - Partnerships, marriage, business",
            8: f"{dasa_lord} in 8th - Transformation, hidden matters",
            9: f"{dasa_lord} in 9th - Fortune, dharma, higher learning",
            10: f"{dasa_lord} in 10th - Career peak, authority, success",
            11: f"{dasa_lord} in 11th - Gains, fulfillment of desires",
            12: f"{dasa_lord} in 12th - Expenses, foreign lands, spirituality",
        }
        return interpretations.get(house, "Neutral position")

    def _analyze_benefic_positions(self, houses: Dict[str, int]) -> Dict[str, Any]:
        """Analyze benefic planet positions"""
        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
        good_houses = [1, 4, 5, 7, 9, 10, 11]

        benefic_analysis = {}
        for planet in benefics:
            house = houses.get(planet, 0)
            benefic_analysis[planet] = {"house": house, "favorable": house in good_houses}

        favorable_count = sum(1 for b in benefic_analysis.values() if b["favorable"])

        return {
            "details": benefic_analysis,
            "favorable_count": favorable_count,
            "assessment": "Strong benefic support" if favorable_count >= 3 else "Moderate benefic support",
        }

    def _analyze_malefic_positions(self, houses: Dict[str, int]) -> Dict[str, Any]:
        """Analyze malefic planet positions"""
        malefics = ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]
        upachaya = [3, 6, 10, 11]  # Good houses for malefics

        malefic_analysis = {}
        for planet in malefics:
            house = houses.get(planet, 0)
            malefic_analysis[planet] = {"house": house, "favorable": house in upachaya}

        return {
            "details": malefic_analysis,
            "assessment": (
                "Malefics well-placed"
                if sum(1 for m in malefic_analysis.values() if m["favorable"]) >= 3
                else "Some malefic challenges"
            ),
        }

    def _analyze_key_transits(self, transit: Dict[str, float], natal: Dict[str, float]) -> List[Dict[str, Any]]:
        """Analyze key transit aspects to natal positions"""
        key_aspects = []

        for t_planet, t_lon in transit.items():
            for n_planet, n_lon in natal.items():
                diff = abs(t_lon - n_lon)
                if diff > 180:
                    diff = 360 - diff

                # Check for conjunction or opposition
                if diff < 10:
                    key_aspects.append({"transit": t_planet, "natal": n_planet, "aspect": "Conjunction", "orb": diff})
                elif abs(diff - 180) < 10:
                    key_aspects.append(
                        {"transit": t_planet, "natal": n_planet, "aspect": "Opposition", "orb": abs(diff - 180)}
                    )

        return key_aspects[:5]  # Top 5 aspects

    def _get_overall_indication(self, houses: Dict[str, int], dasa_lord_house: int) -> str:
        """Get overall indication for the dasha period"""
        # Positive factors
        positive = 0
        if dasa_lord_house in [1, 4, 5, 7, 9, 10, 11]:
            positive += 2
        if houses.get("Jupiter", 0) in [1, 4, 5, 7, 9, 10]:
            positive += 1
        if houses.get("Venus", 0) in [1, 4, 5, 7, 9, 10]:
            positive += 1

        # Negative factors
        negative = 0
        if dasa_lord_house in [6, 8, 12]:
            negative += 2
        if houses.get("Saturn", 0) in [1, 4, 7]:
            negative += 1
        if houses.get("Rahu", 0) in [1, 4, 7]:
            negative += 1

        score = positive - negative

        if score >= 3:
            return "Highly favorable period - success and growth expected"
        elif score >= 1:
            return "Generally favorable with some challenges"
        elif score >= -1:
            return "Mixed results - require careful navigation"
        else:
            return "Challenging period - caution advised"

    def calculate_multiple_pravesh(
        self,
        natal_planets: Dict[str, float],
        natal_ascendant: float,
        dasa_periods: List[Dict[str, Any]],
        birth_latitude: float = 0.0,
        birth_longitude: float = 0.0,
    ) -> List[PraveshChart]:
        """Calculate Pravesh charts for multiple dasa periods"""
        charts = []

        for period in dasa_periods:
            chart = self.calculate_pravesh_chart(
                natal_planets=natal_planets,
                natal_ascendant=natal_ascendant,
                dasa_start_time=period["start_time"],
                dasa_lord=period["ruler"],
                level=period.get("level", "mahadasa"),
                birth_latitude=birth_latitude,
                birth_longitude=birth_longitude,
            )
            charts.append(chart)

        return charts


def calculate_dasa_pravesh(
    natal_planets: Dict[str, float],
    natal_ascendant: float,
    dasa_start: datetime,
    dasa_lord: str,
    level: str = "mahadasa",
) -> Dict[str, Any]:
    """Convenience function for Dasa Pravesh calculation"""
    calc = DasaPraveshCalculator()
    chart = calc.calculate_pravesh_chart(natal_planets, natal_ascendant, dasa_start, dasa_lord, level)

    return {
        "dasa_lord": chart.dasa_lord,
        "level": chart.level,
        "start_time": chart.start_time.isoformat(),
        "ascendant": {"degree": chart.ascendant, "sign": SIGNS[int(chart.ascendant / 30)]},
        "planets": {p: {"longitude": lon, "sign": SIGNS[int(lon / 30)]} for p, lon in chart.planets.items()},
        "analysis": chart.analysis,
    }
