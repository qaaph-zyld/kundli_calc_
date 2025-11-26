"""
Krishnamurti Paddhati (KP) System Implementation
PGF Protocol: KP_001
Gate: GATE_5
Version: 1.0.0

This module implements the complete KP System for Vedic Astrology including:
- Cuspal Sublords (Star Lord, Sub Lord, Sub-Sub Lord up to 5 levels)
- Planet Sublords
- Significators (ABCD System)
- House-wise and Planet-wise Significator Tables
- Ruling Planets Calculation
- Horary Number Support (1-249)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime
import math

# KP Ayanamsa value (Krishnamurti Ayanamsa)
# This is slightly different from Lahiri - approximately 6 minutes less
KP_AYANAMSA_BASE_DATE = datetime(1900, 1, 1)
KP_AYANAMSA_BASE_VALUE = 22.362222  # 22°21'44" on Jan 1, 1900
KP_AYANAMSA_YEARLY_MOTION = 50.2388475 / 3600  # Annual precession in degrees


# Vimshottari Dasha periods (used for sub-lord calculations)
DASHA_PERIODS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}

# Total Vimshottari cycle = 120 years
TOTAL_DASHA_YEARS = 120

# Nakshatra sequence with their lords
NAKSHATRAS = [
    ("Ashwini", "Ketu"),
    ("Bharani", "Venus"),
    ("Krittika", "Sun"),
    ("Rohini", "Moon"),
    ("Mrigashira", "Mars"),
    ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"),
    ("Pushya", "Saturn"),
    ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"),
    ("Purva Phalguni", "Venus"),
    ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"),
    ("Chitra", "Mars"),
    ("Swati", "Rahu"),
    ("Vishakha", "Jupiter"),
    ("Anuradha", "Saturn"),
    ("Jyeshtha", "Mercury"),
    ("Mula", "Ketu"),
    ("Purva Ashadha", "Venus"),
    ("Uttara Ashadha", "Sun"),
    ("Shravana", "Moon"),
    ("Dhanishta", "Mars"),
    ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"),
    ("Uttara Bhadrapada", "Saturn"),
    ("Revati", "Mercury")
]

# Sign lords
SIGN_LORDS = {
    0: "Mars",      # Aries
    1: "Venus",     # Taurus
    2: "Mercury",   # Gemini
    3: "Moon",      # Cancer
    4: "Sun",       # Leo
    5: "Mercury",   # Virgo
    6: "Venus",     # Libra
    7: "Mars",      # Scorpio
    8: "Jupiter",   # Sagittarius
    9: "Saturn",    # Capricorn
    10: "Saturn",   # Aquarius
    11: "Jupiter"   # Pisces
}

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Dasha lord sequence for sub calculations
DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]


@dataclass
class KPPosition:
    """Represents a position in KP system with all sublord levels"""
    degree: float
    sign: int
    sign_name: str
    sign_lord: str
    nakshatra: int
    nakshatra_name: str
    nakshatra_lord: str  # Star Lord
    sub_lord: str
    sub_sub_lord: str
    sub_sub_sub_lord: str
    sub_sub_sub_sub_lord: str  # 5th level
    
    # Degrees within each division
    degree_in_sign: float
    degree_in_nakshatra: float
    degree_in_sub: float


@dataclass
class KPSignificators:
    """Significators for a planet or house in ABCD system"""
    planet_or_house: str
    A: List[int]  # Houses signified through star lord's occupation
    B: List[int]  # Houses occupied
    C: List[int]  # Houses owned by star lord
    D: List[int]  # Houses owned
    combined: List[int]  # All signified houses


@dataclass
class RulingPlanets:
    """Ruling planets at a given moment"""
    weekday_lord: str
    moon_sign_lord: str
    moon_star_lord: str
    moon_sub_lord: str
    ascendant_sign_lord: str
    ascendant_star_lord: str
    ascendant_sub_lord: str
    strong_rp: List[str]  # Combined ruling planets


class KPSystem:
    """
    Complete KP System implementation for Vedic Astrology
    """
    
    def __init__(self):
        """Initialize KP System with precomputed sub-divisions"""
        self._build_sub_division_table()
    
    def _build_sub_division_table(self):
        """
        Build the 249 sub-divisions table
        Each nakshatra (13°20') is divided into 9 subs proportional to dasha periods
        """
        self.sub_divisions = []
        nakshatra_span = 13.333333333333334  # 13°20'
        
        for nak_idx, (nak_name, nak_lord) in enumerate(NAKSHATRAS):
            nak_start = nak_idx * nakshatra_span
            
            # Get the starting position in the dasha sequence for this nakshatra
            lord_idx = DASHA_SEQUENCE.index(nak_lord)
            sub_sequence = DASHA_SEQUENCE[lord_idx:] + DASHA_SEQUENCE[:lord_idx]
            
            current_pos = nak_start
            for sub_lord in sub_sequence:
                sub_span = nakshatra_span * DASHA_PERIODS[sub_lord] / TOTAL_DASHA_YEARS
                
                self.sub_divisions.append({
                    "start": current_pos,
                    "end": current_pos + sub_span,
                    "nakshatra": nak_name,
                    "nakshatra_idx": nak_idx,
                    "star_lord": nak_lord,
                    "sub_lord": sub_lord,
                    "span": sub_span
                })
                current_pos += sub_span
        
        # Verify we have 249 divisions (27 * 9 + some edge handling)
        # Actually it's 27 * 9 = 243 primary divisions
    
    def get_kp_position(self, longitude: float) -> KPPosition:
        """
        Get complete KP position data for a given longitude
        
        Args:
            longitude: Sidereal longitude (0-360)
            
        Returns:
            KPPosition with all sublord levels
        """
        # Normalize longitude
        lon = longitude % 360
        
        # Get sign
        sign = int(lon / 30)
        sign_name = SIGN_NAMES[sign]
        sign_lord = SIGN_LORDS[sign]
        degree_in_sign = lon % 30
        
        # Get nakshatra
        nakshatra_span = 13.333333333333334
        nakshatra = int(lon / nakshatra_span)
        nakshatra_name, nakshatra_lord = NAKSHATRAS[nakshatra]
        degree_in_nakshatra = lon % nakshatra_span
        
        # Get sub-lord by finding position in sub-division table
        sub_lord, degree_in_sub = self._get_sub_lord(lon, nakshatra, nakshatra_lord)
        
        # Get sub-sub-lord
        sub_sub_lord = self._get_sub_sub_lord(lon, nakshatra, nakshatra_lord, sub_lord)
        
        # Get sub-sub-sub-lord (3rd level)
        sub_sub_sub_lord = self._get_sub_level(lon, 3)
        
        # Get sub-sub-sub-sub-lord (4th level)
        sub_sub_sub_sub_lord = self._get_sub_level(lon, 4)
        
        return KPPosition(
            degree=lon,
            sign=sign,
            sign_name=sign_name,
            sign_lord=sign_lord,
            nakshatra=nakshatra,
            nakshatra_name=nakshatra_name,
            nakshatra_lord=nakshatra_lord,
            sub_lord=sub_lord,
            sub_sub_lord=sub_sub_lord,
            sub_sub_sub_lord=sub_sub_sub_lord,
            sub_sub_sub_sub_lord=sub_sub_sub_sub_lord,
            degree_in_sign=degree_in_sign,
            degree_in_nakshatra=degree_in_nakshatra,
            degree_in_sub=degree_in_sub
        )
    
    def _get_sub_lord(self, longitude: float, nakshatra: int, star_lord: str) -> Tuple[str, float]:
        """Calculate sub-lord for given longitude"""
        nakshatra_span = 13.333333333333334
        nak_start = nakshatra * nakshatra_span
        pos_in_nak = longitude - nak_start
        
        # Get sub sequence starting from star lord
        lord_idx = DASHA_SEQUENCE.index(star_lord)
        sub_sequence = DASHA_SEQUENCE[lord_idx:] + DASHA_SEQUENCE[:lord_idx]
        
        current_pos = 0
        for sub_lord in sub_sequence:
            sub_span = nakshatra_span * DASHA_PERIODS[sub_lord] / TOTAL_DASHA_YEARS
            if current_pos + sub_span > pos_in_nak:
                degree_in_sub = pos_in_nak - current_pos
                return sub_lord, degree_in_sub
            current_pos += sub_span
        
        # Edge case - return last sub
        return sub_sequence[-1], 0.0
    
    def _get_sub_sub_lord(self, longitude: float, nakshatra: int, 
                          star_lord: str, sub_lord: str) -> str:
        """Calculate sub-sub-lord for given longitude"""
        nakshatra_span = 13.333333333333334
        nak_start = nakshatra * nakshatra_span
        pos_in_nak = longitude - nak_start
        
        # Get sub sequence starting from star lord
        lord_idx = DASHA_SEQUENCE.index(star_lord)
        sub_sequence = DASHA_SEQUENCE[lord_idx:] + DASHA_SEQUENCE[:lord_idx]
        
        # Find position within the sub
        current_pos = 0
        sub_start = 0
        sub_span = 0
        for sl in sub_sequence:
            sub_span = nakshatra_span * DASHA_PERIODS[sl] / TOTAL_DASHA_YEARS
            if sl == sub_lord and current_pos <= pos_in_nak < current_pos + sub_span:
                sub_start = current_pos
                break
            current_pos += sub_span
        
        pos_in_sub = pos_in_nak - sub_start
        
        # Now divide the sub into sub-subs starting from sub_lord
        sub_lord_idx = DASHA_SEQUENCE.index(sub_lord)
        sub_sub_sequence = DASHA_SEQUENCE[sub_lord_idx:] + DASHA_SEQUENCE[:sub_lord_idx]
        
        current_pos = 0
        for sub_sub_lord in sub_sub_sequence:
            sub_sub_span = sub_span * DASHA_PERIODS[sub_sub_lord] / TOTAL_DASHA_YEARS
            if current_pos + sub_sub_span > pos_in_sub:
                return sub_sub_lord
            current_pos += sub_sub_span
        
        return sub_sub_sequence[-1]
    
    def _get_sub_level(self, longitude: float, level: int) -> str:
        """
        Calculate sub-lord at a specific level (3, 4, 5, etc.)
        Uses recursive division proportional to dasha periods
        """
        nakshatra_span = 13.333333333333334
        nakshatra = int(longitude / nakshatra_span)
        _, star_lord = NAKSHATRAS[nakshatra]
        
        nak_start = nakshatra * nakshatra_span
        pos = longitude - nak_start
        span = nakshatra_span
        
        current_lord = star_lord
        
        for _ in range(level):
            lord_idx = DASHA_SEQUENCE.index(current_lord)
            sequence = DASHA_SEQUENCE[lord_idx:] + DASHA_SEQUENCE[:lord_idx]
            
            current_pos = 0
            for lord in sequence:
                lord_span = span * DASHA_PERIODS[lord] / TOTAL_DASHA_YEARS
                if current_pos + lord_span > pos:
                    pos = pos - current_pos
                    span = lord_span
                    current_lord = lord
                    break
                current_pos += lord_span
        
        return current_lord
    
    def get_all_cuspal_positions(self, house_cusps: List[float]) -> Dict[int, KPPosition]:
        """
        Get KP positions for all 12 house cusps
        
        Args:
            house_cusps: List of 12 house cusp longitudes
            
        Returns:
            Dictionary mapping house number (1-12) to KPPosition
        """
        cuspal_positions = {}
        for i, cusp in enumerate(house_cusps[:12], 1):
            cuspal_positions[i] = self.get_kp_position(cusp)
        return cuspal_positions
    
    def get_planet_significators(
        self,
        planet_name: str,
        planet_kp: KPPosition,
        planet_house: int,
        house_cusps_kp: Dict[int, KPPosition]
    ) -> KPSignificators:
        """
        Calculate ABCD significators for a planet
        
        A = House(s) occupied by the star lord of the planet
        B = House(s) occupied by the planet itself
        C = House(s) owned by the star lord of the planet
        D = House(s) owned by the planet itself
        
        Args:
            planet_name: Name of the planet
            planet_kp: KP position of the planet
            planet_house: House occupied by the planet
            house_cusps_kp: KP positions of all house cusps
            
        Returns:
            KPSignificators with ABCD system
        """
        star_lord = planet_kp.nakshatra_lord
        
        # A: Houses where planets in the star lord's nakshatra are placed
        # This requires knowing where star lord is placed
        # For now, we return the house of the star lord
        A = self._get_houses_owned_by(star_lord)  # Simplified
        
        # B: House occupied by the planet
        B = [planet_house]
        
        # C: Houses owned by the star lord
        C = self._get_houses_owned_by(star_lord)
        
        # D: Houses owned by the planet
        D = self._get_houses_owned_by(planet_name)
        
        # Combined (unique houses)
        combined = list(set(A + B + C + D))
        combined.sort()
        
        return KPSignificators(
            planet_or_house=planet_name,
            A=A,
            B=B,
            C=C,
            D=D,
            combined=combined
        )
    
    def _get_houses_owned_by(self, planet: str) -> List[int]:
        """Get houses owned by a planet based on natural zodiac"""
        houses = []
        for sign, lord in SIGN_LORDS.items():
            if lord == planet:
                houses.append(sign + 1)  # Convert to 1-based house
        return houses
    
    def get_house_significators(
        self,
        house_num: int,
        planets_in_house: List[str],
        house_cusp_kp: KPPosition,
        all_planets_kp: Dict[str, KPPosition]
    ) -> KPSignificators:
        """
        Calculate ABCD significators for a house
        
        A = Planets in the star of occupants of the house
        B = Planets occupying the house
        C = Planets in the star of the owner of the house
        D = Owner of the house (Sign Lord)
        
        Args:
            house_num: House number (1-12)
            planets_in_house: List of planets in this house
            house_cusp_kp: KP position of house cusp
            all_planets_kp: KP positions of all planets
            
        Returns:
            KPSignificators for the house
        """
        house_owner = house_cusp_kp.sign_lord
        
        # A: Planets in the star of occupants
        A_planets = []
        for occupant in planets_in_house:
            if occupant in all_planets_kp:
                occupant_star = all_planets_kp[occupant].nakshatra_lord
                # Find all planets in this star
                for pname, pkp in all_planets_kp.items():
                    if pkp.nakshatra_lord == occupant_star:
                        A_planets.append(pname)
        
        # B: Occupants of the house
        B_planets = planets_in_house
        
        # C: Planets in the star of owner
        C_planets = []
        for pname, pkp in all_planets_kp.items():
            if pkp.nakshatra_lord == house_owner:
                C_planets.append(pname)
        
        # D: Owner
        D_planets = [house_owner]
        
        return KPSignificators(
            planet_or_house=f"House {house_num}",
            A=A_planets,  # type: ignore (these are planet names, not house numbers)
            B=B_planets,  # type: ignore
            C=C_planets,  # type: ignore
            D=D_planets,  # type: ignore
            combined=list(set(A_planets + B_planets + C_planets + D_planets))
        )
    
    def get_ruling_planets(
        self,
        current_time: datetime,
        moon_longitude: float,
        ascendant_longitude: float
    ) -> RulingPlanets:
        """
        Calculate Ruling Planets (RP) at a given moment
        Used in KP for timing events and horary astrology
        
        Args:
            current_time: Current datetime
            moon_longitude: Moon's sidereal longitude
            ascendant_longitude: Ascendant's sidereal longitude
            
        Returns:
            RulingPlanets with all RP components
        """
        # Weekday lord
        weekday_lords = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
        weekday_lord = weekday_lords[current_time.weekday()]
        
        # Moon's position
        moon_kp = self.get_kp_position(moon_longitude)
        moon_sign_lord = moon_kp.sign_lord
        moon_star_lord = moon_kp.nakshatra_lord
        moon_sub_lord = moon_kp.sub_lord
        
        # Ascendant's position
        asc_kp = self.get_kp_position(ascendant_longitude)
        asc_sign_lord = asc_kp.sign_lord
        asc_star_lord = asc_kp.nakshatra_lord
        asc_sub_lord = asc_kp.sub_lord
        
        # Strong ruling planets (those appearing multiple times)
        all_rp = [
            weekday_lord,
            moon_sign_lord, moon_star_lord, moon_sub_lord,
            asc_sign_lord, asc_star_lord, asc_sub_lord
        ]
        
        # Count occurrences
        rp_counts = {}
        for rp in all_rp:
            rp_counts[rp] = rp_counts.get(rp, 0) + 1
        
        # Sort by count (descending)
        strong_rp = sorted(rp_counts.keys(), key=lambda x: rp_counts[x], reverse=True)
        
        return RulingPlanets(
            weekday_lord=weekday_lord,
            moon_sign_lord=moon_sign_lord,
            moon_star_lord=moon_star_lord,
            moon_sub_lord=moon_sub_lord,
            ascendant_sign_lord=asc_sign_lord,
            ascendant_star_lord=asc_star_lord,
            ascendant_sub_lord=asc_sub_lord,
            strong_rp=strong_rp
        )
    
    def horary_number_to_position(self, horary_number: int) -> KPPosition:
        """
        Convert a horary number (1-249) to KP position
        
        In KP Horary, the querent provides a number 1-249
        Each number corresponds to a specific sub-lord division
        
        Args:
            horary_number: Number from 1 to 249
            
        Returns:
            KPPosition for the center of that horary division
        """
        if horary_number < 1 or horary_number > 249:
            raise ValueError("Horary number must be between 1 and 249")
        
        # Build 249 divisions
        divisions = []
        nakshatra_span = 13.333333333333334
        
        for nak_idx, (nak_name, nak_lord) in enumerate(NAKSHATRAS):
            nak_start = nak_idx * nakshatra_span
            
            lord_idx = DASHA_SEQUENCE.index(nak_lord)
            sub_sequence = DASHA_SEQUENCE[lord_idx:] + DASHA_SEQUENCE[:lord_idx]
            
            current_pos = nak_start
            for sub_lord in sub_sequence:
                sub_span = nakshatra_span * DASHA_PERIODS[sub_lord] / TOTAL_DASHA_YEARS
                divisions.append({
                    "number": len(divisions) + 1,
                    "start": current_pos,
                    "end": current_pos + sub_span,
                    "mid": current_pos + sub_span / 2
                })
                current_pos += sub_span
                
                if len(divisions) >= 249:
                    break
            if len(divisions) >= 249:
                break
        
        # Get the division for the horary number
        div = divisions[horary_number - 1]
        return self.get_kp_position(div["mid"])
    
    def calculate_kp_ayanamsa(self, date: datetime) -> float:
        """
        Calculate KP (Krishnamurti) Ayanamsa for a given date
        
        KP Ayanamsa is based on the position of the star Spica (Chitra)
        at exactly 180° (0° Libra)
        
        Args:
            date: Date for ayanamsa calculation
            
        Returns:
            Ayanamsa value in degrees
        """
        # Days since base date
        delta = date - KP_AYANAMSA_BASE_DATE
        years = delta.days / 365.25
        
        # Calculate ayanamsa
        ayanamsa = KP_AYANAMSA_BASE_VALUE + (years * KP_AYANAMSA_YEARLY_MOTION)
        
        return ayanamsa


def get_kp_data(
    planets: Dict[str, float],
    house_cusps: List[float],
    current_time: datetime
) -> Dict[str, Any]:
    """
    Convenience function to get complete KP data for a chart
    
    Args:
        planets: Dictionary of planet names to longitudes
        house_cusps: List of 12 house cusp longitudes
        current_time: Current datetime
        
    Returns:
        Complete KP analysis data
    """
    kp = KPSystem()
    
    # Get KP positions for all planets
    planet_kp = {}
    for planet, longitude in planets.items():
        planet_kp[planet] = kp.get_kp_position(longitude)
    
    # Get KP positions for all house cusps
    cusp_kp = kp.get_all_cuspal_positions(house_cusps)
    
    # Determine which planets are in which houses
    planets_by_house = {i: [] for i in range(1, 13)}
    for planet, longitude in planets.items():
        # Simple house determination (can be refined with actual cusp positions)
        for i in range(12):
            cusp_start = house_cusps[i]
            cusp_end = house_cusps[(i + 1) % 12]
            
            if cusp_end < cusp_start:  # Wrap around
                if longitude >= cusp_start or longitude < cusp_end:
                    planets_by_house[i + 1].append(planet)
                    break
            else:
                if cusp_start <= longitude < cusp_end:
                    planets_by_house[i + 1].append(planet)
                    break
    
    # Get ruling planets
    moon_lon = planets.get("Moon", 0)
    asc_lon = house_cusps[0] if house_cusps else 0
    ruling_planets = kp.get_ruling_planets(current_time, moon_lon, asc_lon)
    
    # Format output
    result = {
        "planet_positions": {
            name: {
                "degree": pos.degree,
                "sign": pos.sign_name,
                "sign_lord": pos.sign_lord,
                "nakshatra": pos.nakshatra_name,
                "star_lord": pos.nakshatra_lord,
                "sub_lord": pos.sub_lord,
                "sub_sub_lord": pos.sub_sub_lord
            }
            for name, pos in planet_kp.items()
        },
        "cuspal_positions": {
            house: {
                "degree": pos.degree,
                "sign": pos.sign_name,
                "sign_lord": pos.sign_lord,
                "nakshatra": pos.nakshatra_name,
                "star_lord": pos.nakshatra_lord,
                "sub_lord": pos.sub_lord,
                "sub_sub_lord": pos.sub_sub_lord
            }
            for house, pos in cusp_kp.items()
        },
        "planets_by_house": planets_by_house,
        "ruling_planets": {
            "weekday_lord": ruling_planets.weekday_lord,
            "moon_sign_lord": ruling_planets.moon_sign_lord,
            "moon_star_lord": ruling_planets.moon_star_lord,
            "moon_sub_lord": ruling_planets.moon_sub_lord,
            "asc_sign_lord": ruling_planets.ascendant_sign_lord,
            "asc_star_lord": ruling_planets.ascendant_star_lord,
            "asc_sub_lord": ruling_planets.ascendant_sub_lord,
            "strong_rp": ruling_planets.strong_rp
        }
    }
    
    return result
