"""
Contextual Interpretation API Endpoints
========================================

Multi-factor contextual interpretation combining:
- Base placement (planet + house + sign + dignity)
- Lordship effects
- Aspects from other planets
- Active yogas
- Dasha period modulation

Evolution from basic "planet in house" to complete contextual synthesis.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.knowledge.engine.contextual_synthesis_engine import (
    ContextualSynthesisEngine,
    ContextualInterpretation
)

router = APIRouter()


class AspectInput(BaseModel):
    """Aspect from another planet"""
    planet: str = Field(..., description="Aspecting planet name")
    type: str = Field(default="full", description="Aspect type: full, 5th, 7th, 9th")


class ContextualRequest(BaseModel):
    """Request for contextual interpretation"""
    planet: str = Field(..., description="Planet name")
    house: int = Field(..., ge=1, le=12, description="House number")
    sign: str = Field(..., description="Sign name")
    dignity: str = Field(default="neutral", description="Planetary dignity")
    lordship_houses: Optional[List[int]] = Field(default=None, description="Houses this planet rules")
    aspects: Optional[List[AspectInput]] = Field(default=None, description="Aspects from other planets")
    active_yogas: Optional[List[str]] = Field(default=None, description="Yoga names this planet participates in")
    current_dasha: Optional[str] = Field(default=None, description="Current mahadasha planet")
    
    class Config:
        json_schema_extra = {
            "example": {
                "planet": "Sun",
                "house": 10,
                "sign": "Aries",
                "dignity": "exalted",
                "lordship_houses": [9],
                "aspects": [{"planet": "Jupiter", "type": "5th"}],
                "active_yogas": ["Dharma_Karma_Adhipati_Yoga"],
                "current_dasha": "Sun"
            }
        }


@router.post(
    "/contextual/planet",
    summary="Get contextual planet interpretation",
    description="""
    **Multi-Factor Contextual Interpretation**
    
    Synthesizes complete interpretation considering:
    - Base planet-in-house effects
    - Sign and dignity strength
    - Lordship implications (which houses it rules)
    - Aspects from other planets
    - Active yoga formations
    - Current dasha period effects
    
    **Returns:**
    - Comprehensive strength assessment (0-100 score)
    - Synthesized interpretation from all factors
    - Source-attributed effects
    - Key themes and timing notes
    
    **Example:**
    ```json
    {
      "planet": "Sun",
      "house": 10,
      "sign": "Aries",
      "dignity": "exalted",
      "lordship_houses": [9],
      "aspects": [{"planet": "Jupiter", "type": "5th"}],
      "active_yogas": ["Dharma_Karma_Adhipati_Yoga"]
    }
    ```
    
    **Output includes:**
    - Strength score with breakdown (dignity + house + aspects + yogas)
    - Synthesized narrative combining all factors
    - Multi-source comparison where available
    - Timing windows for manifestation
    """
)
async def get_contextual_interpretation(request: ContextualRequest):
    """Generate contextual interpretation with multi-factor synthesis"""
    try:
        engine = ContextualSynthesisEngine()
        
        # Convert aspect inputs to dicts
        aspects_list = None
        if request.aspects:
            aspects_list = [{"planet": a.planet, "type": a.type} for a in request.aspects]
        
        # Generate contextual interpretation
        result = engine.synthesize_interpretation(
            planet=request.planet,
            house=request.house,
            sign=request.sign,
            dignity=request.dignity,
            lordship_houses=request.lordship_houses,
            aspects=aspects_list,
            active_yogas=request.active_yogas,
            current_dasha=request.current_dasha
        )
        
        # Format response
        response = {
            "planet": result.planet,
            "house": result.house,
            "sign": result.sign,
            
            "strength_assessment": {
                "overall_level": result.strength_assessment.overall_strength.value,
                "total_score": result.strength_assessment.strength_score,
                "breakdown": {
                    "dignity": result.strength_assessment.dignity_score,
                    "house": result.strength_assessment.house_score,
                    "aspects": result.strength_assessment.aspect_score,
                    "yogas": result.strength_assessment.yoga_score
                },
                "contributing_factors": result.strength_assessment.factors_contributing,
                "weakening_factors": result.strength_assessment.factors_weakening
            },
            
            "synthesized_interpretation": result.synthesized_interpretation,
            
            "key_themes": result.key_themes,
            "timing_notes": result.timing_notes,
            
            "detailed_analysis": {
                "base_interpretation": result.base_interpretation,
                "lordship_effects": result.lordship_effects,
                "aspect_effects": result.aspect_effects,
                "yoga_effects": result.yoga_effects,
                "dasha_modulation": result.dasha_modulation
            },
            
            "multi_source_comparison": result.source_comparison,
            
            "metadata": {
                "confidence_score": result.confidence_score,
                "factors_analyzed": result.factors_analyzed,
                "sources_used": result.sources_used
            },
            
            "status": "success"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating contextual interpretation: {str(e)}"
        )


@router.get(
    "/contextual/demo",
    summary="Demo: Contextual interpretation",
    description="""
    Demonstration of contextual interpretation showing all factors:
    
    **Example Case:**
    - Sun exalted in 10th house (Aries)
    - Rules 9th house (Leo ascendant)
    - Aspected by Jupiter (5th aspect)
    - Participates in Dharma-Karma Adhipati Yoga
    - Currently in Sun mahadasha
    
    Shows complete synthesis with strength assessment and timing.
    """
)
async def demo_contextual_interpretation():
    """Demo endpoint showing contextual interpretation"""
    demo_request = ContextualRequest(
        planet="Sun",
        house=10,
        sign="Aries",
        dignity="exalted",
        lordship_houses=[9],
        aspects=[AspectInput(planet="Jupiter", type="5th")],
        active_yogas=["Dharma_Karma_Adhipati_Yoga"],
        current_dasha="Sun"
    )
    
    result = await get_contextual_interpretation(demo_request)
    
    result["demo_note"] = (
        "This demonstrates contextual synthesis combining planet placement, "
        "dignity, lordship, aspects, yogas, and dasha timing into a holistic interpretation."
    )
    
    result["competitive_advantage"] = {
        "vs_basic_interpretation": "Considers 6+ factors vs. just planet-house",
        "strength_scoring": "Objective 0-100 strength assessment",
        "multi_source": "Compares BPHS and Saravali where available",
        "timing_intelligence": "Shows when effects manifest via dashas",
        "source_attribution": "Every claim traced to classical verses"
    }
    
    return result


@router.get(
    "/contextual/capabilities",
    summary="Get contextual engine capabilities",
    description="Returns information about contextual synthesis capabilities and factors analyzed"
)
async def get_contextual_capabilities():
    """Return contextual engine capabilities"""
    return {
        "engine": "Contextual Synthesis Engine v1.0",
        "factors_analyzed": [
            "house_placement",
            "sign_dignity",
            "lordship",
            "aspects",
            "yogas",
            "dasha_period"
        ],
        "strength_assessment": {
            "components": ["dignity", "house", "aspects", "yogas"],
            "scale": "0-100 points",
            "levels": ["exceptional", "very_strong", "strong", "moderate", "weak", "debilitated"]
        },
        "sources": {
            "classical_texts": ["BPHS", "Saravali"],
            "chapters_covered": ["BPHS Ch 24 (planets in houses)", "BPHS Ch 40-46 (yogas)"],
            "total_interpretations": 122
        },
        "features": [
            "Multi-factor synthesis",
            "Strength scoring with breakdown",
            "Source attribution",
            "Timing intelligence",
            "Multi-source comparison",
            "Key theme extraction"
        ],
        "status": "production_ready"
    }
