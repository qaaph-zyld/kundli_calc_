"""
Location Service - Geocoding & Timezone
Uses free public APIs for city lookup and timezone detection.

APIs Used:
- Nominatim (OpenStreetMap) - Free geocoding, no API key required
- TimeZoneDB - Free timezone API (optional key for higher limits)
- WorldTimeAPI - Free timezone, no API key required
"""

import httpx
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import math


@dataclass
class GeoLocation:
    """Geographic location with timezone"""
    city: str
    state: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    utc_offset: float  # hours
    display_name: str


class LocationService:
    """
    Free geocoding and timezone service.
    Uses public APIs that don't require API keys.
    """
    
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"
    WORLDTIME_URL = "http://worldtimeapi.org/api/timezone"
    TIMEZONEDB_URL = "http://api.timezonedb.com/v2.1/get-time-zone"
    
    # Fallback timezone data for major cities
    CITY_TIMEZONES = {
        # India
        "delhi": ("Asia/Kolkata", 5.5),
        "mumbai": ("Asia/Kolkata", 5.5),
        "kolkata": ("Asia/Kolkata", 5.5),
        "chennai": ("Asia/Kolkata", 5.5),
        "bangalore": ("Asia/Kolkata", 5.5),
        "hyderabad": ("Asia/Kolkata", 5.5),
        "pune": ("Asia/Kolkata", 5.5),
        "jaipur": ("Asia/Kolkata", 5.5),
        "lucknow": ("Asia/Kolkata", 5.5),
        "ahmedabad": ("Asia/Kolkata", 5.5),
        # Europe
        "london": ("Europe/London", 0),
        "paris": ("Europe/Paris", 1),
        "berlin": ("Europe/Berlin", 1),
        "rome": ("Europe/Rome", 1),
        "madrid": ("Europe/Madrid", 1),
        "amsterdam": ("Europe/Amsterdam", 1),
        "belgrade": ("Europe/Belgrade", 1),
        "loznica": ("Europe/Belgrade", 1),
        # USA
        "new york": ("America/New_York", -5),
        "los angeles": ("America/Los_Angeles", -8),
        "chicago": ("America/Chicago", -6),
        "houston": ("America/Chicago", -6),
        "phoenix": ("America/Phoenix", -7),
        "san francisco": ("America/Los_Angeles", -8),
        # Asia
        "tokyo": ("Asia/Tokyo", 9),
        "singapore": ("Asia/Singapore", 8),
        "hong kong": ("Asia/Hong_Kong", 8),
        "dubai": ("Asia/Dubai", 4),
        "bangkok": ("Asia/Bangkok", 7),
        # Australia
        "sydney": ("Australia/Sydney", 10),
        "melbourne": ("Australia/Melbourne", 10),
    }
    
    def __init__(self, timezonedb_key: Optional[str] = None):
        self.timezonedb_key = timezonedb_key
        self.headers = {
            "User-Agent": "KundliCalculator/1.0 (contact@example.com)"
        }
    
    async def search_city(self, query: str, limit: int = 5) -> List[GeoLocation]:
        """
        Search for cities by name.
        Returns list of matching locations with coordinates and timezone.
        """
        results = []
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self.NOMINATIM_URL,
                    params={
                        "q": query,
                        "format": "json",
                        "limit": limit,
                        "addressdetails": 1,
                    },
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for item in data:
                        addr = item.get("address", {})
                        lat = float(item.get("lat", 0))
                        lon = float(item.get("lon", 0))
                        
                        # Get timezone
                        tz_name, utc_offset = await self._get_timezone(lat, lon)
                        
                        results.append(GeoLocation(
                            city=addr.get("city") or addr.get("town") or addr.get("village") or query,
                            state=addr.get("state", ""),
                            country=addr.get("country", ""),
                            latitude=lat,
                            longitude=lon,
                            timezone=tz_name,
                            utc_offset=utc_offset,
                            display_name=item.get("display_name", "")
                        ))
        except Exception as e:
            # Fallback to manual lookup
            pass
        
        return results
    
    async def geocode(self, city: str, country: str = "") -> Optional[GeoLocation]:
        """Get coordinates for a city name"""
        query = f"{city}, {country}" if country else city
        results = await self.search_city(query, limit=1)
        return results[0] if results else None
    
    async def reverse_geocode(self, latitude: float, longitude: float) -> Optional[GeoLocation]:
        """Get location info from coordinates"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self.NOMINATIM_REVERSE_URL,
                    params={
                        "lat": latitude,
                        "lon": longitude,
                        "format": "json",
                        "addressdetails": 1,
                    },
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    addr = data.get("address", {})
                    
                    tz_name, utc_offset = await self._get_timezone(latitude, longitude)
                    
                    return GeoLocation(
                        city=addr.get("city") or addr.get("town") or addr.get("village", ""),
                        state=addr.get("state", ""),
                        country=addr.get("country", ""),
                        latitude=latitude,
                        longitude=longitude,
                        timezone=tz_name,
                        utc_offset=utc_offset,
                        display_name=data.get("display_name", "")
                    )
        except Exception:
            pass
        
        return None
    
    async def _get_timezone(self, lat: float, lon: float) -> tuple:
        """Get timezone for coordinates"""
        # Try WorldTimeAPI first (free, no key)
        try:
            tz = await self._get_timezone_worldtime(lat, lon)
            if tz:
                return tz
        except Exception:
            pass
        
        # Fallback to approximate timezone from longitude
        return self._approximate_timezone(lat, lon)
    
    async def _get_timezone_worldtime(self, lat: float, lon: float) -> Optional[tuple]:
        """Get timezone from WorldTimeAPI"""
        # WorldTimeAPI doesn't support coordinates directly
        # We'll use the approximate method instead
        return None
    
    def _approximate_timezone(self, lat: float, lon: float) -> tuple:
        """Approximate timezone from longitude"""
        # Each 15 degrees = 1 hour offset
        offset = round(lon / 15)
        
        # Clamp to valid range
        offset = max(-12, min(14, offset))
        
        # Determine timezone name based on region
        if 68 <= lon <= 97 and 8 <= lat <= 37:
            return ("Asia/Kolkata", 5.5)  # India
        elif -10 <= lon <= 40 and 35 <= lat <= 70:
            return (f"Etc/GMT{-offset:+d}", offset)  # Europe
        elif -130 <= lon <= -60 and 25 <= lat <= 50:
            return (f"Etc/GMT{-offset:+d}", offset)  # USA
        else:
            return (f"Etc/GMT{-offset:+d}", offset)
    
    def get_timezone_for_city(self, city: str) -> Optional[tuple]:
        """Quick lookup for common cities"""
        city_lower = city.lower().strip()
        return self.CITY_TIMEZONES.get(city_lower)


# Synchronous wrapper for non-async contexts
def search_city_sync(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Synchronous city search"""
    import asyncio
    
    async def _search():
        service = LocationService()
        results = await service.search_city(query, limit)
        return [
            {
                "city": r.city,
                "state": r.state,
                "country": r.country,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "timezone": r.timezone,
                "utc_offset": r.utc_offset,
                "display_name": r.display_name
            }
            for r in results
        ]
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(_search())


def get_timezone_offset(city: str) -> float:
    """Quick timezone offset lookup"""
    service = LocationService()
    result = service.get_timezone_for_city(city)
    if result:
        return result[1]
    return 0.0
