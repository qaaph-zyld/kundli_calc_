"""Base schema models for standardized API responses."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class BaseResponse(BaseModel):
    """Base response model for all API endpoints."""

    status: str = Field(..., description="Response status (success/error)")
    data: Dict[str, Any] = Field(..., description="Response data")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
