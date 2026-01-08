"""
Dasha-Integrated Interpretation Endpoints
==========================================

Provides planetary period (dasha) integrated interpretations combining:
- Current mahadasha effects from Jataka Parijata
- Planet-in-house natal interpretations
- Contextual synthesis with dasha timing
- Life area analysis with timing windows
"""

from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.app.core.knowledge.sources.jataka_parijata_dashas import get_dasha_interpretation
from backend.app.core.knowledge.engine.contextual_synthesis_engine import ContextualSynthesisEngine

router = APIRouter()


class DashaInterpretationRequest(BaseModel):
    """Request for dasha-integrated interpretation"""
    planet: str = Field(..., description="Planet name")
    house: int = Field(..., ge=1, le=12, description="House number")
    sign: str = Field(..., description="Sign name")
    dignity: str = Field(default="neutral", description="Planetary dignity")
    current_dasha: str = Field(..., description="Current mahadasha planet")
    
    class Config:
        json_schema_extra = {
            "example": {
                "planet": "Sun",
                "house": 10,
                "sign": "Aries",
                "dignity": "exalted",
                "current_dasha": "Sun"
            }
        }


@router.post(
    "/dasha-integrated/planet",
    summary="Get dasha-integrated interpretation",
    description="""
    **Dasha-Integrated Planet Interpretation**
    
    Combines natal planet placement with current dasha period effects:
    - Natal interpretation (planet in house)
    - Current mahadasha effects (from Jataka Parijata)
    - Timing activation analysis
    - Life area focus during this period
    
    **When effects manifest:**
    - If current dasha = natal planet: Effects strongly active NOW
    - If different: Effects activate during that planet's dasha
    
    **Example:**
    Sun in 10th (career excellence) during Sun mahadasha
    → Career peak happening NOW with authority gains
    """
)
async def get_dasha_integrated_interpretation(request: DashaInterpretationRequest):
    """Generate interpretation with dasha timing intelligence"""
    try:
        engine = ContextualSynthesisEngine()
        
        # Get natal interpretation with contextual synthesis
        natal_result = engine.synthesize_interpretation(
            planet=request.planet,
            house=request.house,
            sign=request.sign,
            dignity=request.dignity,
            current_dasha=request.current_dasha
        )
        
        # Get current dasha interpretation
        dasha_data = get_dasha_interpretation(request.current_dasha)
        
        if not dasha_data:
            raise ValueError(f"No dasha data available for {request.current_dasha}")
        
        # Determine timing activation
        is_active_now = request.current_dasha == request.planet
        
        # Build response
        response = {
            "planet": request.planet,
            "house": request.house,
            "current_dasha": request.current_dasha,
            
            "timing_analysis": {
                "is_active_now": is_active_now,
                "activation_status": (
                    f"✓ ACTIVE NOW - {request.planet} effects are strongly manifesting during {request.current_dasha} mahadasha"
                    if is_active_now else
                    f"Future activation - These effects will manifest during {request.planet} mahadasha"
                ),
                "natal_promise": natal_result.synthesized_interpretation,
                "current_period_focus": dasha_data.get("general_effects", "")
            },
            
            "natal_interpretation": {
                "synthesis": natal_result.synthesized_interpretation,
                "strength": {
                    "level": natal_result.strength_assessment.overall_strength.value,
                    "score": natal_result.strength_assessment.strength_score,
                    "contributing_factors": natal_result.strength_assessment.factors_contributing
                },
                "key_themes": natal_result.key_themes,
                "confidence": natal_result.confidence_score
            },
            
            "current_dasha_period": {
                "planet": request.current_dasha,
                "duration_years": dasha_data.get("duration_years", 0),
                "general_effects": dasha_data.get("general_effects", ""),
                "detailed_effects": dasha_data.get("detailed_effects", {}),
                "favorable_for": dasha_data.get("favorable_for", []),
                "unfavorable_for": dasha_data.get("unfavorable_for", []),
                "remedial_measures": dasha_data.get("remedial_measures", "")
            },
            
            "integrated_guidance": generate_integrated_guidance(
                request.planet,
                request.house,
                request.current_dasha,
                is_active_now,
                natal_result,
                dasha_data
            ),
            
            "sources": {
                "natal": natal_result.sources_used,
                "dasha": ["Jataka Parijata Ch. 8-9"]
            },
            
            "status": "success"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating dasha-integrated interpretation: {str(e)}"
        )


@router.get(
    "/dasha-integrated/demo",
    summary="Demo: Dasha-integrated interpretation",
    description="""
    Demonstrates dasha-integrated interpretation:
    
    **Example Case:**
    - Sun exalted in 10th house (career excellence)
    - Currently in Sun mahadasha
    - Shows how natal promise + current period = active manifestation
    """
)
async def demo_dasha_integrated():
    """Demo endpoint for dasha-integrated interpretation"""
    demo_request = DashaInterpretationRequest(
        planet="Sun",
        house=10,
        sign="Aries",
        dignity="exalted",
        current_dasha="Sun"
    )
    
    result = await get_dasha_integrated_interpretation(demo_request)
    
    result["demo_note"] = (
        "This demonstrates how natal promise (Sun in 10th for career) "
        "activates during the corresponding dasha period (Sun mahadasha). "
        "Timing intelligence shows WHEN interpretations manifest."
    )
    
    return result


@router.get(
    "/dasha/current-effects/{planet}",
    summary="Get current dasha effects for planet",
    description="Returns detailed effects of current dasha period from Jataka Parijata"
)
async def get_current_dasha_effects(
    planet: str = Path(..., description="Mahadasha planet name")
):
    """Get detailed dasha period effects"""
    try:
        dasha_data = get_dasha_interpretation(planet)
        
        if not dasha_data:
            raise HTTPException(
                status_code=404,
                detail=f"No dasha interpretation available for {planet}"
            )
        
        return {
            "planet": planet,
            "duration_years": dasha_data.get("duration_years"),
            "general_effects": dasha_data.get("general_effects"),
            "detailed_effects": dasha_data.get("detailed_effects"),
            "positive_manifestations": dasha_data.get("positive_manifestations"),
            "challenging_manifestations": dasha_data.get("challenging_manifestations"),
            "favorable_for": dasha_data.get("favorable_for"),
            "unfavorable_for": dasha_data.get("unfavorable_for"),
            "remedial_measures": dasha_data.get("remedial_measures"),
            "source": {
                "text": "Jataka Parijata",
                "chapter": dasha_data.get("chapter"),
                "verses": dasha_data.get("verses")
            },
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving dasha effects: {str(e)}"
        )


def generate_integrated_guidance(
    planet: str,
    house: int,
    current_dasha: str,
    is_active: bool,
    natal_result,
    dasha_data: dict
) -> dict:
    """Generate integrated guidance combining natal + dasha"""
    
    guidance = {
        "timing_window": "",
        "focus_areas": [],
        "recommendations": []
    }
    
    if is_active:
        # Natal planet dasha is active - effects manifesting now
        guidance["timing_window"] = (
            f"CURRENT ACTIVATION: {planet} in {house}th house effects are "
            f"strongly manifesting during {current_dasha} mahadasha. "
            f"This is the prime time for realizing this placement's potential."
        )
        
        # Combine favorable activities from both
        natal_themes = natal_result.key_themes
        dasha_favorable = dasha_data.get("favorable_for", [])
        
        guidance["focus_areas"] = list(set(natal_themes + dasha_favorable[:3]))
        
        guidance["recommendations"] = [
            f"Maximize {house}th house activities (as per natal chart)",
            "Leverage current period strengths from dasha effects",
            "Take initiative in areas showing in natal interpretation"
        ]
        
    else:
        # Different dasha - natal effects await activation
        guidance["timing_window"] = (
            f"FUTURE ACTIVATION: {planet} in {house}th house will manifest "
            f"strongly during {planet} mahadasha. Currently in {current_dasha} "
            f"dasha - prepare foundations now."
        )
        
        guidance["focus_areas"] = [
            f"Current: Focus on {current_dasha} dasha activities",
            f"Prepare: Build foundations for {planet} areas"
        ]
        
        guidance["recommendations"] = [
            f"Work on current {current_dasha} dasha priorities",
            f"Prepare for {planet} dasha activation in future",
            "Build skills relevant to natal placement"
        ]
    
    return guidance
