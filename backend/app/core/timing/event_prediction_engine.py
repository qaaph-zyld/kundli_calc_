"""
Event Prediction Framework
===========================

Predicts timing of life events using multi-factor analysis:
1. Natal Promise: Is event indicated in birth chart?
2. Dasha Alignment: When are relevant planets active?
3. Transit Triggers: When do transits activate promise?
4. Confidence Scoring: How likely is this event?

Answers: "When will I get married?", "When will career breakthrough happen?"
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from app.core.knowledge.engine.career_synthesis_engine import CareerSynthesisEngine
from app.core.knowledge.engine.relationship_synthesis_engine import RelationshipSynthesisEngine
from app.core.knowledge.engine.wealth_synthesis_engine import WealthSynthesisEngine


@dataclass
class TimingWindow:
    """Single timing window for event"""

    period: str  # "2026-03 to 2027-08"
    confidence: float  # 0-100
    triggers: List[str]
    likelihood: str  # "very_high", "high", "moderate", "low"
    explanation: str


@dataclass
class EventPrediction:
    """Complete event prediction"""

    event_type: str
    event_possible: bool
    natal_promise_strength: float  # 0-100
    timing_windows: List[TimingWindow]
    factors_analyzed: int
    sources: List[Dict[str, str]]
    confidence: float  # 0-100
    synthesis: str
    recommendations: List[str]


# Event type definitions
EVENT_INDICATORS = {
    "career_breakthrough": {
        "houses": [10, 6, 2],
        "planets": ["Sun", "Saturn", "Mercury"],
        "yogas": ["Raja", "Dharma_Karma", "Amala"],
        "transits": ["Jupiter to 10th", "Saturn stabilizing career houses"],
    },
    "marriage": {
        "houses": [7, 2, 11],
        "planets": ["Venus", "Jupiter"],
        "yogas": ["marriage", "Shubha"],
        "transits": ["Jupiter to 7th or aspecting 7th", "Venus favorable"],
    },
    "wealth_gain": {
        "houses": [2, 11, 5, 9],
        "planets": ["Jupiter", "Venus"],
        "yogas": ["Dhana", "Lakshmi", "Raja"],
        "transits": ["Jupiter to wealth houses"],
    },
    "health_issue": {
        "houses": [1, 6, 8],
        "planets": ["Mars", "Saturn", "Sun"],
        "yogas": ["Arishta"],
        "transits": ["Saturn to 1st/6th/8th", "Mars afflictions"],
    },
    "spiritual_awakening": {
        "houses": [12, 9, 8],
        "planets": ["Jupiter", "Ketu"],
        "yogas": ["Moksha", "Ketu"],
        "transits": ["Jupiter to 12th/9th", "Ketu activation"],
    },
}


class EventPredictionEngine:
    """
    Engine for predicting life event timing.

    Multi-step analysis:
    1. Check natal promise (0-100 strength)
    2. Identify dasha alignment windows
    3. Find transit triggers
    4. Calculate confidence score
    """

    def __init__(self):
        self.career_engine = CareerSynthesisEngine()
        self.relationship_engine = RelationshipSynthesisEngine()
        self.wealth_engine = WealthSynthesisEngine()

    def predict_event(
        self, event_type: str, chart_data: Dict[str, Any], prediction_period: str = "next_5_years"
    ) -> EventPrediction:
        """
        Predict timing of life event.

        Args:
            event_type: Type of event to predict
            chart_data: Complete chart data
            prediction_period: Time period to analyze

        Returns:
            EventPrediction with timing windows and confidence
        """

        # Step 1: Check natal promise
        natal_promise = self._check_natal_promise(event_type, chart_data)

        # Step 2: Identify dasha alignment
        dasha_windows = self._identify_dasha_windows(event_type, chart_data, prediction_period)

        # Step 3: Find transit triggers
        transit_triggers = self._identify_transit_triggers(event_type, chart_data)

        # Step 4: Generate timing windows
        timing_windows = self._generate_timing_windows(natal_promise, dasha_windows, transit_triggers)

        # Step 5: Calculate overall confidence
        confidence = self._calculate_event_confidence(natal_promise, timing_windows)

        # Step 6: Generate synthesis
        synthesis = self._generate_event_synthesis(event_type, natal_promise, timing_windows, confidence)

        # Step 7: Generate recommendations
        recommendations = self._generate_event_recommendations(event_type, natal_promise, timing_windows)

        # Determine if event is possible
        event_possible = natal_promise["strength"] >= 40.0

        return EventPrediction(
            event_type=event_type,
            event_possible=event_possible,
            natal_promise_strength=natal_promise["strength"],
            timing_windows=timing_windows,
            factors_analyzed=natal_promise["factors_analyzed"],
            sources=natal_promise["sources"],
            confidence=confidence,
            synthesis=synthesis,
            recommendations=recommendations,
        )

    def _check_natal_promise(self, event_type: str, chart_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if event is indicated in natal chart"""

        indicators = EVENT_INDICATORS.get(event_type, {})

        score = 0
        factors_analyzed = 0
        sources = []

        # Check relevant houses
        relevant_houses = indicators.get("houses", [])
        for house in relevant_houses:
            planets_in_house = [p for p, data in chart_data.get("planets", {}).items() if data.get("house") == house]
            if planets_in_house:
                score += 15
                factors_analyzed += 1

        # Check relevant planets
        relevant_planets = indicators.get("planets", [])
        for planet in relevant_planets:
            planet_data = chart_data.get("planets", {}).get(planet, {})
            if planet_data:
                dignity = planet_data.get("dignity", "neutral")
                if dignity in ["exalted", "own_sign", "moolatrikona"]:
                    score += 20
                elif dignity in ["friendly", "neutral"]:
                    score += 10
                factors_analyzed += 1

        # Check relevant yogas
        relevant_yoga_keywords = indicators.get("yogas", [])
        active_yogas = chart_data.get("active_yogas", [])
        for yoga in active_yogas:
            if any(keyword in yoga for keyword in relevant_yoga_keywords):
                score += 25
                factors_analyzed += 1
                sources.append({"text": "BPHS", "chapter": "Yogas", "verse": yoga})

        # Normalize to 0-100
        strength = min(100, score)

        return {"strength": strength, "factors_analyzed": factors_analyzed, "sources": sources}

    def _identify_dasha_windows(
        self, event_type: str, chart_data: Dict[str, Any], prediction_period: str
    ) -> List[Dict[str, Any]]:
        """Identify dasha periods favorable for event"""

        indicators = EVENT_INDICATORS.get(event_type, {})
        relevant_planets = indicators.get("planets", [])

        windows = []

        # Simplified: Identify mahadashas of relevant planets
        for planet in relevant_planets:
            if planet in chart_data.get("planets", {}):
                windows.append(
                    {
                        "planet": planet,
                        "period": f"{planet} mahadasha",
                        "strength": 75.0,
                        "note": f"Favorable period for {event_type}",
                    }
                )

        return windows

    def _identify_transit_triggers(self, event_type: str, chart_data: Dict[str, Any]) -> List[str]:
        """Identify transit triggers for event"""

        indicators = EVENT_INDICATORS.get(event_type, {})
        return indicators.get("transits", [])

    def _generate_timing_windows(
        self, natal_promise: Dict[str, Any], dasha_windows: List[Dict[str, Any]], transit_triggers: List[str]
    ) -> List[TimingWindow]:
        """Generate specific timing windows"""

        windows = []

        if natal_promise["strength"] < 40:
            # Low natal promise - no strong windows
            return windows

        # Generate windows from dasha periods
        for i, dasha in enumerate(dasha_windows[:3]):  # Top 3 dashas
            # Calculate confidence based on natal promise + dasha strength
            confidence = (natal_promise["strength"] + dasha["strength"]) / 2

            # Determine likelihood
            if confidence >= 80:
                likelihood = "very_high"
            elif confidence >= 65:
                likelihood = "high"
            elif confidence >= 50:
                likelihood = "moderate"
            else:
                likelihood = "low"

            # Generate period string (simplified)
            current_year = datetime.now().year
            start_year = current_year + i
            end_year = start_year + 2

            windows.append(
                TimingWindow(
                    period=f"{start_year} to {end_year}",
                    confidence=confidence,
                    triggers=[dasha["period"]] + transit_triggers[:1],
                    likelihood=likelihood,
                    explanation=f"{dasha['note']} during {dasha['period']}",
                )
            )

        # Sort by confidence
        windows.sort(key=lambda w: w.confidence, reverse=True)

        return windows[:3]  # Top 3 windows

    def _calculate_event_confidence(self, natal_promise: Dict[str, Any], timing_windows: List[TimingWindow]) -> float:
        """Calculate overall confidence in prediction"""

        base_confidence = natal_promise["strength"] * 0.6  # 60% weight to natal

        if timing_windows:
            window_confidence = max(w.confidence for w in timing_windows) * 0.4  # 40% to timing
            total_confidence = base_confidence + window_confidence
        else:
            total_confidence = base_confidence * 0.5  # Reduce if no timing windows

        return min(100, total_confidence)

    def _generate_event_synthesis(
        self, event_type: str, natal_promise: Dict[str, Any], timing_windows: List[TimingWindow], confidence: float
    ) -> str:
        """Generate synthesis of event prediction"""

        parts = []

        # Natal promise assessment
        if natal_promise["strength"] >= 70:
            parts.append(
                f"Strong natal promise for {event_type.replace('_', ' ')} "
                f"({natal_promise['strength']:.0f}% strength). "
            )
        elif natal_promise["strength"] >= 40:
            parts.append(
                f"Moderate natal indication for {event_type.replace('_', ' ')} "
                f"({natal_promise['strength']:.0f}% strength). "
            )
        else:
            parts.append(
                f"Weak natal indication for {event_type.replace('_', ' ')} "
                f"({natal_promise['strength']:.0f}% strength). "
            )

        # Timing windows
        if timing_windows:
            parts.append(f"\n\nPredicted Timing Windows ({len(timing_windows)} identified):")
            for window in timing_windows:
                parts.append(
                    f"\n• {window.period} - {window.likelihood.replace('_', ' ').title()} likelihood "
                    f"({window.confidence:.0f}% confidence): {window.explanation}"
                )
        else:
            parts.append("\n\nNo strong timing windows identified in prediction period.")

        # Overall confidence
        parts.append(f"\n\nOverall Prediction Confidence: {confidence:.0f}%")

        return "".join(parts)

    def _generate_event_recommendations(
        self, event_type: str, natal_promise: Dict[str, Any], timing_windows: List[TimingWindow]
    ) -> List[str]:
        """Generate recommendations based on prediction"""

        recommendations = []

        if natal_promise["strength"] >= 70 and timing_windows:
            recommendations.append(
                f"Strong indication for {event_type.replace('_', ' ')} - " f"focus efforts during predicted windows"
            )
            recommendations.append(f"Optimal timing: {timing_windows[0].period}")
        elif natal_promise["strength"] >= 40:
            recommendations.append(f"Moderate indication - success possible with effort and timing")
            if timing_windows:
                recommendations.append(f"Best window: {timing_windows[0].period}")
        else:
            recommendations.append(f"Weak natal indication - event may not manifest strongly")
            recommendations.append("Consider alternative paths or remedial measures")

        return recommendations[:5]

    # Specialized prediction methods

    def predict_career_breakthrough(self, chart_data: Dict[str, Any]) -> EventPrediction:
        """Predict career breakthrough timing"""
        return self.predict_event("career_breakthrough", chart_data)

    def predict_marriage(self, chart_data: Dict[str, Any]) -> EventPrediction:
        """Predict marriage timing"""
        return self.predict_event("marriage", chart_data)

    def predict_wealth_gain(self, chart_data: Dict[str, Any]) -> EventPrediction:
        """Predict wealth gain timing"""
        return self.predict_event("wealth_gain", chart_data)

    def predict_health_issue(self, chart_data: Dict[str, Any]) -> EventPrediction:
        """Predict potential health issues timing"""
        return self.predict_event("health_issue", chart_data)

    def predict_spiritual_awakening(self, chart_data: Dict[str, Any]) -> EventPrediction:
        """Predict spiritual awakening timing"""
        return self.predict_event("spiritual_awakening", chart_data)
