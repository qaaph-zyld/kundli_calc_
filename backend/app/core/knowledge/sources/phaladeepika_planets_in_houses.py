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
            "verses": "10.1",
            "translation": "When the Sun occupies the first house, the native will have scanty hair on the head, be lazy, of a quick temper, tall, with big hands and feet, will have bile as the chief humor, and his right eye will be defective.",
            "detailed_effects": [
                "Scanty hair on head",
                "Lazy temperament",
                "Quick to anger",
                "Tall stature with large hands and feet",
                "Bilious constitution (Pitta dominant)",
                "Right eye weakness or defect"
            ],
            "positive_effects": [
                "Tall and commanding presence",
                "Strong will and determination"
            ],
            "challenging_effects": [
                "Tendency toward laziness",
                "Quick temper and anger",
                "Eye health issues",
                "Health vulnerabilities"
            ],
            "timing": "Effects manifest throughout life, intensify during Sun dasha",
            "tags": ["personality", "health", "appearance", "temperament"],
            "confidence": "high"
        },
        2: {
            "chapter": 10,
            "verses": "10.2",
            "translation": "The Sun in the 2nd makes one scholarly but wrathful, bereft of learning and riches, without food at all times, subservient to the fair sex, and deprived of a good or a beautiful wife or blessed with a wife having the virtues of a male.",
            "detailed_effects": [
                "Scholarly but wrathful disposition",
                "Financial struggles despite education",
                "Irregular food habits",
                "Dominated by women",
                "Wife may be masculine in nature or virtues"
            ],
            "positive_effects": [
                "Scholarly and educated"
            ],
            "challenging_effects": [
                "Wrathful and angry nature",
                "Financial difficulties",
                "Marital challenges",
                "Food insecurity"
            ],
            "timing": "Financial and marital effects throughout life",
            "tags": ["wealth", "speech", "personality", "marriage"],
            "confidence": "high"
        },
        3: {
            "chapter": 10,
            "verses": "10.3",
            "translation": "With the Sun in the 3rd house, one will be very powerful, energetic, very liberal, wealthy, and famous in the world. He will be free from enemies and defeated adversaries.",
            "detailed_effects": [
                "Very powerful and energetic",
                "Liberal and generous nature",
                "Wealthy and famous",
                "Victory over enemies",
                "Strong courage and initiative"
            ],
            "positive_effects": [
                "Power and energy",
                "Wealth and fame",
                "Courage and bravery",
                "Victory over adversaries"
            ],
            "challenging_effects": [],
            "timing": "Courage and initiative throughout life, peak during Sun dasha",
            "tags": ["courage", "siblings", "wealth", "fame"],
            "confidence": "high"
        },
        4: {
            "chapter": 10,
            "verses": "10.4",
            "translation": "The Sun in the 4th makes one devoid of happiness and comforts, deprived of mother, relatives, lands, vehicles, and friends. If the Sun be weak in 4th, the person will be a servant to another.",
            "detailed_effects": [
                "Lack of domestic happiness",
                "Mother's early death or separation",
                "Loss of property and vehicles",
                "Few friends or relatives",
                "Service position if Sun is weak"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Domestic unhappiness",
                "Loss of mother",
                "Property losses",
                "Social isolation",
                "Servitude if weak"
            ],
            "timing": "Mother-related effects in youth, property issues throughout",
            "tags": ["mother", "property", "happiness", "vehicles"],
            "confidence": "high"
        },
        5: {
            "chapter": 10,
            "verses": "10.5",
            "translation": "With Sun in 5th house, one will be bereft of happiness, wealth, and children. He will be intelligent, wander in forests or hilly places, and will be quick in anger.",
            "detailed_effects": [
                "Unhappiness and poverty",
                "Difficulty with children",
                "High intelligence",
                "Tendency to wander or travel",
                "Quick temper"
            ],
            "positive_effects": [
                "High intelligence",
                "Love of nature and travel"
            ],
            "challenging_effects": [
                "Lack of happiness",
                "Financial struggles",
                "Issues with progeny",
                "Anger problems"
            ],
            "timing": "Children-related effects during procreative years",
            "tags": ["children", "intelligence", "wealth", "temperament"],
            "confidence": "high"
        },
        6: {
            "chapter": 10,
            "verses": "10.6",
            "translation": "The Sun in 6th makes one very strong, king or like a king, wealthy, victorious over enemies, stomach disorders, prone to anger.",
            "detailed_effects": [
                "Very strong physically",
                "Authority and leadership (king-like)",
                "Wealthy and prosperous",
                "Victory over adversaries",
                "Digestive issues or stomach problems",
                "Prone to anger"
            ],
            "positive_effects": [
                "Physical strength",
                "Authority and power",
                "Wealth accumulation",
                "Victory over enemies"
            ],
            "challenging_effects": [
                "Stomach and digestive disorders",
                "Anger issues"
            ],
            "timing": "Strength and authority throughout life, health issues may develop",
            "tags": ["health", "enemies", "authority", "wealth"],
            "confidence": "high"
        },
        7: {
            "chapter": 10,
            "verses": "10.7",
            "translation": "Sun in 7th house makes one suffer humiliation, lose wife and wealth, live in foreign lands, and have a diseased body.",
            "detailed_effects": [
                "Loss of respect and dignity",
                "Marital difficulties or loss of spouse",
                "Financial losses",
                "Life in foreign places",
                "Health problems"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Humiliation and loss of dignity",
                "Marital problems",
                "Wealth losses",
                "Foreign residence",
                "Diseased constitution"
            ],
            "timing": "Marital effects after marriage, health issues throughout",
            "tags": ["marriage", "wealth", "health", "foreign"],
            "confidence": "high"
        },
        8: {
            "chapter": 10,
            "verses": "10.8",
            "translation": "With the Sun in 8th, one will be deprived of eyesight, without wealth, friendless, without a good heart, living by other people, and short-lived.",
            "detailed_effects": [
                "Eye problems or blindness",
                "Poverty and financial struggles",
                "Few or no friends",
                "Lacking compassion",
                "Dependent on others",
                "Reduced longevity"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Vision loss",
                "Financial dependency",
                "Social isolation",
                "Hard-hearted nature",
                "Short lifespan"
            ],
            "timing": "Challenges throughout life, longevity concerns in later years",
            "tags": ["longevity", "wealth", "health", "eyes"],
            "confidence": "high"
        },
        9: {
            "chapter": 10,
            "verses": "10.9",
            "translation": "The Sun in 9th makes one bereft of riches, children, and wife. He will not be inclined to religious deeds and will hate his father.",
            "detailed_effects": [
                "Financial difficulties",
                "Issues with children",
                "Marital problems",
                "Lack of religious inclination",
                "Conflict with father"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Poverty",
                "Loss of progeny",
                "Marital discord",
                "Irreligious tendencies",
                "Father-son conflict"
            ],
            "timing": "Father-related effects in youth, dharma issues throughout",
            "tags": ["dharma", "father", "children", "wealth"],
            "confidence": "high"
        },
        10: {
            "chapter": 10,
            "verses": "10.10",
            "translation": "With the Sun in 10th, one will be happy, capable, intelligent, wealthy, famous, will do virtuous deeds, blessed with vehicles and land.",
            "detailed_effects": [
                "Happiness and contentment",
                "High capability and competence",
                "Intelligent and wise",
                "Wealth accumulation",
                "Fame and recognition",
                "Virtuous character and actions",
                "Property and vehicles"
            ],
            "positive_effects": [
                "Career excellence",
                "Fame and recognition",
                "Wealth and prosperity",
                "Virtuous nature",
                "Property ownership"
            ],
            "challenging_effects": [],
            "timing": "Career peaks during Sun mahadasha, recognition throughout life",
            "tags": ["career", "fame", "wealth", "virtue"],
            "confidence": "high"
        },
        11: {
            "chapter": 10,
            "verses": "10.11",
            "translation": "The Sun in 11th makes one wealthy, long-lived, blessed with children, few diseases, brave, with income from multiple sources.",
            "detailed_effects": [
                "Substantial wealth",
                "Long life",
                "Good children",
                "Strong health (minimal diseases)",
                "Courageous nature",
                "Multiple income streams"
            ],
            "positive_effects": [
                "Wealth and prosperity",
                "Longevity",
                "Healthy progeny",
                "Good health",
                "Courage",
                "Diverse income"
            ],
            "challenging_effects": [],
            "timing": "Wealth gains throughout life, peak during Sun dasha",
            "tags": ["wealth", "gains", "longevity", "children"],
            "confidence": "high"
        },
        12: {
            "chapter": 10,
            "verses": "10.12",
            "translation": "With the Sun in 12th, one will be defective in a limb, deprived of eyesight, will lose wealth through royal displeasure or enemies, will live in a foreign land, and be bereft of wife and children.",
            "detailed_effects": [
                "Physical defects or disability",
                "Eye problems or blindness",
                "Financial losses through authority/enemies",
                "Life away from homeland",
                "Loss of spouse and children"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Physical disabilities",
                "Vision loss",
                "Wealth losses",
                "Foreign residence",
                "Loss of family"
            ],
            "timing": "Challenges throughout life, losses in later years",
            "tags": ["losses", "foreign", "health", "marriage"],
            "confidence": "high"
        }
    },
    
    "Moon": {
        1: {
            "chapter": 11,
            "verses": "11.1",
            "translation": "Moon in 1st makes one fickle-minded, given to drinking water often, handsome, with wealth from liquids, kind-hearted, soft-spoken.",
            "detailed_effects": [
                "Changeable and fickle mind",
                "Frequent thirst",
                "Attractive appearance",
                "Income from liquids/water businesses",
                "Kind and compassionate",
                "Soft and pleasant speech"
            ],
            "positive_effects": [
                "Beautiful appearance",
                "Kind-hearted nature",
                "Soft speech",
                "Wealth from water-related activities"
            ],
            "challenging_effects": [
                "Mental fickleness",
                "Changeable moods",
                "Excessive thirst"
            ],
            "timing": "Effects prominent throughout life, intensify during Moon dasha",
            "tags": ["personality", "appearance", "wealth", "temperament"],
            "confidence": "high"
        },
        2: {
            "chapter": 11,
            "verses": "11.2",
            "translation": "Moon in 2nd gives beautiful face, sweet speech, wealth, good food, large family.",
            "detailed_effects": [
                "Beautiful facial features",
                "Sweet and melodious speech",
                "Wealth accumulation",
                "Enjoyment of good food",
                "Large and prosperous family"
            ],
            "positive_effects": [
                "Attractive face",
                "Pleasant speech",
                "Financial prosperity",
                "Good food and nourishment",
                "Large family"
            ],
            "challenging_effects": [],
            "timing": "Wealth gains during Moon dasha, family growth throughout",
            "tags": ["wealth", "speech", "family", "appearance"],
            "confidence": "high"
        },
        3: {
            "chapter": 11,
            "verses": "11.3",
            "translation": "Moon in 3rd makes one cruel, miserly, proud, devoted to relatives, brave.",
            "detailed_effects": [
                "Cruel or harsh nature",
                "Miserly with money",
                "Proud and arrogant",
                "Strong devotion to siblings/relatives",
                "Courageous and brave"
            ],
            "positive_effects": [
                "Courage and bravery",
                "Devotion to family"
            ],
            "challenging_effects": [
                "Cruel tendencies",
                "Miserliness",
                "Pride and arrogance"
            ],
            "timing": "Sibling relationships important throughout life",
            "tags": ["courage", "siblings", "temperament", "wealth"],
            "confidence": "high"
        },
        4: {
            "chapter": 11,
            "verses": "11.4",
            "translation": "The Moon in the 4th house bestows happiness, friendship, enjoyment of comforts, possession of conveyances, and acquisition of wealth.",
            "detailed_effects": [
                "Domestic happiness and peace",
                "Comfortable home environment",
                "Vehicles and properties",
                "Emotional fulfillment from family",
                "Strong connection with mother",
                "Good friendships"
            ],
            "positive_effects": [
                "Domestic bliss",
                "Material comforts",
                "Property and vehicles",
                "Emotional security",
                "Wealth accumulation",
                "Strong friendships"
            ],
            "challenging_effects": [],
            "timing": "Home acquisition during Moon dasha, family happiness throughout",
            "tags": ["mother", "property", "happiness", "vehicles"],
            "confidence": "high"
        },
        5: {
            "chapter": 11,
            "verses": "11.5",
            "translation": "Moon in 5th gives good intelligence, many sons, devotion to Shiva, happiness.",
            "detailed_effects": [
                "High intelligence and wisdom",
                "Blessed with many sons",
                "Devotion to Lord Shiva",
                "General happiness and contentment",
                "Creative and imaginative mind"
            ],
            "positive_effects": [
                "Intelligence",
                "Good progeny",
                "Spiritual devotion",
                "Happiness",
                "Creativity"
            ],
            "challenging_effects": [],
            "timing": "Children born during Moon dasha, intelligence throughout",
            "tags": ["children", "intelligence", "spirituality", "happiness"],
            "confidence": "high"
        },
        6: {
            "chapter": 11,
            "verses": "11.6",
            "translation": "Moon in 6th gives laziness, stomach ailments, many enemies, mental distress.",
            "detailed_effects": [
                "Lazy temperament",
                "Digestive and stomach problems",
                "Many adversaries and enemies",
                "Mental anxiety and distress",
                "Health challenges"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Laziness",
                "Stomach disorders",
                "Enemy problems",
                "Mental distress",
                "Health issues"
            ],
            "timing": "Health issues may develop, enemy conflicts throughout",
            "tags": ["health", "enemies", "mental_health", "temperament"],
            "confidence": "high"
        },
        7: {
            "chapter": 11,
            "verses": "11.7",
            "translation": "Moon in 7th gives beautiful spouse, passionate nature, wealth, travels, diseases from water.",
            "detailed_effects": [
                "Beautiful and attractive spouse",
                "Passionate and romantic nature",
                "Wealth accumulation",
                "Frequent travels",
                "Water-related health issues"
            ],
            "positive_effects": [
                "Beautiful partner",
                "Passionate nature",
                "Wealth",
                "Travel opportunities"
            ],
            "challenging_effects": [
                "Water-related diseases",
                "Excessive passion may cause issues"
            ],
            "timing": "Marriage during Moon dasha, travel throughout life",
            "tags": ["marriage", "wealth", "travel", "health"],
            "confidence": "high"
        },
        8: {
            "chapter": 11,
            "verses": "11.8",
            "translation": "Moon in 8th makes one diseased, sorrowful, dependent on others, short-lived.",
            "detailed_effects": [
                "Chronic diseases",
                "Sorrow and grief",
                "Financial dependency",
                "Reduced longevity",
                "Emotional suffering"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Health problems",
                "Mental sorrow",
                "Dependency on others",
                "Short lifespan",
                "Emotional pain"
            ],
            "timing": "Health challenges throughout, longevity concerns in later years",
            "tags": ["longevity", "health", "sorrow", "dependency"],
            "confidence": "high"
        },
        9: {
            "chapter": 11,
            "verses": "11.9",
            "translation": "Moon in 9th gives wealth, virtuous nature, devotion to deities, happiness from father.",
            "detailed_effects": [
                "Wealth and prosperity",
                "Virtuous and righteous character",
                "Devotion to gods and spirituality",
                "Good relationship with father",
                "Fortune and blessings"
            ],
            "positive_effects": [
                "Wealth",
                "Virtue and righteousness",
                "Spiritual devotion",
                "Father's blessings",
                "Good fortune"
            ],
            "challenging_effects": [],
            "timing": "Fortune throughout life, spiritual growth during Moon dasha",
            "tags": ["dharma", "father", "wealth", "spirituality"],
            "confidence": "high"
        },
        10: {
            "chapter": 11,
            "verses": "11.10",
            "translation": "Moon in 10th gives success in undertakings, intelligence, fame, virtuous deeds, respect.",
            "detailed_effects": [
                "Success in professional endeavors",
                "High intelligence",
                "Fame and recognition",
                "Virtuous actions",
                "Social respect and honor"
            ],
            "positive_effects": [
                "Career success",
                "Intelligence",
                "Fame",
                "Virtue",
                "Respect"
            ],
            "challenging_effects": [],
            "timing": "Career success during Moon dasha, recognition throughout",
            "tags": ["career", "fame", "intelligence", "virtue"],
            "confidence": "high"
        },
        11: {
            "chapter": 11,
            "verses": "11.11",
            "translation": "Moon in 11th gives wealth, long life, good children, few diseases, many friends.",
            "detailed_effects": [
                "Substantial wealth and gains",
                "Long lifespan",
                "Good and virtuous children",
                "Strong health",
                "Large network of friends"
            ],
            "positive_effects": [
                "Wealth and gains",
                "Longevity",
                "Good progeny",
                "Health",
                "Friendships"
            ],
            "challenging_effects": [],
            "timing": "Gains throughout life, peak during Moon dasha",
            "tags": ["wealth", "gains", "longevity", "children"],
            "confidence": "high"
        },
        12: {
            "chapter": 11,
            "verses": "11.12",
            "translation": "Moon in 12th gives eye defects, enmity with mother, expenditure, residence in foreign lands.",
            "detailed_effects": [
                "Eye problems or defects",
                "Conflict with mother",
                "Heavy expenditures",
                "Life in foreign countries",
                "Losses and expenses"
            ],
            "positive_effects": [
                "Spiritual inclinations",
                "Foreign opportunities"
            ],
            "challenging_effects": [
                "Eye health issues",
                "Mother-child conflict",
                "Financial losses",
                "Foreign residence"
            ],
            "timing": "Expenses throughout, foreign residence possible",
            "tags": ["losses", "foreign", "health", "mother"],
            "confidence": "high"
        }
    },
    
    "Mars": {
        1: {
            "chapter": 12,
            "verses": "12.1",
            "translation": "Mars in 1st house makes one cruel, adventurous, eater of forbidden food, quarrelsome, has a scarred body, and unkind to mother.",
            "detailed_effects": [
                "Cruel or harsh temperament",
                "Adventurous and risk-taking nature",
                "Dietary indiscretions",
                "Quarrelsome and aggressive",
                "Physical scars or marks on body",
                "Strained relationship with mother"
            ],
            "positive_effects": [
                "Courage and bravery",
                "Adventurous spirit",
                "Physical strength"
            ],
            "challenging_effects": [
                "Cruel tendencies",
                "Quarrelsome nature",
                "Physical scars",
                "Conflict with mother"
            ],
            "timing": "Aggressive tendencies throughout life, peak during Mars dasha",
            "tags": ["personality", "aggression", "health", "mother"],
            "confidence": "high"
        },
        2: {
            "chapter": 12,
            "verses": "12.2",
            "translation": "Mars in 2nd causes eye disease, loss of wealth, harsh speech, living on others' food, family conflicts.",
            "detailed_effects": [
                "Eye problems or defects",
                "Financial losses",
                "Harsh or abusive speech",
                "Dependent on others for sustenance",
                "Family disputes and conflicts"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Eye health issues",
                "Wealth losses",
                "Harsh speech",
                "Food dependency",
                "Family conflicts"
            ],
            "timing": "Financial and speech issues throughout life",
            "tags": ["wealth", "speech", "health", "family"],
            "confidence": "high"
        },
        3: {
            "chapter": 12,
            "verses": "12.3",
            "translation": "Mars in 3rd gives courage, wealth, happiness from brothers, leadership, and victory over enemies.",
            "detailed_effects": [
                "Exceptional courage and bravery",
                "Wealth accumulation",
                "Good relationship with siblings",
                "Leadership qualities",
                "Victory over adversaries"
            ],
            "positive_effects": [
                "Courage",
                "Wealth",
                "Sibling harmony",
                "Leadership",
                "Victory over enemies"
            ],
            "challenging_effects": [],
            "timing": "Courage and leadership throughout life",
            "tags": ["courage", "siblings", "wealth", "leadership"],
            "confidence": "high"
        },
        4: {
            "chapter": 12,
            "verses": "12.4",
            "translation": "Mars in 4th destroys happiness, mother, lands, vehicles, relatives, and comforts.",
            "detailed_effects": [
                "Loss of domestic happiness",
                "Harm to mother or early separation",
                "Property losses",
                "Loss of vehicles",
                "Few relatives or strained relations"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Domestic unhappiness",
                "Mother's suffering",
                "Property losses",
                "Vehicle losses",
                "Relative conflicts"
            ],
            "timing": "Mother-related effects in youth, property issues throughout",
            "tags": ["mother", "property", "happiness", "vehicles"],
            "confidence": "high"
        },
        5: {
            "chapter": 12,
            "verses": "12.5",
            "translation": "Mars in 5th makes one devoid of happiness, wealth, and children; intelligent but wrathful.",
            "detailed_effects": [
                "Unhappiness and discontent",
                "Financial struggles",
                "Difficulty with children or childlessness",
                "High intelligence",
                "Quick temper and anger"
            ],
            "positive_effects": [
                "High intelligence"
            ],
            "challenging_effects": [
                "Unhappiness",
                "Poverty",
                "Children issues",
                "Anger problems"
            ],
            "timing": "Children-related effects during procreative years",
            "tags": ["children", "intelligence", "wealth", "temperament"],
            "confidence": "high"
        },
        6: {
            "chapter": 12,
            "verses": "12.6",
            "translation": "Mars in 6th gives wealth, victory over enemies, happiness, strong physique, and leadership.",
            "detailed_effects": [
                "Substantial wealth",
                "Victory over adversaries",
                "Overall happiness",
                "Strong and healthy body",
                "Leadership and authority"
            ],
            "positive_effects": [
                "Wealth",
                "Victory over enemies",
                "Happiness",
                "Physical strength",
                "Leadership"
            ],
            "challenging_effects": [],
            "timing": "Strength and victory throughout life",
            "tags": ["health", "enemies", "wealth", "leadership"],
            "confidence": "high",
            "notes": "Mars in 6th (Upachaya) is very strong and favorable"
        },
        7: {
            "chapter": 12,
            "verses": "12.7",
            "translation": "Mars in 7th causes loss of spouse, wealth problems, diseases, and living in foreign lands.",
            "detailed_effects": [
                "Marital difficulties or loss of spouse",
                "Financial problems",
                "Health issues and diseases",
                "Life away from homeland",
                "Conflicts in partnerships"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Marital problems",
                "Wealth issues",
                "Health problems",
                "Foreign residence",
                "Partnership conflicts"
            ],
            "timing": "Marital effects after marriage, health issues throughout",
            "tags": ["marriage", "wealth", "health", "foreign"],
            "confidence": "high",
            "notes": "Mars in 7th (Kuja Dosha) harms marriage and partnerships"
        },
        8: {
            "chapter": 12,
            "verses": "12.8",
            "translation": "Mars in 8th gives eye defects, loss of wealth, friendless, dependent on others, short life.",
            "detailed_effects": [
                "Eye problems",
                "Poverty and financial struggles",
                "Lack of friends",
                "Dependent on others",
                "Reduced longevity"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Eye defects",
                "Financial losses",
                "Social isolation",
                "Dependency",
                "Short lifespan"
            ],
            "timing": "Challenges throughout life, longevity concerns",
            "tags": ["longevity", "wealth", "health", "eyes"],
            "confidence": "high"
        },
        9: {
            "chapter": 12,
            "verses": "12.9",
            "translation": "Mars in 9th destroys father, dharma, fortune, and makes one sinful and irreligious.",
            "detailed_effects": [
                "Harm to father or conflict",
                "Lack of fortune and luck",
                "Irreligious tendencies",
                "Sinful actions",
                "Obstacles in dharma"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Father's suffering",
                "Loss of fortune",
                "Irreligious nature",
                "Sinful tendencies",
                "Dharma obstacles"
            ],
            "timing": "Father-related effects in youth, dharma issues throughout",
            "tags": ["dharma", "father", "fortune", "spirituality"],
            "confidence": "high"
        },
        10: {
            "chapter": 12,
            "verses": "12.10",
            "translation": "Mars in 10th gives wealth, happiness, leadership, fame, courage, and virtuous deeds.",
            "detailed_effects": [
                "Wealth and prosperity",
                "Career success and leadership",
                "Fame and recognition",
                "Exceptional courage",
                "Virtuous actions"
            ],
            "positive_effects": [
                "Wealth",
                "Career success",
                "Fame",
                "Courage",
                "Virtue"
            ],
            "challenging_effects": [],
            "timing": "Career peaks during Mars dasha",
            "tags": ["career", "fame", "wealth", "leadership"],
            "confidence": "high",
            "notes": "Mars in 10th (Kendra/Kona) is very strong for career"
        },
        11: {
            "chapter": 12,
            "verses": "12.11",
            "translation": "Mars in 11th gives wealth, long life, happiness, gains from multiple sources, and courage.",
            "detailed_effects": [
                "Substantial wealth and gains",
                "Long life",
                "Overall happiness",
                "Multiple income streams",
                "Courageous nature"
            ],
            "positive_effects": [
                "Wealth and gains",
                "Longevity",
                "Happiness",
                "Multiple incomes",
                "Courage"
            ],
            "challenging_effects": [],
            "timing": "Gains throughout life, peak during Mars dasha",
            "tags": ["wealth", "gains", "longevity", "courage"],
            "confidence": "high"
        },
        12: {
            "chapter": 12,
            "verses": "12.12",
            "translation": "Mars in 12th causes eye defects, loss of wealth through enemies, living abroad, and physical suffering.",
            "detailed_effects": [
                "Eye problems",
                "Financial losses through adversaries",
                "Life in foreign lands",
                "Physical suffering and diseases",
                "Expenses and losses"
            ],
            "positive_effects": [],
            "challenging_effects": [
                "Eye defects",
                "Wealth losses",
                "Foreign residence",
                "Physical suffering",
                "Heavy expenses"
            ],
            "timing": "Losses and expenses throughout life",
            "tags": ["losses", "foreign", "health", "eyes"],
            "confidence": "high"
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
