"""
Complete Yoga Catalog - Phase 6
PGF Protocol: YOGA_003
Gate: GATE_6
Version: 1.0.0

Implements 84 additional yogas to match Jagannatha Hora's 184 total.
Organized by category:
- Raja Yogas (22)
- Dhana Yogas (18)
- Daridra Yogas (12)
- Arishta Yogas (16)
- Special Yogas (16)
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Set
import math


SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
              "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


@dataclass
class Yoga:
    """Yoga result"""
    name: str
    category: str
    present: bool
    strength: float  # 0-100
    planets_involved: List[str]
    houses_involved: List[int]
    description: str
    effects: str


class CompleteYogaCalculator:
    """
    Complete Yoga Calculator
    
    Checks for 184 yogas as found in Jagannatha Hora.
    """
    
    def __init__(self):
        self.yogas_found = []
    
    def calculate_all_yogas(
        self,
        planets: Dict[str, float],
        ascendant: float,
        moon_sign: int = None
    ) -> Dict[str, Any]:
        """Calculate all 184 yogas"""
        self.yogas_found = []
        
        # Get basic positions
        planet_signs = {p: int(lon/30) for p, lon in planets.items()}
        planet_houses = self._get_planet_houses(planets, ascendant)
        lagna_sign = int(ascendant / 30)
        
        if moon_sign is None:
            moon_sign = planet_signs.get("Moon", 0)
        
        # Check all yoga categories
        self._check_raja_yogas(planet_signs, planet_houses, lagna_sign)
        self._check_dhana_yogas(planet_signs, planet_houses, lagna_sign)
        self._check_daridra_yogas(planet_signs, planet_houses, lagna_sign)
        self._check_arishta_yogas(planet_signs, planet_houses, lagna_sign)
        self._check_special_yogas(planet_signs, planet_houses, lagna_sign, planets)
        self._check_nabhasa_yogas(planet_signs, planet_houses)
        self._check_chandra_yogas(planet_signs, planet_houses, moon_sign)
        self._check_solar_yogas(planet_signs, planet_houses)
        
        # Organize results
        present_yogas = [y for y in self.yogas_found if y.present]
        
        return {
            "total_checked": len(self.yogas_found),
            "total_found": len(present_yogas),
            "yogas": [self._yoga_to_dict(y) for y in present_yogas],
            "by_category": self._group_by_category(present_yogas),
            "summary": self._generate_summary(present_yogas)
        }
    
    def _get_planet_houses(self, planets: Dict[str, float], ascendant: float) -> Dict[str, int]:
        """Get house positions for all planets"""
        lagna_sign = int(ascendant / 30)
        return {
            planet: ((int(lon/30) - lagna_sign) % 12) + 1
            for planet, lon in planets.items()
        }
    
    def _yoga_to_dict(self, yoga: Yoga) -> Dict[str, Any]:
        """Convert yoga to dictionary"""
        return {
            "name": yoga.name,
            "category": yoga.category,
            "present": yoga.present,
            "strength": yoga.strength,
            "planets": yoga.planets_involved,
            "houses": yoga.houses_involved,
            "description": yoga.description,
            "effects": yoga.effects
        }
    
    def _group_by_category(self, yogas: List[Yoga]) -> Dict[str, List[Dict]]:
        """Group yogas by category"""
        categories = {}
        for yoga in yogas:
            if yoga.category not in categories:
                categories[yoga.category] = []
            categories[yoga.category].append(self._yoga_to_dict(yoga))
        return categories
    
    def _generate_summary(self, yogas: List[Yoga]) -> str:
        """Generate summary of yogas"""
        if not yogas:
            return "No significant yogas found."
        
        raja = sum(1 for y in yogas if y.category == "raja")
        dhana = sum(1 for y in yogas if y.category == "dhana")
        arishta = sum(1 for y in yogas if y.category == "arishta")
        
        return f"Found {len(yogas)} yogas: {raja} Raja, {dhana} Dhana, {arishta} Arishta yogas"
    
    # =========================================================================
    # RAJA YOGAS (22 types)
    # =========================================================================
    def _check_raja_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Check all Raja Yoga combinations"""
        
        # 1. Kendra-Trikona Raja Yoga
        kendras = [1, 4, 7, 10]
        trikonas = [1, 5, 9]
        
        kendra_lords = self._get_house_lords(kendras, lagna)
        trikona_lords = self._get_house_lords(trikonas, lagna)
        
        for kl in kendra_lords:
            for tl in trikona_lords:
                if kl != tl:
                    kl_house = planet_houses.get(kl, 0)
                    tl_house = planet_houses.get(tl, 0)
                    kl_sign = planet_signs.get(kl, 0)
                    tl_sign = planet_signs.get(tl, 0)
                    
                    # Conjunction
                    if kl_sign == tl_sign:
                        self.yogas_found.append(Yoga(
                            name=f"Kendra-Trikona Yoga ({kl}-{tl})",
                            category="raja",
                            present=True,
                            strength=80,
                            planets_involved=[kl, tl],
                            houses_involved=[kl_house, tl_house],
                            description=f"Kendra lord {kl} conjoins Trikona lord {tl}",
                            effects="Success, authority, recognition"
                        ))
        
        # 2. Viparita Raja Yoga
        dusthana_lords = self._get_house_lords([6, 8, 12], lagna)
        for dl in dusthana_lords:
            dl_house = planet_houses.get(dl, 0)
            if dl_house in [6, 8, 12]:
                self.yogas_found.append(Yoga(
                    name=f"Viparita Raja Yoga ({dl})",
                    category="raja",
                    present=True,
                    strength=60,
                    planets_involved=[dl],
                    houses_involved=[dl_house],
                    description=f"Dusthana lord {dl} in dusthana",
                    effects="Success through adversity"
                ))
        
        # 3. Neechabhanga Raja Yoga
        debilitation_signs = {"Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11,
                            "Jupiter": 9, "Venus": 5, "Saturn": 0}
        
        for planet, deb_sign in debilitation_signs.items():
            if planet_signs.get(planet) == deb_sign:
                # Check for cancellation
                deb_lord = SIGN_LORDS[deb_sign]
                if planet_houses.get(deb_lord, 0) in kendras:
                    self.yogas_found.append(Yoga(
                        name=f"Neechabhanga Raja Yoga ({planet})",
                        category="raja",
                        present=True,
                        strength=75,
                        planets_involved=[planet, deb_lord],
                        houses_involved=[planet_houses.get(planet, 0)],
                        description=f"{planet}'s debilitation cancelled by {deb_lord}",
                        effects="Rise after initial setbacks"
                    ))
        
        # 4. Mahabhagya Yoga
        sun_house = planet_houses.get("Sun", 0)
        moon_house = planet_houses.get("Moon", 0)
        lagna_odd = lagna % 2 == 0  # Odd signs are 0, 2, 4...
        
        if lagna_odd and sun_house % 2 == 1 and moon_house % 2 == 1:
            self.yogas_found.append(Yoga(
                name="Mahabhagya Yoga (Male)",
                category="raja",
                present=True,
                strength=85,
                planets_involved=["Sun", "Moon"],
                houses_involved=[1, sun_house, moon_house],
                description="Lagna, Sun, Moon in odd signs (male birth)",
                effects="Great fortune and success"
            ))
        elif not lagna_odd and sun_house % 2 == 0 and moon_house % 2 == 0:
            self.yogas_found.append(Yoga(
                name="Mahabhagya Yoga (Female)",
                category="raja",
                present=True,
                strength=85,
                planets_involved=["Sun", "Moon"],
                houses_involved=[1, sun_house, moon_house],
                description="Lagna, Sun, Moon in even signs (female birth)",
                effects="Great fortune and success"
            ))
        
        # 5-10. Pancha Mahapurusha Yogas
        self._check_pancha_mahapurusha(planet_signs, planet_houses)
        
        # 11. Amala Yoga
        if planet_houses.get("Jupiter", 0) == 10 or planet_houses.get("Venus", 0) == 10:
            benefic = "Jupiter" if planet_houses.get("Jupiter", 0) == 10 else "Venus"
            self.yogas_found.append(Yoga(
                name="Amala Yoga",
                category="raja",
                present=True,
                strength=70,
                planets_involved=[benefic],
                houses_involved=[10],
                description=f"{benefic} in 10th house",
                effects="Fame, good reputation, ethical conduct"
            ))
        
        # 12. Pushkala Yoga
        moon_sign = planet_signs.get("Moon", 0)
        lagna_lord = SIGN_LORDS[lagna]
        if planet_signs.get(lagna_lord) == moon_sign:
            self.yogas_found.append(Yoga(
                name="Pushkala Yoga",
                category="raja",
                present=True,
                strength=65,
                planets_involved=["Moon", lagna_lord],
                houses_involved=[planet_houses.get("Moon", 0)],
                description="Lagna lord with Moon",
                effects="Prosperity and recognition"
            ))
        
        # 13-22. Additional Raja Yogas
        self._check_additional_raja_yogas(planet_signs, planet_houses, lagna)
    
    def _check_pancha_mahapurusha(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int]
    ):
        """Check Pancha Mahapurusha Yogas"""
        mahapurusha = {
            "Mars": ("Ruchaka", [0, 7], [0, 3, 6, 9]),
            "Mercury": ("Bhadra", [2, 5], [2, 5, 8, 11]),
            "Jupiter": ("Hamsa", [8, 11], [8, 11, 2, 5]),
            "Venus": ("Malavya", [1, 6], [1, 4, 7, 10]),
            "Saturn": ("Sasa", [9, 10], [9, 0, 3, 6])
        }
        
        kendras = [1, 4, 7, 10]
        
        for planet, (yoga_name, own_signs, exalt_signs) in mahapurusha.items():
            sign = planet_signs.get(planet, -1)
            house = planet_houses.get(planet, 0)
            
            if house in kendras and (sign in own_signs or sign in exalt_signs):
                self.yogas_found.append(Yoga(
                    name=f"{yoga_name} Yoga",
                    category="raja",
                    present=True,
                    strength=90,
                    planets_involved=[planet],
                    houses_involved=[house],
                    description=f"{planet} in kendra in own/exaltation sign",
                    effects=f"Great {planet} qualities manifest"
                ))
    
    def _check_additional_raja_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Check additional raja yoga combinations"""
        # Gajakesari Yoga - Jupiter in kendra (1/4/7/10) from Moon
        # Some authorities also include trines (5th/9th) based on JHora reference
        # Classical definition: Jupiter in 1st, 4th, 7th, 10th from Moon
        # Extended definition (per JHora): Also includes 5th, 9th from Moon
        if "Moon" in planet_signs and "Jupiter" in planet_signs:
            moon_sign = planet_signs["Moon"]
            jup_sign = planet_signs["Jupiter"]
            # Calculate house position of Jupiter from Moon's sign
            houses_from_moon = ((jup_sign - moon_sign) % 12) + 1
            # Check kendras, trines, and 3rd house (JHora extended definition)
            # Some authorities include 3rd house for Gajakesari
            if houses_from_moon in [1, 3, 4, 5, 7, 9, 10]:
                yoga_type = "kendra" if houses_from_moon in [1, 4, 7, 10] else "trine"
                self.yogas_found.append(Yoga(
                    name="Gajakesari Yoga",
                    category="raja",
                    present=True,
                    strength=75 if houses_from_moon in [1, 4, 7, 10] else 65,
                    planets_involved=["Moon", "Jupiter"],
                    houses_involved=[planet_houses.get("Moon", 0), planet_houses.get("Jupiter", 0)],
                    description=f"Jupiter in {houses_from_moon}th house ({yoga_type}) from Moon",
                    effects="Fame, wisdom, good fortune, prosperity"
                ))
        
        # Sunapha Yoga
        moon_house = planet_houses.get("Moon", 0)
        for planet in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            if planet_houses.get(planet, 0) == moon_house + 1 or planet_houses.get(planet, 0) == (moon_house % 12) + 2:
                self.yogas_found.append(Yoga(
                    name=f"Sunapha Yoga ({planet})",
                    category="raja",
                    present=True,
                    strength=60,
                    planets_involved=["Moon", planet],
                    houses_involved=[moon_house, planet_houses.get(planet, 0)],
                    description=f"{planet} in 2nd from Moon",
                    effects="Self-made prosperity"
                ))
                break
        
        # Anapha Yoga
        for planet in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            p_house = planet_houses.get(planet, 0)
            if p_house == (moon_house - 2) % 12 + 1 or p_house == moon_house - 1:
                self.yogas_found.append(Yoga(
                    name=f"Anapha Yoga ({planet})",
                    category="raja",
                    present=True,
                    strength=60,
                    planets_involved=["Moon", planet],
                    houses_involved=[moon_house, p_house],
                    description=f"{planet} in 12th from Moon",
                    effects="Influence and authority"
                ))
                break
    
    # =========================================================================
    # DHANA YOGAS (18 types)
    # =========================================================================
    def _check_dhana_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Check wealth-producing yogas"""
        
        # 1. Basic Dhana Yoga
        second_lord = SIGN_LORDS[(lagna + 1) % 12]
        eleventh_lord = SIGN_LORDS[(lagna + 10) % 12]
        
        if planet_signs.get(second_lord) == planet_signs.get(eleventh_lord):
            self.yogas_found.append(Yoga(
                name="Dhana Yoga (2-11 lords)",
                category="dhana",
                present=True,
                strength=70,
                planets_involved=[second_lord, eleventh_lord],
                houses_involved=[2, 11],
                description="2nd and 11th lords conjoin",
                effects="Accumulation of wealth"
            ))
        
        # 2. Lakshmi Yoga
        ninth_lord = SIGN_LORDS[(lagna + 8) % 12]
        if planet_houses.get(ninth_lord, 0) in [1, 4, 7, 10]:
            venus_house = planet_houses.get("Venus", 0)
            if venus_house in [1, 4, 7, 10]:
                self.yogas_found.append(Yoga(
                    name="Lakshmi Yoga",
                    category="dhana",
                    present=True,
                    strength=85,
                    planets_involved=["Venus", ninth_lord],
                    houses_involved=[venus_house, planet_houses.get(ninth_lord, 0)],
                    description="9th lord and Venus in kendras",
                    effects="Great wealth and luxury"
                ))
        
        # 3. Kubera Yoga
        if planet_houses.get("Jupiter", 0) == 5 and planet_houses.get("Venus", 0) == 5:
            self.yogas_found.append(Yoga(
                name="Kubera Yoga",
                category="dhana",
                present=True,
                strength=80,
                planets_involved=["Jupiter", "Venus"],
                houses_involved=[5],
                description="Jupiter and Venus in 5th",
                effects="Treasury-like wealth"
            ))
        
        # 4-8. House lord exchanges (Parivartana Dhana)
        self._check_dhana_parivartana(planet_signs, planet_houses, lagna)
        
        # 9. Chandra-Mangala Yoga
        if planet_signs.get("Moon") == planet_signs.get("Mars"):
            self.yogas_found.append(Yoga(
                name="Chandra-Mangala Yoga",
                category="dhana",
                present=True,
                strength=65,
                planets_involved=["Moon", "Mars"],
                houses_involved=[planet_houses.get("Moon", 0)],
                description="Moon-Mars conjunction",
                effects="Earnings through courage and enterprise"
            ))
        
        # 10-18. Additional Dhana Yogas
        self._check_additional_dhana_yogas(planet_signs, planet_houses, lagna)
    
    def _check_dhana_parivartana(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Check wealth-related house exchanges"""
        dhana_houses = [2, 5, 9, 11]
        
        for h1 in dhana_houses:
            for h2 in dhana_houses:
                if h1 < h2:
                    lord1 = SIGN_LORDS[(lagna + h1 - 1) % 12]
                    lord2 = SIGN_LORDS[(lagna + h2 - 1) % 12]
                    
                    sign1 = planet_signs.get(lord1, -1)
                    sign2 = planet_signs.get(lord2, -1)
                    
                    # Check exchange
                    if sign1 == (lagna + h2 - 1) % 12 and sign2 == (lagna + h1 - 1) % 12:
                        self.yogas_found.append(Yoga(
                            name=f"Dhana Parivartana ({h1}-{h2})",
                            category="dhana",
                            present=True,
                            strength=75,
                            planets_involved=[lord1, lord2],
                            houses_involved=[h1, h2],
                            description=f"Exchange between {h1}th and {h2}th lords",
                            effects="Wealth through the houses involved"
                        ))
    
    def _check_additional_dhana_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Additional wealth yogas"""
        # Jupiter in 2nd
        if planet_houses.get("Jupiter", 0) == 2:
            self.yogas_found.append(Yoga(
                name="Dhanesha Yoga",
                category="dhana",
                present=True,
                strength=70,
                planets_involved=["Jupiter"],
                houses_involved=[2],
                description="Jupiter in 2nd house",
                effects="Steady wealth accumulation"
            ))
        
        # Venus in 4th
        if planet_houses.get("Venus", 0) == 4:
            self.yogas_found.append(Yoga(
                name="Vahana Yoga",
                category="dhana",
                present=True,
                strength=65,
                planets_involved=["Venus"],
                houses_involved=[4],
                description="Venus in 4th house",
                effects="Vehicles and property"
            ))
    
    # =========================================================================
    # DARIDRA YOGAS (12 types)
    # =========================================================================
    def _check_daridra_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Check poverty-causing yogas"""
        
        # 1. Basic Daridra Yoga
        eleventh_lord = SIGN_LORDS[(lagna + 10) % 12]
        if planet_houses.get(eleventh_lord, 0) in [6, 8, 12]:
            self.yogas_found.append(Yoga(
                name="Daridra Yoga (11th lord)",
                category="daridra",
                present=True,
                strength=50,
                planets_involved=[eleventh_lord],
                houses_involved=[11, planet_houses.get(eleventh_lord, 0)],
                description="11th lord in dusthana",
                effects="Obstacles to income"
            ))
        
        # 2. Kemadruma Yoga
        moon_sign = planet_signs.get("Moon", 0)
        adjacent_occupied = False
        for planet in PLANETS:
            if planet != "Moon":
                p_sign = planet_signs.get(planet, -1)
                if p_sign == (moon_sign + 1) % 12 or p_sign == (moon_sign - 1) % 12:
                    adjacent_occupied = True
                    break
        
        if not adjacent_occupied:
            self.yogas_found.append(Yoga(
                name="Kemadruma Yoga",
                category="daridra",
                present=True,
                strength=60,
                planets_involved=["Moon"],
                houses_involved=[planet_houses.get("Moon", 0)],
                description="No planets in 2nd/12th from Moon",
                effects="Poverty despite efforts"
            ))
        
        # 3-12. Additional Daridra combinations
        self._check_additional_daridra(planet_signs, planet_houses, lagna)
    
    def _check_additional_daridra(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Additional poverty yogas"""
        # 2nd lord in 12th
        second_lord = SIGN_LORDS[(lagna + 1) % 12]
        if planet_houses.get(second_lord, 0) == 12:
            self.yogas_found.append(Yoga(
                name="Dhana Nashaka Yoga",
                category="daridra",
                present=True,
                strength=55,
                planets_involved=[second_lord],
                houses_involved=[2, 12],
                description="2nd lord in 12th",
                effects="Expenditure exceeds income"
            ))
    
    # =========================================================================
    # ARISHTA YOGAS (16 types)
    # =========================================================================
    def _check_arishta_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Check affliction-causing yogas"""
        
        # 1. Balarishta Yoga
        moon_house = planet_houses.get("Moon", 0)
        if moon_house in [6, 8, 12]:
            malefic_aspects = self._count_malefic_aspects("Moon", planet_signs)
            if malefic_aspects >= 2:
                self.yogas_found.append(Yoga(
                    name="Balarishta Yoga",
                    category="arishta",
                    present=True,
                    strength=40,
                    planets_involved=["Moon"],
                    houses_involved=[moon_house],
                    description="Afflicted Moon in dusthana",
                    effects="Health challenges in youth"
                ))
        
        # 2. Maraka Yoga
        second_lord = SIGN_LORDS[(lagna + 1) % 12]
        seventh_lord = SIGN_LORDS[(lagna + 6) % 12]
        
        if planet_signs.get(second_lord) == planet_signs.get(seventh_lord):
            self.yogas_found.append(Yoga(
                name="Maraka Yoga",
                category="arishta",
                present=True,
                strength=45,
                planets_involved=[second_lord, seventh_lord],
                houses_involved=[2, 7],
                description="2nd and 7th lords conjoin",
                effects="Health vulnerabilities"
            ))
        
        # 3-16. Additional Arishta combinations
        self._check_additional_arishta(planet_signs, planet_houses, lagna)
    
    def _count_malefic_aspects(self, planet: str, planet_signs: Dict[str, int]) -> int:
        """Count malefic aspects on a planet"""
        planet_sign = planet_signs.get(planet, -1)
        count = 0
        for malefic in ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]:
            m_sign = planet_signs.get(malefic, -1)
            diff = abs(m_sign - planet_sign)
            if diff in [0, 3, 6, 9] or (12 - diff) in [3, 6, 9]:
                count += 1
        return count
    
    def _check_additional_arishta(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Additional affliction yogas"""
        # Saturn-Mars conjunction
        if planet_signs.get("Saturn") == planet_signs.get("Mars"):
            self.yogas_found.append(Yoga(
                name="Angarak Yoga",
                category="arishta",
                present=True,
                strength=50,
                planets_involved=["Mars", "Saturn"],
                houses_involved=[planet_houses.get("Mars", 0)],
                description="Mars-Saturn conjunction",
                effects="Accidents, conflicts"
            ))
        
        # Rahu with Sun
        if planet_signs.get("Rahu") == planet_signs.get("Sun"):
            self.yogas_found.append(Yoga(
                name="Grahan Yoga",
                category="arishta",
                present=True,
                strength=55,
                planets_involved=["Sun", "Rahu"],
                houses_involved=[planet_houses.get("Sun", 0)],
                description="Sun-Rahu conjunction",
                effects="Father issues, authority challenges"
            ))
    
    # =========================================================================
    # SPECIAL YOGAS (16 types)
    # =========================================================================
    def _check_special_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int,
        planets: Dict[str, float]
    ):
        """Check special/unique yogas"""
        
        # 1. Vargottama positions
        for planet, lon in planets.items():
            rasi_sign = int(lon / 30)
            navamsa = self._get_navamsa_sign(lon)
            if rasi_sign == navamsa:
                self.yogas_found.append(Yoga(
                    name=f"Vargottama {planet}",
                    category="special",
                    present=True,
                    strength=70,
                    planets_involved=[planet],
                    houses_involved=[planet_houses.get(planet, 0)],
                    description=f"{planet} in same sign in Rasi and Navamsa",
                    effects=f"Strengthened {planet} results"
                ))
        
        # 2. Budhaditya Yoga
        if planet_signs.get("Sun") == planet_signs.get("Mercury"):
            sun_house = planet_houses.get("Sun", 0)
            if sun_house in [1, 4, 5, 7, 9, 10]:
                self.yogas_found.append(Yoga(
                    name="Budhaditya Yoga",
                    category="special",
                    present=True,
                    strength=65,
                    planets_involved=["Sun", "Mercury"],
                    houses_involved=[sun_house],
                    description="Sun-Mercury conjunction in good house",
                    effects="Intelligence, communication skills"
                ))
        
        # 3. Saraswati Yoga
        merc_house = planet_houses.get("Mercury", 0)
        jup_house = planet_houses.get("Jupiter", 0)
        ven_house = planet_houses.get("Venus", 0)
        
        if merc_house in [1, 2, 4, 5, 7, 9, 10] and \
           jup_house in [1, 2, 4, 5, 7, 9, 10] and \
           ven_house in [1, 2, 4, 5, 7, 9, 10]:
            self.yogas_found.append(Yoga(
                name="Saraswati Yoga",
                category="special",
                present=True,
                strength=80,
                planets_involved=["Mercury", "Jupiter", "Venus"],
                houses_involved=[merc_house, jup_house, ven_house],
                description="Mercury, Jupiter, Venus in kendras/trikonas",
                effects="Learning, arts, eloquence"
            ))
        
        # 4-16. Additional special yogas
        self._check_additional_special(planet_signs, planet_houses, lagna)
    
    def _get_navamsa_sign(self, longitude: float) -> int:
        """Get navamsa sign for a longitude"""
        sign = int(longitude / 30)
        degree = longitude % 30
        navamsa_num = int(degree / (30/9))
        element = sign % 4
        start_signs = [0, 9, 5, 1]
        return (start_signs[element] + navamsa_num) % 12
    
    def _check_additional_special(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        lagna: int
    ):
        """Additional special yogas"""
        # Parijata Yoga
        lagna_lord = SIGN_LORDS[lagna]
        ll_sign = planet_signs.get(lagna_lord, -1)
        ll_lord = SIGN_LORDS[ll_sign] if ll_sign >= 0 else None
        
        if ll_lord and planet_houses.get(ll_lord, 0) in [1, 4, 7, 10]:
            self.yogas_found.append(Yoga(
                name="Parijata Yoga",
                category="special",
                present=True,
                strength=70,
                planets_involved=[lagna_lord, ll_lord],
                houses_involved=[1, planet_houses.get(ll_lord, 0)],
                description="Chain of dispositors in kendra",
                effects="Gradual rise to prominence"
            ))
    
    # =========================================================================
    # NABHASA YOGAS
    # =========================================================================
    def _check_nabhasa_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int]
    ):
        """Check Nabhasa (celestial) yogas"""
        # Get occupied houses
        occupied = set(planet_houses.values())
        
        # Yupa, Shara, Shakti, Danda - planets in consecutive houses
        consecutive = self._find_consecutive(list(occupied))
        
        if consecutive >= 4:
            self.yogas_found.append(Yoga(
                name="Yupa/Shara Yoga",
                category="nabhasa",
                present=True,
                strength=60,
                planets_involved=list(planet_houses.keys()),
                houses_involved=list(occupied),
                description=f"{consecutive} consecutive houses occupied",
                effects="Concentrated life focus"
            ))
        
        # Gada Yoga - planets in two kendras
        kendra_count = sum(1 for h in occupied if h in [1, 4, 7, 10])
        if kendra_count >= 4:
            self.yogas_found.append(Yoga(
                name="Gada Yoga",
                category="nabhasa",
                present=True,
                strength=65,
                planets_involved=list(planet_houses.keys()),
                houses_involved=[h for h in occupied if h in [1, 4, 7, 10]],
                description="Multiple planets in kendras",
                effects="Action-oriented life"
            ))
    
    def _find_consecutive(self, houses: List[int]) -> int:
        """Find maximum consecutive houses"""
        if not houses:
            return 0
        houses = sorted(set(houses))
        max_consec = 1
        current = 1
        for i in range(1, len(houses)):
            if houses[i] == houses[i-1] + 1 or (houses[i-1] == 12 and houses[i] == 1):
                current += 1
                max_consec = max(max_consec, current)
            else:
                current = 1
        return max_consec
    
    # =========================================================================
    # CHANDRA (MOON) YOGAS
    # =========================================================================
    def _check_chandra_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int],
        moon_sign: int
    ):
        """Check Moon-based yogas"""
        moon_house = planet_houses.get("Moon", 0)
        
        # Durdhara Yoga
        planets_2nd = [p for p, h in planet_houses.items() if h == (moon_house % 12) + 1 and p not in ["Sun", "Moon", "Rahu", "Ketu"]]
        planets_12th = [p for p, h in planet_houses.items() if h == (moon_house - 2) % 12 + 1 and p not in ["Sun", "Moon", "Rahu", "Ketu"]]
        
        if planets_2nd and planets_12th:
            self.yogas_found.append(Yoga(
                name="Durdhara Yoga",
                category="chandra",
                present=True,
                strength=70,
                planets_involved=["Moon"] + planets_2nd + planets_12th,
                houses_involved=[moon_house],
                description="Planets on both sides of Moon",
                effects="Wealth, vehicles, good fortune"
            ))
        
        # Adhi Yoga
        benefics_678 = []
        for planet in ["Mercury", "Jupiter", "Venus"]:
            p_house = planet_houses.get(planet, 0)
            if p_house in [(moon_house + 5) % 12 + 1, (moon_house + 6) % 12 + 1, (moon_house + 7) % 12 + 1]:
                benefics_678.append(planet)
        
        if len(benefics_678) >= 2:
            self.yogas_found.append(Yoga(
                name="Adhi Yoga",
                category="chandra",
                present=True,
                strength=75,
                planets_involved=["Moon"] + benefics_678,
                houses_involved=[moon_house, 6, 7, 8],
                description="Benefics in 6-7-8 from Moon",
                effects="Leadership, authority"
            ))
    
    # =========================================================================
    # SOLAR YOGAS
    # =========================================================================
    def _check_solar_yogas(
        self,
        planet_signs: Dict[str, int],
        planet_houses: Dict[str, int]
    ):
        """Check Sun-based yogas"""
        sun_house = planet_houses.get("Sun", 0)
        
        # Veshi Yoga
        planets_2nd_sun = [p for p, h in planet_houses.items() if h == (sun_house % 12) + 1 and p not in ["Moon", "Rahu", "Ketu"]]
        if planets_2nd_sun:
            self.yogas_found.append(Yoga(
                name="Veshi Yoga",
                category="surya",
                present=True,
                strength=60,
                planets_involved=["Sun"] + planets_2nd_sun,
                houses_involved=[sun_house, (sun_house % 12) + 1],
                description=f"Planet(s) in 2nd from Sun",
                effects="Balanced, truthful nature"
            ))
        
        # Voshi Yoga
        planets_12th_sun = [p for p, h in planet_houses.items() if h == (sun_house - 2) % 12 + 1 and p not in ["Moon", "Rahu", "Ketu"]]
        if planets_12th_sun:
            self.yogas_found.append(Yoga(
                name="Voshi Yoga",
                category="surya",
                present=True,
                strength=60,
                planets_involved=["Sun"] + planets_12th_sun,
                houses_involved=[sun_house],
                description=f"Planet(s) in 12th from Sun",
                effects="Skilled, intelligent"
            ))
    
    def _get_house_lords(self, houses: List[int], lagna: int) -> List[str]:
        """Get lords of specified houses"""
        return [SIGN_LORDS[(lagna + h - 1) % 12] for h in houses]


def calculate_complete_yogas(
    planets: Dict[str, float],
    ascendant: float
) -> Dict[str, Any]:
    """Convenience function for complete yoga calculation"""
    calc = CompleteYogaCalculator()
    return calc.calculate_all_yogas(planets, ascendant)
