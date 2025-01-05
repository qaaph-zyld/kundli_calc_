"""
Error Configuration
PGF Protocol: ERR_002
Gate: GATE_12
Version: 1.0.0
"""

from typing import Dict, Any, List
from .framework import (
    ErrorCode,
    ErrorCategory,
    ErrorSeverity,
    ErrorResponse
)

# Error messages
ERROR_MESSAGES: Dict[ErrorCode, str] = {
    # Validation errors
    ErrorCode.INVALID_INPUT: "The provided input data is invalid",
    ErrorCode.MISSING_FIELD: "Required field is missing",
    ErrorCode.INVALID_FORMAT: "Field format is invalid",
    ErrorCode.INVALID_TYPE: "Field type is invalid",
    
    # Authentication errors
    ErrorCode.INVALID_CREDENTIALS: "Invalid credentials provided",
    ErrorCode.TOKEN_EXPIRED: "Authentication token has expired",
    ErrorCode.INVALID_TOKEN: "Invalid authentication token",
    
    # Authorization errors
    ErrorCode.UNAUTHORIZED: "Unauthorized access",
    ErrorCode.INSUFFICIENT_PERMISSIONS: "Insufficient permissions",
    ErrorCode.FORBIDDEN: "Access forbidden",
    
    # Business logic errors
    ErrorCode.INVALID_OPERATION: "Invalid operation requested",
    ErrorCode.RESOURCE_NOT_FOUND: "Requested resource not found",
    ErrorCode.DUPLICATE_RESOURCE: "Resource already exists",
    ErrorCode.CALCULATION_ERROR: "Error in astrological calculation",
    
    # System errors
    ErrorCode.INTERNAL_ERROR: "Internal server error occurred",
    ErrorCode.SERVICE_UNAVAILABLE: "Service is currently unavailable",
    ErrorCode.TIMEOUT: "Operation timed out",
    
    # External service errors
    ErrorCode.EXTERNAL_SERVICE_ERROR: "External service error occurred",
    ErrorCode.EXTERNAL_SERVICE_TIMEOUT: "External service request timed out",
    ErrorCode.EXTERNAL_SERVICE_UNAVAILABLE: "External service is unavailable",
    
    # Database errors
    ErrorCode.DATABASE_ERROR: "Database error occurred",
    ErrorCode.DATABASE_CONNECTION_ERROR: "Database connection error",
    ErrorCode.DATABASE_TIMEOUT: "Database operation timed out",
    
    # Cache errors
    ErrorCode.CACHE_ERROR: "Cache error occurred",
    ErrorCode.CACHE_CONNECTION_ERROR: "Cache connection error",
    ErrorCode.CACHE_TIMEOUT: "Cache operation timed out",
    
    # Network errors
    ErrorCode.NETWORK_ERROR: "Network error occurred",
    ErrorCode.NETWORK_TIMEOUT: "Network operation timed out",
    ErrorCode.NETWORK_CONNECTION_ERROR: "Network connection error"
}

# Error categories and their default severity
CATEGORY_SEVERITY: Dict[ErrorCategory, ErrorSeverity] = {
    ErrorCategory.VALIDATION: ErrorSeverity.LOW,
    ErrorCategory.AUTHENTICATION: ErrorSeverity.MEDIUM,
    ErrorCategory.AUTHORIZATION: ErrorSeverity.HIGH,
    ErrorCategory.BUSINESS_LOGIC: ErrorSeverity.MEDIUM,
    ErrorCategory.SYSTEM: ErrorSeverity.CRITICAL,
    ErrorCategory.EXTERNAL_SERVICE: ErrorSeverity.HIGH,
    ErrorCategory.DATABASE: ErrorSeverity.HIGH,
    ErrorCategory.CACHE: ErrorSeverity.MEDIUM,
    ErrorCategory.NETWORK: ErrorSeverity.HIGH,
    ErrorCategory.UNKNOWN: ErrorSeverity.HIGH
}

# Error suggestions
ERROR_SUGGESTIONS: Dict[ErrorCode, List[str]] = {
    # Validation errors
    ErrorCode.INVALID_INPUT: [
        "Check the input data format",
        "Ensure all required fields are provided",
        "Verify the data types of all fields"
    ],
    ErrorCode.MISSING_FIELD: [
        "Provide all required fields",
        "Check the API documentation for required fields"
    ],
    
    # Authentication errors
    ErrorCode.INVALID_CREDENTIALS: [
        "Verify your credentials",
        "Reset your password if needed"
    ],
    ErrorCode.TOKEN_EXPIRED: [
        "Please log in again",
        "Refresh your authentication token"
    ],
    
    # Authorization errors
    ErrorCode.UNAUTHORIZED: [
        "Log in to access this resource",
        "Check your account permissions"
    ],
    ErrorCode.INSUFFICIENT_PERMISSIONS: [
        "Request elevated permissions",
        "Contact your administrator"
    ],
    
    # Business logic errors
    ErrorCode.RESOURCE_NOT_FOUND: [
        "Verify the resource identifier",
        "Check if the resource exists"
    ],
    ErrorCode.CALCULATION_ERROR: [
        "Verify input parameters",
        "Check calculation constraints",
        "Try with different input values"
    ],
    
    # System errors
    ErrorCode.INTERNAL_ERROR: [
        "Try again later",
        "Contact support if the issue persists"
    ],
    ErrorCode.SERVICE_UNAVAILABLE: [
        "Wait for service restoration",
        "Check service status page"
    ],
    
    # Database errors
    ErrorCode.DATABASE_ERROR: [
        "Try again later",
        "Check database connection",
        "Verify data integrity"
    ],
    
    # Cache errors
    ErrorCode.CACHE_ERROR: [
        "Try again later",
        "Clear your cache",
        "Refresh the page"
    ],
    
    # Network errors
    ErrorCode.NETWORK_ERROR: [
        "Check your internet connection",
        "Try again later",
        "Contact your network administrator"
    ]
}

def get_error_message(code: ErrorCode) -> str:
    """Get error message for error code"""
    return ERROR_MESSAGES.get(code, "An unknown error occurred")

def get_error_severity(category: ErrorCategory) -> ErrorSeverity:
    """Get default severity for error category"""
    return CATEGORY_SEVERITY.get(category, ErrorSeverity.HIGH)

def get_error_suggestions(code: ErrorCode) -> List[str]:
    """Get suggestions for error code"""
    return ERROR_SUGGESTIONS.get(code, ["Try again later"])
