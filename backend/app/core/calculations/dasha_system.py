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
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
    }
    LORD_SEQUENCE = [
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
    ]
    
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
        # Determine nakshatra (each is 13°20' = 13.333333... degrees)
        nak_len = 13.333333333333334
        lon = moon_longitude % 360.0
        nak_index = int(lon // nak_len)  # 0..26, 0 = Ashwini
        pos_in_nak = lon - (nak_index * nak_len)
        # Remaining fraction of current nakshatra
        remaining_fraction = (nak_len - pos_in_nak) / nak_len
        
        # Starting mahadasha lord for the birth nakshatra
        start_lord = self.LORD_SEQUENCE[nak_index % 9]
        
        # Build full lord order starting from start_lord
        idx = self.LORD_SEQUENCE.index(start_lord)
        order = self.LORD_SEQUENCE[idx:] + self.LORD_SEQUENCE[:idx]
        
        dashas: List[Dict[str, Any]] = []
        current = birth_time
        # First dasha has only the balance portion
        first_years_full = self.DASHA_PERIODS[start_lord]
        first_years_remaining = first_years_full * remaining_fraction
        first_end = current + timedelta(days=first_years_remaining * 365.25)
        dashas.append({
            "planet": start_lord,
            "start_date": current,
            "end_date": first_end,
            "duration_years": first_years_remaining,
        })
        current = first_end
        
        # Remaining mahadashas in order
        for lord in order[1:]:
            yrs = self.DASHA_PERIODS[lord]
            end = current + timedelta(days=yrs * 365.25)
            dashas.append({
                "planet": lord,
                "start_date": current,
                "end_date": end,
                "duration_years": yrs,
            })
            current = end
        
        return {
            "birth_nakshatra": nak_index + 1,
            "balance_at_birth": remaining_fraction,
            "dasha_sequence": dashas,
        }
    
    def calculate_antardasha(
        self,
        main_period: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Calculate antardasha (sub-periods)
        
        Args:
            main_period: Main period planet
            start_date: Start date of main period
            end_date: End date of main period
            
        Returns:
            List of antardasha periods
        """
        main_years = self.DASHA_PERIODS[main_period]
        # Order starts from main_period's own lord in LORD_SEQUENCE order
        start_index = self.LORD_SEQUENCE.index(main_period)
        planet_order = self.LORD_SEQUENCE[start_index:] + self.LORD_SEQUENCE[:start_index]
        total_days = (end_date - start_date).total_seconds() / 86400.0
        current_time = start_date
        antardasha = []
        
        for planet in planet_order:
            sub_years = (self.DASHA_PERIODS[planet] * main_years) / 120
            # Scale to exact main period duration to avoid drift
            sub_days = total_days * (sub_years / main_years)
            end_time = current_time + timedelta(days=sub_days)
            
            antardasha.append({
                "planet": planet,
                "start_date": current_time,
                "end_date": end_time,
                "duration_years": sub_years
            })
            
            current_time = end_time
        
        return antardasha
    
    def calculate_pratyantardasha(
        self,
        main_period: str,
        sub_period: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Calculate pratyantardasha (sub-sub-periods)
        
        Args:
            main_period: Main period planet
            sub_period: Sub period planet
            start_date: Start date of sub period
            end_date: End date of sub period
            
        Returns:
            List of pratyantardasha periods
        """
        main_years = self.DASHA_PERIODS[main_period]
        sub_years = (self.DASHA_PERIODS[sub_period] * main_years) / 120
        start_index = self.LORD_SEQUENCE.index(sub_period)
        planet_order = self.LORD_SEQUENCE[start_index:] + self.LORD_SEQUENCE[:start_index]
        total_days = (end_date - start_date).total_seconds() / 86400.0
        current_time = start_date
        pratyantardasha = []
        
        for planet in planet_order:
            subsub_years = (self.DASHA_PERIODS[planet] * sub_years) / 120
            subsub_days = total_days * (subsub_years / sub_years)
            end_time = current_time + timedelta(days=subsub_days)
            
            pratyantardasha.append({
                "planet": planet,
                "start_date": current_time,
                "end_date": end_time,
                "duration_years": subsub_years
            })
            
            current_time = end_time
        
        return pratyantardasha

    def calculate_all_dasha_levels(
        self,
        birth_time: datetime,
        moon_longitude: float
    ) -> Dict[str, Any]:
        """Calculate Mahadasha with nested Antardasha and Pratyantardasha from birth."""
        birth_info = self.calculate_dasha_at_birth(birth_time, moon_longitude)
        periods: List[Dict[str, Any]] = []
        for maha in birth_info["dasha_sequence"]:
            m_start: datetime = maha["start_date"]
            m_end: datetime = maha["end_date"]
            m_planet: str = maha["planet"]
            # Antardasha within mahadasha
            antas = self.calculate_antardasha(m_planet, m_start, m_end)
            # For each antardasha, compute pratyantardasha
            for a in antas:
                a_start: datetime = a["start_date"]
                a_end: datetime = a["end_date"]
                a_planet: str = a["planet"]
                a["pratyantardasha"] = self.calculate_pratyantardasha(
                    m_planet, a_planet, a_start, a_end
                )
            periods.append({
                "planet": m_planet,
                "start_date": m_start.isoformat(),
                "end_date": m_end.isoformat(),
                "duration_years": maha["duration_years"],
                "antardasha": [
                    {
                        **{k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in a.items() if k in {"planet", "start_date", "end_date", "duration_years"}},
                        "pratyantardasha": [
                            {
                                **{kk: (vv.isoformat() if isinstance(vv, datetime) else vv) for kk, vv in p.items()}
                            }
                            for p in a["pratyantardasha"]
                        ],
                    }
                    for a in antas
                ],
            })
        return {"periods": periods}
