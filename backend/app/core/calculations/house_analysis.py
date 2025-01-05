from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import math
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

@dataclass
class HouseStrength:
    house_number: int
    natural_strength: float
    occupant_strength: float
    aspect_strength: float
    lord_strength: float
    total_strength: float
    functional_nature: str  # Benefic, Malefic, Mixed
    significations: List[str]
    temporal_strength: float  # New field for time-based strength
    dispositorship_strength: float  # New field for dispositorship analysis

class EnhancedHouseAnalysisEngine:
    def __init__(self):
        # Natural house strengths (based on quadrants and triads)
        self.natural_house_strengths = {
            1: 100,  # Ascendant
            4: 90,   # IC
            7: 95,   # Descendant
            10: 95,  # MC
            2: 60,
            3: 70,
            5: 75,
            6: 50,
            8: 45,
            9: 80,
            11: 65,
            12: 40
        }
        
        # House significations
        self.house_significations = {
            1: ["Self", "Personality", "Physical body", "General well-being"],
            2: ["Wealth", "Family", "Speech", "Resources"],
            3: ["Siblings", "Courage", "Communication", "Short journeys"],
            4: ["Mother", "Education", "Property", "Happiness"],
            5: ["Children", "Intelligence", "Creative pursuits", "Romance"],
            6: ["Enemies", "Disease", "Service", "Debt"],
            7: ["Marriage", "Partnership", "Business", "Foreign travel"],
            8: ["Longevity", "Obstacles", "Hidden knowledge", "Inheritance"],
            9: ["Fortune", "Higher learning", "Dharma", "Long journeys"],
            10: ["Career", "Authority", "Fame", "Father"],
            11: ["Gains", "Friends", "Aspirations", "Elder siblings"],
            12: ["Loss", "Spirituality", "Foreign lands", "Liberation"]
        }
        
        # Functional nature of houses
        self.house_nature = {
            1: "Mixed",
            2: "Benefic",
            3: "Mixed",
            4: "Benefic",
            5: "Benefic",
            6: "Malefic",
            7: "Mixed",
            8: "Malefic",
            9: "Benefic",
            10: "Mixed",
            11: "Benefic",
            12: "Malefic"
        }
        
        # House lordship effects
        self.lordship_effects = {
            'own': 100,       # Lord in own house
            'exalted': 90,    # Lord in exaltation
            'friend': 75,     # Lord in friendly sign
            'neutral': 50,    # Lord in neutral sign
            'enemy': 25,      # Lord in enemy sign
            'debilitated': 10 # Lord in debilitation
        }
        
        # Special house combinations
        self.special_combinations = {
            'trikona': {1, 5, 9},    # Trine houses
            'kendra': {1, 4, 7, 10}, # Angular houses
            'upachaya': {3, 6, 10, 11}, # Growth houses
            'trika': {6, 8, 12},     # Evil houses
            'maraka': {2, 7},        # Death-inflicting houses
            'dusthana': {6, 8, 12}   # Malefic houses
        }
        
        # Add temporal strength factors
        self.temporal_factors = {
            'day': {
                'fire_houses': {1, 5, 9},  # Fire houses stronger during day
                'air_houses': {3, 7, 11},  # Air houses moderate during day
                'multiplier': 1.2
            },
            'night': {
                'water_houses': {4, 8, 12},  # Water houses stronger at night
                'earth_houses': {2, 6, 10},  # Earth houses moderate at night
                'multiplier': 1.15
            }
        }
        
        # Add dispositorship relationships
        self.dispositorship_rules = {
            'mutual_reception': 1.3,  # Lords in mutual reception
            'parivartana': 1.25,     # Lords exchanging houses
            'temporary': 1.1         # Temporary dispositorship
        }
        
        # Initialize thread pool for parallel calculations
        self.executor = ThreadPoolExecutor(max_workers=4)

    @lru_cache(maxsize=128)
    def _calculate_natural_strength(self, house: int) -> float:
        """Calculate natural strength of house based on position with caching"""
        base_strength = self.natural_house_strengths[house]
        
        # Modify based on special combinations
        if house in self.special_combinations['kendra']:
            base_strength *= 1.2
        elif house in self.special_combinations['trikona']:
            base_strength *= 1.1
        elif house in self.special_combinations['dusthana']:
            base_strength *= 0.8
        
        return min(100, base_strength)
    
    async def _calculate_occupant_strength(
        self,
        house: int,
        occupants: List[Dict[str, Any]]
    ) -> float:
        """Calculate strength based on planetary occupants with parallel processing"""
        if not occupants:
            return 50
            
        # Process each occupant in parallel
        futures = []
        for planet in occupants:
            futures.append(
                self.executor.submit(
                    self._process_single_occupant,
                    house,
                    planet
                )
            )
            
        # Gather results
        strengths = [f.result() for f in futures]
        return min(100, sum(strengths) / len(strengths))

    def _process_single_occupant(
        self,
        house: int,
        planet: Dict[str, Any]
    ) -> float:
        """Process a single occupant's strength calculation"""
        planet_strength = planet.get('strength', 50)
        
        # Enhanced dignity calculations
        dignity_factor = {
            'exalted': 1.3,
            'moolatrikona': 1.2,
            'own': 1.1,
            'friend': 1.0,
            'neutral': 0.9,
            'enemy': 0.8,
            'debilitated': 0.7,
            'combust': 0.6,  # New factor for combust planets
            'retrograde': 0.85  # Updated retrograde factor
        }
        
        # Get base dignity
        dignity = planet.get('dignity', 'neutral')
        planet_strength *= dignity_factor[dignity]
        
        # Apply additional factors
        if planet.get('is_retrograde', False):
            planet_strength *= dignity_factor['retrograde']
        if planet.get('is_combust', False):
            planet_strength *= dignity_factor['combust']
            
        # Consider house-specific effects
        if house in self.special_combinations['kendra']:
            if planet.get('name') in ['Jupiter', 'Sun', 'Mars']:
                planet_strength *= 1.1
        elif house in self.special_combinations['trikona']:
            if planet.get('name') in ['Jupiter', 'Venus', 'Mercury']:
                planet_strength *= 1.05
                
        return planet_strength

    def _calculate_aspect_strength(
        self,
        house: int,
        aspects: List[Dict[str, Any]]
    ) -> float:
        """Calculate strength based on aspects to the house"""
        if not aspects:
            return 50  # Base strength for unaspected house
        
        total_strength = 0
        for aspect in aspects:
            # Base aspect strength
            aspect_strength = aspect.get('strength', 50)
            
            # Consider aspect type
            aspect_type_factor = {
                'conjunction': 1.0,
                'trine': 0.9,
                'sextile': 0.8,
                'square': 0.6,
                'opposition': 0.5,
                'none': 0.0  # No aspect effect
            }
            aspect_type = aspect.get('type', 'conjunction')
            aspect_strength *= aspect_type_factor[aspect_type]
            
            # Consider if aspect is applying or separating
            if aspect.get('is_applying', False):
                aspect_strength *= 1.1
            
            total_strength += aspect_strength
        
        # Average the total strength
        return min(100, total_strength / len(aspects))

    def _calculate_lord_strength(
        self,
        house: int,
        lord: Dict[str, Any]
    ) -> float:
        """Calculate strength based on house lord placement"""
        # Base lord strength
        lord_strength = lord.get('strength', 50)
        
        # Modify based on lord's house placement
        current_house = lord.get('house', 1)
        house_relationship = self._get_house_relationship(house, current_house)
        
        relationship_factor = {
            'own': 1.2,
            'exalted': 1.3,
            'friend': 1.1,
            'neutral': 1.0,
            'enemy': 0.8,
            'debilitated': 0.7
        }
        
        lord_strength *= relationship_factor[house_relationship]
        
        # Consider special house placements
        if current_house in self.special_combinations['kendra']:
            lord_strength *= 1.1
        elif current_house in self.special_combinations['trikona']:
            lord_strength *= 1.05
        elif current_house in self.special_combinations['dusthana']:
            lord_strength *= 0.9
        
        return min(100, lord_strength)
    
    def _get_house_relationship(self, house: int, lord_house: int) -> str:
        """Determine relationship between house and its lord's placement"""
        if house == lord_house:
            return 'own'
        
        # Define exaltation houses for each house lord (simplified)
        exaltation_houses = {
            1: 10,  # Leo lord (Sun) exalted in Aries
            2: 9,   # Taurus lord (Venus) exalted in Pisces
            3: 7,   # Gemini lord (Mercury) exalted in Virgo
            4: 1,   # Cancer lord (Moon) exalted in Taurus
            5: 10,  # Leo lord (Sun) exalted in Aries
            6: 7,   # Virgo lord (Mercury) exalted in Virgo
            7: 2,   # Libra lord (Venus) exalted in Pisces
            8: 4,   # Scorpio lord (Mars) exalted in Capricorn
            9: 4,   # Sagittarius lord (Jupiter) exalted in Cancer
            10: 1,  # Capricorn lord (Saturn) exalted in Libra
            11: 1,  # Aquarius lord (Saturn) exalted in Libra
            12: 4   # Pisces lord (Jupiter) exalted in Cancer
        }
        
        if lord_house == exaltation_houses.get(house):
            return 'exalted'
            
        # Check if houses form special combinations
        if lord_house in self.special_combinations['kendra']:
            if house in self.special_combinations['kendra']:
                return 'friend'
        
        if lord_house in self.special_combinations['trikona']:
            if house in self.special_combinations['trikona']:
                return 'friend'
                
        if lord_house in self.special_combinations['dusthana']:
            if house not in self.special_combinations['dusthana']:
                return 'enemy'
                
        if house in self.special_combinations['dusthana']:
            if lord_house not in self.special_combinations['dusthana']:
                return 'enemy'
        
        # Default to neutral for other relationships
        return 'neutral'
    
    def _calculate_temporal_strength(
        self,
        house: int,
        time_of_day: str
    ) -> float:
        """Calculate temporal strength based on time of day"""
        base_strength = 50
        factors = self.temporal_factors[time_of_day]
        
        # Check if house belongs to element groups
        if time_of_day == 'day':
            if house in factors['fire_houses']:
                base_strength *= factors['multiplier']
            elif house in factors['air_houses']:
                base_strength *= (factors['multiplier'] * 0.9)
        else:  # night
            if house in factors['water_houses']:
                base_strength *= factors['multiplier']
            elif house in factors['earth_houses']:
                base_strength *= (factors['multiplier'] * 0.9)
                
        return min(100, base_strength)

    def _calculate_dispositorship_strength(
        self,
        house: int,
        lord: Dict[str, Any],
        all_house_lords: Dict[int, Dict[str, Any]]
    ) -> float:
        """Calculate strength based on dispositorship relationships"""
        base_strength = 50
        lord_planet = lord.get('planet')
        lord_house = lord.get('house')
        
        # Check for mutual reception
        for other_house, other_lord in all_house_lords.items():
            if other_house != house:
                if (other_lord.get('planet') == lord_planet and 
                    other_lord.get('house') == house):
                    base_strength *= self.dispositorship_rules['mutual_reception']
                    break
                    
        # Check for parivartana yoga
        if lord_house in all_house_lords:
            other_lord = all_house_lords[lord_house]
            if other_lord.get('house') == house:
                base_strength *= self.dispositorship_rules['parivartana']
                
        # Check for temporary dispositorship
        if lord.get('temporary_ruler', False):
            base_strength *= self.dispositorship_rules['temporary']
            
        return min(100, base_strength)

    async def analyze_house(
        self,
        house: int,
        occupants: List[Dict[str, Any]],
        aspects: List[Dict[str, Any]],
        lord: Dict[str, Any],
        time_of_day: str = 'day',
        all_house_lords: Optional[Dict[int, Dict[str, Any]]] = None
    ) -> HouseStrength:
        """Enhanced house analysis with temporal and dispositorship factors"""
        # Calculate all strength components
        natural_strength = self._calculate_natural_strength(house)
        occupant_strength = await self._calculate_occupant_strength(house, occupants)
        aspect_strength = self._calculate_aspect_strength(house, aspects)
        lord_strength = self._calculate_lord_strength(house, lord)
        temporal_strength = self._calculate_temporal_strength(house, time_of_day)
        dispositorship_strength = self._calculate_dispositorship_strength(
            house,
            lord,
            all_house_lords or {}
        )
        
        # Calculate total strength with weighted components
        weights = {
            'natural': 0.15,
            'occupant': 0.25,
            'aspect': 0.15,
            'lord': 0.20,
            'temporal': 0.10,
            'dispositorship': 0.15
        }
        
        total_strength = sum(
            strength * weights[component]
            for strength, component in [
                (natural_strength, 'natural'),
                (occupant_strength, 'occupant'),
                (aspect_strength, 'aspect'),
                (lord_strength, 'lord'),
                (temporal_strength, 'temporal'),
                (dispositorship_strength, 'dispositorship')
            ]
        )
        
        return HouseStrength(
            house_number=house,
            natural_strength=round(natural_strength, 2),
            occupant_strength=round(occupant_strength, 2),
            aspect_strength=round(aspect_strength, 2),
            lord_strength=round(lord_strength, 2),
            total_strength=round(total_strength, 2),
            functional_nature=self.house_nature[house],
            significations=self.house_significations[house],
            temporal_strength=round(temporal_strength, 2),
            dispositorship_strength=round(dispositorship_strength, 2)
        )
    
    def analyze_house_combinations(
        self,
        house_strengths: Dict[int, HouseStrength]
    ) -> Dict[str, List[int]]:
        """Analyze special house combinations and their strengths"""
        combinations = {}
        
        # Analyze each special combination
        for combo_name, houses in self.special_combinations.items():
            # Get average strength of houses in combination
            combo_strength = sum(
                house_strengths[h].total_strength for h in houses
            ) / len(houses)
            
            combinations[combo_name] = {
                'houses': list(houses),
                'strength': round(combo_strength, 2)
            }
        
        return combinations
    
    def get_strongest_houses(
        self,
        house_strengths: Dict[int, HouseStrength],
        top_n: int = 3
    ) -> List[HouseStrength]:
        """Get the strongest houses by total strength"""
        sorted_houses = sorted(
            house_strengths.values(),
            key=lambda x: x.total_strength,
            reverse=True
        )
        return sorted_houses[:top_n]
    
    def get_weakest_houses(
        self,
        house_strengths: Dict[int, HouseStrength],
        bottom_n: int = 3
    ) -> List[HouseStrength]:
        """Get the weakest houses by total strength"""
        sorted_houses = sorted(
            house_strengths.values(),
            key=lambda x: x.total_strength
        )
        return sorted_houses[:bottom_n]
