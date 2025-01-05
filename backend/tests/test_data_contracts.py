"""
Test Suite for Data Contract Enforcement
PGF Protocol: CON_001
Gate: GATE_4
Version: 1.0.0
"""

import pytest
from datetime import datetime
import json
from pydantic import BaseModel, Field, ValidationError
from app.core.contracts.data_contracts import (
    ContractRegistry,
    ContractEnforcer,
    ContractVersion,
    ContractType,
    ValidationStrategy,
    ContractMetadata,
    BaseRequest,
    BaseResponse,
    BaseEvent
)

# Test Models
class TestRequest(BaseModel):
    """Test request model"""
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")

class TestRequestV2(BaseModel):
    """Test request model v2"""
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    preferences: dict = Field(default_factory=dict)

@pytest.fixture
def registry():
    """Create test registry"""
    registry = ContractRegistry()
    
    # Register test contracts
    registry.register_contract(
        TestRequest,
        ContractMetadata(
            version=ContractVersion.V1_0,
            type=ContractType.REQUEST,
            name="test_request",
            description="Test request contract",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    )
    
    registry.register_contract(
        TestRequestV2,
        ContractMetadata(
            version=ContractVersion.V2_0,
            type=ContractType.REQUEST,
            name="test_request",
            description="Test request contract v2",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    )
    
    return registry

@pytest.fixture
def enforcer(registry):
    """Create test enforcer"""
    return ContractEnforcer(registry)

@pytest.mark.asyncio
async def test_contract_registration(registry):
    """Test contract registration"""
    contract = registry.get_contract("test_request", ContractVersion.V1_0)
    assert contract == TestRequest
    
    metadata = registry.get_metadata("test_request", ContractVersion.V1_0)
    assert metadata.version == ContractVersion.V1_0
    assert metadata.type == ContractType.REQUEST

@pytest.mark.asyncio
async def test_contract_validation_success(enforcer):
    """Test successful contract validation"""
    valid_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }
    
    is_valid, error = await enforcer.validate_request(
        valid_data,
        "test_request",
        ContractVersion.V1_0
    )
    assert is_valid
    assert error is None

@pytest.mark.asyncio
async def test_contract_validation_failure(enforcer):
    """Test contract validation failure"""
    invalid_data = {
        "name": "",  # Invalid: empty string
        "age": -1,   # Invalid: negative age
        "email": "invalid-email"  # Invalid: wrong format
    }
    
    is_valid, error = await enforcer.validate_request(
        invalid_data,
        "test_request",
        ContractVersion.V1_0
    )
    assert not is_valid
    assert error is not None

@pytest.mark.asyncio
async def test_contract_versioning(enforcer):
    """Test contract versioning"""
    data_v1 = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }
    
    data_v2 = {
        **data_v1,
        "preferences": {"theme": "dark"}
    }
    
    # Test V1
    is_valid, _ = await enforcer.validate_request(
        data_v1,
        "test_request",
        ContractVersion.V1_0
    )
    assert is_valid
    
    # Test V2
    is_valid, _ = await enforcer.validate_request(
        data_v2,
        "test_request",
        ContractVersion.V2_0
    )
    assert is_valid

@pytest.mark.asyncio
async def test_validation_strategies(enforcer):
    """Test different validation strategies"""
    # Test strict validation
    invalid_data = {
        "name": "John Doe",
        "age": "30",  # String instead of int
        "email": "john@example.com"
    }
    
    is_valid, _ = await enforcer.validate_request(
        invalid_data,
        "test_request",
        ContractVersion.V1_0,
        ValidationStrategy.STRICT
    )
    assert not is_valid
    
    # Test lenient validation
    is_valid, _ = await enforcer.validate_request(
        invalid_data,
        "test_request",
        ContractVersion.V1_0,
        ValidationStrategy.LENIENT
    )
    assert is_valid  # Should pass due to automatic type conversion

@pytest.mark.asyncio
async def test_contract_decorator(enforcer):
    """Test contract enforcement decorator"""
    @enforcer.enforce_contract("test_request", ContractVersion.V1_0)
    async def test_function(self, data):
        return data
    
    valid_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }
    
    # Test with valid data
    result = await test_function(None, valid_data)
    assert result == valid_data
    
    # Test with invalid data
    invalid_data = {
        "name": "",
        "age": -1,
        "email": "invalid"
    }
    
    with pytest.raises(ValidationError):
        await test_function(None, invalid_data)

@pytest.mark.asyncio
async def test_base_contracts():
    """Test base contract validation"""
    # Test BaseRequest
    valid_request = {
        "request_id": "req_123",
        "timestamp": datetime.now(),
        "version": "1.0"
    }
    request = BaseRequest(**valid_request)
    assert request.request_id == "req_123"
    
    # Test BaseResponse
    valid_response = {
        "request_id": "req_123",
        "timestamp": datetime.now(),
        "status": "success",
        "data": {"result": "ok"},
        "metadata": {"processing_time": 100}
    }
    response = BaseResponse(**valid_response)
    assert response.status == "success"
    
    # Test BaseEvent
    valid_event = {
        "event_id": "evt_123",
        "event_type": "calculation_complete",
        "timestamp": datetime.now(),
        "payload": {"calculation_id": "calc_123"},
        "metadata": {"duration": 200}
    }
    event = BaseEvent(**valid_event)
    assert event.event_type == "calculation_complete"

@pytest.mark.asyncio
async def test_contract_schema(enforcer):
    """Test contract schema generation"""
    schema = enforcer.get_contract_schema(
        "test_request",
        ContractVersion.V1_0
    )
    assert schema["type"] == "object"
    assert "properties" in schema
    assert "name" in schema["properties"]
    assert "age" in schema["properties"]
    assert "email" in schema["properties"]

@pytest.mark.asyncio
async def test_contract_metadata(enforcer):
    """Test contract metadata retrieval"""
    metadata = enforcer.get_contract_metadata(
        "test_request",
        ContractVersion.V1_0
    )
    assert isinstance(metadata, ContractMetadata)
    assert metadata.version == ContractVersion.V1_0
    assert metadata.type == ContractType.REQUEST
    assert metadata.name == "test_request"
    assert metadata.hash is not None

@pytest.mark.asyncio
async def test_multiple_contracts(registry):
    """Test handling multiple contracts"""
    # Register additional test contract
    class AnotherContract(BaseModel):
        field1: str
        field2: int
    
    registry.register_contract(
        AnotherContract,
        ContractMetadata(
            version=ContractVersion.V1_0,
            type=ContractType.INTERNAL,
            name="another_contract",
            description="Another test contract",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    )
    
    # Verify both contracts are accessible
    contract1 = registry.get_contract(
        "test_request",
        ContractVersion.V1_0
    )
    contract2 = registry.get_contract(
        "another_contract",
        ContractVersion.V1_0
    )
    
    assert contract1 == TestRequest
    assert contract2 == AnotherContract

@pytest.mark.asyncio
async def test_error_handling(registry, enforcer):
    """Test error handling"""
    # Test non-existent contract
    with pytest.raises(KeyError):
        registry.get_contract("non_existent")
    
    # Test invalid contract registration
    with pytest.raises(ValueError):
        registry.register_contract(
            TestRequest,
            ContractMetadata(
                version=ContractVersion.V1_0,
                type=ContractType.REQUEST,
                name="test_request",
                description="Duplicate contract",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        )
    
    # Test validation with invalid data type
    with pytest.raises(ValueError):
        await enforcer.validate_request(
            None,
            "test_request",
            ContractVersion.V1_0
        )
