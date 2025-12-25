"""Bhava (House) Strength Analysis
===================================
Comprehensive house strength analysis per traditional Jyotish.

Reference Texts:
- Brihat Parashara Hora Shastra (BPHS), Chapters on Bhava Bala
- Phaladeepika, Chapter 3 (House Strength)
- Saravali, Chapter 2
- Jataka Parijata, Chapter 1

Bhava Bala Components:
1. Bhavadhipati Bala (Lord's strength)
2. Bhava Drishti (Aspectual strength)
3. Bhava Ashtakavarga (from Sarvashtakavarga)
4. Planets in Bhava
5. Karakas in Bhava
6. Bhava Sandhi (cusp considerations)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class BhavaStrength(Enum):
    """Strength levels for houses"""
    EXCELLENT = "Excellent"
    VERY_STRONG = "Very Strong"
    STRONG = "Strong"
    MODERATE = "Moderate"
    WEAK = "Weak"
    VERY_WEAK = "Very Weak"


@dataclass
class BhavaAnalysisResult:
    """Complete Bhava analysis result"""
    house_number: int
    house_name: str
    significations: List[str]
    strength: BhavaStrength
    strength_percentage: float
    lord: str
    lord_position: int
    lord_strength: float
    planets_in_house: List[str]
    aspects_received: List[Dict[str, Any]]
    ashtakavarga_bindus: int
    karakas_in_house: List[str]
    is_dusthana: bool
    is_trikona: bool
    is_kendra: bool
    is_upachaya: bool
    papa_kartari: bool  # Hemmed by malefics
    shubha_kartari: bool  # Hemmed by benefics
    interpretation: str
    recommendations: List[str]


class BhavaAnalyzer:
    """Comprehensive Bhava (house) strength analyzer"""
    
    # House significations per BPHS and classical texts
    HOUSE_SIGNIFICATIONS = {
        1: {
            'name': 'Lagna (Self)',
            'significations': [
                'Physical body, health, vitality',
                'Personality, character, temperament',
                'Overall life direction',
                'Birth, beginning of life',
                'Head and face (body part)',
                'Self-realization, ego'
            ],
            'karaka': 'Sun (Atmakaraka for self)'
        },
        2: {
            'name': 'Dhana Bhava (Wealth)',
            'significations': [
                'Wealth, assets, possessions',
                'Family, especially immediate family',
                'Speech, voice, communication style',
                'Food, eating habits',
                'Face, right eye (body part)',
                'Early childhood, values'
            ],
            'karaka': 'Jupiter (wealth), Venus (family)'
        },
        3: {
            'name': 'Sahaja Bhava (Courage)',
            'significations': [
                'Siblings, especially younger',
                'Courage, valor, efforts',
                'Short journeys, neighbors',
                'Communication, writing, media',
                'Right ear, shoulders, arms (body part)',
                'Hobbies, interests'
            ],
            'karaka': 'Mars (courage, siblings)'
        },
        4: {
            'name': 'Sukha Bhava (Mother)',
            'significations': [
                'Mother, maternal relatives',
                'Home, property, vehicles',
                'Education (early), schooling',
                'Happiness, mental peace',
                'Chest, heart, lungs (body part)',
                'Homeland, patriotism'
            ],
            'karaka': 'Moon (mother), Mercury (education)'
        },
        5: {
            'name': 'Putra Bhava (Children)',
            'significations': [
                'Children, progeny',
                'Creativity, intelligence, intellect',
                'Past life merits (Poorva Punya)',
                'Romance, love affairs',
                'Stomach (body part)',
                'Speculation, investments',
                'Mantras, spiritual practices'
            ],
            'karaka': 'Jupiter (children, intelligence)'
        },
        6: {
            'name': 'Ripu/Roga Bhava (Enemies)',
            'significations': [
                'Enemies, competitors, litigation',
                'Diseases, health problems',
                'Debts, loans, obstacles',
                'Service, employees, servants',
                'Lower abdomen, intestines (body part)',
                'Maternal uncle',
                'Daily work, routine'
            ],
            'karaka': 'Mars (enemies), Saturn (obstacles)'
        },
        7: {
            'name': 'Kalatra Bhava (Spouse)',
            'significations': [
                'Spouse, marriage, partnerships',
                'Business partnerships',
                'Long-term relationships',
                'Sexual organs (body part)',
                'Death (Maraka house)',
                'Trade, commerce',
                'Foreign residence'
            ],
            'karaka': 'Venus (wife), Jupiter (husband)'
        },
        8: {
            'name': 'Ayur Bhava (Longevity)',
            'significations': [
                'Longevity, lifespan',
                'Death, transformation',
                'Inheritance, legacy, insurance',
                'Occult, mysticism, research',
                'Chronic diseases',
                'Sexual organs (body part)',
                'Sudden events, accidents',
                'In-laws wealth'
            ],
            'karaka': 'Saturn (longevity), Mars (death)'
        },
        9: {
            'name': 'Dharma/Bhagya Bhava (Fortune)',
            'significations': [
                'Father, paternal lineage',
                'Fortune, luck, destiny',
                'Dharma, religion, spirituality',
                'Long journeys, pilgrimage',
                'Higher education, philosophy',
                'Thighs (body part)',
                'Guru, teacher, preceptor',
                'Past life credits'
            ],
            'karaka': 'Sun (father), Jupiter (dharma, fortune)'
        },
        10: {
            'name': 'Karma Bhava (Career)',
            'significations': [
                'Career, profession, livelihood',
                'Status, reputation, fame',
                'Authority, power, government',
                'Mother (Matri Karaka)',
                'Knees (body part)',
                'Actions, deeds (Karma)',
                'Public life, social standing'
            ],
            'karaka': 'Sun (authority), Mercury (career), Jupiter (career), Saturn (work)'
        },
        11: {
            'name': 'Labha Bhava (Gains)',
            'significations': [
                'Gains, income, profits',
                'Fulfillment of desires',
                'Elder siblings',
                'Friends, social circle',
                'Left ear, ankles (body part)',
                'Opportunities, windfalls',
                'Recovery from illness'
            ],
            'karaka': 'Jupiter (gains)'
        },
        12: {
            'name': 'Vyaya Bhava (Loss)',
            'significations': [
                'Losses, expenses, expenditure',
                'Foreign lands, distant places',
                'Spirituality, moksha, liberation',
                'Bed pleasures, sexual enjoyment',
                'Feet (body part)',
                'Isolation, hospitalization',
                'Charitable donations',
                'Left eye, sleep'
            ],
            'karaka': 'Saturn (losses), Jupiter (moksha)'
        }
    }
    
    # House classifications
    KENDRA_HOUSES = [1, 4, 7, 10]  # Angular - strongest
    TRIKONA_HOUSES = [1, 5, 9]  # Trinal - most auspicious
    DUSTHANA_HOUSES = [6, 8, 12]  # Malefic houses
    UPACHAYA_HOUSES = [3, 6, 10, 11]  # Growth houses
    MARAKA_HOUSES = [2, 7]  # Death-inflicting
    
    # Sign lords
    SIGN_LORDS = {
        0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury",
        6: "Venus", 7: "Mars", 8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter"
    }
    
    def analyze_bhava(
        self,
        house_number: int,
        ascendant: float,
        planet_positions: Dict[str, float],
        planet_strengths: Dict[str, float],  # Shadbala
        ashtakavarga_bindus: Optional[int] = None,
        chara_karakas: Optional[Dict[str, str]] = None
    ) -> BhavaAnalysisResult:
        """Analyze single Bhava comprehensively
        
        Args:
            house_number: House to analyze (1-12)
            ascendant: Ascendant longitude
            planet_positions: Planet longitudes
            planet_strengths: Shadbala percentages
            ashtakavarga_bindus: Sarvashtakavarga bindus for this house
            chara_karakas: Jaimini Chara Karakas
            
        Returns:
            Complete Bhava analysis
        """
        # Get house sign
        house_sign = (int(ascendant / 30) + house_number - 1) % 12
        lord = self.SIGN_LORDS[house_sign]
        
        # Find lord's position
        lord_position = int(planet_positions.get(lord, 0) / 30)
        lord_house = ((lord_position - int(ascendant / 30)) % 12) + 1
        lord_strength = planet_strengths.get(lord, 0)
        
        # Find planets in this house
        planets_in_house = []
        for planet, lon in planet_positions.items():
            if int(lon / 30) == house_sign:
                planets_in_house.append(planet)
        
        # Check for Karakas
        karakas_in_house = []
        if chara_karakas:
            for karaka, planet in chara_karakas.items():
                if planet in planets_in_house:
                    karakas_in_house.append(f"{planet} ({karaka})")
        
        # Calculate aspects received (simplified)
        aspects = self._calculate_aspects_to_house(
            house_sign, planet_positions
        )
        
        # Check Papa/Shubha Kartari
        papa_kartari, shubha_kartari = self._check_kartari_yoga(
            house_sign, planet_positions
        )
        
        # Calculate overall strength
        strength_pct, strength_level = self._calculate_bhava_strength(
            lord_strength,
            len(planets_in_house),
            len(aspects),
            ashtakavarga_bindus,
            house_number
        )
        
        # Classifications
        is_kendra = house_number in self.KENDRA_HOUSES
        is_trikona = house_number in self.TRIKONA_HOUSES
        is_dusthana = house_number in self.DUSTHANA_HOUSES
        is_upachaya = house_number in self.UPACHAYA_HOUSES
        
        # Generate interpretation
        interpretation = self._interpret_bhava(
            house_number, strength_level, lord, lord_house,
            planets_in_house, papa_kartari, shubha_kartari,
            ashtakavarga_bindus
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            house_number, strength_level, lord, planets_in_house
        )
        
        house_data = self.HOUSE_SIGNIFICATIONS[house_number]
        
        return BhavaAnalysisResult(
            house_number=house_number,
            house_name=house_data['name'],
            significations=house_data['significations'],
            strength=strength_level,
            strength_percentage=strength_pct,
            lord=lord,
            lord_position=lord_house,
            lord_strength=lord_strength,
            planets_in_house=planets_in_house,
            aspects_received=aspects,
            ashtakavarga_bindus=ashtakavarga_bindus or 0,
            karakas_in_house=karakas_in_house,
            is_dusthana=is_dusthana,
            is_trikona=is_trikona,
            is_kendra=is_kendra,
            is_upachaya=is_upachaya,
            papa_kartari=papa_kartari,
            shubha_kartari=shubha_kartari,
            interpretation=interpretation,
            recommendations=recommendations
        )
    
    def _calculate_aspects_to_house(
        self,
        house_sign: int,
        planet_positions: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Calculate which planets aspect this house"""
        aspects = []
        
        for planet, lon in planet_positions.items():
            planet_sign = int(lon / 30)
            
            # 7th aspect (opposition)
            if (planet_sign + 6) % 12 == house_sign:
                aspects.append({
                    'planet': planet,
                    'aspect_type': '7th (Opposition)',
                    'strength': 1.0
                })
            
            # Special aspects
            if planet == 'Mars':
                # Mars aspects 4th and 8th
                if (planet_sign + 3) % 12 == house_sign:
                    aspects.append({'planet': 'Mars', 'aspect_type': '4th', 'strength': 0.75})
                if (planet_sign + 7) % 12 == house_sign:
                    aspects.append({'planet': 'Mars', 'aspect_type': '8th', 'strength': 1.0})
            
            elif planet == 'Jupiter':
                # Jupiter aspects 5th and 9th
                if (planet_sign + 4) % 12 == house_sign:
                    aspects.append({'planet': 'Jupiter', 'aspect_type': '5th', 'strength': 1.0})
                if (planet_sign + 8) % 12 == house_sign:
                    aspects.append({'planet': 'Jupiter', 'aspect_type': '9th', 'strength': 1.0})
            
            elif planet == 'Saturn':
                # Saturn aspects 3rd and 10th
                if (planet_sign + 2) % 12 == house_sign:
                    aspects.append({'planet': 'Saturn', 'aspect_type': '3rd', 'strength': 0.5})
                if (planet_sign + 9) % 12 == house_sign:
                    aspects.append({'planet': 'Saturn', 'aspect_type': '10th', 'strength': 1.0})
        
        return aspects
    
    def _check_kartari_yoga(
        self,
        house_sign: int,
        planet_positions: Dict[str, float]
    ) -> Tuple[bool, bool]:
        """Check for Papa Kartari (hemmed by malefics) or Shubha Kartari (benefics)"""
        prev_sign = (house_sign - 1 + 12) % 12
        next_sign = (house_sign + 1) % 12
        
        malefics = ['Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu']
        benefics = ['Jupiter', 'Venus', 'Mercury', 'Moon']
        
        prev_planets = [p for p, lon in planet_positions.items() if int(lon / 30) == prev_sign]
        next_planets = [p for p, lon in planet_positions.items() if int(lon / 30) == next_sign]
        
        papa_kartari = (any(p in malefics for p in prev_planets) and 
                       any(p in malefics for p in next_planets))
        
        shubha_kartari = (any(p in benefics for p in prev_planets) and 
                         any(p in benefics for p in next_planets))
        
        return papa_kartari, shubha_kartari
    
    def _calculate_bhava_strength(
        self,
        lord_strength: float,
        planet_count: int,
        aspect_count: int,
        av_bindus: Optional[int],
        house_number: int
    ) -> Tuple[float, BhavaStrength]:
        """Calculate overall Bhava strength"""
        # Base strength from lord (40% weight)
        strength = lord_strength * 0.4
        
        # Planets in house (20% weight)
        planet_factor = min(planet_count * 20, 20)
        strength += planet_factor
        
        # Aspects (15% weight)
        aspect_factor = min(aspect_count * 5, 15)
        strength += aspect_factor
        
        # Ashtakavarga (25% weight)
        if av_bindus:
            av_factor = (av_bindus / 30) * 25  # 30 is excellent
            strength += av_factor
        
        # Adjust for house type
        if house_number in self.TRIKONA_HOUSES:
            strength *= 1.1  # Trines naturally stronger
        elif house_number in self.DUSTHANA_HOUSES:
            strength *= 0.9  # Dusthanas naturally weaker
        
        # Classify strength
        if strength >= 80:
            level = BhavaStrength.EXCELLENT
        elif strength >= 70:
            level = BhavaStrength.VERY_STRONG
        elif strength >= 60:
            level = BhavaStrength.STRONG
        elif strength >= 45:
            level = BhavaStrength.MODERATE
        elif strength >= 30:
            level = BhavaStrength.WEAK
        else:
            level = BhavaStrength.VERY_WEAK
        
        return round(strength, 2), level
    
    def _interpret_bhava(
        self,
        house_num: int,
        strength: BhavaStrength,
        lord: str,
        lord_house: int,
        planets: List[str],
        papa_kartari: bool,
        shubha_kartari: bool,
        av_bindus: Optional[int]
    ) -> str:
        """Generate detailed interpretation"""
        house_data = self.HOUSE_SIGNIFICATIONS[house_num]
        
        base = f"**{house_data['name']} Analysis:**\n\n"
        
        # Strength assessment
        if strength == BhavaStrength.EXCELLENT:
            base += f"House strength: EXCELLENT ({av_bindus or 'N/A'} Ashtakavarga bindus). "
            base += f"Significations will manifest powerfully and favorably.\n\n"
        elif strength == BhavaStrength.VERY_STRONG:
            base += f"House strength: VERY STRONG. Good results in {', '.join(house_data['significations'][:2])}.\n\n"
        elif strength == BhavaStrength.STRONG:
            base += f"House strength: STRONG. Above-average results with consistent effort.\n\n"
        elif strength == BhavaStrength.MODERATE:
            base += f"House strength: MODERATE. Mixed results, requires patience and effort.\n\n"
        elif strength == BhavaStrength.WEAK:
            base += f"House strength: WEAK. Challenges likely in {', '.join(house_data['significations'][:2])}. Remedial measures recommended.\n\n"
        else:
            base += f"House strength: VERY WEAK. Significant obstacles. Strong remedial measures essential.\n\n"
        
        # Lord analysis
        base += f"Lord {lord} in {lord_house}th house: "
        if lord_house == house_num:
            base += "Excellent placement (lord in own house).\n"
        elif lord_house in self.TRIKONA_HOUSES:
            base += "Very favorable (lord in trine).\n"
        elif lord_house in self.KENDRA_HOUSES:
            base += "Strong (lord in kendra).\n"
        elif lord_house in self.DUSTHANA_HOUSES:
            base += "Challenging (lord in dusthana) - obstacles expected.\n"
        else:
            base += "Moderate placement.\n"
        
        # Planets in house
        if planets:
            base += f"\nPlanets in house: {', '.join(planets)}. "
            if any(p in ['Jupiter', 'Venus', 'Mercury'] for p in planets):
                base += "Benefic influence strengthens house. "
            if any(p in ['Saturn', 'Mars', 'Rahu', 'Ketu'] for p in planets):
                base += "Malefic influence requires careful handling. "
        
        # Kartari yogas
        if papa_kartari:
            base += "\n⚠️ Papa Kartari Yoga: House hemmed by malefics. Obstacles and delays likely. Remedies essential."
        if shubha_kartari:
            base += "\n✓ Shubha Kartari Yoga: House protected by benefics on both sides. Divine grace present."
        
        return base
    
    def _generate_recommendations(
        self,
        house_num: int,
        strength: BhavaStrength,
        lord: str,
        planets: List[str]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        
        if strength in [BhavaStrength.WEAK, BhavaStrength.VERY_WEAK]:
            recs.append(f"Strengthen house lord {lord} through gemstone/mantra")
            recs.append(f"Perform remedial charity on {lord}'s day")
            recs.append(f"Worship deity associated with {house_num}th house")
        
        if house_num in self.DUSTHANA_HOUSES:
            recs.append("Dusthana house - transform challenges into growth")
            recs.append("Regular spiritual practice recommended")
        
        if house_num in [5, 9]:  # Dharma houses
            recs.append("Strengthen through mantra japa and spiritual study")
        
        if house_num == 10:  # Career
            recs.append("Focus on Karma Yoga - selfless action")
            recs.append("Seek guidance from experienced mentors")
        
        return recs[:5]  # Limit to 5 recommendations
    
    def analyze_all_bhavas(
        self,
        ascendant: float,
        planet_positions: Dict[str, float],
        planet_strengths: Dict[str, float],
        sarvashtakavarga: Optional[List[int]] = None,
        chara_karakas: Optional[Dict[str, str]] = None
    ) -> Dict[int, BhavaAnalysisResult]:
        """Analyze all 12 houses"""
        results = {}
        
        for house_num in range(1, 13):
            av_bindus = sarvashtakavarga[house_num - 1] if sarvashtakavarga else None
            
            results[house_num] = self.analyze_bhava(
                house_num,
                ascendant,
                planet_positions,
                planet_strengths,
                av_bindus,
                chara_karakas
            )
        
        return results


def create_comprehensive_bhava_report(
    ascendant: float,
    planet_positions: Dict[str, float],
    planet_strengths: Dict[str, float],
    sarvashtakavarga: Optional[List[int]] = None,
    chara_karakas: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Create complete Bhava analysis report"""
    analyzer = BhavaAnalyzer()
    
    all_bhavas = analyzer.analyze_all_bhavas(
        ascendant,
        planet_positions,
        planet_strengths,
        sarvashtakavarga,
        chara_karakas
    )
    
    # Identify strongest and weakest houses
    sorted_bhavas = sorted(
        all_bhavas.items(),
        key=lambda x: x[1].strength_percentage,
        reverse=True
    )
    
    strongest = sorted_bhavas[:3]
    weakest = sorted_bhavas[-3:]
    
    return {
        'all_houses': {
            num: {
                'name': result.house_name,
                'strength': result.strength.value,
                'strength_percentage': result.strength_percentage,
                'lord': result.lord,
                'lord_house': result.lord_position,
                'planets': result.planets_in_house,
                'ashtakavarga_bindus': result.ashtakavarga_bindus,
                'interpretation': result.interpretation,
                'recommendations': result.recommendations
            }
            for num, result in all_bhavas.items()
        },
        'strongest_houses': [
            {
                'house': num,
                'name': result.house_name,
                'strength': result.strength_percentage
            }
            for num, result in strongest
        ],
        'weakest_houses': [
            {
                'house': num,
                'name': result.house_name,
                'strength': result.strength_percentage,
                'needs_remedies': True
            }
            for num, result in weakest
        ],
        'reference': 'BPHS Bhava Bala, Phaladeepika Chapter 3'
    }
