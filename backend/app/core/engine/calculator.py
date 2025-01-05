from datetime import datetime
from typing import List, Dict, Any
import swisseph as swe
from app.models.kundli import (
    KundliRequest,
    KundliChart,
    Planet,
    House,
    ChartType,
    AyanamsaType,
    HouseSystem,
)

class KundliCalculator:
    PLANETS = {
        swe.SUN: "Sun",
        swe.MOON: "Moon",
        swe.MARS: "Mars",
        swe.MERCURY: "Mercury",
        swe.JUPITER: "Jupiter",
        swe.VENUS: "Venus",
        swe.SATURN: "Saturn",
        swe.URANUS: "Uranus",
        swe.NEPTUNE: "Neptune",
        swe.PLUTO: "Pluto",
        swe.MEAN_NODE: "Rahu",  # North Node
    }

    SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    NAKSHATRAS = [
        "Ashwini", "Bharani", "Krittika", "Rohini",
        "Mrigashira", "Ardra", "Punarvasu", "Pushya",
        "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha",
        "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
        "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]

    def __init__(self):
        swe.set_ephe_path("/path/to/ephemeris")  # Set path to ephemeris files

    def _set_ayanamsa(self, ayanamsa: AyanamsaType):
        ayanamsa_map = {
            AyanamsaType.LAHIRI: swe.SIDM_LAHIRI,
            AyanamsaType.RAMAN: swe.SIDM_RAMAN,
            AyanamsaType.KP: swe.SIDM_KRISHNAMURTI,
            AyanamsaType.TROPICAL: swe.SIDM_FAGAN_BRADLEY,
        }
        swe.set_sid_mode(ayanamsa_map[ayanamsa])

    def _get_julian_day(self, date: datetime) -> float:
        return swe.julday(
            date.year,
            date.month,
            date.day,
            date.hour + date.minute / 60.0 + date.second / 3600.0
        )

    def _calculate_houses(
        self, jd: float, lat: float, lon: float, house_system: HouseSystem
    ) -> List[House]:
        system_map = {
            HouseSystem.PLACIDUS: b'P',
            HouseSystem.KOCH: b'K',
            HouseSystem.EQUAL: b'E',
            HouseSystem.WHOLE_SIGN: b'W',
        }

        cusps, ascmc = swe.houses(
            jd, lat, lon, system_map[house_system]
        )

        houses = []
        for i in range(12):
            house_num = i + 1
            degree = cusps[i]
            sign_num = int(degree / 30)
            houses.append(
                House(
                    number=house_num,
                    sign=self.SIGNS[sign_num],
                    degree=degree % 30,
                    planets=[],
                )
            )
        return houses

    def _calculate_planets(self, jd: float) -> List[Planet]:
        planets = []
        for planet_id, planet_name in self.PLANETS.items():
            try:
                calc = swe.calc_ut(jd, planet_id)
                longitude = calc[0][0]
                latitude = calc[0][1]
                speed = calc[0][3]

                # Calculate sign and house
                sign_num = int(longitude / 30)
                house_num = (sign_num % 12) + 1

                # Calculate nakshatra
                nakshatra_deg = longitude % 360
                nakshatra_num = int(nakshatra_deg / (360 / 27))
                nakshatra_pada = int((nakshatra_deg % (360 / 27)) / (360 / 108)) + 1

                planet = Planet(
                    name=planet_name,
                    longitude=longitude,
                    latitude=latitude,
                    speed=speed,
                    house=house_num,
                    sign=self.SIGNS[sign_num],
                    nakshatra=self.NAKSHATRAS[nakshatra_num],
                    nakshatra_pada=nakshatra_pada,
                    is_retrograde=speed < 0,
                )
                planets.append(planet)
            except swe.Error:
                continue

        return planets

    def calculate_chart(
        self, request: KundliRequest, chart_type: ChartType
    ) -> KundliChart:
        # Set ayanamsa
        self._set_ayanamsa(request.ayanamsa)

        # Calculate Julian day
        jd = self._get_julian_day(request.date)

        # Calculate houses
        houses = self._calculate_houses(
            jd, request.latitude, request.longitude, request.house_system
        )

        # Calculate planets
        planets = self._calculate_planets(jd)

        # Update house.planets list
        for planet in planets:
            house_idx = planet.house - 1
            houses[house_idx].planets.append(planet.name)

        # Apply divisional chart calculations if needed
        if chart_type != ChartType.RASI:
            planets = self._apply_divisional_chart(planets, chart_type)

        return KundliChart(
            type=chart_type,
            houses=houses,
            planets=planets,
        )

    def _apply_divisional_chart(
        self, planets: List[Planet], chart_type: ChartType
    ) -> List[Planet]:
        # Implement divisional chart calculations
        # This is a simplified version
        division_factor = {
            ChartType.NAVAMSA: 9,
            ChartType.DASHAMSA: 10,
        }.get(chart_type, 1)

        if division_factor == 1:
            return planets

        modified_planets = []
        for planet in planets:
            # Calculate divisional longitude
            div_longitude = (planet.longitude * division_factor) % 360
            sign_num = int(div_longitude / 30)
            house_num = (sign_num % 12) + 1

            # Create new planet with modified position
            modified_planet = Planet(
                name=planet.name,
                longitude=div_longitude,
                latitude=planet.latitude,
                speed=planet.speed,
                house=house_num,
                sign=self.SIGNS[sign_num],
                nakshatra=planet.nakshatra,
                nakshatra_pada=planet.nakshatra_pada,
                is_retrograde=planet.is_retrograde,
            )
            modified_planets.append(modified_planet)

        return modified_planets

    def calculate_all_charts(self, request: KundliRequest) -> List[KundliChart]:
        return [
            self.calculate_chart(request, chart_type)
            for chart_type in request.chart_types
        ]
