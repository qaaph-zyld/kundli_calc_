"""
Astronomical Configuration
PGF Protocol: AST_002
Gate: GATE_15
Version: 1.0.0
"""

from typing import Dict, Any
from .framework import (
    CoordinateSystem,
    AyanamsaSystem,
    CelestialBody,
    ZodiacSign,
    House,
    Aspect
)

# Zodiac sign properties
ZODIAC_PROPERTIES: Dict[ZodiacSign, Dict[str, Any]] = {
    ZodiacSign.ARIES: {
        "element": "fire",
        "quality": "cardinal",
        "polarity": "positive",
        "ruler": CelestialBody.MARS,
        "degrees": (0, 30)
    },
    ZodiacSign.TAURUS: {
        "element": "earth",
        "quality": "fixed",
        "polarity": "negative",
        "ruler": CelestialBody.VENUS,
        "degrees": (30, 60)
    },
    ZodiacSign.GEMINI: {
        "element": "air",
        "quality": "mutable",
        "polarity": "positive",
        "ruler": CelestialBody.MERCURY,
        "degrees": (60, 90)
    },
    ZodiacSign.CANCER: {
        "element": "water",
        "quality": "cardinal",
        "polarity": "negative",
        "ruler": CelestialBody.MOON,
        "degrees": (90, 120)
    },
    ZodiacSign.LEO: {
        "element": "fire",
        "quality": "fixed",
        "polarity": "positive",
        "ruler": CelestialBody.SUN,
        "degrees": (120, 150)
    },
    ZodiacSign.VIRGO: {
        "element": "earth",
        "quality": "mutable",
        "polarity": "negative",
        "ruler": CelestialBody.MERCURY,
        "degrees": (150, 180)
    },
    ZodiacSign.LIBRA: {
        "element": "air",
        "quality": "cardinal",
        "polarity": "positive",
        "ruler": CelestialBody.VENUS,
        "degrees": (180, 210)
    },
    ZodiacSign.SCORPIO: {
        "element": "water",
        "quality": "fixed",
        "polarity": "negative",
        "ruler": CelestialBody.MARS,
        "degrees": (210, 240)
    },
    ZodiacSign.SAGITTARIUS: {
        "element": "fire",
        "quality": "mutable",
        "polarity": "positive",
        "ruler": CelestialBody.JUPITER,
        "degrees": (240, 270)
    },
    ZodiacSign.CAPRICORN: {
        "element": "earth",
        "quality": "cardinal",
        "polarity": "negative",
        "ruler": CelestialBody.SATURN,
        "degrees": (270, 300)
    },
    ZodiacSign.AQUARIUS: {
        "element": "air",
        "quality": "fixed",
        "polarity": "positive",
        "ruler": CelestialBody.SATURN,
        "degrees": (300, 330)
    },
    ZodiacSign.PISCES: {
        "element": "water",
        "quality": "mutable",
        "polarity": "negative",
        "ruler": CelestialBody.JUPITER,
        "degrees": (330, 360)
    }
}

# House significations
HOUSE_SIGNIFICATIONS: Dict[House, Dict[str, Any]] = {
    House.FIRST: {
        "name": "Ascendant",
        "keywords": ["self", "personality", "appearance", "beginnings"],
        "area": "personality and self-projection"
    },
    House.SECOND: {
        "name": "Dhana",
        "keywords": ["wealth", "values", "possessions", "speech"],
        "area": "material and financial resources"
    },
    House.THIRD: {
        "name": "Sahaja",
        "keywords": ["siblings", "communication", "short trips", "courage"],
        "area": "communication and immediate environment"
    },
    House.FOURTH: {
        "name": "Sukha",
        "keywords": ["mother", "home", "emotions", "vehicles"],
        "area": "home and emotional foundation"
    },
    House.FIFTH: {
        "name": "Putra",
        "keywords": ["children", "creativity", "romance", "intelligence"],
        "area": "creativity and self-expression"
    },
    House.SIXTH: {
        "name": "Ari",
        "keywords": ["health", "service", "enemies", "debts"],
        "area": "health and service"
    },
    House.SEVENTH: {
        "name": "Yuvati",
        "keywords": ["partnership", "marriage", "business", "others"],
        "area": "relationships and partnerships"
    },
    House.EIGHTH: {
        "name": "Mrityu",
        "keywords": ["transformation", "occult", "joint resources", "research"],
        "area": "transformation and regeneration"
    },
    House.NINTH: {
        "name": "Dharma",
        "keywords": ["religion", "philosophy", "higher education", "fortune"],
        "area": "higher learning and spirituality"
    },
    House.TENTH: {
        "name": "Karma",
        "keywords": ["career", "status", "authority", "father"],
        "area": "career and public standing"
    },
    House.ELEVENTH: {
        "name": "Labha",
        "keywords": ["gains", "friends", "hopes", "aspirations"],
        "area": "friends and aspirations"
    },
    House.TWELFTH: {
        "name": "Vyaya",
        "keywords": ["loss", "spirituality", "isolation", "liberation"],
        "area": "spiritual liberation and loss"
    }
}

# Aspect properties
ASPECT_PROPERTIES: Dict[Aspect, Dict[str, Any]] = {
    Aspect.CONJUNCTION: {
        "angle": 0,
        "orb": 10,
        "nature": "unifying",
        "quality": "blending of energies",
        "strength": "strong"
    },
    Aspect.SEXTILE: {
        "angle": 60,
        "orb": 6,
        "nature": "harmonious",
        "quality": "opportunities",
        "strength": "mild"
    },
    Aspect.SQUARE: {
        "angle": 90,
        "orb": 8,
        "nature": "challenging",
        "quality": "tension and growth",
        "strength": "strong"
    },
    Aspect.TRINE: {
        "angle": 120,
        "orb": 8,
        "nature": "harmonious",
        "quality": "flow and ease",
        "strength": "strong"
    },
    Aspect.OPPOSITION: {
        "angle": 180,
        "orb": 10,
        "nature": "challenging",
        "quality": "awareness and balance",
        "strength": "strong"
    }
}

# Planet properties
PLANET_PROPERTIES: Dict[CelestialBody, Dict[str, Any]] = {
    CelestialBody.SUN: {
        "nature": "hot and dry",
        "gender": "masculine",
        "speed": 1,  # degrees per day
        "significations": ["soul", "father", "authority", "vitality"],
        "metal": "gold"
    },
    CelestialBody.MOON: {
        "nature": "cold and moist",
        "gender": "feminine",
        "speed": 13.2,  # degrees per day
        "significations": ["mind", "mother", "emotions", "public"],
        "metal": "silver"
    },
    CelestialBody.MARS: {
        "nature": "hot and dry",
        "gender": "masculine",
        "speed": 0.5,  # degrees per day
        "significations": ["energy", "courage", "conflict", "action"],
        "metal": "iron"
    },
    CelestialBody.MERCURY: {
        "nature": "neutral",
        "gender": "neutral",
        "speed": 4.09,  # approx degrees per day
        "significations": ["communication", "intelligence", "trade", "skills"],
        "metal": "mercury"
    },
    CelestialBody.JUPITER: {
        "nature": "hot and moist",
        "gender": "masculine",
        "speed": 0.083,  # degrees per day
        "significations": ["wisdom", "expansion", "fortune", "dharma"],
        "metal": "tin"
    },
    CelestialBody.VENUS: {
        "nature": "cold and moist",
        "gender": "feminine",
        "speed": 1.6,  # approx degrees per day
        "significations": ["love", "pleasure", "arts", "luxury"],
        "metal": "copper"
    },
    CelestialBody.SATURN: {
        "nature": "cold and dry",
        "gender": "neutral",
        "speed": 0.034,  # degrees per day
        "significations": ["discipline", "limitation", "time", "karma"],
        "metal": "lead"
    },
    CelestialBody.RAHU: {
        "nature": "neutral",
        "gender": "neutral",
        "speed": -0.053,  # degrees per day, retrograde
        "significations": ["illusion", "obsession", "materialism", "growth"],
        "metal": None
    },
    CelestialBody.KETU: {
        "nature": "neutral",
        "gender": "neutral",
        "speed": -0.053,  # degrees per day, retrograde
        "significations": ["spirituality", "liberation", "loss", "past life"],
        "metal": None
    }
}

def get_calculator_config(environment: str) -> Dict[str, Any]:
    """Get calculator configuration for environment"""
    
    if environment == "local":
        return {
            "coordinate_system": CoordinateSystem.GEOCENTRIC,
            "ayanamsa_system": AyanamsaSystem.LAHIRI,
            "enable_aspects": True,
            "enable_dignities": True,
            "enable_progressions": False,
            "cache_enabled": False
        }
    
    elif environment == "development":
        return {
            "coordinate_system": CoordinateSystem.GEOCENTRIC,
            "ayanamsa_system": AyanamsaSystem.LAHIRI,
            "enable_aspects": True,
            "enable_dignities": True,
            "enable_progressions": True,
            "cache_enabled": True
        }
    
    else:  # staging and production
        return {
            "coordinate_system": CoordinateSystem.TOPOCENTRIC,
            "ayanamsa_system": AyanamsaSystem.LAHIRI,
            "enable_aspects": True,
            "enable_dignities": True,
            "enable_progressions": True,
            "cache_enabled": True
        }
