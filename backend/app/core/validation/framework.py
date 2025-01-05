"""
Astrological Validation Framework
PGF Protocol: VAL_001
Gate: GATE_20
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Tuple, Union, Set
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field, validator
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
    StrengthResult
)
from ..interpretation.framework import (
    InterpretationDomain,
    InterpretationTimeframe,
    InterpretationStrength,
    DomainInterpretation,
    ComprehensiveInterpretation
)
from ..integration.framework import (
    IntegrationMode,
    ChartType,
    ChartData
)

class ValidationLevel(str, Enum):
    """Validation levels"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    RESEARCH = "research"

class ValidationScope(str, Enum):
    """Validation scopes"""
    ASTRONOMICAL = "astronomical"
    MATHEMATICAL = "mathematical"
    ASTROLOGICAL = "astrological"
    INTERPRETATIVE = "interpretative"
    COMPREHENSIVE = "comprehensive"

@dataclass
class ValidationResult:
    """Validation result"""
    
    is_valid: bool
    level: ValidationLevel
    scope: ValidationScope
    errors: List[AppError]
    warnings: List[str]
    suggestions: List[str]
    metrics: Dict[str, float]

class AstrologicalValidator:
    """Astrological validation engine"""
    
    def __init__(
        self,
        level: ValidationLevel = ValidationLevel.STANDARD,
        scope: ValidationScope = ValidationScope.COMPREHENSIVE
    ):
        """Initialize validator"""
        self.level = level
        self.scope = scope
        self.math = PlanetaryMath()
    
    def validate_chart(
        self,
        chart: ChartData
    ) -> ValidationResult:
        """Validate complete chart"""
        
        errors = []
        warnings = []
        suggestions = []
        metrics = {}
        
        # Validate based on scope
        if self.scope in [
            ValidationScope.ASTRONOMICAL,
            ValidationScope.COMPREHENSIVE
        ]:
            self._validate_astronomical(
                chart,
                errors,
                warnings,
                suggestions,
                metrics
            )
        
        if self.scope in [
            ValidationScope.MATHEMATICAL,
            ValidationScope.COMPREHENSIVE
        ]:
            self._validate_mathematical(
                chart,
                errors,
                warnings,
                suggestions,
                metrics
            )
        
        if self.scope in [
            ValidationScope.ASTROLOGICAL,
            ValidationScope.COMPREHENSIVE
        ]:
            self._validate_astrological(
                chart,
                errors,
                warnings,
                suggestions,
                metrics
            )
        
        if self.scope in [
            ValidationScope.INTERPRETATIVE,
            ValidationScope.COMPREHENSIVE
        ]:
            self._validate_interpretative(
                chart,
                errors,
                warnings,
                suggestions,
                metrics
            )
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            level=self.level,
            scope=self.scope,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def _validate_astronomical(
        self,
        chart: ChartData,
        errors: List[AppError],
        warnings: List[str],
        suggestions: List[str],
        metrics: Dict[str, float]
    ):
        """Validate astronomical calculations"""
        
        # Validate planetary positions
        for body, pos in chart.positions.items():
            # Check longitude range
            if not 0 <= pos.longitude < 360:
                errors.append(AppError(
                    code=ErrorCode.INVALID_LONGITUDE,
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.ERROR,
                    message=f"Invalid longitude for {body.name}: "
                           f"{pos.longitude}"
                ))
            
            # Check latitude range
            if not -90 <= pos.latitude <= 90:
                errors.append(AppError(
                    code=ErrorCode.INVALID_LATITUDE,
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.ERROR,
                    message=f"Invalid latitude for {body.name}: "
                           f"{pos.latitude}"
                ))
            
            # Check for extreme speeds
            if abs(pos.speed) > 2:  # degrees per day
                warnings.append(
                    f"Unusual speed for {body.name}: {pos.speed}"
                )
        
        # Validate house cusps
        prev_cusp = 0
        for house, cusp in chart.houses.items():
            if not 0 <= cusp < 360:
                errors.append(AppError(
                    code=ErrorCode.INVALID_HOUSE_CUSP,
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.ERROR,
                    message=f"Invalid house cusp for {house.name}: "
                           f"{cusp}"
                ))
            
            # Check house sequence
            if cusp < prev_cusp and house != House.FIRST:
                warnings.append(
                    f"Irregular house sequence at {house.name}"
                )
            prev_cusp = cusp
        
        # Calculate astronomical metrics
        metrics["mean_planet_speed"] = np.mean([
            abs(pos.speed) for pos in chart.positions.values()
        ])
        metrics["retrograde_count"] = sum(
            1 for pos in chart.positions.values()
            if pos.is_retrograde
        )
    
    def _validate_mathematical(
        self,
        chart: ChartData,
        errors: List[AppError],
        warnings: List[str],
        suggestions: List[str],
        metrics: Dict[str, float]
    ):
        """Validate mathematical calculations"""
        
        # Validate aspects
        for aspect in chart.aspects:
            # Check orb limits
            if aspect.orb > 10:  # maximum orb
                warnings.append(
                    f"Large orb ({aspect.orb}) for aspect between "
                    f"{aspect.body1.name} and {aspect.body2.name}"
                )
            
            # Verify aspect angle
            pos1 = chart.positions[aspect.body1]
            pos2 = chart.positions[aspect.body2]
            angle = self.math.angular_distance(
                pos1.longitude,
                pos2.longitude
            )
            
            if abs(angle - aspect.aspect.value) > aspect.orb:
                errors.append(AppError(
                    code=ErrorCode.INVALID_ASPECT,
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.ERROR,
                    message=f"Invalid aspect angle between "
                           f"{aspect.body1.name} and {aspect.body2.name}"
                ))
        
        # Calculate mathematical metrics
        metrics["aspect_count"] = len(chart.aspects)
        metrics["mean_orb"] = np.mean([
            aspect.orb for aspect in chart.aspects
        ]) if chart.aspects else 0
    
    def _validate_astrological(
        self,
        chart: ChartData,
        errors: List[AppError],
        warnings: List[str],
        suggestions: List[str],
        metrics: Dict[str, float]
    ):
        """Validate astrological calculations"""
        
        # Validate yogas
        for yoga in chart.yogas:
            # Check yoga strength
            if yoga.strength < 0 or yoga.strength > 100:
                errors.append(AppError(
                    code=ErrorCode.INVALID_YOGA_STRENGTH,
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.ERROR,
                    message=f"Invalid yoga strength for {yoga.name}: "
                           f"{yoga.strength}"
                ))
            
            # Check for required planets
            for planet in yoga.planets:
                if planet not in chart.positions:
                    errors.append(AppError(
                        code=ErrorCode.MISSING_PLANET,
                        category=ErrorCategory.VALIDATION,
                        severity=ErrorSeverity.ERROR,
                        message=f"Missing planet {planet.name} "
                               f"required for {yoga.name}"
                    ))
        
        # Validate dashas
        prev_end = None
        for dasha in chart.dashas:
            # Check date sequence
            if prev_end and dasha.start_date < prev_end:
                errors.append(AppError(
                    code=ErrorCode.INVALID_DASHA_SEQUENCE,
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.ERROR,
                    message=f"Invalid dasha sequence for "
                           f"{dasha.major_planet.name}"
                ))
            prev_end = dasha.end_date
            
            # Check dasha strength
            if dasha.strength < 0 or dasha.strength > 100:
                errors.append(AppError(
                    code=ErrorCode.INVALID_DASHA_STRENGTH,
                    category=ErrorCategory.VALIDATION,
                    severity=ErrorSeverity.ERROR,
                    message=f"Invalid dasha strength for "
                           f"{dasha.major_planet.name}: {dasha.strength}"
                ))
        
        # Calculate astrological metrics
        metrics["yoga_count"] = len(chart.yogas)
        metrics["mean_yoga_strength"] = np.mean([
            yoga.strength for yoga in chart.yogas
        ]) if chart.yogas else 0
    
    def _validate_interpretative(
        self,
        chart: ChartData,
        errors: List[AppError],
        warnings: List[str],
        suggestions: List[str],
        metrics: Dict[str, float]
    ):
        """Validate interpretative calculations"""
        
        # Validate domain interpretations
        for domain, interp in chart.interpretation.domains.items():
            # Check interpretation completeness
            if not interp.description:
                warnings.append(
                    f"Missing description for {domain.value} domain"
                )
            
            if not interp.recommendations:
                suggestions.append(
                    f"Add recommendations for {domain.value} domain"
                )
            
            # Check supporting factors
            if not interp.supporting_yogas and not interp.supporting_dashas:
                warnings.append(
                    f"No supporting factors for {domain.value} domain"
                )
        
        # Validate overall interpretation
        if chart.interpretation.overall_strength < 0 or \
           chart.interpretation.overall_strength > 100:
            errors.append(AppError(
                code=ErrorCode.INVALID_INTERPRETATION_STRENGTH,
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.ERROR,
                message="Invalid overall interpretation strength: "
                       f"{chart.interpretation.overall_strength}"
            ))
        
        # Calculate interpretative metrics
        metrics["interpretation_completeness"] = sum(
            1 for domain in chart.interpretation.domains.values()
            if domain.description and domain.recommendations
        ) / len(chart.interpretation.domains)
        
        metrics["recommendation_count"] = sum(
            len(domain.recommendations)
            for domain in chart.interpretation.domains.values()
        )
    
    def validate_progression(
        self,
        birth_chart: ChartData,
        progressed_chart: ChartData
    ) -> ValidationResult:
        """Validate progression calculations"""
        
        errors = []
        warnings = []
        suggestions = []
        metrics = {}
        
        # Validate progression type
        if progressed_chart.type != ChartType.PROGRESSION:
            errors.append(AppError(
                code=ErrorCode.INVALID_CHART_TYPE,
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.ERROR,
                message="Invalid chart type for progression"
            ))
        
        # Validate progression calculations
        for body in birth_chart.positions:
            if body in progressed_chart.positions:
                birth_pos = birth_chart.positions[body]
                prog_pos = progressed_chart.positions[body]
                
                # Check progression range
                diff = self.math.angular_distance(
                    prog_pos.longitude,
                    birth_pos.longitude
                )
                
                if diff > 30:  # Maximum expected progression
                    warnings.append(
                        f"Large progression for {body.name}: {diff}"
                    )
        
        # Calculate progression metrics
        metrics["mean_progression"] = np.mean([
            self.math.angular_distance(
                progressed_chart.positions[body].longitude,
                birth_chart.positions[body].longitude
            )
            for body in birth_chart.positions
            if body in progressed_chart.positions
        ])
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            level=self.level,
            scope=self.scope,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def validate_transit(
        self,
        birth_chart: ChartData,
        transit_chart: ChartData
    ) -> ValidationResult:
        """Validate transit calculations"""
        
        errors = []
        warnings = []
        suggestions = []
        metrics = {}
        
        # Validate transit type
        if transit_chart.type != ChartType.TRANSIT:
            errors.append(AppError(
                code=ErrorCode.INVALID_CHART_TYPE,
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.ERROR,
                message="Invalid chart type for transit"
            ))
        
        # Validate transit calculations
        for body in transit_chart.positions:
            if body in birth_chart.positions:
                birth_pos = birth_chart.positions[body]
                transit_pos = transit_chart.positions[body]
                
                # Check for stationary points
                if abs(transit_pos.speed) < 0.0001:
                    suggestions.append(
                        f"{body.name} is stationary at "
                        f"{transit_pos.longitude}"
                    )
        
        # Calculate transit metrics
        metrics["active_transits"] = sum(
            1 for aspect in transit_chart.aspects
            if aspect.orb <= 1  # Exact transits
        )
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            level=self.level,
            scope=self.scope,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metrics=metrics
        )
