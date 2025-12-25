"""
User-Friendly Error Messages
============================
Centralized error messages with helpful guidance for users.
"""

from typing import Dict, Any
from enum import Enum


class ErrorCode(str, Enum):
    """Standard error codes for API"""
    
    # Validation Errors (4xx)
    INVALID_DATE_FORMAT = "INVALID_DATE_FORMAT"
    INVALID_TIME_FORMAT = "INVALID_TIME_FORMAT"
    INVALID_COORDINATES = "INVALID_COORDINATES"
    INVALID_TIMEZONE = "INVALID_TIMEZONE"
    FUTURE_DATE = "FUTURE_DATE"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    INVALID_AYANAMSA = "INVALID_AYANAMSA"
    INVALID_HOUSE_SYSTEM = "INVALID_HOUSE_SYSTEM"
    
    # Calculation Errors (5xx)
    CALCULATION_FAILED = "CALCULATION_FAILED"
    EPHEMERIS_ERROR = "EPHEMERIS_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    
    # Rate Limiting (429)
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"


class ErrorMessages:
    """User-friendly error messages with solutions"""
    
    MESSAGES: Dict[ErrorCode, Dict[str, Any]] = {
        ErrorCode.INVALID_DATE_FORMAT: {
            "message": "Invalid date format provided",
            "detail": "Date must be in YYYY-MM-DD format (e.g., 1990-10-09)",
            "solution": "Please provide the date in YYYY-MM-DD format",
            "example": "1990-10-09"
        },
        
        ErrorCode.INVALID_TIME_FORMAT: {
            "message": "Invalid time format provided",
            "detail": "Time must be in HH:MM:SS format (e.g., 14:30:00)",
            "solution": "Please provide the time in 24-hour HH:MM:SS format",
            "example": "14:30:00"
        },
        
        ErrorCode.INVALID_COORDINATES: {
            "message": "Invalid geographic coordinates",
            "detail": "Latitude must be between -90 and +90, Longitude must be between -180 and +180",
            "solution": "Please verify your latitude and longitude values",
            "example": "Latitude: 28.6139, Longitude: 77.2090 (Delhi)"
        },
        
        ErrorCode.INVALID_TIMEZONE: {
            "message": "Invalid or unknown timezone",
            "detail": "The timezone identifier is not recognized",
            "solution": "Use a valid timezone identifier (e.g., 'Asia/Kolkata', 'America/New_York')",
            "example": "Asia/Kolkata"
        },
        
        ErrorCode.FUTURE_DATE: {
            "message": "Birth date cannot be in the future",
            "detail": "The provided date is after the current date",
            "solution": "Please provide a valid past date for birth calculations",
            "example": "Use a date before today"
        },
        
        ErrorCode.MISSING_REQUIRED_FIELD: {
            "message": "Required field is missing",
            "detail": "One or more required fields are not provided",
            "solution": "Please ensure all required fields are included in your request",
            "example": "Required: date, time, latitude, longitude, timezone"
        },
        
        ErrorCode.INVALID_AYANAMSA: {
            "message": "Invalid ayanamsa system specified",
            "detail": "The ayanamsa system is not recognized",
            "solution": "Use one of: lahiri, raman, kp, yukteshwar, true_chitra, fagan_bradley, deluce, sassanian",
            "example": "lahiri"
        },
        
        ErrorCode.INVALID_HOUSE_SYSTEM: {
            "message": "Invalid house system specified",
            "detail": "The house system is not supported",
            "solution": "Use one of: W (Whole Sign), P (Placidus), K (Koch), E (Equal)",
            "example": "W"
        },
        
        ErrorCode.CALCULATION_FAILED: {
            "message": "Calculation failed",
            "detail": "An error occurred during astrological calculations",
            "solution": "Please verify your input data and try again. If the problem persists, contact support.",
            "example": None
        },
        
        ErrorCode.EPHEMERIS_ERROR: {
            "message": "Ephemeris data error",
            "detail": "Unable to calculate planetary positions for the given date",
            "solution": "The date may be outside the supported range (1800-2100). Please use a date within this range.",
            "example": "Supported: 1800-01-01 to 2100-12-31"
        },
        
        ErrorCode.DATABASE_ERROR: {
            "message": "Database connection error",
            "detail": "Unable to access the database",
            "solution": "This is a temporary issue. Please try again in a few moments.",
            "example": None
        },
        
        ErrorCode.TIMEOUT_ERROR: {
            "message": "Request timeout",
            "detail": "The calculation took too long to complete",
            "solution": "Try simplifying your request or try again later.",
            "example": None
        },
        
        ErrorCode.RATE_LIMIT_EXCEEDED: {
            "message": "Rate limit exceeded",
            "detail": "You have made too many requests in a short period",
            "solution": "Please wait a moment before making another request.",
            "example": "Limit: 100 requests per minute"
        }
    }
    
    @classmethod
    def get_error_response(
        cls,
        error_code: ErrorCode,
        field: str = None,
        additional_context: str = None
    ) -> Dict[str, Any]:
        """
        Get formatted error response
        
        Args:
            error_code: Error code enum
            field: Field name that caused the error
            additional_context: Additional context information
            
        Returns:
            Formatted error response dictionary
        """
        error_info = cls.MESSAGES.get(error_code, {
            "message": "An error occurred",
            "detail": "Unknown error",
            "solution": "Please contact support",
            "example": None
        })
        
        response = {
            "error": True,
            "error_code": error_code.value,
            "message": error_info["message"],
            "detail": error_info["detail"],
            "solution": error_info["solution"]
        }
        
        if error_info.get("example"):
            response["example"] = error_info["example"]
        
        if field:
            response["field"] = field
        
        if additional_context:
            response["context"] = additional_context
        
        return response
    
    @classmethod
    def format_validation_error(
        cls,
        field: str,
        value: Any,
        error_code: ErrorCode,
        additional_info: str = None
    ) -> Dict[str, Any]:
        """
        Format a validation error with field information
        
        Args:
            field: Field name that failed validation
            value: The invalid value
            error_code: Error code
            additional_info: Additional information
            
        Returns:
            Formatted validation error
        """
        response = cls.get_error_response(error_code, field)
        response["invalid_value"] = str(value)
        
        if additional_info:
            response["additional_info"] = additional_info
        
        return response


def create_validation_error(
    field: str,
    value: Any,
    error_type: str,
    expected_format: str = None
) -> Dict[str, Any]:
    """
    Create a detailed validation error
    
    Args:
        field: Field name
        value: Invalid value
        error_type: Type of validation error
        expected_format: Expected format description
        
    Returns:
        Validation error dictionary
    """
    error = {
        "error": True,
        "type": "validation_error",
        "field": field,
        "value": str(value),
        "error_type": error_type
    }
    
    if expected_format:
        error["expected_format"] = expected_format
    
    return error


def create_success_response(
    data: Any,
    message: str = "Success",
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message: Success message
        metadata: Optional metadata
        
    Returns:
        Standardized success response
    """
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    
    if metadata:
        response["metadata"] = metadata
    
    return response
