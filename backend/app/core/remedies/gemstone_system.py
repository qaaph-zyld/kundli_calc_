"""Gemstone Recommendation System
=================================
Traditional gemstone prescription per Vedic astrology texts.

Reference Texts:
- Brihat Samhita, Ratna Pariksha Chapter
- Garuda Purana, Ratna Adhyaya
- Jataka Parijata, Chapter 1
- Phala Deepika, Chapter 21
- Hora Shastra traditional texts

Mantras and procedures from:
- Mantra Mahodadhi
- Tantrasara
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class GemstoneQuality(Enum):
    """Gemstone quality grades"""
    UTTAM = "Uttam (Best)"
    MADHYAM = "Madhyam (Medium)"
    ADHAMA = "Adhama (Low)"


@dataclass
class GemstoneRecommendation:
    """Complete gemstone recommendation"""
    planet: str
    primary_gem: str
    substitute_gems: List[str]
    weight_range: str  # In carats
    metal: str
    finger: str
    day: str
    time: str  # Muhurta for wearing
    mantra: str
    mantra_count: int
    purification_procedure: str
    wearing_procedure: str
    effects: List[str]
    contraindications: List[str]
    reference: str


class GemstoneSystem:
    """Traditional gemstone recommendation system"""
    
    # Primary gemstones per planet (Ratna)
    # Reference: Brihat Samhita, Garuda Purana
    PRIMARY_GEMS = {
        'Sun': {
            'gem': 'Ruby',
            'sanskrit': 'Manikya',
            'substitute': ['Red Garnet', 'Red Spinel', 'Red Tourmaline'],
            'weight': '3-6 carats (minimum 3)',
            'metal': 'Gold or Copper',
            'finger': 'Ring finger (right hand)',
            'day': 'Sunday',
            'hora': 'Sun hora on Sunday morning',
            'mantra': 'Om Suryaya Namaha',
            'beej_mantra': 'Om Hraam Hreem Hraum Sah Suryaya Namah',
            'count': 7000,
            'effects': [
                'Strengthens vitality and confidence',
                'Improves leadership abilities',
                'Enhances father relationships',
                'Boosts career in government/authority',
                'Improves heart health and circulation'
            ]
        },
        'Moon': {
            'gem': 'Pearl',
            'sanskrit': 'Moti',
            'substitute': ['Moonstone', 'White Coral'],
            'weight': '4-7 carats (minimum 4)',
            'metal': 'Silver',
            'finger': 'Little finger (right hand)',
            'day': 'Monday',
            'hora': 'Moon hora on Monday evening',
            'mantra': 'Om Chandraya Namaha',
            'beej_mantra': 'Om Shraam Shreem Shraum Sah Chandraya Namah',
            'count': 11000,
            'effects': [
                'Enhances emotional stability',
                'Improves mental peace',
                'Strengthens mother relationships',
                'Benefits mind and memory',
                'Supports respiratory health'
            ]
        },
        'Mars': {
            'gem': 'Red Coral',
            'sanskrit': 'Moonga',
            'substitute': ['Carnelian', 'Red Agate'],
            'weight': '5-8 carats (minimum 5)',
            'metal': 'Gold or Copper',
            'finger': 'Ring finger (right hand)',
            'day': 'Tuesday',
            'hora': 'Mars hora on Tuesday morning',
            'mantra': 'Om Mangalaya Namaha',
            'beej_mantra': 'Om Kraam Kreem Kraum Sah Bhaumaya Namah',
            'count': 10000,
            'effects': [
                'Increases courage and confidence',
                'Improves energy and vitality',
                'Supports property matters',
                'Enhances sibling relationships',
                'Strengthens blood and muscles'
            ]
        },
        'Mercury': {
            'gem': 'Emerald',
            'sanskrit': 'Panna',
            'substitute': ['Green Tourmaline', 'Peridot', 'Green Jade'],
            'weight': '3-6 carats (minimum 3)',
            'metal': 'Gold or Silver',
            'finger': 'Little finger (right hand)',
            'day': 'Wednesday',
            'hora': 'Mercury hora on Wednesday morning',
            'mantra': 'Om Budhaya Namaha',
            'beej_mantra': 'Om Braam Breem Braum Sah Budhaya Namah',
            'count': 9000,
            'effects': [
                'Enhances intelligence and learning',
                'Improves communication skills',
                'Supports business and trade',
                'Benefits nervous system',
                'Strengthens analytical abilities'
            ]
        },
        'Jupiter': {
            'gem': 'Yellow Sapphire',
            'sanskrit': 'Pukhraj',
            'substitute': ['Yellow Topaz', 'Citrine'],
            'weight': '3-6 carats (minimum 3)',
            'metal': 'Gold',
            'finger': 'Index finger (right hand)',
            'day': 'Thursday',
            'hora': 'Jupiter hora on Thursday morning',
            'mantra': 'Om Gurave Namaha',
            'beej_mantra': 'Om Graam Greem Graum Sah Gurave Namah',
            'count': 19000,
            'effects': [
                'Enhances wisdom and knowledge',
                'Improves fortune and prosperity',
                'Supports children and education',
                'Benefits spiritual growth',
                'Strengthens liver and digestion'
            ]
        },
        'Venus': {
            'gem': 'Diamond',
            'sanskrit': 'Heera',
            'substitute': ['White Sapphire', 'White Zircon', 'Clear Quartz'],
            'weight': '1-2 carats (minimum 1)',
            'metal': 'Platinum, White Gold, or Silver',
            'finger': 'Middle finger (right hand)',
            'day': 'Friday',
            'hora': 'Venus hora on Friday morning',
            'mantra': 'Om Shukraya Namaha',
            'beej_mantra': 'Om Draam Dreem Draum Sah Shukraya Namah',
            'count': 16000,
            'effects': [
                'Enhances love and relationships',
                'Improves artistic abilities',
                'Supports marriage and partnerships',
                'Benefits reproductive health',
                'Increases luxury and comforts'
            ]
        },
        'Saturn': {
            'gem': 'Blue Sapphire',
            'sanskrit': 'Neelam',
            'substitute': ['Amethyst', 'Blue Spinel', 'Lapis Lazuli'],
            'weight': '4-7 carats (minimum 4)',
            'metal': 'Silver or Panchdhatu',
            'finger': 'Middle finger (right hand)',
            'day': 'Saturday',
            'hora': 'Saturn hora on Saturday evening',
            'mantra': 'Om Shanaischaraya Namaha',
            'beej_mantra': 'Om Praam Preem Praum Sah Shanaischaraya Namah',
            'count': 23000,
            'effects': [
                'Improves discipline and focus',
                'Supports career longevity',
                'Reduces obstacles gradually',
                'Benefits bones and joints',
                'Enhances spiritual detachment'
            ],
            'warning': 'Test for 3 days before permanent wearing. Can have strong immediate effects.'
        },
        'Rahu': {
            'gem': 'Hessonite Garnet',
            'sanskrit': 'Gomed',
            'substitute': ['Spessartine Garnet'],
            'weight': '5-8 carats (minimum 5)',
            'metal': 'Silver or Panchdhatu',
            'finger': 'Middle finger (right hand)',
            'day': 'Saturday',
            'hora': 'Rahu hora on Saturday',
            'mantra': 'Om Rahave Namaha',
            'beej_mantra': 'Om Bhraam Bhreem Bhraum Sah Rahave Namah',
            'count': 18000,
            'effects': [
                'Reduces confusion and illusions',
                'Supports foreign connections',
                'Improves unconventional success',
                'Benefits research and occult',
                'Helps with addictions and phobias'
            ]
        },
        'Ketu': {
            'gem': "Cat's Eye",
            'sanskrit': 'Vaidurya',
            'substitute': ['Tiger Eye'],
            'weight': '5-8 carats (minimum 5)',
            'metal': 'Silver or Gold',
            'finger': 'Middle finger (right hand)',
            'day': 'Wednesday or Thursday',
            'hora': 'Ketu hora',
            'mantra': 'Om Ketave Namaha',
            'beej_mantra': 'Om Sraam Sreem Sraum Sah Ketave Namah',
            'count': 17000,
            'effects': [
                'Enhances spiritual insight',
                'Supports moksha path',
                'Reduces sudden losses',
                'Benefits occult knowledge',
                'Improves intuition'
            ]
        }
    }
    
    def recommend_gemstone(
        self,
        planet: str,
        planet_strength: float,  # From Shadbala
        is_benefic: bool,
        mahadasha_planet: Optional[str] = None,
        specific_issue: Optional[str] = None
    ) -> GemstoneRecommendation:
        """Recommend gemstone for a planet
        
        Args:
            planet: Planet name
            planet_strength: Shadbala strength percentage
            is_benefic: Whether planet is functional benefic in chart
            mahadasha_planet: Current Mahadasha planet
            specific_issue: Specific area to address
            
        Returns:
            Complete gemstone recommendation with procedures
        """
        if planet not in self.PRIMARY_GEMS:
            raise ValueError(f"No gemstone data for {planet}")
        
        gem_data = self.PRIMARY_GEMS[planet]
        
        # Determine if gemstone is recommended
        should_recommend = self._should_recommend_gem(
            planet, planet_strength, is_benefic, mahadasha_planet
        )
        
        if not should_recommend:
            contraindications = [
                f"{planet} is strong enough (strength: {planet_strength}%)",
                "Gemstone may over-strengthen and cause imbalance",
                "Focus on other planets or remedies"
            ]
        else:
            contraindications = self._get_contraindications(planet, is_benefic)
        
        # Purification procedure (Shodhana)
        purification = self._get_purification_procedure(gem_data['gem'])
        
        # Wearing procedure
        wearing = self._get_wearing_procedure(
            gem_data['gem'],
            gem_data['metal'],
            gem_data['finger'],
            gem_data['day'],
            gem_data['hora'],
            gem_data['mantra'],
            gem_data['count']
        )
        
        return GemstoneRecommendation(
            planet=planet,
            primary_gem=gem_data['gem'],
            substitute_gems=gem_data['substitute'],
            weight_range=gem_data['weight'],
            metal=gem_data['metal'],
            finger=gem_data['finger'],
            day=gem_data['day'],
            time=gem_data['hora'],
            mantra=gem_data['beej_mantra'],
            mantra_count=gem_data['count'],
            purification_procedure=purification,
            wearing_procedure=wearing,
            effects=gem_data['effects'],
            contraindications=contraindications,
            reference="Brihat Samhita, Garuda Purana Ratna Adhyaya"
        )
    
    def _should_recommend_gem(
        self,
        planet: str,
        strength: float,
        is_benefic: bool,
        mahadasha: Optional[str]
    ) -> bool:
        """Determine if gemstone should be recommended"""
        # Don't recommend if planet is already very strong (>80%)
        if strength > 80:
            return False
        
        # Recommend if planet is weak (<50%) and benefic
        if strength < 50 and is_benefic:
            return True
        
        # Recommend if planet's Mahadasha is running
        if mahadasha == planet:
            return True
        
        # Recommend if moderate strength (50-70%) and benefic
        if 50 <= strength <= 70 and is_benefic:
            return True
        
        return False
    
    def _get_contraindications(self, planet: str, is_benefic: bool) -> List[str]:
        """Get contraindications for gemstone"""
        contraindications = []
        
        if not is_benefic:
            contraindications.append(
                f"{planet} is functional malefic - consult qualified astrologer before wearing"
            )
        
        if planet == 'Saturn':
            contraindications.append(
                "Blue Sapphire can have strong immediate effects - trial period mandatory"
            )
        
        if planet in ['Rahu', 'Ketu']:
            contraindications.append(
                "Shadow planet gemstone - requires careful consideration"
            )
        
        return contraindications
    
    def _get_purification_procedure(self, gem_name: str) -> str:
        """Get traditional purification procedure
        
        Reference: Garuda Purana, Ratna Shodhana
        """
        return f"""Traditional Purification (Shodhana) for {gem_name}:

1. Mix raw milk, Ganga water, honey, ghee, and sugar (Panchamrita)
2. Immerse the gemstone in this mixture overnight
3. Next morning, wash with clean water
4. Wipe with clean white cloth
5. Place on altar with flowers and incense
6. Recite planet's mantra 108 times
7. Gemstone is now purified and ready for energization

Alternative: Immerse in sea salt water for 24 hours, then wash and dry.

Note: Repeat purification every 6 months for maintaining energy."""
    
    def _get_wearing_procedure(
        self,
        gem: str,
        metal: str,
        finger: str,
        day: str,
        hora: str,
        mantra: str,
        count: int
    ) -> str:
        """Get complete wearing procedure with Muhurta"""
        return f"""Complete Wearing Procedure for {gem}:

**Preparation (1-2 days before):**
1. Fast or light vegetarian diet
2. Maintain cleanliness and positive thoughts
3. Purchase gemstone on auspicious day

**Day of Wearing ({day}):**

**Morning Procedure:**
1. Wake up early, take bath
2. Wear clean white or yellow clothes
3. Set up small altar facing East
4. Light lamp (ghee or oil) and incense

**Energization (during {hora}):**
5. Place ring/pendant on clean red cloth
6. Offer flowers, sandalwood paste, rice grains
7. Recite mantra "{mantra}" - {count} times
   (Minimum 108 times if cannot complete full count)
8. Offer the gemstone to deity with devotion
9. Touch to forehead (Ajna chakra) and heart

**Wearing:**
10. Wear on {finger} during {hora}
11. Visualize divine light entering the gemstone
12. Express gratitude to planet and seek blessings

**Post-Wearing:**
- Maintain purity for 24 hours (vegetarian food, no alcohol)
- Observe effects for first 3-7 days
- If positive effects, continue wearing
- If negative effects within 3 days, remove and consult astrologer

**Daily Maintenance:**
- Touch gemstone while reciting mantra (morning)
- Clean monthly with soft cloth
- Re-energize on {day} monthly with 108 mantras
- Never remove completely (can take off during sleep/bath)

**Metal Setting:** {metal} - ensures proper transmission of cosmic rays

**Important:** Gemstone works through cosmic ray transmission. Quality and purity are crucial."""
    
    def calculate_suitable_time(
        self,
        planet: str,
        location_lat: float,
        location_lon: float,
        start_date: datetime
    ) -> Dict[str, Any]:
        """Calculate auspicious time (Muhurta) for wearing gemstone
        
        Considers:
        - Planet's hora
        - Ascending planet's sign
        - Nakshatra
        - Tithi
        - Day of week
        
        Reference: Muhurta Chintamani
        """
        # This would integrate with Panchang calculator
        # For now, return general guidance
        
        gem_data = self.PRIMARY_GEMS[planet]
        
        return {
            'planet': planet,
            'gem': gem_data['gem'],
            'recommended_day': gem_data['day'],
            'recommended_hora': gem_data['hora'],
            'next_suitable_dates': 'Calculate using Panchang - avoid Rahu Kala, Yamaghanta',
            'nakshatra_to_avoid': self._get_incompatible_nakshatras(planet),
            'procedure': 'Wear during planet hora when planet in friendly sign'
        }
    
    def _get_incompatible_nakshatras(self, planet: str) -> List[str]:
        """Get nakshatras to avoid for gemstone wearing"""
        # Simplified - traditionally more complex
        incompatible = {
            'Sun': ['Bharani', 'Ashlesha', 'Jyeshtha'],
            'Moon': ['Ashwini', 'Magha', 'Mula'],
            'Mars': ['Rohini', 'Swati', 'Revati'],
            'Mercury': ['Krittika', 'Uttara Phalguni', 'Uttara Ashadha'],
            'Jupiter': ['Ardra', 'Chitra', 'Shatabhisha'],
            'Venus': ['Punarvasu', 'Vishakha', 'Purva Bhadrapada'],
            'Saturn': ['Pushya', 'Anuradha', 'Uttara Bhadrapada']
        }
        
        return incompatible.get(planet, [])


def recommend_gemstones_for_chart(
    planet_strengths: Dict[str, float],
    functional_benefics: List[str],
    current_mahadasha: str,
    specific_concerns: Optional[Dict[str, str]] = None
) -> Dict[str, GemstoneRecommendation]:
    """Recommend gemstones for entire chart
    
    Args:
        planet_strengths: Shadbala percentages for each planet
        functional_benefics: List of functional benefic planets
        current_mahadasha: Currently running Mahadasha planet
        specific_concerns: Optional dict of concerns (career, health, etc.)
        
    Returns:
        Gemstone recommendations for applicable planets
    """
    system = GemstoneSystem()
    recommendations = {}
    
    for planet, strength in planet_strengths.items():
        if planet in ['Rahu', 'Ketu']:
            # Only recommend for shadow planets if specifically needed
            continue
        
        is_benefic = planet in functional_benefics
        
        rec = system.recommend_gemstone(
            planet=planet,
            planet_strength=strength,
            is_benefic=is_benefic,
            mahadasha_planet=current_mahadasha
        )
        
        # Only include if recommended or if matches specific concern
        if len(rec.contraindications) == 0 or planet == current_mahadasha:
            recommendations[planet] = rec
    
    return recommendations
