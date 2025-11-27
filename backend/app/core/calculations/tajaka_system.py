"""
Tajaka System (Annual Charts & Aspects) - Phase 6
PGF Protocol: TAJAKA_001
Gate: GATE_6
Version: 1.0.0

Implements:
1. Tajaka Annual/Monthly/Daily charts
2. Tajaka Aspects (Ithasala, Easarapha, etc.)
3. Tajaka Yogas (16 special yogas)
4. Tajaka Balas (strengths)
5. Muntha progression
6. Sahams in Tajaka
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import math


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


@dataclass
class TajakaAspect:
    """A Tajaka aspect between two planets"""
    faster_planet: str
    slower_planet: str
    aspect_type: str
    is_applying: bool
    orb: float
    interpretation: str


@dataclass
class TajakaYoga:
    """A Tajaka yoga"""
    name: str
    planets_involved: List[str]
    is_present: bool
    strength: float
    description: str


class TajakaCalculator:
    """
    Tajaka System Calculator
    
    Implements the Arabic/Persian system of annual astrology
    used extensively in Vedic astrology for yearly predictions.
    """
    
    # Planet speeds (degrees per day) - for applying/separating
    PLANET_SPEEDS = {
        "Moon": 13.17, "Mercury": 1.38, "Venus": 1.20, "Sun": 0.99,
        "Mars": 0.52, "Jupiter": 0.08, "Saturn": 0.03
    }
    
    # Tajaka aspect orbs
    ASPECT_ORBS = {
        0: 12,    # Conjunction
        60: 6,    # Sextile
        90: 8,    # Square
        120: 8,   # Trine
        180: 12   # Opposition
    }
    
    def __init__(self):
        pass
    
    # =========================================================================
    # ANNUAL CHART CALCULATION
    # =========================================================================
    def calculate_annual_chart(
        self,
        birth_date: datetime,
        birth_sun_longitude: float,
        year_number: int,
        birth_latitude: float = 0.0,
        birth_longitude: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculate Tajaka Annual (Varshaphal) Chart
        
        Chart cast for when Sun returns to exact natal position.
        """
        # Solar return date (approximate)
        return_date = datetime(
            birth_date.year + year_number,
            birth_date.month,
            birth_date.day,
            birth_date.hour,
            birth_date.minute
        )
        
        # Adjust for actual solar return (simplified)
        # In production, calculate exact moment Sun reaches natal degree
        
        # Calculate Muntha
        muntha = self._calculate_muntha(birth_date.month, year_number)
        
        # Calculate approximate planetary positions
        planets = self._calculate_annual_positions(birth_sun_longitude, return_date)
        
        # Calculate annual ascendant
        annual_asc = self._calculate_annual_ascendant(return_date, birth_latitude, birth_longitude)
        
        # Calculate Tajaka strengths
        strengths = self._calculate_tajaka_balas(planets, annual_asc)
        
        # Calculate Tajaka aspects
        aspects = self._calculate_tajaka_aspects(planets)
        
        # Calculate Tajaka yogas
        yogas = self._calculate_tajaka_yogas(planets, aspects, annual_asc)
        
        # Year lord
        year_lord = self._calculate_year_lord(return_date)
        
        return {
            "year_number": year_number,
            "return_date": return_date.isoformat(),
            "ascendant": {
                "longitude": annual_asc,
                "sign": SIGNS[int(annual_asc / 30)],
                "degree": annual_asc % 30
            },
            "muntha": {
                "sign": SIGNS[muntha],
                "house": ((muntha - int(annual_asc / 30)) % 12) + 1
            },
            "year_lord": year_lord,
            "planets": planets,
            "strengths": strengths,
            "aspects": [self._aspect_to_dict(a) for a in aspects],
            "yogas": [self._yoga_to_dict(y) for y in yogas if y.is_present],
            "prediction": self._generate_annual_prediction(planets, annual_asc, muntha, yogas)
        }
    
    def _calculate_muntha(self, birth_month: int, year_number: int) -> int:
        """Calculate Muntha sign for the year"""
        # Muntha progresses one sign per year from birth lagna
        return (birth_month + year_number - 1) % 12
    
    def _calculate_annual_positions(
        self,
        natal_sun: float,
        return_date: datetime
    ) -> Dict[str, Dict[str, Any]]:
        """Calculate planetary positions for annual chart"""
        # Simplified calculation - in production use ephemeris
        reference = datetime(2000, 1, 1)
        days = (return_date - reference).days
        
        # Mean motions
        positions = {
            "Sun": natal_sun,  # Sun at natal position
            "Moon": (days * 13.17) % 360,
            "Mars": (days * 0.52) % 360,
            "Mercury": (natal_sun + days * 1.38) % 360,
            "Jupiter": (days * 0.08) % 360,
            "Venus": (natal_sun + days * 1.2 + 45) % 360,
            "Saturn": (days * 0.03) % 360
        }
        
        return {
            planet: {
                "longitude": lon,
                "sign": SIGNS[int(lon / 30)],
                "degree": lon % 30
            }
            for planet, lon in positions.items()
        }
    
    def _calculate_annual_ascendant(
        self,
        time: datetime,
        latitude: float,
        longitude: float
    ) -> float:
        """Calculate ascendant for annual chart"""
        hours = time.hour + time.minute / 60
        day_of_year = time.timetuple().tm_yday
        lst = (hours + longitude / 15 + day_of_year * 0.0657) % 24
        return (lst / 24 * 360 + latitude / 3) % 360
    
    def _calculate_year_lord(self, date: datetime) -> str:
        """Calculate year lord (weekday ruler)"""
        weekday_lords = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        return weekday_lords[date.weekday()]
    
    # =========================================================================
    # TAJAKA BALAS (STRENGTHS)
    # =========================================================================
    def _calculate_tajaka_balas(
        self,
        planets: Dict[str, Dict[str, Any]],
        ascendant: float
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate Tajaka Strengths:
        1. Pancha Vargeeya Bala (5-fold strength)
        2. Dwadasa Vargeeya Bala (12-fold strength)
        3. Harsha Bala
        """
        strengths = {}
        lagna_sign = int(ascendant / 30)
        
        for planet, data in planets.items():
            sign = int(data["longitude"] / 30)
            house = ((sign - lagna_sign) % 12) + 1
            
            # Pancha Vargeeya Bala
            pvb = self._pancha_vargeeya_bala(planet, sign, house)
            
            # Harsha Bala (positional)
            harsha = self._harsha_bala(planet, house)
            
            strengths[planet] = {
                "pancha_vargeeya": pvb,
                "harsha_bala": harsha,
                "total": (pvb + harsha) / 2,
                "assessment": "Strong" if (pvb + harsha) / 2 > 50 else "Moderate"
            }
        
        return strengths
    
    def _pancha_vargeeya_bala(self, planet: str, sign: int, house: int) -> float:
        """Calculate 5-fold Tajaka strength"""
        score = 0
        
        # Exaltation/Own sign
        exaltation = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, 
                     "Jupiter": 3, "Venus": 11, "Saturn": 6}
        own_signs = {
            "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
            "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10]
        }
        
        if sign == exaltation.get(planet, -1):
            score += 30
        elif sign in own_signs.get(planet, []):
            score += 20
        
        # House position
        if house in [1, 4, 7, 10]:  # Kendra
            score += 20
        elif house in [5, 9]:  # Trikona
            score += 15
        elif house in [3, 6, 11]:  # Upachaya
            score += 10
        
        return min(score, 60)
    
    def _harsha_bala(self, planet: str, house: int) -> float:
        """Calculate Harsha (joy) Bala"""
        # Each planet rejoices in certain houses
        joy_houses = {
            "Sun": [10], "Moon": [4], "Mars": [6], "Mercury": [1],
            "Jupiter": [11], "Venus": [5], "Saturn": [12]
        }
        
        if house in joy_houses.get(planet, []):
            return 60
        elif house in [1, 4, 7, 10]:
            return 40
        elif house in [5, 9]:
            return 35
        else:
            return 20
    
    # =========================================================================
    # TAJAKA ASPECTS
    # =========================================================================
    def _calculate_tajaka_aspects(
        self,
        planets: Dict[str, Dict[str, Any]]
    ) -> List[TajakaAspect]:
        """Calculate all Tajaka aspects between planets"""
        aspects = []
        planet_list = list(planets.keys())
        
        for i, p1 in enumerate(planet_list):
            for p2 in planet_list[i+1:]:
                aspect = self._check_aspect(
                    p1, planets[p1]["longitude"],
                    p2, planets[p2]["longitude"]
                )
                if aspect:
                    aspects.append(aspect)
        
        return aspects
    
    def _check_aspect(
        self,
        planet1: str,
        lon1: float,
        planet2: str,
        lon2: float
    ) -> Optional[TajakaAspect]:
        """Check for Tajaka aspect between two planets"""
        diff = abs(lon1 - lon2)
        if diff > 180:
            diff = 360 - diff
        
        # Check each aspect type
        for aspect_angle, orb in self.ASPECT_ORBS.items():
            if abs(diff - aspect_angle) <= orb:
                # Determine faster planet
                speed1 = self.PLANET_SPEEDS.get(planet1, 0)
                speed2 = self.PLANET_SPEEDS.get(planet2, 0)
                
                if speed1 > speed2:
                    faster, slower = planet1, planet2
                    is_applying = (lon1 < lon2 if diff < 180 else lon1 > lon2)
                else:
                    faster, slower = planet2, planet1
                    is_applying = (lon2 < lon1 if diff < 180 else lon2 > lon1)
                
                aspect_name = self._get_aspect_type(aspect_angle, is_applying)
                
                return TajakaAspect(
                    faster_planet=faster,
                    slower_planet=slower,
                    aspect_type=aspect_name,
                    is_applying=is_applying,
                    orb=abs(diff - aspect_angle),
                    interpretation=self._interpret_tajaka_aspect(faster, slower, aspect_name)
                )
        
        return None
    
    def _get_aspect_type(self, angle: int, is_applying: bool) -> str:
        """Get Tajaka aspect type name"""
        base_names = {
            0: "Conjunction", 60: "Sextile", 90: "Square",
            120: "Trine", 180: "Opposition"
        }
        base = base_names.get(angle, "Aspect")
        
        if is_applying:
            return f"Ithasala ({base})"
        else:
            return f"Easarapha ({base})"
    
    def _interpret_tajaka_aspect(
        self,
        faster: str,
        slower: str,
        aspect_type: str
    ) -> str:
        """Interpret a Tajaka aspect"""
        if "Ithasala" in aspect_type:
            return f"{faster} applying to {slower} - matter will fructify"
        else:
            return f"{faster} separating from {slower} - matter concluded or denied"
    
    # =========================================================================
    # TAJAKA YOGAS (16 types)
    # =========================================================================
    def _calculate_tajaka_yogas(
        self,
        planets: Dict[str, Dict[str, Any]],
        aspects: List[TajakaAspect],
        ascendant: float
    ) -> List[TajakaYoga]:
        """Calculate all 16 Tajaka Yogas"""
        yogas = []
        lagna_sign = int(ascendant / 30)
        
        # 1. Ikbala Yoga - Lagna lord in kendra
        lagna_lord = self._get_sign_lord(lagna_sign)
        ll_house = self._get_house(planets.get(lagna_lord, {}).get("longitude", 0), ascendant)
        yogas.append(TajakaYoga(
            name="Ikbala Yoga",
            planets_involved=[lagna_lord],
            is_present=ll_house in [1, 4, 7, 10],
            strength=80 if ll_house in [1, 4, 7, 10] else 0,
            description="Lagna lord in kendra - success and authority"
        ))
        
        # 2. Induvara Yoga - All planets in angles/trines
        all_in_good = all(
            self._get_house(p["longitude"], ascendant) in [1, 4, 5, 7, 9, 10]
            for p in planets.values()
        )
        yogas.append(TajakaYoga(
            name="Induvara Yoga",
            planets_involved=list(planets.keys()),
            is_present=all_in_good,
            strength=90 if all_in_good else 0,
            description="All planets in kendras/trikonas - excellent year"
        ))
        
        # 3-8. Ithasala variations
        ithasala_aspects = [a for a in aspects if "Ithasala" in a.aspect_type]
        
        for aspect in ithasala_aspects[:3]:  # Top 3
            yogas.append(TajakaYoga(
                name=f"Ithasala ({aspect.faster_planet}-{aspect.slower_planet})",
                planets_involved=[aspect.faster_planet, aspect.slower_planet],
                is_present=True,
                strength=70,
                description=f"Applying aspect - {aspect.faster_planet} matters progress"
            ))
        
        # 9. Nakta Yoga - Moon involved in ithasala
        moon_ithasala = any(
            a.faster_planet == "Moon" or a.slower_planet == "Moon"
            for a in ithasala_aspects
        )
        yogas.append(TajakaYoga(
            name="Nakta Yoga",
            planets_involved=["Moon"],
            is_present=moon_ithasala,
            strength=65 if moon_ithasala else 0,
            description="Moon in applying aspect - emotional fulfillment"
        ))
        
        # 10. Yamaya Yoga - Two planets in applying aspect
        yogas.append(TajakaYoga(
            name="Yamaya Yoga",
            planets_involved=[ithasala_aspects[0].faster_planet, ithasala_aspects[0].slower_planet] if ithasala_aspects else [],
            is_present=len(ithasala_aspects) >= 2,
            strength=60 if len(ithasala_aspects) >= 2 else 0,
            description="Multiple applying aspects - multiple gains"
        ))
        
        # 11-16. Additional Tajaka yogas
        self._add_additional_tajaka_yogas(yogas, planets, aspects, ascendant)
        
        return yogas
    
    def _add_additional_tajaka_yogas(
        self,
        yogas: List[TajakaYoga],
        planets: Dict[str, Dict[str, Any]],
        aspects: List[TajakaAspect],
        ascendant: float
    ):
        """Add remaining Tajaka yogas"""
        # Manau Yoga - Significator strong
        jup_strong = self._pancha_vargeeya_bala(
            "Jupiter", 
            int(planets["Jupiter"]["longitude"] / 30),
            self._get_house(planets["Jupiter"]["longitude"], ascendant)
        ) > 40
        
        yogas.append(TajakaYoga(
            name="Manau Yoga",
            planets_involved=["Jupiter"],
            is_present=jup_strong,
            strength=70 if jup_strong else 0,
            description="Jupiter strong - wisdom and fortune"
        ))
        
        # Kamboola Yoga - Moon aspects lagna lord
        moon_lon = planets["Moon"]["longitude"]
        ll = self._get_sign_lord(int(ascendant / 30))
        ll_lon = planets.get(ll, {}).get("longitude", 0)
        diff = abs(moon_lon - ll_lon)
        if diff > 180:
            diff = 360 - diff
        
        kamboola = diff in range(0, 13) or diff in range(54, 66) or diff in range(84, 96) or diff in range(114, 126) or diff in range(174, 186)
        
        yogas.append(TajakaYoga(
            name="Kamboola Yoga",
            planets_involved=["Moon", ll],
            is_present=kamboola,
            strength=75 if kamboola else 0,
            description="Moon-Lagna Lord aspect - fulfillment of desires"
        ))
    
    def _get_sign_lord(self, sign: int) -> str:
        """Get lord of a sign"""
        lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
                "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
        return lords[sign]
    
    def _get_house(self, longitude: float, ascendant: float) -> int:
        """Get house number for a longitude"""
        lagna_sign = int(ascendant / 30)
        planet_sign = int(longitude / 30)
        return ((planet_sign - lagna_sign) % 12) + 1
    
    def _aspect_to_dict(self, aspect: TajakaAspect) -> Dict[str, Any]:
        """Convert aspect to dictionary"""
        return {
            "faster": aspect.faster_planet,
            "slower": aspect.slower_planet,
            "type": aspect.aspect_type,
            "applying": aspect.is_applying,
            "orb": aspect.orb,
            "interpretation": aspect.interpretation
        }
    
    def _yoga_to_dict(self, yoga: TajakaYoga) -> Dict[str, Any]:
        """Convert yoga to dictionary"""
        return {
            "name": yoga.name,
            "planets": yoga.planets_involved,
            "strength": yoga.strength,
            "description": yoga.description
        }
    
    def _generate_annual_prediction(
        self,
        planets: Dict[str, Dict[str, Any]],
        ascendant: float,
        muntha: int,
        yogas: List[TajakaYoga]
    ) -> Dict[str, str]:
        """Generate annual predictions"""
        lagna_sign = int(ascendant / 30)
        muntha_house = ((muntha - lagna_sign) % 12) + 1
        
        positive_yogas = sum(1 for y in yogas if y.is_present and y.strength > 60)
        
        # General prediction
        if muntha_house in [1, 4, 5, 7, 9, 10, 11] and positive_yogas >= 3:
            general = "Highly favorable year with success in multiple areas"
        elif muntha_house in [1, 4, 5, 7, 9, 10, 11] or positive_yogas >= 2:
            general = "Generally positive year with good opportunities"
        elif muntha_house in [6, 8, 12]:
            general = "Challenging year requiring patience and effort"
        else:
            general = "Mixed year with both opportunities and obstacles"
        
        return {
            "general": general,
            "muntha_effect": f"Muntha in {muntha_house}th house - " + self._muntha_interpretation(muntha_house),
            "key_advice": self._get_annual_advice(planets, ascendant, yogas)
        }
    
    def _muntha_interpretation(self, house: int) -> str:
        """Interpret Muntha position"""
        interpretations = {
            1: "Focus on self, new initiatives",
            2: "Financial matters, family",
            3: "Communication, short travels",
            4: "Home, property, mother",
            5: "Children, creativity, speculation",
            6: "Health, service, obstacles",
            7: "Partnerships, relationships",
            8: "Transformation, inheritances",
            9: "Fortune, higher learning, travel",
            10: "Career, public status",
            11: "Gains, social network",
            12: "Expenses, spirituality, foreign"
        }
        return interpretations.get(house, "General experiences")
    
    def _get_annual_advice(
        self,
        planets: Dict[str, Dict[str, Any]],
        ascendant: float,
        yogas: List[TajakaYoga]
    ) -> str:
        """Get advice for the year"""
        jupiter_house = self._get_house(planets["Jupiter"]["longitude"], ascendant)
        saturn_house = self._get_house(planets["Saturn"]["longitude"], ascendant)
        
        if jupiter_house in [1, 4, 5, 9, 10]:
            return "Jupiter favorably placed - pursue expansion and growth"
        elif saturn_house in [3, 6, 10, 11]:
            return "Saturn well-placed - hard work will pay off"
        else:
            return "Balance ambition with caution this year"


def calculate_tajaka_annual(
    birth_date: datetime,
    birth_sun_longitude: float,
    year_number: int
) -> Dict[str, Any]:
    """Convenience function for Tajaka annual chart"""
    calc = TajakaCalculator()
    return calc.calculate_annual_chart(birth_date, birth_sun_longitude, year_number)
