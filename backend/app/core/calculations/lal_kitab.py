"""
Lal Kitab Astrology System
===========================
PGF Protocol: LAL_KITAB_001
Gate: GATE_5
Version: 1.0.0

Implements the unique Lal Kitab (Red Book) system of Vedic astrology:
- Pakka Ghar (permanent house) concept
- Planet-wise effects in each house
- Remedies (Upay) for planetary afflictions
- Karmic debts (Rin) analysis
- Lal Kitab specific predictions

Based on the original Lal Kitab by Pt. Roop Chand Joshi (1939-1952)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from datetime import datetime


# =============================================================================
# CONSTANTS AND DATA
# =============================================================================

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

HOUSES = list(range(1, 13))

# Pakka Ghar (Permanent House) for each planet in Lal Kitab
# This is where the planet is naturally strong
PAKKA_GHAR = {
    "Sun": 1,      # Sun's permanent house is 1st
    "Moon": 4,     # Moon's permanent house is 4th
    "Mars": 3,     # Mars's permanent house is 3rd
    "Mercury": 7,  # Mercury's permanent house is 7th
    "Jupiter": 2,  # Jupiter's permanent house is 2nd
    "Venus": 7,    # Venus's permanent house is 7th
    "Saturn": 8,   # Saturn's permanent house is 8th
    "Rahu": 12,    # Rahu's permanent house is 12th
    "Ketu": 6      # Ketu's permanent house is 6th
}

# Exalted houses for planets (where they give excellent results)
EXALTED_HOUSES = {
    "Sun": [1, 4],
    "Moon": [1, 2],
    "Mars": [3, 6, 10, 11],
    "Mercury": [3, 5, 6, 7],
    "Jupiter": [2, 5, 9, 12],
    "Venus": [2, 3, 4, 7, 12],
    "Saturn": [3, 6, 11],
    "Rahu": [3, 6],
    "Ketu": [9, 12]
}

# Debilitated houses for planets (where they give poor results)
DEBILITATED_HOUSES = {
    "Sun": [7, 8, 12],
    "Moon": [8, 12],
    "Mars": [4, 8],
    "Mercury": [1, 8, 12],
    "Jupiter": [3, 10],
    "Venus": [6, 9],
    "Saturn": [1, 2, 4],
    "Rahu": [5, 9],
    "Ketu": [3, 7, 11]
}

# Planetary relationships in Lal Kitab (different from Vedic)
FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter", "Ketu"],
    "Mercury": ["Sun", "Venus", "Rahu"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn", "Ketu"],
    "Saturn": ["Mercury", "Venus", "Rahu"],
    "Rahu": ["Mercury", "Venus", "Saturn", "Ketu"],
    "Ketu": ["Mars", "Venus", "Rahu"]
}

ENEMIES = {
    "Sun": ["Saturn", "Rahu", "Ketu"],
    "Moon": ["Rahu", "Ketu"],
    "Mars": ["Mercury", "Rahu"],
    "Mercury": ["Moon", "Ketu"],
    "Jupiter": ["Mercury", "Venus", "Rahu"],
    "Venus": ["Sun", "Moon", "Rahu"],
    "Saturn": ["Sun", "Moon", "Mars"],
    "Rahu": ["Sun", "Moon", "Mars"],
    "Ketu": ["Sun", "Moon"]
}


# =============================================================================
# KARMIC DEBTS (RIN) IN LAL KITAB
# =============================================================================

class KarmicDebt(Enum):
    """Types of Karmic Debts in Lal Kitab"""
    PITRA_RIN = "pitra_rin"           # Ancestors' debt
    MATA_RIN = "mata_rin"             # Mother's debt
    STREE_RIN = "stree_rin"           # Wife/Women's debt
    BRAHMAN_RIN = "brahman_rin"       # Brahmins/Gurus debt
    SWAJATI_RIN = "swajati_rin"       # Self-community debt
    DEVI_RIN = "devi_rin"             # Goddess debt


# Conditions for each type of debt
RIN_CONDITIONS = {
    KarmicDebt.PITRA_RIN: {
        "description": "Debt to ancestors - affects fortune and children",
        "conditions": [
            ("Jupiter", [2, 9, 12], "afflicted"),  # Jupiter afflicted
            ("Sun", [5, 9], "afflicted"),          # Sun afflicted
            ("Ketu", [2, 5], "present")            # Ketu in 2nd or 5th
        ],
        "effects": [
            "Delay in childbirth",
            "Financial instability",
            "Ancestral property disputes",
            "Health issues to father"
        ],
        "remedies_hindi": [
            "पितरों को तर्पण करें",
            "पीपल के पेड़ में जल चढ़ाएं",
            "काले तिल का दान करें"
        ],
        "remedies_english": [
            "Perform Tarpan for ancestors",
            "Offer water to Peepal tree",
            "Donate black sesame seeds"
        ]
    },
    KarmicDebt.MATA_RIN: {
        "description": "Debt to mother - affects peace and prosperity",
        "conditions": [
            ("Moon", [8, 12], "afflicted"),
            ("Venus", [4], "afflicted"),
            ("Rahu", [4], "present")
        ],
        "effects": [
            "Mental unrest",
            "Lack of peace at home",
            "Problems related to property",
            "Health issues to mother"
        ],
        "remedies_hindi": [
            "माँ का आशीर्वाद लें",
            "चांदी का छोटा टुकड़ा बहते पानी में बहाएं",
            "सफेद चीजों का दान करें"
        ],
        "remedies_english": [
            "Seek mother's blessings regularly",
            "Flow small silver piece in running water",
            "Donate white items (milk, rice)"
        ]
    },
    KarmicDebt.STREE_RIN: {
        "description": "Debt to wife/women - affects married life and relations",
        "conditions": [
            ("Venus", [6, 8], "afflicted"),
            ("Moon", [7], "afflicted"),
            ("Saturn", [7], "present")
        ],
        "effects": [
            "Marital discord",
            "Delay in marriage",
            "Problems from female relatives",
            "Reproductive issues"
        ],
        "remedies_hindi": [
            "पत्नी का सम्मान करें",
            "सफेद गाय को रोटी खिलाएं",
            "जवार का दान करें"
        ],
        "remedies_english": [
            "Respect wife and women",
            "Feed white cow with bread",
            "Donate sorghum (jowar)"
        ]
    },
    KarmicDebt.BRAHMAN_RIN: {
        "description": "Debt to teachers/priests - affects wisdom and career",
        "conditions": [
            ("Jupiter", [10], "afflicted"),
            ("Ketu", [9], "present"),
            ("Mercury", [9], "afflicted")
        ],
        "effects": [
            "Career obstacles",
            "Lack of respect in society",
            "Legal problems",
            "Education issues for children"
        ],
        "remedies_hindi": [
            "गुरुजनों का सम्मान करें",
            "पीले रंग की चीजों का दान करें",
            "केसर का तिलक लगाएं"
        ],
        "remedies_english": [
            "Respect elders and teachers",
            "Donate yellow items (turmeric, gold)",
            "Apply saffron tilak"
        ]
    }
}


# =============================================================================
# PLANETARY EFFECTS IN EACH HOUSE (LAL KITAB SPECIFIC)
# =============================================================================

PLANET_HOUSE_EFFECTS = {
    "Sun": {
        1: {
            "result": "excellent",
            "effects_hindi": "राजयोग, उच्च पद, सम्मान, पिता से लाभ",
            "effects_english": "Royal status, high position, respect, benefits from father",
            "health": "Strong constitution, good heart health",
            "remedy_needed": False
        },
        2: {
            "result": "good",
            "effects_hindi": "धन लाभ, परिवार में प्रतिष्ठा",
            "effects_english": "Wealth gains, family respect",
            "health": "Good vision, healthy throat",
            "remedy_needed": False
        },
        3: {
            "result": "mixed",
            "effects_hindi": "भाइयों से विवाद, साहस में कमी",
            "effects_english": "Disputes with siblings, lack of courage",
            "health": "Right arm or shoulder issues",
            "remedy_needed": True
        },
        4: {
            "result": "good",
            "effects_hindi": "माता से सुख, वाहन लाभ, सुख-शांति",
            "effects_english": "Happiness from mother, vehicle gains, peace",
            "health": "Good chest and heart health",
            "remedy_needed": False
        },
        5: {
            "result": "excellent",
            "effects_hindi": "संतान सुख, बुद्धि तीव्र, राजनीतिक सफलता",
            "effects_english": "Happiness from children, sharp intellect, political success",
            "health": "Strong digestive system",
            "remedy_needed": False
        },
        6: {
            "result": "excellent",
            "effects_hindi": "शत्रुओं पर विजय, रोग नाश, न्याय में सफलता",
            "effects_english": "Victory over enemies, disease cure, legal success",
            "health": "Good immunity, overcomes diseases",
            "remedy_needed": False
        },
        7: {
            "result": "poor",
            "effects_hindi": "वैवाहिक कष्ट, साझेदारी में हानि, पिता को कष्ट",
            "effects_english": "Marital problems, partnership losses, father's troubles",
            "health": "Kidney or reproductive issues",
            "remedy_needed": True
        },
        8: {
            "result": "poor",
            "effects_hindi": "अचानक हानि, पैतृक संपत्ति का नुकसान",
            "effects_english": "Sudden losses, ancestral property issues",
            "health": "Chronic diseases, hidden ailments",
            "remedy_needed": True
        },
        9: {
            "result": "mixed",
            "effects_hindi": "धार्मिक रुचि, पिता से मतभेद",
            "effects_english": "Religious inclination, differences with father",
            "health": "Hip or thigh problems",
            "remedy_needed": True
        },
        10: {
            "result": "excellent",
            "effects_hindi": "उच्च पद, राज्य सम्मान, पिता से लाभ",
            "effects_english": "High position, government honors, benefits from father",
            "health": "Strong bones and authority",
            "remedy_needed": False
        },
        11: {
            "result": "excellent",
            "effects_hindi": "अधिक आय, उच्च मित्र मंडली, इच्छा पूर्ति",
            "effects_english": "High income, elite social circle, wish fulfillment",
            "health": "Good circulation",
            "remedy_needed": False
        },
        12: {
            "result": "poor",
            "effects_hindi": "व्यर्थ खर्च, नेत्र रोग, पिता को हानि",
            "effects_english": "Wasteful expenses, eye problems, father's loss",
            "health": "Left eye issues, sleep disorders",
            "remedy_needed": True
        }
    },
    "Moon": {
        1: {
            "result": "excellent",
            "effects_hindi": "मानसिक शांति, माता से सुख, जल से लाभ",
            "effects_english": "Mental peace, happiness from mother, gains from water/liquids",
            "health": "Good mental health, strong immunity",
            "remedy_needed": False
        },
        2: {
            "result": "excellent",
            "effects_hindi": "धन संग्रह, परिवार में सुख, मधुर वाणी",
            "effects_english": "Wealth accumulation, family happiness, sweet speech",
            "health": "Good throat and mouth health",
            "remedy_needed": False
        },
        3: {
            "result": "mixed",
            "effects_hindi": "भाइयों से सहायता, लेकिन मानसिक चिंता",
            "effects_english": "Help from siblings but mental worries",
            "health": "Chest congestion possible",
            "remedy_needed": True
        },
        4: {
            "result": "excellent",
            "effects_hindi": "माता से अत्यधिक सुख, संपत्ति, वाहन",
            "effects_english": "Great happiness from mother, property, vehicles",
            "health": "Strong chest and lungs",
            "remedy_needed": False
        },
        5: {
            "result": "good",
            "effects_hindi": "संतान सुख, रचनात्मकता, प्रेम संबंध",
            "effects_english": "Happiness from children, creativity, love relations",
            "health": "Good stomach health",
            "remedy_needed": False
        },
        6: {
            "result": "poor",
            "effects_hindi": "मातृ पक्ष से विवाद, मानसिक अशांति",
            "effects_english": "Disputes with maternal side, mental unrest",
            "health": "Digestive issues, mental stress",
            "remedy_needed": True
        },
        7: {
            "result": "good",
            "effects_hindi": "सुंदर पत्नी, साझेदारी में लाभ",
            "effects_english": "Beautiful spouse, gains in partnership",
            "health": "Good reproductive health",
            "remedy_needed": False
        },
        8: {
            "result": "poor",
            "effects_hindi": "मानसिक कष्ट, माता को हानि, विरासत में समस्या",
            "effects_english": "Mental suffering, harm to mother, inheritance issues",
            "health": "Chronic mental stress, reproductive issues",
            "remedy_needed": True
        },
        9: {
            "result": "good",
            "effects_hindi": "धार्मिक यात्राएं, गुरु कृपा, भाग्योदय",
            "effects_english": "Religious travels, guru's blessings, fortune rise",
            "health": "Good thigh strength",
            "remedy_needed": False
        },
        10: {
            "result": "excellent",
            "effects_hindi": "जनता में लोकप्रिय, राजनीति में सफलता",
            "effects_english": "Popular among masses, political success",
            "health": "Strong knees and joints",
            "remedy_needed": False
        },
        11: {
            "result": "excellent",
            "effects_hindi": "अधिक आय, मित्रों से लाभ, इच्छा पूर्ति",
            "effects_english": "High income, gains from friends, wish fulfillment",
            "health": "Good blood circulation",
            "remedy_needed": False
        },
        12: {
            "result": "poor",
            "effects_hindi": "नींद में कमी, माता को कष्ट, व्यर्थ खर्च",
            "effects_english": "Sleep deprivation, mother's troubles, wasteful expenses",
            "health": "Sleep disorders, left eye problems",
            "remedy_needed": True
        }
    },
    "Mars": {
        1: {
            "result": "excellent",
            "effects_hindi": "साहसी, नेतृत्व क्षमता, भौतिक संपत्ति",
            "effects_english": "Courageous, leadership qualities, material property",
            "health": "Strong physique, high energy",
            "remedy_needed": False
        },
        2: {
            "result": "mixed",
            "effects_hindi": "कठोर वाणी, पारिवारिक विवाद, धन अस्थिर",
            "effects_english": "Harsh speech, family disputes, unstable wealth",
            "health": "Mouth and throat issues",
            "remedy_needed": True
        },
        3: {
            "result": "excellent",
            "effects_hindi": "भाइयों से सहायता, साहस, पराक्रम",
            "effects_english": "Help from siblings, courage, valor",
            "health": "Strong arms and shoulders",
            "remedy_needed": False
        },
        4: {
            "result": "poor",
            "effects_hindi": "माता से कष्ट, संपत्ति विवाद, घर में अशांति",
            "effects_english": "Troubles to mother, property disputes, home unrest",
            "health": "Chest and heart issues",
            "remedy_needed": True
        },
        5: {
            "result": "mixed",
            "effects_hindi": "संतान से चिंता, निवेश में हानि",
            "effects_english": "Worries from children, investment losses",
            "health": "Stomach issues",
            "remedy_needed": True
        },
        6: {
            "result": "excellent",
            "effects_hindi": "शत्रुओं पर विजय, प्रतिस्पर्धा में सफलता",
            "effects_english": "Victory over enemies, success in competition",
            "health": "Good immunity",
            "remedy_needed": False
        },
        7: {
            "result": "mixed",
            "effects_hindi": "मंगली दोष, वैवाहिक विवाद",
            "effects_english": "Manglik dosha, marital disputes",
            "health": "Reproductive system issues",
            "remedy_needed": True
        },
        8: {
            "result": "poor",
            "effects_hindi": "दुर्घटना, सर्जरी, अचानक हानि",
            "effects_english": "Accidents, surgery, sudden losses",
            "health": "Chronic diseases, accident prone",
            "remedy_needed": True
        },
        9: {
            "result": "good",
            "effects_hindi": "धर्म में रुचि, पिता से विवाद",
            "effects_english": "Interest in religion, disputes with father",
            "health": "Strong thighs",
            "remedy_needed": False
        },
        10: {
            "result": "excellent",
            "effects_hindi": "उच्च पद, सरकारी नौकरी, भूमि लाभ",
            "effects_english": "High position, government job, land gains",
            "health": "Strong bones",
            "remedy_needed": False
        },
        11: {
            "result": "excellent",
            "effects_hindi": "अधिक आय, भाइयों से लाभ, इच्छा पूर्ति",
            "effects_english": "High income, gains from siblings, wish fulfillment",
            "health": "Good circulation",
            "remedy_needed": False
        },
        12: {
            "result": "poor",
            "effects_hindi": "व्यर्थ खर्च, नींद में कमी, विदेश में कष्ट",
            "effects_english": "Wasteful expenses, sleep issues, troubles abroad",
            "health": "Feet problems, insomnia",
            "remedy_needed": True
        }
    }
}

# Continue for remaining planets (abbreviated for length)
# Adding key houses for remaining planets
for planet in ["Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
    if planet not in PLANET_HOUSE_EFFECTS:
        PLANET_HOUSE_EFFECTS[planet] = {}
    for house in range(1, 13):
        if house not in PLANET_HOUSE_EFFECTS.get(planet, {}):
            # Determine basic result based on exalted/debilitated
            if house in EXALTED_HOUSES.get(planet, []):
                result = "good"
                remedy_needed = False
            elif house in DEBILITATED_HOUSES.get(planet, []):
                result = "poor"
                remedy_needed = True
            else:
                result = "mixed"
                remedy_needed = house in [6, 8, 12]
            
            PLANET_HOUSE_EFFECTS[planet][house] = {
                "result": result,
                "effects_hindi": f"{planet} {house}वें भाव में - {'शुभ' if result == 'good' else 'अशुभ' if result == 'poor' else 'मिश्रित'} फल",
                "effects_english": f"{planet} in house {house} - {'beneficial' if result == 'good' else 'malefic' if result == 'poor' else 'mixed'} results",
                "health": "See specific analysis",
                "remedy_needed": remedy_needed
            }


# =============================================================================
# REMEDIES (UPAY) FOR EACH PLANET
# =============================================================================

LAL_KITAB_REMEDIES = {
    "Sun": {
        "general": {
            "hindi": [
                "सूर्य को जल चढ़ाएं (सुबह)",
                "गुड़ और गेहूं का दान करें",
                "माथे पर केसर का तिलक लगाएं",
                "पिता और राजा का सम्मान करें",
                "तांबे का कड़ा पहनें"
            ],
            "english": [
                "Offer water to Sun in morning",
                "Donate jaggery and wheat",
                "Apply saffron tilak on forehead",
                "Respect father and authority figures",
                "Wear copper bangle"
            ]
        },
        "afflicted_houses": {
            7: {
                "hindi": "पत्नी को सोने की चीज भेंट करें",
                "english": "Gift gold item to wife"
            },
            8: {
                "hindi": "बहते पानी में गुड़ बहाएं",
                "english": "Flow jaggery in running water"
            },
            12: {
                "hindi": "बादाम बहते पानी में बहाएं",
                "english": "Flow almonds in running water"
            }
        }
    },
    "Moon": {
        "general": {
            "hindi": [
                "चांदी का छोटा टुकड़ा रखें",
                "दूध का दान करें",
                "माता का आशीर्वाद लें",
                "सफेद चीजें पहनें/खाएं",
                "जल से संबंधित कार्य करें"
            ],
            "english": [
                "Keep small silver piece",
                "Donate milk",
                "Seek mother's blessings",
                "Wear/consume white items",
                "Engage in water-related activities"
            ]
        },
        "afflicted_houses": {
            6: {
                "hindi": "बांस की जड़ घर में रखें",
                "english": "Keep bamboo root in home"
            },
            8: {
                "hindi": "चांदी की गोली बहते पानी में बहाएं",
                "english": "Flow silver ball in running water"
            },
            12: {
                "hindi": "रात को दूध न पिएं",
                "english": "Avoid drinking milk at night"
            }
        }
    },
    "Mars": {
        "general": {
            "hindi": [
                "हनुमान जी की पूजा करें",
                "मसूर दाल का दान करें",
                "लाल रंग का धागा बांधें",
                "मंगलवार का व्रत करें",
                "तांबे का छल्ला पहनें"
            ],
            "english": [
                "Worship Lord Hanuman",
                "Donate red lentils",
                "Tie red thread",
                "Fast on Tuesday",
                "Wear copper ring"
            ]
        },
        "afflicted_houses": {
            4: {
                "hindi": "शहद का दान करें",
                "english": "Donate honey"
            },
            8: {
                "hindi": "मीठी रोटी कुत्ते को खिलाएं",
                "english": "Feed sweet bread to dogs"
            },
            12: {
                "hindi": "बंदरों को गुड़ खिलाएं",
                "english": "Feed jaggery to monkeys"
            }
        }
    },
    "Mercury": {
        "general": {
            "hindi": [
                "हरी चीजों का दान करें",
                "पक्षियों को दाना डालें",
                "मूंग दाल का दान करें",
                "तोते को हरी मिर्च खिलाएं",
                "नाक छेदन करें/कराएं"
            ],
            "english": [
                "Donate green items",
                "Feed grains to birds",
                "Donate moong dal",
                "Feed green chili to parrot",
                "Pierce nose (or get pierced)"
            ]
        }
    },
    "Jupiter": {
        "general": {
            "hindi": [
                "पीले रंग की चीजें पहनें",
                "केसर का तिलक लगाएं",
                "चने की दाल का दान करें",
                "गुरुजनों की सेवा करें",
                "मंदिर में जाएं"
            ],
            "english": [
                "Wear yellow items",
                "Apply saffron tilak",
                "Donate gram dal",
                "Serve elders and teachers",
                "Visit temple regularly"
            ]
        }
    },
    "Venus": {
        "general": {
            "hindi": [
                "सफेद चीजों का दान करें",
                "गाय को आटा खिलाएं",
                "पत्नी का सम्मान करें",
                "जवार का दान करें",
                "चांदी पहनें"
            ],
            "english": [
                "Donate white items",
                "Feed flour to cow",
                "Respect wife",
                "Donate sorghum",
                "Wear silver"
            ]
        }
    },
    "Saturn": {
        "general": {
            "hindi": [
                "काले उड़द का दान करें",
                "कौवों को खाना खिलाएं",
                "शनिवार को तेल दान करें",
                "लोहे की अंगूठी पहनें",
                "सेवकों का सम्मान करें"
            ],
            "english": [
                "Donate black urad dal",
                "Feed crows",
                "Donate oil on Saturday",
                "Wear iron ring",
                "Respect servants and workers"
            ]
        }
    },
    "Rahu": {
        "general": {
            "hindi": [
                "काली सरसों का दान करें",
                "मंदिर में जौ चढ़ाएं",
                "सांप को दूध पिलाएं (पत्थर के)",
                "चांदी पहनें",
                "हाथी दांत न रखें"
            ],
            "english": [
                "Donate black mustard seeds",
                "Offer barley at temple",
                "Offer milk to stone snake",
                "Wear silver",
                "Do not keep ivory"
            ]
        }
    },
    "Ketu": {
        "general": {
            "hindi": [
                "कुत्ते को मीठी रोटी खिलाएं",
                "गणेश जी की पूजा करें",
                "काले और सफेद तिल का दान करें",
                "सोना पहनें",
                "पितरों को तर्पण करें"
            ],
            "english": [
                "Feed sweet bread to dogs",
                "Worship Lord Ganesha",
                "Donate black and white sesame",
                "Wear gold",
                "Perform Tarpan for ancestors"
            ]
        }
    }
}


# =============================================================================
# MAIN CALCULATION CLASSES
# =============================================================================

@dataclass
class LalKitabPlanetAnalysis:
    """Analysis of a planet in Lal Kitab system"""
    planet: str
    house: int
    pakka_ghar: int
    is_in_pakka_ghar: bool
    result_type: str  # excellent, good, mixed, poor
    effects_hindi: str
    effects_english: str
    health_indication: str
    remedy_needed: bool
    remedies_hindi: List[str]
    remedies_english: List[str]
    strength_score: float  # 0-100


@dataclass
class KarmicDebtAnalysis:
    """Analysis of karmic debts"""
    debt_type: KarmicDebt
    is_present: bool
    severity: str  # high, medium, low
    description: str
    effects: List[str]
    remedies_hindi: List[str]
    remedies_english: List[str]


@dataclass
class LalKitabChart:
    """Complete Lal Kitab chart analysis"""
    planets: Dict[str, LalKitabPlanetAnalysis]
    karmic_debts: List[KarmicDebtAnalysis]
    overall_score: float
    lucky_numbers: List[int]
    lucky_colors: List[str]
    favorable_directions: List[str]
    general_predictions_hindi: List[str]
    general_predictions_english: List[str]
    priority_remedies: List[Dict[str, str]]


class LalKitabCalculator:
    """
    Main calculator for Lal Kitab astrology
    """
    
    def __init__(self):
        pass
    
    def analyze_chart(
        self,
        planet_positions: Dict[str, int]  # Planet name -> house number (1-12)
    ) -> LalKitabChart:
        """
        Analyze a chart according to Lal Kitab principles
        
        Args:
            planet_positions: Dictionary mapping planet names to house numbers
            
        Returns:
            Complete Lal Kitab analysis
        """
        # Analyze each planet
        planet_analyses = {}
        for planet, house in planet_positions.items():
            if planet in PLANETS:
                analysis = self._analyze_planet(planet, house)
                planet_analyses[planet] = analysis
        
        # Check karmic debts
        karmic_debts = self._check_karmic_debts(planet_positions)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(planet_analyses)
        
        # Get lucky items
        lucky_numbers = self._get_lucky_numbers(planet_positions)
        lucky_colors = self._get_lucky_colors(planet_positions)
        favorable_directions = self._get_favorable_directions(planet_positions)
        
        # General predictions
        predictions_hindi, predictions_english = self._generate_predictions(
            planet_analyses, karmic_debts
        )
        
        # Priority remedies (most important first)
        priority_remedies = self._get_priority_remedies(planet_analyses, karmic_debts)
        
        return LalKitabChart(
            planets=planet_analyses,
            karmic_debts=karmic_debts,
            overall_score=overall_score,
            lucky_numbers=lucky_numbers,
            lucky_colors=lucky_colors,
            favorable_directions=favorable_directions,
            general_predictions_hindi=predictions_hindi,
            general_predictions_english=predictions_english,
            priority_remedies=priority_remedies
        )
    
    def _analyze_planet(self, planet: str, house: int) -> LalKitabPlanetAnalysis:
        """Analyze a single planet's placement"""
        pakka_ghar = PAKKA_GHAR.get(planet, 1)
        is_in_pakka_ghar = house == pakka_ghar
        
        # Get effects from data
        effects = PLANET_HOUSE_EFFECTS.get(planet, {}).get(house, {})
        result_type = effects.get("result", "mixed")
        
        # Calculate strength score
        strength = 50.0  # Base score
        if is_in_pakka_ghar:
            strength += 30
        if house in EXALTED_HOUSES.get(planet, []):
            strength += 20
        if house in DEBILITATED_HOUSES.get(planet, []):
            strength -= 30
        
        strength = max(0, min(100, strength))
        
        # Get remedies
        remedies = LAL_KITAB_REMEDIES.get(planet, {})
        general_remedies = remedies.get("general", {})
        specific_remedy = remedies.get("afflicted_houses", {}).get(house, {})
        
        remedies_hindi = general_remedies.get("hindi", [])[:3]
        remedies_english = general_remedies.get("english", [])[:3]
        
        if specific_remedy:
            remedies_hindi.insert(0, specific_remedy.get("hindi", ""))
            remedies_english.insert(0, specific_remedy.get("english", ""))
        
        return LalKitabPlanetAnalysis(
            planet=planet,
            house=house,
            pakka_ghar=pakka_ghar,
            is_in_pakka_ghar=is_in_pakka_ghar,
            result_type=result_type,
            effects_hindi=effects.get("effects_hindi", ""),
            effects_english=effects.get("effects_english", ""),
            health_indication=effects.get("health", ""),
            remedy_needed=effects.get("remedy_needed", False),
            remedies_hindi=remedies_hindi,
            remedies_english=remedies_english,
            strength_score=strength
        )
    
    def _check_karmic_debts(
        self,
        planet_positions: Dict[str, int]
    ) -> List[KarmicDebtAnalysis]:
        """Check for karmic debts (rin) in the chart"""
        debts = []
        
        for debt_type, debt_info in RIN_CONDITIONS.items():
            is_present = False
            severity = "low"
            matching_conditions = 0
            
            for planet, houses, condition in debt_info["conditions"]:
                planet_house = planet_positions.get(planet)
                if planet_house and planet_house in houses:
                    matching_conditions += 1
            
            if matching_conditions >= 2:
                is_present = True
                severity = "high" if matching_conditions >= 3 else "medium"
            elif matching_conditions == 1:
                is_present = True
                severity = "low"
            
            if is_present:
                debts.append(KarmicDebtAnalysis(
                    debt_type=debt_type,
                    is_present=True,
                    severity=severity,
                    description=debt_info["description"],
                    effects=debt_info["effects"],
                    remedies_hindi=debt_info["remedies_hindi"],
                    remedies_english=debt_info["remedies_english"]
                ))
        
        return debts
    
    def _calculate_overall_score(
        self,
        planet_analyses: Dict[str, LalKitabPlanetAnalysis]
    ) -> float:
        """Calculate overall chart strength score"""
        if not planet_analyses:
            return 50.0
        
        total = sum(p.strength_score for p in planet_analyses.values())
        return round(total / len(planet_analyses), 1)
    
    def _get_lucky_numbers(self, planet_positions: Dict[str, int]) -> List[int]:
        """Get lucky numbers based on planet placements"""
        numbers = set()
        
        planet_numbers = {
            "Sun": [1, 4], "Moon": [2, 7], "Mars": [3, 9],
            "Mercury": [5], "Jupiter": [3, 6], "Venus": [6, 7],
            "Saturn": [8], "Rahu": [4], "Ketu": [7]
        }
        
        # Add numbers for well-placed planets
        for planet, analysis in planet_positions.items():
            if planet in planet_numbers:
                numbers.update(planet_numbers[planet])
        
        return sorted(list(numbers))[:5]
    
    def _get_lucky_colors(self, planet_positions: Dict[str, int]) -> List[str]:
        """Get lucky colors based on strong planets"""
        colors = []
        
        planet_colors = {
            "Sun": "Orange/Saffron",
            "Moon": "White/Silver",
            "Mars": "Red/Coral",
            "Mercury": "Green",
            "Jupiter": "Yellow/Gold",
            "Venus": "White/Pink",
            "Saturn": "Blue/Black",
            "Rahu": "Grey/Brown",
            "Ketu": "Multi-colored"
        }
        
        # Add colors for well-placed planets (in good houses)
        for planet, house in planet_positions.items():
            if house in EXALTED_HOUSES.get(planet, []):
                if planet in planet_colors:
                    colors.append(planet_colors[planet])
        
        return colors[:4] if colors else ["White", "Yellow"]
    
    def _get_favorable_directions(self, planet_positions: Dict[str, int]) -> List[str]:
        """Get favorable directions"""
        directions = []
        
        planet_directions = {
            "Sun": "East", "Moon": "North-West",
            "Mars": "South", "Mercury": "North",
            "Jupiter": "North-East", "Venus": "South-East",
            "Saturn": "West", "Rahu": "South-West",
            "Ketu": "Up/Spiritual"
        }
        
        # Prioritize directions of well-placed planets
        for planet, house in planet_positions.items():
            if house in EXALTED_HOUSES.get(planet, []) or house == PAKKA_GHAR.get(planet):
                if planet in planet_directions:
                    directions.append(planet_directions[planet])
        
        return directions[:3] if directions else ["East", "North"]
    
    def _generate_predictions(
        self,
        planet_analyses: Dict[str, LalKitabPlanetAnalysis],
        karmic_debts: List[KarmicDebtAnalysis]
    ) -> Tuple[List[str], List[str]]:
        """Generate general predictions in Hindi and English"""
        hindi = []
        english = []
        
        # Count good and bad placements
        good_count = sum(1 for p in planet_analyses.values() if p.result_type in ["excellent", "good"])
        poor_count = sum(1 for p in planet_analyses.values() if p.result_type == "poor")
        
        if good_count >= 5:
            hindi.append("आपका जन्म कुंडली बहुत शुभ है। जीवन में सफलता मिलेगी।")
            english.append("Your birth chart is very auspicious. Success in life is indicated.")
        elif poor_count >= 4:
            hindi.append("कुछ ग्रह कमजोर हैं। उपायों से लाभ होगा।")
            english.append("Some planets are weak. Remedies will help.")
        else:
            hindi.append("मिश्रित फल वाली कुंडली है। संतुलित जीवन जिएं।")
            english.append("Mixed results in chart. Live a balanced life.")
        
        # Add predictions based on key planets
        if "Sun" in planet_analyses:
            sun = planet_analyses["Sun"]
            if sun.result_type in ["excellent", "good"]:
                hindi.append("सूर्य शुभ है - पिता और राज्य से लाभ।")
                english.append("Sun is favorable - benefits from father and government.")
        
        if "Moon" in planet_analyses:
            moon = planet_analyses["Moon"]
            if moon.result_type == "poor":
                hindi.append("चंद्रमा कमजोर है - माता की सेवा करें।")
                english.append("Moon is weak - serve your mother.")
        
        # Add debt-related predictions
        if karmic_debts:
            hindi.append(f"{len(karmic_debts)} प्रकार के ऋण पाए गए। उपाय आवश्यक।")
            english.append(f"{len(karmic_debts)} karmic debt(s) found. Remedies required.")
        
        return hindi, english
    
    def _get_priority_remedies(
        self,
        planet_analyses: Dict[str, LalKitabPlanetAnalysis],
        karmic_debts: List[KarmicDebtAnalysis]
    ) -> List[Dict[str, str]]:
        """Get priority-ordered remedies"""
        remedies = []
        
        # First add remedies for karmic debts (highest priority)
        for debt in karmic_debts:
            if debt.severity in ["high", "medium"]:
                remedies.append({
                    "priority": "high",
                    "reason": debt.description,
                    "remedy_hindi": debt.remedies_hindi[0] if debt.remedies_hindi else "",
                    "remedy_english": debt.remedies_english[0] if debt.remedies_english else ""
                })
        
        # Add remedies for afflicted planets
        for planet, analysis in planet_analyses.items():
            if analysis.remedy_needed and analysis.result_type == "poor":
                remedies.append({
                    "priority": "medium",
                    "reason": f"{planet} in house {analysis.house}",
                    "remedy_hindi": analysis.remedies_hindi[0] if analysis.remedies_hindi else "",
                    "remedy_english": analysis.remedies_english[0] if analysis.remedies_english else ""
                })
        
        return remedies[:10]  # Top 10 remedies


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_lal_kitab_analysis(planet_houses: Dict[str, int]) -> Dict[str, Any]:
    """
    Get complete Lal Kitab analysis for a chart
    
    Args:
        planet_houses: Dictionary mapping planet names to house numbers (1-12)
        
    Returns:
        Complete Lal Kitab analysis dictionary
    """
    calculator = LalKitabCalculator()
    chart = calculator.analyze_chart(planet_houses)
    
    return {
        "planets": {
            planet: {
                "house": analysis.house,
                "pakka_ghar": analysis.pakka_ghar,
                "in_pakka_ghar": analysis.is_in_pakka_ghar,
                "result": analysis.result_type,
                "effects": {
                    "hindi": analysis.effects_hindi,
                    "english": analysis.effects_english
                },
                "health": analysis.health_indication,
                "strength": analysis.strength_score,
                "needs_remedy": analysis.remedy_needed,
                "remedies": {
                    "hindi": analysis.remedies_hindi,
                    "english": analysis.remedies_english
                }
            }
            for planet, analysis in chart.planets.items()
        },
        "karmic_debts": [
            {
                "type": debt.debt_type.value,
                "present": debt.is_present,
                "severity": debt.severity,
                "description": debt.description,
                "effects": debt.effects,
                "remedies": {
                    "hindi": debt.remedies_hindi,
                    "english": debt.remedies_english
                }
            }
            for debt in chart.karmic_debts
        ],
        "overall_score": chart.overall_score,
        "lucky": {
            "numbers": chart.lucky_numbers,
            "colors": chart.lucky_colors,
            "directions": chart.favorable_directions
        },
        "predictions": {
            "hindi": chart.general_predictions_hindi,
            "english": chart.general_predictions_english
        },
        "priority_remedies": chart.priority_remedies
    }


def get_planet_remedy(planet: str, house: int) -> Dict[str, Any]:
    """
    Get specific remedy for a planet in a house
    
    Args:
        planet: Planet name
        house: House number (1-12)
        
    Returns:
        Remedy details
    """
    remedies = LAL_KITAB_REMEDIES.get(planet, {})
    general = remedies.get("general", {})
    specific = remedies.get("afflicted_houses", {}).get(house, {})
    
    return {
        "planet": planet,
        "house": house,
        "general_remedies": {
            "hindi": general.get("hindi", []),
            "english": general.get("english", [])
        },
        "specific_remedy": {
            "hindi": specific.get("hindi", ""),
            "english": specific.get("english", "")
        } if specific else None
    }
