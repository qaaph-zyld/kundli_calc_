"""
Prediction Engine
PGF Protocol: PRED_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
import logging
from enum import Enum
from collections import defaultdict
import numpy as np
from .pattern_detector import PatternDetector, PatternMatch
from .correlation_engine import CorrelationAnalyzer, CorrelationResult
from .yoga_engine import YogaEngine, YogaResult

class PredictionScope(Enum):
    IMMEDIATE = "immediate"
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"
    LIFETIME = "lifetime"

class PredictionDomain(Enum):
    CAREER = "career"
    RELATIONSHIP = "relationship"
    HEALTH = "health"
    FINANCE = "finance"
    EDUCATION = "education"
    SPIRITUAL = "spiritual"
    FAMILY = "family"
    GENERAL = "general"

@dataclass
class PredictionResult:
    """Represents a generated prediction"""
    scope: PredictionScope
    domain: PredictionDomain
    description: str
    probability: float
    confidence: float
    timing: Optional[Dict[str, Any]]
    factors: List[Dict[str, Any]]
    strength: float
    timestamp: datetime

class PredictionEngine:
    """Advanced prediction engine combining multiple analysis methods"""
    
    def __init__(self):
        self.pattern_detector = PatternDetector()
        self.correlation_analyzer = CorrelationAnalyzer()
        self.yoga_engine = YogaEngine()
        self.predictions: List[PredictionResult] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize prediction templates
        self._initialize_templates()
    
    def _initialize_templates(self) -> None:
        """Initialize prediction templates"""
        self.templates = {
            PredictionDomain.CAREER: {
                "positive": [
                    "Excellent career growth opportunities in {field}",
                    "Leadership roles and responsibilities in {timeframe}",
                    "Professional success through {method}"
                ],
                "negative": [
                    "Career challenges requiring attention in {area}",
                    "Need for professional adaptation in {timeframe}",
                    "Temporary setbacks in {field}"
                ]
            },
            PredictionDomain.RELATIONSHIP: {
                "positive": [
                    "Harmonious relationships and connections",
                    "Strong bonds developing in {timeframe}",
                    "Supportive partnerships in {area}"
                ],
                "negative": [
                    "Relationship dynamics requiring attention",
                    "Need for better communication in {area}",
                    "Temporary relationship challenges"
                ]
            },
            PredictionDomain.HEALTH: {
                "positive": [
                    "Good health and vitality indicated",
                    "Improved wellness through {method}",
                    "Positive health developments"
                ],
                "negative": [
                    "Health matters requiring attention",
                    "Need for preventive care in {area}",
                    "Temporary health concerns"
                ]
            },
            PredictionDomain.FINANCE: {
                "positive": [
                    "Financial growth and opportunities",
                    "Profitable ventures in {field}",
                    "Wealth accumulation through {method}"
                ],
                "negative": [
                    "Financial planning needed in {area}",
                    "Careful money management required",
                    "Temporary financial adjustments"
                ]
            }
        }
    
    async def generate_predictions(
        self,
        chart_data: Dict[str, Any],
        scopes: Optional[List[PredictionScope]] = None,
        domains: Optional[List[PredictionDomain]] = None
    ) -> List[PredictionResult]:
        """Generate predictions based on chart analysis
        
        Args:
            chart_data: Dictionary containing chart information
            scopes: List of prediction scopes to analyze
            domains: List of prediction domains to analyze
            
        Returns:
            List of predictions
        """
        try:
            # Detect patterns
            patterns = await self.pattern_detector.detect_patterns(chart_data)
            
            # Analyze correlations
            correlations = await self.correlation_analyzer.analyze_correlations(
                chart_data
            )
            
            # Analyze yogas
            yogas = await self.yoga_engine.analyze_yogas(chart_data)
            
            # Generate predictions
            predictions = await self._generate_combined_predictions(
                patterns, correlations, yogas,
                scopes or list(PredictionScope),
                domains or list(PredictionDomain)
            )
            
            # Store predictions
            self.predictions.extend(predictions)
            
            return predictions
            
        except Exception as e:
            self.logger.error(f"Error generating predictions: {str(e)}")
            return []
    
    async def _generate_combined_predictions(
        self,
        patterns: List[PatternMatch],
        correlations: List[CorrelationResult],
        yogas: List[YogaResult],
        scopes: List[PredictionScope],
        domains: List[PredictionDomain]
    ) -> List[PredictionResult]:
        """Generate predictions by combining different analysis results"""
        predictions = []
        
        # Group patterns by domain
        domain_patterns = self._group_by_domain(patterns)
        
        # Process each domain
        for domain in domains:
            domain_yogas = [y for y in yogas if self._map_yoga_to_domain(y) == domain]
            domain_correlations = [c for c in correlations 
                                 if self._map_correlation_to_domain(c) == domain]
            
            # Generate domain-specific predictions
            for scope in scopes:
                prediction = self._create_prediction(
                    domain,
                    scope,
                    domain_patterns.get(domain, []),
                    domain_correlations,
                    domain_yogas
                )
                
                if prediction:
                    predictions.append(prediction)
        
        return predictions
    
    def _create_prediction(
        self,
        domain: PredictionDomain,
        scope: PredictionScope,
        patterns: List[PatternMatch],
        correlations: List[CorrelationResult],
        yogas: List[YogaResult]
    ) -> Optional[PredictionResult]:
        """Create a prediction for specific domain and scope"""
        if not (patterns or correlations or yogas):
            return None
            
        # Calculate combined strength
        strength = self._calculate_combined_strength(
            patterns, correlations, yogas
        )
        
        # Determine if prediction is positive or negative
        is_positive = strength > 0.5
        
        # Select appropriate template
        templates = self.templates.get(domain, {})
        template_list = templates["positive" if is_positive else "negative"]
        
        if not template_list:
            return None
            
        # Generate prediction text
        template = np.random.choice(template_list)
        description = self._fill_template(
            template,
            domain,
            scope,
            patterns,
            correlations,
            yogas
        )
        
        # Calculate timing
        timing = self._calculate_timing(scope, patterns, yogas)
        
        # Gather contributing factors
        factors = self._gather_factors(patterns, correlations, yogas)
        
        return PredictionResult(
            scope=scope,
            domain=domain,
            description=description,
            probability=strength,
            confidence=self._calculate_confidence(
                patterns, correlations, yogas
            ),
            timing=timing,
            factors=factors,
            strength=strength,
            timestamp=datetime.now()
        )
    
    def _calculate_combined_strength(
        self,
        patterns: List[PatternMatch],
        correlations: List[CorrelationResult],
        yogas: List[YogaResult]
    ) -> float:
        """Calculate combined strength of all factors"""
        strengths = []
        
        if patterns:
            strengths.append(np.mean([p.strength for p in patterns]))
        if correlations:
            strengths.append(np.mean([c.strength for c in correlations]))
        if yogas:
            strengths.append(np.mean([y.strength for y in yogas]))
        
        return np.mean(strengths) if strengths else 0.5
    
    def _calculate_confidence(
        self,
        patterns: List[PatternMatch],
        correlations: List[CorrelationResult],
        yogas: List[YogaResult]
    ) -> float:
        """Calculate overall confidence level"""
        confidences = []
        
        if patterns:
            confidences.append(np.mean([p.confidence for p in patterns]))
        if correlations:
            confidences.append(np.mean([c.confidence for c in correlations]))
        if yogas:
            confidences.append(np.mean([y.confidence for y in yogas]))
        
        return np.mean(confidences) if confidences else 0.5
    
    def _calculate_timing(
        self,
        scope: PredictionScope,
        patterns: List[PatternMatch],
        yogas: List[YogaResult]
    ) -> Dict[str, Any]:
        """Calculate timing information for prediction"""
        timing = {
            "start": datetime.now(),
            "duration": None,
            "peak": None
        }
        
        durations = []
        
        # Collect duration information
        for pattern in patterns:
            if pattern.duration:
                durations.append(pattern.duration)
        
        for yoga in yogas:
            if yoga.duration:
                durations.append(yoga.duration)
        
        # Calculate average duration if available
        if durations:
            timing["duration"] = np.mean(durations)
        else:
            # Use default durations based on scope
            default_durations = {
                PredictionScope.IMMEDIATE: 7,      # days
                PredictionScope.SHORT_TERM: 30,    # days
                PredictionScope.MEDIUM_TERM: 90,   # days
                PredictionScope.LONG_TERM: 365,    # days
                PredictionScope.LIFETIME: None
            }
            timing["duration"] = default_durations[scope]
        
        return timing
    
    def _gather_factors(
        self,
        patterns: List[PatternMatch],
        correlations: List[CorrelationResult],
        yogas: List[YogaResult]
    ) -> List[Dict[str, Any]]:
        """Gather contributing factors for prediction"""
        factors = []
        
        # Add patterns
        for pattern in patterns:
            factors.append({
                "type": "pattern",
                "name": pattern.name,
                "strength": pattern.strength,
                "components": pattern.components
            })
        
        # Add correlations
        for correlation in correlations:
            factors.append({
                "type": "correlation",
                "source": correlation.source,
                "target": correlation.target,
                "strength": correlation.strength,
                "details": correlation.details
            })
        
        # Add yogas
        for yoga in yogas:
            factors.append({
                "type": "yoga",
                "name": yoga.name,
                "strength": yoga.strength,
                "planets": yoga.planets,
                "houses": yoga.houses
            })
        
        return factors
    
    def _group_by_domain(
        self,
        patterns: List[PatternMatch]
    ) -> Dict[PredictionDomain, List[PatternMatch]]:
        """Group patterns by prediction domain"""
        grouped = defaultdict(list)
        
        for pattern in patterns:
            domain = self._map_pattern_to_domain(pattern)
            if domain:
                grouped[domain].append(pattern)
        
        return grouped
    
    def _map_pattern_to_domain(
        self,
        pattern: PatternMatch
    ) -> Optional[PredictionDomain]:
        """Map pattern to prediction domain"""
        # Mapping logic based on pattern type and components
        if "career" in pattern.name.lower():
            return PredictionDomain.CAREER
        elif "relationship" in pattern.name.lower():
            return PredictionDomain.RELATIONSHIP
        elif "health" in pattern.name.lower():
            return PredictionDomain.HEALTH
        elif "wealth" in pattern.name.lower():
            return PredictionDomain.FINANCE
        else:
            return PredictionDomain.GENERAL
    
    def _map_yoga_to_domain(
        self,
        yoga: YogaResult
    ) -> PredictionDomain:
        """Map yoga to prediction domain"""
        # Mapping based on yoga type and effects
        if "wealth" in yoga.effects or "prosperity" in yoga.effects:
            return PredictionDomain.FINANCE
        elif "power" in yoga.effects or "career" in yoga.effects:
            return PredictionDomain.CAREER
        elif "relationship" in yoga.effects:
            return PredictionDomain.RELATIONSHIP
        elif "health" in yoga.effects:
            return PredictionDomain.HEALTH
        else:
            return PredictionDomain.GENERAL
    
    def _map_correlation_to_domain(
        self,
        correlation: CorrelationResult
    ) -> PredictionDomain:
        """Map correlation to prediction domain"""
        # Mapping based on correlation type and details
        if "finance" in correlation.details.get("type", ""):
            return PredictionDomain.FINANCE
        elif "career" in correlation.details.get("type", ""):
            return PredictionDomain.CAREER
        elif "relationship" in correlation.details.get("type", ""):
            return PredictionDomain.RELATIONSHIP
        elif "health" in correlation.details.get("type", ""):
            return PredictionDomain.HEALTH
        else:
            return PredictionDomain.GENERAL
    
    def _fill_template(
        self,
        template: str,
        domain: PredictionDomain,
        scope: PredictionScope,
        patterns: List[PatternMatch],
        correlations: List[CorrelationResult],
        yogas: List[YogaResult]
    ) -> str:
        """Fill prediction template with specific details"""
        # Extract relevant information from patterns, correlations, and yogas
        fields = set()
        methods = set()
        timeframes = set()
        areas = set()
        
        for pattern in patterns:
            if hasattr(pattern, "components"):
                for comp in pattern.components:
                    if isinstance(comp, dict):
                        fields.add(comp.get("field", ""))
                        methods.add(comp.get("method", ""))
                        areas.add(comp.get("area", ""))
        
        # Map scope to timeframe
        scope_timeframes = {
            PredictionScope.IMMEDIATE: "the next few days",
            PredictionScope.SHORT_TERM: "the coming weeks",
            PredictionScope.MEDIUM_TERM: "the next few months",
            PredictionScope.LONG_TERM: "the coming year",
            PredictionScope.LIFETIME: "the long term"
        }
        
        # Fill template placeholders
        filled = template.format(
            field=next(iter(fields), "your field"),
            method=next(iter(methods), "your efforts"),
            timeframe=scope_timeframes.get(scope, "the future"),
            area=next(iter(areas), "this area")
        )
        
        return filled
    
    def get_prediction_metrics(self) -> Dict[str, Any]:
        """Get prediction generation metrics"""
        metrics = {
            "total_predictions": len(self.predictions),
            "predictions_by_domain": defaultdict(int),
            "predictions_by_scope": defaultdict(int),
            "average_probability": 0.0,
            "average_confidence": 0.0
        }
        
        if self.predictions:
            # Count predictions by domain and scope
            for pred in self.predictions:
                metrics["predictions_by_domain"][pred.domain.value] += 1
                metrics["predictions_by_scope"][pred.scope.value] += 1
            
            # Calculate averages
            metrics["average_probability"] = np.mean([
                p.probability for p in self.predictions
            ])
            metrics["average_confidence"] = np.mean([
                p.confidence for p in self.predictions
            ])
        
        return metrics
    
    def reset(self) -> None:
        """Reset prediction engine state"""
        self.predictions.clear()
        self.pattern_detector.reset()
        self.correlation_analyzer.reset()
        self.yoga_engine.reset()
