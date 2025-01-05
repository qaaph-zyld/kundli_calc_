"""
Yoga Analysis Engine
PGF Protocol: YOGA_001
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from datetime import datetime
import logging
from enum import Enum
from collections import defaultdict
import math

class YogaType(Enum):
    RAJAYOGA = "rajayoga"
    DHANYOGA = "dhanyoga"
    PANCHA_MAHAPURUSHA = "pancha_mahapurusha"
    GAJAKESARI = "gajakesari"
    VIPARITA = "viparita"
    NEECHA_BHANGA = "neecha_bhanga"
    PARIVARTANA = "parivartana"
    VESI = "vesi"
    VASI = "vasi"
    UBHAYACHARI = "ubhayachari"

@dataclass
class YogaResult:
    """Represents a detected yoga"""
    yoga_type: YogaType
    name: str
    strength: float
    confidence: float
    planets: List[str]
    houses: List[int]
    effects: Dict[str, float]
    timestamp: datetime
    duration: Optional[float] = None

class YogaEngine:
    """Advanced yoga detection and analysis engine"""
    
    def __init__(self):
        self.detected_yogas: List[YogaResult] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize yoga definitions
        self._initialize_yoga_definitions()
    
    def _initialize_yoga_definitions(self) -> None:
        """Initialize standard yoga definitions"""
        self.raja_yoga_conditions = {
            "kendra_trikona": {
                "lords": ["any"],
                "houses": [1, 4, 7, 10, 5, 9],
                "min_planets": 2,
                "strength": 0.8
            },
            "mutual_aspect": {
                "planets": ["Jupiter", "Venus"],
                "aspect_type": "trine",
                "strength": 0.9
            }
        }
        
        self.dhana_yoga_conditions = {
            "house_2_11": {
                "planets": ["Jupiter", "Venus"],
                "houses": [2, 11],
                "strength": 0.7
            },
            "benefic_aspect": {
                "planets": ["Jupiter", "Venus", "Mercury"],
                "houses": [2, 11],
                "aspect_type": ["trine", "conjunction"],
                "strength": 0.8
            }
        }
        
        self.mahapurusha_conditions = {
            "ruchaka": {
                "planet": "Mars",
                "houses": [1, 4, 7, 10],
                "own_sign": True,
                "strength": 0.9
            },
            "bhadra": {
                "planet": "Mercury",
                "houses": [1, 4, 7, 10],
                "own_sign": True,
                "strength": 0.9
            },
            "hamsa": {
                "planet": "Jupiter",
                "houses": [1, 4, 7, 10],
                "own_sign": True,
                "strength": 0.9
            },
            "malavya": {
                "planet": "Venus",
                "houses": [1, 4, 7, 10],
                "own_sign": True,
                "strength": 0.9
            },
            "sasa": {
                "planet": "Saturn",
                "houses": [1, 4, 7, 10],
                "own_sign": True,
                "strength": 0.9
            }
        }
    
    async def analyze_yogas(
        self,
        chart_data: Dict[str, Any]
    ) -> List[YogaResult]:
        """Analyze chart for yoga formations
        
        Args:
            chart_data: Dictionary containing chart information
            
        Returns:
            List of detected yogas
        """
        results = []
        
        try:
            # Check Raja Yogas
            raja_yogas = await self._check_raja_yogas(chart_data)
            results.extend(raja_yogas)
            
            # Check Dhana Yogas
            dhana_yogas = await self._check_dhana_yogas(chart_data)
            results.extend(dhana_yogas)
            
            # Check Mahapurusha Yogas
            mahapurusha_yogas = await self._check_mahapurusha_yogas(chart_data)
            results.extend(mahapurusha_yogas)
            
            # Check special yogas
            special_yogas = await self._check_special_yogas(chart_data)
            results.extend(special_yogas)
            
            # Store results
            self.detected_yogas.extend(results)
            
        except Exception as e:
            self.logger.error(f"Error analyzing yogas: {str(e)}")
        
        return results
    
    async def _check_raja_yogas(
        self,
        chart_data: Dict[str, Any]
    ) -> List[YogaResult]:
        """Check for Raja Yoga formations"""
        results = []
        planets = chart_data.get("planets", {})
        houses = chart_data.get("houses", {})
        aspects = chart_data.get("aspects", [])
        
        # Check kendra-trikona combinations
        kendra_trikona = self.raja_yoga_conditions["kendra_trikona"]
        for house in kendra_trikona["houses"]:
            house_planets = self._get_planets_in_house(planets, house)
            if len(house_planets) >= kendra_trikona["min_planets"]:
                results.append(YogaResult(
                    yoga_type=YogaType.RAJAYOGA,
                    name=f"Kendra-Trikona Raja Yoga in House {house}",
                    strength=kendra_trikona["strength"],
                    confidence=0.8,
                    planets=house_planets,
                    houses=[house],
                    effects={
                        "power": 0.8,
                        "status": 0.7,
                        "wealth": 0.6
                    },
                    timestamp=datetime.now()
                ))
        
        # Check mutual aspects
        mutual = self.raja_yoga_conditions["mutual_aspect"]
        for aspect in aspects:
            if (aspect["type"] == mutual["aspect_type"] and
                set(aspect["planets"]).issubset(set(mutual["planets"]))):
                results.append(YogaResult(
                    yoga_type=YogaType.RAJAYOGA,
                    name="Mutual Aspect Raja Yoga",
                    strength=mutual["strength"],
                    confidence=0.9,
                    planets=aspect["planets"],
                    houses=[],
                    effects={
                        "power": 0.9,
                        "status": 0.8,
                        "wealth": 0.7
                    },
                    timestamp=datetime.now()
                ))
        
        return results
    
    async def _check_dhana_yogas(
        self,
        chart_data: Dict[str, Any]
    ) -> List[YogaResult]:
        """Check for Dhana Yoga formations"""
        results = []
        planets = chart_data.get("planets", {})
        aspects = chart_data.get("aspects", [])
        
        # Check house placements
        house_condition = self.dhana_yoga_conditions["house_2_11"]
        for house in house_condition["houses"]:
            house_planets = self._get_planets_in_house(planets, house)
            matching_planets = [p for p in house_planets 
                              if p in house_condition["planets"]]
            
            if matching_planets:
                results.append(YogaResult(
                    yoga_type=YogaType.DHANYOGA,
                    name=f"Dhana Yoga in House {house}",
                    strength=house_condition["strength"],
                    confidence=0.7,
                    planets=matching_planets,
                    houses=[house],
                    effects={
                        "wealth": 0.8,
                        "prosperity": 0.7,
                        "abundance": 0.6
                    },
                    timestamp=datetime.now()
                ))
        
        # Check benefic aspects
        benefic = self.dhana_yoga_conditions["benefic_aspect"]
        for aspect in aspects:
            if (aspect["type"] in benefic["aspect_type"] and
                any(p in benefic["planets"] for p in aspect["planets"])):
                results.append(YogaResult(
                    yoga_type=YogaType.DHANYOGA,
                    name="Benefic Aspect Dhana Yoga",
                    strength=benefic["strength"],
                    confidence=0.8,
                    planets=aspect["planets"],
                    houses=[],
                    effects={
                        "wealth": 0.7,
                        "prosperity": 0.8,
                        "abundance": 0.7
                    },
                    timestamp=datetime.now()
                ))
        
        return results
    
    async def _check_mahapurusha_yogas(
        self,
        chart_data: Dict[str, Any]
    ) -> List[YogaResult]:
        """Check for Pancha Mahapurusha Yogas"""
        results = []
        planets = chart_data.get("planets", {})
        
        for yoga_name, condition in self.mahapurusha_conditions.items():
            planet = condition["planet"]
            if planet not in planets:
                continue
                
            planet_data = planets[planet]
            house = planet_data.get("house")
            
            if (house in condition["houses"] and
                (not condition["own_sign"] or 
                 planet_data.get("in_own_sign", False))):
                results.append(YogaResult(
                    yoga_type=YogaType.PANCHA_MAHAPURUSHA,
                    name=f"{yoga_name.title()} Yoga",
                    strength=condition["strength"],
                    confidence=0.9,
                    planets=[planet],
                    houses=[house],
                    effects={
                        "personality": 0.9,
                        "success": 0.8,
                        "leadership": 0.7
                    },
                    timestamp=datetime.now()
                ))
        
        return results
    
    async def _check_special_yogas(
        self,
        chart_data: Dict[str, Any]
    ) -> List[YogaResult]:
        """Check for special yoga formations"""
        results = []
        planets = chart_data.get("planets", {})
        
        # Check Gajakesari Yoga
        if self._check_gajakesari(planets):
            results.append(YogaResult(
                yoga_type=YogaType.GAJAKESARI,
                name="Gajakesari Yoga",
                strength=0.8,
                confidence=0.9,
                planets=["Moon", "Jupiter"],
                houses=[],
                effects={
                    "fortune": 0.8,
                    "wisdom": 0.7,
                    "success": 0.7
                },
                timestamp=datetime.now()
            ))
        
        # Check Viparita Raja Yoga
        viparita = self._check_viparita(planets)
        if viparita:
            results.append(YogaResult(
                yoga_type=YogaType.VIPARITA,
                name="Viparita Raja Yoga",
                strength=0.9,
                confidence=0.8,
                planets=viparita["planets"],
                houses=viparita["houses"],
                effects={
                    "transformation": 0.9,
                    "power": 0.8,
                    "success": 0.8
                },
                timestamp=datetime.now()
            ))
        
        return results
    
    def _get_planets_in_house(
        self,
        planets: Dict[str, Any],
        house: int
    ) -> List[str]:
        """Get list of planets in a specific house"""
        return [
            planet for planet, data in planets.items()
            if data.get("house") == house
        ]
    
    def _check_gajakesari(
        self,
        planets: Dict[str, Any]
    ) -> bool:
        """Check for Gajakesari Yoga formation"""
        if "Moon" not in planets or "Jupiter" not in planets:
            return False
            
        moon_house = planets["Moon"].get("house")
        jupiter_house = planets["Jupiter"].get("house")
        
        if not moon_house or not jupiter_house:
            return False
            
        # Check if Moon and Jupiter are in kendras
        angle = abs(moon_house - jupiter_house)
        return angle in [0, 4, 8] or angle % 3 == 0
    
    def _check_viparita(
        self,
        planets: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Check for Viparita Raja Yoga formation"""
        lords_6_8_12 = set()
        houses_6_8_12 = {6, 8, 12}
        
        # Get lords of 6th, 8th and 12th houses
        for planet, data in planets.items():
            if data.get("lordship") in houses_6_8_12:
                lords_6_8_12.add(planet)
        
        # Check if these lords are in kendra or trikona
        result_planets = []
        result_houses = []
        
        for planet in lords_6_8_12:
            house = planets[planet].get("house")
            if house in {1, 4, 7, 10, 5, 9}:  # Kendra or trikona
                result_planets.append(planet)
                result_houses.append(house)
        
        if result_planets:
            return {
                "planets": result_planets,
                "houses": result_houses
            }
        
        return None
    
    def get_yoga_metrics(self) -> Dict[str, Any]:
        """Get yoga analysis metrics"""
        metrics = {
            "total_yogas": len(self.detected_yogas),
            "yoga_types": defaultdict(int),
            "average_strength": 0.0,
            "average_confidence": 0.0
        }
        
        if self.detected_yogas:
            # Count yoga types
            for yoga in self.detected_yogas:
                metrics["yoga_types"][yoga.yoga_type.value] += 1
            
            # Calculate averages
            metrics["average_strength"] = sum(
                y.strength for y in self.detected_yogas
            ) / len(self.detected_yogas)
            
            metrics["average_confidence"] = sum(
                y.confidence for y in self.detected_yogas
            ) / len(self.detected_yogas)
        
        return metrics
    
    def reset(self) -> None:
        """Reset yoga engine state"""
        self.detected_yogas.clear()
