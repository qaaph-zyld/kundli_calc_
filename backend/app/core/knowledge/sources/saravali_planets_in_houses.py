"""
Saravali - Planets in Houses Interpretations
Source: Saravali by Kalyana Varma (circa 800-900 CE)
Translation: R. Santhanam (Rajan Publications, 1996)

This module contains interpretations for planets in the 12 houses
based on the classical text Saravali, providing a parallel source
to BPHS for multi-source comparison and synthesis.

Saravali is one of the most authoritative classical texts in Vedic astrology,
written by Kalyana Varma. It provides detailed, practical interpretations
that complement and sometimes contrast with BPHS.
"""

from typing import Dict, Any

# Metadata about the source text
SARAVALI_METADATA = {
    "text_name": "Saravali",
    "author": "Kalyana Varma",
    "approximate_date": "800-900 CE",
    "translator": "R. Santhanam",
    "publisher": "Rajan Publications",
    "edition": "1996",
    "chapter": "Various chapters on planetary effects",
    "language": "Sanskrit (translated to English)",
    "tradition": "Vedic/Hindu astrology (Jyotish)",
    "authority_level": "Primary classical text",
    "notes": "One of the earliest comprehensive astrological texts; practical focus"
}

# Saravali Planets in Houses Interpretations
# Format: {planet: {house: {interpretation_data}}}
SARAVALI_PLANETS_IN_HOUSES: Dict[str, Dict[int, Dict[str, Any]]] = {
    
    "Sun": {
        1: {
            "verses": "Ch. 27, v. 1-2",
            "translation": "Should the Sun be in the ascendant, the native will have scanty hair on the head, be lazy in function, impetuous, tall and of firm limbs, will have weak eyesight, a lean and thin body.",
            "detailed_effects": [
                "Strong personality with natural authority",
                "Leadership abilities and commanding presence",
                "May appear proud or ego-driven",
                "Health issues with eyes or head",
                "Athletic or lean body structure",
                "Impetuous and quick to act",
                "Father's influence strong on personality"
            ],
            "positive_effects": [
                "Natural leadership and authority",
                "Strong willpower and determination",
                "Success through self-effort",
                "Respected by others",
                "Courageous and bold"
            ],
            "challenging_effects": [
                "May have ego issues",
                "Impulsive decision-making",
                "Eye or head health concerns",
                "Can be domineering",
                "Scanty hair (baldness tendency)"
            ],
            "timing": "Sun dashas bring prominence to self and career"
        },
        10: {
            "verses": "Ch. 27, v. 10",
            "translation": "If the Sun occupies the 10th, the native will be endowed with royal marks, be happy, valorous, will have firm and strong physique, and will attain kingdom.",
            "detailed_effects": [
                "Exceptional career success and recognition",
                "Government positions or authority roles",
                "Strong professional reputation",
                "Father may be influential",
                "Success through independent business",
                "Leadership in chosen field",
                "Public recognition and fame"
            ],
            "positive_effects": [
                "Outstanding career achievements",
                "Natural authority in profession",
                "Government favor and positions",
                "Strong reputation and fame",
                "Leadership roles"
            ],
            "challenging_effects": [
                "May face challenges from superiors",
                "Work-related stress",
                "Pressure to maintain status"
            ],
            "timing": "Career peaks during Sun mahadasha and dashas of 10th lord"
        }
    },
    
    "Moon": {
        4: {
            "verses": "Ch. 28, v. 4",
            "translation": "With the Moon in the 4th, the native will be endowed with relatives, will possess paraphernalia and vehicles, will be happy, virtuous, and will also enjoy royal favor.",
            "detailed_effects": [
                "Excellent placement for emotional happiness",
                "Strong bond with mother",
                "Property and vehicles",
                "Happy domestic life",
                "Comfortable home environment",
                "Good education and learning",
                "Support from relatives"
            ],
            "positive_effects": [
                "Emotional contentment and peace",
                "Happy relationship with mother",
                "Property and material comforts",
                "Good education",
                "Strong family ties"
            ],
            "challenging_effects": [
                "Emotional attachment to home",
                "May be too dependent on family",
                "Frequent residence changes if weak"
            ],
            "timing": "Peak emotional happiness during Moon dasha; property gains likely"
        },
        10: {
            "verses": "Ch. 28, v. 10",
            "translation": "Should the Moon be in the 10th house, the native will be skillful in his duties, be wealthy, virtuous, famous, and will be endowed with conveyances and paraphernalia.",
            "detailed_effects": [
                "Career involving public dealings",
                "Success in nurturing professions",
                "Popular with masses",
                "Emotional intelligence in career",
                "Fluctuating career trajectory",
                "Mother influential in career",
                "Public recognition"
            ],
            "positive_effects": [
                "Public popularity and fame",
                "Success in people-oriented careers",
                "Wealth through career",
                "Vehicles and comforts",
                "Virtuous professional conduct"
            ],
            "challenging_effects": [
                "Career changes and fluctuations",
                "Emotional stress from work",
                "Public scrutiny"
            ],
            "timing": "Career success in Moon dasha; public recognition peaks"
        }
    },
    
    "Mars": {
        10: {
            "verses": "Ch. 29, v. 10",
            "translation": "If Mars occupies the 10th, the native will be a ruler of the army, be famous, will have his desires fulfilled through kinsmen, be valorous, and will have all kinds of wealth.",
            "detailed_effects": [
                "Dynamic and energetic career",
                "Leadership in competitive fields",
                "Military, police, engineering favorable",
                "Success through courage and action",
                "Aggressive professional approach",
                "Property through career",
                "Technical or mechanical aptitude"
            ],
            "positive_effects": [
                "Outstanding career in Mars-related fields",
                "Leadership and authority",
                "Wealth through profession",
                "Desires fulfilled",
                "Courageous and bold in career"
            ],
            "challenging_effects": [
                "Conflicts with authority",
                "Aggressive professional style",
                "Accidents or injuries at work",
                "Legal issues possible"
            ],
            "timing": "Career peaks in Mars dasha; property gains through profession"
        }
    },
    
    "Mercury": {
        1: {
            "verses": "Ch. 30, v. 1-2",
            "translation": "If Mercury occupies the ascendant, the native will be learned in all Shastras, be sweet in speech, be skillful, and will be endowed with self-earned wealth.",
            "detailed_effects": [
                "Highly intelligent and communicative",
                "Quick learning abilities",
                "Youthful appearance",
                "Business-minded personality",
                "Versatile and adaptable",
                "Sweet and persuasive speech",
                "Self-made success"
            ],
            "positive_effects": [
                "Exceptional intelligence",
                "Excellent communication skills",
                "Success in business and commerce",
                "Quick wit and humor",
                "Educational achievements"
            ],
            "challenging_effects": [
                "Nervous energy and restlessness",
                "Scattered interests",
                "May overthink situations",
                "Difficulty with emotional depth"
            ],
            "timing": "Mercury dasha brings learning, business success, travel"
        },
        10: {
            "verses": "Ch. 30, v. 10",
            "translation": "Should Mercury be in the 10th, the native will be versed in Shastras and fine arts, be extremely famous, will enjoy happiness from wife and sons, and be skillful.",
            "detailed_effects": [
                "Intellectual career pursuits",
                "Success in communication-based professions",
                "Writing, teaching, business favorable",
                "Versatile professional skills",
                "Multiple income sources",
                "Fame through intelligence",
                "Happy family life"
            ],
            "positive_effects": [
                "Outstanding in intellectual professions",
                "Fame and recognition",
                "Happy marriage and children",
                "Skillful in chosen field",
                "Wealth through intellect"
            ],
            "challenging_effects": [
                "Scattered career focus",
                "Nervous tension from multiple projects",
                "May change careers frequently"
            ],
            "timing": "Career success in Mercury dasha; recognition for intellectual work"
        }
    },
    
    "Jupiter": {
        1: {
            "verses": "Ch. 31, v. 1-2",
            "translation": "Should Jupiter be in the ascendant, the native will be handsome, will possess charming physique and speech, be famous, and be endowed with wife, sons, and wealth.",
            "detailed_effects": [
                "Wisdom and philosophical nature",
                "Optimistic and benevolent personality",
                "Well-proportioned, attractive physique",
                "Natural teacher and counselor",
                "Ethical and righteous character",
                "Blessed family life",
                "Divine grace and protection"
            ],
            "positive_effects": [
                "Fortunate and blessed life",
                "Wisdom and good judgment",
                "Happy marriage and children",
                "Respect from society",
                "Wealth and prosperity"
            ],
            "challenging_effects": [
                "May be overly optimistic",
                "Tendency to overindulge",
                "Can be preachy or self-righteous"
            ],
            "timing": "Jupiter dasha brings fortune, marriage, children, spiritual growth"
        },
        5: {
            "verses": "Ch. 31, v. 5",
            "translation": "If Jupiter occupies the 5th, the native will be endowed with sons, be learned, famous, and will enjoy happiness from children.",
            "detailed_effects": [
                "Highly auspicious for children",
                "Intelligent and wise offspring",
                "Success in speculative ventures",
                "Creative wisdom",
                "Teaching and advisory abilities",
                "Good fortune overall",
                "Spiritual knowledge"
            ],
            "positive_effects": [
                "Blessed with good children",
                "Intelligence and wisdom",
                "Success in education",
                "Fame and recognition",
                "Good fortune"
            ],
            "challenging_effects": [
                "May be overly optimistic in speculation",
                "High expectations from children"
            ],
            "timing": "Children born in Jupiter dasha; educational success; spiritual progress"
        }
    },
    
    "Venus": {
        7: {
            "verses": "Ch. 32, v. 7",
            "translation": "Should Venus be in the 7th, the native will be endowed with a beautiful wife, will enjoy excellent sexual pleasures, be virtuous, and famous.",
            "detailed_effects": [
                "Excellent placement for marriage",
                "Beautiful, loving, harmonious spouse",
                "Strong sexual and romantic fulfillment",
                "Success in partnerships",
                "Diplomatic and charming",
                "Wealth through spouse or partnerships",
                "Artistic abilities"
            ],
            "positive_effects": [
                "Outstanding marital happiness",
                "Beautiful and virtuous spouse",
                "Excellent sexual compatibility",
                "Success in business partnerships",
                "Fame and recognition"
            ],
            "challenging_effects": [
                "May be overly focused on relationships",
                "Expenses on spouse or luxuries",
                "Jealousy issues if weak"
            ],
            "timing": "Marriage in Venus dasha; peak relationship happiness"
        }
    },
    
    "Saturn": {
        10: {
            "verses": "Ch. 33, v. 10",
            "translation": "With Saturn in the 10th, the native will be wealthy, virtuous, religious, and will enjoy royal favor.",
            "detailed_effects": [
                "Excellent for career - Saturn's best placement",
                "Success through discipline and hard work",
                "Slow but steady career growth",
                "Authority through responsibility",
                "Long-term professional stability",
                "Government or structured work favorable",
                "Respected for integrity"
            ],
            "positive_effects": [
                "Outstanding career achievements",
                "Wealth through profession",
                "Royal or government favor",
                "Religious and virtuous conduct",
                "Long-lasting success"
            ],
            "challenging_effects": [
                "Success comes slowly",
                "Heavy work responsibilities",
                "May face initial career obstacles"
            ],
            "timing": "Career peaks after age 36; sustained success in Saturn dasha"
        }
    }
}


def get_saravali_interpretation(planet: str, house: int) -> Dict[str, Any]:
    """
    Retrieve Saravali interpretation for a planet in a specific house.
    
    Args:
        planet: Planet name (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
        house: House number (1-12)
        
    Returns:
        Dictionary containing interpretation data with keys:
        - verses: Chapter and verse reference
        - translation: Classical text translation
        - detailed_effects: List of detailed interpretations
        - positive_effects: List of beneficial results
        - challenging_effects: List of difficulties
        - timing: Optional timing patterns
        
    Raises:
        KeyError: If planet or house not found in data
    """
    if planet not in SARAVALI_PLANETS_IN_HOUSES:
        raise KeyError(f"Planet '{planet}' not found in Saravali data")
    
    if house not in SARAVALI_PLANETS_IN_HOUSES[planet]:
        raise KeyError(f"House {house} not found for planet '{planet}' in Saravali data")
    
    return SARAVALI_PLANETS_IN_HOUSES[planet][house]


def get_available_saravali_combinations() -> Dict[str, list]:
    """
    Get list of available planet-house combinations in Saravali data.
    
    Returns:
        Dictionary mapping planet names to lists of available houses
    """
    return {
        planet: sorted(houses.keys())
        for planet, houses in SARAVALI_PLANETS_IN_HOUSES.items()
    }


def get_saravali_coverage_stats() -> Dict[str, Any]:
    """
    Get coverage statistics for Saravali interpretations.
    
    Returns:
        Dictionary with coverage metrics:
        - total_combinations: Total planet-house pairs available
        - planets_covered: Number of planets with data
        - by_planet: Dictionary showing houses covered per planet
        - completion_rate: Percentage of 84 possible combinations covered
    """
    by_planet = {}
    total = 0
    
    for planet, houses in SARAVALI_PLANETS_IN_HOUSES.items():
        count = len(houses)
        by_planet[planet] = {
            "houses_covered": count,
            "completion_rate": (count / 12) * 100
        }
        total += count
    
    return {
        "total_combinations": total,
        "planets_covered": len(SARAVALI_PLANETS_IN_HOUSES),
        "by_planet": by_planet,
        "overall_completion_rate": (total / 84) * 100
    }
