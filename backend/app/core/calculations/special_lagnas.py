"""
Special Lagnas (Special Ascendants) Implementation
PGF Protocol: LAGNA_001
Gate: GATE_5
Version: 1.0.0

This module implements various special lagnas used in Vedic Astrology:
- Hora Lagna (HL) - Wealth indicator
- Ghati Lagna (GL) - Fame and recognition
- Bhava Lagna (BL) - Inner self
- Varnada Lagna (VL) - Status and dignity
- Sree Lagna (SL) - Prosperity
- Pranapada Lagna - Life force
- Indu Lagna - Wealth combinations
- Yoga Point
- Bhrigu Bindu - Destiny point
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Tuple
from datetime import datetime
import math


SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
              "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]


@dataclass
class LagnaResult:
    """Result of a special lagna calculation"""
    name: str
    sanskrit_name: str
    longitude: float
    sign: int
    sign_name: str
    degree_in_sign: float
    nakshatra: str
    lord: str
    house_from_lagna: int
    interpretation: str


class SpecialLagnas:
    """
    Calculator for Special Lagnas in Vedic Astrology
    """
    
    NAKSHATRAS = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    
    def __init__(self):
        pass
    
    def calculate_all_lagnas(
        self,
        birth_datetime: datetime,
        ascendant: float,
        moon_longitude: float,
        sun_longitude: float,
        planets: Dict[str, float]
    ) -> Dict[str, LagnaResult]:
        """
        Calculate all special lagnas
        
        Args:
            birth_datetime: Birth date and time
            ascendant: Ascendant longitude
            moon_longitude: Moon's longitude
            sun_longitude: Sun's longitude
            planets: Dictionary of planet longitudes
            
        Returns:
            Dictionary of all special lagnas
        """
        results = {}
        
        # Hora Lagna
        results['hora_lagna'] = self.calculate_hora_lagna(
            birth_datetime, ascendant
        )
        
        # Ghati Lagna
        results['ghati_lagna'] = self.calculate_ghati_lagna(
            birth_datetime, ascendant
        )
        
        # Bhava Lagna
        results['bhava_lagna'] = self.calculate_bhava_lagna(
            birth_datetime, ascendant
        )
        
        # Varnada Lagna
        results['varnada_lagna'] = self.calculate_varnada_lagna(
            ascendant, birth_datetime
        )
        
        # Sree Lagna
        results['sree_lagna'] = self.calculate_sree_lagna(
            ascendant, moon_longitude
        )
        
        # Pranapada Lagna
        results['pranapada_lagna'] = self.calculate_pranapada_lagna(
            ascendant, sun_longitude
        )
        
        # Indu Lagna
        results['indu_lagna'] = self.calculate_indu_lagna(
            ascendant, moon_longitude, planets
        )
        
        # Bhrigu Bindu
        results['bhrigu_bindu'] = self.calculate_bhrigu_bindu(
            moon_longitude, planets.get('Rahu', 0)
        )
        
        return results
    
    def _create_lagna_result(
        self,
        name: str,
        sanskrit: str,
        longitude: float,
        ascendant: float,
        interpretation: str
    ) -> LagnaResult:
        """Helper to create LagnaResult"""
        lon = longitude % 360
        sign = int(lon / 30)
        deg_in_sign = lon % 30
        nakshatra_idx = int(lon / (360 / 27))
        asc_sign = int(ascendant / 30)
        house = ((sign - asc_sign + 12) % 12) + 1
        
        return LagnaResult(
            name=name,
            sanskrit_name=sanskrit,
            longitude=lon,
            sign=sign,
            sign_name=SIGN_NAMES[sign],
            degree_in_sign=deg_in_sign,
            nakshatra=self.NAKSHATRAS[nakshatra_idx],
            lord=SIGN_LORDS[sign],
            house_from_lagna=house,
            interpretation=interpretation
        )
    
    def calculate_hora_lagna(
        self,
        birth_datetime: datetime,
        ascendant: float
    ) -> LagnaResult:
        """
        Calculate Hora Lagna (HL)
        
        Hora Lagna indicates wealth and material prosperity.
        Moves 30° for every 2.5 ghatis (1 hour) from sunrise.
        
        Formula: HL = Asc + (hours_from_sunrise * 30 / 2.5)
        """
        # Approximate: assume 6 AM sunrise
        sunrise_hour = 6
        birth_hour = birth_datetime.hour + birth_datetime.minute / 60
        hours_from_sunrise = (birth_hour - sunrise_hour) % 24
        
        # HL advances 1 sign per 2.5 hours (or 30° per 2.5 hours)
        advancement = (hours_from_sunrise / 2.5) * 30
        hora_lagna = (ascendant + advancement) % 360
        
        return self._create_lagna_result(
            "Hora Lagna", "होरा लग्न", hora_lagna, ascendant,
            "Indicates wealth, prosperity, and material gains. Planets aspecting HL influence financial fortune."
        )
    
    def calculate_ghati_lagna(
        self,
        birth_datetime: datetime,
        ascendant: float
    ) -> LagnaResult:
        """
        Calculate Ghati Lagna (GL)
        
        Ghati Lagna indicates fame, power, and recognition.
        Moves 30° for every 5 ghatis (2 hours) from sunrise.
        """
        sunrise_hour = 6
        birth_hour = birth_datetime.hour + birth_datetime.minute / 60
        hours_from_sunrise = (birth_hour - sunrise_hour) % 24
        
        # GL advances 1 sign per 5 hours
        advancement = (hours_from_sunrise / 5) * 30
        ghati_lagna = (ascendant + advancement) % 360
        
        return self._create_lagna_result(
            "Ghati Lagna", "घटी लग्न", ghati_lagna, ascendant,
            "Indicates fame, recognition, and social standing. Strong GL gives public acclaim."
        )
    
    def calculate_bhava_lagna(
        self,
        birth_datetime: datetime,
        ascendant: float
    ) -> LagnaResult:
        """
        Calculate Bhava Lagna (BL)
        
        Bhava Lagna represents the inner self and soul purpose.
        Based on time of birth.
        """
        # BL = Asc + (birth_ghatis from midnight * 30/60)
        birth_hour = birth_datetime.hour + birth_datetime.minute / 60
        ghatis_from_midnight = birth_hour * 2.5
        
        advancement = (ghatis_from_midnight / 60) * 360
        bhava_lagna = (ascendant + advancement) % 360
        
        return self._create_lagna_result(
            "Bhava Lagna", "भाव लग्न", bhava_lagna, ascendant,
            "Represents the inner self, emotions, and mental disposition. Important for psychological analysis."
        )
    
    def calculate_varnada_lagna(
        self,
        ascendant: float,
        birth_datetime: datetime
    ) -> LagnaResult:
        """
        Calculate Varnada Lagna (VL)
        
        Varnada indicates dignity, status, and varna (caste/class).
        Based on relationship between Lagna and Hora Lagna.
        """
        # Simplified calculation
        asc_sign = int(ascendant / 30)
        
        # Calculate Hora Lagna sign first
        sunrise_hour = 6
        birth_hour = birth_datetime.hour + birth_datetime.minute / 60
        hours_from_sunrise = (birth_hour - sunrise_hour) % 24
        hora_advancement = (hours_from_sunrise / 2.5) * 30
        hora_lagna = (ascendant + hora_advancement) % 360
        hora_sign = int(hora_lagna / 30)
        
        # Varnada calculation
        if asc_sign % 2 == 0:  # Odd sign (0=Aries is odd)
            varnada_sign = (asc_sign + hora_sign) % 12
        else:  # Even sign
            varnada_sign = (asc_sign - hora_sign + 12) % 12
        
        varnada_lagna = varnada_sign * 30 + (ascendant % 30)
        
        return self._create_lagna_result(
            "Varnada Lagna", "वर्णदा लग्न", varnada_lagna, ascendant,
            "Indicates social status, dignity, and one's place in society. Used in Jaimini astrology."
        )
    
    def calculate_sree_lagna(
        self,
        ascendant: float,
        moon_longitude: float
    ) -> LagnaResult:
        """
        Calculate Sree Lagna (SL)
        
        Sree Lagna indicates prosperity and Lakshmi's blessings.
        Based on Lagna and Moon positions.
        """
        # SL = Midpoint of Lagna and Moon, extended
        midpoint = (ascendant + moon_longitude) / 2
        
        # If Moon is behind Lagna, adjust
        if abs(ascendant - moon_longitude) > 180:
            midpoint = (midpoint + 180) % 360
        
        sree_lagna = midpoint
        
        return self._create_lagna_result(
            "Sree Lagna", "श्री लग्न", sree_lagna, ascendant,
            "Indicates prosperity, fortune, and blessings of Goddess Lakshmi. Strong SL brings abundance."
        )
    
    def calculate_pranapada_lagna(
        self,
        ascendant: float,
        sun_longitude: float
    ) -> LagnaResult:
        """
        Calculate Pranapada Lagna
        
        Pranapada represents life force and vitality.
        Based on Sun's position from Lagna.
        """
        # Distance of Sun from Lagna
        sun_from_asc = (sun_longitude - ascendant + 360) % 360
        
        # Pranapada = Lagna + (Sun_from_Lagna * 5)
        pranapada = (ascendant + (sun_from_asc / 3)) % 360
        
        return self._create_lagna_result(
            "Pranapada Lagna", "प्राणपद लग्न", pranapada, ascendant,
            "Indicates life force, vitality, and physical constitution. Important for health analysis."
        )
    
    def calculate_indu_lagna(
        self,
        ascendant: float,
        moon_longitude: float,
        planets: Dict[str, float]
    ) -> LagnaResult:
        """
        Calculate Indu Lagna
        
        Indu Lagna indicates wealth through specific planetary combinations.
        Based on 9th lord from Lagna and Moon.
        """
        asc_sign = int(ascendant / 30)
        moon_sign = int(moon_longitude / 30)
        
        # 9th house lord from Lagna
        ninth_from_asc = (asc_sign + 8) % 12
        lord_9_lagna = SIGN_LORDS[ninth_from_asc]
        
        # 9th house lord from Moon
        ninth_from_moon = (moon_sign + 8) % 12
        lord_9_moon = SIGN_LORDS[ninth_from_moon]
        
        # Get positions of these lords
        lord_9_lagna_pos = planets.get(lord_9_lagna, 0)
        lord_9_moon_pos = planets.get(lord_9_moon, 0)
        
        # Indu Lagna = Midpoint of 9th lords
        indu_lagna = (lord_9_lagna_pos + lord_9_moon_pos) / 2
        
        return self._create_lagna_result(
            "Indu Lagna", "इन्दु लग्न", indu_lagna, ascendant,
            "Special wealth indicator. Planets in 11th from Indu Lagna indicate sources of wealth."
        )
    
    def calculate_bhrigu_bindu(
        self,
        moon_longitude: float,
        rahu_longitude: float
    ) -> LagnaResult:
        """
        Calculate Bhrigu Bindu (Destiny Point)
        
        Bhrigu Bindu = Midpoint of Moon and Rahu
        Transits over this point trigger significant events.
        """
        midpoint = (moon_longitude + rahu_longitude) / 2
        
        # Adjust if distance > 180
        if abs(moon_longitude - rahu_longitude) > 180:
            midpoint = (midpoint + 180) % 360
        
        # Use Moon's sign as reference for house calculation
        moon_sign = int(moon_longitude / 30)
        
        return self._create_lagna_result(
            "Bhrigu Bindu", "भृगु बिन्दु", midpoint, moon_longitude,
            "Destiny point. Jupiter's transit over this triggers major life events. Saturn's transit brings challenges."
        )


def calculate_special_lagnas(
    birth_datetime: datetime,
    ascendant: float,
    moon: float,
    sun: float,
    planets: Dict[str, float]
) -> Dict[str, Dict[str, Any]]:
    """
    Convenience function to calculate all special lagnas
    
    Args:
        birth_datetime: Birth datetime
        ascendant: Ascendant longitude
        moon: Moon longitude
        sun: Sun longitude
        planets: All planet longitudes
        
    Returns:
        Dictionary of special lagnas with details
    """
    calculator = SpecialLagnas()
    results = calculator.calculate_all_lagnas(
        birth_datetime, ascendant, moon, sun, planets
    )
    
    return {
        name: {
            "longitude": lagna.longitude,
            "sign": lagna.sign_name,
            "degree": lagna.degree_in_sign,
            "nakshatra": lagna.nakshatra,
            "lord": lagna.lord,
            "house": lagna.house_from_lagna,
            "interpretation": lagna.interpretation,
            "sanskrit": lagna.sanskrit_name
        }
        for name, lagna in results.items()
    }
