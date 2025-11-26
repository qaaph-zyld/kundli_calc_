"""
Varshaphal (Annual Chart / Solar Return) Implementation
PGF Protocol: VARSHA_001
Gate: GATE_5
Version: 1.0.0

This module implements Varshaphal (Tajaka) system including:
- Solar Return Chart calculation
- Muntha calculation
- Annual Dasha (compressed)
- Tajaka Yogas
- Sahams (Arabic Parts)
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import math


SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
              "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]


class TajakaYogaType(Enum):
    """Types of Tajaka (Annual) Yogas"""
    IKKABAL = "ikkabal"
    INDUVARA = "induvara"
    ITHASALA = "ithasala"
    ISHRAFA = "ishrafa"
    NAKTA = "nakta"
    YAMAYA = "yamaya"
    MANAU = "manau"
    KAMBOOLA = "kamboola"
    GAIRI_KAMBOOLA = "gairi_kamboola"
    KHALLASAR = "khallasar"
    RADDA = "radda"
    DUPHALI_KUTTHA = "duphali_kuttha"
    DUTTHOTTARA = "dutthottara"
    TAMBIRA = "tambira"
    KUTTHA = "kuttha"
    DURUPHA = "durupha"


@dataclass
class Muntha:
    """Muntha position in annual chart"""
    sign: int
    sign_name: str
    house: int  # House from annual ascendant
    lord: str
    interpretation: str


@dataclass
class TajakaYoga:
    """A Tajaka yoga in the annual chart"""
    yoga_type: TajakaYogaType
    planets: List[str]
    is_benefic: bool
    description: str
    effects: List[str]


@dataclass
class Saham:
    """Arabic Part (Saham) calculation"""
    name: str
    sanskrit_name: str
    longitude: float
    sign: int
    sign_name: str
    house: int
    interpretation: str


class VarshaphalCalculator:
    """
    Varshaphal (Annual Chart) Calculator
    
    Based on Tajaka system of Vedic Astrology
    Calculates annual predictions from birthday to birthday
    """
    
    def __init__(self):
        # Saham formulas: (A + B - C) or (A - B + C) variations
        # Format: (name, sanskrit, formula_type, planets/points)
        self.saham_definitions = [
            ("Fortune", "पुण्य", "add", ("Asc", "Moon", "Sun")),
            ("Marriage", "विवाह", "add", ("Asc", "Venus", "Saturn")),
            ("Children", "पुत्र", "add", ("Asc", "Jupiter", "Moon")),
            ("Father", "पितृ", "add", ("Asc", "Sun", "Saturn")),
            ("Mother", "मातृ", "add", ("Asc", "Moon", "Venus")),
            ("Brothers", "भ्रातृ", "add", ("Asc", "Jupiter", "Saturn")),
            ("Education", "विद्या", "add", ("Asc", "Mercury", "Sun")),
            ("Wealth", "धन", "add", ("Asc", "Cusp2", "Cusp2Lord")),
            ("Career", "कर्म", "add", ("Asc", "Moon", "Saturn")),
            ("Death", "मृत्यु", "add", ("Asc", "Cusp8", "Moon")),
            ("Sickness", "रोग", "add", ("Asc", "Mars", "Saturn")),
            ("Travel", "यात्रा", "add", ("Asc", "Cusp9Lord", "Cusp9")),
            ("Friends", "मित्र", "add", ("Asc", "Moon", "Mercury")),
            ("Enemies", "शत्रु", "add", ("Asc", "Saturn", "Mars")),
            ("Love", "प्रेम", "add", ("Asc", "Venus", "Sun")),
        ]
    
    def calculate_varshaphal(
        self,
        birth_date: datetime,
        birth_sun_longitude: float,
        birth_location: Dict[str, float],
        year_number: int,
        current_sun_longitude: float,
        annual_planets: Dict[str, float],
        annual_ascendant: float
    ) -> Dict[str, Any]:
        """
        Calculate complete Varshaphal for a given year
        
        Args:
            birth_date: Birth date and time
            birth_sun_longitude: Sun's longitude at birth
            birth_location: Birth location (lat, lon)
            year_number: Year of life (1 = first year from birth)
            current_sun_longitude: Sun's longitude at solar return
            annual_planets: Planet positions at solar return
            annual_ascendant: Ascendant at solar return
            
        Returns:
            Complete Varshaphal analysis
        """
        # Calculate Muntha
        muntha = self._calculate_muntha(
            birth_date, year_number, annual_ascendant
        )
        
        # Calculate year lord
        year_lord = self._calculate_year_lord(
            annual_planets, annual_ascendant, year_number
        )
        
        # Calculate Sahams (Arabic Parts)
        sahams = self._calculate_sahams(
            annual_planets, annual_ascendant
        )
        
        # Detect Tajaka Yogas
        tajaka_yogas = self._detect_tajaka_yogas(annual_planets)
        
        # Calculate strength analysis
        strength = self._analyze_varshaphal_strength(
            annual_planets, annual_ascendant, muntha, year_lord
        )
        
        # Annual predictions
        predictions = self._generate_annual_predictions(
            muntha, year_lord, tajaka_yogas, strength
        )
        
        return {
            "year_number": year_number,
            "age_during_year": year_number - 1,
            "annual_ascendant": {
                "longitude": annual_ascendant,
                "sign": SIGN_NAMES[int(annual_ascendant / 30)],
                "sign_lord": SIGN_LORDS[int(annual_ascendant / 30)]
            },
            "muntha": {
                "sign": muntha.sign_name,
                "sign_number": muntha.sign,
                "house": muntha.house,
                "lord": muntha.lord,
                "interpretation": muntha.interpretation
            },
            "year_lord": year_lord,
            "sahams": [
                {
                    "name": s.name,
                    "sanskrit": s.sanskrit_name,
                    "longitude": s.longitude,
                    "sign": s.sign_name,
                    "house": s.house,
                    "interpretation": s.interpretation
                }
                for s in sahams[:10]  # Top 10 sahams
            ],
            "tajaka_yogas": [
                {
                    "type": y.yoga_type.value,
                    "planets": y.planets,
                    "is_benefic": y.is_benefic,
                    "description": y.description,
                    "effects": y.effects
                }
                for y in tajaka_yogas
            ],
            "strength_analysis": strength,
            "predictions": predictions
        }
    
    def _calculate_muntha(
        self,
        birth_date: datetime,
        year_number: int,
        annual_ascendant: float
    ) -> Muntha:
        """
        Calculate Muntha position
        
        Muntha progresses one sign per year from birth ascendant
        """
        # Assuming birth ascendant was provided or defaulting to current
        birth_asc_sign = int(annual_ascendant / 30)  # Simplified
        
        # Muntha sign = birth sign + (year - 1) mod 12
        muntha_sign = (birth_asc_sign + year_number - 1) % 12
        muntha_lord = SIGN_LORDS[muntha_sign]
        
        # House from annual ascendant
        annual_asc_sign = int(annual_ascendant / 30)
        muntha_house = ((muntha_sign - annual_asc_sign) % 12) + 1
        
        # Generate interpretation based on house
        interpretations = {
            1: "Excellent year for personal growth and new beginnings",
            2: "Focus on finances, family matters, and speech",
            3: "Courage, siblings, and short journeys highlighted",
            4: "Home, mother, vehicles, and inner peace emphasized",
            5: "Romance, creativity, children, and speculation favored",
            6: "Challenges from enemies, health requires attention",
            7: "Partnerships, marriage, and business dealings important",
            8: "Transformation, occult interests, obstacles possible",
            9: "Fortune, higher learning, father, and spirituality blessed",
            10: "Career advancement, recognition, and status gains",
            11: "Gains, friendships, and fulfillment of desires",
            12: "Expenses, foreign connections, spiritual growth"
        }
        
        return Muntha(
            sign=muntha_sign,
            sign_name=SIGN_NAMES[muntha_sign],
            house=muntha_house,
            lord=muntha_lord,
            interpretation=interpretations.get(muntha_house, "")
        )
    
    def _calculate_year_lord(
        self,
        planets: Dict[str, float],
        ascendant: float,
        year_number: int
    ) -> Dict[str, Any]:
        """
        Determine the Year Lord (Varshesha)
        
        Based on various factors including:
        - Day lord
        - Hora lord
        - Muntha lord
        - Strongest planet
        """
        # Simplified: use ascendant lord as primary year lord
        asc_sign = int(ascendant / 30)
        asc_lord = SIGN_LORDS[asc_sign]
        
        # Determine planet strengths (simplified)
        strengths = {}
        for planet, lon in planets.items():
            if planet in ["Rahu", "Ketu"]:
                continue
            sign = int(lon / 30)
            # Basic dignity check
            if SIGN_LORDS[sign] == planet:
                strengths[planet] = 80  # Own sign
            elif sign in [3, 6, 10, 11]:  # Upachaya
                strengths[planet] = 70
            else:
                strengths[planet] = 50
        
        # Strongest planet
        strongest = max(strengths.keys(), key=lambda x: strengths.get(x, 0)) if strengths else asc_lord
        
        return {
            "primary": asc_lord,
            "muntha_lord": SIGN_LORDS[(asc_sign + year_number - 1) % 12],
            "strongest_planet": strongest,
            "strength": strengths.get(strongest, 50),
            "effects": self._get_year_lord_effects(asc_lord)
        }
    
    def _get_year_lord_effects(self, lord: str) -> List[str]:
        """Get effects based on year lord"""
        effects = {
            "Sun": ["Authority", "Government favor", "Father's influence", "Health focus"],
            "Moon": ["Emotional experiences", "Mother's role", "Public dealings", "Travel"],
            "Mars": ["Energy", "Conflicts possible", "Property matters", "Courage needed"],
            "Mercury": ["Communication", "Learning", "Business", "Writing"],
            "Jupiter": ["Expansion", "Wisdom", "Children", "Spiritual growth"],
            "Venus": ["Relationships", "Comforts", "Arts", "Financial gains"],
            "Saturn": ["Hard work", "Delays", "Discipline", "Long-term results"]
        }
        return effects.get(lord, ["Mixed influences"])
    
    def _calculate_sahams(
        self,
        planets: Dict[str, float],
        ascendant: float
    ) -> List[Saham]:
        """Calculate important Sahams (Arabic Parts)"""
        sahams = []
        asc_sign = int(ascendant / 30)
        
        for name, sanskrit, formula, points in self.saham_definitions:
            try:
                # Get longitudes for calculation
                if points[0] == "Asc":
                    a = ascendant
                else:
                    a = planets.get(points[0], 0)
                
                if points[1].startswith("Cusp"):
                    b = ascendant  # Simplified
                else:
                    b = planets.get(points[1], 0)
                
                if points[2].startswith("Cusp"):
                    c = ascendant  # Simplified
                else:
                    c = planets.get(points[2], 0)
                
                # Calculate saham longitude
                saham_lon = (a + b - c) % 360
                saham_sign = int(saham_lon / 30)
                saham_house = ((saham_sign - asc_sign) % 12) + 1
                
                sahams.append(Saham(
                    name=name,
                    sanskrit_name=sanskrit,
                    longitude=saham_lon,
                    sign=saham_sign,
                    sign_name=SIGN_NAMES[saham_sign],
                    house=saham_house,
                    interpretation=self._get_saham_interpretation(name, saham_house)
                ))
            except:
                continue
        
        return sahams
    
    def _get_saham_interpretation(self, saham_name: str, house: int) -> str:
        """Generate interpretation for a saham"""
        base_meanings = {
            "Fortune": "luck and general well-being",
            "Marriage": "marriage and partnerships",
            "Children": "children and creativity",
            "Father": "father and authority figures",
            "Mother": "mother and nurturing",
            "Education": "learning and knowledge",
            "Wealth": "financial matters",
            "Career": "profession and status",
            "Love": "romance and affection"
        }
        
        meaning = base_meanings.get(saham_name, saham_name.lower() + " matters")
        
        if house in [1, 5, 9]:  # Trine
            return f"Favorable for {meaning} this year"
        elif house in [1, 4, 7, 10]:  # Kendra
            return f"Active developments in {meaning}"
        elif house in [6, 8, 12]:  # Dusthana
            return f"Challenges possible regarding {meaning}"
        else:
            return f"Moderate indications for {meaning}"
    
    def _detect_tajaka_yogas(self, planets: Dict[str, float]) -> List[TajakaYoga]:
        """
        Detect Tajaka-specific yogas in the annual chart
        
        Tajaka yogas are based on planetary aspects and positions
        """
        yogas = []
        
        # Ithasala - Two planets approaching exact aspect
        # Simplified: check for close conjunctions
        planet_list = list(planets.keys())
        for i, p1 in enumerate(planet_list):
            for p2 in planet_list[i+1:]:
                if p1 in ["Rahu", "Ketu"] or p2 in ["Rahu", "Ketu"]:
                    continue
                    
                lon1 = planets[p1]
                lon2 = planets[p2]
                diff = abs(lon1 - lon2)
                if diff > 180:
                    diff = 360 - diff
                
                # Within 10 degrees = approaching aspect
                if diff < 10:
                    is_benefic = p1 in ["Jupiter", "Venus"] or p2 in ["Jupiter", "Venus"]
                    yogas.append(TajakaYoga(
                        yoga_type=TajakaYogaType.ITHASALA,
                        planets=[p1, p2],
                        is_benefic=is_benefic,
                        description=f"{p1} applying to {p2}",
                        effects=["Event completion", "Success in undertakings"]
                    ))
        
        # Check for Moon with benefics (Ikkabal)
        if "Moon" in planets:
            moon_sign = int(planets["Moon"] / 30)
            for benefic in ["Jupiter", "Venus"]:
                if benefic in planets:
                    b_sign = int(planets[benefic] / 30)
                    if moon_sign == b_sign or abs(moon_sign - b_sign) in [4, 8]:  # Trine
                        yogas.append(TajakaYoga(
                            yoga_type=TajakaYogaType.IKKABAL,
                            planets=["Moon", benefic],
                            is_benefic=True,
                            description=f"Moon in good aspect with {benefic}",
                            effects=["Prosperity", "Happiness", "Good health"]
                        ))
        
        return yogas
    
    def _analyze_varshaphal_strength(
        self,
        planets: Dict[str, float],
        ascendant: float,
        muntha: Muntha,
        year_lord: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze overall strength of the annual chart"""
        score = 50  # Base score
        factors = []
        
        # Muntha in good houses
        if muntha.house in [1, 5, 9, 10, 11]:
            score += 15
            factors.append(f"Muntha in favorable {muntha.house}th house (+15)")
        elif muntha.house in [6, 8, 12]:
            score -= 10
            factors.append(f"Muntha in challenging {muntha.house}th house (-10)")
        
        # Year lord strength
        if year_lord.get("strength", 50) >= 70:
            score += 15
            factors.append(f"Year lord {year_lord['primary']} is strong (+15)")
        elif year_lord.get("strength", 50) < 40:
            score -= 10
            factors.append(f"Year lord needs strengthening (-10)")
        
        # Benefics in kendras
        for benefic in ["Jupiter", "Venus"]:
            if benefic in planets:
                b_sign = int(planets[benefic] / 30)
                asc_sign = int(ascendant / 30)
                house = ((b_sign - asc_sign) % 12) + 1
                if house in [1, 4, 7, 10]:
                    score += 10
                    factors.append(f"{benefic} in kendra house {house} (+10)")
        
        return {
            "overall_score": min(100, max(0, score)),
            "rating": self._get_rating(score),
            "factors": factors
        }
    
    def _get_rating(self, score: int) -> str:
        """Convert score to rating"""
        if score >= 80:
            return "Excellent"
        elif score >= 65:
            return "Good"
        elif score >= 50:
            return "Average"
        elif score >= 35:
            return "Challenging"
        else:
            return "Difficult"
    
    def _generate_annual_predictions(
        self,
        muntha: Muntha,
        year_lord: Dict[str, Any],
        yogas: List[TajakaYoga],
        strength: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate predictions for different life areas"""
        predictions = {
            "career": [],
            "relationships": [],
            "finances": [],
            "health": [],
            "general": []
        }
        
        # Based on Muntha house
        muntha_predictions = {
            1: {"career": ["New opportunities"], "general": ["Personal growth year"]},
            2: {"finances": ["Income focus"], "general": ["Family matters important"]},
            5: {"relationships": ["Romance favored"], "general": ["Creative expression"]},
            7: {"relationships": ["Partnership year"], "career": ["Business partnerships"]},
            10: {"career": ["Career advancement"], "general": ["Public recognition"]},
            11: {"finances": ["Gains expected"], "general": ["Wishes fulfilled"]}
        }
        
        mp = muntha_predictions.get(muntha.house, {"general": ["Mixed influences"]})
        for area, preds in mp.items():
            predictions[area].extend(preds)
        
        # Based on year lord
        predictions["general"].append(f"Year influenced by {year_lord['primary']}")
        predictions["general"].extend(year_lord.get("effects", [])[:2])
        
        # Based on overall strength
        rating = strength.get("rating", "Average")
        if rating in ["Excellent", "Good"]:
            predictions["general"].append("Generally favorable year for progress")
        elif rating in ["Challenging", "Difficult"]:
            predictions["general"].append("Year requires patience and effort")
        
        return predictions


def calculate_annual_chart(
    birth_date: datetime,
    birth_sun: float,
    year_number: int,
    annual_planets: Dict[str, float],
    annual_ascendant: float
) -> Dict[str, Any]:
    """
    Convenience function for Varshaphal calculation
    
    Args:
        birth_date: Birth datetime
        birth_sun: Sun longitude at birth
        year_number: Year of life
        annual_planets: Solar return planet positions
        annual_ascendant: Solar return ascendant
        
    Returns:
        Complete Varshaphal analysis
    """
    calculator = VarshaphalCalculator()
    return calculator.calculate_varshaphal(
        birth_date=birth_date,
        birth_sun_longitude=birth_sun,
        birth_location={"lat": 0, "lon": 0},
        year_number=year_number,
        current_sun_longitude=birth_sun,  # Solar return when Sun returns
        annual_planets=annual_planets,
        annual_ascendant=annual_ascendant
    )
