"""
Deployment Configuration
PGF Protocol: DEP_002
Gate: GATE_9
Version: 1.0.0
"""

from typing import Dict, Any
from .framework import (
    DeploymentConfig,
    DeploymentEnvironment,
    DeploymentMode,
    ServiceType,
    ServiceConfig,
    ResourceRequirements,
    HealthCheck
)

def get_deployment_config(environment: DeploymentEnvironment) -> DeploymentConfig:
    """Get deployment configuration for environment"""
    
    # Base configuration
    base_config = {
        "environment": environment,
        "mode": DeploymentMode.DOCKER if environment in [
            DeploymentEnvironment.LOCAL,
            DeploymentEnvironment.DEVELOPMENT
        ] else DeploymentMode.KUBERNETES,
        "namespace": f"vedic-astrology-{environment}",
        "network": f"vedic-astrology-{environment}",
        "registry": "vedic-astrology" if environment != DeploymentEnvironment.LOCAL else None,
        "monitoring": environment != DeploymentEnvironment.LOCAL,
        "logging": environment != DeploymentEnvironment.LOCAL,
        "global_env_vars": {
            "ENV": environment,
            "LOG_LEVEL": "DEBUG" if environment in [
                DeploymentEnvironment.LOCAL,
                DeploymentEnvironment.DEVELOPMENT
            ] else "INFO"
        }
    }
    
    # Service configurations
    services = {
        "api": ServiceConfig(
            name="api",
            type=ServiceType.API,
            image="vedic-astrology/api",
            tag="latest",
            port=8000,
            env_vars={
                "API_TITLE": "Vedic Astrology API",
                "API_VERSION": "1.0.0",
                "DATABASE_URL": get_database_url(environment),
                "REDIS_URL": get_redis_url(environment)
            },
            resources=ResourceRequirements(
                cpu="100m" if environment == DeploymentEnvironment.LOCAL else "500m",
                memory="128Mi" if environment == DeploymentEnvironment.LOCAL else "512Mi",
                replicas=1 if environment in [
                    DeploymentEnvironment.LOCAL,
                    DeploymentEnvironment.DEVELOPMENT
                ] else 3,
                min_replicas=1,
                max_replicas=1 if environment in [
                    DeploymentEnvironment.LOCAL,
                    DeploymentEnvironment.DEVELOPMENT
                ] else 5
            ),
            health_check=HealthCheck(
                path="/health",
                port=8000,
                initial_delay=30,
                period=10,
                timeout=5,
                success_threshold=1,
                failure_threshold=3
            ),
            dependencies=["cache", "database"]
        ),
        
        "worker": ServiceConfig(
            name="worker",
            type=ServiceType.WORKER,
            image="vedic-astrology/worker",
            tag="latest",
            port=8001,
            env_vars={
                "WORKER_CONCURRENCY": "1" if environment == DeploymentEnvironment.LOCAL else "5",
                "DATABASE_URL": get_database_url(environment),
                "REDIS_URL": get_redis_url(environment)
            },
            resources=ResourceRequirements(
                cpu="100m" if environment == DeploymentEnvironment.LOCAL else "500m",
                memory="128Mi" if environment == DeploymentEnvironment.LOCAL else "512Mi",
                replicas=1 if environment in [
                    DeploymentEnvironment.LOCAL,
                    DeploymentEnvironment.DEVELOPMENT
                ] else 2
            ),
            health_check=HealthCheck(
                path="/health",
                port=8001,
                initial_delay=30,
                period=10,
                timeout=5,
                success_threshold=1,
                failure_threshold=3
            ),
            dependencies=["cache", "database"]
        ),
        
        "cache": ServiceConfig(
            name="cache",
            type=ServiceType.CACHE,
            image="redis",
            tag="6.2-alpine",
            port=6379,
            resources=ResourceRequirements(
                cpu="100m" if environment == DeploymentEnvironment.LOCAL else "200m",
                memory="128Mi" if environment == DeploymentEnvironment.LOCAL else "256Mi",
                replicas=1
            ),
            health_check=HealthCheck(
                path="/",
                port=6379,
                initial_delay=5,
                period=10,
                timeout=5,
                success_threshold=1,
                failure_threshold=3
            ),
            volumes={
                "./data/redis": "/data"
            }
        ),
        
        "database": ServiceConfig(
            name="database",
            type=ServiceType.DATABASE,
            image="postgres",
            tag="13-alpine",
            port=5432,
            env_vars={
                "POSTGRES_DB": "vedic_astrology",
                "POSTGRES_USER": "vedic",
                "POSTGRES_PASSWORD": get_database_password(environment)
            },
            resources=ResourceRequirements(
                cpu="100m" if environment == DeploymentEnvironment.LOCAL else "500m",
                memory="256Mi" if environment == DeploymentEnvironment.LOCAL else "1Gi",
                replicas=1
            ),
            health_check=HealthCheck(
                path="/",
                port=5432,
                initial_delay=30,
                period=10,
                timeout=5,
                success_threshold=1,
                failure_threshold=3
            ),
            volumes={
                "./data/postgres": "/var/lib/postgresql/data"
            }
        ),
        
        "frontend": ServiceConfig(
            name="frontend",
            type=ServiceType.FRONTEND,
            image="vedic-astrology/frontend",
            tag="latest",
            port=3000,
            env_vars={
                "REACT_APP_API_URL": get_api_url(environment),
                "REACT_APP_ENV": environment
            },
            resources=ResourceRequirements(
                cpu="100m" if environment == DeploymentEnvironment.LOCAL else "200m",
                memory="128Mi" if environment == DeploymentEnvironment.LOCAL else "256Mi",
                replicas=1 if environment in [
                    DeploymentEnvironment.LOCAL,
                    DeploymentEnvironment.DEVELOPMENT
                ] else 2
            ),
            health_check=HealthCheck(
                path="/health",
                port=3000,
                initial_delay=30,
                period=10,
                timeout=5,
                success_threshold=1,
                failure_threshold=3
            ),
            dependencies=["api"]
        )
    }
    
    return DeploymentConfig(
        **base_config,
        services=services
    )

def get_database_url(environment: DeploymentEnvironment) -> str:
    """Get database URL for environment"""
    if environment == DeploymentEnvironment.LOCAL:
        return "postgresql://vedic:vedic@database:5432/vedic_astrology"
    else:
        return f"postgresql://vedic:{get_database_password(environment)}@database:5432/vedic_astrology"

def get_redis_url(environment: DeploymentEnvironment) -> str:
    """Get Redis URL for environment"""
    return "redis://cache:6379/0"

def get_api_url(environment: DeploymentEnvironment) -> str:
    """Get API URL for environment"""
    if environment == DeploymentEnvironment.LOCAL:
        return "http://localhost:8000"
    elif environment == DeploymentEnvironment.DEVELOPMENT:
        return "https://dev-api.vedic-astrology.com"
    elif environment == DeploymentEnvironment.STAGING:
        return "https://staging-api.vedic-astrology.com"
    else:
        return "https://api.vedic-astrology.com"

def get_database_password(environment: DeploymentEnvironment) -> str:
    """Get database password for environment"""
    if environment == DeploymentEnvironment.LOCAL:
        return "vedic"
    else:
        # In production, this should be retrieved from a secure secret store
        return "vedic_secure_password"
