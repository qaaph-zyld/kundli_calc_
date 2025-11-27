"""
Advanced Divisional Charts - Phase 6
PGF Protocol: DIV_003
Gate: GATE_6
Version: 1.0.0

Implements:
1. D-81 (Ekaasheetyamsa)
2. D-108 (Ashtottaramsa)
3. D-144 (Dwadas-Dwadasamsa)
4. Generic D-mxn (Sub-divisional)
5. Custom D-N (any N from 1-300)
6. Nadyamsas
7. Ayudha/Sarapa/Pakshi Drekkana
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
import math


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


@dataclass
class DivisionalPosition:
    """Position in a divisional chart"""
    planet: str
    longitude: float
    sign: int
    sign_name: str
    degree: float
    navamsa_position: Optional[int] = None


# =============================================================================
# D-81 EKAASHEETYAMSA
# =============================================================================
class D81Calculator:
    """
    D-81 (Ekaasheetyamsa) - 81st Harmonic
    
    Each sign divided into 81 parts.
    Division = 30/81 = 0.3703° per division
    
    Two methods:
    1. Cyclical: Divisions map to 81 signs starting from same sign
    2. Parasara: Based on element (fire/earth/air/water)
    """
    
    def calculate_cyclical(self, longitude: float) -> DivisionalPosition:
        """Calculate D-81 using cyclical method"""
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        # 81 divisions per sign
        division = int(degree_in_sign / (30/81))
        
        # Map to sign (cyclical from same sign)
        d81_sign = (sign + division) % 12
        
        # Calculate position within D-81 sign
        d81_degree = ((division % 81) / 81) * 30
        
        return DivisionalPosition(
            planet="",
            longitude=(d81_sign * 30) + d81_degree,
            sign=d81_sign,
            sign_name=SIGNS[d81_sign],
            degree=d81_degree
        )
    
    def calculate_parasara(self, longitude: float) -> DivisionalPosition:
        """Calculate D-81 using Parasara method (element-based)"""
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        division = int(degree_in_sign / (30/81))
        
        # Element determines starting sign
        element = sign % 4
        start_signs = [0, 9, 5, 1]  # Fire, Earth, Air, Water
        
        d81_sign = (start_signs[element] + division) % 12
        d81_degree = ((division % 81) / 81) * 30
        
        return DivisionalPosition(
            planet="",
            longitude=(d81_sign * 30) + d81_degree,
            sign=d81_sign,
            sign_name=SIGNS[d81_sign],
            degree=d81_degree
        )
    
    def calculate_all_planets(
        self, 
        planets: Dict[str, float],
        method: str = "cyclical"
    ) -> Dict[str, DivisionalPosition]:
        """Calculate D-81 for all planets"""
        calc_method = self.calculate_cyclical if method == "cyclical" else self.calculate_parasara
        
        results = {}
        for planet, longitude in planets.items():
            pos = calc_method(longitude)
            pos.planet = planet
            results[planet] = pos
        
        return results


# =============================================================================
# D-108 ASHTOTTARAMSA
# =============================================================================
class D108Calculator:
    """
    D-108 (Ashtottaramsa) - 108th Harmonic
    
    Each sign divided into 108 parts (same as navamsas of navamsas).
    Division = 30/108 = 0.2778° per division
    
    Two methods:
    1. Cyclical: From same sign
    2. Navamsa of Navamsa: D-9 x D-9 = D-81, extended to 108
    """
    
    def calculate_cyclical(self, longitude: float) -> DivisionalPosition:
        """Calculate D-108 using cyclical method"""
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        division = int(degree_in_sign / (30/108))
        
        d108_sign = (sign + division) % 12
        d108_degree = ((division % 108) / 108) * 30
        
        return DivisionalPosition(
            planet="",
            longitude=(d108_sign * 30) + d108_degree,
            sign=d108_sign,
            sign_name=SIGNS[d108_sign],
            degree=d108_degree
        )
    
    def calculate_navamsa_navamsa(self, longitude: float) -> DivisionalPosition:
        """Calculate D-108 as Navamsa of Navamsa"""
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        # First navamsa
        navamsa1 = int(degree_in_sign / (30/9))
        element1 = sign % 4
        start1 = [0, 9, 5, 1][element1]
        d9_sign = (start1 + navamsa1) % 12
        
        # Second navamsa (of the navamsa)
        d9_degree = ((navamsa1 * (30/9)) + (degree_in_sign % (30/9))) % 30
        navamsa2 = int(d9_degree / (30/9))
        element2 = d9_sign % 4
        start2 = [0, 9, 5, 1][element2]
        d108_sign = (start2 + navamsa2) % 12
        
        d108_degree = (navamsa2 / 9) * 30
        
        return DivisionalPosition(
            planet="",
            longitude=(d108_sign * 30) + d108_degree,
            sign=d108_sign,
            sign_name=SIGNS[d108_sign],
            degree=d108_degree,
            navamsa_position=navamsa2
        )
    
    def calculate_all_planets(
        self, 
        planets: Dict[str, float],
        method: str = "cyclical"
    ) -> Dict[str, DivisionalPosition]:
        """Calculate D-108 for all planets"""
        calc_method = self.calculate_cyclical if method == "cyclical" else self.calculate_navamsa_navamsa
        
        results = {}
        for planet, longitude in planets.items():
            pos = calc_method(longitude)
            pos.planet = planet
            results[planet] = pos
        
        return results


# =============================================================================
# D-144 DWADAS-DWADASAMSA
# =============================================================================
class D144Calculator:
    """
    D-144 (Dwadas-Dwadasamsa) - 144th Harmonic
    
    D-12 x D-12 = D-144
    Each sign divided into 144 parts.
    Division = 30/144 = 0.2083° per division
    """
    
    def calculate(self, longitude: float) -> DivisionalPosition:
        """Calculate D-144 position"""
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        # First D-12
        d12_1 = int(degree_in_sign / (30/12))
        d12_sign1 = (sign + d12_1) % 12
        
        # Second D-12 (of the D-12)
        d12_degree = (d12_1 * (30/12)) + (degree_in_sign % (30/12))
        d12_2 = int((d12_degree % (30/12)) / (30/144))
        d144_sign = (d12_sign1 + d12_2) % 12
        
        d144_degree = (d12_2 / 12) * 30
        
        return DivisionalPosition(
            planet="",
            longitude=(d144_sign * 30) + d144_degree,
            sign=d144_sign,
            sign_name=SIGNS[d144_sign],
            degree=d144_degree
        )
    
    def calculate_all_planets(self, planets: Dict[str, float]) -> Dict[str, DivisionalPosition]:
        """Calculate D-144 for all planets"""
        results = {}
        for planet, longitude in planets.items():
            pos = self.calculate(longitude)
            pos.planet = planet
            results[planet] = pos
        
        return results


# =============================================================================
# GENERIC D-MxN (SUB-DIVISIONAL)
# =============================================================================
class SubDivisionalCalculator:
    """
    Generic D-mxn Calculator
    
    Takes any divisional chart D-m and further divides it into D-n.
    For example: D-9 x D-10 = D-90
    """
    
    def calculate_sub_divisional(
        self,
        longitude: float,
        m: int,
        n: int
    ) -> DivisionalPosition:
        """
        Calculate sub-divisional chart D-mxn
        
        Args:
            longitude: Planet's rasi longitude
            m: First division (e.g., 9 for navamsa)
            n: Second division (e.g., 10 for dasamsa)
        """
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        # First division D-m
        div_m = int(degree_in_sign / (30/m))
        element = sign % 4
        start_signs = [0, 9, 5, 1]
        dm_sign = (start_signs[element] + div_m) % 12
        
        # Second division D-n (applied to D-m result)
        dm_degree = (div_m / m) * 30
        div_n = int(dm_degree / (30/n))
        element_n = dm_sign % 4
        dmn_sign = (start_signs[element_n] + div_n) % 12
        
        dmn_degree = (div_n / n) * 30
        
        return DivisionalPosition(
            planet="",
            longitude=(dmn_sign * 30) + dmn_degree,
            sign=dmn_sign,
            sign_name=SIGNS[dmn_sign],
            degree=dmn_degree
        )
    
    def calculate_all_planets(
        self,
        planets: Dict[str, float],
        m: int,
        n: int
    ) -> Dict[str, DivisionalPosition]:
        """Calculate D-mxn for all planets"""
        results = {}
        for planet, longitude in planets.items():
            pos = self.calculate_sub_divisional(longitude, m, n)
            pos.planet = planet
            results[planet] = pos
        
        return results


# =============================================================================
# CUSTOM D-N (ANY N FROM 1-300)
# =============================================================================
class CustomDivisionalCalculator:
    """
    Custom D-N Calculator
    
    Calculate any divisional chart from D-1 to D-300.
    Supports multiple mapping methods.
    """
    
    def calculate(
        self,
        longitude: float,
        n: int,
        method: str = "cyclical"
    ) -> DivisionalPosition:
        """
        Calculate custom D-N
        
        Args:
            longitude: Planet longitude
            n: Division number (1-300)
            method: "cyclical", "element", "quality", "element_quality"
        """
        if n < 1 or n > 300:
            raise ValueError("N must be between 1 and 300")
        
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        division = int(degree_in_sign / (30/n))
        
        if method == "cyclical":
            dn_sign = (sign + division) % 12
        
        elif method == "element":
            # Element-based (fire/earth/air/water)
            element = sign % 4
            start_signs = [0, 9, 5, 1]
            dn_sign = (start_signs[element] + division) % 12
        
        elif method == "quality":
            # Quality-based (movable/fixed/dual)
            quality = sign % 3
            if quality == 0:  # Movable
                dn_sign = (sign + division) % 12
            elif quality == 1:  # Fixed
                dn_sign = (sign - division) % 12
            else:  # Dual
                dn_sign = (sign + division) % 12 if division % 2 == 0 else (sign - division) % 12
        
        elif method == "element_quality":
            # Combined element and quality
            element = sign % 4
            quality = sign % 3
            start_map = {
                (0, 0): 0, (0, 1): 3, (0, 2): 6,
                (1, 0): 9, (1, 1): 0, (1, 2): 3,
                (2, 0): 6, (2, 1): 9, (2, 2): 0,
                (3, 0): 3, (3, 1): 6, (3, 2): 9
            }
            start = start_map.get((element, quality), 0)
            dn_sign = (start + division) % 12
        
        else:
            dn_sign = (sign + division) % 12
        
        dn_degree = ((division % n) / n) * 30
        
        return DivisionalPosition(
            planet="",
            longitude=(dn_sign * 30) + dn_degree,
            sign=dn_sign,
            sign_name=SIGNS[dn_sign],
            degree=dn_degree
        )
    
    def calculate_all_planets(
        self,
        planets: Dict[str, float],
        n: int,
        method: str = "cyclical"
    ) -> Dict[str, DivisionalPosition]:
        """Calculate custom D-N for all planets"""
        results = {}
        for planet, longitude in planets.items():
            pos = self.calculate(longitude, n, method)
            pos.planet = planet
            results[planet] = pos
        
        return results


# =============================================================================
# NADYAMSAS
# =============================================================================
class NadyamsaCalculator:
    """
    Nadyamsa Calculator
    
    150 nadyamsas per sign (each 12 minutes of arc).
    Used in Chandra Kala Nadi and other predictive systems.
    """
    
    # Nadi names (C.G. Rajan system - first 12)
    NADI_NAMES_RAJAN = [
        "Vasudha", "Vaishnavi", "Brahmi", "Kalapatni", "Rohini", "Saumya",
        "Mandakini", "Sveta", "Arundhati", "Kumudvati", "Bhadrika", "Mandari"
    ]
    
    # Extended to 150 by cycling and adding suffixes
    
    def calculate(self, longitude: float) -> Dict[str, Any]:
        """Calculate Nadyamsa position"""
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        # 150 nadyamsas per sign (each 12 arc-minutes = 0.2°)
        nadyamsa = int(degree_in_sign / 0.2)
        
        # Determine nadi name (cycling through 12 names)
        nadi_idx = nadyamsa % 12
        nadi_cycle = nadyamsa // 12
        nadi_name = self.NADI_NAMES_RAJAN[nadi_idx]
        
        # Full name includes cycle number
        if nadi_cycle > 0:
            nadi_name = f"{nadi_name}-{nadi_cycle + 1}"
        
        return {
            "sign": SIGNS[sign],
            "nadyamsa_number": nadyamsa + 1,
            "nadi_name": nadi_name,
            "degree_range": f"{nadyamsa * 0.2:.2f}° - {(nadyamsa + 1) * 0.2:.2f}°",
            "ruling_deity": self._get_ruling_deity(nadyamsa)
        }
    
    def _get_ruling_deity(self, nadyamsa: int) -> str:
        """Get ruling deity based on nadyamsa"""
        deities = ["Brahma", "Vishnu", "Shiva", "Surya", "Chandra", 
                   "Mangala", "Budha", "Guru", "Shukra", "Shani", "Rahu", "Ketu"]
        return deities[nadyamsa % 12]
    
    def calculate_all_planets(self, planets: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Calculate Nadyamsa for all planets"""
        return {planet: self.calculate(lon) for planet, lon in planets.items()}


# =============================================================================
# SPECIAL DREKKANAS
# =============================================================================
class SpecialDrekkana:
    """
    Special Drekkana Classifications
    
    Ayudha (Armed), Sarapa (Serpent), Pakshi (Bird), etc.
    Classifications of the 36 drekkanas for delineation.
    """
    
    # Drekkana classifications (1-36)
    CLASSIFICATIONS = {
        # First decanate of each sign (1, 4, 7, 10... = 0° to 10°)
        "ayudha": [1, 3, 5, 7, 10, 12, 14, 16, 19, 21, 23, 25],  # Armed/Weapon
        "sarapa": [2, 8, 11, 17, 20, 26, 29, 35],  # Serpent
        "pakshi": [4, 6, 13, 15, 22, 24, 31, 33],  # Bird
        "chatushpada": [9, 18, 27, 36],  # Four-footed
        "keeta": [28, 30, 32, 34]  # Insect
    }
    
    # Drekkana lords and meanings
    DREKKANA_DATA = [
        {"sign": "Aries", "part": 1, "type": "ayudha", "nature": "aggressive"},
        {"sign": "Aries", "part": 2, "type": "pakshi", "nature": "swift"},
        {"sign": "Aries", "part": 3, "type": "chatushpada", "nature": "strong"},
        # ... (would be 36 total entries)
    ]
    
    def classify(self, longitude: float) -> Dict[str, Any]:
        """Classify a longitude into special drekkana types"""
        sign = int(longitude / 30)
        degree = longitude % 30
        drekkana_part = int(degree / 10) + 1  # 1, 2, or 3
        
        # Absolute drekkana number (1-36)
        drekkana_num = sign * 3 + drekkana_part
        
        # Find classification
        classification = "mixed"
        for type_name, nums in self.CLASSIFICATIONS.items():
            if drekkana_num in nums:
                classification = type_name
                break
        
        # Descriptions
        descriptions = {
            "ayudha": "Armed drekkana - indicates weapons, fighting, aggression",
            "sarapa": "Serpent drekkana - indicates cunning, poison, hidden dangers",
            "pakshi": "Bird drekkana - indicates swiftness, travel, freedom",
            "chatushpada": "Four-footed drekkana - indicates stability, strength, animals",
            "keeta": "Insect drekkana - indicates small matters, disease, persistence"
        }
        
        return {
            "sign": SIGNS[sign],
            "drekkana_part": drekkana_part,
            "absolute_number": drekkana_num,
            "classification": classification,
            "description": descriptions.get(classification, "Mixed nature"),
            "degree_range": f"{(drekkana_part - 1) * 10}° - {drekkana_part * 10}°"
        }
    
    def classify_all_planets(self, planets: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Classify all planets"""
        return {planet: self.classify(lon) for planet, lon in planets.items()}


# =============================================================================
# MASTER CALCULATOR
# =============================================================================
class AdvancedDivisionalCalculator:
    """Master calculator for all advanced divisional charts"""
    
    def __init__(self):
        self.d81 = D81Calculator()
        self.d108 = D108Calculator()
        self.d144 = D144Calculator()
        self.sub_divisional = SubDivisionalCalculator()
        self.custom = CustomDivisionalCalculator()
        self.nadyamsa = NadyamsaCalculator()
        self.special_drekkana = SpecialDrekkana()
    
    def calculate_all(
        self,
        planets: Dict[str, float]
    ) -> Dict[str, Any]:
        """Calculate all advanced divisional charts"""
        return {
            "d81_cyclical": self.d81.calculate_all_planets(planets, "cyclical"),
            "d81_parasara": self.d81.calculate_all_planets(planets, "parasara"),
            "d108_cyclical": self.d108.calculate_all_planets(planets, "cyclical"),
            "d108_navamsa": self.d108.calculate_all_planets(planets, "navamsa_navamsa"),
            "d144": self.d144.calculate_all_planets(planets),
            "nadyamsa": self.nadyamsa.calculate_all_planets(planets),
            "special_drekkana": self.special_drekkana.classify_all_planets(planets)
        }
    
    def calculate_custom(
        self,
        planets: Dict[str, float],
        n: int,
        method: str = "cyclical"
    ) -> Dict[str, DivisionalPosition]:
        """Calculate any custom D-N chart"""
        return self.custom.calculate_all_planets(planets, n, method)
    
    def calculate_sub_divisional(
        self,
        planets: Dict[str, float],
        m: int,
        n: int
    ) -> Dict[str, DivisionalPosition]:
        """Calculate D-mxn sub-divisional chart"""
        return self.sub_divisional.calculate_all_planets(planets, m, n)
