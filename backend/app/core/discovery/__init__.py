"""
Service Discovery Module
PGF Protocol: DSC_003
Gate: GATE_14
Version: 1.0.0
"""

from .config import create_service_instance, get_discovery_config
from .framework import (
    ConsulRegistry,
    DiscoveryConfig,
    EtcdRegistry,
    RegistryType,
    ServiceDiscovery,
    ServiceEndpoint,
    ServiceInstance,
    ServiceMetadata,
    ServiceRegistry,
    ServiceStatus,
)

__all__ = [
    "RegistryType",
    "ServiceStatus",
    "ServiceEndpoint",
    "ServiceMetadata",
    "ServiceInstance",
    "DiscoveryConfig",
    "ServiceRegistry",
    "ConsulRegistry",
    "EtcdRegistry",
    "ServiceDiscovery",
    "get_discovery_config",
    "create_service_instance",
]
