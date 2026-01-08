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
        4: {
            "verses": "24.7",
            "translation": "Sun in the 4th house: The native will be without happiness from relatives, will be bereft of conveyances, relatives, lands, and friends.",
            "detailed_effects": [
                "Challenges with mother or maternal relationships",
                "Property matters require attention",
                "Frequent changes of residence",
                "Inner peace requires conscious cultivation",
                "May distance from homeland",
                "Emotional security sought through achievements"
            ],
            "positive_effects": [
                "Strong will to create own foundation",
                "Success in real estate if Sun well-placed",
                "Leadership in family matters over time"
            ],
            "challenging_effects": [
                "Maternal relationship strained",
                "Lack of emotional peace at home",
                "Property disputes or losses",
                "Difficulty settling in one place"
            ],
            "remedies": [
                "Honor mother despite difficulties",
                "Practice grounding meditation",
                "Perform Vastu remedies for home peace"
            ]
        },
        5: {
            "verses": "24.8",
            "translation": "Sun in the 5th house: The native will be bereft of happiness from children, be intelligent, scholarly, and will have heart disease.",
            "detailed_effects": [
                "Highly intelligent and creative",
                "Strong inclination toward spirituality and learning",
                "Challenges regarding children - delays or difficulties",
                "Excellent for speculation and investments when strong",
                "Past life merit manifests as wisdom",
                "Romantic relationships intense but may face obstacles"
            ],
            "positive_effects": [
                "Exceptional intelligence and creativity",
                "Success in speculation, stock market, gambling",
                "Strong spiritual knowledge",
                "Recognition for intellectual achievements"
            ],
            "challenging_effects": [
                "Difficulties with children - delays or strained relationships",
                "Heart or upper back health issues",
                "Ego in romantic matters",
                "Over-confidence in speculative ventures"
            ],
            "remedies": [
                "Recite Aditya Hridayam for heart health",
                "Be patient regarding children",
                "Balance ego in creative expression"
            ]
        },
        9: {
            "verses": "24.12",
            "translation": "Sun in the 9th house: The native will lack paternal bliss, will make fortunes through wife, be bereft of religious merit and be miserable.",
            "detailed_effects": [
                "Strong dharmic inclination and righteousness",
                "Foreign travel and higher learning favorable",
                "Father relationship complex or distant",
                "Fortune improves after father or through spouse",
                "Natural teacher and guide in spiritual matters",
                "Government or religious work beneficial"
            ],
            "positive_effects": [
                "Strong spiritual and philosophical inclination",
                "Success in higher education and teaching",
                "Foreign connections beneficial",
                "Good fortune in later life",
                "Respected for wisdom and righteousness"
            ],
            "challenging_effects": [
                "Father relationship distant or challenging",
                "Religious dogmatism possible",
                "Conflicts with gurus or mentors"
            ],
            "remedies": [
                "Study and teach sacred texts",
                "Respect father despite difficulties",
                "Practice humility in spiritual matters"
            ]
        },
        11: {
            "verses": "24.14",
            "translation": "Sun in the 11th house: The native will be long-lived, will be endowed with wealth, conveyances and happiness, will have limited progeny and will have permanent enemies.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Strong friendship network and social connections",
                "Elder siblings supportive",
                "Fulfillment of desires and ambitions",
                "Leadership in groups and organizations",
                "Multiple income sources"
            ],
            "positive_effects": [
                "High income and financial gains",
                "Influential social network",
                "Goals and ambitions achieved",
                "Recognition from government or large organizations",
                "Long life and prosperity"
            ],
            "challenging_effects": [
                "Few children or challenges with progeny",
                "Some enemies among friends",
                "May dominate in social groups"
            ],
            "remedies": [
                "Use gains for charitable purposes",
                "Be humble in social circles",
                "Support younger generation"
            ]
        },
        3: {
            "verses": "24.6",
            "translation": "Sun in the 3rd house: The native will be valorous, strong, inimical to relatives, wealthy, will destroy enemies, and will be bereft of brothers.",
            "detailed_effects": [
                "Courageous and adventurous nature",
                "Strong communication and self-expression",
                "Success through own efforts and initiative",
                "May have strained sibling relationships",
                "Good at overcoming obstacles and competitors",
                "Physical strength and vitality",
                "Independent, self-made success"
            ],
            "positive_effects": [
                "Exceptional courage and determination",
                "Victory over enemies and obstacles",
                "Strong willpower and initiative",
                "Success in competitive fields",
                "Good writing or communication abilities"
            ],
            "challenging_effects": [
                "Conflicts with siblings",
                "Aggressive communication style",
                "May lack brotherly support",
                "Tendency toward egoistic self-expression"
            ],
            "remedies": [
                "Practice diplomatic communication",
                "Make peace with siblings",
                "Use courage for righteous causes"
            ]
        },
        6: {
            "verses": "24.9",
            "translation": "Sun in the 6th house: The native will be very strong, will have weak vision, will be devoid of wealth, inimical disposition, and will destroy enemies.",
            "detailed_effects": [
                "Excellent for overcoming enemies and obstacles",
                "Success in service, medicine, law enforcement",
                "Strong digestive fire but health challenges",
                "Ability to handle conflicts and litigation",
                "May face financial ups and downs",
                "Uncle (maternal) support possible",
                "Victory over diseases and adversaries"
            ],
            "positive_effects": [
                "Defeats enemies and competitors",
                "Success in service professions",
                "Ability to overcome health issues",
                "Good for military, police, legal work",
                "Strong constitution despite challenges"
            ],
            "challenging_effects": [
                "Chronic health issues possible",
                "Conflicts and legal battles",
                "Financial struggles",
                "Enemies and opposition",
                "Eye problems"
            ],
            "remedies": [
                "Serve the sick and needy",
                "Maintain strong health discipline",
                "Avoid unnecessary conflicts",
                "Strengthen Sun through worship"
            ]
        },
        7: {
            "verses": "24.10",
            "translation": "Sun in the 7th house: The native will be poor, insulted, suffers from dental and eye problems, will incur royal displeasure, will lose wife, and be devoid of happiness.",
            "detailed_effects": [
                "Challenges in marriage and partnerships",
                "Strong personality that may dominate partner",
                "Late marriage often beneficial",
                "Business partnerships require care",
                "Spouse may have leadership qualities",
                "Public-facing work favorable",
                "Need to balance ego in relationships"
            ],
            "positive_effects": [
                "Leadership in partnerships",
                "Success in public dealings",
                "Strong spouse with character",
                "Business acumen if Sun well-placed"
            ],
            "challenging_effects": [
                "Marital conflicts due to ego",
                "Dominance issues with partner",
                "Separation or delays in marriage",
                "Dental and eye health issues",
                "Partnership disputes"
            ],
            "remedies": [
                "Practice humility in marriage",
                "Marry after age 28",
                "Balance independence with partnership",
                "Strengthen Venus for marital harmony"
            ]
        },
        8: {
            "verses": "24.11 (part)",
            "translation": "Sun in the 8th house: The native will have limited eyesight, be devoid of wealth and happiness, will suffer humiliation and will be dependent on others.",
            "detailed_effects": [
                "Interest in occult, mysticism, transformation",
                "Hidden sources of income possible",
                "Longevity generally good despite challenges",
                "Research and investigation skills",
                "Inheritance matters important",
                "Chronic health issues require attention",
                "Spiritual transformation through crises"
            ],
            "positive_effects": [
                "Deep insight into hidden matters",
                "Success in research and occult",
                "Inheritance and legacy gains possible",
                "Longevity if Sun strong",
                "Transformative spiritual experiences"
            ],
            "challenging_effects": [
                "Financial instability",
                "Health challenges, especially eyes",
                "Sudden upheavals and crises",
                "Issues with inheritance",
                "Hidden enemies"
            ],
            "remedies": [
                "Practice spiritual discipline",
                "Handle father's legacy with care",
                "Donate for eye hospitals",
                "Strengthen Sun through mantras"
            ]
        },
        12: {
            "verses": "24.15",
            "translation": "Sun in the 12th house: The native will have defective eyes, be devoid of wealth, will commit sinful acts, will have a diseased body, and be bereft of virtues.",
            "detailed_effects": [
                "Expenditure on spiritual and charitable causes",
                "Foreign travel and residence possible",
                "Sleep disturbances or eye problems",
                "Success in foreign lands",
                "Isolated work environments favorable",
                "Spiritual seeking and moksha orientation",
                "Hidden expenses and losses"
            ],
            "positive_effects": [
                "Success in foreign countries",
                "Spiritual inclination and liberation",
                "Work in hospitals, ashrams, retreats",
                "Charitable disposition",
                "Moksha orientation"
            ],
            "challenging_effects": [
                "Financial losses and high expenses",
                "Eye problems and sleep issues",
                "Separation from homeland",
                "Father's loss or distance",
                "Hidden enemies"
            ],
            "remedies": [
                "Channel expenses toward spirituality",
                "Serve in charitable institutions",
                "Practice meditation and sleep discipline",
                "Donate for spiritual causes"
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
        },
        2: {
            "verses": "24.16",
            "translation": "Moon in the 2nd house: The native will be wealthy, soft-spoken, will enjoy food, be an eloquent speaker, and will possess beautiful eyes.",
            "detailed_effects": [
                "Sweet, pleasing speech and eloquence",
                "Good relationship with family, especially mother",
                "Wealth accumulation through nurturing professions",
                "Love of food and comfort",
                "Beautiful eyes and pleasant face",
                "Income fluctuates with Moon phases",
                "Emotional security through material stability"
            ],
            "positive_effects": [
                "Excellent for wealth and family happiness",
                "Natural talent for poetry, singing, counseling",
                "Strong maternal family support",
                "Gains through liquids, food, or public-facing work"
            ],
            "challenging_effects": [
                "Income may fluctuate",
                "Emotional spending habits",
                "Over-attachment to material security"
            ],
            "remedies": [
                "Maintain stable savings despite fluctuations",
                "Use eloquence for teaching and uplifting",
                "Honor mother and maternal lineage"
            ]
        },
        4: {
            "verses": "24.18",
            "translation": "Moon in the 4th house: The native will be happy, endowed with relatives, friends, sons, lands, and conveyances, and will be charitable and learned.",
            "detailed_effects": [
                "Excellent placement for emotional happiness and peace",
                "Strong relationship with mother",
                "Property, vehicles, and material comforts",
                "Love of home and domestic life",
                "Nurturing family environment",
                "Success in real estate, hospitality, counseling",
                "Inner peace and contentment"
            ],
            "positive_effects": [
                "Exceptional emotional security and happiness",
                "Blessed with property and conveyances",
                "Loving relationship with mother",
                "Success in nurturing professions",
                "Strong family foundation"
            ],
            "challenging_effects": [
                "Emotional dependency on home environment",
                "Difficulty leaving homeland",
                "May be overly attached to mother"
            ],
            "remedies": [
                "Express gratitude for blessings",
                "Share home comforts with others",
                "Maintain emotional balance"
            ]
        },
        7: {
            "verses": "24.20",
            "translation": "Moon in the 7th house: The native will be amiable, happy, will possess a good physique, be sensuously disposed, and will be wealthy.",
            "detailed_effects": [
                "Attractive, beautiful spouse",
                "Emotional fulfillment through partnership",
                "Public popularity and likability",
                "Success in public relations and hospitality",
                "Strong desire for companionship",
                "Business partnerships favorable",
                "Romantic and sensitive in relationships"
            ],
            "positive_effects": [
                "Happy marriage with emotional connection",
                "Beautiful, caring spouse",
                "Success in businesses dealing with public",
                "Popularity and social grace",
                "Wealth through partnerships"
            ],
            "challenging_effects": [
                "Emotional dependency on partner",
                "Mood affects relationship harmony",
                "May idealize partner unrealistically"
            ],
            "remedies": [
                "Maintain emotional stability in marriage",
                "Practice independence alongside partnership",
                "Use emotional intelligence for harmony"
            ]
        },
        10: {
            "verses": "24.23",
            "translation": "Moon in the 10th house: The native will be virtuous, religious, fortunate, will perform good acts, and will be endowed with sons, happiness, and wealth.",
            "detailed_effects": [
                "Public career dealing with masses",
                "Success through nurturing, caring professions",
                "Popularity with public and authorities",
                "Mother's influence on career",
                "Work involving liquids, food, hospitality, healthcare",
                "Emotional satisfaction from career achievements",
                "Fame through service to others"
            ],
            "positive_effects": [
                "Excellent for public-facing careers",
                "Natural ability to connect with masses",
                "Success in hospitality, nursing, counseling, food",
                "Recognition for caring and service",
                "Mother supports career"
            ],
            "challenging_effects": [
                "Career may fluctuate with emotional state",
                "Public scrutiny affects emotions",
                "Work-life balance challenging"
            ],
            "remedies": [
                "Maintain emotional stability in profession",
                "Use popularity for social benefit",
                "Balance career with family needs"
            ]
        },
        3: {
            "verses": "24.17",
            "translation": "Moon in the 3rd house: The native will have praiseworthy habits, be endowed with brothers, be valorous, happy, and will have weak arms.",
            "detailed_effects": [
                "Good relationship with siblings",
                "Creative communication abilities",
                "Love of travel and short journeys",
                "Emotional courage and initiative",
                "Artistic self-expression",
                "Success through own efforts",
                "Changeable interests"
            ],
            "positive_effects": [
                "Supportive siblings",
                "Good communication skills",
                "Creative writing or arts",
                "Adaptable and versatile",
                "Emotional courage"
            ],
            "challenging_effects": [
                "Restless mind",
                "Inconsistent efforts",
                "May lack physical strength",
                "Emotional instability in projects"
            ]
        },
        5: {
            "verses": "24.19",
            "translation": "Moon in the 5th house: The native will be scholarly, virtuous, will have good sons, be wise, and will be a king's minister or equal to him.",
            "detailed_effects": [
                "Excellent for creativity and intelligence",
                "Good relationship with children",
                "Emotional investment in learning",
                "Success in speculation if Moon strong",
                "Romantic and sensitive nature",
                "Advisory roles suitable",
                "Past life merit manifests"
            ],
            "positive_effects": [
                "Intelligent and learned",
                "Blessed with children",
                "Creative and artistic",
                "Success in education and advisory",
                "Good fortune"
            ],
            "challenging_effects": [
                "Emotional attachment to children",
                "Speculation risky if Moon weak",
                "Mood affects creativity"
            ]
        },
        6: {
            "verses": "24.19 (part)",
            "translation": "Moon in the 6th house: The native will suffer stomach ailments, will be renowned, wealthy, will have many enemies, and be lazy.",
            "detailed_effects": [
                "Service-oriented career",
                "Success in healing professions",
                "Digestive issues common",
                "Ability to overcome obstacles",
                "Maternal relatives may cause issues",
                "Fluctuating health",
                "Emotional resilience"
            ],
            "positive_effects": [
                "Success in nursing, counseling",
                "Overcomes enemies eventually",
                "Wealth through service",
                "Emotional strength"
            ],
            "challenging_effects": [
                "Stomach and digestive problems",
                "Emotional stress from conflicts",
                "Mother's health concerns",
                "Enemies and litigation"
            ]
        },
        8: {
            "verses": "24.21",
            "translation": "Moon in the 8th house: The native will be short-lived, suffer humiliation, be abandoned by his relatives, and undergo many diseases.",
            "detailed_effects": [
                "Interest in occult and mysticism",
                "Emotional depth and transformation",
                "Psychic sensitivity",
                "Research abilities",
                "Mother's longevity concerns",
                "Hidden emotional issues",
                "Inheritance matters"
            ],
            "positive_effects": [
                "Deep intuition",
                "Occult abilities",
                "Psychological insight",
                "Transformative experiences"
            ],
            "challenging_effects": [
                "Emotional crises",
                "Health fluctuations",
                "Mother's health issues",
                "Hidden anxieties",
                "Sudden changes"
            ]
        },
        9: {
            "verses": "24.22",
            "translation": "Moon in the 9th house: The native will be devoted to divine and paternal assignments, will be endowed with happiness, wealth, intelligence, and sons, and will be victorious.",
            "detailed_effects": [
                "Fortunate and blessed",
                "Strong dharmic inclination",
                "Mother supports spiritual growth",
                "Success in higher learning",
                "Foreign travel beneficial",
                "Good relationship with teachers",
                "Wisdom and intuition"
            ],
            "positive_effects": [
                "Excellent fortune",
                "Spiritual wisdom",
                "Higher education success",
                "Foreign gains",
                "Blessed with children"
            ],
            "challenging_effects": [
                "Emotional attachment to beliefs",
                "May change beliefs frequently",
                "Travel may be restless"
            ]
        },
        11: {
            "verses": "24.24",
            "translation": "Moon in the 11th house: The native will be intelligent, endowed with wealth, long-lived, will have lasting children, and be victorious over enemies.",
            "detailed_effects": [
                "Excellent for gains and fulfillment",
                "Strong social network",
                "Popular in groups",
                "Elder siblings supportive",
                "Multiple income sources",
                "Emotional fulfillment through friends",
                "Goals achieved"
            ],
            "positive_effects": [
                "High income",
                "Popular and well-connected",
                "Desires fulfilled",
                "Long life",
                "Good children"
            ],
            "challenging_effects": [
                "Emotional dependency on groups",
                "Income may fluctuate",
                "Friends may be fickle"
            ]
        },
        12: {
            "verses": "24.25",
            "translation": "Moon in the 12th house: The native will be bereft of good looks, will be stupid, will be inimical, will spend on evil deeds, be distressed, and irritable.",
            "detailed_effects": [
                "Spiritual seeking and moksha",
                "Foreign residence likely",
                "Work in isolation beneficial",
                "Sleep issues or insomnia",
                "Emotional seclusion",
                "Expenses on family or mother",
                "Hidden emotional life"
            ],
            "positive_effects": [
                "Strong spiritual inclination",
                "Success in foreign lands",
                "Meditation abilities",
                "Charitable nature",
                "Liberation orientation"
            ],
            "challenging_effects": [
                "Emotional loneliness",
                "Sleep disorders",
                "High expenses",
                "Mother's health or distance",
                "Hidden sorrows"
            ]
        }
    },
    
    "Mars": {
        1: {
            "verses": "24.26",
            "translation": "Mars in the ascendant: The native will suffer from diseases, will be cruel, haughty, will make unsteady or little wealth, will have diseased limbs, and will be devoid of happiness.",
            "detailed_effects": [
                "Dynamic, energetic personality",
                "Strong physical vitality and courage",
                "Independent and assertive nature",
                "Quick to anger but also to forgive",
                "Athletic or competitive inclinations",
                "Tendency toward accidents or injuries",
                "Leadership through action"
            ],
            "positive_effects": [
                "Exceptional courage and determination",
                "Strong physical body and stamina",
                "Natural warrior and competitor",
                "Technical and mechanical skills",
                "Quick decision-making abilities"
            ],
            "challenging_effects": [
                "Aggressive or impulsive behavior",
                "Prone to accidents and injuries",
                "Blood pressure issues",
                "Conflict-prone temperament",
                "Impatience and anger"
            ],
            "remedies": [
                "Practice anger management",
                "Channel energy through sports",
                "Worship Mars deity (Mangal)",
                "Recite Hanuman Chalisa"
            ]
        },
        2: {
            "verses": "24.27",
            "translation": "Mars in the 2nd house: The native will be devoid of learning and wealth, will eat undesirable food, will be dependent on bad people, and will have a troubled face.",
            "detailed_effects": [
                "Harsh or aggressive speech",
                "Financial ups and downs",
                "Family conflicts possible",
                "Strong appetite and metabolism",
                "Self-made wealth through effort",
                "Technical or engineering skills",
                "Direct communication style"
            ],
            "positive_effects": [
                "Ability to rebuild wealth",
                "Strong determination in finances",
                "Technical earning abilities"
            ],
            "challenging_effects": [
                "Harsh speech causes problems",
                "Financial instability",
                "Family disputes",
                "Dental or facial issues"
            ]
        },
        3: {
            "verses": "24.28",
            "translation": "Mars in the 3rd house: The native will be devoid of brothers, be miserable, given to anger, and will have a diseased throat and ears.",
            "detailed_effects": [
                "Excellent for courage and initiative",
                "Success through own efforts",
                "Strained sibling relationships",
                "Strong communication drive",
                "Athletic or competitive pursuits",
                "Technical writing abilities",
                "Victory over obstacles"
            ],
            "positive_effects": [
                "Exceptional courage",
                "Strong initiative and drive",
                "Success in competitive fields",
                "Technical skills",
                "Defeats enemies"
            ],
            "challenging_effects": [
                "Conflicts with siblings",
                "Aggressive communication",
                "Accidents during travel",
                "Ear or throat problems"
            ]
        },
        4: {
            "verses": "24.29",
            "translation": "Mars in the 4th house: The native will be devoid of relatives, conveyances, happiness, and lands, will live in others' houses, and will serve the king.",
            "detailed_effects": [
                "Challenges with mother or home life",
                "Frequent residence changes",
                "Property through own efforts",
                "Technical or engineering career",
                "Emotional restlessness",
                "Vehicle accidents to guard against",
                "Service in military or government"
            ],
            "positive_effects": [
                "Success through service",
                "Self-made property",
                "Technical expertise"
            ],
            "challenging_effects": [
                "Mother relationship strained",
                "Lack of peace at home",
                "Property disputes",
                "Vehicle accidents risk"
            ]
        },
        5: {
            "verses": "24.30",
            "translation": "Mars in the 5th house: The native will be devoid of happiness from sons, will be without wealth and learning, and will be cruel.",
            "detailed_effects": [
                "Challenges with children",
                "Competitive in speculation",
                "Strong romantic drive",
                "Technical or sports abilities",
                "Risk-taking nature",
                "Abdominal health issues",
                "Quick intelligence"
            ],
            "positive_effects": [
                "Success in speculation if strong",
                "Athletic abilities",
                "Quick decision-making",
                "Technical creativity"
            ],
            "challenging_effects": [
                "Difficulties with children",
                "Impulsive speculation losses",
                "Romantic conflicts",
                "Abdominal issues"
            ]
        },
        6: {
            "verses": "24.31",
            "translation": "Mars in the 6th house: The native will attain happiness, wealth, will conquer enemies, will be famous, and will not have brothers.",
            "detailed_effects": [
                "Excellent placement - overcomes obstacles",
                "Success in service and competition",
                "Victory over enemies and diseases",
                "Military, police, medical fields favorable",
                "Strong immune system",
                "Sibling issues possible",
                "Litigation success"
            ],
            "positive_effects": [
                "Defeats all enemies",
                "Success in service",
                "Strong health overall",
                "Wealth through effort",
                "Competitive success"
            ],
            "challenging_effects": [
                "Conflicts are common",
                "Blood-related issues",
                "Strained with siblings"
            ]
        },
        7: {
            "verses": "24.32",
            "translation": "Mars in the 7th house: The native will be deprived of his wife, will suffer from diseases, be mean, be a sexual pervert, and will face downfall.",
            "detailed_effects": [
                "Challenges in marriage - Manglik dosha",
                "Assertive or aggressive spouse",
                "Business partnership conflicts",
                "Strong sexual drive",
                "Late marriage beneficial",
                "Spouse may be technical or athletic",
                "Marital counseling helpful"
            ],
            "positive_effects": [
                "Dynamic business partnerships",
                "Energetic spouse",
                "Success in competitive business"
            ],
            "challenging_effects": [
                "Marital conflicts frequent",
                "Separation risks",
                "Partnership disputes",
                "Sexual issues",
                "Manglik considerations"
            ],
            "remedies": [
                "Marry after 28 or match Manglik",
                "Kuja dosha remedies",
                "Practice patience in marriage"
            ]
        },
        8: {
            "verses": "24.33",
            "translation": "Mars in the 8th house: The native will have few friends, be short-lived, will suffer humiliation, and will be troubled by enemies.",
            "detailed_effects": [
                "Interest in occult and mysteries",
                "Research and investigation skills",
                "Sudden events and transformations",
                "Inheritance conflicts",
                "Chronic health issues",
                "Sexual intensity",
                "Hidden sources of income"
            ],
            "positive_effects": [
                "Deep research abilities",
                "Occult knowledge",
                "Inheritance possible",
                "Transformative power"
            ],
            "challenging_effects": [
                "Accidents and surgeries",
                "Chronic health issues",
                "Sudden crises",
                "Inheritance disputes",
                "Longevity concerns"
            ]
        },
        9: {
            "verses": "24.34",
            "translation": "Mars in the 9th house: The native will be devoid of fortunes, father, religious dispositions, and be sinful and not trustworthy.",
            "detailed_effects": [
                "Conflicts with father or teachers",
                "Independent beliefs",
                "Foreign travel for work",
                "Technical or engineering education",
                "Challenges in higher learning",
                "Dharma through action",
                "Self-made fortune"
            ],
            "positive_effects": [
                "Independent thinking",
                "Success abroad",
                "Technical expertise",
                "Warrior dharma"
            ],
            "challenging_effects": [
                "Father relationship strained",
                "Conflicts with gurus",
                "Religious disagreements",
                "Accidents during travel"
            ]
        },
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
        },
        11: {
            "verses": "24.36",
            "translation": "Mars in the 11th house: The native will be endowed with wealth, happiness, longevity, will be courageous, and will have limited progeny.",
            "detailed_effects": [
                "Excellent for gains and income",
                "Success in competitive fields",
                "Strong social network",
                "Technical income sources",
                "Elder siblings supportive",
                "Ambitious goals achieved",
                "Athletic or competitive groups"
            ],
            "positive_effects": [
                "High income through effort",
                "Ambitious goals fulfilled",
                "Competitive success",
                "Strong network",
                "Long life"
            ],
            "challenging_effects": [
                "Few children",
                "Conflicts in groups",
                "Aggressive friendships"
            ]
        },
        12: {
            "verses": "24.37",
            "translation": "Mars in the 12th house: The native will have diseased eyes, will be bereft of wealth and happiness, will live in foreign lands, suffer pains, and will face imprisonment.",
            "detailed_effects": [
                "High expenditure on various causes",
                "Foreign residence or work",
                "Hidden enemies",
                "Isolated work environments",
                "Sleep disturbances",
                "Sexual expenses",
                "Spiritual warrior path"
            ],
            "positive_effects": [
                "Success in foreign lands",
                "Spiritual discipline",
                "Research in isolation",
                "Moksha through action"
            ],
            "challenging_effects": [
                "Financial losses",
                "Eye problems",
                "Hidden enemies",
                "Accidents or confinement",
                "Sleep issues"
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
    
    "Venus": {
        1: {
            "verses": "24.53",
            "translation": "Venus in the ascendant: The native will be handsome, will possess a beautiful body, be happy, long-lived, and capable of many undertakings.",
            "detailed_effects": [
                "Attractive, charming personality with refined manners",
                "Beautiful physical appearance and graceful demeanor",
                "Natural magnetism and ability to attract others",
                "Love of beauty, arts, and aesthetic pleasures",
                "Diplomatic, harmonious approach to life",
                "Good marriage prospects and happy relationships",
                "Material comforts and luxuries come naturally",
                "Artistic talents and creative expression",
                "Generally fortunate and pleasant life"
            ],
            "positive_effects": [
                "Exceptional charm and social grace",
                "Success in arts, fashion, beauty industries",
                "Happy marriage and romantic fulfillment",
                "Material prosperity and comfortable lifestyle",
                "Popularity and admiration from others",
                "Refined taste and aesthetic sensibilities"
            ],
            "challenging_effects": [
                "May be overly concerned with appearance",
                "Tendency toward sensual indulgence",
                "Can be vain or superficial",
                "May prioritize pleasure over duty",
                "Possible relationship complications due to attractiveness"
            ],
            "remedies": [
                "Practice moderation in sensual pleasures",
                "Use charm for benevolent purposes",
                "Cultivate inner beauty alongside outer",
                "Donate white items or sweets on Fridays",
                "Worship Goddess Lakshmi"
            ],
            "life_areas": {
                "personality": "Charming, artistic, diplomatic, pleasure-loving",
                "appearance": "Attractive and well-groomed with natural grace",
                "relationships": "Success in love and marriage; popular socially",
                "career": "Arts, beauty, fashion, hospitality, luxury goods"
            }
        },
        2: {
            "verses": "24.54",
            "translation": "Venus in the 2nd house: The native will be a poet, will have beautiful speech, be wealthy, handsome, and be an expert in all Shastras.",
            "detailed_effects": [
                "Eloquent, sweet, and persuasive speech",
                "Wealth accumulation through artistic or beauty-related means",
                "Beautiful face and pleasant voice",
                "Family life harmonious and prosperous",
                "Income from creative or luxury goods",
                "Good food habits and culinary appreciation",
                "Education in arts or humanities likely"
            ],
            "positive_effects": [
                "Natural ability for poetry, singing, or eloquent expression",
                "Financial prosperity through Venusian pursuits",
                "Happy family relationships",
                "Refined taste in food, clothing, possessions",
                "Can earn through counseling, beauty, arts"
            ],
            "challenging_effects": [
                "May spend excessively on luxuries",
                "Tendency to prioritize pleasure over savings",
                "Sweet speech may sometimes lack directness"
            ],
            "remedies": [
                "Practice financial discipline",
                "Share wealth with family and needy",
                "Use eloquence for teaching and uplifting others"
            ]
        },
        7: {
            "verses": "24.59",
            "translation": "Venus in the 7th house: The native will be very beautiful, happy with his wife, be fond of sexual pleasures, will have vehicles and wealth, and will lose wealth on account of women.",
            "detailed_effects": [
                "Excellent placement for marriage and partnerships",
                "Attractive, loving, and harmonious spouse",
                "Strong romantic and sexual fulfillment in marriage",
                "Success in business partnerships",
                "Diplomatic skills in negotiations",
                "May have multiple relationships or attraction from many",
                "Wealth through spouse or partnerships",
                "Travel and luxury through relationships"
            ],
            "positive_effects": [
                "Very auspicious for love marriage",
                "Beautiful, cultured, and loving spouse",
                "Happy, harmonious married life",
                "Success in partnership businesses",
                "Social popularity as a couple",
                "Material comforts through spouse"
            ],
            "challenging_effects": [
                "Excessive focus on romantic/sexual pleasures",
                "May face financial losses through spouse or relationships",
                "Tendency to idealize partner",
                "Possible complications from multiple attractions",
                "Spouse may be demanding or expensive"
            ],
            "remedies": [
                "Respect and honor spouse",
                "Balance romantic life with spiritual practices",
                "Be prudent with finances in partnerships",
                "Practice fidelity and loyalty"
            ],
            "life_areas": {
                "marriage": "Excellent - beautiful spouse, happy married life",
                "partnerships": "Success in business partnerships, diplomatic skills",
                "relationships": "Popular, attractive to opposite sex",
                "wealth": "Gains through partnerships but watch expenditures"
            },
            "timing": "Marriage likely during Venus mahadasha or favorable transits. Effects strongest in youth and middle age.",
            "notable_yogas": [
                "Can form Malavya Yoga if Venus in own sign (Taurus/Libra)",
                "Contributes to relationship and wealth yogas"
            ]
        },
        10: {
            "verses": "24.62",
            "translation": "Venus in the 10th house: The native will be liked by all, will perform virtuous deeds, be devoted to his preceptor, be intelligent, and will achieve fame.",
            "detailed_effects": [
                "Success in artistic, creative, or beauty-related careers",
                "Public recognition for taste, style, and refinement",
                "Career involving luxury goods, arts, entertainment, hospitality",
                "Diplomatic approach to professional matters",
                "Harmonious relationships with authority figures",
                "Government or public sector work involving culture/arts",
                "Fame through creative or aesthetic contributions",
                "Professional life enhances social standing"
            ],
            "positive_effects": [
                "Career success in Venusian fields (arts, beauty, luxury)",
                "Popularity and good reputation in profession",
                "Harmonious work environment",
                "Recognition for creative or diplomatic skills",
                "Financial prosperity through career",
                "May work with women or for women-centric industries"
            ],
            "challenging_effects": [
                "May prioritize popularity over hard work",
                "Career may lack discipline or structure",
                "Tendency to avoid conflict at professional cost"
            ],
            "remedies": [
                "Balance charm with competence",
                "Use creative talents for social benefit",
                "Maintain professional ethics in relationships"
            ],
            "life_areas": {
                "career": "Arts, entertainment, fashion, beauty, luxury goods, hospitality",
                "reputation": "Popular, admired for taste and refinement",
                "authority": "Diplomatic approach; harmonious with superiors"
            }
        },
        12: {
            "verses": "24.64",
            "translation": "Venus in the 12th house: The native will be deprived of happiness from his wife, will be bereft of good clothes and bed comforts, and be devoid of bodily pleasures.",
            "detailed_effects": [
                "Challenges in marriage; separation or distance from spouse possible",
                "Expenditure on luxuries and pleasures",
                "Foreign travel for pleasure or romantic pursuits",
                "Spiritual or artistic retreat beneficial",
                "Hidden romantic affairs or secret relationships",
                "Wealth spent on charitable or spiritual causes",
                "May find happiness in solitude or meditation",
                "Hospital, hotel, or spa work favorable"
            ],
            "positive_effects": [
                "Strong spiritual or artistic inclinations",
                "Success in foreign lands",
                "Charitable disposition toward women and arts",
                "Hidden talents in mystical or occult arts",
                "Liberation through renunciation of pleasures"
            ],
            "challenging_effects": [
                "Marital unhappiness or separation",
                "Excessive expenditure on pleasures",
                "Secret affairs may create complications",
                "Health issues related to reproductive system",
                "Financial losses through women or pleasures"
            ],
            "remedies": [
                "Practice detachment from material pleasures",
                "Channel Venusian energy into spiritual arts",
                "Support charitable causes for women",
                "Worship Goddess Lakshmi for marital harmony",
                "Consider celibacy or monastic life if inclined"
            ],
            "life_areas": {
                "marriage": "Challenges likely; may prefer solitude or spiritual life",
                "spirituality": "Strong inclination; artistic spiritual expression",
                "expenses": "High spending on pleasures, foreign travel, charity",
                "foreign": "Success or happiness in foreign lands"
            }
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
    },
    
    "Saturn": {
        1: {
            "verses": "24.66",
            "translation": "Saturn in the ascendant: The native will be indolent, lame, will have unclean habits, be foolish, and will suffer misery in old age.",
            "detailed_effects": [
                "Serious, disciplined, and responsible personality",
                "May appear older than actual age; mature demeanor",
                "Strong sense of duty and perseverance",
                "Challenges in early life build character",
                "Lean or thin body structure",
                "Reserved, introverted nature",
                "Late bloomer - success comes with time and effort",
                "Karmic lessons through self and identity",
                "Patient, enduring, and hardworking"
            ],
            "positive_effects": [
                "Exceptional discipline and work ethic",
                "Longevity and endurance",
                "Wisdom gained through hardship",
                "Success through sustained effort over time",
                "Spiritual maturity and detachment",
                "Leadership through responsibility and duty",
                "Respected for integrity and persistence"
            ],
            "challenging_effects": [
                "Chronic health issues or physical limitations",
                "Depression, pessimism, or melancholy",
                "Delays and obstacles in personal goals",
                "Difficulty with self-confidence in youth",
                "Separation or loneliness",
                "Early life hardships and struggles"
            ],
            "remedies": [
                "Practice patience and acceptance",
                "Serve the poor, elderly, and suffering",
                "Worship Lord Shani and Hanuman",
                "Donate black items or sesame on Saturdays",
                "Strengthen through discipline and meditation",
                "Accept delays as divine timing"
            ],
            "life_areas": {
                "personality": "Serious, disciplined, mature, responsible, reserved",
                "health": "Watch for chronic issues, joint problems, vitality",
                "life_path": "Success through perseverance; late bloomer",
                "spirituality": "Strong karmic lessons; spiritual growth through hardship"
            },
            "timing": "Difficulties in youth (up to age 36), improvement after Sade Sati completion. Saturn mahadasha brings karmic lessons."
        },
        7: {
            "verses": "24.72",
            "translation": "Saturn in the 7th house: The native will lose his wife, be poor, will suffer from tuberculosis or other disease, be distressed, and will wander aimlessly.",
            "detailed_effects": [
                "Delays in marriage; marries late in life",
                "Older spouse or significant age gap possible",
                "Spouse may be serious, mature, or karmic connection",
                "Challenges and lessons through marriage",
                "Business partnerships require patience",
                "Foreign spouse or marriage abroad possible",
                "Marital responsibilities feel heavy",
                "Separation or distance from spouse at times"
            ],
            "positive_effects": [
                "Mature, stable marriage when it occurs",
                "Spouse teaches important life lessons",
                "Long-lasting committed relationships",
                "Success in structured business partnerships",
                "Learns responsibility through relationships",
                "Foreign connections beneficial"
            ],
            "challenging_effects": [
                "Significant delays in marriage",
                "Marital unhappiness or separation possible",
                "Spouse may have health issues or be demanding",
                "Business partnership disputes",
                "Loneliness or isolation from partner",
                "Karmic debts through relationships"
            ],
            "remedies": [
                "Marry after age 28-30 for better results",
                "Practice patience and commitment in relationships",
                "Serve partner's needs selflessly",
                "Worship Saturn deities for marital harmony",
                "Accept marital responsibilities with maturity"
            ],
            "life_areas": {
                "marriage": "Delayed; older or karmic spouse; requires patience",
                "partnerships": "Structured, long-term business partnerships",
                "relationships": "Serious, committed; learns through challenges"
            }
        },
        10: {
            "verses": "24.75",
            "translation": "Saturn in the 10th house: The native will be happy, will have conveyances, be virtuous, intelligent, wealthy, bold, and will command men and wealth.",
            "detailed_effects": [
                "Excellent placement for career - one of Saturn's best positions",
                "Success through hard work, discipline, and perseverance",
                "Slow but steady rise in profession",
                "Authority and leadership through responsibility",
                "Government service, administration, or heavy industries favorable",
                "Long-term career stability and recognition",
                "Respect for integrity and work ethic",
                "Late career success brings lasting results"
            ],
            "positive_effects": [
                "Outstanding career achievement through sustained effort",
                "High positions of responsibility and authority",
                "Reputation for reliability and competence",
                "Success in Saturnian careers (engineering, mining, oil, government)",
                "Longevity in profession; career stability",
                "Recognition for discipline and hard work",
                "Able to handle pressure and long-term projects"
            ],
            "challenging_effects": [
                "Career progress is slow and requires patience",
                "Heavy workload and professional responsibilities",
                "May face obstacles from superiors initially",
                "Work-related stress and pressure",
                "Career success comes late in life"
            ],
            "remedies": [
                "Practice patience in career advancement",
                "Accept responsibility and work diligently",
                "Serve in positions helping the underprivileged",
                "Maintain professional ethics and integrity"
            ],
            "life_areas": {
                "career": "Engineering, government, administration, construction, mining, agriculture",
                "reputation": "Respected for discipline, reliability, integrity",
                "authority": "Gains authority through responsibility and proven competence",
                "timing": "Career peaks after age 36; sustained success"
            },
            "notable_yogas": [
                "Can form Sasa Yoga if Saturn in own sign or exaltation",
                "Strong for Karma Yoga - duty-based success",
                "Contributes to Dhana Yogas through 10th house strength"
            ]
        },
        12: {
            "verses": "24.77",
            "translation": "Saturn in the 12th house: The native will be defective-limbed, will spend without an aim, be stupid, will marry a barren woman, be childless, will help others, and will be insulted by others.",
            "detailed_effects": [
                "High expenditure often on necessary items",
                "Foreign travel or residence possible",
                "Isolated work environments (hospitals, prisons, retreats)",
                "Spiritual inclination through losses and detachment",
                "Hidden enemies or chronic health issues",
                "Sleep disturbances or eye problems",
                "Work in foreign lands beneficial",
                "Liberation through renunciation"
            ],
            "positive_effects": [
                "Strong spiritual growth through detachment",
                "Success in foreign countries",
                "Work in charitable institutions favorable",
                "Meditation and solitude beneficial",
                "Karmic completion and liberation",
                "Research or behind-the-scenes work"
            ],
            "challenging_effects": [
                "Chronic health issues or hospitalizations",
                "Financial losses or heavy expenditures",
                "Loneliness or separation from family",
                "Sleep disorders or anxiety",
                "Hidden obstacles and enemies",
                "Delayed or denied progeny"
            ],
            "remedies": [
                "Practice spiritual discipline and meditation",
                "Serve in hospitals, prisons, or ashrams",
                "Donate to charitable causes regularly",
                "Accept losses as karmic cleansing",
                "Worship Saturn deities for protection"
            ],
            "life_areas": {
                "spirituality": "Strong inclination; liberation through renunciation",
                "expenses": "High spending on health, foreign travel, charity",
                "foreign": "Success in foreign lands; possible settlement abroad",
                "health": "Watch for chronic issues, sleep problems"
            }
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
