"""
Error handling module
PGF Protocol: ERR_001
Gate: GATE_25
Version: 1.0.0
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ErrorCode(str, Enum):
    """Error codes for the application"""
    
    # Authentication errors
    INVALID_CREDENTIALS = "AUTH001"
    TOKEN_EXPIRED = "AUTH002"
    INSUFFICIENT_PERMISSIONS = "AUTH003"
    
    # Validation errors
    INVALID_INPUT = "VAL001"
    MISSING_REQUIRED = "VAL002"
    INVALID_FORMAT = "VAL003"
    
    # Calculation errors
    CALCULATION_FAILED = "CALC001"
    INVALID_COORDINATES = "CALC002"
    EPHEMERIS_ERROR = "CALC003"
    
    # Database errors
    DB_CONNECTION_ERROR = "DB001"
    DB_QUERY_ERROR = "DB002"
    DB_WRITE_ERROR = "DB003"
    
    # Cache errors
    CACHE_CONNECTION_ERROR = "CACHE001"
    CACHE_READ_ERROR = "CACHE002"
    CACHE_WRITE_ERROR = "CACHE003"
    
    # System errors
    INTERNAL_ERROR = "SYS001"
    SERVICE_UNAVAILABLE = "SYS002"
    RATE_LIMIT_EXCEEDED = "SYS003"

class ErrorCategory(str, Enum):
    """Error categories"""
    
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    CALCULATION = "calculation"
    DATABASE = "database"
    CACHE = "cache"
    SYSTEM = "system"

class ErrorSeverity(str, Enum):
    """Error severity levels"""
    
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ErrorResponse(BaseModel):
    """Standardized error response model"""
    
    code: ErrorCode
    message: str
    category: ErrorCategory
    severity: ErrorSeverity
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
    
    class Config:
        use_enum_values = True

class ErrorHandler:
    """Error handler for the application"""
    
    @staticmethod
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        """Handle HTTP exceptions"""
        
        error = ErrorResponse(
            code=ErrorCode.INTERNAL_ERROR,
            message=str(exc.detail),
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.ERROR,
            details={
                "status_code": exc.status_code,
                "headers": dict(exc.headers) if exc.headers else None
            },
            request_id=request.state.request_id if hasattr(request.state, "request_id") else None
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error.dict()
        )
    
    @staticmethod
    async def handle_validation_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle validation exceptions"""
        
        error = ErrorResponse(
            code=ErrorCode.INVALID_INPUT,
            message="Validation error",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
            details={"errors": str(exc)},
            request_id=request.state.request_id if hasattr(request.state, "request_id") else None
        )
        
        return JSONResponse(
            status_code=422,
            content=error.dict()
        )
    
    @staticmethod
    async def handle_calculation_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle calculation exceptions"""
        
        error = ErrorResponse(
            code=ErrorCode.CALCULATION_FAILED,
            message="Calculation error",
            category=ErrorCategory.CALCULATION,
            severity=ErrorSeverity.ERROR,
            details={"error": str(exc)},
            request_id=request.state.request_id if hasattr(request.state, "request_id") else None
        )
        
        return JSONResponse(
            status_code=500,
            content=error.dict()
        )
    
    @staticmethod
    async def handle_database_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle database exceptions"""
        
        error = ErrorResponse(
            code=ErrorCode.DB_QUERY_ERROR,
            message="Database error",
            category=ErrorCategory.DATABASE,
            severity=ErrorSeverity.ERROR,
            details={"error": str(exc)},
            request_id=request.state.request_id if hasattr(request.state, "request_id") else None
        )
        
        return JSONResponse(
            status_code=503,
            content=error.dict()
        )
    
    @staticmethod
    async def handle_cache_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle cache exceptions"""
        
        error = ErrorResponse(
            code=ErrorCode.CACHE_READ_ERROR,
            message="Cache error",
            category=ErrorCategory.CACHE,
            severity=ErrorSeverity.WARNING,
            details={"error": str(exc)},
            request_id=request.state.request_id if hasattr(request.state, "request_id") else None
        )
        
        return JSONResponse(
            status_code=503,
            content=error.dict()
        )
    
    @staticmethod
    async def handle_generic_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle generic exceptions"""
        
        error = ErrorResponse(
            code=ErrorCode.INTERNAL_ERROR,
            message="Internal server error",
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            details={"error": str(exc)},
            request_id=request.state.request_id if hasattr(request.state, "request_id") else None
        )
        
        return JSONResponse(
            status_code=500,
            content=error.dict()
        )
