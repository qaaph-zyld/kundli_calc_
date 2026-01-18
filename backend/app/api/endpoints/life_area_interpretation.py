"""
Life-Area Interpretation Endpoints
===================================

Holistic life-area analysis endpoints for complete chart section synthesis.
"""

from typing import Dict, List, Optional

from app.core.knowledge.engine.career_synthesis_engine import CareerSynthesisEngine
from app.core.knowledge.engine.relationship_synthesis_engine import RelationshipSynthesisEngine
from app.core.knowledge.engine.wealth_synthesis_engine import WealthSynthesisEngine
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class PlanetPlacement(BaseModel):
    house: int = Field(..., ge=1, le=12)
    sign: str
    dignity: str = "neutral"


class LifeAreaRequest(BaseModel):
    planets: Dict[str, PlanetPlacement]
    house_lords: Dict[int, str]
    active_yogas: List[str] = []
    current_dasha: Optional[str] = None


@router.post("/life-area/career")
async def analyze_career(request: LifeAreaRequest):
    """Complete career life-area analysis"""
    try:
        engine = CareerSynthesisEngine()

        chart_data = {
            "planets": {
                p: {"house": pl.house, "sign": pl.sign, "dignity": pl.dignity} for p, pl in request.planets.items()
            },
            "house_lords": request.house_lords,
            "active_yogas": request.active_yogas,
        }

        result = engine.synthesize_career_analysis(chart_data, request.current_dasha)

        return {
            "domain": result.domain,
            "overall_assessment": result.overall_assessment,
            "strength": {"score": result.strength_score, "level": result.strength_level.value},
            "key_factors": [
                {
                    "factor": f.factor_name,
                    "contribution": f.contribution_score,
                    "strength": f.strength_level,
                    "interpretation": f.interpretation,
                    "sources": f.sources,
                }
                for f in result.key_factors
            ],
            "synthesis": result.synthesis,
            "timing": result.timing,
            "recommendations": result.recommendations,
            "metadata": {"sources_consulted": result.sources_consulted, "confidence": result.confidence},
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/life-area/relationships")
async def analyze_relationships(request: LifeAreaRequest):
    """Complete relationship life-area analysis"""
    try:
        engine = RelationshipSynthesisEngine()

        chart_data = {
            "planets": {
                p: {"house": pl.house, "sign": pl.sign, "dignity": pl.dignity} for p, pl in request.planets.items()
            },
            "house_lords": request.house_lords,
            "active_yogas": request.active_yogas,
        }

        result = engine.synthesize_relationship_analysis(chart_data, request.current_dasha)

        return {
            "domain": result.domain,
            "overall_assessment": result.overall_assessment,
            "strength": {"score": result.strength_score, "level": result.strength_level.value},
            "key_factors": [
                {
                    "factor": f.factor_name,
                    "contribution": f.contribution_score,
                    "strength": f.strength_level,
                    "interpretation": f.interpretation,
                    "sources": f.sources,
                }
                for f in result.key_factors
            ],
            "synthesis": result.synthesis,
            "timing": result.timing,
            "recommendations": result.recommendations,
            "metadata": {"sources_consulted": result.sources_consulted, "confidence": result.confidence},
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
