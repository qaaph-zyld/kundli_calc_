"""
Correlation Engine
PGF Protocol: COR_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass
import asyncio
import logging
from datetime import datetime
import numpy as np
from enum import Enum
from collections import defaultdict
import scipy.stats as stats
from sklearn.metrics import mutual_info_score
import pandas as pd

class CorrelationType(Enum):
    DIRECT = "direct"
    INVERSE = "inverse"
    CYCLIC = "cyclic"
    COMPOUND = "compound"
    TEMPORAL = "temporal"

@dataclass
class CorrelationResult:
    """Represents a detected correlation"""
    correlation_type: CorrelationType
    source: str
    target: str
    strength: float
    confidence: float
    timestamp: datetime
    significance: float
    details: Dict[str, Any]
    duration: Optional[float] = None

class CorrelationAnalyzer:
    """Advanced correlation analysis for astrological patterns"""
    
    def __init__(self, significance_threshold: float = 0.05):
        self.significance_threshold = significance_threshold
        self.correlations: List[CorrelationResult] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize analysis components
        self._initialize_analyzers()
    
    def _initialize_analyzers(self) -> None:
        """Initialize correlation analysis components"""
        self.analyzers = {
            CorrelationType.DIRECT: self._analyze_direct_correlation,
            CorrelationType.INVERSE: self._analyze_inverse_correlation,
            CorrelationType.CYCLIC: self._analyze_cyclic_correlation,
            CorrelationType.COMPOUND: self._analyze_compound_correlation,
            CorrelationType.TEMPORAL: self._analyze_temporal_correlation
        }
    
    async def analyze_correlations(
        self,
        data: Dict[str, Any],
        correlation_types: Optional[List[CorrelationType]] = None
    ) -> List[CorrelationResult]:
        """Analyze correlations in astrological data"""
        if correlation_types is None:
            correlation_types = list(CorrelationType)
        
        results = []
        for corr_type in correlation_types:
            try:
                correlations = await self.analyzers[corr_type](data)
                results.extend(correlations)
            except Exception as e:
                self.logger.error(
                    f"Error analyzing {corr_type.value} correlation: {str(e)}"
                )
        
        # Store results
        self.correlations.extend(results)
        
        return results
    
    async def _analyze_direct_correlation(
        self,
        data: Dict[str, Any]
    ) -> List[CorrelationResult]:
        """Analyze direct correlations between elements"""
        results = []
        
        # Extract planetary positions and strengths
        planets = data.get("planets", {})
        planet_positions = {
            name: self._normalize_position(planet["degree"])
            for name, planet in planets.items()
            if "degree" in planet
        }
        
        # Analyze correlations between planetary positions
        for p1 in planet_positions:
            for p2 in planet_positions:
                if p1 >= p2:
                    continue
                
                correlation = self._calculate_correlation(
                    planet_positions[p1],
                    planet_positions[p2]
                )
                
                if abs(correlation["coefficient"]) > 0.3:
                    results.append(CorrelationResult(
                        correlation_type=CorrelationType.DIRECT,
                        source=p1,
                        target=p2,
                        strength=abs(correlation["coefficient"]),
                        confidence=correlation["confidence"],
                        timestamp=datetime.now(),
                        significance=correlation["p_value"],
                        details={
                            "type": "planetary_position",
                            "raw_correlation": correlation["coefficient"]
                        }
                    ))
        
        return results
    
    async def _analyze_inverse_correlation(
        self,
        data: Dict[str, Any]
    ) -> List[CorrelationResult]:
        """Analyze inverse correlations"""
        results = []
        
        # Extract planetary strengths and dignities
        planets = data.get("planets", {})
        strengths = {
            name: planet.get("strength", 0)
            for name, planet in planets.items()
        }
        
        # Analyze inverse relationships
        for p1 in strengths:
            for p2 in strengths:
                if p1 >= p2:
                    continue
                
                correlation = self._calculate_correlation(
                    strengths[p1],
                    -strengths[p2]  # Inverse relationship
                )
                
                if abs(correlation["coefficient"]) > 0.3:
                    results.append(CorrelationResult(
                        correlation_type=CorrelationType.INVERSE,
                        source=p1,
                        target=p2,
                        strength=abs(correlation["coefficient"]),
                        confidence=correlation["confidence"],
                        timestamp=datetime.now(),
                        significance=correlation["p_value"],
                        details={
                            "type": "strength_inverse",
                            "raw_correlation": correlation["coefficient"]
                        }
                    ))
        
        return results
    
    async def _analyze_cyclic_correlation(
        self,
        data: Dict[str, Any]
    ) -> List[CorrelationResult]:
        """Analyze cyclic correlations"""
        results = []
        
        # Extract house and planetary cycles
        houses = data.get("houses", {})
        planets = data.get("planets", {})
        
        # Analyze house cycles
        house_cycles = self._detect_cycles(houses)
        for cycle in house_cycles:
            results.append(CorrelationResult(
                correlation_type=CorrelationType.CYCLIC,
                source=f"house_{cycle['start']}",
                target=f"house_{cycle['end']}",
                strength=cycle["strength"],
                confidence=cycle["confidence"],
                timestamp=datetime.now(),
                significance=cycle["significance"],
                details={
                    "type": "house_cycle",
                    "period": cycle["period"],
                    "phase": cycle["phase"]
                }
            ))
        
        # Analyze planetary cycles
        planet_cycles = self._detect_cycles(planets)
        for cycle in planet_cycles:
            results.append(CorrelationResult(
                correlation_type=CorrelationType.CYCLIC,
                source=f"planet_{cycle['start']}",
                target=f"planet_{cycle['end']}",
                strength=cycle["strength"],
                confidence=cycle["confidence"],
                timestamp=datetime.now(),
                significance=cycle["significance"],
                details={
                    "type": "planetary_cycle",
                    "period": cycle["period"],
                    "phase": cycle["phase"]
                }
            ))
        
        return results
    
    async def _analyze_compound_correlation(
        self,
        data: Dict[str, Any]
    ) -> List[CorrelationResult]:
        """Analyze compound correlations"""
        results = []
        
        # Extract multi-factor correlations
        planets = data.get("planets", {})
        houses = data.get("houses", {})
        aspects = data.get("aspects", [])
        
        # Analyze planet-house-aspect compounds
        compounds = self._find_compound_patterns(
            planets, houses, aspects
        )
        
        for compound in compounds:
            results.append(CorrelationResult(
                correlation_type=CorrelationType.COMPOUND,
                source=compound["primary"],
                target=compound["secondary"],
                strength=compound["strength"],
                confidence=compound["confidence"],
                timestamp=datetime.now(),
                significance=compound["significance"],
                details={
                    "type": "multi_factor",
                    "components": compound["components"],
                    "interaction_type": compound["interaction"]
                }
            ))
        
        return results
    
    async def _analyze_temporal_correlation(
        self,
        data: Dict[str, Any]
    ) -> List[CorrelationResult]:
        """Analyze temporal correlations"""
        results = []
        
        # Extract temporal factors
        temporal = data.get("temporal", {})
        if not temporal:
            return results
        
        # Analyze time-based correlations
        time_patterns = self._analyze_temporal_patterns(temporal)
        
        for pattern in time_patterns:
            results.append(CorrelationResult(
                correlation_type=CorrelationType.TEMPORAL,
                source=pattern["factor"],
                target=pattern["reference"],
                strength=pattern["strength"],
                confidence=pattern["confidence"],
                timestamp=datetime.now(),
                significance=pattern["significance"],
                details={
                    "type": "temporal_pattern",
                    "cycle_length": pattern["cycle_length"],
                    "peak_time": pattern["peak_time"]
                },
                duration=pattern.get("duration")
            ))
        
        return results
    
    def _calculate_correlation(
        self,
        x: Union[float, List[float]],
        y: Union[float, List[float]]
    ) -> Dict[str, float]:
        """Calculate correlation statistics"""
        if isinstance(x, (int, float)):
            x = [x]
        if isinstance(y, (int, float)):
            y = [y]
        
        try:
            coefficient, p_value = stats.pearsonr(x, y)
            confidence = 1 - p_value
            
            return {
                "coefficient": coefficient,
                "p_value": p_value,
                "confidence": confidence
            }
        except Exception:
            return {
                "coefficient": 0.0,
                "p_value": 1.0,
                "confidence": 0.0
            }
    
    def _normalize_position(self, degree: float) -> float:
        """Normalize astronomical position"""
        return degree % 360
    
    def _detect_cycles(
        self,
        data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect cyclic patterns in data"""
        cycles = []
        
        if not data:
            return cycles
        
        try:
            # Convert data to time series
            series = pd.Series(data)
            
            # Detect periodicity using FFT
            fft = np.fft.fft(series)
            freqs = np.fft.fftfreq(len(series))
            
            # Find significant frequencies
            significant_freq_idx = np.where(
                np.abs(fft) > np.mean(np.abs(fft)) + np.std(np.abs(fft))
            )[0]
            
            for idx in significant_freq_idx:
                if freqs[idx] > 0:  # Only positive frequencies
                    period = 1 / freqs[idx]
                    phase = np.angle(fft[idx])
                    strength = np.abs(fft[idx]) / len(series)
                    
                    cycles.append({
                        "start": series.index[0],
                        "end": series.index[-1],
                        "period": period,
                        "phase": phase,
                        "strength": strength,
                        "confidence": strength / np.max(np.abs(fft)),
                        "significance": 1 / (1 + np.exp(-strength))
                    })
        
        except Exception as e:
            self.logger.error(f"Error detecting cycles: {str(e)}")
        
        return cycles
    
    def _find_compound_patterns(
        self,
        planets: Dict[str, Any],
        houses: Dict[str, Any],
        aspects: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Find compound patterns involving multiple factors"""
        compounds = []
        
        try:
            # Create interaction matrix
            components = list(planets.keys()) + list(houses.keys())
            n = len(components)
            
            interaction_matrix = np.zeros((n, n))
            
            # Fill matrix with aspect interactions
            for aspect in aspects:
                p1, p2 = aspect["planets"]
                if p1 in components and p2 in components:
                    i = components.index(p1)
                    j = components.index(p2)
                    interaction_matrix[i, j] = aspect.get("strength", 1.0)
                    interaction_matrix[j, i] = interaction_matrix[i, j]
            
            # Find strong interactions
            strong_interactions = np.where(
                interaction_matrix > np.mean(interaction_matrix) +
                np.std(interaction_matrix)
            )
            
            for i, j in zip(*strong_interactions):
                if i < j:  # Avoid duplicates
                    strength = interaction_matrix[i, j]
                    compounds.append({
                        "primary": components[i],
                        "secondary": components[j],
                        "strength": strength,
                        "confidence": strength / np.max(interaction_matrix),
                        "significance": 1 / (1 + np.exp(-strength)),
                        "components": [components[i], components[j]],
                        "interaction": "aspect"
                    })
        
        except Exception as e:
            self.logger.error(
                f"Error finding compound patterns: {str(e)}"
            )
        
        return compounds
    
    def _analyze_temporal_patterns(
        self,
        temporal: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze temporal patterns"""
        patterns = []
        
        try:
            for factor, data in temporal.items():
                if isinstance(data, (list, np.ndarray)):
                    # Analyze time series
                    series = pd.Series(data)
                    
                    # Calculate basic statistics
                    mean = series.mean()
                    std = series.std()
                    
                    # Detect periodicity
                    fft = np.fft.fft(series)
                    freqs = np.fft.fftfreq(len(series))
                    
                    # Find dominant frequency
                    dominant_freq_idx = np.argmax(np.abs(fft[1:])) + 1
                    cycle_length = 1 / freqs[dominant_freq_idx]
                    
                    patterns.append({
                        "factor": factor,
                        "reference": "time",
                        "strength": np.abs(fft[dominant_freq_idx]) / len(series),
                        "confidence": 1 - (std / (mean + 1e-6)),
                        "significance": stats.norm.sf(abs(mean / (std + 1e-6))),
                        "cycle_length": cycle_length,
                        "peak_time": np.angle(fft[dominant_freq_idx]) / (2 * np.pi)
                    })
        
        except Exception as e:
            self.logger.error(
                f"Error analyzing temporal patterns: {str(e)}"
            )
        
        return patterns
    
    def get_correlation_metrics(self) -> Dict[str, Any]:
        """Get correlation analysis metrics"""
        metrics = {
            "total_correlations": len(self.correlations),
            "correlation_types": defaultdict(int),
            "average_strength": 0.0,
            "average_confidence": 0.0,
            "significant_correlations": 0
        }
        
        if self.correlations:
            # Count correlation types
            for corr in self.correlations:
                metrics["correlation_types"][
                    corr.correlation_type.value
                ] += 1
            
            # Calculate averages
            metrics["average_strength"] = np.mean([
                c.strength for c in self.correlations
            ])
            metrics["average_confidence"] = np.mean([
                c.confidence for c in self.correlations
            ])
            
            # Count significant correlations
            metrics["significant_correlations"] = sum(
                1 for c in self.correlations
                if c.significance < self.significance_threshold
            )
        
        return metrics
    
    def reset(self) -> None:
        """Reset correlation analyzer state"""
        self.correlations.clear()
