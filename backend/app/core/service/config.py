"""
Service Integration Configuration
PGF Protocol: SVC_002
Gate: GATE_22
Version: 1.0.0
"""

from typing import Dict, Any, List
from .framework import (
    ServiceMode,
    ServiceTier,
    ServiceEndpoint
)

# Service configuration
SERVICE_CONFIG = {
    ServiceMode.DEVELOPMENT: {
        "enabled": True,
        "debug": True,
        "logging": "debug",
        "monitoring": True,
        "tracing": True,
        "profiling": True
    },
    ServiceMode.STAGING: {
        "enabled": True,
        "debug": False,
        "logging": "info",
        "monitoring": True,
        "tracing": True,
        "profiling": False
    },
    ServiceMode.PRODUCTION: {
        "enabled": True,
        "debug": False,
        "logging": "warning",
        "monitoring": True,
        "tracing": True,
        "profiling": False
    }
}

# Tier configuration
TIER_CONFIG = {
    ServiceTier.BASIC: {
        "enabled": True,
        "request_limit": 100,
        "concurrent_limit": 2,
        "cache_size": 256,
        "features": [
            "birth_chart",
            "transit_chart"
        ]
    },
    ServiceTier.STANDARD: {
        "enabled": True,
        "request_limit": 1000,
        "concurrent_limit": 5,
        "cache_size": 512,
        "features": [
            "birth_chart",
            "transit_chart",
            "progression_chart"
        ]
    },
    ServiceTier.PREMIUM: {
        "enabled": True,
        "request_limit": 10000,
        "concurrent_limit": 10,
        "cache_size": 1024,
        "features": [
            "birth_chart",
            "transit_chart",
            "progression_chart",
            "compatibility_chart"
        ]
    },
    ServiceTier.ENTERPRISE: {
        "enabled": True,
        "request_limit": None,
        "concurrent_limit": None,
        "cache_size": 2048,
        "features": [
            "birth_chart",
            "transit_chart",
            "progression_chart",
            "compatibility_chart",
            "prediction_chart"
        ]
    }
}

# Endpoint configuration
ENDPOINT_CONFIG = {
    ServiceEndpoint.CHART: {
        "enabled": True,
        "rate_limit": 10,
        "timeout": 30,
        "cache_ttl": 3600
    },
    ServiceEndpoint.TRANSIT: {
        "enabled": True,
        "rate_limit": 20,
        "timeout": 20,
        "cache_ttl": 1800
    },
    ServiceEndpoint.PROGRESSION: {
        "enabled": True,
        "rate_limit": 10,
        "timeout": 30,
        "cache_ttl": 3600
    },
    ServiceEndpoint.COMPATIBILITY: {
        "enabled": True,
        "rate_limit": 5,
        "timeout": 60,
        "cache_ttl": 7200
    },
    ServiceEndpoint.PREDICTION: {
        "enabled": True,
        "rate_limit": 2,
        "timeout": 120,
        "cache_ttl": 14400
    }
}

# Security configuration
SECURITY_CONFIG = {
    "authentication": {
        "enabled": True,
        "provider": "oauth2",
        "token_expiry": 3600,
        "refresh_enabled": True
    },
    "authorization": {
        "enabled": True,
        "role_based": True,
        "scope_based": True
    },
    "encryption": {
        "enabled": True,
        "algorithm": "AES-256",
        "key_rotation": True
    },
    "rate_limiting": {
        "enabled": True,
        "strategy": "token_bucket",
        "window_size": 3600
    }
}

# Monitoring configuration
MONITORING_CONFIG = {
    "metrics": {
        "enabled": True,
        "interval": 60,
        "exporters": ["prometheus"]
    },
    "logging": {
        "enabled": True,
        "level": "info",
        "format": "json"
    },
    "tracing": {
        "enabled": True,
        "sampling_rate": 0.1,
        "exporters": ["jaeger"]
    },
    "alerting": {
        "enabled": True,
        "channels": ["email", "slack"],
        "thresholds": {
            "error_rate": 0.01,
            "latency_p95": 1000,
            "success_rate": 0.99
        }
    }
}

def get_service_config(environment: str) -> Dict[str, Any]:
    """Get service configuration for environment"""
    
    base_config = {
        "service_config": SERVICE_CONFIG,
        "tier_config": TIER_CONFIG,
        "endpoint_config": ENDPOINT_CONFIG,
        "security_config": SECURITY_CONFIG,
        "monitoring_config": MONITORING_CONFIG
    }
    
    if environment == "local":
        # Simplified configuration for local development
        base_config["service_config"] = {
            ServiceMode.DEVELOPMENT: SERVICE_CONFIG[ServiceMode.DEVELOPMENT]
        }
        base_config["tier_config"] = {
            ServiceTier.BASIC: TIER_CONFIG[ServiceTier.BASIC]
        }
        base_config["security_config"]["authentication"]["enabled"] = False
        base_config["monitoring_config"]["enabled"] = False
    
    elif environment == "development":
        # Full configuration with debug options
        base_config["service_config"][ServiceMode.DEVELOPMENT].update({
            "debug_endpoints": True,
            "mock_services": True
        })
        base_config["monitoring_config"]["logging"]["level"] = "debug"
    
    else:  # staging and production
        # Full configuration with security
        base_config["security_config"].update({
            "ssl_required": True,
            "ip_whitelist": True
        })
        base_config["monitoring_config"]["alerting"]["enabled"] = True
    
    return base_config
