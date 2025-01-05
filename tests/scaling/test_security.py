"""
Service Scaling Security Tests
PGF Protocol: SCAL_008
Gate: GATE_39
Version: 1.0.0
"""

import pytest
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.core.scaling.security import (
    ScalingSecurity,
    SecurityMode,
    SecurityScope,
    SecurityAction
)

@pytest.fixture
def security():
    """Security fixture"""
    return ScalingSecurity(
        mode=SecurityMode.STANDARD
    )

def test_create_token(security):
    """Test token creation"""
    # Arrange
    user = "test_user"
    scopes = [SecurityScope.READ, SecurityScope.WRITE]
    
    # Act
    token = security.create_token(user, scopes)
    
    # Assert
    assert isinstance(token, str)
    assert len(token) > 0

def test_validate_token(security):
    """Test token validation"""
    # Arrange
    user = "test_user"
    scopes = [SecurityScope.READ, SecurityScope.WRITE]
    token = security.create_token(user, scopes)
    
    # Create credentials mock
    class CredentialsMock:
        def __init__(self, token):
            self.credentials = token
    
    credentials = CredentialsMock(token)
    
    # Act
    payload = security.validate_token(credentials)
    
    # Assert
    assert payload["user"] == user
    assert all(
        s in payload["scopes"]
        for s in [s.value for s in scopes]
    )

def test_validate_expired_token(security):
    """Test expired token validation"""
    # Arrange
    user = "test_user"
    scopes = [SecurityScope.READ]
    
    # Create expired payload
    payload = {
        "user": user,
        "scopes": [s.value for s in scopes],
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    
    # Create expired token
    token = jwt.encode(
        payload,
        security.config.jwt_secret.get_secret_value(),
        algorithm=security.config.jwt_algorithm
    )
    
    # Create credentials mock
    class CredentialsMock:
        def __init__(self, token):
            self.credentials = token
    
    credentials = CredentialsMock(token)
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        security.validate_token(credentials)
    
    assert exc.value.status_code == 401
    assert "expired" in exc.value.detail.lower()

def test_validate_scope(security):
    """Test scope validation"""
    # Arrange
    payload = {
        "user": "test_user",
        "scopes": [SecurityScope.READ.value]
    }
    
    # Act & Assert - Valid scope
    security.validate_scope(payload, SecurityScope.READ)
    
    # Act & Assert - Invalid scope
    with pytest.raises(HTTPException) as exc:
        security.validate_scope(payload, SecurityScope.ADMIN)
    
    assert exc.value.status_code == 403
    assert "permissions" in exc.value.detail.lower()

def test_validate_rate_limit(security):
    """Test rate limit validation"""
    # Arrange
    user = "test_user"
    action = SecurityAction.SCALE
    
    # Act & Assert - Within limit
    security.validate_rate_limit(user, action)
    
    # Create rate limit entries
    for _ in range(security.config.rate_limit):
        security.audit_action(
            action=action,
            user=user,
            status="success",
            details={}
        )
    
    # Act & Assert - Exceeds limit
    with pytest.raises(HTTPException) as exc:
        security.validate_rate_limit(user, action)
    
    assert exc.value.status_code == 429
    assert "rate limit" in exc.value.detail.lower()

def test_validate_ip(security):
    """Test IP validation"""
    # Arrange
    security.config.allowed_ips = ["192.168.1.1"]
    
    # Act & Assert - Valid IP
    security.validate_ip("192.168.1.1")
    
    # Act & Assert - Invalid IP
    with pytest.raises(HTTPException) as exc:
        security.validate_ip("192.168.1.2")
    
    assert exc.value.status_code == 403
    assert "ip not allowed" in exc.value.detail.lower()

def test_validate_origin(security):
    """Test origin validation"""
    # Arrange
    security.config.allowed_origins = ["https://example.com"]
    
    # Act & Assert - Valid origin
    security.validate_origin("https://example.com")
    
    # Act & Assert - Invalid origin
    with pytest.raises(HTTPException) as exc:
        security.validate_origin("https://evil.com")
    
    assert exc.value.status_code == 403
    assert "origin not allowed" in exc.value.detail.lower()

def test_audit_action(security):
    """Test action auditing"""
    # Arrange
    action = SecurityAction.SCALE
    user = "test_user"
    status = "success"
    details = {"replicas": 3}
    
    # Act
    security.audit_action(
        action=action,
        user=user,
        status=status,
        details=details
    )
    
    # Assert
    assert len(security.audit_log) == 1
    audit = security.audit_log[0]
    assert audit.action == action
    assert audit.user == user
    assert audit.status == status
    assert audit.details == details

def test_hash_secret(security):
    """Test secret hashing"""
    # Arrange
    secret = "test-secret"
    
    # Act
    hashed = security.hash_secret(secret)
    
    # Assert
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # SHA-256 hash length

def test_rotate_secret(security):
    """Test secret rotation"""
    # Arrange
    old_secret = security.config.jwt_secret.get_secret_value()
    
    # Act
    security.rotate_secret()
    
    # Assert
    new_secret = security.config.jwt_secret.get_secret_value()
    assert new_secret != old_secret

def test_get_audit_log(security):
    """Test audit log retrieval"""
    # Arrange
    user = "test_user"
    action = SecurityAction.SCALE
    
    # Create audit entries
    security.audit_action(
        action=action,
        user=user,
        status="success",
        details={}
    )
    security.audit_action(
        action=SecurityAction.MONITOR,
        user="other_user",
        status="success",
        details={}
    )
    
    # Act - Filter by user
    user_log = security.get_audit_log(user=user)
    assert len(user_log) == 1
    assert user_log[0].user == user
    
    # Act - Filter by action
    action_log = security.get_audit_log(action=action)
    assert len(action_log) == 1
    assert action_log[0].action == action
    
    # Act - Filter by time range
    time_log = security.get_audit_log(
        start_time=datetime.utcnow() - timedelta(minutes=1),
        end_time=datetime.utcnow() + timedelta(minutes=1)
    )
    assert len(time_log) == 2
