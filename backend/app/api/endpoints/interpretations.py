"""
Interpretation API Endpoints
=============================
Source-backed astrological interpretations with classical text citations.

All interpretations include:
- Classical text references (BPHS, Saravali, etc.)
- Verse citations
- Translation sources
- Confidence levels
"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.knowledge.engine.interpretation_engine import KnowledgeInterpretationEngine
from app.core.knowledge.schemas.interpretation_schema import (
    PlanetaryDignity, LifeArea, PlanetInHouseInterpretation
)

router = APIRouter()
engine = KnowledgeInterpretationEngine()


class PlanetInHouseRequest(BaseModel):
    """Request for planet in house interpretation"""
    planet: str = Field(..., description="Planet name (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)")
    house: int = Field(..., ge=1, le=12, description="House number (1-12)")
    sign: str = Field(..., description="Sign name (Aries, Taurus, etc.)")
    dignity: PlanetaryDignity = Field(
        default=PlanetaryDignity.NEUTRAL,
        description="Planetary dignity"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "planet": "Sun",
                "house": 10,
                "sign": "Aries",
                "dignity": "exalted"
            }
        }


class InterpretationResponse(BaseModel):
    """Response with interpretation and sources"""
    interpretation: Dict[str, Any]
    sources: List[str] = Field(..., description="Formatted citations")
    confidence_score: float = Field(..., ge=0, le=1)
    tags: List[str]


@router.get("/available", tags=["Interpretations"])
async def get_available_interpretations():
    """
    Get list of available interpretations in knowledge base.
    
    Returns:
        Dictionary showing which planet-house combinations have interpretations
    """
    available = engine.get_available_interpretations()
    
    return {
        "status": "success",
        "data": available,
        "note": "Currently showing BPHS Chapter 24 coverage. More texts being added.",
        "total_combinations": sum(len(houses) for houses in available.values())
    }


@router.post("/planet-in-house", response_model=InterpretationResponse, tags=["Interpretations"])
async def interpret_planet_in_house(request: PlanetInHouseRequest):
    """
    Get classical text-based interpretation for planet in house placement.
    
    Returns interpretation with:
    - Primary classical text source (BPHS)
    - Full verse citations
    - Detailed effects from classical descriptions
    - Life area breakdowns
    - Timing and remedy recommendations
    - Source confidence levels
    
    Example:
    ```
    POST /api/v1/interpret/planet-in-house
    {
      "planet": "Sun",
      "house": 10,
      "sign": "Aries",
      "dignity": "exalted"
    }
    ```
    """
    try:
        interpretation = engine.interpret_planet_in_house(
            planet=request.planet,
            house=request.house,
            sign=request.sign,
            dignity=request.dignity
        )
        
        # Convert to response format
        return InterpretationResponse(
            interpretation=interpretation.model_dump(mode='json'),
            sources=interpretation.sources.get_all_citations(),
            confidence_score=interpretation.metadata.confidence_score,
            tags=interpretation.metadata.tags
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Interpretation not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating interpretation: {str(e)}"
        )


@router.get("/planet-in-house/{planet}/{house}", tags=["Interpretations"])
async def get_planet_in_house_interpretation(
    planet: str,
    house: int,
    sign: Optional[str] = Query(None, description="Sign (optional, affects dignity assessment)"),
    dignity: Optional[PlanetaryDignity] = Query(None, description="Dignity (optional)")
):
    """
    Get interpretation via GET request (simplified).
    
    Args:
        planet: Planet name
        house: House number (1-12)
        sign: Optional sign name
        dignity: Optional dignity
        
    Returns:
        Interpretation with classical text sources
    """
    # Set defaults
    sign = sign or "Unknown"
    dignity = dignity or PlanetaryDignity.NEUTRAL
    
    request_data = PlanetInHouseRequest(
        planet=planet,
        house=house,
        sign=sign,
        dignity=dignity
    )
    
    return await interpret_planet_in_house(request_data)


@router.get("/demo/sun-in-tenth", tags=["Interpretations", "Demo"])
async def demo_sun_in_tenth():
    """
    Demo endpoint showing Sun in 10th house interpretation.
    
    This demonstrates:
    - Classical text citation (BPHS Chapter 24, verses 11)
    - Detailed effects from traditional sources
    - Life area breakdowns
    - Source attribution
    - Confidence levels
    
    **This is what makes our system unique:** Every interpretation
    is traceable to classical texts, not generic AI-generated content.
    """
    interpretation = engine.interpret_planet_in_house(
        planet="Sun",
        house=10,
        sign="Aries",
        dignity=PlanetaryDignity.EXALTED
    )
    
    return {
        "demo_title": "Sun in 10th House - Classical Interpretation",
        "note": "This interpretation comes directly from Brihat Parashara Hora Shastra",
        "interpretation": interpretation.model_dump(mode='json'),
        "why_this_matters": [
            "🎯 Source Attribution: Every statement traces back to BPHS Chapter 24",
            "📚 Classical Authority: Not AI-generated, but traditional Jyotish wisdom",
            "🔍 Transparency: Users can verify interpretations against original texts",
            "⭐ Confidence Tracking: Know which interpretations are direct quotes vs. inferences",
            "🌍 Open Knowledge: Public domain texts, freely shareable"
        ],
        "citations": interpretation.sources.get_all_citations(),
        "competitive_advantage": {
            "vs_astrosage": "They don't cite classical texts",
            "vs_astrodatabank": "We provide classical source verification",
            "vs_vedic_astro_apps": "Most use generic templates without attribution",
            "our_approach": "Every interpretation backed by verse-level citations from BPHS, Saravali, etc."
        }
    }


@router.get("/sources/info", tags=["Interpretations", "Metadata"])
async def get_source_information():
    """
    Get information about classical texts used in interpretations.
    
    Returns metadata about:
    - Which texts are currently digitized
    - Translation sources
    - Coverage statistics
    - Confidence levels
    """
    return {
        "classical_texts": {
            "BPHS": {
                "full_name": "Brihat Parashara Hora Shastra",
                "author": "Sage Parashara (traditional attribution)",
                "translation": "R. Santhanam (1984)",
                "publisher": "Rajan Publications",
                "chapters_digitized": [24],
                "coverage": {
                    "planets_in_houses": "Partial (Sun, Moon, Mars, Mercury, Jupiter in key houses)",
                    "total_verses_referenced": 10
                },
                "notes": "Foundation text of Vedic astrology. Public domain translation used."
            },
            "Saravali": {
                "status": "Planned for Phase 1",
                "author": "Kalyana Varma",
                "estimated_coverage": "Planets in houses, signs, yogas"
            },
            "Phaladeepika": {
                "status": "Planned for Phase 1",
                "author": "Mantreswara",
                "estimated_coverage": "Predictive techniques, dasha effects"
            }
        },
        "confidence_levels": {
            "direct_quote": "0.95-1.0: Direct verse translation",
            "direct_interpretation": "0.85-0.95: Clear traditional interpretation",
            "synthesized": "0.70-0.85: Combined from multiple sources",
            "inferred": "0.50-0.70: Logical inference from principles"
        },
        "roadmap": {
            "current_phase": "MVP - Core BPHS planets in houses",
            "phase_1": "Complete BPHS Ch. 24 + Saravali + Phaladeepika",
            "phase_2": "Yogas from BPHS Ch. 40-45, Saravali Ch. 38-40",
            "phase_3": "Dasha effects, transit interpretations",
            "phase_4": "RAG system for extended coverage"
        }
    }
