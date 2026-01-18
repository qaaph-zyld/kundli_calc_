"""
Extended Yogas API Endpoints
PGF Protocol: API_YOGA_001
Gate: GATE_5
Version: 1.0.0
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from app.core.calculations.extended_yogas import ExtendedYogaCalculator, YogaCategory, calculate_yogas
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()


class YogaRequest(BaseModel):
    """Request model for yoga calculations"""

    planets: Dict[str, Dict[str, Any]] = Field(..., description="Planet data with longitude, sign, house")
    houses: Dict[int, List[str]] = Field(..., description="House to planet list mapping")
    ascendant_sign: int = Field(..., ge=0, le=11, description="Ascendant sign (0-11)")


class YogaResponse(BaseModel):
    """Response model for yoga calculations"""

    success: bool
    total_yogas: int
    benefic_yogas: int
    challenging_yogas: int
    yogas: List[Dict[str, Any]]


@router.post("/calculate")
async def calculate_all_yogas(request: YogaRequest) -> YogaResponse:
    """
    Calculate all yogas present in a chart

    Detects 60+ important Vedic yogas including:
    - Pancha Mahapurusha Yogas
    - Raja Yogas
    - Dhana Yogas
    - Chandra Yogas
    - Vipreet Raja Yogas
    - Neecha Bhanga Raja Yoga
    - And many more
    """
    try:
        # Convert house keys from string to int if needed
        houses = {}
        for k, v in request.houses.items():
            houses[int(k)] = v

        yogas = calculate_yogas(planets=request.planets, houses=houses, ascendant_sign=request.ascendant_sign)

        # Count benefic vs challenging
        benefic_count = sum(1 for y in yogas if y.get("is_benefic", True))
        challenging_count = len(yogas) - benefic_count

        return YogaResponse(
            success=True,
            total_yogas=len(yogas),
            benefic_yogas=benefic_count,
            challenging_yogas=challenging_count,
            yogas=yogas,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_yoga_categories() -> Dict[str, Any]:
    """
    Get all yoga categories and their descriptions
    """
    return {
        "success": True,
        "categories": {
            "raja": {"name": "Raja Yoga", "description": "Power, authority, and success yogas", "nature": "benefic"},
            "dhana": {
                "name": "Dhana Yoga",
                "description": "Wealth and financial prosperity yogas",
                "nature": "benefic",
            },
            "mahapurusha": {
                "name": "Pancha Mahapurusha Yoga",
                "description": "Five great person yogas - strong personality traits",
                "nature": "benefic",
            },
            "chandra": {
                "name": "Chandra (Moon) Yogas",
                "description": "Moon-based yogas affecting mind and emotions",
                "nature": "varies",
            },
            "surya": {
                "name": "Surya (Sun) Yogas",
                "description": "Sun-based yogas affecting authority and vitality",
                "nature": "varies",
            },
            "vipreet": {
                "name": "Vipreet Raja Yoga",
                "description": "Reversal yogas - negatives turning positive",
                "nature": "benefic",
            },
            "neecha_bhanga": {
                "name": "Neecha Bhanga Raja Yoga",
                "description": "Cancellation of debilitation - rise after struggles",
                "nature": "benefic",
            },
            "arishta": {
                "name": "Arishta Yoga",
                "description": "Challenging yogas requiring attention",
                "nature": "malefic",
            },
            "sannyasa": {
                "name": "Sannyasa Yoga",
                "description": "Renunciation and spiritual inclination",
                "nature": "neutral",
            },
            "parivartana": {
                "name": "Parivartana Yoga",
                "description": "Exchange yogas - mutual sign exchange",
                "nature": "varies",
            },
            "nabhasa": {"name": "Nabhasa Yoga", "description": "Celestial pattern yogas", "nature": "varies"},
            "special": {
                "name": "Special Yogas",
                "description": "Other important yogas like Gajakesari",
                "nature": "varies",
            },
        },
    }


@router.get("/list")
async def list_all_yogas() -> Dict[str, Any]:
    """
    Get list of all detectable yogas with brief descriptions
    """
    yoga_list = [
        # Mahapurusha
        {"name": "Ruchaka Yoga", "category": "mahapurusha", "planet": "Mars", "brief": "Valor and courage"},
        {
            "name": "Bhadra Yoga",
            "category": "mahapurusha",
            "planet": "Mercury",
            "brief": "Intelligence and communication",
        },
        {"name": "Hamsa Yoga", "category": "mahapurusha", "planet": "Jupiter", "brief": "Wisdom and spirituality"},
        {"name": "Malavya Yoga", "category": "mahapurusha", "planet": "Venus", "brief": "Beauty and luxury"},
        {"name": "Sasa Yoga", "category": "mahapurusha", "planet": "Saturn", "brief": "Authority and discipline"},
        # Raja
        {"name": "Raja Yoga", "category": "raja", "planet": "Various", "brief": "Power and authority"},
        {"name": "Chamara Yoga", "category": "raja", "planet": "Lagna Lord", "brief": "Royal honor"},
        # Dhana
        {"name": "Dhana Yoga", "category": "dhana", "planet": "2nd/11th lords", "brief": "Wealth accumulation"},
        {"name": "Lakshmi Yoga", "category": "dhana", "planet": "9th/Venus", "brief": "Fortune and prosperity"},
        # Moon-based
        {"name": "Gajakesari Yoga", "category": "special", "planet": "Jupiter/Moon", "brief": "Fame and many virtues"},
        {"name": "Sunapha Yoga", "category": "chandra", "planet": "Moon", "brief": "Self-made wealth"},
        {"name": "Anapha Yoga", "category": "chandra", "planet": "Moon", "brief": "Good character"},
        {"name": "Durudhara Yoga", "category": "chandra", "planet": "Moon", "brief": "Wealth and enjoyments"},
        {"name": "Kemadruma Yoga", "category": "arishta", "planet": "Moon", "brief": "Challenges (needs cancellation)"},
        {"name": "Adhi Yoga", "category": "special", "planet": "Moon", "brief": "Commander/minister"},
        # Sun-based
        {"name": "Budha-Aditya Yoga", "category": "budha", "planet": "Sun/Mercury", "brief": "Intelligence and fame"},
        {"name": "Vesi Yoga", "category": "surya", "planet": "Sun", "brief": "Truthful and learned"},
        {"name": "Vasi Yoga", "category": "surya", "planet": "Sun", "brief": "Prosperous and charitable"},
        {"name": "Ubhayachari Yoga", "category": "surya", "planet": "Sun", "brief": "Royal status"},
        # Vipreet Raja
        {"name": "Harsha Yoga", "category": "vipreet", "planet": "6th lord", "brief": "Victory over enemies"},
        {"name": "Sarala Yoga", "category": "vipreet", "planet": "8th lord", "brief": "Long life and fearlessness"},
        {"name": "Vimala Yoga", "category": "vipreet", "planet": "12th lord", "brief": "Independence and respect"},
        # Neecha Bhanga
        {
            "name": "Neecha Bhanga Raja Yoga",
            "category": "neecha_bhanga",
            "planet": "Debilitated",
            "brief": "Rise after struggles",
        },
        # Others
        {
            "name": "Saraswati Yoga",
            "category": "special",
            "planet": "Jupiter/Venus/Mercury",
            "brief": "Learning and wisdom",
        },
        {"name": "Pushkala Yoga", "category": "special", "planet": "Lagna lord/Moon", "brief": "Fame and sweet speech"},
        {"name": "Kahala Yoga", "category": "special", "planet": "4th/9th lords", "brief": "Leadership"},
        {"name": "Amala Yoga", "category": "special", "planet": "Benefic in 10th", "brief": "Lasting fame"},
        {"name": "Parvata Yoga", "category": "special", "planet": "Benefics", "brief": "Wealth and fame"},
        {"name": "Parivartana Yoga", "category": "parivartana", "planet": "Various", "brief": "Exchange of signs"},
        {"name": "Sannyasa Yoga", "category": "sannyasa", "planet": "4+ planets", "brief": "Spiritual inclination"},
        {"name": "Daridra Yoga", "category": "arishta", "planet": "11th lord", "brief": "Financial challenges"},
    ]

    return {"success": True, "total_yogas_detectable": len(yoga_list), "yogas": yoga_list}


@router.post("/check-specific")
async def check_specific_yoga(
    request: YogaRequest, yoga_name: str = Query(..., description="Name of yoga to check")
) -> Dict[str, Any]:
    """
    Check if a specific yoga is present in the chart
    """
    try:
        # Convert house keys
        houses = {int(k): v for k, v in request.houses.items()}

        yogas = calculate_yogas(planets=request.planets, houses=houses, ascendant_sign=request.ascendant_sign)

        # Find the specific yoga
        found_yogas = [y for y in yogas if yoga_name.lower() in y["name"].lower()]

        return {"success": True, "yoga_name": yoga_name, "is_present": len(found_yogas) > 0, "matches": found_yogas}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strength-analysis")
async def analyze_yoga_strength(request: YogaRequest) -> Dict[str, Any]:
    """
    Get detailed strength analysis of yogas
    """
    try:
        houses = {int(k): v for k, v in request.houses.items()}

        yogas = calculate_yogas(planets=request.planets, houses=houses, ascendant_sign=request.ascendant_sign)

        # Categorize by strength
        excellent = [y for y in yogas if y.get("strength", 0) >= 85]
        good = [y for y in yogas if 70 <= y.get("strength", 0) < 85]
        moderate = [y for y in yogas if 50 <= y.get("strength", 0) < 70]
        weak = [y for y in yogas if y.get("strength", 0) < 50]

        # Overall score
        if yogas:
            avg_strength = sum(y.get("strength", 50) for y in yogas) / len(yogas)
        else:
            avg_strength = 0

        return {
            "success": True,
            "total_yogas": len(yogas),
            "average_strength": round(avg_strength, 1),
            "strength_distribution": {
                "excellent": {"count": len(excellent), "yogas": [y["name"] for y in excellent]},
                "good": {"count": len(good), "yogas": [y["name"] for y in good]},
                "moderate": {"count": len(moderate), "yogas": [y["name"] for y in moderate]},
                "weak": {"count": len(weak), "yogas": [y["name"] for y in weak]},
            },
            "interpretation": self._get_yoga_interpretation(avg_strength, len(yogas)),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_yoga_interpretation(avg_strength: float, yoga_count: int) -> str:
    """Generate interpretation based on yoga analysis"""
    if yoga_count == 0:
        return "No classical yogas detected. Chart should be analyzed for other factors."
    elif avg_strength >= 80 and yoga_count >= 5:
        return "Excellent yoga formation indicating strong potential for success and prosperity."
    elif avg_strength >= 70 and yoga_count >= 3:
        return "Good yoga formation supporting positive life outcomes in key areas."
    elif avg_strength >= 60:
        return "Moderate yoga strength. Results will manifest with appropriate effort."
    else:
        return "Yogas present need strengthening through remedies and focused effort."
