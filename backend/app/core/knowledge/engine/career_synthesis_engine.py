"""
Career Synthesis Engine
========================

Holistic career analysis synthesizing entire chart sections:
- 10th house (career/status) + lord + occupying planets
- 6th house (service/competition) + planets
- 2nd house (income/speech) + planets
- Sun & Saturn (natural career karakas)
- All career-relevant yogas
- Current dasha effects on career
- Timing windows for career changes

Evolution from single planet interpretation to complete life-area synthesis.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from backend.app.core.knowledge.engine.contextual_synthesis_engine import (
    ContextualSynthesisEngine,
    StrengthLevel
)
from backend.app.core.knowledge.sources.bphs_yogas import get_all_yogas


class CareerStrength(Enum):
    """Career potential strength levels"""
    EXCEPTIONAL = "exceptional"      # 90-100: Outstanding career potential
    VERY_STRONG = "very_strong"      # 75-89: Strong career success likely
    STRONG = "strong"                # 60-74: Good career prospects
    MODERATE = "moderate"            # 40-59: Average career path
    CHALLENGING = "challenging"      # 20-39: Career obstacles present
    DIFFICULT = "difficult"          # 0-19: Significant career challenges


@dataclass
class CareerFactor:
    """Single factor contributing to career analysis"""
    factor_name: str
    house_or_planet: str
    contribution_score: int  # Points toward total (0-100)
    strength_level: str
    interpretation: str
    sources: List[str]
    timing_note: Optional[str] = None


@dataclass
class CareerTimingWindow:
    """Timing window for career events"""
    period_name: str
    start_indicator: str  # e.g., "Jupiter mahadasha begins"
    duration: str
    likelihood: str  # "high", "moderate", "low"
    specific_effects: List[str]
    confidence: float


@dataclass
class CareerSynthesis:
    """Complete career life-area analysis"""
    overall_assessment: str
    strength_score: float  # 0-100 aggregate
    strength_level: CareerStrength
    domain: str = "career"
    
    key_factors: List[CareerFactor]
    synthesis: str  # Complete narrative
    
    timing: Dict[str, Any]
    recommendations: List[str]
    
    sources_consulted: int
    sources: List[str]
    confidence: float


class CareerSynthesisEngine:
    """
    Engine for holistic career analysis.
    
    Aggregates analysis from:
    1. 10th house (career/status/profession)
    2. 6th house (service/competition/daily work)
    3. 2nd house (income/speech/resources)
    4. Sun (natural career karaka - authority)
    5. Saturn (natural career karaka - service/discipline)
    6. Career-relevant yogas (Raja, Dharma-Karma, profession-specific)
    7. Current dasha effects on career houses
    8. Timing windows for career changes
    """
    
    def __init__(self):
        self.contextual_engine = ContextualSynthesisEngine()
        self.all_yogas = get_all_yogas()
        
        # Career-relevant yoga categories
        self.career_yoga_keywords = [
            "Raja", "Dharma_Karma", "Amala", "Budha_Aditya",
            "Gaja_Kesari", "Hamsa", "Ruchaka", "Bhadra"
        ]
    
    def synthesize_career_analysis(
        self,
        chart_data: Dict[str, Any],
        current_dasha: Optional[str] = None
    ) -> CareerSynthesis:
        """
        Generate complete career life-area analysis.
        
        Args:
            chart_data: Complete chart information including:
                - planets: {planet_name: {house, sign, dignity}}
                - house_lords: {house_num: planet_name}
                - active_yogas: [yoga_names]
            current_dasha: Current mahadasha planet
            
        Returns:
            CareerSynthesis with complete analysis
        """
        factors = []
        sources_used = set()
        total_score = 0
        
        # 1. Analyze 10th house (primary career indicator)
        tenth_house_factor = self._analyze_career_house(
            chart_data, 10, "Career & Status", current_dasha
        )
        factors.append(tenth_house_factor)
        total_score += tenth_house_factor.contribution_score
        sources_used.update(tenth_house_factor.sources)
        
        # 2. Analyze 6th house (service/competition)
        sixth_house_factor = self._analyze_career_house(
            chart_data, 6, "Service & Competition", current_dasha
        )
        factors.append(sixth_house_factor)
        total_score += sixth_house_factor.contribution_score
        sources_used.update(sixth_house_factor.sources)
        
        # 3. Analyze 2nd house (income/resources)
        second_house_factor = self._analyze_career_house(
            chart_data, 2, "Income & Resources", current_dasha
        )
        factors.append(second_house_factor)
        total_score += second_house_factor.contribution_score
        sources_used.update(second_house_factor.sources)
        
        # 4. Analyze Sun (natural career karaka)
        sun_factor = self._analyze_career_karaka(
            chart_data, "Sun", "Authority & Leadership", current_dasha
        )
        if sun_factor:
            factors.append(sun_factor)
            total_score += sun_factor.contribution_score
            sources_used.update(sun_factor.sources)
        
        # 5. Analyze Saturn (natural career karaka)
        saturn_factor = self._analyze_career_karaka(
            chart_data, "Saturn", "Service & Discipline", current_dasha
        )
        if saturn_factor:
            factors.append(saturn_factor)
            total_score += saturn_factor.contribution_score
            sources_used.update(saturn_factor.sources)
        
        # 6. Analyze career yogas
        yoga_factors = self._analyze_career_yogas(
            chart_data.get("active_yogas", [])
        )
        for yoga_factor in yoga_factors:
            factors.append(yoga_factor)
            total_score += yoga_factor.contribution_score
            sources_used.update(yoga_factor.sources)
        
        # Normalize score to 0-100
        max_possible = 100
        normalized_score = min(100, (total_score / max_possible) * 100)
        
        # Determine strength level
        strength_level = self._determine_career_strength(normalized_score)
        
        # Generate timing analysis
        timing_info = self._generate_career_timing(
            chart_data, factors, current_dasha
        )
        
        # Generate synthesis narrative
        synthesis_text = self._generate_career_synthesis(
            factors, normalized_score, strength_level, timing_info
        )
        
        # Generate overall assessment
        assessment = self._generate_overall_assessment(
            normalized_score, strength_level, factors
        )
        
        # Generate recommendations
        recommendations = self._generate_career_recommendations(
            factors, strength_level, timing_info
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(factors, len(sources_used))
        
        return CareerSynthesis(
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
    
    def _analyze_career_house(
        self,
        chart_data: Dict[str, Any],
        house_num: int,
        house_theme: str,
        current_dasha: Optional[str]
    ) -> CareerFactor:
        """Analyze a career-relevant house"""
        planets_in_house = [
            p for p, data in chart_data.get("planets", {}).items()
            if data.get("house") == house_num
        ]
        
        house_lord = chart_data.get("house_lords", {}).get(house_num)
        
        score = 0
        interpretation_parts = []
        sources = []
        
        # Base score for house
        if house_num == 10:
            base_score = 30  # Most important for career
        elif house_num == 6:
            base_score = 15  # Important for service/work
        else:  # 2nd house
            base_score = 15  # Important for income
        
        # Analyze planets in house
        if planets_in_house:
            for planet in planets_in_house:
                planet_data = chart_data["planets"][planet]
                dignity = planet_data.get("dignity", "neutral")
                
                # Get contextual interpretation
                result = self.contextual_engine.synthesize_interpretation(
                    planet=planet,
                    house=house_num,
                    sign=planet_data.get("sign", ""),
                    dignity=dignity,
                    current_dasha=current_dasha
                )
                
                # Add to score based on strength
                planet_score = result.strength_assessment.strength_score / 10
                score += planet_score
                
                interpretation_parts.append(
                    f"{planet} in {house_num}th ({dignity}): "
                    f"{result.base_interpretation.get('general_effects', '')[:100]}..."
                )
                sources.extend(result.sources_used)
        else:
            interpretation_parts.append(f"No planets in {house_num}th house")
        
        # Analyze house lord
        if house_lord:
            lord_data = chart_data["planets"].get(house_lord, {})
            lord_house = lord_data.get("house", 0)
            
            # House lord placement affects career
            if lord_house in [1, 4, 5, 7, 9, 10, 11]:  # Favorable houses
                score += 5
                interpretation_parts.append(
                    f"{house_num}th lord {house_lord} in {lord_house}th (favorable)"
                )
            elif lord_house in [6, 8, 12]:  # Challenging houses
                score -= 3
                interpretation_parts.append(
                    f"{house_num}th lord {house_lord} in {lord_house}th (challenging)"
                )
        
        final_score = max(0, min(base_score, base_score + score))
        
        strength = "strong" if final_score > base_score * 0.7 else "moderate" if final_score > base_score * 0.4 else "weak"
        
        return CareerFactor(
            factor_name=f"{house_num}th House - {house_theme}",
            house_or_planet=f"House {house_num}",
            contribution_score=int(final_score),
            strength_level=strength,
            interpretation=" | ".join(interpretation_parts),
            sources=list(set(sources)),
            timing_note=f"Effects manifest during {house_lord} dasha" if house_lord else None
        )
    
    def _analyze_career_karaka(
        self,
        chart_data: Dict[str, Any],
        planet: str,
        karaka_theme: str,
        current_dasha: Optional[str]
    ) -> Optional[CareerFactor]:
        """Analyze natural career karaka (Sun or Saturn)"""
        planet_data = chart_data.get("planets", {}).get(planet)
        if not planet_data:
            return None
        
        house = planet_data.get("house")
        sign = planet_data.get("sign", "")
        dignity = planet_data.get("dignity", "neutral")
        
        # Get contextual interpretation
        result = self.contextual_engine.synthesize_interpretation(
            planet=planet,
            house=house,
            sign=sign,
            dignity=dignity,
            current_dasha=current_dasha
        )
        
        # Karaka strength contributes to career
        score = result.strength_assessment.strength_score / 5  # Max 20 points
        
        strength = result.strength_assessment.overall_strength.value
        
        return CareerFactor(
            factor_name=f"{planet} - Natural Karaka ({karaka_theme})",
            house_or_planet=planet,
            contribution_score=int(score),
            strength_level=strength,
            interpretation=result.synthesized_interpretation[:200] + "...",
            sources=result.sources_used,
            timing_note=f"Peak effects during {planet} mahadasha"
        )
    
    def _analyze_career_yogas(
        self,
        active_yogas: List[str]
    ) -> List[CareerFactor]:
        """Analyze career-relevant yogas"""
        yoga_factors = []
        
        for yoga_name in active_yogas:
            # Check if yoga is career-relevant
            is_career_yoga = any(
                keyword in yoga_name for keyword in self.career_yoga_keywords
            )
            
            if not is_career_yoga:
                continue
            
            yoga_data = self.all_yogas.get(yoga_name)
            if not yoga_data:
                continue
            
            # Career yogas contribute significantly
            if "Raja" in yoga_name or "Dharma_Karma" in yoga_name:
                score = 15
            elif "Mahapurusha" in yoga_name:
                score = 12
            else:
                score = 8
            
            effects = yoga_data.get("effects", {})
            career_effect = effects.get("career", effects.get("general", ""))
            
            yoga_factors.append(CareerFactor(
                factor_name=f"Yoga: {yoga_name.replace('_', ' ')}",
                house_or_planet="Yoga",
                contribution_score=score,
                strength_level="strong",
                interpretation=career_effect[:150] + "...",
                sources=[f"BPHS Ch. {yoga_data.get('chapter', 0)}"],
                timing_note="Effects manifest during involved planets' dashas"
            ))
        
        return yoga_factors
    
    def _determine_career_strength(self, score: float) -> CareerStrength:
        """Determine career strength level from score"""
        if score >= 90:
            return CareerStrength.EXCEPTIONAL
        elif score >= 75:
            return CareerStrength.VERY_STRONG
        elif score >= 60:
            return CareerStrength.STRONG
        elif score >= 40:
            return CareerStrength.MODERATE
        elif score >= 20:
            return CareerStrength.CHALLENGING
        else:
            return CareerStrength.DIFFICULT
    
    def _generate_career_timing(
        self,
        chart_data: Dict[str, Any],
        factors: List[CareerFactor],
        current_dasha: Optional[str]
    ) -> Dict[str, Any]:
        """Generate timing analysis for career"""
        timing = {
            "current_period": "",
            "peak_periods": [],
            "favorable_transits": [],
            "career_change_windows": []
        }
        
        # Current period analysis
        if current_dasha:
            timing["current_period"] = (
                f"Currently in {current_dasha} mahadasha. "
                f"Career effects from {current_dasha}'s placement are active now."
            )
        
        # Identify peak periods from factors
        for factor in factors:
            if factor.timing_note and "dasha" in factor.timing_note.lower():
                timing["peak_periods"].append(factor.timing_note)
        
        # Generic favorable transits (would be calculated with ephemeris)
        timing["favorable_transits"] = [
            "Jupiter transit through 10th house (career expansion)",
            "Saturn transit through 10th house (career consolidation)",
            "Jupiter-Saturn conjunction (major career shifts)"
        ]
        
        return timing
    
    def _generate_career_synthesis(
        self,
        factors: List[CareerFactor],
        score: float,
        strength: CareerStrength,
        timing: Dict[str, Any]
    ) -> str:
        """Generate complete career narrative"""
        parts = []
        
        # Opening with overall strength
        parts.append(
            f"Career Analysis shows {strength.value.replace('_', ' ').title()} "
            f"potential (strength score: {score:.1f}/100)."
        )
        
        # Key factors
        parts.append("\n\nKey Career Factors:")
        for factor in factors[:5]:  # Top 5 factors
            parts.append(
                f"\n• {factor.factor_name} ({factor.contribution_score} points): "
                f"{factor.interpretation[:100]}..."
            )
        
        # Timing
        if timing.get("peak_periods"):
            parts.append("\n\nCareer Peak Periods:")
            for period in timing["peak_periods"][:3]:
                parts.append(f"\n• {period}")
        
        return "".join(parts)
    
    def _generate_overall_assessment(
        self,
        score: float,
        strength: CareerStrength,
        factors: List[CareerFactor]
    ) -> str:
        """Generate executive summary assessment"""
        if strength == CareerStrength.EXCEPTIONAL:
            return (
                f"Exceptional career potential ({score:.1f}/100). "
                "Chart shows strong indicators for outstanding professional success, "
                "leadership positions, and recognition. Multiple favorable factors align."
            )
        elif strength == CareerStrength.VERY_STRONG:
            return (
                f"Very strong career prospects ({score:.1f}/100). "
                "Significant potential for professional achievement and advancement. "
                "Key career houses and karakas well-placed."
            )
        elif strength == CareerStrength.STRONG:
            return (
                f"Good career potential ({score:.1f}/100). "
                "Solid foundation for professional growth with favorable indicators. "
                "Success through consistent effort."
            )
        elif strength == CareerStrength.MODERATE:
            return (
                f"Moderate career prospects ({score:.1f}/100). "
                "Average career path with both opportunities and challenges. "
                "Success requires strategic planning."
            )
        elif strength == CareerStrength.CHALLENGING:
            return (
                f"Challenging career indicators ({score:.1f}/100). "
                "Career path may face obstacles requiring extra effort. "
                "Focus on strengths and timing."
            )
        else:
            return (
                f"Difficult career configuration ({score:.1f}/100). "
                "Significant career challenges indicated. "
                "Remedial measures and alternative paths recommended."
            )
    
    def _generate_career_recommendations(
        self,
        factors: List[CareerFactor],
        strength: CareerStrength,
        timing: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable career recommendations"""
        recommendations = []
        
        # Based on strength level
        if strength in [CareerStrength.EXCEPTIONAL, CareerStrength.VERY_STRONG]:
            recommendations.append(
                "Pursue leadership and high-responsibility roles - chart supports authority"
            )
            recommendations.append(
                "Consider entrepreneurship or independent professional practice"
            )
        elif strength == CareerStrength.STRONG:
            recommendations.append(
                "Focus on steady career advancement through demonstrated competence"
            )
            recommendations.append(
                "Build professional network and seek mentorship"
            )
        else:
            recommendations.append(
                "Develop specialized skills to overcome career obstacles"
            )
            recommendations.append(
                "Consider service-oriented or technical professions"
            )
        
        # Timing-based recommendations
        if timing.get("peak_periods"):
            recommendations.append(
                f"Plan major career moves during: {timing['peak_periods'][0]}"
            )
        
        # Factor-specific recommendations
        for factor in factors:
            if "10th" in factor.factor_name and factor.strength_level == "strong":
                recommendations.append(
                    "Leverage strong 10th house for public-facing roles"
                )
                break
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _calculate_confidence(
        self,
        factors: List[CareerFactor],
        sources_count: int
    ) -> float:
        """Calculate confidence in analysis"""
        base_confidence = 0.85
        
        # Boost for multiple factors
        if len(factors) >= 6:
            base_confidence += 0.05
        
        # Boost for multiple sources
        if sources_count >= 10:
            base_confidence += 0.05
        
        return min(0.98, base_confidence)
