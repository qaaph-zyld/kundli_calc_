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
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..schemas.source_schema import (
    SourceCitation, SourcedContent, InterpretationSource,
    InterpretationMetadata, ClassicalText, ConfidenceLevel
)
from ..schemas.interpretation_schema import (
    PlanetInHouseInterpretation, PlanetaryDignity,
    InterpretationContext, LifeArea
)
from ..sources.bphs_planets_in_houses import (
    get_planet_in_house_interpretation,
    BPHS_PLANETS_IN_HOUSES
)


class KnowledgeInterpretationEngine:
    """Engine for generating classical text-based interpretations"""
    
    def __init__(self):
        """Initialize the interpretation engine"""
        self.source_priority = [
            ClassicalText.BPHS,
            ClassicalText.SARAVALI,
            ClassicalText.PHALADEEPIKA
        ]
    
    def interpret_planet_in_house(
        self,
        planet: str,
        house: int,
        sign: str,
        dignity: PlanetaryDignity | str,
        additional_context: Optional[Dict[str, Any]] = None
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
            edition="Rajan Publications, 1984"
        )
        
        primary_source = SourcedContent(
            content=bphs_data["translation"],
            citation=primary_citation,
            confidence=ConfidenceLevel.DIRECT_QUOTE,
            original_language=bphs_data.get("original", None),
            notes="Direct translation from BPHS Chapter 24 on planetary effects in houses"
        )
        
        # Build InterpretationSource
        sources = InterpretationSource(
            primary_sources=[primary_source],
            supporting_sources=[],
            synthesis_note=f"Interpretation based on BPHS Ch. 24, verses {bphs_data.get('verses', 'N/A')}"
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
            tags=[
                planet.lower(),
                f"house_{house}",
                sign.lower(),
                dignity.value,
                "classical_text",
                "bphs"
            ]
        )
        
        # Construct detailed effects narrative
        detailed_effects_list = bphs_data.get("detailed_effects", [])
        general_effects = bphs_data["translation"] + "\n\n" + "\n".join(f"• {effect}" for effect in detailed_effects_list)
        
        # Build positive/negative based on dignity
        strong_effects = None
        weak_effects = None
        
        if dignity in [PlanetaryDignity.EXALTED, PlanetaryDignity.OWN_SIGN, PlanetaryDignity.MOOLATRIKONA]:
            if "positive_effects" in bphs_data:
                strong_effects = "When strongly placed:\n" + "\n".join(f"• {e}" for e in bphs_data["positive_effects"])
        
        if dignity == PlanetaryDignity.DEBILITATED or dignity == PlanetaryDignity.ENEMY:
            if "challenging_effects" in bphs_data:
                weak_effects = "When weakly placed or afflicted:\n" + "\n".join(f"• {e}" for e in bphs_data["challenging_effects"])
        
        # Timing notes
        timing_notes = bphs_data.get("timing", f"Effects manifest primarily during {planet} mahadasha and antardasha periods.")
        
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
            metadata=metadata
        )
    
    def synthesize_chart_interpretation(
        self,
        chart_data: Dict[str, Any],
        focus_areas: Optional[List[LifeArea]] = None
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
        raise NotImplementedError("Full chart synthesis coming in Phase 2")
    
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
