"""
Schema Registry Framework
PGF Protocol: REGISTRY_001
Gate: GATE_4
Version: 1.0.0
"""

from typing import Dict, Type, Optional
from pydantic import BaseModel
from enum import Enum
from .optimization import OptimizationLevel, ResponseFormat, SchemaOptimizer

class SchemaVersion(str, Enum):
    """Schema versioning"""
    V1 = "v1"
    V2 = "v2"
    LATEST = "latest"

class SchemaRegistry:
    """Central registry for managing API schemas"""
    
    def __init__(self):
        self._schemas: Dict[str, Dict[SchemaVersion, Type[BaseModel]]] = {}
        self._optimizers: Dict[str, SchemaOptimizer] = {}
    
    def register_schema(
        self,
        name: str,
        schema: Type[BaseModel],
        version: SchemaVersion = SchemaVersion.V1,
        optimization_level: OptimizationLevel = OptimizationLevel.STANDARD
    ) -> None:
        """Register a new schema version"""
        if name not in self._schemas:
            self._schemas[name] = {}
        
        self._schemas[name][version] = schema
        self._optimizers[name] = SchemaOptimizer(optimization_level)
        
        # Mark as latest version
        if version != SchemaVersion.LATEST:
            self._schemas[name][SchemaVersion.LATEST] = schema
    
    def get_schema(
        self,
        name: str,
        version: SchemaVersion = SchemaVersion.LATEST
    ) -> Optional[Type[BaseModel]]:
        """Get schema by name and version"""
        return self._schemas.get(name, {}).get(version)
    
    def get_optimizer(
        self,
        name: str
    ) -> Optional[SchemaOptimizer]:
        """Get schema optimizer by name"""
        return self._optimizers.get(name)
    
    async def optimize_response(
        self,
        name: str,
        data: dict,
        format: ResponseFormat = ResponseFormat.JSON
    ) -> dict:
        """Optimize response using registered schema optimizer"""
        optimizer = self.get_optimizer(name)
        if not optimizer:
            return data
            
        optimized = await optimizer.optimize_response(data, format)
        return optimized.dict()

# Global schema registry instance
schema_registry = SchemaRegistry()
