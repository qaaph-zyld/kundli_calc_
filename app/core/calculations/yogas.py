"""
Yogas Identification Module
PGF Protocol: CALC_006
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum

class YogaCategory(Enum):
    """Categories of Vedic Yogas."""
    DHANA = "dhana"  # Wealth
    RAJA = "raja"    # Power and Authority
    BRAHMA = "brahma"  # Spiritual
    KAMA = "kama"    # Pleasure
    MOKSHA = "moksha"  # Liberation
    ARISHTA = "arishta"  # Difficulties

@dataclass
class YogaDefinition:
    """Definition of a Yoga formation."""
    name: str
    category: YogaCategory
    strength: float
    description: str
    effects: List[str]

class YogaCalculator:
    """Calculator for identifying Yogas in a birth chart."""
    
    def __init__(self):
        """Initialize Yoga calculator."""
        self.chart_yogas: List[Dict] = []
        self.initialize_yoga_definitions()
    
    def initialize_yoga_definitions(self):
        """Initialize definitions of various Yogas."""
        self.yoga_definitions = {
            # Dhana (Wealth) Yogas
            "Lakshmi": YogaDefinition(
                name="Lakshmi Yoga",
                category=YogaCategory.DHANA,
                strength=0.8,
                description="Formation between Jupiter and Venus",
                effects=["Material prosperity", "Financial success"]
            ),
            
            # Raja (Power) Yogas
            "Raj": YogaDefinition(
                name="Raj Yoga",
                category=YogaCategory.RAJA,
                strength=1.0,
                description="Lords of trine and quadrant houses conjunct",
                effects=["Authority", "Leadership", "Success"]
            ),
            
            # Brahma (Spiritual) Yogas
            "Hamsa": YogaDefinition(
                name="Hamsa Yoga",
                category=YogaCategory.BRAHMA,
                strength=0.9,
                description="Jupiter in Kendra from Moon",
                effects=["Spiritual inclination", "Wisdom"]
            ),
            
            # And many more Yoga definitions...
        }
    
    def check_house_lordship(
        self,
        planet: str,
        houses: Dict[str, List[str]]
    ) -> List[int]:
        """Get houses lorded by a planet."""
        lordships = []
        for house_num, planets in houses.items():
            if planet in planets:
                lordships.append(int(house_num))
        return lordships
    
    def is_kendra_house(self, house: int) -> bool:
        """Check if house is a Kendra (angular) house."""
        return house in [1, 4, 7, 10]
    
    def is_trine_house(self, house: int) -> bool:
        """Check if house is a Trine house."""
        return house in [1, 5, 9]
    
    def get_house_distance(self, house1: int, house2: int) -> int:
        """Calculate distance between two houses."""
        diff = abs(house1 - house2)
        return min(diff, 12 - diff)
    
    def check_dhana_yogas(
        self,
        planet_positions: Dict[str, float],
        houses: Dict[str, List[str]]
    ) -> List[Dict]:
        """Check for wealth-related Yogas."""
        dhana_yogas = []
        
        # Check Lakshmi Yoga
        if ("Jupiter" in planet_positions and "Venus" in planet_positions):
            jupiter_house = next(
                (h for h, p in houses.items() if "Jupiter" in p),
                None
            )
            venus_house = next(
                (h for h, p in houses.items() if "Venus" in p),
                None
            )
            
            if jupiter_house and venus_house:
                if self.get_house_distance(
                    int(jupiter_house),
                    int(venus_house)
                ) in [0, 4, 7, 10]:
                    dhana_yogas.append({
                        "name": "Lakshmi Yoga",
                        "strength": self.yoga_definitions["Lakshmi"].strength,
                        "description": self.yoga_definitions["Lakshmi"].description,
                        "effects": self.yoga_definitions["Lakshmi"].effects
                    })
        
        return dhana_yogas
    
    def check_raja_yogas(
        self,
        planet_positions: Dict[str, float],
        houses: Dict[str, List[str]]
    ) -> List[Dict]:
        """Check for Raja (power) Yogas."""
        raja_yogas = []
        
        # Get lords of kendras and trines
        kendra_lords = set()
        trine_lords = set()
        
        for planet, pos in planet_positions.items():
            lordships = self.check_house_lordship(planet, houses)
            
            if any(self.is_kendra_house(h) for h in lordships):
                kendra_lords.add(planet)
            if any(self.is_trine_house(h) for h in lordships):
                trine_lords.add(planet)
        
        # Check for Raja Yoga
        common_lords = kendra_lords.intersection(trine_lords)
        if common_lords:
            raja_yogas.append({
                "name": "Raj Yoga",
                "strength": self.yoga_definitions["Raj"].strength,
                "description": self.yoga_definitions["Raj"].description,
                "effects": self.yoga_definitions["Raj"].effects,
                "planets": list(common_lords)
            })
        
        return raja_yogas
    
    def check_spiritual_yogas(
        self,
        planet_positions: Dict[str, float],
        houses: Dict[str, List[str]]
    ) -> List[Dict]:
        """Check for spiritual Yogas."""
        spiritual_yogas = []
        
        # Check Hamsa Yoga
        if "Jupiter" in planet_positions and "Moon" in planet_positions:
            moon_house = next(
                (h for h, p in houses.items() if "Moon" in p),
                None
            )
            jupiter_house = next(
                (h for h, p in houses.items() if "Jupiter" in p),
                None
            )
            
            if moon_house and jupiter_house:
                if self.is_kendra_house(
                    self.get_house_distance(
                        int(moon_house),
                        int(jupiter_house)
                    )
                ):
                    spiritual_yogas.append({
                        "name": "Hamsa Yoga",
                        "strength": self.yoga_definitions["Hamsa"].strength,
                        "description": self.yoga_definitions["Hamsa"].description,
                        "effects": self.yoga_definitions["Hamsa"].effects
                    })
        
        return spiritual_yogas
    
    def identify_all_yogas(
        self,
        planet_positions: Dict[str, float],
        houses: Dict[str, List[str]],
        aspects: List[Dict]
    ) -> List[Dict]:
        """Identify all Yogas present in the birth chart."""
        self.chart_yogas = []
        
        # Check different categories of Yogas
        self.chart_yogas.extend(
            self.check_dhana_yogas(planet_positions, houses)
        )
        self.chart_yogas.extend(
            self.check_raja_yogas(planet_positions, houses)
        )
        self.chart_yogas.extend(
            self.check_spiritual_yogas(planet_positions, houses)
        )
        
        # Sort Yogas by strength
        self.chart_yogas.sort(key=lambda x: x["strength"], reverse=True)
        
        return self.chart_yogas
    
    def get_yoga_effects(self) -> Dict[YogaCategory, List[Dict]]:
        """Get effects of Yogas by category."""
        effects = {category: [] for category in YogaCategory}
        
        for yoga in self.chart_yogas:
            yoga_def = self.yoga_definitions.get(yoga["name"])
            if yoga_def:
                effects[yoga_def.category].append({
                    "yoga": yoga["name"],
                    "strength": yoga["strength"],
                    "effects": yoga["effects"]
                })
        
        return effects
    
    def get_prominent_yogas(
        self,
        min_strength: float = 0.7
    ) -> List[Dict]:
        """Get prominent Yogas in the chart."""
        return [
            yoga for yoga in self.chart_yogas
            if yoga["strength"] >= min_strength
        ]
    
    def get_yoga_recommendations(self) -> Dict[str, List[str]]:
        """Get recommendations based on Yoga formations."""
        recommendations = {
            "favorable_periods": [],
            "activities": [],
            "remedies": []
        }
        
        for yoga in self.chart_yogas:
            if yoga["strength"] >= 0.8:
                # Add yoga-specific recommendations
                if yoga["name"] == "Lakshmi Yoga":
                    recommendations["activities"].extend([
                        "Financial investments",
                        "Business ventures"
                    ])
                elif yoga["name"] == "Raj Yoga":
                    recommendations["favorable_periods"].extend([
                        "Career advancement",
                        "Leadership roles"
                    ])
                elif yoga["name"] == "Hamsa Yoga":
                    recommendations["activities"].extend([
                        "Spiritual practices",
                        "Meditation"
                    ])
        
        return recommendations
