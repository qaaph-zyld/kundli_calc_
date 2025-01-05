"""
Astrological Algorithms Configuration
PGF Protocol: ALG_002
Gate: GATE_17
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
    YogaType,
    DashaSystem,
    StrengthFactor
)

# Yoga configuration
YOGA_CONFIG = {
    YogaType.RAJA: {
        "enabled": True,
        "min_strength": 60.0,
        "max_orb": 3.0,
        "required_aspects": [
            Aspect.CONJUNCTION,
            Aspect.TRINE
        ]
    },
    YogaType.DHANA: {
        "enabled": True,
        "min_strength": 50.0,
        "max_orb": 5.0,
        "required_aspects": [
            Aspect.CONJUNCTION,
            Aspect.TRINE,
            Aspect.SEXTILE
        ]
    },
    YogaType.PARIVARTANA: {
        "enabled": True,
        "min_strength": 40.0,
        "consider_aspects": True,
        "consider_houses": True
    },
    YogaType.MAHAPURUSHA: {
        "enabled": True,
        "min_strength": 70.0,
        "consider_retrograde": True,
        "consider_aspects": True
    },
    YogaType.NABHASA: {
        "enabled": True,
        "min_strength": 50.0,
        "pattern_types": [
            "rajju",
            "musala",
            "nala",
            "mala",
            "sarpa"
        ]
    }
}

# Dasha configuration
DASHA_CONFIG = {
    DashaSystem.VIMSHOTTARI: {
        "enabled": True,
        "sub_levels": 4,
        "consider_transits": True,
        "consider_aspects": True
    },
    DashaSystem.YOGINI: {
        "enabled": True,
        "sub_levels": 3,
        "consider_transits": False,
        "consider_aspects": True
    },
    DashaSystem.NARAYANA: {
        "enabled": True,
        "sub_levels": 2,
        "consider_transits": True,
        "consider_aspects": False
    }
}

# Strength calculation configuration
STRENGTH_CONFIG = {
    StrengthFactor.SHADBALA: {
        "enabled": True,
        "components": [
            "sthana_bala",
            "dig_bala",
            "kala_bala",
            "cheshta_bala",
            "naisargika_bala",
            "drik_bala"
        ],
        "weights": {
            "sthana_bala": 1.0,
            "dig_bala": 1.0,
            "kala_bala": 1.0,
            "cheshta_bala": 1.0,
            "naisargika_bala": 1.0,
            "drik_bala": 1.0
        }
    },
    StrengthFactor.ASHTAKAVARGA: {
        "enabled": True,
        "consider_transits": True,
        "consider_aspects": True,
        "bindu_weights": {
            "benefic": 1.0,
            "malefic": -0.5
        }
    },
    StrengthFactor.VIMSOPAKA: {
        "enabled": True,
        "components": [
            "sign",
            "house",
            "aspect",
            "conjunction"
        ],
        "max_score": 20
    }
}

# Algorithm parameters
ALGORITHM_PARAMS = {
    "yoga_analysis": {
        "min_confidence": 0.7,
        "max_combinations": 100,
        "sort_by": "strength"
    },
    "dasha_calculation": {
        "max_sub_periods": 5,
        "include_transits": True,
        "prediction_span": 120  # years
    },
    "strength_calculation": {
        "decimal_places": 2,
        "normalize_scores": True,
        "include_interpretation": True
    }
}

# Interpretation thresholds
INTERPRETATION_THRESHOLDS = {
    "strength": {
        "excellent": 80.0,
        "good": 60.0,
        "moderate": 40.0,
        "weak": 20.0
    },
    "yoga": {
        "powerful": 75.0,
        "significant": 50.0,
        "moderate": 25.0
    },
    "dasha": {
        "favorable": 70.0,
        "neutral": 40.0,
        "challenging": 20.0
    }
}

def get_algorithm_config(environment: str) -> Dict[str, Any]:
    """Get algorithm configuration for environment"""
    
    base_config = {
        "yoga_config": YOGA_CONFIG,
        "dasha_config": DASHA_CONFIG,
        "strength_config": STRENGTH_CONFIG,
        "algorithm_params": ALGORITHM_PARAMS,
        "interpretation_thresholds": INTERPRETATION_THRESHOLDS
    }
    
    if environment == "local":
        # Simplified configuration for local development
        base_config["yoga_config"] = {
            k: v for k, v in YOGA_CONFIG.items()
            if k in [YogaType.RAJA, YogaType.DHANA]
        }
        base_config["dasha_config"] = {
            DashaSystem.VIMSHOTTARI: DASHA_CONFIG[DashaSystem.VIMSHOTTARI]
        }
        base_config["strength_config"] = {
            StrengthFactor.SHADBALA: STRENGTH_CONFIG[StrengthFactor.SHADBALA]
        }
    
    elif environment == "development":
        # Full configuration with debug options
        base_config["algorithm_params"].update({
            "debug_mode": True,
            "log_calculations": True,
            "validate_results": True
        })
    
    else:  # staging and production
        # Full configuration with optimization
        base_config["algorithm_params"].update({
            "cache_results": True,
            "optimize_calculations": True,
            "parallel_processing": True
        })
    
    return base_config
