"""
API endpoints for Shadbala calculations
"""
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.core.calculations.shadbala import ShadbalaSystem
from app.core.calculations.shadbala_complete import CompleteShadbalaCalculator

router = APIRouter()
shadbala_calculator = ShadbalaSystem()
complete_shadbala_calculator = CompleteShadbalaCalculator()

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

class CompleteShadbalaRequest(BaseModel):
    """Request model for complete BPHS-compliant Shadbala calculation"""
    planet_positions: Dict[str, float] = Field(
        ...,
        description="Tropical planetary longitudes in degrees"
    )
    house_cusps: List[float] = Field(
        ...,
        description="List of 12 house cusps in tropical degrees"
    )
    birth_datetime: str = Field(
        ...,
        description="Birth datetime in ISO format (YYYY-MM-DDTHH:MM:SS)"
    )
    latitude: float = Field(..., description="Birth latitude")
    longitude: float = Field(..., description="Birth longitude")
    ayanamsa: Optional[float] = Field(
        default=23.85,
        description="Ayanamsa value (default Lahiri ~23.85°)"
    )
    
    @field_validator('house_cusps')
    @classmethod
    def validate_house_cusps(cls, v: list) -> list:
        if len(v) != 12:
            raise ValueError("Must provide exactly 12 house cusps")
        for cusp in v:
            if not 0 <= cusp < 360:
                raise ValueError(f"Invalid house cusp: {cusp}")
        return v
    
    @field_validator('latitude')
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v
    
    @field_validator('longitude')
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v

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

@router.post("/complete", tags=["Shadbala"])
async def calculate_complete_shadbala(request: CompleteShadbalaRequest):
    """
    Calculate complete BPHS-compliant Shadbala for all planets
    
    This endpoint uses the full six-fold strength calculation per
    Brihat Parashara Hora Shastra Chapter 27.
    
    Args:
        request: CompleteShadbalaRequest with full birth data
        
    Returns:
        Dictionary with detailed Shadbala analysis for all planets
    """
    try:
        from datetime import datetime
        
        # Parse birth datetime
        birth_dt = datetime.fromisoformat(request.birth_datetime)
        
        # Calculate complete Shadbala
        results = complete_shadbala_calculator.calculate_complete_shadbala(
            planet_positions=request.planet_positions,
            house_cusps=request.house_cusps,
            birth_datetime=birth_dt,
            latitude=request.latitude,
            longitude=request.longitude,
            ayanamsa=request.ayanamsa
        )
        
        # Add chart-level summary
        total_rupas = sum(
            r.get('total_rupas', 0) for r in results.values()
        )
        strong_planets = [
            planet for planet, data in results.items()
            if data.get('is_strong', False)
        ]
        weak_planets = [
            planet for planet, data in results.items()
            if not data.get('is_strong', False)
        ]
        
        return {
            'planets': results,
            'summary': {
                'total_rupas': round(total_rupas, 2),
                'average_rupas': round(total_rupas / len(results), 2),
                'strong_planets': strong_planets,
                'weak_planets': weak_planets,
                'calculation_method': 'BPHS Complete (6-fold)',
                'ayanamsa_used': request.ayanamsa
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Shadbala calculation error: {str(e)}")

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
