"""
Dasha Calculation Module
PGF Protocol: CALC_005
Gate: GATE_3
Version: 1.0.0
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import math

@dataclass
class DashaPeriod:
    """Represents a Dasha period."""
    planet: str
    start_date: datetime
    end_date: datetime
    sub_periods: Optional[List['DashaPeriod']] = None

class VimshottariDasha:
    """Calculator for Vimshottari Dasha system."""
    
    # Dasha periods for each planet in years
    DASHA_YEARS = {
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
    
    # Planet sequence in Vimshottari Dasha
    PLANET_SEQUENCE = [
        "Sun", "Moon", "Mars", "Rahu", "Jupiter",
        "Saturn", "Mercury", "Ketu", "Venus"
    ]
    
    def __init__(self):
        """Initialize Vimshottari Dasha calculator."""
        self.birth_time: Optional[datetime] = None
        self.moon_longitude: Optional[float] = None
        self.dasha_periods: List[DashaPeriod] = []
    
    def set_birth_details(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> None:
        """Set birth details for Dasha calculation."""
        self.birth_time = birth_time
        self.moon_longitude = moon_longitude
    
    def calculate_balance_dasha(self) -> Tuple[str, float]:
        """Calculate balance of birth Dasha."""
        # Calculate Nakshatras
        nakshatra_degree = self.moon_longitude % 13.333333
        consumed_degree = nakshatra_degree / 13.333333
        
        # Get birth Dasha planet
        nakshatra_number = math.floor(self.moon_longitude / 13.333333)
        dasha_lord_index = math.floor(nakshatra_number * 0.111111)
        birth_dasha_planet = self.PLANET_SEQUENCE[dasha_lord_index]
        
        # Calculate balance years
        total_years = self.DASHA_YEARS[birth_dasha_planet]
        balance_years = total_years * (1 - consumed_degree)
        
        return birth_dasha_planet, balance_years
    
    def get_dasha_sequence(
        self,
        start_planet: str
    ) -> List[str]:
        """Get the sequence of planets starting from given planet."""
        start_index = self.PLANET_SEQUENCE.index(start_planet)
        sequence = (
            self.PLANET_SEQUENCE[start_index:] +
            self.PLANET_SEQUENCE[:start_index]
        )
        return sequence
    
    def calculate_main_periods(self) -> List[DashaPeriod]:
        """Calculate main Dasha periods."""
        birth_planet, balance = self.calculate_balance_dasha()
        current_date = self.birth_time
        
        # First period is balance of birth Dasha
        first_period = DashaPeriod(
            planet=birth_planet,
            start_date=current_date,
            end_date=current_date + timedelta(days=balance*365.25)
        )
        self.dasha_periods = [first_period]
        current_date = first_period.end_date
        
        # Calculate remaining periods
        sequence = self.get_dasha_sequence(birth_planet)
        start_index = sequence.index(birth_planet) + 1
        
        for planet in sequence[start_index:] + sequence[:start_index]:
            years = self.DASHA_YEARS[planet]
            end_date = current_date + timedelta(days=years*365.25)
            
            period = DashaPeriod(
                planet=planet,
                start_date=current_date,
                end_date=end_date
            )
            self.dasha_periods.append(period)
            current_date = end_date
        
        return self.dasha_periods
    
    def calculate_sub_periods(
        self,
        main_period: DashaPeriod
    ) -> List[DashaPeriod]:
        """Calculate sub-periods (Bhukti) for a main period."""
        sequence = self.get_dasha_sequence(main_period.planet)
        total_days = (main_period.end_date - main_period.start_date).days
        current_date = main_period.start_date
        sub_periods = []
        
        for planet in sequence:
            planet_years = self.DASHA_YEARS[planet]
            period_days = int(total_days * planet_years / 120)
            end_date = current_date + timedelta(days=period_days)
            
            sub_period = DashaPeriod(
                planet=planet,
                start_date=current_date,
                end_date=end_date
            )
            sub_periods.append(sub_period)
            current_date = end_date
        
        return sub_periods
    
    def calculate_all_sub_periods(self) -> None:
        """Calculate sub-periods for all main periods."""
        for period in self.dasha_periods:
            period.sub_periods = self.calculate_sub_periods(period)
    
    def get_current_dasha(
        self,
        date: datetime = None
    ) -> Dict[str, str]:
        """Get current Dasha period for given date."""
        if date is None:
            date = datetime.now()
        
        # Find main period
        main_period = next(
            (period for period in self.dasha_periods
             if period.start_date <= date <= period.end_date),
            None
        )
        
        if not main_period or not main_period.sub_periods:
            return {}
        
        # Find sub period
        sub_period = next(
            (period for period in main_period.sub_periods
             if period.start_date <= date <= period.end_date),
            None
        )
        
        return {
            "mahadasha": main_period.planet,
            "antardasha": sub_period.planet if sub_period else None,
            "start_date": main_period.start_date.isoformat(),
            "end_date": main_period.end_date.isoformat(),
            "sub_start_date": sub_period.start_date.isoformat() if sub_period else None,
            "sub_end_date": sub_period.end_date.isoformat() if sub_period else None
        }
    
    def get_dasha_predictions(
        self,
        period: DashaPeriod
    ) -> Dict[str, str]:
        """Get predictions for a Dasha period."""
        # Implementation for Dasha predictions
        # This would typically involve analyzing:
        # 1. Planet's natural significations
        # 2. House placement and lordship
        # 3. Aspects and conjunctions
        # 4. Strength of the planet
        # This is a placeholder for actual prediction logic
        return {
            "planet": period.planet,
            "general_influence": "Placeholder for general influence",
            "areas_of_life": ["Placeholder for areas of life"],
            "favorable_periods": ["Placeholder for favorable times"],
            "challenges": ["Placeholder for challenges"],
            "remedies": ["Placeholder for remedies"]
        }
