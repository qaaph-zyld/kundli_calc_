"""
BPHS: Dasha Effects
===================
Digitized dasha interpretations from Brihat Parashara Hora Shastra
Chapters 47-49: Effects of Vimshottari Mahadasha and Antardashas

Translation: R. Santhanam (1984)
Source: Rajan Publications

Each planetary period (dasha) produces specific effects based on the planet's
nature, placement, and lordship in the natal chart.
"""
from typing import Dict, Any, List


# BPHS Chapters 47-49: Vimshottari Dasha Effects

BPHS_MAHADASHA_EFFECTS: Dict[str, Dict[str, Any]] = {
    "Sun": {
        "chapter": 47,
        "verses": "47.3-8",
        "duration_years": 6,
        "classical_description": "During Sun mahadasha, the native gains authority, recognition, and connection with government. Effects depend on Sun's placement and dignity.",
        "general_effects": {
            "positive": [
                "Enhanced self-confidence and authority",
                "Recognition from government and superiors",
                "Success in leadership roles and administration",
                "Spiritual inclination and dharmic activities",
                "Father's blessings and support",
                "Improvement in health and vitality",
                "Acquisition of land and property"
            ],
            "challenging": [
                "Ego conflicts and arrogance if Sun afflicted",
                "Issues with authority figures",
                "Health problems related to eyes, bones, heart",
                "Separation from father or paternal issues",
                "Obstacles from government or legal matters"
            ]
        },
        "effects_by_house": {
            1: "Excellent for personal growth, authority, health improvement",
            10: "Outstanding career advancement, fame, government positions",
            4: "Issues with peace of mind, but gains of property possible",
            7: "Marital challenges but professional partnerships favorable"
        },
        "timing_within_dasha": {
            "first_third": "Building foundation, initial challenges",
            "middle_third": "Peak effects, maximum results",
            "last_third": "Consolidation, preparation for next dasha"
        },
        "remedies": [
            "Worship Sun deity (Surya) with Aditya Hridayam",
            "Donate wheat, jaggery, copper on Sundays",
            "Practice humility and service to father/elders",
            "Wear ruby if recommended by expert astrologer"
        ]
    },
    
    "Moon": {
        "chapter": 47,
        "verses": "47.9-14",
        "duration_years": 10,
        "classical_description": "Moon mahadasha brings emotional fulfillment, popularity, and material comforts. Strong focus on home, mother, and public life.",
        "general_effects": {
            "positive": [
                "Emotional happiness and contentment",
                "Popularity with masses and public",
                "Success in nurturing professions and public-facing work",
                "Gains through mother and maternal connections",
                "Acquisition of property, vehicles, comforts",
                "Marriage and family happiness",
                "Successful travels, especially to water bodies"
            ],
            "challenging": [
                "Emotional instability and mood swings",
                "Mental stress and anxiety",
                "Issues with mother or maternal relationships",
                "Health problems related to fluids, stomach, lungs",
                "Tendency toward depression if Moon afflicted"
            ]
        },
        "effects_by_dignity": {
            "waxing_strong": "Excellent results, emotional fulfillment, prosperity",
            "waning_weak": "Emotional challenges, health issues, mental stress"
        },
        "career_effects": [
            "Success in hospitality, nursing, counseling",
            "Public-facing roles and mass communication",
            "Real estate and property dealings",
            "Food and beverage industries",
            "Travel and tourism"
        ],
        "remedies": [
            "Worship Moon deity (Chandra) on Mondays",
            "Maintain emotional balance through meditation",
            "Strengthen relationship with mother",
            "Wear pearl (Moti) if recommended",
            "Donate white items and rice"
        ]
    },
    
    "Mars": {
        "chapter": 47,
        "verses": "47.15-20",
        "duration_years": 7,
        "classical_description": "Mars mahadasha brings energy, courage, and action. Success through determination but also potential for conflicts.",
        "general_effects": {
            "positive": [
                "Increased energy, courage, and determination",
                "Success through action and effort",
                "Gains from property, land, real estate",
                "Support from siblings and friends",
                "Victory over enemies and competitors",
                "Success in Mars-related careers (military, sports, surgery)",
                "Acquisition of vehicles and machinery"
            ],
            "challenging": [
                "Accidents, injuries, and surgeries",
                "Conflicts with siblings and authorities",
                "Blood-related health issues",
                "Legal disputes and property conflicts",
                "Impulsive decisions leading to losses",
                "Marital discord if Mars afflicted"
            ]
        },
        "career_focus": [
            "Military, police, and security services",
            "Sports and competitive fields",
            "Engineering and technical work",
            "Surgery and medical procedures",
            "Real estate and construction",
            "Metals and machinery business"
        ],
        "health_watch": [
            "Blood pressure and blood disorders",
            "Accidents and injuries, especially head",
            "Inflammations and fevers",
            "Surgical procedures may be necessary"
        ],
        "remedies": [
            "Worship Mars deity (Mangal) on Tuesdays",
            "Donate red items, lentils, copper",
            "Practice anger management and patience",
            "Recite Hanuman Chalisa",
            "Wear red coral if recommended"
        ]
    },
    
    "Mercury": {
        "chapter": 48,
        "verses": "48.1-6",
        "duration_years": 17,
        "classical_description": "Mercury mahadasha brings intellectual growth, business success, and communication skills. Longest period for learning and commerce.",
        "general_effects": {
            "positive": [
                "Enhanced intelligence and learning abilities",
                "Success in business, trade, and commerce",
                "Excellent communication and writing skills",
                "Educational achievements and certifications",
                "Multiple income sources",
                "Success in intellectual and analytical work",
                "Good relationships with friends and relatives"
            ],
            "challenging": [
                "Mental stress from overthinking",
                "Nervous system and respiratory issues",
                "Deception in business if Mercury afflicted",
                "Scattered focus and indecisiveness",
                "Skin problems and allergies"
            ]
        },
        "career_peak": [
            "Business and entrepreneurship",
            "Education and teaching",
            "Writing, publishing, journalism",
            "IT and technology fields",
            "Consulting and advisory",
            "Accounting and finance",
            "Communication industries"
        ],
        "life_areas_activated": [
            "Education and skill development",
            "Business ventures and trade",
            "Communication and networking",
            "Travel for business",
            "Intellectual pursuits"
        ],
        "remedies": [
            "Worship Mercury deity (Budha) on Wednesdays",
            "Study and teach sacred knowledge",
            "Donate green items, books, educational materials",
            "Practice ethical business dealings",
            "Wear emerald if recommended"
        ]
    },
    
    "Jupiter": {
        "chapter": 48,
        "verses": "48.7-12",
        "duration_years": 16,
        "classical_description": "Jupiter mahadasha is highly auspicious, bringing wisdom, prosperity, and divine grace. Period of expansion and spiritual growth.",
        "general_effects": {
            "positive": [
                "Spiritual and philosophical growth",
                "Financial prosperity and wealth accumulation",
                "Success in education and higher learning",
                "Birth of children and family happiness",
                "Respect and recognition in society",
                "Religious and charitable activities",
                "Guidance from teachers and mentors",
                "Divine protection and good fortune"
            ],
            "challenging": [
                "Over-optimism and excessive indulgence",
                "Weight gain and liver issues",
                "Financial overextension",
                "Tendency toward complacency"
            ]
        },
        "optimal_for": [
            "Marriage and starting family",
            "Higher education and teaching",
            "Spiritual practices and pilgrimage",
            "Long-term investments",
            "Establishing institutions",
            "Legal matters and justice",
            "Advisory and counseling roles"
        ],
        "wealth_effects": "Generally brings prosperity through legitimate means. Good for investments and long-term financial planning.",
        "spiritual_effects": "Strong period for spiritual initiation, studying scriptures, and connecting with teachers.",
        "remedies": [
            "Worship Jupiter deity (Guru) on Thursdays",
            "Study and share wisdom",
            "Practice generosity and charity",
            "Donate yellow items, turmeric, gold",
            "Wear yellow sapphire if recommended"
        ]
    },
    
    "Venus": {
        "chapter": 48,
        "verses": "48.13-18",
        "duration_years": 20,
        "classical_description": "Venus mahadasha brings luxury, relationships, and artistic success. Longest planetary period focused on beauty and harmony.",
        "general_effects": {
            "positive": [
                "Marriage and romantic fulfillment",
                "Acquisition of luxuries and comforts",
                "Success in arts, music, and creative fields",
                "Enhanced beauty and charm",
                "Profitable partnerships and alliances",
                "Vehicles and expensive possessions",
                "Social popularity and refined lifestyle"
            ],
            "challenging": [
                "Excessive indulgence in sensual pleasures",
                "Relationship complications and infidelity risks",
                "Financial losses through luxury spending",
                "Reproductive health issues",
                "Tendency toward materialism"
            ]
        },
        "relationship_focus": "Prime time for marriage, romance, and partnership formation. But guard against over-attachment and sensual excess.",
        "career_opportunities": [
            "Arts, entertainment, and fashion",
            "Beauty and cosmetics industry",
            "Luxury goods and hospitality",
            "Jewelry and precious items",
            "Relationship counseling",
            "Design and decoration"
        ],
        "wealth_pattern": "Gains through Venusian means - arts, partnerships, luxury goods. Tendency to spend on comforts.",
        "remedies": [
            "Worship Venus deity (Shukra) on Fridays",
            "Practice moderation in pleasures",
            "Use charm for benevolent purposes",
            "Donate white items, sugar, clothes",
            "Wear diamond if recommended"
        ]
    },
    
    "Saturn": {
        "chapter": 49,
        "verses": "49.1-6",
        "duration_years": 19,
        "classical_description": "Saturn mahadasha brings karmic lessons, discipline, and delayed results. Period of hard work, endurance, and spiritual maturity.",
        "general_effects": {
            "positive": [
                "Discipline and patience developed",
                "Success through sustained hard work",
                "Spiritual maturity and detachment",
                "Long-term career stability",
                "Service to underprivileged brings merit",
                "Wisdom gained through hardship",
                "Late but lasting achievements"
            ],
            "challenging": [
                "Delays and obstacles in all matters",
                "Health issues, especially chronic conditions",
                "Separations and loneliness",
                "Financial struggles and poverty if Saturn weak",
                "Depression and pessimism",
                "Professional setbacks initially",
                "Family conflicts and responsibilities"
            ]
        },
        "life_pattern": "First half often difficult with obstacles and delays. Second half brings rewards for patience and hard work.",
        "career_guidance": [
            "Success in Saturnian fields - labor, mining, agriculture",
            "Government service and administration",
            "Engineering and construction",
            "Work with elderly or underprivileged",
            "Research and solitary work",
            "Long-term projects bear fruit"
        ],
        "spiritual_opportunity": "Excellent period for spiritual discipline, meditation, and renunciation. Detachment from worldly matters.",
        "health_focus": [
            "Chronic conditions require attention",
            "Joint and bone problems",
            "Dental issues",
            "Depression and mental health",
            "Vitality may be low"
        ],
        "remedies": [
            "Worship Saturn deity (Shani) on Saturdays",
            "Serve the poor, elderly, and suffering",
            "Practice patience and acceptance",
            "Donate black items, sesame, iron",
            "Worship Lord Hanuman",
            "Accept delays as divine timing"
        ]
    },
    
    "Rahu": {
        "chapter": 49,
        "verses": "49.7-12",
        "duration_years": 18,
        "classical_description": "Rahu mahadasha brings sudden changes, foreign connections, and unconventional paths. Period of material ambition and innovation.",
        "general_effects": {
            "positive": [
                "Sudden gains and unexpected success",
                "Foreign travel and settlement abroad",
                "Success in technology and innovation",
                "Political connections and influence",
                "Material prosperity and luxury",
                "Unconventional success paths",
                "Mass appeal and popularity"
            ],
            "challenging": [
                "Confusion and lack of direction",
                "Unconventional or unethical means",
                "Health issues (mysterious ailments)",
                "Addictions and obsessions",
                "Legal troubles and scandals",
                "Family separations",
                "Mental instability"
            ]
        },
        "unique_opportunities": [
            "Foreign lands and cultures",
            "Technology and cutting-edge fields",
            "Politics and mass movements",
            "Occult and mystical studies",
            "Media and entertainment",
            "Sudden wealth opportunities"
        ],
        "warnings": [
            "Avoid shortcuts and unethical means",
            "Guard against addictions",
            "Maintain mental clarity",
            "Be cautious in speculative ventures",
            "Verify all dealings carefully"
        ],
        "remedies": [
            "Worship Rahu deity on Saturdays",
            "Practice meditation for mental clarity",
            "Donate to outcasts and marginalized",
            "Wear Gomed (hessonite) if recommended",
            "Recite Rahu mantras"
        ]
    },
    
    "Ketu": {
        "chapter": 49,
        "verses": "49.13-18",
        "duration_years": 7,
        "classical_description": "Ketu mahadasha brings spiritual insight, detachment, and karmic completion. Period of inner work and letting go.",
        "general_effects": {
            "positive": [
                "Spiritual enlightenment and moksha",
                "Detachment from worldly matters",
                "Mystical experiences and intuition",
                "Liberation from past karmas",
                "Success in occult and spiritual fields",
                "Sudden insights and wisdom",
                "Service to spiritual causes"
            ],
            "challenging": [
                "Loss and separation from worldly attachments",
                "Confusion and lack of direction",
                "Health issues (mysterious ailments)",
                "Financial instability",
                "Accidents and sudden events",
                "Isolation and loneliness",
                "Difficulty with material achievements"
            ]
        },
        "spiritual_focus": "Excellent for meditation, yoga, spiritual practices. Time to let go of material attachments.",
        "material_effects": "Generally difficult for material progress. Focus shifts to inner world.",
        "career_impact": [
            "Success in spiritual or mystical fields",
            "Research and investigation",
            "Healing and alternative medicine",
            "Occult and astrology",
            "Difficulty in conventional careers"
        ],
        "remedies": [
            "Worship Ketu deity and Ganesha",
            "Practice spiritual discipline intensively",
            "Donate to spiritual causes",
            "Wear cat's eye if recommended",
            "Accept losses as spiritual lessons",
            "Engage in selfless service"
        ]
    }
}


def get_mahadasha_interpretation(planet: str) -> Dict[str, Any]:
    """
    Retrieve BPHS interpretation for a planet's mahadasha.
    
    Args:
        planet: Planet name
        
    Returns:
        Dictionary with mahadasha effects and guidance
    """
    return BPHS_MAHADASHA_EFFECTS.get(planet, None)


def get_all_mahadasha_planets() -> List[str]:
    """Get list of all planets with mahadasha interpretations"""
    return list(BPHS_MAHADASHA_EFFECTS.keys())
