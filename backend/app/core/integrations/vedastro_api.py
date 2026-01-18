"""
VedAstro API Integration
PGF Protocol: API_VEDASTRO_001
Gate: GATE_5
Version: 1.0.0

Integration with VedAstro's free REST API for:
- AI-powered interpretations
- Life predictions
- Dasha period analysis
- Transit predictions
- Yoga effects
- Compatibility analysis

API Documentation: https://vedastro.org/api
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

# VedAstro API Base URL
VEDASTRO_API_BASE = "https://vedastro.org/api"


@dataclass
class VedAstroConfig:
    """Configuration for VedAstro API"""

    base_url: str = VEDASTRO_API_BASE
    timeout: int = 30
    retry_attempts: int = 3


class VedAstroClient:
    """
    Client for VedAstro API

    VedAstro provides free API access for Vedic astrology calculations
    and AI-powered interpretations.
    """

    def __init__(self, config: VedAstroConfig = None):
        self.config = config or VedAstroConfig()
        self.client = httpx.AsyncClient(timeout=self.config.timeout)

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    def _format_time(self, dt: datetime) -> str:
        """Format datetime for VedAstro API"""
        # Format: HH:MM/DD/MM/YYYY
        return dt.strftime("%H:%M/%d/%m/%Y")

    def _format_location(self, lat: float, lon: float, name: str = "Location") -> str:
        """Format location for VedAstro API"""
        # Format: LocationName/Timezone/Lat/Lon
        return f"{name}/+05:30/{lat}/{lon}"

    async def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make API request with retry logic"""
        url = f"{self.config.base_url}/{endpoint}"

        for attempt in range(self.config.retry_attempts):
            try:
                response = await self.client.get(url)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"API Error: {response.status_code}")
            except Exception as e:
                print(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.config.retry_attempts - 1:
                    await asyncio.sleep(1)

        return {"error": "API request failed", "status": "error"}

    async def get_planet_predictions(
        self, birth_time: datetime, latitude: float, longitude: float, planet: str
    ) -> Dict[str, Any]:
        """
        Get AI predictions for a planet

        Args:
            birth_time: Birth datetime
            latitude: Birth latitude
            longitude: Birth longitude
            planet: Planet name (Sun, Moon, Mars, etc.)

        Returns:
            Planet prediction data
        """
        time_str = self._format_time(birth_time)
        location = self._format_location(latitude, longitude)

        # VedAstro endpoint format
        endpoint = f"Calculate/PlanetPrediction/{planet}/{time_str}/{location}"

        result = await self._make_request(endpoint)
        return self._process_prediction(result, planet)

    async def get_all_predictions(self, birth_time: datetime, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get predictions for all planets"""
        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

        predictions = {}
        for planet in planets:
            pred = await self.get_planet_predictions(birth_time, latitude, longitude, planet)
            predictions[planet] = pred

        return predictions

    async def get_dasha_prediction(
        self, birth_time: datetime, latitude: float, longitude: float, dasha_planet: str
    ) -> Dict[str, Any]:
        """
        Get prediction for a Dasha period
        """
        time_str = self._format_time(birth_time)
        location = self._format_location(latitude, longitude)

        endpoint = f"Calculate/DashaPrediction/{dasha_planet}/{time_str}/{location}"

        result = await self._make_request(endpoint)
        return result

    async def get_yoga_predictions(self, birth_time: datetime, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get yoga predictions"""
        time_str = self._format_time(birth_time)
        location = self._format_location(latitude, longitude)

        endpoint = f"Calculate/YogaPrediction/{time_str}/{location}"

        result = await self._make_request(endpoint)
        return result

    async def get_house_predictions(
        self, birth_time: datetime, latitude: float, longitude: float, house: int
    ) -> Dict[str, Any]:
        """Get prediction for a specific house"""
        time_str = self._format_time(birth_time)
        location = self._format_location(latitude, longitude)

        endpoint = f"Calculate/HousePrediction/House{house}/{time_str}/{location}"

        result = await self._make_request(endpoint)
        return result

    async def get_life_predictions(self, birth_time: datetime, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Get comprehensive life predictions

        Covers all major life areas:
        - Career
        - Relationships
        - Health
        - Wealth
        - Education
        """
        time_str = self._format_time(birth_time)
        location = self._format_location(latitude, longitude)

        life_areas = ["Career", "Marriage", "Health", "Wealth", "Education", "Family"]

        predictions = {}
        for area in life_areas:
            endpoint = f"Calculate/LifePrediction/{area}/{time_str}/{location}"
            result = await self._make_request(endpoint)
            predictions[area.lower()] = result

        return predictions

    async def get_transit_prediction(
        self, birth_time: datetime, current_time: datetime, latitude: float, longitude: float
    ) -> Dict[str, Any]:
        """Get transit predictions"""
        birth_str = self._format_time(birth_time)
        current_str = self._format_time(current_time)
        location = self._format_location(latitude, longitude)

        endpoint = f"Calculate/TransitPrediction/{birth_str}/{current_str}/{location}"

        result = await self._make_request(endpoint)
        return result

    def _process_prediction(self, result: Dict, planet: str) -> Dict[str, Any]:
        """Process and format prediction result"""
        if "error" in result:
            return {"planet": planet, "status": "error", "message": result.get("error", "Unknown error")}

        return {
            "planet": planet,
            "status": "success",
            "predictions": result.get("Predictions", []),
            "strength": result.get("Strength", "Unknown"),
            "nature": result.get("Nature", "Unknown"),
        }


class LocalPredictionEngine:
    """
    Local prediction engine as fallback when API is unavailable

    Provides basic predictions based on classical texts
    """

    def __init__(self):
        self.predictions = self._load_predictions()

    def _load_predictions(self) -> Dict:
        """Load prediction templates"""
        return {
            "Sun": {
                "strong": [
                    "Leadership abilities shine bright",
                    "Government favor possible",
                    "Father's influence beneficial",
                    "Good vitality and health",
                ],
                "weak": ["May face ego challenges", "Health requires attention", "Father relationship may be strained"],
            },
            "Moon": {
                "strong": [
                    "Emotional intelligence high",
                    "Public popularity indicated",
                    "Mother's blessings strong",
                    "Mental peace prevails",
                ],
                "weak": ["Emotional turbulence possible", "Mind may be restless", "Need for emotional security"],
            },
            "Mars": {
                "strong": [
                    "Courage and determination high",
                    "Property matters favored",
                    "Technical abilities strong",
                    "Athletic prowess",
                ],
                "weak": ["Anger management needed", "Accident prone period", "Conflicts possible"],
            },
            "Mercury": {
                "strong": [
                    "Communication skills excellent",
                    "Business acumen sharp",
                    "Learning abilities enhanced",
                    "Writing and speaking favored",
                ],
                "weak": ["Nervous tension possible", "May overthink situations", "Communication gaps"],
            },
            "Jupiter": {
                "strong": [
                    "Wisdom and knowledge expand",
                    "Spiritual growth indicated",
                    "Children bring happiness",
                    "Teachers and gurus helpful",
                ],
                "weak": ["Overconfidence may harm", "Legal matters need care", "Liver health attention"],
            },
            "Venus": {
                "strong": [
                    "Relationships harmonious",
                    "Artistic talents flourish",
                    "Luxury and comfort available",
                    "Marriage prospects good",
                ],
                "weak": ["Relationship challenges", "Financial indulgence", "Need for balance in pleasures"],
            },
            "Saturn": {
                "strong": [
                    "Discipline brings rewards",
                    "Long-term gains manifest",
                    "Karmic debts clearing",
                    "Structural stability",
                ],
                "weak": ["Delays and obstacles", "Hard work required", "Chronic issues surface"],
            },
            "Rahu": {
                "strong": [
                    "Unconventional success possible",
                    "Foreign opportunities",
                    "Technology benefits",
                    "Material desires fulfilled",
                ],
                "weak": ["Confusion and illusion", "Obsessive tendencies", "Hidden enemies active"],
            },
            "Ketu": {
                "strong": [
                    "Spiritual evolution",
                    "Moksha seeking enhanced",
                    "Past life wisdom emerges",
                    "Detachment brings peace",
                ],
                "weak": ["Sudden losses possible", "Disconnection feelings", "Mysterious health issues"],
            },
        }

    def get_prediction(self, planet: str, strength: str = "strong") -> List[str]:
        """Get predictions for a planet"""
        planet_preds = self.predictions.get(planet, {})
        return planet_preds.get(strength, ["No predictions available"])

    def get_house_prediction(self, house: int, planets_in_house: List[str]) -> Dict[str, Any]:
        """Get prediction based on planets in a house"""
        house_meanings = {
            1: "Self, personality, health, appearance",
            2: "Wealth, speech, family, values",
            3: "Siblings, courage, communication, short travel",
            4: "Home, mother, comfort, vehicles, land",
            5: "Children, creativity, romance, education",
            6: "Enemies, disease, service, daily work",
            7: "Marriage, partnerships, business, public",
            8: "Transformation, occult, longevity, inheritance",
            9: "Fortune, father, religion, long travel, higher learning",
            10: "Career, status, authority, public image",
            11: "Gains, friends, aspirations, elder siblings",
            12: "Losses, expenses, foreign, spirituality, liberation",
        }

        effects = []
        for planet in planets_in_house:
            planet_preds = self.predictions.get(planet, {})
            effects.extend(planet_preds.get("strong", [])[:1])

        return {
            "house": house,
            "significations": house_meanings.get(house, ""),
            "planets": planets_in_house,
            "effects": effects,
        }


async def get_ai_predictions(
    birth_time: datetime, latitude: float, longitude: float, use_api: bool = True
) -> Dict[str, Any]:
    """
    Get AI predictions - tries API first, falls back to local

    Args:
        birth_time: Birth datetime
        latitude: Birth latitude
        longitude: Birth longitude
        use_api: Whether to try API first

    Returns:
        Comprehensive predictions
    """
    if use_api:
        try:
            client = VedAstroClient()
            predictions = await client.get_all_predictions(birth_time, latitude, longitude)
            await client.close()
            return {"source": "vedastro_api", "predictions": predictions}
        except Exception as e:
            print(f"API failed, using local: {e}")

    # Fallback to local predictions
    local = LocalPredictionEngine()
    predictions = {}
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        predictions[planet] = {
            "strong": local.get_prediction(planet, "strong"),
            "weak": local.get_prediction(planet, "weak"),
        }

    return {"source": "local_engine", "predictions": predictions}


def get_sync_predictions(birth_time: datetime, latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Synchronous wrapper for predictions
    """
    return asyncio.run(get_ai_predictions(birth_time, latitude, longitude, use_api=False))
