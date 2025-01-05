"""
Service Validation Rules
PGF Protocol: VAL_002
Gate: GATE_25
Version: 1.0.0
"""

from typing import Dict, Any, List
from .validators import (
    ValidationType,
    ValidationSeverity,
    ValidationRule
)

# Data validation rules
DATA_VALIDATION_RULES = {
    "required_fields": ValidationRule(
        name="required_fields",
        type=ValidationType.DATA,
        severity=ValidationSeverity.ERROR,
        message="Required fields missing",
        condition="all_required_fields_present",
        parameters={
            "required_fields": [
                "birth_date",
                "birth_time",
                "latitude",
                "longitude"
            ]
        }
    ),
    "date_format": ValidationRule(
        name="date_format",
        type=ValidationType.DATA,
        severity=ValidationSeverity.ERROR,
        message="Invalid date format",
        condition="valid_date_format",
        parameters={
            "format": "YYYY-MM-DD"
        }
    ),
    "time_format": ValidationRule(
        name="time_format",
        type=ValidationType.DATA,
        severity=ValidationSeverity.ERROR,
        message="Invalid time format",
        condition="valid_time_format",
        parameters={
            "format": "HH:mm:ss"
        }
    ),
    "coordinate_range": ValidationRule(
        name="coordinate_range",
        type=ValidationType.DATA,
        severity=ValidationSeverity.ERROR,
        message="Coordinates out of range",
        condition="valid_coordinate_range",
        parameters={
            "latitude_range": [-90, 90],
            "longitude_range": [-180, 180]
        }
    )
}

# Schema validation rules
SCHEMA_VALIDATION_RULES = {
    "chart_request": {
        "type": "object",
        "required": [
            "birth_date",
            "birth_time",
            "latitude",
            "longitude"
        ],
        "properties": {
            "birth_date": {
                "type": "string",
                "format": "date"
            },
            "birth_time": {
                "type": "string",
                "format": "time"
            },
            "latitude": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
            },
            "longitude": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
            }
        }
    },
    "transit_request": {
        "type": "object",
        "required": [
            "birth_date",
            "birth_time",
            "transit_date",
            "latitude",
            "longitude"
        ],
        "properties": {
            "birth_date": {
                "type": "string",
                "format": "date"
            },
            "birth_time": {
                "type": "string",
                "format": "time"
            },
            "transit_date": {
                "type": "string",
                "format": "date"
            },
            "latitude": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
            },
            "longitude": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
            }
        }
    }
}

# Business validation rules
BUSINESS_VALIDATION_RULES = {
    "future_date": ValidationRule(
        name="future_date",
        type=ValidationType.BUSINESS,
        severity=ValidationSeverity.ERROR,
        message="Birth date cannot be in the future",
        condition="date_not_future",
        parameters=None
    ),
    "valid_location": ValidationRule(
        name="valid_location",
        type=ValidationType.BUSINESS,
        severity=ValidationSeverity.WARNING,
        message="Location might be invalid",
        condition="location_exists",
        parameters={
            "geocoding_service": "nominatim"
        }
    ),
    "timezone_match": ValidationRule(
        name="timezone_match",
        type=ValidationType.BUSINESS,
        severity=ValidationSeverity.WARNING,
        message="Time zone might not match location",
        condition="timezone_matches_location",
        parameters={
            "timezone_service": "timezonefinder"
        }
    ),
    "daylight_savings": ValidationRule(
        name="daylight_savings",
        type=ValidationType.BUSINESS,
        severity=ValidationSeverity.WARNING,
        message="Check daylight savings time",
        condition="check_dst",
        parameters={
            "dst_service": "pytz"
        }
    )
}

# Security validation rules
SECURITY_VALIDATION_RULES = {
    "input_sanitization": ValidationRule(
        name="input_sanitization",
        type=ValidationType.SECURITY,
        severity=ValidationSeverity.CRITICAL,
        message="Input contains potentially harmful content",
        condition="sanitize_input",
        parameters={
            "allowed_chars": r"[A-Za-z0-9\s\-\._]"
        }
    ),
    "request_rate": ValidationRule(
        name="request_rate",
        type=ValidationType.SECURITY,
        severity=ValidationSeverity.ERROR,
        message="Request rate exceeded",
        condition="check_request_rate",
        parameters={
            "max_requests": 100,
            "window_seconds": 3600
        }
    ),
    "api_key": ValidationRule(
        name="api_key",
        type=ValidationType.SECURITY,
        severity=ValidationSeverity.CRITICAL,
        message="Invalid API key",
        condition="validate_api_key",
        parameters=None
    ),
    "data_encryption": ValidationRule(
        name="data_encryption",
        type=ValidationType.SECURITY,
        severity=ValidationSeverity.ERROR,
        message="Data must be encrypted",
        condition="check_encryption",
        parameters={
            "required_algorithm": "AES-256"
        }
    )
}

def get_validation_rules(
    validation_type: ValidationType
) -> Dict[str, Any]:
    """Get validation rules by type"""
    
    rules_map = {
        ValidationType.DATA: DATA_VALIDATION_RULES,
        ValidationType.SCHEMA: SCHEMA_VALIDATION_RULES,
        ValidationType.BUSINESS: BUSINESS_VALIDATION_RULES,
        ValidationType.SECURITY: SECURITY_VALIDATION_RULES
    }
    
    return rules_map.get(validation_type, {})
