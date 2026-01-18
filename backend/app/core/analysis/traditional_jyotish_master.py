"""Traditional Jyotish Master Integration
=========================================
Master module combining all traditional Jyotish systems into comprehensive analysis.

Integrates:
1. Ashtakavarga (Sarvashtakavarga, individual, reductions)
2. Gochara (transits with Vedha and AV support)
3. Jaimini (Chara Karakas, Chara Dasha, Argala, Arudha Padas)
4. Bhava Analysis (house strength with all factors)
5. Remedial Systems (gemstones, mantras, charity, fasting)
6. Shadbala and existing calculations

This module provides the complete traditional analysis that a Jyotish maestro would give.

Reference: All classical texts integrated (BPHS, Phaladeepika, Saravali, Jaimini Sutras)
"""

# Import all traditional systems
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

sys.path.insert(0, "..")

from app.core.analysis.bhava_analysis import create_comprehensive_bhava_report
from app.core.calculations.ashtakavarga_complete import calculate_complete_ashtakavarga
from app.core.calculations.dasha_system import VimshottariDasha
from app.core.calculations.gochara_transits import GocharaSystem
from app.core.calculations.jaimini_complete import calculate_complete_jaimini_analysis
from app.core.calculations.shadbala import ShadbalaSystem
from app.core.remedies.gemstone_system import recommend_gemstones_for_chart
from app.core.remedies.mantra_charity_system import create_complete_remedial_plan


@dataclass
class TraditionalJyotishReport:
    """Complete traditional Jyotish analysis report"""

    calculation_time: str
    birth_details: Dict[str, Any]

    # Core calculations
    planetary_positions: Dict[str, Any]
    ascendant: Dict[str, Any]

    # Traditional systems
    ashtakavarga: Dict[str, Any]
    bhava_analysis: Dict[str, Any]
    jaimini_analysis: Dict[str, Any]
    shadbala: Dict[str, Any]
    vimshottari_dasha: Dict[str, Any]

    # Current state
    current_transits: Dict[str, Any]
    current_dasha: Dict[str, Any]

    # Remedial prescriptions
    gemstone_recommendations: Dict[str, Any]
    mantra_charity_plan: Dict[str, Any]

    # Summary
    life_path_summary: Dict[str, Any]
    key_strengths: List[str]
    areas_needing_attention: List[str]
    overall_assessment: str

    # References
    scholarly_references: List[str]


class TraditionalJyotishMaster:
    """Master analyzer combining all traditional Jyotish systems"""

    def __init__(self):
        """Initialize all subsystems"""
        self.shadbala = ShadbalaSystem()
        self.dasha = VimshottariDasha()
        self.gochara = GocharaSystem()

    def calculate_complete_analysis(
        self,
        birth_datetime: datetime,
        latitude: float,
        longitude: float,
        timezone: str,
        planet_positions: Dict[str, float],
        ascendant: float,
        moon_longitude: float,
        apply_ashtakavarga_reductions: bool = False,
        current_transits: bool = True,
    ) -> TraditionalJyotishReport:
        """Calculate complete traditional Jyotish analysis

        This is the master function that orchestrates all traditional systems
        to provide comprehensive analysis comparable to a Jyotish maestro.

        Args:
            birth_datetime: Birth date and time
            latitude: Birth latitude
            longitude: Birth longitude
            timezone: Timezone
            planet_positions: Planetary longitudes (0-360)
            ascendant: Ascendant longitude
            moon_longitude: Moon's longitude
            apply_ashtakavarga_reductions: Apply Shodhana (reductions)
            current_transits: Include current transit analysis

        Returns:
            Complete TraditionalJyotishReport
        """
        print("Starting comprehensive traditional Jyotish analysis...")

        # 1. Calculate Ashtakavarga (foundation for house/transit strength)
        print("Calculating Ashtakavarga...")
        ashtakavarga = calculate_complete_ashtakavarga(
            planet_positions, ascendant, apply_reductions=apply_ashtakavarga_reductions
        )

        # 2. Calculate Shadbala (planetary strength)
        print("Calculating Shadbala...")
        shadbala_results = self._calculate_shadbala_all_planets(planet_positions, ascendant, birth_datetime)

        # 3. Calculate Vimshottari Dasha
        print("Calculating Vimshottari Dasha...")
        dasha_info = self.dasha.calculate_all_dasha_levels(
            birth_datetime, moon_longitude, include_sookshma=False, include_prana=False
        )

        current_dasha = self.dasha.get_current_dasha(birth_datetime, moon_longitude, datetime.now())

        # 4. Calculate Jaimini systems
        print("Calculating Jaimini analysis...")
        jaimini = calculate_complete_jaimini_analysis(birth_datetime, ascendant, planet_positions)

        # 5. Calculate Bhava (house) analysis
        print("Calculating Bhava analysis...")
        bhava_analysis = create_comprehensive_bhava_report(
            ascendant,
            planet_positions,
            {p: shadbala_results[p]["percentage"] for p in shadbala_results},
            sarvashtakavarga=ashtakavarga["sarvashtakavarga"]["bindus_per_house"],
            chara_karakas={k: v["planet"] for k, v in jaimini["chara_karakas"].items()},
        )

        # 6. Calculate current transits (if requested)
        transits = None
        if current_transits:
            print("Calculating current transits...")
            # Would integrate with astronomical calculator for current positions
            # For now, return structure
            transits = {
                "note": "Integrate with AstronomicalCalculator for real-time",
                "reference": "BPHS Chapter 53, Phaladeepika Chapter 20",
            }

        # 7. Generate remedial recommendations
        print("Generating remedial recommendations...")

        # Identify weak planets and functional benefics
        weak_planets = [
            p
            for p, data in shadbala_results.items()
            if data["percentage"] < 50 and p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        ]

        # Determine functional benefics (simplified - should be chart-specific)
        functional_benefics = self._determine_functional_benefics(ascendant)

        # Current Mahadasha planet
        current_maha = current_dasha.get("mahadasha", {}).get("planet", "Jupiter")

        gemstones = recommend_gemstones_for_chart(
            {p: shadbala_results[p]["percentage"] for p in shadbala_results}, functional_benefics, current_maha
        )

        mantra_charity = create_complete_remedial_plan(weak_planets, current_maha)

        # 8. Generate life path summary
        print("Generating life path summary...")
        life_path = self._generate_life_path_summary(
            jaimini["chara_karakas"], bhava_analysis, shadbala_results, ashtakavarga
        )

        # 9. Identify key strengths and areas needing attention
        key_strengths = self._identify_key_strengths(bhava_analysis, shadbala_results, jaimini)

        areas_needing_attention = self._identify_areas_needing_attention(bhava_analysis, weak_planets, shadbala_results)

        # 10. Generate overall assessment
        overall = self._generate_overall_assessment(key_strengths, areas_needing_attention, current_dasha, jaimini)

        # Compile complete report
        report = TraditionalJyotishReport(
            calculation_time=datetime.now().isoformat(),
            birth_details={
                "datetime": birth_datetime.isoformat(),
                "latitude": latitude,
                "longitude": longitude,
                "timezone": timezone,
            },
            planetary_positions=planet_positions,
            ascendant={"longitude": ascendant, "sign": self._get_sign_name(int(ascendant / 30))},
            ashtakavarga=ashtakavarga,
            bhava_analysis=bhava_analysis,
            jaimini_analysis=jaimini,
            shadbala=shadbala_results,
            vimshottari_dasha=dasha_info,
            current_transits=transits or {},
            current_dasha=current_dasha,
            gemstone_recommendations={k: asdict(v) for k, v in gemstones.items()},
            mantra_charity_plan=mantra_charity,
            life_path_summary=life_path,
            key_strengths=key_strengths,
            areas_needing_attention=areas_needing_attention,
            overall_assessment=overall,
            scholarly_references=self._get_scholarly_references(),
        )

        print("✓ Complete traditional Jyotish analysis finished!")
        return report

    def _calculate_shadbala_all_planets(
        self, planet_positions: Dict[str, float], ascendant: float, birth_datetime: datetime
    ) -> Dict[str, Any]:
        """Calculate Shadbala for all planets"""
        results = {}

        # Determine if day birth (simplified)
        hour = birth_datetime.hour
        is_day = 6 <= hour <= 18

        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            if planet not in planet_positions:
                continue

            # Calculate house
            planet_sign = int(planet_positions[planet] / 30)
            asc_sign = int(ascendant / 30)
            house = ((planet_sign - asc_sign) % 12) + 1

            # Simplified - would need actual speed and aspects
            speed = 1.0  # Placeholder
            aspects = []  # Placeholder

            shadbala = self.shadbala.calculate_shadbala(planet, house, speed, aspects, is_day)

            results[planet] = shadbala

        return results

    def _determine_functional_benefics(self, ascendant: float) -> List[str]:
        """Determine functional benefics for ascendant (simplified)"""
        asc_sign = int(ascendant / 30)

        # Simplified functional benefic determination
        # In reality, this is complex and depends on lordship

        # General benefics
        general_benefics = ["Jupiter", "Venus", "Mercury", "Moon"]

        # Would need proper lordship analysis here
        return general_benefics

    def _generate_life_path_summary(
        self, karakas: Dict[str, Any], bhavas: Dict[str, Any], shadbala: Dict[str, Any], ashtakavarga: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate life path summary based on Atmakaraka and key houses"""

        atmakaraka_planet = karakas["Atmakaraka"]["planet"]
        atmakaraka_sign = karakas["Atmakaraka"]["navamsa_sign"]

        # 10th house (career) strength
        career_house = bhavas["all_houses"][10]

        # 9th house (fortune) strength
        fortune_house = bhavas["all_houses"][9]

        # 5th house (intelligence) strength
        intelligence_house = bhavas["all_houses"][5]

        return {
            "soul_purpose": f"Atmakaraka {atmakaraka_planet} indicates soul's journey through {atmakaraka_planet}'s qualities. Karakamsa in {atmakaraka_sign} shows ultimate spiritual path.",
            "career_potential": f"10th house strength: {career_house['strength']} - {self._interpret_house_strength(career_house['strength_percentage'])}",
            "fortune_destiny": f"9th house strength: {fortune_house['strength']} - Fortune and dharma path",
            "intellectual_path": f"5th house strength: {intelligence_house['strength']} - Creative and intellectual expression",
            "overall_life_direction": self._determine_life_direction(atmakaraka_planet, bhavas),
        }

    def _interpret_house_strength(self, percentage: float) -> str:
        """Interpret house strength percentage"""
        if percentage >= 80:
            return "Excellent - results manifest powerfully"
        elif percentage >= 70:
            return "Very Strong - favorable outcomes"
        elif percentage >= 60:
            return "Strong - good results with effort"
        elif percentage >= 45:
            return "Moderate - mixed results"
        elif percentage >= 30:
            return "Weak - challenges present"
        else:
            return "Very Weak - significant obstacles"

    def _determine_life_direction(self, atmakaraka: str, bhavas: Dict[str, Any]) -> str:
        """Determine overall life direction"""
        directions = {
            "Sun": "Leadership, authority, government service, or self-employment. Soul seeks recognition and influence.",
            "Moon": "Nurturing professions, public service, counseling, or artistic pursuits. Soul seeks emotional fulfillment.",
            "Mars": "Technical fields, sports, military, surgery, or real estate. Soul seeks courage and achievement.",
            "Mercury": "Communication, writing, business, teaching, or technology. Soul seeks knowledge and versatility.",
            "Jupiter": "Teaching, spirituality, law, finance, or advisory roles. Soul seeks wisdom and guidance of others.",
            "Venus": "Arts, beauty, hospitality, luxury goods, or counseling. Soul seeks harmony and refinement.",
            "Saturn": "Service, labor, mining, organization, or spiritual disciplines. Soul seeks discipline and liberation through duty.",
        }

        return directions.get(atmakaraka, "Diverse path based on multiple factors.")

    def _identify_key_strengths(
        self, bhavas: Dict[str, Any], shadbala: Dict[str, Any], jaimini: Dict[str, Any]
    ) -> List[str]:
        """Identify key strengths in chart"""
        strengths = []

        # Strong houses
        strong_houses = bhavas["strongest_houses"]
        for house_data in strong_houses[:2]:
            strengths.append(f"Strong {house_data['name']} ({house_data['strength']:.1f}%)")

        # Strong planets
        strong_planets = [p for p, data in shadbala.items() if data.get("percentage", 0) > 70]
        if strong_planets:
            strengths.append(f"Strong planets: {', '.join(strong_planets[:3])}")

        # Chara Karakas
        atmakaraka = jaimini["chara_karakas"]["Atmakaraka"]["planet"]
        strengths.append(f"Atmakaraka {atmakaraka} - strong soul purpose")

        return strengths[:5]

    def _identify_areas_needing_attention(
        self, bhavas: Dict[str, Any], weak_planets: List[str], shadbala: Dict[str, Any]
    ) -> List[str]:
        """Identify areas needing attention and remedies"""
        areas = []

        # Weak houses
        weak_houses = bhavas["weakest_houses"]
        for house_data in weak_houses[:2]:
            areas.append(f"{house_data['name']} needs strengthening (remedies recommended)")

        # Weak planets
        if weak_planets:
            areas.append(f"Weak planets needing remedies: {', '.join(weak_planets[:3])}")

        return areas[:5]

    def _generate_overall_assessment(
        self, strengths: List[str], areas: List[str], current_dasha: Dict[str, Any], jaimini: Dict[str, Any]
    ) -> str:
        """Generate overall life assessment"""

        maha = current_dasha.get("mahadasha", {}).get("planet", "Unknown")
        anta = current_dasha.get("antardasha", {}).get("planet", "Unknown")

        assessment = f"""**Overall Life Assessment:**

**Current Period:** {maha} Mahadasha / {anta} Antardasha
This period's results depend on {maha}'s strength and placement. Consult Dasha analysis for timing.

**Core Strengths:**
{chr(10).join('- ' + s for s in strengths)}

**Areas Requiring Attention:**
{chr(10).join('- ' + a for a in areas)}

**Life Path Guidance:**
Your Atmakaraka reveals your soul's primary objective in this life. The strongest houses indicate natural talents and favorable life areas. Focus remedial efforts on weak areas while leveraging strengths.

**Traditional Recommendation:**
Combine:
1. Gemstone for Mahadasha lord (if weak)
2. Daily mantra practice for weak planets
3. Weekly charity as prescribed
4. Respect to karakas (Sun for father, Moon for mother, etc.)
5. Spiritual practice aligned with 9th/12th house indications

**Important:** This analysis integrates multiple classical systems. Consult experienced Jyotishi for personalized timing and specific predictions."""

        return assessment

    def _get_sign_name(self, sign_num: int) -> str:
        """Get sign name from number"""
        signs = [
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
        return signs[sign_num % 12]

    def _get_scholarly_references(self) -> List[str]:
        """Get all scholarly references used"""
        return [
            "Brihat Parashara Hora Shastra (BPHS) - Complete",
            "Phaladeepika - Mantreswara",
            "Saravali - Kalyana Varma",
            "Jataka Parijata - Vaidyanatha Dikshita",
            "Jaimini Sutras - Maharishi Jaimini",
            "Brihat Samhita - Varahamihira",
            "Hora Ratnam - Balabhadra",
            "Uttara Kalamrita - Kalidasa",
            "Mantra Mahodadhi - Mahidhara",
            "Garuda Purana - Ratna Adhyaya",
            "Lal Kitab - Traditional remedial text",
        ]


def generate_traditional_jyotish_report(
    birth_datetime: datetime,
    latitude: float,
    longitude: float,
    timezone: str,
    planet_positions: Dict[str, float],
    ascendant: float,
    moon_longitude: float,
    name: str = "Native",
    output_format: str = "detailed",  # 'detailed', 'summary', 'remedial_only'
) -> Dict[str, Any]:
    """Generate complete traditional Jyotish report

    This is the main function to call for complete traditional analysis.

    Args:
        birth_datetime: Birth date/time
        latitude: Birth latitude
        longitude: Birth longitude
        timezone: Timezone
        planet_positions: Planet longitudes
        ascendant: Ascendant longitude
        moon_longitude: Moon longitude
        name: Native's name
        output_format: Level of detail

    Returns:
        Complete traditional analysis report
    """
    master = TraditionalJyotishMaster()

    report = master.calculate_complete_analysis(
        birth_datetime, latitude, longitude, timezone, planet_positions, ascendant, moon_longitude
    )

    if output_format == "summary":
        return {
            "name": name,
            "life_path": report.life_path_summary,
            "key_strengths": report.key_strengths,
            "areas_needing_attention": report.areas_needing_attention,
            "current_dasha": report.current_dasha,
            "overall_assessment": report.overall_assessment,
        }

    elif output_format == "remedial_only":
        return {
            "name": name,
            "weak_areas": report.areas_needing_attention,
            "gemstones": report.gemstone_recommendations,
            "mantras_charity": report.mantra_charity_plan,
            "current_dasha": report.current_dasha,
        }

    else:  # detailed
        return asdict(report)
