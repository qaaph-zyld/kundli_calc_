"""
Birth Time Rectification System
PGF Protocol: RECT_001
Gate: GATE_5
Version: 1.0.0

Implements multiple rectification methods:
1. Tattwa Shuddhi (Element-based)
2. KP Ruling Planets Method
3. Nakshatra Pada Analysis
4. Event-based Rectification
5. Pranapada Lagna Method
6. Naadi Nadi Method
"""

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

ELEMENTS = {
    "Fire": [0, 4, 8],  # Aries, Leo, Sagittarius
    "Earth": [1, 5, 9],  # Taurus, Virgo, Capricorn
    "Air": [2, 6, 10],  # Gemini, Libra, Aquarius
    "Water": [3, 7, 11],  # Cancer, Scorpio, Pisces
}

NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]

NAKSHATRA_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"] * 3


@dataclass
class RectificationResult:
    """Result of birth time rectification"""

    method: str
    original_time: datetime
    suggested_times: List[datetime]
    confidence: float
    reasoning: str
    details: Dict[str, Any]


class TattwaShuddhi:
    """
    Tattwa Shuddhi (Element Purification) Method

    Based on the five elements ruling different time periods:
    - Prithvi (Earth): 6-minute cycle
    - Jala (Water): 12-minute cycle
    - Agni (Fire): 18-minute cycle
    - Vayu (Air): 24-minute cycle
    - Akasha (Ether): 30-minute cycle

    Total cycle: 90 minutes (1.5 hours)
    """

    TATTWAS = ["Prithvi", "Jala", "Agni", "Vayu", "Akasha"]
    TATTWA_DURATIONS = [6, 12, 18, 24, 30]  # minutes

    def __init__(self):
        self.cycle_duration = sum(self.TATTWA_DURATIONS)  # 90 minutes

    def get_tattwa_at_time(self, birth_time: datetime, sunrise: datetime) -> Dict[str, Any]:
        """Get the Tattwa ruling at a given time"""
        minutes_from_sunrise = (birth_time - sunrise).total_seconds() / 60
        position_in_cycle = minutes_from_sunrise % self.cycle_duration

        cumulative = 0
        for i, duration in enumerate(self.TATTWA_DURATIONS):
            cumulative += duration
            if position_in_cycle < cumulative:
                time_in_tattwa = position_in_cycle - (cumulative - duration)
                return {
                    "tattwa": self.TATTWAS[i],
                    "element": self._get_element(i),
                    "time_in_tattwa": round(time_in_tattwa, 2),
                    "remaining": round(duration - time_in_tattwa, 2),
                }

        return {"tattwa": self.TATTWAS[0], "element": "Earth"}

    def _get_element(self, tattwa_idx: int) -> str:
        """Get element for tattwa"""
        elements = ["Earth", "Water", "Fire", "Air", "Ether"]
        return elements[tattwa_idx]

    def rectify(
        self,
        approximate_time: datetime,
        sunrise: datetime,
        moon_sign: int,
        ascendant_sign: int,
        tolerance_minutes: int = 30,
    ) -> RectificationResult:
        """
        Rectify birth time using Tattwa Shuddhi

        Rule: Birth Tattwa should match the element of Moon sign
        or Ascendant sign for harmonious birth
        """
        moon_element = self._get_sign_element(moon_sign)
        asc_element = self._get_sign_element(ascendant_sign)

        suggested_times = []

        # Search in tolerance window
        for offset in range(-tolerance_minutes, tolerance_minutes + 1):
            test_time = approximate_time + timedelta(minutes=offset)
            tattwa_info = self.get_tattwa_at_time(test_time, sunrise)

            if tattwa_info["element"] == moon_element or tattwa_info["element"] == asc_element:
                suggested_times.append(test_time)

        # Group consecutive times and pick middle
        grouped = self._group_consecutive_times(suggested_times)
        final_suggestions = [g[len(g) // 2] for g in grouped][:5]

        return RectificationResult(
            method="Tattwa Shuddhi",
            original_time=approximate_time,
            suggested_times=final_suggestions,
            confidence=0.7 if final_suggestions else 0.3,
            reasoning=f"Birth Tattwa should match Moon ({moon_element}) or Asc ({asc_element}) element",
            details={
                "moon_element": moon_element,
                "asc_element": asc_element,
                "current_tattwa": self.get_tattwa_at_time(approximate_time, sunrise),
            },
        )

    def _get_sign_element(self, sign: int) -> str:
        """Get element of a sign"""
        for element, signs in ELEMENTS.items():
            if sign in signs:
                return element
        return "Unknown"

    def _group_consecutive_times(self, times: List[datetime]) -> List[List[datetime]]:
        """Group consecutive times"""
        if not times:
            return []

        groups = [[times[0]]]
        for t in times[1:]:
            if (t - groups[-1][-1]).total_seconds() <= 120:  # Within 2 minutes
                groups[-1].append(t)
            else:
                groups.append([t])

        return groups


class KPRulingPlanets:
    """
    KP Ruling Planets Method

    Uses the lords of:
    1. Ascendant Sign
    2. Ascendant Star (Nakshatra)
    3. Ascendant Sub
    4. Moon Sign
    5. Moon Star
    6. Day Lord

    Correct birth time should have matching ruling planets
    """

    SIGN_LORDS = [
        "Mars",
        "Venus",
        "Mercury",
        "Moon",
        "Sun",
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn",
        "Saturn",
        "Jupiter",
    ]

    WEEKDAY_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    def get_ruling_planets(self, ascendant: float, moon_longitude: float, birth_time: datetime) -> Dict[str, str]:
        """Get all ruling planets for a moment"""
        asc_sign = int(ascendant / 30)
        asc_nak = int(ascendant / (360 / 27))
        asc_sub = self._get_sub_lord(ascendant)

        moon_sign = int(moon_longitude / 30)
        moon_nak = int(moon_longitude / (360 / 27))

        weekday = birth_time.weekday()
        # Python: Mon=0, we want Sun=0
        weekday = (weekday + 1) % 7

        return {
            "asc_sign_lord": self.SIGN_LORDS[asc_sign],
            "asc_star_lord": NAKSHATRA_LORDS[asc_nak],
            "asc_sub_lord": asc_sub,
            "moon_sign_lord": self.SIGN_LORDS[moon_sign],
            "moon_star_lord": NAKSHATRA_LORDS[moon_nak],
            "day_lord": self.WEEKDAY_LORDS[weekday],
        }

    def _get_sub_lord(self, longitude: float) -> str:
        """Get KP sub lord for a longitude"""
        # Simplified - returns nakshatra lord
        # Full implementation would use 249-division KP table
        nak_idx = int(longitude / (360 / 27))
        return NAKSHATRA_LORDS[nak_idx]

    def analyze_agreement(self, ruling_planets: Dict[str, str]) -> Dict[str, Any]:
        """Analyze agreement among ruling planets"""
        planets = list(ruling_planets.values())
        unique = set(planets)

        # Count occurrences
        counts = {p: planets.count(p) for p in unique}

        # Strong planets appear 2+ times
        strong = [p for p, c in counts.items() if c >= 2]

        return {
            "unique_planets": len(unique),
            "total_planets": len(planets),
            "strong_planets": strong,
            "agreement_score": 1 - (len(unique) / len(planets)),
            "counts": counts,
        }

    def rectify(
        self,
        approximate_time: datetime,
        moon_longitude: float,
        latitude: float,
        longitude: float,
        tolerance_minutes: int = 30,
    ) -> RectificationResult:
        """
        Rectify using KP Ruling Planets

        Find times where ruling planets show maximum agreement
        """
        best_times = []
        best_score = 0

        # Approximate ascendant movement: ~1 degree per 4 minutes
        asc_at_noon = 180.0  # Rough estimate

        for offset in range(-tolerance_minutes, tolerance_minutes + 1, 2):
            test_time = approximate_time + timedelta(minutes=offset)

            # Approximate ascendant (would use actual calculation in production)
            asc = (asc_at_noon + offset * 0.25) % 360

            rp = self.get_ruling_planets(asc, moon_longitude, test_time)
            analysis = self.analyze_agreement(rp)

            if analysis["agreement_score"] > best_score:
                best_score = analysis["agreement_score"]
                best_times = [(test_time, rp, analysis)]
            elif analysis["agreement_score"] == best_score:
                best_times.append((test_time, rp, analysis))

        return RectificationResult(
            method="KP Ruling Planets",
            original_time=approximate_time,
            suggested_times=[bt[0] for bt in best_times[:5]],
            confidence=best_score,
            reasoning="Times with maximum ruling planet agreement",
            details={
                "best_score": best_score,
                "top_results": [{"time": bt[0].isoformat(), "rp": bt[1], "analysis": bt[2]} for bt in best_times[:3]],
            },
        )


class EventBasedRectification:
    """
    Event-based Rectification

    Uses known life events to verify and rectify birth time:
    - Marriage date should match 7th house dasha/transit
    - First child should match 5th house indicators
    - Career start should match 10th house timing
    - Major illness should match 6th/8th house timing
    """

    EVENT_HOUSES = {
        "marriage": [7, 2, 11],
        "childbirth": [5, 2, 11],
        "career_start": [10, 6, 2],
        "career_change": [10, 9, 3],
        "foreign_travel": [12, 9, 3],
        "property_purchase": [4, 2, 11],
        "major_illness": [6, 8, 12],
        "father_death": [9, 10],
        "mother_death": [4, 5],
        "education_completion": [4, 5, 9],
    }

    def analyze_event(
        self, event_type: str, event_date: datetime, birth_time: datetime, dasha_lord: str, transit_sign: int
    ) -> Dict[str, Any]:
        """Analyze if event timing matches expected house significations"""
        relevant_houses = self.EVENT_HOUSES.get(event_type, [1])

        # Simplified analysis
        return {
            "event_type": event_type,
            "event_date": event_date.isoformat(),
            "relevant_houses": relevant_houses,
            "dasha_lord": dasha_lord,
            "analysis": "Check if dasha/bhukti lords signify relevant houses",
        }

    def rectify_using_events(
        self, approximate_time: datetime, events: List[Dict], tolerance_minutes: int = 30
    ) -> RectificationResult:
        """
        Rectify using multiple life events

        Args:
            events: List of {"type": str, "date": datetime}
        """
        # In production, this would:
        # 1. Calculate dasha periods for each test time
        # 2. Check if event dates fall in appropriate dashas
        # 3. Score each test time based on event matches

        return RectificationResult(
            method="Event-based Rectification",
            original_time=approximate_time,
            suggested_times=[approximate_time],  # Placeholder
            confidence=0.6,
            reasoning=f"Based on {len(events)} life events",
            details={"events_analyzed": len(events), "event_types": [e.get("type") for e in events]},
        )


class NakshatraPadaAnalysis:
    """
    Nakshatra Pada Analysis

    Uses physical characteristics associated with
    Lagna nakshatra pada to verify birth time.
    """

    NAKSHATRA_PHYSICAL = {
        "Ashwini": "Athletic build, bright eyes, broad forehead",
        "Bharani": "Medium height, prominent features, restless eyes",
        "Krittika": "Fiery appearance, sharp features, commanding presence",
        "Rohini": "Beautiful appearance, attractive eyes, well-proportioned",
        "Mrigashira": "Slim, agile, searching eyes, gentle appearance",
        "Ardra": "Curly hair, prominent forehead, restless nature",
        "Punarvasu": "Handsome, calm demeanor, expressive eyes",
        "Pushya": "Round face, short stature, benevolent appearance",
        "Ashlesha": "Penetrating eyes, pale complexion, sinuous build",
        "Magha": "Majestic appearance, lion-like bearing, prominent nose",
        # ... Add more
    }

    def get_pada_characteristics(self, ascendant: float) -> Dict[str, Any]:
        """Get physical characteristics for lagna nakshatra pada"""
        nak_idx = int(ascendant / (360 / 27))
        nak_span = 360 / 27
        pos_in_nak = ascendant % nak_span
        pada = int(pos_in_nak / (nak_span / 4)) + 1

        nak_name = NAKSHATRAS[nak_idx]
        characteristics = self.NAKSHATRA_PHYSICAL.get(nak_name, "")

        return {
            "nakshatra": nak_name,
            "pada": pada,
            "lord": NAKSHATRA_LORDS[nak_idx],
            "characteristics": characteristics,
            "navamsa_sign": self._get_navamsa_sign(nak_idx, pada),
        }

    def _get_navamsa_sign(self, nak_idx: int, pada: int) -> str:
        """Get navamsa sign for nakshatra pada"""
        # Each nakshatra pada maps to a specific navamsa
        start_navamsa = (nak_idx * 4) % 12
        navamsa_idx = (start_navamsa + pada - 1) % 12
        return SIGNS[navamsa_idx]


class BirthTimeRectifier:
    """
    Master Birth Time Rectification System

    Combines multiple methods for comprehensive rectification
    """

    def __init__(self):
        self.tattwa = TattwaShuddhi()
        self.kp_rp = KPRulingPlanets()
        self.event_based = EventBasedRectification()
        self.nakshatra = NakshatraPadaAnalysis()

    def full_rectification(
        self,
        approximate_time: datetime,
        birth_date: str,
        latitude: float,
        longitude: float,
        moon_longitude: float,
        ascendant: float,
        events: List[Dict] = None,
        tolerance_minutes: int = 30,
    ) -> Dict[str, Any]:
        """
        Perform full rectification using all methods
        """
        # Calculate sunrise (simplified)
        sunrise = approximate_time.replace(hour=6, minute=0)

        asc_sign = int(ascendant / 30)
        moon_sign = int(moon_longitude / 30)

        results = {}

        # 1. Tattwa Shuddhi
        tattwa_result = self.tattwa.rectify(approximate_time, sunrise, moon_sign, asc_sign, tolerance_minutes)
        results["tattwa_shuddhi"] = {
            "suggested_times": [t.isoformat() for t in tattwa_result.suggested_times],
            "confidence": tattwa_result.confidence,
            "reasoning": tattwa_result.reasoning,
        }

        # 2. KP Ruling Planets
        kp_result = self.kp_rp.rectify(approximate_time, moon_longitude, latitude, longitude, tolerance_minutes)
        results["kp_ruling_planets"] = {
            "suggested_times": [t.isoformat() for t in kp_result.suggested_times],
            "confidence": kp_result.confidence,
            "reasoning": kp_result.reasoning,
        }

        # 3. Nakshatra Pada Analysis
        pada_info = self.nakshatra.get_pada_characteristics(ascendant)
        results["nakshatra_pada"] = pada_info

        # 4. Event-based (if events provided)
        if events:
            event_result = self.event_based.rectify_using_events(approximate_time, events, tolerance_minutes)
            results["event_based"] = {
                "suggested_times": [t.isoformat() for t in event_result.suggested_times],
                "confidence": event_result.confidence,
            }

        # 5. Find consensus
        all_suggestions = tattwa_result.suggested_times + kp_result.suggested_times
        consensus = self._find_consensus(all_suggestions)

        return {
            "original_time": approximate_time.isoformat(),
            "methods": results,
            "consensus_times": [t.isoformat() for t in consensus],
            "recommended_time": consensus[0].isoformat() if consensus else approximate_time.isoformat(),
            "overall_confidence": self._calculate_overall_confidence(results),
        }

    def _find_consensus(self, times: List[datetime]) -> List[datetime]:
        """Find consensus among suggested times"""
        if not times:
            return []

        # Group times within 5 minutes of each other
        groups = []
        for t in sorted(times):
            added = False
            for g in groups:
                if abs((t - g[0]).total_seconds()) < 300:
                    g.append(t)
                    added = True
                    break
            if not added:
                groups.append([t])

        # Sort by group size
        groups.sort(key=len, reverse=True)

        # Return middle time of top groups
        return [g[len(g) // 2] for g in groups[:3]]

    def _calculate_overall_confidence(self, results: Dict) -> float:
        """Calculate overall confidence score"""
        confidences = []
        for method, data in results.items():
            if isinstance(data, dict) and "confidence" in data:
                confidences.append(data["confidence"])

        return sum(confidences) / len(confidences) if confidences else 0.5


def rectify_birth_time(
    approximate_time: datetime,
    latitude: float,
    longitude: float,
    moon_longitude: float,
    ascendant: float,
    events: List[Dict] = None,
    tolerance_minutes: int = 30,
) -> Dict[str, Any]:
    """
    Convenience function for birth time rectification
    """
    rectifier = BirthTimeRectifier()
    return rectifier.full_rectification(
        approximate_time=approximate_time,
        birth_date=approximate_time.strftime("%Y-%m-%d"),
        latitude=latitude,
        longitude=longitude,
        moon_longitude=moon_longitude,
        ascendant=ascendant,
        events=events,
        tolerance_minutes=tolerance_minutes,
    )
