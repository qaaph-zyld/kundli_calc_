"""
Dasha System Calculations
PGF Protocol: DASHA_001
Gate: GATE_4
Version: 1.0.0
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import math

class VimshottariDasha:
    """Vimshottari Dasha Calculator"""
    
    # Dasha periods in years for each planet
    DASHA_PERIODS = {
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
        "Ketu": 7,
        "Venus": 20
    }
    
    def __init__(self):
        """Initialize calculator"""
        self.initialized = True
    
    def calculate_dasha_at_birth(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> Dict[str, Any]:
        """Calculate Vimshottari dasha at birth
        
        Args:
            birth_time: Birth date and time
            moon_longitude: Moon's longitude at birth
            
        Returns:
            Dictionary with dasha periods
        """
        # Mock calculation for testing
        total_years = sum(self.DASHA_PERIODS.values())
        nakshatra_degrees = moon_longitude % 360
        nakshatra = math.floor(nakshatra_degrees / 13.333333)
        
        # Calculate balance of dasha at birth
        balance = (13.333333 - (nakshatra_degrees % 13.333333)) / 13.333333
        
        # Get planet order starting from birth nakshatra
        planet_order = list(self.DASHA_PERIODS.keys())
        start_index = nakshatra % 9
        planet_order = planet_order[start_index:] + planet_order[:start_index]
        
        current_time = birth_time
        dashas = []
        
        for planet in planet_order:
            period_years = self.DASHA_PERIODS[planet]
            end_time = current_time + timedelta(days=period_years*365.25)
            
            dashas.append({
                "planet": planet,
                "start_date": current_time.isoformat(),
                "end_date": end_time.isoformat(),
                "duration_years": period_years
            })
            
            current_time = end_time
        
        return {
            "birth_nakshatra": nakshatra + 1,
            "balance_at_birth": balance,
            "dasha_sequence": dashas
        }
    
    def calculate_antardasha(
        self,
        main_period: str,
        start_date: datetime
    ) -> List[Dict[str, Any]]:
        """Calculate antardasha (sub-periods)
        
        Args:
            main_period: Main period planet
            start_date: Start date of main period
            
        Returns:
            List of antardasha periods
        """
        main_years = self.DASHA_PERIODS[main_period]
        planet_order = list(self.DASHA_PERIODS.keys())
        start_index = planet_order.index(main_period)
        planet_order = planet_order[start_index:] + planet_order[:start_index]
        
        current_time = start_date
        antardasha = []
        
        for planet in planet_order:
            sub_years = (self.DASHA_PERIODS[planet] * main_years) / 120
            end_time = current_time + timedelta(days=sub_years*365.25)
            
            antardasha.append({
                "planet": planet,
                "start_date": current_time.isoformat(),
                "end_date": end_time.isoformat(),
                "duration_years": sub_years
            })
            
            current_time = end_time
        
        return antardasha
    
    def calculate_pratyantardasha(
        self,
        main_period: str,
        sub_period: str,
        start_date: datetime
    ) -> List[Dict[str, Any]]:
        """Calculate pratyantardasha (sub-sub-periods)
        
        Args:
            main_period: Main period planet
            sub_period: Sub period planet
            start_date: Start date of sub period
            
        Returns:
            List of pratyantardasha periods
        """
        main_years = self.DASHA_PERIODS[main_period]
        sub_years = (self.DASHA_PERIODS[sub_period] * main_years) / 120
        
        planet_order = list(self.DASHA_PERIODS.keys())
        start_index = planet_order.index(sub_period)
        planet_order = planet_order[start_index:] + planet_order[:start_index]
        
        current_time = start_date
        pratyantardasha = []
        
        for planet in planet_order:
            subsub_years = (self.DASHA_PERIODS[planet] * sub_years) / 120
            end_time = current_time + timedelta(days=subsub_years*365.25)
            
            pratyantardasha.append({
                "planet": planet,
                "start_date": current_time.isoformat(),
                "end_date": end_time.isoformat(),
                "duration_years": subsub_years
            })
            
            current_time = end_time
        
        return pratyantardasha
