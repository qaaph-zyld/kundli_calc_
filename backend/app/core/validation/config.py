"""
Astrological Validation Configuration
PGF Protocol: VAL_002
Gate: GATE_20
Version: 1.0.0
"""

from typing import Dict, Any, List
from ..astronomical.framework import CelestialBody
from .framework import (
    ValidationLevel,
    ValidationScope
)

# Validation configuration
VALIDATION_CONFIG = {
    ValidationLevel.BASIC: {
        "enabled": True,
        "check_ranges": True,
        "check_sequences": False,
        "check_relationships": False,
        "metrics_enabled": False
    },
    ValidationLevel.STANDARD: {
        "enabled": True,
        "check_ranges": True,
        "check_sequences": True,
        "check_relationships": True,
        "metrics_enabled": True
    },
    ValidationLevel.STRICT: {
        "enabled": True,
        "check_ranges": True,
        "check_sequences": True,
        "check_relationships": True,
        "check_advanced": True,
        "metrics_enabled": True
    },
    ValidationLevel.RESEARCH: {
        "enabled": True,
        "check_ranges": True,
        "check_sequences": True,
        "check_relationships": True,
        "check_advanced": True,
        "check_research": True,
        "metrics_enabled": True
    }
}

# Scope configuration
SCOPE_CONFIG = {
    ValidationScope.ASTRONOMICAL: {
        "enabled": True,
        "validate_positions": True,
        "validate_houses": True,
        "validate_speeds": True,
        "validate_distances": True
    },
    ValidationScope.MATHEMATICAL: {
        "enabled": True,
        "validate_aspects": True,
        "validate_angles": True,
        "validate_calculations": True,
        "validate_progressions": True
    },
    ValidationScope.ASTROLOGICAL: {
        "enabled": True,
        "validate_yogas": True,
        "validate_dashas": True,
        "validate_strengths": True,
        "validate_dignities": True
    },
    ValidationScope.INTERPRETATIVE: {
        "enabled": True,
        "validate_domains": True,
        "validate_descriptions": True,
        "validate_recommendations": True,
        "validate_factors": True
    },
    ValidationScope.COMPREHENSIVE: {
        "enabled": True,
        "validate_all": True,
        "cross_validate": True,
        "validate_consistency": True,
        "validate_completeness": True
    }
}

# Validation thresholds
VALIDATION_THRESHOLDS = {
    "position": {
        "longitude_min": 0,
        "longitude_max": 360,
        "latitude_min": -90,
        "latitude_max": 90,
        "speed_max": 2,  # degrees per day
        "distance_min": 0
    },
    "aspect": {
        "orb_max": 10,
        "strength_min": 0,
        "strength_max": 100
    },
    "yoga": {
        "strength_min": 0,
        "strength_max": 100,
        "factor_min": 3
    },
    "dasha": {
        "strength_min": 0,
        "strength_max": 100,
        "duration_min": 1  # year
    },
    "interpretation": {
        "strength_min": 0,
        "strength_max": 100,
        "factor_min": 2
    }
}

# Required elements
REQUIRED_ELEMENTS = {
    "planets": [
        CelestialBody.SUN,
        CelestialBody.MOON,
        CelestialBody.MARS,
        CelestialBody.MERCURY,
        CelestialBody.JUPITER,
        CelestialBody.VENUS,
        CelestialBody.SATURN
    ],
    "houses": list(range(1, 13)),
    "aspects": ["conjunction", "opposition", "trine", "square"],
    "domains": [
        "personality",
        "career",
        "relationships",
        "health",
        "spirituality"
    ]
}

# Metrics configuration
METRICS_CONFIG = {
    "enabled": True,
    "astronomical": [
        "mean_planet_speed",
        "retrograde_count"
    ],
    "mathematical": [
        "aspect_count",
        "mean_orb"
    ],
    "astrological": [
        "yoga_count",
        "mean_yoga_strength"
    ],
    "interpretative": [
        "interpretation_completeness",
        "recommendation_count"
    ]
}

def get_validation_config(environment: str) -> Dict[str, Any]:
    """Get validation configuration for environment"""
    
    base_config = {
        "validation_config": VALIDATION_CONFIG,
        "scope_config": SCOPE_CONFIG,
        "validation_thresholds": VALIDATION_THRESHOLDS,
        "required_elements": REQUIRED_ELEMENTS,
        "metrics_config": METRICS_CONFIG
    }
    
    if environment == "local":
        # Simplified configuration for local development
        base_config["validation_config"] = {
            ValidationLevel.BASIC: VALIDATION_CONFIG[ValidationLevel.BASIC]
        }
        base_config["scope_config"] = {
            ValidationScope.ASTRONOMICAL: SCOPE_CONFIG[ValidationScope.ASTRONOMICAL],
            ValidationScope.MATHEMATICAL: SCOPE_CONFIG[ValidationScope.MATHEMATICAL]
        }
        base_config["metrics_config"]["enabled"] = False
    
    elif environment == "development":
        # Full configuration with debug options
        base_config["validation_config"][ValidationLevel.STANDARD].update({
            "debug_mode": True,
            "log_validations": True
        })
        base_config["metrics_config"]["debug"] = True
    
    else:  # staging and production
        # Full configuration with optimization
        base_config["validation_config"][ValidationLevel.STRICT].update({
            "optimize_validations": True,
            "cache_results": True
        })
        base_config["metrics_config"].update({
            "store_history": True,
            "analyze_trends": True
        })
    
    return base_config
