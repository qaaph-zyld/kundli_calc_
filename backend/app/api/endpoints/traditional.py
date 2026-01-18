from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import pytz
from app.core.analysis.bhava_analysis import create_comprehensive_bhava_report
from app.core.astronomical import AstronomicalCalculator as SweCalculator
from app.core.astronomical import (
    AyanamsaSystem,
    CelestialBody,
    GeoLocation,
)
from app.core.calculations.ashtakavarga_complete import calculate_complete_ashtakavarga
from app.core.calculations.aspects import EnhancedAspectCalculator
from app.core.calculations.dasha_system import VimshottariDasha
from app.core.calculations.gochara_transits import GocharaSystem
from app.core.calculations.houses import HouseCalculator
from app.core.calculations.jaimini_complete import calculate_complete_jaimini_analysis
from app.core.calculations.shadbala import ShadbalaSystem
from app.core.calculations.transit_analysis import get_current_transit_positions
from app.core.remedies.gemstone_system import recommend_gemstones_for_chart
from app.core.remedies.mantra_charity_system import create_complete_remedial_plan
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

router = APIRouter()


_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]


def _planet_house_whole_sign(planet_lon: float, asc_lon: float) -> int:
    p_sign = int(planet_lon / 30) % 12
    a_sign = int(asc_lon / 30) % 12
    return ((p_sign - a_sign) % 12) + 1


def _rotate_sarva_by_house(sarva_by_sign: List[int], asc_lon: float) -> List[int]:
    asc_sign = int(asc_lon / 30) % 12
    return [sarva_by_sign[(asc_sign + i) % 12] for i in range(12)]


def _functional_benefics(asc_lon: float) -> List[str]:
    """Functional benefics by sign-lordship (simplified but deterministic)."""
    asc_sign = int(asc_lon / 30) % 12

    sign_lords = {
        0: "Mars",
        1: "Venus",
        2: "Mercury",
        3: "Moon",
        4: "Sun",
        5: "Mercury",
        6: "Venus",
        7: "Mars",
        8: "Jupiter",
        9: "Saturn",
        10: "Saturn",
        11: "Jupiter",
    }

    house_sign = {house: (asc_sign + (house - 1)) % 12 for house in range(1, 13)}
    planet_houses: Dict[str, List[int]] = {}
    for house, sign in house_sign.items():
        planet = sign_lords[sign]
        planet_houses.setdefault(planet, []).append(house)

    trines = {1, 5, 9}
    dusthanas = {6, 8, 12}

    benefics: List[str] = []
    for planet, houses in planet_houses.items():
        if any(h in trines for h in houses) and not any(h in dusthanas for h in houses):
            benefics.append(planet)

    lagna_lord = sign_lords[asc_sign]
    if lagna_lord not in benefics:
        benefics.append(lagna_lord)

    return benefics


class TraditionalReportRequest(BaseModel):
    date: str = Field(..., description="Birth date YYYY-MM-DD")
    time: str = Field(..., description="Birth time HH:MM or HH:MM:SS")
    timezone: str = Field(..., description="IANA timezone, e.g. Europe/Belgrade")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    ayanamsa: str = Field(default="lahiri", description="Ayanamsa: lahiri|raman|krishnamurti")
    house_system: str = Field(default="W", description="House system code (W recommended)")

    include_ashtakavarga_reductions: bool = Field(default=True)
    include_current_transits: bool = Field(default=True)
    transit_datetime_utc: Optional[datetime] = Field(
        default=None, description="Optional UTC datetime for transit snapshot"
    )

    @field_validator("date")
    @classmethod
    def _validate_date(cls, v: str) -> str:
        datetime.strptime(v, "%Y-%m-%d")
        return v

    @field_validator("time")
    @classmethod
    def _validate_time(cls, v: str) -> str:
        # Accept HH:MM or HH:MM:SS
        for fmt in ("%H:%M", "%H:%M:%S"):
            try:
                datetime.strptime(v, fmt)
                return v
            except ValueError:
                continue
        raise ValueError("Invalid time format. Use HH:MM or HH:MM:SS")


@router.post("/report", tags=["traditional"])
async def traditional_report(req: TraditionalReportRequest) -> Dict[str, Any]:
    """Generate full traditional report using: Lahiri + Whole Sign + traditional engines."""
    try:
        tz = pytz.timezone(req.timezone)

        if len(req.time.split(":")) == 2:
            local_dt = datetime.strptime(f"{req.date} {req.time}", "%Y-%m-%d %H:%M")
        else:
            local_dt = datetime.strptime(f"{req.date} {req.time}", "%Y-%m-%d %H:%M:%S")

        birth_local = tz.localize(local_dt)
        birth_utc = birth_local.astimezone(pytz.UTC)
        birth_utc_naive = birth_utc.replace(tzinfo=None)

        ay_map = {
            "lahiri": AyanamsaSystem.LAHIRI,
            "raman": AyanamsaSystem.RAMAN,
            "krishnamurti": AyanamsaSystem.KRISHNAMURTI,
        }
        ay_system = ay_map.get(req.ayanamsa.lower(), AyanamsaSystem.LAHIRI)

        geo = GeoLocation(latitude=req.latitude, longitude=req.longitude, altitude=0.0)

        swe_calc = SweCalculator(ayanamsa_system=ay_system)
        positions = swe_calc.calculate_all_positions(birth_utc_naive, geo)

        # Ascendant (sidereal) via HouseCalculator
        house_calc = HouseCalculator()
        houses = house_calc.calculate_houses(birth_utc_naive, req.latitude, req.longitude, "WHOLE_SIGN")
        asc_lon = float(houses["ascendant"])
        asc_sign = int(asc_lon / 30) % 12

        # Extract natal longitudes/speeds
        natal_lons: Dict[str, float] = {}
        natal_speeds: Dict[str, float] = {}
        for body, pos in positions.items():
            name = (
                body.value.title()
                if body.value not in ["rahu", "ketu"]
                else ("Rahu" if body == CelestialBody.RAHU else "Ketu")
            )
            if name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                natal_lons[name] = float(pos.longitude)
                natal_speeds[name] = float(pos.speed)

        # Aspects (for shadbala Drik Bala)
        aspect_calc = EnhancedAspectCalculator()
        aspect_input: Dict[str, Dict[str, Any]] = {}
        for planet, lon in natal_lons.items():
            if planet not in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
                continue
            aspect_input[planet] = {
                "longitude": lon,
                "speed": natal_speeds.get(planet, 0.0),
                "is_retrograde": natal_speeds.get(planet, 0.0) < 0,
                "house": _planet_house_whole_sign(lon, asc_lon),
                "dignity": "neutral",
            }
        aspects = aspect_calc.calculate_aspects(aspect_input)
        aspects_by_planet: Dict[str, List[Dict[str, Any]]] = {p: [] for p in aspect_input}
        for a in aspects:
            atype = a.aspect.name.lower()
            aspects_by_planet[a.planet1].append({"type": atype})
            aspects_by_planet[a.planet2].append({"type": atype})

        # Shadbala
        is_day = 6 <= birth_local.hour < 18
        shadbala = ShadbalaSystem()
        shadbala_results: Dict[str, Any] = {}
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            house_num = _planet_house_whole_sign(natal_lons[planet], asc_lon)
            shadbala_results[planet] = shadbala.calculate_shadbala(
                planet=planet,
                house=house_num,
                speed=natal_speeds.get(planet, 0.0),
                aspects=aspects_by_planet.get(planet, []),
                is_day=is_day,
            )

        # Vimshottari Dasha
        dasha_calc = VimshottariDasha()
        dasha_at_birth = dasha_calc.calculate_dasha_at_birth(birth_utc_naive, natal_lons["Moon"])
        current_dasha = dasha_calc.get_current_dasha(
            birth_utc_naive,
            natal_lons["Moon"],
            datetime.now(timezone.utc).replace(tzinfo=None),
        )

        # Ashtakavarga
        av = calculate_complete_ashtakavarga(
            natal_lons,
            asc_lon,
            apply_reductions=req.include_ashtakavarga_reductions,
        )
        sarva_by_sign = av["sarvashtakavarga"]["bindus_per_house"]
        sarva_by_house = _rotate_sarva_by_house(sarva_by_sign, asc_lon)

        # Jaimini
        jaimini = calculate_complete_jaimini_analysis(birth_utc_naive, asc_lon, natal_lons)

        # Bhava
        bhava = create_comprehensive_bhava_report(
            ascendant=asc_lon,
            planet_positions=natal_lons,
            planet_strengths={p: shadbala_results[p]["percentage"] for p in shadbala_results},
            sarvashtakavarga=sarva_by_house,
            chara_karakas={k: v["planet"] for k, v in jaimini["chara_karakas"].items()},
        )

        # Remedies
        functional_benefics = _functional_benefics(asc_lon)
        current_maha = (
            current_dasha.get("mahadasha", {}).get("planet") if isinstance(current_dasha, dict) else None
        ) or dasha_at_birth["dasha_sequence"][0]["planet"]

        gemstones = recommend_gemstones_for_chart(
            {p: shadbala_results[p]["percentage"] for p in shadbala_results},
            functional_benefics,
            current_maha,
        )

        weak_planets = [p for p in shadbala_results if shadbala_results[p]["percentage"] < 50.0]
        mantra_charity = create_complete_remedial_plan(weak_planets, current_maha)

        # Current transits with Vedha
        transits: Optional[Dict[str, Any]] = None
        if req.include_current_transits:
            transit_snapshot_dt = req.transit_datetime_utc
            current_positions = get_current_transit_positions(
                target_datetime=transit_snapshot_dt,
                ayanamsa_type=req.ayanamsa,
            )
            current_positions_map = (
                current_positions.get("positions", {}) if isinstance(current_positions, dict) else {}
            )
            current_lons = {
                p: float(v["longitude"])
                for p, v in current_positions_map.items()
                if isinstance(v, dict) and "longitude" in v
            }
            gochara = GocharaSystem()
            av_bindus_for_transits = {p: v["bindus"] for p, v in av["individual_ashtakavarga"].items()}
            transits = gochara.analyze_all_transits(
                natal_positions=natal_lons,
                transit_positions=current_lons,
                ascendant=asc_lon,
                ashtakavarga_bindus=av_bindus_for_transits,
            )

        return {
            "birth": {
                "local": birth_local.isoformat(),
                "utc": birth_utc.isoformat(),
                "timezone": req.timezone,
                "latitude": req.latitude,
                "longitude": req.longitude,
                "ayanamsa": req.ayanamsa,
                "house_system": "W",
            },
            "ascendant": {
                "longitude": round(asc_lon, 4),
                "sign": _SIGNS[asc_sign],
                "degree_in_sign": round(asc_lon % 30, 2),
            },
            "planets": {
                p: {
                    "longitude": round(lon, 4),
                    "sign": _SIGNS[int(lon / 30) % 12],
                    "degree_in_sign": round(lon % 30, 2),
                    "house": _planet_house_whole_sign(lon, asc_lon),
                }
                for p, lon in natal_lons.items()
            },
            "ashtakavarga": {
                "sarvashtakavarga_by_sign": sarva_by_sign,
                "sarvashtakavarga_by_house": sarva_by_house,
                "sarvashtakavarga_analysis": av["sarvashtakavarga"],
                "individual": av["individual_ashtakavarga"],
                **({"reductions": av.get("reductions")} if req.include_ashtakavarga_reductions else {}),
            },
            "jaimini": jaimini,
            "vimshottari": {
                "at_birth": {
                    "birth_nakshatra": dasha_at_birth["birth_nakshatra"],
                    "starting_mahadasha": dasha_at_birth["dasha_sequence"][0]["planet"],
                    "balance_fraction": dasha_at_birth["balance_at_birth"],
                },
                "current": {
                    "mahadasha": current_dasha.get("mahadasha"),
                    "antardasha": current_dasha.get("antardasha"),
                },
            },
            "shadbala": shadbala_results,
            "bhava": bhava,
            "transits": transits,
            "remedies": {
                "functional_benefics_used": functional_benefics,
                "current_mahadasha_for_remedies": current_maha,
                "gemstones": {
                    planet: {
                        "primary_gem": rec.primary_gem,
                        "weight_range": rec.weight_range,
                        "metal": rec.metal,
                        "finger": rec.finger,
                        "day": rec.day,
                        "time": rec.time,
                        "mantra": rec.mantra,
                        "mantra_count": rec.mantra_count,
                        "purification_procedure": rec.purification_procedure,
                        "wearing_procedure": rec.wearing_procedure,
                        "effects": rec.effects,
                        "contraindications": rec.contraindications,
                        "reference": rec.reference,
                    }
                    for planet, rec in gemstones.items()
                },
                "mantra_charity": mantra_charity,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
