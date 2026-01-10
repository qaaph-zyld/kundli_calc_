"""
Relationship Synthesis Engine
==============================

Holistic relationship analysis synthesizing:
- 7th house (marriage/partnership) + lord + planets
- 5th house (romance/children) + planets  
- 8th house (intimacy/transformation) + planets
- Venus (natural relationship karaka)
- Marriage yogas, delay yogas, separation yogas
- Current dasha effects on relationships
- Timing for marriage/partnership

Evolution from single planet to complete relationship life-area synthesis.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from app.core.knowledge.engine.contextual_synthesis_engine import (
    ContextualSynthesisEngine,
    StrengthLevel
)
from app.core.knowledge.sources.bphs_yogas import get_all_yogas


class RelationshipStrength(Enum):
    """Relationship potential strength levels"""
    EXCEPTIONAL = "exceptional"      # 90-100: Outstanding relationship harmony
    VERY_STRONG = "very_strong"      # 75-89: Strong relationship potential
    STRONG = "strong"                # 60-74: Good relationship prospects
    MODERATE = "moderate"            # 40-59: Average relationship path
    CHALLENGING = "challenging"      # 20-39: Relationship obstacles
    DIFFICULT = "difficult"          # 0-19: Significant challenges


@dataclass
class RelationshipFactor:
    """Single factor contributing to relationship analysis"""
    factor_name: str
    house_or_planet: str
    contribution_score: int
    strength_level: str
    interpretation: str
    sources: List[str]
    timing_note: Optional[str] = None


@dataclass
class RelationshipSynthesis:
    """Complete relationship life-area analysis"""
    overall_assessment: str
    strength_score: float
    strength_level: RelationshipStrength
    key_factors: List[RelationshipFactor]
    synthesis: str
    timing: Dict[str, Any]
    recommendations: List[str]
    sources_consulted: int
    sources: List[str]
    confidence: float
    domain: str = "relationships"


class RelationshipSynthesisEngine:
    """
    Engine for holistic relationship analysis.
    
    Aggregates:
    1. 7th house (marriage/partnership/spouse)
    2. 5th house (romance/love/children)
    3. 8th house (intimacy/transformation/in-laws)
    4. Venus (natural relationship karaka)
    5. Marriage yogas and delay/separation yogas
    6. Current dasha effects on relationships
    7. Timing windows for marriage/partnership
    """
    
    def __init__(self):
        self.contextual_engine = ContextualSynthesisEngine()
        self.all_yogas = get_all_yogas()
        
        # Relationship-relevant yoga keywords
        self.relationship_yoga_keywords = [
            "Marriage", "Kalatr", "Venus", "Shubha", "Parivartana"
        ]
    
    def synthesize_relationship_analysis(
        self,
        chart_data: Dict[str, Any],
        current_dasha: Optional[str] = None
    ) -> RelationshipSynthesis:
        """Generate complete relationship life-area analysis"""
        
        factors = []
        sources_used = set()
        total_score = 0
        
        # 1. Analyze 7th house (primary marriage/partnership)
        seventh_factor = self._analyze_relationship_house(
            chart_data, 7, "Marriage & Partnership", current_dasha
        )
        factors.append(seventh_factor)
        total_score += seventh_factor.contribution_score
        sources_used.update(seventh_factor.sources)
        
        # 2. Analyze 5th house (romance/love)
        fifth_factor = self._analyze_relationship_house(
            chart_data, 5, "Romance & Love", current_dasha
        )
        factors.append(fifth_factor)
        total_score += fifth_factor.contribution_score
        sources_used.update(fifth_factor.sources)
        
        # 3. Analyze 8th house (intimacy/transformation)
        eighth_factor = self._analyze_relationship_house(
            chart_data, 8, "Intimacy & Transformation", current_dasha
        )
        factors.append(eighth_factor)
        total_score += eighth_factor.contribution_score
        sources_used.update(eighth_factor.sources)
        
        # 4. Analyze Venus (natural relationship karaka)
        venus_factor = self._analyze_relationship_karaka(
            chart_data, "Venus", "Love & Harmony", current_dasha
        )
        if venus_factor:
            factors.append(venus_factor)
            total_score += venus_factor.contribution_score
            sources_used.update(venus_factor.sources)
        
        # 5. Analyze relationship yogas
        yoga_factors = self._analyze_relationship_yogas(
            chart_data.get("active_yogas", [])
        )
        for yoga_factor in yoga_factors:
            factors.append(yoga_factor)
            total_score += yoga_factor.contribution_score
            sources_used.update(yoga_factor.sources)
        
        # Normalize score
        max_possible = 100
        normalized_score = min(100, (total_score / max_possible) * 100)
        
        # Determine strength level
        strength_level = self._determine_relationship_strength(normalized_score)
        
        # Generate timing analysis
        timing_info = self._generate_relationship_timing(
            chart_data, factors, current_dasha
        )
        
        # Generate synthesis
        synthesis_text = self._generate_relationship_synthesis(
            factors, normalized_score, strength_level, timing_info
        )
        
        # Generate assessment
        assessment = self._generate_overall_assessment(
            normalized_score, strength_level, factors
        )
        
        # Generate recommendations
        recommendations = self._generate_relationship_recommendations(
            factors, strength_level, timing_info
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(factors, len(sources_used))
        
        return RelationshipSynthesis(
            overall_assessment=assessment,
            strength_score=round(normalized_score, 1),
            strength_level=strength_level,
            key_factors=factors,
            synthesis=synthesis_text,
            timing=timing_info,
            recommendations=recommendations,
            sources_consulted=len(sources_used),
            sources=sorted(list(sources_used)),
            confidence=confidence
        )
    
    def _analyze_relationship_house(
        self,
        chart_data: Dict[str, Any],
        house_num: int,
        house_theme: str,
        current_dasha: Optional[str]
    ) -> RelationshipFactor:
        """Analyze relationship-relevant house"""
        
        planets_in_house = [
            p for p, data in chart_data.get("planets", {}).items()
            if data.get("house") == house_num
        ]
        
        house_lord = chart_data.get("house_lords", {}).get(house_num)
        
        score = 0
        interpretation_parts = []
        sources = []
        
        # Base score
        if house_num == 7:
            base_score = 35  # Most important for marriage
        elif house_num == 5:
            base_score = 20  # Important for romance
        else:  # 8th house
            base_score = 15  # Important for intimacy
        
        # Analyze planets
        if planets_in_house:
            for planet in planets_in_house:
                planet_data = chart_data["planets"][planet]
                dignity = planet_data.get("dignity", "neutral")
                
                result = self.contextual_engine.synthesize_interpretation(
                    planet=planet,
                    house=house_num,
                    sign=planet_data.get("sign", ""),
                    dignity=dignity,
                    current_dasha=current_dasha
                )
                
                planet_score = result.strength_assessment.strength_score / 10
                
                # Benefics in 7th are good, malefics challenging
                if house_num == 7:
                    if planet in ["Venus", "Jupiter", "Mercury", "Moon"]:
                        score += planet_score
                    else:  # Malefics
                        score += planet_score * 0.5
                else:
                    score += planet_score
                
                interpretation_parts.append(
                    f"{planet} in {house_num}th ({dignity}): "
                    f"{result.base_interpretation.get('general_effects', '')[:80]}..."
                )
                sources.extend(result.sources_used)
        else:
            interpretation_parts.append(f"No planets in {house_num}th house")
        
        # House lord placement
        if house_lord:
            lord_data = chart_data["planets"].get(house_lord, {})
            lord_house = lord_data.get("house", 0)
            
            if lord_house in [1, 4, 5, 7, 9, 10, 11]:
                score += 5
                interpretation_parts.append(
                    f"{house_num}th lord {house_lord} in {lord_house}th (favorable)"
                )
            elif lord_house in [6, 8, 12]:
                score -= 3
                interpretation_parts.append(
                    f"{house_num}th lord {house_lord} in {lord_house}th (challenging)"
                )
        
        final_score = max(0, min(base_score, base_score + score))
        strength = "strong" if final_score > base_score * 0.7 else "moderate" if final_score > base_score * 0.4 else "weak"
        
        return RelationshipFactor(
            factor_name=f"{house_num}th House - {house_theme}",
            house_or_planet=f"House {house_num}",
            contribution_score=int(final_score),
            strength_level=strength,
            interpretation=" | ".join(interpretation_parts),
            sources=list(set(sources)),
            timing_note=f"Effects manifest during {house_lord} dasha" if house_lord else None
        )
    
    def _analyze_relationship_karaka(
        self,
        chart_data: Dict[str, Any],
        planet: str,
        karaka_theme: str,
        current_dasha: Optional[str]
    ) -> Optional[RelationshipFactor]:
        """Analyze Venus (natural relationship karaka)"""
        
        planet_data = chart_data.get("planets", {}).get(planet)
        if not planet_data:
            return None
        
        house = planet_data.get("house")
        sign = planet_data.get("sign", "")
        dignity = planet_data.get("dignity", "neutral")
        
        result = self.contextual_engine.synthesize_interpretation(
            planet=planet,
            house=house,
            sign=sign,
            dignity=dignity,
            current_dasha=current_dasha
        )
        
        score = result.strength_assessment.strength_score / 4  # Max 25 points
        strength = result.strength_assessment.overall_strength.value
        
        return RelationshipFactor(
            factor_name=f"{planet} - Natural Karaka ({karaka_theme})",
            house_or_planet=planet,
            contribution_score=int(score),
            strength_level=strength,
            interpretation=result.synthesized_interpretation[:200] + "...",
            sources=result.sources_used,
            timing_note=f"Peak effects during {planet} mahadasha"
        )
    
    def _analyze_relationship_yogas(
        self,
        active_yogas: List[str]
    ) -> List[RelationshipFactor]:
        """Analyze relationship-relevant yogas"""
        
        yoga_factors = []
        
        for yoga_name in active_yogas:
            is_relationship_yoga = any(
                keyword in yoga_name for keyword in self.relationship_yoga_keywords
            )
            
            if not is_relationship_yoga:
                continue
            
            yoga_data = self.all_yogas.get(yoga_name)
            if not yoga_data:
                continue
            
            score = 10  # Relationship yogas contribute moderately
            
            effects = yoga_data.get("effects", {})
            relationship_effect = effects.get("relationships", effects.get("general", ""))
            
            yoga_factors.append(RelationshipFactor(
                factor_name=f"Yoga: {yoga_name.replace('_', ' ')}",
                house_or_planet="Yoga",
                contribution_score=score,
                strength_level="strong",
                interpretation=relationship_effect[:150] + "...",
                sources=[f"BPHS Ch. {yoga_data.get('chapter', 0)}"],
                timing_note="Effects manifest during involved planets' dashas"
            ))
        
        return yoga_factors
    
    def _determine_relationship_strength(self, score: float) -> RelationshipStrength:
        """Determine relationship strength from score"""
        if score >= 90:
            return RelationshipStrength.EXCEPTIONAL
        elif score >= 75:
            return RelationshipStrength.VERY_STRONG
        elif score >= 60:
            return RelationshipStrength.STRONG
        elif score >= 40:
            return RelationshipStrength.MODERATE
        elif score >= 20:
            return RelationshipStrength.CHALLENGING
        else:
            return RelationshipStrength.DIFFICULT
    
    def _generate_relationship_timing(
        self,
        chart_data: Dict[str, Any],
        factors: List[RelationshipFactor],
        current_dasha: Optional[str]
    ) -> Dict[str, Any]:
        """Generate timing analysis for relationships"""
        
        timing = {
            "current_period": "",
            "marriage_windows": [],
            "favorable_periods": []
        }
        
        if current_dasha:
            timing["current_period"] = (
                f"Currently in {current_dasha} mahadasha. "
                f"Relationship effects from {current_dasha}'s placement active now."
            )
        
        # Marriage timing indicators
        seventh_lord = chart_data.get("house_lords", {}).get(7)
        if seventh_lord:
            timing["marriage_windows"].append(
                f"{seventh_lord} mahadasha (7th lord period)"
            )
        
        venus_data = chart_data.get("planets", {}).get("Venus", {})
        if venus_data:
            timing["marriage_windows"].append("Venus mahadasha (karaka period)")
        
        return timing
    
    def _generate_relationship_synthesis(
        self,
        factors: List[RelationshipFactor],
        score: float,
        strength: RelationshipStrength,
        timing: Dict[str, Any]
    ) -> str:
        """Generate complete relationship narrative"""
        
        parts = []
        
        parts.append(
            f"Relationship Analysis shows {strength.value.replace('_', ' ').title()} "
            f"potential (strength score: {score:.1f}/100)."
        )
        
        parts.append("\n\nKey Relationship Factors:")
        for factor in factors[:5]:
            parts.append(
                f"\n• {factor.factor_name} ({factor.contribution_score} points): "
                f"{factor.interpretation[:100]}..."
            )
        
        if timing.get("marriage_windows"):
            parts.append("\n\nMarriage Timing Windows:")
            for window in timing["marriage_windows"][:3]:
                parts.append(f"\n• {window}")
        
        return "".join(parts)
    
    def _generate_overall_assessment(
        self,
        score: float,
        strength: RelationshipStrength,
        factors: List[RelationshipFactor]
    ) -> str:
        """Generate executive summary"""
        
        if strength == RelationshipStrength.EXCEPTIONAL:
            return (
                f"Exceptional relationship potential ({score:.1f}/100). "
                "Chart shows strong indicators for harmonious partnerships, "
                "marital happiness, and fulfilling relationships."
            )
        elif strength == RelationshipStrength.VERY_STRONG:
            return (
                f"Very strong relationship prospects ({score:.1f}/100). "
                "Significant potential for happy marriage and partnerships. "
                "Key relationship houses well-placed."
            )
        elif strength == RelationshipStrength.STRONG:
            return (
                f"Good relationship potential ({score:.1f}/100). "
                "Solid foundation for partnerships with favorable indicators. "
                "Success through mutual understanding."
            )
        elif strength == RelationshipStrength.MODERATE:
            return (
                f"Moderate relationship prospects ({score:.1f}/100). "
                "Average relationship path with both harmony and challenges. "
                "Success requires effort and compatibility."
            )
        elif strength == RelationshipStrength.CHALLENGING:
            return (
                f"Challenging relationship indicators ({score:.1f}/100). "
                "Partnerships may face obstacles requiring patience. "
                "Focus on communication and timing."
            )
        else:
            return (
                f"Difficult relationship configuration ({score:.1f}/100). "
                "Significant relationship challenges indicated. "
                "Careful partner selection and remedial measures recommended."
            )
    
    def _generate_relationship_recommendations(
        self,
        factors: List[RelationshipFactor],
        strength: RelationshipStrength,
        timing: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        if strength in [RelationshipStrength.EXCEPTIONAL, RelationshipStrength.VERY_STRONG]:
            recommendations.append(
                "Pursue relationships during favorable dasha periods for best results"
            )
            recommendations.append(
                "Strong indicators for harmonious marriage - trust natural timing"
            )
        elif strength == RelationshipStrength.STRONG:
            recommendations.append(
                "Focus on compatibility and shared values in partner selection"
            )
            recommendations.append(
                "Build strong communication foundation before commitment"
            )
        else:
            recommendations.append(
                "Careful partner selection crucial - seek astrological compatibility"
            )
            recommendations.append(
                "Consider relationship counseling or pre-marital guidance"
            )
            recommendations.append(
                "Strengthen Venus through remedial measures"
            )
        
        if timing.get("marriage_windows"):
            recommendations.append(
                f"Optimal marriage timing: {timing['marriage_windows'][0]}"
            )
        
        return recommendations[:5]
    
    def _calculate_confidence(
        self,
        factors: List[RelationshipFactor],
        sources_count: int
    ) -> float:
        """Calculate confidence in analysis"""
        
        base_confidence = 0.85
        
        if len(factors) >= 5:
            base_confidence += 0.05
        
        if sources_count >= 8:
            base_confidence += 0.05
        
        return min(0.98, base_confidence)
