from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime
from typing import Optional, Dict, Any, List
from decimal import Decimal

from ..models import ChartRequest, ChartResponse
from ...core.astronomical import (
    AstronomicalCalculator as SweCalculator,
    GeoLocation,
    AyanamsaSystem,
    CelestialBody,
)
from ...core.calculations.houses import HouseCalculator
from ...core.calculations.aspects import EnhancedAspectCalculator
from ...core.calculations.nakshatra import NakshatraCalculator
from ...core.calculations.divisional_charts import DivisionalChartEngine
import json
from ...core.cache import redis_cache as cache
from ...core.config import settings
import swisseph as swe

router = APIRouter()

@router.post(
    "/calculate",
    response_model=ChartResponse,
    summary="Calculate birth chart",
    description="""
    Calculate a Vedic birth chart based on date, time, and location.
    
    This endpoint performs the following calculations:
    - Planetary positions using Swiss Ephemeris
    - House cusps and angles
    - Planetary aspects
    - Nakshatras for all planets
    
    The response includes:
    - Planetary positions (longitude, latitude, distance, speed)
    - House system data (cusps, ascendant, midheaven, vertex)
    - Planetary aspects
    - Ayanamsa value used in calculations
    """,
    response_description="Complete birth chart data"
)
async def calculate_chart(
    request: ChartRequest
) -> ChartResponse:
    """Calculate a Vedic birth chart."""
    try:
        cache_key = (
            f"chart:{request.date_time.isoformat()}"
            f":{request.latitude}:{request.longitude}:{request.altitude}"
            f":{request.ayanamsa}:{request.house_system}"
        )
        
        # Try to get from cache
        cached_json = cache.get(cache_key)
        if cached_json:
            try:
                cached_obj = json.loads(cached_json)
                return ChartResponse(**cached_obj)
            except Exception:
                pass
        
        # Build GeoLocation
        geo = GeoLocation(
            latitude=float(request.latitude),
            longitude=float(request.longitude),
            altitude=float(request.altitude),
        )
        
        # Ayanamsa mapping (int or string)
        ay_map_int = {
            1: AyanamsaSystem.LAHIRI,
            2: AyanamsaSystem.RAMAN,
            3: AyanamsaSystem.KRISHNAMURTI,
        }
        ay_map_str = {
            "lahiri": AyanamsaSystem.LAHIRI,
            "raman": AyanamsaSystem.RAMAN,
            "krishnamurti": AyanamsaSystem.KRISHNAMURTI,
            "fagan_bradley": AyanamsaSystem.FAGAN_BRADLEY,
            "fagan": AyanamsaSystem.FAGAN_BRADLEY,
        }
        if getattr(request, "ayanamsa_type", None):
            ay_system = ay_map_str.get(str(request.ayanamsa_type).lower(), AyanamsaSystem.LAHIRI)
        else:
            ay_system = ay_map_int.get(int(request.ayanamsa or 1), AyanamsaSystem.LAHIRI)
        swe_calc = SweCalculator(ayanamsa_system=ay_system)
        house_calc = HouseCalculator()
        
        # Planetary positions via Swiss Ephemeris
        positions = swe_calc.calculate_all_positions(request.date_time, geo)
        
        # Convert to API-friendly dict
        def body_name(b: CelestialBody) -> str:
            name_map = {
                CelestialBody.SUN: "Sun",
                CelestialBody.MOON: "Moon",
                CelestialBody.MARS: "Mars",
                CelestialBody.MERCURY: "Mercury",
                CelestialBody.JUPITER: "Jupiter",
                CelestialBody.VENUS: "Venus",
                CelestialBody.SATURN: "Saturn",
                CelestialBody.RAHU: "Rahu",
                CelestialBody.KETU: "Ketu",
                CelestialBody.URANUS: "Uranus",
                CelestialBody.NEPTUNE: "Neptune",
                CelestialBody.PLUTO: "Pluto",
            }
            return name_map.get(b, str(b))

        planetary_positions_api: Dict[str, Dict[str, Decimal]] = {}
        planetary_positions_for_aspects: Dict[str, Dict[str, Any]] = {}
        for body, pos in positions.items():
            name = body_name(body)
            planetary_positions_api[name] = {
                "longitude": Decimal(str(pos.longitude)),
                "latitude": Decimal(str(pos.latitude)),
                "distance": Decimal(str(pos.distance)),
                "speed": Decimal(str(pos.speed)),
            }
            planetary_positions_for_aspects[name] = {
                "longitude": float(pos.longitude),
                "speed": float(pos.speed),
                "is_retrograde": bool(pos.is_retrograde),
                "house": 1,
                "dignity": "neutral",
            }
        
        # Houses
        hs_code_map = {
            "P": "PLACIDUS",
            "K": "KOCH",
            "E": "EQUAL",
            "W": "WHOLE_SIGN",
            "R": "REGIOMONTANUS",
            "C": "CAMPANUS",
        }
        hs_name = hs_code_map.get(request.house_system, "PLACIDUS")
        houses_dict = house_calc.calculate_houses(
            request.date_time,
            float(request.latitude),
            float(request.longitude),
            hs_name,
        )
        
        # Aspects
        aspect_calc = EnhancedAspectCalculator()
        # Compute house per planet for aspect strength
        for pname, pdata in planetary_positions_for_aspects.items():
            pdata["house"] = house_calc.get_house_for_longitude(
                pdata["longitude"], houses_dict["cusps"]
            )

        aspects_list = aspect_calc.calculate_aspects(planetary_positions_for_aspects)
        aspects_api: List[Dict[str, Any]] = []
        for a in aspects_list:
            aspects_api.append({
                "aspect_type": a.aspect.name,
                "strength": Decimal(str(a.total_influence)),
                "is_beneficial": bool(a.aspect.benefic_nature >= 0),
                "special_effects": None,
            })
        
        # Ayanamsa value
        jd = swe.julday(
            request.date_time.year,
            request.date_time.month,
            request.date_time.day,
            request.date_time.hour + request.date_time.minute / 60.0 + request.date_time.second / 3600.0,
        )
        ay_value = Decimal(str(swe.get_ayanamsa_ut(jd)))

        # Planetary strengths
        from ...core.calculations.planetary_strength import PlanetaryStrengthCalculator
        psc = PlanetaryStrengthCalculator()
        planetary_strengths: Dict[str, Dict[str, Decimal]] = {}
        for pname, pdata in planetary_positions_api.items():
            house_num = house_calc.get_house_for_longitude(float(pdata["longitude"]), houses_dict["cusps"]) if isinstance(pdata["longitude"], Decimal) else house_calc.get_house_for_longitude(pdata["longitude"], houses_dict["cusps"]) 
            strength = psc.calculate_strength(
                pname,
                float(pdata["longitude"]),
                request.date_time,
                house_num,
            )
            planetary_strengths[pname] = {
                "shadbala": Decimal(str(strength.shadbala)),
                "dignity_score": Decimal(str(strength.dignity_score)),
                "positional_strength": Decimal(str(strength.positional_strength)),
                "temporal_strength": Decimal(str(strength.temporal_strength)),
                "aspect_strength": Decimal(str(strength.aspect_strength)),
                "total_strength": Decimal(str(strength.total_strength)),
            }

        # Divisional charts (D9, D10)
        div_engine = DivisionalChartEngine()
        d9 = div_engine.calculate_chart(request.date_time, 9, {
            "lat": float(request.latitude),
            "lon": float(request.longitude),
            "alt": float(request.altitude),
        })
        d10 = div_engine.calculate_chart(request.date_time, 10, {
            "lat": float(request.latitude),
            "lon": float(request.longitude),
            "alt": float(request.altitude),
        })

        # Build response payload
        result_payload: Dict[str, Any] = {
            "planetary_positions": planetary_positions_api,
            "houses": {
                "cusps": [Decimal(str(x)) for x in houses_dict["cusps"]],
                "ascendant": Decimal(str(houses_dict["ascendant"])),
                "midheaven": Decimal(str(houses_dict["midheaven"])),
                "vertex": Decimal(str(houses_dict["vertex"])),
            },
            "aspects": aspects_api,
            "ayanamsa_value": ay_value,
            "planetary_strengths": planetary_strengths,
            "divisional_charts": {
                "D9": {
                    "division": 9,
                    "planetary_positions": {
                        k: {
                            "longitude": Decimal(str(v)),
                            "latitude": Decimal("0"),
                            "distance": Decimal("0"),
                            "speed": Decimal("0"),
                        }
                        for k, v in d9.planets.items()
                    },
                    "house_cusps": [Decimal(str(x)) for x in d9.houses],
                    "special_points": {},
                },
                "D10": {
                    "division": 10,
                    "planetary_positions": {
                        k: {
                            "longitude": Decimal(str(v)),
                            "latitude": Decimal("0"),
                            "distance": Decimal("0"),
                            "speed": Decimal("0"),
                        }
                        for k, v in d10.planets.items()
                    },
                    "house_cusps": [Decimal(str(x)) for x in d10.houses],
                    "special_points": {},
                },
            },
        }
        result = ChartResponse(**result_payload)
        
        # Cache the result
        try:
            cache.set(
                cache_key,
                json.dumps(result.model_dump()),
                expire=settings.REDIS_CACHE_EXPIRE_SECONDS,
            )
        except Exception:
            pass
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error calculating birth chart: {str(e)}"
        )
