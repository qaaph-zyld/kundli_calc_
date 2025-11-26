"""
Jaimini & Additional Dasha Systems
PGF Protocol: DASHA_003
Gate: GATE_5
Version: 1.0.0

Implements:
- Narayana Dasha (Jaimini)
- Sudasa (Sri Lagna Kendradi Rashi Dasha)
- Dwi-Saptati Sama Dasha (72-year cycle)
- Sthira Dasha
- Shoola Dasha
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import math


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# Jaimini Sign Lords (including Rahu/Ketu for Aquarius/Scorpio)
JAIMINI_SIGN_LORDS = {
    0: "Mars",      # Aries
    1: "Venus",     # Taurus
    2: "Mercury",   # Gemini
    3: "Moon",      # Cancer
    4: "Sun",       # Leo
    5: "Mercury",   # Virgo
    6: "Venus",     # Libra
    7: "Mars",      # Scorpio (also Ketu)
    8: "Jupiter",   # Sagittarius
    9: "Saturn",    # Capricorn
    10: "Saturn",   # Aquarius (also Rahu)
    11: "Jupiter"   # Pisces
}

# Chara Karaka order (highest to lowest longitude)
KARAKA_NAMES = ["Atmakaraka", "Amatyakaraka", "Bhratrukaraka", "Matrukaraka",
                "Putrakaraka", "Gnatikaraka", "Darakaraka"]


@dataclass
class DashaPeriod:
    """A dasha period"""
    sign: str
    sign_number: int
    start_date: datetime
    end_date: datetime
    years: float
    level: int  # 1=Mahadasha, 2=Antardasha, etc.
    sub_periods: List['DashaPeriod'] = field(default_factory=list)


class NarayanaDasha:
    """
    Narayana Dasha (Padakrama Dasha)
    
    Most important Jaimini rashi dasha.
    Progression based on whether the starting sign is odd/even.
    Duration = sign's lord's distance from sign.
    """
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        planets: Dict[str, float],
        lagna_type: str = "lagna"  # 'lagna', 'moon', 'sun'
    ) -> List[DashaPeriod]:
        """
        Calculate Narayana Dasha
        
        Args:
            birth_time: Birth datetime
            ascendant: Ascendant longitude
            planets: All planet longitudes
            lagna_type: Starting point (lagna, moon, or sun)
            
        Returns:
            List of dasha periods
        """
        # Get starting sign
        if lagna_type == "moon":
            start_sign = int(planets.get("Moon", 0) / 30)
        elif lagna_type == "sun":
            start_sign = int(planets.get("Sun", 0) / 30)
        else:
            start_sign = int(ascendant / 30)
        
        # Get planet positions in signs
        planet_signs = {p: int(lon / 30) for p, lon in planets.items()}
        
        periods = []
        current_date = birth_time
        
        # Progression direction
        is_odd_sign = start_sign % 2 == 0  # Aries=0 is odd
        
        for i in range(12):
            # Calculate which sign
            if is_odd_sign:
                sign_num = (start_sign + i) % 12
            else:
                sign_num = (start_sign - i + 12) % 12
            
            # Calculate duration
            years = self._get_sign_duration(sign_num, planet_signs)
            
            end_date = current_date + timedelta(days=years * 365.25)
            
            periods.append(DashaPeriod(
                sign=SIGNS[sign_num],
                sign_number=sign_num,
                start_date=current_date,
                end_date=end_date,
                years=years,
                level=1
            ))
            
            current_date = end_date
        
        return periods
    
    def _get_sign_duration(
        self,
        sign_num: int,
        planet_signs: Dict[str, int]
    ) -> float:
        """
        Get duration for a sign based on its lord's position
        
        Duration = distance of lord from sign + 1 (in years)
        """
        lord = JAIMINI_SIGN_LORDS[sign_num]
        
        # Find lord's position
        if lord in planet_signs:
            lord_sign = planet_signs[lord]
        else:
            lord_sign = sign_num  # Default to same sign
        
        # Calculate distance
        is_odd = sign_num % 2 == 0
        if is_odd:
            distance = (lord_sign - sign_num + 12) % 12
        else:
            distance = (sign_num - lord_sign + 12) % 12
        
        # Duration = distance + 1 (minimum 1 year)
        return max(1, distance + 1)
    
    def get_antardasha(
        self,
        mahadasha: DashaPeriod,
        planets: Dict[str, float]
    ) -> List[DashaPeriod]:
        """Calculate antardasha within a mahadasha"""
        planet_signs = {p: int(lon / 30) for p, lon in planets.items()}
        antardashas = []
        
        is_odd = mahadasha.sign_number % 2 == 0
        total_duration = (mahadasha.end_date - mahadasha.start_date).days / 365.25
        
        # Calculate proportional durations
        durations = []
        for i in range(12):
            if is_odd:
                sign_num = (mahadasha.sign_number + i) % 12
            else:
                sign_num = (mahadasha.sign_number - i + 12) % 12
            
            years = self._get_sign_duration(sign_num, planet_signs)
            durations.append((sign_num, years))
        
        total_years = sum(d[1] for d in durations)
        
        current_date = mahadasha.start_date
        for sign_num, years in durations:
            proportion = years / total_years
            ad_years = total_duration * proportion
            end_date = current_date + timedelta(days=ad_years * 365.25)
            
            antardashas.append(DashaPeriod(
                sign=SIGNS[sign_num],
                sign_number=sign_num,
                start_date=current_date,
                end_date=end_date,
                years=ad_years,
                level=2
            ))
            
            current_date = end_date
        
        return antardashas


class SudasaDasha:
    """
    Sudasa (Sri Lagna Kendradi Rashi Dasha)
    
    Based on Sri Lagna (prosperity point).
    Progression from kendras, then panaparas, then apoklimas.
    """
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        birth_time: datetime,
        sree_lagna: float,
        planets: Dict[str, float]
    ) -> List[DashaPeriod]:
        """
        Calculate Sudasa Dasha
        
        Args:
            birth_time: Birth datetime
            sree_lagna: Sri Lagna longitude
            planets: All planet longitudes
            
        Returns:
            List of dasha periods
        """
        sl_sign = int(sree_lagna / 30)
        planet_signs = {p: int(lon / 30) for p, lon in planets.items()}
        
        # Order: Kendras (1,4,7,10), Panaparas (2,5,8,11), Apoklimas (3,6,9,12)
        order = []
        
        # Kendras from Sri Lagna
        for offset in [0, 3, 6, 9]:
            order.append((sl_sign + offset) % 12)
        
        # Panaparas
        for offset in [1, 4, 7, 10]:
            order.append((sl_sign + offset) % 12)
        
        # Apoklimas
        for offset in [2, 5, 8, 11]:
            order.append((sl_sign + offset) % 12)
        
        periods = []
        current_date = birth_time
        
        for sign_num in order:
            years = self._get_duration(sign_num, planet_signs, sl_sign)
            end_date = current_date + timedelta(days=years * 365.25)
            
            periods.append(DashaPeriod(
                sign=SIGNS[sign_num],
                sign_number=sign_num,
                start_date=current_date,
                end_date=end_date,
                years=years,
                level=1
            ))
            
            current_date = end_date
        
        return periods
    
    def _get_duration(
        self,
        sign_num: int,
        planet_signs: Dict[str, int],
        sl_sign: int
    ) -> float:
        """Calculate duration for Sudasa"""
        lord = JAIMINI_SIGN_LORDS[sign_num]
        
        if lord in planet_signs:
            lord_sign = planet_signs[lord]
        else:
            lord_sign = sign_num
        
        # Similar to Narayana but from Sri Lagna
        is_odd = sl_sign % 2 == 0
        if is_odd:
            distance = (lord_sign - sign_num + 12) % 12
        else:
            distance = (sign_num - lord_sign + 12) % 12
        
        return max(1, distance + 1)


class DwiSaptatiSamaDasha:
    """
    Dwi-Saptati Sama Dasha (72-year cycle)
    
    Equal 6-year periods for each sign.
    Total cycle = 72 years (12 signs x 6 years).
    Used when specific conditions are met.
    """
    
    YEARS_PER_SIGN = 6
    TOTAL_CYCLE = 72
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float
    ) -> List[DashaPeriod]:
        """
        Calculate Dwi-Saptati Sama Dasha
        
        Each sign gets 6 years. Starts from Lagna sign.
        """
        start_sign = int(ascendant / 30)
        periods = []
        current_date = birth_time
        
        for i in range(12):
            sign_num = (start_sign + i) % 12
            years = self.YEARS_PER_SIGN
            end_date = current_date + timedelta(days=years * 365.25)
            
            periods.append(DashaPeriod(
                sign=SIGNS[sign_num],
                sign_number=sign_num,
                start_date=current_date,
                end_date=end_date,
                years=years,
                level=1
            ))
            
            current_date = end_date
        
        return periods
    
    def is_applicable(
        self,
        sun_sign: int,
        moon_sign: int,
        ascendant_sign: int
    ) -> bool:
        """
        Check if Dwi-Saptati Sama Dasha is applicable
        
        Applicable when:
        - Lagna and Moon are in same sign, or
        - Sun and Lagna are in same sign, or
        - Lagna lord is in Lagna
        """
        if moon_sign == ascendant_sign:
            return True
        if sun_sign == ascendant_sign:
            return True
        return False


class SthiraDasha:
    """
    Sthira Dasha (Fixed Dasha)
    
    Fixed durations based on sign type:
    - Movable (Chara): 7 years
    - Fixed (Sthira): 8 years  
    - Dual (Dwiswabhava): 9 years
    """
    
    # Sign types: 0=Movable, 1=Fixed, 2=Dual
    SIGN_TYPES = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    DURATIONS = [7, 8, 9]  # Years for each type
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float
    ) -> List[DashaPeriod]:
        """Calculate Sthira Dasha"""
        start_sign = int(ascendant / 30)
        periods = []
        current_date = birth_time
        
        # Progression based on odd/even
        is_odd = start_sign % 2 == 0
        
        for i in range(12):
            if is_odd:
                sign_num = (start_sign + i) % 12
            else:
                sign_num = (start_sign - i + 12) % 12
            
            sign_type = self.SIGN_TYPES[sign_num]
            years = self.DURATIONS[sign_type]
            end_date = current_date + timedelta(days=years * 365.25)
            
            periods.append(DashaPeriod(
                sign=SIGNS[sign_num],
                sign_number=sign_num,
                start_date=current_date,
                end_date=end_date,
                years=years,
                level=1
            ))
            
            current_date = end_date
        
        return periods


class ShoolaDasha:
    """
    Shoola Dasha
    
    For timing death/major health events.
    Based on trine relationships.
    """
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        focus: str = "longevity"  # 'longevity', 'marriage', 'children'
    ) -> List[DashaPeriod]:
        """Calculate Shoola Dasha"""
        start_sign = int(ascendant / 30)
        
        # Group signs into trine sets
        trine_sets = [
            [0, 4, 8],    # Fire trines
            [1, 5, 9],    # Earth trines
            [2, 6, 10],   # Air trines
            [3, 7, 11]    # Water trines
        ]
        
        # Find which trine set contains the start sign
        for trine_set in trine_sets:
            if start_sign in trine_set:
                active_trines = trine_set
                break
        
        periods = []
        current_date = birth_time
        
        # Each trine gets 9 years (total 27 years per set)
        for sign_num in active_trines:
            years = 9
            end_date = current_date + timedelta(days=years * 365.25)
            
            periods.append(DashaPeriod(
                sign=SIGNS[sign_num],
                sign_number=sign_num,
                start_date=current_date,
                end_date=end_date,
                years=years,
                level=1
            ))
            
            current_date = end_date
        
        return periods


def calculate_all_jaimini_dashas(
    birth_time: datetime,
    ascendant: float,
    planets: Dict[str, float],
    sree_lagna: float
) -> Dict[str, Any]:
    """
    Calculate all Jaimini dasha systems
    
    Args:
        birth_time: Birth datetime
        ascendant: Ascendant longitude
        planets: Planet longitudes
        sree_lagna: Sri Lagna longitude
        
    Returns:
        All dasha systems data
    """
    narayana = NarayanaDasha()
    sudasa = SudasaDasha()
    dwisaptati = DwiSaptatiSamaDasha()
    sthira = SthiraDasha()
    shoola = ShoolaDasha()
    
    return {
        "narayana_dasha": {
            "name": "Narayana Dasha",
            "cycle": "Variable",
            "applicability": "Universal Jaimini dasha",
            "periods": [
                {
                    "sign": p.sign,
                    "start": p.start_date.isoformat(),
                    "end": p.end_date.isoformat(),
                    "years": round(p.years, 2)
                }
                for p in narayana.calculate(birth_time, ascendant, planets)
            ]
        },
        "sudasa_dasha": {
            "name": "Sudasa (Sri Lagna Kendradi)",
            "cycle": "Variable",
            "applicability": "Prosperity and wealth timing",
            "periods": [
                {
                    "sign": p.sign,
                    "start": p.start_date.isoformat(),
                    "end": p.end_date.isoformat(),
                    "years": round(p.years, 2)
                }
                for p in sudasa.calculate(birth_time, sree_lagna, planets)
            ]
        },
        "dwi_saptati_sama": {
            "name": "Dwi-Saptati Sama Dasha",
            "cycle": "72 years",
            "applicability": "When specific conditions met",
            "periods": [
                {
                    "sign": p.sign,
                    "start": p.start_date.isoformat(),
                    "end": p.end_date.isoformat(),
                    "years": round(p.years, 2)
                }
                for p in dwisaptati.calculate(birth_time, ascendant)
            ]
        },
        "sthira_dasha": {
            "name": "Sthira Dasha",
            "cycle": "96 years",
            "applicability": "General timing",
            "periods": [
                {
                    "sign": p.sign,
                    "start": p.start_date.isoformat(),
                    "end": p.end_date.isoformat(),
                    "years": round(p.years, 2)
                }
                for p in sthira.calculate(birth_time, ascendant)
            ]
        },
        "shoola_dasha": {
            "name": "Shoola Dasha",
            "cycle": "27 years per trine",
            "applicability": "Health and longevity",
            "periods": [
                {
                    "sign": p.sign,
                    "start": p.start_date.isoformat(),
                    "end": p.end_date.isoformat(),
                    "years": round(p.years, 2)
                }
                for p in shoola.calculate(birth_time, ascendant)
            ]
        }
    }
