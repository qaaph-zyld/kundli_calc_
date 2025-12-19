"""
API endpoints for Shadbala calculations
"""
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.core.calculations.shadbala import ShadbalaSystem

router = APIRouter()
shadbala_calculator = ShadbalaSystem()

class AspectData(BaseModel):
    """Model for aspect data"""
    type: str = Field(..., description="Type of aspect")
    angle: float = Field(..., description="Aspect angle in degrees")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        valid_types = {'conjunction', 'sextile', 'square', 'trine', 'opposition'}
        if v not in valid_types:
            raise ValueError(f"Invalid aspect type. Must be one of: {valid_types}")
        return v
    
    @field_validator('angle')
    @classmethod
    def validate_angle(cls, v: float) -> float:
        if not 0 <= v < 360:
            raise ValueError("Angle must be between 0 and 360 degrees")
        return v

class ShadbalaRequest(BaseModel):
    """Request model for Shadbala calculation"""
    planet: str = Field(..., description="Planet name")
    position: float = Field(..., description="Planet position in degrees")
    house: int = Field(..., description="House number (1-12)")
    is_day: bool = Field(..., description="Whether birth is during day")
    aspects: List[AspectData] = Field(
        ..., 
        description="List of aspects to the planet"
    )
    planet_positions: Dict[str, float] = Field(
        ..., 
        description="Positions of all planets"
    )
    
    @field_validator('planet')
    @classmethod
    def validate_planet(cls, v: str) -> str:
        valid_planets = {
            'sun', 'moon', 'mars', 'mercury',
            'jupiter', 'venus', 'saturn'
        }
        if v.lower() not in valid_planets:
            raise ValueError(f"Invalid planet: {v}")
        return v.lower()
    
    @field_validator('position')
    @classmethod
    def validate_position(cls, v: float) -> float:
        if not 0 <= v < 360:
            raise ValueError("Position must be between 0 and 360 degrees")
        return v
    
    @field_validator('house')
    @classmethod
    def validate_house(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("House must be between 1 and 12")
        return v
    
    @field_validator('planet_positions')
    @classmethod
    def validate_planet_positions(cls, v: dict) -> dict:
        valid_planets = {
            'sun', 'moon', 'mars', 'mercury',
            'jupiter', 'venus', 'saturn'
        }
        for planet, position in v.items():
            if planet.lower() not in valid_planets:
                raise ValueError(f"Invalid planet: {planet}")
            if not 0 <= position < 360:
                raise ValueError(f"Invalid position for {planet}: {position}")
        return {k.lower(): v for k, v in v.items()}

class ShadbalaAnalysisRequest(BaseModel):
    """Request model for complete Shadbala analysis"""
    birth_time_is_day: bool = Field(
        ..., 
        description="Whether birth time is during day"
    )
    planet_positions: Dict[str, float] = Field(
        ..., 
        description="Positions of all planets"
    )
    aspects: Dict[str, List[AspectData]] = Field(
        ..., 
        description="Aspects for each planet"
    )
    house_positions: Dict[str, int] = Field(
        ..., 
        description="House positions of planets"
    )

@router.post("/calculate", tags=["Shadbala"])
async def calculate_shadbala(request: ShadbalaRequest):
    """
    Calculate Shadbala strength for a single planet
    
    Args:
        request: ShadbalaRequest containing planet data
        
    Returns:
        Dictionary containing Shadbala analysis
    """
    try:
        # Convert aspects to dict format expected by calculator
        aspects = [{"type": a.type, "angle": a.angle} for a in request.aspects]
        
        # Use default speed of 1.0 if not provided (simplified)
        speed = 1.0
        
        result = shadbala_calculator.calculate_shadbala(
            request.planet,
            request.house,
            speed,
            aspects,
            request.is_day
        )
        
        # Add interpretation
        result["interpretation"] = _interpret_shadbala(result)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def _interpret_shadbala(result: dict) -> str:
    """Generate interpretation text for Shadbala result."""
    planet = result.get("planet", "Planet")
    is_strong = result.get("is_strong", False)
    percentage = result.get("percentage", 0)
    
    if is_strong:
        return f"{planet} has strong Shadbala ({percentage}% of minimum required). This indicates good capacity to deliver positive results."
    else:
        return f"{planet} has weak Shadbala ({percentage}% of minimum required). Results may be delayed or diminished."

@router.post("/analyze", tags=["Shadbala"])
async def analyze_all_planets(request: ShadbalaAnalysisRequest):
    """
    Calculate Shadbala strength for all planets
    
    Args:
        request: ShadbalaAnalysisRequest containing birth data
        
    Returns:
        Dictionary containing Shadbala analysis for all planets
    """
    try:
        results = {}
        for planet, position in request.planet_positions.items():
            aspects_data = request.aspects.get(planet, [])
            house = request.house_positions.get(planet)
            
            if house is None:
                raise ValueError(f"Missing house position for {planet}")
            
            # Convert aspects to dict format
            aspects = [{"type": a.type, "angle": a.angle} for a in aspects_data]
            
            # Use default speed
            speed = 1.0
                
            result = shadbala_calculator.calculate_shadbala(
                planet,
                house,
                speed,
                aspects,
                request.birth_time_is_day
            )
            result["interpretation"] = _interpret_shadbala(result)
            results[planet] = result
            
        # Calculate overall chart strength
        total_rupas = sum(r['total_rupas'] for r in results.values())
        average_rupas = total_rupas / len(results) if results else 0
        
        return {
            'planets': results,
            'chart_analysis': {
                'total_rupas': round(total_rupas, 2),
                'average_rupas': round(average_rupas, 2),
                'interpretation': f"Average Shadbala: {round(average_rupas, 2)} Rupas"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
