"""
Service Discovery Framework
PGF Protocol: DSC_001
Gate: GATE_14
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Set, Callable
from enum import Enum
from datetime import datetime, timedelta
import asyncio
import json
import aiohttp
from pydantic import BaseModel, Field
import consul.aio
import etcd3.aio as etcd3
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)

class RegistryType(str, Enum):
    """Service registry types"""
    CONSUL = "consul"
    ETCD = "etcd"
    ZOOKEEPER = "zookeeper"
    EUREKA = "eureka"

class ServiceStatus(str, Enum):
    """Service status"""
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"

class ServiceEndpoint(BaseModel):
    """Service endpoint"""
    
    path: str
    methods: List[str]
    auth_required: bool = True
    rate_limited: bool = False
    cached: bool = False
    deprecated: bool = False
    version: str = "v1"

class ServiceMetadata(BaseModel):
    """Service metadata"""
    
    version: str
    environment: str
    region: str
    datacenter: str
    tags: List[str] = Field(default_factory=list)
    endpoints: List[ServiceEndpoint] = Field(default_factory=list)

class ServiceInstance(BaseModel):
    """Service instance"""
    
    id: str
    name: str
    host: str
    port: int
    status: ServiceStatus
    metadata: ServiceMetadata
    health_check_url: str
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow)
    registration_time: datetime = Field(default_factory=datetime.utcnow)

class DiscoveryConfig(BaseModel):
    """Discovery configuration"""
    
    registry_type: RegistryType
    registry_urls: List[str]
    service_ttl: int = 30
    health_check_interval: int = 10
    deregistration_delay: int = 60
    auto_sync_interval: int = 30

class ServiceRegistry:
    """Service registry base class"""
    
    def __init__(self, config: DiscoveryConfig):
        self.config = config
        self._instances: Dict[str, Dict[str, ServiceInstance]] = {}
        self._watchers: Dict[str, Set[Callable]] = {}
    
    async def register(
        self,
        instance: ServiceInstance
    ) -> None:
        """Register service instance"""
        raise NotImplementedError
    
    async def deregister(
        self,
        service_name: str,
        instance_id: str
    ) -> None:
        """Deregister service instance"""
        raise NotImplementedError
    
    async def get_instances(
        self,
        service_name: str
    ) -> List[ServiceInstance]:
        """Get service instances"""
        raise NotImplementedError
    
    async def watch_service(
        self,
        service_name: str,
        callback: Callable[[List[ServiceInstance]], None]
    ) -> None:
        """Watch service for changes"""
        raise NotImplementedError
    
    async def unwatch_service(
        self,
        service_name: str,
        callback: Callable[[List[ServiceInstance]], None]
    ) -> None:
        """Unwatch service"""
        if service_name in self._watchers:
            self._watchers[service_name].remove(callback)

class ConsulRegistry(ServiceRegistry):
    """Consul service registry"""
    
    def __init__(self, config: DiscoveryConfig):
        super().__init__(config)
        self.client = consul.aio.Consul(
            host=config.registry_urls[0].split(":")[0],
            port=int(config.registry_urls[0].split(":")[1])
        )
    
    async def register(
        self,
        instance: ServiceInstance
    ) -> None:
        """Register service instance in Consul"""
        try:
            service_id = f"{instance.name}-{instance.id}"
            
            # Create service check
            check = {
                "http": instance.health_check_url,
                "interval": f"{self.config.health_check_interval}s",
                "timeout": "5s",
                "deregister_critical_service_after": 
                    f"{self.config.deregistration_delay}s"
            }
            
            # Register service
            await self.client.agent.service.register(
                name=instance.name,
                service_id=service_id,
                address=instance.host,
                port=instance.port,
                tags=instance.metadata.tags,
                check=check,
                meta={
                    "version": instance.metadata.version,
                    "environment": instance.metadata.environment,
                    "region": instance.metadata.region,
                    "datacenter": instance.metadata.datacenter,
                    "endpoints": json.dumps([
                        endpoint.dict() for endpoint in instance.metadata.endpoints
                    ])
                }
            )
            
            # Store instance locally
            if instance.name not in self._instances:
                self._instances[instance.name] = {}
            self._instances[instance.name][instance.id] = instance
            
        except Exception as e:
            raise AppError(
                code=ErrorCode.SERVICE_REGISTRATION_ERROR,
                message="Failed to register service in Consul",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                details={"error": str(e)}
            )
    
    async def deregister(
        self,
        service_name: str,
        instance_id: str
    ) -> None:
        """Deregister service instance from Consul"""
        try:
            service_id = f"{service_name}-{instance_id}"
            await self.client.agent.service.deregister(service_id)
            
            if (service_name in self._instances and
                    instance_id in self._instances[service_name]):
                del self._instances[service_name][instance_id]
                
        except Exception as e:
            raise AppError(
                code=ErrorCode.SERVICE_DEREGISTRATION_ERROR,
                message="Failed to deregister service from Consul",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                details={"error": str(e)}
            )
    
    async def get_instances(
        self,
        service_name: str
    ) -> List[ServiceInstance]:
        """Get service instances from Consul"""
        try:
            # Get service catalog
            _, services = await self.client.health.service(
                service_name,
                passing=True
            )
            
            instances = []
            for service in services:
                service_data = service["Service"]
                
                # Parse metadata
                meta = service_data.get("Meta", {})
                endpoints = json.loads(meta.get("endpoints", "[]"))
                
                instance = ServiceInstance(
                    id=service_data["ID"].split("-")[-1],
                    name=service_data["Service"],
                    host=service_data["Address"],
                    port=service_data["Port"],
                    status=ServiceStatus.RUNNING,
                    metadata=ServiceMetadata(
                        version=meta.get("version", "unknown"),
                        environment=meta.get("environment", "unknown"),
                        region=meta.get("region", "unknown"),
                        datacenter=meta.get("datacenter", "unknown"),
                        tags=service_data.get("Tags", []),
                        endpoints=[
                            ServiceEndpoint(**endpoint)
                            for endpoint in endpoints
                        ]
                    ),
                    health_check_url=f"http://{service_data['Address']}:"
                                   f"{service_data['Port']}/health"
                )
                instances.append(instance)
            
            return instances
            
        except Exception as e:
            raise AppError(
                code=ErrorCode.SERVICE_DISCOVERY_ERROR,
                message="Failed to get service instances from Consul",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                details={"error": str(e)}
            )
    
    async def watch_service(
        self,
        service_name: str,
        callback: Callable[[List[ServiceInstance]], None]
    ) -> None:
        """Watch service for changes in Consul"""
        if service_name not in self._watchers:
            self._watchers[service_name] = set()
        self._watchers[service_name].add(callback)
        
        async def watch_loop():
            index = None
            while True:
                try:
                    index, services = await self.client.health.service(
                        service_name,
                        index=index,
                        passing=True
                    )
                    instances = await self.get_instances(service_name)
                    for cb in self._watchers[service_name]:
                        cb(instances)
                except Exception:
                    await asyncio.sleep(5)
        
        asyncio.create_task(watch_loop())

class EtcdRegistry(ServiceRegistry):
    """Etcd service registry"""
    
    def __init__(self, config: DiscoveryConfig):
        super().__init__(config)
        host, port = config.registry_urls[0].split(":")
        self.client = etcd3.client(host=host, port=int(port))
    
    async def register(
        self,
        instance: ServiceInstance
    ) -> None:
        """Register service instance in Etcd"""
        try:
            key = f"/services/{instance.name}/{instance.id}"
            value = instance.json()
            lease = await self.client.lease(self.config.service_ttl)
            await self.client.put(key, value, lease=lease)
            
            if instance.name not in self._instances:
                self._instances[instance.name] = {}
            self._instances[instance.name][instance.id] = instance
            
            # Start TTL refresh loop
            async def refresh_loop():
                while True:
                    await asyncio.sleep(self.config.service_ttl // 2)
                    try:
                        await lease.refresh()
                    except Exception:
                        break
            
            asyncio.create_task(refresh_loop())
            
        except Exception as e:
            raise AppError(
                code=ErrorCode.SERVICE_REGISTRATION_ERROR,
                message="Failed to register service in Etcd",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                details={"error": str(e)}
            )
    
    async def deregister(
        self,
        service_name: str,
        instance_id: str
    ) -> None:
        """Deregister service instance from Etcd"""
        try:
            key = f"/services/{service_name}/{instance_id}"
            await self.client.delete(key)
            
            if (service_name in self._instances and
                    instance_id in self._instances[service_name]):
                del self._instances[service_name][instance_id]
                
        except Exception as e:
            raise AppError(
                code=ErrorCode.SERVICE_DEREGISTRATION_ERROR,
                message="Failed to deregister service from Etcd",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                details={"error": str(e)}
            )
    
    async def get_instances(
        self,
        service_name: str
    ) -> List[ServiceInstance]:
        """Get service instances from Etcd"""
        try:
            prefix = f"/services/{service_name}/"
            instances = []
            
            async for value, _ in self.client.get_prefix(prefix):
                instance = ServiceInstance.parse_raw(value)
                instances.append(instance)
            
            return instances
            
        except Exception as e:
            raise AppError(
                code=ErrorCode.SERVICE_DISCOVERY_ERROR,
                message="Failed to get service instances from Etcd",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                details={"error": str(e)}
            )
    
    async def watch_service(
        self,
        service_name: str,
        callback: Callable[[List[ServiceInstance]], None]
    ) -> None:
        """Watch service for changes in Etcd"""
        if service_name not in self._watchers:
            self._watchers[service_name] = set()
        self._watchers[service_name].add(callback)
        
        async def watch_loop():
            prefix = f"/services/{service_name}/"
            async for event in self.client.watch_prefix(prefix):
                try:
                    instances = await self.get_instances(service_name)
                    for cb in self._watchers[service_name]:
                        cb(instances)
                except Exception:
                    await asyncio.sleep(5)
        
        asyncio.create_task(watch_loop())

class ServiceDiscovery:
    """Service discovery"""
    
    def __init__(self, config: DiscoveryConfig):
        self.config = config
        self.registry = self._create_registry()
    
    def _create_registry(self) -> ServiceRegistry:
        """Create service registry based on configuration"""
        if self.config.registry_type == RegistryType.CONSUL:
            return ConsulRegistry(self.config)
        elif self.config.registry_type == RegistryType.ETCD:
            return EtcdRegistry(self.config)
        else:
            raise AppError(
                code=ErrorCode.INVALID_CONFIGURATION,
                message=f"Unsupported registry type: {self.config.registry_type}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH
            )
    
    async def register_service(
        self,
        instance: ServiceInstance
    ) -> None:
        """Register service instance"""
        await self.registry.register(instance)
    
    async def deregister_service(
        self,
        service_name: str,
        instance_id: str
    ) -> None:
        """Deregister service instance"""
        await self.registry.deregister(service_name, instance_id)
    
    async def get_service_instances(
        self,
        service_name: str
    ) -> List[ServiceInstance]:
        """Get service instances"""
        return await self.registry.get_instances(service_name)
    
    async def watch_service(
        self,
        service_name: str,
        callback: Callable[[List[ServiceInstance]], None]
    ) -> None:
        """Watch service for changes"""
        await self.registry.watch_service(service_name, callback)
    
    async def unwatch_service(
        self,
        service_name: str,
        callback: Callable[[List[ServiceInstance]], None]
    ) -> None:
        """Unwatch service"""
        await self.registry.unwatch_service(service_name, callback)
