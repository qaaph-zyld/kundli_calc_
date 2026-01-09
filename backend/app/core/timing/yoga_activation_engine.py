"""
Yoga Activation Window Calculator
==================================

Determines WHEN yogas give results based on:
- Mahadasha periods of involved planets
- Antardasha combinations
- Formation strength multipliers
- House lord activation
- Transit triggers

Answers: "This yoga is in my chart - when does it activate?"
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

from backend.app.core.knowledge.sources.bphs_yogas import get_all_yogas


# Vimshottari Dasha durations (in years)
DASHA_DURATIONS = {
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


@dataclass
class DashaPeriod:
    """Single dasha period"""
    planet: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    duration_years: int = 0
    activation_strength: float = 0.0  # 0-100%


@dataclass
class YogaActivationWindow:
    """Complete yoga activation timing analysis"""
    yoga_name: str
    formation_strength: float  # 0-100
    involved_planets: List[str]
    
    primary_periods: List[DashaPeriod]  # Mahadashas
    peak_activation: List[Dict[str, Any]]  # Specific antardashas
    transit_triggers: List[str]  # Jupiter/Saturn transits
    manifestation_timeline: Dict[str, str]
    
    overall_timing_note: str
    confidence: float


class YogaActivationEngine:
    """
    Engine for calculating yoga activation windows.
    
    Core Logic:
    1. Identify planets involved in yoga formation
    2. Calculate mahadasha periods of those planets
    3. Determine peak antardashas (planet A maha + planet B antara)
    4. Apply formation strength multiplier
    5. Identify transit triggers (Jupiter/Saturn)
    6. Generate manifestation timeline
    """
    
    def __init__(self):
        self.all_yogas = get_all_yogas()
        self.dasha_durations = DASHA_DURATIONS
    
    def calculate_activation_windows(
        self,
        yoga_name: str,
        involved_planets: List[str],
        formation_strength: float,
        chart_data: Optional[Dict[str, Any]] = None
    ) -> YogaActivationWindow:
        """
        Calculate when yoga gives results.
        
        Args:
            yoga_name: Name of the yoga
            involved_planets: Planets forming the yoga
            formation_strength: How well-formed (0-100)
            chart_data: Optional chart data for house analysis
            
        Returns:
            YogaActivationWindow with complete timing analysis
        """
        
        # Get yoga data
        yoga_data = self.all_yogas.get(yoga_name, {})
        
        # Calculate primary periods (mahadashas)
        primary_periods = self._calculate_primary_periods(
            involved_planets, formation_strength
        )
        
        # Calculate peak activation (antardashas)
        peak_activation = self._calculate_peak_antardashas(
            involved_planets, formation_strength
        )
        
        # Identify transit triggers
        transit_triggers = self._identify_transit_triggers(
            yoga_name, involved_planets
        )
        
        # Generate manifestation timeline
        timeline = self._generate_manifestation_timeline(
            primary_periods, formation_strength
        )
        
        # Generate overall timing note
        timing_note = self._generate_timing_note(
            yoga_name, primary_periods, formation_strength
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            len(involved_planets), formation_strength
        )
        
        return YogaActivationWindow(
            yoga_name=yoga_name,
            formation_strength=formation_strength,
            involved_planets=involved_planets,
            primary_periods=primary_periods,
            peak_activation=peak_activation,
            transit_triggers=transit_triggers,
            manifestation_timeline=timeline,
            overall_timing_note=timing_note,
            confidence=confidence
        )
    
    def _calculate_primary_periods(
        self,
        planets: List[str],
        formation_strength: float
    ) -> List[DashaPeriod]:
        """Calculate mahadasha periods for involved planets"""
        
        periods = []
        
        for planet in planets:
            if planet not in self.dasha_durations:
                continue
            
            duration = self.dasha_durations[planet]
            
            # Activation strength = formation strength during that planet's dasha
            # Strong formation (90%) = 90% manifestation during dasha
            activation_strength = formation_strength
            
            periods.append(DashaPeriod(
                planet=planet,
                duration_years=duration,
                activation_strength=activation_strength
            ))
        
        # Sort by activation strength (strongest first)
        periods.sort(key=lambda p: p.activation_strength, reverse=True)
        
        return periods
    
    def _calculate_peak_antardashas(
        self,
        planets: List[str],
        formation_strength: float
    ) -> List[Dict[str, Any]]:
        """Calculate peak antardasha combinations"""
        
        peak_periods = []
        
        # Peak activation when both involved planets are active
        # E.g., Jupiter mahadasha + Moon antardasha for Gaja Kesari Yoga
        
        if len(planets) >= 2:
            for i, maha_planet in enumerate(planets):
                for j, antara_planet in enumerate(planets):
                    if i != j:  # Different planets
                        # Peak strength = formation strength + 10% boost for double activation
                        peak_strength = min(100, formation_strength + 10)
                        
                        peak_periods.append({
                            "mahadasha": maha_planet,
                            "antardasha": antara_planet,
                            "activation_strength": peak_strength,
                            "note": f"Peak manifestation during {maha_planet} maha + {antara_planet} antara"
                        })
        
        # Sort by strength
        peak_periods.sort(key=lambda p: p["activation_strength"], reverse=True)
        
        return peak_periods[:3]  # Top 3 peak periods
    
    def _identify_transit_triggers(
        self,
        yoga_name: str,
        planets: List[str]
    ) -> List[str]:
        """Identify transit triggers for yoga activation"""
        
        triggers = []
        
        # Jupiter transits activate benefic yogas
        if any(p in ["Jupiter", "Venus", "Mercury"] for p in planets):
            triggers.append(
                "Jupiter transit through natal positions of involved planets"
            )
        
        # Saturn transits activate karmic yogas
        if "Saturn" in planets or "Raja" in yoga_name:
            triggers.append(
                "Saturn transit through 10th house or natal Saturn"
            )
        
        # Rahu/Ketu transits for unconventional yogas
        if "Rahu" in planets or "Ketu" in planets:
            triggers.append(
                "Rahu/Ketu transit through involved houses"
            )
        
        # Generic trigger
        if not triggers:
            triggers.append(
                "Jupiter or Saturn transit through houses containing yoga planets"
            )
        
        return triggers
    
    def _generate_manifestation_timeline(
        self,
        periods: List[DashaPeriod],
        formation_strength: float
    ) -> Dict[str, str]:
        """Generate manifestation timeline"""
        
        timeline = {}
        
        if not periods:
            return {"note": "Timing depends on dasha periods of involved planets"}
        
        # Primary manifestation
        primary_planet = periods[0].planet
        timeline["primary_manifestation"] = (
            f"During {primary_planet} mahadasha ({periods[0].duration_years} years) "
            f"- {periods[0].activation_strength:.0f}% strength"
        )
        
        # Secondary manifestation
        if len(periods) > 1:
            secondary_planet = periods[1].planet
            timeline["secondary_manifestation"] = (
                f"During {secondary_planet} mahadasha ({periods[1].duration_years} years) "
                f"- {periods[1].activation_strength:.0f}% strength"
            )
        
        # Strength-based timing note
        if formation_strength >= 85:
            timeline["strength_note"] = "Strong formation - effects manifest clearly"
        elif formation_strength >= 70:
            timeline["strength_note"] = "Good formation - noticeable effects"
        elif formation_strength >= 50:
            timeline["strength_note"] = "Moderate formation - subtle effects"
        else:
            timeline["strength_note"] = "Weak formation - limited manifestation"
        
        return timeline
    
    def _generate_timing_note(
        self,
        yoga_name: str,
        periods: List[DashaPeriod],
        formation_strength: float
    ) -> str:
        """Generate overall timing note"""
        
        if not periods:
            return f"{yoga_name} timing depends on dasha periods of involved planets."
        
        primary = periods[0]
        
        note = (
            f"{yoga_name} (formation strength: {formation_strength:.0f}%) "
            f"manifests primarily during {primary.planet} mahadasha "
            f"({primary.duration_years} years). "
        )
        
        if formation_strength >= 85:
            note += "Strong formation ensures clear manifestation of effects."
        elif formation_strength >= 70:
            note += "Good formation provides noticeable results."
        else:
            note += "Moderate formation gives subtle effects."
        
        if len(periods) > 1:
            secondary = periods[1]
            note += f" Secondary activation during {secondary.planet} mahadasha."
        
        return note
    
    def _calculate_confidence(
        self,
        planet_count: int,
        formation_strength: float
    ) -> float:
        """Calculate confidence in timing prediction"""
        
        base_confidence = 0.80
        
        # More planets = more specific timing
        if planet_count >= 2:
            base_confidence += 0.05
        
        # Stronger formation = more confident prediction
        if formation_strength >= 85:
            base_confidence += 0.10
        elif formation_strength >= 70:
            base_confidence += 0.05
        
        return min(0.98, base_confidence)
    
    def analyze_yoga_timing_batch(
        self,
        active_yogas: List[str],
        chart_data: Dict[str, Any]
    ) -> List[YogaActivationWindow]:
        """Analyze timing for multiple yogas"""
        
        results = []
        
        for yoga_name in active_yogas:
            yoga_data = self.all_yogas.get(yoga_name)
            if not yoga_data:
                continue
            
            # Extract involved planets from yoga formation
            # This is simplified - real implementation would parse formation rules
            involved_planets = self._extract_involved_planets(yoga_name, yoga_data)
            
            # Estimate formation strength (simplified)
            formation_strength = 75.0  # Default moderate strength
            
            result = self.calculate_activation_windows(
                yoga_name=yoga_name,
                involved_planets=involved_planets,
                formation_strength=formation_strength,
                chart_data=chart_data
            )
            
            results.append(result)
        
        return results
    
    def _extract_involved_planets(
        self,
        yoga_name: str,
        yoga_data: Dict[str, Any]
    ) -> List[str]:
        """Extract planets involved in yoga (simplified)"""
        
        # Simplified extraction based on yoga name
        if "Gaja_Kesari" in yoga_name:
            return ["Jupiter", "Moon"]
        elif "Dharma_Karma" in yoga_name:
            return ["Jupiter", "Saturn"]  # Simplified
        elif "Hamsa" in yoga_name:
            return ["Jupiter"]
        elif "Ruchaka" in yoga_name:
            return ["Mars"]
        elif "Bhadra" in yoga_name:
            return ["Mercury"]
        elif "Malavya" in yoga_name:
            return ["Venus"]
        elif "Shasha" in yoga_name:
            return ["Saturn"]
        else:
            # Default: assume 2 planets
            return ["Jupiter", "Venus"]
