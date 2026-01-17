"""Security package"""

from .authorization import authorization_manager
from .engine import SecurityScope, security_engine

# Export commonly used functions from security_engine
create_access_token = security_engine.create_access_token
verify_password = security_engine.verify_password
get_password_hash = security_engine.get_password_hash

__all__ = [
    "security_engine",
    "SecurityScope",
    "authorization_manager",
    "create_access_token",
    "verify_password",
    "get_password_hash",
]
