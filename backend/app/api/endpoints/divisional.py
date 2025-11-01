"""
Divisional chart API endpoints.
"""
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.calculations.divisional_charts import DivisionalChartEngine

router = APIRouter()
_engine = DivisionalChartEngine()


class DivisionalRequest(BaseModel):
    date_time: datetime = Field(..., description="UTC datetime")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude: float = Field(0.0, description="Meters")
    division: int = Field(..., ge=1, le=60, description="D-division, e.g., 9 for D9")


class DivisionalResponse(BaseModel):
    division: int
    planetary_positions: Dict[str, float]
    house_cusps: Dict[str, float]
    ayanamsa_value: float


@router.post("/divisional/calculate", response_model=DivisionalResponse)
async def calculate_divisional_chart(req: DivisionalRequest) -> DivisionalResponse:
    try:
        chart = _engine.calculate_chart(
            req.date_time,
            req.division,
            {
                "lat": float(req.latitude),
                "lon": float(req.longitude),
                "alt": float(req.altitude),
            },
        )
        return DivisionalResponse(
            division=chart.division,
            planetary_positions={k: float(v) for k, v in chart.planets.items()},
            house_cusps={str(i + 1): float(x) for i, x in enumerate(chart.houses)},
            ayanamsa_value=float(chart.ayanamsa),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Divisional calculation failed: {str(e)}")
