from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

try:
    import requests
except Exception:  # pragma: no cover
    requests = None

try:
    from timezonefinder import TimezoneFinder  # type: ignore
except Exception:  # pragma: no cover
    TimezoneFinder = None  # type: ignore

router = APIRouter()

tf = None
if TimezoneFinder is not None:
    tf = TimezoneFinder(in_memory=True)


class GeoResolveRequest(BaseModel):
    query: str = Field(..., description="Place name to resolve (e.g., 'Loznica, Serbia')")


class GeoResolveResponse(BaseModel):
    latitude: float
    longitude: float
    display_name: str
    raw: Dict[str, Any]


@router.post("/geo/resolve", response_model=GeoResolveResponse)
async def resolve_place_name(req: GeoResolveRequest) -> GeoResolveResponse:
    if requests is None:
        raise HTTPException(status_code=500, detail="requests library not installed")
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": req.query,
            "format": "json",
            "addressdetails": 1,
            "limit": 1,
        }
        headers = {"User-Agent": "kundli-calc/1.0 (OSS)"}
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            raise HTTPException(status_code=404, detail="Place not found")
        top = data[0]
        lat = float(top["lat"])  # type: ignore[index]
        lon = float(top["lon"])  # type: ignore[index]
        return GeoResolveResponse(
            latitude=lat,
            longitude=lon,
            display_name=top.get("display_name", req.query),
            raw=top,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Geocoding error: {str(e)}")


class TimezoneRequest(BaseModel):
    latitude: float
    longitude: float


class TimezoneResponse(BaseModel):
    timezone: str


@router.post("/geo/timezone", response_model=TimezoneResponse)
async def timezone_from_coords(req: TimezoneRequest) -> TimezoneResponse:
    if tf is None:
        raise HTTPException(status_code=500, detail="timezonefinder not installed")
    try:
        tz = tf.timezone_at(lat=req.latitude, lng=req.longitude)
        if not tz:
            raise HTTPException(status_code=404, detail="Timezone not found for coordinates")
        return TimezoneResponse(timezone=tz)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Timezone error: {str(e)}")
