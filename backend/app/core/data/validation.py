"""
Data Excellence Framework - Validation
PGF Protocol: DATA_001
Gate: GATE_4
Version: 1.0.0
"""

from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel, ValidationError, Field
from datetime import datetime
from enum import Enum
import re

class ValidationLevel(str, Enum):
    """Data validation levels"""
    STRICT = "strict"        # All rules enforced
    STANDARD = "standard"    # Common rules enforced
    RELAXED = "relaxed"      # Basic rules enforced
    CUSTOM = "custom"        # Custom rule set

class ValidationScope(str, Enum):
    """Data validation scopes"""
    INPUT = "input"          # Input data validation
    PROCESSING = "processing"  # Data processing validation
    OUTPUT = "output"        # Output data validation
    STORAGE = "storage"      # Storage data validation

class ValidationRule(BaseModel):
    """Data validation rule definition"""
    
    name: str
    description: str
    validation_type: str
    parameters: Dict[str, Any]
    level: ValidationLevel
    scope: ValidationScope
    priority: int = Field(default=1, ge=1, le=10)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "date_format",
                "description": "Validates date format",
                "validation_type": "regex",
                "parameters": {
                    "pattern": r"^\d{4}-\d{2}-\d{2}$",
                    "error_message": "Invalid date format. Use YYYY-MM-DD"
                },
                "level": ValidationLevel.STRICT,
                "scope": ValidationScope.INPUT,
                "priority": 1
            }
        }

class ValidationResult(BaseModel):
    """Validation result"""
    
    valid: bool
    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DataValidator:
    """Enterprise data validation engine"""
    
    def __init__(self):
        self._rules: Dict[str, ValidationRule] = {}
        self._custom_validators: Dict[str, callable] = {}
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Initialize default validation rules"""
        self.add_rule(ValidationRule(
            name="date_format",
            description="Validates date format",
            validation_type="regex",
            parameters={
                "pattern": r"^\d{4}-\d{2}-\d{2}$",
                "error_message": "Invalid date format. Use YYYY-MM-DD"
            },
            level=ValidationLevel.STRICT,
            scope=ValidationScope.INPUT
        ))
        
        self.add_rule(ValidationRule(
            name="time_format",
            description="Validates time format",
            validation_type="regex",
            parameters={
                "pattern": r"^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$",
                "error_message": "Invalid time format. Use HH:MM:SS"
            },
            level=ValidationLevel.STRICT,
            scope=ValidationScope.INPUT
        ))
        
        self.add_rule(ValidationRule(
            name="latitude",
            description="Validates latitude value",
            validation_type="range",
            parameters={
                "min": -90,
                "max": 90,
                "error_message": "Invalid latitude. Must be between -90 and 90"
            },
            level=ValidationLevel.STRICT,
            scope=ValidationScope.INPUT
        ))
        
        self.add_rule(ValidationRule(
            name="longitude",
            description="Validates longitude value",
            validation_type="range",
            parameters={
                "min": -180,
                "max": 180,
                "error_message": "Invalid longitude. Must be between -180 and 180"
            },
            level=ValidationLevel.STRICT,
            scope=ValidationScope.INPUT
        ))
    
    def add_rule(self, rule: ValidationRule) -> None:
        """Add validation rule"""
        self._rules[rule.name] = rule
    
    def add_custom_validator(self, name: str, validator: callable) -> None:
        """Add custom validator function"""
        self._custom_validators[name] = validator
    
    async def validate(
        self,
        data: Union[Dict[str, Any], BaseModel],
        level: ValidationLevel = ValidationLevel.STANDARD,
        scope: ValidationScope = ValidationScope.INPUT
    ) -> ValidationResult:
        """Validate data against rules"""
        errors = []
        warnings = []
        metadata = {
            "validation_level": level,
            "validation_scope": scope,
            "rules_applied": []
        }
        
        # Convert BaseModel to dict if necessary
        if isinstance(data, BaseModel):
            data = data.dict()
        
        # Apply rules in priority order
        sorted_rules = sorted(
            [rule for rule in self._rules.values() if rule.level == level and rule.scope == scope],
            key=lambda x: x.priority
        )
        
        for rule in sorted_rules:
            try:
                if rule.validation_type == "regex":
                    await self._validate_regex(data, rule, errors, warnings)
                elif rule.validation_type == "range":
                    await self._validate_range(data, rule, errors, warnings)
                elif rule.validation_type == "custom":
                    await self._validate_custom(data, rule, errors, warnings)
                
                metadata["rules_applied"].append(rule.name)
                
            except Exception as e:
                errors.append({
                    "rule": rule.name,
                    "error": str(e),
                    "field": None
                })
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )
    
    async def _validate_regex(
        self,
        data: Dict[str, Any],
        rule: ValidationRule,
        errors: List[Dict[str, Any]],
        warnings: List[Dict[str, Any]]
    ) -> None:
        """Validate using regex pattern"""
        pattern = rule.parameters["pattern"]
        for field, value in data.items():
            if isinstance(value, str) and not re.match(pattern, value):
                errors.append({
                    "rule": rule.name,
                    "error": rule.parameters["error_message"],
                    "field": field,
                    "value": value
                })
    
    async def _validate_range(
        self,
        data: Dict[str, Any],
        rule: ValidationRule,
        errors: List[Dict[str, Any]],
        warnings: List[Dict[str, Any]]
    ) -> None:
        """Validate numeric range"""
        min_val = rule.parameters["min"]
        max_val = rule.parameters["max"]
        for field, value in data.items():
            if isinstance(value, (int, float)) and (value < min_val or value > max_val):
                errors.append({
                    "rule": rule.name,
                    "error": rule.parameters["error_message"],
                    "field": field,
                    "value": value
                })
    
    async def _validate_custom(
        self,
        data: Dict[str, Any],
        rule: ValidationRule,
        errors: List[Dict[str, Any]],
        warnings: List[Dict[str, Any]]
    ) -> None:
        """Execute custom validation"""
        validator = self._custom_validators.get(rule.name)
        if validator:
            result = await validator(data, rule.parameters)
            if not result["valid"]:
                errors.append({
                    "rule": rule.name,
                    "error": result["error"],
                    "field": result.get("field"),
                    "value": result.get("value")
                })

# Global validator instance
data_validator = DataValidator()
