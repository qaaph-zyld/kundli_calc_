"""
Planetary Mathematics Framework
PGF Protocol: MTH_001
Gate: GATE_16
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union
import math
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
from pydantic import BaseModel, Field
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
    PlanetaryPosition
)

@dataclass
class SphericalCoordinate:
    """Spherical coordinate"""
    
    longitude: float  # λ (lambda)
    latitude: float   # β (beta)
    distance: float   # r
    
    def to_cartesian(self) -> Tuple[float, float, float]:
        """Convert to Cartesian coordinates"""
        r = self.distance
        λ = math.radians(self.longitude)
        β = math.radians(self.latitude)
        
        x = r * math.cos(β) * math.cos(λ)
        y = r * math.cos(β) * math.sin(λ)
        z = r * math.sin(β)
        
        return (x, y, z)
    
    @classmethod
    def from_cartesian(
        cls,
        x: float,
        y: float,
        z: float
    ) -> 'SphericalCoordinate':
        """Create from Cartesian coordinates"""
        r = math.sqrt(x*x + y*y + z*z)
        λ = math.degrees(math.atan2(y, x))
        if λ < 0:
            λ += 360
        β = math.degrees(math.asin(z/r))
        
        return cls(longitude=λ, latitude=β, distance=r)

@dataclass
class EclipticCoordinate:
    """Ecliptic coordinate"""
    
    longitude: float  # λ (lambda)
    latitude: float   # β (beta)
    
    def to_equatorial(self, obliquity: float) -> 'EquatorialCoordinate':
        """Convert to equatorial coordinates"""
        λ = math.radians(self.longitude)
        β = math.radians(self.latitude)
        ε = math.radians(obliquity)
        
        # Calculate right ascension (α) and declination (δ)
        sin_δ = math.sin(β) * math.cos(ε) + math.cos(β) * math.sin(ε) * math.sin(λ)
        δ = math.degrees(math.asin(sin_δ))
        
        y = math.sin(λ) * math.cos(ε) - math.tan(β) * math.sin(ε)
        x = math.cos(λ)
        α = math.degrees(math.atan2(y, x))
        if α < 0:
            α += 360
        
        return EquatorialCoordinate(
            right_ascension=α,
            declination=δ
        )

@dataclass
class EquatorialCoordinate:
    """Equatorial coordinate"""
    
    right_ascension: float  # α (alpha)
    declination: float      # δ (delta)
    
    def to_horizontal(
        self,
        location: GeoLocation,
        sidereal_time: float
    ) -> 'HorizontalCoordinate':
        """Convert to horizontal coordinates"""
        α = math.radians(self.right_ascension)
        δ = math.radians(self.declination)
        φ = math.radians(location.latitude)
        H = math.radians(sidereal_time - self.right_ascension)
        
        # Calculate altitude (h) and azimuth (A)
        sin_h = math.sin(φ) * math.sin(δ) + math.cos(φ) * math.cos(δ) * math.cos(H)
        h = math.degrees(math.asin(sin_h))
        
        y = -math.cos(δ) * math.sin(H)
        x = math.cos(φ) * math.sin(δ) - math.sin(φ) * math.cos(δ) * math.cos(H)
        A = math.degrees(math.atan2(y, x))
        if A < 0:
            A += 360
        
        return HorizontalCoordinate(
            azimuth=A,
            altitude=h
        )

@dataclass
class HorizontalCoordinate:
    """Horizontal coordinate"""
    
    azimuth: float    # A
    altitude: float   # h

class PlanetaryMath:
    """Planetary mathematics"""
    
    @staticmethod
    def normalize_angle(angle: float) -> float:
        """Normalize angle to 0-360 range"""
        return angle % 360
    
    @staticmethod
    def angular_distance(angle1: float, angle2: float) -> float:
        """Calculate shortest angular distance between two angles"""
        diff = abs(angle1 - angle2) % 360
        return min(diff, 360 - diff)
    
    @staticmethod
    def angular_velocity(
        pos1: PlanetaryPosition,
        pos2: PlanetaryPosition,
        time_diff: timedelta
    ) -> float:
        """Calculate angular velocity between two positions"""
        angle_diff = PlanetaryMath.angular_distance(
            pos1.longitude,
            pos2.longitude
        )
        days = time_diff.total_seconds() / 86400
        return angle_diff / days if days != 0 else 0
    
    @staticmethod
    def calculate_midpoint(angle1: float, angle2: float) -> float:
        """Calculate midpoint between two angles"""
        diff = (angle2 - angle1) % 360
        if diff > 180:
            return (angle1 + diff/2) % 360
        return (angle1 + angle2) / 2 % 360
    
    @staticmethod
    def calculate_harmonic(angle: float, harmonic: int) -> float:
        """Calculate harmonic of an angle"""
        return (angle * harmonic) % 360
    
    @staticmethod
    def calculate_phase_angle(
        body_lon: float,
        sun_lon: float
    ) -> float:
        """Calculate phase angle relative to Sun"""
        return PlanetaryMath.normalize_angle(body_lon - sun_lon)
    
    @staticmethod
    def calculate_aspect_orb(
        pos1: PlanetaryPosition,
        pos2: PlanetaryPosition,
        aspect: Aspect
    ) -> float:
        """Calculate aspect orb"""
        actual_angle = PlanetaryMath.angular_distance(
            pos1.longitude,
            pos2.longitude
        )
        
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
        
        return abs(actual_angle - target_angle)
    
    @staticmethod
    def calculate_dignity_score(
        body: CelestialBody,
        sign: ZodiacSign,
        house: House
    ) -> float:
        """Calculate dignity score"""
        from ..astronomical.config import (
            ZODIAC_PROPERTIES,
            HOUSE_SIGNIFICATIONS,
            PLANET_PROPERTIES
        )
        
        score = 0.0
        
        # Rulership
        if ZODIAC_PROPERTIES[sign]["ruler"] == body:
            score += 5
        
        # Exaltation (simplified)
        exaltation_map = {
            CelestialBody.SUN: ZodiacSign.ARIES,
            CelestialBody.MOON: ZodiacSign.TAURUS,
            CelestialBody.MARS: ZodiacSign.CAPRICORN,
            CelestialBody.MERCURY: ZodiacSign.VIRGO,
            CelestialBody.JUPITER: ZodiacSign.CANCER,
            CelestialBody.VENUS: ZodiacSign.PISCES,
            CelestialBody.SATURN: ZodiacSign.LIBRA
        }
        if body in exaltation_map and exaltation_map[body] == sign:
            score += 4
        
        # House placement (simplified)
        house_scores = {
            House.FIRST: 5,
            House.TENTH: 4,
            House.SEVENTH: 3,
            House.FOURTH: 3,
            House.ELEVENTH: 2,
            House.FIFTH: 2,
            House.NINTH: 2,
            House.SECOND: 1,
            House.THIRD: 1,
            House.EIGHTH: 0,
            House.SIXTH: -1,
            House.TWELFTH: -2
        }
        score += house_scores[house]
        
        return score
    
    @staticmethod
    def calculate_dispositor_chain(
        positions: Dict[CelestialBody, PlanetaryPosition]
    ) -> List[List[CelestialBody]]:
        """Calculate dispositor chains"""
        from ..astronomical.config import ZODIAC_PROPERTIES
        
        # Build dispositor map
        dispositor_map = {}
        for body, pos in positions.items():
            if body in [CelestialBody.RAHU, CelestialBody.KETU]:
                continue
            ruler = ZODIAC_PROPERTIES[pos.sign]["ruler"]
            dispositor_map[body] = ruler
        
        # Find chains
        chains = []
        visited = set()
        
        for body in dispositor_map:
            if body in visited:
                continue
            
            chain = []
            current = body
            chain_set = set()
            
            while current not in chain_set:
                chain.append(current)
                chain_set.add(current)
                current = dispositor_map[current]
                
                if current in chain_set:
                    # Found mutual reception or final dispositor
                    start_idx = chain.index(current)
                    final_chain = chain[start_idx:]
                    chains.append(final_chain)
                    visited.update(final_chain)
                    break
        
        return chains
    
    @staticmethod
    def calculate_progression(
        birth_pos: PlanetaryPosition,
        current_date: datetime,
        birth_date: datetime
    ) -> float:
        """Calculate secondary progression"""
        days = (current_date - birth_date).days
        years = days / 365.25
        
        # Secondary progression: 1 day = 1 year
        progressed_longitude = birth_pos.longitude + years
        return PlanetaryMath.normalize_angle(progressed_longitude)
    
    @staticmethod
    def calculate_solar_arc(
        birth_sun: PlanetaryPosition,
        current_sun: PlanetaryPosition,
        birth_pos: PlanetaryPosition
    ) -> float:
        """Calculate solar arc direction"""
        solar_arc = PlanetaryMath.angular_distance(
            current_sun.longitude,
            birth_sun.longitude
        )
        directed_longitude = birth_pos.longitude + solar_arc
        return PlanetaryMath.normalize_angle(directed_longitude)
    
    @staticmethod
    def calculate_composite(
        pos1: PlanetaryPosition,
        pos2: PlanetaryPosition
    ) -> float:
        """Calculate composite position"""
        return PlanetaryMath.calculate_midpoint(
            pos1.longitude,
            pos2.longitude
        )
    
    @staticmethod
    def calculate_harmonics(
        positions: Dict[CelestialBody, PlanetaryPosition],
        harmonic: int
    ) -> Dict[CelestialBody, float]:
        """Calculate harmonic positions"""
        harmonic_positions = {}
        for body, pos in positions.items():
            harmonic_pos = PlanetaryMath.calculate_harmonic(
                pos.longitude,
                harmonic
            )
            harmonic_positions[body] = harmonic_pos
        return harmonic_positions
