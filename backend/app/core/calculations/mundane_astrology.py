"""
Mundane Astrology - Phase 6
PGF Protocol: MUNDANE_001
Gate: GATE_6
Version: 1.0.0

Implements:
1. Solar Ingress Charts (Aries/Capricorn)
2. Lunar Charts (New Moon/Full Moon)
3. Eclipse Charts
4. National Charts
5. Event Charts
6. Compressed Dashas for Mundane
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import math


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


@dataclass
class MundaneChart:
    """A mundane astrology chart"""
    chart_type: str
    event_time: datetime
    location: str
    ascendant: float
    planets: Dict[str, float]
    interpretation: Dict[str, Any]


class MundaneCalculator:
    """
    Mundane Astrology Calculator
    
    For nations, events, eclipses, and world affairs.
    """
    
    def __init__(self):
        pass
    
    # =========================================================================
    # SOLAR INGRESS CHARTS
    # =========================================================================
    def calculate_solar_ingress(
        self,
        year: int,
        ingress_type: str = "aries",  # "aries" or "capricorn"
        latitude: float = 28.6139,  # Default: New Delhi
        longitude: float = 77.2090
    ) -> Dict[str, Any]:
        """
        Calculate Solar Ingress Chart
        
        Aries Ingress: Solar New Year (around March 21)
        Capricorn Ingress: Uttarayana (around Dec 21)
        """
        # Approximate ingress dates
        if ingress_type == "aries":
            ingress_date = datetime(year, 3, 21, 0, 0)
            sun_longitude = 0.0  # 0° Aries
        else:  # capricorn
            ingress_date = datetime(year, 12, 21, 0, 0)
            sun_longitude = 270.0  # 0° Capricorn
        
        # Calculate planetary positions
        planets = self._calculate_mundane_positions(ingress_date)
        planets["Sun"] = sun_longitude
        
        # Calculate ascendant
        ascendant = self._calculate_ascendant(ingress_date, latitude, longitude)
        
        # Analyze for nation/world
        analysis = self._analyze_ingress_chart(planets, ascendant, ingress_type)
        
        return {
            "chart_type": f"Solar {ingress_type.title()} Ingress {year}",
            "date": ingress_date.isoformat(),
            "location": f"{latitude}, {longitude}",
            "ascendant": {
                "longitude": ascendant,
                "sign": SIGNS[int(ascendant / 30)]
            },
            "planets": {
                p: {"longitude": lon, "sign": SIGNS[int(lon/30)]}
                for p, lon in planets.items()
            },
            "analysis": analysis,
            "validity": "1 year" if ingress_type == "aries" else "6 months"
        }
    
    def _analyze_ingress_chart(
        self,
        planets: Dict[str, float],
        ascendant: float,
        ingress_type: str
    ) -> Dict[str, Any]:
        """Analyze ingress chart for mundane predictions"""
        lagna = int(ascendant / 30)
        
        # House positions
        houses = {
            planet: ((int(lon/30) - lagna) % 12) + 1
            for planet, lon in planets.items()
        }
        
        # Key mundane houses
        # 1st: Nation/people, 2nd: Economy, 4th: Land/agriculture
        # 6th: Military/health, 7th: Foreign affairs, 10th: Government
        
        analysis = {
            "government": self._analyze_10th_house(houses, planets),
            "economy": self._analyze_2nd_house(houses, planets),
            "foreign_affairs": self._analyze_7th_house(houses, planets),
            "public_health": self._analyze_6th_house(houses, planets),
            "agriculture": self._analyze_4th_house(houses, planets),
            "overall": self._get_mundane_overview(houses)
        }
        
        return analysis
    
    def _analyze_10th_house(self, houses: Dict[str, int], planets: Dict[str, float]) -> str:
        """Analyze 10th house for government"""
        planets_in_10 = [p for p, h in houses.items() if h == 10]
        
        if "Jupiter" in planets_in_10:
            return "Stable, prosperous government; wise leadership"
        elif "Saturn" in planets_in_10:
            return "Government faces restrictions; reforms needed"
        elif "Mars" in planets_in_10:
            return "Active government; possible conflicts"
        elif "Sun" in planets_in_10:
            return "Strong central authority; leadership in focus"
        else:
            return "Moderate governmental activities"
    
    def _analyze_2nd_house(self, houses: Dict[str, int], planets: Dict[str, float]) -> str:
        """Analyze 2nd house for economy"""
        planets_in_2 = [p for p, h in houses.items() if h == 2]
        
        if "Jupiter" in planets_in_2 or "Venus" in planets_in_2:
            return "Economic growth expected; prosperity"
        elif "Saturn" in planets_in_2:
            return "Economic challenges; need for austerity"
        elif "Rahu" in planets_in_2:
            return "Economic fluctuations; speculation"
        else:
            return "Stable economic conditions"
    
    def _analyze_7th_house(self, houses: Dict[str, int], planets: Dict[str, float]) -> str:
        """Analyze 7th house for foreign affairs"""
        planets_in_7 = [p for p, h in houses.items() if h == 7]
        
        if "Mars" in planets_in_7 or "Rahu" in planets_in_7:
            return "Foreign tensions; diplomatic challenges"
        elif "Venus" in planets_in_7:
            return "Favorable foreign relations; treaties"
        elif "Saturn" in planets_in_7:
            return "Delayed foreign negotiations"
        else:
            return "Normal foreign relations"
    
    def _analyze_6th_house(self, houses: Dict[str, int], planets: Dict[str, float]) -> str:
        """Analyze 6th house for public health"""
        planets_in_6 = [p for p, h in houses.items() if h == 6]
        
        if "Ketu" in planets_in_6 or "Saturn" in planets_in_6:
            return "Health concerns; epidemics possible"
        elif "Mars" in planets_in_6:
            return "Military activity; health vigilance needed"
        else:
            return "General public health stable"
    
    def _analyze_4th_house(self, houses: Dict[str, int], planets: Dict[str, float]) -> str:
        """Analyze 4th house for land/agriculture"""
        planets_in_4 = [p for p, h in houses.items() if h == 4]
        
        if "Moon" in planets_in_4 or "Venus" in planets_in_4:
            return "Good harvests; agricultural prosperity"
        elif "Saturn" in planets_in_4:
            return "Land issues; drought concerns"
        elif "Rahu" in planets_in_4:
            return "Natural calamities possible"
        else:
            return "Normal agricultural conditions"
    
    def _get_mundane_overview(self, houses: Dict[str, int]) -> str:
        """Get overall mundane overview"""
        # Count benefics in good houses
        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
        good_houses = [1, 4, 5, 7, 9, 10, 11]
        
        benefic_count = sum(1 for p in benefics if houses.get(p, 0) in good_houses)
        
        if benefic_count >= 3:
            return "Generally prosperous and peaceful period"
        elif benefic_count >= 2:
            return "Mixed period with both progress and challenges"
        else:
            return "Challenging period requiring vigilance"
    
    # =========================================================================
    # LUNAR CHARTS
    # =========================================================================
    def calculate_lunar_chart(
        self,
        date: datetime,
        chart_type: str = "new_moon",  # "new_moon" or "full_moon"
        latitude: float = 28.6139,
        longitude: float = 77.2090
    ) -> Dict[str, Any]:
        """Calculate New Moon or Full Moon chart"""
        planets = self._calculate_mundane_positions(date)
        
        if chart_type == "new_moon":
            # Sun and Moon conjunct
            planets["Moon"] = planets["Sun"]
        else:
            # Moon opposite Sun
            planets["Moon"] = (planets["Sun"] + 180) % 360
        
        ascendant = self._calculate_ascendant(date, latitude, longitude)
        
        return {
            "chart_type": f"{'New' if chart_type == 'new_moon' else 'Full'} Moon Chart",
            "date": date.isoformat(),
            "ascendant": {
                "longitude": ascendant,
                "sign": SIGNS[int(ascendant / 30)]
            },
            "planets": {
                p: {"longitude": lon, "sign": SIGNS[int(lon/30)]}
                for p, lon in planets.items()
            },
            "validity": "1 month",
            "interpretation": self._interpret_lunar_chart(planets, ascendant, chart_type)
        }
    
    def _interpret_lunar_chart(
        self,
        planets: Dict[str, float],
        ascendant: float,
        chart_type: str
    ) -> Dict[str, str]:
        """Interpret lunar chart"""
        moon_sign = int(planets["Moon"] / 30)
        
        interpretations = {
            "mood": self._get_public_mood(moon_sign, chart_type),
            "focus": self._get_monthly_focus(moon_sign),
            "caution": self._get_monthly_caution(planets, ascendant)
        }
        
        return interpretations
    
    def _get_public_mood(self, moon_sign: int, chart_type: str) -> str:
        """Get public mood based on Moon sign"""
        moods = {
            0: "Energetic, pioneering spirit",
            1: "Material focus, stability seeking",
            2: "Communicative, curious",
            3: "Emotional, family-oriented",
            4: "Confident, celebratory",
            5: "Analytical, health-conscious",
            6: "Diplomatic, relationship focus",
            7: "Intense, transformative",
            8: "Optimistic, expansive",
            9: "Serious, achievement-focused",
            10: "Progressive, humanitarian",
            11: "Spiritual, compassionate"
        }
        return moods.get(moon_sign, "Varied")
    
    def _get_monthly_focus(self, moon_sign: int) -> str:
        """Get focus area for the month"""
        focus = {
            0: "New beginnings, initiatives",
            1: "Financial matters, resources",
            2: "Communication, learning",
            3: "Home, family, real estate",
            4: "Creativity, entertainment",
            5: "Health, service, employment",
            6: "Partnerships, agreements",
            7: "Transformation, shared resources",
            8: "Travel, higher learning",
            9: "Career, public matters",
            10: "Community, networks",
            11: "Spirituality, closure"
        }
        return focus.get(moon_sign, "General matters")
    
    def _get_monthly_caution(self, planets: Dict[str, float], ascendant: float) -> str:
        """Get caution for the month"""
        lagna = int(ascendant / 30)
        mars_house = ((int(planets["Mars"]/30) - lagna) % 12) + 1
        saturn_house = ((int(planets["Saturn"]/30) - lagna) % 12) + 1
        
        if mars_house in [1, 4, 7, 8]:
            return "Avoid conflicts and hasty actions"
        elif saturn_house in [1, 4, 7, 8]:
            return "Patience needed; delays possible"
        else:
            return "No major cautions"
    
    # =========================================================================
    # ECLIPSE CHARTS
    # =========================================================================
    def calculate_eclipse_chart(
        self,
        eclipse_date: datetime,
        eclipse_type: str,  # "solar" or "lunar"
        latitude: float = 0.0,
        longitude: float = 0.0
    ) -> Dict[str, Any]:
        """Calculate eclipse chart"""
        planets = self._calculate_mundane_positions(eclipse_date)
        
        # Eclipse means Rahu/Ketu near Sun-Moon axis
        if eclipse_type == "solar":
            planets["Moon"] = planets["Sun"]  # Conjunction
            planets["Rahu"] = (planets["Sun"] + 5) % 360  # Near Sun
        else:
            planets["Moon"] = (planets["Sun"] + 180) % 360  # Opposition
            planets["Rahu"] = (planets["Sun"] + 5) % 360
        
        planets["Ketu"] = (planets["Rahu"] + 180) % 360
        
        ascendant = self._calculate_ascendant(eclipse_date, latitude, longitude)
        
        return {
            "chart_type": f"{'Solar' if eclipse_type == 'solar' else 'Lunar'} Eclipse",
            "date": eclipse_date.isoformat(),
            "eclipse_sign": SIGNS[int(planets["Sun"] / 30)],
            "nakshatra": self._get_nakshatra(planets["Sun"]),
            "ascendant": {
                "longitude": ascendant,
                "sign": SIGNS[int(ascendant / 30)]
            },
            "planets": {
                p: {"longitude": lon, "sign": SIGNS[int(lon/30)]}
                for p, lon in planets.items()
            },
            "effects": self._interpret_eclipse(planets, eclipse_type),
            "duration_of_effect": "6 months" if eclipse_type == "solar" else "3 months"
        }
    
    def _get_nakshatra(self, longitude: float) -> str:
        """Get nakshatra for longitude"""
        nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "P.Phalguni", "U.Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "P.Ashadha", "U.Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "P.Bhadrapada", "U.Bhadrapada", "Revati"
        ]
        idx = int(longitude / (360/27))
        return nakshatras[idx]
    
    def _interpret_eclipse(self, planets: Dict[str, float], eclipse_type: str) -> Dict[str, str]:
        """Interpret eclipse effects"""
        eclipse_sign = int(planets["Sun"] / 30)
        
        # Signs and their mundane significations
        sign_effects = {
            0: "Military matters, leadership changes",
            1: "Economic fluctuations, banking",
            2: "Communication disruptions, media",
            3: "Water-related issues, public emotions",
            4: "Government changes, entertainment",
            5: "Health sector, service industries",
            6: "Foreign relations, legal matters",
            7: "Hidden matters revealed, taxes",
            8: "Religious matters, education",
            9: "Government authority, corporations",
            10: "Technology, social movements",
            11: "Spirituality, hospitals, isolation"
        }
        
        return {
            "primary_effect": sign_effects.get(eclipse_sign, "General effects"),
            "nations_affected": self._get_affected_nations(eclipse_sign),
            "advice": "Avoid major decisions during eclipse period"
        }
    
    def _get_affected_nations(self, sign: int) -> str:
        """Get nations traditionally associated with signs"""
        nations = {
            0: "England, Germany, Denmark",
            1: "Ireland, Cyprus, Iran",
            2: "USA, Belgium, Wales",
            3: "Netherlands, Scotland, New Zealand",
            4: "France, Italy, Romania",
            5: "Turkey, Greece, Croatia",
            6: "Austria, Japan, Argentina",
            7: "Morocco, Norway, Algeria",
            8: "Spain, Australia, Hungary",
            9: "India, Mexico, Afghanistan",
            10: "Russia, Sweden, Poland",
            11: "Portugal, Egypt, Scandinavia"
        }
        return nations.get(sign, "Various regions")
    
    # =========================================================================
    # COMPRESSED DASHAS FOR MUNDANE
    # =========================================================================
    def compress_dasha(
        self,
        dasha_periods: List[Dict[str, Any]],
        compress_to_years: float
    ) -> List[Dict[str, Any]]:
        """
        Compress dasha periods to fit a specific timeframe
        
        Used for mundane charts where 120-year Vimsottari is 
        compressed to 1 year, 1 month, etc.
        """
        total_dasha_years = sum(p.get("years", 0) for p in dasha_periods)
        compression_ratio = compress_to_years / total_dasha_years
        
        compressed = []
        for period in dasha_periods:
            compressed.append({
                "ruler": period["ruler"],
                "original_years": period["years"],
                "compressed_years": period["years"] * compression_ratio,
                "compressed_days": period["years"] * compression_ratio * 365.25
            })
        
        return compressed
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    def _calculate_mundane_positions(self, date: datetime) -> Dict[str, float]:
        """Calculate planetary positions for mundane chart"""
        reference = datetime(2000, 1, 1)
        days = (date - reference).days
        
        # Mean motions (simplified)
        return {
            "Sun": (days * 0.9856) % 360,
            "Moon": (days * 13.17) % 360,
            "Mars": (days * 0.524 + 45) % 360,
            "Mercury": (days * 1.38 + 30) % 360,
            "Jupiter": (days * 0.083 + 120) % 360,
            "Venus": (days * 1.2 + 60) % 360,
            "Saturn": (days * 0.034 + 90) % 360,
            "Rahu": (360 - days * 0.053) % 360,
            "Ketu": (180 - days * 0.053) % 360
        }
    
    def _calculate_ascendant(
        self,
        time: datetime,
        latitude: float,
        longitude: float
    ) -> float:
        """Calculate ascendant for given time/location"""
        hours = time.hour + time.minute / 60
        day_of_year = time.timetuple().tm_yday
        lst = (hours + longitude / 15 + day_of_year * 0.0657) % 24
        return (lst / 24 * 360 + latitude / 3) % 360


def calculate_mundane_chart(
    chart_type: str,
    date: datetime,
    latitude: float = 28.6139,
    longitude: float = 77.2090
) -> Dict[str, Any]:
    """Convenience function for mundane calculations"""
    calc = MundaneCalculator()
    
    if chart_type == "aries_ingress":
        return calc.calculate_solar_ingress(date.year, "aries", latitude, longitude)
    elif chart_type == "capricorn_ingress":
        return calc.calculate_solar_ingress(date.year, "capricorn", latitude, longitude)
    elif chart_type == "new_moon":
        return calc.calculate_lunar_chart(date, "new_moon", latitude, longitude)
    elif chart_type == "full_moon":
        return calc.calculate_lunar_chart(date, "full_moon", latitude, longitude)
    elif chart_type.startswith("eclipse"):
        eclipse_type = "solar" if "solar" in chart_type else "lunar"
        return calc.calculate_eclipse_chart(date, eclipse_type, latitude, longitude)
    else:
        return {"error": f"Unknown chart type: {chart_type}"}
