"""
Upagraha (Sub-Planet) Calculations
===================================
Implements calculations for traditional Vedic upagrahas (sub-planets).

Upagrahas are sensitive points calculated from planetary positions,
used in Vedic astrology for additional insights.

Primary Upagrahas (5):
- Dhuma (Smoke) - From Sun
- Vyatipata (Calamity) - From Sun  
- Parivesha (Halo) - From Sun
- Indrachapa (Rainbow) - From Sun
- Upaketu (Secondary Tail) - From Sun

Additional Upagrahas (5):
- Gulika (Son of Saturn) - From Saturn's portion
- Mandi (Son of Saturn) - Similar to Gulika
- Kala (Time) - From Sun
- Mrityu (Death) - From Sun
- Ardhaprahara (Half Watch) - From Sun

Reference: Brihat Parashara Hora Shastra, Chapters on Special Lagnas
"""
from typing import Dict, Tuple
from datetime import datetime
import math


class UpagrahaCalculator:
    """Calculator for upagraha (sub-planet) positions"""
    
    # Gulika timing divisions by weekday (in ghatis, 1 ghati = 24 minutes)
    # Format: (start_ghati, duration_ghati) for day and night
    GULIKA_TIMINGS = {
        0: {'day': (26, 4), 'night': (22, 4)},  # Sunday
        1: {'day': (22, 4), 'night': (18, 4)},  # Monday
        2: {'day': (18, 4), 'night': (14, 4)},  # Tuesday
        3: {'day': (14, 4), 'night': (10, 4)},  # Wednesday
        4: {'day': (10, 4), 'night': (6, 4)},   # Thursday
        5: {'day': (6, 4), 'night': (2, 4)},    # Friday
        6: {'day': (2, 4), 'night': (26, 4)},   # Saturday
    }
    
    @staticmethod
    def calculate_dhuma(sun_longitude: float) -> float:
        """
        Calculate Dhuma (Smoke) position
        Formula: Sun + 133°20' (in some texts 4 signs + 13°20')
        
        Args:
            sun_longitude: Sun's longitude in degrees
            
        Returns:
            Dhuma longitude in degrees (0-360)
        """
        dhuma = (sun_longitude + 133.333333) % 360
        return dhuma
    
    @staticmethod
    def calculate_vyatipata(dhuma_longitude: float) -> float:
        """
        Calculate Vyatipata (Calamity) position
        Formula: 360° - Dhuma
        
        Args:
            dhuma_longitude: Dhuma's longitude in degrees
            
        Returns:
            Vyatipata longitude in degrees (0-360)
        """
        vyatipata = (360 - dhuma_longitude) % 360
        return vyatipata
    
    @staticmethod
    def calculate_parivesha(vyatipata_longitude: float) -> float:
        """
        Calculate Parivesha (Halo) position
        Formula: Vyatipata + 180°
        
        Args:
            vyatipata_longitude: Vyatipata's longitude in degrees
            
        Returns:
            Parivesha longitude in degrees (0-360)
        """
        parivesha = (vyatipata_longitude + 180) % 360
        return parivesha
    
    @staticmethod
    def calculate_indrachapa(parivesha_longitude: float) -> float:
        """
        Calculate Indrachapa (Rainbow) position
        Formula: 360° - Parivesha
        
        Args:
            parivesha_longitude: Parivesha's longitude in degrees
            
        Returns:
            Indrachapa longitude in degrees (0-360)
        """
        indrachapa = (360 - parivesha_longitude) % 360
        return indrachapa
    
    @staticmethod
    def calculate_upaketu(indrachapa_longitude: float) -> float:
        """
        Calculate Upaketu (Secondary Ketu) position
        Formula: Indrachapa + 16°40'
        
        Args:
            indrachapa_longitude: Indrachapa's longitude in degrees
            
        Returns:
            Upaketu longitude in degrees (0-360)
        """
        upaketu = (indrachapa_longitude + 16.666667) % 360
        return upaketu
    
    @classmethod
    def calculate_gulika(
        cls,
        birth_datetime: datetime,
        sunrise_time: datetime,
        sunset_time: datetime,
        ascendant: float
    ) -> float:
        """
        Calculate Gulika (Son of Saturn) position
        Gulika is calculated based on birth time relative to sunrise/sunset
        
        Args:
            birth_datetime: Birth date and time
            sunrise_time: Sunrise time on birth date
            sunset_time: Sunset time on birth date
            ascendant: Ascendant degree
            
        Returns:
            Gulika longitude in degrees (0-360)
        """
        weekday = birth_datetime.weekday()  # 0 = Monday in Python
        # Adjust to Sunday = 0
        weekday = (weekday + 1) % 7
        
        # Determine if birth is during day or night
        is_day = sunrise_time <= birth_datetime <= sunset_time
        
        # Get day/night duration in minutes
        if is_day:
            day_duration = (sunset_time - sunrise_time).total_seconds() / 60
            elapsed = (birth_datetime - sunrise_time).total_seconds() / 60
            timings = cls.GULIKA_TIMINGS[weekday]['day']
        else:
            if birth_datetime < sunrise_time:
                # Night portion before sunrise
                night_start = sunset_time - timedelta(days=1)
            else:
                # Night portion after sunset
                night_start = sunset_time
            next_sunrise = sunrise_time + timedelta(days=1) if birth_datetime > sunset_time else sunrise_time
            day_duration = (next_sunrise - night_start).total_seconds() / 60
            elapsed = (birth_datetime - night_start).total_seconds() / 60
            timings = cls.GULIKA_TIMINGS[weekday]['night']
        
        # Calculate Gulika's portion
        # Each ghati = day_duration / 30 (30 ghatis in a day/night)
        ghati_duration = day_duration / 30
        gulika_start_min = timings[0] * ghati_duration
        gulika_duration_min = timings[1] * ghati_duration
        
        # If birth is during Gulika's period, use ascendant
        # Otherwise calculate based on elapsed time
        if gulika_start_min <= elapsed < (gulika_start_min + gulika_duration_min):
            gulika_longitude = ascendant
        else:
            # Calculate proportional position
            portion = (elapsed - gulika_start_min) / gulika_duration_min if gulika_duration_min > 0 else 0
            gulika_longitude = (ascendant + (portion * 30)) % 360  # Move 1 sign per gulika period
        
        return gulika_longitude
    
    @staticmethod
    def calculate_mandi(saturn_longitude: float) -> float:
        """
        Calculate Mandi (Son of Saturn) position
        Simplified formula: Saturn + 133°20' (similar to Dhuma from Sun)
        
        Args:
            saturn_longitude: Saturn's longitude in degrees
            
        Returns:
            Mandi longitude in degrees (0-360)
        """
        mandi = (saturn_longitude + 133.333333) % 360
        return mandi
    
    @staticmethod
    def calculate_kala(sun_longitude: float) -> float:
        """
        Calculate Kala (Time) position
        Formula: Sun + 220° (or 7 signs + 10°)
        
        Args:
            sun_longitude: Sun's longitude in degrees
            
        Returns:
            Kala longitude in degrees (0-360)
        """
        kala = (sun_longitude + 220) % 360
        return kala
    
    @staticmethod
    def calculate_mrityu(sun_longitude: float) -> float:
        """
        Calculate Mrityu (Death) position
        Formula: Sun + 237°30' (or 7 signs + 27°30')
        
        Args:
            sun_longitude: Sun's longitude in degrees
            
        Returns:
            Mrityu longitude in degrees (0-360)
        """
        mrityu = (sun_longitude + 237.5) % 360
        return mrityu
    
    @staticmethod
    def calculate_ardhaprahara(sun_longitude: float) -> float:
        """
        Calculate Ardhaprahara (Half Watch) position
        Formula: Sun + 255° (or 8 signs + 15°)
        
        Args:
            sun_longitude: Sun's longitude in degrees
            
        Returns:
            Ardhaprahara longitude in degrees (0-360)
        """
        ardhaprahara = (sun_longitude + 255) % 360
        return ardhaprahara
    
    @classmethod
    def calculate_all_upagrahas(
        cls,
        sun_longitude: float,
        saturn_longitude: float = None,
        birth_datetime: datetime = None,
        sunrise_time: datetime = None,
        sunset_time: datetime = None,
        ascendant: float = None
    ) -> Dict[str, float]:
        """
        Calculate all upagraha positions
        
        Args:
            sun_longitude: Sun's longitude (required)
            saturn_longitude: Saturn's longitude (for Mandi)
            birth_datetime: Birth datetime (for Gulika)
            sunrise_time: Sunrise time (for Gulika)
            sunset_time: Sunset time (for Gulika)
            ascendant: Ascendant degree (for Gulika)
            
        Returns:
            Dictionary with all upagraha longitudes
        """
        # Primary upagrahas (Sun-based)
        dhuma = cls.calculate_dhuma(sun_longitude)
        vyatipata = cls.calculate_vyatipata(dhuma)
        parivesha = cls.calculate_parivesha(vyatipata)
        indrachapa = cls.calculate_indrachapa(parivesha)
        upaketu = cls.calculate_upaketu(indrachapa)
        
        result = {
            'Dhuma': dhuma,
            'Vyatipata': vyatipata,
            'Parivesha': parivesha,
            'Indrachapa': indrachapa,
            'Upaketu': upaketu,
            'Kala': cls.calculate_kala(sun_longitude),
            'Mrityu': cls.calculate_mrityu(sun_longitude),
            'Ardhaprahara': cls.calculate_ardhaprahara(sun_longitude),
        }
        
        # Optional Saturn-based upagrahas
        if saturn_longitude is not None:
            result['Mandi'] = cls.calculate_mandi(saturn_longitude)
        
        # Optional time-based Gulika
        if all([birth_datetime, sunrise_time, sunset_time, ascendant]):
            try:
                result['Gulika'] = cls.calculate_gulika(
                    birth_datetime, sunrise_time, sunset_time, ascendant
                )
            except Exception:
                # If Gulika calculation fails, skip it
                pass
        
        return result
    
    @staticmethod
    def get_upagraha_sign(longitude: float) -> Tuple[str, int]:
        """
        Get zodiac sign and sign number for upagraha position
        
        Args:
            longitude: Longitude in degrees (0-360)
            
        Returns:
            Tuple of (sign_name, sign_number)
        """
        signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        sign_num = int(longitude / 30)
        return (signs[sign_num], sign_num + 1)
    
    @classmethod
    def format_upagraha_positions(
        cls,
        upagrahas: Dict[str, float]
    ) -> Dict[str, Dict[str, any]]:
        """
        Format upagraha positions with sign information
        
        Args:
            upagrahas: Dictionary of upagraha longitudes
            
        Returns:
            Formatted dictionary with longitude, sign, and degree info
        """
        result = {}
        for name, longitude in upagrahas.items():
            sign_name, sign_num = cls.get_upagraha_sign(longitude)
            degree_in_sign = longitude % 30
            
            result[name] = {
                'longitude': round(longitude, 6),
                'sign': sign_name,
                'sign_num': sign_num,
                'degree_in_sign': round(degree_in_sign, 6),
                'formatted': f"{sign_name} {int(degree_in_sign)}°{int((degree_in_sign % 1) * 60)}'"
            }
        
        return result


# Import fix for Gulika calculation
from datetime import timedelta
