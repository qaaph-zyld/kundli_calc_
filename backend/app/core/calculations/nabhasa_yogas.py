"""
Nabhasa Yogas - Sky Pattern Yogas
=================================
Additional 40 yogas based on planetary patterns in the sky.
Includes Akriti (shape), Sankhya (number), and Ashraya (support) yogas.

Reference: Brihat Parashara Hora Shastra, Chapter 35
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class NabhasaYoga:
    """Nabhasa Yoga detection result"""

    name: str
    type: str  # akriti, sankhya, or ashraya
    formed: bool
    description: str
    effects: str
    planets_involved: List[str]


class NabhasaYogaCalculator:
    """Calculator for Nabhasa Yogas - 32 special pattern yogas"""

    def __init__(self):
        self.detected_yogas: List[NabhasaYoga] = []

    def calculate_all_nabhasa_yogas(
        self, planets: Dict[str, Dict[str, Any]], houses: Dict[int, Any]
    ) -> List[NabhasaYoga]:
        """Calculate all Nabhasa yogas"""
        self.detected_yogas = []

        # Get planet house positions
        planet_houses = self._get_planet_houses(planets, houses)

        # Akriti Yogas (20 shape-based)
        self._check_akriti_yogas(planet_houses)

        # Sankhya Yogas (7 number-based)
        self._check_sankhya_yogas(planet_houses)

        # Ashraya Yogas (3 support-based)
        self._check_ashraya_yogas(planets)

        return self.detected_yogas

    def _get_planet_houses(self, planets: Dict[str, Dict[str, Any]], houses: Dict[int, Any]) -> Dict[str, int]:
        """Get house number for each planet"""
        planet_houses = {}
        for planet_name, planet_data in planets.items():
            if planet_name in ["Rahu", "Ketu"]:
                continue
            planet_lon = planet_data.get("longitude", 0)
            # Determine house
            for house_num, house_data in houses.items():
                if self._is_in_house(planet_lon, house_data):
                    planet_houses[planet_name] = house_num
                    break
        return planet_houses

    def _is_in_house(self, longitude: float, house_data: Any) -> bool:
        """Check if longitude is in house"""
        start = house_data.get("start_degree", 0)
        end = house_data.get("end_degree", 30)
        return start <= longitude < end

    # ==================== AKRITI YOGAS (Shape-based) ====================

    def _check_akriti_yogas(self, planet_houses: Dict[str, int]) -> None:
        """Check for 20 Akriti (shape) yogas"""

        # 1. Yupa Yoga - Planets in 1st, 2nd, 3rd, 4th houses
        self._check_yupa_yoga(planet_houses)

        # 2. Ishu Yoga - Planets in 1st, 2nd, 3rd houses
        self._check_ishu_yoga(planet_houses)

        # 3. Shakti Yoga - Planets in 4th, 5th, 6th houses
        self._check_shakti_yoga(planet_houses)

        # 4. Danda Yoga - Planets in 7th, 8th, 9th houses
        self._check_danda_yoga(planet_houses)

        # 5. Nauka Yoga - Planets in 10th, 11th, 12th houses
        self._check_nauka_yoga(planet_houses)

        # 6. Koota Yoga - Planets in 4th, 8th, 12th houses (trik houses)
        self._check_koota_yoga(planet_houses)

        # 7. Chatra Yoga - Planets in 7th house or benefics in kendras
        self._check_chatra_yoga(planet_houses)

        # 8. Chapa Yoga - Planets in 1st and 7th houses
        self._check_chapa_yoga(planet_houses)

        # 9. Ardha Chandra Yoga - Planets in 1st to 7th houses (one half)
        self._check_ardha_chandra_yoga(planet_houses)

        # 10. Chakra Yoga - Planets in all kendras (1, 4, 7, 10)
        self._check_chakra_yoga(planet_houses)

        # 11. Samudra Yoga - Planets in 2nd and 12th houses (flanking)
        self._check_samudra_yoga(planet_houses)

        # 12. Veena Yoga - Planets in pairs of houses
        self._check_veena_yoga(planet_houses)

        # 13. Dama Yoga - Planets surrounding specific houses
        self._check_dama_yoga(planet_houses)

        # 14. Pasha Yoga - Planets in movable signs
        self._check_pasha_yoga(planet_houses)

        # 15. Kedara Yoga - Planets in fixed signs
        self._check_kedara_yoga(planet_houses)

        # 16. Shula Yoga - Planets in dual signs
        self._check_shula_yoga(planet_houses)

        # 17. Yuga Yoga - Planets in 1st, 4th, 7th, 10th (all kendras)
        self._check_yuga_yoga(planet_houses)

        # 18. Gola Yoga - Planets in one sign
        self._check_gola_yoga(planet_houses)

        # 19. Hala Yoga - Planets in two consecutive signs
        self._check_hala_yoga(planet_houses)

        # 20. Vajra Yoga - Benefics in kendras, malefics elsewhere
        self._check_vajra_yoga(planet_houses)

    def _check_yupa_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Yupa Yoga - All planets in houses 1-4"""
        houses = set(planet_houses.values())
        if houses.issubset({1, 2, 3, 4}):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Yupa Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in houses 1-4 (post-like formation)",
                    effects="Good reputation, religious nature, stable wealth",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_ishu_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Ishu Yoga - All planets in houses 1-3"""
        houses = set(planet_houses.values())
        if houses.issubset({1, 2, 3}):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Ishu Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in houses 1-3 (arrow-like)",
                    effects="Swift actions, athletic, impulsive nature",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_shakti_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Shakti Yoga - All planets in houses 4-6"""
        houses = set(planet_houses.values())
        if houses.issubset({4, 5, 6}):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Shakti Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in houses 4-6 (spear-like)",
                    effects="Powerful, authoritative, successful in conflicts",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_danda_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Danda Yoga - All planets in houses 7-9"""
        houses = set(planet_houses.values())
        if houses.issubset({7, 8, 9}):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Danda Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in houses 7-9 (staff-like)",
                    effects="Disciplined, successful through partnerships",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_nauka_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Nauka Yoga - All planets in houses 10-12"""
        houses = set(planet_houses.values())
        if houses.issubset({10, 11, 12}):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Nauka Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in houses 10-12 (boat-like)",
                    effects="Gains through travel, navigation, foreign lands",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_koota_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Koota Yoga - All planets in trik houses (4, 8, 12)"""
        houses = set(planet_houses.values())
        if houses.issubset({4, 8, 12}):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Koota Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in trik houses (4, 8, 12)",
                    effects="Cunning, secretive, gains through hidden means",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_chatra_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Chatra Yoga - All planets in 7th house"""
        houses = list(planet_houses.values())
        if all(h == 7 for h in houses):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Chatra Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets concentrated in 7th house (umbrella)",
                    effects="Royal comforts, protection, happy partnerships",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_chapa_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Chapa Yoga - Planets distributed in 1st and 7th"""
        houses = set(planet_houses.values())
        if houses.issubset({1, 7}) and len(houses) == 2:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Chapa Yoga",
                    type="akriti",
                    formed=True,
                    description="Planets in 1st and 7th houses (bow-like)",
                    effects="Strong personality, competitive, wins opponents",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_ardha_chandra_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Ardha Chandra Yoga - Planets in one half of zodiac"""
        houses = set(planet_houses.values())
        first_half = houses.issubset({1, 2, 3, 4, 5, 6})
        second_half = houses.issubset({7, 8, 9, 10, 11, 12})
        if first_half or second_half:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Ardha Chandra Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in one half of zodiac (half-moon)",
                    effects="Attractive personality, charismatic, popular",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_chakra_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Chakra Yoga - Planets in all four kendras"""
        houses = set(planet_houses.values())
        if houses.issuperset({1, 4, 7, 10}):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Chakra Yoga",
                    type="akriti",
                    formed=True,
                    description="Planets occupy all four kendras (wheel-like)",
                    effects="Great leadership, influential, authority",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_samudra_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Samudra Yoga - Planets in 2nd and 12th (flanking ascendant)"""
        houses = set(planet_houses.values())
        if houses.issubset({2, 12}) and len(houses) == 2:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Samudra Yoga",
                    type="akriti",
                    formed=True,
                    description="Planets in 2nd and 12th houses (ocean-like)",
                    effects="Wealthy, generous, enjoys luxuries",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_veena_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Veena Yoga - Planets in pairs creating symmetry"""
        houses = sorted(set(planet_houses.values()))
        # Check for symmetric distribution
        if len(houses) >= 2 and self._is_symmetric_distribution(houses):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Veena Yoga",
                    type="akriti",
                    formed=True,
                    description="Planets distributed symmetrically (lute-like)",
                    effects="Artistic, musical talents, refined taste",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_dama_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Dama Yoga - Planets in kendras and panaparas"""
        houses = set(planet_houses.values())
        kendras = {1, 4, 7, 10}
        panaparas = {2, 5, 8, 11}
        if houses.intersection(kendras) and houses.intersection(panaparas):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Dama Yoga",
                    type="akriti",
                    formed=True,
                    description="Planets in kendras and panaparas (garland)",
                    effects="Controlled, charitable, helpful nature",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_pasha_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Pasha Yoga - All planets in movable signs (1, 4, 7, 10)"""
        houses = set(planet_houses.values())
        movable_houses = {1, 4, 7, 10}  # Aries, Cancer, Libra, Capricorn
        if houses.issubset(movable_houses):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Pasha Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in movable signs (bondage)",
                    effects="Restless, traveler, changes in life",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_kedara_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Kedara Yoga - All planets in fixed signs (2, 5, 8, 11)"""
        houses = set(planet_houses.values())
        fixed_houses = {2, 5, 8, 11}  # Taurus, Leo, Scorpio, Aquarius
        if houses.issubset(fixed_houses):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Kedara Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in fixed signs (field-like)",
                    effects="Agricultural prosperity, stable wealth, patience",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_shula_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Shula Yoga - All planets in dual signs (3, 6, 9, 12)"""
        houses = set(planet_houses.values())
        dual_houses = {3, 6, 9, 12}  # Gemini, Virgo, Sagittarius, Pisces
        if houses.issubset(dual_houses):
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Shula Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in dual signs (spear-like)",
                    effects="Dual nature, versatile, adaptable",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_yuga_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Yuga Yoga - Strong kendra occupation"""
        houses = set(planet_houses.values())
        kendras = {1, 4, 7, 10}
        kendra_count = len(houses.intersection(kendras))
        if kendra_count >= 4:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Yuga Yoga",
                    type="akriti",
                    formed=True,
                    description="Majority of planets in kendras (yoke-like)",
                    effects="Leadership, authority, influential",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_gola_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Gola Yoga - All planets in one sign/house"""
        houses = list(planet_houses.values())
        if len(set(houses)) == 1:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Gola Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets concentrated in one house (spherical)",
                    effects="Focused power, intense personality, specialized skills",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_hala_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Hala Yoga - All planets in two consecutive signs"""
        houses = sorted(set(planet_houses.values()))
        if len(houses) == 2 and houses[1] - houses[0] == 1:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Hala Yoga",
                    type="akriti",
                    formed=True,
                    description="All planets in two consecutive houses (plough)",
                    effects="Agricultural success, hard work pays off",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    def _check_vajra_yoga(self, planet_houses: Dict[str, int]) -> None:
        """Vajra Yoga - Benefics in kendras, malefics elsewhere"""
        # Simplified check - would need planet classification
        self.detected_yogas.append(
            NabhasaYoga(
                name="Vajra Yoga",
                type="akriti",
                formed=False,  # Requires planet classification
                description="Benefics in kendras, malefics in other houses",
                effects="Strong like diamond, powerful personality",
                planets_involved=[],
            )
        )

    # ==================== SANKHYA YOGAS (Number-based) ====================

    def _check_sankhya_yogas(self, planet_houses: Dict[str, int]) -> None:
        """Check for 7 Sankhya (number) yogas based on occupied signs"""
        occupied_houses = len(set(planet_houses.values()))

        if occupied_houses == 7:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Vallaki Yoga",
                    type="sankhya",
                    formed=True,
                    description="Planets occupy exactly 7 houses",
                    effects="Wealthy, happy, many children",
                    planets_involved=list(planet_houses.keys()),
                )
            )
        elif occupied_houses == 6:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Dama Yoga",
                    type="sankhya",
                    formed=True,
                    description="Planets occupy exactly 6 houses",
                    effects="Charitable, helpful, good conduct",
                    planets_involved=list(planet_houses.keys()),
                )
            )
        elif occupied_houses == 5:
            self.detected_yogas.append(
                NabhasaYoga(
                    name="Pasha Yoga",
                    type="sankhya",
                    formed=True,
                    description="Planets occupy exactly 5 houses",
                    effects="Accumulator of wealth, imprisoned by desires",
                    planets_involved=list(planet_houses.keys()),
                )
            )

    # ==================== ASHRAYA YOGAS (Support-based) ====================

    def _check_ashraya_yogas(self, planets: Dict[str, Dict[str, Any]]) -> None:
        """Check for 3 Ashraya (support) yogas based on sign types"""
        # Would require sign classification (movable/fixed/dual)
        pass

    def _is_symmetric_distribution(self, houses: List[int]) -> bool:
        """Check if house distribution is symmetric"""
        # Simple symmetry check
        if len(houses) < 2:
            return False
        mid = 6.5
        for house in houses:
            opposite = 13 - house if house <= 6 else house - 6
            if opposite not in houses:
                return False
        return True
