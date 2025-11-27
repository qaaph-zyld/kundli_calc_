"""
Transit Search System
PGF Protocol: TRANSIT_SEARCH_001
Gate: GATE_5
Version: 1.0.0

Search for when planets will be at specific positions:
- Conjunction with natal planets
- Transit to house cusps
- Return transits (planet returns to natal position)
- Specific degree searches
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import math


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


@dataclass
class TransitEvent:
    """A transit event found by search"""
    transit_planet: str
    target: str
    target_type: str  # "planet", "house_cusp", "degree"
    event_type: str   # "conjunction", "opposition", "trine", "square", "return"
    date: datetime
    longitude: float
    orb: float


class TransitSearcher:
    """
    Transit Search Engine
    
    Provides search functionality for finding when transit planets
    reach specific positions relative to natal chart.
    """
    
    # Average daily motion of planets (degrees per day)
    DAILY_MOTION = {
        "Sun": 0.9856,
        "Moon": 13.1764,
        "Mars": 0.5240,
        "Mercury": 1.3833,
        "Jupiter": 0.0831,
        "Venus": 1.2000,
        "Saturn": 0.0335,
        "Rahu": -0.0530,  # Retrograde
        "Ketu": -0.0530
    }
    
    # Aspect definitions (degrees)
    ASPECTS = {
        "conjunction": 0,
        "opposition": 180,
        "trine": 120,
        "square": 90,
        "sextile": 60
    }
    
    def __init__(self):
        pass
    
    def search_conjunction(
        self,
        transit_planet: str,
        target_longitude: float,
        current_transit_lon: float,
        start_date: datetime,
        orb: float = 1.0,
        direction: str = "forward"
    ) -> Optional[TransitEvent]:
        """
        Search for when a transit planet will conjunct a specific degree
        
        Args:
            transit_planet: Planet to track
            target_longitude: Target degree to search for
            current_transit_lon: Current position of transit planet
            start_date: Date to start search from
            orb: Orb of conjunction (degrees)
            direction: "forward" or "backward"
        """
        if transit_planet not in self.DAILY_MOTION:
            return None
        
        daily_motion = self.DAILY_MOTION[transit_planet]
        if direction == "backward":
            daily_motion = -daily_motion
        
        # Handle retrograde planets (Rahu/Ketu already negative)
        if transit_planet in ["Rahu", "Ketu"] and direction == "backward":
            daily_motion = abs(daily_motion)
        
        # Calculate days to target
        diff = (target_longitude - current_transit_lon + 360) % 360
        
        # For retrograde, reverse the difference
        if daily_motion < 0:
            diff = 360 - diff
        
        if diff > 180 and direction == "forward":
            diff = diff - 360
        
        if abs(daily_motion) < 0.001:
            return None
        
        days_to_target = abs(diff / daily_motion)
        
        # Cap search at 5 years
        if days_to_target > 1825:
            return None
        
        event_date = start_date + timedelta(days=days_to_target)
        
        return TransitEvent(
            transit_planet=transit_planet,
            target=f"{target_longitude:.1f}°",
            target_type="degree",
            event_type="conjunction",
            date=event_date,
            longitude=target_longitude,
            orb=orb
        )
    
    def search_aspect(
        self,
        transit_planet: str,
        target_longitude: float,
        current_transit_lon: float,
        aspect_type: str,
        start_date: datetime,
        orb: float = 1.0
    ) -> Optional[TransitEvent]:
        """
        Search for when a transit planet will form a specific aspect
        """
        if aspect_type not in self.ASPECTS:
            return None
        
        aspect_angle = self.ASPECTS[aspect_type]
        target_for_aspect = (target_longitude + aspect_angle) % 360
        
        result = self.search_conjunction(
            transit_planet=transit_planet,
            target_longitude=target_for_aspect,
            current_transit_lon=current_transit_lon,
            start_date=start_date,
            orb=orb
        )
        
        if result:
            result.event_type = aspect_type
            result.target = f"{target_longitude:.1f}° ({aspect_type})"
        
        return result
    
    def search_planetary_return(
        self,
        planet: str,
        natal_longitude: float,
        current_longitude: float,
        start_date: datetime
    ) -> Optional[TransitEvent]:
        """
        Search for planetary return (planet returns to natal position)
        """
        result = self.search_conjunction(
            transit_planet=planet,
            target_longitude=natal_longitude,
            current_transit_lon=current_longitude,
            start_date=start_date
        )
        
        if result:
            result.event_type = "return"
            result.target = f"Natal {planet}"
            result.target_type = "return"
        
        return result
    
    def search_house_ingress(
        self,
        transit_planet: str,
        house_cusp: float,
        current_transit_lon: float,
        start_date: datetime,
        house_number: int
    ) -> Optional[TransitEvent]:
        """
        Search for when a planet enters a specific house
        """
        result = self.search_conjunction(
            transit_planet=transit_planet,
            target_longitude=house_cusp,
            current_transit_lon=current_transit_lon,
            start_date=start_date
        )
        
        if result:
            result.event_type = "house_ingress"
            result.target = f"House {house_number}"
            result.target_type = "house_cusp"
        
        return result
    
    def search_sign_ingress(
        self,
        transit_planet: str,
        target_sign: int,
        current_transit_lon: float,
        start_date: datetime
    ) -> Optional[TransitEvent]:
        """
        Search for when a planet enters a specific sign
        """
        sign_start = target_sign * 30
        
        result = self.search_conjunction(
            transit_planet=transit_planet,
            target_longitude=sign_start,
            current_transit_lon=current_transit_lon,
            start_date=start_date
        )
        
        if result:
            result.event_type = "sign_ingress"
            result.target = SIGNS[target_sign]
            result.target_type = "sign"
        
        return result
    
    def search_all_aspects_to_planet(
        self,
        transit_planet: str,
        natal_planet: str,
        natal_longitude: float,
        current_transit_lon: float,
        start_date: datetime,
        days_ahead: int = 365
    ) -> List[TransitEvent]:
        """
        Search for all major aspects from transit planet to natal planet
        within the specified time range
        """
        events = []
        end_date = start_date + timedelta(days=days_ahead)
        
        for aspect_name in ["conjunction", "opposition", "trine", "square", "sextile"]:
            event = self.search_aspect(
                transit_planet=transit_planet,
                target_longitude=natal_longitude,
                current_transit_lon=current_transit_lon,
                aspect_type=aspect_name,
                start_date=start_date
            )
            
            if event and event.date < end_date:
                event.target = f"Natal {natal_planet}"
                events.append(event)
        
        return sorted(events, key=lambda x: x.date)
    
    def search_major_transits(
        self,
        natal_planets: Dict[str, float],
        transit_planets: Dict[str, float],
        start_date: datetime,
        days_ahead: int = 365
    ) -> Dict[str, Any]:
        """
        Search for all major transits (Jupiter, Saturn, Rahu, Ketu)
        to all natal planets
        """
        major_transit_planets = ["Jupiter", "Saturn", "Rahu", "Ketu"]
        all_events = []
        
        for transit_planet in major_transit_planets:
            if transit_planet not in transit_planets:
                continue
            
            for natal_planet, natal_lon in natal_planets.items():
                events = self.search_all_aspects_to_planet(
                    transit_planet=transit_planet,
                    natal_planet=natal_planet,
                    natal_longitude=natal_lon,
                    current_transit_lon=transit_planets[transit_planet],
                    start_date=start_date,
                    days_ahead=days_ahead
                )
                all_events.extend(events)
        
        # Sort by date
        all_events.sort(key=lambda x: x.date)
        
        # Group by month
        by_month = {}
        for event in all_events:
            month_key = event.date.strftime("%Y-%m")
            if month_key not in by_month:
                by_month[month_key] = []
            by_month[month_key].append({
                "date": event.date.strftime("%Y-%m-%d"),
                "transit_planet": event.transit_planet,
                "aspect": event.event_type,
                "target": event.target
            })
        
        return {
            "total_events": len(all_events),
            "events": [
                {
                    "date": e.date.strftime("%Y-%m-%d"),
                    "transit_planet": e.transit_planet,
                    "aspect": e.event_type,
                    "target": e.target,
                    "longitude": e.longitude
                }
                for e in all_events[:50]  # Limit to 50
            ],
            "by_month": by_month
        }
    
    def search_specific_transit(
        self,
        transit_planet: str,
        transit_current_lon: float,
        target_type: str,  # "planet", "degree", "sign", "house"
        target_value: Any,  # longitude, sign number, or house number
        natal_ascendant: float,
        start_date: datetime
    ) -> Optional[TransitEvent]:
        """
        General-purpose transit search
        """
        if target_type == "degree":
            return self.search_conjunction(
                transit_planet, float(target_value),
                transit_current_lon, start_date
            )
        
        elif target_type == "sign":
            return self.search_sign_ingress(
                transit_planet, int(target_value),
                transit_current_lon, start_date
            )
        
        elif target_type == "house":
            house_num = int(target_value)
            house_cusp = (natal_ascendant + (house_num - 1) * 30) % 360
            return self.search_house_ingress(
                transit_planet, house_cusp,
                transit_current_lon, start_date, house_num
            )
        
        return None


def search_transits(
    natal_planets: Dict[str, float],
    transit_planets: Dict[str, float],
    natal_ascendant: float,
    search_type: str = "major",
    start_date: datetime = None,
    days_ahead: int = 365
) -> Dict[str, Any]:
    """
    Convenience function for transit search
    
    Args:
        search_type: "major" for Jupiter/Saturn/Nodes, "all" for all planets
    """
    if start_date is None:
        start_date = datetime.now()
    
    searcher = TransitSearcher()
    
    if search_type == "major":
        return searcher.search_major_transits(
            natal_planets, transit_planets, start_date, days_ahead
        )
    
    # Full search for all planets
    all_events = []
    for transit_planet, transit_lon in transit_planets.items():
        for natal_planet, natal_lon in natal_planets.items():
            events = searcher.search_all_aspects_to_planet(
                transit_planet, natal_planet, natal_lon,
                transit_lon, start_date, days_ahead
            )
            all_events.extend(events)
    
    all_events.sort(key=lambda x: x.date)
    
    return {
        "total_events": len(all_events),
        "events": [
            {
                "date": e.date.strftime("%Y-%m-%d"),
                "transit_planet": e.transit_planet,
                "aspect": e.event_type,
                "target": e.target
            }
            for e in all_events[:100]
        ]
    }
