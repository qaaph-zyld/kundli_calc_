"""Ashtakavarga Calculation System
===================================
Implements complete Ashtakavarga (Eight-Fold Strength) as per BPHS Ch.51-52.

Ashtakavarga measures benefic points (bindus) contributed to each house
from 8 reference points: Lagna and 7 planets (Sun through Saturn).

Reference: Brihat Parashara Hora Shastra, Chapters 51-52
           Phaladeepika, Chapter 9
           Saravali, Chapter 38

Traditional Usage:
- Sarvashtakavarga: Total bindus across all planets (minimum 28 per house)
- Individual Ashtakavarga: Planet-specific strength per house
- Transit analysis: Planet transits give results when crossing high-bindu houses
- Dasha results: Ashtakavarga modulates Vimshottari results
"""
from typing import Dict, List, Tuple, Any
from decimal import Decimal
from dataclasses import dataclass

class Ashtakavarga:
    """
    Implements Ashtakavarga calculations for analyzing planetary strengths and influences
    """
    
    # Benefic points for each planet in houses (1-12)
    benefic_points = {
        'Sun': [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon': [3, 6, 7, 8, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 7, 8, 9, 10, 11],
        'Jupiter': [1, 2, 3, 4, 7, 8, 9, 10, 11],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 10, 11],
        'Saturn': [3, 5, 6, 8, 9, 10, 11]
    }
    
    # Complete BPHS Ashtakavarga Tables
    # Format: {reference_point: {target_planet: [houses_getting_bindus]}}
    # Reference points: Lagna, Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
    # Houses are numbered 1-12 from reference point
    
    ASHTAKAVARGA_TABLES = {
        # SUN ASHTAKAVARGA (Ravi Ashtakavarga)
        'Sun': {
            'Lagna': [1, 2, 4, 7, 8, 9, 10, 11],
            'Sun': [1, 2, 4, 7, 8, 9, 10, 11],
            'Moon': [3, 6, 10, 11],
            'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
            'Mercury': [3, 5, 6, 9, 10, 11, 12],
            'Jupiter': [5, 6, 9, 11],
            'Venus': [6, 7, 12],
            'Saturn': [1, 2, 4, 7, 8, 9, 10, 11]
        },
        # MOON ASHTAKAVARGA (Chandra Ashtakavarga)
        'Moon': {
            'Lagna': [3, 6, 7, 8, 10, 11],
            'Sun': [3, 6, 7, 8, 10, 11],
            'Moon': [1, 3, 6, 7, 10, 11],
            'Mars': [2, 3, 5, 6, 9, 10, 11],
            'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
            'Jupiter': [1, 4, 7, 8, 10, 11, 12],
            'Venus': [3, 4, 5, 7, 9, 10, 11],
            'Saturn': [3, 5, 6, 11]
        },
        # MARS ASHTAKAVARGA (Mangal/Kuja Ashtakavarga)
        'Mars': {
            'Lagna': [1, 2, 4, 7, 8, 10, 11],
            'Sun': [3, 5, 6, 10, 11],
            'Moon': [3, 6, 11],
            'Mars': [1, 2, 4, 7, 8, 10, 11],
            'Mercury': [3, 5, 6, 11],
            'Jupiter': [6, 10, 11, 12],
            'Venus': [6, 8, 11, 12],
            'Saturn': [1, 4, 7, 8, 9, 10, 11]
        },
        # MERCURY ASHTAKAVARGA (Budha Ashtakavarga)
        'Mercury': {
            'Lagna': [1, 3, 5, 6, 9, 10, 11, 12],
            'Sun': [5, 6, 9, 11, 12],
            'Moon': [2, 4, 6, 8, 10, 11],
            'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
            'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
            'Jupiter': [6, 8, 11, 12],
            'Venus': [1, 2, 3, 4, 5, 8, 9, 11],
            'Saturn': [1, 2, 4, 7, 8, 9, 10, 11]
        },
        # JUPITER ASHTAKAVARGA (Guru Ashtakavarga)
        'Jupiter': {
            'Lagna': [1, 2, 3, 4, 7, 8, 9, 10, 11],
            'Sun': [1, 2, 3, 4, 7, 8, 9, 10, 11],
            'Moon': [2, 5, 7, 9, 11],
            'Mars': [1, 2, 4, 7, 8, 10, 11],
            'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
            'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
            'Venus': [2, 5, 6, 9, 10, 11],
            'Saturn': [3, 5, 6, 12]
        },
        # VENUS ASHTAKAVARGA (Shukra Ashtakavarga)
        'Venus': {
            'Lagna': [1, 2, 3, 4, 5, 8, 9, 11, 12],
            'Sun': [8, 11, 12],
            'Moon': [1, 2, 3, 4, 5, 8, 9, 11, 12],
            'Mars': [3, 4, 6, 9, 11, 12],
            'Mercury': [3, 5, 6, 9, 11],
            'Jupiter': [5, 8, 9, 10, 11],
            'Venus': [1, 2, 3, 4, 5, 8, 9, 10, 11],
            'Saturn': [3, 4, 5, 8, 9, 10, 11]
        },
        # SATURN ASHTAKAVARGA (Shani Ashtakavarga)
        'Saturn': {
            'Lagna': [3, 5, 6, 11],
            'Sun': [1, 2, 4, 7, 8, 10, 11],
            'Moon': [3, 6, 11],
            'Mars': [3, 5, 6, 10, 11, 12],
            'Mercury': [6, 8, 9, 10, 11, 12],
            'Jupiter': [5, 6, 11, 12],
            'Venus': [6, 11, 12],
            'Saturn': [3, 5, 6, 11]
        }
    }
    
    @classmethod
    def calculate_bindus(cls, 
                        planet: str, 
                        house: int, 
                        planet_positions: Dict[str, int]) -> int:
        """
        Calculate bindus (benefic points) for a planet in a house
        
        Args:
            planet: Name of the planet
            house: House number (1-12)
            planet_positions: Dictionary of planet positions in houses
            
        Returns:
            Number of bindus
        """
        bindus = 0
        
        # Check if house is benefic for the planet itself
        if house in cls.benefic_points.get(planet, []):
            bindus += 1
            
        # Add contributions from other planets
        for contributing_planet, position in planet_positions.items():
            if contributing_planet == planet:
                continue
                
            # Calculate relative house position
            relative_house = ((house - position) % 12) + 1
            
            # Check if this relative position contributes a bindu
            if (planet in cls.contribution_matrix and 
                contributing_planet in cls.contribution_matrix[planet] and
                relative_house in cls.contribution_matrix[planet][contributing_planet]):
                bindus += 1
                
        return bindus
    
    @classmethod
    def calculate_sarvashtakavarga(cls, 
                                 planet_positions: Dict[str, int]) -> Dict[str, List[int]]:
        """
        Calculate Sarvashtakavarga (combined Ashtakavarga) for all planets
        
        Args:
            planet_positions: Dictionary of planet positions in houses
            
        Returns:
            Dictionary of bindu counts for each house for each planet
        """
        result = {}
        
        for planet in cls.benefic_points.keys():
            planet_bindus = []
            for house in range(1, 13):
                bindus = cls.calculate_bindus(planet, house, planet_positions)
                planet_bindus.append(bindus)
            result[planet] = planet_bindus
            
        return result
    
    @classmethod
    def calculate_house_strength(cls, 
                               house: int, 
                               sarvashtakavarga: Dict[str, List[int]]) -> Decimal:
        """
        Calculate overall strength of a house based on Sarvashtakavarga
        
        Args:
            house: House number (1-12)
            sarvashtakavarga: Dictionary of bindu counts from calculate_sarvashtakavarga
            
        Returns:
            Strength value between 0 and 1
        """
        total_bindus = 0
        max_possible = len(cls.benefic_points) * 7  # Maximum possible bindus per house
        
        for planet, bindus in sarvashtakavarga.items():
            total_bindus += bindus[house - 1]
            
        return Decimal(total_bindus) / Decimal(max_possible)
    
    @classmethod
    def get_strong_houses(cls, 
                         sarvashtakavarga: Dict[str, List[int]], 
                         threshold: Decimal = Decimal('0.5')) -> List[int]:
        """
        Identify houses with strength above threshold
        
        Args:
            sarvashtakavarga: Dictionary of bindu counts
            threshold: Minimum strength threshold (0-1)
            
        Returns:
            List of house numbers with strength above threshold
        """
        strong_houses = []
        
        for house in range(1, 13):
            strength = cls.calculate_house_strength(house, sarvashtakavarga)
            if strength >= threshold:
                strong_houses.append(house)
                
        return strong_houses
    
    @classmethod
    def analyze_planet_strength(cls, 
                              planet: str, 
                              sarvashtakavarga: Dict[str, List[int]]) -> Dict[str, any]:
        """
        Analyze overall strength and placement quality for a planet
        
        Args:
            planet: Name of the planet
            sarvashtakavarga: Dictionary of bindu counts
            
        Returns:
            Dictionary containing strength analysis
        """
        if planet not in sarvashtakavarga:
            return {
                'strength': Decimal('0'),
                'favorable_houses': [],
                'unfavorable_houses': [],
                'recommendations': []
            }
            
        bindus = sarvashtakavarga[planet]
        total_bindus = sum(bindus)
        max_possible = 12 * 7  # Maximum possible bindus for all houses
        
        strength = Decimal(total_bindus) / Decimal(max_possible)
        
        # Identify favorable and unfavorable houses
        favorable_houses = [i + 1 for i, b in enumerate(bindus) if b >= 4]
        unfavorable_houses = [i + 1 for i, b in enumerate(bindus) if b <= 2]
        
        # Generate recommendations
        recommendations = []
        if strength >= Decimal('0.7'):
            recommendations.append(f"Strong {planet} placement - good for {planet}-related activities")
        elif strength <= Decimal('0.3'):
            recommendations.append(f"Weak {planet} placement - {planet}-related activities need caution")
            
        if favorable_houses:
            recommendations.append(f"Houses {favorable_houses} are strong for {planet}")
        if unfavorable_houses:
            recommendations.append(f"Houses {unfavorable_houses} are weak for {planet}")
            
        return {
            'strength': strength,
            'favorable_houses': favorable_houses,
            'unfavorable_houses': unfavorable_houses,
            'recommendations': recommendations
        }
