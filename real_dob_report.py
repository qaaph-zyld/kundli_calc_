from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Any, List
import sys

import pytz

# Make backend importable
sys.path.insert(0, "backend")

from app.core.astronomical import AstronomicalCalculator as SweCalculator, GeoLocation, AyanamsaSystem, CelestialBody
from app.core.calculations.houses import HouseCalculator
from app.core.calculations.aspects import EnhancedAspectCalculator
from app.core.calculations.dasha_system import VimshottariDasha
from app.core.calculations.shadbala import ShadbalaSystem
from app.core.calculations.transit_analysis import get_current_transit_positions

from app.core.calculations.ashtakavarga_complete import calculate_complete_ashtakavarga
from app.core.calculations.jaimini_complete import calculate_complete_jaimini_analysis
from app.core.calculations.gochara_transits import GocharaSystem
from app.core.analysis.bhava_analysis import create_comprehensive_bhava_report
from app.core.remedies.gemstone_system import recommend_gemstones_for_chart
from app.core.remedies.mantra_charity_system import create_complete_remedial_plan


SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def _rotate_by_asc(sign_list: List[int], asc_lon: float) -> List[int]:
    asc_sign = int(asc_lon / 30) % 12
    return [sign_list[(asc_sign + i) % 12] for i in range(12)]


def _planet_house_whole_sign(planet_lon: float, asc_lon: float) -> int:
    p_sign = int(planet_lon / 30) % 12
    a_sign = int(asc_lon / 30) % 12
    return ((p_sign - a_sign) % 12) + 1


def _functional_benefics(asc_lon: float) -> List[str]:
    # Simplified functional benefics by lordship: strong preference for trine lords.
    # For Scorpio Lagna this yields Moon(9th), Jupiter(5th), Sun(10th) and optionally Mars (lagna lord).
    asc_sign = int(asc_lon / 30) % 12

    # Sign lords
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

    # House->sign from Lagna
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

    # Always include Lagna lord (important for vitality)
    lagna_lord = sign_lords[asc_sign]
    if lagna_lord not in benefics:
        benefics.append(lagna_lord)

    return benefics


def main() -> None:
    # Your birth details
    tz = pytz.timezone("Europe/Belgrade")
    birth_local = tz.localize(datetime(1990, 10, 9, 9, 10, 0))
    birth_utc = birth_local.astimezone(pytz.UTC)
    birth_utc_naive = birth_utc.replace(tzinfo=None)

    latitude = 44.5333
    longitude = 19.2333

    geo = GeoLocation(latitude=latitude, longitude=longitude, altitude=0.0)

    # Core Swiss Ephemeris calculator (sidereal Lahiri)
    swe_calc = SweCalculator(ayanamsa_system=AyanamsaSystem.LAHIRI)

    # Compute planetary positions (sidereal) at birth moment
    positions = swe_calc.calculate_all_positions(birth_utc_naive, geo)

    # Compute sidereal ascendant via HouseCalculator WHOLE_SIGN
    house_calc = HouseCalculator()
    houses = house_calc.calculate_houses(birth_utc_naive, latitude, longitude, "WHOLE_SIGN")
    asc_lon = float(houses["ascendant"])
    asc_sign = int(asc_lon / 30) % 12

    # Build natal longitude map
    natal_lons: Dict[str, float] = {}
    natal_speeds: Dict[str, float] = {}
    for body, pos in positions.items():
        name = body.value.title() if body.value not in ["rahu", "ketu"] else ("Rahu" if body == CelestialBody.RAHU else "Ketu")
        # Keep only classical planets + nodes
        if name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            natal_lons[name] = float(pos.longitude)
            natal_speeds[name] = float(pos.speed)

    # Aspects for shadbala Drik Bala
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

    computed_aspects = aspect_calc.calculate_aspects(aspect_input)
    aspects_by_planet: Dict[str, List[Dict[str, Any]]] = {p: [] for p in aspect_input}
    for a in computed_aspects:
        atype = a.aspect.name.lower()
        aspects_by_planet[a.planet1].append({"type": atype})
        aspects_by_planet[a.planet2].append({"type": atype})

    # Shadbala
    shadbala = ShadbalaSystem()
    is_day = 6 <= birth_local.hour < 18
    shadbala_results: Dict[str, Dict[str, Any]] = {}
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        lon = natal_lons[planet]
        house_num = _planet_house_whole_sign(lon, asc_lon)
        speed = natal_speeds.get(planet, 0.0)
        asp = aspects_by_planet.get(planet, [])
        shadbala_results[planet] = shadbala.calculate_shadbala(planet, house_num, speed, asp, is_day)

    # Vimshottari Dasha at birth
    dasha_calc = VimshottariDasha()
    dasha_at_birth = dasha_calc.calculate_dasha_at_birth(birth_utc_naive, natal_lons["Moon"])
    current_dasha = dasha_calc.get_current_dasha(birth_utc_naive, natal_lons["Moon"], datetime.now(timezone.utc).replace(tzinfo=None))

    # Ashtakavarga (complete)
    av = calculate_complete_ashtakavarga(natal_lons, asc_lon, apply_reductions=True)
    sarva_by_sign = av["sarvashtakavarga"]["bindus_per_house"]
    sarva_by_house = _rotate_by_asc(sarva_by_sign, asc_lon)

    # Jaimini
    jaimini = calculate_complete_jaimini_analysis(birth_utc_naive, asc_lon, natal_lons)

    # Bhava analysis expects sarvashtakavarga in house order
    bhava = create_comprehensive_bhava_report(
        asc_lon,
        natal_lons,
        {p: shadbala_results[p]["percentage"] for p in shadbala_results},
        sarvashtakavarga=sarva_by_house,
        chara_karakas={k: v["planet"] for k, v in jaimini["chara_karakas"].items()},
    )

    # Current transits + Vedha using our GocharaSystem
    current_positions = get_current_transit_positions(ayanamsa_type="lahiri")
    current_positions_map = current_positions.get("positions", {}) if isinstance(current_positions, dict) else {}
    current_lons = {
        p: float(v["longitude"])
        for p, v in current_positions_map.items()
        if isinstance(v, dict) and "longitude" in v
    }

    gochara = GocharaSystem()
    av_bindus_for_transits = {p: v["bindus"] for p, v in av["individual_ashtakavarga"].items()}
    transit_report = gochara.analyze_all_transits(
        natal_positions=natal_lons,
        transit_positions=current_lons,
        ascendant=asc_lon,
        ashtakavarga_bindus=av_bindus_for_transits,
    )

    # Remedies
    functional_benefics = _functional_benefics(asc_lon)
    current_maha = (
        current_dasha.get("mahadasha", {}).get("planet")
        if isinstance(current_dasha, dict)
        else None
    ) or dasha_at_birth["dasha_sequence"][0]["planet"]
    gemstones = recommend_gemstones_for_chart(
        {p: shadbala_results[p]["percentage"] for p in shadbala_results},
        functional_benefics,
        current_maha,
    )
    weak_planets = [p for p in shadbala_results if shadbala_results[p]["percentage"] < 50.0]
    remedies = create_complete_remedial_plan(weak_planets, current_maha)

    # Print REAL DATA
    print("=" * 80)
    print("REAL TRADITIONAL REPORT (Lahiri + Whole Sign)")
    print("Birth local:", birth_local.isoformat())
    print("Birth UTC  :", birth_utc.isoformat())
    print("Location   :", latitude, longitude)
    print("Ascendant  :", round(asc_lon, 4), "in", SIGNS[asc_sign])

    print("\nPLANETS (sidereal longitudes):")
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        lon = natal_lons[p]
        print(f"- {p:8s}: {lon:8.4f}°  {SIGNS[int(lon/30)%12]} {lon%30:05.2f}°  House {_planet_house_whole_sign(lon, asc_lon)}")

    print("\nASHTAKAVARGA (Sarvashtakavarga):")
    print("- By SIGN (Aries..Pisces):", sarva_by_sign)
    print("- By HOUSE from Lagna:", sarva_by_house)

    print("\nJAIMINI (Chara Karakas):")
    for k, v in jaimini["chara_karakas"].items():
        print(f"- {k:15s}: {v['planet']:8s}  {v['sign']}  (Navamsa {v['navamsa_sign']})")

    print("\nVIMSHOTTARI DASHA at birth:")
    print("- Birth Nakshatra:", dasha_at_birth["birth_nakshatra"])
    print("- Starting Mahadasha:", dasha_at_birth["dasha_sequence"][0]["planet"], "balance", round(dasha_at_birth["balance_at_birth"]*100, 2), "%")

    if isinstance(current_dasha, dict) and current_dasha.get("mahadasha"):
        print(
            "- Current Mahadasha:",
            current_dasha["mahadasha"]["planet"],
            "ends",
            str(current_dasha["mahadasha"].get("end"))[:10],
        )
        if current_dasha.get("antardasha"):
            print(
                "- Current Antardasha:",
                current_dasha["antardasha"]["planet"],
                "ends",
                str(current_dasha["antardasha"].get("end"))[:10],
            )

    print("\nSHADBALA (percentage vs minimum):")
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        print(f"- {p:8s}: {shadbala_results[p]['percentage']:6.1f}%  (rupas={shadbala_results[p]['total_rupas']}, min={shadbala_results[p]['minimum_required']})")

    print("\nBHAVA SUMMARY (top/bottom 3 by computed strength):")
    print("- Strongest:", bhava["strongest_houses"])
    print("- Weakest  :", bhava["weakest_houses"])

    print("\nCURRENT TRANSITS (Gochara with Vedha + Ashtakavarga support):")
    print("- Overall:", transit_report["overall_assessment"])

    print("- Debug counts:")
    print("  - current_lons_len:", len(current_lons))
    print("  - current_lons_keys:", sorted(list(current_lons.keys())))
    print("  - gochara_planets:", gochara.planets)
    print("  - transits_from_moon:", len(transit_report.get("transits_from_moon", {})))
    print("  - transits_from_lagna:", len(transit_report.get("transits_from_lagna", {})))
    print("  - key_transits:", len(transit_report.get("key_transits", [])))

    print("- From Moon (per planet):")
    for planet, data in transit_report["transits_from_moon"].items():
        print(
            f"  - {planet:8s}: house={data['house']:2d} strength={data['strength']:13s} "
            f"AV={data.get('ashtakavarga_bindus')} vedha={data.get('has_vedha')} "
            f"vedha_from={data.get('vedha_from')}"
        )

    print("- From Lagna (per planet):")
    for planet, data in transit_report["transits_from_lagna"].items():
        print(
            f"  - {planet:8s}: house={data['house']:2d} strength={data['strength']:13s} "
            f"AV={data.get('ashtakavarga_bindus')} vedha={data.get('has_vedha')} "
            f"vedha_from={data.get('vedha_from')}"
        )

    if transit_report["key_transits"]:
        print("- Key transits:")
        for kt in transit_report["key_transits"][:10]:
            print("  -", kt["planet"], kt["strength"], "|", kt["interpretation"])

    print("\nGEMSTONES (if applicable):")
    for planet, rec in gemstones.items():
        print(f"- {planet}: {rec.primary_gem} | {rec.weight_range} | {rec.metal} | {rec.finger} | {rec.day}")

    print("\nMANTRA/CHARITY (for first 3 planets selected):")
    for planet, plan in remedies["remedial_plans"].items():
        mantra = plan["mantra"]
        charity = plan["charity"]
        fasting = plan["fasting"]
        print(f"- {planet}: mantra_daily={mantra.count_per_day} duration_days={mantra.duration_days} | charity_day={charity.day} | fasting_day={fasting.fasting_day}")


if __name__ == "__main__":
    main()
