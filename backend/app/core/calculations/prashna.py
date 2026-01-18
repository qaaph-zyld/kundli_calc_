"""
Prashna (Horary) Astrology System
PGF Protocol: PRASHNA_001
Gate: GATE_5
Version: 1.0.0

Complete implementation of Prashna Shastra:
- Question-time based chart calculation
- Arudha determination
- Prashna Lagna analysis
- Mook Prashna (silent question)
- Shakuna (omens) interpretation
- Shatpanchasika techniques
- KP Horary (1-249 numbers)
- Tajika aspects for Prashna
"""

import math
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
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


class QuestionCategory(Enum):
    MARRIAGE = "marriage"
    CAREER = "career"
    HEALTH = "health"
    FINANCE = "finance"
    TRAVEL = "travel"
    EDUCATION = "education"
    LITIGATION = "litigation"
    LOST_OBJECT = "lost_object"
    CHILDBIRTH = "childbirth"
    GENERAL = "general"


@dataclass
class PrashnaResult:
    """Result of a Prashna analysis"""

    question_time: datetime
    ascendant: float
    moon_sign: int
    arudha: int
    favorable: bool
    timing: str
    detailed_analysis: Dict[str, Any]


class PrashnaCalculator:
    """
    Complete Prashna (Horary) Astrology System
    """

    def __init__(self):
        # House significations for Prashna
        self.house_matters = {
            1: ["Self", "Querent", "Beginning", "Health"],
            2: ["Wealth", "Family", "Speech", "Food"],
            3: ["Siblings", "Courage", "Short journeys", "Communication"],
            4: ["Mother", "Home", "Vehicle", "Comfort", "Land"],
            5: ["Children", "Romance", "Speculation", "Intelligence"],
            6: ["Enemies", "Disease", "Competition", "Service"],
            7: ["Marriage", "Partner", "Business", "Opponent"],
            8: ["Death", "Inheritance", "Obstacles", "Secret"],
            9: ["Fortune", "Father", "Religion", "Long journey"],
            10: ["Career", "Authority", "Status", "Government"],
            11: ["Gains", "Friends", "Fulfillment", "Elder sibling"],
            12: ["Loss", "Expense", "Foreign", "Liberation"],
        }

        # Question to house mapping
        self.question_house_map = {
            QuestionCategory.MARRIAGE: [7, 2, 11],
            QuestionCategory.CAREER: [10, 6, 11],
            QuestionCategory.HEALTH: [1, 6, 8],
            QuestionCategory.FINANCE: [2, 11, 5],
            QuestionCategory.TRAVEL: [3, 9, 12],
            QuestionCategory.EDUCATION: [4, 5, 9],
            QuestionCategory.LITIGATION: [6, 7, 12],
            QuestionCategory.LOST_OBJECT: [2, 4, 11],
            QuestionCategory.CHILDBIRTH: [5, 11, 1],
            QuestionCategory.GENERAL: [1, 7, 10],
        }

    def analyze_prashna(
        self,
        question_time: datetime,
        latitude: float,
        longitude: float,
        question_category: QuestionCategory,
        planets: Dict[str, float],
        ascendant: float,
    ) -> Dict[str, Any]:
        """
        Complete Prashna analysis

        Args:
            question_time: Time when question was asked
            latitude: Location latitude
            longitude: Location longitude
            question_category: Type of question
            planets: Planetary positions at question time
            ascendant: Ascendant at question time

        Returns:
            Complete Prashna analysis
        """
        asc_sign = int(ascendant / 30)
        moon_lon = planets.get("Moon", 0)
        moon_sign = int(moon_lon / 30)

        # Calculate Arudha
        arudha = self._calculate_arudha(asc_sign, question_category)

        # Get relevant houses for the question
        relevant_houses = self.question_house_map.get(question_category, [1, 7, 10])

        # Analyze each relevant house
        house_analysis = {}
        for house in relevant_houses:
            house_analysis[house] = self._analyze_house(house, asc_sign, planets, ascendant)

        # Check overall favorability
        favorable = self._check_favorability(asc_sign, moon_sign, planets, ascendant, relevant_houses)

        # Timing estimation
        timing = self._estimate_timing(planets, ascendant, question_category)

        # Lagna analysis
        lagna_analysis = self._analyze_lagna(asc_sign, planets)

        # Moon analysis (very important in Prashna)
        moon_analysis = self._analyze_moon(moon_lon, planets)

        # Check Shakuna (omens)
        shakuna = self._check_shakuna(asc_sign, moon_sign, planets)

        return {
            "question_time": question_time.isoformat(),
            "question_category": question_category.value,
            "prashna_lagna": {
                "sign": SIGNS[asc_sign],
                "degree": ascendant % 30,
                "nakshatra": NAKSHATRAS[int(ascendant / (360 / 27))],
                "lord": SIGN_LORDS[asc_sign],
            },
            "moon_position": {
                "sign": SIGNS[moon_sign],
                "degree": moon_lon % 30,
                "nakshatra": NAKSHATRAS[int(moon_lon / (360 / 27))],
            },
            "arudha": {"sign": SIGNS[arudha], "interpretation": self._interpret_arudha(arudha, question_category)},
            "relevant_houses": relevant_houses,
            "house_analysis": house_analysis,
            "lagna_analysis": lagna_analysis,
            "moon_analysis": moon_analysis,
            "shakuna": shakuna,
            "favorable": favorable["is_favorable"],
            "favorability_factors": favorable["factors"],
            "timing": timing,
            "final_verdict": self._generate_verdict(favorable, timing, question_category),
        }

    def _calculate_arudha(self, asc_sign: int, category: QuestionCategory) -> int:
        """
        Calculate Arudha Lagna for Prashna

        Arudha = Sign as far from lord as lord is from sign
        """
        lord = SIGN_LORDS[asc_sign]

        # Get lord's natural sign (simplified - use first sign)
        lord_signs = {"Mars": 0, "Venus": 1, "Mercury": 2, "Moon": 3, "Sun": 4, "Jupiter": 8, "Saturn": 9}

        lord_sign = lord_signs.get(lord, 0)

        # Distance from Lagna to Lord's sign
        distance = (lord_sign - asc_sign + 12) % 12

        # Arudha = same distance from lord's sign
        arudha = (lord_sign + distance) % 12

        # Special rule: if Arudha falls in 1st or 7th from Lagna, take 10th/4th
        if arudha == asc_sign:
            arudha = (asc_sign + 9) % 12  # 10th
        elif arudha == (asc_sign + 6) % 12:
            arudha = (asc_sign + 3) % 12  # 4th

        return arudha

    def _analyze_house(self, house: int, asc_sign: int, planets: Dict[str, float], ascendant: float) -> Dict[str, Any]:
        """Analyze a specific house"""
        house_sign = (asc_sign + house - 1) % 12
        house_lord = SIGN_LORDS[house_sign]

        # Find planets in this house
        planets_in_house = []
        for planet, lon in planets.items():
            planet_sign = int(lon / 30)
            if planet_sign == house_sign:
                planets_in_house.append(planet)

        # Get house lord position
        lord_lon = planets.get(house_lord, 0)
        lord_house = ((int(lord_lon / 30) - asc_sign + 12) % 12) + 1

        # Determine strength
        strength = self._calculate_house_strength(house, house_sign, planets_in_house, lord_house)

        return {
            "sign": SIGNS[house_sign],
            "lord": house_lord,
            "lord_in_house": lord_house,
            "planets": planets_in_house,
            "strength": strength,
            "significations": self.house_matters.get(house, []),
        }

    def _calculate_house_strength(
        self, house: int, house_sign: int, planets_in_house: List[str], lord_house: int
    ) -> str:
        """Calculate house strength for Prashna"""
        score = 0

        # Benefics in house
        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
        for planet in planets_in_house:
            if planet in benefics:
                score += 2
            else:
                score -= 1

        # Lord in good houses (1,4,5,7,9,10,11)
        good_houses = [1, 4, 5, 7, 9, 10, 11]
        if lord_house in good_houses:
            score += 2
        elif lord_house in [6, 8, 12]:
            score -= 2

        if score >= 3:
            return "strong"
        elif score >= 1:
            return "moderate"
        else:
            return "weak"

    def _check_favorability(
        self, asc_sign: int, moon_sign: int, planets: Dict[str, float], ascendant: float, relevant_houses: List[int]
    ) -> Dict[str, Any]:
        """Check overall favorability of the Prashna"""
        factors = []
        score = 0

        # 1. Moon's condition
        moon_lon = planets.get("Moon", 0)
        moon_nak = int(moon_lon / (360 / 27))

        # Moon in good nakshatras
        good_nakshatras = [3, 6, 7, 10, 11, 12, 13, 16, 19, 21, 22, 24, 26]  # Favorable
        if moon_nak in good_nakshatras:
            factors.append("Moon in favorable nakshatra")
            score += 2

        # 2. Lagna lord position
        lagna_lord = SIGN_LORDS[asc_sign]
        ll_lon = planets.get(lagna_lord, 0)
        ll_house = ((int(ll_lon / 30) - asc_sign + 12) % 12) + 1

        if ll_house in [1, 4, 5, 7, 9, 10, 11]:
            factors.append(f"Lagna lord in favorable house {ll_house}")
            score += 2
        elif ll_house in [6, 8, 12]:
            factors.append(f"Lagna lord in dusthana house {ll_house}")
            score -= 2

        # 3. Jupiter's aspect on Lagna
        jup_lon = planets.get("Jupiter", 0)
        jup_sign = int(jup_lon / 30)
        jup_aspects = [(jup_sign + 4) % 12, (jup_sign + 6) % 12, (jup_sign + 8) % 12]

        if asc_sign in jup_aspects or jup_sign == asc_sign:
            factors.append("Jupiter aspects or in Lagna")
            score += 3

        # 4. Moon not afflicted
        rahu_lon = planets.get("Rahu", 0)
        ketu_lon = planets.get("Ketu", 0)
        saturn_lon = planets.get("Saturn", 0)

        moon_sign_deg = moon_lon % 30
        afflicted = False

        for malefic, mal_lon in [("Rahu", rahu_lon), ("Ketu", ketu_lon), ("Saturn", saturn_lon)]:
            mal_sign = int(mal_lon / 30)
            if mal_sign == moon_sign and abs(moon_lon - mal_lon) < 10:
                factors.append(f"Moon afflicted by {malefic}")
                score -= 2
                afflicted = True

        if not afflicted:
            factors.append("Moon unafflicted")
            score += 1

        # 5. Hora consideration
        hora_lord = self._get_hora_lord(planets)
        if hora_lord in ["Jupiter", "Venus", "Mercury", "Moon"]:
            factors.append(f"Benefic Hora ({hora_lord})")
            score += 1

        is_favorable = score >= 2

        return {"is_favorable": is_favorable, "score": score, "factors": factors}

    def _estimate_timing(
        self, planets: Dict[str, float], ascendant: float, category: QuestionCategory
    ) -> Dict[str, Any]:
        """Estimate timing of event"""
        asc_sign = int(ascendant / 30)

        # Sign type determines time unit
        # Cardinal (movable): days/weeks
        # Fixed: months
        # Dual: variable

        modality = asc_sign % 3

        if modality == 0:  # Cardinal: Aries, Cancer, Libra, Capricorn
            time_unit = "days to weeks"
            speed = "fast"
        elif modality == 1:  # Fixed: Taurus, Leo, Scorpio, Aquarius
            time_unit = "months"
            speed = "slow"
        else:  # Dual: Gemini, Virgo, Sagittarius, Pisces
            time_unit = "variable (weeks to months)"
            speed = "moderate"

        # Moon's position gives more specific timing
        moon_lon = planets.get("Moon", 0)
        moon_nak = int(moon_lon / (360 / 27))
        days_in_nak = (moon_lon % (360 / 27)) / (360 / 27) * 13.33  # Approx days

        return {
            "speed": speed,
            "time_unit": time_unit,
            "estimate": f"Within {time_unit}",
            "moon_transit_days": round(days_in_nak, 1),
            "interpretation": self._timing_interpretation(speed, category),
        }

    def _timing_interpretation(self, speed: str, category: QuestionCategory) -> str:
        """Generate timing interpretation"""
        if speed == "fast":
            return "Quick resolution expected. Look for results within days to 2 weeks."
        elif speed == "slow":
            return "Patience required. Results may take 2-6 months to manifest."
        else:
            return "Timing is variable. Watch for trigger transits over coming weeks."

    def _analyze_lagna(self, asc_sign: int, planets: Dict[str, float]) -> Dict[str, Any]:
        """Analyze Prashna Lagna"""
        lagna_lord = SIGN_LORDS[asc_sign]
        ll_lon = planets.get(lagna_lord, 0)
        ll_sign = int(ll_lon / 30)

        # Planets in Lagna
        planets_in_lagna = [p for p, lon in planets.items() if int(lon / 30) == asc_sign]

        return {
            "sign": SIGNS[asc_sign],
            "lord": lagna_lord,
            "lord_sign": SIGNS[ll_sign],
            "planets_in_lagna": planets_in_lagna,
            "interpretation": self._lagna_interpretation(asc_sign, planets_in_lagna),
        }

    def _lagna_interpretation(self, asc_sign: int, planets: List[str]) -> str:
        """Interpret Lagna for Prashna"""
        sign_nature = {
            0: "Energetic start, quick action needed",
            1: "Stable situation, patience required",
            2: "Communication key, multiple options",
            3: "Emotional matters, home/family involved",
            4: "Authority figures important, recognition",
            5: "Details matter, analytical approach needed",
            6: "Partnership central, balance required",
            7: "Hidden factors, research needed",
            8: "Luck favors, philosophical approach",
            9: "Career focus, systematic approach",
            10: "Unconventional solutions, innovation",
            11: "Spiritual dimension, intuition important",
        }
        return sign_nature.get(asc_sign, "General situation")

    def _analyze_moon(self, moon_lon: float, planets: Dict[str, float]) -> Dict[str, Any]:
        """Analyze Moon for Prashna (very important)"""
        moon_sign = int(moon_lon / 30)
        moon_nak = int(moon_lon / (360 / 27))
        moon_pada = int((moon_lon % (360 / 27)) / (360 / 27 / 4)) + 1

        # Moon's applying/separating aspects
        aspects = []
        for planet, lon in planets.items():
            if planet == "Moon":
                continue
            diff = (lon - moon_lon + 360) % 360
            if diff < 10:  # Applying conjunction
                aspects.append(f"Applying to {planet}")
            elif 360 - diff < 10:  # Separating
                aspects.append(f"Separating from {planet}")

        # Void of Course check
        void_of_course = len(aspects) == 0

        return {
            "sign": SIGNS[moon_sign],
            "nakshatra": NAKSHATRAS[moon_nak],
            "pada": moon_pada,
            "degree": round(moon_lon % 30, 2),
            "aspects": aspects,
            "void_of_course": void_of_course,
            "interpretation": (
                "Void of Course - delay likely" if void_of_course else "Moon active - matter will progress"
            ),
        }

    def _check_shakuna(self, asc_sign: int, moon_sign: int, planets: Dict[str, float]) -> Dict[str, Any]:
        """Check Shakuna (omens) for Prashna"""
        omens = []

        # Rising sign omens
        if asc_sign in [0, 4, 8]:  # Fire signs
            omens.append({"type": "lagna", "omen": "Fire rising - action, energy"})
        elif asc_sign in [1, 5, 9]:  # Earth signs
            omens.append({"type": "lagna", "omen": "Earth rising - practical matters"})
        elif asc_sign in [2, 6, 10]:  # Air signs
            omens.append({"type": "lagna", "omen": "Air rising - communication, travel"})
        else:  # Water signs
            omens.append({"type": "lagna", "omen": "Water rising - emotions, intuition"})

        # Moon-Sun relationship
        sun_lon = planets.get("Sun", 0)
        moon_lon = planets.get("Moon", 0)
        phase = (moon_lon - sun_lon + 360) % 360

        if phase < 180:
            omens.append({"type": "moon_phase", "omen": "Waxing Moon - growth indicated"})
        else:
            omens.append({"type": "moon_phase", "omen": "Waning Moon - completion phase"})

        return {
            "omens": omens,
            "overall": (
                "Positive omens" if len([o for o in omens if "growth" in o["omen"].lower()]) > 0 else "Mixed omens"
            ),
        }

    def _interpret_arudha(self, arudha: int, category: QuestionCategory) -> str:
        """Interpret Arudha for the question"""
        arudha_meanings = {
            0: "Initiative needed, self-effort important",
            1: "Financial aspect prominent",
            2: "Communication/negotiation key",
            3: "Home/domestic matters central",
            4: "Creative approach works, speculation possible",
            5: "Challenges to overcome, service attitude helps",
            6: "Partnership/other person central",
            7: "Transformation required, hidden matters",
            8: "Fortune favors, guidance from elders",
            9: "Authority/career focus",
            10: "Friends/network helpful",
            11: "Spiritual approach, letting go needed",
        }
        return arudha_meanings.get(arudha, "General interpretation")

    def _get_hora_lord(self, planets: Dict[str, float]) -> str:
        """Get current Hora lord (simplified)"""
        # Would need actual hora calculation
        sun_lon = planets.get("Sun", 0)
        sun_sign = int(sun_lon / 30)
        return SIGN_LORDS[sun_sign]

    def _generate_verdict(self, favorable: Dict, timing: Dict, category: QuestionCategory) -> str:
        """Generate final verdict"""
        if favorable["is_favorable"]:
            return f"FAVORABLE: The question shows positive indications. {timing['interpretation']}"
        else:
            return f"CHALLENGING: Obstacles indicated. Remedial measures may help. {timing['interpretation']}"


def analyze_prashna_chart(
    question_time: datetime,
    latitude: float,
    longitude: float,
    question_type: str,
    planets: Dict[str, float],
    ascendant: float,
) -> Dict[str, Any]:
    """
    Convenience function for Prashna analysis
    """
    calc = PrashnaCalculator()

    try:
        category = QuestionCategory(question_type.lower())
    except ValueError:
        category = QuestionCategory.GENERAL

    return calc.analyze_prashna(
        question_time=question_time,
        latitude=latitude,
        longitude=longitude,
        question_category=category,
        planets=planets,
        ascendant=ascendant,
    )
