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
        2: {
            "verses": "Ch. 27, v. 2",
            "translation": "If the Sun is in the 2nd house, the native will be devoid of learning and wealth, will have an ugly face, will be without happiness, and will destroy the family.",
            "detailed_effects": [
                "Challenges in accumulating wealth",
                "Harsh or blunt speech patterns",
                "Strained family relationships",
                "Self-esteem issues related to finances",
                "May need to rebuild family fortune",
                "Strong opinions on values and money",
                "Facial features may be stern"
            ],
            "positive_effects": [
                "Strong voice and authoritative speech when well-placed",
                "Determination to create own wealth",
                "Value-driven approach to resources",
                "Can be powerful speaker if Sun is strong"
            ],
            "challenging_effects": [
                "Financial instability",
                "Harsh speech causing conflicts",
                "Family disputes over money",
                "Difficulty in formal education",
                "Eye or facial issues"
            ],
            "timing": "Financial challenges in early life; improvement after Sun dasha"
        },
        3: {
            "verses": "Ch. 27, v. 3",
            "translation": "Should the Sun be in the 3rd, the native will be valorous, strong, will lose co-born, be liberal in giving, and be skillful in all jobs.",
            "detailed_effects": [
                "Exceptional courage and bravery",
                "Strong physical vitality",
                "Loss of siblings or strained sibling relations",
                "Generous and charitable nature",
                "Skilled in multiple areas",
                "Self-made success through effort",
                "Initiative and entrepreneurial spirit"
            ],
            "positive_effects": [
                "Outstanding courage and valor",
                "Physical strength and energy",
                "Generosity and liberality",
                "Skillful and versatile",
                "Success through self-effort"
            ],
            "challenging_effects": [
                "Loss of or separation from siblings",
                "Conflicts with brothers/sisters",
                "Overly aggressive approach",
                "Ego in communications"
            ],
            "timing": "Courage develops early; sibling issues in youth; success through initiative"
        },
        4: {
            "verses": "Ch. 27, v. 4",
            "translation": "If the Sun occupies the 4th, the native will be devoid of conveyances, relatives, happiness, lands, and friends, and will serve a king.",
            "detailed_effects": [
                "Challenges with mother or maternal relations",
                "Lack of domestic peace and comfort",
                "Property matters require attention",
                "May work in government service",
                "Emotional distance from family",
                "Frequent changes of residence",
                "Heart-related health concerns"
            ],
            "positive_effects": [
                "Government service opportunities",
                "Authority in domestic matters if Sun strong",
                "Self-reliance and independence"
            ],
            "challenging_effects": [
                "Lack of domestic happiness",
                "Mother's health or separation",
                "Loss of property or vehicles",
                "Few close friends",
                "Emotional instability"
            ],
            "timing": "Domestic challenges throughout life; property gains delayed"
        },
        5: {
            "verses": "Ch. 27, v. 5",
            "translation": "Should the Sun be in the 5th, the native will be bereft of happiness, wealth, and sons, will be evil-minded, and will suffer from stomach diseases.",
            "detailed_effects": [
                "Challenges with children or progeny",
                "Delayed or difficult childbirth",
                "Speculative losses if not careful",
                "Digestive health issues",
                "Creative blocks or frustrations",
                "Ego affecting romantic relationships",
                "Intelligence but harsh expression"
            ],
            "positive_effects": [
                "Strong intellect and analytical ability",
                "Leadership in creative fields if well-placed",
                "Authority in educational settings"
            ],
            "challenging_effects": [
                "Difficulties with children",
                "Financial losses through speculation",
                "Stomach and digestive problems",
                "Harsh or critical nature",
                "Romantic disappointments"
            ],
            "timing": "Children delayed or challenging; health issues in middle age"
        },
        6: {
            "verses": "Ch. 27, v. 6",
            "translation": "If the Sun is in the 6th, the native will be very strong, will be a king, will have enmity with his own men, be famous, and be without diseases.",
            "detailed_effects": [
                "Excellent for overcoming enemies and obstacles",
                "Strong physical constitution",
                "Success in competitive fields",
                "Victory in legal matters and disputes",
                "Leadership in service or health sectors",
                "Conflicts with subordinates or employees",
                "Generally good health"
            ],
            "positive_effects": [
                "Outstanding ability to defeat enemies",
                "Strong health and vitality",
                "Success in competition",
                "Fame and recognition",
                "Leadership positions"
            ],
            "challenging_effects": [
                "Conflicts with employees or servants",
                "Enmity from relatives",
                "Ego in service relationships",
                "Legal disputes"
            ],
            "timing": "Victory over enemies in Sun dasha; health remains strong"
        },
        7: {
            "verses": "Ch. 27, v. 7",
            "translation": "Should the Sun be in the 7th, the native will suffer humiliation, will have a diseased wife, be devoid of wealth, will lose in quarrels, and be sinful.",
            "detailed_effects": [
                "Challenges in marriage and partnerships",
                "Spouse may have health issues",
                "Ego conflicts in relationships",
                "Business partnership difficulties",
                "Public humiliation or criticism",
                "Financial losses through partnerships",
                "Late marriage or multiple marriages"
            ],
            "positive_effects": [
                "Strong personality attracts partners",
                "Leadership in partnerships if Sun well-placed",
                "Public recognition despite challenges"
            ],
            "challenging_effects": [
                "Marital discord and conflicts",
                "Spouse's health problems",
                "Loss of wealth through partnerships",
                "Defeat in legal disputes",
                "Public humiliation"
            ],
            "timing": "Marriage challenges throughout life; partnerships require careful management"
        },
        8: {
            "verses": "Ch. 27, v. 8",
            "translation": "If the Sun occupies the 8th, the native will have defective eyesight, be devoid of wealth and happiness, and be short-lived.",
            "detailed_effects": [
                "Eye problems or vision defects",
                "Chronic health concerns",
                "Financial instability and losses",
                "Interest in occult and mysticism",
                "Sudden ups and downs in life",
                "Inheritance issues or delays",
                "Transformative life experiences"
            ],
            "positive_effects": [
                "Deep insight into mysteries",
                "Transformative spiritual growth",
                "Research and investigation abilities",
                "Gains through inheritance if well-placed"
            ],
            "challenging_effects": [
                "Serious eye problems",
                "Chronic health issues",
                "Financial difficulties",
                "Reduced longevity",
                "Sudden losses and crises"
            ],
            "timing": "Health challenges throughout life; spiritual transformation in later years"
        },
        9: {
            "verses": "Ch. 27, v. 9",
            "translation": "Should the Sun be in the 9th, the native will be bereft of wealth, children, and wife, will hate his father, and will not be inclined to religious deeds.",
            "detailed_effects": [
                "Strained relationship with father",
                "Challenges in higher education or philosophy",
                "Difficulties with children",
                "Marital challenges",
                "Financial struggles",
                "Lack of interest in religion or spirituality",
                "Foreign travel may bring difficulties"
            ],
            "positive_effects": [
                "Independent thinking and philosophy",
                "Authority in teaching if well-placed",
                "Leadership in foreign lands"
            ],
            "challenging_effects": [
                "Father's health issues or separation",
                "Loss of wealth",
                "Difficulties with children",
                "Marital problems",
                "Lack of spiritual inclination"
            ],
            "timing": "Father-related issues in youth; spiritual awakening delayed or absent"
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
        },
        11: {
            "verses": "Ch. 27, v. 11",
            "translation": "If the Sun is in the 11th, the native will be long-lived, will have abundant wealth, be endowed with conveyances, and will have limited number of children.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Long and healthy life",
                "Multiple sources of income",
                "Fulfillment of desires and ambitions",
                "Success in social networks",
                "Vehicles and material comforts",
                "Few children but successful"
            ],
            "positive_effects": [
                "Outstanding financial gains",
                "Longevity and good health",
                "Wealth from multiple sources",
                "Vehicles and luxuries",
                "Achievement of goals"
            ],
            "challenging_effects": [
                "Limited number of children",
                "Ego in friendships",
                "May dominate social groups"
            ],
            "timing": "Gains increase with age; peak prosperity in Sun dasha"
        },
        12: {
            "verses": "Ch. 27, v. 12",
            "translation": "Should the Sun be in the 12th, the native will have defective eyesight, be devoid of wealth, be bereft of sons, and will serve others.",
            "detailed_effects": [
                "Eye problems or vision defects",
                "Financial losses and expenses",
                "Difficulties with children",
                "Service to others or foreign lands",
                "Spiritual inclinations develop",
                "Expenditure exceeds income",
                "Interest in isolation or meditation"
            ],
            "positive_effects": [
                "Spiritual growth and moksha",
                "Service to humanity",
                "Success in foreign lands",
                "Charitable nature"
            ],
            "challenging_effects": [
                "Serious eye problems",
                "Financial difficulties",
                "Loss of children or childlessness",
                "Serving others rather than leading",
                "Expenses and losses"
            ],
            "timing": "Expenses throughout life; spiritual growth in later years"
        }
    },
    
    "Moon": {
        1: {
            "verses": "Ch. 28, v. 1",
            "translation": "If the Moon is in the ascendant, the native will be fickle-minded, will have a beautiful body, be fond of water and flowers, be learned, and will suffer from diseases of phlegm.",
            "detailed_effects": [
                "Attractive and pleasant appearance",
                "Emotional and sensitive nature",
                "Changeable mind and moods",
                "Love for beauty, water, and nature",
                "Good education and learning",
                "Kapha (phlegm) constitution",
                "Nurturing and caring personality"
            ],
            "positive_effects": [
                "Beautiful and attractive physique",
                "Emotional intelligence",
                "Love for arts and beauty",
                "Good learning abilities",
                "Nurturing nature"
            ],
            "challenging_effects": [
                "Fickle-minded and changeable",
                "Emotional instability",
                "Phlegm-related health issues",
                "Overly sensitive",
                "Mood swings"
            ],
            "timing": "Emotional nature evident from birth; Moon dasha brings changes"
        },
        2: {
            "verses": "Ch. 28, v. 2",
            "translation": "Should the Moon be in the 2nd, the native will enjoy incomparable happiness and friends, be wealthy, will have beautiful eyes and face, and be learned in Shastras.",
            "detailed_effects": [
                "Excellent for wealth accumulation",
                "Beautiful facial features and eyes",
                "Sweet and pleasant speech",
                "Good education and knowledge",
                "Happy family life",
                "Many friends and social connections",
                "Gains through liquids or nurturing professions"
            ],
            "positive_effects": [
                "Outstanding wealth and prosperity",
                "Beautiful face and eyes",
                "Sweet speech and communication",
                "Educational achievements",
                "Happy family relationships"
            ],
            "challenging_effects": [
                "Emotional attachment to money",
                "Fluctuating finances",
                "May overindulge in food"
            ],
            "timing": "Wealth increases in Moon dasha; family happiness throughout life"
        },
        3: {
            "verses": "Ch. 28, v. 3",
            "translation": "If the Moon occupies the 3rd, the native will be endowed with relatives, be corpulent, will have a strong body, be valorous, and will have wealth.",
            "detailed_effects": [
                "Strong relationship with siblings",
                "Courageous and brave nature",
                "Well-built, possibly corpulent physique",
                "Success through self-effort",
                "Good communication abilities",
                "Wealth through initiative",
                "Artistic and creative talents"
            ],
            "positive_effects": [
                "Strong courage and initiative",
                "Good sibling relationships",
                "Wealth and prosperity",
                "Strong physical constitution",
                "Creative abilities"
            ],
            "challenging_effects": [
                "Tendency to gain weight",
                "Emotional approach to courage",
                "May be overly attached to siblings"
            ],
            "timing": "Courage develops early; wealth through self-effort in Moon dasha"
        },
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
        5: {
            "verses": "Ch. 28, v. 5",
            "translation": "Should the Moon be in the 5th, the native will be endowed with sons, be learned, famous, and will enjoy happiness.",
            "detailed_effects": [
                "Highly auspicious for children",
                "Intelligent and creative offspring",
                "Good education and learning",
                "Fame and recognition",
                "Emotional intelligence",
                "Success in creative pursuits",
                "Romantic and loving nature"
            ],
            "positive_effects": [
                "Blessed with good children",
                "Intelligence and wisdom",
                "Fame and reputation",
                "Creative talents",
                "Emotional happiness"
            ],
            "challenging_effects": [
                "Emotional attachment to children",
                "Fluctuating creative output",
                "Romantic mood swings"
            ],
            "timing": "Children in Moon dasha; creative success; educational achievements"
        },
        6: {
            "verses": "Ch. 28, v. 6",
            "translation": "If the Moon is in the 6th, the native will suffer from phlegmatic disorders, be short-tempered, will have many enemies, be devoid of happiness, and be sinful.",
            "detailed_effects": [
                "Health issues related to phlegm and fluids",
                "Emotional sensitivity to criticism",
                "Many enemies and competitors",
                "Digestive and stomach problems",
                "Service-oriented work",
                "Emotional stress from conflicts",
                "Lack of peace of mind"
            ],
            "positive_effects": [
                "Ability to serve and help others",
                "Emotional resilience when developed",
                "Success in healing professions"
            ],
            "challenging_effects": [
                "Phlegm and water-related diseases",
                "Short temper and irritability",
                "Many enemies and conflicts",
                "Lack of happiness",
                "Mental stress"
            ],
            "timing": "Health challenges throughout life; enemies in Moon dasha"
        },
        7: {
            "verses": "Ch. 28, v. 7",
            "translation": "Should the Moon be in the 7th, the native will be amiable, will have a beautiful wife, be learned, and will be endowed with all kinds of wealth.",
            "detailed_effects": [
                "Excellent for marriage and partnerships",
                "Beautiful and loving spouse",
                "Emotional fulfillment in relationships",
                "Pleasant and amiable personality",
                "Success in business partnerships",
                "Wealth through partnerships",
                "Good education"
            ],
            "positive_effects": [
                "Outstanding marital happiness",
                "Beautiful and compatible spouse",
                "Wealth and prosperity",
                "Pleasant personality",
                "Success in partnerships"
            ],
            "challenging_effects": [
                "Emotional dependency on partner",
                "Fluctuating relationship dynamics",
                "May be too accommodating"
            ],
            "timing": "Marriage in Moon dasha; partnership success; emotional fulfillment"
        },
        8: {
            "verses": "Ch. 28, v. 8",
            "translation": "If the Moon occupies the 8th, the native will be short-lived, will suffer from diseases, be devoid of wealth, and will have a defective body.",
            "detailed_effects": [
                "Chronic health concerns",
                "Emotional turbulence and crises",
                "Interest in occult and mysteries",
                "Financial instability",
                "Transformative life experiences",
                "Inheritance issues",
                "Reduced vitality"
            ],
            "positive_effects": [
                "Deep emotional insight",
                "Psychic and intuitive abilities",
                "Transformative spiritual growth",
                "Research abilities"
            ],
            "challenging_effects": [
                "Chronic diseases",
                "Short lifespan",
                "Financial difficulties",
                "Physical defects or weakness",
                "Emotional crises"
            ],
            "timing": "Health challenges throughout life; crises in Moon dasha"
        },
        9: {
            "verses": "Ch. 28, v. 9",
            "translation": "Should the Moon be in the 9th, the native will be devoted to divine and paternal assignments, be endowed with happiness, wealth, intelligence, and sons, and will attract the fair sex.",
            "detailed_effects": [
                "Strong devotion to father and dharma",
                "Religious and spiritual inclinations",
                "Good fortune and blessings",
                "Wealth and prosperity",
                "Intelligent and wise",
                "Blessed with children",
                "Attractive to opposite sex"
            ],
            "positive_effects": [
                "Outstanding fortune and blessings",
                "Spiritual devotion",
                "Wealth and happiness",
                "Intelligence and wisdom",
                "Good children"
            ],
            "challenging_effects": [
                "Emotional attachment to beliefs",
                "May be overly idealistic",
                "Fluctuating faith"
            ],
            "timing": "Fortune increases in Moon dasha; spiritual growth; foreign travel"
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
        },
        11: {
            "verses": "Ch. 28, v. 11",
            "translation": "If the Moon is in the 11th, the native will be wealthy, will have many sons, be long-lived, and will have attendants.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Multiple sources of wealth",
                "Many children and progeny",
                "Long and healthy life",
                "Success in social networks",
                "Fulfillment of desires",
                "Servants and helpers"
            ],
            "positive_effects": [
                "Outstanding financial gains",
                "Many children",
                "Longevity",
                "Social success",
                "Achievement of goals"
            ],
            "challenging_effects": [
                "Emotional attachment to gains",
                "Fluctuating income",
                "May have too many obligations"
            ],
            "timing": "Gains increase with age; peak prosperity in Moon dasha"
        },
        12: {
            "verses": "Ch. 28, v. 12",
            "translation": "Should the Moon be in the 12th, the native will be odious, will suffer eye diseases, be devoid of wealth and learning, and will be indolent.",
            "detailed_effects": [
                "Eye problems or vision issues",
                "Financial losses and expenses",
                "Lack of formal education",
                "Lazy or indolent nature",
                "Spiritual inclinations develop",
                "Interest in foreign lands",
                "Expenditure exceeds income"
            ],
            "positive_effects": [
                "Spiritual growth and moksha",
                "Intuitive and psychic abilities",
                "Success in foreign lands",
                "Charitable nature"
            ],
            "challenging_effects": [
                "Eye diseases",
                "Financial difficulties",
                "Lack of education",
                "Indolence and laziness",
                "Expenses and losses"
            ],
            "timing": "Expenses throughout life; spiritual awakening in later years"
        }
    },
    
    "Mars": {
        1: {
            "verses": "Ch. 29, v. 1",
            "translation": "If Mars is in the ascendant, the native will be cruel, adventurous, dull-witted, short-lived, will have an injured body, and will have a bilious constitution.",
            "detailed_effects": [
                "Courageous and bold personality",
                "Athletic and energetic physique",
                "Aggressive and assertive nature",
                "Prone to injuries and accidents",
                "Bilious (Pitta) constitution",
                "Quick temper and impulsive",
                "Strong physical vitality"
            ],
            "positive_effects": [
                "Outstanding courage and bravery",
                "Strong physical energy",
                "Leadership abilities",
                "Athletic prowess",
                "Competitive spirit"
            ],
            "challenging_effects": [
                "Cruel or harsh nature",
                "Impulsive and rash decisions",
                "Prone to injuries",
                "Short temper",
                "Reduced longevity if afflicted"
            ],
            "timing": "Mars dasha brings energy, courage, but also conflicts and injuries"
        },
        2: {
            "verses": "Ch. 29, v. 2",
            "translation": "Should Mars be in the 2nd, the native will be poor, will eat bad food, will possess an ugly face, will join others' wives, and will be bereft of learning and happiness.",
            "detailed_effects": [
                "Financial challenges and instability",
                "Harsh or aggressive speech",
                "Facial scars or marks",
                "Relationship indiscretions",
                "Lack of formal education",
                "Family disputes over money",
                "Poor dietary habits"
            ],
            "positive_effects": [
                "Strong voice and assertive speech",
                "Ability to fight for resources",
                "Self-made wealth if Mars strong"
            ],
            "challenging_effects": [
                "Financial difficulties",
                "Harsh speech causing conflicts",
                "Facial injuries or ugliness",
                "Immoral relationships",
                "Lack of education and happiness"
            ],
            "timing": "Financial struggles in early life; speech-related conflicts"
        },
        3: {
            "verses": "Ch. 29, v. 3",
            "translation": "If Mars occupies the 3rd, the native will be very valorous, will lose co-born, be a talebearer, and will have all kinds of wealth.",
            "detailed_effects": [
                "Exceptional courage and valor",
                "Loss of siblings or conflicts with them",
                "Strong communication abilities",
                "Entrepreneurial spirit",
                "Wealth through self-effort",
                "Competitive nature",
                "Initiative and drive"
            ],
            "positive_effects": [
                "Outstanding courage and bravery",
                "Wealth through initiative",
                "Strong communication skills",
                "Success in competitive fields",
                "Self-made achievements"
            ],
            "challenging_effects": [
                "Loss of siblings",
                "Conflicts with brothers/sisters",
                "Gossip or tale-bearing",
                "Aggressive communication"
            ],
            "timing": "Courage evident early; wealth through self-effort in Mars dasha"
        },
        4: {
            "verses": "Ch. 29, v. 4",
            "translation": "Should Mars be in the 4th, the native will be devoid of relatives, paraphernalia, and happiness, will betray his friends, and will destroy his lands and patrimony.",
            "detailed_effects": [
                "Challenges with mother and domestic peace",
                "Property disputes and losses",
                "Lack of vehicles or frequent accidents",
                "Betrayal in friendships",
                "Emotional turbulence at home",
                "Heart-related health concerns",
                "Frequent residence changes"
            ],
            "positive_effects": [
                "Independence and self-reliance",
                "Ability to rebuild after losses",
                "Strong will in domestic matters"
            ],
            "challenging_effects": [
                "Lack of domestic happiness",
                "Mother's health issues",
                "Property losses",
                "Betrayal of friends",
                "Loss of patrimony"
            ],
            "timing": "Domestic challenges throughout life; property issues in Mars dasha"
        },
        5: {
            "verses": "Ch. 29, v. 5",
            "translation": "If Mars is in the 5th, the native will be devoid of happiness, wealth, and sons, be fickle-minded, be a talebearer, and will have a bad wife.",
            "detailed_effects": [
                "Difficulties with children or delayed progeny",
                "Speculative losses",
                "Changeable mind and opinions",
                "Marital discord",
                "Creative frustrations",
                "Aggressive romantic approach",
                "Digestive health issues"
            ],
            "positive_effects": [
                "Strong intellect and analytical ability",
                "Competitive in creative fields",
                "Athletic children if Mars well-placed"
            ],
            "challenging_effects": [
                "Difficulties with children",
                "Loss through speculation",
                "Fickle-minded nature",
                "Marital problems",
                "Lack of happiness and wealth"
            ],
            "timing": "Children delayed or challenging; speculative losses in Mars dasha"
        },
        6: {
            "verses": "Ch. 29, v. 6",
            "translation": "Should Mars be in the 6th, the native will be very libidinous, will have powerful enemies, will suffer from diseases, and will have wounds.",
            "detailed_effects": [
                "Excellent for defeating enemies",
                "Strong sexual drive",
                "Victory in competitions and disputes",
                "Prone to injuries and wounds",
                "Success in military or police work",
                "Health issues from accidents",
                "Powerful but manageable enemies"
            ],
            "positive_effects": [
                "Outstanding ability to defeat enemies",
                "Success in competitive fields",
                "Victory in legal matters",
                "Strong physical constitution",
                "Leadership in service sectors"
            ],
            "challenging_effects": [
                "Excessive sexual desires",
                "Powerful enemies",
                "Diseases and wounds",
                "Accidents and injuries",
                "Conflicts with subordinates"
            ],
            "timing": "Victory over enemies in Mars dasha; injuries and health issues"
        },
        7: {
            "verses": "Ch. 29, v. 7",
            "translation": "If Mars occupies the 7th, the native will lose his wife, will suffer from diseases, be sinful, will go to others' wives, and be devoid of happiness.",
            "detailed_effects": [
                "Marital challenges and conflicts",
                "Loss of spouse or separation",
                "Health issues affecting marriage",
                "Extramarital affairs",
                "Business partnership disputes",
                "Aggressive approach to relationships",
                "Late marriage or multiple marriages"
            ],
            "positive_effects": [
                "Passionate and energetic partner if Mars strong",
                "Success in competitive partnerships",
                "Strong will in relationships"
            ],
            "challenging_effects": [
                "Loss of wife or marital discord",
                "Health problems",
                "Immoral relationships",
                "Lack of happiness",
                "Partnership conflicts"
            ],
            "timing": "Marriage challenges throughout life; partnerships require careful management"
        },
        8: {
            "verses": "Ch. 29, v. 8",
            "translation": "Should Mars be in the 8th, the native will have deformed eyes, be devoid of wealth, happiness, and intelligence, and be short-lived.",
            "detailed_effects": [
                "Eye problems or injuries",
                "Chronic health concerns",
                "Financial instability",
                "Interest in occult and mysteries",
                "Sudden accidents and crises",
                "Inheritance disputes",
                "Reduced longevity if afflicted"
            ],
            "positive_effects": [
                "Deep research abilities",
                "Transformative spiritual growth",
                "Courage in crises",
                "Gains through inheritance if well-placed"
            ],
            "challenging_effects": [
                "Eye deformities or injuries",
                "Financial difficulties",
                "Lack of happiness and intelligence",
                "Short lifespan",
                "Sudden losses and accidents"
            ],
            "timing": "Health challenges and crises throughout life; accidents in Mars dasha"
        },
        9: {
            "verses": "Ch. 29, v. 9",
            "translation": "If Mars is in the 9th, the native will not be skillful, will have an adverse wife, will kill living beings, and will not be virtuous.",
            "detailed_effects": [
                "Challenges with father and teachers",
                "Lack of higher education or philosophy",
                "Marital discord",
                "Aggressive or violent tendencies",
                "Lack of religious inclination",
                "Conflicts in foreign lands",
                "Unethical behavior"
            ],
            "positive_effects": [
                "Independent philosophy",
                "Courage in foreign lands",
                "Athletic or military pursuits abroad"
            ],
            "challenging_effects": [
                "Lack of skills",
                "Adverse spouse",
                "Violent tendencies",
                "Lack of virtue and dharma",
                "Father-related issues"
            ],
            "timing": "Father-related conflicts; lack of spiritual inclination; foreign travel issues"
        },
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
        },
        11: {
            "verses": "Ch. 29, v. 11",
            "translation": "Should Mars be in the 11th, the native will be wealthy, will have limited number of children, be long-lived, and will have attendants.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Wealth through competitive fields",
                "Few children but successful",
                "Long and healthy life",
                "Success in social networks",
                "Fulfillment of desires through effort",
                "Servants and helpers"
            ],
            "positive_effects": [
                "Outstanding financial gains",
                "Longevity and good health",
                "Wealth from multiple sources",
                "Achievement of goals",
                "Social success"
            ],
            "challenging_effects": [
                "Limited number of children",
                "Aggressive in friendships",
                "Conflicts in social groups"
            ],
            "timing": "Gains increase with age; peak prosperity in Mars dasha"
        },
        12: {
            "verses": "Ch. 29, v. 12",
            "translation": "If Mars occupies the 12th, the native will have diseased eyes, will fall from his position, be devoid of wealth and happiness, and will have a defective body.",
            "detailed_effects": [
                "Eye diseases or injuries",
                "Financial losses and expenses",
                "Loss of position or status",
                "Physical defects or injuries",
                "Expenditure exceeds income",
                "Interest in foreign lands",
                "Spiritual warrior path"
            ],
            "positive_effects": [
                "Spiritual growth through challenges",
                "Service to humanity",
                "Success in foreign lands",
                "Courage in isolation"
            ],
            "challenging_effects": [
                "Eye diseases",
                "Financial difficulties",
                "Loss of position",
                "Physical defects",
                "Expenses and losses"
            ],
            "timing": "Expenses and losses throughout life; spiritual growth in later years"
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
        2: {
            "verses": "Ch. 30, v. 2",
            "translation": "Should Mercury be in the 2nd, the native will earn wealth through his own intelligence, be sweet in speech, and will enjoy good food.",
            "detailed_effects": [
                "Excellent for wealth through intellect",
                "Sweet and persuasive speech",
                "Business acumen and commercial success",
                "Good education and learning",
                "Happy family life",
                "Enjoyment of good food",
                "Multiple income sources"
            ],
            "positive_effects": [
                "Outstanding wealth through intelligence",
                "Sweet and effective communication",
                "Business success",
                "Educational achievements",
                "Happy family relationships"
            ],
            "challenging_effects": [
                "May be too talkative",
                "Scattered financial focus",
                "Nervous speech patterns"
            ],
            "timing": "Wealth increases in Mercury dasha; business success; good food"
        },
        3: {
            "verses": "Ch. 30, v. 3",
            "translation": "If Mercury occupies the 3rd, the native will always toil hard, be devoid of near and dear, skillful, endowed with co-born, and be cheerful.",
            "detailed_effects": [
                "Hard-working and industrious nature",
                "Good relationship with siblings",
                "Skillful in communication and writing",
                "Cheerful and optimistic disposition",
                "Success through self-effort",
                "Versatile talents",
                "May lack close emotional bonds"
            ],
            "positive_effects": [
                "Outstanding communication skills",
                "Good sibling relationships",
                "Skillful and versatile",
                "Cheerful nature",
                "Success through effort"
            ],
            "challenging_effects": [
                "Constant hard work required",
                "Lack of close relationships",
                "Restless nature"
            ],
            "timing": "Hard work throughout life; success through communication in Mercury dasha"
        },
        4: {
            "verses": "Ch. 30, v. 4",
            "translation": "Should Mercury be in the 4th, the native will be endowed with relatives, paraphernalia, and lands, be learned, intelligent, and happy.",
            "detailed_effects": [
                "Excellent for domestic happiness",
                "Good relationship with mother",
                "Property and vehicles",
                "Intelligence and learning",
                "Happy home environment",
                "Success in education",
                "Comfortable living"
            ],
            "positive_effects": [
                "Outstanding domestic happiness",
                "Property and vehicles",
                "Intelligence and education",
                "Good family relationships",
                "Comfortable life"
            ],
            "challenging_effects": [
                "May overthink domestic matters",
                "Restless at home",
                "Frequent residence changes"
            ],
            "timing": "Domestic happiness in Mercury dasha; property gains; educational success"
        },
        5: {
            "verses": "Ch. 30, v. 5",
            "translation": "If Mercury is in the 5th, the native will be learned in Shastras, be endowed with sons, be skillful, and will enjoy happiness.",
            "detailed_effects": [
                "Highly auspicious for children",
                "Intelligent and communicative offspring",
                "Excellent education and learning",
                "Creative and intellectual pursuits",
                "Success in speculation if careful",
                "Teaching abilities",
                "Happiness and contentment"
            ],
            "positive_effects": [
                "Blessed with intelligent children",
                "Outstanding education",
                "Creative and intellectual success",
                "Skillful in chosen field",
                "Happiness and joy"
            ],
            "challenging_effects": [
                "May overthink creative matters",
                "Scattered interests",
                "Nervous energy in romance"
            ],
            "timing": "Children in Mercury dasha; educational success; creative achievements"
        },
        6: {
            "verses": "Ch. 30, v. 6",
            "translation": "Should Mercury be in the 6th, the native will always have enemies, be devoid of wealth, be harsh in speech, and will serve others.",
            "detailed_effects": [
                "Conflicts and enemies",
                "Financial challenges",
                "Harsh or critical speech",
                "Service-oriented work",
                "Health issues from stress",
                "Victory over enemies through intelligence",
                "Analytical abilities"
            ],
            "positive_effects": [
                "Ability to defeat enemies through wit",
                "Analytical problem-solving",
                "Success in service professions",
                "Critical thinking skills"
            ],
            "challenging_effects": [
                "Many enemies and conflicts",
                "Financial difficulties",
                "Harsh speech causing problems",
                "Serving others rather than leading",
                "Nervous health issues"
            ],
            "timing": "Enemies throughout life; financial challenges; service work"
        },
        7: {
            "verses": "Ch. 30, v. 7",
            "translation": "If Mercury occupies the 7th, the native will be endowed with a beautiful wife, be learned, will have wealth, and will enjoy happiness.",
            "detailed_effects": [
                "Excellent for marriage and partnerships",
                "Intelligent and communicative spouse",
                "Success in business partnerships",
                "Good education and learning",
                "Wealth through partnerships",
                "Happy marital life",
                "Diplomatic abilities"
            ],
            "positive_effects": [
                "Outstanding marital happiness",
                "Intelligent and beautiful spouse",
                "Wealth and prosperity",
                "Success in partnerships",
                "Educational achievements"
            ],
            "challenging_effects": [
                "May overthink relationships",
                "Communication issues in marriage",
                "Restless in partnerships"
            ],
            "timing": "Marriage in Mercury dasha; partnership success; wealth through spouse"
        },
        8: {
            "verses": "Ch. 30, v. 8",
            "translation": "Should Mercury be in the 8th, the native will be famous, learned, will have long life, and will be endowed with wealth.",
            "detailed_effects": [
                "Interest in occult and mysteries",
                "Research and investigation abilities",
                "Long life and longevity",
                "Fame and recognition",
                "Wealth through inheritance or research",
                "Deep intellectual pursuits",
                "Transformative learning"
            ],
            "positive_effects": [
                "Outstanding research abilities",
                "Fame and recognition",
                "Long life",
                "Wealth and prosperity",
                "Deep knowledge"
            ],
            "challenging_effects": [
                "Obsessive thinking",
                "Nervous health issues",
                "Secretive nature"
            ],
            "timing": "Long life; fame in Mercury dasha; wealth through research"
        },
        9: {
            "verses": "Ch. 30, v. 9",
            "translation": "If Mercury is in the 9th, the native will be wealthy, skillful, famous, will have a good wife and sons, and will be endowed with all kinds of learning.",
            "detailed_effects": [
                "Excellent fortune and blessings",
                "Outstanding education and learning",
                "Wealth and prosperity",
                "Good marriage and children",
                "Fame and recognition",
                "Skillful in multiple areas",
                "Religious and philosophical knowledge"
            ],
            "positive_effects": [
                "Outstanding fortune and blessings",
                "Wealth and prosperity",
                "Excellent education",
                "Happy marriage and children",
                "Fame and recognition"
            ],
            "challenging_effects": [
                "May be overly intellectual",
                "Scattered philosophical interests",
                "Restless in spiritual pursuits"
            ],
            "timing": "Fortune increases in Mercury dasha; educational success; foreign travel"
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
        },
        11: {
            "verses": "Ch. 30, v. 11",
            "translation": "Should Mercury be in the 11th, the native will be wealthy, will have limited number of children, be long-lived, and will have attendants.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Wealth through intellectual pursuits",
                "Few children but intelligent",
                "Long and healthy life",
                "Success in social networks",
                "Fulfillment of desires",
                "Servants and helpers"
            ],
            "positive_effects": [
                "Outstanding financial gains",
                "Longevity",
                "Wealth from multiple sources",
                "Achievement of goals",
                "Social success"
            ],
            "challenging_effects": [
                "Limited number of children",
                "Scattered focus on gains",
                "Restless in friendships"
            ],
            "timing": "Gains increase with age; peak prosperity in Mercury dasha"
        },
        12: {
            "verses": "Ch. 30, v. 12",
            "translation": "If Mercury occupies the 12th, the native will be learned in Shastras, be skillful, will have a good wife, and will enjoy happiness.",
            "detailed_effects": [
                "Excellent for spiritual learning",
                "Success in foreign lands",
                "Good marriage and spouse",
                "Happiness and contentment",
                "Interest in meditation and isolation",
                "Charitable nature",
                "Expenses on education"
            ],
            "positive_effects": [
                "Outstanding spiritual learning",
                "Good marriage",
                "Happiness and joy",
                "Success in foreign lands",
                "Skillful in chosen field"
            ],
            "challenging_effects": [
                "Expenses and losses",
                "Overthinking in isolation",
                "Nervous energy"
            ],
            "timing": "Spiritual growth in Mercury dasha; foreign success; expenses on learning"
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
        2: {
            "verses": "Ch. 31, v. 2",
            "translation": "Should Jupiter be in the 2nd, the native will be rich, will enjoy good food, be an eloquent speaker, be fortunate, and will have a beautiful face.",
            "detailed_effects": [
                "Excellent for wealth accumulation",
                "Beautiful facial features",
                "Eloquent and wise speech",
                "Good fortune and blessings",
                "Happy family life",
                "Enjoyment of good food",
                "Educational achievements"
            ],
            "positive_effects": [
                "Outstanding wealth and prosperity",
                "Beautiful face and appearance",
                "Eloquent speech",
                "Good fortune",
                "Happy family relationships"
            ],
            "challenging_effects": [
                "May be overly optimistic about finances",
                "Tendency to overindulge in food",
                "Can be preachy in speech"
            ],
            "timing": "Wealth increases in Jupiter dasha; family happiness; good food"
        },
        3: {
            "verses": "Ch. 31, v. 3",
            "translation": "If Jupiter occupies the 3rd, the native will be devoid of happiness from co-born, be intelligent, and will have limited wealth.",
            "detailed_effects": [
                "Challenges with siblings",
                "Intelligence and wisdom",
                "Moderate wealth",
                "Courage and initiative",
                "Teaching and advisory abilities",
                "Success through self-effort",
                "Communication skills"
            ],
            "positive_effects": [
                "Outstanding intelligence",
                "Wisdom and good judgment",
                "Courage and initiative",
                "Teaching abilities",
                "Success through effort"
            ],
            "challenging_effects": [
                "Lack of happiness from siblings",
                "Limited wealth",
                "Sibling conflicts"
            ],
            "timing": "Intelligence develops early; limited wealth; sibling issues"
        },
        4: {
            "verses": "Ch. 31, v. 4",
            "translation": "Should Jupiter be in the 4th, the native will be endowed with relatives, paraphernalia, conveyances, happiness, intelligence, and will be a king.",
            "detailed_effects": [
                "Excellent for domestic happiness",
                "Good relationship with mother",
                "Property and vehicles",
                "Intelligence and wisdom",
                "Happy home environment",
                "Authority and leadership",
                "Comfortable living"
            ],
            "positive_effects": [
                "Outstanding domestic happiness",
                "Property and vehicles",
                "Intelligence and wisdom",
                "Good family relationships",
                "Authority and status"
            ],
            "challenging_effects": [
                "May be overly attached to home",
                "Can be too comfortable",
                "Expectations from family"
            ],
            "timing": "Domestic happiness in Jupiter dasha; property gains; authority"
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
        },
        6: {
            "verses": "Ch. 31, v. 6",
            "translation": "If Jupiter is in the 6th, the native will destroy his enemies, be famous, will have limited happiness from children, and be devoid of wealth.",
            "detailed_effects": [
                "Excellent for defeating enemies",
                "Fame and recognition",
                "Victory in disputes and competitions",
                "Limited happiness from children",
                "Financial challenges",
                "Success in service professions",
                "Wisdom in overcoming obstacles"
            ],
            "positive_effects": [
                "Outstanding ability to defeat enemies",
                "Fame and recognition",
                "Victory in legal matters",
                "Success in service sectors",
                "Wisdom and good judgment"
            ],
            "challenging_effects": [
                "Limited happiness from children",
                "Financial difficulties",
                "Health issues from overwork"
            ],
            "timing": "Victory over enemies in Jupiter dasha; fame; financial challenges"
        },
        7: {
            "verses": "Ch. 31, v. 7",
            "translation": "Should Jupiter be in the 7th, the native will be endowed with a beautiful wife, be intelligent, will have wealth, and will enjoy happiness.",
            "detailed_effects": [
                "Excellent for marriage and partnerships",
                "Beautiful and virtuous spouse",
                "Intelligence and wisdom",
                "Wealth through partnerships",
                "Happy marital life",
                "Success in business partnerships",
                "Diplomatic abilities"
            ],
            "positive_effects": [
                "Outstanding marital happiness",
                "Beautiful and wise spouse",
                "Wealth and prosperity",
                "Success in partnerships",
                "Intelligence and wisdom"
            ],
            "challenging_effects": [
                "May be overly optimistic about partnerships",
                "Expectations from spouse",
                "Can be preachy in relationships"
            ],
            "timing": "Marriage in Jupiter dasha; partnership success; wealth through spouse"
        },
        8: {
            "verses": "Ch. 31, v. 8",
            "translation": "If Jupiter occupies the 8th, the native will be devoid of happiness, will have limited longevity, be indolent, and will be bereft of wealth.",
            "detailed_effects": [
                "Challenges and obstacles",
                "Reduced longevity if afflicted",
                "Lazy or indolent nature",
                "Financial difficulties",
                "Interest in occult and spirituality",
                "Transformative experiences",
                "Inheritance issues"
            ],
            "positive_effects": [
                "Deep spiritual insight",
                "Interest in occult knowledge",
                "Transformative wisdom",
                "Research abilities"
            ],
            "challenging_effects": [
                "Lack of happiness",
                "Reduced longevity",
                "Indolence and laziness",
                "Financial difficulties",
                "Sudden losses"
            ],
            "timing": "Challenges throughout life; spiritual growth in later years"
        },
        9: {
            "verses": "Ch. 31, v. 9",
            "translation": "Should Jupiter be in the 9th, the native will be devoted to divine and paternal assignments, be endowed with happiness, wealth, intelligence, and sons.",
            "detailed_effects": [
                "Excellent fortune and blessings",
                "Strong devotion to father and dharma",
                "Religious and spiritual inclinations",
                "Wealth and prosperity",
                "Intelligence and wisdom",
                "Blessed with children",
                "Success in higher education"
            ],
            "positive_effects": [
                "Outstanding fortune and blessings",
                "Spiritual devotion",
                "Wealth and happiness",
                "Intelligence and wisdom",
                "Good children"
            ],
            "challenging_effects": [
                "May be overly idealistic",
                "Can be preachy about beliefs",
                "High expectations from father"
            ],
            "timing": "Fortune increases in Jupiter dasha; spiritual growth; foreign travel"
        },
        10: {
            "verses": "Ch. 31, v. 10",
            "translation": "If Jupiter is in the 10th, the native will be endowed with royal marks, be happy, valorous, will have a firm and strong physique, and will attain kingdom.",
            "detailed_effects": [
                "Excellent for career success",
                "Authority and leadership positions",
                "Government favor and recognition",
                "Strong physique and health",
                "Happiness and contentment",
                "Courage and valor",
                "Fame and reputation"
            ],
            "positive_effects": [
                "Outstanding career achievements",
                "Authority and status",
                "Government positions",
                "Fame and recognition",
                "Strong health"
            ],
            "challenging_effects": [
                "High expectations from career",
                "Pressure to maintain status",
                "May be overly ambitious"
            ],
            "timing": "Career peaks in Jupiter dasha; authority and recognition"
        },
        11: {
            "verses": "Ch. 31, v. 11",
            "translation": "Should Jupiter be in the 11th, the native will be wealthy, will have many sons, be long-lived, and will have attendants.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Wealth and prosperity",
                "Many children and progeny",
                "Long and healthy life",
                "Success in social networks",
                "Fulfillment of desires",
                "Servants and helpers"
            ],
            "positive_effects": [
                "Outstanding financial gains",
                "Many children",
                "Longevity",
                "Social success",
                "Achievement of goals"
            ],
            "challenging_effects": [
                "May be overly optimistic about gains",
                "High expectations from friends",
                "Can be too generous"
            ],
            "timing": "Gains increase with age; peak prosperity in Jupiter dasha"
        },
        12: {
            "verses": "Ch. 31, v. 12",
            "translation": "If Jupiter occupies the 12th, the native will be devoid of wealth and learning, will have limited happiness, and will serve others.",
            "detailed_effects": [
                "Financial losses and expenses",
                "Lack of formal education",
                "Limited happiness",
                "Service to others or foreign lands",
                "Spiritual inclinations develop",
                "Charitable nature",
                "Interest in isolation or meditation"
            ],
            "positive_effects": [
                "Spiritual growth and moksha",
                "Service to humanity",
                "Success in foreign lands",
                "Charitable and generous nature"
            ],
            "challenging_effects": [
                "Financial difficulties",
                "Lack of education",
                "Limited happiness",
                "Serving others rather than leading",
                "Expenses and losses"
            ],
            "timing": "Expenses throughout life; spiritual growth in later years"
        }
    },
    
    "Venus": {
        1: {
            "verses": "Ch. 32, v. 1",
            "translation": "If Venus is in the ascendant, the native will be beautiful, will have a charming physique, be happy, long-lived, timid, and will possess attractive eyes.",
            "detailed_effects": [
                "Beautiful and attractive appearance",
                "Charming and pleasant personality",
                "Artistic and creative nature",
                "Happy and content disposition",
                "Long life and good health",
                "Attractive eyes and features",
                "Gentle and timid nature"
            ],
            "positive_effects": [
                "Outstanding beauty and charm",
                "Artistic talents",
                "Happy and content life",
                "Longevity",
                "Attractive appearance"
            ],
            "challenging_effects": [
                "Timid or shy nature",
                "May be too pleasure-seeking",
                "Can be vain about appearance"
            ],
            "timing": "Venus dasha brings beauty, marriage, artistic success, happiness"
        },
        2: {
            "verses": "Ch. 32, v. 2",
            "translation": "Should Venus be in the 2nd, the native will be a poet, will have attractive speech, will accumulate wealth, and will have a beautiful face.",
            "detailed_effects": [
                "Excellent for wealth accumulation",
                "Beautiful facial features",
                "Sweet and attractive speech",
                "Poetic and artistic abilities",
                "Happy family life",
                "Enjoyment of luxuries",
                "Multiple income sources"
            ],
            "positive_effects": [
                "Outstanding wealth and prosperity",
                "Beautiful face and speech",
                "Poetic and artistic talents",
                "Happy family relationships",
                "Enjoyment of luxuries"
            ],
            "challenging_effects": [
                "May be too focused on material pleasures",
                "Expenses on luxuries",
                "Can be too sweet in speech"
            ],
            "timing": "Wealth increases in Venus dasha; family happiness; artistic success"
        },
        3: {
            "verses": "Ch. 32, v. 3",
            "translation": "If Venus occupies the 3rd, the native will be devoid of happiness from co-born, be miserly, will have a beautiful wife, and be skillful.",
            "detailed_effects": [
                "Challenges with siblings",
                "Miserly or frugal nature",
                "Beautiful and loving spouse",
                "Artistic and creative skills",
                "Success through self-effort",
                "Communication abilities",
                "Courage in artistic pursuits"
            ],
            "positive_effects": [
                "Beautiful spouse",
                "Artistic and creative skills",
                "Success through effort",
                "Communication talents",
                "Financial prudence"
            ],
            "challenging_effects": [
                "Lack of happiness from siblings",
                "Miserly nature",
                "Sibling conflicts"
            ],
            "timing": "Artistic success in Venus dasha; beautiful spouse; sibling issues"
        },
        4: {
            "verses": "Ch. 32, v. 4",
            "translation": "Should Venus be in the 4th, the native will be endowed with excellent conveyances, garments, ornaments, and will enjoy happiness from mother.",
            "detailed_effects": [
                "Excellent for domestic happiness",
                "Good relationship with mother",
                "Vehicles and conveyances",
                "Beautiful clothes and ornaments",
                "Happy home environment",
                "Property and comforts",
                "Artistic home decoration"
            ],
            "positive_effects": [
                "Outstanding domestic happiness",
                "Vehicles and luxuries",
                "Good relationship with mother",
                "Beautiful home and possessions",
                "Comfortable living"
            ],
            "challenging_effects": [
                "May be too attached to comforts",
                "Expenses on luxuries",
                "Can be too comfortable"
            ],
            "timing": "Domestic happiness in Venus dasha; vehicles and luxuries; mother's blessings"
        },
        5: {
            "verses": "Ch. 32, v. 5",
            "translation": "If Venus is in the 5th, the native will be endowed with sons, be happy, intelligent, and will enjoy all kinds of pleasures.",
            "detailed_effects": [
                "Highly auspicious for children",
                "Beautiful and talented offspring",
                "Intelligence and creativity",
                "Romantic and loving nature",
                "Success in creative pursuits",
                "Happiness and pleasure",
                "Artistic talents"
            ],
            "positive_effects": [
                "Blessed with good children",
                "Intelligence and creativity",
                "Happiness and pleasure",
                "Artistic success",
                "Romantic fulfillment"
            ],
            "challenging_effects": [
                "May be too pleasure-seeking",
                "Overindulgence in romance",
                "Expenses on entertainment"
            ],
            "timing": "Children in Venus dasha; creative success; romantic happiness"
        },
        6: {
            "verses": "Ch. 32, v. 6",
            "translation": "Should Venus be in the 6th, the native will have no enemies, be famous, will have a beautiful wife, and will enjoy happiness.",
            "detailed_effects": [
                "Excellent for defeating enemies",
                "Fame and recognition",
                "Beautiful and loving spouse",
                "Victory in disputes",
                "Success in service professions",
                "Happiness and contentment",
                "Diplomatic abilities"
            ],
            "positive_effects": [
                "Outstanding ability to defeat enemies",
                "Fame and recognition",
                "Beautiful spouse",
                "Happiness and success",
                "Diplomatic skills"
            ],
            "challenging_effects": [
                "May face health issues from indulgence",
                "Expenses on pleasures",
                "Can be too accommodating"
            ],
            "timing": "Victory over enemies in Venus dasha; fame; marital happiness"
        },
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
        },
        8: {
            "verses": "Ch. 32, v. 8",
            "translation": "If Venus occupies the 8th, the native will be long-lived, will have limited wealth, and will be devoid of happiness from wife.",
            "detailed_effects": [
                "Long life and longevity",
                "Limited financial resources",
                "Marital challenges",
                "Interest in occult and mysteries",
                "Transformative relationships",
                "Inheritance issues",
                "Deep emotional experiences"
            ],
            "positive_effects": [
                "Outstanding longevity",
                "Deep emotional insight",
                "Interest in occult knowledge",
                "Transformative experiences",
                "Research abilities"
            ],
            "challenging_effects": [
                "Limited wealth",
                "Lack of happiness from spouse",
                "Marital discord",
                "Financial challenges",
                "Sudden losses"
            ],
            "timing": "Long life; marital challenges; financial difficulties"
        },
        9: {
            "verses": "Ch. 32, v. 9",
            "translation": "Should Venus be in the 9th, the native will be devoted to divine and paternal assignments, be endowed with happiness, wealth, and sons.",
            "detailed_effects": [
                "Excellent fortune and blessings",
                "Strong devotion to father and dharma",
                "Religious and spiritual inclinations",
                "Wealth and prosperity",
                "Blessed with children",
                "Artistic and creative talents",
                "Success in higher education"
            ],
            "positive_effects": [
                "Outstanding fortune and blessings",
                "Spiritual devotion",
                "Wealth and happiness",
                "Good children",
                "Artistic success"
            ],
            "challenging_effects": [
                "May be too idealistic in beliefs",
                "Expenses on religious activities",
                "Can be too devoted to pleasures"
            ],
            "timing": "Fortune increases in Venus dasha; spiritual growth; foreign travel"
        },
        10: {
            "verses": "Ch. 32, v. 10",
            "translation": "If Venus is in the 10th, the native will be endowed with royal marks, be happy, valorous, and will attain kingdom.",
            "detailed_effects": [
                "Excellent for career success",
                "Authority and leadership positions",
                "Success in artistic professions",
                "Fame and recognition",
                "Happiness and contentment",
                "Diplomatic abilities",
                "Wealth through career"
            ],
            "positive_effects": [
                "Outstanding career achievements",
                "Authority and status",
                "Fame and recognition",
                "Success in arts and diplomacy",
                "Happiness and prosperity"
            ],
            "challenging_effects": [
                "May be too focused on career pleasures",
                "Expenses on status symbols",
                "Can be too diplomatic"
            ],
            "timing": "Career peaks in Venus dasha; fame and recognition; artistic success"
        },
        11: {
            "verses": "Ch. 32, v. 11",
            "translation": "Should Venus be in the 11th, the native will be wealthy, will have many sons, be long-lived, and will have attendants.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Wealth and prosperity",
                "Many children and progeny",
                "Long and healthy life",
                "Success in social networks",
                "Fulfillment of desires",
                "Servants and helpers"
            ],
            "positive_effects": [
                "Outstanding financial gains",
                "Many children",
                "Longevity",
                "Social success",
                "Achievement of goals"
            ],
            "challenging_effects": [
                "May be too focused on gains",
                "Expenses on social activities",
                "Can be too pleasure-seeking"
            ],
            "timing": "Gains increase with age; peak prosperity in Venus dasha"
        },
        12: {
            "verses": "Ch. 32, v. 12",
            "translation": "If Venus occupies the 12th, the native will be learned in Shastras, be skillful, will have a good wife, and will enjoy happiness.",
            "detailed_effects": [
                "Excellent for spiritual learning",
                "Success in foreign lands",
                "Good marriage and spouse",
                "Happiness and contentment",
                "Interest in meditation and isolation",
                "Charitable nature",
                "Expenses on luxuries"
            ],
            "positive_effects": [
                "Outstanding spiritual learning",
                "Good marriage",
                "Happiness and joy",
                "Success in foreign lands",
                "Artistic and skillful"
            ],
            "challenging_effects": [
                "Expenses and losses",
                "Expenses on pleasures",
                "May be too isolated"
            ],
            "timing": "Spiritual growth in Venus dasha; foreign success; expenses on luxuries"
        }
    },
    
    "Saturn": {
        1: {
            "verses": "Ch. 33, v. 1",
            "translation": "If Saturn is in the ascendant, the native will be lazy, lame, will have a deformed body, be devoid of wealth, and will suffer from diseases.",
            "detailed_effects": [
                "Challenges with physical health",
                "Lazy or slow-moving nature",
                "Possible physical deformities or lameness",
                "Financial difficulties",
                "Chronic health issues",
                "Serious and melancholic disposition",
                "Delays and obstacles in life"
            ],
            "positive_effects": [
                "Discipline and perseverance",
                "Philosophical and introspective nature",
                "Wisdom through hardship",
                "Long-term endurance"
            ],
            "challenging_effects": [
                "Laziness and lethargy",
                "Physical deformities or lameness",
                "Financial difficulties",
                "Chronic diseases",
                "Melancholic nature"
            ],
            "timing": "Saturn dasha brings delays, hardships, but also discipline and wisdom"
        },
        2: {
            "verses": "Ch. 33, v. 2",
            "translation": "Should Saturn be in the 2nd, the native will have an ugly face, will be devoid of wealth, will have a bad wife, and will eat bad food.",
            "detailed_effects": [
                "Financial challenges and poverty",
                "Unattractive facial features",
                "Marital discord",
                "Poor dietary habits",
                "Harsh or slow speech",
                "Family difficulties",
                "Delayed wealth accumulation"
            ],
            "positive_effects": [
                "Discipline in finances if Saturn strong",
                "Frugal and careful with resources",
                "Wisdom in speech when mature"
            ],
            "challenging_effects": [
                "Ugly or unattractive face",
                "Financial difficulties",
                "Bad or difficult spouse",
                "Poor food and nutrition",
                "Family conflicts"
            ],
            "timing": "Financial struggles in early life; improvement after age 36"
        },
        3: {
            "verses": "Ch. 33, v. 3",
            "translation": "If Saturn occupies the 3rd, the native will be valorous, will have limited happiness from co-born, be intelligent, and will have wealth.",
            "detailed_effects": [
                "Courage and perseverance",
                "Limited happiness from siblings",
                "Intelligence and wisdom",
                "Wealth through hard work",
                "Success through self-effort",
                "Disciplined communication",
                "Long-term initiatives"
            ],
            "positive_effects": [
                "Outstanding courage and perseverance",
                "Intelligence and wisdom",
                "Wealth through effort",
                "Disciplined approach",
                "Success through hard work"
            ],
            "challenging_effects": [
                "Limited happiness from siblings",
                "Sibling conflicts or loss",
                "Slow progress",
                "Delays in initiatives"
            ],
            "timing": "Courage develops slowly; wealth through persistent effort in Saturn dasha"
        },
        4: {
            "verses": "Ch. 33, v. 4",
            "translation": "Should Saturn be in the 4th, the native will be devoid of conveyances, relatives, happiness, and lands, and will lose his mother.",
            "detailed_effects": [
                "Challenges with mother or early loss",
                "Lack of domestic peace",
                "Property difficulties or delays",
                "Few vehicles or old vehicles",
                "Emotional distance from family",
                "Heart-related health concerns",
                "Frequent residence changes"
            ],
            "positive_effects": [
                "Independence and self-reliance",
                "Discipline in domestic matters",
                "Property gains after age 36"
            ],
            "challenging_effects": [
                "Lack of domestic happiness",
                "Mother's early death or separation",
                "Loss of property",
                "Few or no vehicles",
                "Emotional coldness"
            ],
            "timing": "Domestic challenges throughout life; property gains delayed"
        },
        5: {
            "verses": "Ch. 33, v. 5",
            "translation": "If Saturn is in the 5th, the native will be devoid of happiness, wealth, and sons, be evil-minded, and will suffer from stomach diseases.",
            "detailed_effects": [
                "Difficulties with children or childlessness",
                "Delayed or no progeny",
                "Financial challenges",
                "Digestive health issues",
                "Pessimistic or negative thinking",
                "Creative blocks",
                "Speculative losses"
            ],
            "positive_effects": [
                "Discipline in creative pursuits",
                "Wisdom and philosophical thinking",
                "Adopted children may bring happiness"
            ],
            "challenging_effects": [
                "Lack of children or childlessness",
                "Financial difficulties",
                "Evil or negative mindset",
                "Stomach and digestive problems",
                "Lack of happiness"
            ],
            "timing": "Children delayed or absent; financial struggles; health issues"
        },
        6: {
            "verses": "Ch. 33, v. 6",
            "translation": "Should Saturn be in the 6th, the native will be very strong, will destroy his enemies, be famous, and will enjoy happiness.",
            "detailed_effects": [
                "Excellent for defeating enemies",
                "Strong physical constitution",
                "Victory in disputes and competitions",
                "Fame and recognition",
                "Success in service professions",
                "Happiness and contentment",
                "Disciplined approach to work"
            ],
            "positive_effects": [
                "Outstanding ability to defeat enemies",
                "Strong health and vitality",
                "Fame and recognition",
                "Success in competition",
                "Happiness and prosperity"
            ],
            "challenging_effects": [
                "Chronic health issues if afflicted",
                "Slow victory over enemies",
                "Work-related stress"
            ],
            "timing": "Victory over enemies in Saturn dasha; fame and recognition"
        },
        7: {
            "verses": "Ch. 33, v. 7",
            "translation": "If Saturn occupies the 7th, the native will lose his wife, will suffer from diseases, be sinful, and will be devoid of happiness.",
            "detailed_effects": [
                "Marital challenges and delays",
                "Loss of spouse or separation",
                "Health issues affecting marriage",
                "Late marriage or multiple marriages",
                "Business partnership difficulties",
                "Chronic health problems",
                "Lack of happiness"
            ],
            "positive_effects": [
                "Discipline in partnerships if Saturn strong",
                "Long-lasting relationships when formed",
                "Success with older or mature partners"
            ],
            "challenging_effects": [
                "Loss of wife or marital discord",
                "Chronic diseases",
                "Sinful or unethical behavior",
                "Lack of happiness",
                "Partnership conflicts"
            ],
            "timing": "Marriage challenges throughout life; late marriage common"
        },
        8: {
            "verses": "Ch. 33, v. 8",
            "translation": "Should Saturn be in the 8th, the native will be short-lived, will suffer from diseases, be devoid of wealth, and will have a defective body.",
            "detailed_effects": [
                "Chronic health concerns",
                "Reduced longevity if afflicted",
                "Financial instability",
                "Interest in occult and mysteries",
                "Physical defects or weakness",
                "Inheritance issues",
                "Sudden losses and crises"
            ],
            "positive_effects": [
                "Deep research abilities",
                "Interest in occult knowledge",
                "Transformative wisdom",
                "Discipline in crises"
            ],
            "challenging_effects": [
                "Short lifespan",
                "Chronic diseases",
                "Financial difficulties",
                "Physical defects",
                "Sudden losses"
            ],
            "timing": "Health challenges throughout life; crises and transformations"
        },
        9: {
            "verses": "Ch. 33, v. 9",
            "translation": "If Saturn is in the 9th, the native will be devoid of wealth, children, and wife, will hate his father, and will not be inclined to religious deeds.",
            "detailed_effects": [
                "Strained relationship with father",
                "Challenges in higher education",
                "Difficulties with children",
                "Marital challenges",
                "Financial struggles",
                "Lack of religious inclination",
                "Foreign travel difficulties"
            ],
            "positive_effects": [
                "Independent philosophy",
                "Discipline in spiritual pursuits when mature",
                "Wisdom through hardship"
            ],
            "challenging_effects": [
                "Father's health issues or separation",
                "Loss of wealth",
                "Difficulties with children",
                "Marital problems",
                "Lack of spiritual inclination"
            ],
            "timing": "Father-related issues; spiritual awakening delayed or absent"
        },
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
        },
        11: {
            "verses": "Ch. 33, v. 11",
            "translation": "Should Saturn be in the 11th, the native will be wealthy, will have limited number of children, be long-lived, and will have attendants.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Wealth through discipline and hard work",
                "Few children but responsible",
                "Long and healthy life",
                "Success in social networks",
                "Fulfillment of desires through effort",
                "Servants and helpers"
            ],
            "positive_effects": [
                "Outstanding financial gains",
                "Longevity and good health",
                "Wealth from persistent effort",
                "Achievement of goals",
                "Social success"
            ],
            "challenging_effects": [
                "Limited number of children",
                "Slow gains and delays",
                "Serious friendships"
            ],
            "timing": "Gains increase with age; peak prosperity after age 36 in Saturn dasha"
        },
        12: {
            "verses": "Ch. 33, v. 12",
            "translation": "If Saturn occupies the 12th, the native will be devoid of wealth and learning, will have limited happiness, and will serve others.",
            "detailed_effects": [
                "Financial losses and expenses",
                "Lack of formal education",
                "Limited happiness",
                "Service to others or foreign lands",
                "Spiritual inclinations develop",
                "Interest in isolation or meditation",
                "Expenditure exceeds income"
            ],
            "positive_effects": [
                "Spiritual growth and moksha",
                "Service to humanity",
                "Success in foreign lands",
                "Discipline in spiritual practices"
            ],
            "challenging_effects": [
                "Financial difficulties",
                "Lack of education",
                "Limited happiness",
                "Serving others rather than leading",
                "Expenses and losses"
            ],
            "timing": "Expenses throughout life; spiritual growth in later years"
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
