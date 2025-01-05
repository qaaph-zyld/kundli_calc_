"""
Kundli-specific validators
PGF Protocol: VAL_002
Gate: GATE_25
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import pytz
from pydantic import BaseModel, Field, validator
from .validators import (
    ValidationRule,
    ValidationType,
    ValidationSeverity,
    DataValidator,
    BusinessValidator
)

class KundliDataValidator(DataValidator):
    """Validator for Kundli calculation input data"""

    def __init__(self):
        """Initialize Kundli data validator"""
        super().__init__()
        self._initialize_rules()

    def _initialize_rules(self):
        """Initialize Kundli-specific validation rules"""
        
        # Date validation rule
        self.add_rule(ValidationRule(
            name="date_format",
            type=ValidationType.DATA,
            severity=ValidationSeverity.ERROR,
            message="Invalid date format. Use YYYY-MM-DD",
            condition="datetime.strptime(value, '%Y-%m-%d')",
            parameters={"format": "%Y-%m-%d"}
        ))

        # Time validation rule
        self.add_rule(ValidationRule(
            name="time_format",
            type=ValidationType.DATA,
            severity=ValidationSeverity.ERROR,
            message="Invalid time format. Use HH:MM:SS",
            condition="datetime.strptime(value, '%H:%M:%S')",
            parameters={"format": "%H:%M:%S"}
        ))

        # Latitude validation rule
        self.add_rule(ValidationRule(
            name="latitude_range",
            type=ValidationType.DATA,
            severity=ValidationSeverity.ERROR,
            message="Latitude must be between -90 and 90 degrees",
            condition="-90 <= float(value) <= 90",
            parameters={"min": -90, "max": 90}
        ))

        # Longitude validation rule
        self.add_rule(ValidationRule(
            name="longitude_range",
            type=ValidationType.DATA,
            severity=ValidationSeverity.ERROR,
            message="Longitude must be between -180 and 180 degrees",
            condition="-180 <= float(value) <= 180",
            parameters={"min": -180, "max": 180}
        ))

        # Timezone validation rule
        self.add_rule(ValidationRule(
            name="timezone_valid",
            type=ValidationType.DATA,
            severity=ValidationSeverity.ERROR,
            message="Invalid timezone",
            condition="value in pytz.all_timezones",
            parameters={"timezones": pytz.all_timezones}
        ))

class KundliBusinessValidator(BusinessValidator):
    """Validator for Kundli business rules"""

    def __init__(self):
        """Initialize Kundli business validator"""
        super().__init__()
        self._initialize_rules()

    def _initialize_rules(self):
        """Initialize Kundli-specific business rules"""
        
        # Future date validation
        self.add_rule(ValidationRule(
            name="no_future_date",
            type=ValidationType.BUSINESS,
            severity=ValidationSeverity.ERROR,
            message="Birth date cannot be in the future",
            condition="datetime.strptime(value, '%Y-%m-%d') <= datetime.now()",
            parameters={}
        ))

        # Ancient date validation
        self.add_rule(ValidationRule(
            name="no_ancient_date",
            type=ValidationType.BUSINESS,
            severity=ValidationSeverity.WARNING,
            message="Birth date is very old (before 1800)",
            condition="datetime.strptime(value, '%Y-%m-%d').year >= 1800",
            parameters={"min_year": 1800}
        ))

        # Location accuracy validation
        self.add_rule(ValidationRule(
            name="location_precision",
            type=ValidationType.BUSINESS,
            severity=ValidationSeverity.WARNING,
            message="Location coordinates should have at least 4 decimal places for accuracy",
            condition="len(str(float(value)).split('.')[-1]) >= 4",
            parameters={"min_precision": 4}
        ))

class KundliValidationRequest(BaseModel):
    """Request model for Kundli validation"""

    date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    time: str = Field(..., description="Birth time (HH:MM:SS)")
    latitude: float = Field(..., description="Birth place latitude")
    longitude: float = Field(..., description="Birth place longitude")
    timezone: str = Field(..., description="Timezone name")
    validation_types: Optional[List[ValidationType]] = Field(
        default=[ValidationType.DATA, ValidationType.BUSINESS],
        description="Types of validation to perform"
    )

class KundliValidationResponse(BaseModel):
    """Response model for Kundli validation"""

    is_valid: bool = Field(..., description="Overall validation result")
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of validation errors"
    )
    warnings: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of validation warnings"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Validation metadata"
    )

async def validate_kundli_data(request: KundliValidationRequest) -> KundliValidationResponse:
    """Validate Kundli calculation input data"""
    
    # Initialize validators
    data_validator = KundliDataValidator()
    business_validator = KundliBusinessValidator()
    
    # Convert request to dictionary
    data = request.dict()
    
    # Initialize response
    response = KundliValidationResponse(
        is_valid=True,
        metadata={"timestamp": datetime.utcnow()}
    )
    
    # Perform data validation
    if ValidationType.DATA in request.validation_types:
        data_results = await data_validator.validate(data)
        for result in data_results:
            if not result.passed:
                response.is_valid = False
                if result.rule.severity == ValidationSeverity.ERROR:
                    response.errors.append({
                        "type": "data",
                        "rule": result.rule.name,
                        "message": result.message
                    })
                else:
                    response.warnings.append({
                        "type": "data",
                        "rule": result.rule.name,
                        "message": result.message
                    })
    
    # Perform business validation
    if ValidationType.BUSINESS in request.validation_types:
        business_results = await business_validator.validate(data)
        for result in business_results:
            if not result.passed:
                if result.rule.severity == ValidationSeverity.ERROR:
                    response.is_valid = False
                    response.errors.append({
                        "type": "business",
                        "rule": result.rule.name,
                        "message": result.message
                    })
                else:
                    response.warnings.append({
                        "type": "business",
                        "rule": result.rule.name,
                        "message": result.message
                    })
    
    # Add validation metrics to metadata
    response.metadata.update({
        "data_metrics": data_validator.metrics.__dict__,
        "business_metrics": business_validator.metrics.__dict__
    })
    
    return response
