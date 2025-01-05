"""
API Response Models
PGF Protocol: MOD_001
Gate: GATE_1
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class BaseResponse(BaseModel):
    """Base response model"""
    status: str = Field(..., description="Response status")
    message: Optional[str] = Field(None, description="Response message")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Response metadata")

class KundliResponse(BaseResponse):
    """Response model for Kundli calculations"""
    data: Dict[str, Any] = Field(..., description="Kundli calculation data")
    chart_data: Optional[Dict[str, Any]] = Field(None, description="Chart data")
    patterns: Optional[List[Dict[str, Any]]] = Field(None, description="Detected patterns")
    yogas: Optional[List[Dict[str, Any]]] = Field(None, description="Detected yogas")

class TransitResponse(BaseResponse):
    """Response model for transit calculations"""
    data: Dict[str, Any] = Field(..., description="Transit calculation data")
    birth_chart: Dict[str, Any] = Field(..., description="Birth chart data")
    transit_chart: Dict[str, Any] = Field(..., description="Transit chart data")
    aspects: List[Dict[str, Any]] = Field(..., description="Transit aspects")

class MatchingResponse(BaseResponse):
    """Response model for compatibility matching"""
    data: Dict[str, Any] = Field(..., description="Matching calculation data")
    chart1: Dict[str, Any] = Field(..., description="First person's chart")
    chart2: Dict[str, Any] = Field(..., description="Second person's chart")
    correlations: List[Dict[str, Any]] = Field(..., description="Chart correlations")
    scores: Dict[str, float] = Field(..., description="Matching scores")

class PredictionResponse(BaseResponse):
    """Response model for predictions"""
    data: Dict[str, Any] = Field(..., description="Prediction data")
    chart_data: Dict[str, Any] = Field(..., description="Chart data")
    predictions: List[Dict[str, Any]] = Field(..., description="Generated predictions")

class DashaResponse(BaseResponse):
    """Response model for dasha calculations"""
    data: Dict[str, Any] = Field(..., description="Dasha calculation data")
    chart_data: Dict[str, Any] = Field(..., description="Chart data")
    dasha_periods: List[Dict[str, Any]] = Field(..., description="Dasha periods")

class MuhurtaResponse(BaseResponse):
    """Response model for muhurta calculations"""
    data: Dict[str, Any] = Field(..., description="Muhurta calculation data")
    auspicious_times: List[Dict[str, Any]] = Field(..., description="Auspicious times")
    activity_type: str = Field(..., description="Activity type")

class ErrorResponse(BaseResponse):
    """Response model for errors"""
    error: Dict[str, Any] = Field(..., description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
