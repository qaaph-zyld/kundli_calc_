"""
Lal Kitab API Endpoints
========================
Provides API access to Lal Kitab predictions and remedies
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.core.calculations.lal_kitab import (
    get_lal_kitab_analysis,
    get_planet_remedy,
    LalKitabCalculator,
    PLANETS,
    LAL_KITAB_REMEDIES,
    PAKKA_GHAR,
    RIN_CONDITIONS,
    KarmicDebt
)


router = APIRouter(prefix="/lal-kitab", tags=["Lal Kitab"])


# =============================================================================
# REQUEST MODELS
# =============================================================================

class LalKitabAnalysisRequest(BaseModel):
    """Request for Lal Kitab chart analysis"""
    planet_houses: Dict[str, int] = Field(
        ...,
        description="Dictionary mapping planet names to house numbers (1-12)",
        json_schema_extra={
            "example": {
                "Sun": 1, "Moon": 4, "Mars": 10, "Mercury": 3,
                "Jupiter": 5, "Venus": 7, "Saturn": 8, "Rahu": 12, "Ketu": 6
            }
        }
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "planet_houses": {
                    "Sun": 10,
                    "Moon": 4,
                    "Mars": 6,
                    "Mercury": 9,
                    "Jupiter": 2,
                    "Venus": 7,
                    "Saturn": 11,
                    "Rahu": 3,
                    "Ketu": 9
                }
            }
        }
    }


class PlanetRemedyRequest(BaseModel):
    """Request for specific planet remedy"""
    planet: str = Field(..., description="Planet name")
    house: int = Field(..., ge=1, le=12, description="House number (1-12)")


# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post("/analyze")
async def analyze_lal_kitab_chart(request: LalKitabAnalysisRequest) -> Dict[str, Any]:
    """
    Get complete Lal Kitab analysis for a birth chart.
    
    Includes:
    - Planet-wise effects in each house
    - Karmic debts (Rin) analysis
    - Lucky numbers, colors, and directions
    - Priority remedies (Upay)
    - Predictions in Hindi and English
    
    Args:
        request: Planet positions in houses (1-12)
        
    Returns:
        Complete Lal Kitab analysis
    """
    try:
        # Validate planet names
        for planet in request.planet_houses.keys():
            if planet not in PLANETS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid planet name: {planet}. Valid planets: {PLANETS}"
                )
        
        # Validate house numbers
        for planet, house in request.planet_houses.items():
            if not 1 <= house <= 12:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid house number for {planet}: {house}. Must be 1-12."
                )
        
        analysis = get_lal_kitab_analysis(request.planet_houses)
        
        return {
            "success": True,
            "system": "Lal Kitab",
            "data": analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/remedy")
async def get_specific_remedy(request: PlanetRemedyRequest) -> Dict[str, Any]:
    """
    Get specific Lal Kitab remedy for a planet in a house.
    
    Returns both general remedies for the planet and
    specific remedies for its placement in that house.
    """
    try:
        if request.planet not in PLANETS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid planet: {request.planet}. Valid: {PLANETS}"
            )
        
        remedy = get_planet_remedy(request.planet, request.house)
        
        return {
            "success": True,
            "data": remedy
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/planets/{planet}/info")
async def get_planet_info(planet: str) -> Dict[str, Any]:
    """
    Get Lal Kitab information about a specific planet.
    
    Returns:
    - Pakka Ghar (permanent house)
    - Exalted and debilitated houses
    - General remedies
    - Friendly and enemy planets
    """
    if planet not in PLANETS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid planet: {planet}. Valid: {PLANETS}"
        )
    
    from app.core.calculations.lal_kitab import (
        EXALTED_HOUSES, DEBILITATED_HOUSES, FRIENDS, ENEMIES
    )
    
    remedies = LAL_KITAB_REMEDIES.get(planet, {}).get("general", {})
    
    return {
        "success": True,
        "planet": planet,
        "pakka_ghar": PAKKA_GHAR.get(planet),
        "exalted_houses": EXALTED_HOUSES.get(planet, []),
        "debilitated_houses": DEBILITATED_HOUSES.get(planet, []),
        "friends": FRIENDS.get(planet, []),
        "enemies": ENEMIES.get(planet, []),
        "remedies": {
            "hindi": remedies.get("hindi", []),
            "english": remedies.get("english", [])
        }
    }


@router.get("/karmic-debts")
async def get_karmic_debt_info() -> Dict[str, Any]:
    """
    Get information about all types of karmic debts (Rin) in Lal Kitab.
    
    Returns details about:
    - Pitra Rin (Ancestors' debt)
    - Mata Rin (Mother's debt)
    - Stree Rin (Wife/Women's debt)
    - Brahman Rin (Teachers' debt)
    """
    debts_info = []
    
    for debt_type, info in RIN_CONDITIONS.items():
        debts_info.append({
            "type": debt_type.value,
            "name": debt_type.name.replace("_", " ").title(),
            "description": info["description"],
            "effects": info["effects"],
            "remedies": {
                "hindi": info["remedies_hindi"],
                "english": info["remedies_english"]
            }
        })
    
    return {
        "success": True,
        "karmic_debts": debts_info
    }


@router.get("/all-remedies")
async def get_all_remedies(
    language: str = Query("both", description="Language: hindi, english, or both")
) -> Dict[str, Any]:
    """
    Get all Lal Kitab remedies organized by planet.
    
    Useful for reference and creating remedy guides.
    """
    all_remedies = {}
    
    for planet, remedy_data in LAL_KITAB_REMEDIES.items():
        general = remedy_data.get("general", {})
        afflicted = remedy_data.get("afflicted_houses", {})
        
        if language == "hindi":
            all_remedies[planet] = {
                "general": general.get("hindi", []),
                "house_specific": {
                    h: r.get("hindi", "") for h, r in afflicted.items()
                }
            }
        elif language == "english":
            all_remedies[planet] = {
                "general": general.get("english", []),
                "house_specific": {
                    h: r.get("english", "") for h, r in afflicted.items()
                }
            }
        else:
            all_remedies[planet] = {
                "general": {
                    "hindi": general.get("hindi", []),
                    "english": general.get("english", [])
                },
                "house_specific": {
                    h: {"hindi": r.get("hindi", ""), "english": r.get("english", "")}
                    for h, r in afflicted.items()
                }
            }
    
    return {
        "success": True,
        "language": language,
        "remedies": all_remedies
    }


@router.get("/pakka-ghar")
async def get_pakka_ghar_info() -> Dict[str, Any]:
    """
    Get the Pakka Ghar (permanent house) for each planet.
    
    In Lal Kitab, each planet has a permanent house where
    it is naturally strong and gives best results.
    """
    return {
        "success": True,
        "description": "Pakka Ghar is the permanent house for each planet in Lal Kitab. "
                       "A planet in its Pakka Ghar gives excellent results.",
        "pakka_ghar": PAKKA_GHAR,
        "details": {
            "Sun": {"house": 1, "signifies": "Self, soul, father, government"},
            "Moon": {"house": 4, "signifies": "Mother, mind, emotions, home"},
            "Mars": {"house": 3, "signifies": "Courage, siblings, energy"},
            "Mercury": {"house": 7, "signifies": "Communication, spouse, business"},
            "Jupiter": {"house": 2, "signifies": "Wealth, family, speech, wisdom"},
            "Venus": {"house": 7, "signifies": "Love, marriage, luxury, arts"},
            "Saturn": {"house": 8, "signifies": "Longevity, transformation, karma"},
            "Rahu": {"house": 12, "signifies": "Foreign, spirituality, isolation"},
            "Ketu": {"house": 6, "signifies": "Enemies, diseases, service"}
        }
    }
