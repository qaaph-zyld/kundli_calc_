"""
Service Registry Framework
PGF Protocol: SERVICE_001
Gate: GATE_4
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
from enum import Enum
import uuid
import json

class ServiceStatus(str, Enum):
    """Service status states"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"

class ServiceType(str, Enum):
    """Service types"""
    CALCULATION = "calculation"
    ANALYSIS = "analysis"
    STORAGE = "storage"
    CACHE = "cache"
    QUEUE = "queue"

class ServiceEndpoint(BaseModel):
    """Service endpoint configuration"""
    
    path: str
    method: str
    description: str
    requires_auth: bool = True
    rate_limit: Optional[int] = None
    timeout: int = 30
    retry_policy: Dict[str, Any] = Field(default_factory=dict)

class ServiceDefinition(BaseModel):
    """Service definition"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    version: str
    type: ServiceType
    description: str
    status: ServiceStatus = ServiceStatus.ACTIVE
    endpoints: Dict[str, ServiceEndpoint]
    dependencies: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    health_check_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ServiceRegistry:
    """Service registry and discovery system"""
    
    def __init__(self):
        self._services: Dict[str, ServiceDefinition] = {}
        self._health_check_interval: int = 30  # seconds
        self._health_check_task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """Start service registry"""
        self._health_check_task = asyncio.create_task(self._health_check_loop())
    
    async def stop(self) -> None:
        """Stop service registry"""
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
    
    def register_service(self, service: ServiceDefinition) -> str:
        """Register a new service"""
        if service.id in self._services:
            raise ValueError(f"Service with ID {service.id} already exists")
        
        self._services[service.id] = service
        return service.id
    
    def unregister_service(self, service_id: str) -> None:
        """Unregister a service"""
        if service_id not in self._services:
            raise ValueError(f"Service with ID {service_id} not found")
        
        del self._services[service_id]
    
    def get_service(self, service_id: str) -> ServiceDefinition:
        """Get service by ID"""
        if service_id not in self._services:
            raise ValueError(f"Service with ID {service_id} not found")
        
        return self._services[service_id]
    
    def list_services(
        self,
        service_type: Optional[ServiceType] = None,
        status: Optional[ServiceStatus] = None
    ) -> List[ServiceDefinition]:
        """List registered services with optional filtering"""
        services = list(self._services.values())
        
        if service_type:
            services = [s for s in services if s.type == service_type]
        
        if status:
            services = [s for s in services if s.status == status]
        
        return services
    
    def update_service_status(self, service_id: str, status: ServiceStatus) -> None:
        """Update service status"""
        if service_id not in self._services:
            raise ValueError(f"Service with ID {service_id} not found")
        
        service = self._services[service_id]
        service.status = status
        service.updated_at = datetime.utcnow()
    
    def get_service_dependencies(self, service_id: str) -> List[ServiceDefinition]:
        """Get service dependencies"""
        service = self.get_service(service_id)
        return [self.get_service(dep_id) for dep_id in service.dependencies]
    
    def get_dependent_services(self, service_id: str) -> List[ServiceDefinition]:
        """Get services that depend on the specified service"""
        return [
            service for service in self._services.values()
            if service_id in service.dependencies
        ]
    
    async def _health_check_loop(self) -> None:
        """Health check loop for registered services"""
        while True:
            try:
                await self._check_services_health()
                await asyncio.sleep(self._health_check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in health check loop: {e}")
                await asyncio.sleep(5)  # Shorter interval on error
    
    async def _check_services_health(self) -> None:
        """Check health of all registered services"""
        for service in self._services.values():
            if service.health_check_url:
                try:
                    # Implement health check logic here
                    # For now, just update the timestamp
                    service.updated_at = datetime.utcnow()
                except Exception as e:
                    print(f"Health check failed for service {service.id}: {e}")
                    self.update_service_status(service.id, ServiceStatus.DEGRADED)

# Global service registry instance
service_registry = ServiceRegistry()
