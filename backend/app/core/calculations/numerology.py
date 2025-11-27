"""
Vedic Numerology System
PGF Protocol: NUMER_001
Gate: GATE_5
Version: 1.0.0

Implements:
1. Birth Number (Moolank)
2. Destiny Number (Bhagyank)
3. Name Number (Namank)
4. Soul Number
5. Personality Number
6. Lucky Numbers
7. Compatibility Analysis
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime


@dataclass
class NumerologyResult:
    """Result of numerology analysis"""
    number: int
    name: str
    ruling_planet: str
    characteristics: List[str]
    strengths: List[str]
    challenges: List[str]
    lucky_colors: List[str]
    lucky_days: List[str]


class VedicNumerology:
    """
    Vedic Numerology Calculator
    
    Based on the connection between numbers and planets:
    1 - Sun
    2 - Moon
    3 - Jupiter
    4 - Rahu (Uranus in Western)
    5 - Mercury
    6 - Venus
    7 - Ketu (Neptune in Western)
    8 - Saturn
    9 - Mars
    """
    
    NUMBER_PLANETS = {
        1: "Sun",
        2: "Moon",
        3: "Jupiter",
        4: "Rahu",
        5: "Mercury",
        6: "Venus",
        7: "Ketu",
        8: "Saturn",
        9: "Mars"
    }
    
    NUMBER_CHARACTERISTICS = {
        1: {
            "name": "The Leader",
            "characteristics": [
                "Leadership qualities", "Independence", "Originality",
                "Ambition", "Determination", "Creative force"
            ],
            "strengths": ["Initiative", "Self-confidence", "Willpower"],
            "challenges": ["Stubbornness", "Ego", "Impatience"],
            "colors": ["Gold", "Yellow", "Orange"],
            "days": ["Sunday"]
        },
        2: {
            "name": "The Diplomat",
            "characteristics": [
                "Cooperation", "Sensitivity", "Balance",
                "Intuition", "Adaptability", "Receptivity"
            ],
            "strengths": ["Diplomacy", "Patience", "Empathy"],
            "challenges": ["Indecision", "Over-sensitivity", "Dependency"],
            "colors": ["White", "Silver", "Light green"],
            "days": ["Monday"]
        },
        3: {
            "name": "The Communicator",
            "characteristics": [
                "Expression", "Creativity", "Optimism",
                "Sociability", "Joy", "Inspiration"
            ],
            "strengths": ["Creativity", "Communication", "Enthusiasm"],
            "challenges": ["Scattered energy", "Superficiality", "Over-indulgence"],
            "colors": ["Yellow", "Purple", "Orange"],
            "days": ["Thursday"]
        },
        4: {
            "name": "The Builder",
            "characteristics": [
                "Stability", "Hard work", "Practicality",
                "Discipline", "Order", "Foundation"
            ],
            "strengths": ["Organization", "Dedication", "Reliability"],
            "challenges": ["Rigidity", "Stubbornness", "Limitation"],
            "colors": ["Grey", "Blue", "Electric blue"],
            "days": ["Saturday", "Sunday"]
        },
        5: {
            "name": "The Freedom Seeker",
            "characteristics": [
                "Change", "Freedom", "Versatility",
                "Adventure", "Curiosity", "Adaptability"
            ],
            "strengths": ["Adaptability", "Intelligence", "Resourcefulness"],
            "challenges": ["Restlessness", "Inconsistency", "Excess"],
            "colors": ["Green", "Light grey", "White"],
            "days": ["Wednesday"]
        },
        6: {
            "name": "The Nurturer",
            "characteristics": [
                "Love", "Responsibility", "Beauty",
                "Harmony", "Family", "Service"
            ],
            "strengths": ["Compassion", "Responsibility", "Artistic sense"],
            "challenges": ["Self-sacrifice", "Perfectionism", "Worry"],
            "colors": ["Blue", "Pink", "Pastel colors"],
            "days": ["Friday"]
        },
        7: {
            "name": "The Seeker",
            "characteristics": [
                "Spirituality", "Wisdom", "Analysis",
                "Intuition", "Mystery", "Introspection"
            ],
            "strengths": ["Wisdom", "Intuition", "Analytical mind"],
            "challenges": ["Isolation", "Skepticism", "Secrecy"],
            "colors": ["Grey", "Light green", "White"],
            "days": ["Monday"]
        },
        8: {
            "name": "The Powerhouse",
            "characteristics": [
                "Power", "Authority", "Material success",
                "Karma", "Justice", "Achievement"
            ],
            "strengths": ["Business acumen", "Authority", "Efficiency"],
            "challenges": ["Materialism", "Control issues", "Workaholism"],
            "colors": ["Black", "Dark blue", "Grey"],
            "days": ["Saturday"]
        },
        9: {
            "name": "The Humanitarian",
            "characteristics": [
                "Compassion", "Idealism", "Completion",
                "Universal love", "Wisdom", "Service"
            ],
            "strengths": ["Generosity", "Idealism", "Broad vision"],
            "challenges": ["Self-sacrifice", "Emotional extremes", "Impracticality"],
            "colors": ["Red", "Pink", "Coral"],
            "days": ["Tuesday"]
        }
    }
    
    # Chaldean numerology letter values
    CHALDEAN_VALUES = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5,
        'I': 1, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8,
        'Q': 1, 'R': 2, 'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5,
        'Y': 1, 'Z': 7
    }
    
    # Pythagorean numerology letter values
    PYTHAGOREAN_VALUES = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
        'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7,
        'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6,
        'Y': 7, 'Z': 8
    }
    
    VOWELS = set('AEIOU')
    
    def __init__(self, system: str = "pythagorean"):
        self.system = system
        self.letter_values = (
            self.PYTHAGOREAN_VALUES if system == "pythagorean"
            else self.CHALDEAN_VALUES
        )
    
    def reduce_to_single(self, number: int) -> int:
        """Reduce a number to single digit (1-9) or master number (11, 22, 33)"""
        while number > 9 and number not in [11, 22, 33]:
            number = sum(int(d) for d in str(number))
        return number
    
    def calculate_birth_number(self, day: int) -> NumerologyResult:
        """
        Calculate Birth Number (Moolank)
        
        Birth number = Day of birth reduced to single digit
        """
        birth_num = self.reduce_to_single(day)
        # Handle master numbers by using their root
        lookup_num = birth_num if birth_num <= 9 else self.reduce_to_single(sum(int(d) for d in str(birth_num)))
        info = self.NUMBER_CHARACTERISTICS[lookup_num]
        
        return NumerologyResult(
            number=birth_num,
            name=info["name"],
            ruling_planet=self.NUMBER_PLANETS.get(lookup_num, "Multiple"),
            characteristics=info["characteristics"],
            strengths=info["strengths"],
            challenges=info["challenges"],
            lucky_colors=info["colors"],
            lucky_days=info["days"]
        )
    
    def calculate_destiny_number(
        self,
        day: int,
        month: int,
        year: int
    ) -> NumerologyResult:
        """
        Calculate Destiny Number (Bhagyank)
        
        Destiny number = Full birth date reduced to single digit
        """
        total = day + month + sum(int(d) for d in str(year))
        destiny_num = self.reduce_to_single(total)
        lookup_num = destiny_num if destiny_num <= 9 else self.reduce_to_single(sum(int(d) for d in str(destiny_num)))
        info = self.NUMBER_CHARACTERISTICS[lookup_num]
        
        return NumerologyResult(
            number=destiny_num,
            name=info["name"],
            ruling_planet=self.NUMBER_PLANETS.get(lookup_num, "Multiple"),
            characteristics=info["characteristics"],
            strengths=info["strengths"],
            challenges=info["challenges"],
            lucky_colors=info["colors"],
            lucky_days=info["days"]
        )
    
    def calculate_name_number(self, name: str) -> NumerologyResult:
        """
        Calculate Name Number (Namank)
        
        Name number = Sum of letter values reduced to single digit
        """
        name = name.upper().replace(" ", "")
        total = sum(self.letter_values.get(c, 0) for c in name)
        name_num = self.reduce_to_single(total)
        lookup_num = name_num if name_num <= 9 else self.reduce_to_single(sum(int(d) for d in str(name_num)))
        info = self.NUMBER_CHARACTERISTICS[lookup_num]
        
        return NumerologyResult(
            number=name_num,
            name=info["name"],
            ruling_planet=self.NUMBER_PLANETS.get(lookup_num, "Multiple"),
            characteristics=info["characteristics"],
            strengths=info["strengths"],
            challenges=info["challenges"],
            lucky_colors=info["colors"],
            lucky_days=info["days"]
        )
    
    def calculate_soul_number(self, name: str) -> NumerologyResult:
        """
        Calculate Soul Number (from vowels only)
        
        Represents inner desires and motivations
        """
        name = name.upper().replace(" ", "")
        vowel_total = sum(
            self.letter_values.get(c, 0) for c in name if c in self.VOWELS
        )
        soul_num = self.reduce_to_single(vowel_total) if vowel_total > 0 else 1
        lookup_num = soul_num if soul_num <= 9 else self.reduce_to_single(sum(int(d) for d in str(soul_num)))
        info = self.NUMBER_CHARACTERISTICS[lookup_num]
        
        return NumerologyResult(
            number=soul_num,
            name=info["name"],
            ruling_planet=self.NUMBER_PLANETS.get(lookup_num, "Multiple"),
            characteristics=info["characteristics"],
            strengths=info["strengths"],
            challenges=info["challenges"],
            lucky_colors=info["colors"],
            lucky_days=info["days"]
        )
    
    def calculate_personality_number(self, name: str) -> NumerologyResult:
        """
        Calculate Personality Number (from consonants only)
        
        Represents outer personality and how others see you
        """
        name = name.upper().replace(" ", "")
        consonant_total = sum(
            self.letter_values.get(c, 0) for c in name if c not in self.VOWELS and c.isalpha()
        )
        pers_num = self.reduce_to_single(consonant_total) if consonant_total > 0 else 1
        lookup_num = pers_num if pers_num <= 9 else self.reduce_to_single(sum(int(d) for d in str(pers_num)))
        info = self.NUMBER_CHARACTERISTICS[lookup_num]
        
        return NumerologyResult(
            number=pers_num,
            name=info["name"],
            ruling_planet=self.NUMBER_PLANETS.get(lookup_num, "Multiple"),
            characteristics=info["characteristics"],
            strengths=info["strengths"],
            challenges=info["challenges"],
            lucky_colors=info["colors"],
            lucky_days=info["days"]
        )
    
    def calculate_lucky_numbers(
        self,
        birth_number: int,
        destiny_number: int
    ) -> Dict[str, Any]:
        """
        Calculate lucky numbers based on birth and destiny numbers
        """
        # Normalize master numbers for lookup
        birth_lookup = birth_number if birth_number <= 9 else self.reduce_to_single(sum(int(d) for d in str(birth_number)))
        destiny_lookup = destiny_number if destiny_number <= 9 else self.reduce_to_single(sum(int(d) for d in str(destiny_number)))
        
        # Primary lucky numbers
        primary = [birth_number, destiny_number]
        
        # Friendly numbers
        friendly_map = {
            1: [1, 2, 3, 9],
            2: [1, 2, 7],
            3: [1, 3, 6, 9],
            4: [1, 4, 5, 7],
            5: [1, 4, 5, 6, 8],
            6: [3, 5, 6, 9],
            7: [2, 4, 7],
            8: [5, 8],
            9: [1, 3, 6, 9]
        }
        
        friendly = set(friendly_map.get(birth_lookup, [])) | set(friendly_map.get(destiny_lookup, []))
        
        # Calculate compound lucky numbers
        compound = [birth_lookup * 10 + d for d in range(10) if self.reduce_to_single(birth_lookup * 10 + d) in friendly][:3]
        
        return {
            "primary": list(set(primary)),
            "friendly": list(friendly),
            "compound": compound,
            "avoid": [n for n in range(1, 10) if n not in friendly]
        }
    
    def check_compatibility(
        self,
        person1_birth: int,
        person2_birth: int
    ) -> Dict[str, Any]:
        """
        Check numerology compatibility between two people
        """
        compatibility_matrix = {
            (1, 1): 80, (1, 2): 60, (1, 3): 90, (1, 4): 50, (1, 5): 70,
            (1, 6): 60, (1, 7): 50, (1, 8): 40, (1, 9): 90,
            (2, 2): 70, (2, 3): 60, (2, 4): 50, (2, 5): 60,
            (2, 6): 60, (2, 7): 90, (2, 8): 40, (2, 9): 70,
            (3, 3): 80, (3, 4): 50, (3, 5): 70, (3, 6): 90,
            (3, 7): 50, (3, 8): 60, (3, 9): 90,
            (4, 4): 70, (4, 5): 80, (4, 6): 60, (4, 7): 80,
            (4, 8): 70, (4, 9): 50,
            (5, 5): 80, (5, 6): 80, (5, 7): 60, (5, 8): 90, (5, 9): 70,
            (6, 6): 80, (6, 7): 50, (6, 8): 70, (6, 9): 90,
            (7, 7): 80, (7, 8): 60, (7, 9): 50,
            (8, 8): 70, (8, 9): 60,
            (9, 9): 80
        }
        
        key = tuple(sorted([person1_birth, person2_birth]))
        score = compatibility_matrix.get(key, 50)
        
        if score >= 80:
            verdict = "Excellent compatibility"
        elif score >= 60:
            verdict = "Good compatibility"
        elif score >= 50:
            verdict = "Average compatibility"
        else:
            verdict = "Challenging compatibility"
        
        return {
            "person1_number": person1_birth,
            "person2_number": person2_birth,
            "score": score,
            "verdict": verdict
        }
    
    def full_analysis(
        self,
        name: str,
        day: int,
        month: int,
        year: int
    ) -> Dict[str, Any]:
        """
        Complete numerology analysis
        """
        birth = self.calculate_birth_number(day)
        destiny = self.calculate_destiny_number(day, month, year)
        name_num = self.calculate_name_number(name)
        soul = self.calculate_soul_number(name)
        personality = self.calculate_personality_number(name)
        lucky = self.calculate_lucky_numbers(birth.number, destiny.number)
        
        return {
            "name": name,
            "birth_date": f"{day}/{month}/{year}",
            "birth_number": {
                "number": birth.number,
                "name": birth.name,
                "planet": birth.ruling_planet,
                "characteristics": birth.characteristics
            },
            "destiny_number": {
                "number": destiny.number,
                "name": destiny.name,
                "planet": destiny.ruling_planet,
                "characteristics": destiny.characteristics
            },
            "name_number": {
                "number": name_num.number,
                "name": name_num.name,
                "planet": name_num.ruling_planet
            },
            "soul_number": {
                "number": soul.number,
                "name": soul.name,
                "interpretation": "Inner desires and motivations"
            },
            "personality_number": {
                "number": personality.number,
                "name": personality.name,
                "interpretation": "How others perceive you"
            },
            "lucky_numbers": lucky,
            "lucky_colors": list(set(birth.lucky_colors + destiny.lucky_colors)),
            "lucky_days": list(set(birth.lucky_days + destiny.lucky_days)),
            "strengths": birth.strengths,
            "challenges": birth.challenges
        }


def calculate_numerology(
    name: str,
    day: int,
    month: int,
    year: int,
    system: str = "pythagorean"
) -> Dict[str, Any]:
    """Convenience function for numerology calculation"""
    calc = VedicNumerology(system)
    return calc.full_analysis(name, day, month, year)
