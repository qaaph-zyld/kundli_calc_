"""
Phaladeepika: Planets in Houses
================================
Digitized interpretations from Phaladeepika by Mantreswara
Chapters 10-21: Planetary placements in houses

Translation: V. Subrahmanya Sastri (1963)
Source: Ranjan Publications

Phaladeepika (Light on Results) is a classical Vedic astrology text
focusing on practical predictive techniques.
"""

from typing import Dict, Any


# Phaladeepika Chapters 10-21: Planet-in-House Interpretations

PHALADEEPIKA_PLANETS_IN_HOUSES: Dict[str, Dict[int, Dict[str, Any]]] = {
    "Sun": {
        1: {
            "chapter": 10,
            "verses": "10.3-4",
            "translation": "The Sun in the first house makes the native fond of roaming in forests and mountains, cruel-hearted, afflicted with eye diseases, valorous, and generally having diseased constitution.",
            "detailed_effects": [
                "Strong physical constitution but prone to health issues",
                "Courageous and valorous nature",
                "Interest in mountainous regions and solitude",
                "Potential eye-related health concerns",
                "Independent and self-reliant personality"
            ],
            "positive_effects": [
                "Valorous and courageous",
                "Strong will and leadership qualities",
                "Independent thinking"
            ],
            "challenging_effects": [
                "Tendency toward harshness",
                "Eye health issues",
                "Health vulnerabilities",
                "May prefer solitude over social interaction"
            ],
            "timing": "Effects manifest throughout life, intensify during Sun dasha"
        },
        10: {
            "chapter": 10,
            "verses": "10.12",
            "translation": "When the Sun occupies the 10th house, the native will be blessed with happiness from children, will be intelligent, wealthy, valorous, and will shine in royal favor.",
            "detailed_effects": [
                "Excellence in career and professional life",
                "Recognition from authority figures",
                "Wealth accumulation through profession",
                "Intelligent and strategic mind",
                "Joy and satisfaction from children"
            ],
            "positive_effects": [
                "Career success and recognition",
                "Wealth and prosperity",
                "Intelligence and wisdom",
                "Royal or governmental favor",
                "Happiness from progeny"
            ],
            "challenging_effects": [
                "May face competition in career",
                "Pressure to maintain high status"
            ],
            "timing": "Career peaks during Sun mahadasha, recognition in youth to middle age"
        }
    },
    
    "Moon": {
        1: {
            "chapter": 11,
            "verses": "11.3",
            "translation": "The Moon in the first house makes one good-looking, with a beautiful body, afflicted by wind diseases, fickle-minded, and water-loving.",
            "detailed_effects": [
                "Attractive physical appearance",
                "Emotional and sensitive nature",
                "Love for water, travel, and change",
                "Variable mental state",
                "Nurturing personality"
            ],
            "positive_effects": [
                "Beautiful appearance",
                "Emotional intelligence",
                "Adaptability",
                "Nurturing nature"
            ],
            "challenging_effects": [
                "Mental fickleness",
                "Wind-related health issues",
                "Emotional instability at times"
            ],
            "timing": "Effects prominent during Moon dasha and waxing Moon periods"
        },
        4: {
            "chapter": 11,
            "verses": "11.6",
            "translation": "The Moon in the 4th house bestows upon the native happiness, friendship, enjoyment of all comforts, possession of conveyances, and acquisition of wealth.",
            "detailed_effects": [
                "Domestic happiness and peace",
                "Comfortable home environment",
                "Vehicles and properties",
                "Emotional fulfillment from family",
                "Strong connection with mother"
            ],
            "positive_effects": [
                "Domestic bliss",
                "Material comforts",
                "Property and vehicles",
                "Emotional security",
                "Good friendships"
            ],
            "challenging_effects": [
                "Emotional attachment to possessions",
                "May be overly dependent on comfort"
            ],
            "timing": "Home acquisition during Moon dasha, family happiness throughout"
        }
    },
    
    "Mars": {
        1: {
            "chapter": 12,
            "verses": "12.3",
            "translation": "Mars in the first house makes one cruel, adventurous, daring in acts, with scars on the body, short-tempered, and engaged in violent activities.",
            "detailed_effects": [
                "Courageous and fearless nature",
                "Tendency toward aggression",
                "Physical marks or scars",
                "Quick temper and impulsive actions",
                "Athletic or martial interests"
            ],
            "positive_effects": [
                "Courage and bravery",
                "Physical strength",
                "Leadership in action",
                "Protection abilities"
            ],
            "challenging_effects": [
                "Aggressive tendencies",
                "Anger management issues",
                "Prone to accidents or injuries",
                "Conflicts with others"
            ],
            "timing": "Martial activities peak during Mars dasha"
        },
        10: {
            "chapter": 12,
            "verses": "12.12",
            "translation": "Mars in the 10th house makes the native virtuous, successful in undertakings, protector of relatives, and achiever of desired objectives.",
            "detailed_effects": [
                "Success in professional endeavors",
                "Protective of family and community",
                "Achievement-oriented personality",
                "Leadership in work environment",
                "Righteous and ethical conduct"
            ],
            "positive_effects": [
                "Career success",
                "Protective nature",
                "Achievement of goals",
                "Virtuous character",
                "Leadership abilities"
            ],
            "challenging_effects": [
                "May face professional conflicts",
                "Competitive work environment"
            ],
            "timing": "Career achievements during Mars dasha"
        }
    },
    
    "Mercury": {
        1: {
            "chapter": 13,
            "verses": "13.3",
            "translation": "Mercury in the first house makes one skilled in arts, eloquent in speech, intelligent, long-lived, and with beautiful eyes.",
            "detailed_effects": [
                "Exceptional communication skills",
                "Artistic and creative abilities",
                "Sharp intellect and quick learning",
                "Attractive features, especially eyes",
                "Longevity and good health"
            ],
            "positive_effects": [
                "Eloquence and communication",
                "Intelligence and wit",
                "Artistic talents",
                "Longevity",
                "Physical attractiveness"
            ],
            "challenging_effects": [
                "May overthink situations",
                "Nervous energy"
            ],
            "timing": "Intellectual pursuits flourish during Mercury dasha"
        },
        11: {
            "chapter": 13,
            "verses": "13.13",
            "translation": "Mercury in the 11th house bestows learning, wealth, happiness, many sources of income, and fulfillment of desires.",
            "detailed_effects": [
                "Multiple income streams",
                "Educational achievements",
                "Network of influential friends",
                "Fulfillment of ambitions",
                "Financial prosperity"
            ],
            "positive_effects": [
                "Wealth accumulation",
                "Educational success",
                "Desire fulfillment",
                "Multiple income sources",
                "Social connections"
            ],
            "challenging_effects": [
                "May scatter energies across too many ventures"
            ],
            "timing": "Financial gains during Mercury dasha"
        }
    },
    
    "Jupiter": {
        1: {
            "chapter": 14,
            "verses": "14.3",
            "translation": "Jupiter in the first house makes one learned, virtuous, long-lived, firm in friendship, of good conduct, and having many sons.",
            "detailed_effects": [
                "Wisdom and scholarly pursuits",
                "Ethical and virtuous nature",
                "Long and prosperous life",
                "Loyal friendships",
                "Blessed with children"
            ],
            "positive_effects": [
                "Wisdom and learning",
                "Virtuous character",
                "Longevity",
                "Good children",
                "Loyal friends"
            ],
            "challenging_effects": [
                "May be overly optimistic at times",
                "Tendency toward weight gain"
            ],
            "timing": "Spiritual growth and wisdom during Jupiter dasha"
        },
        9: {
            "chapter": 14,
            "verses": "14.11",
            "translation": "Jupiter in the 9th house makes one fortunate, wealthy, learned in scriptures, religious, and blessed with father's grace.",
            "detailed_effects": [
                "Exceptional fortune and blessings",
                "Wealth from righteous means",
                "Deep spiritual knowledge",
                "Good relationship with father",
                "Religious and philosophical inclinations"
            ],
            "positive_effects": [
                "Exceptional fortune",
                "Wealth and prosperity",
                "Spiritual wisdom",
                "Father's blessings",
                "Religious inclination"
            ],
            "challenging_effects": [
                "May be overly idealistic"
            ],
            "timing": "Fortune manifests during Jupiter dasha, pilgrimage during this period"
        }
    },
    
    "Venus": {
        1: {
            "chapter": 15,
            "verses": "15.3",
            "translation": "Venus in the first house bestows beauty, attractive eyes, happiness, poetic nature, enjoyment of pleasures, and good fortune.",
            "detailed_effects": [
                "Physical beauty and charm",
                "Artistic and poetic abilities",
                "Enjoyment of life's pleasures",
                "Attractive personality",
                "Material comforts"
            ],
            "positive_effects": [
                "Physical beauty",
                "Artistic talents",
                "Charm and grace",
                "Material comforts",
                "Pleasant personality"
            ],
            "challenging_effects": [
                "May be overly indulgent",
                "Attachment to pleasures"
            ],
            "timing": "Romance and artistic pursuits during Venus dasha"
        },
        7: {
            "chapter": 15,
            "verses": "15.9",
            "translation": "Venus in the 7th house gives a beautiful and virtuous spouse, happiness in marriage, and gains through partnerships.",
            "detailed_effects": [
                "Beautiful and compatible spouse",
                "Harmonious marital life",
                "Success through partnerships",
                "Diplomatic abilities",
                "Material gains from marriage"
            ],
            "positive_effects": [
                "Excellent marriage",
                "Beautiful spouse",
                "Partnership success",
                "Diplomatic skills",
                "Marital happiness"
            ],
            "challenging_effects": [
                "High expectations from partner",
                "May be overly dependent on relationships"
            ],
            "timing": "Marriage during Venus dasha, partnership gains throughout"
        }
    },
    
    "Saturn": {
        1: {
            "chapter": 16,
            "verses": "16.3",
            "translation": "Saturn in the first house makes one lame, suffering from wind diseases, poor, slow in action, cruel, and of wicked disposition.",
            "detailed_effects": [
                "Serious and disciplined nature",
                "Potential health challenges",
                "Slow but steady approach",
                "Hardworking disposition",
                "Challenges in early life"
            ],
            "positive_effects": [
                "Discipline and perseverance",
                "Depth of character",
                "Ability to endure hardships",
                "Wisdom through experience"
            ],
            "challenging_effects": [
                "Health vulnerabilities",
                "Slow progress",
                "Pessimistic tendencies",
                "Early life difficulties"
            ],
            "timing": "Challenges in youth, improvement during and after Saturn dasha"
        },
        10: {
            "chapter": 16,
            "verses": "16.12",
            "translation": "Saturn in the 10th house bestows authority, leadership, success through perseverance, gains from agriculture, and respect in society.",
            "detailed_effects": [
                "Authority and leadership roles",
                "Success through hard work",
                "Gains from land and agriculture",
                "Social respect and recognition",
                "Sustained career growth"
            ],
            "positive_effects": [
                "Authority and power",
                "Career success through effort",
                "Land and property gains",
                "Social respect",
                "Leadership abilities"
            ],
            "challenging_effects": [
                "Slow career progression",
                "Heavy responsibilities",
                "Delays in recognition"
            ],
            "timing": "Authority peaks during Saturn dasha, recognition in later life"
        }
    }
}


def get_phaladeepika_interpretation(planet: str, house: int) -> Dict[str, Any]:
    """
    Get Phaladeepika interpretation for planet in house.
    
    Args:
        planet: Planet name
        house: House number (1-12)
        
    Returns:
        Dictionary with interpretation data or None if not available
    """
    planet_data = PHALADEEPIKA_PLANETS_IN_HOUSES.get(planet, {})
    return planet_data.get(house, None)


def get_available_phaladeepika_combinations() -> list:
    """Get list of available planet-house combinations in Phaladeepika"""
    combinations = []
    for planet, houses in PHALADEEPIKA_PLANETS_IN_HOUSES.items():
        for house in houses.keys():
            combinations.append({"planet": planet, "house": house})
    return combinations
