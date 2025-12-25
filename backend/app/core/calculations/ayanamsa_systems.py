"""
Multiple Ayanamsa Systems
=========================
Support for various ayanamsa calculation systems beyond Lahiri.

Supported Systems:
1. Lahiri (Chitrapaksha) - Default, Indian Govt standard
2. Raman - B.V. Raman's system
3. Krishnamurti (KP) - KP system ayanamsa
4. Yukteshwar - Sri Yukteshwar's calculation
5. True Chitrapaksha - Spica-based
6. Fagan-Bradley - Western sidereal
"""

from datetime import datetime, timezone
from typing import Dict
import math


class AyanamsaSystem:
    """Base class for ayanamsa calculation systems"""
    
    def __init__(self, name: str, base_date: datetime, base_value: float, annual_rate: float):
        self.name = name
        self.base_date = base_date
        self.base_value = base_value
        self.annual_rate = annual_rate
    
    def calculate(self, target_date: datetime) -> float:
        """Calculate ayanamsa for given date"""
        # Handle both timezone-aware and naive datetimes
        if target_date.tzinfo is None:
            target_date = target_date.replace(tzinfo=timezone.utc)
        if self.base_date.tzinfo is None:
            base_date = self.base_date.replace(tzinfo=timezone.utc)
        else:
            base_date = self.base_date
        
        years_diff = (target_date - base_date).days / 365.25
        ayanamsa = self.base_value + (years_diff * self.annual_rate)
        return ayanamsa


class AyanamsaCalculator:
    """Calculator for multiple ayanamsa systems"""
    
    # Base date for most systems
    BASE_DATE_1900 = datetime(1900, 1, 1, 0, 0, 0)
    BASE_DATE_1950 = datetime(1950, 1, 1, 0, 0, 0)
    BASE_DATE_2000 = datetime(2000, 1, 1, 0, 0, 0)
    
    # Annual precession rate (approximately 50.29 arc seconds per year)
    ANNUAL_PRECESSION = 50.29 / 3600  # Convert to degrees
    
    def __init__(self):
        """Initialize ayanamsa systems"""
        self.systems: Dict[str, AyanamsaSystem] = {}
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Initialize all supported ayanamsa systems"""
        
        # 1. Lahiri (Chitrapaksha) - Indian standard
        # Base: 22.46° on 1900-01-01
        self.systems['lahiri'] = AyanamsaSystem(
            name="Lahiri (Chitrapaksha)",
            base_date=self.BASE_DATE_1900,
            base_value=22.46,
            annual_rate=self.ANNUAL_PRECESSION
        )
        
        # 2. Raman - B.V. Raman's system
        # Similar to Lahiri but slightly different base
        self.systems['raman'] = AyanamsaSystem(
            name="B.V. Raman",
            base_date=self.BASE_DATE_1900,
            base_value=22.38,  # Slightly less than Lahiri
            annual_rate=self.ANNUAL_PRECESSION
        )
        
        # 3. Krishnamurti (KP) - KP system
        # Base: 22.362222° (22°21'44") on 1900-01-01
        self.systems['kp'] = AyanamsaSystem(
            name="Krishnamurti (KP)",
            base_date=self.BASE_DATE_1900,
            base_value=22.362222,
            annual_rate=50.2388475 / 3600  # KP specific rate
        )
        
        # 4. Yukteshwar - Sri Yukteshwar's calculation
        # Based on his book "The Holy Science"
        self.systems['yukteshwar'] = AyanamsaSystem(
            name="Yukteshwar",
            base_date=self.BASE_DATE_1900,
            base_value=20.54,  # Significantly different
            annual_rate=self.ANNUAL_PRECESSION
        )
        
        # 5. True Chitrapaksha - Spica-based
        # Based on actual star Spica (Chitra)
        self.systems['true_chitra'] = AyanamsaSystem(
            name="True Chitrapaksha (Spica)",
            base_date=self.BASE_DATE_2000,
            base_value=23.85,
            annual_rate=self.ANNUAL_PRECESSION
        )
        
        # 6. Fagan-Bradley - Western sidereal
        # Used by Western sidereal astrologers
        self.systems['fagan_bradley'] = AyanamsaSystem(
            name="Fagan-Bradley",
            base_date=self.BASE_DATE_1950,
            base_value=24.02,  # Different zero point
            annual_rate=self.ANNUAL_PRECESSION
        )
        
        # 7. DeLuce - Another Western system
        self.systems['deluce'] = AyanamsaSystem(
            name="DeLuce",
            base_date=self.BASE_DATE_1900,
            base_value=22.90,
            annual_rate=self.ANNUAL_PRECESSION
        )
        
        # 8. Sassanian - Ancient Persian system
        self.systems['sassanian'] = AyanamsaSystem(
            name="Sassanian",
            base_date=self.BASE_DATE_1900,
            base_value=21.36,
            annual_rate=self.ANNUAL_PRECESSION
        )
    
    def calculate_ayanamsa(
        self, 
        date: datetime, 
        system: str = 'lahiri'
    ) -> float:
        """
        Calculate ayanamsa for given date and system
        
        Args:
            date: Target date
            system: Ayanamsa system name (default: 'lahiri')
            
        Returns:
            Ayanamsa value in degrees
        """
        system_key = system.lower()
        if system_key not in self.systems:
            raise ValueError(f"Unknown ayanamsa system: {system}")
        
        return self.systems[system_key].calculate(date)
    
    def get_all_systems(self, date: datetime) -> Dict[str, float]:
        """
        Get ayanamsa values for all systems
        
        Args:
            date: Target date
            
        Returns:
            Dictionary with system names and ayanamsa values
        """
        return {
            name: system.calculate(date)
            for name, system in self.systems.items()
        }
    
    def compare_systems(self, date: datetime) -> Dict[str, Dict]:
        """
        Compare all ayanamsa systems for a given date
        
        Args:
            date: Target date
            
        Returns:
            Detailed comparison of all systems
        """
        lahiri_value = self.calculate_ayanamsa(date, 'lahiri')
        
        comparison = {}
        for name, system in self.systems.items():
            value = system.calculate(date)
            comparison[name] = {
                'value_degrees': round(value, 4),
                'value_dms': self._to_dms(value),
                'diff_from_lahiri': round(value - lahiri_value, 4),
                'system_name': system.name
            }
        
        return comparison
    
    def _to_dms(self, degrees: float) -> str:
        """Convert decimal degrees to DMS format"""
        d = int(degrees)
        m = int((degrees - d) * 60)
        s = int(((degrees - d) * 60 - m) * 60)
        return f"{d}°{m}'{s}\""
    
    def tropical_to_sidereal(
        self, 
        tropical_longitude: float, 
        date: datetime,
        system: str = 'lahiri'
    ) -> float:
        """
        Convert tropical longitude to sidereal
        
        Args:
            tropical_longitude: Tropical longitude in degrees
            date: Date of calculation
            system: Ayanamsa system to use
            
        Returns:
            Sidereal longitude in degrees
        """
        ayanamsa = self.calculate_ayanamsa(date, system)
        sidereal = (tropical_longitude - ayanamsa) % 360
        return sidereal
    
    def sidereal_to_tropical(
        self,
        sidereal_longitude: float,
        date: datetime,
        system: str = 'lahiri'
    ) -> float:
        """
        Convert sidereal longitude to tropical
        
        Args:
            sidereal_longitude: Sidereal longitude in degrees
            date: Date of calculation
            system: Ayanamsa system to use
            
        Returns:
            Tropical longitude in degrees
        """
        ayanamsa = self.calculate_ayanamsa(date, system)
        tropical = (sidereal_longitude + ayanamsa) % 360
        return tropical


# Utility functions

def get_ayanamsa_for_date(date: datetime, system: str = 'lahiri') -> float:
    """
    Convenience function to get ayanamsa for a date
    
    Args:
        date: Target date
        system: Ayanamsa system name
        
    Returns:
        Ayanamsa value in degrees
    """
    calc = AyanamsaCalculator()
    return calc.calculate_ayanamsa(date, system)


def compare_all_ayanamsas(date: datetime) -> Dict:
    """
    Convenience function to compare all ayanamsa systems
    
    Args:
        date: Target date
        
    Returns:
        Comparison dictionary
    """
    calc = AyanamsaCalculator()
    return calc.compare_systems(date)
