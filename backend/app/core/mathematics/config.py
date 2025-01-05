"""
Planetary Mathematics Configuration
PGF Protocol: MTH_002
Gate: GATE_16
Version: 1.0.0
"""

from typing import Dict, Any, List
from ..astronomical.framework import (
    CelestialBody,
    ZodiacSign,
    House,
    Aspect
)

# Astronomical constants
ASTRONOMICAL_CONSTANTS = {
    "OBLIQUITY_2000": 23.43929111,  # Earth's obliquity J2000
    "PRECESSION_RATE": 50.290966,    # Precession rate in arcseconds per year
    "SIDEREAL_DAY": 23.9344696,      # Length of sidereal day in hours
    "TROPICAL_YEAR": 365.242190,     # Length of tropical year in days
    "SYNODIC_MONTH": 29.530589,      # Length of synodic month in days
    "MEAN_LUNAR_SPEED": 13.1763581,  # Mean lunar speed in degrees per day
    "MEAN_SOLAR_SPEED": 0.9856473,   # Mean solar speed in degrees per day
}

# Harmonic relationships
HARMONIC_RELATIONSHIPS = {
    2: {
        "name": "Opposition",
        "meaning": "Awareness, Balance, Tension",
        "keywords": ["polarity", "objectivity", "relationship"]
    },
    3: {
        "name": "Trine",
        "meaning": "Flow, Harmony, Integration",
        "keywords": ["creativity", "expression", "growth"]
    },
    4: {
        "name": "Square",
        "meaning": "Challenge, Action, Development",
        "keywords": ["crisis", "building", "manifestation"]
    },
    5: {
        "name": "Quintile",
        "meaning": "Talent, Creativity, Gift",
        "keywords": ["unique abilities", "self-expression", "artistry"]
    },
    6: {
        "name": "Sextile",
        "meaning": "Opportunity, Learning, Growth",
        "keywords": ["education", "communication", "development"]
    },
    7: {
        "name": "Septile",
        "meaning": "Spiritual, Mystical, Fated",
        "keywords": ["destiny", "spiritual wisdom", "inner knowing"]
    },
    8: {
        "name": "Octile",
        "meaning": "Adjustment, Stress, Growth",
        "keywords": ["transformation", "crisis", "evolution"]
    },
    9: {
        "name": "Novile",
        "meaning": "Completion, Integration, Wisdom",
        "keywords": ["understanding", "synthesis", "culmination"]
    },
    10: {
        "name": "Decile",
        "meaning": "Opportunity, Aspiration",
        "keywords": ["potential", "development", "growth"]
    },
    12: {
        "name": "Dodecile",
        "meaning": "Pattern, Cycle, Completion",
        "keywords": ["wholeness", "integration", "perfection"]
    }
}

# Dignity scores
DIGNITY_SCORES = {
    "RULERSHIP": 5,
    "EXALTATION": 4,
    "TRIPLICITY": 3,
    "TERM": 2,
    "FACE": 1,
    "DETRIMENT": -5,
    "FALL": -4
}

# Essential dignities
ESSENTIAL_DIGNITIES: Dict[ZodiacSign, Dict[str, Any]] = {
    ZodiacSign.ARIES: {
        "ruler": CelestialBody.MARS,
        "exaltation": CelestialBody.SUN,
        "detriment": CelestialBody.VENUS,
        "fall": CelestialBody.SATURN,
        "triplicity_rulers": {
            "day": CelestialBody.SUN,
            "night": CelestialBody.JUPITER,
            "participating": CelestialBody.SATURN
        }
    },
    ZodiacSign.TAURUS: {
        "ruler": CelestialBody.VENUS,
        "exaltation": CelestialBody.MOON,
        "detriment": CelestialBody.MARS,
        "fall": None,
        "triplicity_rulers": {
            "day": CelestialBody.VENUS,
            "night": CelestialBody.MOON,
            "participating": CelestialBody.MARS
        }
    },
    # ... (similar entries for other signs)
}

# Aspect orbs
ASPECT_ORBS = {
    Aspect.CONJUNCTION: {
        "major_bodies": 10.0,
        "minor_bodies": 8.0,
        "nodes": 6.0
    },
    Aspect.OPPOSITION: {
        "major_bodies": 10.0,
        "minor_bodies": 8.0,
        "nodes": 6.0
    },
    Aspect.TRINE: {
        "major_bodies": 8.0,
        "minor_bodies": 6.0,
        "nodes": 4.0
    },
    Aspect.SQUARE: {
        "major_bodies": 8.0,
        "minor_bodies": 6.0,
        "nodes": 4.0
    },
    Aspect.SEXTILE: {
        "major_bodies": 6.0,
        "minor_bodies": 4.0,
        "nodes": 2.0
    }
}

# Mathematical functions configuration
MATH_CONFIG = {
    "use_true_node": True,           # Use true node instead of mean node
    "topocentric": True,             # Use topocentric positions
    "true_positions": True,          # Use true positions instead of mean
    "harmonic_analysis": True,       # Enable harmonic analysis
    "progression_method": "secondary",  # secondary, solar arc, or tertiary
    "house_system": "placidus",      # placidus, koch, campanus, etc.
    "coordinate_system": "ecliptic",  # ecliptic or equatorial
    "precision": {
        "longitude": 6,              # Decimal places for longitude
        "latitude": 6,               # Decimal places for latitude
        "distance": 8,               # Decimal places for distance
        "speed": 8                   # Decimal places for speed
    }
}

def get_math_config(environment: str) -> Dict[str, Any]:
    """Get mathematics configuration for environment"""
    
    base_config = {
        "constants": ASTRONOMICAL_CONSTANTS,
        "harmonics": HARMONIC_RELATIONSHIPS,
        "dignities": DIGNITY_SCORES,
        "essential_dignities": ESSENTIAL_DIGNITIES,
        "aspect_orbs": ASPECT_ORBS,
        "math_config": MATH_CONFIG
    }
    
    if environment == "local":
        base_config["math_config"].update({
            "topocentric": False,
            "true_positions": False,
            "harmonic_analysis": False
        })
    
    elif environment == "development":
        base_config["math_config"].update({
            "topocentric": True,
            "true_positions": True,
            "harmonic_analysis": True
        })
    
    else:  # staging and production
        base_config["math_config"].update({
            "topocentric": True,
            "true_positions": True,
            "harmonic_analysis": True,
            "precision": {
                "longitude": 8,
                "latitude": 8,
                "distance": 10,
                "speed": 10
            }
        })
    
    return base_config
