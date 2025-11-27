"""
Additional Chakra Systems - Phase 6
PGF Protocol: CHAKRA_003
Gate: GATE_6
Version: 1.0.0

Implements:
1. Tripataki Chakra
2. Shoola Chakra
3. Sarvatobhadra Chakra (enhanced)
4. Kalachakra (enhanced)
5. Durga Chakra / Kota Chakra
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import math


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "P.Phalguni", "U.Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "P.Ashadha", "U.Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "P.Bhadrapada", "U.Bhadrapada", "Revati"
]


@dataclass
class ChakraResult:
    """Result from chakra analysis"""
    chakra_name: str
    positions: Dict[str, Any]
    interpretation: str
    favorable: List[str]
    unfavorable: List[str]


# =============================================================================
# TRIPATAKI CHAKRA
# =============================================================================
class TripatakiChakra:
    """
    Tripataki Chakra - Three-Winged Wheel
    
    Used primarily for Muhurta and transit analysis.
    Based on the Moon's nakshatra position.
    """
    
    # Three groups (wings) of 9 nakshatras each
    WINGS = {
        "uttara": [0, 3, 6, 9, 12, 15, 18, 21, 24],   # North wing
        "dakshina": [1, 4, 7, 10, 13, 16, 19, 22, 25], # South wing
        "madhya": [2, 5, 8, 11, 14, 17, 20, 23, 26]    # Middle wing
    }
    
    WING_MEANINGS = {
        "uttara": "Auspicious for starting new ventures, prosperity",
        "dakshina": "Good for completing tasks, endings",
        "madhya": "Neutral, suitable for routine activities"
    }
    
    def calculate(self, moon_nakshatra_idx: int) -> ChakraResult:
        """Calculate Tripataki Chakra position"""
        # Find which wing
        wing = None
        for wing_name, nakshatras in self.WINGS.items():
            if moon_nakshatra_idx in nakshatras:
                wing = wing_name
                break
        
        if wing is None:
            wing = "madhya"
        
        # Determine favorable and unfavorable nakshatras
        favorable_wing = "uttara" if wing != "uttara" else "dakshina"
        unfavorable_wing = "madhya" if wing == "uttara" else "uttara"
        
        return ChakraResult(
            chakra_name="Tripataki Chakra",
            positions={
                "moon_nakshatra": NAKSHATRAS[moon_nakshatra_idx],
                "wing": wing,
                "wing_meaning": self.WING_MEANINGS[wing]
            },
            interpretation=f"Moon in {wing.title()} wing - {self.WING_MEANINGS[wing]}",
            favorable=[NAKSHATRAS[i] for i in self.WINGS[favorable_wing][:3]],
            unfavorable=[NAKSHATRAS[i] for i in self.WINGS[unfavorable_wing][:3]]
        )


# =============================================================================
# SHOOLA CHAKRA
# =============================================================================
class ShoolaChakra:
    """
    Shoola Chakra - Trident Wheel
    
    Used for determining auspicious directions and timing.
    Based on weekday.
    """
    
    # Shoola directions for each weekday
    SHOOLA_DIRECTIONS = {
        0: {"direction": "East", "avoid": "East travel"},      # Sunday
        1: {"direction": "North", "avoid": "North travel"},    # Monday
        2: {"direction": "South", "avoid": "South travel"},    # Tuesday
        3: {"direction": "West", "avoid": "West travel"},      # Wednesday
        4: {"direction": "North-East", "avoid": "NE travel"},  # Thursday
        5: {"direction": "South-East", "avoid": "SE travel"},  # Friday
        6: {"direction": "South-West", "avoid": "SW travel"}   # Saturday
    }
    
    WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    def calculate(self, weekday: int) -> ChakraResult:
        """
        Calculate Shoola Chakra
        
        Args:
            weekday: 0=Sunday, 1=Monday, etc.
        """
        shoola = self.SHOOLA_DIRECTIONS[weekday]
        
        # Safe directions
        all_directions = ["East", "West", "North", "South", "NE", "NW", "SE", "SW"]
        unsafe = shoola["direction"]
        safe = [d for d in all_directions if d != unsafe and unsafe not in d]
        
        return ChakraResult(
            chakra_name="Shoola Chakra",
            positions={
                "weekday": self.WEEKDAYS[weekday],
                "shoola_direction": shoola["direction"],
                "effect": shoola["avoid"]
            },
            interpretation=f"On {self.WEEKDAYS[weekday]}, avoid {shoola['direction']} direction",
            favorable=safe[:4],
            unfavorable=[shoola["direction"]]
        )


# =============================================================================
# SARVATOBHADRA CHAKRA (Enhanced)
# =============================================================================
class SarvatobhadraChakra:
    """
    Sarvatobhadra Chakra - All-Auspicious Wheel
    
    9x9 grid combining nakshatras, vowels, weekdays, and tithis.
    Used for transit analysis and muhurta.
    """
    
    # Center positions in the 9x9 grid
    NAKSHATRA_POSITIONS = {
        "Ashwini": (0, 4), "Bharani": (0, 5), "Krittika": (0, 6),
        "Rohini": (1, 7), "Mrigashira": (2, 8), "Ardra": (3, 8),
        "Punarvasu": (4, 8), "Pushya": (5, 8), "Ashlesha": (6, 8),
        "Magha": (7, 8), "P.Phalguni": (8, 7), "U.Phalguni": (8, 6),
        "Hasta": (8, 5), "Chitra": (8, 4), "Swati": (8, 3),
        "Vishakha": (8, 2), "Anuradha": (8, 1), "Jyeshtha": (8, 0),
        "Mula": (7, 0), "P.Ashadha": (6, 0), "U.Ashadha": (5, 0),
        "Shravana": (4, 0), "Dhanishta": (3, 0), "Shatabhisha": (2, 0),
        "P.Bhadrapada": (1, 0), "U.Bhadrapada": (0, 1), "Revati": (0, 2)
    }
    
    # Vedha (affliction) patterns
    VEDHA_PATTERNS = {
        "front": [(0, 1), (0, -1)],
        "sides": [(1, 0), (-1, 0)],
        "diagonals": [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    }
    
    def calculate(
        self,
        moon_nakshatra: str,
        transit_nakshatra: str = None
    ) -> ChakraResult:
        """
        Calculate Sarvatobhadra Chakra analysis
        
        Args:
            moon_nakshatra: Birth Moon's nakshatra
            transit_nakshatra: Current transit nakshatra (optional)
        """
        moon_pos = self.NAKSHATRA_POSITIONS.get(moon_nakshatra, (4, 4))
        
        # Calculate vedha points
        vedha_nakshatras = self._find_vedha_nakshatras(moon_pos)
        
        # Favorable nakshatras (trines in chakra)
        favorable = self._find_favorable_nakshatras(moon_pos)
        
        # Check transit vedha
        transit_vedha = None
        if transit_nakshatra:
            transit_pos = self.NAKSHATRA_POSITIONS.get(transit_nakshatra)
            if transit_pos and transit_nakshatra in vedha_nakshatras:
                transit_vedha = f"Transit in {transit_nakshatra} causes Vedha"
        
        return ChakraResult(
            chakra_name="Sarvatobhadra Chakra",
            positions={
                "moon_nakshatra": moon_nakshatra,
                "moon_position": moon_pos,
                "vedha_points": vedha_nakshatras,
                "transit_vedha": transit_vedha
            },
            interpretation=f"Moon in {moon_nakshatra} - watch for transits in vedha nakshatras",
            favorable=favorable[:5],
            unfavorable=vedha_nakshatras[:5]
        )
    
    def _find_vedha_nakshatras(self, pos: tuple) -> List[str]:
        """Find nakshatras that cause vedha"""
        vedha = []
        row, col = pos
        
        for pattern_type, offsets in self.VEDHA_PATTERNS.items():
            for dr, dc in offsets:
                new_pos = (row + dr, col + dc)
                # Find nakshatra at this position
                for nak, nak_pos in self.NAKSHATRA_POSITIONS.items():
                    if nak_pos == new_pos:
                        vedha.append(nak)
        
        return vedha
    
    def _find_favorable_nakshatras(self, pos: tuple) -> List[str]:
        """Find favorable nakshatras (trine positions)"""
        favorable = []
        row, col = pos
        
        # Trine-like positions
        trine_offsets = [(3, 0), (-3, 0), (0, 3), (0, -3), (3, 3), (-3, -3)]
        
        for dr, dc in trine_offsets:
            new_pos = ((row + dr) % 9, (col + dc) % 9)
            for nak, nak_pos in self.NAKSHATRA_POSITIONS.items():
                if nak_pos == new_pos:
                    favorable.append(nak)
        
        return favorable


# =============================================================================
# KALACHAKRA (Enhanced)
# =============================================================================
class KalachakraEnhanced:
    """
    Kalachakra - Wheel of Time (Enhanced)
    
    Maps nakshatras to a wheel for timing and transit analysis.
    More detailed than basic kalachakra.
    """
    
    # Kalachakra groups with navamsas
    GROUPS = {
        "savya": {  # Clockwise
            "aries_group": list(range(0, 7)),
            "cancer_group": list(range(7, 14)),
            "libra_group": list(range(14, 21)),
            "capricorn_group": list(range(21, 27))
        },
        "apasavya": {  # Counter-clockwise
            "aries_group": list(range(0, 7)),
            "cancer_group": list(range(7, 14)),
            "libra_group": list(range(14, 21)),
            "capricorn_group": list(range(21, 27))
        }
    }
    
    # Gati (movement) types
    GATI_TYPES = {
        "mandooka": "Frog - jumping movement",
        "simha": "Lion - straight movement",
        "sarpa": "Serpent - winding movement"
    }
    
    def calculate(
        self,
        moon_nakshatra_idx: int,
        birth_sign: int
    ) -> ChakraResult:
        """Calculate enhanced Kalachakra"""
        # Determine savya or apasavya
        is_savya = birth_sign in [0, 1, 2, 3, 8, 9, 10, 11]  # Fire/Earth or Sag-Pisces
        direction = "savya" if is_savya else "apasavya"
        
        # Find nakshatra group
        group = None
        for group_name, nakshatras in self.GROUPS[direction].items():
            if moon_nakshatra_idx in nakshatras:
                group = group_name
                break
        
        # Determine Gati
        pada = moon_nakshatra_idx % 4
        gati = list(self.GATI_TYPES.keys())[pada % 3]
        
        # Calculate progression
        if is_savya:
            progression = [(moon_nakshatra_idx + i) % 27 for i in range(9)]
        else:
            progression = [(moon_nakshatra_idx - i) % 27 for i in range(9)]
        
        return ChakraResult(
            chakra_name="Kalachakra (Enhanced)",
            positions={
                "moon_nakshatra": NAKSHATRAS[moon_nakshatra_idx],
                "direction": direction,
                "group": group,
                "gati": gati,
                "gati_meaning": self.GATI_TYPES[gati],
                "progression": [NAKSHATRAS[i] for i in progression]
            },
            interpretation=f"Kalachakra {direction.title()} direction with {gati.title()} gati",
            favorable=[NAKSHATRAS[progression[i]] for i in [0, 4, 8]],
            unfavorable=[NAKSHATRAS[progression[i]] for i in [2, 5, 7]]
        )


# =============================================================================
# DURGA CHAKRA / KOTA CHAKRA
# =============================================================================
class DurgaChakra:
    """
    Durga Chakra / Kota Chakra - Fort Wheel
    
    Represents the native as a fort with various zones.
    Used for transit analysis.
    """
    
    # Zones of the fort
    ZONES = {
        "stambha": "Central pillar - strongest protection",
        "madhya": "Middle zone - moderate protection",
        "prakara": "Outer wall - first defense",
        "dwara": "Gates - vulnerable points"
    }
    
    # Nakshatra assignments to zones (based on janma nakshatra)
    def _assign_zones(self, janma_nak_idx: int) -> Dict[str, List[int]]:
        """Assign nakshatras to zones based on birth nakshatra"""
        return {
            "stambha": [janma_nak_idx],
            "madhya": [(janma_nak_idx + i) % 27 for i in [1, 26, 9, 18]],
            "prakara": [(janma_nak_idx + i) % 27 for i in [2, 3, 25, 24]],
            "dwara": [(janma_nak_idx + i) % 27 for i in [4, 5, 6, 7, 8]]
        }
    
    def calculate(
        self,
        janma_nakshatra_idx: int,
        transit_nakshatra_idx: int = None
    ) -> ChakraResult:
        """Calculate Durga/Kota Chakra"""
        zones = self._assign_zones(janma_nakshatra_idx)
        
        # Analyze transit if provided
        transit_zone = None
        transit_effect = None
        
        if transit_nakshatra_idx is not None:
            for zone_name, zone_naks in zones.items():
                if transit_nakshatra_idx in zone_naks:
                    transit_zone = zone_name
                    transit_effect = self._get_transit_effect(zone_name)
                    break
        
        return ChakraResult(
            chakra_name="Durga Chakra (Kota)",
            positions={
                "janma_nakshatra": NAKSHATRAS[janma_nakshatra_idx],
                "stambha": NAKSHATRAS[janma_nakshatra_idx],
                "zones": {
                    zone: [NAKSHATRAS[i] for i in naks]
                    for zone, naks in zones.items()
                },
                "transit_zone": transit_zone,
                "transit_effect": transit_effect
            },
            interpretation=f"Fort centered on {NAKSHATRAS[janma_nakshatra_idx]}",
            favorable=[NAKSHATRAS[i] for i in zones["stambha"] + zones["madhya"]],
            unfavorable=[NAKSHATRAS[i] for i in zones["dwara"][:3]]
        )
    
    def _get_transit_effect(self, zone: str) -> str:
        """Get effect of transit in zone"""
        effects = {
            "stambha": "Transit over birth star - major life events",
            "madhya": "Transit in middle zone - moderate effects",
            "prakara": "Transit in outer wall - minor challenges",
            "dwara": "Transit through gates - vulnerability period"
        }
        return effects.get(zone, "Neutral effect")


# =============================================================================
# MASTER CALCULATOR
# =============================================================================
class AdditionalChakraCalculator:
    """Calculate all additional chakras"""
    
    def __init__(self):
        self.tripataki = TripatakiChakra()
        self.shoola = ShoolaChakra()
        self.sarvatobhadra = SarvatobhadraChakra()
        self.kalachakra = KalachakraEnhanced()
        self.durga = DurgaChakra()
    
    def calculate_all(
        self,
        moon_nakshatra_idx: int,
        birth_sign: int,
        weekday: int,
        transit_nakshatra_idx: int = None
    ) -> Dict[str, ChakraResult]:
        """Calculate all additional chakras"""
        moon_nak = NAKSHATRAS[moon_nakshatra_idx]
        transit_nak = NAKSHATRAS[transit_nakshatra_idx] if transit_nakshatra_idx else None
        
        return {
            "tripataki": self.tripataki.calculate(moon_nakshatra_idx),
            "shoola": self.shoola.calculate(weekday),
            "sarvatobhadra": self.sarvatobhadra.calculate(moon_nak, transit_nak),
            "kalachakra": self.kalachakra.calculate(moon_nakshatra_idx, birth_sign),
            "durga": self.durga.calculate(moon_nakshatra_idx, transit_nakshatra_idx)
        }


def calculate_additional_chakras(
    moon_longitude: float,
    weekday: int = 0
) -> Dict[str, Any]:
    """Convenience function for additional chakras"""
    moon_nak_idx = int(moon_longitude / (360/27))
    birth_sign = int(moon_longitude / 30)
    
    calc = AdditionalChakraCalculator()
    results = calc.calculate_all(moon_nak_idx, birth_sign, weekday)
    
    return {
        name: {
            "chakra_name": result.chakra_name,
            "positions": result.positions,
            "interpretation": result.interpretation,
            "favorable": result.favorable,
            "unfavorable": result.unfavorable
        }
        for name, result in results.items()
    }
