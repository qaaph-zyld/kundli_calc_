"""
Service Validation Validators
PGF Protocol: VAL_001
Gate: GATE_25
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union, Set, Callable
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field, validator
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)

class ValidationType(str, Enum):
    """Validation types"""
    DATA = "data"
    SCHEMA = "schema"
    BUSINESS = "business"
    SECURITY = "security"

class ValidationSeverity(str, Enum):
    """Validation severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ValidationRule(BaseModel):
    """Validation rule"""
    
    name: str
    type: ValidationType
    severity: ValidationSeverity
    message: str
    condition: str
    parameters: Optional[Dict[str, Any]] = None

class ValidationResult(BaseModel):
    """Validation result"""
    
    rule: ValidationRule
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

@dataclass
class ValidationMetrics:
    """Validation metrics"""
    
    total_validations: int
    passed_validations: int
    failed_validations: int
    warning_count: int
    error_count: int
    average_validation_time: float

class DataValidator:
    """Data validator"""
    
    def __init__(self):
        """Initialize validator"""
        self.rules: Dict[str, ValidationRule] = {}
        
        # Initialize metrics
        self.metrics = ValidationMetrics(
            total_validations=0,
            passed_validations=0,
            failed_validations=0,
            warning_count=0,
            error_count=0,
            average_validation_time=0.0
        )
    
    def add_rule(self, rule: ValidationRule):
        """Add validation rule"""
        self.rules[rule.name] = rule
    
    def remove_rule(self, rule_name: str):
        """Remove validation rule"""
        if rule_name in self.rules:
            del self.rules[rule_name]
    
    async def validate(
        self,
        data: Dict[str, Any],
        rule_types: Optional[List[ValidationType]] = None
    ) -> List[ValidationResult]:
        """Validate data against rules"""
        start_time = datetime.utcnow()
        results: List[ValidationResult] = []
        
        # Filter rules by type if specified
        rules = self.rules.values()
        if rule_types:
            rules = [r for r in rules if r.type in rule_types]
        
        for rule in rules:
            result = await self._evaluate_rule(rule, data)
            results.append(result)
            
            # Update metrics
            self.metrics.total_validations += 1
            if result.passed:
                self.metrics.passed_validations += 1
            else:
                self.metrics.failed_validations += 1
                if rule.severity == ValidationSeverity.WARNING:
                    self.metrics.warning_count += 1
                elif rule.severity in [
                    ValidationSeverity.ERROR,
                    ValidationSeverity.CRITICAL
                ]:
                    self.metrics.error_count += 1
        
        # Update average validation time
        end_time = datetime.utcnow()
        validation_time = (
            end_time - start_time
        ).total_seconds()
        
        self.metrics.average_validation_time = (
            self.metrics.average_validation_time *
            (self.metrics.total_validations - len(results)) +
            validation_time
        ) / self.metrics.total_validations
        
        return results
    
    async def _evaluate_rule(
        self,
        rule: ValidationRule,
        data: Dict[str, Any]
    ) -> ValidationResult:
        """Evaluate validation rule"""
        try:
            # Evaluate rule condition
            # In a real implementation, you would:
            # 1. Parse the condition expression
            # 2. Evaluate it against the data
            # 3. Return the result
            passed = True  # Placeholder
            message = rule.message
            
            if not passed:
                message = f"Validation failed: {message}"
            
            return ValidationResult(
                rule=rule,
                passed=passed,
                message=message,
                details={"data": data}
            )
        
        except Exception as e:
            return ValidationResult(
                rule=rule,
                passed=False,
                message=f"Validation error: {str(e)}",
                details={"error": str(e)}
            )

class SchemaValidator:
    """Schema validator"""
    
    def __init__(self):
        """Initialize validator"""
        self.schemas: Dict[str, Dict[str, Any]] = {}
        
        # Initialize metrics
        self.metrics = ValidationMetrics(
            total_validations=0,
            passed_validations=0,
            failed_validations=0,
            warning_count=0,
            error_count=0,
            average_validation_time=0.0
        )
    
    def add_schema(
        self,
        name: str,
        schema: Dict[str, Any]
    ):
        """Add validation schema"""
        self.schemas[name] = schema
    
    def remove_schema(self, schema_name: str):
        """Remove validation schema"""
        if schema_name in self.schemas:
            del self.schemas[schema_name]
    
    async def validate(
        self,
        data: Dict[str, Any],
        schema_name: str
    ) -> ValidationResult:
        """Validate data against schema"""
        start_time = datetime.utcnow()
        
        if schema_name not in self.schemas:
            return ValidationResult(
                rule=ValidationRule(
                    name="schema_validation",
                    type=ValidationType.SCHEMA,
                    severity=ValidationSeverity.ERROR,
                    message="Schema not found",
                    condition=""
                ),
                passed=False,
                message=f"Schema '{schema_name}' not found",
                details={"schema_name": schema_name}
            )
        
        try:
            # Validate data against schema
            # In a real implementation, you would:
            # 1. Use a schema validation library
            # 2. Validate the data
            # 3. Return the result
            passed = True  # Placeholder
            message = "Schema validation passed"
            
            if not passed:
                message = "Schema validation failed"
            
            # Update metrics
            self.metrics.total_validations += 1
            if passed:
                self.metrics.passed_validations += 1
            else:
                self.metrics.failed_validations += 1
                self.metrics.error_count += 1
            
            # Update average validation time
            end_time = datetime.utcnow()
            validation_time = (
                end_time - start_time
            ).total_seconds()
            
            self.metrics.average_validation_time = (
                self.metrics.average_validation_time *
                (self.metrics.total_validations - 1) +
                validation_time
            ) / self.metrics.total_validations
            
            return ValidationResult(
                rule=ValidationRule(
                    name="schema_validation",
                    type=ValidationType.SCHEMA,
                    severity=ValidationSeverity.ERROR,
                    message=message,
                    condition=""
                ),
                passed=passed,
                message=message,
                details={"data": data}
            )
        
        except Exception as e:
            return ValidationResult(
                rule=ValidationRule(
                    name="schema_validation",
                    type=ValidationType.SCHEMA,
                    severity=ValidationSeverity.ERROR,
                    message="Schema validation error",
                    condition=""
                ),
                passed=False,
                message=f"Schema validation error: {str(e)}",
                details={"error": str(e)}
            )

class BusinessValidator:
    """Business validator"""
    
    def __init__(self):
        """Initialize validator"""
        self.rules: Dict[str, ValidationRule] = {}
        
        # Initialize metrics
        self.metrics = ValidationMetrics(
            total_validations=0,
            passed_validations=0,
            failed_validations=0,
            warning_count=0,
            error_count=0,
            average_validation_time=0.0
        )
    
    def add_rule(self, rule: ValidationRule):
        """Add business rule"""
        self.rules[rule.name] = rule
    
    def remove_rule(self, rule_name: str):
        """Remove business rule"""
        if rule_name in self.rules:
            del self.rules[rule_name]
    
    async def validate(
        self,
        data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate data against business rules"""
        start_time = datetime.utcnow()
        results: List[ValidationResult] = []
        
        for rule in self.rules.values():
            result = await self._evaluate_rule(rule, data)
            results.append(result)
            
            # Update metrics
            self.metrics.total_validations += 1
            if result.passed:
                self.metrics.passed_validations += 1
            else:
                self.metrics.failed_validations += 1
                if rule.severity == ValidationSeverity.WARNING:
                    self.metrics.warning_count += 1
                elif rule.severity in [
                    ValidationSeverity.ERROR,
                    ValidationSeverity.CRITICAL
                ]:
                    self.metrics.error_count += 1
        
        # Update average validation time
        end_time = datetime.utcnow()
        validation_time = (
            end_time - start_time
        ).total_seconds()
        
        self.metrics.average_validation_time = (
            self.metrics.average_validation_time *
            (self.metrics.total_validations - len(results)) +
            validation_time
        ) / self.metrics.total_validations
        
        return results
    
    async def _evaluate_rule(
        self,
        rule: ValidationRule,
        data: Dict[str, Any]
    ) -> ValidationResult:
        """Evaluate business rule"""
        try:
            # Evaluate rule condition
            # In a real implementation, you would:
            # 1. Parse the business rule
            # 2. Apply it to the data
            # 3. Return the result
            passed = True  # Placeholder
            message = rule.message
            
            if not passed:
                message = f"Business validation failed: {message}"
            
            return ValidationResult(
                rule=rule,
                passed=passed,
                message=message,
                details={"data": data}
            )
        
        except Exception as e:
            return ValidationResult(
                rule=rule,
                passed=False,
                message=f"Business validation error: {str(e)}",
                details={"error": str(e)}
            )

class SecurityValidator:
    """Security validator"""
    
    def __init__(self):
        """Initialize validator"""
        self.rules: Dict[str, ValidationRule] = {}
        
        # Initialize metrics
        self.metrics = ValidationMetrics(
            total_validations=0,
            passed_validations=0,
            failed_validations=0,
            warning_count=0,
            error_count=0,
            average_validation_time=0.0
        )
    
    def add_rule(self, rule: ValidationRule):
        """Add security rule"""
        self.rules[rule.name] = rule
    
    def remove_rule(self, rule_name: str):
        """Remove security rule"""
        if rule_name in self.rules:
            del self.rules[rule_name]
    
    async def validate(
        self,
        data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate data against security rules"""
        start_time = datetime.utcnow()
        results: List[ValidationResult] = []
        
        for rule in self.rules.values():
            result = await self._evaluate_rule(rule, data)
            results.append(result)
            
            # Update metrics
            self.metrics.total_validations += 1
            if result.passed:
                self.metrics.passed_validations += 1
            else:
                self.metrics.failed_validations += 1
                if rule.severity == ValidationSeverity.WARNING:
                    self.metrics.warning_count += 1
                elif rule.severity in [
                    ValidationSeverity.ERROR,
                    ValidationSeverity.CRITICAL
                ]:
                    self.metrics.error_count += 1
        
        # Update average validation time
        end_time = datetime.utcnow()
        validation_time = (
            end_time - start_time
        ).total_seconds()
        
        self.metrics.average_validation_time = (
            self.metrics.average_validation_time *
            (self.metrics.total_validations - len(results)) +
            validation_time
        ) / self.metrics.total_validations
        
        return results
    
    async def _evaluate_rule(
        self,
        rule: ValidationRule,
        data: Dict[str, Any]
    ) -> ValidationResult:
        """Evaluate security rule"""
        try:
            # Evaluate rule condition
            # In a real implementation, you would:
            # 1. Parse the security rule
            # 2. Apply it to the data
            # 3. Return the result
            passed = True  # Placeholder
            message = rule.message
            
            if not passed:
                message = f"Security validation failed: {message}"
            
            return ValidationResult(
                rule=rule,
                passed=passed,
                message=message,
                details={"data": data}
            )
        
        except Exception as e:
            return ValidationResult(
                rule=rule,
                passed=False,
                message=f"Security validation error: {str(e)}",
                details={"error": str(e)}
            )
