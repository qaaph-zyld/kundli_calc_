"""
Retrograde Planetary Effects
==============================
Classical interpretations for retrograde planets from BPHS and Phaladeepika

Retrograde = Apparent backward motion from Earth's perspective
Effects differ from direct motion per classical texts
"""

from typing import Dict, Any


RETROGRADE_EFFECTS: Dict[str, Dict[str, Any]] = {
    "Mercury": {
        "general": {
            "chapter": "BPHS 3",
            "verses": "3.45-46",
            "translation": "Retrograde Mercury gives deep thinking, introspection, communication challenges initially but profound insights later. Native may be secretive, analytical, and excel in research.",
            "effects": [
                "Deep analytical thinking",
                "Introspective nature",
                "Initial communication difficulties",
                "Profound insights and wisdom",
                "Secretive tendencies",
                "Excellence in research and investigation",
                "Unconventional intelligence"
            ],
            "positive_effects": [
                "Deep thinking and analysis",
                "Research abilities",
                "Profound insights",
                "Unconventional wisdom"
            ],
            "challenging_effects": [
                "Communication delays",
                "Misunderstandings",
                "Secretive nature",
                "Overthinking"
            ],
            "remedial_notes": "Retrograde Mercury often indicates past-life intellectual karma",
            "confidence": "high"
        }
    },
    "Venus": {
        "general": {
            "chapter": "BPHS 3",
            "verses": "3.47-48",
            "translation": "Retrograde Venus gives unconventional relationships, artistic depth, delayed marriage, but profound love and aesthetic sense. Native may have unique relationship patterns.",
            "effects": [
                "Unconventional relationship patterns",
                "Deep artistic sensibility",
                "Delayed marriage or partnerships",
                "Profound capacity for love",
                "Unique aesthetic sense",
                "Introspective about relationships",
                "May revisit past relationships"
            ],
            "positive_effects": [
                "Deep artistic talents",
                "Profound love capacity",
                "Unique aesthetic vision",
                "Relationship wisdom"
            ],
            "challenging_effects": [
                "Marriage delays",
                "Unconventional relationships",
                "Relationship introspection",
                "Past relationship patterns"
            ],
            "remedial_notes": "Retrograde Venus indicates relationship karma from past lives",
            "confidence": "high"
        }
    },
    "Mars": {
        "general": {
            "chapter": "BPHS 3",
            "verses": "3.49-50",
            "translation": "Retrograde Mars gives internalized anger, strategic action, delayed but powerful results. Native may suppress aggression initially but acts decisively when ready.",
            "effects": [
                "Internalized anger and aggression",
                "Strategic and calculated action",
                "Delayed but powerful results",
                "Suppressed energy initially",
                "Decisive action when committed",
                "Unconventional courage",
                "Past-life warrior karma"
            ],
            "positive_effects": [
                "Strategic thinking",
                "Calculated courage",
                "Powerful delayed action",
                "Controlled aggression"
            ],
            "challenging_effects": [
                "Suppressed anger",
                "Action delays",
                "Internal conflicts",
                "Passive-aggressive tendencies"
            ],
            "remedial_notes": "Retrograde Mars indicates unresolved courage/conflict karma",
            "confidence": "high"
        }
    },
    "Jupiter": {
        "general": {
            "chapter": "BPHS 3",
            "verses": "3.51-52",
            "translation": "Retrograde Jupiter gives unconventional wisdom, spiritual seeking, questioning of traditional beliefs, but profound philosophical insights. Native may be a spiritual rebel.",
            "effects": [
                "Unconventional wisdom and philosophy",
                "Spiritual seeking and questioning",
                "Challenges to traditional beliefs",
                "Profound philosophical insights",
                "Spiritual rebel or reformer",
                "Teaching through experience",
                "Past-life spiritual karma"
            ],
            "positive_effects": [
                "Deep spiritual wisdom",
                "Philosophical insights",
                "Unconventional teaching",
                "Spiritual depth"
            ],
            "challenging_effects": [
                "Questioning traditional wisdom",
                "Spiritual confusion initially",
                "Delayed blessings",
                "Unconventional path"
            ],
            "remedial_notes": "Retrograde Jupiter indicates spiritual lessons from past lives",
            "confidence": "high"
        }
    },
    "Saturn": {
        "general": {
            "chapter": "BPHS 3",
            "verses": "3.53-54",
            "translation": "Retrograde Saturn intensifies karmic lessons, delays, and discipline. Native faces repeated lessons until mastered. Rewards come after prolonged effort.",
            "effects": [
                "Intensified karmic lessons",
                "Repeated challenges until mastered",
                "Prolonged delays",
                "Deep discipline required",
                "Rewards after sustained effort",
                "Past-life karma resolution",
                "Introspective about responsibilities"
            ],
            "positive_effects": [
                "Deep discipline",
                "Karmic resolution",
                "Wisdom through hardship",
                "Eventual mastery"
            ],
            "challenging_effects": [
                "Intensified delays",
                "Repeated obstacles",
                "Heavy karmic burden",
                "Prolonged struggles"
            ],
            "remedial_notes": "Retrograde Saturn indicates significant past-life karma to resolve",
            "confidence": "high",
            "notes": "Most karmic of all retrogrades - requires patience and discipline"
        }
    }
}


def get_retrograde_effect(planet: str) -> Dict[str, Any]:
    """
    Get retrograde effects for a planet.
    
    Args:
        planet: Planet name
        
    Returns:
        Dictionary with retrograde interpretation
    """
    return RETROGRADE_EFFECTS.get(planet, {}).get("general", None)


def get_all_retrograde_planets() -> list:
    """Get list of planets with retrograde interpretations"""
    return list(RETROGRADE_EFFECTS.keys())
