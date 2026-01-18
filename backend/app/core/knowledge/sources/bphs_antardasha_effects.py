"""
BPHS: Antardasha Effects
=========================
Digitized antardasha (sub-period) effects from BPHS
Chapters 47-48: Detailed dasha-antardasha combinations

Translation: R. Santhanam (1984)

Antardasha = Sub-period within mahadasha
Example: Sun mahadasha → Moon antardasha (specific 6-month period)
"""

from typing import Any, Dict

BPHS_ANTARDASHA_EFFECTS: Dict[str, Dict[str, Dict[str, Any]]] = {
    "Sun": {
        "Sun": {
            "chapter": 47,
            "verses": "47.10-11",
            "translation": "During Sun-Sun period, the native gains authority, recognition from government, success in endeavors, but may face ego conflicts and health issues related to heat.",
            "effects": {
                "career": "Peak authority and recognition, government favor",
                "health": "Strong vitality but watch for fever, bile issues, eye strain",
                "relationships": "Commanding presence may strain relationships",
                "wealth": "Gains through authority positions",
                "timing": "Peak manifestation of Sun's natal promise",
            },
            "positive_manifestations": [
                "Authority and power peak",
                "Government recognition",
                "Leadership opportunities",
                "Confidence and self-esteem high",
            ],
            "challenging_manifestations": [
                "Ego conflicts",
                "Health issues from heat/bile",
                "Strained relationships due to dominance",
            ],
            "duration_months": 3.6,
            "confidence": "high",
        },
        "Moon": {
            "chapter": 47,
            "verses": "47.12-13",
            "translation": "Sun-Moon antardasha brings emotional balance to authority, gains from mother or women, public popularity, but mental fluctuations.",
            "effects": {
                "career": "Public-facing roles successful, popularity increases",
                "health": "Emotional health important, digestive balance needed",
                "relationships": "Mother's influence positive, emotional connections",
                "wealth": "Gains from public, women, or mother's side",
                "timing": "Balances Sun's authority with emotional intelligence",
            },
            "positive_manifestations": [
                "Public popularity",
                "Mother's blessings",
                "Emotional balance in leadership",
                "Gains from public",
            ],
            "challenging_manifestations": [
                "Mental fluctuations",
                "Emotional stress from authority",
                "Digestive issues",
            ],
            "duration_months": 6.0,
            "confidence": "high",
        },
        "Mars": {
            "chapter": 47,
            "verses": "47.14-15",
            "translation": "Sun-Mars period gives courage, victory over enemies, property gains, but also conflicts, accidents, and aggression.",
            "effects": {
                "career": "Bold career moves, competitive success, military/police favor",
                "health": "High energy but prone to accidents, fever, injuries",
                "relationships": "Conflicts with siblings, aggressive communication",
                "wealth": "Property and land gains, competitive earnings",
                "timing": "Action-oriented period with both gains and conflicts",
            },
            "positive_manifestations": [
                "Courage and valor peak",
                "Victory over enemies",
                "Property acquisition",
                "Competitive success",
            ],
            "challenging_manifestations": [
                "Accidents and injuries",
                "Conflicts and disputes",
                "Aggressive behavior",
                "Blood-related health issues",
            ],
            "duration_months": 4.2,
            "confidence": "high",
        },
        "Jupiter": {
            "chapter": 47,
            "verses": "47.20-21",
            "translation": "Sun-Jupiter antardasha brings wisdom, fortune, children's happiness, spiritual growth, and righteous success.",
            "effects": {
                "career": "Ethical success, teaching/counseling roles, recognition for wisdom",
                "health": "Generally good, watch for liver if excessive",
                "relationships": "Children's welfare, guru's grace, elder's blessings",
                "wealth": "Wealth through righteous means, property, gold",
                "timing": "Highly auspicious period combining authority with wisdom",
            },
            "positive_manifestations": [
                "Wisdom and knowledge expansion",
                "Children's happiness",
                "Fortune and blessings",
                "Spiritual growth",
                "Ethical success",
            ],
            "challenging_manifestations": ["Over-optimism", "Weight gain if excessive"],
            "duration_months": 9.6,
            "confidence": "high",
            "notes": "One of the most auspicious antardasha combinations",
        },
        "Venus": {
            "chapter": 47,
            "verses": "47.24-25",
            "translation": "Sun-Venus period brings artistic success, romance, luxury, vehicles, but may cause ego-desire conflicts.",
            "effects": {
                "career": "Success in arts, entertainment, luxury goods, diplomacy",
                "health": "Generally good, watch for reproductive system",
                "relationships": "Romance flourishes, marriage possible, artistic partnerships",
                "wealth": "Gains from arts, beauty industry, luxury items, vehicles",
                "timing": "Balances authority with pleasure and aesthetics",
            },
            "positive_manifestations": [
                "Artistic success",
                "Romance and love",
                "Luxury and comforts",
                "Vehicle acquisition",
                "Aesthetic refinement",
            ],
            "challenging_manifestations": [
                "Ego-desire conflicts",
                "Over-indulgence in pleasures",
                "Authority vs relationship balance",
            ],
            "duration_months": 12.0,
            "confidence": "high",
        },
    },
    "Jupiter": {
        "Jupiter": {
            "chapter": 48,
            "verses": "48.15-16",
            "translation": "Jupiter-Jupiter period is highly auspicious bringing wisdom, wealth, children, spiritual growth, and fortune. Peak manifestation of Jupiter's blessings.",
            "effects": {
                "career": "Teaching, counseling, advisory roles peak, recognition for wisdom",
                "health": "Generally excellent, watch for weight gain, liver, diabetes",
                "relationships": "Marriage if unmarried, children born, guru's grace",
                "wealth": "Wealth expansion, property, gold, ethical earnings peak",
                "timing": "Most auspicious period of Jupiter mahadasha",
            },
            "positive_manifestations": [
                "Wisdom and knowledge peak",
                "Wealth accumulation maximum",
                "Children born or children's success",
                "Spiritual awakening",
                "Fortune and blessings abundant",
                "Marriage if unmarried",
            ],
            "challenging_manifestations": [
                "Over-optimism leading to poor decisions",
                "Weight gain and obesity",
                "Liver issues if excessive",
                "Complacency",
            ],
            "duration_months": 25.6,
            "confidence": "high",
            "notes": "Peak period for Jupiter's blessings - marriage, children, wealth",
        },
        "Saturn": {
            "chapter": 48,
            "verses": "48.20-21",
            "translation": "Jupiter-Saturn period brings disciplined wisdom, long-term planning success, property through effort, but delays and obstacles test patience.",
            "effects": {
                "career": "Structured growth, organizational success, long-term projects",
                "health": "Generally stable, watch for joint pain, chronic issues",
                "relationships": "Serious commitments, responsibility to elders, delays in marriage",
                "wealth": "Slow but steady accumulation, property through persistence",
                "timing": "Tests patience but rewards discipline",
            },
            "positive_manifestations": [
                "Disciplined wisdom",
                "Long-term success",
                "Property through effort",
                "Organizational skills",
                "Karmic rewards",
            ],
            "challenging_manifestations": [
                "Delays and obstacles",
                "Heavy responsibilities",
                "Pessimism",
                "Chronic health issues",
                "Separation from loved ones",
            ],
            "duration_months": 30.4,
            "confidence": "high",
            "notes": "Combines Jupiter's wisdom with Saturn's discipline",
        },
    },
}
