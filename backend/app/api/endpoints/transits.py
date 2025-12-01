"""
Transit Analysis API Endpoints
PGF Protocol: API_TRANSIT_001
Gate: GATE_5
Version: 1.0.0
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.core.calculations.transit_analysis import (
    TransitAnalyzer,
    analyze_transits,
    get_current_transits_summary
)

router = APIRouter()


class TransitRequest(BaseModel):
    """Request model for transit analysis"""
    natal_moon_sign: int = Field(..., ge=0, le=11, description="Natal Moon sign (0-11)")
    natal_planets: Dict[str, float] = Field(..., description="Natal planet longitudes")
    current_positions: Dict[str, float] = Field(..., description="Current transit positions")
    datetime: str = Field(default=None, description="Analysis datetime (defaults to now)")


class SadeSatiRequest(BaseModel):
    """Request for Sade Sati check"""
    natal_moon_sign: int = Field(..., ge=0, le=11)
    current_saturn_longitude: float = Field(..., ge=0, lt=360)


class MajorTransitsRequest(BaseModel):
    """Request for major transits summary"""
    natal_moon_sign: int = Field(..., ge=0, le=11)
    saturn_longitude: float = Field(..., ge=0, lt=360)
    jupiter_longitude: float = Field(..., ge=0, lt=360)
    rahu_longitude: float = Field(..., ge=0, lt=360)


@router.post("/analyze")
async def analyze_current_transits(request: TransitRequest) -> Dict[str, Any]:
    """
    Complete transit analysis
    
    Analyzes all planet transits from natal Moon including:
    - Gochara (transit) results for each planet
    - Vedha (obstruction) analysis
    - Ashtakavarga transit scores
    - Sade Sati status
    - Overall transit score
    - Predictions and important transits
    """
    try:
        if request.datetime:
            current_time = datetime.fromisoformat(request.datetime.replace('Z', '+00:00'))
        else:
            current_time = datetime.now()
        
        result = analyze_transits(
            natal_moon_sign=request.natal_moon_sign,
            natal_planets=request.natal_planets,
            current_positions=request.current_positions,
            current_time=current_time
        )
        
        return {
            "success": True,
            "analysis": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sade-sati")
async def check_sade_sati(request: SadeSatiRequest) -> Dict[str, Any]:
    """
    Check Sade Sati (7.5 years Saturn transit) status
    
    Sade Sati occurs when Saturn transits:
    - 12th from Moon (rising phase - 2.5 years)
    - 1st from Moon (peak phase - 2.5 years)  
    - 2nd from Moon (setting phase - 2.5 years)
    """
    try:
        analyzer = TransitAnalyzer(request.natal_moon_sign, {})
        sade_sati = analyzer._check_sade_sati(request.current_saturn_longitude)
        
        return {
            "success": True,
            "natal_moon_sign": request.natal_moon_sign,
            "saturn_longitude": request.current_saturn_longitude,
            "sade_sati": {
                "is_active": sade_sati.is_active,
                "phase": sade_sati.phase,
                "intensity": sade_sati.intensity,
                "affected_houses": sade_sati.affected_houses,
                "remedies": sade_sati.remedies if sade_sati.is_active else [],
                "description": _get_sade_sati_description(sade_sati)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/major-transits")
async def get_major_transits(request: MajorTransitsRequest) -> Dict[str, Any]:
    """
    Get quick summary of major (slow-moving) planet transits
    
    Focuses on Saturn, Jupiter, and Rahu/Ketu which have
    longer-lasting effects.
    """
    try:
        summary = get_current_transits_summary(
            natal_moon_sign=request.natal_moon_sign,
            current_saturn=request.saturn_longitude,
            current_jupiter=request.jupiter_longitude,
            current_rahu=request.rahu_longitude
        )
        
        return {
            "success": True,
            "natal_moon_sign": request.natal_moon_sign,
            "major_transits": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gochara-rules")
async def get_gochara_rules() -> Dict[str, Any]:
    """
    Get Gochara (transit) rules - benefic houses from Moon for each planet
    """
    return {
        "success": True,
        "description": "Houses from natal Moon where planetary transit gives good results",
        "rules": {
            "Sun": {
                "benefic_houses": [3, 6, 10, 11],
                "vedha_points": {3: 9, 6: 12, 10: 4, 11: 5},
                "note": "Good in upachaya, avoid in 12th"
            },
            "Moon": {
                "benefic_houses": [1, 3, 6, 7, 10, 11],
                "vedha_points": {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8},
                "note": "Emotional support in angular and upachaya houses"
            },
            "Mars": {
                "benefic_houses": [3, 6, 11],
                "vedha_points": {3: 12, 6: 9, 11: 5},
                "note": "Energy and courage in upachaya houses"
            },
            "Mercury": {
                "benefic_houses": [2, 4, 6, 8, 10, 11],
                "vedha_points": {2: 5, 4: 3, 6: 9, 8: 1, 10: 8, 11: 12},
                "note": "Communication and intellect support"
            },
            "Jupiter": {
                "benefic_houses": [2, 5, 7, 9, 11],
                "vedha_points": {2: 12, 5: 4, 7: 3, 9: 10, 11: 8},
                "note": "Expansion and blessings - most important transit"
            },
            "Venus": {
                "benefic_houses": [1, 2, 3, 4, 5, 8, 9, 11, 12],
                "vedha_points": {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 5, 9: 11, 11: 6, 12: 3},
                "note": "Generally benefic in most houses"
            },
            "Saturn": {
                "benefic_houses": [3, 6, 11],
                "vedha_points": {3: 12, 6: 9, 11: 5},
                "note": "Only upachaya houses favorable - Sade Sati from 12,1,2"
            },
            "Rahu": {
                "benefic_houses": [3, 6, 10, 11],
                "vedha_points": {},
                "note": "Material gains in upachaya houses"
            },
            "Ketu": {
                "benefic_houses": [3, 6, 10, 11],
                "vedha_points": {},
                "note": "Spiritual insights in upachaya houses"
            }
        },
        "vedha_explanation": "Vedha occurs when another planet is in the obstruction point, canceling the good effects"
    }


@router.get("/ashtakavarga-transit")
async def get_transit_ashtakavarga_info() -> Dict[str, Any]:
    """
    Get information about Ashtakavarga in transit analysis
    """
    return {
        "success": True,
        "description": "Ashtakavarga points help evaluate transit strength",
        "scoring": {
            "0-2 points": "Very weak transit - minimal or negative results",
            "3-4 points": "Moderate transit - mixed results",
            "5-6 points": "Good transit - positive results",
            "7-8 points": "Excellent transit - strong positive results"
        },
        "usage": [
            "Check Ashtakavarga score of transiting planet in the sign",
            "Higher scores indicate better results during transit",
            "Jupiter and Saturn transits are most significant",
            "Combine with Gochara rules for complete analysis"
        ],
        "example": "Jupiter transiting a sign with 5+ bindus from natal chart will give excellent results"
    }


@router.post("/transit-predictions")
async def get_transit_predictions(request: TransitRequest) -> Dict[str, Any]:
    """
    Get transit-based predictions for different life areas
    """
    try:
        if request.datetime:
            current_time = datetime.fromisoformat(request.datetime.replace('Z', '+00:00'))
        else:
            current_time = datetime.now()
        
        result = analyze_transits(
            natal_moon_sign=request.natal_moon_sign,
            natal_planets=request.natal_planets,
            current_positions=request.current_positions,
            current_time=current_time
        )
        
        # Extract predictions organized by life area
        life_areas = {
            "career": [],
            "relationships": [],
            "finances": [],
            "health": [],
            "spirituality": []
        }
        
        for gr in result["gochara_results"]:
            planet = gr["planet"]
            house = gr["house_from_moon"]
            is_benefic = gr["is_benefic"]
            
            # Career (10th house, Saturn, Sun, Jupiter)
            if house == 10 or planet in ["Saturn", "Sun"]:
                if is_benefic:
                    life_areas["career"].append(f"Favorable {planet} transit supports career growth")
                else:
                    life_areas["career"].append(f"{planet} transit requires patience in career matters")
            
            # Relationships (7th house, Venus)
            if house == 7 or planet == "Venus":
                if is_benefic:
                    life_areas["relationships"].append(f"{planet} transit supports relationships")
                else:
                    life_areas["relationships"].append(f"{planet} transit may bring relationship challenges")
            
            # Finances (2nd, 11th house, Jupiter)
            if house in [2, 11] or planet == "Jupiter":
                if is_benefic:
                    life_areas["finances"].append(f"{planet} transit favors financial gains")
                else:
                    life_areas["finances"].append(f"Financial caution advised during {planet} transit")
            
            # Health (1st, 6th house)
            if house in [1, 6]:
                if is_benefic:
                    life_areas["health"].append(f"{planet} transit supports good health")
                else:
                    life_areas["health"].append(f"Health awareness needed during {planet} transit")
            
            # Spirituality (9th, 12th house, Ketu)
            if house in [9, 12] or planet == "Ketu":
                if is_benefic:
                    life_areas["spirituality"].append(f"{planet} transit enhances spiritual growth")
                else:
                    life_areas["spirituality"].append(f"{planet} transit may bring spiritual insights through challenges")
        
        return {
            "success": True,
            "timestamp": current_time.isoformat(),
            "overall_score": result["overall_score"],
            "predictions_by_area": life_areas,
            "general_advice": _get_general_transit_advice(result["overall_score"]["score"])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_sade_sati_description(sade_sati) -> str:
    """Generate Sade Sati description"""
    if not sade_sati.is_active:
        return "Sade Sati is not active. Saturn is not transiting 12th, 1st, or 2nd from Moon."
    
    descriptions = {
        "rising": "Rising phase of Sade Sati. Saturn is in 12th from Moon. Initial challenges, increased expenses, need for introspection. Generally lighter phase.",
        "peak": "Peak phase of Sade Sati. Saturn is transiting over natal Moon. Most intense period with career challenges, health concerns, and mental stress. Stay disciplined and patient.",
        "setting": "Setting phase of Sade Sati. Saturn is in 2nd from Moon. Financial pressures and family matters. Learning phase that leads to wisdom. Relief begins."
    }
    
    return descriptions.get(sade_sati.phase, "Sade Sati active.")


def _get_general_transit_advice(score: float) -> str:
    """Generate general advice based on transit score"""
    if score >= 75:
        return "Transits are highly favorable. Take initiative, start new projects, and make important decisions. Fortune supports your efforts."
    elif score >= 60:
        return "Generally positive transits with some areas needing attention. Proceed with confidence while staying aware of challenges."
    elif score >= 45:
        return "Mixed transit period. Balance optimism with caution. Some areas favorable, others require patience and careful planning."
    elif score >= 30:
        return "Challenging transit period. Focus on consolidation rather than expansion. Remedial measures recommended."
    else:
        return "Difficult transit phase. Prioritize stability, avoid major decisions, focus on remedies and self-care. This too shall pass."


# =============================================================================
# REAL-TIME TRANSIT ENDPOINTS
# =============================================================================

from app.core.calculations.transit_analysis import (
    get_current_transit_positions,
    get_transit_to_natal_aspects,
    get_upcoming_transits
)


class CurrentTransitsRequest(BaseModel):
    """Request for current transit positions"""
    datetime: Optional[str] = Field(None, description="Target datetime (defaults to now)")
    ayanamsa: str = Field(default="lahiri", description="Ayanamsa: lahiri, raman, krishnamurti")


class TransitAspectsRequest(BaseModel):
    """Request for transit-to-natal aspects"""
    natal_positions: Dict[str, float] = Field(..., description="Natal planet longitudes")
    transit_positions: Optional[Dict[str, float]] = Field(None, description="Transit positions (defaults to current)")
    orb: float = Field(default=10.0, ge=1, le=15, description="Aspect orb in degrees")


class UpcomingTransitsRequest(BaseModel):
    """Request for upcoming transits"""
    natal_moon_sign: int = Field(..., ge=0, le=11, description="Natal Moon sign (0-11)")
    days_ahead: int = Field(default=30, ge=1, le=365, description="Days to look ahead")


@router.get("/current")
async def get_current_transits(
    datetime_str: Optional[str] = Query(None, alias="datetime", description="Target datetime ISO format"),
    ayanamsa: str = Query("lahiri", description="Ayanamsa type")
) -> Dict[str, Any]:
    """
    Get current planetary transit positions using Swiss Ephemeris.
    
    Returns real-time positions with sign, nakshatra, and retrograde status.
    Uses Lahiri ayanamsa by default.
    """
    try:
        target_dt = None
        if datetime_str:
            target_dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        
        result = get_current_transit_positions(target_dt, ayanamsa)
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/aspects")
async def calculate_transit_aspects(request: TransitAspectsRequest) -> Dict[str, Any]:
    """
    Calculate aspects between transit and natal planets.
    
    Includes standard aspects (conjunction, opposition, trine, square, sextile)
    and special Vedic aspects (Mars 4th/8th, Saturn 3rd/10th, Jupiter 5th/9th).
    """
    try:
        # Get current positions if not provided
        transit_pos = request.transit_positions
        if transit_pos is None:
            current = get_current_transit_positions()
            transit_pos = {p: data["longitude"] for p, data in current["positions"].items()}
        
        aspects = get_transit_to_natal_aspects(
            transit_pos,
            request.natal_positions,
            request.orb
        )
        
        return {
            "success": True,
            "total_aspects": len(aspects),
            "aspects": aspects,
            "note": "Aspects sorted by tightness (orb). Lower orb = stronger influence."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upcoming")
async def get_upcoming_transit_events(request: UpcomingTransitsRequest) -> Dict[str, Any]:
    """
    Get upcoming significant transit events.
    
    Tracks sign changes for slow-moving planets (Saturn, Jupiter, Rahu)
    and their effects relative to natal Moon.
    """
    try:
        upcoming = get_upcoming_transits(
            request.natal_moon_sign,
            request.days_ahead
        )
        
        return {
            "success": True,
            "natal_moon_sign": request.natal_moon_sign,
            "days_ahead": request.days_ahead,
            "events_count": len(upcoming),
            "upcoming_events": upcoming
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
