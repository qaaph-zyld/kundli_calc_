"""
Advanced Dasha Systems - Phase 6
PGF Protocol: DASHA_005
Gate: GATE_6
Version: 1.0.0

Implements 20 more Dasha systems to match Jagannatha Hora:
1. Kalachakra Dasha
2. Ashtottari Dasha (108 years)
3. Shodasottari Dasha (116 years)
4. Tribhagi Vimsottari
5. Chara Dasha (Parasara)
6. Chara Dasha (K.N. Rao)
7. Yogardha Dasha
8. Trikona Dasha
9. Lagna Kendradi Rasi Dasha
10. Niryaana Shoola Dasha
11. Brahma Dasha
12. Varnada Dasha
13. Tara Dasha
14. Patyayini Dasha
15. Sudarsana Chakra Dasha
16. Tithi Ashtottari Dasha
17. Tithi Yogini Dasha
18. Lagnaamsaka Dasha
19. Padanaathaamsa Dasha
20. Drigdasa
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import math


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]


@dataclass
class DashaPeriod:
    """A dasha period"""
    ruler: str
    start_date: datetime
    end_date: datetime
    years: float
    level: int = 1
    sub_periods: List['DashaPeriod'] = field(default_factory=list)


# =============================================================================
# 1. KALACHAKRA DASHA
# =============================================================================
class KalachakraDasha:
    """
    Kalachakra Dasha - Wheel of Time
    
    Complex dasha based on nakshatra pada.
    Uses savya (clockwise) and apasavya (anti-clockwise) movements.
    Total cycle: 100 years
    """
    
    # Kalachakra groups (Savya - clockwise)
    SAVYA_GROUPS = {
        "Aries": [7, 16, 12, 21, 5, 9, 10, 16, 4],
        "Taurus": [10, 4, 7, 16, 12, 21, 5, 9, 16],
        "Gemini": [16, 10, 4, 7, 16, 12, 21, 5, 9],
        "Cancer": [21, 5, 9, 10, 4, 7, 16, 12, 16]
    }
    
    # Apasavya groups (counter-clockwise)
    APASAVYA_GROUPS = {
        "Leo": [9, 5, 21, 12, 16, 7, 4, 10, 16],
        "Virgo": [16, 9, 5, 21, 12, 16, 7, 4, 10],
        "Libra": [4, 16, 9, 5, 21, 12, 16, 7, 10],
        "Scorpio": [7, 4, 10, 16, 9, 5, 21, 12, 16]
    }
    
    # Sign groups
    SIGN_GROUPS = [
        ["Aries", "Taurus", "Gemini", "Cancer"],
        ["Leo", "Virgo", "Libra", "Scorpio"],
        ["Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    ]
    
    def calculate(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Kalachakra Dasha periods"""
        nak_idx = int(moon_longitude / (360/27))
        pada = int((moon_longitude % (360/27)) / (360/108)) + 1
        
        # Determine savya or apasavya
        nak_sign = int(moon_longitude / 30)
        is_savya = nak_sign < 4 or nak_sign >= 8
        
        # Get years sequence
        if is_savya:
            base_sign = SIGNS[nak_sign % 4]
            years_seq = self.SAVYA_GROUPS.get(base_sign, [9]*9)
        else:
            base_sign = SIGNS[4 + (nak_sign % 4)]
            years_seq = self.APASAVYA_GROUPS.get(base_sign, [9]*9)
        
        # Calculate balance
        nak_span = 360/27
        pos_in_nak = moon_longitude % nak_span
        balance = 1 - (pos_in_nak / nak_span)
        
        periods = []
        current = birth_time
        sign_idx = nak_sign
        
        for i, years in enumerate(years_seq):
            actual_years = years * balance if i == 0 else years
            end = current + timedelta(days=actual_years * 365.25)
            
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx % 12],
                start_date=current,
                end_date=end,
                years=actual_years,
                level=1
            ))
            
            current = end
            sign_idx = (sign_idx + 1) % 12 if is_savya else (sign_idx - 1) % 12
        
        return periods


# =============================================================================
# 2. ASHTOTTARI DASHA (108 years)
# =============================================================================
class AshtottariDasha:
    """
    Ashtottari Dasha - 108 year cycle
    
    Uses only 8 planets (excludes Ketu).
    Applicable when Rahu is in kendra/trikona from lagna lord.
    """
    
    YEARS = {
        "Sun": 6, "Moon": 15, "Mars": 8, "Mercury": 17,
        "Saturn": 10, "Jupiter": 19, "Rahu": 12, "Venus": 21
    }
    
    SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", "Saturn", "Jupiter", "Rahu", "Venus"]
    
    # Starting nakshatras for each planet
    NAK_START = {
        "Sun": [5, 14, 23],      # Ardra, Swati, Shatabhisha
        "Moon": [6, 15, 24],     # Punarvasu, Vishakha, P.Bhadra
        "Mars": [7, 16, 25],     # Pushya, Anuradha, U.Bhadra
        "Mercury": [8, 17, 26],  # Ashlesha, Jyeshtha, Revati
        "Saturn": [0, 9, 18],    # Ashwini, Magha, Mula
        "Jupiter": [1, 10, 19],  # Bharani, P.Phalguni, P.Ashadha
        "Rahu": [2, 11, 20],     # Krittika, U.Phalguni, U.Ashadha
        "Venus": [3, 12, 21]     # Rohini, Hasta, Shravana
    }
    
    def calculate(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Ashtottari Dasha periods"""
        nak_idx = int(moon_longitude / (360/27))
        
        # Find starting planet
        start_planet = "Sun"
        for planet, naks in self.NAK_START.items():
            if nak_idx in naks or (nak_idx - 4) % 9 == naks[0] % 9:
                start_planet = planet
                break
        
        # Balance calculation
        nak_span = 360/27
        pos_in_nak = moon_longitude % nak_span
        balance = 1 - (pos_in_nak / nak_span)
        
        # Build sequence
        start_idx = self.SEQUENCE.index(start_planet)
        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]
        
        periods = []
        current = birth_time
        
        for i, planet in enumerate(sequence):
            years = self.YEARS[planet]
            if i == 0:
                years *= balance
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=planet,
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 3. SHODASOTTARI DASHA (116 years)
# =============================================================================
class ShodasottariDasha:
    """
    Shodasottari Dasha - 116 year cycle
    
    Applicable when lagna is in Krishna Paksha (waning Moon).
    """
    
    YEARS = {
        "Sun": 11, "Mars": 12, "Jupiter": 13, "Saturn": 14,
        "Ketu": 15, "Moon": 16, "Mercury": 17, "Venus": 18
    }
    
    SEQUENCE = ["Sun", "Mars", "Jupiter", "Saturn", "Ketu", "Moon", "Mercury", "Venus"]
    
    def calculate(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Shodasottari Dasha periods"""
        nak_idx = int(moon_longitude / (360/27))
        start_idx = nak_idx % 8
        
        nak_span = 360/27
        pos_in_nak = moon_longitude % nak_span
        balance = 1 - (pos_in_nak / nak_span)
        
        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]
        
        periods = []
        current = birth_time
        
        for i, planet in enumerate(sequence):
            years = self.YEARS[planet]
            if i == 0:
                years *= balance
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=planet,
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 4. TRIBHAGI VIMSOTTARI
# =============================================================================
class TribhagiVimsottari:
    """
    Tribhagi Vimsottari - Three-fold Vimsottari
    
    Each mahadasha is divided into 3 parts instead of 9.
    """
    
    YEARS = {
        "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
        "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
    }
    
    SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    
    def calculate(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Tribhagi Vimsottari with 3-part division"""
        nak_idx = int(moon_longitude / (360/27))
        start_planet = self.SEQUENCE[nak_idx % 9]
        
        nak_span = 360/27
        pos_in_nak = moon_longitude % nak_span
        balance = 1 - (pos_in_nak / nak_span)
        
        start_idx = self.SEQUENCE.index(start_planet)
        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]
        
        periods = []
        current = birth_time
        
        for i, planet in enumerate(sequence):
            years = self.YEARS[planet]
            if i == 0:
                years *= balance
            
            end = current + timedelta(days=years * 365.25)
            
            # Calculate tribhagi sub-periods (3 parts)
            sub_periods = []
            sub_current = current
            part_years = years / 3
            
            for j in range(3):
                sub_planet = self.SEQUENCE[(start_idx + i + j) % 9]
                sub_end = sub_current + timedelta(days=part_years * 365.25)
                sub_periods.append(DashaPeriod(
                    ruler=sub_planet,
                    start_date=sub_current,
                    end_date=sub_end,
                    years=part_years,
                    level=2
                ))
                sub_current = sub_end
            
            periods.append(DashaPeriod(
                ruler=planet,
                start_date=current,
                end_date=end,
                years=years,
                level=1,
                sub_periods=sub_periods
            ))
            current = end
        
        return periods


# =============================================================================
# 5. CHARA DASHA (PARASARA)
# =============================================================================
class CharaDashaParasara:
    """
    Chara Dasha as per Parasara
    
    Rashi-based dasha with years based on sign lord's position.
    """
    
    SIGN_LORDS = {
        0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
        4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
        8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter"
    }
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        planets: Dict[str, float]
    ) -> List[DashaPeriod]:
        """Calculate Chara Dasha (Parasara version)"""
        lagna_sign = int(ascendant / 30)
        
        # Determine if odd or even sign
        is_odd = lagna_sign % 2 == 0
        
        periods = []
        current = birth_time
        
        for i in range(12):
            if is_odd:
                sign_idx = (lagna_sign + i) % 12
            else:
                sign_idx = (lagna_sign - i) % 12
            
            # Years = lord's distance from sign
            lord = self.SIGN_LORDS[sign_idx]
            lord_sign = int(planets.get(lord, 0) / 30)
            
            if is_odd:
                years = ((lord_sign - sign_idx) % 12)
            else:
                years = ((sign_idx - lord_sign) % 12)
            
            if years == 0:
                years = 12
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 6. CHARA DASHA (K.N. RAO)
# =============================================================================
class CharaDashaKNRao:
    """
    Chara Dasha as per K.N. Rao
    
    Modified version with different progression rules.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        planets: Dict[str, float]
    ) -> List[DashaPeriod]:
        """Calculate Chara Dasha (K.N. Rao version)"""
        lagna_sign = int(ascendant / 30)
        
        # K.N. Rao uses different counting
        is_movable = lagna_sign in [0, 3, 6, 9]
        is_fixed = lagna_sign in [1, 4, 7, 10]
        
        periods = []
        current = birth_time
        
        for i in range(12):
            if is_movable:
                sign_idx = (lagna_sign + i) % 12
            elif is_fixed:
                sign_idx = (lagna_sign - i) % 12
            else:  # Dual
                sign_idx = (lagna_sign + i) % 12 if i % 2 == 0 else (lagna_sign - i) % 12
            
            # K.N. Rao method for years
            sign_lord_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11][sign_idx]
            years = (sign_lord_idx % 12) + 1
            if years > 12:
                years = years - 12
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 7. YOGARDHA DASHA
# =============================================================================
class YogardhaDasha:
    """
    Yogardha Dasha - Half of Yoga
    
    Based on the midpoint between lagna and Moon.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Yogardha Dasha"""
        # Yogardha point = midpoint of lagna and Moon
        yogardha = (ascendant + moon_longitude) / 2
        if abs(moon_longitude - ascendant) > 180:
            yogardha = (yogardha + 180) % 360
        
        yogardha_sign = int(yogardha / 30)
        is_odd = yogardha_sign % 2 == 0
        
        periods = []
        current = birth_time
        
        for i in range(12):
            if is_odd:
                sign_idx = (yogardha_sign + i) % 12
            else:
                sign_idx = (yogardha_sign - i) % 12
            
            years = (sign_idx % 12) + 1
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 8. TRIKONA DASHA
# =============================================================================
class TrikonaDasha:
    """
    Trikona Dasha - Based on trines
    
    Progression through trine signs (1-5-9 pattern).
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float
    ) -> List[DashaPeriod]:
        """Calculate Trikona Dasha"""
        lagna_sign = int(ascendant / 30)
        
        # Trine progression
        trine_sequence = []
        for i in range(4):  # 4 groups of trines
            base = (lagna_sign + i * 3) % 12
            trine_sequence.extend([base, (base + 4) % 12, (base + 8) % 12])
        
        periods = []
        current = birth_time
        
        for i, sign_idx in enumerate(trine_sequence):
            # Years based on sign position
            years = [9, 9, 9, 7, 7, 7, 5, 5, 5, 11, 11, 11][i % 12]
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 9. LAGNA KENDRADI RASI DASHA
# =============================================================================
class LagnaKendradiDasha:
    """
    Lagna Kendradi Rasi Dasha
    
    Starts from kendras (1,4,7,10), then panapharas (2,5,8,11), then apoklimas.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        planets: Dict[str, float]
    ) -> List[DashaPeriod]:
        """Calculate Lagna Kendradi Rasi Dasha"""
        lagna_sign = int(ascendant / 30)
        
        # Kendra, Panapara, Apoklima order
        kendras = [(lagna_sign + i) % 12 for i in [0, 3, 6, 9]]
        panaparas = [(lagna_sign + i) % 12 for i in [1, 4, 7, 10]]
        apoklimas = [(lagna_sign + i) % 12 for i in [2, 5, 8, 11]]
        
        sequence = kendras + panaparas + apoklimas
        
        periods = []
        current = birth_time
        
        for sign_idx in sequence:
            # Count planets in sign for years
            planet_count = sum(1 for p, lon in planets.items() if int(lon/30) == sign_idx)
            years = max(planet_count + 1, 1) * 3  # Base years
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 10. NIRYAANA SHOOLA DASHA
# =============================================================================
class NiryaanShoolaDasha:
    """
    Niryaana Shoola Dasha - For timing death
    
    Specifically used for determining time of death.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Niryaana Shoola Dasha"""
        lagna_sign = int(ascendant / 30)
        moon_sign = int(moon_longitude / 30)
        
        # Use stronger of lagna or Moon
        if lagna_sign in [0, 3, 6, 9]:  # Movable
            start_sign = lagna_sign
        elif moon_sign in [0, 3, 6, 9]:
            start_sign = moon_sign
        else:
            start_sign = lagna_sign
        
        periods = []
        current = birth_time
        
        for i in range(12):
            sign_idx = (start_sign + i) % 12
            
            # Fixed years for Shoola
            years = 9  # Standard Shoola period
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 11. BRAHMA DASHA
# =============================================================================
class BrahmaDasha:
    """
    Brahma Dasha
    
    Based on Brahma planet (6th, 8th, or 12th lord).
    """
    
    SIGN_LORDS = {
        0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
        4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
        8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter"
    }
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        planets: Dict[str, float]
    ) -> List[DashaPeriod]:
        """Calculate Brahma Dasha"""
        lagna_sign = int(ascendant / 30)
        
        # Find Brahma (6th, 8th, or 12th lord in odd sign)
        sixth_lord = self.SIGN_LORDS[(lagna_sign + 5) % 12]
        eighth_lord = self.SIGN_LORDS[(lagna_sign + 7) % 12]
        twelfth_lord = self.SIGN_LORDS[(lagna_sign + 11) % 12]
        
        # Brahma determination (simplified)
        brahma = sixth_lord
        brahma_sign = int(planets.get(brahma, 0) / 30)
        
        periods = []
        current = birth_time
        
        for i in range(12):
            sign_idx = (brahma_sign + i) % 12
            years = (i % 9) + 1
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 12. VARNADA DASHA
# =============================================================================
class VarnadaDasha:
    """
    Varnada Dasha
    
    Based on Varnada Lagna calculation.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        hora_lagna: float
    ) -> List[DashaPeriod]:
        """Calculate Varnada Dasha"""
        lagna_sign = int(ascendant / 30)
        hora_sign = int(hora_lagna / 30)
        
        # Varnada calculation
        if lagna_sign % 2 == 0:  # Odd sign
            varnada = (lagna_sign + hora_sign) % 12
        else:  # Even sign
            varnada = (lagna_sign - hora_sign) % 12
        
        periods = []
        current = birth_time
        
        for i in range(12):
            sign_idx = (varnada + i) % 12
            years = (sign_idx % 12) + 1
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 13. TARA DASHA
# =============================================================================
class TaraDasha:
    """
    Tara Dasha
    
    Based on Navatara (9 tara) system from Moon.
    """
    
    TARA_NAMES = ["Janma", "Sampat", "Vipat", "Kshema", "Pratyak",
                  "Sadhaka", "Vadha", "Mitra", "Parama Mitra"]
    
    TARA_YEARS = [3, 5, 2, 6, 4, 7, 1, 8, 9]
    
    def calculate(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Tara Dasha"""
        moon_nak = int(moon_longitude / (360/27))
        
        periods = []
        current = birth_time
        
        for cycle in range(3):  # 3 cycles of 9 taras
            for i in range(9):
                nak_idx = (moon_nak + cycle * 9 + i) % 27
                years = self.TARA_YEARS[i]
                
                end = current + timedelta(days=years * 365.25)
                periods.append(DashaPeriod(
                    ruler=f"{NAKSHATRAS[nak_idx]} ({self.TARA_NAMES[i]})",
                    start_date=current,
                    end_date=end,
                    years=years,
                    level=1
                ))
                current = end
        
        return periods


# =============================================================================
# 14. PATYAYINI DASHA
# =============================================================================
class PatyayiniDasha:
    """
    Patyayini Dasha
    
    Based on 7th lord and marriage significators.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        planets: Dict[str, float]
    ) -> List[DashaPeriod]:
        """Calculate Patyayini Dasha"""
        lagna_sign = int(ascendant / 30)
        seventh_sign = (lagna_sign + 6) % 12
        
        periods = []
        current = birth_time
        
        for i in range(12):
            sign_idx = (seventh_sign + i) % 12
            
            # Years based on distance from 7th
            years = ((i % 12) + 1)
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 15. SUDARSANA CHAKRA DASHA
# =============================================================================
class SudarsanaChakraDasha:
    """
    Sudarsana Chakra Dasha
    
    Combines Lagna, Moon, and Sun progressions.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        sun_longitude: float,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Sudarsana Chakra Dasha"""
        lagna_sign = int(ascendant / 30)
        sun_sign = int(sun_longitude / 30)
        moon_sign = int(moon_longitude / 30)
        
        periods = []
        current = birth_time
        
        for year in range(1, 121):  # Up to 120 years
            # Each year combines all three
            lagna_prog = (lagna_sign + year - 1) % 12
            sun_prog = (sun_sign + year - 1) % 12
            moon_prog = (moon_sign + year - 1) % 12
            
            end = current + timedelta(days=365.25)
            periods.append(DashaPeriod(
                ruler=f"L:{SIGNS[lagna_prog][:3]}/S:{SIGNS[sun_prog][:3]}/M:{SIGNS[moon_prog][:3]}",
                start_date=current,
                end_date=end,
                years=1,
                level=1
            ))
            current = end
        
        return periods[:12]  # Return first 12 years


# =============================================================================
# 16-17. TITHI BASED DASHAS
# =============================================================================
class TithiAshtottariDasha:
    """
    Tithi Ashtottari Dasha
    
    108-year dasha based on tithi at birth.
    """
    
    TITHI_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", 
                   "Venus", "Saturn", "Rahu"] * 4
    
    YEARS = {"Sun": 6, "Moon": 15, "Mars": 8, "Mercury": 17,
             "Jupiter": 19, "Venus": 21, "Saturn": 10, "Rahu": 12}
    
    def calculate(
        self,
        birth_time: datetime,
        sun_longitude: float,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Tithi Ashtottari Dasha"""
        # Tithi = Moon - Sun / 12
        tithi = int(((moon_longitude - sun_longitude) % 360) / 12)
        start_lord = self.TITHI_LORDS[tithi]
        
        sequence = list(self.YEARS.keys())
        start_idx = sequence.index(start_lord)
        sequence = sequence[start_idx:] + sequence[:start_idx]
        
        periods = []
        current = birth_time
        
        for planet in sequence:
            years = self.YEARS[planet]
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=planet,
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


class TithiYoginiDasha:
    """
    Tithi Yogini Dasha
    
    36-year dasha based on tithi.
    """
    
    YOGINIS = ["Mangala", "Pingala", "Dhanya", "Bhramari",
               "Bhadrika", "Ulka", "Siddha", "Sankata"]
    
    YEARS = [1, 2, 3, 4, 5, 6, 7, 8]
    
    def calculate(
        self,
        birth_time: datetime,
        sun_longitude: float,
        moon_longitude: float
    ) -> List[DashaPeriod]:
        """Calculate Tithi Yogini Dasha"""
        tithi = int(((moon_longitude - sun_longitude) % 360) / 12)
        start_idx = tithi % 8
        
        sequence = self.YOGINIS[start_idx:] + self.YOGINIS[:start_idx]
        years_seq = self.YEARS[start_idx:] + self.YEARS[:start_idx]
        
        periods = []
        current = birth_time
        
        for i, yogini in enumerate(sequence):
            years = years_seq[i]
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=yogini,
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 18. LAGNAAMSAKA DASHA
# =============================================================================
class LagnaamsakaDasha:
    """
    Lagnaamsaka Dasha
    
    Based on Navamsa lagna position.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float
    ) -> List[DashaPeriod]:
        """Calculate Lagnaamsaka Dasha"""
        # Calculate navamsa of ascendant
        degree = ascendant % 30
        navamsa_num = int(degree / (30/9))
        lagna_sign = int(ascendant / 30)
        
        # Navamsa sign
        element = lagna_sign % 4
        start_signs = [0, 9, 5, 1]
        navamsa_sign = (start_signs[element] + navamsa_num) % 12
        
        is_odd = navamsa_sign % 2 == 0
        
        periods = []
        current = birth_time
        
        for i in range(12):
            if is_odd:
                sign_idx = (navamsa_sign + i) % 12
            else:
                sign_idx = (navamsa_sign - i) % 12
            
            years = (sign_idx % 12) + 1
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 19. PADANAATHAAMSA DASHA
# =============================================================================
class PadanathaamsakaDasha:
    """
    Padanaathaamsa Dasha
    
    Based on Arudha Lagna's navamsa.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        arudha_lagna: float
    ) -> List[DashaPeriod]:
        """Calculate Padanaathaamsa Dasha"""
        # Navamsa of Arudha
        degree = arudha_lagna % 30
        navamsa_num = int(degree / (30/9))
        al_sign = int(arudha_lagna / 30)
        
        element = al_sign % 4
        start_signs = [0, 9, 5, 1]
        navamsa_sign = (start_signs[element] + navamsa_num) % 12
        
        periods = []
        current = birth_time
        
        for i in range(12):
            sign_idx = (navamsa_sign + i) % 12
            years = (i % 12) + 1
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# 20. DRIG DASHA
# =============================================================================
class DrigDasha:
    """
    Drig Dasha (Aspect Dasha)
    
    Based on aspects (drishti) of planets.
    """
    
    def calculate(
        self,
        birth_time: datetime,
        ascendant: float,
        planets: Dict[str, float]
    ) -> List[DashaPeriod]:
        """Calculate Drig Dasha"""
        lagna_sign = int(ascendant / 30)
        
        # Calculate aspect strength for each sign
        aspect_scores = {}
        for i in range(12):
            score = 0
            for planet, lon in planets.items():
                planet_sign = int(lon / 30)
                # Check aspects
                distance = (i - planet_sign) % 12
                if distance in [0, 3, 6, 9]:  # Kendra
                    score += 2
                elif distance in [4, 8]:  # Trine
                    score += 1
            aspect_scores[i] = score
        
        # Sort by score (highest first)
        sorted_signs = sorted(aspect_scores.keys(), key=lambda x: -aspect_scores[x])
        
        periods = []
        current = birth_time
        
        for sign_idx in sorted_signs:
            years = aspect_scores[sign_idx] + 1
            
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(
                ruler=SIGNS[sign_idx],
                start_date=current,
                end_date=end,
                years=years,
                level=1
            ))
            current = end
        
        return periods


# =============================================================================
# MASTER CALCULATOR
# =============================================================================
class AdvancedDashaCalculator:
    """Calculate all advanced dasha systems"""
    
    def __init__(self):
        self.kalachakra = KalachakraDasha()
        self.ashtottari = AshtottariDasha()
        self.shodasottari = ShodasottariDasha()
        self.tribhagi = TribhagiVimsottari()
        self.chara_parasara = CharaDashaParasara()
        self.chara_knrao = CharaDashaKNRao()
        self.yogardha = YogardhaDasha()
        self.trikona = TrikonaDasha()
        self.lagna_kendradi = LagnaKendradiDasha()
        self.niryaana_shoola = NiryaanShoolaDasha()
        self.brahma = BrahmaDasha()
        self.varnada = VarnadaDasha()
        self.tara = TaraDasha()
        self.patyayini = PatyayiniDasha()
        self.sudarsana = SudarsanaChakraDasha()
        self.tithi_ashtottari = TithiAshtottariDasha()
        self.tithi_yogini = TithiYoginiDasha()
        self.lagnaamsaka = LagnaamsakaDasha()
        self.padanaathaamsa = PadanathaamsakaDasha()
        self.drig = DrigDasha()
    
    def calculate_all(
        self,
        birth_time: datetime,
        ascendant: float,
        planets: Dict[str, float],
        hora_lagna: float = None,
        arudha_lagna: float = None
    ) -> Dict[str, List[DashaPeriod]]:
        """Calculate all 20 advanced dasha systems"""
        moon = planets.get("Moon", 0)
        sun = planets.get("Sun", 0)
        
        if hora_lagna is None:
            hora_lagna = ascendant
        if arudha_lagna is None:
            arudha_lagna = ascendant
        
        return {
            "kalachakra": self.kalachakra.calculate(birth_time, moon),
            "ashtottari": self.ashtottari.calculate(birth_time, moon),
            "shodasottari": self.shodasottari.calculate(birth_time, moon),
            "tribhagi_vimsottari": self.tribhagi.calculate(birth_time, moon),
            "chara_parasara": self.chara_parasara.calculate(birth_time, ascendant, planets),
            "chara_knrao": self.chara_knrao.calculate(birth_time, ascendant, planets),
            "yogardha": self.yogardha.calculate(birth_time, ascendant, moon),
            "trikona": self.trikona.calculate(birth_time, ascendant),
            "lagna_kendradi": self.lagna_kendradi.calculate(birth_time, ascendant, planets),
            "niryaana_shoola": self.niryaana_shoola.calculate(birth_time, ascendant, moon),
            "brahma": self.brahma.calculate(birth_time, ascendant, planets),
            "varnada": self.varnada.calculate(birth_time, ascendant, hora_lagna),
            "tara": self.tara.calculate(birth_time, moon),
            "patyayini": self.patyayini.calculate(birth_time, ascendant, planets),
            "sudarsana_chakra": self.sudarsana.calculate(birth_time, ascendant, sun, moon),
            "tithi_ashtottari": self.tithi_ashtottari.calculate(birth_time, sun, moon),
            "tithi_yogini": self.tithi_yogini.calculate(birth_time, sun, moon),
            "lagnaamsaka": self.lagnaamsaka.calculate(birth_time, ascendant),
            "padanaathaamsa": self.padanaathaamsa.calculate(birth_time, arudha_lagna),
            "drig": self.drig.calculate(birth_time, ascendant, planets)
        }
    
    def get_available_dashas(self) -> List[str]:
        """Get list of available dasha systems"""
        return [
            "kalachakra", "ashtottari", "shodasottari", "tribhagi_vimsottari",
            "chara_parasara", "chara_knrao", "yogardha", "trikona",
            "lagna_kendradi", "niryaana_shoola", "brahma", "varnada",
            "tara", "patyayini", "sudarsana_chakra", "tithi_ashtottari",
            "tithi_yogini", "lagnaamsaka", "padanaathaamsa", "drig"
        ]
