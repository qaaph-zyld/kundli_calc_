"""
Astrological Interpretation Configuration
PGF Protocol: INT_002
Gate: GATE_18
Version: 1.0.0
"""

from typing import Dict, Any, List
from ..astronomical.framework import (
    CelestialBody,
    ZodiacSign,
    House,
    Aspect
)
from .framework import (
    InterpretationDomain,
    InterpretationTimeframe,
    InterpretationStrength
)

# Domain configuration
DOMAIN_CONFIG = {
    InterpretationDomain.PERSONALITY: {
        "weight": 1.0,
        "required_planets": [
            CelestialBody.SUN,
            CelestialBody.MOON,
            CelestialBody.MARS
        ],
        "required_houses": [
            House.FIRST,
            House.FOURTH,
            House.TENTH
        ],
        "key_aspects": [
            Aspect.CONJUNCTION,
            Aspect.TRINE,
            Aspect.SQUARE
        ]
    },
    InterpretationDomain.CAREER: {
        "weight": 1.0,
        "required_planets": [
            CelestialBody.SATURN,
            CelestialBody.SUN,
            CelestialBody.JUPITER
        ],
        "required_houses": [
            House.TENTH,
            House.SIXTH,
            House.SECOND
        ],
        "key_aspects": [
            Aspect.CONJUNCTION,
            Aspect.TRINE,
            Aspect.SEXTILE
        ]
    },
    InterpretationDomain.RELATIONSHIPS: {
        "weight": 1.0,
        "required_planets": [
            CelestialBody.VENUS,
            CelestialBody.JUPITER,
            CelestialBody.MOON
        ],
        "required_houses": [
            House.SEVENTH,
            House.FIFTH,
            House.ELEVENTH
        ],
        "key_aspects": [
            Aspect.CONJUNCTION,
            Aspect.TRINE,
            Aspect.OPPOSITION
        ]
    },
    InterpretationDomain.HEALTH: {
        "weight": 1.0,
        "required_planets": [
            CelestialBody.SUN,
            CelestialBody.MARS,
            CelestialBody.SATURN
        ],
        "required_houses": [
            House.FIRST,
            House.SIXTH,
            House.EIGHTH
        ],
        "key_aspects": [
            Aspect.CONJUNCTION,
            Aspect.SQUARE,
            Aspect.OPPOSITION
        ]
    },
    InterpretationDomain.SPIRITUALITY: {
        "weight": 1.0,
        "required_planets": [
            CelestialBody.JUPITER,
            CelestialBody.KETU,
            CelestialBody.SATURN
        ],
        "required_houses": [
            House.NINTH,
            House.TWELFTH,
            House.FOURTH
        ],
        "key_aspects": [
            Aspect.CONJUNCTION,
            Aspect.TRINE,
            Aspect.SEXTILE
        ]
    }
}

# Timeframe configuration
TIMEFRAME_CONFIG = {
    InterpretationTimeframe.PAST: {
        "weight": 0.5,
        "lookback_years": 5,
        "include_transits": False
    },
    InterpretationTimeframe.PRESENT: {
        "weight": 1.0,
        "orb_degrees": 3,
        "include_transits": True
    },
    InterpretationTimeframe.SHORT_TERM: {
        "weight": 1.0,
        "forecast_months": 3,
        "include_transits": True
    },
    InterpretationTimeframe.MEDIUM_TERM: {
        "weight": 0.8,
        "forecast_years": 1,
        "include_transits": True
    },
    InterpretationTimeframe.LONG_TERM: {
        "weight": 0.6,
        "forecast_years": 5,
        "include_transits": False
    }
}

# Strength configuration
STRENGTH_CONFIG = {
    InterpretationStrength.VERY_STRONG: {
        "min_score": 80,
        "weight": 1.0,
        "description": "Exceptional manifestation potential"
    },
    InterpretationStrength.STRONG: {
        "min_score": 60,
        "weight": 0.8,
        "description": "Above average manifestation"
    },
    InterpretationStrength.MODERATE: {
        "min_score": 40,
        "weight": 0.6,
        "description": "Average manifestation"
    },
    InterpretationStrength.WEAK: {
        "min_score": 20,
        "weight": 0.4,
        "description": "Below average manifestation"
    },
    InterpretationStrength.VERY_WEAK: {
        "min_score": 0,
        "weight": 0.2,
        "description": "Limited manifestation potential"
    }
}

# Interpretation parameters
INTERPRETATION_PARAMS = {
    "domain_analysis": {
        "min_confidence": 0.7,
        "max_factors": 5,
        "sort_by": "strength"
    },
    "timeframe_analysis": {
        "max_periods": 5,
        "include_transits": True,
        "prediction_span": 60  # months
    },
    "strength_analysis": {
        "decimal_places": 2,
        "normalize_scores": True,
        "include_description": True
    }
}

# Template configuration
TEMPLATE_CONFIG = {
    "domain_templates": {
        "personality": {
            "very_strong": "Exceptionally strong personality traits...",
            "strong": "Well-developed personality...",
            "moderate": "Balanced personality traits...",
            "weak": "Developing personality...",
            "very_weak": "Challenging personality development..."
        },
        "career": {
            "very_strong": "Excellent career prospects...",
            "strong": "Favorable career development...",
            "moderate": "Steady career progress...",
            "weak": "Career challenges present...",
            "very_weak": "Significant career obstacles..."
        }
        # ... (similar for other domains)
    },
    "recommendation_templates": {
        "personality": {
            "very_strong": [
                "Leverage your natural leadership abilities",
                "Share your experiences to inspire others",
                "Focus on personal growth and development"
            ],
            "strong": [
                "Continue developing your strengths",
                "Take on leadership roles",
                "Mentor others in your field"
            ]
            # ... (similar for other strengths)
        }
        # ... (similar for other domains)
    }
}

def get_interpretation_config(environment: str) -> Dict[str, Any]:
    """Get interpretation configuration for environment"""
    
    base_config = {
        "domain_config": DOMAIN_CONFIG,
        "timeframe_config": TIMEFRAME_CONFIG,
        "strength_config": STRENGTH_CONFIG,
        "interpretation_params": INTERPRETATION_PARAMS,
        "template_config": TEMPLATE_CONFIG
    }
    
    if environment == "local":
        # Simplified configuration for local development
        base_config["interpretation_params"].update({
            "max_factors": 3,
            "prediction_span": 12
        })
        base_config["domain_config"] = {
            k: v for k, v in DOMAIN_CONFIG.items()
            if k in [
                InterpretationDomain.PERSONALITY,
                InterpretationDomain.CAREER
            ]
        }
    
    elif environment == "development":
        # Full configuration with debug options
        base_config["interpretation_params"].update({
            "debug_mode": True,
            "log_interpretations": True,
            "validate_results": True
        })
    
    else:  # staging and production
        # Full configuration with optimization
        base_config["interpretation_params"].update({
            "cache_results": True,
            "optimize_calculations": True,
            "parallel_processing": True
        })
    
    return base_config
