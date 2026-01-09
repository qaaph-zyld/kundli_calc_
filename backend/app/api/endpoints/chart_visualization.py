"""
Chart Visualization API
========================

Provides structured chart data for frontend rendering.
Includes planets, houses, aspects, yogas in JSON format optimized for D3.js/Canvas/SVG.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter()


class PlanetVisualization(BaseModel):
    """Planet data for visualization"""
    name: str
    longitude: float = Field(..., ge=0, lt=360)
    sign: str
    house: int = Field(..., ge=1, le=12)
    dignity: str
    retrograde: bool = False
    degree_in_sign: float = Field(..., ge=0, lt=30)


class HouseVisualization(BaseModel):
    """House data for visualization"""
    number: int = Field(..., ge=1, le=12)
    sign: str
    cusp_longitude: float = Field(..., ge=0, lt=360)


class AspectVisualization(BaseModel):
    """Aspect data for visualization"""
    from_planet: str
    to_planet: str
    aspect_type: str
    strength: float = Field(..., ge=0, le=100)
    is_benefic: bool


class YogaVisualization(BaseModel):
    """Yoga data for visualization"""
    name: str
    planets_involved: List[str]
    houses_involved: List[int]
    formation_strength: float = Field(..., ge=0, le=100)
    category: str


class ChartVisualizationResponse(BaseModel):
    """Complete chart visualization data"""
    chart_id: str
    planets: List[PlanetVisualization]
    houses: List[HouseVisualization]
    aspects: List[AspectVisualization]
    yogas: List[YogaVisualization]
    ascendant_sign: str
    ascendant_degree: float


@router.get(
    "/visualization/{chart_id}",
    response_model=ChartVisualizationResponse,
    summary="Get chart visualization data",
    description="""
    **Chart Visualization Data for Frontend Rendering**
    
    Provides complete structured data for drawing Vedic astrology charts:
    - Planet positions with exact longitudes
    - House cusps (Whole Sign system)
    - Aspects with strength calculations
    - Active yogas with formation strength
    
    **Optimized for:**
    - D3.js chart rendering
    - HTML Canvas drawing
    - SVG visualization
    - React/Next.js components
    
    **Response includes:**
    - Exact planetary longitudes (0-360°)
    - Degree within sign (0-30°)
    - Retrograde status
    - Dignity (exalted/own/debilitated)
    - Aspect lines with strength
    - Yoga highlighting data
    
    **Use this to:**
    - Draw interactive birth charts
    - Highlight yogas visually
    - Show aspect lines
    - Enable click-to-interpret functionality
    """
)
async def get_chart_visualization(chart_id: str):
    """Get structured chart data for frontend visualization"""
    try:
        # In production, retrieve from database
        # For now, return structured example data
        
        example_chart = ChartVisualizationResponse(
            chart_id=chart_id,
            planets=[
                PlanetVisualization(
                    name="Sun",
                    longitude=45.23,
                    sign="Taurus",
                    house=10,
                    dignity="neutral",
                    retrograde=False,
                    degree_in_sign=15.23
                ),
                PlanetVisualization(
                    name="Moon",
                    longitude=105.67,
                    sign="Cancer",
                    house=4,
                    dignity="own_sign",
                    retrograde=False,
                    degree_in_sign=15.67
                ),
                PlanetVisualization(
                    name="Jupiter",
                    longitude=255.89,
                    sign="Sagittarius",
                    house=9,
                    dignity="own_sign",
                    retrograde=False,
                    degree_in_sign=15.89
                )
            ],
            houses=[
                HouseVisualization(number=i, sign=signs[(i-1) % 12], cusp_longitude=i*30.0)
                for i, signs in [(j, ["Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn",
                                      "Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer"])]
                for j in range(1, 13)
            ],
            aspects=[
                AspectVisualization(
                    from_planet="Jupiter",
                    to_planet="Sun",
                    aspect_type="5th_aspect",
                    strength=85.0,
                    is_benefic=True
                )
            ],
            yogas=[
                YogaVisualization(
                    name="Gaja Kesari Yoga",
                    planets_involved=["Jupiter", "Moon"],
                    houses_involved=[9, 4],
                    formation_strength=87.5,
                    category="Raja Yoga"
                )
            ],
            ascendant_sign="Leo",
            ascendant_degree=0.0
        )
        
        return example_chart
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating chart visualization: {str(e)}"
        )


@router.post("/visualization/generate")
async def generate_chart_visualization(birth_data: Dict[str, Any]):
    """Generate chart visualization from birth data"""
    try:
        # This would calculate actual positions using Swiss Ephemeris
        # For now, return structured format
        
        return {
            "status": "success",
            "message": "Chart visualization data generated",
            "note": "Integrate with calculation engine for real positions"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )
