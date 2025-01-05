"""
Data Contract Enforcement System
PGF Protocol: CON_001
Gate: GATE_4
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, Type, TypeVar
from datetime import datetime
from enum import Enum
import json
import logging
from pydantic import (
    BaseModel,
    Field,
    validator,
    ValidationError,
    create_model,
    constr
)
from dataclasses import dataclass, field
import jsonschema
from jsonschema import validate, ValidationError as JsonSchemaError
import hashlib
import asyncio
from functools import wraps

T = TypeVar('T', bound=BaseModel)

class ContractVersion(str, Enum):
    """Contract version enumeration"""
    V1_0 = "1.0"
    V1_1 = "1.1"
    V2_0 = "2.0"
    LATEST = "2.0"

class ContractType(str, Enum):
    """Contract type enumeration"""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    INTERNAL = "internal"

class ValidationStrategy(str, Enum):
    """Validation strategy enumeration"""
    STRICT = "strict"
    LENIENT = "lenient"
    MIGRATION = "migration"

@dataclass
class ContractMetadata:
    """Contract metadata"""
    version: ContractVersion
    type: ContractType
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    hash: str = field(init=False)
    
    def __post_init__(self):
        """Generate contract hash"""
        content = f"{self.version}{self.type}{self.name}{self.created_at}"
        self.hash = hashlib.sha256(content.encode()).hexdigest()

class ContractRegistry:
    """Contract registry for managing data contracts"""
    
    def __init__(self):
        self._contracts: Dict[str, Type[BaseModel]] = {}
        self._metadata: Dict[str, ContractMetadata] = {}
        self._migrations: Dict[str, Dict[str, callable]] = {}
        self._validators: Dict[str, callable] = {}
        self.logger = logging.getLogger(__name__)
    
    def register_contract(
        self,
        contract: Type[BaseModel],
        metadata: ContractMetadata,
        validators: Optional[List[callable]] = None
    ) -> None:
        """Register a new contract"""
        contract_id = f"{metadata.name}_{metadata.version}"
        
        if contract_id in self._contracts:
            raise ValueError(f"Contract {contract_id} already registered")
        
        self._contracts[contract_id] = contract
        self._metadata[contract_id] = metadata
        
        if validators:
            self._validators[contract_id] = validators
    
    def register_migration(
        self,
        source_version: ContractVersion,
        target_version: ContractVersion,
        contract_name: str,
        migration_func: callable
    ) -> None:
        """Register a contract migration"""
        migration_key = (
            f"{contract_name}_{source_version}_to_{target_version}"
        )
        
        if migration_key not in self._migrations:
            self._migrations[migration_key] = {}
        
        self._migrations[migration_key] = migration_func
    
    def get_contract(
        self,
        name: str,
        version: Optional[ContractVersion] = None
    ) -> Type[BaseModel]:
        """Get a contract by name and version"""
        version = version or ContractVersion.LATEST
        contract_id = f"{name}_{version}"
        
        if contract_id not in self._contracts:
            raise KeyError(f"Contract {contract_id} not found")
        
        return self._contracts[contract_id]
    
    def get_metadata(
        self,
        name: str,
        version: Optional[ContractVersion] = None
    ) -> ContractMetadata:
        """Get contract metadata"""
        version = version or ContractVersion.LATEST
        contract_id = f"{name}_{version}"
        
        if contract_id not in self._metadata:
            raise KeyError(f"Metadata for {contract_id} not found")
        
        return self._metadata[contract_id]
    
    async def validate_data(
        self,
        data: Dict[str, Any],
        contract_name: str,
        version: Optional[ContractVersion] = None,
        strategy: ValidationStrategy = ValidationStrategy.STRICT
    ) -> Tuple[bool, Optional[str]]:
        """Validate data against a contract"""
        try:
            version = version or ContractVersion.LATEST
            contract = self.get_contract(contract_name, version)
            
            # Create contract instance
            instance = contract(**data)
            
            # Run custom validators
            contract_id = f"{contract_name}_{version}"
            if contract_id in self._validators:
                for validator in self._validators[contract_id]:
                    await validator(instance)
            
            return True, None
            
        except ValidationError as e:
            error_msg = str(e)
            
            if strategy == ValidationStrategy.LENIENT:
                # Try to fix common issues
                fixed_data = self._attempt_fix(data, contract)
                if fixed_data:
                    return await self.validate_data(
                        fixed_data,
                        contract_name,
                        version,
                        ValidationStrategy.STRICT
                    )
            
            elif strategy == ValidationStrategy.MIGRATION:
                # Try to migrate to latest version
                migrated_data = await self._attempt_migration(
                    data,
                    contract_name,
                    version
                )
                if migrated_data:
                    return await self.validate_data(
                        migrated_data,
                        contract_name,
                        ContractVersion.LATEST,
                        ValidationStrategy.STRICT
                    )
            
            return False, error_msg
    
    def _attempt_fix(
        self,
        data: Dict[str, Any],
        contract: Type[BaseModel]
    ) -> Optional[Dict[str, Any]]:
        """Attempt to fix common data issues"""
        fixed_data = data.copy()
        
        try:
            # Get field types from contract
            field_types = {
                field_name: field.type_
                for field_name, field in contract.__fields__.items()
            }
            
            # Apply fixes
            for field_name, field_type in field_types.items():
                if field_name not in fixed_data:
                    continue
                
                value = fixed_data[field_name]
                
                # Type conversion
                if isinstance(value, str):
                    if field_type == int:
                        try:
                            fixed_data[field_name] = int(value)
                        except ValueError:
                            pass
                    elif field_type == float:
                        try:
                            fixed_data[field_name] = float(value)
                        except ValueError:
                            pass
                    elif field_type == bool:
                        fixed_data[field_name] = value.lower() == "true"
                
                # String cleanup
                if isinstance(value, str):
                    fixed_data[field_name] = value.strip()
            
            return fixed_data
            
        except Exception as e:
            self.logger.error(f"Error fixing data: {str(e)}")
            return None
    
    async def _attempt_migration(
        self,
        data: Dict[str, Any],
        contract_name: str,
        current_version: ContractVersion
    ) -> Optional[Dict[str, Any]]:
        """Attempt to migrate data to latest version"""
        try:
            migrated_data = data.copy()
            target_version = ContractVersion.LATEST
            
            while current_version != target_version:
                migration_key = (
                    f"{contract_name}_{current_version}_to_{target_version}"
                )
                
                if migration_key not in self._migrations:
                    return None
                
                migration_func = self._migrations[migration_key]
                migrated_data = await migration_func(migrated_data)
                
                # Update version for next iteration
                versions = list(ContractVersion)
                current_idx = versions.index(current_version)
                current_version = versions[current_idx + 1]
            
            return migrated_data
            
        except Exception as e:
            self.logger.error(f"Error migrating data: {str(e)}")
            return None

class ContractEnforcer:
    """Contract enforcement system"""
    
    def __init__(
        self,
        registry: ContractRegistry,
        default_strategy: ValidationStrategy = ValidationStrategy.STRICT
    ):
        self.registry = registry
        self.default_strategy = default_strategy
        self.logger = logging.getLogger(__name__)
    
    def enforce_contract(
        self,
        contract_name: str,
        version: Optional[ContractVersion] = None,
        strategy: Optional[ValidationStrategy] = None
    ):
        """Decorator for enforcing contracts"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Get data from first argument after self
                data = args[1] if len(args) > 1 else kwargs.get('data')
                
                if not data:
                    raise ValueError("No data provided for validation")
                
                # Validate data
                is_valid, error = await self.registry.validate_data(
                    data,
                    contract_name,
                    version,
                    strategy or self.default_strategy
                )
                
                if not is_valid:
                    raise ValidationError(
                        f"Contract validation failed: {error}"
                    )
                
                # Execute function
                return await func(*args, **kwargs)
            
            return wrapper
        return decorator
    
    async def validate_request(
        self,
        data: Dict[str, Any],
        contract_name: str,
        version: Optional[ContractVersion] = None,
        strategy: Optional[ValidationStrategy] = None
    ) -> Tuple[bool, Optional[str]]:
        """Validate request data"""
        return await self.registry.validate_data(
            data,
            contract_name,
            version,
            strategy or self.default_strategy
        )
    
    def get_contract_schema(
        self,
        contract_name: str,
        version: Optional[ContractVersion] = None
    ) -> Dict[str, Any]:
        """Get JSON schema for a contract"""
        contract = self.registry.get_contract(contract_name, version)
        return contract.schema()
    
    def get_contract_metadata(
        self,
        contract_name: str,
        version: Optional[ContractVersion] = None
    ) -> ContractMetadata:
        """Get contract metadata"""
        return self.registry.get_metadata(contract_name, version)

# Example Usage and Base Contracts
class BaseRequest(BaseModel):
    """Base request contract"""
    request_id: str = Field(..., min_length=1)
    timestamp: datetime
    version: str = Field(..., regex=r"^\d+\.\d+$")

class BaseResponse(BaseModel):
    """Base response contract"""
    request_id: str = Field(..., min_length=1)
    timestamp: datetime
    status: str = Field(..., regex=r"^(success|error)$")
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]]

class BaseEvent(BaseModel):
    """Base event contract"""
    event_id: str = Field(..., min_length=1)
    event_type: str
    timestamp: datetime
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]]

# Initialize global registry
contract_registry = ContractRegistry()

# Register base contracts
contract_registry.register_contract(
    BaseRequest,
    ContractMetadata(
        version=ContractVersion.V1_0,
        type=ContractType.REQUEST,
        name="base_request",
        description="Base request contract",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
)

contract_registry.register_contract(
    BaseResponse,
    ContractMetadata(
        version=ContractVersion.V1_0,
        type=ContractType.RESPONSE,
        name="base_response",
        description="Base response contract",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
)

contract_registry.register_contract(
    BaseEvent,
    ContractMetadata(
        version=ContractVersion.V1_0,
        type=ContractType.EVENT,
        name="base_event",
        description="Base event contract",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
)
