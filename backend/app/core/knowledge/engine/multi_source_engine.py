"""
Multi-Source Interpretation Engine

This module provides multi-source comparison and synthesis capabilities,
combining interpretations from multiple classical texts (BPHS, Saravali, etc.)
to provide comprehensive, cross-referenced astrological interpretations.

Features:
- Compare interpretations across multiple sources
- Identify agreements and contradictions
- Synthesize combined interpretations
- Track source attribution for all claims
- Provide confidence scores for synthesized results
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from app.core.knowledge.sources.bphs_planets_in_houses import BPHS_PLANETS_IN_HOUSES, get_planet_in_house_interpretation
from app.core.knowledge.sources.hora_sara_planets_in_houses import (
    HORA_SARA_PLANETS_IN_HOUSES,
    get_hora_sara_interpretation,
)
from app.core.knowledge.sources.phaladeepika_planets_in_houses import (
    PHALADEEPIKA_PLANETS_IN_HOUSES,
    get_phaladeepika_interpretation,
)
from app.core.knowledge.sources.saravali_planets_in_houses import (
    SARAVALI_METADATA,
    SARAVALI_PLANETS_IN_HOUSES,
    get_saravali_interpretation,
)


class AgreementLevel(str, Enum):
    """Level of agreement between sources"""

    STRONG_AGREEMENT = "strong_agreement"  # Sources strongly agree
    MODERATE_AGREEMENT = "moderate_agreement"  # Sources generally agree
    NEUTRAL = "neutral"  # No clear agreement or disagreement
    MODERATE_DISAGREEMENT = "moderate_disagreement"  # Some contradictions
    STRONG_DISAGREEMENT = "strong_disagreement"  # Major contradictions


@dataclass
class SourceComparison:
    """Comparison result between multiple sources"""

    planet: str
    house: int
    sources_available: List[str]
    agreement_level: AgreementLevel
    common_themes: List[str]
    unique_insights: Dict[str, List[str]]  # Changed from separate fields per source
    contradictions: List[Dict[str, str]]
    synthesis: str
    confidence_score: float


class MultiSourceEngine:
    """
    Engine for comparing and synthesizing interpretations from multiple sources.

    Capabilities:
    - Compare BPHS and Saravali interpretations
    - Identify agreements and contradictions
    - Synthesize unified interpretations
    - Track source attribution
    """

    def __init__(self):
        """Initialize the multi-source engine with all available sources"""
        self.sources = {
            "BPHS": {
                "data": BPHS_PLANETS_IN_HOUSES,
                "get_func": get_planet_in_house_interpretation,
                "metadata": {"translator": "R. Santhanam", "edition": "1984", "chapter": 24},
            },
            "Saravali": {
                "data": SARAVALI_PLANETS_IN_HOUSES,
                "get_func": get_saravali_interpretation,
                "metadata": SARAVALI_METADATA,
            },
            "Phaladeepika": {
                "data": PHALADEEPIKA_PLANETS_IN_HOUSES,
                "get_func": get_phaladeepika_interpretation,
                "metadata": {"translator": "V. Subrahmanya Sastri", "edition": "1963"},
            },
            "Hora Sara": {
                "data": HORA_SARA_PLANETS_IN_HOUSES,
                "get_func": get_hora_sara_interpretation,
                "metadata": {"translator": "R. Santhanam", "edition": "1996"},
            },
        }

    def get_available_sources(self, planet: str, house: int) -> List[str]:
        """
        Get list of sources that have data for this planet-house combination.

        Args:
            planet: Planet name
            house: House number (1-12)

        Returns:
            List of source names that have this combination
        """
        available = []

        for source_name, source_info in self.sources.items():
            source_data = source_info["data"]
            if planet in source_data and house in source_data[planet]:
                available.append(source_name)

        return available

    def compare_sources(self, planet: str, house: int) -> SourceComparison:
        """
        Compare interpretations from multiple sources for a planet-house combination.

        Args:
            planet: Planet name
            house: House number (1-12)

        Returns:
            SourceComparison object with detailed comparison

        Raises:
            ValueError: If no sources available for this combination
        """
        sources_available = self.get_available_sources(planet, house)

        if not sources_available:
            raise ValueError(f"No sources available for {planet} in house {house}")

        # Get interpretations from all available sources dynamically
        interpretations = {}

        for source_name in sources_available:
            get_func = self.sources[source_name]["get_func"]
            interpretations[source_name] = get_func(planet, house)

        # Analyze agreements and contradictions across all sources
        common_themes, unique_insights, contradictions = self._analyze_interpretations(interpretations)

        # Determine agreement level
        agreement_level = self._calculate_agreement_level(common_themes, contradictions)

        # Synthesize combined interpretation
        synthesis = self._synthesize_interpretation(planet, house, interpretations, common_themes, contradictions)

        # Calculate confidence score
        confidence = self._calculate_multi_source_confidence(sources_available, agreement_level)

        return SourceComparison(
            planet=planet,
            house=house,
            sources_available=sources_available,
            agreement_level=agreement_level,
            common_themes=common_themes,
            unique_insights=unique_insights,
            contradictions=contradictions,
            synthesis=synthesis,
            confidence_score=confidence,
        )

    def _analyze_interpretations(
        self, interpretations: Dict[str, Dict[str, Any]]
    ) -> Tuple[List[str], Dict[str, List[str]], List[Dict[str, str]]]:
        """
        Analyze interpretations to find common themes and contradictions across N sources.

        Returns:
            Tuple of (common_themes, unique_insights_by_source, contradictions)
        """
        common_themes = []
        unique_insights = {source: [] for source in interpretations.keys()}
        contradictions = []

        # If only one source, return its effects as unique
        if len(interpretations) == 1:
            source_name = list(interpretations.keys())[0]
            effects = interpretations[source_name].get("detailed_effects", [])
            unique_insights[source_name] = effects[:5]
            return common_themes, unique_insights, contradictions

        # Collect all effects from all sources
        all_effects_by_source = {}
        for source_name, data in interpretations.items():
            positive = set(data.get("positive_effects", []))
            challenging = set(data.get("challenging_effects", []))
            all_effects_by_source[source_name] = positive | challenging

        # Find common keywords across ALL sources
        if len(all_effects_by_source) >= 2:
            # Start with first source's effects
            source_names = list(all_effects_by_source.keys())
            common_keywords = self._find_common_keywords_multi([all_effects_by_source[s] for s in source_names])
            common_themes = [f"All sources emphasize: {theme}" for theme in common_keywords[:5]]

        # Identify unique effects per source (effects not found in other sources)
        for source_name, effects in all_effects_by_source.items():
            other_effects = set()
            for other_source, other_source_effects in all_effects_by_source.items():
                if other_source != source_name:
                    other_effects |= other_source_effects

            # Effects unique to this source
            unique = list(effects - other_effects)[:3]
            if unique:
                unique_insights[source_name] = unique

        # Look for contradictions across all sources
        source_names = list(interpretations.keys())
        for i, source1 in enumerate(source_names):
            for source2 in source_names[i + 1 :]:
                positive1 = set(interpretations[source1].get("positive_effects", []))
                challenging2 = set(interpretations[source2].get("challenging_effects", []))

                for effect1 in positive1:
                    for effect2 in challenging2:
                        if self._are_contradictory(effect1, effect2):
                            contradictions.append({source1: effect1, source2: effect2})

        return common_themes, unique_insights, contradictions

    def _find_common_keywords_multi(self, effect_sets: List[set]) -> List[str]:
        """Find common keywords across multiple sets of effects"""
        keywords = []

        # Simple keyword extraction (could be enhanced with NLP)
        important_words = {
            "wealth",
            "health",
            "career",
            "marriage",
            "children",
            "education",
            "happiness",
            "success",
            "fame",
            "property",
            "vehicles",
            "wisdom",
            "leadership",
            "courage",
            "intelligence",
            "spiritual",
            "fortune",
            "longevity",
            "enemies",
            "father",
            "mother",
            "siblings",
        }

        for word in important_words:
            # Check if word appears in ALL effect sets
            found_in_all = all(any(word in str(item).lower() for item in effect_set) for effect_set in effect_sets)
            if found_in_all:
                keywords.append(word)

        return keywords

    def _are_contradictory(self, effect1: str, effect2: str) -> bool:
        """Check if two effects are contradictory"""
        # Simple contradiction detection (could be enhanced)
        contradictory_pairs = [
            ("wealth", "poor"),
            ("happy", "unhappy"),
            ("success", "failure"),
            ("healthy", "disease"),
            ("long", "short"),
        ]

        effect1_lower = effect1.lower()
        effect2_lower = effect2.lower()

        for word1, word2 in contradictory_pairs:
            if (word1 in effect1_lower and word2 in effect2_lower) or (
                word2 in effect1_lower and word1 in effect2_lower
            ):
                return True

        return False

    def _calculate_agreement_level(
        self, common_themes: List[str], contradictions: List[Dict[str, str]]
    ) -> AgreementLevel:
        """Calculate the level of agreement between sources"""
        if len(contradictions) >= 3:
            return AgreementLevel.STRONG_DISAGREEMENT
        elif len(contradictions) >= 1:
            return AgreementLevel.MODERATE_DISAGREEMENT
        elif len(common_themes) >= 4:
            return AgreementLevel.STRONG_AGREEMENT
        elif len(common_themes) >= 2:
            return AgreementLevel.MODERATE_AGREEMENT
        else:
            return AgreementLevel.NEUTRAL

    def _synthesize_interpretation(
        self,
        planet: str,
        house: int,
        interpretations: Dict[str, Dict[str, Any]],
        common_themes: List[str],
        contradictions: List[Dict[str, str]],
    ) -> str:
        """Synthesize a unified interpretation from multiple sources"""
        synthesis_parts = []
        num_sources = len(interpretations)

        # Start with planet and house
        synthesis_parts.append(
            f"For {planet} in the {house}th house, {num_sources} classical text(s) provide the following synthesis:"
        )

        # Add common themes
        if common_themes:
            synthesis_parts.append(f"\n\nAll sources agree on key themes: {', '.join(common_themes[:5])}.")

        # Add each source's translation in order of authority
        source_order = ["BPHS", "Saravali", "Phaladeepika", "Hora Sara"]
        for source_name in source_order:
            if source_name in interpretations:
                trans = interpretations[source_name].get("translation", "")
                if trans:
                    chapter_info = ""
                    if source_name == "BPHS":
                        chapter_info = "Ch. 24"
                    elif source_name == "Saravali":
                        verses = interpretations[source_name].get("verses", "")
                        chapter_info = verses.split(",")[0] if verses else ""
                    elif source_name == "Phaladeepika":
                        chapter = interpretations[source_name].get("chapter", "")
                        chapter_info = f"Ch. {chapter}" if chapter else ""
                    elif source_name == "Hora Sara":
                        chapter = interpretations[source_name].get("chapter", "")
                        chapter_info = f"Ch. {chapter}" if chapter else ""

                    synthesis_parts.append(
                        f"\n\n{source_name} ({chapter_info}): '{trans[:120]}{'...' if len(trans) > 120 else ''}"
                    )

        # Address contradictions if any
        if contradictions:
            synthesis_parts.append(
                f"\n\nNote: Sources show some variation in interpretation ({len(contradictions)} point(s) of divergence). "
                f"Classical texts provide complementary perspectives. "
                f"Individual chart context determines which interpretation manifests most strongly."
            )

        return "".join(synthesis_parts)

    def _calculate_multi_source_confidence(
        self, sources_available: List[str], agreement_level: AgreementLevel
    ) -> float:
        """Calculate confidence score for multi-source interpretation"""
        base_confidence = 0.85  # Base for having classical sources

        # Boost for multiple sources
        if len(sources_available) >= 2:
            base_confidence += 0.05

        # Adjust based on agreement
        agreement_adjustments = {
            AgreementLevel.STRONG_AGREEMENT: 0.10,
            AgreementLevel.MODERATE_AGREEMENT: 0.05,
            AgreementLevel.NEUTRAL: 0.00,
            AgreementLevel.MODERATE_DISAGREEMENT: -0.05,
            AgreementLevel.STRONG_DISAGREEMENT: -0.10,
        }

        base_confidence += agreement_adjustments[agreement_level]

        # Cap between 0.7 and 0.98
        return max(0.70, min(0.98, base_confidence))

    def get_comprehensive_interpretation(
        self, planet: str, house: int, include_comparison: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive interpretation with multi-source comparison.

        Args:
            planet: Planet name
            house: House number
            include_comparison: Whether to include detailed comparison

        Returns:
            Comprehensive interpretation dictionary
        """
        sources_available = self.get_available_sources(planet, house)

        if not sources_available:
            raise ValueError(f"No sources available for {planet} in house {house}")

        result = {"planet": planet, "house": house, "sources_available": sources_available, "interpretations": {}}

        # Get individual source interpretations dynamically
        for source_name in sources_available:
            get_func = self.sources[source_name]["get_func"]
            result["interpretations"][source_name] = get_func(planet, house)

        # Add comparison if requested and multiple sources available
        if include_comparison and len(sources_available) > 1:
            comparison = self.compare_sources(planet, house)
            result["comparison"] = {
                "agreement_level": comparison.agreement_level.value,
                "common_themes": comparison.common_themes,
                "unique_insights": comparison.unique_insights,
                "contradictions": comparison.contradictions,
                "synthesis": comparison.synthesis,
                "confidence_score": comparison.confidence_score,
            }

        return result
