"""Debug and Verification API endpoints."""

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.core.calculations.birth_rectification import rectify_birth_time
from app.core.calculations.sahamas import calculate_sahamas
from app.core.calculations.critical_points import analyze_all_critical_points
from app.core.calculations.latta_system import analyze_latta
from app.core.calculations.transit_search import search_transits
from app.core.calculations.numerology import calculate_numerology
from app.core.calculations.extended_dashas import calculate_all_extended_dashas
from app.core.calculations.jaimini_dashas import calculate_all_jaimini_dashas
from app.core.calculations.extended_chakras import calculate_all_chakras
from app.core.calculations.prashna import analyze_prashna_chart
from app.core.calculations.advanced_dashas import AdvancedDashaCalculator
from app.core.calculations.advanced_divisional import AdvancedDivisionalCalculator
from app.core.calculations.complete_yogas import calculate_complete_yogas
from app.core.calculations.dasa_pravesh import calculate_dasa_pravesh
from app.core.calculations.tajaka_system import calculate_tajaka_annual
from app.core.calculations.mundane_astrology import calculate_mundane_chart
from app.core.calculations.chart_superimposition import ChartSuperimposition
from app.core.calculations.additional_chakras import calculate_additional_chakras
from app.core.calculations.panchang import PanchangCalculator
from app.core.calculations.compatibility import calculate_compatibility


router = APIRouter()


BIRTH_DATA = {
    "year": 1990,
    "month": 10,
    "day": 9,
    "hour": 9,
    "minute": 10,
    "latitude": 44.5333,
    "longitude": 19.2261,
}

SAMPLE_PLANETS = {
    "Sun": 171.8,
    "Moon": 314.3,
    "Mars": 44.3,
    "Mercury": 178.3,
    "Jupiter": 93.3,
    "Venus": 145.3,
    "Saturn": 265.3,
    "Rahu": 286.3,
    "Ketu": 106.3,
}

SAMPLE_ASCENDANT = 200.0


def _ok(data: Any) -> Dict[str, Any]:
    return {"status": "pass", "data": data}


def _err(error: Exception) -> Dict[str, Any]:
    return {"status": "fail", "error": str(error)}


@router.get("/verify")
async def debug_verify() -> Dict[str, Any]:
    """Run a consolidated verification of major calculation modules."""
    results: Dict[str, Any] = {}

    # Birth datetime
    birth_dt = datetime(
        BIRTH_DATA["year"],
        BIRTH_DATA["month"],
        BIRTH_DATA["day"],
        BIRTH_DATA["hour"],
        BIRTH_DATA["minute"],
    )

    # 1) Panchang
    try:
        panchang_calc = PanchangCalculator()
        panchang = panchang_calc.calculate_panchang(
            birth_dt,
            SAMPLE_PLANETS["Sun"],
            SAMPLE_PLANETS["Moon"],
            BIRTH_DATA["latitude"],
            BIRTH_DATA["longitude"],
        )
        results["panchang"] = _ok(
            {
                "weekday": panchang.weekday,
                "tithi": panchang.tithi,
                "nakshatra": panchang.nakshatra,
                "yoga": panchang.yoga,
            }
        )
    except Exception as e:
        results["panchang"] = _err(e)

    # 2) Compatibility
    try:
        comp = calculate_compatibility(boy_moon_lon=315.0, girl_moon_lon=45.0)
        results["compatibility"] = _ok(
            {
                "total_score": comp["total_score"],
                "percentage": comp["percentage"],
                "recommendation": comp["recommendation"],
            }
        )
    except Exception as e:
        results["compatibility"] = _err(e)

    # 3) Birth Rectification
    try:
        from app.core.calculations.birth_rectification import BirthTimeRectifier

        rectifier = BirthTimeRectifier()
        rect = rectifier.full_rectification(
            approximate_time=birth_dt,
            birth_date=birth_dt.date(),
            latitude=BIRTH_DATA["latitude"],
            longitude=BIRTH_DATA["longitude"],
            moon_longitude=SAMPLE_PLANETS["Moon"],
            ascendant=SAMPLE_ASCENDANT,
        )
        results["birth_rectification"] = _ok(
            {
                "recommended_time": rect["recommended_time"].isoformat()
                if rect.get("recommended_time")
                else None,
                "overall_confidence": rect.get("overall_confidence"),
                "methods": list(rect.get("methods", {}).keys()),
            }
        )
    except Exception as e:
        results["birth_rectification"] = _err(e)

    # 4) Sahamas
    try:
        sah = calculate_sahamas(
            planets=SAMPLE_PLANETS,
            ascendant=SAMPLE_ASCENDANT,
            sun_longitude=SAMPLE_PLANETS["Sun"],
        )
        results["sahamas"] = _ok(
            {
                "total_count": sah.get("total_count"),
                "is_day_birth": sah.get("is_day_birth"),
                "key_sahamas": sah.get("key_sahamas"),
            }
        )
    except Exception as e:
        results["sahamas"] = _err(e)

    # 5) Critical Points (Mrityu Bhaga, 64th Navamsa, etc.)
    try:
        crit = analyze_all_critical_points(SAMPLE_PLANETS, SAMPLE_PLANETS["Moon"])
        results["critical_points"] = _ok(
            {
                "summary": crit.get("summary"),
                "mrityu_bhaga": crit["mrityu_bhaga"].get("afflicted_planets"),
                "navamsa_64th": crit.get("64th_navamsa"),
                "drekkana_22nd": crit.get("22nd_drekkana"),
            }
        )
    except Exception as e:
        results["critical_points"] = _err(e)

    # 6) Latta System
    try:
        latta = analyze_latta(SAMPLE_PLANETS, SAMPLE_PLANETS["Moon"])
        results["latta_system"] = _ok(latta)
    except Exception as e:
        results["latta_system"] = _err(e)

    # 7) Transit Search
    try:
        transit_planets = {k: (v + 30) % 360 for k, v in SAMPLE_PLANETS.items()}
        transits = search_transits(
            natal_planets=SAMPLE_PLANETS,
            transit_planets=transit_planets,
            natal_ascendant=SAMPLE_ASCENDANT,
            search_type="major",
            days_ahead=365,
        )
        results["transit_search"] = _ok(
            {
                "total_events": transits.get("total_events"),
                "sample_event": (transits.get("events") or [None])[0],
            }
        )
    except Exception as e:
        results["transit_search"] = _err(e)

    # 8) Numerology
    try:
        numer = calculate_numerology("Test User", 9, 10, 1990)
        results["numerology"] = _ok(
            {
                "birth_number": numer["birth_number"],
                "destiny_number": numer["destiny_number"],
                "name_number": numer["name_number"],
            }
        )
    except Exception as e:
        results["numerology"] = _err(e)

    # 9) Extended Dashas (Phase 3/4)
    try:
        ext = calculate_all_extended_dashas(
            birth_time=birth_dt,
            moon_longitude=SAMPLE_PLANETS["Moon"],
            sun_longitude=SAMPLE_PLANETS["Sun"],
            ascendant=SAMPLE_ASCENDANT,
            planets=SAMPLE_PLANETS,
        )
        results["extended_dashas"] = _ok({"systems": list(ext.keys())})
    except Exception as e:
        results["extended_dashas"] = _err(e)

    # 10) Jaimini Dashas
    try:
        jai = calculate_all_jaimini_dashas(
            birth_time=birth_dt,
            ascendant=SAMPLE_ASCENDANT,
            planets=SAMPLE_PLANETS,
            sree_lagna=210.0,
        )
        results["jaimini_dashas"] = _ok({"systems": list(jai.keys())})
    except Exception as e:
        results["jaimini_dashas"] = _err(e)

    # 11) Chakras
    try:
        chak = calculate_all_chakras(
            sun_longitude=SAMPLE_PLANETS["Sun"],
            moon_longitude=SAMPLE_PLANETS["Moon"],
            ascendant=SAMPLE_ASCENDANT,
            planets=SAMPLE_PLANETS,
        )
        results["chakras"] = _ok({"systems": list(chak.keys())})
    except Exception as e:
        results["chakras"] = _err(e)

    # 12) Prashna
    try:
        prashna = analyze_prashna_chart(
            question_time=datetime.now(),
            latitude=BIRTH_DATA["latitude"],
            longitude=BIRTH_DATA["longitude"],
            question_type="career",
            planets=SAMPLE_PLANETS,
            ascendant=SAMPLE_ASCENDANT,
        )
        results["prashna"] = _ok(
            {
                "question_category": prashna.get("question_category"),
                "prashna_lagna": prashna.get("prashna_lagna"),
                "favorable": prashna.get("favorable"),
            }
        )
    except Exception as e:
        results["prashna"] = _err(e)

    # 13) Advanced Dashas
    try:
        adv_d = AdvancedDashaCalculator()
        adv_res = adv_d.calculate_all(
            birth_time=birth_dt,
            ascendant=SAMPLE_ASCENDANT,
            planets=SAMPLE_PLANETS,
        )
        results["advanced_dashas"] = _ok({"systems": list(adv_res.keys())})
    except Exception as e:
        results["advanced_dashas"] = _err(e)

    # 14) Advanced Divisional
    try:
        adv_div = AdvancedDivisionalCalculator()
        advd = adv_div.calculate_all(SAMPLE_PLANETS)
        results["advanced_divisional"] = _ok(
            {
                "d81_sun": advd["d81_cyclical"]["Sun"].sign_name,
                "d108_sun": advd["d108_cyclical"]["Sun"].sign_name,
                "d144_sun": advd["d144"]["Sun"].sign_name,
            }
        )
    except Exception as e:
        results["advanced_divisional"] = _err(e)

    # 15) Complete Yogas
    try:
        yogas = calculate_complete_yogas(SAMPLE_PLANETS, SAMPLE_ASCENDANT)
        results["complete_yogas"] = _ok(
            {
                "total_checked": yogas.get("total_checked"),
                "total_found": yogas.get("total_found"),
                "summary": yogas.get("summary"),
            }
        )
    except Exception as e:
        results["complete_yogas"] = _err(e)

    # 16) Dasa Pravesh
    try:
        dasa_start = datetime(1995, 10, 9)
        dp = calculate_dasa_pravesh(
            natal_planets=SAMPLE_PLANETS,
            natal_ascendant=SAMPLE_ASCENDANT,
            dasa_start=dasa_start,
            dasa_lord="Rahu",
        )
        results["dasa_pravesh"] = _ok({"dasa_lord": dp.get("dasa_lord"), "ascendant": dp.get("ascendant")})
    except Exception as e:
        results["dasa_pravesh"] = _err(e)

    # 17) Tajaka Annual
    try:
        tajaka = calculate_tajaka_annual(
            birth_date=birth_dt,
            birth_sun_longitude=SAMPLE_PLANETS["Sun"],
            year_number=35,
        )
        results["tajaka"] = _ok(
            {
                "year_number": tajaka.get("year_number"),
                "muntha": tajaka.get("muntha"),
                "year_lord": tajaka.get("year_lord"),
            }
        )
    except Exception as e:
        results["tajaka"] = _err(e)

    # 18) Mundane Astrology
    try:
        ingress = calculate_mundane_chart("aries_ingress", datetime(2024, 3, 21))
        results["mundane"] = _ok(
            {
                "chart_type": ingress.get("chart_type"),
                "ascendant": ingress.get("ascendant"),
                "government": ingress.get("analysis", {}).get("government"),
            }
        )
    except Exception as e:
        results["mundane"] = _err(e)

    # 19) Chart Superimposition
    try:
        cs = ChartSuperimposition()
        transit = {k: (v + 45) % 360 for k, v in SAMPLE_PLANETS.items()}
        overlay = cs.natal_transit_overlay(SAMPLE_PLANETS, transit, SAMPLE_ASCENDANT)
        results["chart_superimposition"] = _ok(
            {
                "aspect_count": len(overlay.get("aspects", [])),
                "harmony_score": overlay.get("harmony_score"),
            }
        )
    except Exception as e:
        results["chart_superimposition"] = _err(e)

    # 20) Additional Chakras
    try:
        add_ch = calculate_additional_chakras(SAMPLE_PLANETS["Moon"], weekday=2)
        results["additional_chakras"] = _ok(
            {name: {"chakra_name": v["chakra_name"]} for name, v in add_ch.items()}
        )
    except Exception as e:
        results["additional_chakras"] = _err(e)

    # Global summary
    passed = [k for k, v in results.items() if v.get("status") == "pass"]
    failed = [k for k, v in results.items() if v.get("status") == "fail"]

    return {
        "summary": {
            "passed": passed,
            "failed": failed,
            "all_passed": not failed,
        },
        "results": results,
    }
