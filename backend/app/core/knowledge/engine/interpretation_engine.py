"""
Interpretation Engine
=====================
Core engine for generating source-backed astrological interpretations.

This engine:
1. Takes astrological chart data
2. Queries knowledge base for relevant classical text passages
3. Synthesizes interpretations with full source attribution
4. Returns structured interpretations with citations
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from ..schemas.interpretation_schema import (
    InterpretationContext,
    LifeArea,
    PlanetaryDignity,
    PlanetInHouseInterpretation,
)
from ..schemas.source_schema import (
    ClassicalText,
    ConfidenceLevel,
    InterpretationMetadata,
    InterpretationSource,
    SourceCitation,
    SourcedContent,
)
from ..sources.bphs_planets_in_houses import BPHS_PLANETS_IN_HOUSES, get_planet_in_house_interpretation


class KnowledgeInterpretationEngine:
    """Engine for generating classical text-based interpretations"""

    def __init__(self):
        """Initialize the interpretation engine"""
        self.source_priority = [ClassicalText.BPHS, ClassicalText.SARAVALI, ClassicalText.PHALADEEPIKA]

    def interpret_planet_in_house(
        self,
        planet: str,
        house: int,
        sign: str,
        dignity: PlanetaryDignity | str,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> PlanetInHouseInterpretation:
        """
        Generate interpretation for planet in house placement.

        Args:
            planet: Planet name
            house: House number (1-12)
            sign: Sign name (Aries, Taurus, etc.)
            dignity: Planetary dignity
            additional_context: Optional additional factors

        Returns:
            PlanetInHouseInterpretation with full source attribution
        """
        # Convert dignity to enum if string
        if isinstance(dignity, str):
            dignity = PlanetaryDignity(dignity)

        # Get BPHS interpretation
        bphs_data = get_planet_in_house_interpretation(planet, house)

        if not bphs_data:
            raise ValueError(f"No BPHS interpretation found for {planet} in house {house}")

        # Build source citations
        primary_citation = SourceCitation(
            text=ClassicalText.BPHS,
            chapter=24,
            verses=bphs_data.get("verses", ""),
            translator="R. Santhanam",
            edition="Rajan Publications, 1984",
        )

        primary_source = SourcedContent(
            content=bphs_data["translation"],
            citation=primary_citation,
            confidence=ConfidenceLevel.DIRECT_QUOTE,
            original_language=bphs_data.get("original", None),
            notes="Direct translation from BPHS Chapter 24 on planetary effects in houses",
        )

        # Build InterpretationSource
        sources = InterpretationSource(
            primary_sources=[primary_source],
            supporting_sources=[],
            synthesis_note=f"Interpretation based on BPHS Ch. 24, verses {bphs_data.get('verses', 'N/A')}",
        )

        # Build life area interpretations
        life_areas = {}
        if "life_areas" in bphs_data:
            for area_key, description in bphs_data["life_areas"].items():
                try:
                    life_area_enum = LifeArea(area_key)
                    life_areas[life_area_enum] = description
                except ValueError:
                    # Skip invalid life area keys
                    pass

        # Build metadata
        metadata = InterpretationMetadata(
            interpretation_type="planet_in_house",
            confidence_score=0.95 if bphs_data else 0.5,
            last_updated=datetime.now().isoformat(),
            validator="BPHS Chapter 24",
            tags=[planet.lower(), f"house_{house}", sign.lower(), dignity.value, "classical_text", "bphs"],
        )

        # Construct detailed effects narrative
        detailed_effects_list = bphs_data.get("detailed_effects", [])
        general_effects = (
            bphs_data["translation"] + "\n\n" + "\n".join(f"• {effect}" for effect in detailed_effects_list)
        )

        # Build positive/negative based on dignity
        strong_effects = None
        weak_effects = None

        if dignity in [PlanetaryDignity.EXALTED, PlanetaryDignity.OWN_SIGN, PlanetaryDignity.MOOLATRIKONA]:
            if "positive_effects" in bphs_data:
                strong_effects = "When strongly placed:\n" + "\n".join(f"• {e}" for e in bphs_data["positive_effects"])

        if dignity == PlanetaryDignity.DEBILITATED or dignity == PlanetaryDignity.ENEMY:
            if "challenging_effects" in bphs_data:
                weak_effects = "When weakly placed or afflicted:\n" + "\n".join(
                    f"• {e}" for e in bphs_data["challenging_effects"]
                )

        # Timing notes
        timing_notes = bphs_data.get(
            "timing", f"Effects manifest primarily during {planet} mahadasha and antardasha periods."
        )

        # Notable yogas
        if "notable_yogas" in bphs_data:
            timing_notes += "\n\nYogas: " + ", ".join(bphs_data["notable_yogas"])

        # Remedies
        remedies = bphs_data.get("remedies", [])

        return PlanetInHouseInterpretation(
            planet=planet,
            house=house,
            sign=sign,
            dignity=dignity,
            general_effects=general_effects,
            life_areas=life_areas,
            strong_placement_effects=strong_effects,
            weak_placement_effects=weak_effects,
            timing_notes=timing_notes,
            remedies=remedies,
            sources=sources,
            metadata=metadata,
        )

    def interpret_yoga(
        self, yoga_name: str, detected_in_chart: bool = True, formation_details: Optional[Dict[str, Any]] = None
    ):
        """
        Generate interpretation for a yoga with classical text sources.

        Args:
            yoga_name: Name of the yoga
            detected_in_chart: Whether yoga is actually present
            formation_details: Optional details about how yoga formed

        Returns:
            YogaInterpretation with full source attribution
        """
        from ..schemas.interpretation_schema import YogaInterpretation
        from ..sources.bphs_yogas import get_yoga_interpretation

        yoga_data = get_yoga_interpretation(yoga_name)

        if not yoga_data:
            raise ValueError(f"No BPHS interpretation found for yoga: {yoga_name}")

        # Build source citations
        chapter = yoga_data.get("chapter", 40)
        verses = yoga_data.get("verses", "")

        primary_citation = SourceCitation(
            text=ClassicalText.BPHS,
            chapter=chapter,
            verses=verses,
            translator="R. Santhanam",
            edition="Rajan Publications, 1984",
        )

        primary_source = SourcedContent(
            content=yoga_data.get("classical_description", ""),
            citation=primary_citation,
            confidence=ConfidenceLevel.DIRECT_QUOTE,
            notes=f"Direct interpretation from BPHS Chapter {chapter} on yogas",
        )

        # Build InterpretationSource
        sources = InterpretationSource(
            primary_sources=[primary_source],
            supporting_sources=[],
            synthesis_note=f"Yoga interpretation from BPHS Ch. {chapter}, verses {verses}",
        )

        # Build metadata
        metadata = InterpretationMetadata(
            interpretation_type="yoga",
            confidence_score=0.95,
            last_updated=datetime.now().isoformat(),
            validator=f"BPHS Chapter {chapter}",
            tags=[
                yoga_name.lower().replace("_", "-"),
                yoga_data.get("category", "yoga").lower().replace(" ", "-"),
                "bphs",
                "classical_text",
            ],
        )

        return YogaInterpretation(
            yoga_name=yoga_name,
            category=yoga_data.get("category", "Yoga"),
            formation=yoga_data.get("formation", ""),
            classical_description=yoga_data.get("classical_description", ""),
            planets_involved=yoga_data.get("planets_involved"),
            houses_involved=yoga_data.get("houses_involved"),
            effects=yoga_data.get("effects", {}),
            strength_factors=yoga_data.get("strength_factors"),
            strength_assessment=yoga_data.get("strength_assessment"),
            examples=yoga_data.get("examples"),
            timing=yoga_data.get("timing"),
            cancellation_factors=yoga_data.get("cancellation_factors"),
            special_notes=yoga_data.get("special_notes"),
            modern_interpretation=yoga_data.get("modern_interpretation"),
            sources=sources,
            metadata=metadata,
        )

    def synthesize_chart_interpretation(
        self, chart_data: Dict[str, Any], focus_areas: Optional[List[LifeArea]] = None
    ) -> Dict[str, Any]:
        """
        Synthesize full chart interpretation from multiple factors.

        Args:
            chart_data: Complete chart data
            focus_areas: Optional list of life areas to focus on

        Returns:
            Synthesized interpretation with sources
        """
        # TODO: Implement multi-factor synthesis
        # This will combine:
        # - Planet positions
        # - Yogas
        # - Aspects
        # - Dashas
        # Into coherent narrative
        raise NotImplementedError("Full chart synthesis coming in Phase 3")

    def get_available_interpretations(self) -> Dict[str, List[int]]:
        """
        Get list of available planet-house interpretations.

        Returns:
            Dictionary of planet -> list of houses with interpretations
        """
        available = {}
        for planet, houses in BPHS_PLANETS_IN_HOUSES.items():
            available[planet] = list(houses.keys())
        return available

    def get_available_yogas(self) -> Dict[str, List[str]]:
        """
        Get list of available yogas by category.

        Returns:
            Dictionary of category -> list of yoga names
        """
        from ..sources.bphs_yogas import BPHS_DHANA_YOGAS, BPHS_PANCHA_MAHAPURUSHA_YOGAS, BPHS_RAJA_YOGAS

        return {
            "Raja Yoga": list(BPHS_RAJA_YOGAS.keys()),
            "Wealth Yoga": list(BPHS_DHANA_YOGAS.keys()),
            "Mahapurusha Yoga": list(BPHS_PANCHA_MAHAPURUSHA_YOGAS.keys()),
        }

    def interpret_dasha(
        self, planet: str, dasha_type: str = "Vimshottari", chart_context: Optional[Dict[str, Any]] = None
    ):
        """
        Generate interpretation for planetary dasha period.

        Args:
            planet: Planet whose dasha is running
            dasha_type: Type of dasha system (default: Vimshottari)
            chart_context: Optional chart data for contextualized interpretation

        Returns:
            DashaInterpretation with classical text sources
        """
        from ..schemas.interpretation_schema import DashaInterpretation, LifeArea
        from ..sources.bphs_dasha_effects import get_mahadasha_interpretation

        dasha_data = get_mahadasha_interpretation(planet)

        if not dasha_data:
            raise ValueError(f"No BPHS interpretation found for {planet} mahadasha")

        # Build source citations
        chapter = dasha_data.get("chapter", 47)
        verses = dasha_data.get("verses", "")

        primary_citation = SourceCitation(
            text=ClassicalText.BPHS,
            chapter=chapter,
            verses=verses,
            translator="R. Santhanam",
            edition="Rajan Publications, 1984",
        )

        primary_source = SourcedContent(
            content=dasha_data.get("classical_description", ""),
            citation=primary_citation,
            confidence=ConfidenceLevel.DIRECT_QUOTE,
            notes=f"Direct interpretation from BPHS Chapter {chapter} on Vimshottari Dasha effects",
        )

        # Build InterpretationSource
        sources = InterpretationSource(
            primary_sources=[primary_source],
            supporting_sources=[],
            synthesis_note=f"Dasha interpretation from BPHS Ch. {chapter}, verses {verses}",
        )

        # Build metadata
        metadata = InterpretationMetadata(
            interpretation_type="dasha",
            confidence_score=0.95,
            last_updated=datetime.now().isoformat(),
            validator=f"BPHS Chapter {chapter}",
            tags=[planet.lower(), "mahadasha", dasha_type.lower(), "bphs", "classical_text"],
        )

        # Extract life areas from effects
        life_areas_activated = []
        general_effects = dasha_data.get("general_effects", {})

        # Build general theme
        general_theme = dasha_data.get("classical_description", "")

        # Extract positive and challenging indications
        positive = general_effects.get("positive", [])
        challenging = general_effects.get("challenging", [])

        # Build recommendations from remedies
        recommendations = dasha_data.get("remedies", [])

        return DashaInterpretation(
            planet=planet,
            dasha_type=dasha_type,
            level="Mahadasha",
            general_theme=general_theme,
            life_areas_activated=life_areas_activated,
            positive_indications=positive,
            challenging_indications=challenging,
            effects_by_house_placement=(
                str(dasha_data.get("effects_by_house", {})) if "effects_by_house" in dasha_data else None
            ),
            recommendations=recommendations,
            sources=sources,
            metadata=metadata,
        )
