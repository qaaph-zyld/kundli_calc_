"""
API endpoints for Ashtakavarga calculations
"""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from app.core.calculations.ashtakavarga import Ashtakavarga
from app.core.calculations.ashtakavarga_complete import calculate_complete_ashtakavarga

router = APIRouter()

class AshtakavargaRequest(BaseModel):
    """Request model for Ashtakavarga calculations"""
    planet_positions: Dict[str, int] = Field(
        ..., 
        description="Dictionary of planet positions in houses (1-12)"
    )
    
    @field_validator('planet_positions')
    @classmethod
    def validate_positions(cls, v: Dict[str, int]) -> Dict[str, int]:
        valid_planets = {'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'}
        for planet, position in v.items():
            if planet not in valid_planets:
                raise ValueError(f"Invalid planet: {planet}")
            if not 1 <= position <= 12:
                raise ValueError(f"Invalid house position for {planet}: {position}")
        return v

class CompleteAshtakavargaRequest(BaseModel):
    """Request model for complete BPHS-compliant Ashtakavarga calculation"""
    planet_longitudes: Dict[str, float] = Field(
        ...,
        description="Sidereal planetary longitudes in degrees (0-360)"
    )
    ascendant: float = Field(
        ...,
        description="Ascendant/Lagna longitude in sidereal degrees"
    )
    
    @field_validator('planet_longitudes')
    @classmethod
    def validate_longitudes(cls, v: Dict[str, float]) -> Dict[str, float]:
        valid_planets = {'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'}
        for planet, longitude in v.items():
            if planet not in valid_planets:
                raise ValueError(f"Invalid planet: {planet}")
            if not 0 <= longitude < 360:
                raise ValueError(f"Invalid longitude for {planet}: {longitude}")
        return v
    
    @field_validator('ascendant')
    @classmethod
    def validate_ascendant(cls, v: float) -> float:
        if not 0 <= v < 360:
            raise ValueError(f"Ascendant must be between 0 and 360 degrees")
        return v

@router.post("/calculate", response_model=Dict[str, Any], tags=["Ashtakavarga"])
async def calculate_ashtakavarga(request: AshtakavargaRequest) -> Dict[str, Any]:
    """
    Calculate Sarvashtakavarga and analyze planetary strengths
    
    Args:
        request: AshtakavargaRequest containing planet positions
        
    Returns:
        Dictionary containing Sarvashtakavarga and analysis results
        
    Raises:
        HTTPException: If calculation fails
    """
    try:
        # Calculate Sarvashtakavarga
        sarvashtakavarga = Ashtakavarga.calculate_sarvashtakavarga(
            request.planet_positions
        )
        
        # Analyze each planet's strength
        planet_analysis = {}
        for planet in request.planet_positions.keys():
            analysis = Ashtakavarga.analyze_planet_strength(
                planet,
                sarvashtakavarga
            )
            planet_analysis[planet] = analysis
        
        # Get strong houses
        strong_houses = Ashtakavarga.get_strong_houses(sarvashtakavarga)
        
        return {
            'sarvashtakavarga': sarvashtakavarga,
            'planet_analysis': planet_analysis,
            'strong_houses': strong_houses
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze_planet", response_model=Dict[str, Any], tags=["Ashtakavarga"])
async def analyze_planet(
    planet: str,
    request: AshtakavargaRequest
) -> Dict[str, Any]:
    """
    Analyze specific planet's strength using Ashtakavarga
    
    Args:
        planet: Name of the planet to analyze
        request: AshtakavargaRequest containing planet positions
        
    Returns:
        Dictionary containing analysis results for the specified planet
        
    Raises:
        HTTPException: If planet is invalid or calculation fails
    """
    try:
        # Calculate Sarvashtakavarga
        sarvashtakavarga = Ashtakavarga.calculate_sarvashtakavarga(
            request.planet_positions
        )
        
        # Analyze specified planet
        analysis = Ashtakavarga.analyze_planet_strength(
            planet,
            sarvashtakavarga
        )
        
        return {
            'planet': planet,
            'analysis': analysis,
            'bindus_per_house': sarvashtakavarga.get(planet, [])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/complete", response_model=Dict[str, Any], tags=["Ashtakavarga"])
async def calculate_complete_ashtakavarga_endpoint(request: CompleteAshtakavargaRequest) -> Dict[str, Any]:
    """
    Calculate complete BPHS-compliant Ashtakavarga with accurate bindu tables
    
    Implements traditional Ashtakavarga per BPHS Chapters 51-52 using exact
    bindu contribution tables from classical texts.
    
    Args:
        request: CompleteAshtakavargaRequest with planet longitudes and ascendant
        
    Returns:
        Dictionary containing individual and Sarvashtakavarga with house analysis
        
    Reference: BPHS Ch.51-52, Phaladeepika Ch.9, Saravali Ch.38
    """
    try:
        result = calculate_complete_ashtakavarga(
            planet_longitudes=request.planet_longitudes,
            ascendant=request.ascendant
        )
        
        return {
            'individual_ashtakavarga': result.get('individual_ashtakavarga', {}),
            'sarvashtakavarga': result.get('sarvashtakavarga', {}),
            'house_analysis': result.get('house_analysis', {}),
            'calculation_method': 'BPHS Complete (Ch.51-52)',
            'notes': 'Traditional bindu contribution tables per classical texts'
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ashtakavarga error: {str(e)}")
