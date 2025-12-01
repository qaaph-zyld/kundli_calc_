"""
Varshphal (Annual Horoscope) API Endpoints
============================================
Provides API access to Varshphal/Tajaka system calculations
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.core.calculations.varshaphal import VarshaphalCalculator


router = APIRouter(prefix="/varshphal", tags=["Varshphal"])


# =============================================================================
# REQUEST MODELS
# =============================================================================

class VarshphalRequest(BaseModel):
    """Request for Varshphal (Annual Chart) calculation"""
    birth_date: str = Field(..., description="Birth date in ISO format (YYYY-MM-DDTHH:MM:SS)")
    birth_sun_longitude: float = Field(..., ge=0, lt=360, description="Sun longitude at birth")
    birth_latitude: float = Field(..., ge=-90, le=90, description="Birth latitude")
    birth_longitude: float = Field(..., ge=-180, le=180, description="Birth longitude")
    year_number: int = Field(..., ge=1, le=120, description="Year of life (1 = first year)")
    annual_planets: Dict[str, float] = Field(
        ..., 
        description="Planet longitudes at solar return",
        example={"Sun": 270.0, "Moon": 120.0, "Mars": 45.0}
    )
    annual_ascendant: float = Field(..., ge=0, lt=360, description="Ascendant at solar return")

    class Config:
        json_schema_extra = {
            "example": {
                "birth_date": "1990-01-15T12:00:00",
                "birth_sun_longitude": 271.0,
                "birth_latitude": 28.6139,
                "birth_longitude": 77.209,
                "year_number": 35,
                "annual_planets": {
                    "Sun": 271.0,
                    "Moon": 145.0,
                    "Mars": 200.0,
                    "Mercury": 255.0,
                    "Jupiter": 70.0,
                    "Venus": 280.0,
                    "Saturn": 290.0
                },
                "annual_ascendant": 120.0
            }
        }


class MunthaRequest(BaseModel):
    """Request for Muntha calculation only"""
    birth_ascendant_sign: int = Field(..., ge=0, le=11, description="Birth ascendant sign (0-11)")
    year_number: int = Field(..., ge=1, le=120, description="Year of life")


# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.post("/calculate")
async def calculate_varshphal(request: VarshphalRequest) -> Dict[str, Any]:
    """
    Calculate complete Varshphal (Annual Horoscope) for a given year.
    
    Includes:
    - Muntha position and interpretation
    - Year Lord calculation
    - Tajaka Yogas
    - Sahams (Arabic Parts)
    - Annual predictions
    
    The Varshphal is calculated from birthday to birthday,
    based on the exact moment when Sun returns to its birth position.
    """
    try:
        birth_date = datetime.fromisoformat(request.birth_date)
        
        calculator = VarshaphalCalculator()
        
        result = calculator.calculate_varshaphal(
            birth_date=birth_date,
            birth_sun_longitude=request.birth_sun_longitude,
            birth_location={
                "latitude": request.birth_latitude,
                "longitude": request.birth_longitude
            },
            year_number=request.year_number,
            current_sun_longitude=request.birth_sun_longitude,  # At solar return
            annual_planets=request.annual_planets,
            annual_ascendant=request.annual_ascendant
        )
        
        return {
            "success": True,
            "year_number": request.year_number,
            "system": "Varshphal/Tajaka",
            "data": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/muntha")
async def calculate_muntha(request: MunthaRequest) -> Dict[str, Any]:
    """
    Calculate Muntha position for a specific year.
    
    Muntha moves one sign per year from birth ascendant.
    Its position indicates focus areas for that year.
    """
    try:
        # Muntha moves one sign per year
        muntha_sign = (request.birth_ascendant_sign + request.year_number - 1) % 12
        
        sign_names = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        sign_lords = {
            0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
            4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
            8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter"
        }
        
        # Muntha interpretation by house from annual ascendant
        interpretations = {
            1: "Muntha in 1st: Focus on self, health, new beginnings. Generally favorable.",
            2: "Muntha in 2nd: Focus on wealth, family matters, speech. Good for finances.",
            3: "Muntha in 3rd: Focus on siblings, courage, short travels. Communication important.",
            4: "Muntha in 4th: Focus on home, mother, property, vehicles. Domestic matters.",
            5: "Muntha in 5th: Focus on children, creativity, romance. Speculation possible.",
            6: "Muntha in 6th: Focus on health, enemies, service. Need to address obstacles.",
            7: "Muntha in 7th: Focus on partnerships, marriage, business. Relationships key.",
            8: "Muntha in 8th: Focus on transformation, occult, inheritance. Challenging year.",
            9: "Muntha in 9th: Focus on fortune, father, higher learning. Spiritual growth.",
            10: "Muntha in 10th: Focus on career, status, authority. Professional year.",
            11: "Muntha in 11th: Focus on gains, friends, aspirations. Favorable for income.",
            12: "Muntha in 12th: Focus on expenses, foreign lands, spirituality. Introspective year."
        }
        
        # House from 1st (assuming annual ascendant is same as birth for simple calculation)
        house = (muntha_sign - request.birth_ascendant_sign + 12) % 12 + 1
        
        return {
            "success": True,
            "year_number": request.year_number,
            "muntha": {
                "sign_number": muntha_sign,
                "sign_name": sign_names[muntha_sign],
                "lord": sign_lords[muntha_sign],
                "house_from_birth_asc": house,
                "interpretation": interpretations.get(house, "")
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tajaka-yogas")
async def get_tajaka_yoga_info() -> Dict[str, Any]:
    """
    Get information about all Tajaka Yogas used in Varshphal.
    
    These are special planetary combinations analyzed in annual charts.
    """
    yogas = [
        {
            "name": "Ikkabal",
            "sanskrit": "इक्कबाल",
            "description": "When a planet is in its own sign or exaltation in annual chart",
            "effect": "Gives strength and positive results for that planet's significations"
        },
        {
            "name": "Ithasala",
            "sanskrit": "इत्थशाल",
            "description": "Faster planet applying to slower planet within orb",
            "effect": "Success and fulfillment of the matters signified"
        },
        {
            "name": "Ishrafa",
            "sanskrit": "इश्राफ",
            "description": "Faster planet separating from slower planet",
            "effect": "Opportunities may be lost or delayed"
        },
        {
            "name": "Nakta",
            "sanskrit": "नक्त",
            "description": "Translation of light between three planets",
            "effect": "Success through intermediary or indirect means"
        },
        {
            "name": "Yamaya",
            "sanskrit": "यमया",
            "description": "Mutual translation between planets",
            "effect": "Mutual support and cooperation brings success"
        },
        {
            "name": "Kamboola",
            "sanskrit": "कम्बूल",
            "description": "Moon applying to year lord or other significant planet",
            "effect": "Mental peace and emotional fulfillment"
        },
        {
            "name": "Radda",
            "sanskrit": "रद्द",
            "description": "Retrogression breaking other yogas",
            "effect": "Obstacles and delays in otherwise favorable combinations"
        },
        {
            "name": "Khallasar",
            "sanskrit": "खल्लासर",
            "description": "Moon separating from planets",
            "effect": "Loss of opportunity, need for patience"
        },
        {
            "name": "Durupha",
            "sanskrit": "दुरुफ",
            "description": "Planets in 12th from each other",
            "effect": "Hidden tensions, secret obstacles"
        }
    ]
    
    return {
        "success": True,
        "system": "Tajaka",
        "total_yogas": len(yogas),
        "yogas": yogas
    }


@router.get("/sahams")
async def get_saham_info() -> Dict[str, Any]:
    """
    Get information about Sahams (Arabic Parts) used in Varshphal.
    
    Sahams are sensitive points calculated using planetary positions.
    """
    sahams = [
        {"name": "Punya Saham", "sanskrit": "पुण्य", "formula": "Asc + Moon - Sun", "signifies": "Fortune, luck, spiritual merit"},
        {"name": "Vivaha Saham", "sanskrit": "विवाह", "formula": "Asc + Venus - Saturn", "signifies": "Marriage, relationships"},
        {"name": "Putra Saham", "sanskrit": "पुत्र", "formula": "Asc + Jupiter - Moon", "signifies": "Children, creativity"},
        {"name": "Pitru Saham", "sanskrit": "पितृ", "formula": "Asc + Sun - Saturn", "signifies": "Father, authority figures"},
        {"name": "Matru Saham", "sanskrit": "मातृ", "formula": "Asc + Moon - Venus", "signifies": "Mother, nurturing"},
        {"name": "Vidya Saham", "sanskrit": "विद्या", "formula": "Asc + Mercury - Sun", "signifies": "Education, learning"},
        {"name": "Dhana Saham", "sanskrit": "धन", "formula": "Asc + 2nd cusp - 2nd lord", "signifies": "Wealth, finances"},
        {"name": "Karma Saham", "sanskrit": "कर्म", "formula": "Asc + Moon - Saturn", "signifies": "Career, profession"},
        {"name": "Mrityu Saham", "sanskrit": "मृत्यु", "formula": "Asc + 8th cusp - Moon", "signifies": "Longevity, transformation"},
        {"name": "Roga Saham", "sanskrit": "रोग", "formula": "Asc + Mars - Saturn", "signifies": "Health, diseases"},
        {"name": "Yatra Saham", "sanskrit": "यात्रा", "formula": "Asc + 9th lord - 9th cusp", "signifies": "Travels, pilgrimages"},
        {"name": "Mitra Saham", "sanskrit": "मित्र", "formula": "Asc + Moon - Mercury", "signifies": "Friends, allies"},
        {"name": "Shatru Saham", "sanskrit": "शत्रु", "formula": "Asc + Saturn - Mars", "signifies": "Enemies, obstacles"},
        {"name": "Prema Saham", "sanskrit": "प्रेम", "formula": "Asc + Venus - Sun", "signifies": "Love, romance"}
    ]
    
    return {
        "success": True,
        "total_sahams": len(sahams),
        "sahams": sahams
    }
