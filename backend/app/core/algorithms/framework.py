"""
Astrological Algorithms Framework
PGF Protocol: ALG_001
Gate: GATE_17
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union, Set
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field
import numpy as np
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)
from ..astronomical.framework import (
    CelestialBody,
    ZodiacSign,
    House,
    Aspect,
    GeoLocation,
    PlanetaryPosition,
    AspectPosition
)
from ..mathematics.framework import PlanetaryMath

class YogaType(str, Enum):
    """Types of yogas"""
    RAJA = "raja"           # Royal combinations
    DHANA = "dhana"         # Wealth combinations
    PARIVARTANA = "parivartana"  # Exchange combinations
    MAHAPURUSHA = "mahapurusha"  # Great person combinations
    NABHASA = "nabhasa"     # Special pattern combinations
    CHANDRA = "chandra"     # Moon-based combinations
    SUNABHAGA = "sunabhaga"  # Auspicious degree combinations
    DOSHAYOGA = "doshayoga"  # Difficult combinations
    ARGALA = "argala"       # Intervention combinations
    VIPAREETA = "vipareeta"  # Reversal combinations

class DashaSystem(str, Enum):
    """Dasha systems"""
    VIMSHOTTARI = "vimshottari"
    ASHTOTTARI = "ashtottari"
    YOGINI = "yogini"
    KALACHAKRA = "kalachakra"
    NARAYANA = "narayana"

class StrengthFactor(str, Enum):
    """Planetary strength factors"""
    SHADBALA = "shadbala"
    ASHTAKAVARGA = "ashtakavarga"
    VIMSOPAKA = "vimsopaka"
    HARSHA = "harsha"
    PANCHAVARGIYA = "panchavargiya"

@dataclass
class YogaResult:
    """Yoga analysis result"""
    
    type: YogaType
    name: str
    planets: List[CelestialBody]
    houses: List[House]
    strength: float
    description: str
    effects: List[str]

@dataclass
class DashaResult:
    """Dasha period result"""
    
    system: DashaSystem
    major_planet: CelestialBody
    sub_planet: Optional[CelestialBody]
    start_date: datetime
    end_date: datetime
    strength: float
    effects: List[str]

@dataclass
class StrengthResult:
    """Planetary strength result"""
    
    body: CelestialBody
    factor: StrengthFactor
    value: float
    percentage: float
    interpretation: str

class AstrologicalAlgorithms:
    """Astrological algorithms"""
    
    def __init__(self):
        self.math = PlanetaryMath()
    
    def analyze_raja_yoga(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition]
    ) -> List[YogaResult]:
        """Analyze Raja Yoga combinations"""
        results = []
        
        # Check for mutual aspects between lords of trine and quadrant houses
        trine_houses = [House.FIRST, House.FIFTH, House.NINTH]
        quadrant_houses = [House.FIRST, House.FOURTH, House.SEVENTH, House.TENTH]
        
        for trine in trine_houses:
            for quadrant in quadrant_houses:
                trine_lord = self._get_house_lord(positions, trine)
                quadrant_lord = self._get_house_lord(positions, quadrant)
                
                if trine_lord and quadrant_lord:
                    aspect = self._check_mutual_aspect(
                        positions[trine_lord],
                        positions[quadrant_lord]
                    )
                    
                    if aspect:
                        results.append(YogaResult(
                            type=YogaType.RAJA,
                            name=f"Raja Yoga from {trine.name}-{quadrant.name}",
                            planets=[trine_lord, quadrant_lord],
                            houses=[trine, quadrant],
                            strength=self._calculate_yoga_strength(
                                [positions[trine_lord], positions[quadrant_lord]]
                            ),
                            description="Powerful Raja Yoga formed by mutual "
                                      "aspect between trine and quadrant lords",
                            effects=[
                                "Rise to power and authority",
                                "Leadership abilities",
                                "Success in endeavors",
                                "Royal status or high position"
                            ]
                        ))
        
        return results
    
    def analyze_dhana_yoga(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition]
    ) -> List[YogaResult]:
        """Analyze Dhana Yoga combinations"""
        results = []
        
        # Check for 2nd and 11th house combinations
        wealth_houses = [House.SECOND, House.ELEVENTH]
        wealth_planets = [
            CelestialBody.JUPITER,
            CelestialBody.VENUS,
            CelestialBody.MERCURY
        ]
        
        for house in wealth_houses:
            house_lord = self._get_house_lord(positions, house)
            if house_lord:
                for planet in wealth_planets:
                    if planet in positions:
                        aspect = self._check_mutual_aspect(
                            positions[house_lord],
                            positions[planet]
                        )
                        
                        if aspect:
                            results.append(YogaResult(
                                type=YogaType.DHANA,
                                name=f"Dhana Yoga in {house.name}",
                                planets=[house_lord, planet],
                                houses=[house],
                                strength=self._calculate_yoga_strength(
                                    [positions[house_lord], positions[planet]]
                                ),
                                description="Wealth-generating combination "
                                          "between house lord and benefic",
                                effects=[
                                    "Financial prosperity",
                                    "Material gains",
                                    "Business success",
                                    "Accumulation of wealth"
                                ]
                            ))
        
        return results
    
    def analyze_mahapurusha_yoga(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition]
    ) -> List[YogaResult]:
        """Analyze Mahapurusha Yoga combinations"""
        results = []
        
        # Check for planets in own or exaltation sign in angles
        angles = [House.FIRST, House.FOURTH, House.SEVENTH, House.TENTH]
        mahapurusha_planets = [
            CelestialBody.MARS,
            CelestialBody.MERCURY,
            CelestialBody.JUPITER,
            CelestialBody.VENUS,
            CelestialBody.SATURN
        ]
        
        for planet in mahapurusha_planets:
            if planet in positions:
                pos = positions[planet]
                if pos.house in angles:
                    if self._is_in_own_sign(planet, pos.sign) or \
                       self._is_in_exaltation(planet, pos.sign):
                        results.append(YogaResult(
                            type=YogaType.MAHAPURUSHA,
                            name=f"{planet.name} Mahapurusha Yoga",
                            planets=[planet],
                            houses=[pos.house],
                            strength=self._calculate_yoga_strength([pos]),
                            description=f"Great person yoga formed by {planet.name} "
                                      f"in angle",
                            effects=self._get_mahapurusha_effects(planet)
                        ))
        
        return results
    
    def calculate_dasha_periods(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition],
        birth_time: datetime,
        system: DashaSystem = DashaSystem.VIMSHOTTARI
    ) -> List[DashaResult]:
        """Calculate dasha periods"""
        results = []
        
        if system == DashaSystem.VIMSHOTTARI:
            # Vimshottari dasha calculation
            moon_pos = positions[CelestialBody.MOON]
            nakshatra_deg = moon_pos.longitude * 3 / 40
            nakshatra = int(nakshatra_deg)
            balance = 1 - (nakshatra_deg - nakshatra)
            
            # Dasha sequence and duration (in years)
            sequence = [
                (CelestialBody.SUN, 6),
                (CelestialBody.MOON, 10),
                (CelestialBody.MARS, 7),
                (CelestialBody.RAHU, 18),
                (CelestialBody.JUPITER, 16),
                (CelestialBody.SATURN, 19),
                (CelestialBody.MERCURY, 17),
                (CelestialBody.KETU, 7),
                (CelestialBody.VENUS, 20)
            ]
            
            # Calculate periods
            current_date = birth_time
            for planet, years in sequence:
                duration = years * 365.25 * 24 * 3600  # Convert to seconds
                end_date = current_date.fromtimestamp(
                    current_date.timestamp() + duration
                )
                
                results.append(DashaResult(
                    system=system,
                    major_planet=planet,
                    sub_planet=None,
                    start_date=current_date,
                    end_date=end_date,
                    strength=self._calculate_dasha_strength(
                        positions[planet],
                        positions
                    ),
                    effects=self._get_dasha_effects(planet)
                ))
                
                current_date = end_date
        
        return results
    
    def calculate_planetary_strength(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition],
        factor: StrengthFactor = StrengthFactor.SHADBALA
    ) -> Dict[CelestialBody, StrengthResult]:
        """Calculate planetary strength"""
        results = {}
        
        if factor == StrengthFactor.SHADBALA:
            # Calculate Shadbala (sixfold strength)
            for body, pos in positions.items():
                if body in [CelestialBody.RAHU, CelestialBody.KETU]:
                    continue
                
                # Calculate various strength factors
                sthana_bala = self._calculate_positional_strength(pos)
                dig_bala = self._calculate_directional_strength(pos)
                kala_bala = self._calculate_temporal_strength(pos)
                cheshta_bala = self._calculate_motional_strength(pos)
                naisargika_bala = self._calculate_natural_strength(body)
                drik_bala = self._calculate_aspectual_strength(pos, positions)
                
                # Total strength
                total = (
                    sthana_bala +
                    dig_bala +
                    kala_bala +
                    cheshta_bala +
                    naisargika_bala +
                    drik_bala
                )
                
                # Maximum possible strength
                max_strength = 6.0  # Maximum for Shadbala
                percentage = (total / max_strength) * 100
                
                results[body] = StrengthResult(
                    body=body,
                    factor=factor,
                    value=total,
                    percentage=percentage,
                    interpretation=self._interpret_strength(percentage)
                )
        
        return results
    
    def _get_house_lord(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition],
        house: House
    ) -> Optional[CelestialBody]:
        """Get lord of house"""
        from ..astronomical.config import ZODIAC_PROPERTIES
        
        # Find sign in house
        for body, pos in positions.items():
            if pos.house == house:
                sign = pos.sign
                return ZODIAC_PROPERTIES[sign]["ruler"]
        
        return None
    
    def _check_mutual_aspect(
        self,
        pos1: PlanetaryPosition,
        pos2: PlanetaryPosition
    ) -> Optional[Aspect]:
        """Check for mutual aspect between positions"""
        aspect = self.math._calculate_aspect(pos1, pos2)
        if aspect and aspect.orb <= 3:  # Strict orb for yoga
            return aspect.aspect
        return None
    
    def _calculate_yoga_strength(
        self,
        positions: List[PlanetaryPosition]
    ) -> float:
        """Calculate yoga strength"""
        total_strength = 0.0
        max_strength = len(positions) * 20  # Maximum 20 points per planet
        
        for pos in positions:
            # Dignity score
            dignity = self.math.calculate_dignity_score(
                pos.body,
                pos.sign,
                pos.house
            )
            
            # Aspect strength
            aspect_strength = 5 if not pos.is_retrograde else 3
            
            # House strength
            house_strength = {
                House.FIRST: 5,
                House.FOURTH: 4,
                House.SEVENTH: 4,
                House.TENTH: 5,
                House.FIFTH: 3,
                House.NINTH: 3
            }.get(pos.house, 1)
            
            total_strength += dignity + aspect_strength + house_strength
        
        return (total_strength / max_strength) * 100
    
    def _is_in_own_sign(
        self,
        body: CelestialBody,
        sign: ZodiacSign
    ) -> bool:
        """Check if planet is in own sign"""
        from ..astronomical.config import ZODIAC_PROPERTIES
        return ZODIAC_PROPERTIES[sign]["ruler"] == body
    
    def _is_in_exaltation(
        self,
        body: CelestialBody,
        sign: ZodiacSign
    ) -> bool:
        """Check if planet is in exaltation"""
        exaltation_map = {
            CelestialBody.SUN: ZodiacSign.ARIES,
            CelestialBody.MOON: ZodiacSign.TAURUS,
            CelestialBody.MARS: ZodiacSign.CAPRICORN,
            CelestialBody.MERCURY: ZodiacSign.VIRGO,
            CelestialBody.JUPITER: ZodiacSign.CANCER,
            CelestialBody.VENUS: ZodiacSign.PISCES,
            CelestialBody.SATURN: ZodiacSign.LIBRA
        }
        return body in exaltation_map and exaltation_map[body] == sign
    
    def _get_mahapurusha_effects(
        self,
        body: CelestialBody
    ) -> List[str]:
        """Get effects of Mahapurusha yoga"""
        effects_map = {
            CelestialBody.MARS: [
                "Leadership abilities",
                "Physical strength",
                "Military success",
                "Technical expertise"
            ],
            CelestialBody.MERCURY: [
                "Intelligence",
                "Business acumen",
                "Communication skills",
                "Scientific knowledge"
            ],
            CelestialBody.JUPITER: [
                "Wisdom",
                "Spiritual advancement",
                "Teaching abilities",
                "Wealth and prosperity"
            ],
            CelestialBody.VENUS: [
                "Artistic talents",
                "Luxury and comfort",
                "Diplomatic skills",
                "Success in entertainment"
            ],
            CelestialBody.SATURN: [
                "Disciplined nature",
                "Professional success",
                "Administrative skills",
                "Long-term achievements"
            ]
        }
        return effects_map.get(body, [])
    
    def _calculate_dasha_strength(
        self,
        planet_pos: PlanetaryPosition,
        all_positions: Dict[CelestialBody, PlanetaryPosition]
    ) -> float:
        """Calculate dasha period strength"""
        # Base strength from dignity
        strength = self.math.calculate_dignity_score(
            planet_pos.body,
            planet_pos.sign,
            planet_pos.house
        )
        
        # Aspect modifications
        for body, pos in all_positions.items():
            if body != planet_pos.body:
                aspect = self._check_mutual_aspect(planet_pos, pos)
                if aspect:
                    if body in [CelestialBody.JUPITER, CelestialBody.VENUS]:
                        strength += 2  # Benefic aspect
                    elif body in [CelestialBody.SATURN, CelestialBody.MARS]:
                        strength -= 1  # Malefic aspect
        
        # Normalize to 0-100 scale
        return min(max(strength * 10, 0), 100)
    
    def _get_dasha_effects(
        self,
        body: CelestialBody
    ) -> List[str]:
        """Get dasha period effects"""
        effects_map = {
            CelestialBody.SUN: [
                "Authority and power",
                "Government relations",
                "Father-related matters",
                "Health and vitality"
            ],
            CelestialBody.MOON: [
                "Emotional well-being",
                "Public life",
                "Mother-related matters",
                "Travel and changes"
            ],
            CelestialBody.MARS: [
                "Energy and initiative",
                "Property matters",
                "Technical projects",
                "Competition"
            ],
            CelestialBody.RAHU: [
                "Foreign influences",
                "Unconventional paths",
                "Sudden changes",
                "Material gains"
            ],
            CelestialBody.JUPITER: [
                "Knowledge and wisdom",
                "Financial growth",
                "Children matters",
                "Spiritual progress"
            ],
            CelestialBody.SATURN: [
                "Career development",
                "Responsibility",
                "Delays and obstacles",
                "Long-term gains"
            ],
            CelestialBody.MERCURY: [
                "Education and skills",
                "Business ventures",
                "Communication",
                "Short travels"
            ],
            CelestialBody.KETU: [
                "Spiritual insights",
                "Liberation",
                "Technical skills",
                "Detachment"
            ],
            CelestialBody.VENUS: [
                "Relationships",
                "Luxury and comfort",
                "Arts and entertainment",
                "Vehicle or property"
            ]
        }
        return effects_map.get(body, [])
