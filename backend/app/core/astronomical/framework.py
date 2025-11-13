"""
Astronomical Data Framework
PGF Protocol: AST_001
Gate: GATE_15
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union
from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass
import math
from pydantic import BaseModel, Field
import swisseph as swe
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)

class CelestialBody(str, Enum):
    """Celestial bodies"""
    SUN = "sun"
    MOON = "moon"
    MARS = "mars"
    MERCURY = "mercury"
    JUPITER = "jupiter"
    VENUS = "venus"
    SATURN = "saturn"
    RAHU = "rahu"  # North Node
    KETU = "ketu"  # South Node
    URANUS = "uranus"
    NEPTUNE = "neptune"
    PLUTO = "pluto"

class ZodiacSign(str, Enum):
    """Zodiac signs"""
    ARIES = "aries"
    TAURUS = "taurus"
    GEMINI = "gemini"
    CANCER = "cancer"
    LEO = "leo"
    VIRGO = "virgo"
    LIBRA = "libra"
    SCORPIO = "scorpio"
    SAGITTARIUS = "sagittarius"
    CAPRICORN = "capricorn"
    AQUARIUS = "aquarius"
    PISCES = "pisces"

class House(str, Enum):
    """Astrological houses"""
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"
    FOURTH = "fourth"
    FIFTH = "fifth"
    SIXTH = "sixth"
    SEVENTH = "seventh"
    EIGHTH = "eighth"
    NINTH = "ninth"
    TENTH = "tenth"
    ELEVENTH = "eleventh"
    TWELFTH = "twelfth"

class Aspect(str, Enum):
    """Planetary aspects"""
    CONJUNCTION = "conjunction"  # 0°
    SEXTILE = "sextile"  # 60°
    SQUARE = "square"  # 90°
    TRINE = "trine"  # 120°
    OPPOSITION = "opposition"  # 180°

class CoordinateSystem(str, Enum):
    """Coordinate systems"""
    GEOCENTRIC = "geocentric"
    HELIOCENTRIC = "heliocentric"
    TOPOCENTRIC = "topocentric"

class AyanamsaSystem(str, Enum):
    """Ayanamsa systems"""
    LAHIRI = "lahiri"
    RAMAN = "raman"
    KRISHNAMURTI = "krishnamurti"
    FAGAN_BRADLEY = "fagan_bradley"

@dataclass
class GeoLocation:
    """Geographical location"""
    latitude: float
    longitude: float
    altitude: float = 0.0
    
    def validate(self) -> None:
        """Validate geographical coordinates"""
        if not -90 <= self.latitude <= 90:
            raise AppError(
                code=ErrorCode.INVALID_INPUT,
                message="Invalid latitude value",
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.HIGH,
                details={"latitude": self.latitude}
            )
        if not -180 <= self.longitude <= 180:
            raise AppError(
                code=ErrorCode.INVALID_INPUT,
                message="Invalid longitude value",
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.HIGH,
                details={"longitude": self.longitude}
            )

class PlanetaryPosition(BaseModel):
    """Planetary position"""
    
    body: CelestialBody
    longitude: float
    latitude: float
    distance: float
    speed: float
    sign: ZodiacSign
    house: House
    is_retrograde: bool
    
    @property
    def degree_in_sign(self) -> float:
        """Get degree within sign"""
        return self.longitude % 30
    
    @property
    def nakshatra_index(self) -> int:
        """Get nakshatra index (1-27)"""
        return math.floor(self.longitude * 3 / 40) + 1
    
    @property
    def nakshatra_degree(self) -> float:
        """Get degree within nakshatra"""
        return (self.longitude * 3 / 40) % 1 * 13.333333

class AspectPosition(BaseModel):
    """Aspect position"""
    
    body1: CelestialBody
    body2: CelestialBody
    aspect: Aspect
    orb: float
    exact_degree: float
    applying: bool

class AstronomicalCalculator:
    """Astronomical calculator"""
    
    def __init__(
        self,
        coordinate_system: CoordinateSystem = CoordinateSystem.GEOCENTRIC,
        ayanamsa_system: AyanamsaSystem = AyanamsaSystem.LAHIRI
    ):
        self.coordinate_system = coordinate_system
        self.ayanamsa_system = ayanamsa_system
        self._setup_ephemeris()
    
    def _setup_ephemeris(self) -> None:
        """Setup ephemeris"""
        # Initialize Swiss Ephemeris
        swe.set_ephe_path()  # Use default ephemeris path
        
        # Set ayanamsa
        if self.ayanamsa_system == AyanamsaSystem.LAHIRI:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
        elif self.ayanamsa_system == AyanamsaSystem.RAMAN:
            swe.set_sid_mode(swe.SIDM_RAMAN)
        elif self.ayanamsa_system == AyanamsaSystem.KRISHNAMURTI:
            swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
        elif self.ayanamsa_system == AyanamsaSystem.FAGAN_BRADLEY:
            swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)
    
    def _get_julian_day(self, dt: datetime) -> float:
        """Get Julian day number"""
        return swe.julday(
            dt.year,
            dt.month,
            dt.day,
            dt.hour + dt.minute/60.0 + dt.second/3600.0
        )
    
    def _get_planet_id(self, body: CelestialBody) -> int:
        """Get Swiss Ephemeris planet ID"""
        planet_map = {
            CelestialBody.SUN: swe.SUN,
            CelestialBody.MOON: swe.MOON,
            CelestialBody.MARS: swe.MARS,
            CelestialBody.MERCURY: swe.MERCURY,
            CelestialBody.JUPITER: swe.JUPITER,
            CelestialBody.VENUS: swe.VENUS,
            CelestialBody.SATURN: swe.SATURN,
            CelestialBody.URANUS: swe.URANUS,
            CelestialBody.NEPTUNE: swe.NEPTUNE,
            CelestialBody.PLUTO: swe.PLUTO,
            CelestialBody.RAHU: swe.MEAN_NODE,
            CelestialBody.KETU: swe.MEAN_NODE  # Calculated from Rahu
        }
        return planet_map[body]
    
    def _get_zodiac_sign(self, longitude: float) -> ZodiacSign:
        """Get zodiac sign from longitude"""
        sign_index = int(longitude / 30)
        return list(ZodiacSign)[sign_index]
    
    def _get_house(
        self,
        longitude: float,
        ascendant: float
    ) -> House:
        """Get house from longitude and ascendant"""
        house_longitude = (longitude - ascendant + 360) % 360
        house_index = int(house_longitude / 30)
        return list(House)[house_index]
    
    def _calculate_aspect(
        self,
        body1_pos: PlanetaryPosition,
        body2_pos: PlanetaryPosition
    ) -> Optional[AspectPosition]:
        """Calculate aspect between two planets"""
        # Calculate angular distance
        angle = abs(body1_pos.longitude - body2_pos.longitude) % 360
        if angle > 180:
            angle = 360 - angle
        
        # Define aspect orbs
        orbs = {
            Aspect.CONJUNCTION: 10,
            Aspect.SEXTILE: 6,
            Aspect.SQUARE: 8,
            Aspect.TRINE: 8,
            Aspect.OPPOSITION: 10
        }
        
        # Check for aspects
        for aspect in Aspect:
            if aspect == Aspect.CONJUNCTION:
                target_angle = 0
            elif aspect == Aspect.SEXTILE:
                target_angle = 60
            elif aspect == Aspect.SQUARE:
                target_angle = 90
            elif aspect == Aspect.TRINE:
                target_angle = 120
            else:  # OPPOSITION
                target_angle = 180
            
            orb = orbs[aspect]
            if abs(angle - target_angle) <= orb:
                # Calculate if aspect is applying or separating
                applying = (
                    (body1_pos.speed - body2_pos.speed) < 0
                    if angle < target_angle
                    else (body1_pos.speed - body2_pos.speed) > 0
                )
                
                return AspectPosition(
                    body1=body1_pos.body,
                    body2=body2_pos.body,
                    aspect=aspect,
                    orb=abs(angle - target_angle),
                    exact_degree=target_angle,
                    applying=applying
                )
        
        return None
    
    def calculate_planet_position(
        self,
        body: CelestialBody,
        dt: datetime,
        location: GeoLocation
    ) -> PlanetaryPosition:
        """Calculate planetary position"""
        try:
            # Validate location
            location.validate()
            
            # Convert to Julian day
            jd = self._get_julian_day(dt)
            
            # Set geographic location for topocentric calculations
            if self.coordinate_system == CoordinateSystem.TOPOCENTRIC:
                swe.set_topo(
                    location.longitude,
                    location.latitude,
                    location.altitude
                )
            
            # Calculate planet position
            planet_id = self._get_planet_id(body)
            calc_flags = (
                (swe.FLG_TOPOCENTRIC | swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
                if self.coordinate_system == CoordinateSystem.TOPOCENTRIC
                else (swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
            )

            def _calc(planet: int, flags: int):
                return swe.calc_ut(jd, planet, flags)

            try:
                if body == CelestialBody.KETU:
                    res = _calc(swe.MEAN_NODE, calc_flags)
                    longitude = (res[0][0] + 180) % 360
                    latitude = -res[0][1]
                    distance = res[0][2]
                    speed = -res[0][3]
                else:
                    res = _calc(planet_id, calc_flags)
                    longitude = res[0][0]
                    latitude = res[0][1]
                    distance = res[0][2]
                    speed = res[0][3]
            except Exception:
                # Fallback to Moshier ephemeris if Swiss ephemeris files are unavailable
                fallback_flags = (
                    (swe.FLG_TOPOCENTRIC | swe.FLG_MOSEPH | swe.FLG_SIDEREAL)
                    if self.coordinate_system == CoordinateSystem.TOPOCENTRIC
                    else (swe.FLG_MOSEPH | swe.FLG_SIDEREAL)
                )
                if body == CelestialBody.KETU:
                    res = _calc(swe.MEAN_NODE, fallback_flags)
                    longitude = (res[0][0] + 180) % 360
                    latitude = -res[0][1]
                    distance = res[0][2]
                    speed = -res[0][3]
                else:
                    res = _calc(planet_id, fallback_flags)
                    longitude = res[0][0]
                    latitude = res[0][1]
                    distance = res[0][2]
                    speed = res[0][3]
            
            # Calculate houses
            houses = swe.houses(
                jd,
                location.latitude,
                location.longitude,
                b'P'  # Placidus house system
            )
            ascendant = houses[1][0]
            
            return PlanetaryPosition(
                body=body,
                longitude=longitude,
                latitude=latitude,
                distance=distance,
                speed=speed,
                sign=self._get_zodiac_sign(longitude),
                house=self._get_house(longitude, ascendant),
                is_retrograde=speed < 0
            )
            
        except Exception as e:
            raise AppError(
                code=ErrorCode.CALCULATION_ERROR,
                message="Failed to calculate planetary position",
                category=ErrorCategory.BUSINESS_LOGIC,
                severity=ErrorSeverity.HIGH,
                details={
                    "body": body,
                    "datetime": dt.isoformat(),
                    "location": location.__dict__,
                    "error": str(e)
                }
            )
    
    def calculate_all_positions(
        self,
        dt: datetime,
        location: GeoLocation
    ) -> Dict[CelestialBody, PlanetaryPosition]:
        """Calculate positions for all planets"""
        positions = {}
        for body in CelestialBody:
            positions[body] = self.calculate_planet_position(
                body,
                dt,
                location
            )
        return positions
    
    def calculate_aspects(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition]
    ) -> List[AspectPosition]:
        """Calculate aspects between all planets"""
        aspects = []
        bodies = list(positions.keys())
        
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                body1, body2 = bodies[i], bodies[j]
                aspect = self._calculate_aspect(
                    positions[body1],
                    positions[body2]
                )
                if aspect:
                    aspects.append(aspect)
        
        return aspects
    
    def cleanup(self) -> None:
        """Cleanup ephemeris"""
        swe.close()
