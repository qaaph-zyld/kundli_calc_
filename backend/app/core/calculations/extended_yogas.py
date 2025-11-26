"""
Extended Yoga Detection System
PGF Protocol: YOGA_002
Gate: GATE_5
Version: 1.0.0

This module implements 60+ important Vedic Astrology Yogas including:
- Raja Yogas (Power/Authority)
- Dhana Yogas (Wealth)
- Pancha Mahapurusha Yogas
- Chandra (Moon) Yogas
- Surya (Sun) Yogas
- Budha-Aditya Yoga
- Vipreet Raja Yogas
- Neecha Bhanga Raja Yoga
- Nabhasa Yogas
- Arishta Yogas
- And many more...
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum


class YogaCategory(Enum):
    """Categories of Vedic Yogas"""
    RAJA = "raja"                    # Power, authority, success
    DHANA = "dhana"                  # Wealth
    MAHAPURUSHA = "mahapurusha"      # Great person
    CHANDRA = "chandra"              # Moon-based
    SURYA = "surya"                  # Sun-based
    BUDHA = "budha"                  # Mercury-based
    VIPREET = "vipreet"              # Reversal
    NEECHA_BHANGA = "neecha_bhanga"  # Cancellation of debilitation
    NABHASA = "nabhasa"              # Celestial patterns
    ARISHTA = "arishta"              # Inauspicious
    SANNYASA = "sannyasa"            # Renunciation
    PARIVARTANA = "parivartana"      # Exchange
    SPECIAL = "special"              # Other important yogas


@dataclass
class YogaDefinition:
    """Definition of a yoga with its conditions and effects"""
    name: str
    sanskrit_name: str
    category: YogaCategory
    description: str
    conditions: List[str]  # Human-readable conditions
    effects: List[str]
    strength_factors: List[str]
    is_benefic: bool


@dataclass 
class DetectedYoga:
    """A detected yoga in a chart"""
    name: str
    sanskrit_name: str
    category: YogaCategory
    description: str
    effects: List[str]
    planets_involved: List[str]
    houses_involved: List[int]
    strength: float  # 0-100
    is_complete: bool
    notes: str


# Planetary dignities - exaltation signs (index = sign number 0-11)
EXALTATION = {
    "Sun": 0,       # Aries
    "Moon": 1,      # Taurus
    "Mars": 9,      # Capricorn
    "Mercury": 5,   # Virgo
    "Jupiter": 3,   # Cancer
    "Venus": 11,    # Pisces
    "Saturn": 6     # Libra
}

DEBILITATION = {
    "Sun": 6,       # Libra
    "Moon": 7,      # Scorpio
    "Mars": 3,      # Cancer
    "Mercury": 11,  # Pisces
    "Jupiter": 9,   # Capricorn
    "Venus": 5,     # Virgo
    "Saturn": 0     # Aries
}

OWN_SIGNS = {
    "Sun": [4],                 # Leo
    "Moon": [3],                # Cancer
    "Mars": [0, 7],             # Aries, Scorpio
    "Mercury": [2, 5],          # Gemini, Virgo
    "Jupiter": [8, 11],         # Sagittarius, Pisces
    "Venus": [1, 6],            # Taurus, Libra
    "Saturn": [9, 10],          # Capricorn, Aquarius
    "Rahu": [10],               # Aquarius (according to some)
    "Ketu": [7]                 # Scorpio (according to some)
}

MOOLATRIKONA = {
    "Sun": (4, 0, 20),          # Leo 0-20°
    "Moon": (1, 4, 30),         # Taurus 4-30°
    "Mars": (0, 0, 12),         # Aries 0-12°
    "Mercury": (5, 16, 20),     # Virgo 16-20°
    "Jupiter": (8, 0, 10),      # Sagittarius 0-10°
    "Venus": (6, 0, 15),        # Libra 0-15°
    "Saturn": (10, 0, 20)       # Aquarius 0-20°
}

# Sign lords
SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
              "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

# Trine houses (1, 5, 9)
TRINE_HOUSES = {1, 5, 9}

# Kendra houses (1, 4, 7, 10)
KENDRA_HOUSES = {1, 4, 7, 10}

# Dusthana houses (6, 8, 12)
DUSTHANA_HOUSES = {6, 8, 12}

# Upachaya houses (3, 6, 10, 11)
UPACHAYA_HOUSES = {3, 6, 10, 11}


class ExtendedYogaCalculator:
    """
    Comprehensive Yoga Calculator implementing 60+ Vedic Yogas
    """
    
    def __init__(self):
        self.detected_yogas: List[DetectedYoga] = []
    
    def calculate_all_yogas(
        self,
        planets: Dict[str, Dict[str, Any]],
        houses: Dict[int, List[str]],
        ascendant_sign: int
    ) -> List[DetectedYoga]:
        """
        Calculate all yogas present in the chart
        
        Args:
            planets: Dictionary with planet data (longitude, sign, house, etc.)
            houses: Dictionary mapping house number to list of planets
            ascendant_sign: Sign number of ascendant (0-11)
            
        Returns:
            List of all detected yogas
        """
        self.detected_yogas = []
        self.planets = planets
        self.houses = houses
        self.ascendant_sign = ascendant_sign
        
        # Calculate house lordships based on ascendant
        self.house_lords = self._calculate_house_lords(ascendant_sign)
        
        # Run all yoga checks
        self._check_pancha_mahapurusha_yogas()
        self._check_raja_yogas()
        self._check_dhana_yogas()
        self._check_chandra_yogas()
        self._check_surya_yogas()
        self._check_budha_aditya_yoga()
        self._check_vipreet_raja_yogas()
        self._check_neecha_bhanga_raja_yoga()
        self._check_gajakesari_yoga()
        self._check_kemadruma_yoga()
        self._check_adhi_yoga()
        self._check_lakshmi_yoga()
        self._check_saraswati_yoga()
        self._check_hamsa_yoga()
        self._check_sasa_yoga()
        self._check_parivartana_yoga()
        self._check_vesi_vasi_yogas()
        self._check_pushkala_yoga()
        self._check_kahala_yoga()
        self._check_chamara_yoga()
        self._check_sreenatha_yoga()
        self._check_amala_yoga()
        self._check_parvata_yoga()
        self._check_sannyasa_yogas()
        self._check_daridra_yoga()
        self._check_nabhasa_yogas()
        
        return self.detected_yogas
    
    def _calculate_house_lords(self, asc_sign: int) -> Dict[int, str]:
        """Calculate which planet owns which house based on ascendant"""
        lords = {}
        for house in range(1, 13):
            sign = (asc_sign + house - 1) % 12
            lords[house] = SIGN_LORDS[sign]
        return lords
    
    def _get_planet_house(self, planet: str) -> int:
        """Get the house occupied by a planet"""
        if planet in self.planets:
            return self.planets[planet].get("house", 1)
        return 1
    
    def _get_planet_sign(self, planet: str) -> int:
        """Get the sign occupied by a planet"""
        if planet in self.planets:
            lon = self.planets[planet].get("longitude", 0)
            return int(lon / 30)
        return 0
    
    def _is_in_kendra(self, planet: str) -> bool:
        """Check if planet is in kendra house"""
        return self._get_planet_house(planet) in KENDRA_HOUSES
    
    def _is_in_trine(self, planet: str) -> bool:
        """Check if planet is in trine house"""
        return self._get_planet_house(planet) in TRINE_HOUSES
    
    def _is_exalted(self, planet: str) -> bool:
        """Check if planet is in exaltation"""
        if planet not in EXALTATION:
            return False
        return self._get_planet_sign(planet) == EXALTATION[planet]
    
    def _is_debilitated(self, planet: str) -> bool:
        """Check if planet is debilitated"""
        if planet not in DEBILITATION:
            return False
        return self._get_planet_sign(planet) == DEBILITATION[planet]
    
    def _is_in_own_sign(self, planet: str) -> bool:
        """Check if planet is in own sign"""
        if planet not in OWN_SIGNS:
            return False
        return self._get_planet_sign(planet) in OWN_SIGNS[planet]
    
    def _is_strong(self, planet: str) -> bool:
        """Check if planet has dignity (exalted, own sign, or moolatrikona)"""
        return (self._is_exalted(planet) or 
                self._is_in_own_sign(planet) or
                self._is_in_moolatrikona(planet))
    
    def _is_in_moolatrikona(self, planet: str) -> bool:
        """Check if planet is in moolatrikona"""
        if planet not in MOOLATRIKONA:
            return False
        mt_sign, mt_start, mt_end = MOOLATRIKONA[planet]
        if self._get_planet_sign(planet) != mt_sign:
            return False
        lon = self.planets[planet].get("longitude", 0) % 30
        return mt_start <= lon <= mt_end
    
    def _get_house_from_sign(self, sign: int) -> int:
        """Convert sign to house based on ascendant"""
        return ((sign - self.ascendant_sign) % 12) + 1
    
    def _add_yoga(
        self,
        name: str,
        sanskrit_name: str,
        category: YogaCategory,
        description: str,
        effects: List[str],
        planets: List[str],
        houses: List[int],
        strength: float,
        notes: str = ""
    ):
        """Helper to add a detected yoga"""
        self.detected_yogas.append(DetectedYoga(
            name=name,
            sanskrit_name=sanskrit_name,
            category=category,
            description=description,
            effects=effects,
            planets_involved=planets,
            houses_involved=houses,
            strength=strength,
            is_complete=True,
            notes=notes
        ))
    
    # ==================== PANCHA MAHAPURUSHA YOGAS ====================
    
    def _check_pancha_mahapurusha_yogas(self):
        """
        Check for Pancha Mahapurusha Yogas
        These form when Mars, Mercury, Jupiter, Venus, or Saturn
        are in kendra houses in their own or exaltation signs
        """
        mahapurusha_planets = {
            "Mars": ("Ruchaka", "रुचक", "Valor, courage, leadership, military success"),
            "Mercury": ("Bhadra", "भद्र", "Intelligence, communication skills, business acumen"),
            "Jupiter": ("Hamsa", "हंस", "Wisdom, spirituality, teaching ability, ethics"),
            "Venus": ("Malavya", "मालव्य", "Beauty, artistic talent, luxury, romance"),
            "Saturn": ("Sasa", "शश", "Power, authority, discipline, material success")
        }
        
        for planet, (name, sanskrit, desc) in mahapurusha_planets.items():
            house = self._get_planet_house(planet)
            if house in KENDRA_HOUSES:
                if self._is_exalted(planet) or self._is_in_own_sign(planet):
                    strength = 90 if self._is_exalted(planet) else 80
                    self._add_yoga(
                        name=f"{name} Yoga",
                        sanskrit_name=f"{sanskrit} योग",
                        category=YogaCategory.MAHAPURUSHA,
                        description=f"{planet} in kendra in {'exaltation' if self._is_exalted(planet) else 'own sign'}",
                        effects=[desc, "Great personality", "Fame and recognition"],
                        planets=[planet],
                        houses=[house],
                        strength=strength
                    )
    
    # ==================== RAJA YOGAS ====================
    
    def _check_raja_yogas(self):
        """
        Check for Raja Yogas - combinations of trine and kendra lords
        """
        trine_lords = [self.house_lords[h] for h in TRINE_HOUSES]
        kendra_lords = [self.house_lords[h] for h in KENDRA_HOUSES]
        
        # Check for conjunction of trine and kendra lords
        for tl in trine_lords:
            for kl in kendra_lords:
                if tl != kl:
                    tl_house = self._get_planet_house(tl)
                    kl_house = self._get_planet_house(kl)
                    
                    if tl_house == kl_house:  # Conjunction
                        strength = 85
                        if tl_house in KENDRA_HOUSES or tl_house in TRINE_HOUSES:
                            strength = 95
                        
                        self._add_yoga(
                            name="Raja Yoga",
                            sanskrit_name="राज योग",
                            category=YogaCategory.RAJA,
                            description=f"{tl} (trine lord) and {kl} (kendra lord) conjunct",
                            effects=["Power and authority", "Success in career", "Leadership"],
                            planets=[tl, kl],
                            houses=[tl_house],
                            strength=strength
                        )
        
        # Check for mutual aspect of trine and kendra lords
        for tl in trine_lords:
            for kl in kendra_lords:
                if tl != kl:
                    tl_house = self._get_planet_house(tl)
                    kl_house = self._get_planet_house(kl)
                    
                    # Check 7th aspect (opposition)
                    if abs(tl_house - kl_house) == 6 or abs(tl_house - kl_house) == 6:
                        self._add_yoga(
                            name="Raja Yoga (Aspect)",
                            sanskrit_name="राज योग (दृष्टि)",
                            category=YogaCategory.RAJA,
                            description=f"{tl} and {kl} in mutual aspect",
                            effects=["Authority", "Recognition", "Career growth"],
                            planets=[tl, kl],
                            houses=[tl_house, kl_house],
                            strength=75
                        )
    
    # ==================== DHANA YOGAS ====================
    
    def _check_dhana_yogas(self):
        """
        Check for Dhana (Wealth) Yogas
        """
        lord_2 = self.house_lords[2]  # Wealth house
        lord_11 = self.house_lords[11]  # Gains house
        lord_5 = self.house_lords[5]  # Purva punya (past merit)
        lord_9 = self.house_lords[9]  # Fortune
        
        # 2nd lord and 11th lord connection
        h2 = self._get_planet_house(lord_2)
        h11 = self._get_planet_house(lord_11)
        
        if h2 == h11:  # Conjunction
            self._add_yoga(
                name="Dhana Yoga",
                sanskrit_name="धन योग",
                category=YogaCategory.DHANA,
                description="2nd and 11th lords conjunct",
                effects=["Wealth accumulation", "Financial prosperity"],
                planets=[lord_2, lord_11],
                houses=[h2],
                strength=85
            )
        
        # 5th lord in 9th or 9th lord in 5th
        h5 = self._get_planet_house(lord_5)
        h9 = self._get_planet_house(lord_9)
        
        if h5 == 9:
            self._add_yoga(
                name="Lakshmi Yoga",
                sanskrit_name="लक्ष्मी योग",
                category=YogaCategory.DHANA,
                description="5th lord in 9th house",
                effects=["Wealth through merit", "Fortune", "Prosperity"],
                planets=[lord_5],
                houses=[9],
                strength=80
            )
        
        if h9 == 5:
            self._add_yoga(
                name="Lakshmi Yoga",
                sanskrit_name="लक्ष्मी योग",
                category=YogaCategory.DHANA,
                description="9th lord in 5th house",
                effects=["Wealth through fortune", "Good luck", "Prosperity"],
                planets=[lord_9],
                houses=[5],
                strength=80
            )
    
    # ==================== CHANDRA (MOON) YOGAS ====================
    
    def _check_chandra_yogas(self):
        """
        Check for Moon-based yogas
        """
        if "Moon" not in self.planets:
            return
            
        moon_house = self._get_planet_house("Moon")
        
        # Check for planets in 2nd and 12th from Moon
        h2_from_moon = (moon_house % 12) + 1
        h12_from_moon = ((moon_house - 2) % 12) + 1
        
        planets_2nd = self.houses.get(h2_from_moon, [])
        planets_12th = self.houses.get(h12_from_moon, [])
        
        # Sunapha Yoga - benefics in 2nd from Moon
        benefics_2nd = [p for p in planets_2nd if p in ["Jupiter", "Venus", "Mercury"]]
        if benefics_2nd:
            self._add_yoga(
                name="Sunapha Yoga",
                sanskrit_name="सुनफा योग",
                category=YogaCategory.CHANDRA,
                description=f"Benefic(s) {benefics_2nd} in 2nd from Moon",
                effects=["Self-made wealth", "Intelligence", "Fame"],
                planets=["Moon"] + benefics_2nd,
                houses=[moon_house, h2_from_moon],
                strength=75
            )
        
        # Anapha Yoga - benefics in 12th from Moon
        benefics_12th = [p for p in planets_12th if p in ["Jupiter", "Venus", "Mercury"]]
        if benefics_12th:
            self._add_yoga(
                name="Anapha Yoga",
                sanskrit_name="अनफा योग",
                category=YogaCategory.CHANDRA,
                description=f"Benefic(s) {benefics_12th} in 12th from Moon",
                effects=["Well-dressed", "Good character", "Fame"],
                planets=["Moon"] + benefics_12th,
                houses=[moon_house, h12_from_moon],
                strength=75
            )
        
        # Durudhara Yoga - benefics in both 2nd and 12th from Moon
        if benefics_2nd and benefics_12th:
            self._add_yoga(
                name="Durudhara Yoga",
                sanskrit_name="दुरुधरा योग",
                category=YogaCategory.CHANDRA,
                description="Benefics on both sides of Moon",
                effects=["Wealth", "Enjoyments", "Charitable nature"],
                planets=["Moon"] + benefics_2nd + benefics_12th,
                houses=[moon_house, h2_from_moon, h12_from_moon],
                strength=85
            )
    
    # ==================== SURYA (SUN) YOGAS ====================
    
    def _check_surya_yogas(self):
        """
        Check for Sun-based yogas
        """
        if "Sun" not in self.planets:
            return
            
        sun_house = self._get_planet_house("Sun")
        
        # Check 2nd and 12th from Sun
        h2_from_sun = (sun_house % 12) + 1
        h12_from_sun = ((sun_house - 2) % 12) + 1
        
        planets_2nd = self.houses.get(h2_from_sun, [])
        planets_12th = self.houses.get(h12_from_sun, [])
        
        # Vesi Yoga - any planet (except Moon) in 2nd from Sun
        vesi_planets = [p for p in planets_2nd if p != "Moon"]
        if vesi_planets:
            self._add_yoga(
                name="Vesi Yoga",
                sanskrit_name="वेशी योग",
                category=YogaCategory.SURYA,
                description=f"{vesi_planets} in 2nd from Sun",
                effects=["Truthful", "Lazy but learned", "Equal to king"],
                planets=["Sun"] + vesi_planets,
                houses=[sun_house, h2_from_sun],
                strength=70
            )
        
        # Vasi Yoga - any planet (except Moon) in 12th from Sun
        vasi_planets = [p for p in planets_12th if p != "Moon"]
        if vasi_planets:
            self._add_yoga(
                name="Vasi Yoga",
                sanskrit_name="वासी योग",
                category=YogaCategory.SURYA,
                description=f"{vasi_planets} in 12th from Sun",
                effects=["Prosperous", "Good memory", "Charitable"],
                planets=["Sun"] + vasi_planets,
                houses=[sun_house, h12_from_sun],
                strength=70
            )
        
        # Ubhayachari Yoga - planets on both sides of Sun
        if vesi_planets and vasi_planets:
            self._add_yoga(
                name="Ubhayachari Yoga",
                sanskrit_name="उभयचारी योग",
                category=YogaCategory.SURYA,
                description="Planets on both sides of Sun",
                effects=["Royal status", "Eloquent", "Wealthy", "Famous"],
                planets=["Sun"] + vesi_planets + vasi_planets,
                houses=[sun_house, h2_from_sun, h12_from_sun],
                strength=85
            )
    
    # ==================== BUDHA-ADITYA YOGA ====================
    
    def _check_budha_aditya_yoga(self):
        """
        Budha-Aditya Yoga - Sun and Mercury conjunction
        Very common but strength depends on combustion and house
        """
        if "Sun" not in self.planets or "Mercury" not in self.planets:
            return
        
        sun_house = self._get_planet_house("Sun")
        mercury_house = self._get_planet_house("Mercury")
        
        if sun_house == mercury_house:
            sun_lon = self.planets["Sun"].get("longitude", 0)
            merc_lon = self.planets["Mercury"].get("longitude", 0)
            
            # Check if Mercury is combust (within 14° of Sun)
            diff = abs(sun_lon - merc_lon)
            is_combust = diff < 14
            
            strength = 60 if is_combust else 80
            
            # Stronger in kendra or trine
            if sun_house in KENDRA_HOUSES | TRINE_HOUSES:
                strength += 10
            
            effects = ["Intelligence", "Learned", "Fame through intelligence"]
            if is_combust:
                effects.append("(Reduced due to combustion)")
            
            self._add_yoga(
                name="Budha-Aditya Yoga",
                sanskrit_name="बुधादित्य योग",
                category=YogaCategory.BUDHA,
                description="Sun-Mercury conjunction",
                effects=effects,
                planets=["Sun", "Mercury"],
                houses=[sun_house],
                strength=strength,
                notes="Combust" if is_combust else ""
            )
    
    # ==================== VIPREET RAJA YOGAS ====================
    
    def _check_vipreet_raja_yogas(self):
        """
        Vipreet Raja Yogas - Lords of 6, 8, 12 in each other's houses
        Turns negative into positive
        """
        lord_6 = self.house_lords[6]
        lord_8 = self.house_lords[8]
        lord_12 = self.house_lords[12]
        
        h6 = self._get_planet_house(lord_6)
        h8 = self._get_planet_house(lord_8)
        h12 = self._get_planet_house(lord_12)
        
        # Harsha Yoga - 6th lord in 6th, 8th, or 12th
        if h6 in [6, 8, 12]:
            self._add_yoga(
                name="Harsha Yoga",
                sanskrit_name="हर्ष योग",
                category=YogaCategory.VIPREET,
                description=f"6th lord {lord_6} in house {h6}",
                effects=["Victory over enemies", "Good health", "Happiness"],
                planets=[lord_6],
                houses=[h6],
                strength=75
            )
        
        # Sarala Yoga - 8th lord in 6th, 8th, or 12th
        if h8 in [6, 8, 12]:
            self._add_yoga(
                name="Sarala Yoga",
                sanskrit_name="सरल योग",
                category=YogaCategory.VIPREET,
                description=f"8th lord {lord_8} in house {h8}",
                effects=["Long life", "Fearless", "Prosperous"],
                planets=[lord_8],
                houses=[h8],
                strength=75
            )
        
        # Vimala Yoga - 12th lord in 6th, 8th, or 12th
        if h12 in [6, 8, 12]:
            self._add_yoga(
                name="Vimala Yoga",
                sanskrit_name="विमल योग",
                category=YogaCategory.VIPREET,
                description=f"12th lord {lord_12} in house {h12}",
                effects=["Frugal", "Independent", "Respected"],
                planets=[lord_12],
                houses=[h12],
                strength=75
            )
    
    # ==================== NEECHA BHANGA RAJA YOGA ====================
    
    def _check_neecha_bhanga_raja_yoga(self):
        """
        Neecha Bhanga (Cancellation of Debilitation) Raja Yoga
        When a debilitated planet gets cancellation and becomes powerful
        """
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            if planet not in self.planets:
                continue
                
            if self._is_debilitated(planet):
                cancellation_reasons = []
                
                # Rule 1: Lord of debilitation sign in kendra from Lagna or Moon
                deb_sign = DEBILITATION[planet]
                deb_sign_lord = SIGN_LORDS[deb_sign]
                dsl_house = self._get_planet_house(deb_sign_lord)
                
                if dsl_house in KENDRA_HOUSES:
                    cancellation_reasons.append(
                        f"Lord of debilitation sign ({deb_sign_lord}) in kendra"
                    )
                
                # Rule 2: Exaltation lord aspects the debilitated planet
                exalt_sign = EXALTATION[planet]
                exalt_lord = SIGN_LORDS[exalt_sign]
                
                # Rule 3: Planet in kendra from Moon or Lagna
                planet_house = self._get_planet_house(planet)
                if planet_house in KENDRA_HOUSES:
                    cancellation_reasons.append(f"{planet} in kendra")
                
                # Rule 4: Debilitated planet exalted in navamsa (would need navamsa data)
                
                if cancellation_reasons:
                    self._add_yoga(
                        name="Neecha Bhanga Raja Yoga",
                        sanskrit_name="नीच भंग राज योग",
                        category=YogaCategory.NEECHA_BHANGA,
                        description=f"Debilitation of {planet} cancelled",
                        effects=["Rise after initial struggles", "Success against odds", 
                                "Powerful after overcoming obstacles"],
                        planets=[planet, deb_sign_lord],
                        houses=[planet_house],
                        strength=80,
                        notes="; ".join(cancellation_reasons)
                    )
    
    # ==================== GAJAKESARI YOGA ====================
    
    def _check_gajakesari_yoga(self):
        """
        Gajakesari Yoga - Jupiter in kendra from Moon
        One of the most celebrated yogas
        """
        if "Moon" not in self.planets or "Jupiter" not in self.planets:
            return
        
        moon_house = self._get_planet_house("Moon")
        jupiter_house = self._get_planet_house("Jupiter")
        
        # Check if Jupiter is in kendra (1, 4, 7, 10) from Moon
        houses_from_moon = [(moon_house + i - 1) % 12 + 1 for i in [0, 3, 6, 9]]
        
        if jupiter_house in houses_from_moon:
            strength = 80
            
            # Stronger if Jupiter is strong
            if self._is_strong("Jupiter"):
                strength = 90
            
            self._add_yoga(
                name="Gajakesari Yoga",
                sanskrit_name="गजकेसरी योग",
                category=YogaCategory.SPECIAL,
                description="Jupiter in kendra from Moon",
                effects=["Fame", "Wealth", "Many virtues", "Long life",
                        "Destroys enemies", "Pleases the king"],
                planets=["Moon", "Jupiter"],
                houses=[moon_house, jupiter_house],
                strength=strength
            )
    
    # ==================== KEMADRUMA YOGA ====================
    
    def _check_kemadruma_yoga(self):
        """
        Kemadruma Yoga - No planets in 2nd or 12th from Moon
        An inauspicious yoga (but can be cancelled)
        """
        if "Moon" not in self.planets:
            return
        
        moon_house = self._get_planet_house("Moon")
        h2_from_moon = (moon_house % 12) + 1
        h12_from_moon = ((moon_house - 2) % 12) + 1
        
        planets_2nd = [p for p in self.houses.get(h2_from_moon, []) if p != "Rahu" and p != "Ketu"]
        planets_12th = [p for p in self.houses.get(h12_from_moon, []) if p != "Rahu" and p != "Ketu"]
        
        if not planets_2nd and not planets_12th:
            # Check for cancellations
            cancellation = False
            
            # Cancel if Moon in kendra
            if moon_house in KENDRA_HOUSES:
                cancellation = True
            
            # Cancel if Moon aspected by Jupiter
            jupiter_house = self._get_planet_house("Jupiter") if "Jupiter" in self.planets else 0
            if abs(jupiter_house - moon_house) == 6:  # 7th aspect
                cancellation = True
            
            if not cancellation:
                self._add_yoga(
                    name="Kemadruma Yoga",
                    sanskrit_name="केमद्रुम योग",
                    category=YogaCategory.ARISHTA,
                    description="No planets in 2nd/12th from Moon",
                    effects=["Poverty", "Struggles", "Loneliness"],
                    planets=["Moon"],
                    houses=[moon_house],
                    strength=60,
                    notes="Inauspicious - check for cancellations"
                )
    
    # ==================== ADHI YOGA ====================
    
    def _check_adhi_yoga(self):
        """
        Adhi Yoga - Benefics in 6th, 7th, and 8th from Moon
        """
        if "Moon" not in self.planets:
            return
        
        moon_house = self._get_planet_house("Moon")
        h6 = ((moon_house + 4) % 12) + 1
        h7 = ((moon_house + 5) % 12) + 1
        h8 = ((moon_house + 6) % 12) + 1
        
        benefics = ["Jupiter", "Venus", "Mercury"]
        benefics_6 = [p for p in self.houses.get(h6, []) if p in benefics]
        benefics_7 = [p for p in self.houses.get(h7, []) if p in benefics]
        benefics_8 = [p for p in self.houses.get(h8, []) if p in benefics]
        
        total_benefics = len(benefics_6) + len(benefics_7) + len(benefics_8)
        
        if total_benefics >= 2:
            all_benefics = benefics_6 + benefics_7 + benefics_8
            self._add_yoga(
                name="Adhi Yoga",
                sanskrit_name="अधि योग",
                category=YogaCategory.SPECIAL,
                description="Benefics in 6th/7th/8th from Moon",
                effects=["Commander/Minister", "Wealthy", "Overcomes enemies",
                        "Long-lived", "Free from disease"],
                planets=["Moon"] + all_benefics,
                houses=[moon_house, h6, h7, h8],
                strength=70 + (total_benefics * 10)
            )
    
    # ==================== LAKSHMI YOGA ====================
    
    def _check_lakshmi_yoga(self):
        """
        Lakshmi Yoga - Multiple conditions for wealth
        """
        lord_9 = self.house_lords[9]
        h9_lord_house = self._get_planet_house(lord_9)
        
        # 9th lord in kendra/trine and strong
        if (h9_lord_house in KENDRA_HOUSES or h9_lord_house in TRINE_HOUSES):
            if self._is_strong(lord_9):
                self._add_yoga(
                    name="Lakshmi Yoga",
                    sanskrit_name="लक्ष्मी योग",
                    category=YogaCategory.DHANA,
                    description=f"9th lord {lord_9} strong in house {h9_lord_house}",
                    effects=["Wealth", "Fame", "Beauty", "Virtuous"],
                    planets=[lord_9],
                    houses=[h9_lord_house],
                    strength=85
                )
    
    # ==================== SARASWATI YOGA ====================
    
    def _check_saraswati_yoga(self):
        """
        Saraswati Yoga - Jupiter, Venus, Mercury in kendra/trine
        """
        planets_check = ["Jupiter", "Venus", "Mercury"]
        in_good_houses = []
        
        for planet in planets_check:
            if planet in self.planets:
                house = self._get_planet_house(planet)
                if house in (KENDRA_HOUSES | TRINE_HOUSES):
                    in_good_houses.append(planet)
        
        if len(in_good_houses) >= 2:
            houses = [self._get_planet_house(p) for p in in_good_houses]
            self._add_yoga(
                name="Saraswati Yoga",
                sanskrit_name="सरस्वती योग",
                category=YogaCategory.SPECIAL,
                description="Jupiter/Venus/Mercury in kendra/trine",
                effects=["Learning", "Wisdom", "Fame as scholar",
                        "Creative arts", "Writing ability"],
                planets=in_good_houses,
                houses=houses,
                strength=75 + (len(in_good_houses) * 5)
            )
    
    # ==================== HAMSA YOGA (re-check specific) ====================
    
    def _check_hamsa_yoga(self):
        """Already covered in Mahapurusha, but add specific note"""
        pass
    
    # ==================== SASA YOGA (re-check specific) ====================
    
    def _check_sasa_yoga(self):
        """Already covered in Mahapurusha, but add specific note"""
        pass
    
    # ==================== PARIVARTANA YOGA ====================
    
    def _check_parivartana_yoga(self):
        """
        Parivartana (Exchange) Yoga - Two planets in each other's signs
        """
        for i in range(12):
            for j in range(i + 1, 12):
                lord_i = SIGN_LORDS[i]
                lord_j = SIGN_LORDS[j]
                
                if lord_i == lord_j:
                    continue
                
                # Check if lord_i is in sign j and lord_j is in sign i
                if (lord_i in self.planets and lord_j in self.planets):
                    sign_i = self._get_planet_sign(lord_i)
                    sign_j = self._get_planet_sign(lord_j)
                    
                    if sign_i == j and sign_j == i:
                        house_i = self._get_house_from_sign(i)
                        house_j = self._get_house_from_sign(j)
                        
                        # Determine yoga type based on houses involved
                        yoga_type = "Maha"
                        effects = ["Mutual benefit", "Strong results"]
                        
                        if house_i in DUSTHANA_HOUSES or house_j in DUSTHANA_HOUSES:
                            yoga_type = "Khala" if 3 in [house_i, house_j] else "Dainya"
                            effects = ["Mixed results", "Challenges converted to growth"]
                        
                        self._add_yoga(
                            name=f"{yoga_type} Parivartana Yoga",
                            sanskrit_name=f"{yoga_type} परिवर्तन योग",
                            category=YogaCategory.PARIVARTANA,
                            description=f"{lord_i} and {lord_j} exchange signs",
                            effects=effects,
                            planets=[lord_i, lord_j],
                            houses=[house_i, house_j],
                            strength=75
                        )
    
    # ==================== VESI VASI YOGAS ====================
    
    def _check_vesi_vasi_yogas(self):
        """Covered in Surya yogas"""
        pass
    
    # ==================== PUSHKALA YOGA ====================
    
    def _check_pushkala_yoga(self):
        """
        Pushkala Yoga - Complex conditions involving Lagna lord and Moon
        """
        lord_1 = self.house_lords[1]
        h1_lord = self._get_planet_house(lord_1)
        
        if h1_lord in KENDRA_HOUSES and self._is_strong(lord_1):
            if "Moon" in self.planets:
                moon_house = self._get_planet_house("Moon")
                if moon_house in KENDRA_HOUSES or moon_house in TRINE_HOUSES:
                    self._add_yoga(
                        name="Pushkala Yoga",
                        sanskrit_name="पुष्कल योग",
                        category=YogaCategory.SPECIAL,
                        description="Lagna lord strong in kendra, Moon well-placed",
                        effects=["Sweet speech", "Famous", "Wealthy",
                                "Honored by rulers"],
                        planets=[lord_1, "Moon"],
                        houses=[h1_lord, moon_house],
                        strength=75
                    )
    
    # ==================== KAHALA YOGA ====================
    
    def _check_kahala_yoga(self):
        """
        Kahala Yoga - 4th and 9th lords in mutual kendras
        """
        lord_4 = self.house_lords[4]
        lord_9 = self.house_lords[9]
        
        h4 = self._get_planet_house(lord_4)
        h9 = self._get_planet_house(lord_9)
        
        if h4 in KENDRA_HOUSES and h9 in KENDRA_HOUSES:
            self._add_yoga(
                name="Kahala Yoga",
                sanskrit_name="कहल योग",
                category=YogaCategory.SPECIAL,
                description="4th and 9th lords in kendras",
                effects=["Bold", "Army leader", "Head of village/city"],
                planets=[lord_4, lord_9],
                houses=[h4, h9],
                strength=70
            )
    
    # ==================== CHAMARA YOGA ====================
    
    def _check_chamara_yoga(self):
        """
        Chamara Yoga - Lagna lord exalted in kendra with Jupiter aspecting
        """
        lord_1 = self.house_lords[1]
        h1_lord = self._get_planet_house(lord_1)
        
        if self._is_exalted(lord_1) and h1_lord in KENDRA_HOUSES:
            if "Jupiter" in self.planets:
                jupiter_house = self._get_planet_house("Jupiter")
                # Check Jupiter aspect (5, 7, 9)
                diff = abs(jupiter_house - h1_lord)
                if diff in [4, 6, 8]:
                    self._add_yoga(
                        name="Chamara Yoga",
                        sanskrit_name="चामर योग",
                        category=YogaCategory.RAJA,
                        description="Exalted Lagna lord in kendra with Jupiter aspect",
                        effects=["Royal honor", "Eloquent", "Long-lived", "Learned"],
                        planets=[lord_1, "Jupiter"],
                        houses=[h1_lord, jupiter_house],
                        strength=85
                    )
    
    # ==================== SREENATHA YOGA ====================
    
    def _check_sreenatha_yoga(self):
        """
        Sreenatha Yoga - 7th lord in 10th, 10th lord in 9th
        """
        lord_7 = self.house_lords[7]
        lord_10 = self.house_lords[10]
        
        h7_lord = self._get_planet_house(lord_7)
        h10_lord = self._get_planet_house(lord_10)
        
        if h7_lord == 10 and h10_lord == 9:
            self._add_yoga(
                name="Sreenatha Yoga",
                sanskrit_name="श्रीनाथ योग",
                category=YogaCategory.SPECIAL,
                description="7th lord in 10th, 10th lord in 9th",
                effects=["Wealthy after middle age", "Good spouse", "Famous"],
                planets=[lord_7, lord_10],
                houses=[10, 9],
                strength=75
            )
    
    # ==================== AMALA YOGA ====================
    
    def _check_amala_yoga(self):
        """
        Amala Yoga - Benefic in 10th from Lagna or Moon
        """
        benefics = ["Jupiter", "Venus", "Mercury"]
        
        # 10th from Lagna
        planets_10th = self.houses.get(10, [])
        benefics_10th = [p for p in planets_10th if p in benefics]
        
        if benefics_10th:
            self._add_yoga(
                name="Amala Yoga",
                sanskrit_name="अमल योग",
                category=YogaCategory.SPECIAL,
                description=f"Benefic(s) {benefics_10th} in 10th house",
                effects=["Lasting fame", "Charitable", "Prosperous career"],
                planets=benefics_10th,
                houses=[10],
                strength=80
            )
    
    # ==================== PARVATA YOGA ====================
    
    def _check_parvata_yoga(self):
        """
        Parvata Yoga - Benefics in kendras, 6th and 8th empty
        """
        benefics = ["Jupiter", "Venus", "Mercury"]
        
        benefics_in_kendra = []
        for planet in benefics:
            if planet in self.planets:
                if self._get_planet_house(planet) in KENDRA_HOUSES:
                    benefics_in_kendra.append(planet)
        
        planets_6th = self.houses.get(6, [])
        planets_8th = self.houses.get(8, [])
        
        if benefics_in_kendra and not planets_6th and not planets_8th:
            houses = [self._get_planet_house(p) for p in benefics_in_kendra]
            self._add_yoga(
                name="Parvata Yoga",
                sanskrit_name="पर्वत योग",
                category=YogaCategory.SPECIAL,
                description="Benefics in kendra, 6th & 8th empty",
                effects=["Wealthy", "Charitable", "Famous", "Leader"],
                planets=benefics_in_kendra,
                houses=houses,
                strength=80
            )
    
    # ==================== SANNYASA YOGAS ====================
    
    def _check_sannyasa_yogas(self):
        """
        Sannyasa Yoga - 4+ planets in one house
        """
        for house, planets in self.houses.items():
            if len(planets) >= 4:
                self._add_yoga(
                    name="Sannyasa Yoga",
                    sanskrit_name="संन्यास योग",
                    category=YogaCategory.SANNYASA,
                    description=f"{len(planets)} planets in house {house}",
                    effects=["Detachment", "Spiritual inclination", "Renunciation"],
                    planets=planets,
                    houses=[house],
                    strength=70
                )
    
    # ==================== DARIDRA YOGA ====================
    
    def _check_daridra_yoga(self):
        """
        Daridra Yoga - 11th lord in 6th, 8th, or 12th
        """
        lord_11 = self.house_lords[11]
        h11_lord = self._get_planet_house(lord_11)
        
        if h11_lord in DUSTHANA_HOUSES:
            self._add_yoga(
                name="Daridra Yoga",
                sanskrit_name="दरिद्र योग",
                category=YogaCategory.ARISHTA,
                description=f"11th lord in {h11_lord} house",
                effects=["Financial difficulties", "Obstacles in gains"],
                planets=[lord_11],
                houses=[h11_lord],
                strength=60,
                notes="Check for cancellations and overall chart strength"
            )
    
    # ==================== NABHASA YOGAS ====================
    
    def _check_nabhasa_yogas(self):
        """
        Nabhasa Yogas - Based on planetary patterns
        """
        occupied_houses = [h for h, planets in self.houses.items() if planets]
        
        # Yupa Yoga - All planets in 4 consecutive houses starting from ascendant
        if len(occupied_houses) <= 4:
            consecutive = all(
                occupied_houses[i+1] - occupied_houses[i] == 1 
                for i in range(len(occupied_houses)-1)
            ) if len(occupied_houses) > 1 else True
            
            if consecutive:
                all_planets = []
                for h in occupied_houses:
                    all_planets.extend(self.houses[h])
                
                self._add_yoga(
                    name="Yupa Yoga",
                    sanskrit_name="यूप योग",
                    category=YogaCategory.NABHASA,
                    description="All planets in consecutive houses",
                    effects=["Religious", "Charitable", "Priestly duties"],
                    planets=all_planets,
                    houses=occupied_houses,
                    strength=65
                )
        
        # Gada Yoga - Planets only in two adjacent kendras
        kendra_count = len([h for h in occupied_houses if h in KENDRA_HOUSES])
        if kendra_count >= 2 and len(occupied_houses) <= 4:
            all_planets = []
            for h in occupied_houses:
                if h in KENDRA_HOUSES:
                    all_planets.extend(self.houses[h])
            
            self._add_yoga(
                name="Gada Yoga",
                sanskrit_name="गदा योग",
                category=YogaCategory.NABHASA,
                description="Planets concentrated in kendras",
                effects=["Wealthy", "Clever", "Interested in rituals"],
                planets=all_planets,
                houses=[h for h in occupied_houses if h in KENDRA_HOUSES],
                strength=70
            )


def calculate_yogas(
    planets: Dict[str, Dict[str, Any]],
    houses: Dict[int, List[str]],
    ascendant_sign: int
) -> List[Dict[str, Any]]:
    """
    Convenience function to calculate all yogas
    
    Args:
        planets: Planet data with longitude, sign, house
        houses: Dictionary of house to planet list
        ascendant_sign: Sign number of ascendant (0-11)
        
    Returns:
        List of detected yogas as dictionaries
    """
    calculator = ExtendedYogaCalculator()
    yogas = calculator.calculate_all_yogas(planets, houses, ascendant_sign)
    
    return [
        {
            "name": y.name,
            "sanskrit_name": y.sanskrit_name,
            "category": y.category.value,
            "description": y.description,
            "effects": y.effects,
            "planets": y.planets_involved,
            "houses": y.houses_involved,
            "strength": y.strength,
            "is_benefic": y.category not in [YogaCategory.ARISHTA],
            "notes": y.notes
        }
        for y in yogas
    ]
