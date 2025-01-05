"""
Service Scaling Strategies
PGF Protocol: SCAL_001
Gate: GATE_32
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union, Set
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
import asyncio
import json
import logging

class ScalingMode(str, Enum):
    """Scaling modes"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    HYBRID = "hybrid"

class ScalingTrigger(str, Enum):
    """Scaling triggers"""
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    REQUEST_COUNT = "request_count"
    LATENCY = "latency"
    CUSTOM = "custom"

class ScalingState(str, Enum):
    """Scaling states"""
    STABLE = "stable"
    SCALING_UP = "scaling_up"
    SCALING_DOWN = "scaling_down"
    COOLDOWN = "cooldown"

@dataclass
class ScalingMetrics:
    """Scaling metrics"""
    
    scale_up_count: int
    scale_down_count: int
    average_response_time: float
    resource_utilization: Dict[str, float]
    current_capacity: int
    target_capacity: int

class HorizontalScaling:
    """Horizontal scaling strategy"""
    
    def __init__(
        self,
        min_replicas: int = 1,
        max_replicas: int = 10,
        cooldown_seconds: int = 300
    ):
        """Initialize strategy"""
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.cooldown = cooldown_seconds
        self.state = ScalingState.STABLE
        
        # Initialize metrics
        self.metrics = ScalingMetrics(
            scale_up_count=0,
            scale_down_count=0,
            average_response_time=0.0,
            resource_utilization={},
            current_capacity=min_replicas,
            target_capacity=min_replicas
        )
    
    async def scale(
        self,
        config: Dict[str, Any]
    ) -> bool:
        """Execute horizontal scaling"""
        try:
            # Check cooldown period
            if not self._check_cooldown():
                return False
            
            # Calculate target capacity
            target = self._calculate_target_capacity(config)
            
            # Apply scaling
            if target > self.metrics.current_capacity:
                await self._scale_up(
                    target - self.metrics.current_capacity
                )
            elif target < self.metrics.current_capacity:
                await self._scale_down(
                    self.metrics.current_capacity - target
                )
            
            return True
        
        except Exception as e:
            self.state = ScalingState.STABLE
            raise e
    
    def _check_cooldown(self) -> bool:
        """Check cooldown period"""
        if self.state == ScalingState.COOLDOWN:
            return False
        return True
    
    def _calculate_target_capacity(
        self,
        config: Dict[str, Any]
    ) -> int:
        """Calculate target capacity"""
        # Get current metrics
        cpu_usage = config.get("cpu_usage", 0.0)
        memory_usage = config.get("memory_usage", 0.0)
        request_count = config.get("request_count", 0)
        
        # Calculate target based on highest utilization
        target = self.metrics.current_capacity
        
        if cpu_usage > 0.8:
            target += 1
        elif cpu_usage < 0.2:
            target -= 1
        
        if memory_usage > 0.8:
            target += 1
        elif memory_usage < 0.2:
            target -= 1
        
        # Ensure within limits
        target = max(self.min_replicas, min(target, self.max_replicas))
        
        return target
    
    async def _scale_up(
        self,
        count: int
    ):
        """Scale up replicas"""
        self.state = ScalingState.SCALING_UP
        self.metrics.scale_up_count += 1
        
        try:
            # Add replicas
            self.metrics.current_capacity += count
            
            # Update state
            self.state = ScalingState.COOLDOWN
            
            # Start cooldown timer
            asyncio.create_task(
                self._start_cooldown()
            )
        
        except Exception as e:
            self.state = ScalingState.STABLE
            raise e
    
    async def _scale_down(
        self,
        count: int
    ):
        """Scale down replicas"""
        self.state = ScalingState.SCALING_DOWN
        self.metrics.scale_down_count += 1
        
        try:
            # Remove replicas
            self.metrics.current_capacity -= count
            
            # Update state
            self.state = ScalingState.COOLDOWN
            
            # Start cooldown timer
            asyncio.create_task(
                self._start_cooldown()
            )
        
        except Exception as e:
            self.state = ScalingState.STABLE
            raise e
    
    async def _start_cooldown(self):
        """Start cooldown timer"""
        await asyncio.sleep(self.cooldown)
        self.state = ScalingState.STABLE

class VerticalScaling:
    """Vertical scaling strategy"""
    
    def __init__(
        self,
        min_resources: Dict[str, float],
        max_resources: Dict[str, float],
        cooldown_seconds: int = 300
    ):
        """Initialize strategy"""
        self.min_resources = min_resources
        self.max_resources = max_resources
        self.cooldown = cooldown_seconds
        self.state = ScalingState.STABLE
        
        # Initialize metrics
        self.metrics = ScalingMetrics(
            scale_up_count=0,
            scale_down_count=0,
            average_response_time=0.0,
            resource_utilization={},
            current_capacity=0,
            target_capacity=0
        )
    
    async def scale(
        self,
        config: Dict[str, Any]
    ) -> bool:
        """Execute vertical scaling"""
        try:
            # Check cooldown period
            if not self._check_cooldown():
                return False
            
            # Calculate target resources
            target = self._calculate_target_resources(config)
            
            # Apply scaling
            current = self.metrics.resource_utilization
            
            for resource, value in target.items():
                if value > current.get(resource, 0.0):
                    await self._scale_up_resource(
                        resource,
                        value
                    )
                elif value < current.get(resource, 0.0):
                    await self._scale_down_resource(
                        resource,
                        value
                    )
            
            return True
        
        except Exception as e:
            self.state = ScalingState.STABLE
            raise e
    
    def _check_cooldown(self) -> bool:
        """Check cooldown period"""
        if self.state == ScalingState.COOLDOWN:
            return False
        return True
    
    def _calculate_target_resources(
        self,
        config: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate target resources"""
        target = {}
        
        # Calculate CPU target
        cpu_usage = config.get("cpu_usage", 0.0)
        current_cpu = self.metrics.resource_utilization.get(
            "cpu",
            self.min_resources["cpu"]
        )
        
        if cpu_usage > 0.8:
            target["cpu"] = min(
                current_cpu * 1.5,
                self.max_resources["cpu"]
            )
        elif cpu_usage < 0.2:
            target["cpu"] = max(
                current_cpu * 0.75,
                self.min_resources["cpu"]
            )
        else:
            target["cpu"] = current_cpu
        
        # Calculate memory target
        memory_usage = config.get("memory_usage", 0.0)
        current_memory = self.metrics.resource_utilization.get(
            "memory",
            self.min_resources["memory"]
        )
        
        if memory_usage > 0.8:
            target["memory"] = min(
                current_memory * 1.5,
                self.max_resources["memory"]
            )
        elif memory_usage < 0.2:
            target["memory"] = max(
                current_memory * 0.75,
                self.min_resources["memory"]
            )
        else:
            target["memory"] = current_memory
        
        return target
    
    async def _scale_up_resource(
        self,
        resource: str,
        target: float
    ):
        """Scale up resource"""
        self.state = ScalingState.SCALING_UP
        self.metrics.scale_up_count += 1
        
        try:
            # Update resource
            self.metrics.resource_utilization[resource] = target
            
            # Update state
            self.state = ScalingState.COOLDOWN
            
            # Start cooldown timer
            asyncio.create_task(
                self._start_cooldown()
            )
        
        except Exception as e:
            self.state = ScalingState.STABLE
            raise e
    
    async def _scale_down_resource(
        self,
        resource: str,
        target: float
    ):
        """Scale down resource"""
        self.state = ScalingState.SCALING_DOWN
        self.metrics.scale_down_count += 1
        
        try:
            # Update resource
            self.metrics.resource_utilization[resource] = target
            
            # Update state
            self.state = ScalingState.COOLDOWN
            
            # Start cooldown timer
            asyncio.create_task(
                self._start_cooldown()
            )
        
        except Exception as e:
            self.state = ScalingState.STABLE
            raise e
    
    async def _start_cooldown(self):
        """Start cooldown timer"""
        await asyncio.sleep(self.cooldown)
        self.state = ScalingState.STABLE

class HybridScaling:
    """Hybrid scaling strategy"""
    
    def __init__(
        self,
        horizontal: HorizontalScaling,
        vertical: VerticalScaling
    ):
        """Initialize strategy"""
        self.horizontal = horizontal
        self.vertical = vertical
        self.state = ScalingState.STABLE
        
        # Initialize metrics
        self.metrics = ScalingMetrics(
            scale_up_count=0,
            scale_down_count=0,
            average_response_time=0.0,
            resource_utilization={},
            current_capacity=0,
            target_capacity=0
        )
    
    async def scale(
        self,
        config: Dict[str, Any]
    ) -> bool:
        """Execute hybrid scaling"""
        try:
            # Try vertical scaling first
            vertical_result = await self.vertical.scale(config)
            
            # If vertical scaling fails, try horizontal
            if not vertical_result:
                horizontal_result = await self.horizontal.scale(
                    config
                )
                return horizontal_result
            
            return vertical_result
        
        except Exception as e:
            self.state = ScalingState.STABLE
            raise e
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get scaling metrics"""
        return {
            "horizontal": vars(self.horizontal.metrics),
            "vertical": vars(self.vertical.metrics),
            "hybrid": vars(self.metrics)
        }
