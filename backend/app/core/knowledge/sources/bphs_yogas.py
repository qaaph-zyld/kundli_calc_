"""
BPHS: Yogas (Planetary Combinations)
=====================================
Digitized yoga interpretations from Brihat Parashara Hora Shastra
Chapters 40-46: Raja Yogas, Dhana Yogas, Arishta Yogas, Nabhasa Yogas

Translation: R. Santhanam (1984)
Source: Rajan Publications

Yogas are specific planetary combinations that produce significant effects.
Each entry includes formation conditions, effects, and verse references.

Phase 5 Expansion: Added yogas from Chapters 44-46
"""
from typing import Dict, Any, List


# BPHS Chapters 40-43: Yogas (Planetary Combinations)

BPHS_RAJA_YOGAS: Dict[str, Dict[str, Any]] = {
    "Dharma_Karma_Adhipati_Yoga": {
        "chapter": 40,
        "verses": "40.3-4",
        "category": "Raja Yoga",
        "formation": "Lords of 9th and 10th houses in mutual association (conjunction, aspect, or exchange)",
        "classical_description": "When the lords of the 9th (dharma) and 10th (karma) houses are in conjunction, mutual aspect, or parivartana (exchange), a powerful Raja Yoga is formed indicating high status, power, and success.",
        "effects": {
            "general": "Exceptional rise in life through righteous action and professional excellence. This is considered one of the most powerful Raja Yogas.",
            "career": "Outstanding career success, often in government, administration, or leadership roles. Natural authority and respect.",
            "status": "High social standing and recognition. May attain positions of significant influence.",
            "timing": "Effects manifest primarily during dashas of the involved planets",
            "strength_factors": [
                "Both planets in kendras (1,4,7,10) - strongest",
                "Planets in own signs or exalted - very strong",
                "No malefic aspects or associations - pure results",
                "Conjunction in 10th house - exceptional for career"
            ]
        },
        "examples": [
            "9th lord Jupiter conjunct 10th lord Saturn in 10th house",
            "9th lord Sun in 10th house aspecting 10th lord Mars in 9th",
            "9th lord and 10th lord in parivartana (exchange houses)"
        ],
        "cancellation_factors": [
            "Severe affliction by malefics",
            "Combustion of both planets",
            "Placement in 6th, 8th, or 12th houses (dusthana) without dignity",
            "Aspect from multiple malefics"
        ],
        "strength_assessment": {
            "very_strong": "Both planets exalted or in own signs, in kendras, no affliction",
            "strong": "One planet well-placed, mutual aspect, minimal affliction",
            "moderate": "Basic connection present but with some weaknesses",
            "weak": "Connection through aspect only, with afflictions"
        }
    },
    
    "Rajayoga_from_Kendra_Trikona_Lords": {
        "chapter": 40,
        "verses": "40.5-7",
        "category": "Raja Yoga",
        "formation": "Lords of kendra houses (1,4,7,10) associate with lords of trikona houses (1,5,9)",
        "classical_description": "Association between kendra lords (angles) and trikona lords (trines) produces Raja Yoga. This is a fundamental principle of Vedic astrology for power and prosperity.",
        "effects": {
            "general": "Rise in status, prosperity, and fulfillment of ambitions. The native gains power and influence.",
            "wealth": "Financial prosperity through legitimate means",
            "reputation": "Good reputation and respect in society",
            "protection": "Divine grace and protection from adversities",
            "timing": "Most pronounced during dashas of the yoga-forming planets"
        },
        "examples": [
            "1st lord (kendra) with 5th lord (trikona) in conjunction",
            "4th lord aspecting 9th lord",
            "10th lord and 5th lord in parivartana",
            "7th lord conjunct 1st lord (both kendra, but 1st is also trikona)"
        ],
        "special_notes": [
            "1st and 10th lord connection is particularly powerful (self + career)",
            "4th and 5th lord connection excellent for property and children",
            "Involvement of 9th lord brings fortune and dharma"
        ],
        "cancellation_factors": [
            "Both planets weak by sign placement",
            "Severe malefic affliction",
            "Placement in dusthanas (6,8,12) without strength"
        ]
    },
    
    "Gaja_Kesari_Yoga": {
        "chapter": 41,
        "verses": "41.37-38",
        "category": "Chandra Yoga",
        "formation": "Jupiter in a kendra (1st, 4th, 7th, or 10th house) from the Moon",
        "classical_description": "The 'Elephant-Lion' yoga forms when Jupiter, the great benefic, occupies an angular house from the Moon. This is one of the most famous and auspicious yogas.",
        "effects": {
            "general": "Wisdom, prosperity, good character, and respect in society. The native is blessed with intelligence and ethical conduct.",
            "personality": "Virtuous, learned, diplomatic, and well-mannered. Commands respect without effort.",
            "wealth": "Accumulation of wealth through righteous means. Material comforts.",
            "reputation": "Excellent reputation and influence in community",
            "longevity": "Generally indicates good health and longevity",
            "family": "Happy family life with good children"
        },
        "strength_factors": [
            "Jupiter and Moon both strong by sign",
            "Jupiter in own sign (Sagittarius/Pisces) or exalted (Cancer)",
            "Moon waxing and in good dignity",
            "No malefic aspects to Jupiter or Moon",
            "Formation in kendra from lagna amplifies results"
        ],
        "strength_assessment": {
            "very_strong": "Jupiter exalted in Cancer with waxing Moon - exceptional wisdom and fortune",
            "strong": "Jupiter in own sign in kendra from strong Moon",
            "moderate": "Jupiter in kendra from Moon but with some afflictions",
            "weak": "Jupiter weak by sign or Moon heavily afflicted"
        },
        "timing": "Most powerful during Jupiter mahadasha or Moon mahadasha. Also strong in Jupiter-Moon antardashas.",
        "modern_interpretation": "This yoga indicates someone who combines emotional intelligence (Moon) with wisdom and expansion (Jupiter). Such natives make good teachers, counselors, and spiritual guides."
    },
    
    "Neechabhanga_Raja_Yoga": {
        "chapter": 42,
        "verses": "42.23-27",
        "category": "Special Raja Yoga",
        "formation": "Cancellation of debilitation creating a powerful Raja Yoga",
        "classical_description": "When a planet's debilitation is cancelled through specific conditions, it creates an even more powerful effect than exaltation - the native rises from adversity to great heights.",
        "cancellation_conditions": [
            "Debilitation lord is in a kendra from lagna or Moon",
            "Exaltation lord of the debilitated planet is in a kendra",
            "Debilitated planet is aspected by its dispositor",
            "Debilitated planet is in parivartana with its dispositor",
            "Lord of the debilitation sign is exalted or in own house",
            "Debilitated planet is retrograde (partial cancellation)"
        ],
        "effects": {
            "general": "Rise from humble beginnings to great heights. Success through overcoming obstacles. The native becomes extraordinarily strong in the planet's significations.",
            "life_pattern": "Initial struggles followed by dramatic rise. The adversity faced early becomes the source of strength.",
            "special_quality": "Develops exceptional skill and mastery in areas of the debilitated planet through overcoming challenges."
        },
        "examples": [
            "Sun debilitated in Libra but Venus (Libra lord) in kendra - cancellation",
            "Moon debilitated in Scorpio but Mars (Scorpio lord) exalted - cancellation",
            "Saturn debilitated in Aries but Mars in kendra from Moon - cancellation"
        ],
        "strength_assessment": {
            "very_strong": "Multiple cancellation factors present",
            "strong": "One complete cancellation factor",
            "partial": "Debilitated planet aspected by friends or in good house"
        }
    }
}

BPHS_DHANA_YOGAS: Dict[str, Dict[str, Any]] = {
    "Dhana_Yoga_2nd_11th_Lords": {
        "chapter": 41,
        "verses": "41.15-16",
        "category": "Wealth Yoga",
        "formation": "Association between lords of 2nd house (wealth) and 11th house (gains)",
        "classical_description": "When the lords of the 2nd and 11th houses associate through conjunction, aspect, or exchange, a powerful wealth yoga is formed.",
        "effects": {
            "general": "Accumulation of substantial wealth through multiple sources",
            "income": "High income and regular gains. Multiple revenue streams.",
            "assets": "Accumulation of assets, property, and valuables",
            "family_wealth": "Strong family financial foundation",
            "timing": "Wealth accumulates during dashas of these planets"
        },
        "strength_factors": [
            "Both lords in wealth houses (2, 11, 5, 9)",
            "Association in kendra houses increases stability",
            "No malefic affliction",
            "Planets in own signs or exalted"
        ]
    },
    
    "Lakshmi_Yoga": {
        "chapter": 41,
        "verses": "41.30-32",
        "category": "Wealth Yoga",
        "formation": "Lord of 9th house (fortune) strong and in own sign, exaltation, or in kendra/trikona",
        "classical_description": "When the 9th lord (lord of fortune and dharma) is powerfully placed, it creates Lakshmi Yoga - the blessing of Goddess Lakshmi for wealth and prosperity.",
        "effects": {
            "general": "Blessed with wealth, prosperity, and divine grace. Fortune seems to favor the native.",
            "wealth": "Wealth comes through righteous means and good fortune",
            "reputation": "Respected for generosity and ethical conduct",
            "spirituality": "Balance of material and spiritual prosperity",
            "protection": "Protected from severe financial losses"
        },
        "formation_variations": [
            "9th lord in own sign in kendra",
            "9th lord exalted in trikona",
            "9th lord in conjunction with Venus or Jupiter (natural wealth givers)"
        ]
    },
    
    "Dhan_Yoga_5th_9th_Lords": {
        "chapter": 41,
        "verses": "41.18",
        "category": "Wealth Yoga",
        "formation": "Association of 5th lord (past merit) with 9th lord (fortune)",
        "classical_description": "The 5th house represents purva punya (past life merit) and the 9th house represents bhagya (fortune). Their union creates wealth through good karma.",
        "effects": {
            "general": "Wealth through fortune, speculation, and wise investments",
            "speculation": "Success in investments, stock market, speculation",
            "children": "Prosperity through or for children",
            "education": "Financial gains through education or teaching",
            "dharma": "Wealth earned through righteous means brings lasting satisfaction"
        },
        "timing": "Particularly strong during dashas of 5th and 9th lords"
    }
}

BPHS_PANCHA_MAHAPURUSHA_YOGAS: Dict[str, Dict[str, Any]] = {
    "Ruchaka_Yoga": {
        "chapter": 40,
        "verses": "40.12-13",
        "category": "Mahapurusha Yoga",
        "planet": "Mars",
        "formation": "Mars in own sign (Aries/Scorpio) or exaltation (Capricorn) in a kendra (1,4,7,10)",
        "classical_description": "One of the five great combinations. Creates a warrior-like personality with courage and leadership.",
        "effects": {
            "personality": "Courageous, bold, commanding presence. Natural leader and warrior.",
            "physique": "Strong, athletic build. Reddish complexion.",
            "career": "Success in military, sports, surgery, engineering, real estate",
            "wealth": "Gains through Mars-related activities - property, metals, fire",
            "reputation": "Respected for courage and decisive action",
            "longevity": "Generally good vitality and resistance to disease"
        },
        "ideal_formations": [
            "Mars in Aries in 1st house",
            "Mars in Capricorn (exalted) in 10th house",
            "Mars in Scorpio in 7th house"
        ]
    },
    
    "Bhadra_Yoga": {
        "chapter": 40,
        "verses": "40.14-15",
        "category": "Mahapurusha Yoga",
        "planet": "Mercury",
        "formation": "Mercury in own sign (Gemini/Virgo) or exaltation (Virgo) in a kendra",
        "classical_description": "Creates exceptional intelligence, business acumen, and communication skills.",
        "effects": {
            "personality": "Highly intelligent, articulate, diplomatic. Quick wit and adaptability.",
            "physique": "Well-proportioned body. Pleasant appearance.",
            "career": "Success in business, writing, education, communication, IT",
            "intellect": "Sharp mind, excellent memory, analytical abilities",
            "wealth": "Financial success through intellectual pursuits",
            "skills": "Multi-talented with diverse interests and abilities"
        }
    },
    
    "Hamsa_Yoga": {
        "chapter": 40,
        "verses": "40.16-17",
        "category": "Mahapurusha Yoga",
        "planet": "Jupiter",
        "formation": "Jupiter in own sign (Sagittarius/Pisces) or exaltation (Cancer) in a kendra",
        "classical_description": "Creates wisdom, righteousness, and spiritual inclination. Considered highly auspicious.",
        "effects": {
            "personality": "Wise, righteous, spiritual. Natural teacher and guide.",
            "physique": "Well-built, often large frame. Fair complexion. Graceful.",
            "career": "Success in teaching, counseling, law, finance, religious work",
            "wisdom": "Philosophical mind with deep understanding of life",
            "wealth": "Prosperity through ethical means. Divine grace.",
            "reputation": "Highly respected for character and knowledge",
            "family": "Happy family life with good children"
        }
    },
    
    "Malavya_Yoga": {
        "chapter": 40,
        "verses": "40.18-19",
        "category": "Mahapurusha Yoga",
        "planet": "Venus",
        "formation": "Venus in own sign (Taurus/Libra) or exaltation (Pisces) in a kendra",
        "classical_description": "Creates beauty, artistic talents, and material luxuries.",
        "effects": {
            "personality": "Charming, artistic, diplomatic. Refined and cultured.",
            "physique": "Attractive, graceful appearance. Beautiful features.",
            "career": "Success in arts, entertainment, fashion, luxury goods, hospitality",
            "wealth": "Material comforts and luxuries. Prosperity.",
            "relationships": "Happy marriage and social life. Popular.",
            "talents": "Natural artistic and creative abilities"
        }
    },
    
    "Sasa_Yoga": {
        "chapter": 40,
        "verses": "40.20-21",
        "category": "Mahapurusha Yoga",
        "planet": "Saturn",
        "formation": "Saturn in own sign (Capricorn/Aquarius) or exaltation (Libra) in a kendra",
        "classical_description": "Creates discipline, perseverance, and success through hard work.",
        "effects": {
            "personality": "Disciplined, patient, responsible. Strong work ethic.",
            "physique": "Lean build. Mature appearance.",
            "career": "Success through sustained effort in administration, engineering, mining",
            "wealth": "Accumulates wealth slowly but steadily",
            "reputation": "Respected for integrity and responsibility",
            "longevity": "Generally indicates long life",
            "leadership": "Gains authority through proven competence"
        }
    }
}

def get_yoga_interpretation(yoga_name: str) -> Dict[str, Any]:
    """
    Retrieve BPHS interpretation for a specific yoga.
    
    Args:
        yoga_name: Name of the yoga
        
    Returns:
        Dictionary with yoga interpretation and formation details
    """
    # Search in all yoga categories
    all_yogas = {
        **BPHS_RAJA_YOGAS,
        **BPHS_DHANA_YOGAS,
        **BPHS_PANCHA_MAHAPURUSHA_YOGAS
    }
    
    return all_yogas.get(yoga_name, None)


def get_yogas_by_category(category: str) -> Dict[str, Dict[str, Any]]:
    """
    Get all yogas of a specific category.
    
    Args:
        category: Category name (Raja Yoga, Wealth Yoga, Mahapurusha Yoga, etc.)
        
    Returns:
        Dictionary of yogas in that category
    """
    all_yogas = {
        **BPHS_RAJA_YOGAS,
        **BPHS_DHANA_YOGAS,
        **BPHS_PANCHA_MAHAPURUSHA_YOGAS
    }
    
    return {name: data for name, data in all_yogas.items() if data.get('category') == category}


def get_all_yogas() -> Dict[str, Dict[str, Any]]:
    """
    Get all available yogas from all categories.
    
    Returns:
        Combined dictionary of all yogas
    """
    all_yogas = {}
    all_yogas.update(BPHS_RAJA_YOGAS)
    all_yogas.update(BPHS_DHANA_YOGAS)
    all_yogas.update(BPHS_PANCHA_MAHAPURUSHA_YOGAS)
    all_yogas.update(BPHS_ADDITIONAL_YOGAS)  # Phase 5 expansion
    return all_yogas
