from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import math

@dataclass
class Aspect:
    name: str
    angle: float
    orb: float
    is_major: bool
    strength: float = 100.0  # Base strength for the aspect
    benefic_nature: float = 0.0  # -100 to +100, negative for malefic

@dataclass
class PlanetaryAspect:
    planet1: str
    planet2: str
    aspect: Aspect
    orb: float
    is_applying: bool
    strength: float
    total_influence: float

class EnhancedAspectCalculator:
    ASPECTS = {
        "Conjunction": Aspect("Conjunction", 0, 10, True, 100, 0),
        "Opposition": Aspect("Opposition", 180, 10, True, 80, -60),
        "Trine": Aspect("Trine", 120, 8, True, 70, 80),
        "Square": Aspect("Square", 90, 8, True, 60, -70),
        "Sextile": Aspect("Sextile", 60, 6, True, 50, 50),
        "Semisextile": Aspect("Semisextile", 30, 2, False, 20, 20),
        "Quincunx": Aspect("Quincunx", 150, 3, False, 30, -30),
        "Semisquare": Aspect("Semisquare", 45, 2, False, 25, -40),
        "Sesquiquadrate": Aspect("Sesquiquadrate", 135, 2, False, 25, -40),
        "Quintile": Aspect("Quintile", 72, 2, False, 20, 30),
        "Biquintile": Aspect("Biquintile", 144, 2, False, 20, 30),
        "Parallel": Aspect("Parallel", 0, 1, True, 40, 0),
        "Contraparallel": Aspect("Contraparallel", 180, 1, True, 40, -20)
    }
    
    # Planetary relationships (friendship, neutrality, enmity)
    PLANETARY_RELATIONSHIPS = {
        "Sun": {"friend": ["Moon", "Mars", "Jupiter"], "enemy": ["Saturn", "Venus"]},
        "Moon": {"friend": ["Sun", "Mercury"], "enemy": ["Rahu", "Ketu"]},
        "Mars": {"friend": ["Sun", "Jupiter", "Saturn"], "enemy": ["Mercury"]},
        "Mercury": {"friend": ["Sun", "Venus"], "enemy": ["Moon"]},
        "Jupiter": {"friend": ["Sun", "Mars", "Moon"], "enemy": ["Mercury", "Venus"]},
        "Venus": {"friend": ["Mercury", "Saturn"], "enemy": ["Sun", "Moon"]},
        "Saturn": {"friend": ["Mercury", "Venus"], "enemy": ["Sun", "Moon", "Mars"]}
    }
    
    # Special aspect rules
    SPECIAL_ASPECTS = {
        "Mars": [4, 8],      # Mars aspects 4th and 8th houses
        "Jupiter": [5, 7, 9], # Jupiter aspects 5th, 7th, and 9th houses
        "Saturn": [3, 7, 10]  # Saturn aspects 3rd, 7th, and 10th houses
    }
    
    def __init__(self):
        self.aspect_strength_modifiers = {
            'orb': self._calculate_orb_strength,
            'speed': self._calculate_speed_strength,
            'dignity': self._calculate_dignity_strength,
            'relationship': self._calculate_relationship_strength,
            'house_position': self._calculate_house_position_strength
        }
    
    def _calculate_orb_strength(
        self,
        aspect: Aspect,
        orb: float
    ) -> float:
        """Calculate strength based on orb"""
        if orb == 0:
            return 100
        return max(0, 100 - (orb / aspect.orb) * 100)
    
    def _calculate_speed_strength(
        self,
        planet1_speed: float,
        planet2_speed: float
    ) -> float:
        """Calculate strength based on planetary speeds."""
        speed_diff = abs(planet1_speed - planet2_speed)
        if speed_diff < 0.1:
            return 100.0
        elif speed_diff < 0.5:
            return 75.0
        elif speed_diff < 1.0:
            return 50.0
        else:
            return max(0, 100 - (speed_diff * 50))

    def _calculate_dignity_strength(
        self,
        planet1_dignity: str,
        planet2_dignity: str
    ) -> float:
        """Calculate strength based on planetary dignities"""
        dignity_values = {
            'exalted': 100,
            'moolatrikona': 85,
            'own': 70,
            'friend': 50,
            'neutral': 30,
            'enemy': 15,
            'debilitated': 5
        }
        return (dignity_values.get(planet1_dignity, 30) + 
                dignity_values.get(planet2_dignity, 30)) / 2
    
    def _calculate_relationship_strength(
        self,
        planet1: str,
        planet2: str
    ) -> float:
        """Calculate strength based on planetary relationships"""
        if planet1 in self.PLANETARY_RELATIONSHIPS:
            if planet2 in self.PLANETARY_RELATIONSHIPS[planet1]['friend']:
                return 100
            elif planet2 in self.PLANETARY_RELATIONSHIPS[planet1]['enemy']:
                return 25
        return 50  # Neutral
    
    def _calculate_house_position_strength(
        self,
        house1: int,
        house2: int
    ) -> float:
        """Calculate strength based on house positions"""
        # Stronger in angles (1, 4, 7, 10)
        angles = {1, 4, 7, 10}
        if house1 in angles and house2 in angles:
            return 100
        elif house1 in angles or house2 in angles:
            return 75
        return 50
    
    def calculate_aspect_angle(self, long1: float, long2: float) -> float:
        """Calculate the aspect angle between two longitudes."""
        diff = abs(long1 - long2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def is_aspect_within_orb(self, angle1: float, angle2: float, orb: float) -> bool:
        """Check if two angles form an aspect within the given orb."""
        return abs(angle1 - angle2) <= orb

    def get_aspect_type(self, angle: float, orb: float) -> Optional[str]:
        """Get the type of aspect based on the angle."""
        for aspect_name, aspect in self.ASPECTS.items():
            if aspect.is_major and self.is_aspect_within_orb(aspect.angle, angle, orb):
                return aspect_name.lower()
        return None

    def calculate_planet_aspects(self, planet_positions: Dict[str, float], orb: float) -> List[Dict[str, Any]]:
        """Calculate aspects between planets."""
        aspects = []
        planets = list(planet_positions.keys())

        for i, planet1 in enumerate(planets):
            for planet2 in planets[i+1:]:
                angle = self.calculate_aspect_angle(
                    planet_positions[planet1],
                    planet_positions[planet2]
                )
                aspect_type = self.get_aspect_type(angle, orb)
                if aspect_type:
                    aspects.append({
                        "planet1": planet1,
                        "planet2": planet2,
                        "angle": angle,
                        "aspect": aspect_type,
                        "orb": abs(angle - self.ASPECTS[aspect_type.title()].angle)
                    })
        return aspects

    @staticmethod
    def _is_applying(planet1: Dict[str, Any], planet2: Dict[str, Any]) -> bool:
        """Enhanced determination of applying vs separating aspect"""
        if "speed" not in planet1 or "speed" not in planet2:
            return False
            
        # Consider both longitudinal and latitudinal motion
        relative_speed = (
            planet1.get("speed", 0) - planet2.get("speed", 0)
        )
        
        # Consider retrograde motion
        is_p1_retro = planet1.get("is_retrograde", False)
        is_p2_retro = planet2.get("is_retrograde", False)
        
        if is_p1_retro and is_p2_retro:
            return relative_speed > 0
        elif is_p1_retro or is_p2_retro:
            return relative_speed < 0
            
        return relative_speed < 0  # Normal case

    def calculate_aspect_strength(
        self,
        aspect: Aspect,
        planet1: Dict[str, Any],
        planet2: Dict[str, Any],
        orb: float
    ) -> float:
        """Calculate comprehensive aspect strength"""
        strengths = []
        
        # Calculate individual strength components
        strengths.append(self._calculate_orb_strength(aspect, orb))
        strengths.append(self._calculate_speed_strength(
            planet1.get('speed', 0),
            planet2.get('speed', 0)
        ))
        strengths.append(self._calculate_dignity_strength(
            planet1.get('dignity', 'neutral'),
            planet2.get('dignity', 'neutral')
        ))
        strengths.append(self._calculate_relationship_strength(
            planet1['name'],
            planet2['name']
        ))
        strengths.append(self._calculate_house_position_strength(
            planet1.get('house', 1),
            planet2.get('house', 1)
        ))
        
        # Weight and combine strengths
        weights = [0.3, 0.15, 0.2, 0.2, 0.15]  # Must sum to 1
        total_strength = sum(s * w for s, w in zip(strengths, weights))
        
        return total_strength
    
    def calculate_total_influence(
        self,
        aspect: Aspect,
        strength: float,
        is_applying: bool
    ) -> float:
        """Calculate total influence of the aspect"""
        # Base influence from aspect strength and type
        influence = (strength * aspect.strength) / 100
        
        # Modify based on whether aspect is applying or separating
        influence *= 1.2 if is_applying else 0.8
        
        # Apply benefic/malefic nature
        influence *= (1 + aspect.benefic_nature / 100)
        
        return max(0, min(100, influence))
    
    def calculate_aspects(
        self,
        planetary_positions: Dict[str, Dict[str, Any]]
    ) -> List[PlanetaryAspect]:
        """Calculate enhanced aspects between planets"""
        aspects = []
        planets = list(planetary_positions.keys())

        for i, planet1 in enumerate(planets):
            for planet2 in planets[i+1:]:
                # Get planet details
                p1_data = planetary_positions[planet1]
                p2_data = planetary_positions[planet2]
                
                # Calculate basic angular difference
                long1 = p1_data["longitude"]
                long2 = p2_data["longitude"]
                diff = self.calculate_aspect_angle(long1, long2)
                
                # Check for aspects
                for aspect in self.ASPECTS.values():
                    if self.is_aspect_within_orb(aspect.angle, diff, aspect.orb):
                        # Calculate if aspect is applying
                        is_applying = self._is_applying(p1_data, p2_data)
                        
                        # Calculate orb
                        orb = abs(diff - aspect.angle)
                        
                        # Calculate strength
                        strength = self.calculate_aspect_strength(
                            aspect,
                            {'name': planet1, **p1_data},
                            {'name': planet2, **p2_data},
                            orb
                        )
                        
                        # Calculate total influence
                        total_influence = self.calculate_total_influence(
                            aspect,
                            strength,
                            is_applying
                        )
                        
                        # Create PlanetaryAspect object
                        planetary_aspect = PlanetaryAspect(
                            planet1=planet1,
                            planet2=planet2,
                            aspect=aspect,
                            orb=round(orb, 2),
                            is_applying=is_applying,
                            strength=round(strength, 2),
                            total_influence=round(total_influence, 2)
                        )
                        
                        aspects.append(planetary_aspect)
        
        return aspects
    
    def calculate_special_aspects(
        self,
        planet: str,
        house: int,
        special_aspects: Optional[List[int]] = None
    ) -> List[int]:
        """Calculate special aspects for planets"""
        if special_aspects is None:
            special_aspects = self.SPECIAL_ASPECTS.get(planet, [])
        
        aspected_houses = []
        for aspect in special_aspects:
            aspected_house = (house + aspect - 1) % 12 + 1
            aspected_houses.append(aspected_house)
        
        return aspected_houses
