#!/usr/bin/env python3
"""
Accuracy Validation Script for Kundli Calculations
Phase 1: Run all charts through calculation engine and log results

Tolerance Standards:
- Planetary longitude: ±0.01° (36 arc-seconds)
- Ayanamsa value: ±0.0001°
- Dasha dates: ±1 day
- Nakshatra pada: Exact match

Usage:
    python validate_accuracy.py
    python validate_accuracy.py --chart chart_016
    python validate_accuracy.py --compare-jhora
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import math

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.core.astronomical.framework import (
    AstronomicalCalculator,
    CelestialBody,
    GeoLocation,
    AyanamsaSystem,
    CoordinateSystem,
)
import swisseph as swe


# Tolerance thresholds (degrees)
TOLERANCE_LONGITUDE = 0.01  # ±0.01° = 36 arc-seconds
TOLERANCE_AYANAMSA = 0.0001  # ±0.0001° = 0.36 arc-seconds
TOLERANCE_DASHA_DAYS = 1  # ±1 day


@dataclass
class ValidationResult:
    """Result of validating a single calculation"""
    planet: str
    calculated: float
    expected: Optional[float]
    deviation: Optional[float]
    within_tolerance: Optional[bool]
    sign_calculated: str
    sign_expected: Optional[str]
    sign_match: Optional[bool]
    nakshatra_calculated: str
    nakshatra_expected: Optional[str]
    nakshatra_match: Optional[bool]


@dataclass
class ChartValidationReport:
    """Complete validation report for a chart"""
    chart_id: str
    chart_name: str
    timestamp: str
    birth_data: Dict[str, Any]
    ayanamsa_value: float
    ayanamsa_expected: Optional[float]
    ayanamsa_deviation: Optional[float]
    lagna_longitude: float
    lagna_sign: str
    planetary_results: List[ValidationResult]
    all_within_tolerance: bool
    has_jhora_reference: bool
    deviations_found: List[str]
    execution_time_ms: float


def get_zodiac_sign(longitude: float) -> str:
    """Get zodiac sign name from longitude"""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return signs[int(longitude / 30)]


def get_nakshatra(longitude: float) -> tuple[str, int]:
    """Get nakshatra name and pada from longitude"""
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigasira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    nakshatra_span = 360 / 27  # 13.333... degrees each
    nakshatra_idx = int(longitude / nakshatra_span)
    pada = int((longitude % nakshatra_span) / (nakshatra_span / 4)) + 1
    return nakshatras[nakshatra_idx], pada


def load_sample_charts() -> List[Dict]:
    """Load all sample charts from fixture file"""
    fixture_path = Path(__file__).parent.parent / "tests" / "fixtures" / "sample_birth_data.json"
    if not fixture_path.exists():
        # Try alternate location
        fixture_path = Path(__file__).parent.parent / "agent_orchestration" / "sample_birth_data.json"
    
    with open(fixture_path) as f:
        data = json.load(f)
    return data["charts"]


def load_jhora_reference(chart_id: str) -> Optional[Dict]:
    """Load JHora reference data if available"""
    ref_dir = Path(__file__).parent.parent / "tests" / "fixtures" / "jhora_reference"
    
    # Try to find matching reference file
    for ref_file in ref_dir.glob("*.json"):
        with open(ref_file) as f:
            ref_data = json.load(f)
        if ref_data.get("birth_data", {}).get("id") == chart_id:
            return ref_data
    
    return None


def calculate_chart(birth_data: Dict) -> Dict[str, Any]:
    """Calculate chart using our engine"""
    # Create calculator with Lahiri ayanamsa (default)
    calc = AstronomicalCalculator(
        coordinate_system=CoordinateSystem.GEOCENTRIC,
        ayanamsa_system=AyanamsaSystem.LAHIRI
    )
    
    # Build datetime
    dt = datetime(
        birth_data["year"],
        birth_data["month"],
        birth_data["day"],
        birth_data["hour"],
        birth_data["minute"],
        birth_data.get("second", 0)
    )
    
    # Adjust for timezone to get UTC
    tz_offset = birth_data.get("timezone_offset", 0)
    from datetime import timedelta
    dt_utc = dt - timedelta(hours=tz_offset)
    
    # Create location
    location = GeoLocation(
        latitude=birth_data["latitude"],
        longitude=birth_data["longitude"],
        altitude=0.0
    )
    
    # Calculate all positions
    positions = calc.calculate_all_positions(dt_utc, location)
    
    # Get ayanamsa value
    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, 
                    dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    
    # Calculate Lagna (Ascendant)
    cusps, ascmc = swe.houses(jd, location.latitude, location.longitude, b"W")  # W = Whole Sign
    lagna_tropical = ascmc[0]
    lagna_sidereal = (lagna_tropical - ayanamsa) % 360
    
    calc.cleanup()
    
    return {
        "positions": positions,
        "ayanamsa": ayanamsa,
        "lagna": lagna_sidereal,
        "julian_day": jd
    }


def validate_chart(chart: Dict, jhora_ref: Optional[Dict] = None) -> ChartValidationReport:
    """Validate a single chart"""
    start_time = datetime.now()
    
    birth_data = chart["birth_data"]
    chart_id = chart.get("id", "unknown")
    chart_name = birth_data.get("name", chart_id)
    
    # Calculate chart
    result = calculate_chart(birth_data)
    positions = result["positions"]
    ayanamsa = result["ayanamsa"]
    lagna = result["lagna"]
    
    # Build planetary results
    planetary_results = []
    deviations_found = []
    all_within_tolerance = True
    
    planet_map = {
        CelestialBody.SUN: "Sun",
        CelestialBody.MOON: "Moon",
        CelestialBody.MARS: "Mars",
        CelestialBody.MERCURY: "Mercury",
        CelestialBody.JUPITER: "Jupiter",
        CelestialBody.VENUS: "Venus",
        CelestialBody.SATURN: "Saturn",
        CelestialBody.RAHU: "Rahu",
        CelestialBody.KETU: "Ketu",
    }
    
    for body, pos in positions.items():
        if body not in planet_map:
            continue
            
        planet_name = planet_map[body]
        calc_lon = pos.longitude
        calc_sign = get_zodiac_sign(calc_lon)
        calc_nak, calc_pada = get_nakshatra(calc_lon)
        
        # Find expected values from JHora reference
        expected_lon = None
        expected_sign = None
        expected_nak = None
        deviation = None
        within_tol = None
        sign_match = None
        nak_match = None
        
        if jhora_ref:
            for p in jhora_ref.get("planetary_positions", []):
                if p.get("planet") == planet_name:
                    expected_lon = p.get("longitude")
                    expected_sign = p.get("sign")
                    expected_nak = p.get("nakshatra")
                    
                    if expected_lon is not None:
                        deviation = abs(calc_lon - expected_lon)
                        # Handle wrap-around at 360°
                        if deviation > 180:
                            deviation = 360 - deviation
                        within_tol = deviation <= TOLERANCE_LONGITUDE
                        if not within_tol:
                            all_within_tolerance = False
                            deviations_found.append(
                                f"{planet_name}: {deviation:.4f}° deviation (expected {expected_lon:.4f}°, got {calc_lon:.4f}°)"
                            )
                    
                    sign_match = calc_sign == expected_sign if expected_sign else None
                    nak_match = calc_nak == expected_nak if expected_nak else None
                    
                    if sign_match is False:
                        deviations_found.append(f"{planet_name}: Sign mismatch (expected {expected_sign}, got {calc_sign})")
                    if nak_match is False:
                        deviations_found.append(f"{planet_name}: Nakshatra mismatch (expected {expected_nak}, got {calc_nak})")
                    break
        
        planetary_results.append(ValidationResult(
            planet=planet_name,
            calculated=round(calc_lon, 6),
            expected=round(expected_lon, 6) if expected_lon else None,
            deviation=round(deviation, 6) if deviation else None,
            within_tolerance=within_tol,
            sign_calculated=calc_sign,
            sign_expected=expected_sign,
            sign_match=sign_match,
            nakshatra_calculated=calc_nak,
            nakshatra_expected=expected_nak,
            nakshatra_match=nak_match,
        ))
    
    # Check ayanamsa
    ayanamsa_expected = None
    ayanamsa_deviation = None
    if jhora_ref:
        ayanamsa_expected = jhora_ref.get("settings", {}).get("ayanamsa_value")
        if ayanamsa_expected:
            ayanamsa_deviation = abs(ayanamsa - ayanamsa_expected)
            if ayanamsa_deviation > TOLERANCE_AYANAMSA:
                deviations_found.append(
                    f"Ayanamsa: {ayanamsa_deviation:.6f}° deviation (expected {ayanamsa_expected:.6f}°, got {ayanamsa:.6f}°)"
                )
    
    execution_time = (datetime.now() - start_time).total_seconds() * 1000
    
    return ChartValidationReport(
        chart_id=chart_id,
        chart_name=chart_name,
        timestamp=datetime.now().isoformat(),
        birth_data=birth_data,
        ayanamsa_value=round(ayanamsa, 6),
        ayanamsa_expected=round(ayanamsa_expected, 6) if ayanamsa_expected else None,
        ayanamsa_deviation=round(ayanamsa_deviation, 6) if ayanamsa_deviation else None,
        lagna_longitude=round(lagna, 6),
        lagna_sign=get_zodiac_sign(lagna),
        planetary_results=planetary_results,
        all_within_tolerance=all_within_tolerance if jhora_ref else True,
        has_jhora_reference=jhora_ref is not None,
        deviations_found=deviations_found,
        execution_time_ms=round(execution_time, 2),
    )


def run_all_validations(output_file: str = None) -> Dict:
    """Run validation on all charts"""
    print("=" * 70)
    print("KUNDLI CALCULATION ACCURACY VALIDATION")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Tolerance: ±{TOLERANCE_LONGITUDE}° for planetary positions")
    print("=" * 70)
    print()
    
    # Load all charts
    charts = load_sample_charts()
    
    # Add user's JHora reference chart
    user_ref = load_jhora_reference("chart_016")
    if user_ref:
        charts.append({
            "id": "chart_016",
            "category": "reference",
            "description": "User's JHora reference - Nikola Jelacic",
            "birth_data": user_ref["birth_data"]
        })
    
    print(f"Total charts to validate: {len(charts)}")
    print()
    
    results = []
    passed = 0
    failed = 0
    no_reference = 0
    
    for chart in charts:
        chart_id = chart.get("id", "unknown")
        print(f"Processing {chart_id}...", end=" ")
        
        # Load JHora reference if available
        jhora_ref = load_jhora_reference(chart_id)
        
        # Validate
        report = validate_chart(chart, jhora_ref)
        results.append(asdict(report))
        
        # Status
        if not report.has_jhora_reference:
            print(f"✓ Calculated ({report.execution_time_ms:.0f}ms) [No JHora reference]")
            no_reference += 1
        elif report.all_within_tolerance:
            print(f"✓ PASSED ({report.execution_time_ms:.0f}ms)")
            passed += 1
        else:
            print(f"✗ DEVIATIONS FOUND ({report.execution_time_ms:.0f}ms)")
            failed += 1
            for dev in report.deviations_found:
                print(f"    - {dev}")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total charts:      {len(charts)}")
    print(f"With JHora ref:    {passed + failed}")
    print(f"  Passed:          {passed}")
    print(f"  Failed:          {failed}")
    print(f"No reference:      {no_reference}")
    print()
    
    # Create output
    output = {
        "validation_run": {
            "timestamp": datetime.now().isoformat(),
            "tolerance_longitude": TOLERANCE_LONGITUDE,
            "tolerance_ayanamsa": TOLERANCE_AYANAMSA,
            "total_charts": len(charts),
            "passed": passed,
            "failed": failed,
            "no_reference": no_reference,
        },
        "results": results,
    }
    
    # Save to file
    if output_file is None:
        output_file = Path(__file__).parent.parent / "tests" / "fixtures" / "validation_results.json"
    
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"Results saved to: {output_file}")
    print()
    
    # Print detailed results for chart_016 (user's reference)
    for r in results:
        if r["chart_id"] == "chart_016":
            print("=" * 70)
            print("DETAILED RESULTS: chart_016 (User's JHora Reference)")
            print("=" * 70)
            print(f"Name: {r['chart_name']}")
            print(f"Ayanamsa: {r['ayanamsa_value']}° (expected: {r['ayanamsa_expected']}°)")
            print(f"Lagna: {r['lagna_longitude']}° in {r['lagna_sign']}")
            print()
            print("Planetary Positions:")
            print("-" * 70)
            print(f"{'Planet':<10} {'Calculated':<12} {'Expected':<12} {'Deviation':<10} {'Status':<8}")
            print("-" * 70)
            for p in r["planetary_results"]:
                exp = f"{p['expected']:.4f}" if p["expected"] else "N/A"
                dev = f"{p['deviation']:.4f}" if p["deviation"] else "N/A"
                status = "✓" if p["within_tolerance"] else ("✗" if p["within_tolerance"] is False else "-")
                print(f"{p['planet']:<10} {p['calculated']:<12.4f} {exp:<12} {dev:<10} {status:<8}")
            print()
            break
    
    return output


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Kundli calculation accuracy")
    parser.add_argument("--chart", help="Validate specific chart ID")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--compare-jhora", action="store_true", help="Only compare charts with JHora reference")
    
    args = parser.parse_args()
    
    if args.chart:
        # Validate single chart
        charts = load_sample_charts()
        chart = next((c for c in charts if c.get("id") == args.chart), None)
        
        if not chart:
            # Check if it's the user's reference chart
            ref = load_jhora_reference(args.chart)
            if ref:
                chart = {
                    "id": args.chart,
                    "birth_data": ref["birth_data"]
                }
        
        if not chart:
            print(f"Chart {args.chart} not found")
            sys.exit(1)
        
        jhora_ref = load_jhora_reference(args.chart)
        report = validate_chart(chart, jhora_ref)
        print(json.dumps(asdict(report), indent=2, default=str))
    else:
        # Run all validations
        run_all_validations(args.output)


if __name__ == "__main__":
    main()
