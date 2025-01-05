from typing import List, Dict, Any
from app.models.kundli import (
    KundliChart,
    Planet,
    House,
    Prediction,
)

class KundliPredictor:
    ASPECTS = {
        "conjunction": 0,
        "sextile": 60,
        "square": 90,
        "trine": 120,
        "opposition": 180,
    }

    ASPECT_ORBS = {
        "conjunction": 8,
        "sextile": 6,
        "square": 7,
        "trine": 8,
        "opposition": 8,
    }

    PLANET_STRENGTHS = {
        "Sun": {"Leo": 1.0, "Aries": 0.8},
        "Moon": {"Cancer": 1.0, "Taurus": 0.8},
        "Mars": {"Aries": 1.0, "Scorpio": 1.0},
        "Mercury": {"Gemini": 1.0, "Virgo": 1.0},
        "Jupiter": {"Sagittarius": 1.0, "Pisces": 1.0},
        "Venus": {"Libra": 1.0, "Taurus": 1.0},
        "Saturn": {"Capricorn": 1.0, "Aquarius": 1.0},
    }

    def __init__(self):
        self.prediction_rules = self._load_prediction_rules()

    def _load_prediction_rules(self) -> Dict[str, Any]:
        # In a real implementation, this would load from a database or file
        return {
            "planet_in_house": {
                "Sun_1": {
                    "category": "Personality",
                    "description": "Strong leadership qualities and self-expression",
                    "strength": 0.8,
                },
                # Add more rules
            },
            "planet_in_sign": {
                "Jupiter_Sagittarius": {
                    "category": "Fortune",
                    "description": "Excellent period for growth and expansion",
                    "strength": 0.9,
                },
                # Add more rules
            },
            "aspects": {
                "Sun_Jupiter_trine": {
                    "category": "Opportunities",
                    "description": "Favorable time for success and recognition",
                    "strength": 0.85,
                },
                # Add more rules
            },
        }

    def _calculate_aspects(self, planets: List[Planet]) -> List[Dict[str, Any]]:
        aspects = []
        for i, p1 in enumerate(planets):
            for p2 in planets[i + 1:]:
                angle = abs(p1.longitude - p2.longitude) % 360
                if angle > 180:
                    angle = 360 - angle

                for aspect_name, aspect_angle in self.ASPECTS.items():
                    orb = self.ASPECT_ORBS[aspect_name]
                    if abs(angle - aspect_angle) <= orb:
                        aspects.append({
                            "planet1": p1.name,
                            "planet2": p2.name,
                            "aspect": aspect_name,
                            "angle": angle,
                            "orb": abs(angle - aspect_angle),
                        })

        return aspects

    def _calculate_planet_strengths(
        self, planets: List[Planet], houses: List[House]
    ) -> Dict[str, float]:
        strengths = {}
        for planet in planets:
            base_strength = 0.5  # Default strength

            # Add strength based on sign placement
            if planet.name in self.PLANET_STRENGTHS:
                sign_strengths = self.PLANET_STRENGTHS[planet.name]
                if planet.sign in sign_strengths:
                    base_strength += sign_strengths[planet.sign]

            # Modify strength based on retrograde status
            if planet.is_retrograde:
                base_strength *= 0.8

            # Add house placement effects
            house = houses[planet.house - 1]
            if planet.house in [1, 4, 7, 10]:  # Angular houses
                base_strength *= 1.2
            elif planet.house in [2, 5, 8, 11]:  # Succedent houses
                base_strength *= 1.1

            strengths[planet.name] = min(base_strength, 1.0)

        return strengths

    def generate_predictions(self, chart: KundliChart) -> List[Prediction]:
        predictions = []
        
        # Calculate aspects and planet strengths
        aspects = self._calculate_aspects(chart.planets)
        planet_strengths = self._calculate_planet_strengths(
            chart.planets, chart.houses
        )

        # Generate predictions based on planet placements
        for planet in chart.planets:
            # Planet in house predictions
            key = f"{planet.name}_{planet.house}"
            if key in self.prediction_rules["planet_in_house"]:
                rule = self.prediction_rules["planet_in_house"][key]
                predictions.append(
                    Prediction(
                        category=rule["category"],
                        description=rule["description"],
                        strength=rule["strength"] * planet_strengths[planet.name],
                        planets_involved=[planet.name],
                        houses_involved=[planet.house],
                    )
                )

            # Planet in sign predictions
            key = f"{planet.name}_{planet.sign}"
            if key in self.prediction_rules["planet_in_sign"]:
                rule = self.prediction_rules["planet_in_sign"][key]
                predictions.append(
                    Prediction(
                        category=rule["category"],
                        description=rule["description"],
                        strength=rule["strength"] * planet_strengths[planet.name],
                        planets_involved=[planet.name],
                        houses_involved=[planet.house],
                    )
                )

        # Generate predictions based on aspects
        for aspect in aspects:
            key = f"{aspect['planet1']}_{aspect['planet2']}_{aspect['aspect']}"
            if key in self.prediction_rules["aspects"]:
                rule = self.prediction_rules["aspects"][key]
                strength = (
                    rule["strength"] *
                    planet_strengths[aspect["planet1"]] *
                    planet_strengths[aspect["planet2"]]
                )
                predictions.append(
                    Prediction(
                        category=rule["category"],
                        description=rule["description"],
                        strength=strength,
                        planets_involved=[aspect["planet1"], aspect["planet2"]],
                        houses_involved=[],
                    )
                )

        # Sort predictions by strength
        predictions.sort(key=lambda x: x.strength, reverse=True)
        return predictions[:10]  # Return top 10 predictions
