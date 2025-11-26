"""
Additional Dasha Systems API Endpoints
PGF Protocol: API_DASHA_002
Gate: GATE_5
Version: 1.0.0
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.core.calculations.additional_dashas import (
    YoginiDasha,
    AshtottariDasha,
    CharaDasha,
    KalachakraDasha,
    calculate_all_dasha_systems,
    get_current_dasha_all_systems
)

router = APIRouter()


class DashaRequest(BaseModel):
    """Request model for dasha calculations"""
    birth_datetime: str = Field(..., description="Birth datetime in ISO format")
    moon_longitude: float = Field(..., ge=0, lt=360)
    ascendant_longitude: float = Field(default=0, ge=0, lt=360)
    planet_longitudes: Dict[str, float] = Field(default_factory=dict)


class CurrentDashaRequest(BaseModel):
    """Request for current running dasha"""
    birth_datetime: str
    moon_longitude: float
    ascendant_longitude: float = 0
    planet_longitudes: Dict[str, float] = Field(default_factory=dict)
    current_datetime: str = Field(default=None)


@router.post("/yogini")
async def calculate_yogini_dasha(request: DashaRequest) -> Dict[str, Any]:
    """
    Calculate Yogini Dasha
    
    36-year cycle with 8 Yoginis (feminine deities)
    Faster cycle - useful for short-term predictions
    
    Yoginis:
    - Mangala (1 year) - Moon
    - Pingala (2 years) - Sun
    - Dhanya (3 years) - Jupiter
    - Bhramari (4 years) - Mars
    - Bhadrika (5 years) - Mercury
    - Ulka (6 years) - Saturn
    - Siddha (7 years) - Venus
    - Sankata (8 years) - Rahu
    """
    try:
        birth_time = datetime.fromisoformat(request.birth_datetime.replace('Z', '+00:00'))
        
        yogini = YoginiDasha()
        result = yogini.calculate_dasha_at_birth(birth_time, request.moon_longitude)
        
        return {
            "success": True,
            "dasha_system": "Yogini Dasha",
            "applicability": "General use, especially for timing events and short-term predictions",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ashtottari")
async def calculate_ashtottari_dasha(request: DashaRequest) -> Dict[str, Any]:
    """
    Calculate Ashtottari Dasha
    
    108-year cycle using 8 planets (excludes Ketu)
    Applicable when Rahu is in kendra/trikona from Lagna lord
    
    Periods:
    - Sun: 6 years
    - Moon: 15 years
    - Mars: 8 years
    - Mercury: 17 years
    - Saturn: 10 years
    - Jupiter: 19 years
    - Rahu: 12 years
    - Venus: 21 years
    """
    try:
        birth_time = datetime.fromisoformat(request.birth_datetime.replace('Z', '+00:00'))
        
        ashtottari = AshtottariDasha()
        result = ashtottari.calculate_dasha_at_birth(birth_time, request.moon_longitude)
        
        return {
            "success": True,
            "dasha_system": "Ashtottari Dasha",
            "applicability": "When Rahu is in kendra/trikona from Lagna lord, or for night births",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chara")
async def calculate_chara_dasha(request: DashaRequest) -> Dict[str, Any]:
    """
    Calculate Chara Dasha (Jaimini System)
    
    Rashi (sign) based dasha using Jaimini principles
    Duration based on sign's distance from its lord
    
    Features:
    - Progression varies based on ascendant (odd/even sign)
    - Duration = distance of lord from sign + 1 (years)
    - Uses Jaimini sign lordships
    """
    try:
        birth_time = datetime.fromisoformat(request.birth_datetime.replace('Z', '+00:00'))
        
        chara = CharaDasha()
        result = chara.calculate_dasha_at_birth(
            birth_time, 
            request.ascendant_longitude,
            request.planet_longitudes
        )
        
        return {
            "success": True,
            "dasha_system": "Chara Dasha (Jaimini)",
            "applicability": "Jaimini system practitioners, sign-based predictions",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kalachakra")
async def calculate_kalachakra_dasha(request: DashaRequest) -> Dict[str, Any]:
    """
    Calculate Kalachakra Dasha
    
    Based on Moon's navamsa and direction (Savya/Apsavya)
    Complex but very precise timing system
    
    Features:
    - Uses navamsa position of Moon
    - Savya (clockwise) or Apsavya (anti-clockwise) progression
    - Variable durations for different signs
    """
    try:
        birth_time = datetime.fromisoformat(request.birth_datetime.replace('Z', '+00:00'))
        
        kalachakra = KalachakraDasha()
        result = kalachakra.calculate_dasha_at_birth(birth_time, request.moon_longitude)
        
        return {
            "success": True,
            "dasha_system": "Kalachakra Dasha",
            "applicability": "Advanced timing, navamsa-based analysis",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/all-systems")
async def calculate_all_systems(request: DashaRequest) -> Dict[str, Any]:
    """
    Calculate all dasha systems for comparison
    
    Returns:
    - Vimshottari (standard - from main dasha module)
    - Yogini
    - Ashtottari
    - Chara
    - Kalachakra
    """
    try:
        birth_time = datetime.fromisoformat(request.birth_datetime.replace('Z', '+00:00'))
        
        result = calculate_all_dasha_systems(
            birth_time,
            request.moon_longitude,
            request.ascendant_longitude,
            request.planet_longitudes
        )
        
        return {
            "success": True,
            "description": "All dasha systems calculated for comparison",
            "note": "Different systems may be applicable based on chart conditions",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/current")
async def get_current_running_dasha(request: CurrentDashaRequest) -> Dict[str, Any]:
    """
    Get current running dasha in all systems
    
    Useful for quick comparison of which dasha is active
    across different systems at the present moment.
    """
    try:
        birth_time = datetime.fromisoformat(request.birth_datetime.replace('Z', '+00:00'))
        
        if request.current_datetime:
            current_time = datetime.fromisoformat(request.current_datetime.replace('Z', '+00:00'))
        else:
            current_time = datetime.now()
        
        result = get_current_dasha_all_systems(
            birth_time,
            request.moon_longitude,
            request.ascendant_longitude,
            request.planet_longitudes,
            current_time
        )
        
        return {
            "success": True,
            "query_time": current_time.isoformat(),
            "current_dashas": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comparison")
async def compare_dasha_systems() -> Dict[str, Any]:
    """
    Get comparison of all dasha systems
    """
    return {
        "success": True,
        "dasha_systems": {
            "vimshottari": {
                "cycle": "120 years",
                "planets": 9,
                "basis": "Moon's nakshatra",
                "applicability": "Universal - most widely used",
                "best_for": "General life predictions, major life events"
            },
            "yogini": {
                "cycle": "36 years",
                "planets": 8,
                "basis": "Moon's nakshatra",
                "applicability": "Universal",
                "best_for": "Short-term predictions, timing events"
            },
            "ashtottari": {
                "cycle": "108 years",
                "planets": 8,
                "basis": "Moon's nakshatra (28 nakshatras)",
                "applicability": "When Rahu in kendra/trikona from Lagna lord",
                "best_for": "Night births, specific chart conditions"
            },
            "chara": {
                "cycle": "Variable",
                "planets": "Sign-based",
                "basis": "Ascendant and planet positions",
                "applicability": "Jaimini system",
                "best_for": "Sign-level predictions, Jaimini analysis"
            },
            "kalachakra": {
                "cycle": "~83 years",
                "planets": "Nakshatra-based",
                "basis": "Moon's navamsa",
                "applicability": "Advanced analysis",
                "best_for": "Precise timing, navamsa-level predictions"
            }
        },
        "recommendation": "Use Vimshottari as primary, Yogini for short-term, others based on chart conditions and expertise"
    }


@router.post("/yogini/antardasha")
async def get_yogini_antardasha(
    yogini: str = Query(..., description="Main Yogini name"),
    start_date: str = Query(..., description="Start date ISO format"),
    end_date: str = Query(..., description="End date ISO format")
) -> Dict[str, Any]:
    """
    Get Yogini antardasha (sub-periods) for a mahadasha
    """
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        yogini_calc = YoginiDasha()
        result = yogini_calc.get_antardasha(yogini, start, end)
        
        return {
            "success": True,
            "mahadasha": yogini,
            "antardashas": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ashtottari/antardasha")
async def get_ashtottari_antardasha(
    planet: str = Query(..., description="Main planet name"),
    start_date: str = Query(..., description="Start date ISO format"),
    end_date: str = Query(..., description="End date ISO format")
) -> Dict[str, Any]:
    """
    Get Ashtottari antardasha (sub-periods) for a mahadasha
    """
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        ashtottari = AshtottariDasha()
        result = ashtottari.get_antardasha(planet, start, end)
        
        return {
            "success": True,
            "mahadasha": planet,
            "antardashas": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
