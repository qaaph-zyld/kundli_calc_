"""
Panchang (Hindu Calendar) & Muhurta Calculator
PGF Protocol: PANCHANG_001
Gate: GATE_5
Version: 1.0.0

Complete implementation of:
- Tithi (Lunar Day)
- Nakshatra (Lunar Mansion)
- Yoga (Sun-Moon combination)
- Karana (Half-Tithi)
- Vara (Weekday)
- Rahu Kalam, Yamagandam, Gulika Kalam
- Abhijit Muhurta
- Brahma Muhurta
- Choghadiya
- Hora
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import math


# Constants
TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury"
]

YOGA_NAMES = [
    "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti"
]

YOGA_QUALITY = [
    "malefic", "benefic", "benefic", "benefic", "benefic",
    "malefic", "benefic", "benefic", "malefic", "malefic",
    "benefic", "benefic", "malefic", "benefic", "benefic",
    "benefic", "malefic", "benefic", "malefic", "benefic",
    "benefic", "benefic", "benefic", "benefic", "benefic",
    "benefic", "malefic"
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Gara",
    "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
]

WEEKDAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
WEEKDAY_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Rahu Kalam order for each day (segments 1-8)
RAHU_KALAM = [8, 2, 7, 5, 6, 4, 3]  # Sun=8th, Mon=2nd, etc.
YAMAGANDAM = [5, 4, 3, 2, 1, 7, 6]
GULIKA_KALAM = [7, 6, 5, 4, 3, 2, 1]


class MuhurtaQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    MODERATE = "moderate"
    AVOID = "avoid"
    INAUSPICIOUS = "inauspicious"


@dataclass
class PanchangData:
    """Complete Panchang for a given moment"""
    datetime: datetime
    weekday: str
    weekday_lord: str
    tithi: str
    tithi_number: int
    tithi_paksha: str  # Shukla or Krishna
    nakshatra: str
    nakshatra_lord: str
    nakshatra_pada: int
    yoga: str
    yoga_quality: str
    karana: str
    sunrise: datetime
    sunset: datetime
    moon_sign: str
    sun_sign: str


@dataclass
class MuhurtaWindow:
    """A muhurta time window"""
    name: str
    start: datetime
    end: datetime
    quality: MuhurtaQuality
    suitable_for: List[str]
    avoid_for: List[str]
    notes: str


class PanchangCalculator:
    """
    Complete Panchang Calculator
    """
    
    def __init__(self):
        pass
    
    def calculate_panchang(
        self,
        date_time: datetime,
        sun_longitude: float,
        moon_longitude: float,
        latitude: float = 28.6139,  # Default: Delhi
        longitude: float = 77.2090
    ) -> PanchangData:
        """
        Calculate complete Panchang for a given moment
        
        Args:
            date_time: Date and time
            sun_longitude: Sun's longitude
            moon_longitude: Moon's longitude
            latitude: Location latitude
            longitude: Location longitude
            
        Returns:
            Complete Panchang data
        """
        # Weekday
        weekday_idx = date_time.weekday()
        # Python weekday: Mon=0, but we want Sun=0
        weekday_idx = (weekday_idx + 1) % 7
        weekday = WEEKDAY_NAMES[weekday_idx]
        weekday_lord = WEEKDAY_LORDS[weekday_idx]
        
        # Tithi
        tithi_info = self._calculate_tithi(sun_longitude, moon_longitude)
        
        # Nakshatra
        nakshatra_info = self._calculate_nakshatra(moon_longitude)
        
        # Yoga
        yoga_info = self._calculate_yoga(sun_longitude, moon_longitude)
        
        # Karana
        karana = self._calculate_karana(tithi_info['number'])
        
        # Sunrise/Sunset (simplified calculation)
        sunrise, sunset = self._calculate_sun_times(date_time, latitude, longitude)
        
        # Signs
        moon_sign = self._get_sign_name(moon_longitude)
        sun_sign = self._get_sign_name(sun_longitude)
        
        return PanchangData(
            datetime=date_time,
            weekday=weekday,
            weekday_lord=weekday_lord,
            tithi=tithi_info['name'],
            tithi_number=tithi_info['number'],
            tithi_paksha=tithi_info['paksha'],
            nakshatra=nakshatra_info['name'],
            nakshatra_lord=nakshatra_info['lord'],
            nakshatra_pada=nakshatra_info['pada'],
            yoga=yoga_info['name'],
            yoga_quality=yoga_info['quality'],
            karana=karana,
            sunrise=sunrise,
            sunset=sunset,
            moon_sign=moon_sign,
            sun_sign=sun_sign
        )
    
    def _calculate_tithi(self, sun_lon: float, moon_lon: float) -> Dict:
        """Calculate Tithi (lunar day)"""
        # Tithi = (Moon - Sun) / 12
        diff = (moon_lon - sun_lon + 360) % 360
        tithi_num = int(diff / 12) + 1
        
        if tithi_num > 30:
            tithi_num = 30
        
        paksha = "Shukla" if tithi_num <= 15 else "Krishna"
        tithi_name = TITHI_NAMES[tithi_num - 1]
        
        return {
            'number': tithi_num,
            'name': tithi_name,
            'paksha': paksha,
            'remaining_degrees': 12 - (diff % 12)
        }
    
    def _calculate_nakshatra(self, moon_lon: float) -> Dict:
        """Calculate Nakshatra and Pada"""
        nakshatra_span = 360 / 27
        nakshatra_idx = int(moon_lon / nakshatra_span)
        position_in_nak = moon_lon % nakshatra_span
        pada = int(position_in_nak / (nakshatra_span / 4)) + 1
        
        return {
            'name': NAKSHATRA_NAMES[nakshatra_idx],
            'lord': NAKSHATRA_LORDS[nakshatra_idx],
            'pada': pada,
            'index': nakshatra_idx
        }
    
    def _calculate_yoga(self, sun_lon: float, moon_lon: float) -> Dict:
        """Calculate Yoga (Sun + Moon combination)"""
        # Yoga = (Sun + Moon) / (360/27)
        combined = (sun_lon + moon_lon) % 360
        yoga_idx = int(combined / (360 / 27))
        
        return {
            'name': YOGA_NAMES[yoga_idx],
            'quality': YOGA_QUALITY[yoga_idx],
            'index': yoga_idx
        }
    
    def _calculate_karana(self, tithi_num: int) -> str:
        """Calculate Karana (half-tithi)"""
        # Each tithi has 2 karanas
        # First 7 karanas repeat, last 4 are fixed
        karana_num = (tithi_num * 2 - 1) % 60
        
        if karana_num <= 7:
            return KARANA_NAMES[(karana_num - 1) % 7]
        else:
            # Fixed karanas at specific points
            fixed_karanas = {57: "Shakuni", 58: "Chatushpada", 59: "Naga", 60: "Kimstughna"}
            return fixed_karanas.get(karana_num, KARANA_NAMES[(karana_num - 1) % 7])
    
    def _calculate_sun_times(
        self,
        date: datetime,
        lat: float,
        lon: float
    ) -> Tuple[datetime, datetime]:
        """Simplified sunrise/sunset calculation"""
        # Approximate calculation
        # For accurate results, use Swiss Ephemeris
        day_of_year = date.timetuple().tm_yday
        
        # Approximate sunrise at 6 AM, sunset at 6 PM
        # Adjust based on latitude and season
        base_sunrise = 6.0
        base_sunset = 18.0
        
        # Seasonal adjustment (simplified)
        seasonal_adj = math.sin((day_of_year - 80) * 2 * math.pi / 365) * 1.5
        
        sunrise_hour = base_sunrise - seasonal_adj
        sunset_hour = base_sunset + seasonal_adj
        
        sunrise = date.replace(
            hour=int(sunrise_hour),
            minute=int((sunrise_hour % 1) * 60),
            second=0
        )
        sunset = date.replace(
            hour=int(sunset_hour),
            minute=int((sunset_hour % 1) * 60),
            second=0
        )
        
        return sunrise, sunset
    
    def _get_sign_name(self, longitude: float) -> str:
        """Get zodiac sign name from longitude"""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return signs[int(longitude / 30)]


class MuhurtaCalculator:
    """
    Muhurta (Auspicious Time) Calculator
    """
    
    def __init__(self):
        self.panchang_calc = PanchangCalculator()
    
    def get_rahu_kalam(
        self,
        date: datetime,
        sunrise: datetime,
        sunset: datetime
    ) -> Tuple[datetime, datetime]:
        """
        Calculate Rahu Kalam (inauspicious period)
        
        Rahu Kalam is 1/8th of the day, position varies by weekday
        """
        weekday = (date.weekday() + 1) % 7  # Sun=0
        segment = RAHU_KALAM[weekday]
        
        day_duration = (sunset - sunrise).total_seconds()
        segment_duration = day_duration / 8
        
        start = sunrise + timedelta(seconds=(segment - 1) * segment_duration)
        end = start + timedelta(seconds=segment_duration)
        
        return start, end
    
    def get_yamagandam(
        self,
        date: datetime,
        sunrise: datetime,
        sunset: datetime
    ) -> Tuple[datetime, datetime]:
        """Calculate Yamagandam (inauspicious period)"""
        weekday = (date.weekday() + 1) % 7
        segment = YAMAGANDAM[weekday]
        
        day_duration = (sunset - sunrise).total_seconds()
        segment_duration = day_duration / 8
        
        start = sunrise + timedelta(seconds=(segment - 1) * segment_duration)
        end = start + timedelta(seconds=segment_duration)
        
        return start, end
    
    def get_gulika_kalam(
        self,
        date: datetime,
        sunrise: datetime,
        sunset: datetime
    ) -> Tuple[datetime, datetime]:
        """Calculate Gulika Kalam (Saturn's period)"""
        weekday = (date.weekday() + 1) % 7
        segment = GULIKA_KALAM[weekday]
        
        day_duration = (sunset - sunrise).total_seconds()
        segment_duration = day_duration / 8
        
        start = sunrise + timedelta(seconds=(segment - 1) * segment_duration)
        end = start + timedelta(seconds=segment_duration)
        
        return start, end
    
    def get_abhijit_muhurta(
        self,
        sunrise: datetime,
        sunset: datetime
    ) -> Tuple[datetime, datetime]:
        """
        Calculate Abhijit Muhurta
        
        The most auspicious muhurta, occurs around midday
        8th muhurta of the day (out of 15 day muhurtas)
        """
        day_duration = (sunset - sunrise).total_seconds()
        muhurta_duration = day_duration / 15
        
        # Abhijit is the 8th muhurta
        start = sunrise + timedelta(seconds=7 * muhurta_duration)
        end = start + timedelta(seconds=muhurta_duration)
        
        return start, end
    
    def get_brahma_muhurta(
        self,
        sunrise: datetime
    ) -> Tuple[datetime, datetime]:
        """
        Calculate Brahma Muhurta
        
        Auspicious pre-dawn period, ~1.5 hours before sunrise
        """
        end = sunrise
        start = sunrise - timedelta(hours=1, minutes=36)  # 96 minutes
        
        return start, end
    
    def get_choghadiya(
        self,
        date: datetime,
        sunrise: datetime,
        sunset: datetime
    ) -> List[Dict]:
        """
        Calculate Choghadiya periods
        
        7 types of choghadiyas, each ~1.5 hours
        """
        choghadiya_types = [
            ("Udveg", "avoid", "Mars"),
            ("Char", "good", "Venus"),
            ("Labh", "excellent", "Mercury"),
            ("Amrit", "excellent", "Moon"),
            ("Kaal", "avoid", "Saturn"),
            ("Shubh", "good", "Jupiter"),
            ("Rog", "avoid", "Sun")
        ]
        
        # Order varies by weekday
        weekday_order = [
            [0, 1, 2, 3, 4, 5, 6, 0],  # Sunday
            [3, 4, 5, 6, 0, 1, 2, 3],  # Monday
            [6, 0, 1, 2, 3, 4, 5, 6],  # Tuesday
            [1, 2, 3, 4, 5, 6, 0, 1],  # Wednesday
            [5, 6, 0, 1, 2, 3, 4, 5],  # Thursday
            [2, 3, 4, 5, 6, 0, 1, 2],  # Friday
            [4, 5, 6, 0, 1, 2, 3, 4]   # Saturday
        ]
        
        weekday = (date.weekday() + 1) % 7
        order = weekday_order[weekday]
        
        day_duration = (sunset - sunrise).total_seconds()
        chog_duration = day_duration / 8
        
        choghadiyas = []
        for i, type_idx in enumerate(order):
            name, quality, lord = choghadiya_types[type_idx]
            start = sunrise + timedelta(seconds=i * chog_duration)
            end = start + timedelta(seconds=chog_duration)
            
            choghadiyas.append({
                "name": name,
                "quality": quality,
                "lord": lord,
                "start": start.strftime("%H:%M"),
                "end": end.strftime("%H:%M"),
                "period": i + 1
            })
        
        return choghadiyas
    
    def get_hora(
        self,
        date_time: datetime,
        sunrise: datetime
    ) -> Dict:
        """
        Calculate current Hora (planetary hour)
        
        Each hour is ruled by a planet, starting from weekday lord at sunrise
        """
        hora_order = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
        
        weekday = (date_time.weekday() + 1) % 7
        start_planet_idx = hora_order.index(WEEKDAY_LORDS[weekday])
        
        hours_from_sunrise = (date_time - sunrise).total_seconds() / 3600
        hora_num = int(hours_from_sunrise) % 24
        
        current_hora_idx = (start_planet_idx + hora_num) % 7
        current_hora = hora_order[current_hora_idx]
        
        # Quality based on planet
        quality_map = {
            "Jupiter": "excellent",
            "Venus": "good",
            "Mercury": "good",
            "Moon": "good",
            "Sun": "moderate",
            "Mars": "avoid",
            "Saturn": "avoid"
        }
        
        return {
            "planet": current_hora,
            "quality": quality_map[current_hora],
            "hora_number": hora_num + 1,
            "suitable_for": self._get_hora_activities(current_hora)
        }
    
    def _get_hora_activities(self, planet: str) -> List[str]:
        """Get suitable activities for a hora"""
        activities = {
            "Sun": ["Government work", "Authority matters", "Health"],
            "Moon": ["Travel", "Public dealings", "Domestic"],
            "Mars": ["Competition", "Surgery", "Courage-based"],
            "Mercury": ["Business", "Communication", "Learning"],
            "Jupiter": ["Religious", "Education", "Legal", "Marriage"],
            "Venus": ["Arts", "Romance", "Luxury", "Entertainment"],
            "Saturn": ["Property", "Agriculture", "Delayed work"]
        }
        return activities.get(planet, [])
    
    def find_good_muhurtas(
        self,
        date: datetime,
        activity: str,
        panchang: PanchangData
    ) -> List[MuhurtaWindow]:
        """
        Find good muhurtas for a specific activity on a given day
        """
        muhurtas = []
        
        # Abhijit Muhurta - good for almost everything
        abhijit_start, abhijit_end = self.get_abhijit_muhurta(
            panchang.sunrise, panchang.sunset
        )
        muhurtas.append(MuhurtaWindow(
            name="Abhijit Muhurta",
            start=abhijit_start,
            end=abhijit_end,
            quality=MuhurtaQuality.EXCELLENT,
            suitable_for=["All auspicious activities", "New beginnings"],
            avoid_for=["Nothing - universally auspicious"],
            notes="Best muhurta of the day, except on Wednesday"
        ))
        
        # Brahma Muhurta - for spiritual activities
        brahma_start, brahma_end = self.get_brahma_muhurta(panchang.sunrise)
        muhurtas.append(MuhurtaWindow(
            name="Brahma Muhurta",
            start=brahma_start,
            end=brahma_end,
            quality=MuhurtaQuality.EXCELLENT,
            suitable_for=["Meditation", "Study", "Spiritual practices"],
            avoid_for=["Material activities"],
            notes="Pre-dawn auspicious period"
        ))
        
        # Add choghadiya-based muhurtas
        choghadiyas = self.get_choghadiya(
            date, panchang.sunrise, panchang.sunset
        )
        for chog in choghadiyas:
            if chog["quality"] in ["excellent", "good"]:
                muhurtas.append(MuhurtaWindow(
                    name=f"{chog['name']} Choghadiya",
                    start=datetime.strptime(chog["start"], "%H:%M").replace(
                        year=date.year, month=date.month, day=date.day
                    ),
                    end=datetime.strptime(chog["end"], "%H:%M").replace(
                        year=date.year, month=date.month, day=date.day
                    ),
                    quality=MuhurtaQuality.EXCELLENT if chog["quality"] == "excellent" else MuhurtaQuality.GOOD,
                    suitable_for=self._get_choghadiya_activities(chog["name"]),
                    avoid_for=[],
                    notes=f"Ruled by {chog['lord']}"
                ))
        
        return muhurtas
    
    def _get_choghadiya_activities(self, name: str) -> List[str]:
        """Get suitable activities for a choghadiya"""
        activities = {
            "Amrit": ["All auspicious work", "Marriage", "Business start"],
            "Labh": ["Business", "Finance", "Gains"],
            "Shubh": ["Auspicious work", "Religious ceremonies"],
            "Char": ["Travel", "Movement", "Short journeys"]
        }
        return activities.get(name, [])
    
    def get_inauspicious_times(
        self,
        date: datetime,
        sunrise: datetime,
        sunset: datetime
    ) -> Dict:
        """Get all inauspicious times for the day"""
        rahu_start, rahu_end = self.get_rahu_kalam(date, sunrise, sunset)
        yama_start, yama_end = self.get_yamagandam(date, sunrise, sunset)
        gulika_start, gulika_end = self.get_gulika_kalam(date, sunrise, sunset)
        
        return {
            "rahu_kalam": {
                "start": rahu_start.strftime("%H:%M"),
                "end": rahu_end.strftime("%H:%M"),
                "avoid": "All new beginnings, auspicious work"
            },
            "yamagandam": {
                "start": yama_start.strftime("%H:%M"),
                "end": yama_end.strftime("%H:%M"),
                "avoid": "Important decisions, travel"
            },
            "gulika_kalam": {
                "start": gulika_start.strftime("%H:%M"),
                "end": gulika_end.strftime("%H:%M"),
                "avoid": "Medicine, health matters"
            }
        }


def get_daily_panchang(
    date_time: datetime,
    sun_lon: float,
    moon_lon: float,
    latitude: float = 28.6139,
    longitude: float = 77.2090
) -> Dict[str, Any]:
    """
    Get complete daily Panchang with muhurtas
    """
    panchang_calc = PanchangCalculator()
    muhurta_calc = MuhurtaCalculator()
    
    panchang = panchang_calc.calculate_panchang(
        date_time, sun_lon, moon_lon, latitude, longitude
    )
    
    inauspicious = muhurta_calc.get_inauspicious_times(
        date_time, panchang.sunrise, panchang.sunset
    )
    
    choghadiyas = muhurta_calc.get_choghadiya(
        date_time, panchang.sunrise, panchang.sunset
    )
    
    hora = muhurta_calc.get_hora(date_time, panchang.sunrise)
    
    abhijit = muhurta_calc.get_abhijit_muhurta(panchang.sunrise, panchang.sunset)
    brahma = muhurta_calc.get_brahma_muhurta(panchang.sunrise)
    
    return {
        "date": date_time.strftime("%Y-%m-%d"),
        "weekday": panchang.weekday,
        "weekday_lord": panchang.weekday_lord,
        "tithi": {
            "name": panchang.tithi,
            "number": panchang.tithi_number,
            "paksha": panchang.tithi_paksha
        },
        "nakshatra": {
            "name": panchang.nakshatra,
            "lord": panchang.nakshatra_lord,
            "pada": panchang.nakshatra_pada
        },
        "yoga": {
            "name": panchang.yoga,
            "quality": panchang.yoga_quality
        },
        "karana": panchang.karana,
        "moon_sign": panchang.moon_sign,
        "sun_sign": panchang.sun_sign,
        "sunrise": panchang.sunrise.strftime("%H:%M"),
        "sunset": panchang.sunset.strftime("%H:%M"),
        "inauspicious_times": inauspicious,
        "choghadiyas": choghadiyas,
        "current_hora": hora,
        "special_muhurtas": {
            "abhijit": {
                "start": abhijit[0].strftime("%H:%M"),
                "end": abhijit[1].strftime("%H:%M"),
                "quality": "excellent"
            },
            "brahma": {
                "start": brahma[0].strftime("%H:%M"),
                "end": brahma[1].strftime("%H:%M"),
                "quality": "excellent"
            }
        }
    }
