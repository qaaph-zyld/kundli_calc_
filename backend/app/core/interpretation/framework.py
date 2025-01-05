"""
Astrological Interpretation Framework
PGF Protocol: INT_001
Gate: GATE_18
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union, Set
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field
import numpy as np
from ..errors import (
    AppError,
    ErrorCode,
    ErrorCategory,
    ErrorSeverity
)
from ..astronomical.framework import (
    CelestialBody,
    ZodiacSign,
    House,
    Aspect,
    GeoLocation,
    PlanetaryPosition,
    AspectPosition
)
from ..mathematics.framework import PlanetaryMath
from ..algorithms.framework import (
    YogaType,
    DashaSystem,
    StrengthFactor,
    YogaResult,
    DashaResult,
    StrengthResult,
    AstrologicalAlgorithms
)

class InterpretationDomain(str, Enum):
    """Interpretation domains"""
    PERSONALITY = "personality"
    CAREER = "career"
    RELATIONSHIPS = "relationships"
    HEALTH = "health"
    SPIRITUALITY = "spirituality"
    WEALTH = "wealth"
    EDUCATION = "education"
    FAMILY = "family"

class InterpretationTimeframe(str, Enum):
    """Interpretation timeframes"""
    PAST = "past"
    PRESENT = "present"
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"

class InterpretationStrength(str, Enum):
    """Interpretation strength levels"""
    VERY_STRONG = "very_strong"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    VERY_WEAK = "very_weak"

@dataclass
class DomainInterpretation:
    """Domain-specific interpretation"""
    
    domain: InterpretationDomain
    strength: InterpretationStrength
    timeframe: InterpretationTimeframe
    description: str
    factors: List[str]
    recommendations: List[str]
    supporting_yogas: List[YogaResult]
    supporting_dashas: List[DashaResult]

@dataclass
class ComprehensiveInterpretation:
    """Comprehensive chart interpretation"""
    
    timestamp: datetime
    birth_time: datetime
    location: GeoLocation
    domains: Dict[InterpretationDomain, DomainInterpretation]
    overall_strength: float
    key_periods: List[DashaResult]
    major_yogas: List[YogaResult]
    planetary_strengths: Dict[CelestialBody, StrengthResult]

class AstrologicalInterpreter:
    """Astrological interpretation engine"""
    
    def __init__(self):
        self.algorithms = AstrologicalAlgorithms()
        self.math = PlanetaryMath()
    
    def interpret_chart(
        self,
        positions: Dict[CelestialBody, PlanetaryPosition],
        birth_time: datetime,
        location: GeoLocation
    ) -> ComprehensiveInterpretation:
        """Generate comprehensive chart interpretation"""
        
        # Calculate yogas
        all_yogas = []
        all_yogas.extend(self.algorithms.analyze_raja_yoga(positions))
        all_yogas.extend(self.algorithms.analyze_dhana_yoga(positions))
        all_yogas.extend(self.algorithms.analyze_mahapurusha_yoga(positions))
        
        # Calculate dasha periods
        dasha_periods = self.algorithms.calculate_dasha_periods(
            positions,
            birth_time
        )
        
        # Calculate planetary strengths
        strengths = self.algorithms.calculate_planetary_strength(positions)
        
        # Generate domain interpretations
        domains = {}
        for domain in InterpretationDomain:
            domains[domain] = self._interpret_domain(
                domain,
                positions,
                all_yogas,
                dasha_periods,
                strengths
            )
        
        # Calculate overall strength
        overall_strength = self._calculate_overall_strength(
            domains,
            all_yogas,
            strengths
        )
        
        return ComprehensiveInterpretation(
            timestamp=datetime.now(),
            birth_time=birth_time,
            location=location,
            domains=domains,
            overall_strength=overall_strength,
            key_periods=self._identify_key_periods(dasha_periods),
            major_yogas=self._identify_major_yogas(all_yogas),
            planetary_strengths=strengths
        )
    
    def _interpret_domain(
        self,
        domain: InterpretationDomain,
        positions: Dict[CelestialBody, PlanetaryPosition],
        yogas: List[YogaResult],
        dashas: List[DashaResult],
        strengths: Dict[CelestialBody, StrengthResult]
    ) -> DomainInterpretation:
        """Generate domain-specific interpretation"""
        
        # Get relevant houses for domain
        houses = self._get_domain_houses(domain)
        
        # Get relevant planets for domain
        planets = self._get_domain_planets(domain)
        
        # Filter relevant yogas
        relevant_yogas = [
            yoga for yoga in yogas
            if any(p in planets for p in yoga.planets) or
            any(h in houses for h in yoga.houses)
        ]
        
        # Filter relevant dashas
        relevant_dashas = [
            dasha for dasha in dashas
            if dasha.major_planet in planets
        ]
        
        # Calculate domain strength
        strength = self._calculate_domain_strength(
            domain,
            positions,
            relevant_yogas,
            strengths
        )
        
        # Generate interpretation
        description = self._generate_domain_description(
            domain,
            positions,
            relevant_yogas,
            strength
        )
        
        # Generate recommendations
        recommendations = self._generate_domain_recommendations(
            domain,
            strength,
            relevant_yogas,
            relevant_dashas
        )
        
        # Identify supporting factors
        factors = self._identify_supporting_factors(
            domain,
            positions,
            relevant_yogas,
            strengths
        )
        
        return DomainInterpretation(
            domain=domain,
            strength=strength,
            timeframe=self._determine_timeframe(relevant_dashas),
            description=description,
            factors=factors,
            recommendations=recommendations,
            supporting_yogas=relevant_yogas,
            supporting_dashas=relevant_dashas
        )
    
    def _get_domain_houses(
        self,
        domain: InterpretationDomain
    ) -> Set[House]:
        """Get houses relevant to domain"""
        domain_houses = {
            InterpretationDomain.PERSONALITY: {
                House.FIRST,
                House.FOURTH,
                House.TENTH
            },
            InterpretationDomain.CAREER: {
                House.TENTH,
                House.SIXTH,
                House.SECOND
            },
            InterpretationDomain.RELATIONSHIPS: {
                House.SEVENTH,
                House.FIFTH,
                House.ELEVENTH
            },
            InterpretationDomain.HEALTH: {
                House.FIRST,
                House.SIXTH,
                House.EIGHTH
            },
            InterpretationDomain.SPIRITUALITY: {
                House.NINTH,
                House.TWELFTH,
                House.FOURTH
            },
            InterpretationDomain.WEALTH: {
                House.SECOND,
                House.ELEVENTH,
                House.FIFTH
            },
            InterpretationDomain.EDUCATION: {
                House.FOURTH,
                House.FIFTH,
                House.NINTH
            },
            InterpretationDomain.FAMILY: {
                House.FOURTH,
                House.SECOND,
                House.THIRD
            }
        }
        return domain_houses[domain]
    
    def _get_domain_planets(
        self,
        domain: InterpretationDomain
    ) -> Set[CelestialBody]:
        """Get planets relevant to domain"""
        domain_planets = {
            InterpretationDomain.PERSONALITY: {
                CelestialBody.SUN,
                CelestialBody.MOON,
                CelestialBody.MARS
            },
            InterpretationDomain.CAREER: {
                CelestialBody.SATURN,
                CelestialBody.SUN,
                CelestialBody.JUPITER
            },
            InterpretationDomain.RELATIONSHIPS: {
                CelestialBody.VENUS,
                CelestialBody.JUPITER,
                CelestialBody.MOON
            },
            InterpretationDomain.HEALTH: {
                CelestialBody.SUN,
                CelestialBody.MARS,
                CelestialBody.SATURN
            },
            InterpretationDomain.SPIRITUALITY: {
                CelestialBody.JUPITER,
                CelestialBody.KETU,
                CelestialBody.SATURN
            },
            InterpretationDomain.WEALTH: {
                CelestialBody.JUPITER,
                CelestialBody.VENUS,
                CelestialBody.MERCURY
            },
            InterpretationDomain.EDUCATION: {
                CelestialBody.MERCURY,
                CelestialBody.JUPITER,
                CelestialBody.VENUS
            },
            InterpretationDomain.FAMILY: {
                CelestialBody.MOON,
                CelestialBody.VENUS,
                CelestialBody.JUPITER
            }
        }
        return domain_planets[domain]
    
    def _calculate_domain_strength(
        self,
        domain: InterpretationDomain,
        positions: Dict[CelestialBody, PlanetaryPosition],
        yogas: List[YogaResult],
        strengths: Dict[CelestialBody, StrengthResult]
    ) -> InterpretationStrength:
        """Calculate domain strength"""
        
        # Get relevant planets and houses
        planets = self._get_domain_planets(domain)
        houses = self._get_domain_houses(domain)
        
        # Calculate average planetary strength
        planet_strengths = [
            strengths[p].percentage
            for p in planets
            if p in strengths
        ]
        avg_planet_strength = (
            sum(planet_strengths) / len(planet_strengths)
            if planet_strengths else 0
        )
        
        # Calculate yoga strength
        yoga_strength = sum(
            yoga.strength for yoga in yogas
        ) / len(yogas) if yogas else 0
        
        # Calculate house strength
        house_strength = sum(
            self._calculate_house_strength(h, positions)
            for h in houses
        ) / len(houses)
        
        # Weighted average
        total_strength = (
            avg_planet_strength * 0.4 +
            yoga_strength * 0.4 +
            house_strength * 0.2
        )
        
        # Map to strength level
        if total_strength >= 80:
            return InterpretationStrength.VERY_STRONG
        elif total_strength >= 60:
            return InterpretationStrength.STRONG
        elif total_strength >= 40:
            return InterpretationStrength.MODERATE
        elif total_strength >= 20:
            return InterpretationStrength.WEAK
        else:
            return InterpretationStrength.VERY_WEAK
    
    def _calculate_house_strength(
        self,
        house: House,
        positions: Dict[CelestialBody, PlanetaryPosition]
    ) -> float:
        """Calculate house strength"""
        
        strength = 0.0
        
        # Check planets in house
        planets_in_house = [
            pos for pos in positions.values()
            if pos.house == house
        ]
        
        for pos in planets_in_house:
            # Base points for occupation
            strength += 5
            
            # Additional points for dignity
            dignity = self.math.calculate_dignity_score(
                pos.body,
                pos.sign,
                house
            )
            strength += dignity
            
            # Points for beneficial aspects
            for other_pos in positions.values():
                if other_pos.body != pos.body:
                    aspect = self.algorithms._check_mutual_aspect(
                        pos,
                        other_pos
                    )
                    if aspect in [Aspect.TRINE, Aspect.SEXTILE]:
                        strength += 2
                    elif aspect == Aspect.CONJUNCTION:
                        strength += 3
        
        # Normalize to 0-100
        return min(strength * 5, 100)
    
    def _generate_domain_description(
        self,
        domain: InterpretationDomain,
        positions: Dict[CelestialBody, PlanetaryPosition],
        yogas: List[YogaResult],
        strength: InterpretationStrength
    ) -> str:
        """Generate domain description"""
        
        # Get base description template
        template = self._get_domain_template(domain, strength)
        
        # Get relevant planets and houses
        planets = self._get_domain_planets(domain)
        houses = self._get_domain_houses(domain)
        
        # Format with specific details
        description = template.format(
            planets=", ".join(p.name for p in planets),
            houses=", ".join(h.name for h in houses),
            yogas=", ".join(y.name for y in yogas[:3]),
            strength=strength.value
        )
        
        return description
    
    def _get_domain_template(
        self,
        domain: InterpretationDomain,
        strength: InterpretationStrength
    ) -> str:
        """Get domain description template"""
        
        templates = {
            InterpretationDomain.PERSONALITY: {
                InterpretationStrength.VERY_STRONG: "Exceptionally strong personality traits...",
                InterpretationStrength.STRONG: "Well-developed personality...",
                InterpretationStrength.MODERATE: "Balanced personality traits...",
                InterpretationStrength.WEAK: "Developing personality...",
                InterpretationStrength.VERY_WEAK: "Challenging personality development..."
            },
            # ... (similar templates for other domains)
        }
        
        return templates.get(domain, {}).get(
            strength,
            "General interpretation for {domain} with {strength} strength..."
        )
    
    def _generate_domain_recommendations(
        self,
        domain: InterpretationDomain,
        strength: InterpretationStrength,
        yogas: List[YogaResult],
        dashas: List[DashaResult]
    ) -> List[str]:
        """Generate domain-specific recommendations"""
        
        recommendations = []
        
        # Base recommendations by domain and strength
        base_recs = self._get_base_recommendations(domain, strength)
        recommendations.extend(base_recs)
        
        # Yoga-based recommendations
        for yoga in yogas[:3]:  # Top 3 yogas
            recommendations.extend(
                self._get_yoga_recommendations(yoga)
            )
        
        # Dasha-based recommendations
        for dasha in dashas[:2]:  # Next 2 periods
            recommendations.extend(
                self._get_dasha_recommendations(dasha)
            )
        
        return recommendations
    
    def _get_base_recommendations(
        self,
        domain: InterpretationDomain,
        strength: InterpretationStrength
    ) -> List[str]:
        """Get base domain recommendations"""
        
        recommendations = {
            InterpretationDomain.PERSONALITY: {
                InterpretationStrength.VERY_STRONG: [
                    "Leverage your natural leadership abilities",
                    "Share your experiences to inspire others",
                    "Focus on personal growth and development"
                ],
                # ... (similar for other strengths)
            },
            # ... (similar for other domains)
        }
        
        return recommendations.get(domain, {}).get(
            strength,
            ["General recommendation for domain"]
        )
    
    def _identify_supporting_factors(
        self,
        domain: InterpretationDomain,
        positions: Dict[CelestialBody, PlanetaryPosition],
        yogas: List[YogaResult],
        strengths: Dict[CelestialBody, StrengthResult]
    ) -> List[str]:
        """Identify supporting factors for domain"""
        
        factors = []
        
        # Planet positions
        planets = self._get_domain_planets(domain)
        for planet in planets:
            if planet in positions:
                pos = positions[planet]
                factors.append(
                    f"{planet.name} in {pos.sign.name} "
                    f"({pos.house.name} House)"
                )
        
        # Strong yogas
        for yoga in yogas[:3]:
            if yoga.strength >= 60:
                factors.append(
                    f"Strong {yoga.name} "
                    f"({yoga.strength:.1f}% strength)"
                )
        
        # Strong planets
        for planet in planets:
            if planet in strengths:
                strength = strengths[planet]
                if strength.percentage >= 60:
                    factors.append(
                        f"Strong {planet.name} "
                        f"({strength.percentage:.1f}%)"
                    )
        
        return factors
    
    def _determine_timeframe(
        self,
        dashas: List[DashaResult]
    ) -> InterpretationTimeframe:
        """Determine interpretation timeframe"""
        
        if not dashas:
            return InterpretationTimeframe.PRESENT
        
        # Get current and next major periods
        current_dasha = dashas[0]
        next_dasha = dashas[1] if len(dashas) > 1 else None
        
        # Calculate period durations
        current_duration = (
            current_dasha.end_date - current_dasha.start_date
        ).days / 365.25
        
        if current_duration <= 1:
            return InterpretationTimeframe.SHORT_TERM
        elif current_duration <= 5:
            return InterpretationTimeframe.MEDIUM_TERM
        else:
            return InterpretationTimeframe.LONG_TERM
    
    def _calculate_overall_strength(
        self,
        domains: Dict[InterpretationDomain, DomainInterpretation],
        yogas: List[YogaResult],
        strengths: Dict[CelestialBody, StrengthResult]
    ) -> float:
        """Calculate overall chart strength"""
        
        # Domain strengths
        domain_values = {
            InterpretationStrength.VERY_STRONG: 100,
            InterpretationStrength.STRONG: 75,
            InterpretationStrength.MODERATE: 50,
            InterpretationStrength.WEAK: 25,
            InterpretationStrength.VERY_WEAK: 0
        }
        
        domain_strengths = [
            domain_values[d.strength]
            for d in domains.values()
        ]
        avg_domain_strength = (
            sum(domain_strengths) / len(domain_strengths)
        )
        
        # Yoga strength
        yoga_strength = (
            sum(y.strength for y in yogas) / len(yogas)
            if yogas else 0
        )
        
        # Planetary strength
        planet_strength = (
            sum(s.percentage for s in strengths.values()) /
            len(strengths)
        )
        
        # Weighted average
        return (
            avg_domain_strength * 0.4 +
            yoga_strength * 0.4 +
            planet_strength * 0.2
        )
    
    def _identify_key_periods(
        self,
        dashas: List[DashaResult]
    ) -> List[DashaResult]:
        """Identify key dasha periods"""
        
        # Sort by strength and get top periods
        sorted_dashas = sorted(
            dashas,
            key=lambda x: x.strength,
            reverse=True
        )
        return sorted_dashas[:5]  # Top 5 periods
    
    def _identify_major_yogas(
        self,
        yogas: List[YogaResult]
    ) -> List[YogaResult]:
        """Identify major yogas"""
        
        # Sort by strength and get top yogas
        sorted_yogas = sorted(
            yogas,
            key=lambda x: x.strength,
            reverse=True
        )
        return sorted_yogas[:5]  # Top 5 yogas
