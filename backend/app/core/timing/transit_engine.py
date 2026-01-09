"""
Transit Intelligence Engine
============================

Calculates current planetary transits and their effects on natal chart.

Analyzes:
- Jupiter (12-year cycle, expansive/beneficial)
- Saturn (30-year cycle, karmic/restrictive)
- Rahu (18-year cycle, amplification/obsession)
- Ketu (18-year cycle, detachment/spirituality)

For each transit:
1. Which house it's transiting in natal chart
2. Which natal planets it's aspecting
3. Which yogas it's activating
4. Duration in current house
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TransitPosition:
    """Single planet's transit position"""
    planet: str
    sign: str
    house_in_natal: int
    aspects_natal_planets: List[str]
    entry_date: Optional[datetime] = None
    exit_date: Optional[datetime] = None
    duration_days: int = 0


@dataclass
class TransitEffect:
    """Single transit effect on natal chart"""
    transit_planet: str
    effect_type: str  # "activating_yoga", "aspecting_planet", "transiting_house"
    description: str
    strength: float  # 0-100
    timing: str
    sources: List[Dict[str, str]]


@dataclass
class CurrentTransits:
    """Complete current transit analysis"""
    reference_date: datetime
    jupiter: TransitPosition
    saturn: TransitPosition
    rahu: TransitPosition
    ketu: TransitPosition
    active_effects: List[TransitEffect]
    synthesis: str
    recommendations: List[str]


class TransitIntelligenceEngine:
    """
    Engine for transit analysis and effects.
    
    Vedic Aspect Rules:
    - All planets aspect 7th house from position
    - Jupiter aspects 5th, 7th, 9th houses
    - Saturn aspects 3rd, 7th, 10th houses
    - Mars aspects 4th, 7th, 8th houses
    - Rahu/Ketu aspect 5th, 7th, 9th houses
    """
    
    # Vedic aspect rules (houses aspected from planet's position)
    ASPECT_RULES = {
        "Jupiter": [5, 7, 9],
        "Saturn": [3, 7, 10],
        "Mars": [4, 7, 8],
        "Rahu": [5, 7, 9],
        "Ketu": [5, 7, 9],
        "default": [7]  # All planets aspect 7th
    }
    
    # Approximate transit durations (in days)
    TRANSIT_DURATIONS = {
        "Jupiter": 365,  # ~1 year per sign
        "Saturn": 912,   # ~2.5 years per sign
        "Rahu": 548,     # ~1.5 years per sign (retrograde)
        "Ketu": 548      # ~1.5 years per sign (retrograde)
    }
    
    def __init__(self):
        pass
    
    def get_current_transits(
        self,
        birth_data: Dict[str, Any],
        current_date: Optional[datetime] = None
    ) -> CurrentTransits:
        """
        Calculate current transits and their effects.
        
        Args:
            birth_data: Birth chart data with planet positions
            current_date: Reference date (defaults to now)
            
        Returns:
            CurrentTransits with complete analysis
        """
        
        if current_date is None:
            current_date = datetime.now()
        
        # Simplified: Use estimated positions based on current date
        # Real implementation would use Swiss Ephemeris
        jupiter_transit = self._calculate_jupiter_transit(birth_data, current_date)
        saturn_transit = self._calculate_saturn_transit(birth_data, current_date)
        rahu_transit = self._calculate_rahu_transit(birth_data, current_date)
        ketu_transit = self._calculate_ketu_transit(birth_data, current_date)
        
        # Analyze effects
        active_effects = self._analyze_transit_effects(
            birth_data,
            jupiter_transit,
            saturn_transit,
            rahu_transit,
            ketu_transit
        )
        
        # Generate synthesis
        synthesis = self._generate_transit_synthesis(
            jupiter_transit, saturn_transit, rahu_transit, ketu_transit, active_effects
        )
        
        # Generate recommendations
        recommendations = self._generate_transit_recommendations(active_effects)
        
        return CurrentTransits(
            reference_date=current_date,
            jupiter=jupiter_transit,
            saturn=saturn_transit,
            rahu=rahu_transit,
            ketu=ketu_transit,
            active_effects=active_effects,
            synthesis=synthesis,
            recommendations=recommendations
        )
    
    def _calculate_jupiter_transit(
        self,
        birth_data: Dict[str, Any],
        current_date: datetime
    ) -> TransitPosition:
        """Calculate Jupiter's current transit position"""
        
        # Simplified calculation (real would use ephemeris)
        # Jupiter moves ~30° per year (1 sign per year)
        years_since_birth = (current_date.year - 1990)  # Simplified reference
        jupiter_sign_index = years_since_birth % 12
        
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        current_sign = signs[jupiter_sign_index]
        
        # Determine house in natal chart (simplified)
        house_in_natal = self._determine_transit_house(
            current_sign, birth_data.get("ascendant_sign", "Aries")
        )
        
        # Determine aspects to natal planets
        aspects_planets = self._calculate_aspects(
            "Jupiter", house_in_natal, birth_data.get("planets", {})
        )
        
        return TransitPosition(
            planet="Jupiter",
            sign=current_sign,
            house_in_natal=house_in_natal,
            aspects_natal_planets=aspects_planets,
            duration_days=self.TRANSIT_DURATIONS["Jupiter"]
        )
    
    def _calculate_saturn_transit(
        self,
        birth_data: Dict[str, Any],
        current_date: datetime
    ) -> TransitPosition:
        """Calculate Saturn's current transit position"""
        
        # Simplified: Saturn moves ~12° per year (~2.5 years per sign)
        years_since_birth = (current_date.year - 1990)
        saturn_sign_index = (years_since_birth // 2) % 12
        
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        current_sign = signs[saturn_sign_index]
        
        house_in_natal = self._determine_transit_house(
            current_sign, birth_data.get("ascendant_sign", "Aries")
        )
        
        aspects_planets = self._calculate_aspects(
            "Saturn", house_in_natal, birth_data.get("planets", {})
        )
        
        return TransitPosition(
            planet="Saturn",
            sign=current_sign,
            house_in_natal=house_in_natal,
            aspects_natal_planets=aspects_planets,
            duration_days=self.TRANSIT_DURATIONS["Saturn"]
        )
    
    def _calculate_rahu_transit(
        self,
        birth_data: Dict[str, Any],
        current_date: datetime
    ) -> TransitPosition:
        """Calculate Rahu's current transit position (retrograde)"""
        
        # Rahu moves retrograde ~20° per year (~1.5 years per sign)
        years_since_birth = (current_date.year - 1990)
        rahu_sign_index = (12 - (years_since_birth // 2)) % 12  # Retrograde
        
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        current_sign = signs[rahu_sign_index]
        
        house_in_natal = self._determine_transit_house(
            current_sign, birth_data.get("ascendant_sign", "Aries")
        )
        
        aspects_planets = self._calculate_aspects(
            "Rahu", house_in_natal, birth_data.get("planets", {})
        )
        
        return TransitPosition(
            planet="Rahu",
            sign=current_sign,
            house_in_natal=house_in_natal,
            aspects_natal_planets=aspects_planets,
            duration_days=self.TRANSIT_DURATIONS["Rahu"]
        )
    
    def _calculate_ketu_transit(
        self,
        birth_data: Dict[str, Any],
        current_date: datetime
    ) -> TransitPosition:
        """Calculate Ketu's current transit position (opposite Rahu)"""
        
        # Ketu is always opposite Rahu
        years_since_birth = (current_date.year - 1990)
        rahu_sign_index = (12 - (years_since_birth // 2)) % 12
        ketu_sign_index = (rahu_sign_index + 6) % 12  # Opposite sign
        
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        current_sign = signs[ketu_sign_index]
        
        house_in_natal = self._determine_transit_house(
            current_sign, birth_data.get("ascendant_sign", "Aries")
        )
        
        aspects_planets = self._calculate_aspects(
            "Ketu", house_in_natal, birth_data.get("planets", {})
        )
        
        return TransitPosition(
            planet="Ketu",
            sign=current_sign,
            house_in_natal=house_in_natal,
            aspects_natal_planets=aspects_planets,
            duration_days=self.TRANSIT_DURATIONS["Ketu"]
        )
    
    def _determine_transit_house(
        self,
        transit_sign: str,
        ascendant_sign: str
    ) -> int:
        """Determine which house a sign falls in given ascendant"""
        
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        try:
            asc_index = signs.index(ascendant_sign)
            transit_index = signs.index(transit_sign)
            
            # House = (transit_sign - ascendant_sign + 1) mod 12
            house = ((transit_index - asc_index) % 12) + 1
            return house
        except ValueError:
            return 1  # Default to 1st house if signs not found
    
    def _calculate_aspects(
        self,
        transit_planet: str,
        transit_house: int,
        natal_planets: Dict[str, Any]
    ) -> List[str]:
        """Calculate which natal planets are aspected by transit"""
        
        aspect_houses = self.ASPECT_RULES.get(transit_planet, self.ASPECT_RULES["default"])
        
        aspected_planets = []
        
        for planet_name, planet_data in natal_planets.items():
            natal_house = planet_data.get("house", 0)
            
            # Check if natal planet's house is aspected
            for aspect_offset in aspect_houses:
                aspected_house = ((transit_house + aspect_offset - 1) % 12) + 1
                if natal_house == aspected_house:
                    aspected_planets.append(planet_name)
                    break
        
        return aspected_planets
    
    def _analyze_transit_effects(
        self,
        birth_data: Dict[str, Any],
        jupiter: TransitPosition,
        saturn: TransitPosition,
        rahu: TransitPosition,
        ketu: TransitPosition
    ) -> List[TransitEffect]:
        """Analyze effects of all transits"""
        
        effects = []
        
        # Jupiter transit effects
        if jupiter.house_in_natal in [1, 2, 5, 7, 9, 10, 11]:
            effects.append(TransitEffect(
                transit_planet="Jupiter",
                effect_type="transiting_house",
                description=f"Jupiter transiting {jupiter.house_in_natal}th house - expansion and growth in this life area",
                strength=85.0,
                timing="active now, beneficial effects for next 12 months",
                sources=[{"text": "BPHS", "chapter": "50", "verse": "12"}]
            ))
        
        # Jupiter aspecting natal planets
        for planet in jupiter.aspects_natal_planets:
            effects.append(TransitEffect(
                transit_planet="Jupiter",
                effect_type="aspecting_planet",
                description=f"Jupiter aspecting natal {planet} - blessings and opportunities related to {planet}'s significations",
                strength=75.0,
                timing="active now",
                sources=[{"text": "BPHS", "chapter": "50", "verse": "15"}]
            ))
        
        # Saturn transit effects
        if saturn.house_in_natal in [3, 6, 10, 11]:
            effects.append(TransitEffect(
                transit_planet="Saturn",
                effect_type="transiting_house",
                description=f"Saturn transiting {saturn.house_in_natal}th house - discipline and structure, favorable for hard work",
                strength=70.0,
                timing="active now, effects for next 2.5 years",
                sources=[{"text": "BPHS", "chapter": "50", "verse": "20"}]
            ))
        elif saturn.house_in_natal in [1, 4, 7, 8, 12]:
            effects.append(TransitEffect(
                transit_planet="Saturn",
                effect_type="transiting_house",
                description=f"Saturn transiting {saturn.house_in_natal}th house - challenges and delays, patience required",
                strength=65.0,
                timing="active now, challenging period for next 2.5 years",
                sources=[{"text": "BPHS", "chapter": "50", "verse": "21"}]
            ))
        
        # Rahu/Ketu axis effects
        effects.append(TransitEffect(
            transit_planet="Rahu",
            effect_type="transiting_house",
            description=f"Rahu in {rahu.house_in_natal}th house - intensification and obsession with this area",
            strength=60.0,
            timing="active now, effects for next 18 months",
            sources=[{"text": "Classical", "chapter": "Transit", "verse": "Rahu"}]
        ))
        
        return effects
    
    def _generate_transit_synthesis(
        self,
        jupiter: TransitPosition,
        saturn: TransitPosition,
        rahu: TransitPosition,
        ketu: TransitPosition,
        effects: List[TransitEffect]
    ) -> str:
        """Generate synthesis of current transits"""
        
        parts = []
        
        parts.append(
            f"Current Transit Analysis: Jupiter in {jupiter.sign} ({jupiter.house_in_natal}th house), "
            f"Saturn in {saturn.sign} ({saturn.house_in_natal}th house), "
            f"Rahu in {rahu.sign} ({rahu.house_in_natal}th house)."
        )
        
        parts.append(f"\n\nActive Transit Effects ({len(effects)} identified):")
        for effect in effects[:3]:  # Top 3 effects
            parts.append(f"\n• {effect.description}")
        
        return "".join(parts)
    
    def _generate_transit_recommendations(
        self,
        effects: List[TransitEffect]
    ) -> List[str]:
        """Generate recommendations based on transits"""
        
        recommendations = []
        
        # Jupiter recommendations
        jupiter_effects = [e for e in effects if e.transit_planet == "Jupiter"]
        if jupiter_effects:
            recommendations.append(
                "Leverage Jupiter's beneficial influence for expansion and growth opportunities"
            )
        
        # Saturn recommendations
        saturn_effects = [e for e in effects if e.transit_planet == "Saturn"]
        if saturn_effects:
            recommendations.append(
                "Exercise patience and discipline during Saturn transit - focus on long-term goals"
            )
        
        # Rahu recommendations
        rahu_effects = [e for e in effects if e.transit_planet == "Rahu"]
        if rahu_effects:
            recommendations.append(
                "Be mindful of Rahu's intensifying influence - avoid obsession and maintain balance"
            )
        
        return recommendations[:5]
