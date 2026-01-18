"""Shadbala Calculation Module
==========================
Implements the six-fold strength (Shadbala) calculation per BPHS.

The six components are:
1. Sthana Bala (Positional Strength) - 5 sub-components
2. Dig Bala (Directional Strength)
3. Kala Bala (Temporal Strength) - 9 sub-components
4. Chesta Bala (Motional Strength)
5. Naisargika Bala (Natural Strength)
6. Drik Bala (Aspectual Strength)

Reference: Brihat Parashara Hora Shastra, Chapter 27
Units: Shashtiamsas (1/60th of a Rupa)
"""

import math
from datetime import datetime
from typing import Any, Dict, List, Optional

# Minimum required Shadbala in Rupas for each planet (BPHS standard)
MINIMUM_SHADBALA = {
    "Sun": 6.5,
    "Moon": 6.0,
    "Mars": 5.0,
    "Mercury": 7.0,
    "Jupiter": 6.5,
    "Venus": 5.5,
    "Saturn": 5.0,
}

# Natural strength in Shashtiamsas (Naisargika Bala)
NAISARGIKA_BALA = {
    "Sun": 60.0,
    "Moon": 51.43,
    "Mars": 17.14,
    "Mercury": 25.71,
    "Jupiter": 34.29,
    "Venus": 42.86,
    "Saturn": 8.57,
}


class ShadbalaSystem:
    """Shadbala calculation system."""

    def __init__(self):
        """Initialize Shadbala system."""
        self.planet_strengths = {
            "Sun": 60,
            "Moon": 51,
            "Mars": 28,
            "Mercury": 34,
            "Jupiter": 20,
            "Venus": 50,
            "Saturn": 40,
        }

        self.house_strengths = {1: 10, 2: 8, 3: 6, 4: 4, 5: 2, 6: 0, 7: 10, 8: 8, 9: 6, 10: 4, 11: 2, 12: 0}

        self.aspect_strengths = {"conjunction": 1.0, "sextile": 0.5, "square": -0.5, "trine": 0.75, "opposition": -1.0}

    def calculate_sthan_bala(self, house: int) -> float:
        """Calculate positional strength."""
        return self.house_strengths.get(house, 0)

    def calculate_dig_bala(self, planet: str, house: int) -> float:
        """Calculate directional strength."""
        dig_bala_map = {
            "Sun": {10: 1.0, 7: -1.0},
            "Moon": {4: 1.0, 10: -1.0},
            "Mars": {1: 1.0, 7: -1.0},
            "Mercury": {7: 1.0, 1: -1.0},
            "Jupiter": {1: 1.0, 7: -1.0},
            "Venus": {4: 1.0, 10: -1.0},
            "Saturn": {7: 1.0, 1: -1.0},
        }
        return dig_bala_map.get(planet, {}).get(house, 0)

    def calculate_chesta_bala(self, planet: str, speed: float) -> float:
        """Calculate motional strength."""
        # Normalize speed to a value between 0 and 1
        abs_speed = abs(speed)
        max_speed = {
            "Sun": 1.0,
            "Moon": 13.0,
            "Mars": 0.5,
            "Mercury": 1.5,
            "Jupiter": 0.2,
            "Venus": 1.2,
            "Saturn": 0.1,
        }.get(planet, 1.0)

        normalized_speed = min(abs_speed / max_speed, 1.0)
        return normalized_speed * self.planet_strengths[planet]

    def calculate_aspect_bala(self, aspects: List[Dict]) -> float:
        """Calculate aspectual strength (Drik Bala)."""
        total_strength = 0
        for aspect in aspects:
            strength = self.aspect_strengths.get(aspect["type"], 0)
            total_strength += strength
        return total_strength

    def calculate_naisargika_bala(self, planet: str) -> float:
        """Calculate natural strength (Naisargika Bala).

        This is fixed strength based on planet's inherent luminosity.
        Sun is brightest, Saturn is dimmest.
        Returns value in Shashtiamsas.
        """
        return NAISARGIKA_BALA.get(planet.capitalize(), 0.0)

    def calculate_shadbala(
        self, planet: str, house: int, speed: float, aspects: List[Dict], is_day: bool
    ) -> Dict[str, Any]:
        """Calculate total Shadbala strength (all 6 components).

        Args:
            planet: Planet name (Sun, Moon, Mars, etc.)
            house: House number (1-12)
            speed: Planet's daily motion in degrees
            aspects: List of aspects to this planet
            is_day: Whether birth is during daytime

        Returns:
            Dictionary with all 6 Shadbala components and total
        """
        planet_cap = planet.capitalize()

        # 1. Sthana Bala (Positional)
        sthan_bala = self.calculate_sthan_bala(house)

        # 2. Dig Bala (Directional)
        dig_bala = self.calculate_dig_bala(planet_cap, house)

        # 3. Kala Bala (Temporal) - simplified day/night
        kala_bala = 1.0 if is_day else -1.0
        if planet_cap in ["Moon", "Venus", "Saturn"]:
            kala_bala *= -1  # Nocturnal planets stronger at night

        # 4. Chesta Bala (Motional)
        chesta_bala = self.calculate_chesta_bala(planet_cap, speed)

        # 5. Naisargika Bala (Natural) - fixed per planet
        naisargika_bala = self.calculate_naisargika_bala(planet_cap)

        # 6. Drik Bala (Aspectual)
        drik_bala = self.calculate_aspect_bala(aspects)

        # Total in Shashtiamsas
        total_shashtiamsas = (
            sthan_bala * 6  # Scale positional
            + dig_bala * 60  # Scale directional
            + kala_bala * 30  # Scale temporal
            + chesta_bala  # Already scaled
            + naisargika_bala  # Fixed value
            + drik_bala * 30  # Scale aspectual
        )

        # Convert to Rupas (60 Shashtiamsas = 1 Rupa)
        total_rupas = total_shashtiamsas / 60.0

        # Get minimum required for this planet
        min_required = MINIMUM_SHADBALA.get(planet_cap, 5.0)
        is_strong = total_rupas >= min_required

        return {
            "planet": planet_cap,
            "total_shashtiamsas": round(total_shashtiamsas, 2),
            "total_rupas": round(total_rupas, 2),
            "minimum_required": min_required,
            "is_strong": is_strong,
            "percentage": round((total_rupas / min_required) * 100, 1),
            "components": {
                "sthana_bala": round(sthan_bala * 6, 2),
                "dig_bala": round(dig_bala * 60, 2),
                "kala_bala": round(kala_bala * 30, 2),
                "chesta_bala": round(chesta_bala, 2),
                "naisargika_bala": round(naisargika_bala, 2),
                "drik_bala": round(drik_bala * 30, 2),
            },
        }
