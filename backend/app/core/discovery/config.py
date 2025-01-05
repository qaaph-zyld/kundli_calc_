"""
Service Discovery Configuration
PGF Protocol: DSC_002
Gate: GATE_14
Version: 1.0.0
"""

from typing import Dict, List
import uuid
from .framework import (
    RegistryType,
    ServiceStatus,
    ServiceEndpoint,
    ServiceMetadata,
    ServiceInstance,
    DiscoveryConfig
)

def get_discovery_config(environment: str) -> DiscoveryConfig:
    """Get discovery configuration for environment"""
    
    if environment == "local":
        return DiscoveryConfig(
            registry_type=RegistryType.CONSUL,
            registry_urls=["localhost:8500"],
            service_ttl=30,
            health_check_interval=10,
            deregistration_delay=60,
            auto_sync_interval=30
        )
    
    elif environment == "development":
        return DiscoveryConfig(
            registry_type=RegistryType.CONSUL,
            registry_urls=[
                "consul-1.dev.vedic-astrology.com:8500",
                "consul-2.dev.vedic-astrology.com:8500",
                "consul-3.dev.vedic-astrology.com:8500"
            ],
            service_ttl=30,
            health_check_interval=10,
            deregistration_delay=60,
            auto_sync_interval=30
        )
    
    elif environment == "staging":
        return DiscoveryConfig(
            registry_type=RegistryType.ETCD,
            registry_urls=[
                "etcd-1.staging.vedic-astrology.com:2379",
                "etcd-2.staging.vedic-astrology.com:2379",
                "etcd-3.staging.vedic-astrology.com:2379"
            ],
            service_ttl=30,
            health_check_interval=10,
            deregistration_delay=60,
            auto_sync_interval=30
        )
    
    else:  # production
        return DiscoveryConfig(
            registry_type=RegistryType.ETCD,
            registry_urls=[
                "etcd-1.vedic-astrology.com:2379",
                "etcd-2.vedic-astrology.com:2379",
                "etcd-3.vedic-astrology.com:2379",
                "etcd-4.vedic-astrology.com:2379",
                "etcd-5.vedic-astrology.com:2379"
            ],
            service_ttl=30,
            health_check_interval=10,
            deregistration_delay=60,
            auto_sync_interval=30
        )

def create_service_instance(
    name: str,
    host: str,
    port: int,
    environment: str,
    region: str = "us-east-1",
    datacenter: str = "dc1"
) -> ServiceInstance:
    """Create service instance"""
    
    # Define service endpoints
    endpoints: List[ServiceEndpoint] = []
    
    if name == "api":
        endpoints = [
            ServiceEndpoint(
                path="/api/v1/kundli/calculate",
                methods=["POST"],
                auth_required=True,
                rate_limited=True,
                cached=True,
                version="v1"
            ),
            ServiceEndpoint(
                path="/api/v1/kundli/analyze",
                methods=["POST"],
                auth_required=True,
                rate_limited=True,
                cached=True,
                version="v1"
            ),
            ServiceEndpoint(
                path="/api/v1/health",
                methods=["GET"],
                auth_required=False,
                rate_limited=False,
                cached=False,
                version="v1"
            )
        ]
    
    elif name == "auth":
        endpoints = [
            ServiceEndpoint(
                path="/api/v1/auth/login",
                methods=["POST"],
                auth_required=False,
                rate_limited=True,
                cached=False,
                version="v1"
            ),
            ServiceEndpoint(
                path="/api/v1/auth/refresh",
                methods=["POST"],
                auth_required=False,
                rate_limited=True,
                cached=False,
                version="v1"
            ),
            ServiceEndpoint(
                path="/api/v1/health",
                methods=["GET"],
                auth_required=False,
                rate_limited=False,
                cached=False,
                version="v1"
            )
        ]
    
    elif name == "admin":
        endpoints = [
            ServiceEndpoint(
                path="/api/v1/admin/users",
                methods=["GET", "POST", "PUT", "DELETE"],
                auth_required=True,
                rate_limited=True,
                cached=False,
                version="v1"
            ),
            ServiceEndpoint(
                path="/api/v1/admin/metrics",
                methods=["GET"],
                auth_required=True,
                rate_limited=True,
                cached=True,
                version="v1"
            ),
            ServiceEndpoint(
                path="/api/v1/health",
                methods=["GET"],
                auth_required=False,
                rate_limited=False,
                cached=False,
                version="v1"
            )
        ]
    
    # Create service metadata
    metadata = ServiceMetadata(
        version="1.0.0",
        environment=environment,
        region=region,
        datacenter=datacenter,
        tags=[
            name,
            environment,
            region,
            datacenter,
            "vedic-astrology"
        ],
        endpoints=endpoints
    )
    
    # Create service instance
    return ServiceInstance(
        id=str(uuid.uuid4()),
        name=name,
        host=host,
        port=port,
        status=ServiceStatus.STARTING,
        metadata=metadata,
        health_check_url=f"http://{host}:{port}/health"
    )
