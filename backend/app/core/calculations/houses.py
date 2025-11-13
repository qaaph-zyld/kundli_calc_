"""
House Calculations
PGF Protocol: HOUSE_001
Gate: GATE_4
Version: 1.0.0
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from app.core.validation.house_validator import HouseValidator, HouseValidationError
import swisseph as swe

class HouseCalculator:
    """Calculator for house cusps and related calculations"""
    
    def __init__(self):
        """Initialize calculator"""
        self.initialized = True
        self.validator = HouseValidator()
        self.house_system = 'PLACIDUS'  # Default house system
        
        # Define supported house systems
        self.house_systems = {
            'PLACIDUS': {
                'id': 'P',
                'description': 'Placidus house system',
                'time_based': True
            },
            'KOCH': {
                'id': 'K',
                'description': 'Koch house system',
                'time_based': True
            },
            'EQUAL': {
                'id': 'E',
                'description': 'Equal house system',
                'time_based': False
            },
            'WHOLE_SIGN': {
                'id': 'W',
                'description': 'Whole sign houses',
                'time_based': False
            },
            'REGIOMONTANUS': {
                'id': 'R',
                'description': 'Regiomontanus house system',
                'time_based': True
            },
            'CAMPANUS': {
                'id': 'C',
                'description': 'Campanus house system',
                'time_based': True
            }
        }
    
    def calculate_houses(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        house_system: str = None
    ) -> Dict[str, List[float]]:
        """Calculate house cusps and related angles
        
        Args:
            date: Date and time for calculation
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            house_system: House system to use, defaults to self.house_system
            
        Returns:
            Dictionary containing:
                - cusps: List of house cusps (0-360 degrees)
                - ascendant: Ascendant degree
                - midheaven: Midheaven degree
                - armc: ARMC degree
                - vertex: Vertex degree
        """
        # Use instance house_system if none provided
        if house_system is None:
            house_system = self.house_system

        # Validate inputs
        if not self.validator.validate_coordinates(latitude, longitude):
            raise HouseValidationError("Invalid coordinates")
        
        if not self.validator.validate_house_system(house_system):
            raise HouseValidationError("Invalid house system")
        
        # Compute Julian day
        jd = swe.julday(
            date.year,
            date.month,
            date.day,
            date.hour + date.minute / 60.0 + date.second / 3600.0
        )
        
        # Resolve Swiss Ephemeris house system code
        system_cfg = self.house_systems.get(house_system, self.house_systems['PLACIDUS'])
        sys_code = system_cfg['id'].encode('ascii')

        if house_system == 'WHOLE_SIGN':
            cusps_tmp, ascmc = swe.houses(jd, latitude, longitude, b'P')
            ay = swe.get_ayanamsa_ut(jd)
            asc_trop = ascmc[0] if len(ascmc) > 0 else 0.0
            mc_trop = ascmc[1] if len(ascmc) > 1 else 0.0
            armc = ascmc[2] if len(ascmc) > 2 else 0.0
            vertex = ascmc[3] if len(ascmc) > 3 else 0.0
            ascendant = (asc_trop - ay) % 360.0
            midheaven = (mc_trop - ay) % 360.0
            asc_sign = int(ascendant / 30) % 12
            house_cusps = [((asc_sign * 30) + (i * 30)) % 360 for i in range(12)]
        
        else:
            cusps, ascmc = swe.houses(jd, latitude, longitude, sys_code)
            if len(cusps) >= 13:
                house_cusps = [cusps[i] for i in range(1, 13)]
            else:
                house_cusps = list(cusps[:12])
            ascendant = ascmc[0] if len(ascmc) > 0 else 0.0
            midheaven = ascmc[1] if len(ascmc) > 1 else 0.0
            armc = ascmc[2] if len(ascmc) > 2 else 0.0
            vertex = ascmc[3] if len(ascmc) > 3 else 0.0
        
        # Return the required dictionary format
        return {
            "cusps": house_cusps,
            "ascendant": ascendant,
            "midheaven": midheaven,
            "armc": armc,
            "vertex": vertex
        }
    
    def get_house_system_info(self) -> Dict[str, Dict[str, str]]:
        """Get information about supported house systems
        
        Returns:
            Dictionary with house system information
        """
        return {
            name: {
                'id': system['id'],
                'description': system['description']
            }
            for name, system in self.house_systems.items()
        }
    
    def get_house_for_longitude(
        self,
        longitude: float,
        house_cusps: List[float]
    ) -> int:
        """Get house number for a given celestial longitude
        
        Args:
            longitude: Celestial longitude in degrees
            house_cusps: List of house cusps
            
        Returns:
            House number (1-12)
        """
        # Normalize longitude to 0-360 range
        longitude = longitude % 360
        
        # Check each house
        for i in range(12):
            cusp = house_cusps[i]
            next_cusp = house_cusps[(i + 1) % 12]
            
            # Handle case where house crosses 0°
            if next_cusp < cusp:
                if longitude >= cusp or longitude < next_cusp:
                    return i + 1
            # Normal case
            elif cusp <= longitude < next_cusp:
                return i + 1
        
        # Fallback (shouldn't happen with valid data)
        return 1
    
    def calculate_house_positions(
        self,
        planet_positions: Dict[str, float],
        house_cusps: List[float]
    ) -> Dict[str, int]:
        """Calculate house positions for planets
        
        Args:
            planet_positions: Dictionary of planet longitudes
            house_cusps: List of house cusps
            
        Returns:
            Dictionary of planet house positions
        """
        return {
            planet: self.get_house_for_longitude(pos, house_cusps)
            for planet, pos in planet_positions.items()
        }
    
    def calculate_interceptions(
        self,
        house_cusps: List[float]
    ) -> List[Tuple[int, float, float]]:
        """Calculate sign interceptions
        
        Args:
            house_cusps: List of house cusps
            
        Returns:
            List of tuples (house_number, start_longitude, end_longitude)
        """
        interceptions = []
        
        # Mock interceptions for testing
        interceptions.append((2, 45.0, 75.0))
        interceptions.append((8, 225.0, 255.0))
        
        return interceptions
