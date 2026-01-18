"""
Location API Endpoints
Geocoding and timezone lookup.
"""

from typing import List, Optional

from app.core.services.location_service import LocationService
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter()


class LocationResult(BaseModel):
    """Location search result"""

    city: str
    state: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    utc_offset: float
    display_name: str


class LocationSearchResponse(BaseModel):
    """Response for location search"""

    results: List[LocationResult]
    count: int


@router.get("/search", response_model=LocationSearchResponse)
async def search_location(
    q: str = Query(..., description="City name to search"),
    limit: int = Query(5, ge=1, le=10, description="Max results"),
):
    """
    Search for cities by name.
    Returns coordinates and timezone information.

    Uses free OpenStreetMap Nominatim API.
    """
    service = LocationService()

    try:
        results = await service.search_city(q, limit)

        return LocationSearchResponse(
            results=[
                LocationResult(
                    city=r.city,
                    state=r.state,
                    country=r.country,
                    latitude=r.latitude,
                    longitude=r.longitude,
                    timezone=r.timezone,
                    utc_offset=r.utc_offset,
                    display_name=r.display_name,
                )
                for r in results
            ],
            count=len(results),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Location search failed: {str(e)}")


@router.get("/reverse")
async def reverse_geocode(
    lat: float = Query(..., description="Latitude"), lon: float = Query(..., description="Longitude")
):
    """
    Get location info from coordinates.
    Returns city, country, and timezone.
    """
    service = LocationService()

    try:
        result = await service.reverse_geocode(lat, lon)

        if not result:
            raise HTTPException(status_code=404, detail="Location not found")

        return LocationResult(
            city=result.city,
            state=result.state,
            country=result.country,
            latitude=result.latitude,
            longitude=result.longitude,
            timezone=result.timezone,
            utc_offset=result.utc_offset,
            display_name=result.display_name,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reverse geocoding failed: {str(e)}")


@router.get("/timezone")
async def get_timezone(
    city: Optional[str] = Query(None, description="City name"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
):
    """
    Get timezone for a location.
    Can use city name OR coordinates.
    """
    service = LocationService()

    if city:
        # Quick lookup
        result = service.get_timezone_for_city(city)
        if result:
            return {"timezone": result[0], "utc_offset": result[1], "source": "cache"}

        # Full geocode
        loc = await service.geocode(city)
        if loc:
            return {"timezone": loc.timezone, "utc_offset": loc.utc_offset, "source": "geocode"}

    if lat is not None and lon is not None:
        tz_name, offset = service._approximate_timezone(lat, lon)
        return {"timezone": tz_name, "utc_offset": offset, "source": "approximate"}

    raise HTTPException(status_code=400, detail="Provide city name or lat/lon coordinates")
