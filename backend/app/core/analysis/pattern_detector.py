"""
Pattern Detection System
PGF Protocol: PAT_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass
import asyncio
import logging
from datetime import datetime
import numpy as np
from enum import Enum
from collections import defaultdict
import math

class PatternType(Enum):
    PLANETARY = "planetary"
    HOUSE = "house"
    ASPECT = "aspect"
    TEMPORAL = "temporal"
    COMBINED = "combined"

@dataclass
class PatternMatch:
    """Represents a detected pattern"""
    pattern_type: PatternType
    name: str
    confidence: float
    components: List[Dict[str, Any]]
    timestamp: datetime
    strength: float
    effects: Dict[str, float]
    duration: Optional[float] = None

class PatternSignature:
    """Defines a pattern signature for detection"""
    
    def __init__(
        self,
        name: str,
        pattern_type: PatternType,
        conditions: List[Dict[str, Any]],
        effects: Dict[str, float],
        min_strength: float = 0.6
    ):
        self.name = name
        self.pattern_type = pattern_type
        self.conditions = conditions
        self.effects = effects
        self.min_strength = min_strength

class PatternDetector:
    """Advanced pattern detection system for astrological calculations"""
    
    def __init__(self):
        self.signatures: Dict[str, PatternSignature] = {}
        self.detected_patterns: List[PatternMatch] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize standard patterns
        self._initialize_patterns()
    
    def _initialize_patterns(self) -> None:
        """Initialize standard astrological patterns"""
        # Planetary Patterns
        self.signatures["exaltation"] = PatternSignature(
            name="Exaltation",
            pattern_type=PatternType.PLANETARY,
            conditions=[{
                "type": "planet_sign",
                "relations": {
                    "Sun": "Aries",
                    "Moon": "Taurus",
                    "Mars": "Capricorn",
                    "Mercury": "Virgo",
                    "Jupiter": "Cancer",
                    "Venus": "Pisces",
                    "Saturn": "Libra"
                }
            }],
            effects={"strength": 1.0, "dignity": 1.0}
        )
        
        self.signatures["mutual_reception"] = PatternSignature(
            name="Mutual Reception",
            pattern_type=PatternType.PLANETARY,
            conditions=[{
                "type": "planet_exchange",
                "min_planets": 2,
                "exchange_type": "rulership"
            }],
            effects={"strength": 0.8, "harmony": 0.7}
        )
        
        # House Patterns
        self.signatures["trikona"] = PatternSignature(
            name="Trikona",
            pattern_type=PatternType.HOUSE,
            conditions=[{
                "type": "house_angle",
                "angle": 120,
                "tolerance": 5
            }],
            effects={"auspiciousness": 0.8}
        )
        
        self.signatures["kendra"] = PatternSignature(
            name="Kendra",
            pattern_type=PatternType.HOUSE,
            conditions=[{
                "type": "house_angle",
                "angle": 90,
                "tolerance": 5
            }],
            effects={"power": 0.9}
        )
        
        # Aspect Patterns
        self.signatures["grand_trine"] = PatternSignature(
            name="Grand Trine",
            pattern_type=PatternType.ASPECT,
            conditions=[{
                "type": "aspect_chain",
                "aspect": "trine",
                "min_planets": 3
            }],
            effects={"harmony": 1.0, "flow": 0.9}
        )
        
        # Temporal Patterns
        self.signatures["planetary_hour"] = PatternSignature(
            name="Planetary Hour",
            pattern_type=PatternType.TEMPORAL,
            conditions=[{
                "type": "temporal_match",
                "factor": "hour_ruler",
                "match_type": "planet"
            }],
            effects={"timing": 0.7}
        )
    
    async def detect_patterns(
        self,
        chart_data: Dict[str, Any]
    ) -> List[PatternMatch]:
        """Detect patterns in chart data"""
        detected = []
        
        for signature in self.signatures.values():
            matches = await self._match_signature(signature, chart_data)
            detected.extend(matches)
        
        # Store detected patterns
        self.detected_patterns.extend(detected)
        
        return detected
    
    async def _match_signature(
        self,
        signature: PatternSignature,
        chart_data: Dict[str, Any]
    ) -> List[PatternMatch]:
        """Match a specific pattern signature"""
        matches = []
        
        try:
            if signature.pattern_type == PatternType.PLANETARY:
                matches.extend(
                    await self._detect_planetary_patterns(
                        signature, chart_data
                    )
                )
            elif signature.pattern_type == PatternType.HOUSE:
                matches.extend(
                    await self._detect_house_patterns(
                        signature, chart_data
                    )
                )
            elif signature.pattern_type == PatternType.ASPECT:
                matches.extend(
                    await self._detect_aspect_patterns(
                        signature, chart_data
                    )
                )
            elif signature.pattern_type == PatternType.TEMPORAL:
                matches.extend(
                    await self._detect_temporal_patterns(
                        signature, chart_data
                    )
                )
            
        except Exception as e:
            self.logger.error(
                f"Error detecting {signature.name} pattern: {str(e)}"
            )
        
        return matches
    
    async def _detect_planetary_patterns(
        self,
        signature: PatternSignature,
        chart_data: Dict[str, Any]
    ) -> List[PatternMatch]:
        """Detect planetary-based patterns"""
        matches = []
        planets = chart_data.get("planets", {})
        
        for condition in signature.conditions:
            if condition["type"] == "planet_sign":
                # Check planet-sign relationships
                matched_planets = []
                for planet, sign in condition["relations"].items():
                    if (planet in planets and
                        planets[planet].get("sign") == sign):
                        matched_planets.append({
                            "planet": planet,
                            "sign": sign
                        })
                
                if matched_planets:
                    strength = len(matched_planets) / len(
                        condition["relations"]
                    )
                    if strength >= signature.min_strength:
                        matches.append(PatternMatch(
                            pattern_type=signature.pattern_type,
                            name=signature.name,
                            confidence=strength,
                            components=matched_planets,
                            timestamp=datetime.now(),
                            strength=strength,
                            effects=signature.effects
                        ))
            
            elif condition["type"] == "planet_exchange":
                # Check mutual receptions
                exchanges = self._find_planet_exchanges(
                    planets,
                    condition["exchange_type"]
                )
                for exchange in exchanges:
                    if len(exchange) >= condition["min_planets"]:
                        matches.append(PatternMatch(
                            pattern_type=signature.pattern_type,
                            name=signature.name,
                            confidence=0.8,
                            components=exchange,
                            timestamp=datetime.now(),
                            strength=0.8,
                            effects=signature.effects
                        ))
        
        return matches
    
    async def _detect_house_patterns(
        self,
        signature: PatternSignature,
        chart_data: Dict[str, Any]
    ) -> List[PatternMatch]:
        """Detect house-based patterns"""
        matches = []
        houses = chart_data.get("houses", {})
        
        for condition in signature.conditions:
            if condition["type"] == "house_angle":
                # Find houses at specified angles
                angle = condition["angle"]
                tolerance = condition["tolerance"]
                
                house_groups = self._find_angular_relationships(
                    houses,
                    angle,
                    tolerance
                )
                
                for group in house_groups:
                    matches.append(PatternMatch(
                        pattern_type=signature.pattern_type,
                        name=signature.name,
                        confidence=0.9,
                        components=group,
                        timestamp=datetime.now(),
                        strength=0.9,
                        effects=signature.effects
                    ))
        
        return matches
    
    async def _detect_aspect_patterns(
        self,
        signature: PatternSignature,
        chart_data: Dict[str, Any]
    ) -> List[PatternMatch]:
        """Detect aspect-based patterns"""
        matches = []
        aspects = chart_data.get("aspects", [])
        
        for condition in signature.conditions:
            if condition["type"] == "aspect_chain":
                # Find chains of aspects
                chains = self._find_aspect_chains(
                    aspects,
                    condition["aspect"],
                    condition["min_planets"]
                )
                
                for chain in chains:
                    matches.append(PatternMatch(
                        pattern_type=signature.pattern_type,
                        name=signature.name,
                        confidence=0.85,
                        components=chain,
                        timestamp=datetime.now(),
                        strength=0.85,
                        effects=signature.effects
                    ))
        
        return matches
    
    async def _detect_temporal_patterns(
        self,
        signature: PatternSignature,
        chart_data: Dict[str, Any]
    ) -> List[PatternMatch]:
        """Detect time-based patterns"""
        matches = []
        temporal = chart_data.get("temporal", {})
        
        for condition in signature.conditions:
            if condition["type"] == "temporal_match":
                # Check temporal factors
                if condition["factor"] in temporal:
                    factor_value = temporal[condition["factor"]]
                    if self._check_temporal_match(
                        factor_value,
                        condition["match_type"]
                    ):
                        matches.append(PatternMatch(
                            pattern_type=signature.pattern_type,
                            name=signature.name,
                            confidence=0.75,
                            components=[{
                                "factor": condition["factor"],
                                "value": factor_value
                            }],
                            timestamp=datetime.now(),
                            strength=0.75,
                            effects=signature.effects,
                            duration=temporal.get("duration")
                        ))
        
        return matches
    
    def _find_planet_exchanges(
        self,
        planets: Dict[str, Any],
        exchange_type: str
    ) -> List[List[Dict[str, Any]]]:
        """Find planetary exchanges"""
        exchanges = []
        processed = set()
        
        for p1_name, p1_data in planets.items():
            if p1_name in processed:
                continue
                
            exchange_group = []
            for p2_name, p2_data in planets.items():
                if (p1_name != p2_name and
                    self._check_exchange(
                        p1_data, p2_data, exchange_type
                    )):
                    exchange_group.extend([
                        {"planet": p1_name, "data": p1_data},
                        {"planet": p2_name, "data": p2_data}
                    ])
                    processed.add(p1_name)
                    processed.add(p2_name)
            
            if exchange_group:
                exchanges.append(exchange_group)
        
        return exchanges
    
    def _find_angular_relationships(
        self,
        houses: Dict[int, Any],
        target_angle: float,
        tolerance: float
    ) -> List[List[Dict[str, Any]]]:
        """Find houses at specified angles"""
        relationships = []
        processed = set()
        
        for h1 in houses:
            if h1 in processed:
                continue
                
            group = []
            for h2 in houses:
                if h1 != h2:
                    angle = self._calculate_house_angle(h1, h2)
                    if abs(angle - target_angle) <= tolerance:
                        group.extend([
                            {"house": h1, "data": houses[h1]},
                            {"house": h2, "data": houses[h2]}
                        ])
                        processed.add(h1)
                        processed.add(h2)
            
            if group:
                relationships.append(group)
        
        return relationships
    
    def _find_aspect_chains(
        self,
        aspects: List[Dict[str, Any]],
        aspect_type: str,
        min_planets: int
    ) -> List[List[Dict[str, Any]]]:
        """Find chains of aspects"""
        chains = []
        graph = defaultdict(list)
        
        # Build aspect graph
        for aspect in aspects:
            if aspect["type"] == aspect_type:
                p1, p2 = aspect["planets"]
                graph[p1].append(p2)
                graph[p2].append(p1)
        
        # Find chains using DFS
        visited = set()
        
        def dfs(planet: str, chain: List[str]) -> None:
            if len(chain) >= min_planets:
                chains.append([
                    {"planet": p} for p in chain
                ])
            
            for next_planet in graph[planet]:
                if next_planet not in visited:
                    visited.add(next_planet)
                    dfs(next_planet, chain + [next_planet])
                    visited.remove(next_planet)
        
        # Start DFS from each planet
        for planet in graph:
            if planet not in visited:
                visited.add(planet)
                dfs(planet, [planet])
                visited.remove(planet)
        
        return chains
    
    def _check_exchange(
        self,
        p1_data: Dict[str, Any],
        p2_data: Dict[str, Any],
        exchange_type: str
    ) -> bool:
        """Check if two planets are in exchange"""
        if exchange_type == "rulership":
            return (
                p1_data.get("rules") == p2_data.get("sign") and
                p2_data.get("rules") == p1_data.get("sign")
            )
        return False
    
    def _calculate_house_angle(
        self,
        house1: int,
        house2: int
    ) -> float:
        """Calculate angle between houses"""
        return abs((house2 - house1) * 30)
    
    def _check_temporal_match(
        self,
        value: Any,
        match_type: str
    ) -> bool:
        """Check temporal factor match"""
        if match_type == "planet":
            return isinstance(value, str)
        return False
    
    async def analyze_pattern_sequence(
        self,
        timeframe: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """Analyze sequence of detected patterns"""
        patterns = self.detected_patterns
        if timeframe:
            start, end = timeframe
            patterns = [
                p for p in patterns
                if start <= p.timestamp <= end
            ]
        
        analysis = {
            "total_patterns": len(patterns),
            "pattern_types": defaultdict(int),
            "pattern_strengths": defaultdict(list),
            "temporal_distribution": defaultdict(int),
            "common_combinations": defaultdict(int)
        }
        
        for pattern in patterns:
            # Count pattern types
            analysis["pattern_types"][pattern.pattern_type.value] += 1
            
            # Track strengths
            analysis["pattern_strengths"][pattern.name].append(
                pattern.strength
            )
            
            # Temporal distribution
            hour = pattern.timestamp.hour
            analysis["temporal_distribution"][hour] += 1
            
            # Track combinations
            if pattern.pattern_type == PatternType.COMBINED:
                for comp in pattern.components:
                    if "pattern" in comp:
                        analysis["common_combinations"][
                            comp["pattern"]
                        ] += 1
        
        # Calculate averages
        for name, strengths in analysis["pattern_strengths"].items():
            analysis["pattern_strengths"][name] = {
                "mean": np.mean(strengths),
                "std": np.std(strengths),
                "max": max(strengths),
                "min": min(strengths)
            }
        
        return analysis
    
    def get_pattern_metrics(self) -> Dict[str, Any]:
        """Get pattern detection metrics"""
        return {
            "total_detected": len(self.detected_patterns),
            "pattern_types": {
                pt.value: len([
                    p for p in self.detected_patterns
                    if p.pattern_type == pt
                ])
                for pt in PatternType
            },
            "average_confidence": np.mean([
                p.confidence for p in self.detected_patterns
            ]) if self.detected_patterns else 0,
            "latest_detection": max(
                (p.timestamp for p in self.detected_patterns),
                default=None
            )
        }
    
    def reset(self) -> None:
        """Reset pattern detector state"""
        self.detected_patterns.clear()
