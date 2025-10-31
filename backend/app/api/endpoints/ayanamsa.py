"""Ayanamsa calculation endpoints."""
from typing import Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import swisseph as swe

router = APIRouter()


class AyanamsaRequest(BaseModel):
    """Request model for ayanamsa calculation."""

    date: datetime = Field(..., description="Date for ayanamsa calculation")
    ayanamsa_type: str = Field(
        "lahiri",
        description="Type of ayanamsa (lahiri, raman, krishnamurti, etc.)"
    )


@router.post("/calculate", response_model=Dict[str, float])
async def calculate_ayanamsa(request: AyanamsaRequest):
    """
    Calculate ayanamsa value for a given date.

    Args:
        request: AyanamsaRequest containing date and ayanamsa type

    Returns:
        Dictionary containing ayanamsa value
    """
    try:
        # Map ayanamsa type to Swiss Ephemeris mode
        amap = {
            "lahiri": swe.SIDM_LAHIRI,
            "raman": swe.SIDM_RAMAN,
            "krishnamurti": swe.SIDM_KRISHNAMURTI,
            "fagan_bradley": swe.SIDM_FAGAN_BRADLEY,
            "fagan": swe.SIDM_FAGAN_BRADLEY,
        }
        mode = amap.get(request.ayanamsa_type.lower(), swe.SIDM_LAHIRI)
        swe.set_sid_mode(mode)

        jd = swe.julday(
            request.date.year,
            request.date.month,
            request.date.day,
            request.date.hour + request.date.minute / 60.0 + request.date.second / 3600.0,
        )
        val = float(swe.get_ayanamsa_ut(jd))
        return {"ayanamsa": val}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating ayanamsa: {str(e)}"
        )