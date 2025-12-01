"""
Complete Compatibility Analysis (Ashtakoot Milan)
PGF Protocol: COMPAT_001
Gate: GATE_5
Version: 1.0.0

Implements:
- Ashtakoot (8-fold) matching with full 36 points
- Dashakoot (10-fold) matching
- Manglik Dosha check
- Nadi Dosha analysis
- Bhakoot Dosha analysis
- Gana compatibility
- Overall compatibility score and recommendations
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum


# Nakshatra data
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Nakshatra Nadi (3 types)
NAKSHATRA_NADI = [
    "Aadi", "Madhya", "Antya", "Aadi", "Madhya", "Antya",
    "Aadi", "Madhya", "Antya", "Aadi", "Madhya", "Antya",
    "Aadi", "Madhya", "Antya", "Aadi", "Madhya", "Antya",
    "Aadi", "Madhya", "Antya", "Aadi", "Madhya", "Antya",
    "Aadi", "Madhya", "Antya"
]

# Nakshatra Gana (3 types)
NAKSHATRA_GANA = [
    "Deva", "Manushya", "Rakshasa", "Manushya", "Deva", "Rakshasa",
    "Deva", "Deva", "Rakshasa", "Rakshasa", "Manushya", "Manushya",
    "Deva", "Rakshasa", "Deva", "Rakshasa", "Deva", "Rakshasa",
    "Rakshasa", "Manushya", "Manushya", "Deva", "Rakshasa", "Rakshasa",
    "Manushya", "Manushya", "Deva"
]

# Nakshatra Yoni (Animal type)
NAKSHATRA_YONI = [
    ("Horse", "Male"), ("Elephant", "Male"), ("Sheep", "Female"), ("Serpent", "Male"),
    ("Serpent", "Female"), ("Dog", "Female"), ("Cat", "Female"), ("Sheep", "Male"),
    ("Cat", "Male"), ("Rat", "Male"), ("Rat", "Female"), ("Cow", "Male"),
    ("Buffalo", "Female"), ("Tiger", "Female"), ("Buffalo", "Male"), ("Tiger", "Male"),
    ("Deer", "Female"), ("Deer", "Male"), ("Dog", "Male"), ("Monkey", "Male"),
    ("Mongoose", "Male"), ("Monkey", "Female"), ("Lion", "Female"), ("Horse", "Female"),
    ("Lion", "Male"), ("Cow", "Female"), ("Elephant", "Female")
]

# Yoni compatibility scores
YONI_COMPAT = {
    ("Horse", "Horse"): 4, ("Elephant", "Elephant"): 4, ("Sheep", "Sheep"): 4,
    ("Serpent", "Serpent"): 4, ("Dog", "Dog"): 4, ("Cat", "Cat"): 4,
    ("Rat", "Rat"): 4, ("Cow", "Cow"): 4, ("Buffalo", "Buffalo"): 4,
    ("Tiger", "Tiger"): 4, ("Deer", "Deer"): 4, ("Monkey", "Monkey"): 4,
    ("Mongoose", "Mongoose"): 4, ("Lion", "Lion"): 4,
    # Enemies
    ("Cat", "Rat"): 0, ("Rat", "Cat"): 0,
    ("Cow", "Tiger"): 0, ("Tiger", "Cow"): 0,
    ("Horse", "Buffalo"): 0, ("Buffalo", "Horse"): 0,
    ("Dog", "Deer"): 0, ("Deer", "Dog"): 0,
    ("Serpent", "Mongoose"): 0, ("Mongoose", "Serpent"): 0,
    ("Monkey", "Sheep"): 0, ("Sheep", "Monkey"): 0,
    ("Lion", "Elephant"): 0, ("Elephant", "Lion"): 0,
}

# Sign data
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# Sign lords
SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
              "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

# Planet friendships
PLANET_FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"]
}

PLANET_ENEMIES = {
    "Sun": ["Saturn", "Venus"],
    "Moon": [],
    "Mars": ["Mercury"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Moon"],
    "Saturn": ["Sun", "Moon", "Mars"]
}


@dataclass
class KootaResult:
    """Result for a single koota"""
    name: str
    max_points: float
    obtained_points: float
    description: str
    quality: str  # 'good', 'average', 'poor'


@dataclass
class CompatibilityResult:
    """Complete compatibility result"""
    total_points: float
    max_points: float
    percentage: float
    kootas: List[KootaResult]
    doshas: List[Dict]
    recommendation: str
    detailed_analysis: Dict


class AshtakootMilan:
    """
    Complete Ashtakoot (8-fold) Matching System
    
    Eight aspects analyzed:
    1. Varna (Caste) - 1 point
    2. Vashya (Dominance) - 2 points
    3. Tara (Destiny) - 3 points
    4. Yoni (Nature) - 4 points
    5. Graha Maitri (Planetary friendship) - 5 points
    6. Gana (Temperament) - 6 points
    7. Bhakoot (Love) - 7 points
    8. Nadi (Health/Progeny) - 8 points
    
    Total: 36 points
    """
    
    def __init__(self):
        pass
    
    def calculate_compatibility(
        self,
        boy_moon_lon: float,
        girl_moon_lon: float
    ) -> CompatibilityResult:
        """
        Calculate complete Ashtakoot compatibility
        
        Args:
            boy_moon_lon: Boy's Moon longitude
            girl_moon_lon: Girl's Moon longitude
            
        Returns:
            Complete compatibility analysis
        """
        # Get nakshatras and signs
        boy_nak = int(boy_moon_lon / (360 / 27))
        girl_nak = int(girl_moon_lon / (360 / 27))
        boy_sign = int(boy_moon_lon / 30)
        girl_sign = int(girl_moon_lon / 30)
        
        kootas = []
        doshas = []
        
        # 1. Varna Koota (1 point)
        varna = self._check_varna(boy_sign, girl_sign)
        kootas.append(varna)
        
        # 2. Vashya Koota (2 points)
        vashya = self._check_vashya(boy_sign, girl_sign)
        kootas.append(vashya)
        
        # 3. Tara Koota (3 points)
        tara = self._check_tara(boy_nak, girl_nak)
        kootas.append(tara)
        
        # 4. Yoni Koota (4 points)
        yoni = self._check_yoni(boy_nak, girl_nak)
        kootas.append(yoni)
        
        # 5. Graha Maitri (5 points)
        maitri = self._check_graha_maitri(boy_sign, girl_sign)
        kootas.append(maitri)
        
        # 6. Gana Koota (6 points)
        gana = self._check_gana(boy_nak, girl_nak)
        kootas.append(gana)
        
        # 7. Bhakoot Koota (7 points)
        bhakoot = self._check_bhakoot(boy_sign, girl_sign)
        kootas.append(bhakoot)
        if bhakoot.obtained_points == 0:
            doshas.append({
                "name": "Bhakoot Dosha",
                "severity": "high",
                "description": "6-8 or 2-12 relationship between Moon signs",
                "remedies": ["Specific poojas", "Matching other factors well"]
            })
        
        # 8. Nadi Koota (8 points)
        nadi = self._check_nadi(boy_nak, girl_nak)
        kootas.append(nadi)
        if nadi.obtained_points == 0:
            doshas.append({
                "name": "Nadi Dosha",
                "severity": "high",
                "description": "Same Nadi - affects health and progeny",
                "remedies": ["Nadi Nivarana Pooja", "Donation"]
            })
        
        # Calculate totals
        total = sum(k.obtained_points for k in kootas)
        max_total = 36.0
        percentage = (total / max_total) * 100
        
        # Generate recommendation
        recommendation = self._get_recommendation(total, doshas)
        
        # Detailed analysis
        detailed = {
            "boy": {
                "moon_sign": SIGNS[boy_sign],
                "nakshatra": NAKSHATRAS[boy_nak],
                "nadi": NAKSHATRA_NADI[boy_nak],
                "gana": NAKSHATRA_GANA[boy_nak]
            },
            "girl": {
                "moon_sign": SIGNS[girl_sign],
                "nakshatra": NAKSHATRAS[girl_nak],
                "nadi": NAKSHATRA_NADI[girl_nak],
                "gana": NAKSHATRA_GANA[girl_nak]
            }
        }
        
        return CompatibilityResult(
            total_points=total,
            max_points=max_total,
            percentage=percentage,
            kootas=kootas,
            doshas=doshas,
            recommendation=recommendation,
            detailed_analysis=detailed
        )
    
    def _check_varna(self, boy_sign: int, girl_sign: int) -> KootaResult:
        """
        Varna Koota (1 point)
        
        Varnas: Brahmin (Cancer, Scorpio, Pisces), Kshatriya (Aries, Leo, Sagittarius),
        Vaishya (Taurus, Virgo, Capricorn), Shudra (Gemini, Libra, Aquarius)
        
        Boy's varna should be >= Girl's varna
        """
        varna_map = {
            0: 2, 1: 1, 2: 0, 3: 3,   # Aries=Ksha, Taurus=Vai, Gemini=Shu, Cancer=Bra
            4: 2, 5: 1, 6: 0, 7: 3,   # Leo=Ksha, Virgo=Vai, Libra=Shu, Scorpio=Bra
            8: 2, 9: 1, 10: 0, 11: 3  # Sagi=Ksha, Capri=Vai, Aqua=Shu, Pisces=Bra
        }
        
        boy_varna = varna_map[boy_sign]
        girl_varna = varna_map[girl_sign]
        
        if boy_varna >= girl_varna:
            points = 1.0
            quality = "good"
            desc = "Boy's varna is equal or higher - Compatible"
        else:
            points = 0.0
            quality = "poor"
            desc = "Girl's varna is higher - May have ego issues"
        
        return KootaResult("Varna", 1.0, points, desc, quality)
    
    def _check_vashya(self, boy_sign: int, girl_sign: int) -> KootaResult:
        """
        Vashya Koota (2 points)
        
        Types: Chatushpada (quadruped), Dwipad (biped), Jalchar (aquatic),
        Vanchar (wild), Keet (insect)
        """
        vashya_map = {
            0: "chatushpada", 1: "chatushpada", 2: "dwipad", 3: "jalchar",
            4: "vanchar", 5: "dwipad", 6: "dwipad", 7: "keet",
            8: "dwipad", 9: "chatushpada", 10: "dwipad", 11: "jalchar"
        }
        
        boy_vashya = vashya_map[boy_sign]
        girl_vashya = vashya_map[girl_sign]
        
        # Same type = 2, Compatible = 1, Others = 0.5, Enemy = 0
        if boy_vashya == girl_vashya:
            points = 2.0
            quality = "good"
            desc = "Same Vashya - Excellent mutual control"
        elif (boy_vashya == "dwipad" and girl_vashya in ["chatushpada", "jalchar"]):
            points = 1.0
            quality = "average"
            desc = "Partial Vashya - Moderate control"
        else:
            points = 0.5
            quality = "average"
            desc = "Different Vashya - Some adjustment needed"
        
        return KootaResult("Vashya", 2.0, points, desc, quality)
    
    def _check_tara(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """
        Tara Koota (3 points)
        
        Based on counting nakshatras from one to another
        """
        # Count from girl to boy
        count1 = (boy_nak - girl_nak + 27) % 27
        tara1 = (count1 % 9) + 1
        
        # Count from boy to girl
        count2 = (girl_nak - boy_nak + 27) % 27
        tara2 = (count2 % 9) + 1
        
        # Inauspicious taras: 3, 5, 7
        bad_taras = [3, 5, 7]
        
        if tara1 not in bad_taras and tara2 not in bad_taras:
            points = 3.0
            quality = "good"
            desc = "Both taras auspicious - Excellent"
        elif tara1 not in bad_taras or tara2 not in bad_taras:
            points = 1.5
            quality = "average"
            desc = "One tara auspicious - Moderate"
        else:
            points = 0.0
            quality = "poor"
            desc = "Both taras inauspicious - Challenges"
        
        return KootaResult("Tara", 3.0, points, desc, quality)
    
    def _check_yoni(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """
        Yoni Koota (4 points)
        
        Animal compatibility based on nakshatra
        """
        boy_yoni = NAKSHATRA_YONI[boy_nak]
        girl_yoni = NAKSHATRA_YONI[girl_nak]
        
        boy_animal = boy_yoni[0]
        girl_animal = girl_yoni[0]
        boy_gender = boy_yoni[1]
        girl_gender = girl_yoni[1]
        
        # Check compatibility
        key = (boy_animal, girl_animal)
        rev_key = (girl_animal, boy_animal)
        
        if key in YONI_COMPAT:
            points = float(YONI_COMPAT[key])
        elif rev_key in YONI_COMPAT:
            points = float(YONI_COMPAT[rev_key])
        elif boy_animal == girl_animal:
            # Same animal, check gender
            if boy_gender != girl_gender:
                points = 4.0
            else:
                points = 3.0
        else:
            # Neutral
            points = 2.0
        
        if points >= 3:
            quality = "good"
            desc = f"Yoni compatible ({boy_animal} & {girl_animal})"
        elif points >= 1:
            quality = "average"
            desc = f"Yoni neutral ({boy_animal} & {girl_animal})"
        else:
            quality = "poor"
            desc = f"Yoni enemies ({boy_animal} & {girl_animal})"
        
        return KootaResult("Yoni", 4.0, points, desc, quality)
    
    def _check_graha_maitri(self, boy_sign: int, girl_sign: int) -> KootaResult:
        """
        Graha Maitri Koota (5 points)
        
        Planetary friendship between sign lords
        """
        boy_lord = SIGN_LORDS[boy_sign]
        girl_lord = SIGN_LORDS[girl_sign]
        
        if boy_lord == girl_lord:
            points = 5.0
            quality = "good"
            desc = "Same lord - Excellent friendship"
        elif girl_lord in PLANET_FRIENDS.get(boy_lord, []) and boy_lord in PLANET_FRIENDS.get(girl_lord, []):
            points = 5.0
            quality = "good"
            desc = "Mutual friends - Very good"
        elif girl_lord in PLANET_FRIENDS.get(boy_lord, []) or boy_lord in PLANET_FRIENDS.get(girl_lord, []):
            points = 4.0
            quality = "good"
            desc = "One-sided friendship - Good"
        elif girl_lord in PLANET_ENEMIES.get(boy_lord, []) or boy_lord in PLANET_ENEMIES.get(girl_lord, []):
            points = 0.0
            quality = "poor"
            desc = f"{boy_lord} and {girl_lord} are enemies"
        else:
            points = 2.5
            quality = "average"
            desc = "Neutral relationship"
        
        return KootaResult("Graha Maitri", 5.0, points, desc, quality)
    
    def _check_gana(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """
        Gana Koota (6 points)
        
        Temperament matching: Deva, Manushya, Rakshasa
        """
        boy_gana = NAKSHATRA_GANA[boy_nak]
        girl_gana = NAKSHATRA_GANA[girl_nak]
        
        if boy_gana == girl_gana:
            points = 6.0
            quality = "good"
            desc = f"Same Gana ({boy_gana}) - Excellent"
        elif boy_gana == "Deva" and girl_gana == "Manushya":
            points = 5.0
            quality = "good"
            desc = "Deva-Manushya - Good"
        elif boy_gana == "Manushya" and girl_gana == "Deva":
            points = 5.0
            quality = "good"
            desc = "Manushya-Deva - Good"
        elif boy_gana == "Rakshasa" or girl_gana == "Rakshasa":
            if boy_gana != girl_gana:
                points = 0.0
                quality = "poor"
                desc = "Rakshasa with other Gana - Conflict likely"
            else:
                points = 6.0
                quality = "good"
                desc = "Both Rakshasa - Compatible"
        else:
            points = 3.0
            quality = "average"
            desc = "Mixed Gana - Some adjustment"
        
        return KootaResult("Gana", 6.0, points, desc, quality)
    
    def _check_bhakoot(self, boy_sign: int, girl_sign: int) -> KootaResult:
        """
        Bhakoot Koota (7 points)
        
        Moon sign relationship - most important after Nadi
        """
        diff = abs(boy_sign - girl_sign)
        if diff > 6:
            diff = 12 - diff
        
        # Problematic combinations: 2/12, 5/9, 6/8
        relationship = (boy_sign - girl_sign + 12) % 12 + 1
        
        bad_combos = [(2, 12), (12, 2), (6, 8), (8, 6)]
        # 5/9 is actually considered good in some traditions
        
        actual = ((boy_sign - girl_sign + 12) % 12 + 1, 
                  (girl_sign - boy_sign + 12) % 12 + 1)
        
        if actual in bad_combos or actual[::-1] in bad_combos:
            points = 0.0
            quality = "poor"
            desc = f"Bhakoot Dosha ({actual[0]}/{actual[1]}) - Challenges"
        elif diff in [0, 4, 5]:  # Same, 5th, 6th from each other
            points = 7.0
            quality = "good"
            desc = "Excellent Bhakoot - Harmonious"
        else:
            points = 3.5
            quality = "average"
            desc = "Moderate Bhakoot"
        
        return KootaResult("Bhakoot", 7.0, points, desc, quality)
    
    def _check_nadi(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """
        Nadi Koota (8 points)
        
        Most important koota - affects health and progeny
        """
        boy_nadi = NAKSHATRA_NADI[boy_nak]
        girl_nadi = NAKSHATRA_NADI[girl_nak]
        
        if boy_nadi != girl_nadi:
            points = 8.0
            quality = "good"
            desc = f"Different Nadi ({boy_nadi} & {girl_nadi}) - Excellent"
        else:
            points = 0.0
            quality = "poor"
            desc = f"Same Nadi ({boy_nadi}) - Nadi Dosha present"
        
        return KootaResult("Nadi", 8.0, points, desc, quality)
    
    def _get_recommendation(self, total: float, doshas: List) -> str:
        """Generate recommendation based on score"""
        if total >= 28:
            if not doshas:
                return "Excellent match! Highly recommended for marriage."
            else:
                return f"Very good match with {len(doshas)} dosha(s). Remedies recommended."
        elif total >= 21:
            if not doshas:
                return "Good match. Compatible for marriage."
            else:
                return "Average match with some doshas. Consider remedies."
        elif total >= 18:
            return "Below average. Careful consideration needed."
        else:
            return "Not recommended without strong remedial measures."


class ManglikDosha:
    """
    Manglik Dosha (Kuja Dosha) Analysis
    """
    
    MANGLIK_HOUSES = [1, 2, 4, 7, 8, 12]
    
    def check_manglik(
        self,
        mars_house: int,
        ascendant_sign: int
    ) -> Dict[str, Any]:
        """
        Check for Manglik Dosha
        
        Mars in 1, 2, 4, 7, 8, or 12 from Lagna/Moon/Venus = Manglik
        """
        is_manglik = mars_house in self.MANGLIK_HOUSES
        
        # Check for cancellation
        cancellation = []
        
        # Mars in own sign (Aries, Scorpio)
        if ascendant_sign in [0, 7]:
            cancellation.append("Mars in own sign")
        
        # Mars in friendly signs
        if ascendant_sign in [3, 4, 8, 11]:  # Cancer, Leo, Sagittarius, Pisces
            cancellation.append("Mars in friendly sign")
        
        severity = "high"
        if cancellation:
            severity = "low" if len(cancellation) >= 2 else "medium"
        
        return {
            "is_manglik": is_manglik,
            "mars_house": mars_house,
            "severity": severity if is_manglik else "none",
            "cancellation_factors": cancellation,
            "recommendation": self._get_manglik_recommendation(is_manglik, severity)
        }
    
    def _get_manglik_recommendation(self, is_manglik: bool, severity: str) -> str:
        """Get recommendation for Manglik"""
        if not is_manglik:
            return "No Manglik Dosha present."
        
        if severity == "low":
            return "Mild Manglik - Can marry non-Manglik with some remedies."
        elif severity == "medium":
            return "Moderate Manglik - Better to match with Manglik or perform remedies."
        else:
            return "Strong Manglik - Should marry Manglik partner or perform Kumbh Vivah."


class DashakootMilan:
    """
    Dashakoot (10-fold) Matching System
    
    South Indian tradition with 10 kootas (total 50 points):
    1. Dina (Nakshatra) - 3 points
    2. Gana - 6 points  
    3. Mahendra - 3 points
    4. Stree Deergha - 3 points
    5. Yoni - 4 points
    6. Rasi (Bhakoot) - 7 points
    7. Rasi Lord (Graha Maitri) - 5 points
    8. Vasya - 2 points
    9. Rajju - 8 points
    10. Vedha - 9 points (absence of vedha = points)
    """
    
    # Rajju classification (body parts)
    # Rajju dosha occurs when both nakshatras fall in same Rajju
    NAKSHATRA_RAJJU = {
        # Paada (Feet): 1, 5, 12, 14, 21, 25
        "paada": [0, 4, 11, 13, 20, 24],  # 0-indexed
        # Kati (Waist): 2, 6, 13, 15, 22, 26
        "kati": [1, 5, 12, 14, 21, 25],
        # Nabhi (Navel): 3, 7, 16, 23, 27
        "nabhi": [2, 6, 15, 22, 26],
        # Kantha (Neck): 4, 8, 10, 17, 19, 24
        "kantha": [3, 7, 9, 16, 18, 23],
        # Shira (Head): 9, 11, 18, 20
        "shira": [8, 10, 17, 19]
    }
    
    # Vedha (obstruction) pairs - these nakshatras should not match
    VEDHA_PAIRS = [
        (0, 17),   # Ashwini - Jyeshtha
        (1, 16),   # Bharani - Anuradha
        (2, 26),   # Krittika - Revati
        (3, 21),   # Rohini - Shravana
        (4, 22),   # Mrigashira - Dhanishta
        (5, 20),   # Ardra - Uttara Ashadha
        (6, 19),   # Punarvasu - Purva Ashadha
        (7, 18),   # Pushya - Mula
        (9, 12),   # Magha - Hasta
        (10, 11),  # P.Phalguni - U.Phalguni
        (13, 24),  # Chitra - P.Bhadrapada
        (14, 25),  # Swati - U.Bhadrapada
        (15, 23),  # Vishakha - Shatabhisha
    ]
    
    def __init__(self):
        pass
    
    def calculate_dashakoot(
        self,
        boy_moon_lon: float,
        girl_moon_lon: float
    ) -> Dict[str, Any]:
        """Calculate 10-fold compatibility"""
        boy_nak = int(boy_moon_lon / (360 / 27))
        girl_nak = int(girl_moon_lon / (360 / 27))
        boy_sign = int(boy_moon_lon / 30)
        girl_sign = int(girl_moon_lon / 30)
        
        kootas = []
        total = 0.0
        max_total = 50.0
        
        # 1. Dina Koota (3 points)
        dina = self._check_dina(boy_nak, girl_nak)
        kootas.append(dina)
        total += dina.obtained_points
        
        # 2. Gana Koota (6 points)
        gana = self._check_gana(boy_nak, girl_nak)
        kootas.append(gana)
        total += gana.obtained_points
        
        # 3. Mahendra (3 points)
        mahendra = self._check_mahendra(boy_nak, girl_nak)
        kootas.append(mahendra)
        total += mahendra.obtained_points
        
        # 4. Stree Deergha (3 points)
        stree_deergha = self._check_stree_deergha(boy_nak, girl_nak)
        kootas.append(stree_deergha)
        total += stree_deergha.obtained_points
        
        # 5. Yoni (4 points) - same as Ashtakoot
        yoni = self._check_yoni(boy_nak, girl_nak)
        kootas.append(yoni)
        total += yoni.obtained_points
        
        # 6. Rasi/Bhakoot (7 points)
        rasi = self._check_rasi(boy_sign, girl_sign)
        kootas.append(rasi)
        total += rasi.obtained_points
        
        # 7. Rasi Lord (5 points)
        rasi_lord = self._check_rasi_lord(boy_sign, girl_sign)
        kootas.append(rasi_lord)
        total += rasi_lord.obtained_points
        
        # 8. Vasya (2 points)
        vasya = self._check_vasya(boy_sign, girl_sign)
        kootas.append(vasya)
        total += vasya.obtained_points
        
        # 9. Rajju (8 points)
        rajju = self._check_rajju(boy_nak, girl_nak)
        kootas.append(rajju)
        total += rajju.obtained_points
        
        # 10. Vedha (9 points)
        vedha = self._check_vedha(boy_nak, girl_nak)
        kootas.append(vedha)
        total += vedha.obtained_points
        
        percentage = (total / max_total) * 100
        
        return {
            "system": "Dashakoot",
            "total_points": total,
            "max_points": max_total,
            "percentage": round(percentage, 1),
            "kootas": [
                {
                    "name": k.name,
                    "max": k.max_points,
                    "obtained": k.obtained_points,
                    "quality": k.quality,
                    "description": k.description
                }
                for k in kootas
            ],
            "recommendation": self._get_recommendation(total, percentage)
        }
    
    def _check_dina(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """Dina Koota - Nakshatra compatibility"""
        count = (boy_nak - girl_nak + 27) % 27
        tara = (count % 9) + 1
        
        # Favorable taras: 1, 2, 4, 6, 8, 9
        favorable = [1, 2, 4, 6, 8, 9]
        
        if tara in favorable:
            return KootaResult("Dina", 3.0, 3.0, "Favorable Dina - Good", "good")
        elif tara in [3, 5]:
            return KootaResult("Dina", 3.0, 1.5, "Moderate Dina", "average")
        else:
            return KootaResult("Dina", 3.0, 0.0, "Unfavorable Dina", "poor")
    
    def _check_gana(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """Gana Koota - Same as Ashtakoot"""
        boy_gana = NAKSHATRA_GANA[boy_nak]
        girl_gana = NAKSHATRA_GANA[girl_nak]
        
        if boy_gana == girl_gana:
            return KootaResult("Gana", 6.0, 6.0, f"Same Gana ({boy_gana})", "good")
        elif (boy_gana == "Deva" and girl_gana == "Manushya") or \
             (boy_gana == "Manushya" and girl_gana == "Deva"):
            return KootaResult("Gana", 6.0, 5.0, "Deva-Manushya compatible", "good")
        elif "Rakshasa" in [boy_gana, girl_gana]:
            return KootaResult("Gana", 6.0, 0.0, "Rakshasa incompatible", "poor")
        else:
            return KootaResult("Gana", 6.0, 3.0, "Moderate Gana match", "average")
    
    def _check_mahendra(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """Mahendra Koota - For progeny and prosperity"""
        count = (boy_nak - girl_nak + 27) % 27
        
        # Favorable if boy's nakshatra is 4th, 7th, 10th, 13th, 16th, 19th, 22nd, 25th from girl's
        favorable_positions = [4, 7, 10, 13, 16, 19, 22, 25]
        
        if count in favorable_positions:
            return KootaResult("Mahendra", 3.0, 3.0, "Mahendra present - Prosperity", "good")
        else:
            return KootaResult("Mahendra", 3.0, 0.0, "Mahendra absent", "average")
    
    def _check_stree_deergha(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """Stree Deergha - For longevity of wife"""
        count = (boy_nak - girl_nak + 27) % 27
        
        # Boy's nakshatra should be at least 13 away from girl's
        if count >= 13:
            return KootaResult("Stree Deergha", 3.0, 3.0, "Stree Deergha fulfilled", "good")
        elif count >= 7:
            return KootaResult("Stree Deergha", 3.0, 1.5, "Partial Stree Deergha", "average")
        else:
            return KootaResult("Stree Deergha", 3.0, 0.0, "Stree Deergha not met", "poor")
    
    def _check_yoni(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """Yoni Koota - Animal compatibility"""
        boy_yoni = NAKSHATRA_YONI[boy_nak][0]
        girl_yoni = NAKSHATRA_YONI[girl_nak][0]
        
        if boy_yoni == girl_yoni:
            return KootaResult("Yoni", 4.0, 4.0, f"Same Yoni ({boy_yoni})", "good")
        
        key = (boy_yoni, girl_yoni)
        rev_key = (girl_yoni, boy_yoni)
        
        if key in YONI_COMPAT or rev_key in YONI_COMPAT:
            score = YONI_COMPAT.get(key, YONI_COMPAT.get(rev_key, 2))
            quality = "good" if score >= 3 else "poor" if score == 0 else "average"
            return KootaResult("Yoni", 4.0, float(score), f"{boy_yoni}-{girl_yoni}", quality)
        
        return KootaResult("Yoni", 4.0, 2.0, "Neutral Yoni", "average")
    
    def _check_rasi(self, boy_sign: int, girl_sign: int) -> KootaResult:
        """Rasi/Bhakoot Koota"""
        diff = abs(boy_sign - girl_sign)
        if diff > 6:
            diff = 12 - diff
        
        # 6/8 and 2/12 are bad
        rel = (boy_sign - girl_sign + 12) % 12 + 1
        
        if diff in [0, 4, 5]:  # Same, 5th, 6th
            return KootaResult("Rasi", 7.0, 7.0, "Excellent Rasi match", "good")
        elif rel in [2, 6, 8, 12]:
            return KootaResult("Rasi", 7.0, 0.0, f"Rasi Dosha ({rel}th)", "poor")
        else:
            return KootaResult("Rasi", 7.0, 3.5, "Moderate Rasi", "average")
    
    def _check_rasi_lord(self, boy_sign: int, girl_sign: int) -> KootaResult:
        """Rasi Lord compatibility"""
        boy_lord = SIGN_LORDS[boy_sign]
        girl_lord = SIGN_LORDS[girl_sign]
        
        if boy_lord == girl_lord:
            return KootaResult("Rasi Lord", 5.0, 5.0, "Same lord", "good")
        elif girl_lord in PLANET_FRIENDS.get(boy_lord, []):
            return KootaResult("Rasi Lord", 5.0, 4.0, "Friendly lords", "good")
        elif girl_lord in PLANET_ENEMIES.get(boy_lord, []):
            return KootaResult("Rasi Lord", 5.0, 0.0, "Enemy lords", "poor")
        else:
            return KootaResult("Rasi Lord", 5.0, 2.5, "Neutral lords", "average")
    
    def _check_vasya(self, boy_sign: int, girl_sign: int) -> KootaResult:
        """Vasya Koota"""
        vashya_map = {
            0: "chatushpada", 1: "chatushpada", 2: "dwipad", 3: "jalchar",
            4: "vanchar", 5: "dwipad", 6: "dwipad", 7: "keet",
            8: "dwipad", 9: "chatushpada", 10: "dwipad", 11: "jalchar"
        }
        
        boy_v = vashya_map[boy_sign]
        girl_v = vashya_map[girl_sign]
        
        if boy_v == girl_v:
            return KootaResult("Vasya", 2.0, 2.0, "Same Vasya", "good")
        elif boy_v == "dwipad":
            return KootaResult("Vasya", 2.0, 1.0, "Partial Vasya", "average")
        else:
            return KootaResult("Vasya", 2.0, 0.5, "Different Vasya", "average")
    
    def _check_rajju(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """Rajju Koota - Most important, affects longevity"""
        boy_rajju = None
        girl_rajju = None
        
        for rajju_type, nakshatras in self.NAKSHATRA_RAJJU.items():
            if boy_nak in nakshatras:
                boy_rajju = rajju_type
            if girl_nak in nakshatras:
                girl_rajju = rajju_type
        
        if boy_rajju is None or girl_rajju is None:
            return KootaResult("Rajju", 8.0, 8.0, "Rajju not applicable", "good")
        
        if boy_rajju != girl_rajju:
            return KootaResult("Rajju", 8.0, 8.0, "Different Rajju - Safe", "good")
        else:
            rajju_desc = {
                "paada": "Paada Rajju - Affects travel",
                "kati": "Kati Rajju - Affects prosperity",
                "nabhi": "Nabhi Rajju - Affects children",
                "kantha": "Kantha Rajju - Affects family",
                "shira": "Shira Rajju - Affects longevity"
            }
            return KootaResult("Rajju", 8.0, 0.0, rajju_desc.get(boy_rajju, "Same Rajju"), "poor")
    
    def _check_vedha(self, boy_nak: int, girl_nak: int) -> KootaResult:
        """Vedha Koota - Obstruction check"""
        pair = (min(boy_nak, girl_nak), max(boy_nak, girl_nak))
        
        for vedha_pair in self.VEDHA_PAIRS:
            sorted_vedha = (min(vedha_pair), max(vedha_pair))
            if pair == sorted_vedha:
                return KootaResult("Vedha", 9.0, 0.0, "Vedha Dosha present", "poor")
        
        return KootaResult("Vedha", 9.0, 9.0, "No Vedha - Good", "good")
    
    def _get_recommendation(self, total: float, percentage: float) -> str:
        """Get recommendation based on Dashakoot score"""
        if percentage >= 70:
            return "Excellent match by Dashakoot. Highly recommended."
        elif percentage >= 55:
            return "Good match. Compatible for marriage."
        elif percentage >= 40:
            return "Average match. Some remedies may help."
        else:
            return "Below average. Careful consideration needed."


def calculate_compatibility(
    boy_moon_lon: float,
    girl_moon_lon: float,
    boy_mars_house: int = None,
    girl_mars_house: int = None,
    system: str = "ashtakoot"
) -> Dict[str, Any]:
    """
    Complete compatibility analysis
    
    Args:
        boy_moon_lon: Boy's Moon longitude
        girl_moon_lon: Girl's Moon longitude
        boy_mars_house: Boy's Mars house (for Manglik check)
        girl_mars_house: Girl's Mars house (for Manglik check)
        system: "ashtakoot" (36 points), "dashakoot" (50 points), or "both"
        
    Returns:
        Complete compatibility analysis
    """
    output = {}
    
    if system in ["ashtakoot", "both"]:
        ashtakoot = AshtakootMilan()
        result = ashtakoot.calculate_compatibility(boy_moon_lon, girl_moon_lon)
        
        output["ashtakoot"] = {
            "total_score": result.total_points,
            "max_score": result.max_points,
            "percentage": round(result.percentage, 1),
            "recommendation": result.recommendation,
            "kootas": [
                {
                    "name": k.name,
                    "max": k.max_points,
                    "obtained": k.obtained_points,
                    "quality": k.quality,
                    "description": k.description
                }
                for k in result.kootas
            ],
            "doshas": result.doshas,
            "detailed_analysis": result.detailed_analysis
        }
    
    if system in ["dashakoot", "both"]:
        dashakoot = DashakootMilan()
        output["dashakoot"] = dashakoot.calculate_dashakoot(boy_moon_lon, girl_moon_lon)
    
    # For backward compatibility, if only ashtakoot requested, flatten
    if system == "ashtakoot":
        output = output["ashtakoot"]
    
    # Add Manglik analysis if Mars houses provided
    if boy_mars_house is not None:
        manglik = ManglikDosha()
        if isinstance(output, dict) and "ashtakoot" in output:
            output["boy_manglik"] = manglik.check_manglik(boy_mars_house, 0)
        else:
            output["boy_manglik"] = manglik.check_manglik(boy_mars_house, 0)
    
    if girl_mars_house is not None:
        manglik = ManglikDosha()
        if isinstance(output, dict) and "ashtakoot" in output:
            output["girl_manglik"] = manglik.check_manglik(girl_mars_house, 0)
        else:
            output["girl_manglik"] = manglik.check_manglik(girl_mars_house, 0)
    
    return output
