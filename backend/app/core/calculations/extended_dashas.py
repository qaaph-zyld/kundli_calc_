"""
Extended Dasha Systems (10 Additional)
PGF Protocol: DASHA_004
Gate: GATE_5
Version: 1.0.0

Implements:
1. Moola Dasha
2. Niryana Shodashottari Dasha
3. Panchottari Dasha (105 year)
4. Shatabdika Dasha (100 year)
5. Chaturashthi Sama Dasha (64 year)
6. Dwadashottari Dasha (112 year)
7. Shashti Hayani Dasha (60 year)
8. Shat Trimsha Sama Dasha (36 year)
9. Karaka Dasha (Jaimini)
10. Mandooka Dasha (Frog Dasha)
"""

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
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

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

NAKSHATRA_NAMES = [
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


@dataclass
class DashaPeriod:
    """A dasha period"""

    ruler: str  # Planet or Sign
    start_date: datetime
    end_date: datetime
    years: float
    level: int = 1
    sub_periods: List["DashaPeriod"] = field(default_factory=list)


class MoolaDasha:
    """
    Moola Dasha (Root Dasha)

    Based on Nakshatra at birth. Uses nakshatra lords.
    Special dasha for determining root karma.
    """

    # Nakshatra lord years for Moola Dasha
    MOOLA_YEARS = {
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
    }

    NAKSHATRA_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"] * 3

    def calculate(self, birth_time: datetime, moon_longitude: float) -> List[DashaPeriod]:
        """Calculate Moola Dasha periods"""
        nak_idx = int(moon_longitude / (360 / 27))
        start_lord = self.NAKSHATRA_LORDS[nak_idx]

        # Balance at birth
        nak_span = 360 / 27
        pos_in_nak = moon_longitude % nak_span
        balance = 1 - (pos_in_nak / nak_span)

        # Build sequence
        lord_idx = [k for k in self.MOOLA_YEARS.keys()].index(start_lord)
        sequence = list(self.MOOLA_YEARS.keys())[lord_idx:] + list(self.MOOLA_YEARS.keys())[:lord_idx]

        periods = []
        current = birth_time

        for i, lord in enumerate(sequence[:9]):
            years = self.MOOLA_YEARS[lord]
            if i == 0:
                years *= balance

            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=lord, start_date=current, end_date=end, years=round(years, 2)))
            current = end

        return periods


class NiryanaShodashottariDasha:
    """
    Niryana Shodashottari Dasha (116 year cycle)

    Applicable when Lagna is in Krishna Paksha and Moon
    is in angles (1,4,7,10) from Sun.
    """

    YEARS = {"Sun": 11, "Moon": 5, "Mars": 12, "Mercury": 13, "Saturn": 29, "Jupiter": 12, "Rahu": 12, "Venus": 22}

    SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", "Saturn", "Jupiter", "Rahu", "Venus"]

    def calculate(self, birth_time: datetime, moon_longitude: float) -> List[DashaPeriod]:
        """Calculate Niryana Shodashottari Dasha"""
        nak_idx = int(moon_longitude / (360 / 27))
        start_idx = nak_idx % 8

        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]

        nak_span = 360 / 27
        balance = 1 - (moon_longitude % nak_span) / nak_span

        periods = []
        current = birth_time

        for i, planet in enumerate(sequence):
            years = self.YEARS[planet]
            if i == 0:
                years *= balance

            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=planet, start_date=current, end_date=end, years=round(years, 2)))
            current = end

        return periods


class PanchottariDasha:
    """
    Panchottari Dasha (105 year cycle)

    Applicable when Lagna is in Cancer.
    """

    YEARS = {"Sun": 12, "Moon": 13, "Mars": 8, "Mercury": 17, "Saturn": 11, "Jupiter": 22, "Rahu": 8, "Venus": 14}

    SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", "Saturn", "Jupiter", "Rahu", "Venus"]

    def calculate(self, birth_time: datetime, moon_longitude: float) -> List[DashaPeriod]:
        """Calculate Panchottari Dasha"""
        nak_idx = int(moon_longitude / (360 / 27))
        start_idx = nak_idx % 8

        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]

        nak_span = 360 / 27
        balance = 1 - (moon_longitude % nak_span) / nak_span

        periods = []
        current = birth_time

        for i, planet in enumerate(sequence):
            years = self.YEARS[planet]
            if i == 0:
                years *= balance

            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=planet, start_date=current, end_date=end, years=round(years, 2)))
            current = end

        return periods


class ShatabdikaDasha:
    """
    Shatabdika Dasha (100 year cycle)

    Applied for longevity calculations.
    """

    YEARS = {
        "Sun": 5,
        "Moon": 5,
        "Venus": 10,
        "Mercury": 10,
        "Jupiter": 20,
        "Mars": 20,
        "Saturn": 20,
        "Rahu": 5,
        "Ketu": 5,
    }

    SEQUENCE = ["Sun", "Moon", "Venus", "Mercury", "Jupiter", "Mars", "Saturn", "Rahu", "Ketu"]

    def calculate(self, birth_time: datetime, moon_longitude: float) -> List[DashaPeriod]:
        """Calculate Shatabdika Dasha"""
        nak_idx = int(moon_longitude / (360 / 27))
        start_idx = nak_idx % 9

        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]

        nak_span = 360 / 27
        balance = 1 - (moon_longitude % nak_span) / nak_span

        periods = []
        current = birth_time

        for i, planet in enumerate(sequence):
            years = self.YEARS[planet]
            if i == 0:
                years *= balance

            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=planet, start_date=current, end_date=end, years=round(years, 2)))
            current = end

        return periods


class ChaturashtihiSamaDasha:
    """
    Chaturashthi Sama Dasha (64 year cycle)

    Equal 8-year periods for each planet.
    """

    YEARS_PER_PLANET = 8
    SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]

    def calculate(self, birth_time: datetime, ascendant: float) -> List[DashaPeriod]:
        """Calculate Chaturashthi Sama Dasha"""
        asc_sign = int(ascendant / 30)
        start_idx = asc_sign % 8

        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]

        periods = []
        current = birth_time

        for planet in sequence:
            years = self.YEARS_PER_PLANET
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=planet, start_date=current, end_date=end, years=years))
            current = end

        return periods


class DwadashottariDasha:
    """
    Dwadashottari Dasha (112 year cycle)

    Applicable when Lagna is in Venus signs (Taurus/Libra).
    """

    YEARS = {"Sun": 7, "Moon": 9, "Mars": 11, "Mercury": 17, "Jupiter": 11, "Venus": 21, "Saturn": 21, "Rahu": 15}

    SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]

    def calculate(self, birth_time: datetime, moon_longitude: float) -> List[DashaPeriod]:
        """Calculate Dwadashottari Dasha"""
        nak_idx = int(moon_longitude / (360 / 27))
        start_idx = nak_idx % 8

        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]

        nak_span = 360 / 27
        balance = 1 - (moon_longitude % nak_span) / nak_span

        periods = []
        current = birth_time

        for i, planet in enumerate(sequence):
            years = self.YEARS[planet]
            if i == 0:
                years *= balance

            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=planet, start_date=current, end_date=end, years=round(years, 2)))
            current = end

        return periods


class ShastiHayaniDasha:
    """
    Shashti Hayani Dasha (60 year cycle)

    Tropical-style dasha based on Sun's position.
    """

    YEARS = {
        "Sun": 6,
        "Moon": 6,
        "Mars": 6,
        "Mercury": 6,
        "Jupiter": 10,
        "Venus": 10,
        "Saturn": 10,
        "Rahu": 3,
        "Ketu": 3,
    }

    SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

    def calculate(self, birth_time: datetime, sun_longitude: float) -> List[DashaPeriod]:
        """Calculate Shashti Hayani Dasha based on Sun's position"""
        sun_sign = int(sun_longitude / 30)
        start_idx = sun_sign % 9

        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]

        # Balance from Sun's position in sign
        balance = 1 - (sun_longitude % 30) / 30

        periods = []
        current = birth_time

        for i, planet in enumerate(sequence):
            years = self.YEARS[planet]
            if i == 0:
                years *= balance

            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=planet, start_date=current, end_date=end, years=round(years, 2)))
            current = end

        return periods


class ShatTrimsaSamaDasha:
    """
    Shat Trimsha Sama Dasha (36 year cycle)

    Equal 4-year periods. Similar to Yogini but different sequence.
    """

    YEARS_PER_PLANET = 4
    SEQUENCE = ["Moon", "Sun", "Jupiter", "Mars", "Mercury", "Saturn", "Venus", "Rahu", "Ketu"]

    def calculate(self, birth_time: datetime, moon_longitude: float) -> List[DashaPeriod]:
        """Calculate Shat Trimsha Sama Dasha"""
        nak_idx = int(moon_longitude / (360 / 27))
        start_idx = nak_idx % 9

        sequence = self.SEQUENCE[start_idx:] + self.SEQUENCE[:start_idx]

        periods = []
        current = birth_time

        for planet in sequence:
            years = self.YEARS_PER_PLANET
            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=planet, start_date=current, end_date=end, years=years))
            current = end

        return periods


class KarakaDasha:
    """
    Karaka Dasha (Jaimini)

    Based on Chara Karakas (temporal significators).
    """

    KARAKA_ORDER = ["AK", "AmK", "BK", "MK", "PK", "GK", "DK"]

    def calculate(self, birth_time: datetime, planets: Dict[str, float]) -> List[DashaPeriod]:
        """
        Calculate Karaka Dasha

        Karakas are determined by longitude (excluding signs).
        """
        # Calculate Chara Karakas
        planet_degrees = {}
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            if planet in planets:
                planet_degrees[planet] = planets[planet] % 30

        # Sort by degree (highest = Atmakaraka)
        sorted_planets = sorted(planet_degrees.items(), key=lambda x: x[1], reverse=True)

        karakas = {}
        for i, (planet, _) in enumerate(sorted_planets):
            if i < len(self.KARAKA_ORDER):
                karakas[self.KARAKA_ORDER[i]] = planet

        # Periods based on sign count from Karaka
        periods = []
        current = birth_time

        for karaka_name, planet in karakas.items():
            planet_lon = planets.get(planet, 0)
            planet_sign = int(planet_lon / 30)

            # Years = sign position + 1 (simplified)
            years = planet_sign + 1

            end = current + timedelta(days=years * 365.25)
            periods.append(
                DashaPeriod(ruler=f"{karaka_name} ({planet})", start_date=current, end_date=end, years=years)
            )
            current = end

        return periods


class MandookaDasha:
    """
    Mandooka Dasha (Frog Dasha)

    Jumps through signs like a frog.
    Progression: 1→4→7→10 (or 3 signs each time)
    """

    def calculate(self, birth_time: datetime, ascendant: float) -> List[DashaPeriod]:
        """Calculate Mandooka Dasha"""
        asc_sign = int(ascendant / 30)

        periods = []
        current = birth_time

        # Jump through signs (every 3rd)
        for i in range(12):
            sign_num = (asc_sign + i * 3) % 12

            # Years = sign modality
            # Cardinal: 7, Fixed: 8, Dual: 9
            modality = sign_num % 3
            years = 7 + modality

            end = current + timedelta(days=years * 365.25)
            periods.append(DashaPeriod(ruler=SIGNS[sign_num], start_date=current, end_date=end, years=years))
            current = end

        return periods


def calculate_all_extended_dashas(
    birth_time: datetime, moon_longitude: float, sun_longitude: float, ascendant: float, planets: Dict[str, float]
) -> Dict[str, Any]:
    """
    Calculate all 10 extended dasha systems

    Returns complete dasha data for all systems
    """
    results = {}

    # 1. Moola Dasha
    moola = MoolaDasha()
    results["moola_dasha"] = {
        "name": "Moola Dasha",
        "cycle": "120 years",
        "applicability": "Root karma determination",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in moola.calculate(birth_time, moon_longitude)
        ],
    }

    # 2. Niryana Shodashottari
    niryana = NiryanaShodashottariDasha()
    results["niryana_shodashottari"] = {
        "name": "Niryana Shodashottari Dasha",
        "cycle": "116 years",
        "applicability": "Krishna Paksha, Moon in angles",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in niryana.calculate(birth_time, moon_longitude)
        ],
    }

    # 3. Panchottari
    panchottari = PanchottariDasha()
    results["panchottari"] = {
        "name": "Panchottari Dasha",
        "cycle": "105 years",
        "applicability": "Cancer Lagna",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in panchottari.calculate(birth_time, moon_longitude)
        ],
    }

    # 4. Shatabdika
    shatabdika = ShatabdikaDasha()
    results["shatabdika"] = {
        "name": "Shatabdika Dasha",
        "cycle": "100 years",
        "applicability": "Longevity calculations",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in shatabdika.calculate(birth_time, moon_longitude)
        ],
    }

    # 5. Chaturashthi Sama
    chaturashthi = ChaturashtihiSamaDasha()
    results["chaturashthi_sama"] = {
        "name": "Chaturashthi Sama Dasha",
        "cycle": "64 years",
        "applicability": "Equal periods",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in chaturashthi.calculate(birth_time, ascendant)
        ],
    }

    # 6. Dwadashottari
    dwadashottari = DwadashottariDasha()
    results["dwadashottari"] = {
        "name": "Dwadashottari Dasha",
        "cycle": "112 years",
        "applicability": "Venus Lagna (Taurus/Libra)",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in dwadashottari.calculate(birth_time, moon_longitude)
        ],
    }

    # 7. Shashti Hayani
    shashti = ShastiHayaniDasha()
    results["shashti_hayani"] = {
        "name": "Shashti Hayani Dasha",
        "cycle": "60 years",
        "applicability": "Based on Sun's position",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in shashti.calculate(birth_time, sun_longitude)
        ],
    }

    # 8. Shat Trimsha Sama
    shat_trimsha = ShatTrimsaSamaDasha()
    results["shat_trimsha_sama"] = {
        "name": "Shat Trimsha Sama Dasha",
        "cycle": "36 years",
        "applicability": "Equal 4-year periods",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in shat_trimsha.calculate(birth_time, moon_longitude)
        ],
    }

    # 9. Karaka Dasha
    karaka = KarakaDasha()
    results["karaka_dasha"] = {
        "name": "Karaka Dasha (Jaimini)",
        "cycle": "Variable",
        "applicability": "Chara Karaka based",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in karaka.calculate(birth_time, planets)
        ],
    }

    # 10. Mandooka Dasha
    mandooka = MandookaDasha()
    results["mandooka"] = {
        "name": "Mandooka Dasha (Frog)",
        "cycle": "96 years",
        "applicability": "Jumping progression",
        "periods": [
            {"ruler": p.ruler, "start": p.start_date.isoformat(), "end": p.end_date.isoformat(), "years": p.years}
            for p in mandooka.calculate(birth_time, ascendant)
        ],
    }

    return results
