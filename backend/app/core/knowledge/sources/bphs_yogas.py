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

from typing import Any, Dict, List

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
                "Conjunction in 10th house - exceptional for career",
            ],
        },
        "examples": [
            "9th lord Jupiter conjunct 10th lord Saturn in 10th house",
            "9th lord Sun in 10th house aspecting 10th lord Mars in 9th",
            "9th lord and 10th lord in parivartana (exchange houses)",
        ],
        "cancellation_factors": [
            "Severe affliction by malefics",
            "Combustion of both planets",
            "Placement in 6th, 8th, or 12th houses (dusthana) without dignity",
            "Aspect from multiple malefics",
        ],
        "strength_assessment": {
            "very_strong": "Both planets exalted or in own signs, in kendras, no affliction",
            "strong": "One planet well-placed, mutual aspect, minimal affliction",
            "moderate": "Basic connection present but with some weaknesses",
            "weak": "Connection through aspect only, with afflictions",
        },
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
            "timing": "Most pronounced during dashas of the yoga-forming planets",
        },
        "examples": [
            "1st lord (kendra) with 5th lord (trikona) in conjunction",
            "4th lord aspecting 9th lord",
            "10th lord and 5th lord in parivartana",
            "7th lord conjunct 1st lord (both kendra, but 1st is also trikona)",
        ],
        "special_notes": [
            "1st and 10th lord connection is particularly powerful (self + career)",
            "4th and 5th lord connection excellent for property and children",
            "Involvement of 9th lord brings fortune and dharma",
        ],
        "cancellation_factors": [
            "Both planets weak by sign placement",
            "Severe malefic affliction",
            "Placement in dusthanas (6,8,12) without strength",
        ],
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
            "family": "Happy family life with good children",
        },
        "strength_factors": [
            "Jupiter and Moon both strong by sign",
            "Jupiter in own sign (Sagittarius/Pisces) or exalted (Cancer)",
            "Moon waxing and in good dignity",
            "No malefic aspects to Jupiter or Moon",
            "Formation in kendra from lagna amplifies results",
        ],
        "strength_assessment": {
            "very_strong": "Jupiter exalted in Cancer with waxing Moon - exceptional wisdom and fortune",
            "strong": "Jupiter in own sign in kendra from strong Moon",
            "moderate": "Jupiter in kendra from Moon but with some afflictions",
            "weak": "Jupiter weak by sign or Moon heavily afflicted",
        },
        "timing": "Most powerful during Jupiter mahadasha or Moon mahadasha. Also strong in Jupiter-Moon antardashas.",
        "modern_interpretation": "This yoga indicates someone who combines emotional intelligence (Moon) with wisdom and expansion (Jupiter). Such natives make good teachers, counselors, and spiritual guides.",
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
            "Debilitated planet is retrograde (partial cancellation)",
        ],
        "effects": {
            "general": "Rise from humble beginnings to great heights. Success through overcoming obstacles. The native becomes extraordinarily strong in the planet's significations.",
            "life_pattern": "Initial struggles followed by dramatic rise. The adversity faced early becomes the source of strength.",
            "special_quality": "Develops exceptional skill and mastery in areas of the debilitated planet through overcoming challenges.",
        },
        "examples": [
            "Sun debilitated in Libra but Venus (Libra lord) in kendra - cancellation",
            "Moon debilitated in Scorpio but Mars (Scorpio lord) exalted - cancellation",
            "Saturn debilitated in Aries but Mars in kendra from Moon - cancellation",
        ],
        "strength_assessment": {
            "very_strong": "Multiple cancellation factors present",
            "strong": "One complete cancellation factor",
            "partial": "Debilitated planet aspected by friends or in good house",
        },
    },
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
            "timing": "Wealth accumulates during dashas of these planets",
        },
        "strength_factors": [
            "Both lords in wealth houses (2, 11, 5, 9)",
            "Association in kendra houses increases stability",
            "No malefic affliction",
            "Planets in own signs or exalted",
        ],
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
            "protection": "Protected from severe financial losses",
        },
        "formation_variations": [
            "9th lord in own sign in kendra",
            "9th lord exalted in trikona",
            "9th lord in conjunction with Venus or Jupiter (natural wealth givers)",
        ],
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
            "dharma": "Wealth earned through righteous means brings lasting satisfaction",
        },
        "timing": "Particularly strong during dashas of 5th and 9th lords",
    },
}

BPHS_ARISHTA_YOGAS: Dict[str, Dict[str, Any]] = {
    "Daridra_Yoga": {
        "chapter": 44,
        "verses": "44.3-5",
        "category": "Arishta Yoga",
        "formation": "Lord of 11th house in 6th, 8th, or 12th house (dusthana)",
        "classical_description": "Daridra means poverty. When the lord of gains (11th) occupies a dusthana, it creates obstacles to wealth accumulation and financial difficulties.",
        "effects": {
            "general": "Financial difficulties, poverty, obstacles to wealth accumulation",
            "wealth": "Chronic financial struggles, inability to save money, losses of gains",
            "career": "Obstacles in achieving financial goals, income instability",
            "timing": "Most pronounced during dasha of 11th lord",
        },
        "strength_factors": [
            "11th lord in 8th house - most severe (sudden losses)",
            "11th lord in 12th house - severe (constant expenses)",
            "11th lord in 6th house - moderate (debts and conflicts)",
            "Affliction by malefics increases severity",
        ],
        "cancellation_factors": [
            "11th lord in own sign or exaltation despite dusthana placement",
            "Strong aspect from Jupiter or benefics",
            "Formation of Raja Yoga or Dhana Yoga simultaneously",
            "11th lord in Vargottama (same sign in D1 and D9)",
        ],
        "remedies": [
            "Strengthen 11th lord through gemstone if appropriate",
            "Worship deity associated with 11th lord planet",
            "Charity and service to reduce karmic debt",
            "Avoid speculation and risky investments",
        ],
    },
    "Duryoga": {
        "chapter": 44,
        "verses": "44.6-8",
        "category": "Arishta Yoga",
        "formation": "Lord of 10th house in 6th, 8th, or 12th house",
        "classical_description": "Duryoga means bad combination. When the lord of career (10th) occupies a dusthana, it creates professional difficulties and obstacles to success.",
        "effects": {
            "general": "Career obstacles, professional setbacks, loss of reputation",
            "career": "Difficulties in profession, job instability, conflicts with authority",
            "reputation": "Damage to public image, loss of status",
            "health": "Work-related stress and health issues",
            "timing": "Career challenges during 10th lord dasha",
        },
        "strength_factors": [
            "10th lord in 8th house - severe (sudden career losses)",
            "10th lord in 12th house - severe (foreign employment, losses)",
            "10th lord in 6th house - moderate (service positions, conflicts)",
        ],
        "cancellation_factors": [
            "10th lord in own sign or exaltation",
            "Raja Yoga formation simultaneously",
            "Strong benefic aspects",
            "10th lord conjunct or aspected by 9th lord",
        ],
    },
    "Kemadruma_Yoga": {
        "chapter": 44,
        "verses": "44.15-17",
        "category": "Arishta Yoga",
        "formation": "Moon without planets in houses 2nd and 12th from it (Moon isolated)",
        "classical_description": "Kemadruma means 'without support'. When Moon has no planets on either side, the native lacks emotional and material support.",
        "effects": {
            "general": "Poverty, lack of support, emotional isolation, mental distress",
            "emotional": "Loneliness, lack of emotional support, mental anxiety",
            "wealth": "Financial difficulties, lack of resources",
            "relationships": "Difficulty forming lasting bonds, isolation",
            "health": "Mental health challenges, depression tendencies",
        },
        "strength_factors": [
            "Moon weak by sign or afflicted - most severe",
            "Moon in dusthana (6,8,12) - very severe",
            "No benefic aspects to Moon - severe",
        ],
        "cancellation_factors": [
            "Planets in kendras (1,4,7,10) from Moon",
            "Moon in kendra from ascendant",
            "Moon in own sign (Cancer) or exaltation (Taurus)",
            "Jupiter aspecting Moon",
            "Moon conjunct benefic planet",
        ],
        "notes": "One of the most important Arishta yogas. Cancellation is common, so check carefully.",
    },
    "Shakata_Yoga": {
        "chapter": 44,
        "verses": "44.18-20",
        "category": "Arishta Yoga",
        "formation": "Jupiter in 6th, 8th, or 12th house from Moon",
        "classical_description": "Shakata means 'cart'. Like a cart that goes up and down, this yoga creates fluctuating fortunes and instability.",
        "effects": {
            "general": "Fluctuating fortunes, ups and downs in life, instability",
            "wealth": "Financial instability, gains followed by losses",
            "career": "Career fluctuations, periods of success and failure",
            "emotional": "Emotional ups and downs, lack of stability",
            "timing": "Fluctuations throughout life, especially in Jupiter and Moon dashas",
        },
        "strength_factors": [
            "Jupiter in 8th from Moon - most severe",
            "Jupiter weak by sign - severe",
            "Moon also weak - very severe",
        ],
        "cancellation_factors": [
            "Jupiter in own sign or exaltation",
            "Jupiter in kendra from ascendant",
            "Strong benefic aspects to Jupiter or Moon",
            "Formation of Gaja Kesari Yoga (Jupiter in kendra from Moon)",
        ],
    },
    "Graha_Yuddha_Dosha": {
        "chapter": 44,
        "verses": "44.25-27",
        "category": "Arishta Yoga",
        "formation": "Planetary war - two planets within 1 degree in same sign (excluding Sun, Moon, Rahu, Ketu)",
        "classical_description": "When planets are in close combat (Graha Yuddha), the defeated planet loses strength and creates difficulties in its significations.",
        "effects": {
            "general": "Conflict in planetary significations, weakened results of defeated planet",
            "specific": "Depends on which planet is defeated - that planet's significations suffer",
            "timing": "Effects manifest during dashas of defeated planet",
        },
        "strength_factors": [
            "Defeated planet's significations severely weakened",
            "Victor planet's significations strengthened",
            "Degree difference <0.5° - most severe combat",
        ],
        "cancellation_factors": [
            "Defeated planet in own sign or exaltation",
            "Strong benefic aspects to defeated planet",
            "Defeated planet forms other strong yogas",
        ],
        "notes": "Determine victor by brightness/size: Mars>Mercury>Jupiter>Venus>Saturn",
    },
    "Vipareeta_Raja_Yoga": {
        "chapter": 44,
        "verses": "44.30-32",
        "category": "Special Yoga",
        "formation": "Lords of dusthanas (6,8,12) in dusthanas, or in mutual exchange",
        "classical_description": "Vipareeta means 'reversed'. Paradoxically, when dusthana lords occupy dusthanas, they create Raja Yoga-like effects through overcoming adversities.",
        "effects": {
            "general": "Success through adversity, gains from enemies' losses, unexpected fortune",
            "career": "Rise after setbacks, success in crisis management",
            "wealth": "Gains from unexpected sources, inheritance, enemies' losses",
            "reputation": "Fame through overcoming obstacles",
            "timing": "Benefits manifest during dusthana lords' dashas",
        },
        "types": [
            "Harsha Yoga: 6th lord in 6th, 8th, or 12th",
            "Sarala Yoga: 8th lord in 8th, 6th, or 12th",
            "Vimala Yoga: 12th lord in 12th, 6th, or 8th",
        ],
        "strength_factors": [
            "Dusthana lord in own sign - stronger",
            "Multiple Vipareeta yogas - very strong",
            "No affliction to dusthana lords - pure results",
        ],
        "notes": "Unique yoga that turns adversity into advantage. Highly valued in predictive astrology.",
    },
    "Kala_Sarpa_Yoga": {
        "chapter": 45,
        "verses": "45.10-12",
        "category": "Arishta Yoga",
        "formation": "All seven planets (Sun through Saturn) hemmed between Rahu and Ketu",
        "classical_description": "Kala Sarpa means 'serpent of time'. When all planets are trapped between the lunar nodes, it creates intense karmic patterns and obstacles.",
        "effects": {
            "general": "Intense life experiences, karmic challenges, obstacles and delays",
            "psychological": "Mental restlessness, anxiety, obsessive tendencies",
            "career": "Obstacles to success, sudden rises and falls",
            "relationships": "Challenges in relationships, separations",
            "spiritual": "Strong spiritual inclinations, interest in occult",
            "timing": "Effects vary by Rahu-Ketu axis and which houses they occupy",
        },
        "strength_factors": [
            "Partial Kala Sarpa (one planet outside) - milder",
            "Complete Kala Sarpa - severe",
            "Rahu-Ketu in dusthanas - more challenging",
            "Rahu-Ketu in kendras/trikonas - more manageable",
        ],
        "cancellation_factors": [
            "Even one planet outside Rahu-Ketu axis",
            "Strong benefic yogas present",
            "Exalted planets within the axis",
            "Jupiter or Venus strong and well-placed",
        ],
        "remedies": [
            "Rahu-Ketu remedies (Naga Dosha remedies)",
            "Worship of Lord Shiva or Subramanya",
            "Sarpa Dosha puja at specific temples",
            "Strengthen benefic planets in chart",
        ],
        "notes": "Controversial yoga - some astrologers consider it overemphasized. Effects depend heavily on overall chart strength.",
    },
    "Graha_Malika_Yoga": {
        "chapter": 45,
        "verses": "45.15-17",
        "category": "Special Yoga",
        "formation": "Planets occupying consecutive houses forming a chain/garland pattern",
        "classical_description": "Graha Malika means 'planetary garland'. When planets occupy consecutive houses, they create a chain of connected energies.",
        "effects": {
            "general": "Balanced life experiences, systematic progress, connected life areas",
            "personality": "Well-rounded character, multiple talents",
            "career": "Success through systematic approach, gradual growth",
            "timing": "Effects depend on which houses are occupied and starting point",
        },
        "types": [
            "Starting from 1st house - strong personality focus",
            "Starting from 10th house - strong career focus",
            "Longer chains (7+ houses) - more powerful",
        ],
        "strength_factors": [
            "More consecutive houses - stronger",
            "Planets in own signs or exaltation - very strong",
            "No breaks in the chain - pure results",
        ],
    },
    "Dur_Yoga": {
        "chapter": 44,
        "verses": "44.35-37",
        "category": "Arishta Yoga",
        "formation": "Lord of 2nd or 12th house in dusthana, or malefics in 2nd/12th",
        "classical_description": "Creates difficulties in wealth accumulation, family life, and causes excessive expenses.",
        "effects": {
            "general": "Financial difficulties, family problems, excessive expenses",
            "wealth": "Loss of wealth, inability to save, chronic debt",
            "family": "Family conflicts, separation from family",
            "speech": "Harsh speech causing problems",
            "eyes": "Eye problems if 2nd lord severely afflicted",
        },
        "cancellation_factors": ["2nd/12th lords in own signs", "Strong benefic aspects", "Formation of Dhana Yoga"],
    },
    "Matru_Dosha": {
        "chapter": 44,
        "verses": "44.40-42",
        "category": "Arishta Yoga",
        "formation": "Moon or 4th lord severely afflicted, or malefics in 4th house",
        "classical_description": "Creates difficulties related to mother, domestic happiness, and emotional well-being.",
        "effects": {
            "general": "Mother's health issues, lack of domestic happiness, emotional challenges",
            "mother": "Mother's early death, separation, or health problems",
            "domestic": "Lack of peace at home, property issues",
            "emotional": "Emotional instability, mental distress",
            "education": "Obstacles in education",
        },
        "cancellation_factors": [
            "Moon or 4th lord in exaltation",
            "Strong benefic in 4th house",
            "Jupiter aspecting 4th house or Moon",
        ],
    },
    "Pitru_Dosha": {
        "chapter": 44,
        "verses": "44.43-45",
        "category": "Arishta Yoga",
        "formation": "Sun or 9th lord severely afflicted, or malefics in 9th house",
        "classical_description": "Creates difficulties related to father, dharma, and fortune.",
        "effects": {
            "general": "Father's health issues, lack of fortune, obstacles to dharma",
            "father": "Father's early death, separation, or conflicts",
            "fortune": "Lack of luck and blessings, obstacles to success",
            "dharma": "Difficulties in religious/spiritual pursuits",
            "education": "Obstacles in higher education",
        },
        "cancellation_factors": [
            "Sun or 9th lord in exaltation",
            "Strong benefic in 9th house",
            "Jupiter aspecting 9th house or Sun",
        ],
    },
    "Putra_Dosha": {
        "chapter": 44,
        "verses": "44.46-48",
        "category": "Arishta Yoga",
        "formation": "Jupiter or 5th lord severely afflicted, or malefics in 5th house",
        "classical_description": "Creates difficulties related to children, intelligence, and creative pursuits.",
        "effects": {
            "general": "Difficulties with children, creative blocks, speculative losses",
            "children": "Childlessness, delayed children, or children's health issues",
            "intelligence": "Mental stress, poor judgment in speculation",
            "creativity": "Creative frustrations, blocks",
            "romance": "Romantic disappointments",
        },
        "cancellation_factors": [
            "Jupiter or 5th lord in exaltation",
            "Strong benefic in 5th house",
            "Jupiter aspecting 5th house",
            "5th lord in kendra or trikona",
        ],
    },
    "Kalatra_Dosha": {
        "chapter": 44,
        "verses": "44.50-52",
        "category": "Arishta Yoga",
        "formation": "Venus or 7th lord severely afflicted, or malefics in 7th house",
        "classical_description": "Creates difficulties in marriage, partnerships, and relationships.",
        "effects": {
            "general": "Marital difficulties, partnership problems, relationship challenges",
            "marriage": "Late marriage, marital discord, separation, or spouse's health issues",
            "partnerships": "Business partnership conflicts, losses",
            "health": "Reproductive health issues",
        },
        "cancellation_factors": [
            "Venus or 7th lord in exaltation",
            "Strong benefic in 7th house",
            "Jupiter aspecting 7th house or Venus",
            "7th lord in kendra or trikona",
        ],
    },
    "Balarishta_Yoga": {
        "chapter": 45,
        "verses": "45.3-5",
        "category": "Arishta Yoga",
        "formation": "Moon and ascendant lord both in dusthanas (6,8,12) with malefic aspects",
        "classical_description": "Balarishta means 'infant mortality'. Indicates health challenges in childhood.",
        "effects": {
            "general": "Health challenges in childhood, early life difficulties",
            "health": "Childhood diseases, weak constitution in youth",
            "longevity": "Reduced longevity if severe and uncancelled",
            "timing": "Most critical in first 12 years of life",
        },
        "strength_factors": [
            "Both Moon and ascendant lord in 8th - most severe",
            "Malefic aspects from Mars, Saturn, Rahu - severe",
            "No benefic aspects - very dangerous",
        ],
        "cancellation_factors": [
            "Strong benefic in ascendant or with Moon",
            "Jupiter aspecting ascendant or Moon",
            "Ascendant lord or Moon in exaltation",
            "Strong benefic yogas present",
            "Survival past age 12 indicates cancellation",
        ],
        "notes": "Important to check for cancellations. Modern medicine reduces severity.",
    },
    "Angarak_Yoga": {
        "chapter": 45,
        "verses": "45.20-22",
        "category": "Arishta Yoga",
        "formation": "Mars conjunct Rahu (especially in ascendant, 5th, 7th, 8th, or 12th)",
        "classical_description": "Angarak means 'burning coal'. The fiery combination of Mars and Rahu creates intense, explosive energy.",
        "effects": {
            "general": "Aggressive tendencies, accidents, sudden events, intense experiences",
            "personality": "Aggressive, impulsive, risk-taking nature",
            "health": "Prone to accidents, injuries, surgeries, blood-related issues",
            "relationships": "Conflicts in relationships, aggressive behavior",
            "career": "Success in Mars-Rahu fields (military, surgery, technology) but with challenges",
        },
        "strength_factors": [
            "In ascendant - affects personality severely",
            "In 7th - marital challenges",
            "In 8th - accidents and sudden events",
            "In 12th - expenses, losses, foreign issues",
        ],
        "cancellation_factors": [
            "Mars in own sign or exaltation",
            "Strong Jupiter aspect",
            "Conjunction in 3rd, 6th, or 11th (upachaya) - less severe",
        ],
    },
    "Guru_Chandal_Yoga": {
        "chapter": 45,
        "verses": "45.25-27",
        "category": "Arishta Yoga",
        "formation": "Jupiter conjunct Rahu (especially in ascendant, 5th, 9th, or 10th)",
        "classical_description": "Chandal means 'outcaste'. Jupiter's purity is tainted by Rahu's shadowy influence, affecting wisdom and judgment.",
        "effects": {
            "general": "Unconventional beliefs, challenges to traditional values, wisdom through unorthodox paths",
            "wisdom": "Unconventional thinking, may reject traditional teachings",
            "children": "Difficulties with children or unconventional children",
            "dharma": "Challenges to religious beliefs, spiritual confusion",
            "reputation": "May face criticism for unconventional views",
        },
        "strength_factors": [
            "In 5th house - children and intelligence affected",
            "In 9th house - dharma and fortune affected",
            "In 10th house - career and reputation affected",
        ],
        "cancellation_factors": [
            "Jupiter in own sign (Sagittarius/Pisces)",
            "Jupiter in exaltation (Cancer)",
            "Strong benefic aspects to Jupiter",
            "Jupiter in kendra from Moon (forms Gaja Kesari despite Rahu)",
        ],
        "notes": "Modern interpretation: Can indicate genius through unconventional thinking. Not always negative.",
    },
}

BPHS_NABHASA_YOGAS: Dict[str, Dict[str, Any]] = {
    "Rajju_Yoga": {
        "chapter": 46,
        "verses": "46.5-6",
        "category": "Nabhasa Yoga - Ashraya",
        "formation": "All planets in movable signs (Aries, Cancer, Libra, Capricorn)",
        "classical_description": "Rajju means 'rope'. Creates a wandering, traveling nature with frequent changes.",
        "effects": {
            "general": "Frequent travels, changes of residence, wandering nature",
            "personality": "Restless, adaptable, loves travel and change",
            "career": "Success in travel-related fields, frequent job changes",
            "wealth": "Gains through travel and foreign connections",
        },
        "strength_factors": ["More planets in movable signs - stronger", "Planets in own signs - better results"],
    },
    "Musala_Yoga": {
        "chapter": 46,
        "verses": "46.7-8",
        "category": "Nabhasa Yoga - Ashraya",
        "formation": "All planets in fixed signs (Taurus, Leo, Scorpio, Aquarius)",
        "classical_description": "Musala means 'pestle'. Creates stability, determination, and fixed nature.",
        "effects": {
            "general": "Stable life, determination, fixed opinions, wealth accumulation",
            "personality": "Stubborn, determined, resistant to change",
            "career": "Long-term career stability, success through persistence",
            "wealth": "Steady wealth accumulation, property ownership",
        },
        "strength_factors": ["All planets in fixed signs - very strong", "Planets in own signs - excellent results"],
    },
    "Nala_Yoga": {
        "chapter": 46,
        "verses": "46.9-10",
        "category": "Nabhasa Yoga - Ashraya",
        "formation": "All planets in dual signs (Gemini, Virgo, Sagittarius, Pisces)",
        "classical_description": "Creates versatility, adaptability, and multiple interests.",
        "effects": {
            "general": "Versatile nature, multiple talents, adaptability",
            "personality": "Flexible, multi-talented, intellectual",
            "career": "Success in multiple fields, diverse interests",
            "wealth": "Multiple income sources",
        },
        "strength_factors": ["Planets in own signs - stronger", "Mercury and Jupiter strong - excellent"],
    },
    "Gada_Yoga": {
        "chapter": 46,
        "verses": "46.15-16",
        "category": "Nabhasa Yoga - Dala",
        "formation": "All planets in 1st and 7th houses only",
        "classical_description": "Gada means 'mace'. Creates strong personality and partnership focus.",
        "effects": {
            "general": "Strong personality, focus on self and relationships",
            "personality": "Powerful presence, relationship-oriented",
            "marriage": "Marriage and partnerships central to life",
            "career": "Success through partnerships",
        },
        "strength_factors": ["Benefics in 1st, malefics in 7th - balanced", "Strong ascendant lord - powerful"],
    },
    "Shakata_Yoga_Nabhasa": {
        "chapter": 46,
        "verses": "46.17-18",
        "category": "Nabhasa Yoga - Dala",
        "formation": "All planets in 4th and 10th houses only",
        "classical_description": "Creates focus on domestic life and career.",
        "effects": {
            "general": "Balance between home and career, property and profession",
            "career": "Strong career focus",
            "domestic": "Emphasis on home and property",
            "wealth": "Gains through property and career",
        },
        "strength_factors": ["Benefics in 4th, malefics in 10th - good", "4th and 10th lords strong - excellent"],
    },
    "Yupa_Yoga": {
        "chapter": 46,
        "verses": "46.20-21",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 1st, 2nd, 3rd, and 4th houses",
        "classical_description": "Yupa means 'sacrificial post'. Creates focus on self-development and early life houses.",
        "effects": {
            "general": "Focus on self, family, courage, and home",
            "personality": "Self-focused, family-oriented",
            "wealth": "Wealth through family and self-effort",
            "courage": "Courageous and self-reliant",
        },
        "strength_factors": ["Benefics in these houses - very good", "Ascendant lord strong - powerful"],
    },
    "Ishu_Yoga": {
        "chapter": 46,
        "verses": "46.22-23",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 4th, 5th, 6th, and 7th houses",
        "classical_description": "Ishu means 'arrow'. Creates focus on middle life areas.",
        "effects": {
            "general": "Focus on home, children, service, and partnerships",
            "domestic": "Strong domestic focus",
            "children": "Emphasis on children and creativity",
            "partnerships": "Partnership-oriented life",
        },
        "strength_factors": ["Benefics in 4th, 5th, 7th - excellent", "5th and 7th lords strong - good"],
    },
    "Shakti_Yoga": {
        "chapter": 46,
        "verses": "46.24-25",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 7th, 8th, 9th, and 10th houses",
        "classical_description": "Shakti means 'power'. Creates focus on partnerships, transformation, dharma, and career.",
        "effects": {
            "general": "Power through partnerships and career, transformative life",
            "career": "Strong career focus and success",
            "partnerships": "Important partnerships",
            "spiritual": "Transformative spiritual experiences",
        },
        "strength_factors": [
            "Benefics in 9th, 10th - excellent career and fortune",
            "9th and 10th lords strong - powerful",
        ],
    },
    "Danda_Yoga": {
        "chapter": 46,
        "verses": "46.26-27",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 10th, 11th, 12th, and 1st houses",
        "classical_description": "Danda means 'staff'. Creates focus on career, gains, expenses, and self.",
        "effects": {
            "general": "Career and gains focus, expenses and self-development",
            "career": "Strong career emphasis",
            "gains": "Focus on income and achievements",
            "expenses": "Significant expenses but for good causes",
        },
        "strength_factors": [
            "Benefics in 1st, 10th, 11th - very good",
            "10th and 11th lords strong - wealth and career",
        ],
    },
    "Nau_Yoga": {
        "chapter": 46,
        "verses": "46.28-29",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 1st, 2nd, 3rd, 4th, 5th, 6th, and 7th houses (first seven houses)",
        "classical_description": "Nau means 'boat'. Creates emphasis on personal development and relationships.",
        "effects": {
            "general": "Focus on self-development and relationships",
            "personality": "Strong personality development",
            "relationships": "Relationship-oriented",
            "wealth": "Wealth through self and partnerships",
        },
        "strength_factors": ["Benefics well-distributed - good", "Ascendant and 7th lords strong - excellent"],
    },
    "Kuta_Yoga": {
        "chapter": 46,
        "verses": "46.30-31",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 4th, 5th, 6th, 7th, 8th, 9th, and 10th houses",
        "classical_description": "Creates focus on middle and later life areas.",
        "effects": {
            "general": "Focus on home, children, service, partnerships, transformation, dharma, career",
            "career": "Career and dharma emphasis",
            "family": "Family and children focus",
            "transformation": "Transformative experiences",
        },
        "strength_factors": ["Benefics in 4th, 5th, 9th, 10th - excellent", "Multiple lords strong - powerful"],
    },
    "Chhatra_Yoga": {
        "chapter": 46,
        "verses": "46.32-33",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 7th, 8th, 9th, 10th, 11th, 12th, and 1st houses",
        "classical_description": "Chhatra means 'umbrella/protection'. Creates protective influence and authority.",
        "effects": {
            "general": "Protection, authority, success in later life",
            "career": "Authority and leadership",
            "protection": "Divine protection and grace",
            "wealth": "Gains and prosperity",
        },
        "strength_factors": ["Benefics in 1st, 9th, 10th, 11th - very powerful", "Multiple Raja Yogas - excellent"],
    },
    "Chapa_Yoga": {
        "chapter": 46,
        "verses": "46.34-35",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 1st, 2nd, 3rd, 7th, 8th, and 9th houses",
        "classical_description": "Chapa means 'bow'. Creates warrior-like qualities and strategic thinking.",
        "effects": {
            "general": "Strategic thinking, warrior qualities, success through effort",
            "personality": "Strategic, courageous",
            "career": "Success in competitive fields",
            "dharma": "Righteous warrior path",
        },
        "strength_factors": ["Mars and Sun strong - warrior qualities", "9th lord strong - dharmic success"],
    },
    "Samudra_Yoga": {
        "chapter": 46,
        "verses": "46.36-37",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 2nd, 3rd, 4th, 8th, 9th, and 10th houses",
        "classical_description": "Samudra means 'ocean'. Creates depth, wisdom, and vast resources.",
        "effects": {
            "general": "Wealth, wisdom, depth of character",
            "wealth": "Vast resources like ocean",
            "wisdom": "Deep knowledge and understanding",
            "career": "Success and authority",
        },
        "strength_factors": ["Benefics in 2nd, 9th, 10th - wealth and fortune", "Jupiter strong - wisdom"],
    },
    "Vallaki_Yoga": {
        "chapter": 46,
        "verses": "46.38-39",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 3rd, 4th, 5th, 9th, 10th, and 11th houses",
        "classical_description": "Creates success, happiness, and prosperity.",
        "effects": {
            "general": "Success, happiness, prosperity, good fortune",
            "career": "Career success and gains",
            "children": "Good children",
            "fortune": "Excellent fortune and blessings",
        },
        "strength_factors": ["Benefics in 5th, 9th, 10th, 11th - very auspicious", "Multiple Dhana Yogas - wealthy"],
    },
    "Damaru_Yoga": {
        "chapter": 46,
        "verses": "46.40-41",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 1st, 2nd, 7th, and 8th houses",
        "classical_description": "Damaru means 'drum'. Creates rhythmic ups and downs.",
        "effects": {
            "general": "Fluctuating fortunes, ups and downs",
            "personality": "Strong but unstable",
            "relationships": "Important partnerships",
            "transformation": "Transformative experiences",
        },
        "strength_factors": ["Benefics in 1st and 7th - better", "Malefics in 8th - challenges"],
    },
    "Pasha_Yoga": {
        "chapter": 46,
        "verses": "46.42-43",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 4th, 5th, 10th, and 11th houses",
        "classical_description": "Pasha means 'noose/bondage'. Creates attachment to material success.",
        "effects": {
            "general": "Material success, attachment to wealth and career",
            "career": "Strong career focus",
            "wealth": "Wealth and gains",
            "children": "Good children",
        },
        "strength_factors": [
            "Benefics in all four houses - very wealthy",
            "10th and 11th lords strong - career and gains",
        ],
    },
    "Kedara_Yoga": {
        "chapter": 46,
        "verses": "46.44-45",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 2nd, 3rd, 8th, and 9th houses",
        "classical_description": "Kedara means 'field'. Creates agricultural success and land ownership.",
        "effects": {
            "general": "Success in agriculture, land ownership, wealth",
            "wealth": "Wealth through land and agriculture",
            "courage": "Courageous nature",
            "transformation": "Transformative experiences",
        },
        "strength_factors": ["Benefics in 2nd and 9th - wealth and fortune", "Mars strong - land and property"],
    },
    "Shula_Yoga": {
        "chapter": 46,
        "verses": "46.46-47",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 3rd, 4th, 5th, and 6th houses",
        "classical_description": "Shula means 'spear'. Creates sharp intellect and competitive nature.",
        "effects": {
            "general": "Sharp intellect, competitive success, service orientation",
            "intelligence": "Sharp mind and analytical abilities",
            "courage": "Courageous and competitive",
            "service": "Success in service professions",
        },
        "strength_factors": ["Benefics in 4th and 5th - good", "Malefics in 6th - victory over enemies"],
    },
    "Yuga_Yoga": {
        "chapter": 46,
        "verses": "46.48-49",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 7th, 8th, 9th, and 10th houses",
        "classical_description": "Creates focus on partnerships, transformation, dharma, and career.",
        "effects": {
            "general": "Success through partnerships and career, spiritual transformation",
            "career": "Strong career success",
            "partnerships": "Important partnerships",
            "dharma": "Spiritual and philosophical inclinations",
        },
        "strength_factors": [
            "Benefics in 7th, 9th, 10th - excellent",
            "9th and 10th lords strong - fortune and career",
        ],
    },
    "Gola_Yoga": {
        "chapter": 46,
        "verses": "46.50-51",
        "category": "Nabhasa Yoga - Akriti",
        "formation": "All planets in 5th, 6th, 11th, and 12th houses",
        "classical_description": "Gola means 'sphere/globe'. Creates balanced material and spiritual pursuits.",
        "effects": {
            "general": "Balance between material gains and spiritual expenses",
            "children": "Good children",
            "gains": "Financial gains",
            "spirituality": "Spiritual inclinations and expenses",
        },
        "strength_factors": ["Benefics in 5th and 11th - children and gains", "Jupiter strong - wisdom"],
    },
    "Sringhataka_Yoga": {
        "chapter": 46,
        "verses": "46.52-53",
        "category": "Nabhasa Yoga - Sankhya",
        "formation": "All planets in four kendras (1st, 4th, 7th, 10th houses)",
        "classical_description": "Creates exceptional strength, authority, and success. Highly auspicious.",
        "effects": {
            "general": "Outstanding success, authority, happiness, prosperity",
            "personality": "Strong and authoritative",
            "career": "Exceptional career success",
            "wealth": "Prosperity and material comforts",
            "reputation": "Fame and recognition",
        },
        "strength_factors": [
            "All kendras occupied - very powerful",
            "Benefics in kendras - excellent",
            "Kendra lords strong - outstanding",
        ],
        "notes": "One of the most auspicious Nabhasa yogas",
    },
    "Hala_Yoga": {
        "chapter": 46,
        "verses": "46.54-55",
        "category": "Nabhasa Yoga - Sankhya",
        "formation": "All planets in four panaparas (2nd, 5th, 8th, 11th houses)",
        "classical_description": "Hala means 'plough'. Creates wealth through agriculture and steady effort.",
        "effects": {
            "general": "Wealth through agriculture, steady gains, moderate success",
            "wealth": "Wealth accumulation through effort",
            "agriculture": "Success in farming and land",
            "gains": "Steady income and gains",
        },
        "strength_factors": [
            "Benefics in 2nd, 5th, 11th - wealth and children",
            "Venus and Jupiter strong - prosperity",
        ],
    },
    "Vajra_Yoga": {
        "chapter": 46,
        "verses": "46.56-57",
        "category": "Nabhasa Yoga - Sankhya",
        "formation": "All benefics in kendras and all malefics in apoklimas (3,6,9,12), or vice versa",
        "classical_description": "Vajra means 'thunderbolt/diamond'. Creates exceptional strength and resilience.",
        "effects": {
            "general": "Exceptional strength, resilience, success through effort",
            "personality": "Strong and resilient character",
            "career": "Success through perseverance",
            "wealth": "Prosperity through effort",
        },
        "strength_factors": [
            "Benefics in kendras - very strong",
            "Malefics in upachaya (3,6) - good",
            "Clear separation - powerful",
        ],
        "notes": "Highly auspicious for strength and success",
    },
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
            "longevity": "Generally good vitality and resistance to disease",
        },
        "ideal_formations": [
            "Mars in Aries in 1st house",
            "Mars in Capricorn (exalted) in 10th house",
            "Mars in Scorpio in 7th house",
        ],
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
            "skills": "Multi-talented with diverse interests and abilities",
        },
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
            "family": "Happy family life with good children",
        },
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
            "talents": "Natural artistic and creative abilities",
        },
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
            "leadership": "Gains authority through proven competence",
        },
    },
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
    all_yogas = {**BPHS_RAJA_YOGAS, **BPHS_DHANA_YOGAS, **BPHS_PANCHA_MAHAPURUSHA_YOGAS, **BPHS_ARISHTA_YOGAS}

    return all_yogas.get(yoga_name, None)


def get_yogas_by_category(category: str) -> Dict[str, Dict[str, Any]]:
    """
    Get all yogas of a specific category.

    Args:
        category: Category name (Raja Yoga, Dhana Yoga, Mahapurusha Yoga, Arishta Yoga, etc.)

    Returns:
        Dictionary of yogas in that category
    """
    all_yogas = {
        **BPHS_RAJA_YOGAS,
        **BPHS_DHANA_YOGAS,
        **BPHS_PANCHA_MAHAPURUSHA_YOGAS,
        **BPHS_ARISHTA_YOGAS,
        **BPHS_NABHASA_YOGAS,
    }

    return {name: data for name, data in all_yogas.items() if data.get("category") == category}


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
    all_yogas.update(BPHS_ARISHTA_YOGAS)
    all_yogas.update(BPHS_NABHASA_YOGAS)
    return all_yogas
