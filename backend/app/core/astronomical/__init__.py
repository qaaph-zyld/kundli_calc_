"""
Astronomical Module
PGF Protocol: AST_003
Gate: GATE_15
Version: 1.0.0
"""

from .framework import (
    CelestialBody,
    ZodiacSign,
    House,
    Aspect,
    CoordinateSystem,
    AyanamsaSystem,
    GeoLocation,
    PlanetaryPosition,
    AspectPosition,
    AstronomicalCalculator
)
from .config import (
    ZODIAC_PROPERTIES,
    HOUSE_SIGNIFICATIONS,
    ASPECT_PROPERTIES,
    PLANET_PROPERTIES,
    get_calculator_config
)

__all__ = [
    'CelestialBody',
    'ZodiacSign',
    'House',
    'Aspect',
    'CoordinateSystem',
    'AyanamsaSystem',
    'GeoLocation',
    'PlanetaryPosition',
    'AspectPosition',
    'AstronomicalCalculator',
    'ZODIAC_PROPERTIES',
    'HOUSE_SIGNIFICATIONS',
    'ASPECT_PROPERTIES',
    'PLANET_PROPERTIES',
    'get_calculator_config'
]
