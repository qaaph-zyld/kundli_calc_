"""
BPHS: Planets in Houses
========================
Digitized interpretations from Brihat Parashara Hora Shastra, Chapter 24
"Effects of Planets in Twelve Bhavas"

Translation: R. Santhanam (1984)
Source: Rajan Publications

Note: This is a structured representation of public domain classical knowledge.
Each entry includes verse references for verification.
"""
from typing import Dict, Any

# BPHS Chapter 24: Planets in Bhavas (Houses)
# Verses 1-78 cover all planet-house combinations

BPHS_PLANETS_IN_HOUSES: Dict[str, Dict[int, Dict[str, Any]]] = {
    "Sun": {
        1: {
            "verses": "24.3-4",
            "original": "सूर्यो लग्नगतः...",  # Sanskrit reference
            "translation": "If the Sun is in the ascendant, the native will have scanty hair on the head, will be lazy, of hot constitution, impetuous, tall in stature, and will have weak eye-sight.",
            "detailed_effects": [
                "Strong, prominent personality with natural authority",
                "Lean or well-built physique, often tall stature",
                "Tendency toward bilious constitution (Pitta imbalance)",
                "May have weak eyesight or eye issues, especially in later life",
                "Courageous nature but can be impulsive or hasty",
                "Leadership qualities manifest naturally",
                "May have less hair on head or experience hair thinning",
                "Independent, self-reliant temperament"
            ],
            "positive_effects": [
                "Natural leadership and commanding presence",
                "Strong vitality and life force",
                "Recognition and respect from others",
                "Self-confidence and willpower",
                "Interest in government, authority, or spirituality"
            ],
            "challenging_effects": [
                "Tendency toward arrogance or ego issues",
                "Can be domineering or overly authoritative",
                "Health issues related to heat (fevers, inflammation)",
                "Possible eye problems",
                "May face obstacles from father or authority figures"
            ],
            "remedies": [
                "Worship the Sun deity (Surya) at sunrise",
                "Recite Aditya Hridayam stotra",
                "Practice humility and respect toward elders",
                "Donate wheat, jaggery, or copper on Sundays",
                "Wear ruby (if recommended by qualified astrologer)"
            ],
            "life_areas": {
                "personality": "Strong, authoritative, and independent character",
                "health": "Generally strong vitality but watch for eye issues and bilious disorders",
                "career": "Natural inclination toward leadership, government service, administration",
                "relationships": "May dominate in relationships; need to balance ego"
            }
        },
        2: {
            "verses": "24.5",
            "translation": "Sun in the 2nd house: The native will be devoid of learning and wealth, will be dependent on others, dumb, will have ugly face, and will destroy his family.",
            "detailed_effects": [
                "Challenges in family life and wealth accumulation",
                "Speech may be harsh or blunt, sometimes creating misunderstandings",
                "Family patrimony may be diminished or lost",
                "Strong opinions that may conflict with family values",
                "Education may face obstacles initially",
                "Self-esteem tied to material possessions",
                "May need to create own wealth rather than inherit"
            ],
            "positive_effects": [
                "Strong voice and commanding speech when positively placed",
                "Can be powerful public speaker if Sun is strong",
                "Determination to rebuild family fortune",
                "Value-driven approach to wealth"
            ],
            "challenging_effects": [
                "Harsh speech may damage relationships",
                "Financial ups and downs",
                "Conflicts with family members",
                "Difficulty in formal education",
                "Eye or face-related issues"
            ],
            "remedies": [
                "Practice mindful speech",
                "Donate food and resources to the needy",
                "Worship ancestors (Pitru tarpan)",
                "Maintain harmonious family relationships",
                "Recite Gayatri Mantra daily"
            ]
        },
        10: {
            "verses": "24.11",
            "translation": "Sun in the 10th house: The native will be happy, will have abundant wealth, will perform religious sacrifices, and will have excellent conveyances, fame, and expertise in multiple sciences.",
            "detailed_effects": [
                "Outstanding for career and public life - one of the best placements",
                "Natural leader in professional sphere",
                "Fame and recognition in chosen field",
                "Government positions, authority roles, or self-employment in leadership capacity",
                "Father's influence important in career path",
                "Strong sense of duty and responsibility",
                "Reputation for integrity and competence",
                "Success through own efforts and merit",
                "May hold positions of power and influence"
            ],
            "positive_effects": [
                "Exceptional career success and professional recognition",
                "Natural authority and commanding presence at work",
                "Respect from superiors and subordinates alike",
                "Strong ethical foundation in professional life",
                "Fame within chosen field or profession",
                "Ability to lead large organizations or initiatives",
                "Government favor and support possible",
                "Father may be prominent or helpful in career"
            ],
            "challenging_effects": [
                "Work may consume personal life",
                "Excessive focus on career at expense of family",
                "Ego conflicts with superiors possible",
                "Intense pressure and responsibility",
                "Public scrutiny and criticism"
            ],
            "remedies": [
                "Worship Sun deity (Surya) for continued success",
                "Maintain humility despite achievements",
                "Honor father and authority figures",
                "Use position to serve others",
                "Balance work with spiritual practices"
            ],
            "life_areas": {
                "career": "Exceptional placement for career - leadership, authority, fame, government service",
                "reputation": "Excellent public image and respect in society",
                "father": "Strong relationship with father; father may be prominent",
                "dharma": "Strong sense of duty and righteous action in profession"
            },
            "timing": "Most powerful during Sun mahadasha. Effects strengthen after age 30.",
            "notable_yogas": [
                "Can form Ruchaka Yoga if in own sign (Leo)",
                "Contributes to Raja Yogas if connected with lords of kendras/trikonas",
                "Strengthens any Dharma-Karma Adhipati Yoga"
            ]
        }
    },
    
    "Moon": {
        1: {
            "verses": "24.14-15",
            "translation": "Moon in the ascendant: The native will be attractive, will have phlegmatic temperament, be long-lived, will have few sons, be helpful to others, highly intelligent, bold, and respectable.",
            "detailed_effects": [
                "Pleasant, attractive personality with magnetic charm",
                "Emotional, sensitive, and intuitive nature",
                "Receptive and adaptable to circumstances",
                "Strong imagination and creative abilities",
                "Nurturing, caring disposition toward others",
                "Youthful appearance, often looking younger than age",
                "Mind-dominated personality; thoughts influence health",
                "May have Kapha constitution (cool, moist)"
            ],
            "positive_effects": [
                "Likeable personality with strong people skills",
                "Emotional intelligence and empathy",
                "Creative and imaginative mindset",
                "Good relationship with mother",
                "Ability to influence others through emotional appeal",
                "Longevity and generally good health"
            ],
            "challenging_effects": [
                "Emotional fluctuations and mood swings",
                "Tendency toward mental stress or anxiety",
                "May be overly sensitive to criticism",
                "Dependency on others for emotional security",
                "Possible challenges with children (as per classical text)"
            ],
            "remedies": [
                "Practice emotional regulation through meditation",
                "Worship Moon deity (Chandra)",
                "Strengthen relationship with mother",
                "Pearl (Moti) if recommended by expert",
                "Fasting on Mondays"
            ]
        }
    },
    
    "Mars": {
        10: {
            "verses": "24.35",
            "translation": "Mars in the 10th house: The native will be religious, famous, valorous, and will be endowed with jewels, gold, and wealth.",
            "detailed_effects": [
                "Dynamic, energetic approach to career",
                "Success through courage, action, and determination",
                "Good for military, police, sports, surgery, engineering",
                "Competitive nature drives professional success",
                "Gains through property and real estate",
                "Leadership through strength and decisiveness",
                "May work in fields involving fire, metals, or machinery"
            ],
            "positive_effects": [
                "High energy and drive for career success",
                "Courage to take risks in profession",
                "Success in competitive fields",
                "Accumulation of property and wealth",
                "Respected for bravery and direct action"
            ],
            "challenging_effects": [
                "Conflicts with authority figures",
                "Aggressive or domineering professional style",
                "Accidents or injuries related to career",
                "Legal disputes over property or career matters"
            ]
        }
    },
    
    "Mercury": {
        10: {
            "verses": "24.38",
            "translation": "Mercury in the 10th house: The native will be learned in Shastras, will possess good speech and wealth, will be truthful, and will have happiness from wife and sons.",
            "detailed_effects": [
                "Intellectual and analytical career pursuits",
                "Success in communication, business, education, IT",
                "Multi-talented with diverse skills",
                "Good networking and business acumen",
                "Success through mental agility and adaptability",
                "Teaching, writing, consulting are favorable",
                "Reputation for intelligence and versatility"
            ],
            "positive_effects": [
                "Excellent communication skills in profession",
                "Success in business and commerce",
                "Recognition for intellectual abilities",
                "Multiple income sources possible",
                "Good reputation for honesty and intelligence"
            ],
            "challenging_effects": [
                "Scattered professional focus",
                "Nervous tension from multitasking",
                "Tendency to overanalyze career decisions"
            ]
        }
    },
    
    "Jupiter": {
        1: {
            "verses": "24.40",
            "translation": "Jupiter in the ascendant: The native will be handsome, will have strength, honor, fame, longevity, grace, be learned, and be an expert in all Shastras.",
            "detailed_effects": [
                "Wisdom, optimism, and philosophical nature",
                "Well-proportioned, often larger body frame",
                "Natural teacher and guide to others",
                "Ethical, righteous character",
                "Interest in higher knowledge and spirituality",
                "Generally fortunate and protected",
                "Respected for wisdom and good character"
            ],
            "positive_effects": [
                "Generally fortunate life with divine grace",
                "Wisdom and good judgment",
                "Respect from society and elders",
                "Inclined toward righteous action",
                "Good health and longevity",
                "Success in education and spiritual pursuits",
                "Beneficial for children and family life"
            ],
            "challenging_effects": [
                "May become overly idealistic",
                "Tendency toward excess (weight gain, overindulgence)",
                "Can be judgmental or preachy"
            ]
        },
        10: {
            "verses": "24.49",
            "translation": "Jupiter in the 10th house: The native will enjoy happiness from sons, will be religious, learned, famous, and will be an advisor to the king or government.",
            "detailed_effects": [
                "Highly auspicious for career - one of the best placements for Jupiter",
                "Success in advisory, teaching, counseling, finance, law",
                "Ethical professional reputation",
                "Recognition for wisdom and expertise",
                "Government positions or working with authorities",
                "Father-figure in professional sphere",
                "Natural mentor and guide to colleagues"
            ],
            "positive_effects": [
                "Career based on wisdom, knowledge, ethics",
                "Respect and honor in profession",
                "Opportunities to guide and teach others",
                "Financial prosperity through legitimate means",
                "Blessings from superiors and government",
                "Children support career success"
            ],
            "notable_yogas": [
                "Can form Hamsa Yoga if in own sign or exaltation",
                "Strong contributor to Raja Yogas",
                "Gaja Kesari Yoga if Moon is in kendra"
            ]
        }
    }
}

def get_planet_in_house_interpretation(planet: str, house: int) -> Dict[str, Any]:
    """
    Retrieve BPHS interpretation for planet in house.
    
    Args:
        planet: Planet name (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
        house: House number (1-12)
        
    Returns:
        Dictionary with interpretation data and verse references
    """
    if planet not in BPHS_PLANETS_IN_HOUSES:
        return None
    
    if house not in BPHS_PLANETS_IN_HOUSES[planet]:
        return None
    
    return BPHS_PLANETS_IN_HOUSES[planet][house]
