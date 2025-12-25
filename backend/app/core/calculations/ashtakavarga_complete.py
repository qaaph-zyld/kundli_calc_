"""Complete Ashtakavarga System
================================
Full implementation of traditional Ashtakavarga per BPHS Chapters 51-52.

Reference Texts:
- Brihat Parashara Hora Shastra (BPHS), Chapters 51-52
- Phaladeepika, Chapter 9  
- Saravali, Chapter 38
- Uttara Kalamrita

Shlokas Referenced:
- BPHS 51.1-5: Introduction to Ashtakavarga
- BPHS 51.6-52: Individual Ashtakavarga tables
- BPHS 52.1-15: Sarvashtakavarga calculation
- BPHS 52.16-25: Reduction (Trikona Shodhana, Ekadhipatya Shodhana)
"""

from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class AshtakavargaResult:
    """Result of Ashtakavarga calculation for a planet"""
    planet: str
    bindus_per_house: List[int]  # 12 houses
    total_bindus: int
    average_bindus: float
    strong_houses: List[int]  # Houses with >=4 bindus
    weak_houses: List[int]  # Houses with <=2 bindus
    benefic_houses: List[int]  # Traditional benefic houses for this planet


class AshtakavargaSystem:
    """Complete Ashtakavarga calculation system per BPHS"""
    
    # Complete BPHS Ashtakavarga Contribution Tables
    # Format: TABLES[target_planet][reference_point] = [houses from reference getting bindu]
    # Reference: BPHS Ch.51, Verses 6-52
    
    TABLES = {
        # SUN ASHTAKAVARGA (Ravi/Surya Ashtakavarga)
        # BPHS 51.6-12
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
        # BPHS 51.13-19
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
        # BPHS 51.20-26
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
        # BPHS 51.27-33
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
        
        # JUPITER ASHTAKAVARGA (Guru/Brihaspati Ashtakavarga)
        # BPHS 51.34-40
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
        # BPHS 51.41-47
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
        # BPHS 51.48-52
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
    
    def __init__(self):
        """Initialize Ashtakavarga calculator"""
        self.planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        self.reference_points = ['Lagna', 'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    
    def calculate_individual_ashtakavarga(
        self,
        planet: str,
        planet_positions: Dict[str, float],  # Longitudes in degrees
        ascendant: float
    ) -> AshtakavargaResult:
        """Calculate Ashtakavarga for a single planet
        
        Args:
            planet: Target planet name
            planet_positions: Dict of planet longitudes {planet: degrees}
            ascendant: Ascendant longitude in degrees
            
        Returns:
            AshtakavargaResult with bindus for all 12 houses
            
        Reference: BPHS 51.6-52
        """
        if planet not in self.TABLES:
            raise ValueError(f"No Ashtakavarga table for {planet}")
        
        # Convert longitudes to house positions (sign numbers 0-11)
        positions = {'Lagna': int(ascendant / 30)}
        for p, lon in planet_positions.items():
            if p in self.reference_points:
                positions[p] = int(lon / 30)
        
        # Calculate bindus for each house
        bindus = [0] * 12
        
        table = self.TABLES[planet]
        
        for ref_point in self.reference_points:
            if ref_point not in positions:
                continue
                
            ref_sign = positions[ref_point]
            
            # Get contributing houses from this reference point
            if ref_point in table:
                contributing_houses = table[ref_point]
                
                # Convert to absolute house numbers
                for rel_house in contributing_houses:
                    abs_house = (ref_sign + rel_house - 1) % 12
                    bindus[abs_house] += 1
        
        # Analyze strength
        total = sum(bindus)
        avg = total / 12.0
        strong = [i+1 for i, b in enumerate(bindus) if b >= 4]
        weak = [i+1 for i, b in enumerate(bindus) if b <= 2]
        
        # Traditional benefic houses (based on average)
        benefic = [i+1 for i, b in enumerate(bindus) if b > avg]
        
        return AshtakavargaResult(
            planet=planet,
            bindus_per_house=bindus,
            total_bindus=total,
            average_bindus=round(avg, 2),
            strong_houses=strong,
            weak_houses=weak,
            benefic_houses=benefic
        )
    
    def calculate_sarvashtakavarga(
        self,
        planet_positions: Dict[str, float],
        ascendant: float
    ) -> Dict[str, Any]:
        """Calculate Sarvashtakavarga (combined Ashtakavarga of all planets)
        
        Reference: BPHS 52.1-15
        Sarvashtakavarga shows total benefic points in each house from all planets.
        Minimum 28 bindus required for a house to be considered strong.
        
        Args:
            planet_positions: Planet longitudes
            ascendant: Ascendant longitude
            
        Returns:
            Dict with individual results and combined totals
        """
        individual_results = {}
        sarva_bindus = [0] * 12
        
        # Calculate for each planet
        for planet in self.planets:
            result = self.calculate_individual_ashtakavarga(planet, planet_positions, ascendant)
            individual_results[planet] = result
            
            # Add to Sarvashtakavarga total
            for i, b in enumerate(result.bindus_per_house):
                sarva_bindus[i] += b
        
        # Analyze Sarvashtakavarga
        sarva_total = sum(sarva_bindus)
        sarva_avg = sarva_total / 12.0
        
        # Houses with >= 28 bindus are considered very strong (BPHS standard)
        very_strong = [i+1 for i, b in enumerate(sarva_bindus) if b >= 28]
        strong = [i+1 for i, b in enumerate(sarva_bindus) if 25 <= b < 28]
        weak = [i+1 for i, b in enumerate(sarva_bindus) if b < 25]
        
        return {
            'individual_ashtakavarga': {
                p: {
                    'bindus': r.bindus_per_house,
                    'total': r.total_bindus,
                    'average': r.average_bindus,
                    'strong_houses': r.strong_houses,
                    'weak_houses': r.weak_houses,
                    'benefic_houses': r.benefic_houses
                }
                for p, r in individual_results.items()
            },
            'sarvashtakavarga': {
                'bindus_per_house': sarva_bindus,
                'total_bindus': sarva_total,
                'average_bindus': round(sarva_avg, 2),
                'very_strong_houses': very_strong,  # >= 28 bindus
                'strong_houses': strong,  # 25-27 bindus
                'weak_houses': weak,  # < 25 bindus
                'interpretation': self._interpret_sarvashtakavarga(sarva_bindus)
            },
            'reference': 'BPHS Chapters 51-52, Phaladeepika Chapter 9'
        }
    
    def _interpret_sarvashtakavarga(self, bindus: List[int]) -> Dict[str, str]:
        """Provide traditional interpretation of Sarvashtakavarga
        
        Reference: BPHS 52.16-25, Phaladeepika 9.10-15
        """
        interpretations = {}
        
        house_names = ['1st (Lagna)', '2nd (Wealth)', '3rd (Siblings)', '4th (Mother)', 
                       '5th (Children)', '6th (Enemies)', '7th (Spouse)', '8th (Longevity)',
                       '9th (Fortune)', '10th (Career)', '11th (Gains)', '12th (Loss)']
        
        for i, (house, b) in enumerate(zip(house_names, bindus)):
            if b >= 30:
                strength = "Excellent"
                interpretation = f"Very strong house - results manifest fully and easily"
            elif b >= 28:
                strength = "Very Good"
                interpretation = f"Strong house - good results with moderate effort"
            elif b >= 25:
                strength = "Good"
                interpretation = f"Above average - results manifest with consistent effort"
            elif b >= 22:
                strength = "Moderate"
                interpretation = f"Average house - mixed results, requires sustained effort"
            elif b >= 18:
                strength = "Weak"
                interpretation = f"Below average - challenges likely, results need patience"
            else:
                strength = "Very Weak"
                interpretation = f"Difficult house - significant obstacles, remedial measures recommended"
            
            interpretations[house] = {
                'bindus': b,
                'strength': strength,
                'interpretation': interpretation
            }
        
        return interpretations
    
    def apply_trikona_shodhana(
        self,
        sarva_bindus: List[int]
    ) -> List[int]:
        """Apply Trikona Shodhana (Trinal Reduction)
        
        Reference: BPHS 52.26-30
        Reduces bindus in trinal houses (1-5-9, 2-6-10, 3-7-11, 4-8-12)
        to get Sodhya Pinda (reduced points).
        
        Traditional rule: Subtract minimum of each trine set from all three.
        """
        reduced = sarva_bindus.copy()
        
        # Four trine sets
        trine_sets = [
            [0, 4, 8],    # 1-5-9
            [1, 5, 9],    # 2-6-10
            [2, 6, 10],   # 3-7-11
            [3, 7, 11]    # 4-8-12
        ]
        
        for trine in trine_sets:
            # Find minimum in this trine
            min_bindu = min(reduced[i] for i in trine)
            
            # Subtract from all three
            for i in trine:
                reduced[i] -= min_bindu
        
        return reduced
    
    def apply_ekadhipatya_shodhana(
        self,
        individual_results: Dict[str, AshtakavargaResult]
    ) -> Dict[str, List[int]]:
        """Apply Ekadhipatya Shodhana (Same-lordship Reduction)
        
        Reference: BPHS 52.31-35
        For planets ruling same signs (Mercury: Gemini+Virgo, Venus: Taurus+Libra,
        Jupiter: Sagittarius+Pisces, Saturn: Capricorn+Aquarius), reduce bindus
        in one sign by the other.
        """
        reduced_results = {}
        
        # Dual-lordship planets and their signs
        dual_lords = {
            'Mercury': [2, 5],  # Gemini (2), Virgo (5)  [0-indexed]
            'Venus': [1, 6],    # Taurus (1), Libra (6)
            'Jupiter': [8, 11], # Sagittarius (8), Pisces (11)
            'Saturn': [9, 10]   # Capricorn (9), Aquarius (10)
        }
        
        for planet, result in individual_results.items():
            bindus = result.bindus_per_house.copy()
            
            if planet in dual_lords:
                signs = dual_lords[planet]
                sign1, sign2 = signs
                
                # Reduce by minimum
                min_val = min(bindus[sign1], bindus[sign2])
                bindus[sign1] -= min_val
                bindus[sign2] -= min_val
            
            reduced_results[planet] = bindus
        
        return reduced_results
    
    def calculate_prastara_ashtakavarga(
        self,
        planet_positions: Dict[str, float],
        ascendant: float
    ) -> Dict[str, Any]:
        """Calculate Prastara Ashtakavarga (detailed contribution matrix)
        
        Reference: BPHS 52.36-45
        Shows which reference point contributes to which house for each planet.
        Useful for detailed analysis and timing.
        """
        prastara = {}
        
        for planet in self.planets:
            result = self.calculate_individual_ashtakavarga(planet, planet_positions, ascendant)
            
            # Build contribution matrix
            contribution_matrix = {}
            positions = {'Lagna': int(ascendant / 30)}
            for p, lon in planet_positions.items():
                if p in self.reference_points:
                    positions[p] = int(lon / 30)
            
            table = self.TABLES[planet]
            
            for ref_point in self.reference_points:
                if ref_point not in positions or ref_point not in table:
                    continue
                
                ref_sign = positions[ref_point]
                contributing = [0] * 12
                
                for rel_house in table[ref_point]:
                    abs_house = (ref_sign + rel_house - 1) % 12
                    contributing[abs_house] = 1
                
                contribution_matrix[ref_point] = contributing
            
            prastara[planet] = {
                'total_bindus': result.bindus_per_house,
                'contributions': contribution_matrix
            }
        
        return prastara


def calculate_complete_ashtakavarga(
    planet_positions: Dict[str, float],
    ascendant: float,
    apply_reductions: bool = False
) -> Dict[str, Any]:
    """Calculate complete Ashtakavarga analysis
    
    Args:
        planet_positions: Planet longitudes in degrees
        ascendant: Ascendant longitude in degrees
        apply_reductions: Whether to apply Shodhana (reductions)
        
    Returns:
        Complete Ashtakavarga analysis with interpretations
    """
    system = AshtakavargaSystem()
    result = system.calculate_sarvashtakavarga(planet_positions, ascendant)
    
    if apply_reductions:
        # Apply Trikona Shodhana
        sarva_bindus = result['sarvashtakavarga']['bindus_per_house']
        reduced_sarva = system.apply_trikona_shodhana(sarva_bindus)
        
        # Apply Ekadhipatya Shodhana
        individual_results = {
            p: AshtakavargaResult(
                planet=p,
                bindus_per_house=data['bindus'],
                total_bindus=data['total'],
                average_bindus=data['average'],
                strong_houses=data['strong_houses'],
                weak_houses=data['weak_houses'],
                benefic_houses=data['benefic_houses']
            )
            for p, data in result['individual_ashtakavarga'].items()
        }
        reduced_individual = system.apply_ekadhipatya_shodhana(individual_results)
        
        result['reductions'] = {
            'trikona_shodhana': {
                'original': sarva_bindus,
                'reduced': reduced_sarva,
                'interpretation': 'Trinal reduction per BPHS 52.26-30'
            },
            'ekadhipatya_shodhana': {
                'reduced_bindus': reduced_individual,
                'interpretation': 'Dual-lordship reduction per BPHS 52.31-35'
            }
        }
    
    # Add Prastara for detailed analysis
    result['prastara_ashtakavarga'] = system.calculate_prastara_ashtakavarga(
        planet_positions, ascendant
    )
    
    return result
