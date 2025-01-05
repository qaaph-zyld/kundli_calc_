"""
Service Integration Manager
PGF Protocol: SERVICE_002
Gate: GATE_4
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Type
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
from enum import Enum
import httpx
from .registry import service_registry, ServiceDefinition, ServiceStatus, ServiceType

class IntegrationProtocol(str, Enum):
    """Integration protocols"""
    REST = "rest"
    GRAPHQL = "graphql"
    GRPC = "grpc"
    EVENT = "event"

class IntegrationPolicy(BaseModel):
    """Integration policy configuration"""
    
    protocol: IntegrationProtocol
    timeout: int = 30
    retry_count: int = 3
    retry_delay: int = 1
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60
    rate_limit: Optional[int] = None
    cache_ttl: Optional[int] = None

class IntegrationMetrics(BaseModel):
    """Integration metrics"""
    
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency: float = 0.0
    circuit_breaker_trips: int = 0
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None

class ServiceIntegration:
    """Service integration handler"""
    
    def __init__(
        self,
        service: ServiceDefinition,
        policy: IntegrationPolicy,
        response_model: Optional[Type[BaseModel]] = None
    ):
        self.service = service
        self.policy = policy
        self.response_model = response_model
        self.metrics = IntegrationMetrics()
        self._circuit_breaker_state = {
            "is_open": False,
            "failure_count": 0,
            "last_failure_time": None
        }
        self._http_client = httpx.AsyncClient(timeout=policy.timeout)
    
    async def close(self) -> None:
        """Close integration resources"""
        await self._http_client.aclose()
    
    async def execute(
        self,
        endpoint_name: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Any:
        """Execute service integration"""
        if self._is_circuit_breaker_open():
            raise Exception("Circuit breaker is open")
        
        endpoint = self.service.endpoints.get(endpoint_name)
        if not endpoint:
            raise ValueError(f"Endpoint {endpoint_name} not found")
        
        for attempt in range(self.policy.retry_count):
            try:
                start_time = datetime.utcnow()
                
                response = await self._make_request(endpoint, data, headers)
                
                # Update metrics
                self.metrics.total_requests += 1
                self.metrics.successful_requests += 1
                self.metrics.total_latency += (datetime.utcnow() - start_time).total_seconds()
                self.metrics.last_success = datetime.utcnow()
                
                # Reset circuit breaker
                self._circuit_breaker_state["failure_count"] = 0
                self._circuit_breaker_state["is_open"] = False
                
                return self._process_response(response)
                
            except Exception as e:
                self.metrics.failed_requests += 1
                self.metrics.last_failure = datetime.utcnow()
                
                # Update circuit breaker
                self._update_circuit_breaker()
                
                if attempt == self.policy.retry_count - 1:
                    raise Exception(f"Service integration failed after {attempt + 1} attempts: {str(e)}")
                
                await asyncio.sleep(self.policy.retry_delay)
    
    async def _make_request(
        self,
        endpoint: Any,
        data: Optional[Dict[str, Any]],
        headers: Optional[Dict[str, str]]
    ) -> Any:
        """Make HTTP request to service endpoint"""
        url = f"{self.service.metadata.get('base_url', '')}{endpoint.path}"
        
        if self.policy.protocol == IntegrationProtocol.REST:
            if endpoint.method.lower() == "get":
                response = await self._http_client.get(url, params=data, headers=headers)
            elif endpoint.method.lower() == "post":
                response = await self._http_client.post(url, json=data, headers=headers)
            elif endpoint.method.lower() == "put":
                response = await self._http_client.put(url, json=data, headers=headers)
            elif endpoint.method.lower() == "delete":
                response = await self._http_client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {endpoint.method}")
            
            response.raise_for_status()
            return response.json()
            
        elif self.policy.protocol == IntegrationProtocol.GRAPHQL:
            # Implement GraphQL request handling
            pass
            
        elif self.policy.protocol == IntegrationProtocol.GRPC:
            # Implement gRPC request handling
            pass
            
        elif self.policy.protocol == IntegrationProtocol.EVENT:
            # Implement event-based integration
            pass
    
    def _process_response(self, response: Any) -> Any:
        """Process service response"""
        if self.response_model:
            return self.response_model(**response)
        return response
    
    def _is_circuit_breaker_open(self) -> bool:
        """Check if circuit breaker is open"""
        if not self._circuit_breaker_state["is_open"]:
            return False
            
        if self._circuit_breaker_state["last_failure_time"]:
            elapsed = (datetime.utcnow() - self._circuit_breaker_state["last_failure_time"]).total_seconds()
            if elapsed > self.policy.circuit_breaker_timeout:
                self._circuit_breaker_state["is_open"] = False
                return False
                
        return True
    
    def _update_circuit_breaker(self) -> None:
        """Update circuit breaker state"""
        self._circuit_breaker_state["failure_count"] += 1
        self._circuit_breaker_state["last_failure_time"] = datetime.utcnow()
        
        if (
            self._circuit_breaker_state["failure_count"]
            >= self.policy.circuit_breaker_threshold
        ):
            self._circuit_breaker_state["is_open"] = True
            self.metrics.circuit_breaker_trips += 1

class IntegrationManager:
    """Service integration manager"""
    
    def __init__(self):
        self._integrations: Dict[str, ServiceIntegration] = {}
        self._policies: Dict[ServiceType, IntegrationPolicy] = self._initialize_policies()
    
    def _initialize_policies(self) -> Dict[ServiceType, IntegrationPolicy]:
        """Initialize default integration policies"""
        return {
            ServiceType.CALCULATION: IntegrationPolicy(
                protocol=IntegrationProtocol.REST,
                timeout=60,
                retry_count=3,
                cache_ttl=300
            ),
            ServiceType.ANALYSIS: IntegrationPolicy(
                protocol=IntegrationProtocol.REST,
                timeout=30,
                retry_count=2,
                cache_ttl=600
            ),
            ServiceType.STORAGE: IntegrationPolicy(
                protocol=IntegrationProtocol.REST,
                timeout=10,
                retry_count=3
            ),
            ServiceType.CACHE: IntegrationPolicy(
                protocol=IntegrationProtocol.REST,
                timeout=5,
                retry_count=2
            ),
            ServiceType.QUEUE: IntegrationPolicy(
                protocol=IntegrationProtocol.EVENT,
                timeout=5,
                retry_count=3
            )
        }
    
    def register_integration(
        self,
        service: ServiceDefinition,
        policy: Optional[IntegrationPolicy] = None,
        response_model: Optional[Type[BaseModel]] = None
    ) -> ServiceIntegration:
        """Register service integration"""
        if service.id in self._integrations:
            raise ValueError(f"Integration for service {service.id} already exists")
        
        integration_policy = policy or self._policies.get(service.type)
        if not integration_policy:
            raise ValueError(f"No integration policy found for service type {service.type}")
        
        integration = ServiceIntegration(service, integration_policy, response_model)
        self._integrations[service.id] = integration
        
        return integration
    
    def get_integration(self, service_id: str) -> ServiceIntegration:
        """Get service integration by ID"""
        if service_id not in self._integrations:
            raise ValueError(f"Integration for service {service_id} not found")
        
        return self._integrations[service_id]
    
    async def close_all(self) -> None:
        """Close all service integrations"""
        for integration in self._integrations.values():
            await integration.close()

# Global integration manager instance
integration_manager = IntegrationManager()
