"""
Astrological Integration Configuration
PGF Protocol: INT_002
Gate: GATE_19
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
    IntegrationMode,
    ChartType
)

# Integration configuration
INTEGRATION_CONFIG = {
    IntegrationMode.STANDALONE: {
        "enabled": True,
        "use_caching": True,
        "calculation_method": "internal"
    },
    IntegrationMode.SWISS_EPHEMERIS: {
        "enabled": True,
        "use_caching": True,
        "calculation_method": "swiss_ephemeris",
        "ephemeris_path": "./ephe",
        "use_topocentric": True
    },
    IntegrationMode.EPHEM: {
        "enabled": True,
        "use_caching": True,
        "calculation_method": "pyephem",
        "use_topocentric": False
    },
    IntegrationMode.HYBRID: {
        "enabled": True,
        "use_caching": True,
        "calculation_method": "hybrid",
        "primary_engine": "swiss_ephemeris",
        "fallback_engine": "internal"
    }
}

# Chart type configuration
CHART_CONFIG = {
    ChartType.BIRTH: {
        "enabled": True,
        "required_calculations": [
            "positions",
            "houses",
            "aspects",
            "yogas",
            "dashas",
            "strengths",
            "interpretation"
        ],
        "calculation_mode": "high_precision"
    },
    ChartType.TRANSIT: {
        "enabled": True,
        "required_calculations": [
            "positions",
            "aspects",
            "interpretation"
        ],
        "calculation_mode": "standard"
    },
    ChartType.PROGRESSION: {
        "enabled": True,
        "required_calculations": [
            "positions",
            "aspects",
            "interpretation"
        ],
        "calculation_mode": "standard",
        "progression_method": "secondary"
    },
    ChartType.SOLAR_RETURN: {
        "enabled": True,
        "required_calculations": [
            "positions",
            "houses",
            "aspects",
            "interpretation"
        ],
        "calculation_mode": "high_precision"
    },
    ChartType.COMPOSITE: {
        "enabled": True,
        "required_calculations": [
            "positions",
            "houses",
            "aspects",
            "interpretation"
        ],
        "calculation_mode": "standard",
        "composite_method": "midpoint"
    }
}

# Calculation parameters
CALCULATION_PARAMS = {
    "high_precision": {
        "position_decimals": 8,
        "house_decimals": 6,
        "aspect_orb_precision": 0.0001,
        "time_precision": "microsecond"
    },
    "standard": {
        "position_decimals": 4,
        "house_decimals": 4,
        "aspect_orb_precision": 0.01,
        "time_precision": "second"
    },
    "quick": {
        "position_decimals": 2,
        "house_decimals": 2,
        "aspect_orb_precision": 0.1,
        "time_precision": "minute"
    }
}

# Cache configuration
CACHE_CONFIG = {
    "enabled": True,
    "backend": "redis",
    "ttl": 3600,  # 1 hour
    "max_size": 10000,
    "compression": True
}

# Optimization settings
OPTIMIZATION_CONFIG = {
    "parallel_processing": True,
    "batch_size": 100,
    "thread_pool_size": 4,
    "use_gpu": False
}

def get_integration_config(environment: str) -> Dict[str, Any]:
    """Get integration configuration for environment"""
    
    base_config = {
        "integration_config": INTEGRATION_CONFIG,
        "chart_config": CHART_CONFIG,
        "calculation_params": CALCULATION_PARAMS,
        "cache_config": CACHE_CONFIG,
        "optimization_config": OPTIMIZATION_CONFIG
    }
    
    if environment == "local":
        # Simplified configuration for local development
        base_config["integration_config"] = {
            IntegrationMode.STANDALONE: INTEGRATION_CONFIG[IntegrationMode.STANDALONE]
        }
        base_config["chart_config"] = {
            k: v for k, v in CHART_CONFIG.items()
            if k in [ChartType.BIRTH, ChartType.TRANSIT]
        }
        base_config["calculation_params"] = {
            "standard": CALCULATION_PARAMS["standard"],
            "quick": CALCULATION_PARAMS["quick"]
        }
        base_config["cache_config"]["enabled"] = False
        base_config["optimization_config"]["parallel_processing"] = False
    
    elif environment == "development":
        # Full configuration with debug options
        base_config["integration_config"][IntegrationMode.HYBRID].update({
            "debug_mode": True,
            "log_calculations": True,
            "validate_results": True
        })
        base_config["cache_config"]["ttl"] = 300  # 5 minutes
    
    else:  # staging and production
        # Full configuration with optimization
        base_config["integration_config"][IntegrationMode.HYBRID].update({
            "use_caching": True,
            "optimize_calculations": True
        })
        base_config["optimization_config"].update({
            "parallel_processing": True,
            "batch_size": 1000,
            "thread_pool_size": 8,
            "use_gpu": True
        })
    
    return base_config
