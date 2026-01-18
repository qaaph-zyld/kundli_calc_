"""
Planetary Mathematics Module
PGF Protocol: MTH_003
Gate: GATE_16
Version: 1.0.0
"""

from .config import (
    ASPECT_ORBS,
    ASTRONOMICAL_CONSTANTS,
    DIGNITY_SCORES,
    ESSENTIAL_DIGNITIES,
    HARMONIC_RELATIONSHIPS,
    MATH_CONFIG,
    get_math_config,
)
from .framework import (
    EclipticCoordinate,
    EquatorialCoordinate,
    HorizontalCoordinate,
    PlanetaryMath,
    SphericalCoordinate,
)

__all__ = [
    "SphericalCoordinate",
    "EclipticCoordinate",
    "EquatorialCoordinate",
    "HorizontalCoordinate",
    "PlanetaryMath",
    "ASTRONOMICAL_CONSTANTS",
    "HARMONIC_RELATIONSHIPS",
    "DIGNITY_SCORES",
    "ESSENTIAL_DIGNITIES",
    "ASPECT_ORBS",
    "MATH_CONFIG",
    "get_math_config",
]
