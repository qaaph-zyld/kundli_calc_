"""
Location Model
PGF Protocol: LOC_001
Gate: GATE_4
Version: 1.0.0
"""

from pydantic import BaseModel, Field

class Location(BaseModel):
    """Location model for astronomical calculations"""
    
    latitude: float = Field(
        ...,
        description="Latitude in decimal degrees",
        ge=-90,
        le=90
    )
    longitude: float = Field(
        ...,
        description="Longitude in decimal degrees",
        ge=-180,
        le=180
    )
    altitude: float = Field(
        0.0,
        description="Altitude in meters above sea level"
    )
    timezone: str = Field(
        ...,
        description="Timezone name (e.g., 'Asia/Kolkata')"
    )
