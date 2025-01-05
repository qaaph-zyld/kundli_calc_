"""
Astrological Integration Framework
PGF Protocol: INT_001
Gate: GATE_19
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union, Set
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field
import swisseph as swe
import ephem
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)
from ..astronomical.framework import (
    CelestialBody,
    ZodiacSign,
    House,
    Aspect,
    GeoLocation,
    PlanetaryPosition,
    AspectPosition,
    AstronomicalCalculator
)
from ..mathematics.framework import (
    PlanetaryMath,
    SphericalCoordinate,
    EclipticCoordinate
)
from ..algorithms.framework import (
    YogaType,
    DashaSystem,
    StrengthFactor,
    YogaResult,
    DashaResult,
    StrengthResult,
    AstrologicalAlgorithms
)
from ..interpretation.framework import (
    InterpretationDomain,
    InterpretationTimeframe,
    InterpretationStrength,
    DomainInterpretation,
    ComprehensiveInterpretation,
    AstrologicalInterpreter
)

class IntegrationMode(str, Enum):
    """Integration modes"""
    STANDALONE = "standalone"
    SWISS_EPHEMERIS = "swiss_ephemeris"
    EPHEM = "ephem"
    HYBRID = "hybrid"

class ChartType(str, Enum):
    """Chart types"""
    BIRTH = "birth"
    TRANSIT = "transit"
    PROGRESSION = "progression"
    SOLAR_RETURN = "solar_return"
    COMPOSITE = "composite"

@dataclass
class ChartData:
    """Chart data"""
    
    type: ChartType
    timestamp: datetime
    location: GeoLocation
    positions: Dict[CelestialBody, PlanetaryPosition]
    houses: Dict[House, float]
    aspects: List[AspectPosition]
    yogas: List[YogaResult]
    dashas: List[DashaResult]
    strengths: Dict[CelestialBody, StrengthResult]
    interpretation: ComprehensiveInterpretation

class AstrologicalIntegrator:
    """Astrological integration engine"""
    
    def __init__(
        self,
        mode: IntegrationMode = IntegrationMode.HYBRID,
        ephemeris_path: Optional[str] = None
    ):
        """Initialize integrator"""
        self.mode = mode
        self.ephemeris_path = ephemeris_path
        
        # Initialize components
        self.calculator = AstronomicalCalculator()
        self.math = PlanetaryMath()
        self.algorithms = AstrologicalAlgorithms()
        self.interpreter = AstrologicalInterpreter()
        
        # Initialize ephemeris
        if mode in [
            IntegrationMode.SWISS_EPHEMERIS,
            IntegrationMode.HYBRID
        ]:
            if ephemeris_path:
                swe.set_ephe_path(ephemeris_path)
            swe.set_topo(0, 0, 0)  # Default location
    
    def calculate_chart(
        self,
        chart_type: ChartType,
        timestamp: datetime,
        location: GeoLocation,
        reference_chart: Optional[ChartData] = None
    ) -> ChartData:
        """Calculate complete chart"""
        
        # Calculate planetary positions
        positions = self._calculate_positions(
            timestamp,
            location,
            chart_type,
            reference_chart
        )
        
        # Calculate house cusps
        houses = self._calculate_houses(
            timestamp,
            location
        )
        
        # Calculate aspects
        aspects = self._calculate_aspects(positions)
        
        # Calculate yogas
        yogas = self.algorithms.analyze_raja_yoga(positions)
        yogas.extend(self.algorithms.analyze_dhana_yoga(positions))
        yogas.extend(self.algorithms.analyze_mahapurusha_yoga(positions))
        
        # Calculate dashas
        dashas = self.algorithms.calculate_dasha_periods(
            positions,
            timestamp
        )
        
        # Calculate strengths
        strengths = self.algorithms.calculate_planetary_strength(
            positions
        )
        
        # Generate interpretation
        interpretation = self.interpreter.interpret_chart(
            positions,
            timestamp,
            location
        )
        
        return ChartData(
            type=chart_type,
            timestamp=timestamp,
            location=location,
            positions=positions,
            houses=houses,
            aspects=aspects,
            yogas=yogas,
            dashas=dashas,
            strengths=strengths,
            interpretation=interpretation
        )
    
    def calculate_transit_chart(
        self,
        birth_chart: ChartData,
        transit_time: datetime,
        location: Optional[GeoLocation] = None
    ) -> ChartData:
        """Calculate transit chart"""
        return self.calculate_chart(
            ChartType.TRANSIT,
            transit_time,
            location or birth_chart.location,
            birth_chart
        )
    
    def calculate_progression_chart(
        self,
        birth_chart: ChartData,
        progression_date: datetime
    ) -> ChartData:
        """Calculate progression chart"""
        return self.calculate_chart(
            ChartType.PROGRESSION,
            progression_date,
            birth_chart.location,
            birth_chart
        )
    
    def calculate_solar_return(
        self,
        birth_chart: ChartData,
        year: int,
        location: Optional[GeoLocation] = None
    ) -> ChartData:
        """Calculate solar return chart"""
        
        # Find exact solar return time
        sun_pos = birth_chart.positions[CelestialBody.SUN]
        target_lon = sun_pos.longitude
        
        # Start from approximate time
        start_time = datetime(
            year,
            birth_chart.timestamp.month,
            birth_chart.timestamp.day,
            birth_chart.timestamp.hour,
            birth_chart.timestamp.minute
        )
        
        # Binary search for exact time
        time_window = timedelta(days=2)
        exact_time = self._find_solar_return_time(
            start_time,
            target_lon,
            time_window
        )
        
        return self.calculate_chart(
            ChartType.SOLAR_RETURN,
            exact_time,
            location or birth_chart.location,
            birth_chart
        )
    
    def calculate_composite_chart(
        self,
        chart1: ChartData,
        chart2: ChartData
    ) -> ChartData:
        """Calculate composite chart"""
        
        # Calculate midpoint of times
        mid_timestamp = chart1.timestamp + (
            chart2.timestamp - chart1.timestamp
        ) / 2
        
        # Calculate midpoint of locations
        mid_lat = (
            chart1.location.latitude +
            chart2.location.latitude
        ) / 2
        mid_lon = (
            chart1.location.longitude +
            chart2.location.longitude
        ) / 2
        mid_location = GeoLocation(
            latitude=mid_lat,
            longitude=mid_lon,
            altitude=(
                chart1.location.altitude +
                chart2.location.altitude
            ) / 2 if chart1.location.altitude and chart2.location.altitude
            else None
        )
        
        # Calculate composite positions
        composite_positions = {}
        for body in CelestialBody:
            if (
                body in chart1.positions and
                body in chart2.positions
            ):
                pos1 = chart1.positions[body]
                pos2 = chart2.positions[body]
                
                # Calculate midpoint longitude
                mid_lon = self.math.calculate_midpoint(
                    pos1.longitude,
                    pos2.longitude
                )
                
                # Calculate midpoint latitude
                mid_lat = (pos1.latitude + pos2.latitude) / 2
                
                composite_positions[body] = PlanetaryPosition(
                    body=body,
                    longitude=mid_lon,
                    latitude=mid_lat,
                    distance=(pos1.distance + pos2.distance) / 2,
                    speed=(pos1.speed + pos2.speed) / 2,
                    is_retrograde=pos1.is_retrograde or pos2.is_retrograde
                )
        
        return self.calculate_chart(
            ChartType.COMPOSITE,
            mid_timestamp,
            mid_location,
            None  # No reference chart for composite
        )
    
    def _calculate_positions(
        self,
        timestamp: datetime,
        location: GeoLocation,
        chart_type: ChartType,
        reference_chart: Optional[ChartData]
    ) -> Dict[CelestialBody, PlanetaryPosition]:
        """Calculate planetary positions"""
        
        positions = {}
        
        if self.mode == IntegrationMode.SWISS_EPHEMERIS:
            # Use Swiss Ephemeris
            julian_day = self._to_julian_day(timestamp)
            
            for body in CelestialBody:
                if body in [CelestialBody.RAHU, CelestialBody.KETU]:
                    continue
                
                # Get body position
                flags = swe.FLG_SPEED | swe.FLG_TOPOCTR
                result = swe.calc_ut(
                    julian_day,
                    self._to_swe_body(body),
                    flags
                )
                
                lon = result[0]
                lat = result[1]
                dist = result[2]
                speed = result[3]
                
                positions[body] = PlanetaryPosition(
                    body=body,
                    longitude=lon,
                    latitude=lat,
                    distance=dist,
                    speed=speed,
                    is_retrograde=speed < 0
                )
        
        elif self.mode == IntegrationMode.EPHEM:
            # Use PyEphem
            observer = ephem.Observer()
            observer.lat = str(location.latitude)
            observer.lon = str(location.longitude)
            observer.date = timestamp
            
            for body in CelestialBody:
                if body in [CelestialBody.RAHU, CelestialBody.KETU]:
                    continue
                
                # Get body position
                ephem_body = self._to_ephem_body(body)
                ephem_body.compute(observer)
                
                # Convert to ecliptic coordinates
                eq = EclipticCoordinate(
                    longitude=ephem_body.ra * 180 / math.pi,
                    latitude=ephem_body.dec * 180 / math.pi
                )
                
                positions[body] = PlanetaryPosition(
                    body=body,
                    longitude=eq.longitude,
                    latitude=eq.latitude,
                    distance=ephem_body.earth_distance,
                    speed=0,  # PyEphem doesn't provide speed
                    is_retrograde=False
                )
        
        else:  # HYBRID or STANDALONE
            # Use combination or built-in calculations
            positions = self.calculator.calculate_positions(
                timestamp,
                location
            )
        
        # Special handling for chart types
        if chart_type == ChartType.PROGRESSION:
            assert reference_chart is not None
            positions = self._progress_positions(
                positions,
                reference_chart.positions,
                reference_chart.timestamp,
                timestamp
            )
        
        return positions
    
    def _calculate_houses(
        self,
        timestamp: datetime,
        location: GeoLocation
    ) -> Dict[House, float]:
        """Calculate house cusps"""
        
        houses = {}
        
        if self.mode == IntegrationMode.SWISS_EPHEMERIS:
            # Use Swiss Ephemeris
            julian_day = self._to_julian_day(timestamp)
            
            # Calculate houses using Placidus system
            cusps, ascmc = swe.houses(
                julian_day,
                location.latitude,
                location.longitude,
                b'P'  # Placidus
            )
            
            for i, house in enumerate(House):
                houses[house] = cusps[i]
        
        elif self.mode == IntegrationMode.EPHEM:
            # Use PyEphem
            observer = ephem.Observer()
            observer.lat = str(location.latitude)
            observer.lon = str(location.longitude)
            observer.date = timestamp
            
            # Calculate Ascendant
            houses[House.FIRST] = math.degrees(
                float(observer.sidereal_time())
            )
            
            # Calculate other houses (simplified)
            for i, house in enumerate(House):
                if house != House.FIRST:
                    houses[house] = (
                        houses[House.FIRST] + i * 30
                    ) % 360
        
        else:  # HYBRID or STANDALONE
            # Use built-in calculations
            houses = self.calculator.calculate_houses(
                timestamp,
                location
            )
        
        return houses
    
    def _calculate_aspects(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition]
    ) -> List[AspectPosition]:
        """Calculate aspects between planets"""
        aspects = []
        
        # Calculate aspects between all planet pairs
        bodies = list(positions.keys())
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                body1 = bodies[i]
                body2 = bodies[j]
                
                pos1 = positions[body1]
                pos2 = positions[body2]
                
                # Check for aspects
                aspect = self.algorithms._check_mutual_aspect(
                    pos1,
                    pos2
                )
                
                if aspect:
                    aspects.append(AspectPosition(
                        body1=body1,
                        body2=body2,
                        aspect=aspect,
                        orb=self.math.angular_distance(
                            pos1.longitude,
                            pos2.longitude
                        )
                    ))
        
        return aspects
    
    def _progress_positions(
        self,
        current_positions: Dict[CelestialBody, PlanetaryPosition],
        birth_positions: Dict[CelestialBody, PlanetaryPosition],
        birth_time: datetime,
        progression_time: datetime
    ) -> Dict[CelestialBody, PlanetaryPosition]:
        """Progress positions using secondary progression"""
        
        progressed = {}
        
        for body, birth_pos in birth_positions.items():
            # Secondary progression: 1 day = 1 year
            progressed_lon = self.math.calculate_progression(
                birth_pos,
                progression_time,
                birth_time
            )
            
            # Keep other attributes from birth position
            progressed[body] = PlanetaryPosition(
                body=body,
                longitude=progressed_lon,
                latitude=birth_pos.latitude,
                distance=birth_pos.distance,
                speed=birth_pos.speed,
                is_retrograde=birth_pos.is_retrograde
            )
        
        return progressed
    
    def _find_solar_return_time(
        self,
        start_time: datetime,
        target_longitude: float,
        time_window: timedelta,
        precision: float = 0.0001
    ) -> datetime:
        """Find exact solar return time"""
        
        left = start_time - time_window
        right = start_time + time_window
        
        while (right - left) > timedelta(minutes=1):
            mid = left + (right - left) / 2
            
            # Calculate Sun's position
            positions = self._calculate_positions(
                mid,
                GeoLocation(0, 0),  # Location doesn't matter for Sun
                ChartType.TRANSIT,
                None
            )
            
            sun_lon = positions[CelestialBody.SUN].longitude
            
            if abs(sun_lon - target_longitude) < precision:
                return mid
            elif sun_lon < target_longitude:
                left = mid
            else:
                right = mid
        
        return left
    
    def _to_julian_day(self, timestamp: datetime) -> float:
        """Convert datetime to Julian Day"""
        return swe.julday(
            timestamp.year,
            timestamp.month,
            timestamp.day,
            timestamp.hour +
            timestamp.minute / 60 +
            timestamp.second / 3600
        )
    
    def _to_swe_body(self, body: CelestialBody) -> int:
        """Convert CelestialBody to Swiss Ephemeris body number"""
        swe_bodies = {
            CelestialBody.SUN: swe.SUN,
            CelestialBody.MOON: swe.MOON,
            CelestialBody.MARS: swe.MARS,
            CelestialBody.MERCURY: swe.MERCURY,
            CelestialBody.JUPITER: swe.JUPITER,
            CelestialBody.VENUS: swe.VENUS,
            CelestialBody.SATURN: swe.SATURN,
            CelestialBody.RAHU: swe.MEAN_NODE,
            CelestialBody.KETU: swe.MEAN_NODE
        }
        return swe_bodies[body]
    
    def _to_ephem_body(self, body: CelestialBody) -> ephem.Body:
        """Convert CelestialBody to PyEphem body"""
        ephem_bodies = {
            CelestialBody.SUN: ephem.Sun(),
            CelestialBody.MOON: ephem.Moon(),
            CelestialBody.MARS: ephem.Mars(),
            CelestialBody.MERCURY: ephem.Mercury(),
            CelestialBody.JUPITER: ephem.Jupiter(),
            CelestialBody.VENUS: ephem.Venus(),
            CelestialBody.SATURN: ephem.Saturn()
        }
        return ephem_bodies[body]
