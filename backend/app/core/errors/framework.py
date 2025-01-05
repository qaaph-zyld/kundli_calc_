"""
Error Handling Framework
PGF Protocol: ERR_001
Gate: GATE_12
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Type, Union, Callable
from enum import Enum
from datetime import datetime
import traceback
import sys
from pydantic import BaseModel, Field
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class ErrorSeverity(str, Enum):
    """Error severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ErrorCategory(str, Enum):
    """Error categories"""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    BUSINESS_LOGIC = "business_logic"
    SYSTEM = "system"
    EXTERNAL_SERVICE = "external_service"
    DATABASE = "database"
    CACHE = "cache"
    NETWORK = "network"
    UNKNOWN = "unknown"

class ErrorCode(str, Enum):
    """Error codes"""
    # Validation errors (1xxx)
    INVALID_INPUT = "ERR_1001"
    MISSING_FIELD = "ERR_1002"
    INVALID_FORMAT = "ERR_1003"
    INVALID_TYPE = "ERR_1004"
    
    # Authentication errors (2xxx)
    INVALID_CREDENTIALS = "ERR_2001"
    TOKEN_EXPIRED = "ERR_2002"
    INVALID_TOKEN = "ERR_2003"
    
    # Authorization errors (3xxx)
    UNAUTHORIZED = "ERR_3001"
    INSUFFICIENT_PERMISSIONS = "ERR_3002"
    FORBIDDEN = "ERR_3003"
    
    # Business logic errors (4xxx)
    INVALID_OPERATION = "ERR_4001"
    RESOURCE_NOT_FOUND = "ERR_4002"
    DUPLICATE_RESOURCE = "ERR_4003"
    CALCULATION_ERROR = "ERR_4004"
    
    # System errors (5xxx)
    INTERNAL_ERROR = "ERR_5001"
    SERVICE_UNAVAILABLE = "ERR_5002"
    TIMEOUT = "ERR_5003"
    
    # External service errors (6xxx)
    EXTERNAL_SERVICE_ERROR = "ERR_6001"
    EXTERNAL_SERVICE_TIMEOUT = "ERR_6002"
    EXTERNAL_SERVICE_UNAVAILABLE = "ERR_6003"
    
    # Database errors (7xxx)
    DATABASE_ERROR = "ERR_7001"
    DATABASE_CONNECTION_ERROR = "ERR_7002"
    DATABASE_TIMEOUT = "ERR_7003"
    
    # Cache errors (8xxx)
    CACHE_ERROR = "ERR_8001"
    CACHE_CONNECTION_ERROR = "ERR_8002"
    CACHE_TIMEOUT = "ERR_8003"
    
    # Network errors (9xxx)
    NETWORK_ERROR = "ERR_9001"
    NETWORK_TIMEOUT = "ERR_9002"
    NETWORK_CONNECTION_ERROR = "ERR_9003"

class ErrorContext(BaseModel):
    """Error context"""
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    stack_trace: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    """Error response"""
    
    code: ErrorCode
    message: str
    category: ErrorCategory
    severity: ErrorSeverity
    context: Optional[ErrorContext] = None
    details: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None

class AppError(Exception):
    """Base application error"""
    
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        category: ErrorCategory,
        severity: ErrorSeverity,
        context: Optional[ErrorContext] = None,
        details: Optional[Dict[str, Any]] = None,
        suggestions: Optional[List[str]] = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        self.code = code
        self.message = message
        self.category = category
        self.severity = severity
        self.context = context or ErrorContext()
        self.details = details
        self.suggestions = suggestions
        self.status_code = status_code
        super().__init__(message)
    
    def to_response(self) -> ErrorResponse:
        """Convert to error response"""
        return ErrorResponse(
            code=self.code,
            message=self.message,
            category=self.category,
            severity=self.severity,
            context=self.context,
            details=self.details,
            suggestions=self.suggestions
        )

class ValidationError(AppError):
    """Validation error"""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        context: Optional[ErrorContext] = None
    ):
        super().__init__(
            code=ErrorCode.INVALID_INPUT,
            message=message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            context=context,
            details=details,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class AuthenticationError(AppError):
    """Authentication error"""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.INVALID_CREDENTIALS,
        context: Optional[ErrorContext] = None
    ):
        super().__init__(
            code=code,
            message=message,
            category=ErrorCategory.AUTHENTICATION,
            severity=ErrorSeverity.MEDIUM,
            context=context,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class AuthorizationError(AppError):
    """Authorization error"""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNAUTHORIZED,
        context: Optional[ErrorContext] = None
    ):
        super().__init__(
            code=code,
            message=message,
            category=ErrorCategory.AUTHORIZATION,
            severity=ErrorSeverity.HIGH,
            context=context,
            status_code=status.HTTP_403_FORBIDDEN
        )

class BusinessError(AppError):
    """Business logic error"""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.INVALID_OPERATION,
        context: Optional[ErrorContext] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=code,
            message=message,
            category=ErrorCategory.BUSINESS_LOGIC,
            severity=ErrorSeverity.MEDIUM,
            context=context,
            details=details,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class SystemError(AppError):
    """System error"""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        context: Optional[ErrorContext] = None
    ):
        super().__init__(
            code=code,
            message=message,
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            context=context,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class ExternalServiceError(AppError):
    """External service error"""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.EXTERNAL_SERVICE_ERROR,
        context: Optional[ErrorContext] = None
    ):
        super().__init__(
            code=code,
            message=message,
            category=ErrorCategory.EXTERNAL_SERVICE,
            severity=ErrorSeverity.HIGH,
            context=context,
            status_code=status.HTTP_502_BAD_GATEWAY
        )

class ErrorHandler:
    """Error handler"""
    
    def __init__(self):
        self.handlers: Dict[Type[Exception], Callable] = {}
        self._setup_default_handlers()
    
    def _setup_default_handlers(self) -> None:
        """Setup default error handlers"""
        self.handlers.update({
            RequestValidationError: self._handle_validation_error,
            StarletteHTTPException: self._handle_http_error,
            AppError: self._handle_app_error,
            Exception: self._handle_unknown_error
        })
    
    def register_handler(
        self,
        exception_type: Type[Exception],
        handler: Callable
    ) -> None:
        """Register error handler"""
        self.handlers[exception_type] = handler
    
    def _get_handler(self, exception: Exception) -> Callable:
        """Get appropriate error handler"""
        for exc_type, handler in self.handlers.items():
            if isinstance(exception, exc_type):
                return handler
        return self._handle_unknown_error
    
    def _create_error_context(
        self,
        request: Optional[Request] = None,
        exc_info: Optional[tuple] = None
    ) -> ErrorContext:
        """Create error context"""
        context = ErrorContext(
            timestamp=datetime.utcnow()
        )
        
        if request:
            context.request_id = request.headers.get("X-Request-ID")
            context.user_id = getattr(request.state, "user_id", None)
            context.ip_address = request.client.host
            context.endpoint = str(request.url)
            context.method = request.method
        
        if exc_info:
            context.stack_trace = "".join(traceback.format_exception(*exc_info))
        
        return context
    
    async def _handle_validation_error(
        self,
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        """Handle validation error"""
        context = self._create_error_context(request)
        error = ValidationError(
            message="Invalid input data",
            details={"errors": exc.errors()},
            context=context
        )
        return JSONResponse(
            status_code=error.status_code,
            content=error.to_response().dict()
        )
    
    async def _handle_http_error(
        self,
        request: Request,
        exc: StarletteHTTPException
    ) -> JSONResponse:
        """Handle HTTP error"""
        context = self._create_error_context(request)
        error = AppError(
            code=ErrorCode.INTERNAL_ERROR,
            message=str(exc.detail),
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.HIGH,
            context=context,
            status_code=exc.status_code
        )
        return JSONResponse(
            status_code=error.status_code,
            content=error.to_response().dict()
        )
    
    async def _handle_app_error(
        self,
        request: Request,
        exc: AppError
    ) -> JSONResponse:
        """Handle application error"""
        context = self._create_error_context(request)
        exc.context = context
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_response().dict()
        )
    
    async def _handle_unknown_error(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """Handle unknown error"""
        context = self._create_error_context(request, sys.exc_info())
        error = SystemError(
            message="An unexpected error occurred",
            context=context
        )
        return JSONResponse(
            status_code=error.status_code,
            content=error.to_response().dict()
        )
    
    async def handle_error(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """Handle error"""
        handler = self._get_handler(exc)
        return await handler(request, exc)
