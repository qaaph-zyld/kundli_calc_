"""
Planetary Mathematics Module
PGF Protocol: MTH_003
Gate: GATE_16
Version: 1.0.0
"""

from .framework import (
    SphericalCoordinate,
    EclipticCoordinate,
    EquatorialCoordinate,
    HorizontalCoordinate,
    PlanetaryMath
)
from .config import (
    ASTRONOMICAL_CONSTANTS,
    HARMONIC_RELATIONSHIPS,
    DIGNITY_SCORES,
    ESSENTIAL_DIGNITIES,
    ASPECT_ORBS,
    MATH_CONFIG,
    get_math_config
)

__all__ = [
    'SphericalCoordinate',
    'EclipticCoordinate',
    'EquatorialCoordinate',
    'HorizontalCoordinate',
    'PlanetaryMath',
    'ASTRONOMICAL_CONSTANTS',
    'HARMONIC_RELATIONSHIPS',
    'DIGNITY_SCORES',
    'ESSENTIAL_DIGNITIES',
    'ASPECT_ORBS',
    'MATH_CONFIG',
    'get_math_config'
]
