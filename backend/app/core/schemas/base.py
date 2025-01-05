"""Base schema models for standardized API responses."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, Dict

class BaseResponse(BaseModel):
    """Base response model for all API endpoints."""
    
    status: str = Field(..., description="Response status (success/error)")
    data: Dict[str, Any] = Field(..., description="Response data")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
