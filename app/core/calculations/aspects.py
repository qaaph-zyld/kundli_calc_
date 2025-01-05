"""
Aspect Calculation Module
PGF Protocol: CALC_004
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Tuple
import math
from dataclasses import dataclass
from enum import Enum

@dataclass
class AspectDefinition:
    """Definition of a planetary aspect."""
    angle: float
    orb: float
    strength: float
    nature: str

class AspectType(Enum):
    """Types of aspects in Vedic astrology."""
    CONJUNCTION = "conjunction"
    OPPOSITION = "opposition"
    TRINE = "trine"
    SQUARE = "square"
    SEXTILE = "sextile"
    SEVENTH = "seventh_aspect"
    FOURTH = "fourth_aspect"
    EIGHTH = "eighth_aspect"
    TENTH = "tenth_aspect"

class AspectCalculator:
    """Calculator for planetary aspects in a birth chart."""
    
    # Standard aspect definitions
    STANDARD_ASPECTS = {
        AspectType.CONJUNCTION: AspectDefinition(0, 8, 1.0, "strongest"),
        AspectType.OPPOSITION: AspectDefinition(180, 8, 0.8, "challenging"),
        AspectType.TRINE: AspectDefinition(120, 8, 0.6, "harmonious"),
        AspectType.SQUARE: AspectDefinition(90, 7, 0.4, "challenging"),
        AspectType.SEXTILE: AspectDefinition(60, 6, 0.3, "harmonious"),
        AspectType.SEVENTH: AspectDefinition(210, 5, 0.5, "mixed"),
        AspectType.FOURTH: AspectDefinition(120, 5, 0.4, "harmonious"),
        AspectType.EIGHTH: AspectDefinition(240, 5, 0.3, "challenging"),
        AspectType.TENTH: AspectDefinition(300, 5, 0.2, "mixed")
    }
    
    # Special aspects for specific planets
    SPECIAL_ASPECTS = {
        "Mars": [AspectType.FOURTH, AspectType.EIGHTH],
        "Jupiter": [AspectType.FIFTH, AspectType.SEVENTH, AspectType.NINTH],
        "Saturn": [AspectType.THIRD, AspectType.SEVENTH, AspectType.TENTH]
    }
    
    def __init__(self):
        """Initialize aspect calculator."""
        self.aspects: List[Dict] = []
    
    def calculate_orb(self, angle1: float, angle2: float) -> float:
        """Calculate the orb between two planetary positions."""
        diff = abs(angle1 - angle2)
        if diff > 180:
            diff = 360 - diff
        return diff
    
    def is_aspect_valid(
        self,
        orb: float,
        aspect_def: AspectDefinition
    ) -> bool:
        """Check if an aspect is valid based on its orb."""
        return abs(orb - aspect_def.angle) <= aspect_def.orb
    
    def calculate_aspect_strength(
        self,
        orb: float,
        aspect_def: AspectDefinition
    ) -> float:
        """Calculate the strength of an aspect based on its orb."""
        orb_diff = abs(orb - aspect_def.angle)
        if orb_diff > aspect_def.orb:
            return 0
        
        # Strength decreases linearly with orb difference
        strength_factor = 1 - (orb_diff / aspect_def.orb)
        return aspect_def.strength * strength_factor
    
    def get_planet_aspects(
        self,
        planet: str,
        longitude: float,
        other_planets: Dict[str, float]
    ) -> List[Dict]:
        """Calculate aspects for a specific planet."""
        aspects = []
        
        # Get applicable aspects for the planet
        applicable_aspects = list(self.STANDARD_ASPECTS.items())
        if planet in self.SPECIAL_ASPECTS:
            applicable_aspects.extend([
                (aspect_type, self.STANDARD_ASPECTS[aspect_type])
                for aspect_type in self.SPECIAL_ASPECTS[planet]
            ])
        
        # Calculate aspects with other planets
        for other_planet, other_long in other_planets.items():
            if planet == other_planet:
                continue
            
            orb = self.calculate_orb(longitude, other_long)
            
            for aspect_type, aspect_def in applicable_aspects:
                if self.is_aspect_valid(orb, aspect_def):
                    strength = self.calculate_aspect_strength(orb, aspect_def)
                    
                    aspects.append({
                        "planet1": planet,
                        "planet2": other_planet,
                        "type": aspect_type.value,
                        "orb": orb,
                        "strength": strength,
                        "nature": aspect_def.nature
                    })
        
        return aspects
    
    def calculate_all_aspects(
        self,
        planet_positions: Dict[str, float]
    ) -> List[Dict]:
        """Calculate all aspects between planets in the chart."""
        self.aspects = []
        
        for planet, longitude in planet_positions.items():
            other_planets = {
                p: pos for p, pos in planet_positions.items()
                if p != planet
            }
            
            planet_aspects = self.get_planet_aspects(
                planet,
                longitude,
                other_planets
            )
            
            self.aspects.extend(planet_aspects)
        
        # Sort aspects by strength
        self.aspects.sort(key=lambda x: x["strength"], reverse=True)
        
        return self.aspects
    
    def get_aspect_influences(self) -> Dict[str, List[Dict]]:
        """Get the influences of aspects on each planet."""
        influences = {}
        
        for aspect in self.aspects:
            # Add influence for first planet
            if aspect["planet1"] not in influences:
                influences[aspect["planet1"]] = []
            influences[aspect["planet1"]].append({
                "influencing_planet": aspect["planet2"],
                "aspect_type": aspect["type"],
                "strength": aspect["strength"],
                "nature": aspect["nature"]
            })
            
            # Add influence for second planet
            if aspect["planet2"] not in influences:
                influences[aspect["planet2"]] = []
            influences[aspect["planet2"]].append({
                "influencing_planet": aspect["planet1"],
                "aspect_type": aspect["type"],
                "strength": aspect["strength"],
                "nature": aspect["nature"]
            })
        
        return influences
    
    def get_dominant_aspects(
        self,
        min_strength: float = 0.5
    ) -> List[Dict]:
        """Get the most significant aspects in the chart."""
        return [
            aspect for aspect in self.aspects
            if aspect["strength"] >= min_strength
        ]
    
    def get_challenging_aspects(self) -> List[Dict]:
        """Get challenging aspects in the chart."""
        return [
            aspect for aspect in self.aspects
            if aspect["nature"] == "challenging"
        ]
    
    def get_harmonious_aspects(self) -> List[Dict]:
        """Get harmonious aspects in the chart."""
        return [
            aspect for aspect in self.aspects
            if aspect["nature"] == "harmonious"
        ]
