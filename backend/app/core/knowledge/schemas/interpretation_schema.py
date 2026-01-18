"""
Interpretation Schema
=====================
Pydantic models for structured astrological interpretations.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .source_schema import InterpretationMetadata, InterpretationSource


class PlanetaryDignity(str, Enum):
    """Planetary dignity states"""

    EXALTED = "exalted"
    OWN_SIGN = "own_sign"
    MOOLATRIKONA = "moolatrikona"
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"
    ENEMY = "enemy"
    DEBILITATED = "debilitated"


class LifeArea(str, Enum):
    """Life areas for interpretation focus"""

    PERSONALITY = "personality"
    WEALTH = "wealth"
    SIBLINGS = "siblings"
    MOTHER_HOME = "mother_home"
    CHILDREN_EDUCATION = "children_education"
    HEALTH_ENEMIES = "health_enemies"
    RELATIONSHIPS_MARRIAGE = "relationships_marriage"
    LONGEVITY_TRANSFORMATION = "longevity_transformation"
    FORTUNE_DHARMA = "fortune_dharma"
    CAREER_STATUS = "career_status"
    GAINS_FULFILLMENT = "gains_fulfillment"
    LOSSES_SPIRITUALITY = "losses_spirituality"


class InterpretationContext(BaseModel):
    """Context for interpretation generation"""

    planet: str
    house: int
    sign: str
    dignity: PlanetaryDignity
    lordship: List[int] = Field(default_factory=list, description="Houses this planet rules")
    aspects_to: List[str] = Field(default_factory=list, description="Planets aspected")
    aspects_from: List[str] = Field(default_factory=list, description="Aspects received")
    conjunctions: List[str] = Field(default_factory=list, description="Planets conjoined")
    retrograde: bool = False
    combust: bool = False
    current_dasha: Optional[str] = None


class BaseInterpretation(BaseModel):
    """Base interpretation with source attribution"""

    summary: str = Field(..., description="Brief summary of the interpretation")
    detailed: str = Field(..., description="Detailed interpretation")
    keywords: List[str] = Field(default_factory=list, description="Key themes")
    sources: InterpretationSource = Field(..., description="Source citations")
    context: InterpretationContext = Field(..., description="Astrological context")
    metadata: InterpretationMetadata = Field(..., description="Interpretation metadata")


class PlanetInHouseInterpretation(BaseModel):
    """Interpretation for planet in house placement"""

    planet: str
    house: int
    sign: str
    dignity: PlanetaryDignity

    # Core interpretation
    general_effects: str = Field(..., description="General effects per classical texts")
    life_areas: Dict[LifeArea, str] = Field(default_factory=dict, description="Effects on specific life areas")

    # Strength-based variations
    strong_placement_effects: Optional[str] = None
    weak_placement_effects: Optional[str] = None

    # Timing
    timing_notes: Optional[str] = Field(None, description="When effects manifest (dashas, transits)")

    # Remedies
    remedies: List[str] = Field(default_factory=list, description="Classical remedies")

    # Source attribution
    sources: InterpretationSource = Field(..., description="Classical text sources")
    metadata: InterpretationMetadata


class YogaInterpretation(BaseModel):
    """Interpretation for a specific yoga"""

    yoga_name: str
    category: str = Field(..., description="Category (Raja Yoga, Wealth Yoga, Mahapurusha Yoga, etc.)")

    # Formation details
    formation: str = Field(..., description="How the yoga forms - conditions required")
    classical_description: str = Field(..., description="Description from classical texts")
    planets_involved: Optional[List[str]] = None
    houses_involved: Optional[List[int]] = None

    # Effects
    effects: Dict[str, Any] = Field(..., description="Categorized effects (general, career, wealth, etc.)")

    # Strength assessment
    strength_factors: Optional[List[str]] = Field(None, description="Factors that strengthen the yoga")
    strength_assessment: Optional[Dict[str, str]] = Field(
        None, description="Effects by strength level (very_strong, strong, moderate, weak)"
    )

    # Formation examples
    examples: Optional[List[str]] = Field(None, description="Example formations of this yoga")

    # Timing
    timing: Optional[str] = Field(None, description="When effects manifest")

    # Cancellation factors
    cancellation_factors: Optional[List[str]] = Field(None, description="Factors that cancel or weaken the yoga")

    # Special notes
    special_notes: Optional[List[str]] = None
    modern_interpretation: Optional[str] = None

    # Source attribution
    sources: InterpretationSource
    metadata: InterpretationMetadata


class DashaInterpretation(BaseModel):
    """Interpretation for dasha period"""

    planet: str
    dasha_type: str = Field(..., description="Vimshottari, Yogini, etc.")
    level: str = Field(..., description="Mahadasha, Antardasha, etc.")

    # General effects
    general_theme: str = Field(..., description="Overall theme of the period")
    life_areas_activated: List[LifeArea] = Field(default_factory=list, description="Life areas most affected")

    # Positive and challenging
    positive_indications: List[str] = Field(default_factory=list)
    challenging_indications: List[str] = Field(default_factory=list)

    # House-specific effects
    effects_by_house_placement: Optional[str] = Field(
        None, description="Effects based on planet's house position in chart"
    )

    # Recommendations
    recommendations: List[str] = Field(default_factory=list, description="How to navigate this period")

    # Source attribution
    sources: InterpretationSource
    metadata: InterpretationMetadata


class SynthesizedInterpretation(BaseModel):
    """Synthesized interpretation combining multiple factors"""

    interpretation_id: str

    # Components analyzed
    primary_factors: List[str] = Field(
        ..., description="Main factors considered (e.g., 'Sun in 10th', 'Exalted', 'Jupiter aspect')"
    )

    # Synthesized narrative
    narrative: str = Field(..., description="Coherent interpretation narrative")

    # Confidence and nuance
    confidence_notes: str = Field(..., description="Notes on interpretation confidence and any contradictions")

    # Source synthesis
    sources_used: List[str] = Field(..., description="All sources consulted for this synthesis")
    synthesis_method: str = Field(..., description="How multiple sources were combined")

    # Full source attribution
    detailed_sources: InterpretationSource
    metadata: InterpretationMetadata
