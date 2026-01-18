"""
Compatibility API Endpoints
PGF Protocol: API_COMPAT_001
Gate: GATE_5
Version: 1.0.0
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/compatibility", tags=["compatibility"])


class CompatibilityRequest(BaseModel):
    """Request for compatibility calculation"""

    boy_moon_longitude: float = Field(..., ge=0, lt=360, description="Boy's Moon longitude")
    girl_moon_longitude: float = Field(..., ge=0, lt=360, description="Girl's Moon longitude")
    boy_mars_house: Optional[int] = Field(None, ge=1, le=12, description="Boy's Mars house")
    girl_mars_house: Optional[int] = Field(None, ge=1, le=12, description="Girl's Mars house")


class ManglikRequest(BaseModel):
    """Request for Manglik check"""

    mars_house: int = Field(..., ge=1, le=12, description="Mars house position")
    ascendant_sign: int = Field(..., ge=0, lt=12, description="Ascendant sign number")


@router.post("/calculate")
async def calculate_compatibility(request: CompatibilityRequest) -> Dict[str, Any]:
    """
    Calculate Ashtakoot compatibility between two charts

    Returns 36-point matching with detailed koota analysis
    """
    try:
        # Import here to avoid circular imports
        from ...core.calculations.compatibility import calculate_compatibility

        result = calculate_compatibility(
            boy_moon_lon=request.boy_moon_longitude,
            girl_moon_lon=request.girl_moon_longitude,
            boy_mars_house=request.boy_mars_house,
            girl_mars_house=request.girl_mars_house,
        )

        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/manglik")
async def check_manglik(request: ManglikRequest) -> Dict[str, Any]:
    """
    Check for Manglik (Kuja) Dosha
    """
    try:
        from ...core.calculations.compatibility import ManglikDosha

        manglik = ManglikDosha()
        result = manglik.check_manglik(mars_house=request.mars_house, ascendant_sign=request.ascendant_sign)

        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/koota-info")
async def get_koota_info() -> Dict[str, Any]:
    """
    Get information about the 8 kootas
    """
    return {
        "status": "success",
        "data": {
            "kootas": [
                {
                    "name": "Varna",
                    "max_points": 1,
                    "description": "Spiritual/ego compatibility",
                    "significance": "Work ethic and spiritual development",
                },
                {
                    "name": "Vashya",
                    "max_points": 2,
                    "description": "Mutual attraction and control",
                    "significance": "Influence over each other",
                },
                {
                    "name": "Tara",
                    "max_points": 3,
                    "description": "Destiny compatibility",
                    "significance": "Health and well-being together",
                },
                {
                    "name": "Yoni",
                    "max_points": 4,
                    "description": "Physical/sexual compatibility",
                    "significance": "Intimacy and understanding",
                },
                {
                    "name": "Graha Maitri",
                    "max_points": 5,
                    "description": "Planetary friendship",
                    "significance": "Mental compatibility and understanding",
                },
                {
                    "name": "Gana",
                    "max_points": 6,
                    "description": "Temperament matching",
                    "significance": "Behavior and nature compatibility",
                },
                {
                    "name": "Bhakoot",
                    "max_points": 7,
                    "description": "Moon sign compatibility",
                    "significance": "Prosperity, love, and family",
                },
                {
                    "name": "Nadi",
                    "max_points": 8,
                    "description": "Health and genetic compatibility",
                    "significance": "Progeny and health inheritance",
                },
            ],
            "total_max": 36,
            "thresholds": {"excellent": 28, "good": 21, "average": 18, "poor": 0},
        },
    }


@router.get("/doshas")
async def get_dosha_info() -> Dict[str, Any]:
    """
    Get information about major doshas in compatibility
    """
    return {
        "status": "success",
        "data": {
            "doshas": [
                {
                    "name": "Nadi Dosha",
                    "severity": "high",
                    "occurs_when": "Both have same Nadi (Aadi, Madhya, or Antya)",
                    "effects": "Health issues, progeny problems",
                    "remedies": ["Nadi Nivarana Pooja", "Donation of gold equal to weight of boy", "Feeding Brahmins"],
                },
                {
                    "name": "Bhakoot Dosha",
                    "severity": "high",
                    "occurs_when": "Moon signs in 6-8 or 2-12 relationship",
                    "effects": "Financial problems, separation",
                    "remedies": ["Bhakoot Shanti Pooja", "Specific planetary mantras", "Charity on specific days"],
                },
                {
                    "name": "Gana Dosha",
                    "severity": "medium",
                    "occurs_when": "Deva-Rakshasa or Manushya-Rakshasa combination",
                    "effects": "Conflicts, misunderstandings",
                    "remedies": ["Gana Pooja", "Maha Mrityunjaya Jaap"],
                },
                {
                    "name": "Manglik Dosha",
                    "severity": "high",
                    "occurs_when": "Mars in 1, 2, 4, 7, 8, or 12 from Lagna/Moon",
                    "effects": "Marital discord, spouse health issues",
                    "remedies": ["Mangal Shanti Pooja", "Kumbh Vivah", "Marrying another Manglik"],
                },
            ]
        },
    }
