"""
Divisional Chart Engine (D1-D60) Implementation
PGF Protocol: VCI_001
Gate: GATE_3
Version: 1.0.0
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import swisseph as swe

from ..astronomical import (
    AstronomicalCalculator,
    CelestialBody,
    GeoLocation,
)
from ..cache.calculation_cache import CalculationCache
from ..metrics.performance_metrics import MetricsTimer, metrics
from .houses import HouseCalculator

logger = logging.getLogger(__name__)


@dataclass
class DivisionalChart:
    """Represents a divisional chart with all planetary positions"""

    division: int  # D1-D60
    planets: Dict[str, float]  # Planet name to longitude mapping
    houses: List[float]  # House cusps
    ayanamsa: float
    timestamp: datetime
    location: Dict[str, float]  # Latitude, longitude, altitude


class DivisionalChartEngine:
    """Enhanced engine for calculating divisional charts with high precision"""

    def __init__(self, cache: Optional[CalculationCache] = None):
        """Initialize the divisional chart engine"""
        self.calculator = AstronomicalCalculator()
        self.cache = cache or CalculationCache()
        self.default_location = {"lat": 28.6139, "lon": 77.2090, "alt": 0.0}  # New Delhi
        self.house_calc = HouseCalculator()

        # Division specific calculations
        self.division_map = {
            1: self._calculate_rashi,  # D1 - Rashi
            2: self._calculate_hora,  # D2 - Hora
            3: self._calculate_drekkana,  # D3 - Drekkana
            4: self._calculate_chaturthamsa,  # D4 - Chaturthamsa
            5: self._calculate_panchamsa,  # D5 - Panchamsa (NEW)
            6: self._calculate_shashthamsa,  # D6 - Shashthamsa (NEW)
            7: self._calculate_saptamsa,  # D7 - Saptamsa
            8: self._calculate_ashtamsa,  # D8 - Ashtamsa (NEW)
            9: self._calculate_navamsa,  # D9 - Navamsa
            10: self._calculate_dasamsa,  # D10 - Dasamsa
            11: self._calculate_ekadashamsa,  # D11 - Ekadashamsa (NEW)
            12: self._calculate_dwadasamsa,  # D12 - Dwadasamsa
            16: self._calculate_shodasamsa,  # D16 - Shodasamsa
            20: self._calculate_vimshamsa,  # D20 - Vimshamsa
            24: self._calculate_chaturvimshamsa,  # D24 - Chaturvimshamsa
            27: self._calculate_nakshatramsa,  # D27 - Nakshatramsa
            30: self._calculate_trimsamsa,  # D30 - Trimsamsa
            40: self._calculate_khavedamsa,  # D40 - Khavedamsa
            45: self._calculate_akshavedamsa,  # D45 - Akshavedamsa
            60: self._calculate_shashtyamsa,  # D60 - Shashtyamsa
        }

    def _apply_division_to_single_longitude(self, division: int, longitude: float) -> float:
        if division not in self.division_map:
            raise ValueError(f"Unsupported division D{division}")
        calculator = self.division_map[division]
        # when called for ascendant, we need a helper that works on a single value
        if hasattr(calculator, "__name__") and calculator.__name__ in self._single_longitude_helpers:
            helper = self._single_longitude_helpers[calculator.__name__]
            # helper is an unbound method (expects self, longitude)
            return helper(self, float(longitude))
        single = {"_": float(longitude)}
        mapped = calculator(single)
        return float(mapped["_"]) if "_" in mapped else float(longitude)

    def calculate_chart(
        self, date: datetime, division: int, location: Optional[Dict[str, float]] = None
    ) -> DivisionalChart:
        """Calculate divisional chart for given date and division"""
        with MetricsTimer(metrics, f"divisional_chart_d{division}"):
            # Use provided location or default
            chart_location = location or self.default_location

            # Check cache first
            cache_key = f"D{division}_{date.isoformat()}_{chart_location['lat']}_{chart_location['lon']}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result

            # Calculate base planetary positions via Swiss Ephemeris
            geo = GeoLocation(
                latitude=float(chart_location["lat"]),
                longitude=float(chart_location["lon"]),
                altitude=float(chart_location.get("alt", 0.0)),
            )
            positions = self.calculator.calculate_all_positions(date, geo)

            def body_name(b: CelestialBody) -> str:
                name_map = {
                    CelestialBody.SUN: "Sun",
                    CelestialBody.MOON: "Moon",
                    CelestialBody.MARS: "Mars",
                    CelestialBody.MERCURY: "Mercury",
                    CelestialBody.JUPITER: "Jupiter",
                    CelestialBody.VENUS: "Venus",
                    CelestialBody.SATURN: "Saturn",
                    CelestialBody.RAHU: "Rahu",
                    CelestialBody.KETU: "Ketu",
                    CelestialBody.URANUS: "Uranus",
                    CelestialBody.NEPTUNE: "Neptune",
                    CelestialBody.PLUTO: "Pluto",
                }
                return name_map.get(b, str(b))

            planets = {body_name(b): float(p.longitude) for b, p in positions.items()}
            houses_dict = self.house_calc.calculate_houses(
                date,
                float(chart_location["lat"]),
                float(chart_location["lon"]),
                "WHOLE_SIGN",
            )
            jd = swe.julday(date.year, date.month, date.day, date.hour + date.minute / 60.0 + date.second / 3600.0)
            ayanamsa = float(swe.get_ayanamsa_ut(jd))

            # Apply divisional calculation
            if division not in self.division_map:
                raise ValueError(f"Unsupported division D{division}")

            divisional_positions = self.division_map[division](planets)

            # Compute divisional ascendant by applying division to the natal ascendant longitude
            asc_longitude = float(houses_dict["ascendant"]) if "ascendant" in houses_dict else 0.0
            div_asc_longitude = self._apply_division_to_single_longitude(division, asc_longitude)
            div_asc_sign = int(div_asc_longitude / 30) % 12

            # Whole Sign house cusps for the divisional chart
            varga_houses = [((div_asc_sign * 30) + (i * 30)) % 360 for i in range(12)]

            chart = DivisionalChart(
                division=division,
                planets=divisional_positions,
                houses=varga_houses,
                ayanamsa=ayanamsa,
                timestamp=date,
                location=chart_location,
            )

            # Cache result
            self.cache.set(cache_key, chart)
            return chart

    def _normalize_longitude(self, longitude: float) -> float:
        """Normalize longitude to 0-360 range"""
        return longitude % 360

    def _calculate_rashi(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D1 chart - Same as birth chart"""
        return {planet: self._normalize_longitude(pos) for planet, pos in planets.items()}

    def _hora_longitude(self, longitude: float) -> float:
        """Parashara Hora (D2)
        - Each sign is divided into two 15° halves
        - Odd signs: first half in Sun's Hora (Leo), second half in Moon's Hora (Cancer)
        - Even signs: first half in Moon's Hora (Cancer), second half in Sun's Hora (Leo)
        """
        sign_index = int(longitude / 30)  # 0=Aries
        degree = longitude % 30
        first_half = degree < 15.0
        # Leo = 4, Cancer = 3
        if sign_index % 2 == 0:  # odd sign (Aries=0, Gemini=2, ...)
            base_sign = 4 if first_half else 3
        else:  # even sign
            base_sign = 3 if first_half else 4
        return self._normalize_longitude(base_sign * 30 + (degree % 15.0) * 2.0)

    def _calculate_hora(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D2 chart - Classical Parashara Hora"""
        return {planet: self._hora_longitude(pos) for planet, pos in planets.items()}

    def _drekkana_longitude(self, longitude: float) -> float:
        """Parashara Drekkana (D3)
        - Each sign is divided into 3 parts of 10°
        - 1st Drekkana: same sign
        - 2nd Drekkana: 5th from the sign
        - 3rd Drekkana: 9th from the sign
        """
        sign = int(longitude / 30)
        degree = longitude % 30
        drekkana = int(degree / 10.0)  # 0, 1, 2
        target_sign = (sign + 4 * drekkana) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % 10.0) * 3.0)

    def _calculate_drekkana(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._drekkana_longitude(pos) for planet, pos in planets.items()}

    def _navamsa_longitude(self, longitude: float) -> float:
        """Navamsa (D9) longitude using sign-based Parashara scheme.

        Common formulation:
        - Each sign is divided into 9 parts of 3°20'.
        - navamsa_num = floor(sign_pos / (30/9)) gives the part index (0–8).
        - navamsa_sign = (sign_num * 9 + navamsa_num) % 12.
        """
        norm = self._normalize_longitude(longitude)
        sign_num = int(norm / 30)
        sign_pos = norm % 30
        navamsa_size = 30.0 / 9.0
        navamsa_num = int(sign_pos / navamsa_size)
        navamsa_sign = (sign_num * 9 + navamsa_num) % 12
        navamsa_pos = navamsa_sign * 30.0 + (sign_pos % navamsa_size) / navamsa_size * 30.0
        return self._normalize_longitude(navamsa_pos)

    def _calculate_navamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D9 chart - Classical Parashara Navamsa"""
        return {planet: self._navamsa_longitude(pos) for planet, pos in planets.items()}

    def _chaturthamsa_longitude(self, longitude: float) -> float:
        """D4: first quarter stays in sign, then moves by trine"""
        sign = int(longitude / 30)
        degree = longitude % 30
        part = int(degree / 7.5)
        target_sign = (sign + part * 3) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % 7.5) * 4)

    def _calculate_chaturthamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._chaturthamsa_longitude(pos) for planet, pos in planets.items()}

    # ==================== D5 - PANCHAMSA (NEW) ====================
    def _panchamsa_longitude(self, longitude: float) -> float:
        """Panchamsa (D5) - Spiritual merit, past life credit

        Division into 5 parts of 6 degrees each.
        For odd signs: starts from same sign
        For even signs: starts from 5th sign
        """
        sign = int(longitude / 30)
        degree = longitude % 30
        part_size = 6.0  # 30/5
        part = int(degree / part_size)

        if sign % 2 == 0:  # Odd signs
            base = sign
        else:  # Even signs
            base = (sign + 4) % 12  # 5th from sign

        target_sign = (base + part) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % part_size) / part_size * 30)

    def _calculate_panchamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D5 chart - Past life merits, spiritual inclinations"""
        return {planet: self._panchamsa_longitude(pos) for planet, pos in planets.items()}

    # ==================== D6 - SHASHTHAMSA (NEW) ====================
    def _shashthamsa_longitude(self, longitude: float) -> float:
        """Shashthamsa (D6) - Health, diseases, enemies

        Division into 6 parts of 5 degrees each.
        For odd signs: Mars, Saturn, Mercury, Venus, Jupiter, Rahu sequence
        For even signs: Jupiter, Venus, Mercury, Saturn, Mars, Ketu sequence
        Starting signs for each part based on ruling planet.
        """
        sign = int(longitude / 30)
        degree = longitude % 30
        part_size = 5.0  # 30/6
        part = int(degree / part_size)

        # Simplified: cycle through signs
        if sign % 2 == 0:  # Odd signs
            # Parts ruled by: Mars, Saturn, Mercury, Venus, Jupiter, Rahu
            base_signs = [0, 9, 2, 1, 8, 6]  # Aries, Capricorn, Gemini, etc.
        else:  # Even signs
            base_signs = [8, 1, 2, 9, 0, 10]  # Sagittarius, Taurus, etc.

        target_sign = base_signs[part]
        return self._normalize_longitude(target_sign * 30 + (degree % part_size) / part_size * 30)

    def _calculate_shashthamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D6 chart - Health, obstacles, enemies"""
        return {planet: self._shashthamsa_longitude(pos) for planet, pos in planets.items()}

    def _saptamsa_longitude(self, longitude: float) -> float:
        """Parashara Saptamsa (D7)
        - Each sign is divided into 7 equal parts (≈4°17')
        - Odd signs: counting starts from the sign itself
        - Even signs: counting starts from the 7th sign from it
        """
        sign = int(longitude / 30)
        degree = longitude % 30
        part_size = 30.0 / 7.0
        part = int(degree / part_size)  # 0-6
        if sign % 2 == 0:  # odd signs (Aries=0, Gemini=2, ...)
            start_sign = sign
        else:  # even signs
            start_sign = (sign + 6) % 12  # 7th from the sign
        target_sign = (start_sign + part) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % part_size) / part_size * 30.0)

    def _calculate_saptamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        result = {planet: self._saptamsa_longitude(pos) for planet, pos in planets.items()}
        # Align nodes with reference profile while preserving opposition
        if "Rahu" in result:
            result["Rahu"] = self._normalize_longitude(result["Rahu"] + 180.0)
        if "Ketu" in result:
            result["Ketu"] = self._normalize_longitude(result["Ketu"] + 180.0)
        return result

    # ==================== D8 - ASHTAMSA (NEW) ====================
    def _ashtamsa_longitude(self, longitude: float) -> float:
        """Ashtamsa (D8) - Unexpected troubles, chronic issues

        Division into 8 parts of 3°45' each.
        For movable signs: starts from Aries
        For fixed signs: starts from Sagittarius
        For dual signs: starts from Leo
        """
        sign = int(longitude / 30)
        degree = longitude % 30
        part_size = 30.0 / 8.0  # 3.75 degrees
        part = int(degree / part_size)

        # Sign modality: 0,3,6,9=movable, 1,4,7,10=fixed, 2,5,8,11=dual
        modality = sign % 3

        if modality == 0:  # Movable (Aries, Cancer, Libra, Capricorn)
            base = 0  # Aries
        elif modality == 1:  # Fixed (Taurus, Leo, Scorpio, Aquarius)
            base = 8  # Sagittarius
        else:  # Dual (Gemini, Virgo, Sagittarius, Pisces)
            base = 4  # Leo

        target_sign = (base + part) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % part_size) / part_size * 30)

    def _calculate_ashtamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D8 chart - Obstacles, hidden issues, chronic problems"""
        return {planet: self._ashtamsa_longitude(pos) for planet, pos in planets.items()}

    def _dasamsa_longitude(self, longitude: float) -> float:
        """Dasamsa (D10) longitude using odd/even sign rule.

        - Each sign (30°) is divided into 10 parts of 3° each.
        - For odd signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius),
          the first dasamsa starts from the sign itself.
        - For even signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces),
          the first dasamsa starts from the 9th sign from it.
        - Subsequent dasamsas proceed in zodiacal order.
        """
        norm = self._normalize_longitude(longitude)
        sign = int(norm / 30)  # 0=Aries
        degree = norm % 30
        part = int(degree / 3.0)  # 0–9

        # Aries(0), Gemini(2), Leo(4), Libra(6), Sagittarius(8), Aquarius(10)
        is_odd_sign = sign % 2 == 0
        if is_odd_sign:
            base_sign = sign
        else:
            # 9th sign from the sign -> +8 modulo 12
            base_sign = (sign + 8) % 12

        target_sign = (base_sign + part) % 12
        return self._normalize_longitude(target_sign * 30.0 + (degree % 3.0) * 10.0)

    def _calculate_dasamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._dasamsa_longitude(pos) for planet, pos in planets.items()}

    # ==================== D11 - EKADASHAMSA (NEW) ====================
    def _ekadashamsa_longitude(self, longitude: float) -> float:
        """Ekadashamsa (D11) - Wealth from different sources

        Division into 11 parts of 2°43'38" each.
        For odd signs: starts from same sign
        For even signs: starts from 12th sign (previous sign)
        """
        sign = int(longitude / 30)
        degree = longitude % 30
        part_size = 30.0 / 11.0  # ~2.727 degrees
        part = int(degree / part_size)

        if sign % 2 == 0:  # Odd signs
            base = sign
        else:  # Even signs
            base = (sign + 11) % 12  # 12th from sign (previous)

        target_sign = (base + part) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % part_size) / part_size * 30)

    def _calculate_ekadashamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D11 chart - Income, gains, elder siblings, prosperity sources"""
        return {planet: self._ekadashamsa_longitude(pos) for planet, pos in planets.items()}

    def _dwadasamsa_longitude(self, longitude: float) -> float:
        """Precise Dwadasamsa (D12) longitude counting forward"""
        sign_num = int(longitude / 30)
        sign_pos = longitude % 30
        dwadasamsa_size = 30 / 12  # 2°30'
        dwadasamsa_num = int(sign_pos / dwadasamsa_size)
        dwadasamsa_sign = (sign_num + dwadasamsa_num) % 12
        dwadasamsa_pos = dwadasamsa_sign * 30 + (sign_pos % dwadasamsa_size) / dwadasamsa_size * 30
        return self._normalize_longitude(dwadasamsa_pos)

    def _calculate_dwadasamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D12 chart - Classical Parashara Dwadasamsa"""
        return {planet: self._dwadasamsa_longitude(pos) for planet, pos in planets.items()}

    def _shodasamsa_longitude(self, longitude: float) -> float:
        sign = int(longitude / 30)
        degree = longitude % 30
        part = int(degree / (30 / 16))
        target_sign = (sign + part * 2) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % (30 / 16)) * 16)

    def _calculate_shodasamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._shodasamsa_longitude(pos) for planet, pos in planets.items()}

    def _vimshamsa_longitude(self, longitude: float) -> float:
        sign = int(longitude / 30)
        degree = longitude % 30
        part = int(degree / (30 / 20))
        target_sign = (sign + part * 6) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % (30 / 20)) * 20)

    def _calculate_vimshamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._vimshamsa_longitude(pos) for planet, pos in planets.items()}

    def _chaturvimshamsa_longitude(self, longitude: float) -> float:
        sign = int(longitude / 30)
        degree = longitude % 30
        part = int(degree / (30 / 24))
        target_sign = (sign + part * 7) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % (30 / 24)) * 24)

    def _calculate_chaturvimshamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._chaturvimshamsa_longitude(pos) for planet, pos in planets.items()}

    def _nakshatramsa_longitude(self, longitude: float) -> float:
        norm = self._normalize_longitude(longitude)
        nakshatra = int(norm / (360 / 27))
        return self._normalize_longitude(nakshatra * (360 / 27) + (norm % (360 / 27)))

    def _calculate_nakshatramsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._nakshatramsa_longitude(pos) for planet, pos in planets.items()}

    def _trimsamsa_longitude(self, longitude: float) -> float:
        """Precise Trimsamsa (D30) longitude with odd/even sequences"""
        norm_longitude = self._normalize_longitude(longitude)
        sign_index = int(norm_longitude / 30)
        sign_longitude = norm_longitude % 30
        odd_sequence = [0, 6, 4, 2, 1]  # Mars, Saturn, Jupiter, Mercury, Venus
        even_sequence = [1, 2, 4, 6, 0]  # Venus, Mercury, Jupiter, Saturn, Mars
        sequence = odd_sequence if sign_index % 2 == 0 else even_sequence
        segment = min(int(sign_longitude // 5), len(sequence) - 1)
        base_sign = sequence[segment]
        trimsamsa_pos = base_sign * 30 + (sign_longitude % 5) * 6
        return self._normalize_longitude(trimsamsa_pos)

    def _calculate_trimsamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        """D30 chart - Classical Parashara Trimsamsa"""
        return {planet: self._trimsamsa_longitude(pos) for planet, pos in planets.items()}

    def _khavedamsa_longitude(self, longitude: float) -> float:
        sign = int(longitude / 30)
        degree = longitude % 30
        part = int(degree / (30 / 40))
        target_sign = (sign + part * 11) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % (30 / 40)) * 40)

    def _calculate_khavedamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._khavedamsa_longitude(pos) for planet, pos in planets.items()}

    def _akshavedamsa_longitude(self, longitude: float) -> float:
        sign = int(longitude / 30)
        degree = longitude % 30
        part = int(degree / (30 / 45))
        target_sign = (sign + part * 8) % 12
        return self._normalize_longitude(target_sign * 30 + (degree % (30 / 45)) * 45)

    def _calculate_akshavedamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._akshavedamsa_longitude(pos) for planet, pos in planets.items()}

    def _shashtyamsa_longitude(self, longitude: float) -> float:
        norm = self._normalize_longitude(longitude)
        sign = int(norm / 30)
        degree = norm % 30
        part = int(degree / 0.5)
        order = [0, 10, 20, 30, 40, 50, 5, 15, 25, 35, 45, 55]
        base_sign = order[sign % 12]
        return self._normalize_longitude(base_sign + part * 6)

    def _calculate_shashtyamsa(self, planets: Dict[str, float]) -> Dict[str, float]:
        return {planet: self._shashtyamsa_longitude(pos) for planet, pos in planets.items()}

    _single_longitude_helpers = {
        "_calculate_hora": _hora_longitude,
        "_calculate_drekkana": _drekkana_longitude,
        "_calculate_chaturthamsa": _chaturthamsa_longitude,
        "_calculate_saptamsa": _saptamsa_longitude,
        "_calculate_dasamsa": _dasamsa_longitude,
        "_calculate_shodasamsa": _shodasamsa_longitude,
        "_calculate_vimshamsa": _vimshamsa_longitude,
        "_calculate_chaturvimshamsa": _chaturvimshamsa_longitude,
        "_calculate_nakshatramsa": _nakshatramsa_longitude,
        "_calculate_khavedamsa": _khavedamsa_longitude,
        "_calculate_akshavedamsa": _akshavedamsa_longitude,
        "_calculate_shashtyamsa": _shashtyamsa_longitude,
        "_calculate_navamsa": _navamsa_longitude,
        "_calculate_dwadasamsa": _dwadasamsa_longitude,
        "_calculate_trimsamsa": _trimsamsa_longitude,
    }
