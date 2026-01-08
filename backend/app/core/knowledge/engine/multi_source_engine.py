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

from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

from backend.app.core.knowledge.sources.bphs_planets_in_houses import (
    get_planet_in_house_interpretation,
    BPHS_PLANETS_IN_HOUSES
)
from backend.app.core.knowledge.sources.saravali_planets_in_houses import (
    get_saravali_interpretation,
    SARAVALI_PLANETS_IN_HOUSES,
    SARAVALI_METADATA
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
    unique_to_bphs: List[str]
    unique_to_saravali: List[str]
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
        """Initialize the multi-source engine"""
        self.sources = {
            'BPHS': {
                'data': BPHS_PLANETS_IN_HOUSES,
                'get_func': get_planet_in_house_interpretation
            },
            'Saravali': {
                'data': SARAVALI_PLANETS_IN_HOUSES,
                'get_func': get_saravali_interpretation
            }
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
        
        if planet in BPHS_PLANETS_IN_HOUSES and house in BPHS_PLANETS_IN_HOUSES[planet]:
            available.append('BPHS')
        
        if planet in SARAVALI_PLANETS_IN_HOUSES and house in SARAVALI_PLANETS_IN_HOUSES[planet]:
            available.append('Saravali')
        
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
        
        # Get interpretations from available sources
        interpretations = {}
        
        if 'BPHS' in sources_available:
            interpretations['BPHS'] = get_planet_in_house_interpretation(planet, house)
        
        if 'Saravali' in sources_available:
            interpretations['Saravali'] = get_saravali_interpretation(planet, house)
        
        # Analyze agreements and contradictions
        common_themes, unique_bphs, unique_saravali, contradictions = self._analyze_interpretations(
            interpretations
        )
        
        # Determine agreement level
        agreement_level = self._calculate_agreement_level(
            common_themes, contradictions
        )
        
        # Synthesize combined interpretation
        synthesis = self._synthesize_interpretation(
            planet, house, interpretations, common_themes, contradictions
        )
        
        # Calculate confidence score
        confidence = self._calculate_multi_source_confidence(
            sources_available, agreement_level
        )
        
        return SourceComparison(
            planet=planet,
            house=house,
            sources_available=sources_available,
            agreement_level=agreement_level,
            common_themes=common_themes,
            unique_to_bphs=unique_bphs,
            unique_to_saravali=unique_saravali,
            contradictions=contradictions,
            synthesis=synthesis,
            confidence_score=confidence
        )
    
    def _analyze_interpretations(
        self, 
        interpretations: Dict[str, Dict[str, Any]]
    ) -> Tuple[List[str], List[str], List[str], List[Dict[str, str]]]:
        """
        Analyze interpretations to find common themes and contradictions.
        
        Returns:
            Tuple of (common_themes, unique_to_bphs, unique_to_saravali, contradictions)
        """
        common_themes = []
        unique_bphs = []
        unique_saravali = []
        contradictions = []
        
        # If only one source, return its effects as unique
        if len(interpretations) == 1:
            source_name = list(interpretations.keys())[0]
            effects = interpretations[source_name].get('detailed_effects', [])
            if source_name == 'BPHS':
                unique_bphs = effects
            else:
                unique_saravali = effects
            return common_themes, unique_bphs, unique_saravali, contradictions
        
        # Compare BPHS and Saravali
        bphs_data = interpretations.get('BPHS', {})
        saravali_data = interpretations.get('Saravali', {})
        
        bphs_positive = set(bphs_data.get('positive_effects', []))
        saravali_positive = set(saravali_data.get('positive_effects', []))
        
        bphs_challenging = set(bphs_data.get('challenging_effects', []))
        saravali_challenging = set(saravali_data.get('challenging_effects', []))
        
        # Find common positive themes (semantic matching would be better, but using keywords for now)
        common_keywords = self._find_common_keywords(
            bphs_positive | bphs_challenging,
            saravali_positive | saravali_challenging
        )
        common_themes = [f"Both sources emphasize: {theme}" for theme in common_keywords[:5]]
        
        # Identify unique effects
        unique_bphs = list(bphs_positive - saravali_positive)[:3]
        unique_saravali = list(saravali_positive - bphs_positive)[:3]
        
        # Look for contradictions (positive in one, challenging in another)
        for bphs_effect in bphs_positive:
            for saravali_effect in saravali_challenging:
                if self._are_contradictory(bphs_effect, saravali_effect):
                    contradictions.append({
                        'BPHS': bphs_effect,
                        'Saravali': saravali_effect
                    })
        
        return common_themes, unique_bphs, unique_saravali, contradictions
    
    def _find_common_keywords(self, set1: set, set2: set) -> List[str]:
        """Find common keywords between two sets of effects"""
        keywords = []
        
        # Simple keyword extraction (could be enhanced with NLP)
        important_words = {
            'wealth', 'health', 'career', 'marriage', 'children', 'education',
            'happiness', 'success', 'fame', 'property', 'vehicles', 'wisdom',
            'leadership', 'courage', 'intelligence', 'spiritual', 'fortune'
        }
        
        for word in important_words:
            found_in_1 = any(word in str(item).lower() for item in set1)
            found_in_2 = any(word in str(item).lower() for item in set2)
            if found_in_1 and found_in_2:
                keywords.append(word)
        
        return keywords
    
    def _are_contradictory(self, effect1: str, effect2: str) -> bool:
        """Check if two effects are contradictory"""
        # Simple contradiction detection (could be enhanced)
        contradictory_pairs = [
            ('wealth', 'poor'),
            ('happy', 'unhappy'),
            ('success', 'failure'),
            ('healthy', 'disease'),
            ('long', 'short')
        ]
        
        effect1_lower = effect1.lower()
        effect2_lower = effect2.lower()
        
        for word1, word2 in contradictory_pairs:
            if (word1 in effect1_lower and word2 in effect2_lower) or \
               (word2 in effect1_lower and word1 in effect2_lower):
                return True
        
        return False
    
    def _calculate_agreement_level(
        self,
        common_themes: List[str],
        contradictions: List[Dict[str, str]]
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
        contradictions: List[Dict[str, str]]
    ) -> str:
        """Synthesize a unified interpretation from multiple sources"""
        synthesis_parts = []
        
        # Start with planet and house
        synthesis_parts.append(
            f"For {planet} in the {house}th house, classical texts provide the following synthesis:"
        )
        
        # Add common themes
        if common_themes:
            synthesis_parts.append(
                f"\n\nBoth BPHS and Saravali agree on key themes including {', '.join(common_themes[:3])}."
            )
        
        # Add source-specific insights
        if 'BPHS' in interpretations:
            bphs_trans = interpretations['BPHS'].get('translation', '')
            if bphs_trans:
                synthesis_parts.append(
                    f"\n\nBPHS (Ch. 24) states: '{bphs_trans[:150]}...'"
                )
        
        if 'Saravali' in interpretations:
            saravali_trans = interpretations['Saravali'].get('translation', '')
            if saravali_trans:
                synthesis_parts.append(
                    f"\n\nSaravali adds: '{saravali_trans[:150]}...'"
                )
        
        # Address contradictions if any
        if contradictions:
            synthesis_parts.append(
                f"\n\nNote: Sources show some variation in interpretation. "
                f"BPHS emphasizes certain aspects while Saravali provides complementary perspectives. "
                f"Individual chart context determines which interpretation manifests most strongly."
            )
        
        return ''.join(synthesis_parts)
    
    def _calculate_multi_source_confidence(
        self,
        sources_available: List[str],
        agreement_level: AgreementLevel
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
            AgreementLevel.STRONG_DISAGREEMENT: -0.10
        }
        
        base_confidence += agreement_adjustments[agreement_level]
        
        # Cap between 0.7 and 0.98
        return max(0.70, min(0.98, base_confidence))
    
    def get_comprehensive_interpretation(
        self,
        planet: str,
        house: int,
        include_comparison: bool = True
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
        
        result = {
            'planet': planet,
            'house': house,
            'sources_available': sources_available,
            'interpretations': {}
        }
        
        # Get individual source interpretations
        if 'BPHS' in sources_available:
            result['interpretations']['BPHS'] = get_planet_in_house_interpretation(planet, house)
        
        if 'Saravali' in sources_available:
            result['interpretations']['Saravali'] = get_saravali_interpretation(planet, house)
        
        # Add comparison if requested and multiple sources available
        if include_comparison and len(sources_available) > 1:
            comparison = self.compare_sources(planet, house)
            result['comparison'] = {
                'agreement_level': comparison.agreement_level.value,
                'common_themes': comparison.common_themes,
                'unique_to_bphs': comparison.unique_to_bphs,
                'unique_to_saravali': comparison.unique_to_saravali,
                'contradictions': comparison.contradictions,
                'synthesis': comparison.synthesis,
                'confidence_score': comparison.confidence_score
            }
        
        return result
