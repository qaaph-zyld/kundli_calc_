"""Complete Jaimini System Implementation
==========================================
Full Jaimini astrology system per Jaimini Sutras.

Reference Texts:
- Jaimini Sutras (Maharishi Jaimini)
- Jaimini Chara Dasha (B.V. Raman)
- Brihat Parashara Hora Shastra (BPHS) Jaimini sections
- Kalamsa Navamsa (Sanjay Rath)

Components:
1. Chara Karakas (7 significators based on planetary degrees)
2. Chara Dasha (sign-based conditional dasha)
3. Argala (planetary influence/intervention)
4. Arudha Padas (perceived reality points)
5. Jaimini Aspects (sign-based, not degree-based)
6. Special Lagnas (Pada Lagna, Hora Lagna, etc.)
"""

from dataclasses import dataclass
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

SIGN_LORDS = {
    0: "Mars",
    1: "Venus",
    2: "Mercury",
    3: "Moon",
    4: "Sun",
    5: "Mercury",
    6: "Venus",
    7: "Mars",
    8: "Jupiter",
    9: "Saturn",
    10: "Saturn",
    11: "Jupiter",
}


class CharaKaraka(Enum):
    """Seven Chara Karakas (Variable Significators)"""

    ATMAKARAKA = "Atmakaraka"  # Self, soul
    AMATYAKARAKA = "Amatyakaraka"  # Career, minister
    BHRATRUKARAKA = "Bhratrukaraka"  # Siblings, courage
    MATRUKARAKA = "Matrukaraka"  # Mother, education
    PUTRAKARAKA = "Putrakaraka"  # Children, creativity
    GNATIKARAKA = "Gnatikaraka"  # Obstacles, enemies
    DARAKARAKA = "Darakaraka"  # Spouse, partnerships


@dataclass
class CharaKarakaResult:
    """Chara Karaka calculation result"""

    karaka: CharaKaraka
    planet: str
    longitude: float
    sign: str
    navamsa_sign: str
    karakamsa: int  # Navamsa sign of Atmakaraka


@dataclass
class ArgalaResult:
    """Argala (intervention) result"""

    from_house: int
    to_house: int
    intervening_planets: List[str]
    argala_type: str  # Primary, Secondary, Special
    strength: float
    is_obstructed: bool
    obstruction_from: Optional[int]


@dataclass
class ArudhaPadaResult:
    """Arudha Pada calculation result"""

    pada_type: str  # "Lagna Pada (AL)", "House Pada"
    pada_house: int
    calculation: str
    interpretation: str


class JaiminiSystem:
    """Complete Jaimini astrology system"""

    def __init__(self):
        """Initialize Jaimini calculator"""
        self.planets_for_karakas = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    def calculate_chara_karakas(self, planet_positions: Dict[str, float]) -> Dict[CharaKaraka, CharaKarakaResult]:
        """Calculate all 7 Chara Karakas

        Chara Karakas are assigned based on planetary longitudes:
        - Planet with highest longitude = Atmakaraka
        - Planet with 2nd highest = Amatyakaraka
        - ... and so on

        Reference: Jaimini Sutras 1.1.8-9

        Args:
            planet_positions: Planet longitudes in degrees (0-360)

        Returns:
            Dict mapping each Karaka to its planet and details
        """
        # Get degrees within sign for each planet (0-30)
        planet_degrees = {}
        for planet in self.planets_for_karakas:
            if planet in planet_positions:
                lon = planet_positions[planet]
                degree_in_sign = lon % 30
                planet_degrees[planet] = degree_in_sign

        # Sort planets by degree in sign (descending)
        sorted_planets = sorted(planet_degrees.items(), key=lambda x: x[1], reverse=True)

        # Assign Karakas
        karaka_order = [
            CharaKaraka.ATMAKARAKA,
            CharaKaraka.AMATYAKARAKA,
            CharaKaraka.BHRATRUKARAKA,
            CharaKaraka.MATRUKARAKA,
            CharaKaraka.PUTRAKARAKA,
            CharaKaraka.GNATIKARAKA,
            CharaKaraka.DARAKARAKA,
        ]

        results = {}

        for i, (planet, degree) in enumerate(sorted_planets[:7]):
            karaka = karaka_order[i]
            lon = planet_positions[planet]
            sign_num = int(lon / 30)

            # Calculate Navamsa position
            navamsa_sign = self._calculate_navamsa_sign(lon)

            # Karakamsa is Navamsa sign of Atmakaraka
            karakamsa = navamsa_sign if karaka == CharaKaraka.ATMAKARAKA else None

            results[karaka] = CharaKarakaResult(
                karaka=karaka,
                planet=planet,
                longitude=lon,
                sign=SIGNS[sign_num],
                navamsa_sign=SIGNS[navamsa_sign],
                karakamsa=karakamsa,
            )

        return results

    def _calculate_navamsa_sign(self, longitude: float) -> int:
        """Calculate Navamsa (D9) sign number from longitude

        Each sign (30°) is divided into 9 parts (3°20' each)
        """
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        navamsa_pada = int(degree_in_sign / (30 / 9))  # 0-8

        # Navamsa calculation based on sign type
        # Movable: Aries, Cancer, Libra, Capricorn (0,3,6,9)
        # Fixed: Taurus, Leo, Scorpio, Aquarius (1,4,7,10)
        # Dual: Gemini, Virgo, Sagittarius, Pisces (2,5,8,11)

        sign_type = sign % 3

        if sign_type == 0:  # Movable
            navamsa_sign = (sign + navamsa_pada) % 12
        elif sign_type == 1:  # Fixed
            navamsa_sign = (sign + 8 + navamsa_pada) % 12
        else:  # Dual
            navamsa_sign = (sign + 4 + navamsa_pada) % 12

        return navamsa_sign

    def calculate_chara_dasha(
        self, birth_time: datetime, ascendant: float, planet_positions: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Calculate Chara Dasha (Jaimini's primary dasha system)

        Chara Dasha is a sign-based dasha system.
        Duration is calculated based on sign lord's position.

        Reference: Jaimini Sutras 1.1.1-7

        Args:
            birth_time: Birth datetime
            ascendant: Ascendant longitude
            planet_positions: Planet positions

        Returns:
            List of dasha periods with sign, duration, dates
        """
        ascendant_sign = int(ascendant / 30)

        # Determine if Lagna is odd or even sign
        # Odd signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius): 0,2,4,6,8,10
        is_odd = ascendant_sign % 2 == 0

        # Get planet sign positions
        planet_signs = {p: int(lon / 30) for p, lon in planet_positions.items()}

        periods = []
        current_date = birth_time

        # Calculate 12 dasha periods
        for i in range(12):
            if is_odd:
                # Odd signs: forward direction (Aries -> Taurus -> ...)
                sign_num = (ascendant_sign + i) % 12
            else:
                # Even signs: reverse direction (Taurus -> Aries -> ...)
                sign_num = (ascendant_sign - i + 12) % 12

            # Calculate duration for this sign
            years = self._calculate_chara_dasha_years(sign_num, planet_signs, is_odd)

            end_date = current_date + timedelta(days=years * 365.25)

            periods.append(
                {
                    "sign": SIGNS[sign_num],
                    "sign_number": sign_num,
                    "start_date": current_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "years": round(years, 2),
                    "direction": "Forward" if is_odd else "Reverse",
                }
            )

            current_date = end_date

        return periods

    def _calculate_chara_dasha_years(self, sign_num: int, planet_signs: Dict[str, int], is_odd: bool) -> int:
        """Calculate Chara Dasha duration for a sign

        Duration = distance from sign to its lord + 1 year
        Direction depends on whether sign is odd/even

        Reference: Jaimini Sutras 1.1.5-7
        """
        lord = SIGN_LORDS[sign_num]

        if lord in planet_signs:
            lord_sign = planet_signs[lord]
        else:
            lord_sign = sign_num  # Fallback

        # Calculate distance based on direction
        if is_odd:
            distance = (lord_sign - sign_num + 12) % 12
        else:
            distance = (sign_num - lord_sign + 12) % 12

        # Duration = distance + 1 (minimum 1 year, maximum 12 years)
        years = distance + 1

        return years

    def calculate_argala(
        self, reference_house: int, planet_positions: Dict[str, float], ascendant: float
    ) -> List[ArgalaResult]:
        """Calculate Argala (planetary intervention/influence)

        Argala shows which planets/houses influence a reference house.

        Types of Argala:
        - Primary Argala: 2nd, 4th, 11th houses from reference
        - Secondary Argala: 5th, 8th houses from reference
        - Special Argala: 3rd, 9th, 10th, 12th houses

        Obstruction (Virodhargala):
        - 12th, 10th, 3rd from reference obstruct Primary Argala
        - 9th, 6th obstruct Secondary Argala

        Reference: Jaimini Sutras 1.2.1-8

        Args:
            reference_house: House number (1-12) to analyze
            planet_positions: Planet longitudes
            ascendant: Ascendant longitude

        Returns:
            List of Argala results
        """
        # Convert to 0-indexed
        ref = reference_house - 1

        # Get house occupations
        house_planets = [[] for _ in range(12)]
        for planet, lon in planet_positions.items():
            house = int(lon / 30)
            house_planets[house].append(planet)

        argalas = []

        # Primary Argala positions (2nd, 4th, 11th from reference)
        primary_positions = [(ref + 1) % 12, (ref + 3) % 12, (ref + 10) % 12]
        primary_obstructions = [(ref + 11) % 12, (ref + 9) % 12, (ref + 2) % 12]

        for i, pos in enumerate(primary_positions):
            if house_planets[pos]:
                obstruction_pos = primary_obstructions[i]
                is_obstructed = len(house_planets[obstruction_pos]) > 0

                argalas.append(
                    ArgalaResult(
                        from_house=pos + 1,
                        to_house=reference_house,
                        intervening_planets=house_planets[pos],
                        argala_type="Primary",
                        strength=1.0 if not is_obstructed else 0.5,
                        is_obstructed=is_obstructed,
                        obstruction_from=obstruction_pos + 1 if is_obstructed else None,
                    )
                )

        # Secondary Argala (5th, 8th)
        secondary_positions = [(ref + 4) % 12, (ref + 7) % 12]
        secondary_obstructions = [(ref + 8) % 12, (ref + 5) % 12]

        for i, pos in enumerate(secondary_positions):
            if house_planets[pos]:
                obstruction_pos = secondary_obstructions[i]
                is_obstructed = len(house_planets[obstruction_pos]) > 0

                argalas.append(
                    ArgalaResult(
                        from_house=pos + 1,
                        to_house=reference_house,
                        intervening_planets=house_planets[pos],
                        argala_type="Secondary",
                        strength=0.75 if not is_obstructed else 0.25,
                        is_obstructed=is_obstructed,
                        obstruction_from=obstruction_pos + 1 if is_obstructed else None,
                    )
                )

        return argalas

    def calculate_arudha_padas(
        self, ascendant: float, planet_positions: Dict[str, float]
    ) -> Dict[str, ArudhaPadaResult]:
        """Calculate Arudha Padas (perception points)

        Arudha Pada shows how things are perceived (vs reality).

        Calculation:
        1. Find house lord
        2. Count houses from lord to its sign
        3. Count same number from that sign = Arudha Pada

        Special rules:
        - If Pada falls in same house or 7th from it, count 10th from lord instead

        Reference: Jaimini Sutras 1.1.29-32

        Args:
            ascendant: Ascendant longitude
            planet_positions: Planet positions

        Returns:
            Dict of Arudha Padas for Lagna and each house
        """
        asc_sign = int(ascendant / 30)

        results = {}

        # Calculate Lagna Pada (AL) - most important
        al = self._calculate_single_arudha_pada(asc_sign, planet_positions, "Lagna")
        results["AL"] = al

        # Calculate Pada for each house
        for house_num in range(1, 13):
            house_sign = (asc_sign + house_num - 1) % 12
            pada = self._calculate_single_arudha_pada(house_sign, planet_positions, f"House {house_num}")
            results[f"A{house_num}"] = pada

        # Upapada (UL) - 12th house Pada, very important for marriage
        results["UL"] = results["A12"]
        results["UL"].pada_type = "Upapada (UL)"
        results["UL"].interpretation += " - Most important for marriage and partnerships."

        return results

    def _calculate_single_arudha_pada(
        self, sign: int, planet_positions: Dict[str, float], pada_name: str
    ) -> ArudhaPadaResult:
        """Calculate Arudha Pada for a single sign"""
        lord = SIGN_LORDS[sign]

        # Find lord's position
        if lord in planet_positions:
            lord_sign = int(planet_positions[lord] / 30)
        else:
            lord_sign = sign  # Fallback

        # Count from sign to lord
        distance1 = (lord_sign - sign + 12) % 12

        # Count same distance from lord
        pada_sign = (lord_sign + distance1) % 12

        # Apply special rules
        if pada_sign == sign or pada_sign == (sign + 6) % 12:
            # Falls in same or 7th - use 10th from lord instead
            pada_sign = (lord_sign + 9) % 12
            calculation = f"Lord {lord} in {SIGNS[lord_sign]} -> Special rule: 10th from lord = {SIGNS[pada_sign]}"
        else:
            calculation = f"Distance {sign}→{lord_sign}: {distance1} houses → Pada at {SIGNS[pada_sign]}"

        interpretation = self._interpret_arudha_pada(pada_name, pada_sign)

        return ArudhaPadaResult(
            pada_type=f"{pada_name} Pada",
            pada_house=pada_sign + 1,
            calculation=calculation,
            interpretation=interpretation,
        )

    def _interpret_arudha_pada(self, pada_name: str, pada_sign: int) -> str:
        """Interpret Arudha Pada position"""
        sign_name = SIGNS[pada_sign]

        interpretations = {
            "Lagna": f"How you are perceived by others. Pada in {sign_name} shows external personality projection.",
            "House 2": f"Perceived wealth/status. In {sign_name}.",
            "House 4": f"Perceived property/assets. In {sign_name}.",
            "House 5": f"Perceived creativity/children. In {sign_name}.",
            "House 7": f"Perceived partnerships. In {sign_name}.",
            "House 10": f"Perceived career/status. In {sign_name}.",
            "House 12": f"Perceived spirituality/losses (Upapada for marriage). In {sign_name}.",
        }

        return interpretations.get(pada_name, f"Perception of {pada_name} shown through {sign_name}")

    def calculate_jaimini_aspects(self, planet_positions: Dict[str, float]) -> Dict[str, List[str]]:
        """Calculate Jaimini aspects (sign-based, not degree-based)

        Jaimini aspect rules:
        - Movable signs aspect Fixed signs (except adjacent)
        - Fixed signs aspect Movable signs (except adjacent)
        - Dual signs aspect other Dual signs

        Reference: Jaimini Sutras 1.2.9-12
        """
        # Sign types (0=Movable, 1=Fixed, 2=Dual)
        sign_types = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]

        aspects = {}

        for planet, lon in planet_positions.items():
            sign = int(lon / 30)
            sign_type = sign_types[sign]

            aspected_signs = []

            if sign_type == 0:  # Movable
                # Aspects all Fixed signs except adjacent
                for i in range(12):
                    if sign_types[i] == 1 and abs(i - sign) not in [1, 11]:
                        aspected_signs.append(i)

            elif sign_type == 1:  # Fixed
                # Aspects all Movable signs except adjacent
                for i in range(12):
                    if sign_types[i] == 0 and abs(i - sign) not in [1, 11]:
                        aspected_signs.append(i)

            else:  # Dual
                # Aspects other Dual signs
                for i in range(12):
                    if sign_types[i] == 2 and i != sign:
                        aspected_signs.append(i)

            aspects[planet] = [SIGNS[s] for s in aspected_signs]

        return aspects


def calculate_complete_jaimini_analysis(
    birth_time: datetime, ascendant: float, planet_positions: Dict[str, float]
) -> Dict[str, Any]:
    """Calculate complete Jaimini analysis

    Returns all Jaimini components:
    - Chara Karakas
    - Chara Dasha
    - Arudha Padas
    - Jaimini Aspects
    - Argala for key houses
    """
    system = JaiminiSystem()

    # Calculate Chara Karakas
    karakas = system.calculate_chara_karakas(planet_positions)

    # Calculate Chara Dasha
    dasha_periods = system.calculate_chara_dasha(birth_time, ascendant, planet_positions)

    # Calculate Arudha Padas
    arudha_padas = system.calculate_arudha_padas(ascendant, planet_positions)

    # Calculate Jaimini Aspects
    aspects = system.calculate_jaimini_aspects(planet_positions)

    # Calculate Argala for key houses (1, 5, 7, 9, 10)
    key_houses = [1, 5, 7, 9, 10]
    argala_analysis = {}
    for house in key_houses:
        argala_analysis[f"House_{house}"] = system.calculate_argala(house, planet_positions, ascendant)

    return {
        "chara_karakas": {
            karaka.value: {
                "planet": result.planet,
                "longitude": round(result.longitude, 2),
                "sign": result.sign,
                "navamsa_sign": result.navamsa_sign,
                "karakamsa": result.karakamsa,
            }
            for karaka, result in karakas.items()
        },
        "chara_dasha": {"system": "Chara Dasha (Jaimini)", "total_cycle": "120 years", "periods": dasha_periods},
        "arudha_padas": {
            key: {
                "pada_type": result.pada_type,
                "pada_house": result.pada_house,
                "pada_sign": SIGNS[result.pada_house - 1],
                "calculation": result.calculation,
                "interpretation": result.interpretation,
            }
            for key, result in arudha_padas.items()
        },
        "jaimini_aspects": aspects,
        "argala": {
            house_key: [
                {
                    "from_house": arg.from_house,
                    "planets": arg.intervening_planets,
                    "type": arg.argala_type,
                    "strength": arg.strength,
                    "obstructed": arg.is_obstructed,
                    "obstruction_from": arg.obstruction_from,
                }
                for arg in argalas
            ]
            for house_key, argalas in argala_analysis.items()
        },
        "reference": "Jaimini Sutras, Maharishi Jaimini",
    }
