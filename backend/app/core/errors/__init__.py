"""
Error Handling Module
PGF Protocol: ERR_003
Gate: GATE_12
Version: 1.0.0
"""

from .config import get_error_message, get_error_severity, get_error_suggestions
from .framework import (
    AppError,
    AuthenticationError,
    AuthorizationError,
    BusinessError,
    ErrorCategory,
    ErrorCode,
    ErrorContext,
    ErrorHandler,
    ErrorResponse,
    ErrorSeverity,
    ExternalServiceError,
    SystemError,
    ValidationError,
)

__all__ = [
    "ErrorSeverity",
    "ErrorCategory",
    "ErrorCode",
    "ErrorContext",
    "ErrorResponse",
    "AppError",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "BusinessError",
    "SystemError",
    "ExternalServiceError",
    "ErrorHandler",
    "get_error_message",
    "get_error_severity",
    "get_error_suggestions",
]
