"""
Service Validation Processors
PGF Protocol: VAL_003
Gate: GATE_25
Version: 1.0.0
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re
from .validators import (
    ValidationType,
    ValidationSeverity,
    ValidationRule,
    ValidationResult,
    DataValidator,
    SchemaValidator,
    BusinessValidator,
    SecurityValidator
)
from .rules import (
    get_validation_rules,
    DATA_VALIDATION_RULES,
    SCHEMA_VALIDATION_RULES,
    BUSINESS_VALIDATION_RULES,
    SECURITY_VALIDATION_RULES
)

class ValidationProcessor:
    """Validation processor"""
    
    def __init__(self):
        """Initialize processor"""
        # Initialize validators
        self.data_validator = DataValidator()
        self.schema_validator = SchemaValidator()
        self.business_validator = BusinessValidator()
        self.security_validator = SecurityValidator()
        
        # Load validation rules
        self._load_validation_rules()
    
    def _load_validation_rules(self):
        """Load validation rules into validators"""
        # Load data validation rules
        for rule in DATA_VALIDATION_RULES.values():
            self.data_validator.add_rule(rule)
        
        # Load schema validation rules
        for name, schema in SCHEMA_VALIDATION_RULES.items():
            self.schema_validator.add_schema(name, schema)
        
        # Load business validation rules
        for rule in BUSINESS_VALIDATION_RULES.values():
            self.business_validator.add_rule(rule)
        
        # Load security validation rules
        for rule in SECURITY_VALIDATION_RULES.values():
            self.security_validator.add_rule(rule)
    
    async def validate_request(
        self,
        request_type: str,
        data: Dict[str, Any],
        validation_types: Optional[List[ValidationType]] = None
    ) -> List[ValidationResult]:
        """Validate request data"""
        results: List[ValidationResult] = []
        
        # Determine validation types
        if validation_types is None:
            validation_types = [
                ValidationType.DATA,
                ValidationType.SCHEMA,
                ValidationType.BUSINESS,
                ValidationType.SECURITY
            ]
        
        # Perform validations
        if ValidationType.DATA in validation_types:
            data_results = await self.data_validator.validate(
                data,
                [ValidationType.DATA]
            )
            results.extend(data_results)
        
        if ValidationType.SCHEMA in validation_types:
            schema_result = await self.schema_validator.validate(
                data,
                request_type
            )
            results.append(schema_result)
        
        if ValidationType.BUSINESS in validation_types:
            business_results = await self.business_validator.validate(
                data
            )
            results.extend(business_results)
        
        if ValidationType.SECURITY in validation_types:
            security_results = await self.security_validator.validate(
                data
            )
            results.extend(security_results)
        
        return results
    
    def get_validation_metrics(self) -> Dict[str, Any]:
        """Get validation metrics"""
        return {
            "data_validation": vars(self.data_validator.metrics),
            "schema_validation": vars(self.schema_validator.metrics),
            "business_validation": vars(self.business_validator.metrics),
            "security_validation": vars(self.security_validator.metrics)
        }
    
    async def validate_chart_request(
        self,
        data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate chart request"""
        return await self.validate_request(
            "chart_request",
            data
        )
    
    async def validate_transit_request(
        self,
        data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate transit request"""
        return await self.validate_request(
            "transit_request",
            data
        )
    
    async def validate_progression_request(
        self,
        data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate progression request"""
        return await self.validate_request(
            "progression_request",
            data
        )
    
    async def validate_compatibility_request(
        self,
        data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate compatibility request"""
        return await self.validate_request(
            "compatibility_request",
            data
        )
    
    async def validate_prediction_request(
        self,
        data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate prediction request"""
        return await self.validate_request(
            "prediction_request",
            data
        )
    
    def _validate_date_format(
        self,
        date_str: str,
        format: str = "%Y-%m-%d"
    ) -> bool:
        """Validate date format"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    def _validate_time_format(
        self,
        time_str: str,
        format: str = "%H:%M:%S"
    ) -> bool:
        """Validate time format"""
        try:
            datetime.strptime(time_str, format)
            return True
        except ValueError:
            return False
    
    def _validate_coordinate_range(
        self,
        latitude: float,
        longitude: float
    ) -> bool:
        """Validate coordinate range"""
        return (
            -90 <= latitude <= 90 and
            -180 <= longitude <= 180
        )
    
    def _sanitize_input(
        self,
        input_str: str,
        pattern: str = r"[A-Za-z0-9\s\-\._]"
    ) -> str:
        """Sanitize input string"""
        return re.sub(f"[^{pattern}]", "", input_str)
    
    def _check_request_rate(
        self,
        user_id: str,
        max_requests: int = 100,
        window_seconds: int = 3600
    ) -> bool:
        """Check request rate"""
        # In a real implementation, you would:
        # 1. Track request counts in a database
        # 2. Check against the limit
        # 3. Update the count
        return True
    
    def _validate_api_key(
        self,
        api_key: str
    ) -> bool:
        """Validate API key"""
        # In a real implementation, you would:
        # 1. Check the API key against a database
        # 2. Verify its validity and permissions
        return True
    
    def _check_encryption(
        self,
        data: Dict[str, Any],
        required_algorithm: str = "AES-256"
    ) -> bool:
        """Check data encryption"""
        # In a real implementation, you would:
        # 1. Check if the data is encrypted
        # 2. Verify the encryption algorithm
        return True
