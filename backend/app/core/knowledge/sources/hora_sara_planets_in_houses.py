"""
Hora Sara: Planets in Houses
==============================
Digitized interpretations from Hora Sara by Prithuyasas
Detailed planet-in-house analysis

Translation: R. Santhanam (1996)
Source: Ranjan Publications

Hora Sara provides detailed predictive interpretations for planetary placements.
"""

from typing import Dict, Any


HORA_SARA_PLANETS_IN_HOUSES: Dict[str, Dict[int, Dict[str, Any]]] = {
    "Sun": {
        1: {
            "chapter": 7,
            "verses": "7.1-2",
            "translation": "If the Sun occupies the ascendant, the native will have a lean body, be courageous, will have weak eyes, be valorous, firm in his decisions, will have weak hair, be impatient, and will have a bilious temperament.",
            "detailed_effects": [
                "Lean and athletic body type",
                "Courageous and brave nature",
                "Weak eyesight or eye problems",
                "Valorous and heroic",
                "Firm and decisive",
                "Thin or weak hair",
                "Impatient temperament",
                "Bilious constitution (Pitta dominant)"
            ],
            "positive_effects": [
                "Courage and valor",
                "Firm decision-making",
                "Athletic build",
                "Leadership qualities"
            ],
            "challenging_effects": [
                "Weak eyes",
                "Impatience",
                "Hair problems",
                "Bilious health issues"
            ],
            "timing": "Physical traits manifest from birth, leadership develops with age",
            "tags": ["personality", "health", "courage", "appearance"],
            "confidence": "high",
            "notes": "Hora Sara provides detailed physical and temperamental descriptions"
        },
        2: {
            "chapter": 7,
            "verses": "7.3",
            "translation": "The Sun in the 2nd house makes one learned in Shastras, will have an angry disposition, will serve others, will have a diseased face, and will be devoid of wealth and happiness.",
            "detailed_effects": [
                "Learned in scriptures and philosophy",
                "Angry and wrathful temperament",
                "Service to others or employers",
                "Facial health issues",
                "Financial struggles",
                "Lack of happiness"
            ],
            "positive_effects": [
                "Scholarly knowledge",
                "Service-oriented"
            ],
            "challenging_effects": [
                "Anger problems",
                "Facial diseases",
                "Financial difficulties",
                "Unhappiness"
            ],
            "timing": "Learning throughout life, financial struggles persistent",
            "tags": ["wealth", "speech", "education", "health"],
            "confidence": "high"
        },
        3: {
            "chapter": 7,
            "verses": "7.4",
            "translation": "With the Sun in the 3rd house, one will be valorous, strong, will lose co-born, be liberal, charitable, and will have good qualities.",
            "detailed_effects": [
                "Valorous and courageous",
                "Physical strength",
                "Loss of siblings or strained relations",
                "Liberal and generous nature",
                "Charitable disposition",
                "Good moral qualities"
            ],
            "positive_effects": [
                "Valor and courage",
                "Physical strength",
                "Generosity",
                "Charity",
                "Good character"
            ],
            "challenging_effects": [
                "Loss of siblings",
                "Sibling conflicts"
            ],
            "timing": "Courage throughout life, sibling issues in youth",
            "tags": ["courage", "siblings", "character", "charity"],
            "confidence": "high"
        },
        4: {
            "chapter": 7,
            "verses": "7.5",
            "translation": "If the Sun is in the 4th house, one will be devoid of conveyances and relatives, will suffer heart diseases, will destroy paternal house and wealth, and will serve a bad king.",
            "detailed_effects": [
                "Lack of vehicles",
                "Few relatives or isolation",
                "Heart and cardiac problems",
                "Destruction of father's property",
                "Loss of paternal wealth",
                "Service under difficult authority"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "No vehicles",
                "Social isolation",
                "Heart disease",
                "Property losses",
                "Difficult employment"
            ],
            "timing": "Property issues throughout, heart health concerns in middle age",
            "tags": ["mother", "property", "health", "vehicles"],
            "confidence": "high",
            "notes": "Sun in 4th (Maraka house) gives multiple challenges"
        },
        5: {
            "chapter": 7,
            "verses": "7.6",
            "translation": "The Sun in the 5th house denotes that one will be bereft of happiness, wealth, and sons, will live in foreign places, be intelligent, and will have heart diseases.",
            "detailed_effects": [
                "Lack of happiness",
                "Financial difficulties",
                "Issues with children or childlessness",
                "Life in foreign lands",
                "High intelligence",
                "Heart and cardiac problems"
            ],
            "positive_effects": [
                "High intelligence",
                "Foreign opportunities"
            ],
            "challenging_effects": [
                "Unhappiness",
                "Poverty",
                "Children problems",
                "Heart disease"
            ],
            "timing": "Children issues during procreative years, intelligence throughout",
            "tags": ["children", "intelligence", "wealth", "health"],
            "confidence": "high"
        },
        6: {
            "chapter": 7,
            "verses": "7.7",
            "translation": "If the Sun occupies the 6th house, one will be very strong, will be a king or equal to a king, will have enmity with his relatives, and will conquer his enemies.",
            "detailed_effects": [
                "Exceptional physical strength",
                "Authority and leadership (king-like)",
                "Conflicts with relatives",
                "Victory over enemies",
                "Power and dominance"
            ],
            "positive_effects": [
                "Physical strength",
                "Authority and power",
                "Victory over enemies",
                "Leadership"
            ],
            "challenging_effects": [
                "Relative conflicts",
                "Family enmity"
            ],
            "timing": "Strength throughout life, authority in career years",
            "tags": ["health", "enemies", "authority", "relatives"],
            "confidence": "high",
            "notes": "Sun in 6th (Upachaya) gives strength and victory"
        },
        7: {
            "chapter": 7,
            "verses": "7.8",
            "translation": "The Sun in the 7th house makes one suffer from diseases, will have a diseased wife, be devoid of wealth, will wander, and will suffer humiliation.",
            "detailed_effects": [
                "Chronic health problems",
                "Spouse with health issues",
                "Financial losses",
                "Wandering or travel",
                "Loss of dignity and respect"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Health problems",
                "Spouse's ill health",
                "Poverty",
                "Wandering life",
                "Humiliation"
            ],
            "timing": "Marital and health issues after marriage",
            "tags": ["marriage", "health", "wealth", "dignity"],
            "confidence": "high"
        },
        8: {
            "chapter": 7,
            "verses": "7.9",
            "translation": "With the Sun in the 8th house, one will have defective eyes, be devoid of wealth and happiness, will suffer from diseases, and will have a short life.",
            "detailed_effects": [
                "Eye defects or blindness",
                "Poverty and financial struggles",
                "Lack of happiness",
                "Chronic diseases",
                "Reduced longevity"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Eye problems",
                "Financial losses",
                "Unhappiness",
                "Health issues",
                "Short lifespan"
            ],
            "timing": "Multiple challenges throughout life",
            "tags": ["longevity", "wealth", "health", "eyes"],
            "confidence": "high",
            "notes": "Sun in 8th (Dusthana) gives severe afflictions"
        },
        9: {
            "chapter": 7,
            "verses": "7.10",
            "translation": "If the Sun is in the 9th house, one will be devoid of wealth, children, and happiness, will be irreligious, and will lose his father.",
            "detailed_effects": [
                "Financial difficulties",
                "Issues with children",
                "Lack of happiness",
                "Irreligious tendencies",
                "Loss of father or conflict"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Poverty",
                "Children problems",
                "Unhappiness",
                "Lack of dharma",
                "Father's loss"
            ],
            "timing": "Father-related effects in youth, dharma issues throughout",
            "tags": ["dharma", "father", "children", "wealth"],
            "confidence": "high"
        },
        10: {
            "chapter": 7,
            "verses": "7.11",
            "translation": "The Sun in the 10th house makes one learned, will perform good acts, be a king or minister, will have sons, be virtuous, and will have conveyances.",
            "detailed_effects": [
                "Scholarly and learned",
                "Virtuous actions",
                "Authority position (king/minister)",
                "Good children",
                "Virtuous character",
                "Vehicles and conveyances"
            ],
            "positive_effects": [
                "Learning and wisdom",
                "Authority and power",
                "Good progeny",
                "Virtue",
                "Vehicles"
            ],
            "challenging_effects": [],
            "timing": "Career success throughout, authority in middle age",
            "tags": ["career", "authority", "virtue", "children"],
            "confidence": "high",
            "notes": "Sun in 10th (own house) is very strong and auspicious"
        },
        11: {
            "chapter": 7,
            "verses": "7.12",
            "translation": "If the Sun occupies the 11th house, one will be long-lived, will have abundant wealth, be endowed with sons, be happy, and will have limited diseases.",
            "detailed_effects": [
                "Long lifespan",
                "Abundant wealth and gains",
                "Good children",
                "Overall happiness",
                "Strong health with minimal diseases"
            ],
            "positive_effects": [
                "Longevity",
                "Wealth and gains",
                "Good progeny",
                "Happiness",
                "Good health"
            ],
            "challenging_effects": [],
            "timing": "Gains throughout life, peak during Sun dasha",
            "tags": ["wealth", "gains", "longevity", "children"],
            "confidence": "high",
            "notes": "Sun in 11th (Upachaya/gains) is very favorable"
        },
        12: {
            "chapter": 7,
            "verses": "7.13",
            "translation": "The Sun in the 12th house makes one have defective eyes, be devoid of wealth, will have limited sons, be inimical to his father, and will have a weak body.",
            "detailed_effects": [
                "Eye defects or vision problems",
                "Poverty and financial losses",
                "Few children or childlessness",
                "Conflict with father",
                "Weak physical constitution"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Eye problems",
                "Financial losses",
                "Children issues",
                "Father conflicts",
                "Weak health"
            ],
            "timing": "Multiple challenges throughout life",
            "tags": ["losses", "health", "father", "children"],
            "confidence": "high",
            "notes": "Sun in 12th (Dusthana/losses) gives multiple afflictions"
        }
    },
    
    "Moon": {
        1: {
            "chapter": 8,
            "verses": "8.1",
            "translation": "Moon in 1st makes one fickle-minded, handsome, with beautiful eyes, fond of water, kind-hearted, and soft-spoken.",
            "detailed_effects": [
                "Fickle and changeable mind",
                "Handsome appearance",
                "Beautiful eyes",
                "Love for water and liquids",
                "Kind and compassionate",
                "Soft and gentle speech"
            ],
            "positive_effects": [
                "Beauty",
                "Kind nature",
                "Soft speech",
                "Compassion"
            ],
            "challenging_effects": [
                "Mental fickleness",
                "Changeable moods"
            ],
            "timing": "Emotional patterns throughout life",
            "tags": ["personality", "appearance", "emotions", "temperament"],
            "confidence": "high"
        },
        4: {
            "chapter": 8,
            "verses": "8.4",
            "translation": "Moon in 4th gives happiness, mother's blessings, property, vehicles, comforts, and good friends.",
            "detailed_effects": [
                "Domestic happiness",
                "Mother's blessings and grace",
                "Property and land ownership",
                "Vehicles and conveyances",
                "Material comforts",
                "Good friendships"
            ],
            "positive_effects": [
                "Happiness",
                "Mother's grace",
                "Property",
                "Vehicles",
                "Comforts",
                "Friends"
            ],
            "challenging_effects": [],
            "timing": "Property during Moon dasha, happiness throughout",
            "tags": ["mother", "property", "happiness", "vehicles"],
            "confidence": "high"
        },
        7: {
            "chapter": 8,
            "verses": "8.7",
            "translation": "Moon in 7th gives beautiful spouse, passionate nature, wealth, and happiness in marriage.",
            "detailed_effects": [
                "Beautiful and attractive spouse",
                "Passionate and romantic nature",
                "Wealth through marriage",
                "Marital happiness",
                "Emotional fulfillment"
            ],
            "positive_effects": [
                "Beautiful spouse",
                "Marital bliss",
                "Wealth",
                "Passion"
            ],
            "challenging_effects": [],
            "timing": "Marriage during Moon dasha",
            "tags": ["marriage", "wealth", "happiness", "passion"],
            "confidence": "high"
        },
        10: {
            "chapter": 8,
            "verses": "8.10",
            "translation": "Moon in 10th gives success, intelligence, fame, virtue, and respect.",
            "detailed_effects": [
                "Professional success",
                "High intelligence",
                "Fame and recognition",
                "Virtuous character",
                "Social respect"
            ],
            "positive_effects": [
                "Career success",
                "Intelligence",
                "Fame",
                "Virtue",
                "Respect"
            ],
            "challenging_effects": [],
            "timing": "Career success during Moon dasha",
            "tags": ["career", "fame", "intelligence", "virtue"],
            "confidence": "high"
        }
    }
}


def get_hora_sara_interpretation(planet: str, house: int) -> Dict[str, Any]:
    """
    Get Hora Sara interpretation for planet in house.
    
    Args:
        planet: Planet name
        house: House number (1-12)
        
    Returns:
        Dictionary with interpretation data or None if not available
    """
    planet_data = HORA_SARA_PLANETS_IN_HOUSES.get(planet, {})
    return planet_data.get(house, None)


def get_available_hora_sara_combinations() -> list:
    """Get list of available planet-house combinations in Hora Sara"""
    combinations = []
    for planet, houses in HORA_SARA_PLANETS_IN_HOUSES.items():
        for house in houses.keys():
            combinations.append({"planet": planet, "house": house})
    return combinations
