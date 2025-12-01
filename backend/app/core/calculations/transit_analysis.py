"""
Transit (Gochara) Analysis System
PGF Protocol: TRANSIT_001
Gate: GATE_5
Version: 1.0.0

This module implements comprehensive transit analysis including:
- Current planetary transits
- Transit from natal Moon (Gochara)
- Ashtakavarga transit scoring
- Vedha (obstruction) analysis
- Transit predictions and timing
- Sade Sati calculation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from enum import Enum
import math

# Sign names
SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Benefic and malefic planets
BENEFIC_PLANETS = ["Jupiter", "Venus", "Mercury", "Moon"]
MALEFIC_PLANETS = ["Saturn", "Mars", "Rahu", "Ketu", "Sun"]


class TransitResult(Enum):
    """Result classification for transits"""
    EXCELLENT = "excellent"
    GOOD = "good"
    NEUTRAL = "neutral"
    CHALLENGING = "challenging"
    DIFFICULT = "difficult"


@dataclass
class TransitPosition:
    """Current transit position of a planet"""
    planet: str
    longitude: float
    sign: int
    sign_name: str
    nakshatra: int
    nakshatra_name: str
    is_retrograde: bool
    speed: float


@dataclass
class GocharaResult:
    """Transit result from natal Moon"""
    planet: str
    transit_house: int  # House from Moon
    is_benefic: bool
    has_vedha: bool
    vedha_planet: Optional[str]
    ashtakavarga_score: int
    interpretation: str
    effects: List[str]
    overall_result: TransitResult


@dataclass
class SadeSatiStatus:
    """Sade Sati (7.5 years Saturn transit) status"""
    is_active: bool
    phase: Optional[str]  # "rising", "peak", "setting"
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    intensity: str  # "light", "medium", "heavy"
    affected_houses: List[int]
    remedies: List[str]


# Gochara (transit) benefic houses from Moon
# Based on classical texts (Brihat Parashara Hora Shastra)
GOCHARA_BENEFIC_HOUSES = {
    "Sun": [3, 6, 10, 11],
    "Moon": [1, 3, 6, 7, 10, 11],
    "Mars": [3, 6, 11],
    "Mercury": [2, 4, 6, 8, 10, 11],
    "Jupiter": [2, 5, 7, 9, 11],
    "Venus": [1, 2, 3, 4, 5, 8, 9, 11, 12],
    "Saturn": [3, 6, 11],
    "Rahu": [3, 6, 10, 11],
    "Ketu": [3, 6, 10, 11]
}

# Vedha points - houses that obstruct the good effects
# Format: {planet: {benefic_house: vedha_house}}
VEDHA_POINTS = {
    "Sun": {3: 9, 6: 12, 10: 4, 11: 5},
    "Moon": {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8},
    "Mars": {3: 12, 6: 9, 11: 5},
    "Mercury": {2: 5, 4: 3, 6: 9, 8: 1, 10: 8, 11: 12},
    "Jupiter": {2: 12, 5: 4, 7: 3, 9: 10, 11: 8},
    "Venus": {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 5, 9: 11, 11: 6, 12: 3},
    "Saturn": {3: 12, 6: 9, 11: 5}
}

# Ashtakavarga benefic points for transit scoring
# Simplified table - real calculation is more complex
ASHTAKAVARGA_BASE = {
    "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
    "Moon": [3, 6, 7, 8, 10, 11],
    "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
    "Mercury": [1, 3, 5, 6, 7, 8, 9, 10, 11],
    "Jupiter": [1, 2, 3, 4, 7, 8, 9, 10, 11],
    "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
    "Saturn": [3, 5, 6, 8, 9, 10, 11]
}

# Nakshatra data
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]


class TransitAnalyzer:
    """
    Comprehensive Transit Analysis Engine
    """
    
    def __init__(self, natal_moon_sign: int, natal_planets: Dict[str, float]):
        """
        Initialize transit analyzer with natal chart data
        
        Args:
            natal_moon_sign: Moon's sign in natal chart (0-11)
            natal_planets: Dictionary of natal planet longitudes
        """
        self.natal_moon_sign = natal_moon_sign
        self.natal_planets = natal_planets
        self.natal_moon_house = 1  # Moon is always in 1st from itself
    
    def analyze_transit(
        self,
        transit_positions: Dict[str, float],
        current_time: datetime
    ) -> Dict[str, Any]:
        """
        Complete transit analysis
        
        Args:
            transit_positions: Current planetary positions
            current_time: Current datetime
            
        Returns:
            Complete transit analysis data
        """
        # Get transit positions with details
        positions = self._get_transit_positions(transit_positions)
        
        # Gochara analysis for each planet
        gochara_results = []
        for planet, lon in transit_positions.items():
            if planet in ["Uranus", "Neptune", "Pluto"]:
                continue  # Skip outer planets for Vedic analysis
            gochara = self._analyze_gochara(planet, lon, transit_positions)
            gochara_results.append(gochara)
        
        # Sade Sati check
        saturn_lon = transit_positions.get("Saturn", 0)
        sade_sati = self._check_sade_sati(saturn_lon)
        
        # Calculate overall transit score
        overall_score = self._calculate_overall_score(gochara_results)
        
        # Generate predictions
        predictions = self._generate_predictions(gochara_results, sade_sati)
        
        # Important transits (slow planets in significant positions)
        important_transits = self._identify_important_transits(positions)
        
        return {
            "timestamp": current_time.isoformat(),
            "transit_positions": [
                {
                    "planet": p.planet,
                    "longitude": p.longitude,
                    "sign": p.sign_name,
                    "nakshatra": p.nakshatra_name,
                    "retrograde": p.is_retrograde
                }
                for p in positions
            ],
            "gochara_results": [
                {
                    "planet": g.planet,
                    "house_from_moon": g.transit_house,
                    "is_benefic": g.is_benefic,
                    "has_vedha": g.has_vedha,
                    "vedha_by": g.vedha_planet,
                    "ashtakavarga_score": g.ashtakavarga_score,
                    "result": g.overall_result.value,
                    "interpretation": g.interpretation,
                    "effects": g.effects
                }
                for g in gochara_results
            ],
            "sade_sati": {
                "is_active": sade_sati.is_active,
                "phase": sade_sati.phase,
                "intensity": sade_sati.intensity,
                "affected_houses": sade_sati.affected_houses,
                "remedies": sade_sati.remedies
            },
            "overall_score": overall_score,
            "predictions": predictions,
            "important_transits": important_transits
        }
    
    def _get_transit_positions(self, positions: Dict[str, float]) -> List[TransitPosition]:
        """Convert longitude dict to detailed transit positions"""
        result = []
        for planet, lon in positions.items():
            sign = int(lon / 30)
            nakshatra = int(lon / (360 / 27))
            
            result.append(TransitPosition(
                planet=planet,
                longitude=lon,
                sign=sign,
                sign_name=SIGN_NAMES[sign],
                nakshatra=nakshatra,
                nakshatra_name=NAKSHATRAS[nakshatra],
                is_retrograde=positions.get(f"{planet}_retrograde", False),
                speed=positions.get(f"{planet}_speed", 0)
            ))
        
        return result
    
    def _analyze_gochara(
        self,
        planet: str,
        longitude: float,
        all_transits: Dict[str, float]
    ) -> GocharaResult:
        """
        Analyze transit of a planet from natal Moon
        
        Args:
            planet: Planet name
            longitude: Current transit longitude
            all_transits: All current transit positions
            
        Returns:
            GocharaResult with complete analysis
        """
        # Calculate house from natal Moon
        transit_sign = int(longitude / 30)
        house_from_moon = ((transit_sign - self.natal_moon_sign) % 12) + 1
        
        # Check if benefic position
        benefic_houses = GOCHARA_BENEFIC_HOUSES.get(planet, [])
        is_benefic = house_from_moon in benefic_houses
        
        # Check for Vedha
        has_vedha = False
        vedha_planet = None
        
        if is_benefic and planet in VEDHA_POINTS:
            vedha_house = VEDHA_POINTS[planet].get(house_from_moon)
            if vedha_house:
                # Check if any planet is in vedha position
                for other_planet, other_lon in all_transits.items():
                    if other_planet != planet:
                        other_sign = int(other_lon / 30)
                        other_house = ((other_sign - self.natal_moon_sign) % 12) + 1
                        if other_house == vedha_house:
                            has_vedha = True
                            vedha_planet = other_planet
                            break
        
        # Calculate Ashtakavarga score (simplified)
        ashtakavarga_score = self._calculate_transit_ashtakavarga(planet, transit_sign)
        
        # Determine overall result
        if is_benefic and not has_vedha and ashtakavarga_score >= 4:
            result = TransitResult.EXCELLENT
        elif is_benefic and not has_vedha:
            result = TransitResult.GOOD
        elif is_benefic and has_vedha:
            result = TransitResult.NEUTRAL
        elif not is_benefic and ashtakavarga_score >= 4:
            result = TransitResult.NEUTRAL
        elif not is_benefic and ashtakavarga_score >= 2:
            result = TransitResult.CHALLENGING
        else:
            result = TransitResult.DIFFICULT
        
        # Generate interpretation
        interpretation = self._generate_interpretation(
            planet, house_from_moon, is_benefic, has_vedha, vedha_planet
        )
        
        # Generate effects
        effects = self._get_transit_effects(planet, house_from_moon, is_benefic)
        
        return GocharaResult(
            planet=planet,
            transit_house=house_from_moon,
            is_benefic=is_benefic,
            has_vedha=has_vedha,
            vedha_planet=vedha_planet,
            ashtakavarga_score=ashtakavarga_score,
            interpretation=interpretation,
            effects=effects,
            overall_result=result
        )
    
    def _calculate_transit_ashtakavarga(self, planet: str, transit_sign: int) -> int:
        """
        Calculate simplified Ashtakavarga score for transit
        Returns score 0-8 (number of benefic points)
        """
        if planet not in ASHTAKAVARGA_BASE:
            return 4  # Default middle score
        
        # House from natal planet position
        natal_lon = self.natal_planets.get(planet, 0)
        natal_sign = int(natal_lon / 30)
        house_from_natal = ((transit_sign - natal_sign) % 12) + 1
        
        # Check if this house position gives benefic points
        benefic_houses = ASHTAKAVARGA_BASE[planet]
        score = 0
        
        # Simplified: check position from each planet
        for check_planet, check_lon in self.natal_planets.items():
            if check_planet in ["Rahu", "Ketu"]:
                continue
            check_sign = int(check_lon / 30)
            house_from_check = ((transit_sign - check_sign) % 12) + 1
            if house_from_check in benefic_houses:
                score += 1
        
        return min(8, score)  # Cap at 8
    
    def _check_sade_sati(self, saturn_longitude: float) -> SadeSatiStatus:
        """
        Check Sade Sati status (7.5 year Saturn transit)
        
        Sade Sati occurs when Saturn transits:
        - 12th from Moon (rising phase)
        - 1st from Moon (peak phase)
        - 2nd from Moon (setting phase)
        """
        saturn_sign = int(saturn_longitude / 30)
        
        # Calculate positions relative to Moon
        house_from_moon = ((saturn_sign - self.natal_moon_sign) % 12) + 1
        
        is_active = house_from_moon in [12, 1, 2]
        
        if not is_active:
            return SadeSatiStatus(
                is_active=False,
                phase=None,
                start_date=None,
                end_date=None,
                intensity="none",
                affected_houses=[],
                remedies=[]
            )
        
        # Determine phase
        if house_from_moon == 12:
            phase = "rising"
            intensity = "light"
            affected = [12, 1]
        elif house_from_moon == 1:
            phase = "peak"
            intensity = "heavy"
            affected = [1, 2, 12]
        else:  # house 2
            phase = "setting"
            intensity = "medium"
            affected = [2, 3]
        
        remedies = [
            "Worship Lord Hanuman",
            "Recite Saturn mantras (Shani Stotram)",
            "Donate black items on Saturdays",
            "Wear blue sapphire (after consultation)",
            "Feed crows",
            "Help the elderly and disabled"
        ]
        
        return SadeSatiStatus(
            is_active=True,
            phase=phase,
            start_date=None,  # Would need ephemeris for exact dates
            end_date=None,
            intensity=intensity,
            affected_houses=affected,
            remedies=remedies
        )
    
    def _generate_interpretation(
        self,
        planet: str,
        house: int,
        is_benefic: bool,
        has_vedha: bool,
        vedha_planet: Optional[str]
    ) -> str:
        """Generate human-readable interpretation"""
        house_meanings = {
            1: "personality, health, new beginnings",
            2: "finances, family, speech",
            3: "courage, siblings, short journeys",
            4: "home, mother, mental peace",
            5: "children, creativity, romance",
            6: "enemies, health issues, debts",
            7: "partnerships, marriage, business",
            8: "transformation, obstacles, occult",
            9: "luck, father, long journeys",
            10: "career, status, authority",
            11: "gains, friends, aspirations",
            12: "losses, spirituality, foreign lands"
        }
        
        base = f"{planet} transiting {house}th house from Moon "
        base += f"(affecting {house_meanings[house]}). "
        
        if is_benefic:
            base += "This is generally a favorable transit. "
            if has_vedha:
                base += f"However, {vedha_planet} creates vedha (obstruction), "
                base += "reducing the positive effects. "
        else:
            base += "This transit may bring challenges. "
            base += "Extra caution and patience advised. "
        
        return base
    
    def _get_transit_effects(
        self,
        planet: str,
        house: int,
        is_benefic: bool
    ) -> List[str]:
        """Get specific effects of transit"""
        effects_map = {
            "Sun": {
                "benefic": ["Authority", "Recognition", "Vitality", "Government favor"],
                "malefic": ["Ego conflicts", "Father's health", "Eye issues"]
            },
            "Moon": {
                "benefic": ["Emotional satisfaction", "Public support", "Mother's blessings"],
                "malefic": ["Mental stress", "Mood swings", "Water-related issues"]
            },
            "Mars": {
                "benefic": ["Energy", "Courage", "Property gains", "Victory"],
                "malefic": ["Accidents", "Conflicts", "Anger issues", "Surgery"]
            },
            "Mercury": {
                "benefic": ["Intelligence", "Communication", "Business success"],
                "malefic": ["Confusion", "Wrong decisions", "Document issues"]
            },
            "Jupiter": {
                "benefic": ["Wisdom", "Expansion", "Children", "Spirituality"],
                "malefic": ["Overconfidence", "Weight gain", "Legal issues"]
            },
            "Venus": {
                "benefic": ["Love", "Luxury", "Arts", "Marriage"],
                "malefic": ["Relationship issues", "Overspending", "Laziness"]
            },
            "Saturn": {
                "benefic": ["Discipline", "Long-term gains", "Property", "Stability"],
                "malefic": ["Delays", "Hard work", "Health issues", "Restrictions"]
            },
            "Rahu": {
                "benefic": ["Material gains", "Foreign connections", "Innovation"],
                "malefic": ["Confusion", "Illusions", "Addictions", "Sudden changes"]
            },
            "Ketu": {
                "benefic": ["Spirituality", "Liberation", "Past-life wisdom"],
                "malefic": ["Losses", "Detachment", "Accidents", "Skin issues"]
            }
        }
        
        planet_effects = effects_map.get(planet, {"benefic": [], "malefic": []})
        return planet_effects["benefic"] if is_benefic else planet_effects["malefic"]
    
    def _calculate_overall_score(self, gochara_results: List[GocharaResult]) -> Dict[str, Any]:
        """Calculate overall transit score"""
        total_score = 0
        max_score = len(gochara_results) * 10
        
        result_scores = {
            TransitResult.EXCELLENT: 10,
            TransitResult.GOOD: 8,
            TransitResult.NEUTRAL: 5,
            TransitResult.CHALLENGING: 3,
            TransitResult.DIFFICULT: 1
        }
        
        for result in gochara_results:
            total_score += result_scores[result.overall_result]
        
        percentage = (total_score / max_score) * 100 if max_score > 0 else 50
        
        if percentage >= 75:
            status = "Excellent period for progress"
        elif percentage >= 60:
            status = "Good period with minor challenges"
        elif percentage >= 45:
            status = "Mixed period - be balanced"
        elif percentage >= 30:
            status = "Challenging period - exercise caution"
        else:
            status = "Difficult period - focus on remedies"
        
        return {
            "score": round(percentage, 1),
            "status": status,
            "favorable_planets": [
                r.planet for r in gochara_results 
                if r.overall_result in [TransitResult.EXCELLENT, TransitResult.GOOD]
            ],
            "challenging_planets": [
                r.planet for r in gochara_results
                if r.overall_result in [TransitResult.CHALLENGING, TransitResult.DIFFICULT]
            ]
        }
    
    def _generate_predictions(
        self,
        gochara_results: List[GocharaResult],
        sade_sati: SadeSatiStatus
    ) -> List[Dict[str, str]]:
        """Generate predictions based on transits"""
        predictions = []
        
        # Jupiter predictions (most benefic)
        jupiter_result = next((r for r in gochara_results if r.planet == "Jupiter"), None)
        if jupiter_result:
            if jupiter_result.is_benefic:
                predictions.append({
                    "area": "Fortune & Growth",
                    "prediction": f"Jupiter in {jupiter_result.transit_house}th from Moon brings expansion and blessings.",
                    "timing": "Throughout Jupiter's transit in this sign (~1 year)"
                })
        
        # Saturn predictions
        saturn_result = next((r for r in gochara_results if r.planet == "Saturn"), None)
        if saturn_result:
            if sade_sati.is_active:
                predictions.append({
                    "area": "Challenges & Discipline",
                    "prediction": f"Sade Sati {sade_sati.phase} phase active. Focus on hard work and patience.",
                    "timing": "For the next 2.5 years approximately"
                })
            elif saturn_result.is_benefic:
                predictions.append({
                    "area": "Career & Structure",
                    "prediction": "Saturn supports long-term achievements and stability.",
                    "timing": "Throughout Saturn's transit (~2.5 years)"
                })
        
        # Venus predictions
        venus_result = next((r for r in gochara_results if r.planet == "Venus"), None)
        if venus_result and venus_result.is_benefic:
            predictions.append({
                "area": "Love & Luxury",
                "prediction": f"Venus in {venus_result.transit_house}th favors relationships and comforts.",
                "timing": "Next few weeks"
            })
        
        # Mars predictions
        mars_result = next((r for r in gochara_results if r.planet == "Mars"), None)
        if mars_result:
            if mars_result.overall_result == TransitResult.DIFFICULT:
                predictions.append({
                    "area": "Energy & Conflicts",
                    "prediction": "Mars transit requires caution in arguments and driving.",
                    "timing": "Next 6-8 weeks"
                })
            elif mars_result.is_benefic:
                predictions.append({
                    "area": "Action & Victory",
                    "prediction": "Mars supports competitive efforts and physical activities.",
                    "timing": "Next 6-8 weeks"
                })
        
        return predictions
    
    def _identify_important_transits(
        self,
        positions: List[TransitPosition]
    ) -> List[Dict[str, str]]:
        """Identify most important current transits"""
        important = []
        
        for pos in positions:
            # Jupiter sign change
            if pos.planet == "Jupiter":
                important.append({
                    "planet": "Jupiter",
                    "position": f"{pos.sign_name}",
                    "significance": "Expands matters of this sign for ~1 year",
                    "advice": "Focus on growth in areas ruled by Jupiter's current sign"
                })
            
            # Saturn position
            if pos.planet == "Saturn":
                important.append({
                    "planet": "Saturn",
                    "position": f"{pos.sign_name}",
                    "significance": "Tests and restructures for ~2.5 years",
                    "advice": "Build discipline and long-term foundations"
                })
            
            # Rahu-Ketu axis
            if pos.planet in ["Rahu", "Ketu"]:
                important.append({
                    "planet": pos.planet,
                    "position": f"{pos.sign_name}",
                    "significance": "Karmic lessons for ~1.5 years",
                    "advice": "Address past patterns and embrace new directions"
                })
        
        return important


def analyze_transits(
    natal_moon_sign: int,
    natal_planets: Dict[str, float],
    current_positions: Dict[str, float],
    current_time: datetime
) -> Dict[str, Any]:
    """
    Convenience function for transit analysis
    
    Args:
        natal_moon_sign: Moon's sign in natal chart (0-11)
        natal_planets: Dictionary of natal planet longitudes
        current_positions: Dictionary of current transit positions
        current_time: Current datetime
        
    Returns:
        Complete transit analysis
    """
    analyzer = TransitAnalyzer(natal_moon_sign, natal_planets)
    return analyzer.analyze_transit(current_positions, current_time)


def get_current_transits_summary(
    natal_moon_sign: int,
    current_saturn: float,
    current_jupiter: float,
    current_rahu: float
) -> Dict[str, str]:
    """
    Quick summary of major transits
    
    Args:
        natal_moon_sign: Moon sign (0-11)
        current_saturn: Saturn longitude
        current_jupiter: Jupiter longitude
        current_rahu: Rahu longitude
        
    Returns:
        Summary of major transits
    """
    saturn_sign = int(current_saturn / 30)
    jupiter_sign = int(current_jupiter / 30)
    rahu_sign = int(current_rahu / 30)
    
    saturn_house = ((saturn_sign - natal_moon_sign) % 12) + 1
    jupiter_house = ((jupiter_sign - natal_moon_sign) % 12) + 1
    rahu_house = ((rahu_sign - natal_moon_sign) % 12) + 1
    
    # Sade Sati check
    sade_sati = saturn_house in [12, 1, 2]
    
    summary = {
        "saturn": {
            "sign": SIGN_NAMES[saturn_sign],
            "house_from_moon": saturn_house,
            "is_favorable": saturn_house in [3, 6, 11],
            "sade_sati_active": sade_sati
        },
        "jupiter": {
            "sign": SIGN_NAMES[jupiter_sign],
            "house_from_moon": jupiter_house,
            "is_favorable": jupiter_house in [2, 5, 7, 9, 11]
        },
        "rahu": {
            "sign": SIGN_NAMES[rahu_sign],
            "house_from_moon": rahu_house,
            "is_favorable": rahu_house in [3, 6, 10, 11]
        }
    }
    
    # Overall assessment
    favorable_count = sum([
        summary["saturn"]["is_favorable"],
        summary["jupiter"]["is_favorable"],
        summary["rahu"]["is_favorable"]
    ])
    
    if sade_sati:
        summary["overall"] = "Challenging period due to Sade Sati - focus on patience"
    elif favorable_count >= 2:
        summary["overall"] = "Favorable major transits - good for progress"
    elif favorable_count == 1:
        summary["overall"] = "Mixed major transits - selective opportunities"
    else:
        summary["overall"] = "Challenging major transits - focus on remedies"
    
    return summary


# =============================================================================
# REAL-TIME TRANSIT CALCULATIONS USING SWISS EPHEMERIS
# =============================================================================

def get_current_transit_positions(
    target_datetime: datetime = None,
    ayanamsa_type: str = "lahiri"
) -> Dict[str, Dict[str, Any]]:
    """
    Get current (or specified) planetary positions using Swiss Ephemeris.
    
    Args:
        target_datetime: DateTime for positions (defaults to now)
        ayanamsa_type: Ayanamsa to use (lahiri, raman, krishnamurti)
        
    Returns:
        Dictionary of planet positions with longitude, sign, nakshatra, retrograde status
    """
    import swisseph as swe
    
    if target_datetime is None:
        target_datetime = datetime.now()
    
    # Set ayanamsa
    ayanamsa_modes = {
        "lahiri": swe.SIDM_LAHIRI,
        "raman": swe.SIDM_RAMAN,
        "krishnamurti": swe.SIDM_KRISHNAMURTI,
    }
    swe.set_sid_mode(ayanamsa_modes.get(ayanamsa_type.lower(), swe.SIDM_LAHIRI))
    
    # Calculate Julian Day
    jd = swe.julday(
        target_datetime.year,
        target_datetime.month,
        target_datetime.day,
        target_datetime.hour + target_datetime.minute / 60.0 + target_datetime.second / 3600.0
    )
    
    # Get ayanamsa value
    ayanamsa = swe.get_ayanamsa_ut(jd)
    
    # Planet mappings
    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
    }
    
    positions = {}
    
    for planet_name, planet_id in planets.items():
        try:
            # Calculate position with sidereal flag
            flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
            result = swe.calc_ut(jd, planet_id, flags)
            
            longitude = result[0][0]
            speed = result[0][3]
            is_retrograde = speed < 0
            
            # Calculate Ketu (opposite of Rahu)
            if planet_name == "Rahu":
                ketu_lon = (longitude + 180) % 360
            
            # Get sign and nakshatra
            sign_num = int(longitude / 30)
            nakshatra_num = int(longitude / (360 / 27))
            degree_in_sign = longitude % 30
            
            positions[planet_name] = {
                "longitude": round(longitude, 4),
                "sign": SIGN_NAMES[sign_num],
                "sign_num": sign_num,
                "degree_in_sign": round(degree_in_sign, 2),
                "nakshatra": NAKSHATRAS[nakshatra_num],
                "nakshatra_num": nakshatra_num,
                "is_retrograde": is_retrograde,
                "speed": round(speed, 4)
            }
            
        except Exception as e:
            positions[planet_name] = {
                "error": str(e),
                "longitude": 0,
                "sign": "Unknown",
                "is_retrograde": False
            }
    
    # Add Ketu
    if "Rahu" in positions and "error" not in positions["Rahu"]:
        rahu_lon = positions["Rahu"]["longitude"]
        ketu_lon = (rahu_lon + 180) % 360
        ketu_sign = int(ketu_lon / 30)
        ketu_nak = int(ketu_lon / (360 / 27))
        
        positions["Ketu"] = {
            "longitude": round(ketu_lon, 4),
            "sign": SIGN_NAMES[ketu_sign],
            "sign_num": ketu_sign,
            "degree_in_sign": round(ketu_lon % 30, 2),
            "nakshatra": NAKSHATRAS[ketu_nak],
            "nakshatra_num": ketu_nak,
            "is_retrograde": True,  # Rahu/Ketu always retrograde
            "speed": -positions["Rahu"]["speed"]
        }
    
    return {
        "timestamp": target_datetime.isoformat(),
        "ayanamsa": round(ayanamsa, 4),
        "ayanamsa_type": ayanamsa_type,
        "positions": positions
    }


def get_transit_to_natal_aspects(
    transit_positions: Dict[str, float],
    natal_positions: Dict[str, float],
    orb: float = 10.0
) -> List[Dict[str, Any]]:
    """
    Calculate aspects between transit and natal planets.
    
    Args:
        transit_positions: Current planetary longitudes
        natal_positions: Natal chart planetary longitudes
        orb: Maximum orb for aspects in degrees
        
    Returns:
        List of active transit-to-natal aspects
    """
    # Aspect definitions (Vedic drishti)
    aspects = {
        0: "Conjunction",
        60: "Sextile",
        90: "Square", 
        120: "Trine",
        180: "Opposition"
    }
    
    # Mars aspects 4th and 8th houses (90° and 210°)
    # Saturn aspects 3rd and 10th houses (60° and 270°)
    # Jupiter aspects 5th and 9th houses (120° and 240°)
    special_aspects = {
        "Mars": [90, 210],
        "Saturn": [60, 270],
        "Jupiter": [120, 240]
    }
    
    active_aspects = []
    
    for t_planet, t_lon in transit_positions.items():
        for n_planet, n_lon in natal_positions.items():
            # Calculate angular distance
            diff = abs(t_lon - n_lon)
            if diff > 180:
                diff = 360 - diff
            
            # Check standard aspects
            for aspect_angle, aspect_name in aspects.items():
                if abs(diff - aspect_angle) <= orb:
                    active_aspects.append({
                        "transit_planet": t_planet,
                        "natal_planet": n_planet,
                        "aspect": aspect_name,
                        "angle": aspect_angle,
                        "orb": round(abs(diff - aspect_angle), 2),
                        "exact_degree_diff": round(diff, 2),
                        "applying": t_lon < n_lon  # Simplified
                    })
            
            # Check special aspects for Mars, Saturn, Jupiter
            if t_planet in special_aspects:
                for special_angle in special_aspects[t_planet]:
                    if abs(diff - special_angle) <= orb:
                        active_aspects.append({
                            "transit_planet": t_planet,
                            "natal_planet": n_planet,
                            "aspect": f"Special ({t_planet} Drishti)",
                            "angle": special_angle,
                            "orb": round(abs(diff - special_angle), 2),
                            "exact_degree_diff": round(diff, 2),
                            "applying": t_lon < n_lon
                        })
    
    # Sort by orb (tightest aspects first)
    active_aspects.sort(key=lambda x: x["orb"])
    
    return active_aspects


def get_upcoming_transits(
    natal_moon_sign: int,
    days_ahead: int = 30
) -> List[Dict[str, Any]]:
    """
    Get upcoming significant transits for the next N days.
    
    Args:
        natal_moon_sign: Moon's sign in natal chart (0-11)
        days_ahead: Number of days to look ahead
        
    Returns:
        List of upcoming significant transits with dates
    """
    import swisseph as swe
    
    upcoming = []
    current_date = datetime.now()
    
    # Get current positions of slow planets
    current = get_current_transit_positions(current_date)
    
    # Track sign changes for slow planets (Saturn, Jupiter, Rahu)
    slow_planets = ["Saturn", "Jupiter", "Rahu"]
    
    for planet in slow_planets:
        if planet in current["positions"]:
            current_sign = current["positions"][planet]["sign_num"]
            
            # Check each day for sign change
            for day_offset in range(1, days_ahead + 1):
                check_date = current_date + timedelta(days=day_offset)
                future_pos = get_current_transit_positions(check_date)
                
                if planet in future_pos["positions"]:
                    future_sign = future_pos["positions"][planet]["sign_num"]
                    
                    if future_sign != current_sign:
                        # Sign change detected
                        house_from_moon = (future_sign - natal_moon_sign + 12) % 12 + 1
                        
                        upcoming.append({
                            "date": check_date.date().isoformat(),
                            "planet": planet,
                            "event": "Sign Change",
                            "from_sign": SIGN_NAMES[current_sign],
                            "to_sign": SIGN_NAMES[future_sign],
                            "house_from_moon": house_from_moon,
                            "is_favorable": house_from_moon in GOCHARA_BENEFIC_HOUSES.get(planet, []),
                            "significance": "High" if planet in ["Saturn", "Jupiter"] else "Medium"
                        })
                        
                        current_sign = future_sign
    
    # Sort by date
    upcoming.sort(key=lambda x: x["date"])
    
    return upcoming
