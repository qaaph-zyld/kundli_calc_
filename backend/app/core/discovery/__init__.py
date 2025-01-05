"""
Service Discovery Module
PGF Protocol: DSC_003
Gate: GATE_14
Version: 1.0.0
"""

from .framework import (
    RegistryType,
    ServiceStatus,
    ServiceEndpoint,
    ServiceMetadata,
    ServiceInstance,
    DiscoveryConfig,
    ServiceRegistry,
    ConsulRegistry,
    EtcdRegistry,
    ServiceDiscovery
)
from .config import (
    get_discovery_config,
    create_service_instance
)

__all__ = [
    'RegistryType',
    'ServiceStatus',
    'ServiceEndpoint',
    'ServiceMetadata',
    'ServiceInstance',
    'DiscoveryConfig',
    'ServiceRegistry',
    'ConsulRegistry',
    'EtcdRegistry',
    'ServiceDiscovery',
    'get_discovery_config',
    'create_service_instance'
]
