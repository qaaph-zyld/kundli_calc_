"""
Wealth Synthesis Engine
========================

Holistic wealth analysis synthesizing:
- 2nd house (family wealth, assets, speech) + lord + planets
- 11th house (gains, income, networks) + lord + planets
- 5th house (speculation, investments) + lord + planets
- 9th house (fortune, inheritance) + lord + planets
- Jupiter (natural wealth karaka - Dhana Karaka)
- All Dhana yogas (wealth-forming combinations)
- Poverty yogas / cancellation factors
- Current dasha effects on wealth
- Timing windows for financial gains

Evolution from single planet to complete wealth life-area synthesis.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from backend.app.core.knowledge.engine.contextual_synthesis_engine import (
    ContextualSynthesisEngine,
    StrengthLevel
)
from backend.app.core.knowledge.sources.bphs_yogas import get_all_yogas


class WealthStrength(Enum):
    """Wealth potential strength levels"""
    EXCEPTIONAL = "exceptional"      # 90-100: Outstanding wealth potential
    VERY_STRONG = "very_strong"      # 75-89: Strong wealth accumulation
    STRONG = "strong"                # 60-74: Good financial prospects
    MODERATE = "moderate"            # 40-59: Average wealth path
    CHALLENGING = "challenging"      # 20-39: Financial obstacles
    DIFFICULT = "difficult"          # 0-19: Significant challenges


@dataclass
class WealthFactor:
    """Single factor contributing to wealth analysis"""
    factor_name: str
    house_or_planet: str
    contribution_score: int
    strength_level: str
    interpretation: str
    sources: List[str]
    timing_note: Optional[str] = None


@dataclass
class WealthSynthesis:
    """Complete wealth life-area analysis"""
    overall_assessment: str
    strength_score: float
    strength_level: WealthStrength
    key_factors: List[WealthFactor]
    synthesis: str
    timing: Dict[str, Any]
    recommendations: List[str]
    sources_consulted: int
    sources: List[str]
    confidence: float
    domain: str = "wealth"


class WealthSynthesisEngine:
    """
    Engine for holistic wealth analysis.
    
    Aggregates:
    1. 2nd house (family wealth/assets/resources)
    2. 11th house (gains/income/networks)
    3. 5th house (speculation/investments/creativity)
    4. 9th house (fortune/inheritance/dharma)
    5. Jupiter (natural wealth karaka - Dhana Karaka)
    6. Dhana yogas (wealth-forming combinations)
    7. Poverty yogas (cancellation factors)
    8. Current dasha effects on wealth houses
    9. Timing windows for financial gains
    """
    
    def __init__(self):
        self.contextual_engine = ContextualSynthesisEngine()
        self.all_yogas = get_all_yogas()
        
        # Wealth-relevant yoga keywords
        self.wealth_yoga_keywords = [
            "Dhana", "Lakshmi", "Wealth", "Prosperity", "Gaja_Kesari"
        ]
    
    def synthesize_wealth_analysis(
        self,
        chart_data: Dict[str, Any],
        current_dasha: Optional[str] = None
    ) -> WealthSynthesis:
        """Generate complete wealth life-area analysis"""
        
        factors = []
        sources_used = set()
        total_score = 0
        
        # 1. Analyze 2nd house (primary wealth indicator)
        second_factor = self._analyze_wealth_house(
            chart_data, 2, "Family Wealth & Assets", current_dasha
        )
        factors.append(second_factor)
        total_score += second_factor.contribution_score
        sources_used.update(second_factor.sources)
        
        # 2. Analyze 11th house (gains/income)
        eleventh_factor = self._analyze_wealth_house(
            chart_data, 11, "Gains & Income", current_dasha
        )
        factors.append(eleventh_factor)
        total_score += eleventh_factor.contribution_score
        sources_used.update(eleventh_factor.sources)
        
        # 3. Analyze 5th house (speculation/investments)
        fifth_factor = self._analyze_wealth_house(
            chart_data, 5, "Speculation & Investments", current_dasha
        )
        factors.append(fifth_factor)
        total_score += fifth_factor.contribution_score
        sources_used.update(fifth_factor.sources)
        
        # 4. Analyze 9th house (fortune/inheritance)
        ninth_factor = self._analyze_wealth_house(
            chart_data, 9, "Fortune & Inheritance", current_dasha
        )
        factors.append(ninth_factor)
        total_score += ninth_factor.contribution_score
        sources_used.update(ninth_factor.sources)
        
        # 5. Analyze Jupiter (natural wealth karaka)
        jupiter_factor = self._analyze_wealth_karaka(
            chart_data, "Jupiter", "Prosperity & Expansion", current_dasha
        )
        if jupiter_factor:
            factors.append(jupiter_factor)
            total_score += jupiter_factor.contribution_score
            sources_used.update(jupiter_factor.sources)
        
        # 6. Analyze Dhana yogas
        yoga_factors = self._analyze_wealth_yogas(
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
        strength_level = self._determine_wealth_strength(normalized_score)
        
        # Generate timing analysis
        timing_info = self._generate_wealth_timing(
            chart_data, factors, current_dasha
        )
        
        # Generate synthesis
        synthesis_text = self._generate_wealth_synthesis(
            factors, normalized_score, strength_level, timing_info
        )
        
        # Generate assessment
        assessment = self._generate_overall_assessment(
            normalized_score, strength_level, factors
        )
        
        # Generate recommendations
        recommendations = self._generate_wealth_recommendations(
            factors, strength_level, timing_info
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(factors, len(sources_used))
        
        return WealthSynthesis(
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
    
    def _analyze_wealth_house(
        self,
        chart_data: Dict[str, Any],
        house_num: int,
        house_theme: str,
        current_dasha: Optional[str]
    ) -> WealthFactor:
        """Analyze wealth-relevant house"""
        
        planets_in_house = [
            p for p, data in chart_data.get("planets", {}).items()
            if data.get("house") == house_num
        ]
        
        house_lord = chart_data.get("house_lords", {}).get(house_num)
        
        score = 0
        interpretation_parts = []
        sources = []
        
        # Base score
        if house_num == 2:
            base_score = 20  # Primary wealth house
        elif house_num == 11:
            base_score = 20  # Primary gains house
        elif house_num == 5:
            base_score = 15  # Speculation/investments
        else:  # 9th house
            base_score = 15  # Fortune/inheritance
        
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
                
                # Benefics in wealth houses are excellent
                if planet in ["Jupiter", "Venus", "Mercury"]:
                    score += planet_score * 1.2
                elif planet == "Moon":
                    score += planet_score
                else:  # Malefics can give wealth through struggle
                    score += planet_score * 0.7
                
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
            
            # Wealth lords in wealth houses (2,5,9,11) or kendras (1,4,7,10) are good
            if lord_house in [1, 2, 4, 5, 7, 9, 10, 11]:
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
        
        return WealthFactor(
            factor_name=f"{house_num}th House - {house_theme}",
            house_or_planet=f"House {house_num}",
            contribution_score=int(final_score),
            strength_level=strength,
            interpretation=" | ".join(interpretation_parts),
            sources=list(set(sources)),
            timing_note=f"Effects manifest during {house_lord} dasha" if house_lord else None
        )
    
    def _analyze_wealth_karaka(
        self,
        chart_data: Dict[str, Any],
        planet: str,
        karaka_theme: str,
        current_dasha: Optional[str]
    ) -> Optional[WealthFactor]:
        """Analyze Jupiter (natural wealth karaka)"""
        
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
        
        # Jupiter as Dhana Karaka contributes significantly
        score = result.strength_assessment.strength_score / 5  # Max 20 points
        strength = result.strength_assessment.overall_strength.value
        
        return WealthFactor(
            factor_name=f"{planet} - Natural Karaka ({karaka_theme})",
            house_or_planet=planet,
            contribution_score=int(score),
            strength_level=strength,
            interpretation=result.synthesized_interpretation[:200] + "...",
            sources=result.sources_used,
            timing_note=f"Peak wealth effects during {planet} mahadasha"
        )
    
    def _analyze_wealth_yogas(
        self,
        active_yogas: List[str]
    ) -> List[WealthFactor]:
        """Analyze Dhana yogas (wealth-forming combinations)"""
        
        yoga_factors = []
        
        for yoga_name in active_yogas:
            is_wealth_yoga = any(
                keyword in yoga_name for keyword in self.wealth_yoga_keywords
            )
            
            if not is_wealth_yoga:
                continue
            
            yoga_data = self.all_yogas.get(yoga_name)
            if not yoga_data:
                continue
            
            # Dhana yogas contribute significantly to wealth
            if "Dhana" in yoga_name or "Lakshmi" in yoga_name:
                score = 15
            elif "Gaja_Kesari" in yoga_name:
                score = 12
            else:
                score = 10
            
            effects = yoga_data.get("effects", {})
            wealth_effect = effects.get("wealth", effects.get("general", ""))
            
            yoga_factors.append(WealthFactor(
                factor_name=f"Yoga: {yoga_name.replace('_', ' ')}",
                house_or_planet="Yoga",
                contribution_score=score,
                strength_level="strong",
                interpretation=wealth_effect[:150] + "...",
                sources=[f"BPHS Ch. {yoga_data.get('chapter', 0)}"],
                timing_note="Effects manifest during involved planets' dashas"
            ))
        
        return yoga_factors
    
    def _determine_wealth_strength(self, score: float) -> WealthStrength:
        """Determine wealth strength from score"""
        if score >= 90:
            return WealthStrength.EXCEPTIONAL
        elif score >= 75:
            return WealthStrength.VERY_STRONG
        elif score >= 60:
            return WealthStrength.STRONG
        elif score >= 40:
            return WealthStrength.MODERATE
        elif score >= 20:
            return WealthStrength.CHALLENGING
        else:
            return WealthStrength.DIFFICULT
    
    def _generate_wealth_timing(
        self,
        chart_data: Dict[str, Any],
        factors: List[WealthFactor],
        current_dasha: Optional[str]
    ) -> Dict[str, Any]:
        """Generate timing analysis for wealth"""
        
        timing = {
            "current_period": "",
            "wealth_gain_windows": [],
            "favorable_periods": []
        }
        
        if current_dasha:
            timing["current_period"] = (
                f"Currently in {current_dasha} mahadasha. "
                f"Wealth effects from {current_dasha}'s placement active now."
            )
        
        # Wealth timing indicators
        second_lord = chart_data.get("house_lords", {}).get(2)
        if second_lord:
            timing["wealth_gain_windows"].append(
                f"{second_lord} mahadasha (2nd lord period - family wealth)"
            )
        
        eleventh_lord = chart_data.get("house_lords", {}).get(11)
        if eleventh_lord:
            timing["wealth_gain_windows"].append(
                f"{eleventh_lord} mahadasha (11th lord period - gains)"
            )
        
        jupiter_data = chart_data.get("planets", {}).get("Jupiter", {})
        if jupiter_data:
            timing["wealth_gain_windows"].append(
                "Jupiter mahadasha (Dhana Karaka period)"
            )
        
        return timing
    
    def _generate_wealth_synthesis(
        self,
        factors: List[WealthFactor],
        score: float,
        strength: WealthStrength,
        timing: Dict[str, Any]
    ) -> str:
        """Generate complete wealth narrative"""
        
        parts = []
        
        parts.append(
            f"Wealth Analysis shows {strength.value.replace('_', ' ').title()} "
            f"potential (strength score: {score:.1f}/100)."
        )
        
        parts.append("\n\nKey Wealth Factors:")
        for factor in factors[:5]:
            parts.append(
                f"\n• {factor.factor_name} ({factor.contribution_score} points): "
                f"{factor.interpretation[:100]}..."
            )
        
        if timing.get("wealth_gain_windows"):
            parts.append("\n\nWealth Gain Windows:")
            for window in timing["wealth_gain_windows"][:3]:
                parts.append(f"\n• {window}")
        
        return "".join(parts)
    
    def _generate_overall_assessment(
        self,
        score: float,
        strength: WealthStrength,
        factors: List[WealthFactor]
    ) -> str:
        """Generate executive summary"""
        
        if strength == WealthStrength.EXCEPTIONAL:
            return (
                f"Exceptional wealth potential ({score:.1f}/100). "
                "Chart shows strong indicators for significant wealth accumulation, "
                "financial prosperity, and material abundance."
            )
        elif strength == WealthStrength.VERY_STRONG:
            return (
                f"Very strong wealth prospects ({score:.1f}/100). "
                "Significant potential for financial success and wealth building. "
                "Key wealth houses well-placed."
            )
        elif strength == WealthStrength.STRONG:
            return (
                f"Good wealth potential ({score:.1f}/100). "
                "Solid foundation for financial growth with favorable indicators. "
                "Success through consistent effort and wise investments."
            )
        elif strength == WealthStrength.MODERATE:
            return (
                f"Moderate wealth prospects ({score:.1f}/100). "
                "Average financial path with both opportunities and challenges. "
                "Success requires strategic planning and discipline."
            )
        elif strength == WealthStrength.CHALLENGING:
            return (
                f"Challenging wealth indicators ({score:.1f}/100). "
                "Financial path may face obstacles requiring extra effort. "
                "Focus on savings and timing."
            )
        else:
            return (
                f"Difficult wealth configuration ({score:.1f}/100). "
                "Significant financial challenges indicated. "
                "Careful planning and remedial measures recommended."
            )
    
    def _generate_wealth_recommendations(
        self,
        factors: List[WealthFactor],
        strength: WealthStrength,
        timing: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable wealth recommendations"""
        
        recommendations = []
        
        if strength in [WealthStrength.EXCEPTIONAL, WealthStrength.VERY_STRONG]:
            recommendations.append(
                "Pursue wealth-building opportunities during favorable dasha periods"
            )
            recommendations.append(
                "Consider investments and business ventures - chart supports financial growth"
            )
            recommendations.append(
                "Leverage strong Jupiter/wealth houses for prosperity"
            )
        elif strength == WealthStrength.STRONG:
            recommendations.append(
                "Focus on steady wealth accumulation through savings and investments"
            )
            recommendations.append(
                "Build multiple income streams for financial security"
            )
        else:
            recommendations.append(
                "Prioritize financial discipline and careful budgeting"
            )
            recommendations.append(
                "Avoid speculation - focus on stable income sources"
            )
            recommendations.append(
                "Strengthen Jupiter through remedial measures for wealth"
            )
        
        if timing.get("wealth_gain_windows"):
            recommendations.append(
                f"Optimal wealth timing: {timing['wealth_gain_windows'][0]}"
            )
        
        return recommendations[:5]
    
    def _calculate_confidence(
        self,
        factors: List[WealthFactor],
        sources_count: int
    ) -> float:
        """Calculate confidence in analysis"""
        
        base_confidence = 0.85
        
        if len(factors) >= 6:
            base_confidence += 0.05
        
        if sources_count >= 10:
            base_confidence += 0.05
        
        return min(0.98, base_confidence)
