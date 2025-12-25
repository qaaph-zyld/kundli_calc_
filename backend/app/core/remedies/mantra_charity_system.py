"""Mantra and Charity Remedial System
======================================
Traditional Vedic remedial measures through mantras, charity, and observances.

Reference Texts:
- Brihat Parashara Hora Shastra, Upaaya Adhyaya
- Lal Kitab
- Mantra Mahodadhi
- Phala Deepika, Chapter 21
- Hora Ratnam

Mantras from:
- Vedic traditions
- Puranic sources
- Tantric lineages
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class MantraType(Enum):
    """Types of mantras"""
    VEDIC = "Vedic (from Vedas)"
    PURANIC = "Puranic (from Puranas)"
    TANTRIC = "Tantric/Beej Mantra"
    SIMPLE = "Simple Nama Mantra"


@dataclass
class MantraRecommendation:
    """Mantra prescription for a planet"""
    planet: str
    mantra_type: MantraType
    mantra_text: str
    translation: str
    count_per_day: int
    total_count: int  # For completion
    duration_days: int
    best_time: str
    deity: str
    benefits: List[str]
    procedure: str
    reference: str


@dataclass
class CharityRecommendation:
    """Charity (Daan) prescription"""
    planet: str
    items_to_donate: List[str]
    recipients: List[str]
    day: str
    time: str
    color_to_wear: str
    additional_observances: List[str]
    benefits: List[str]
    reference: str


@dataclass
class FastingRecommendation:
    """Fasting (Vrata) prescription"""
    planet: str
    fasting_day: str
    fasting_type: str  # Full, partial, specific food
    duration: str
    procedure: str
    deity_worship: str
    benefits: List[str]


class MantraCharitySystem:
    """Traditional mantra and charity remedial system"""
    
    # Planet-wise mantra data
    # Reference: Mantra Mahodadhi, BPHS Upaaya Adhyaya
    MANTRA_DATA = {
        'Sun': {
            'deity': 'Surya (Sun God)',
            'simple': {
                'text': 'Om Suryaya Namaha',
                'translation': 'Salutations to the Sun God',
                'count': 7000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Japa Kusuma Sankasham Kashyapeyam Mahadyutim | Tamorim Sarva Papaghnam Pranatosmi Divakaram ||',
                'translation': 'I bow to Surya, who shines like the Hibiscus flower, son of Kashyapa, destroyer of darkness and all sins',
                'count': 7000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Hraam Hreem Hraum Sah Suryaya Namaha',
                'translation': 'Beej mantra invoking Sun\'s seed energy',
                'count': 7000,
                'daily': 108
            },
            'gayatri': {
                'text': 'Om Bhaskaraya Vidmahe Divakaraya Dhimahi Tanno Suryah Prachodayat',
                'translation': 'Surya Gayatri - meditation on Sun\'s illumination',
                'count': 7000,
                'daily': 108
            },
            'best_time': 'Sunrise (within 1 hour after sunrise)',
            'benefits': [
                'Strengthens vitality and immunity',
                'Improves father relationships',
                'Enhances leadership qualities',
                'Supports government/authority career',
                'Increases self-confidence'
            ]
        },
        'Moon': {
            'deity': 'Chandra (Moon God)',
            'simple': {
                'text': 'Om Chandraya Namaha',
                'translation': 'Salutations to the Moon God',
                'count': 11000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Dadhi Shankha Tusharabham Kshirodarnava Sambhavam | Namami Shashinam Somam Shambhor Mukuta Bhushanam ||',
                'translation': 'I bow to Chandra, who shines like curd and conch shell, born from ocean of milk, adorning Shiva\'s crown',
                'count': 11000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Shraam Shreem Shraum Sah Chandraya Namaha',
                'translation': 'Beej mantra invoking Moon\'s seed energy',
                'count': 11000,
                'daily': 108
            },
            'gayatri': {
                'text': 'Om Padma Dwajaya Vidmahe Hema Roopaya Dhimahi Tanno Chandra Prachodayat',
                'translation': 'Chandra Gayatri - meditation on Moon\'s cooling grace',
                'count': 11000,
                'daily': 108
            },
            'best_time': 'Evening (after sunset) or Full Moon nights',
            'benefits': [
                'Enhances emotional stability',
                'Improves mental peace',
                'Strengthens mother relationships',
                'Benefits mind and memory',
                'Supports nurturing qualities'
            ]
        },
        'Mars': {
            'deity': 'Mangala/Kartikeya',
            'simple': {
                'text': 'Om Mangalaya Namaha',
                'translation': 'Salutations to Mars',
                'count': 10000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Dharani Garbha Sambhutam Vidyut Kanti Samaprabham | Kumaram Shakti Hastam Tam Mangalam Pranamamy Aham ||',
                'translation': 'I bow to Mangala, born from Earth, shining like lightning, holding weapon, the auspicious one',
                'count': 10000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Kraam Kreem Kraum Sah Bhaumaya Namaha',
                'translation': 'Beej mantra invoking Mars\' seed energy',
                'count': 10000,
                'daily': 108
            },
            'best_time': 'Tuesday morning or Mars hora',
            'benefits': [
                'Increases courage and confidence',
                'Improves energy and vitality',
                'Supports property matters',
                'Enhances sibling relationships',
                'Reduces accidents and injuries'
            ]
        },
        'Mercury': {
            'deity': 'Budha (Mercury God)',
            'simple': {
                'text': 'Om Budhaya Namaha',
                'translation': 'Salutations to Mercury',
                'count': 9000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Priyangava Shyamalam Roopena Pratimam Budham | Soumyam Soumya Gunopetam Tam Budham Pranamamy Aham ||',
                'translation': 'I bow to Budha, dark like Priyangu flower, gentle with auspicious qualities',
                'count': 9000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Braam Breem Braum Sah Budhaya Namaha',
                'translation': 'Beej mantra invoking Mercury\'s seed energy',
                'count': 9000,
                'daily': 108
            },
            'best_time': 'Wednesday morning or Mercury hora',
            'benefits': [
                'Enhances intelligence and learning',
                'Improves communication skills',
                'Supports business and trade',
                'Benefits students and writers',
                'Sharpens analytical abilities'
            ]
        },
        'Jupiter': {
            'deity': 'Brihaspati (Jupiter/Guru)',
            'simple': {
                'text': 'Om Gurave Namaha',
                'translation': 'Salutations to Jupiter/Guru',
                'count': 19000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Devanam Cha Rishinam Cha Gurum Kanchana Sannibham | Buddhi Bhutam Trilokesham Tam Namami Brihaspatim ||',
                'translation': 'I bow to Brihaspati, Guru of gods and sages, shining like gold, lord of three worlds',
                'count': 19000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Graam Greem Graum Sah Gurave Namaha',
                'translation': 'Beej mantra invoking Jupiter\'s seed energy',
                'count': 19000,
                'daily': 108
            },
            'gayatri': {
                'text': 'Om Vrisha Bhwajaya Vidmahe Kruni Hastaya Dhimahi Tanno Guruh Prachodayat',
                'translation': 'Jupiter Gayatri - meditation on divine wisdom',
                'count': 19000,
                'daily': 108
            },
            'best_time': 'Thursday morning during Jupiter hora',
            'benefits': [
                'Enhances wisdom and knowledge',
                'Improves fortune and prosperity',
                'Supports children and education',
                'Benefits spiritual growth',
                'Attracts good teachers and guides'
            ]
        },
        'Venus': {
            'deity': 'Shukra (Venus God)',
            'simple': {
                'text': 'Om Shukraya Namaha',
                'translation': 'Salutations to Venus',
                'count': 16000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Hima Kunda Mrinalalabham Daityanam Paramam Gurum | Sarva Shastra Pravaktaram Bhargavam Pranamamy Aham ||',
                'translation': 'I bow to Shukra, fair like jasmine, Guru of demons, teacher of all scriptures',
                'count': 16000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Draam Dreem Draum Sah Shukraya Namaha',
                'translation': 'Beej mantra invoking Venus\' seed energy',
                'count': 16000,
                'daily': 108
            },
            'best_time': 'Friday morning during Venus hora',
            'benefits': [
                'Enhances love and relationships',
                'Improves artistic abilities',
                'Supports marriage and partnerships',
                'Increases comforts and luxuries',
                'Benefits beauty and charm'
            ]
        },
        'Saturn': {
            'deity': 'Shani (Saturn God)',
            'simple': {
                'text': 'Om Shanaischaraya Namaha',
                'translation': 'Salutations to Saturn',
                'count': 23000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Nilanjana Samabhasam Ravi Putram Yamagrajam | Chhaya Martanda Sambhutam Tam Namami Shanescharam ||',
                'translation': 'I bow to Shani, dark blue like collyrium, son of Sun and Chhaya, slow-moving one',
                'count': 23000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Praam Preem Praum Sah Shanaischaraya Namaha',
                'translation': 'Beej mantra invoking Saturn\'s seed energy',
                'count': 23000,
                'daily': 108
            },
            'best_time': 'Saturday evening during Saturn hora',
            'benefits': [
                'Reduces obstacles and delays',
                'Improves discipline and focus',
                'Supports career longevity',
                'Eases Sade Sati effects',
                'Enhances patience and perseverance'
            ]
        },
        'Rahu': {
            'deity': 'Rahu (North Node)',
            'simple': {
                'text': 'Om Rahave Namaha',
                'translation': 'Salutations to Rahu',
                'count': 18000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Ardha Kayam Maha Viryam Chandraditya Vimardanam | Simhika Garbha Sambhutam Tam Rahum Pranamamy Aham ||',
                'translation': 'I bow to Rahu, half-bodied, mighty, eclipser of Sun and Moon, born of Simhika',
                'count': 18000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Bhraam Bhreem Bhraum Sah Rahave Namaha',
                'translation': 'Beej mantra invoking Rahu\'s seed energy',
                'count': 18000,
                'daily': 108
            },
            'best_time': 'Saturday during Rahu Kala or sunset',
            'benefits': [
                'Reduces confusion and illusions',
                'Supports foreign connections',
                'Improves unconventional success',
                'Helps with phobias and addictions',
                'Benefits research and occult'
            ]
        },
        'Ketu': {
            'deity': 'Ketu (South Node)',
            'simple': {
                'text': 'Om Ketave Namaha',
                'translation': 'Salutations to Ketu',
                'count': 17000,
                'daily': 108
            },
            'vedic': {
                'text': 'Om Palasha Pushpa Sankasham Taraka Graha Mastakam | Raudram Raudratmakam Ghoram Tam Ketum Pranamamy Aham ||',
                'translation': 'I bow to Ketu, like Palasha flower, fierce and terrible, head of stars',
                'count': 17000,
                'daily': 108
            },
            'beej': {
                'text': 'Om Sraam Sreem Sraum Sah Ketave Namaha',
                'translation': 'Beej mantra invoking Ketu\'s seed energy',
                'count': 17000,
                'daily': 108
            },
            'best_time': 'Tuesday or Thursday, early morning',
            'benefits': [
                'Enhances spiritual insight',
                'Supports moksha path',
                'Reduces sudden losses',
                'Benefits occult knowledge',
                'Improves intuition and detachment'
            ]
        }
    }
    
    # Charity (Daan) recommendations per planet
    # Reference: BPHS Upaaya Adhyaya, Lal Kitab
    CHARITY_DATA = {
        'Sun': {
            'items': ['Wheat', 'Jaggery', 'Red cloth', 'Copper', 'Ruby (if possible)', 'Saffron'],
            'recipients': ['Father', 'Government servants', 'Elderly men', 'Temples', 'Brahmins'],
            'day': 'Sunday',
            'time': 'Sunrise or afternoon',
            'color': 'Red, Orange, or Golden',
            'observances': [
                'Offer water to Sun at sunrise (Surya Arghya)',
                'Light lamp with ghee facing East',
                'Practice Surya Namaskar (Sun Salutation)',
                'Serve father with respect'
            ],
            'benefits': [
                'Strengthens Sun\'s positive influence',
                'Improves health and vitality',
                'Enhances father\'s well-being',
                'Supports government-related matters'
            ]
        },
        'Moon': {
            'items': ['White rice', 'Milk', 'White cloth', 'Silver', 'Pearl (if possible)', 'White flowers'],
            'recipients': ['Mother', 'Women', 'Nursing mothers', 'Poor families', 'Water bodies (feed fish)'],
            'day': 'Monday',
            'time': 'Evening or Full Moon night',
            'color': 'White or Light colors',
            'observances': [
                'Drink milk before sleep',
                'Keep water in silver vessel overnight',
                'Practice Moon meditation (Chandra Dhyana)',
                'Serve mother with love'
            ],
            'benefits': [
                'Enhances emotional stability',
                'Improves mother\'s well-being',
                'Strengthens mind and memory',
                'Brings mental peace'
            ]
        },
        'Mars': {
            'items': ['Red lentils (Masoor dal)', 'Jaggery', 'Red cloth', 'Copper', 'Red Coral', 'Wheat bread'],
            'recipients': ['Brothers', 'Soldiers', 'Athletes', 'Laborers', 'Hanuman temples'],
            'day': 'Tuesday',
            'time': 'Morning after sunrise',
            'color': 'Red',
            'observances': [
                'Visit Hanuman temple on Tuesdays',
                'Recite Hanuman Chalisa',
                'Practice physical exercise',
                'Serve siblings with care'
            ],
            'benefits': [
                'Increases courage and strength',
                'Reduces accidents and injuries',
                'Improves sibling relationships',
                'Supports property matters'
            ]
        },
        'Mercury': {
            'items': ['Green vegetables', 'Green cloth', 'Books', 'Pens', 'Emerald (if possible)', 'Moong dal'],
            'recipients': ['Students', 'Teachers', 'Writers', 'Merchants', 'Schools'],
            'day': 'Wednesday',
            'time': 'Morning',
            'color': 'Green',
            'observances': [
                'Feed green grass to cows',
                'Donate books to students',
                'Study sacred texts',
                'Practice speech discipline'
            ],
            'benefits': [
                'Enhances learning and intelligence',
                'Improves communication',
                'Supports business success',
                'Benefits students and writers'
            ]
        },
        'Jupiter': {
            'items': ['Yellow clothes', 'Turmeric', 'Chana dal', 'Gold', 'Yellow Sapphire', 'Books', 'Saffron'],
            'recipients': ['Brahmins', 'Teachers', 'Priests', 'Temples', 'Educational institutions'],
            'day': 'Thursday',
            'time': 'Morning during Jupiter hora',
            'color': 'Yellow or Golden',
            'observances': [
                'Feed Brahmins on Thursdays',
                'Worship Banana tree',
                'Study spiritual texts',
                'Respect teachers and elders'
            ],
            'benefits': [
                'Enhances wisdom and prosperity',
                'Improves children\'s well-being',
                'Supports education',
                'Attracts good fortune'
            ]
        },
        'Venus': {
            'items': ['White clothes', 'Sugar', 'Cow\'s ghee', 'Silver', 'Diamond/White Sapphire', 'White flowers', 'Perfumes'],
            'recipients': ['Young women', 'Newly married couples', 'Artists', 'Musicians', 'Cow shelters'],
            'day': 'Friday',
            'time': 'Morning during Venus hora',
            'color': 'White or Light Pink',
            'observances': [
                'Serve wife/spouse with love',
                'Feed cows',
                'Appreciate beauty and arts',
                'Practice forgiveness'
            ],
            'benefits': [
                'Enhances love and relationships',
                'Improves marital harmony',
                'Supports artistic pursuits',
                'Increases comforts'
            ]
        },
        'Saturn': {
            'items': ['Black sesame', 'Black cloth', 'Iron', 'Mustard oil', 'Black Urad dal', 'Leather shoes to poor'],
            'recipients': ['Poor people', 'Disabled', 'Elderly', 'Servants', 'Crows', 'Black dogs'],
            'day': 'Saturday',
            'time': 'Evening',
            'color': 'Black or Dark Blue',
            'observances': [
                'Feed crows and black dogs',
                'Serve handicapped and elderly',
                'Light mustard oil lamp under Peepal tree',
                'Practice humility and service'
            ],
            'benefits': [
                'Reduces Saturn\'s malefic effects',
                'Eases Sade Sati difficulties',
                'Improves patience and discipline',
                'Reduces obstacles gradually'
            ]
        },
        'Rahu': {
            'items': ['Blue/Black cloth', 'Mustard', 'Coconut', 'Hessonite Garnet', 'Iron'],
            'recipients': ['Outcasts', 'Foreigners', 'Servants', 'Black dogs', 'Snakes (feed milk)'],
            'day': 'Saturday',
            'time': 'During Rahu Kala',
            'color': 'Blue or Black',
            'observances': [
                'Feed black dogs',
                'Donate to lepers or outcasts',
                'Worship Goddess Durga',
                'Practice meditation'
            ],
            'benefits': [
                'Reduces Rahu\'s negative effects',
                'Improves foreign prospects',
                'Reduces confusion',
                'Protects from evil eye'
            ]
        },
        'Ketu': {
            'items': ['Grey/multicolor cloth', 'Black sesame', 'Blankets', 'Umbrellas', 'Cat\'s Eye'],
            'recipients': ['Spiritual seekers', 'Ascetics', 'Temples', 'Dogs', 'Religious institutions'],
            'day': 'Tuesday or Thursday',
            'time': 'Early morning',
            'color': 'Grey or Mixed colors',
            'observances': [
                'Feed dogs',
                'Donate to spiritual institutions',
                'Worship Lord Ganesha',
                'Practice detachment'
            ],
            'benefits': [
                'Enhances spiritual growth',
                'Reduces sudden losses',
                'Improves intuition',
                'Supports moksha path'
            ]
        }
    }
    
    # Fasting recommendations
    FASTING_DATA = {
        'Sun': {
            'day': 'Sunday',
            'type': 'No salt, one meal',
            'duration': 'Sunrise to sunset',
            'deity': 'Surya',
            'procedure': 'Break fast with jaggery and wheat preparations'
        },
        'Moon': {
            'day': 'Monday',
            'type': 'Milk only or fruits',
            'duration': 'Full day or evening',
            'deity': 'Chandra/Shiva',
            'procedure': 'Break fast with milk and white sweets'
        },
        'Mars': {
            'day': 'Tuesday',
            'type': 'One meal, no lentils',
            'duration': 'Sunrise to sunset',
            'deity': 'Hanuman/Kartikeya',
            'procedure': 'Visit Hanuman temple, break fast after evening prayers'
        },
        'Mercury': {
            'day': 'Wednesday',
            'type': 'Light food, no heavy meals',
            'duration': 'Morning',
            'deity': 'Budha/Vishnu',
            'procedure': 'Break fast with green vegetables'
        },
        'Jupiter': {
            'day': 'Thursday',
            'type': 'No salt, yellow foods only',
            'duration': 'One meal only',
            'deity': 'Brihaspati/Vishnu',
            'procedure': 'Feed Brahmins, break fast after puja'
        },
        'Venus': {
            'day': 'Friday',
            'type': 'Light food, no heavy spices',
            'duration': 'One meal',
            'deity': 'Lakshmi/Shukra',
            'procedure': 'Break fast with white sweets and milk'
        },
        'Saturn': {
            'day': 'Saturday',
            'type': 'No salt, sesame based foods',
            'duration': 'After sunset',
            'deity': 'Shani/Hanuman',
            'procedure': 'Light lamp with mustard oil, break fast after prayers'
        }
    }
    
    def recommend_mantra(
        self,
        planet: str,
        intensity: str = 'moderate'  # simple, moderate, intensive
    ) -> MantraRecommendation:
        """Recommend mantra for a planet"""
        if planet not in self.MANTRA_DATA:
            raise ValueError(f"No mantra data for {planet}")
        
        data = self.MANTRA_DATA[planet]
        
        # Select mantra type based on intensity
        if intensity == 'simple':
            mantra_info = data['simple']
            mantra_type = MantraType.SIMPLE
        elif intensity == 'intensive':
            mantra_info = data.get('beej', data['simple'])
            mantra_type = MantraType.TANTRIC
        else:  # moderate
            mantra_info = data.get('vedic', data['simple'])
            mantra_type = MantraType.VEDIC
        
        # Calculate duration (40 days minimum for completion)
        daily_count = mantra_info['daily']
        total_count = mantra_info['count']
        duration = max(40, int(total_count / daily_count))
        
        procedure = self._get_mantra_procedure(
            planet, data['deity'], mantra_info['text'], 
            daily_count, data['best_time']
        )
        
        return MantraRecommendation(
            planet=planet,
            mantra_type=mantra_type,
            mantra_text=mantra_info['text'],
            translation=mantra_info['translation'],
            count_per_day=daily_count,
            total_count=total_count,
            duration_days=duration,
            best_time=data['best_time'],
            deity=data['deity'],
            benefits=data['benefits'],
            procedure=procedure,
            reference="Mantra Mahodadhi, BPHS Upaaya Adhyaya"
        )
    
    def _get_mantra_procedure(
        self,
        planet: str,
        deity: str,
        mantra: str,
        count: int,
        time: str
    ) -> str:
        """Get detailed mantra japa procedure"""
        return f"""Mantra Japa Procedure for {planet} ({deity}):

**Preparation:**
1. Take bath and wear clean clothes
2. Face appropriate direction (East for most planets)
3. Sit on comfortable seat (wool or silk recommended)
4. Keep mala (rosary) of appropriate material:
   - Rudraksha (general)
   - Tulsi for spiritual planets
   - Crystal for benefics
   - Lotus seeds for Moon

**Daily Practice:**
1. Light lamp and incense
2. Offer flowers and water to deity
3. Sit in meditation posture (Padmasana/Sukhasana)
4. Take sankalpa (intention): "I am reciting this mantra {count} times for [specific purpose]"
5. Begin japa with concentration
6. Use mala for counting (one bead = one mantra)
7. Complete {count} repetitions
8. Best time: {time}

**During Japa:**
- Maintain focus on deity form or mantra itself
- Keep voice low (whisper) or mental recitation
- Don't cross the meru (main bead) - reverse direction
- Maintain regular timing daily

**Completion:**
- After final count, offer prayers
- Havan (fire ceremony) recommended on completion day
- Brahmin feeding (if possible)
- Maintain effects through weekly practice

**Duration:** Minimum 40 days without break. If missed, restart count.

**Special Note:** Maximum benefit when done during {deity}'s specific periods or planetary hora."""
    
    def recommend_charity(self, planet: str) -> CharityRecommendation:
        """Recommend charity (daan) for a planet"""
        if planet not in self.CHARITY_DATA:
            raise ValueError(f"No charity data for {planet}")
        
        data = self.CHARITY_DATA[planet]
        
        return CharityRecommendation(
            planet=planet,
            items_to_donate=data['items'],
            recipients=data['recipients'],
            day=data['day'],
            time=data['time'],
            color_to_wear=data['color'],
            additional_observances=data['observances'],
            benefits=data['benefits'],
            reference="BPHS Upaaya Adhyaya, Lal Kitab"
        )
    
    def recommend_fasting(self, planet: str) -> FastingRecommendation:
        """Recommend fasting (vrata) for a planet"""
        if planet not in self.FASTING_DATA:
            raise ValueError(f"No fasting data for {planet}")
        
        data = self.FASTING_DATA[planet]
        
        procedure = f"""Fasting Procedure for {planet}:

**Fast Type:** {data['type']}
**Day:** {data['day']}
**Duration:** {data['duration']}

**Procedure:**
1. Wake up early, take bath
2. Wear {self.CHARITY_DATA[planet]['color']} colored clothes
3. Light lamp to {data['deity']}
4. Declare intention for fasting
5. {data['procedure']}

**During Fast:**
- Maintain purity of thought and speech
- Recite mantras when possible
- Avoid negative activities
- Practice charity

**Benefits:** Strengthens {planet}'s positive influence gradually over time.

**Duration:** Minimum 11 consecutive {data['day']}s for visible effects.
Continue for 40 weeks for permanent strengthening."""
        
        return FastingRecommendation(
            planet=planet,
            fasting_day=data['day'],
            fasting_type=data['type'],
            duration=data['duration'],
            procedure=procedure,
            deity_worship=data['deity'],
            benefits=self.CHARITY_DATA[planet]['benefits']
        )


def create_complete_remedial_plan(
    weak_planets: List[str],
    current_mahadasha: str,
    user_preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create complete remedial plan for weak planets
    
    Args:
        weak_planets: List of planets needing remediation
        current_mahadasha: Current running Mahadasha
        user_preferences: User preferences (intensity, budget, time commitment)
        
    Returns:
        Complete remedial plan with mantras, charity, fasting, gemstones
    """
    system = MantraCharitySystem()
    
    intensity = user_preferences.get('intensity', 'moderate') if user_preferences else 'moderate'
    
    remedial_plan = {}
    
    for planet in weak_planets:
        remedial_plan[planet] = {
            'planet': planet,
            'priority': 'High' if planet == current_mahadasha else 'Medium',
            'mantra': system.recommend_mantra(planet, intensity),
            'charity': system.recommend_charity(planet),
            'fasting': system.recommend_fasting(planet),
            'combined_approach': f"""Integrated Remedial Approach for {planet}:

**Weekly Schedule:**
- {system.CHARITY_DATA[planet]['day']}: Fasting + Special Puja
- Daily: Mantra japa ({system.MANTRA_DATA[planet]['simple']['daily']} times)
- Weekly charity on {system.CHARITY_DATA[planet]['day']}

**Monthly Observances:**
- Full/New Moon: Special prayers
- Planetary transit days: Enhanced practice
- Ekadashi: Additional spiritual observance

**Duration:** Minimum 40 days for initial effects, 120 days for stable results.

**Note:** Combine with gemstone if recommended by astrologer."""
        }
    
    return {
        'remedial_plans': remedial_plan,
        'general_recommendations': [
            'Maintain daily spiritual practice',
            'Practice gratitude and positive thinking',
            'Serve others selflessly',
            'Study sacred texts',
            'Maintain purity in thought, word, and deed'
        ],
        'reference': 'BPHS Upaaya Adhyaya, Mantra Mahodadhi, Lal Kitab'
    }
