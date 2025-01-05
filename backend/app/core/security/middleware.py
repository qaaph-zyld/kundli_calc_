"""
Authentication Middleware
PGF Protocol: AUTH_002
Gate: GATE_4
Version: 1.0.0
"""

from fastapi import Request, Response
from ..middleware.base import BaseMiddleware, MiddlewarePriority
from .auth import auth_context, SecurityLevel
from typing import Optional
import jwt
from datetime import datetime

class AuthenticationMiddleware(BaseMiddleware):
    """Zero-trust authentication middleware"""
    
    def __init__(self):
        super().__init__(priority=MiddlewarePriority.CRITICAL)
        self._public_paths = {"/api/docs", "/api/redoc", "/api/openapi.json"}
    
    async def process_request(self, request: Request) -> Request:
        """Process and validate authentication for incoming requests"""
        # Skip authentication for public paths
        if request.url.path in self._public_paths:
            return request
            
        # Extract token
        token = self._extract_token(request)
        if not token:
            request.state.auth = {"security_level": SecurityLevel.PUBLIC}
            return request
            
        try:
            # Validate token
            token_data = await auth_context.validate_token(token)
            
            # Enhance request with auth data
            request.state.auth = {
                "user_id": token_data.sub,
                "scopes": token_data.scopes,
                "security_level": token_data.security_level,
                "device_id": token_data.device_id,
                "ip_address": token_data.ip_address
            }
            
            # Verify IP address if provided
            if token_data.ip_address and token_data.ip_address != request.client.host:
                raise jwt.InvalidTokenError("IP address mismatch")
            
        except jwt.InvalidTokenError:
            request.state.auth = {"security_level": SecurityLevel.PUBLIC}
        
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Process authentication for outgoing responses"""
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """Extract authentication token from request"""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
            
        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return None
            
        return parts[1]

class SecurityMiddleware(BaseMiddleware):
    """Additional security measures middleware"""
    
    def __init__(self):
        super().__init__(priority=MiddlewarePriority.CRITICAL)
    
    async def process_request(self, request: Request) -> Request:
        """Apply security measures to incoming requests"""
        # Add request timestamp
        request.state.timestamp = datetime.utcnow()
        
        # Verify content type
        content_type = request.headers.get("content-type", "")
        if request.method in ["POST", "PUT", "PATCH"] and "application/json" not in content_type:
            raise ValueError("Invalid content type")
        
        return request
    
    async def process_response(self, response: Response) -> Response:
        """Apply security measures to outgoing responses"""
        # Remove sensitive headers
        response.headers.pop("Server", None)
        response.headers.pop("X-Powered-By", None)
        
        # Add security headers
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response
