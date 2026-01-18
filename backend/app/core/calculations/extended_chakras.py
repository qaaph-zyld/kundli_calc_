"""
Extended Chakra Systems
PGF Protocol: CHAKRA_002
Gate: GATE_5
Version: 1.0.0

Implements:
1. Surya Chakra (Solar Wheel)
2. Chandra Chakra (Lunar Wheel)
3. Bhava Chakra (House Wheel)
4. Rashi Chakra (Sign Wheel)
5. Nakshatra Chakra (27-Star Wheel)
6. Navamsa Chakra
7. Shodashamsa Chakra
"""

import math
from dataclasses import dataclass, field
from datetime import datetime
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
class ChakraCell:
    """A cell in a chakra diagram"""

    position: int
    sign: str = ""
    nakshatra: str = ""
    planets: List[str] = field(default_factory=list)
    degree: float = 0.0
    quality: str = "neutral"


class SuryaChakra:
    """
    Surya Chakra (Solar Wheel)

    Based on Sun's position. 12 spokes representing houses from Sun.
    Used for analyzing Sun-based life themes and vitality.
    """

    def __init__(self):
        self.name = "Surya Chakra"
        self.spokes = 12

    def calculate(self, sun_longitude: float, planets: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate Surya Chakra

        Places Sun at center and arranges houses from Sun's position.
        """
        sun_sign = int(sun_longitude / 30)

        # Create 12 houses from Sun
        houses = []
        for i in range(12):
            house_sign = (sun_sign + i) % 12

            # Find planets in this house
            planets_in_house = []
            for planet, lon in planets.items():
                if planet == "Sun":
                    continue
                planet_sign = int(lon / 30)
                if planet_sign == house_sign:
                    planets_in_house.append({"planet": planet, "degree": round(lon % 30, 2)})

            # House significations from Sun
            significations = self._get_sun_house_meaning(i + 1)

            houses.append(
                {
                    "house": i + 1,
                    "sign": SIGNS[house_sign],
                    "planets": planets_in_house,
                    "significations": significations,
                    "strength": self._calculate_house_strength(i + 1, planets_in_house),
                }
            )

        # Analyze vitality areas
        vitality_analysis = self._analyze_vitality(houses, planets)

        return {
            "chakra_name": self.name,
            "sun_sign": SIGNS[sun_sign],
            "sun_degree": round(sun_longitude % 30, 2),
            "houses": houses,
            "vitality_analysis": vitality_analysis,
            "interpretation": self._generate_interpretation(houses, sun_sign),
        }

    def _get_sun_house_meaning(self, house: int) -> List[str]:
        """Get significations for houses from Sun"""
        meanings = {
            1: ["Self-identity", "Vitality", "Soul purpose"],
            2: ["Resources", "Values", "Self-worth"],
            3: ["Expression", "Courage", "Will power"],
            4: ["Heart", "Inner authority", "Core self"],
            5: ["Creativity", "Children", "Divine grace"],
            6: ["Service", "Health routines", "Enemies of ego"],
            7: ["Partners", "Public image", "Others' perception"],
            8: ["Transformation", "Hidden strengths", "Regeneration"],
            9: ["Dharma", "Father", "Higher purpose"],
            10: ["Career", "Public status", "Life direction"],
            11: ["Aspirations", "Gains", "Elder support"],
            12: ["Liberation", "Losses", "Spiritual growth"],
        }
        return meanings.get(house, [])

    def _calculate_house_strength(self, house: int, planets: List[Dict]) -> str:
        """Calculate house strength in Surya Chakra"""
        if not planets:
            return "empty"

        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
        benefic_count = sum(1 for p in planets if p["planet"] in benefics)

        if benefic_count > 0:
            return "strong"
        return "afflicted"

    def _analyze_vitality(self, houses: List[Dict], planets: Dict[str, float]) -> Dict[str, Any]:
        """Analyze vitality based on Surya Chakra"""
        # First house = vitality
        vitality_house = houses[0]
        vitality_score = 100

        # Deduct for malefics in 1st
        malefics = ["Saturn", "Mars", "Rahu", "Ketu"]
        for p in vitality_house["planets"]:
            if p["planet"] in malefics:
                vitality_score -= 15

        # 6th house = health challenges
        sixth_house = houses[5]
        health_challenges = len(sixth_house["planets"]) * 10

        return {
            "vitality_score": max(0, vitality_score),
            "health_challenges": health_challenges,
            "strength_areas": [h["house"] for h in houses if h["strength"] == "strong"],
            "recommendation": self._get_vitality_recommendation(vitality_score),
        }

    def _get_vitality_recommendation(self, score: int) -> str:
        """Get vitality recommendation"""
        if score >= 80:
            return "Strong vitality. Sun worship enhances life force."
        elif score >= 60:
            return "Moderate vitality. Regular surya namaskar recommended."
        else:
            return "Vitality needs support. Copper in water, ruby gemstone may help."

    def _generate_interpretation(self, houses: List[Dict], sun_sign: int) -> str:
        """Generate overall interpretation"""
        strong_houses = [h["house"] for h in houses if h["strength"] == "strong"]

        if strong_houses:
            areas = [self._get_sun_house_meaning(h)[0] for h in strong_houses[:3]]
            return f"Sun strengthens: {', '.join(areas)}. Focus life energy here."
        return "Balanced solar energy. Cultivate Sun through discipline and purpose."


class ChandraChakra:
    """
    Chandra Chakra (Lunar Wheel)

    Based on Moon's position. 27 spokes representing nakshatras.
    Used for analyzing emotional patterns and mind.
    """

    def __init__(self):
        self.name = "Chandra Chakra"
        self.spokes = 27

    def calculate(self, moon_longitude: float, planets: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate Chandra Chakra

        Places Moon at center and arranges nakshatras from Moon's position.
        """
        moon_nak = int(moon_longitude / (360 / 27))
        moon_sign = int(moon_longitude / 30)

        # Create 27 nakshatra cells
        nakshatras = []
        for i in range(27):
            nak_idx = (moon_nak + i) % 27

            # Nakshatra longitude range
            nak_start = nak_idx * (360 / 27)
            nak_end = (nak_idx + 1) * (360 / 27)

            # Find planets in this nakshatra
            planets_in_nak = []
            for planet, lon in planets.items():
                if nak_start <= lon < nak_end:
                    planets_in_nak.append({"planet": planet, "degree": round(lon, 2)})

            # Nakshatra quality
            quality = self._get_nakshatra_quality(nak_idx)

            nakshatras.append(
                {
                    "position": i + 1,
                    "nakshatra": NAKSHATRAS[nak_idx],
                    "lord": self._get_nakshatra_lord(nak_idx),
                    "planets": planets_in_nak,
                    "quality": quality,
                    "tara": self._get_tara(i + 1),
                }
            )

        # Emotional analysis
        emotional_analysis = self._analyze_emotions(nakshatras, moon_longitude)

        return {
            "chakra_name": self.name,
            "moon_nakshatra": NAKSHATRAS[moon_nak],
            "moon_sign": SIGNS[moon_sign],
            "moon_degree": round(moon_longitude % 30, 2),
            "nakshatras": nakshatras,
            "emotional_analysis": emotional_analysis,
            "mind_pattern": self._analyze_mind_pattern(moon_nak),
        }

    def _get_nakshatra_lord(self, nak_idx: int) -> str:
        """Get nakshatra lord"""
        lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"] * 3
        return lords[nak_idx]

    def _get_nakshatra_quality(self, nak_idx: int) -> str:
        """Get nakshatra quality"""
        # Deva, Manushya, Rakshasa
        qualities = [
            "Deva",
            "Manushya",
            "Rakshasa",
            "Manushya",
            "Deva",
            "Rakshasa",
            "Deva",
            "Deva",
            "Rakshasa",
            "Rakshasa",
            "Manushya",
            "Manushya",
            "Deva",
            "Rakshasa",
            "Deva",
            "Rakshasa",
            "Deva",
            "Rakshasa",
            "Rakshasa",
            "Manushya",
            "Manushya",
            "Deva",
            "Rakshasa",
            "Rakshasa",
            "Manushya",
            "Manushya",
            "Deva",
        ]
        return qualities[nak_idx]

    def _get_tara(self, position: int) -> Dict[str, Any]:
        """Get Tara (star relationship) for position"""
        tara_num = ((position - 1) % 9) + 1
        tara_names = {
            1: ("Janma", "Birth star - sensitive"),
            2: ("Sampat", "Wealth - favorable"),
            3: ("Vipat", "Danger - challenging"),
            4: ("Kshema", "Well-being - good"),
            5: ("Pratyak", "Obstacles - difficult"),
            6: ("Sadhana", "Achievement - good"),
            7: ("Vadha", "Death - very bad"),
            8: ("Mitra", "Friend - favorable"),
            9: ("Ati Mitra", "Great friend - excellent"),
        }
        name, meaning = tara_names.get(tara_num, ("", ""))
        return {"number": tara_num, "name": name, "meaning": meaning}

    def _analyze_emotions(self, nakshatras: List[Dict], moon_lon: float) -> Dict[str, Any]:
        """Analyze emotional patterns"""
        moon_nak = int(moon_lon / (360 / 27))
        quality = self._get_nakshatra_quality(moon_nak)

        emotional_nature = {
            "Deva": "Gentle, spiritual, peace-loving",
            "Manushya": "Balanced, practical, adaptable",
            "Rakshasa": "Intense, powerful, transformative",
        }

        return {
            "emotional_nature": emotional_nature.get(quality, "Mixed"),
            "moon_quality": quality,
            "sensitivity_level": "High" if quality == "Deva" else "Medium" if quality == "Manushya" else "Low",
            "recommendation": self._get_emotional_recommendation(quality),
        }

    def _get_emotional_recommendation(self, quality: str) -> str:
        """Get emotional balance recommendation"""
        if quality == "Deva":
            return "Protect sensitivity. Moon-gazing and meditation beneficial."
        elif quality == "Manushya":
            return "Balance emotions with logic. Journaling helps process feelings."
        else:
            return "Channel intensity constructively. Physical activity releases emotional energy."

    def _analyze_mind_pattern(self, moon_nak: int) -> Dict[str, Any]:
        """Analyze mind patterns based on Moon nakshatra"""
        # Categorize mind types
        creative_naks = [0, 3, 10, 11, 12, 19]  # Ashwini, Rohini, etc.
        analytical_naks = [2, 5, 13, 16, 22, 25]  # Krittika, Ardra, etc.
        emotional_naks = [6, 7, 14, 17, 20, 26]  # Punarvasu, Pushya, etc.

        if moon_nak in creative_naks:
            mind_type = "Creative"
            strengths = ["Innovation", "Artistic vision", "Original thinking"]
        elif moon_nak in analytical_naks:
            mind_type = "Analytical"
            strengths = ["Logic", "Research", "Problem-solving"]
        elif moon_nak in emotional_naks:
            mind_type = "Emotional"
            strengths = ["Empathy", "Intuition", "Caring"]
        else:
            mind_type = "Practical"
            strengths = ["Execution", "Planning", "Organization"]

        return {
            "mind_type": mind_type,
            "strengths": strengths,
            "learning_style": f"{mind_type}-based learning works best",
        }


class BhavaChakra:
    """
    Bhava Chakra (House Wheel)

    Traditional 12-house chart with house cusps and significations.
    """

    def __init__(self):
        self.name = "Bhava Chakra"

    def calculate(self, ascendant: float, planets: Dict[str, float]) -> Dict[str, Any]:
        """Calculate Bhava Chakra"""
        asc_sign = int(ascendant / 30)

        houses = []
        for i in range(12):
            house_sign = (asc_sign + i) % 12

            # Equal house system - each house is 30 degrees
            house_start = (asc_sign * 30 + i * 30) % 360
            house_end = (house_start + 30) % 360

            # Find planets in this house
            planets_in_house = []
            for planet, lon in planets.items():
                # Normalize both to same range
                planet_pos = lon % 360
                if house_start <= planet_pos < house_start + 30:
                    planets_in_house.append(
                        {
                            "planet": planet,
                            "degree": round(lon % 30, 2),
                            "dignity": self._get_dignity(planet, house_sign),
                        }
                    )

            houses.append(
                {
                    "house": i + 1,
                    "sign": SIGNS[house_sign],
                    "cusp": round(house_start, 2),
                    "planets": planets_in_house,
                    "lord": self._get_sign_lord(house_sign),
                    "karakas": self._get_house_karakas(i + 1),
                    "bhava_madhya": round((house_start + 15) % 360, 2),
                }
            )

        return {
            "chakra_name": self.name,
            "ascendant": SIGNS[asc_sign],
            "houses": houses,
            "house_strengths": self._analyze_house_strengths(houses),
        }

    def _get_sign_lord(self, sign: int) -> str:
        """Get sign lord"""
        lords = [
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
        return lords[sign]

    def _get_dignity(self, planet: str, sign: int) -> str:
        """Get planet dignity in sign"""
        exaltation = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, "Jupiter": 3, "Venus": 11, "Saturn": 6}
        debilitation = {"Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11, "Jupiter": 9, "Venus": 5, "Saturn": 0}
        own_signs = {
            "Sun": [4],
            "Moon": [3],
            "Mars": [0, 7],
            "Mercury": [2, 5],
            "Jupiter": [8, 11],
            "Venus": [1, 6],
            "Saturn": [9, 10],
        }

        if exaltation.get(planet) == sign:
            return "Exalted"
        if debilitation.get(planet) == sign:
            return "Debilitated"
        if sign in own_signs.get(planet, []):
            return "Own Sign"
        return "Neutral"

    def _get_house_karakas(self, house: int) -> List[str]:
        """Get natural karakas for each house"""
        karakas = {
            1: ["Sun", "Mars"],
            2: ["Jupiter", "Mercury"],
            3: ["Mars", "Mercury"],
            4: ["Moon", "Venus"],
            5: ["Jupiter", "Sun"],
            6: ["Mars", "Saturn"],
            7: ["Venus", "Jupiter"],
            8: ["Saturn"],
            9: ["Jupiter", "Sun"],
            10: ["Saturn", "Sun", "Mercury"],
            11: ["Jupiter"],
            12: ["Saturn", "Ketu"],
        }
        return karakas.get(house, [])

    def _analyze_house_strengths(self, houses: List[Dict]) -> Dict[str, Any]:
        """Analyze overall house strengths"""
        strong_houses = []
        weak_houses = []

        for house in houses:
            planet_count = len(house["planets"])
            has_benefic = any(p["planet"] in ["Jupiter", "Venus", "Mercury", "Moon"] for p in house["planets"])
            has_lord = house["lord"] in [p["planet"] for p in house["planets"]]

            if planet_count > 0 and (has_benefic or has_lord):
                strong_houses.append(house["house"])
            elif planet_count == 0:
                weak_houses.append(house["house"])

        return {
            "strong_houses": strong_houses,
            "weak_houses": weak_houses,
            "kendras": [1, 4, 7, 10],
            "trikonas": [1, 5, 9],
            "dusthanas": [6, 8, 12],
        }


class NakshatraChakra:
    """
    Nakshatra Chakra (27-Star Wheel)

    Complete 27-nakshatra circular representation.
    """

    def __init__(self):
        self.name = "Nakshatra Chakra"

    def calculate(self, planets: Dict[str, float]) -> Dict[str, Any]:
        """Calculate Nakshatra Chakra with all planets placed"""
        nakshatra_data = []

        for i in range(27):
            nak_start = i * (360 / 27)
            nak_end = (i + 1) * (360 / 27)

            planets_here = []
            for planet, lon in planets.items():
                if nak_start <= lon < nak_end:
                    pada = int((lon - nak_start) / (360 / 27 / 4)) + 1
                    planets_here.append({"planet": planet, "pada": pada, "exact_degree": round(lon, 2)})

            nakshatra_data.append(
                {
                    "index": i,
                    "name": NAKSHATRAS[i],
                    "lord": self._get_lord(i),
                    "deity": self._get_deity(i),
                    "symbol": self._get_symbol(i),
                    "planets": planets_here,
                    "nature": self._get_nature(i),
                }
            )

        return {
            "chakra_name": self.name,
            "nakshatras": nakshatra_data,
            "summary": self._generate_summary(nakshatra_data),
        }

    def _get_lord(self, idx: int) -> str:
        """Get nakshatra lord"""
        lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"] * 3
        return lords[idx]

    def _get_deity(self, idx: int) -> str:
        """Get ruling deity"""
        deities = [
            "Ashwini Kumaras",
            "Yama",
            "Agni",
            "Brahma",
            "Soma",
            "Rudra",
            "Aditi",
            "Brihaspati",
            "Sarpa",
            "Pitris",
            "Bhaga",
            "Aryaman",
            "Savitar",
            "Tvashtar",
            "Vayu",
            "Indragni",
            "Mitra",
            "Indra",
            "Nirriti",
            "Apas",
            "Vishvadevas",
            "Vishnu",
            "Vasus",
            "Varuna",
            "Ajaikapada",
            "Ahirbudhnya",
            "Pushan",
        ]
        return deities[idx] if idx < len(deities) else ""

    def _get_symbol(self, idx: int) -> str:
        """Get nakshatra symbol"""
        symbols = [
            "Horse head",
            "Yoni",
            "Razor",
            "Chariot",
            "Deer head",
            "Tear drop",
            "Bow",
            "Flower",
            "Serpent",
            "Throne",
            "Hammock",
            "Bed",
            "Hand",
            "Pearl",
            "Coral",
            "Triumphal arch",
            "Lotus",
            "Earring",
            "Elephant goad",
            "Fan",
            "Elephant tusk",
            "Ear",
            "Drum",
            "Circle",
            "Sword",
            "Twin",
            "Fish",
        ]
        return symbols[idx] if idx < len(symbols) else ""

    def _get_nature(self, idx: int) -> str:
        """Get nakshatra nature/guna"""
        natures = [
            "Swift",
            "Fierce",
            "Mixed",
            "Fixed",
            "Soft",
            "Sharp",
            "Movable",
            "Light",
            "Sharp",
            "Fierce",
            "Fierce",
            "Fixed",
            "Light",
            "Soft",
            "Movable",
            "Mixed",
            "Soft",
            "Sharp",
            "Sharp",
            "Fierce",
            "Fixed",
            "Movable",
            "Movable",
            "Movable",
            "Fierce",
            "Fixed",
            "Soft",
        ]
        return natures[idx] if idx < len(natures) else "Mixed"

    def _generate_summary(self, nakshatras: List[Dict]) -> Dict[str, Any]:
        """Generate summary of planetary distribution"""
        occupied = [n for n in nakshatras if n["planets"]]

        return {
            "occupied_nakshatras": len(occupied),
            "empty_nakshatras": 27 - len(occupied),
            "planets_by_lord": self._group_by_lord(nakshatras),
        }

    def _group_by_lord(self, nakshatras: List[Dict]) -> Dict[str, List[str]]:
        """Group planets by their nakshatra lord"""
        by_lord = {}
        for nak in nakshatras:
            for p in nak["planets"]:
                lord = nak["lord"]
                if lord not in by_lord:
                    by_lord[lord] = []
                by_lord[lord].append(p["planet"])
        return by_lord


def calculate_all_chakras(
    sun_longitude: float, moon_longitude: float, ascendant: float, planets: Dict[str, float]
) -> Dict[str, Any]:
    """
    Calculate all chakra systems
    """
    surya = SuryaChakra()
    chandra = ChandraChakra()
    bhava = BhavaChakra()
    nakshatra = NakshatraChakra()

    return {
        "surya_chakra": surya.calculate(sun_longitude, planets),
        "chandra_chakra": chandra.calculate(moon_longitude, planets),
        "bhava_chakra": bhava.calculate(ascendant, planets),
        "nakshatra_chakra": nakshatra.calculate(planets),
    }
