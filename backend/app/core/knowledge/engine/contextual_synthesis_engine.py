"""
Contextual Synthesis Engine
============================

Multi-factor interpretation synthesis combining:
- Planet placement (house + sign + dignity)
- Planetary lordship (which houses the planet rules)
- Aspects from other planets
- Active yogas involving this planet
- Dasha period effects (current/upcoming)

Transforms from: "Sun in 10th house"
To: "Sun (exalted) in 10th as 9th lord + Jupiter aspect + Dharma-Karma Yoga"
    with complete synthesis from all classical sources
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass

from app.core.knowledge.engine.interpretation_engine import KnowledgeInterpretationEngine
from app.core.knowledge.engine.multi_source_engine import MultiSourceEngine
from app.core.knowledge.sources.bphs_yogas import get_all_yogas


class ContextualFactor(Enum):
    """Types of contextual factors in synthesis"""
    HOUSE_PLACEMENT = "house_placement"
    SIGN_DIGNITY = "sign_dignity"
    LORDSHIP = "lordship"
    ASPECTS = "aspects"
    YOGAS = "yogas"
    DASHA_PERIOD = "dasha_period"


class StrengthLevel(Enum):
    """Overall strength assessment levels"""
    EXCEPTIONAL = "exceptional"  # 90-100%
    VERY_STRONG = "very_strong"  # 75-89%
    STRONG = "strong"  # 60-74%
    MODERATE = "moderate"  # 40-59%
    WEAK = "weak"  # 20-39%
    DEBILITATED = "debilitated"  # 0-19%


@dataclass
class ContextualFactor:
    """Single contextual factor in interpretation"""
    factor_type: str
    value: Any
    weight: float  # 0.0-1.0 importance weight
    influence: str  # "positive", "negative", "neutral", "mixed"
    description: str


@dataclass
class StrengthAssessment:
    """Comprehensive strength assessment"""
    overall_strength: StrengthLevel
    strength_score: float  # 0-100
    dignity_score: float
    house_score: float
    aspect_score: float
    yoga_score: float
    factors_contributing: List[str]
    factors_weakening: List[str]


@dataclass
class ContextualInterpretation:
    """Complete contextual interpretation result"""
    planet: str
    house: int
    sign: str
    
    # Individual factor interpretations
    base_interpretation: Dict[str, Any]
    lordship_effects: Optional[Dict[str, Any]]
    aspect_effects: List[Dict[str, Any]]
    yoga_effects: List[Dict[str, Any]]
    dasha_modulation: Optional[Dict[str, Any]]
    
    # Synthesis
    strength_assessment: StrengthAssessment
    synthesized_interpretation: str
    key_themes: List[str]
    timing_notes: List[str]
    
    # Multi-source comparison
    source_comparison: Optional[Dict[str, Any]]
    
    # Metadata
    confidence_score: float
    factors_analyzed: List[str]
    sources_used: List[str]


class ContextualSynthesisEngine:
    """
    Engine for contextual interpretation synthesis.
    
    Combines multiple factors to create holistic interpretation:
    1. Base planet-in-house interpretation
    2. Sign and dignity effects
    3. Lordship implications
    4. Aspect influences
    5. Yoga formations
    6. Current dasha period effects
    """
    
    def __init__(self):
        self.knowledge_engine = KnowledgeInterpretationEngine()
        self.multi_source_engine = MultiSourceEngine()
        self.all_yogas = get_all_yogas()
    
    def synthesize_interpretation(
        self,
        planet: str,
        house: int,
        sign: str,
        dignity: str = "neutral",
        lordship_houses: Optional[List[int]] = None,
        aspects: Optional[List[Dict[str, Any]]] = None,
        active_yogas: Optional[List[str]] = None,
        current_dasha: Optional[str] = None
    ) -> ContextualInterpretation:
        """
        Generate complete contextual interpretation.
        
        Args:
            planet: Planet name
            house: House number (1-12)
            sign: Sign name
            dignity: Planetary dignity (exalted, own_sign, friendly, neutral, enemy, debilitated)
            lordship_houses: Which houses this planet rules (e.g., [9, 10] for Jupiter ruling 9th and 10th)
            aspects: List of aspects from other planets
            active_yogas: List of yoga names this planet participates in
            current_dasha: Current mahadasha planet
            
        Returns:
            ContextualInterpretation with complete synthesis
        """
        # 1. Get base interpretation
        base = self.knowledge_engine.interpret_planet_in_house(
            planet=planet,
            house=house,
            sign=sign,
            dignity=dignity
        )
        
        base_dict = {
            "general_effects": base.general_effects,
            "confidence": base.metadata.confidence_score,
            "sources": base.sources.get_all_citations()
        }
        
        # 2. Multi-source comparison if available
        source_comparison = None
        sources_available = self.multi_source_engine.get_available_sources(planet, house)
        if len(sources_available) > 1:
            comparison = self.multi_source_engine.compare_sources(planet, house)
            source_comparison = {
                "agreement_level": comparison.agreement_level.value,
                "common_themes": comparison.common_themes,
                "synthesis": comparison.synthesis,
                "confidence": comparison.confidence_score
            }
        
        # 3. Analyze lordship effects
        lordship_effects = None
        if lordship_houses:
            lordship_effects = self._analyze_lordship(planet, house, lordship_houses)
        
        # 4. Analyze aspects
        aspect_effects = []
        if aspects:
            aspect_effects = self._analyze_aspects(planet, house, aspects)
        
        # 5. Analyze yoga effects
        yoga_effects = []
        if active_yogas:
            yoga_effects = self._analyze_yogas(planet, active_yogas)
        
        # 6. Dasha modulation
        dasha_modulation = None
        if current_dasha:
            dasha_modulation = self._analyze_dasha_effect(planet, current_dasha, house)
        
        # 7. Assess overall strength
        strength = self._assess_strength(
            planet, house, sign, dignity,
            lordship_houses, aspects, active_yogas
        )
        
        # 8. Synthesize all factors
        synthesis = self._synthesize_all_factors(
            planet, house, sign, dignity,
            base_dict, lordship_effects, aspect_effects,
            yoga_effects, dasha_modulation, strength
        )
        
        # 9. Extract key themes
        key_themes = self._extract_key_themes(
            base_dict, lordship_effects, aspect_effects, yoga_effects
        )
        
        # 10. Generate timing notes
        timing_notes = self._generate_timing_notes(
            planet, dasha_modulation, yoga_effects
        )
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(
            base_dict, source_comparison, lordship_effects,
            aspect_effects, yoga_effects
        )
        
        # Determine factors analyzed
        factors = ["house_placement", "sign_dignity"]
        if lordship_houses:
            factors.append("lordship")
        if aspects:
            factors.append("aspects")
        if active_yogas:
            factors.append("yogas")
        if current_dasha:
            factors.append("dasha_period")
        
        # Collect sources
        sources = base_dict["sources"]
        if source_comparison:
            sources.extend(["Saravali (multi-source)"])
        if yoga_effects:
            sources.extend([f"BPHS Ch {y['chapter']}" for y in yoga_effects])
        sources = list(set(sources))  # Deduplicate
        
        return ContextualInterpretation(
            planet=planet,
            house=house,
            sign=sign,
            base_interpretation=base_dict,
            lordship_effects=lordship_effects,
            aspect_effects=aspect_effects,
            yoga_effects=yoga_effects,
            dasha_modulation=dasha_modulation,
            strength_assessment=strength,
            synthesized_interpretation=synthesis,
            key_themes=key_themes,
            timing_notes=timing_notes,
            source_comparison=source_comparison,
            confidence_score=confidence,
            factors_analyzed=factors,
            sources_used=sources
        )
    
    def _analyze_lordship(
        self,
        planet: str,
        current_house: int,
        lordship_houses: List[int]
    ) -> Dict[str, Any]:
        """Analyze effects of planetary lordship"""
        effects = {
            "ruling_houses": lordship_houses,
            "house_connections": [],
            "strength_note": ""
        }
        
        # Analyze each house ruled
        for ruled_house in lordship_houses:
            house_theme = self._get_house_theme(ruled_house)
            connection = f"Rules {ruled_house}th house ({house_theme})"
            
            # Check if ruling benefic houses (1,5,9 - trikonas)
            if ruled_house in [1, 5, 9]:
                connection += " - trikona lord (highly auspicious)"
            # Check if ruling angular houses (1,4,7,10)
            elif ruled_house in [4, 7, 10]:
                connection += " - kendra lord (strong)"
            # Check if ruling dusthana (6,8,12)
            elif ruled_house in [6, 8, 12]:
                connection += " - dusthana lord (challenging)"
            
            effects["house_connections"].append(connection)
        
        # Assess lordship strength
        if any(h in [1, 5, 9] for h in lordship_houses):
            effects["strength_note"] = "Strong - rules trikona house(s)"
        elif any(h in [4, 7, 10] for h in lordship_houses):
            effects["strength_note"] = "Good - rules kendra house(s)"
        else:
            effects["strength_note"] = "Neutral lordship"
        
        return effects
    
    def _analyze_aspects(
        self,
        planet: str,
        house: int,
        aspects: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze effects of aspects from other planets"""
        aspect_effects = []
        
        for aspect in aspects:
            aspecting_planet = aspect.get("planet", "Unknown")
            aspect_type = aspect.get("type", "full")  # full, 5th, 7th, 9th
            
            effect = {
                "aspecting_planet": aspecting_planet,
                "aspect_type": aspect_type,
                "influence": self._determine_aspect_influence(aspecting_planet, planet),
                "note": f"{aspecting_planet} aspects via {aspect_type} aspect"
            }
            
            aspect_effects.append(effect)
        
        return aspect_effects
    
    def _analyze_yogas(
        self,
        planet: str,
        active_yogas: List[str]
    ) -> List[Dict[str, Any]]:
        """Analyze effects of yogas involving this planet"""
        yoga_effects = []
        
        for yoga_name in active_yogas:
            yoga_data = self.all_yogas.get(yoga_name)
            if yoga_data:
                effect = {
                    "yoga_name": yoga_name,
                    "category": yoga_data.get("category", "Unknown"),
                    "chapter": yoga_data.get("chapter", 0),
                    "formation": yoga_data.get("formation", ""),
                    "key_effects": self._extract_yoga_key_effects(yoga_data),
                    "strength": "strong"  # Could be calculated based on formation quality
                }
                yoga_effects.append(effect)
        
        return yoga_effects
    
    def _analyze_dasha_effect(
        self,
        planet: str,
        current_dasha: str,
        house: int
    ) -> Dict[str, Any]:
        """Analyze how current dasha modulates interpretation"""
        modulation = {
            "current_dasha": current_dasha,
            "relationship": "",
            "timing_note": ""
        }
        
        if current_dasha == planet:
            modulation["relationship"] = "self_dasha"
            modulation["timing_note"] = f"Currently in {planet} mahadasha - these effects are strongly active now"
        else:
            modulation["relationship"] = "other_dasha"
            modulation["timing_note"] = f"Effects will manifest strongly during {planet} mahadasha period"
        
        return modulation
    
    def _assess_strength(
        self,
        planet: str,
        house: int,
        sign: str,
        dignity: str,
        lordship_houses: Optional[List[int]],
        aspects: Optional[List[Dict[str, Any]]],
        active_yogas: Optional[List[str]]
    ) -> StrengthAssessment:
        """Comprehensive strength assessment"""
        
        # Dignity score (0-40 points)
        dignity_map = {
            "exalted": 40,
            "moolatrikona": 35,
            "own_sign": 30,
            "friendly": 20,
            "neutral": 15,
            "enemy": 5,
            "debilitated": 0
        }
        dignity_score = dignity_map.get(dignity, 15)
        
        # House score (0-25 points)
        house_scores = {
            1: 25, 4: 22, 5: 23, 7: 22, 9: 24, 10: 25,  # Strong houses
            2: 18, 3: 15, 11: 20,  # Moderate
            6: 10, 8: 8, 12: 12  # Challenging
        }
        house_score = house_scores.get(house, 15)
        
        # Aspect score (0-15 points)
        aspect_score = 0
        if aspects:
            benefic_aspects = sum(1 for a in aspects if self._is_benefic(a.get("planet", "")))
            malefic_aspects = sum(1 for a in aspects if self._is_malefic(a.get("planet", "")))
            aspect_score = min(15, (benefic_aspects * 5) - (malefic_aspects * 3))
            aspect_score = max(0, aspect_score)
        
        # Yoga score (0-20 points)
        yoga_score = 0
        if active_yogas:
            raja_yogas = sum(1 for y in active_yogas if "Raja" in y or "Dharma_Karma" in y)
            dhana_yogas = sum(1 for y in active_yogas if "Dhana" in y or "Lakshmi" in y)
            yoga_score = min(20, (raja_yogas * 8) + (dhana_yogas * 6) + (len(active_yogas) * 2))
        
        # Total strength (0-100)
        total_strength = dignity_score + house_score + aspect_score + yoga_score
        
        # Determine level
        if total_strength >= 90:
            level = StrengthLevel.EXCEPTIONAL
        elif total_strength >= 75:
            level = StrengthLevel.VERY_STRONG
        elif total_strength >= 60:
            level = StrengthLevel.STRONG
        elif total_strength >= 40:
            level = StrengthLevel.MODERATE
        elif total_strength >= 20:
            level = StrengthLevel.WEAK
        else:
            level = StrengthLevel.DEBILITATED
        
        # Contributing factors
        contributing = []
        weakening = []
        
        if dignity_score >= 30:
            contributing.append(f"{dignity.replace('_', ' ').title()} dignity")
        elif dignity_score < 10:
            weakening.append(f"{dignity.replace('_', ' ').title()} dignity")
        
        if house_score >= 22:
            contributing.append(f"Excellent house placement ({house}th)")
        elif house_score < 12:
            weakening.append(f"Challenging house ({house}th)")
        
        if yoga_score > 10:
            contributing.append(f"Participates in {len(active_yogas) if active_yogas else 0} yoga(s)")
        
        return StrengthAssessment(
            overall_strength=level,
            strength_score=round(total_strength, 1),
            dignity_score=dignity_score,
            house_score=house_score,
            aspect_score=aspect_score,
            yoga_score=yoga_score,
            factors_contributing=contributing,
            factors_weakening=weakening if weakening else ["None identified"]
        )
    
    def _synthesize_all_factors(
        self,
        planet: str,
        house: int,
        sign: str,
        dignity: str,
        base: Dict[str, Any],
        lordship: Optional[Dict[str, Any]],
        aspects: List[Dict[str, Any]],
        yogas: List[Dict[str, Any]],
        dasha: Optional[Dict[str, Any]],
        strength: StrengthAssessment
    ) -> str:
        """Synthesize all factors into coherent interpretation"""
        
        synthesis_parts = []
        
        # Opening with strength assessment
        synthesis_parts.append(
            f"{planet} in {house}th house ({sign}) shows {strength.overall_strength.value} "
            f"strength (score: {strength.strength_score}/100)."
        )
        
        # Base interpretation
        synthesis_parts.append(f"\n\nCore Effects: {base['general_effects']}")
        
        # Lordship
        if lordship:
            synthesis_parts.append(
                f"\n\nLordship Context: {lordship['strength_note']}. "
                f"{' '.join(lordship['house_connections'])}"
            )
        
        # Yogas
        if yogas:
            yoga_names = [y['yoga_name'].replace('_', ' ') for y in yogas]
            synthesis_parts.append(
                f"\n\nActive Yogas: Participates in {', '.join(yoga_names)}. "
                f"These combinations significantly enhance results."
            )
        
        # Aspects
        if aspects:
            benefic_count = sum(1 for a in aspects if a['influence'] == 'positive')
            if benefic_count > 0:
                synthesis_parts.append(
                    f"\n\nBenefic Influences: Receives {benefic_count} positive aspect(s), "
                    f"supporting favorable outcomes."
                )
        
        # Timing
        if dasha:
            synthesis_parts.append(f"\n\nTiming: {dasha['timing_note']}")
        
        return ''.join(synthesis_parts)
    
    def _extract_key_themes(
        self,
        base: Dict[str, Any],
        lordship: Optional[Dict[str, Any]],
        aspects: List[Dict[str, Any]],
        yogas: List[Dict[str, Any]]
    ) -> List[str]:
        """Extract key themes from all factors"""
        themes = []
        
        # Add yoga categories as themes
        if yogas:
            for yoga in yogas:
                category = yoga.get('category', '')
                if category and category not in themes:
                    themes.append(category)
        
        # Add lordship themes
        if lordship and lordship.get('ruling_houses'):
            for house_num in lordship['ruling_houses']:
                theme = self._get_house_theme(house_num)
                if theme not in themes:
                    themes.append(theme)
        
        return themes[:5]  # Top 5 themes
    
    def _generate_timing_notes(
        self,
        planet: str,
        dasha: Optional[Dict[str, Any]],
        yogas: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate timing-related notes"""
        notes = []
        
        if dasha:
            notes.append(dasha['timing_note'])
        
        if yogas:
            notes.append(
                f"Yoga effects manifest primarily during {planet} dasha period "
                f"and sub-periods"
            )
        
        return notes
    
    def _calculate_confidence(
        self,
        base: Dict[str, Any],
        source_comparison: Optional[Dict[str, Any]],
        lordship: Optional[Dict[str, Any]],
        aspects: List[Dict[str, Any]],
        yogas: List[Dict[str, Any]]
    ) -> float:
        """Calculate overall confidence score"""
        base_confidence = base.get('confidence', 0.90)
        
        # Boost for multi-source agreement
        if source_comparison and source_comparison.get('confidence', 0) > 0.85:
            base_confidence = min(0.98, base_confidence + 0.03)
        
        # Boost for yoga participation
        if yogas:
            base_confidence = min(0.98, base_confidence + (len(yogas) * 0.01))
        
        return round(base_confidence, 2)
    
    # Helper methods
    def _get_house_theme(self, house: int) -> str:
        """Get primary theme for house"""
        themes = {
            1: "Self/Personality", 2: "Wealth/Family", 3: "Siblings/Courage",
            4: "Home/Mother", 5: "Children/Intelligence", 6: "Health/Service",
            7: "Partnerships", 8: "Transformation", 9: "Fortune/Dharma",
            10: "Career/Status", 11: "Gains/Network", 12: "Spirituality/Loss"
        }
        return themes.get(house, "Unknown")
    
    def _determine_aspect_influence(self, aspecting: str, aspected: str) -> str:
        """Determine if aspect is positive, negative, or neutral"""
        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
        malefics = ["Saturn", "Mars", "Sun", "Rahu", "Ketu"]
        
        if aspecting in benefics:
            return "positive"
        elif aspecting in malefics:
            return "negative"
        return "neutral"
    
    def _is_benefic(self, planet: str) -> bool:
        return planet in ["Jupiter", "Venus", "Mercury", "Moon"]
    
    def _is_malefic(self, planet: str) -> bool:
        return planet in ["Saturn", "Mars", "Sun", "Rahu", "Ketu"]
    
    def _extract_yoga_key_effects(self, yoga_data: Dict[str, Any]) -> str:
        """Extract key effects from yoga data"""
        effects = yoga_data.get('effects', {})
        if isinstance(effects, dict):
            general = effects.get('general', '')
            if general:
                return general[:150] + "..." if len(general) > 150 else general
        return "Enhances life results through special combination"
