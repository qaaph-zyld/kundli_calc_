"""
KP System API Endpoints
PGF Protocol: API_KP_001
Gate: GATE_5
Version: 1.0.0
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.core.calculations.kp_system import (
    KPSystem,
    get_kp_data,
    KPPosition
)

router = APIRouter()


class KPRequest(BaseModel):
    """Request model for KP calculations"""
    datetime: str = Field(..., description="Birth datetime in ISO format")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str = Field(default="UTC")
    planets: Dict[str, float] = Field(..., description="Planet longitudes")
    house_cusps: List[float] = Field(..., description="12 house cusp longitudes")


class HoraryRequest(BaseModel):
    """Request model for KP Horary chart"""
    horary_number: int = Field(..., ge=1, le=249)
    datetime: str = Field(..., description="Query datetime")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class RulingPlanetsRequest(BaseModel):
    """Request model for ruling planets"""
    datetime: str = Field(..., description="Current datetime")
    moon_longitude: float = Field(..., ge=0, lt=360)
    ascendant_longitude: float = Field(..., ge=0, lt=360)


@router.post("/calculate")
async def calculate_kp_data(request: KPRequest) -> Dict[str, Any]:
    """
    Calculate complete KP (Krishnamurti Paddhati) data
    
    Returns:
    - Planet positions with star lord, sub lord, sub-sub lord
    - Cuspal positions with sublords
    - Ruling planets
    - Planets by house
    """
    try:
        birth_time = datetime.fromisoformat(request.datetime.replace('Z', '+00:00'))
        
        result = get_kp_data(
            planets=request.planets,
            house_cusps=request.house_cusps,
            current_time=birth_time
        )
        
        return {
            "success": True,
            "data": result,
            "system": "Krishnamurti Paddhati (KP)"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/position/{longitude}")
async def get_kp_position(
    longitude: float = Query(..., ge=0, lt=360, description="Sidereal longitude")
) -> Dict[str, Any]:
    """
    Get KP position details for any longitude
    
    Returns sign lord, star lord, sub lord up to 5 levels
    """
    try:
        kp = KPSystem()
        position = kp.get_kp_position(longitude)
        
        return {
            "success": True,
            "data": {
                "degree": position.degree,
                "sign": position.sign_name,
                "sign_lord": position.sign_lord,
                "nakshatra": position.nakshatra_name,
                "star_lord": position.nakshatra_lord,
                "sub_lord": position.sub_lord,
                "sub_sub_lord": position.sub_sub_lord,
                "sub_sub_sub_lord": position.sub_sub_sub_lord,
                "sub_sub_sub_sub_lord": position.sub_sub_sub_sub_lord,
                "degree_in_sign": position.degree_in_sign,
                "degree_in_nakshatra": position.degree_in_nakshatra
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/horary")
async def calculate_horary(request: HoraryRequest) -> Dict[str, Any]:
    """
    Calculate KP Horary chart from number (1-249)
    
    Used for prasna/horary astrology
    """
    try:
        kp = KPSystem()
        position = kp.horary_number_to_position(request.horary_number)
        
        return {
            "success": True,
            "horary_number": request.horary_number,
            "data": {
                "ascendant_degree": position.degree,
                "sign": position.sign_name,
                "sign_lord": position.sign_lord,
                "nakshatra": position.nakshatra_name,
                "star_lord": position.nakshatra_lord,
                "sub_lord": position.sub_lord,
                "sub_sub_lord": position.sub_sub_lord
            },
            "interpretation": f"Horary #{request.horary_number} gives {position.sign_name} ascendant with {position.nakshatra_lord} star lord and {position.sub_lord} sub lord"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ruling-planets")
async def get_ruling_planets(request: RulingPlanetsRequest) -> Dict[str, Any]:
    """
    Get Ruling Planets (RP) at a given moment
    
    Used for timing events and confirming chart rectification
    """
    try:
        kp = KPSystem()
        current_time = datetime.fromisoformat(request.datetime.replace('Z', '+00:00'))
        
        rp = kp.get_ruling_planets(
            current_time,
            request.moon_longitude,
            request.ascendant_longitude
        )
        
        return {
            "success": True,
            "timestamp": current_time.isoformat(),
            "ruling_planets": {
                "weekday_lord": rp.weekday_lord,
                "moon_sign_lord": rp.moon_sign_lord,
                "moon_star_lord": rp.moon_star_lord,
                "moon_sub_lord": rp.moon_sub_lord,
                "ascendant_sign_lord": rp.ascendant_sign_lord,
                "ascendant_star_lord": rp.ascendant_star_lord,
                "ascendant_sub_lord": rp.ascendant_sub_lord
            },
            "strong_ruling_planets": rp.strong_rp,
            "usage": "Planets appearing multiple times are stronger ruling planets"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/significators/{house_num}")
async def get_house_significators(
    house_num: int = Query(..., ge=1, le=12),
    planets: str = Query(..., description="Comma-separated planet longitudes")
) -> Dict[str, Any]:
    """
    Get ABCD significators for a house
    
    Args:
        house_num: House number (1-12)
        planets: Comma-separated "planet:longitude" pairs
    """
    try:
        # Parse planets
        planet_dict = {}
        for pair in planets.split(","):
            if ":" in pair:
                name, lon = pair.split(":")
                planet_dict[name.strip()] = float(lon)
        
        kp = KPSystem()
        
        # Get KP positions for all planets
        planet_kp = {name: kp.get_kp_position(lon) for name, lon in planet_dict.items()}
        
        # Determine planets in the requested house (simplified)
        planets_in_house = []  # Would need actual house calculation
        
        return {
            "success": True,
            "house": house_num,
            "significator_system": "ABCD",
            "explanation": {
                "A": "Planets in star of occupants",
                "B": "Planets in the house",
                "C": "Planets in star of owner",
                "D": "Owner of the house"
            },
            "note": "Full significator calculation requires complete chart data"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ayanamsa")
async def get_kp_ayanamsa(
    year: int = Query(..., description="Year"),
    month: int = Query(1, ge=1, le=12),
    day: int = Query(1, ge=1, le=31)
) -> Dict[str, float]:
    """
    Get KP (Krishnamurti) Ayanamsa for a date
    
    KP Ayanamsa is slightly different from Lahiri
    """
    try:
        kp = KPSystem()
        date = datetime(year, month, day)
        ayanamsa = kp.calculate_kp_ayanamsa(date)
        
        return {
            "success": True,
            "date": date.isoformat(),
            "kp_ayanamsa": round(ayanamsa, 6),
            "kp_ayanamsa_dms": f"{int(ayanamsa)}° {int((ayanamsa % 1) * 60)}' {int(((ayanamsa % 1) * 60 % 1) * 60)}\""
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
