"""
Additional Dasha Systems Implementation
PGF Protocol: DASHA_002
Gate: GATE_5
Version: 1.0.0

This module implements additional Dasha systems beyond Vimshottari:
- Yogini Dasha (36 year cycle)
- Ashtottari Dasha (108 year cycle)
- Chara Dasha (Jaimini system)
- Kalachakra Dasha
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import math


# ============= YOGINI DASHA =============

# Yogini Dasha periods (total 36 years)
YOGINI_PERIODS = {
    "Mangala": 1,      # Mars - अमृत सिद्धि
    "Pingala": 2,      # Sun - प्रेत सिद्धि
    "Dhanya": 3,       # Jupiter - विद्या सिद्धि
    "Bhramari": 4,     # Mars - लक्ष्मी सिद्धि
    "Bhadrika": 5,     # Mercury - गोधूलि
    "Ulka": 6,         # Saturn - षड्ज  
    "Siddha": 7,       # Venus - खर
    "Sankata": 8       # Rahu - संकट
}

YOGINI_SEQUENCE = ["Mangala", "Pingala", "Dhanya", "Bhramari", 
                   "Bhadrika", "Ulka", "Siddha", "Sankata"]

YOGINI_PLANETS = {
    "Mangala": "Moon",
    "Pingala": "Sun", 
    "Dhanya": "Jupiter",
    "Bhramari": "Mars",
    "Bhadrika": "Mercury",
    "Ulka": "Saturn",
    "Siddha": "Venus",
    "Sankata": "Rahu"
}

TOTAL_YOGINI_YEARS = 36


# ============= ASHTOTTARI DASHA =============

# Ashtottari Dasha periods (total 108 years)
ASHTOTTARI_PERIODS = {
    "Sun": 6,
    "Moon": 15,
    "Mars": 8,
    "Mercury": 17,
    "Saturn": 10,
    "Jupiter": 19,
    "Rahu": 12,
    "Venus": 21
}

ASHTOTTARI_SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", 
                       "Saturn", "Jupiter", "Rahu", "Venus"]

# Ashtottari Nakshatra starting points
ASHTOTTARI_NAKSHATRAS = {
    "Sun": [5, 14, 23],      # Ardra, Swati, Shatabhisha
    "Moon": [6, 15, 24],     # Punarvasu, Vishakha, Purva Bhadrapada
    "Mars": [7, 16, 25],     # Pushya, Anuradha, Uttara Bhadrapada
    "Mercury": [8, 17, 26],  # Ashlesha, Jyeshtha, Revati
    "Saturn": [0, 9, 18],    # Ashwini, Magha, Mula
    "Jupiter": [1, 10, 19],  # Bharani, Purva Phalguni, Purva Ashadha
    "Rahu": [2, 11, 20],     # Krittika, Uttara Phalguni, Uttara Ashadha
    "Venus": [3, 12, 21]     # Rohini, Hasta, Shravana
}

TOTAL_ASHTOTTARI_YEARS = 108


# ============= CHARA DASHA (Jaimini) =============

SIGN_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]


@dataclass
class DashaPeriod:
    """Generic dasha period"""
    planet_or_sign: str
    start_date: datetime
    end_date: datetime
    duration_years: float
    sub_periods: Optional[List['DashaPeriod']] = None


class YoginiDasha:
    """
    Yogini Dasha Calculator
    
    Based on Moon's nakshatra position
    8 Yoginis with periods totaling 36 years
    Faster cycle, useful for short-term predictions
    """
    
    def __init__(self):
        self.total_years = TOTAL_YOGINI_YEARS
    
    def calculate_dasha_at_birth(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> Dict[str, Any]:
        """
        Calculate Yogini dasha at birth
        
        Args:
            birth_time: Birth date and time
            moon_longitude: Moon's longitude at birth
            
        Returns:
            Dictionary with dasha periods
        """
        # Calculate nakshatra (each is 13°20')
        nakshatra_span = 13.333333333333334
        nakshatra_idx = int(moon_longitude / nakshatra_span)
        pos_in_nakshatra = moon_longitude % nakshatra_span
        
        # Starting Yogini based on nakshatra
        # Cycle: nakshatra mod 8 maps to yogini
        starting_yogini_idx = (nakshatra_idx + 3) % 8  # Offset by 3 as per tradition
        
        # Calculate balance of first dasha
        remaining_fraction = 1 - (pos_in_nakshatra / nakshatra_span)
        
        # Build dasha sequence
        yogini_order = (
            YOGINI_SEQUENCE[starting_yogini_idx:] + 
            YOGINI_SEQUENCE[:starting_yogini_idx]
        )
        
        periods: List[Dict[str, Any]] = []
        current = birth_time
        
        # First period (balance)
        first_yogini = yogini_order[0]
        first_years = YOGINI_PERIODS[first_yogini] * remaining_fraction
        first_end = current + timedelta(days=first_years * 365.25)
        
        periods.append({
            "yogini": first_yogini,
            "planet": YOGINI_PLANETS[first_yogini],
            "start_date": current.isoformat(),
            "end_date": first_end.isoformat(),
            "duration_years": first_years
        })
        current = first_end
        
        # Remaining periods
        for yogini in yogini_order[1:]:
            years = YOGINI_PERIODS[yogini]
            end = current + timedelta(days=years * 365.25)
            periods.append({
                "yogini": yogini,
                "planet": YOGINI_PLANETS[yogini],
                "start_date": current.isoformat(),
                "end_date": end.isoformat(),
                "duration_years": years
            })
            current = end
        
        return {
            "dasha_type": "Yogini",
            "total_cycle": self.total_years,
            "starting_yogini": first_yogini,
            "balance_at_birth": remaining_fraction,
            "periods": periods
        }
    
    def get_antardasha(
        self,
        main_yogini: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Calculate sub-periods within a Yogini mahadasha"""
        main_years = YOGINI_PERIODS[main_yogini]
        
        # Antardasha starts from main yogini
        start_idx = YOGINI_SEQUENCE.index(main_yogini)
        sequence = YOGINI_SEQUENCE[start_idx:] + YOGINI_SEQUENCE[:start_idx]
        
        total_days = (end_date - start_date).total_seconds() / 86400
        current = start_date
        antardashas = []
        
        for yogini in sequence:
            sub_years = (YOGINI_PERIODS[yogini] * main_years) / self.total_years
            sub_days = total_days * (sub_years / main_years)
            end = current + timedelta(days=sub_days)
            
            antardashas.append({
                "yogini": yogini,
                "planet": YOGINI_PLANETS[yogini],
                "start_date": current.isoformat(),
                "end_date": end.isoformat(),
                "duration_years": sub_years
            })
            current = end
        
        return antardashas


class AshtottariDasha:
    """
    Ashtottari Dasha Calculator
    
    108 year cycle using 8 planets (excluding Ketu)
    Used when Rahu is in kendra/trikona from Lagna lord
    More relevant for night births
    """
    
    def __init__(self):
        self.total_years = TOTAL_ASHTOTTARI_YEARS
    
    def calculate_dasha_at_birth(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> Dict[str, Any]:
        """
        Calculate Ashtottari dasha at birth
        
        Only uses 28 nakshatras (excludes Abhijit which is part of Uttarashada/Shravana)
        Starts from Ardra nakshatra
        """
        # Calculate nakshatra
        nakshatra_span = 13.333333333333334
        nakshatra_idx = int(moon_longitude / nakshatra_span)
        pos_in_nakshatra = moon_longitude % nakshatra_span
        
        # Find starting planet based on nakshatra
        starting_planet = self._get_starting_planet(nakshatra_idx)
        
        # Calculate balance
        remaining_fraction = 1 - (pos_in_nakshatra / nakshatra_span)
        
        # Build sequence starting from starting_planet
        start_idx = ASHTOTTARI_SEQUENCE.index(starting_planet)
        planet_order = ASHTOTTARI_SEQUENCE[start_idx:] + ASHTOTTARI_SEQUENCE[:start_idx]
        
        periods: List[Dict[str, Any]] = []
        current = birth_time
        
        # First period (balance)
        first_planet = planet_order[0]
        first_years = ASHTOTTARI_PERIODS[first_planet] * remaining_fraction
        first_end = current + timedelta(days=first_years * 365.25)
        
        periods.append({
            "planet": first_planet,
            "start_date": current.isoformat(),
            "end_date": first_end.isoformat(),
            "duration_years": first_years
        })
        current = first_end
        
        # Remaining periods
        for planet in planet_order[1:]:
            years = ASHTOTTARI_PERIODS[planet]
            end = current + timedelta(days=years * 365.25)
            periods.append({
                "planet": planet,
                "start_date": current.isoformat(),
                "end_date": end.isoformat(),
                "duration_years": years
            })
            current = end
        
        return {
            "dasha_type": "Ashtottari",
            "total_cycle": self.total_years,
            "starting_planet": first_planet,
            "balance_at_birth": remaining_fraction,
            "periods": periods,
            "applicability": "Applicable when Rahu in kendra/trikona from lagna lord"
        }
    
    def _get_starting_planet(self, nakshatra_idx: int) -> str:
        """Determine starting planet based on nakshatra"""
        for planet, nakshatras in ASHTOTTARI_NAKSHATRAS.items():
            if nakshatra_idx in nakshatras:
                return planet
        # Default fallback
        return "Sun"
    
    def get_antardasha(
        self,
        main_planet: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Calculate sub-periods"""
        main_years = ASHTOTTARI_PERIODS[main_planet]
        
        start_idx = ASHTOTTARI_SEQUENCE.index(main_planet)
        sequence = ASHTOTTARI_SEQUENCE[start_idx:] + ASHTOTTARI_SEQUENCE[:start_idx]
        
        total_days = (end_date - start_date).total_seconds() / 86400
        current = start_date
        antardashas = []
        
        for planet in sequence:
            sub_years = (ASHTOTTARI_PERIODS[planet] * main_years) / self.total_years
            sub_days = total_days * (sub_years / main_years)
            end = current + timedelta(days=sub_days)
            
            antardashas.append({
                "planet": planet,
                "start_date": current.isoformat(),
                "end_date": end.isoformat(),
                "duration_years": sub_years
            })
            current = end
        
        return antardashas


class CharaDasha:
    """
    Chara Dasha (Jaimini System)
    
    Rashi-based dasha using Jaimini principles
    Duration based on sign's distance from its lord
    """
    
    def __init__(self):
        # Jaimini sign lords (different from Parashara for some signs)
        self.sign_lords = {
            0: "Mars",      # Aries
            1: "Venus",     # Taurus
            2: "Mercury",   # Gemini
            3: "Moon",      # Cancer
            4: "Sun",       # Leo
            5: "Mercury",   # Virgo
            6: "Venus",     # Libra
            7: "Mars",      # Scorpio (Jaimini uses Mars, not Ketu)
            8: "Jupiter",   # Sagittarius
            9: "Saturn",    # Capricorn
            10: "Saturn",   # Aquarius (Jaimini uses Saturn, not Rahu)
            11: "Jupiter"   # Pisces
        }
    
    def calculate_dasha_at_birth(
        self,
        birth_time: datetime,
        ascendant_longitude: float,
        planet_longitudes: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate Chara dasha at birth
        
        Args:
            birth_time: Birth datetime
            ascendant_longitude: Ascendant longitude
            planet_longitudes: All planet longitudes
            
        Returns:
            Dictionary with Chara dasha periods
        """
        # Determine ascendant sign
        asc_sign = int(ascendant_longitude / 30)
        
        # Determine dasha progression order based on sign type
        # Odd signs (Aries, Gemini, etc.): direct order
        # Even signs (Taurus, Cancer, etc.): reverse order
        if asc_sign % 2 == 0:  # Odd signs (0=Aries is odd in Jaimini)
            sign_order = list(range(asc_sign, 12)) + list(range(0, asc_sign))
        else:  # Even signs
            sign_order = list(range(asc_sign, -1, -1)) + list(range(11, asc_sign, -1))
        
        periods: List[Dict[str, Any]] = []
        current = birth_time
        
        for sign in sign_order:
            # Calculate duration based on lord's position
            duration = self._calculate_sign_duration(sign, planet_longitudes)
            end = current + timedelta(days=duration * 365.25)
            
            periods.append({
                "sign": SIGN_NAMES[sign],
                "sign_number": sign,
                "lord": self.sign_lords[sign],
                "start_date": current.isoformat(),
                "end_date": end.isoformat(),
                "duration_years": duration
            })
            current = end
        
        return {
            "dasha_type": "Chara (Jaimini)",
            "ascendant_sign": SIGN_NAMES[asc_sign],
            "progression": "direct" if asc_sign % 2 == 0 else "reverse",
            "periods": periods
        }
    
    def _calculate_sign_duration(
        self,
        sign: int,
        planet_longitudes: Dict[str, float]
    ) -> int:
        """
        Calculate dasha duration for a sign
        
        Based on distance of sign lord from the sign
        """
        lord = self.sign_lords[sign]
        
        if lord not in planet_longitudes:
            return 7  # Default
        
        lord_longitude = planet_longitudes[lord]
        lord_sign = int(lord_longitude / 30)
        
        # Calculate distance
        # For odd signs: count forward
        # For even signs: count backward
        if sign % 2 == 0:  # Odd sign
            distance = (lord_sign - sign) % 12
        else:  # Even sign
            distance = (sign - lord_sign) % 12
        
        # Duration is distance + 1, but if lord is in same sign, it's 12
        if distance == 0:
            return 12
        else:
            return distance + 1


class KalachakraDasha:
    """
    Kalachakra Dasha
    
    Based on Moon's navamsa and direction (savya/apsavya)
    Complex but very precise timing system
    """
    
    # Kalachakra navamsa sequence
    SAVYA_SEQUENCE = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Scorpio", "Libra", "Virgo", "Leo", "Sagittarius"
    ]
    
    APSAVYA_SEQUENCE = [
        "Pisces", "Aquarius", "Capricorn", "Sagittarius",
        "Leo", "Virgo", "Libra", "Scorpio", "Aries"
    ]
    
    # Duration in years for each sign group
    DURATIONS = {
        "Aries": 7, "Taurus": 16, "Gemini": 9, "Cancer": 21,
        "Leo": 5, "Virgo": 9, "Libra": 16, "Scorpio": 7,
        "Sagittarius": 10, "Capricorn": 4, "Aquarius": 4, "Pisces": 10
    }
    
    def __init__(self):
        self.total_cycle = 83  # Approximation
    
    def calculate_dasha_at_birth(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> Dict[str, Any]:
        """
        Calculate Kalachakra dasha
        
        Args:
            birth_time: Birth datetime
            moon_longitude: Moon's longitude
            
        Returns:
            Kalachakra dasha periods
        """
        # Calculate Moon's navamsa
        navamsa = self._calculate_navamsa(moon_longitude)
        
        # Determine if savya or apsavya
        # Based on nakshatra group (1-9 savya, 10-18 savya, 19-27 apsavya roughly)
        nakshatra = int(moon_longitude / (360/27))
        
        # Simplification: odd nakshatra groups are savya
        is_savya = (nakshatra // 9) % 2 == 0
        
        sequence = self.SAVYA_SEQUENCE if is_savya else self.APSAVYA_SEQUENCE
        
        # Find starting position in sequence
        navamsa_sign = SIGN_NAMES[navamsa]
        start_idx = 0
        for i, sign in enumerate(sequence):
            if sign == navamsa_sign:
                start_idx = i
                break
        
        # Build order
        order = sequence[start_idx:] + sequence[:start_idx]
        
        periods: List[Dict[str, Any]] = []
        current = birth_time
        
        for sign in order:
            duration = self.DURATIONS[sign]
            end = current + timedelta(days=duration * 365.25)
            
            periods.append({
                "sign": sign,
                "start_date": current.isoformat(),
                "end_date": end.isoformat(),
                "duration_years": duration
            })
            current = end
        
        return {
            "dasha_type": "Kalachakra",
            "direction": "Savya" if is_savya else "Apsavya",
            "moon_navamsa": navamsa_sign,
            "periods": periods
        }
    
    def _calculate_navamsa(self, longitude: float) -> int:
        """Calculate navamsa sign from longitude"""
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        navamsa_in_sign = int(degree_in_sign / (30/9))
        navamsa_sign = (sign * 9 + navamsa_in_sign) % 12
        return navamsa_sign


# ============= CONVENIENCE FUNCTIONS =============

def calculate_all_dasha_systems(
    birth_time: datetime,
    moon_longitude: float,
    ascendant_longitude: float,
    planet_longitudes: Dict[str, float]
) -> Dict[str, Any]:
    """
    Calculate all dasha systems for comparison
    
    Args:
        birth_time: Birth datetime
        moon_longitude: Moon's longitude
        ascendant_longitude: Ascendant longitude
        planet_longitudes: All planet longitudes
        
    Returns:
        All dasha systems data
    """
    yogini = YoginiDasha()
    ashtottari = AshtottariDasha()
    chara = CharaDasha()
    kalachakra = KalachakraDasha()
    
    return {
        "yogini_dasha": yogini.calculate_dasha_at_birth(birth_time, moon_longitude),
        "ashtottari_dasha": ashtottari.calculate_dasha_at_birth(birth_time, moon_longitude),
        "chara_dasha": chara.calculate_dasha_at_birth(
            birth_time, ascendant_longitude, planet_longitudes
        ),
        "kalachakra_dasha": kalachakra.calculate_dasha_at_birth(birth_time, moon_longitude)
    }


def get_current_dasha_all_systems(
    birth_time: datetime,
    moon_longitude: float,
    ascendant_longitude: float,
    planet_longitudes: Dict[str, float],
    current_time: datetime
) -> Dict[str, str]:
    """
    Get current running dasha in all systems
    
    Returns:
        Dictionary with current dasha for each system
    """
    all_dashas = calculate_all_dasha_systems(
        birth_time, moon_longitude, ascendant_longitude, planet_longitudes
    )
    
    result = {}
    
    for system_name, system_data in all_dashas.items():
        for period in system_data.get("periods", []):
            start = datetime.fromisoformat(period["start_date"])
            end = datetime.fromisoformat(period["end_date"])
            
            if start <= current_time <= end:
                if "yogini" in period:
                    result[system_name] = f"{period['yogini']} ({period['planet']})"
                elif "planet" in period:
                    result[system_name] = period["planet"]
                elif "sign" in period:
                    result[system_name] = period["sign"]
                break
    
    return result
