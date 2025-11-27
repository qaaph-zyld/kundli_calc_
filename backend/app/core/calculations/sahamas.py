"""
Sahamas (Arabic Parts/Lots) Calculator
PGF Protocol: SAHAMA_001
Gate: GATE_5
Version: 1.0.0

Implements 36 traditional Sahamas as per Jataka Parijata and other classics:
- Punya Saham (Fortune)
- Vivaha Saham (Marriage)
- Santana Saham (Children)
- Matri Saham (Mother)
- Pitri Saham (Father)
- And 31 more...
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]


@dataclass
class Sahama:
    """A calculated Sahama point"""
    name: str
    sanskrit_name: str
    longitude: float
    sign: str
    degree: float
    house: int
    formula: str
    signification: str


class SahamaCalculator:
    """
    Complete Sahama Calculator
    
    Sahamas are sensitive points calculated using the formula:
    Saham = A + B - C (adjusted to 0-360 range)
    
    Day/Night birth may reverse B and C in some traditions.
    """
    
    # Sahama definitions: (name, sanskrit, A, B, C, signification)
    # A, B, C are: "Asc", "Sun", "Moon", "Mars", "Mercury", "Jupiter", 
    #               "Venus", "Saturn", "Rahu", "Ketu", or house cusp "H1"-"H12"
    
    SAHAMAS = {
        "punya": {
            "name": "Punya Saham",
            "sanskrit": "पुण्य सहम",
            "day": ("Asc", "Moon", "Sun"),
            "night": ("Asc", "Sun", "Moon"),
            "signification": "Fortune, luck, merit, spiritual advancement"
        },
        "vivaha": {
            "name": "Vivaha Saham",
            "sanskrit": "विवाह सहम",
            "day": ("Asc", "Venus", "Saturn"),
            "night": ("Asc", "Saturn", "Venus"),
            "signification": "Marriage, partnership, spouse"
        },
        "santana": {
            "name": "Santana Saham",
            "sanskrit": "संतान सहम",
            "day": ("Asc", "Jupiter", "Moon"),
            "night": ("Asc", "Moon", "Jupiter"),
            "signification": "Children, progeny, creativity"
        },
        "matri": {
            "name": "Matri Saham",
            "sanskrit": "मातृ सहम",
            "day": ("Asc", "Moon", "Venus"),
            "night": ("Asc", "Venus", "Moon"),
            "signification": "Mother, maternal relationships"
        },
        "pitri": {
            "name": "Pitri Saham",
            "sanskrit": "पितृ सहम",
            "day": ("Asc", "Sun", "Saturn"),
            "night": ("Asc", "Saturn", "Sun"),
            "signification": "Father, paternal relationships"
        },
        "bhratri": {
            "name": "Bhratri Saham",
            "sanskrit": "भ्रातृ सहम",
            "day": ("Asc", "Jupiter", "Saturn"),
            "night": ("Asc", "Saturn", "Jupiter"),
            "signification": "Siblings, brothers"
        },
        "mrityu": {
            "name": "Mrityu Saham",
            "sanskrit": "मृत्यु सहम",
            "day": ("Asc", "Moon", "H8"),
            "night": ("Asc", "H8", "Moon"),
            "signification": "Death, transformation, longevity"
        },
        "roga": {
            "name": "Roga Saham",
            "sanskrit": "रोग सहम",
            "day": ("Asc", "Mars", "Saturn"),
            "night": ("Asc", "Saturn", "Mars"),
            "signification": "Disease, illness, health issues"
        },
        "kali": {
            "name": "Kali Saham",
            "sanskrit": "काली सहम",
            "day": ("Asc", "Saturn", "Jupiter"),
            "night": ("Asc", "Jupiter", "Saturn"),
            "signification": "Strife, quarrels, conflict"
        },
        "vidya": {
            "name": "Vidya Saham",
            "sanskrit": "विद्या सहम",
            "day": ("Asc", "Mercury", "Sun"),
            "night": ("Asc", "Sun", "Mercury"),
            "signification": "Education, knowledge, learning"
        },
        "karma": {
            "name": "Karma Saham",
            "sanskrit": "कर्म सहम",
            "day": ("Asc", "Sun", "Moon"),
            "night": ("Asc", "Moon", "Sun"),
            "signification": "Profession, work, duty"
        },
        "dhana": {
            "name": "Dhana Saham",
            "sanskrit": "धन सहम",
            "day": ("Asc", "H2", "H2_lord"),
            "night": ("Asc", "H2_lord", "H2"),
            "signification": "Wealth, money, finances"
        },
        "rajya": {
            "name": "Rajya Saham",
            "sanskrit": "राज्य सहम",
            "day": ("Asc", "Sun", "Saturn"),
            "night": ("Asc", "Saturn", "Sun"),
            "signification": "Kingdom, authority, power"
        },
        "paradesa": {
            "name": "Paradesa Saham",
            "sanskrit": "परदेश सहम",
            "day": ("Asc", "H9", "H9_lord"),
            "night": ("Asc", "H9_lord", "H9"),
            "signification": "Foreign lands, travel abroad"
        },
        "yashas": {
            "name": "Yashas Saham",
            "sanskrit": "यशस् सहम",
            "day": ("Asc", "Jupiter", "Sun"),
            "night": ("Asc", "Sun", "Jupiter"),
            "signification": "Fame, reputation, honor"
        },
        "jaya": {
            "name": "Jaya Saham",
            "sanskrit": "जय सहम",
            "day": ("Asc", "Mars", "Sun"),
            "night": ("Asc", "Sun", "Mars"),
            "signification": "Victory, success, triumph"
        },
        "vanika": {
            "name": "Vanika Saham",
            "sanskrit": "वाणिक सहम",
            "day": ("Asc", "Moon", "Mercury"),
            "night": ("Asc", "Mercury", "Moon"),
            "signification": "Business, commerce, trade"
        },
        "bandhava": {
            "name": "Bandhava Saham",
            "sanskrit": "बांधव सहम",
            "day": ("Asc", "Mercury", "Moon"),
            "night": ("Asc", "Moon", "Mercury"),
            "signification": "Relatives, kinsmen"
        },
        "karyasiddhi": {
            "name": "Karyasiddhi Saham",
            "sanskrit": "कार्यसिद्धि सहम",
            "day": ("Asc", "Saturn", "Sun"),
            "night": ("Asc", "Sun", "Saturn"),
            "signification": "Success in undertakings"
        },
        "shatru": {
            "name": "Shatru Saham",
            "sanskrit": "शत्रु सहम",
            "day": ("Asc", "Mars", "Saturn"),
            "night": ("Asc", "Saturn", "Mars"),
            "signification": "Enemies, opponents"
        },
        "apamrityu": {
            "name": "Apamrityu Saham",
            "sanskrit": "अपमृत्यु सहम",
            "day": ("Asc", "H8", "Moon"),
            "night": ("Asc", "Moon", "H8"),
            "signification": "Unnatural death, accidents"
        },
        "parakrama": {
            "name": "Parakrama Saham",
            "sanskrit": "पराक्रम सहम",
            "day": ("Asc", "Mars", "Mercury"),
            "night": ("Asc", "Mercury", "Mars"),
            "signification": "Courage, valor, bravery"
        },
        "gaurava": {
            "name": "Gaurava Saham",
            "sanskrit": "गौरव सहम",
            "day": ("Asc", "Jupiter", "Moon"),
            "night": ("Asc", "Moon", "Jupiter"),
            "signification": "Dignity, respect, honor"
        },
        "saubhagya": {
            "name": "Saubhagya Saham",
            "sanskrit": "सौभाग्य सहम",
            "day": ("Asc", "Venus", "Moon"),
            "night": ("Asc", "Moon", "Venus"),
            "signification": "Good fortune, beauty"
        },
        "sastra": {
            "name": "Sastra Saham",
            "sanskrit": "शास्त्र सहम",
            "day": ("Asc", "Jupiter", "Saturn"),
            "night": ("Asc", "Saturn", "Jupiter"),
            "signification": "Scriptures, sciences, learning"
        },
        "guru": {
            "name": "Guru Saham",
            "sanskrit": "गुरु सहम",
            "day": ("Asc", "Sun", "Jupiter"),
            "night": ("Asc", "Jupiter", "Sun"),
            "signification": "Teacher, mentor, guide"
        },
        "mahatmya": {
            "name": "Mahatmya Saham",
            "sanskrit": "माहात्म्य सहम",
            "day": ("Asc", "Mars", "Sun"),
            "night": ("Asc", "Sun", "Mars"),
            "signification": "Greatness, magnanimity"
        },
        "krishi": {
            "name": "Krishi Saham",
            "sanskrit": "कृषि सहम",
            "day": ("Asc", "Saturn", "Venus"),
            "night": ("Asc", "Venus", "Saturn"),
            "signification": "Agriculture, farming"
        },
        "jalapatana": {
            "name": "Jalapatana Saham",
            "sanskrit": "जलपतन सहम",
            "day": ("Asc", "Venus", "Moon"),
            "night": ("Asc", "Moon", "Venus"),
            "signification": "Drowning, water-related danger"
        },
        "nauka": {
            "name": "Nauka Saham",
            "sanskrit": "नौका सहम",
            "day": ("Asc", "Saturn", "Moon"),
            "night": ("Asc", "Moon", "Saturn"),
            "signification": "Ships, boats, sea travel"
        },
        "vitta": {
            "name": "Vitta Saham",
            "sanskrit": "वित्त सहम",
            "day": ("Asc", "Moon", "Mercury"),
            "night": ("Asc", "Mercury", "Moon"),
            "signification": "Finances, monetary gains"
        },
        "mrityukara": {
            "name": "Mrityukara Saham",
            "sanskrit": "मृत्युकार सहम",
            "day": ("Asc", "H8_lord", "H8"),
            "night": ("Asc", "H8", "H8_lord"),
            "signification": "Cause of death"
        },
        "dustha": {
            "name": "Dustha Saham",
            "sanskrit": "दुष्ट सहम",
            "day": ("Asc", "Rahu", "Mars"),
            "night": ("Asc", "Mars", "Rahu"),
            "signification": "Wickedness, evil influences"
        },
        "ayush": {
            "name": "Ayush Saham",
            "sanskrit": "आयुष सहम",
            "day": ("Asc", "Moon", "Saturn"),
            "night": ("Asc", "Saturn", "Moon"),
            "signification": "Longevity, lifespan"
        },
        "karya": {
            "name": "Karya Saham",
            "sanskrit": "कार्य सहम",
            "day": ("Asc", "Sun", "Mars"),
            "night": ("Asc", "Mars", "Sun"),
            "signification": "Actions, deeds, work"
        },
        "siddhi": {
            "name": "Siddhi Saham",
            "sanskrit": "सिद्धि सहम",
            "day": ("Asc", "Mercury", "Jupiter"),
            "night": ("Asc", "Jupiter", "Mercury"),
            "signification": "Accomplishment, perfection"
        }
    }
    
    SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                  "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    
    def __init__(self):
        pass
    
    def _get_point_longitude(
        self,
        point: str,
        planets: Dict[str, float],
        ascendant: float
    ) -> float:
        """Get longitude for a point (planet, house, or house lord)"""
        if point == "Asc":
            return ascendant
        
        if point in planets:
            return planets[point]
        
        # House cusps (equal house system)
        if point.startswith("H") and not point.endswith("_lord"):
            house_num = int(point[1:])
            return (ascendant + (house_num - 1) * 30) % 360
        
        # House lord
        if point.endswith("_lord"):
            house_num = int(point[1:-5])
            house_sign = int((ascendant + (house_num - 1) * 30) / 30) % 12
            lord = self.SIGN_LORDS[house_sign]
            return planets.get(lord, 0)
        
        return 0
    
    def calculate_sahama(
        self,
        sahama_key: str,
        planets: Dict[str, float],
        ascendant: float,
        is_day_birth: bool
    ) -> Optional[Sahama]:
        """Calculate a single sahama"""
        if sahama_key not in self.SAHAMAS:
            return None
        
        sahama_def = self.SAHAMAS[sahama_key]
        
        # Get formula based on day/night birth
        formula_key = "day" if is_day_birth else "night"
        A, B, C = sahama_def[formula_key]
        
        # Get longitudes
        lon_A = self._get_point_longitude(A, planets, ascendant)
        lon_B = self._get_point_longitude(B, planets, ascendant)
        lon_C = self._get_point_longitude(C, planets, ascendant)
        
        # Calculate sahama: A + B - C
        sahama_lon = (lon_A + lon_B - lon_C) % 360
        
        # Get sign and degree
        sign_num = int(sahama_lon / 30)
        degree = sahama_lon % 30
        
        # Get house (from ascendant)
        asc_sign = int(ascendant / 30)
        house = ((sign_num - asc_sign + 12) % 12) + 1
        
        return Sahama(
            name=sahama_def["name"],
            sanskrit_name=sahama_def["sanskrit"],
            longitude=round(sahama_lon, 2),
            sign=SIGNS[sign_num],
            degree=round(degree, 2),
            house=house,
            formula=f"{A} + {B} - {C}",
            signification=sahama_def["signification"]
        )
    
    def calculate_all_sahamas(
        self,
        planets: Dict[str, float],
        ascendant: float,
        sun_longitude: float
    ) -> Dict[str, Any]:
        """
        Calculate all 36 sahamas
        
        Day birth: Sun above horizon (roughly 180° difference from Asc)
        Night birth: Sun below horizon
        """
        # Determine day/night birth
        sun_sign = int(sun_longitude / 30)
        asc_sign = int(ascendant / 30)
        
        # Simplified day/night determination
        # Sun in houses 7-12 from Asc = day birth
        sun_house = ((sun_sign - asc_sign + 12) % 12) + 1
        is_day_birth = 7 <= sun_house <= 12
        
        sahamas = {}
        by_house = {h: [] for h in range(1, 13)}
        
        for key in self.SAHAMAS:
            sahama = self.calculate_sahama(key, planets, ascendant, is_day_birth)
            if sahama:
                sahamas[key] = {
                    "name": sahama.name,
                    "sanskrit": sahama.sanskrit_name,
                    "longitude": sahama.longitude,
                    "sign": sahama.sign,
                    "degree": sahama.degree,
                    "house": sahama.house,
                    "formula": sahama.formula,
                    "signification": sahama.signification
                }
                by_house[sahama.house].append(sahama.name)
        
        # Key sahamas summary
        key_sahamas = {
            "fortune": sahamas.get("punya", {}),
            "marriage": sahamas.get("vivaha", {}),
            "children": sahamas.get("santana", {}),
            "career": sahamas.get("karma", {}),
            "health": sahamas.get("roga", {}),
            "longevity": sahamas.get("ayush", {})
        }
        
        return {
            "is_day_birth": is_day_birth,
            "sahamas": sahamas,
            "by_house": by_house,
            "key_sahamas": key_sahamas,
            "total_count": len(sahamas)
        }


def calculate_sahamas(
    planets: Dict[str, float],
    ascendant: float,
    sun_longitude: float
) -> Dict[str, Any]:
    """Convenience function to calculate all sahamas"""
    calculator = SahamaCalculator()
    return calculator.calculate_all_sahamas(planets, ascendant, sun_longitude)
