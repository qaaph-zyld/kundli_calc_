"""
Dasha Interpretation Engine
============================
Generates natural language interpretations for dasha periods.
"""
from typing import Dict, List, Any
from datetime import datetime


class DashaInterpreter:
    """Generates interpretations for dasha periods"""
    
    # Mahadasha interpretations
    MAHADASHA_INTERPRETATIONS = {
        "Sun": {
            "general": "Period of self-expression, authority, and recognition. Focus on career advancement and leadership roles.",
            "positive": "Enhanced confidence, government favor, career success, spiritual inclination, and paternal blessings.",
            "challenges": "Ego conflicts, authority issues, health concerns (eyes, heart), and separation from father.",
            "advice": "Cultivate humility while pursuing ambitions. Practice meditation and serve authority figures.",
            "career": "Excellent for government service, politics, administration, and leadership positions.",
            "health": "Monitor heart, bones, eyes, and digestive system. Maintain regular routine.",
            "relationships": "May face challenges with authority figures. Good for establishing one's identity."
        },
        "Moon": {
            "general": "Period of emotional sensitivity, intuition, and nurturing. Focus on home, mother, and inner peace.",
            "positive": "Emotional fulfillment, good relationship with mother, popularity, creativity, and material gains.",
            "challenges": "Mood fluctuations, mental stress, health issues related to fluids, and dependency.",
            "advice": "Practice emotional balance through meditation. Maintain close family ties.",
            "career": "Favorable for hospitality, nursing, psychology, creative arts, and public-facing roles.",
            "health": "Monitor mental health, digestive system, and fluid balance. Avoid excessive worry.",
            "relationships": "Strong maternal connections. Enhanced empathy and relationship building."
        },
        "Mars": {
            "general": "Period of energy, courage, and action. Focus on competitive pursuits and physical activities.",
            "positive": "Courage, determination, property gains, success through effort, and sibling support.",
            "challenges": "Accidents, conflicts, impulsiveness, blood-related health issues, and legal problems.",
            "advice": "Channel energy constructively. Practice patience and avoid conflicts.",
            "career": "Good for military, sports, engineering, surgery, real estate, and entrepreneurship.",
            "health": "Monitor blood pressure, injuries, inflammations, and head-related issues.",
            "relationships": "May experience conflicts. Practice anger management and compromise."
        },
        "Mercury": {
            "general": "Period of intellect, communication, and business. Focus on learning and commercial activities.",
            "positive": "Enhanced intelligence, business success, education, communication skills, and networking.",
            "challenges": "Mental stress, nervous system issues, overthinking, and deception in business.",
            "advice": "Maintain clarity in communications. Practice discrimination in business dealings.",
            "career": "Excellent for education, writing, commerce, IT, consulting, and communication fields.",
            "health": "Monitor nervous system, respiratory system, and skin. Manage stress effectively.",
            "relationships": "Good communication but may lack emotional depth. Intellectual connections thrive."
        },
        "Jupiter": {
            "general": "Period of wisdom, expansion, and blessings. Focus on spirituality, education, and growth.",
            "positive": "Spiritual growth, education, wealth, children, wisdom, ethical success, and good fortune.",
            "challenges": "Over-optimism, weight gain, liver issues, and financial overextension.",
            "advice": "Seek knowledge and share wisdom. Practice generosity and ethical conduct.",
            "career": "Favorable for teaching, counseling, law, finance, religious work, and advisory roles.",
            "health": "Monitor liver, weight, and blood sugar. Maintain moderation in diet.",
            "relationships": "Harmonious relationships. Good for marriage and children. Teacher-student connections."
        },
        "Venus": {
            "general": "Period of luxury, love, and aesthetics. Focus on relationships, arts, and material comforts.",
            "positive": "Marriage, romance, artistic success, luxury items, beauty, and social popularity.",
            "challenges": "Relationship complications, materialism, reproductive health, and indulgence.",
            "advice": "Balance pleasure with responsibility. Cultivate refined tastes and healthy relationships.",
            "career": "Excellent for arts, fashion, entertainment, hospitality, jewelry, and beauty industries.",
            "health": "Monitor reproductive system, kidneys, and diabetes. Avoid excessive indulgence.",
            "relationships": "Prime time for romance and marriage. Enhanced social life and partnerships."
        },
        "Saturn": {
            "general": "Period of discipline, karma, and hard work. Focus on responsibility and long-term goals.",
            "positive": "Discipline, hard work pays off, spiritual maturity, service, and karmic resolution.",
            "challenges": "Delays, obstacles, depression, health issues, separation, and financial stress.",
            "advice": "Practice patience and persistence. Serve the needy and elderly. Accept delays as divine timing.",
            "career": "Success through sustained effort. Good for labor-intensive work, mining, and service industries.",
            "health": "Monitor bones, teeth, joints, and chronic conditions. Maintain regular health checks.",
            "relationships": "May experience separations or delays. Focus on duty and long-term commitments."
        },
        "Rahu": {
            "general": "Period of ambition, innovation, and unconventional paths. Focus on material gains and foreign connections.",
            "positive": "Sudden gains, foreign travel, technology success, political connections, and material prosperity.",
            "challenges": "Confusion, deception, addictions, enemies, legal troubles, and health mysteries.",
            "advice": "Maintain ethical standards. Avoid shortcuts and speculative ventures. Practice grounding techniques.",
            "career": "Favorable for technology, politics, foreign trade, research, and unconventional fields.",
            "health": "Monitor skin conditions, allergies, mysterious illnesses, and mental health.",
            "relationships": "Unconventional relationships. May face deception. Practice discernment."
        },
        "Ketu": {
            "general": "Period of spirituality, detachment, and liberation. Focus on inner growth and letting go.",
            "positive": "Spiritual enlightenment, intuition, occult knowledge, detachment, and karmic release.",
            "challenges": "Losses, confusion, health issues, separation, accidents, and lack of direction.",
            "advice": "Embrace spirituality. Practice detachment without neglecting duties. Seek spiritual guidance.",
            "career": "Good for spiritual work, research, occult sciences, and solitary pursuits.",
            "health": "Monitor nervous system, mysterious ailments, and injuries. Practice grounding.",
            "relationships": "Tendency toward isolation. May experience separations. Focus on spiritual connections."
        }
    }
    
    @classmethod
    def interpret_mahadasha(cls, planet: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Generate interpretation for a mahadasha period
        
        Args:
            planet: Mahadasha planet name
            start_date: Start date of mahadasha
            end_date: End date of mahadasha
            
        Returns:
            Comprehensive interpretation dictionary
        """
        template = cls.MAHADASHA_INTERPRETATIONS.get(planet, {})
        
        if not template:
            return {
                "planet": planet,
                "duration": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                "general": f"{planet} mahadasha period - consult classical texts for specific interpretations",
                "advice": "Strengthen this planet through appropriate remedies and ethical living"
            }
        
        duration_years = (end_date - start_date).days / 365.25
        
        return {
            "planet": planet,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "duration_years": round(duration_years, 1),
            "general_influence": template.get("general", ""),
            "positive_effects": template.get("positive", ""),
            "potential_challenges": template.get("challenges", ""),
            "recommended_actions": template.get("advice", ""),
            "career_impact": template.get("career", ""),
            "health_considerations": template.get("health", ""),
            "relationship_dynamics": template.get("relationships", "")
        }
    
    @classmethod
    def get_current_period_guidance(cls, mahadasha: str, antardasha: str) -> str:
        """
        Get specific guidance for current dasha combination
        
        Args:
            mahadasha: Current mahadasha planet
            antardasha: Current antardasha planet
            
        Returns:
            Guidance string
        """
        maha_influence = cls.MAHADASHA_INTERPRETATIONS.get(mahadasha, {}).get("general", "")
        antar_influence = cls.MAHADASHA_INTERPRETATIONS.get(antardasha, {}).get("general", "")
        
        if not maha_influence or not antar_influence:
            return f"Current period: {mahadasha} Mahadasha, {antardasha} Antardasha. The overall tone is set by {mahadasha} with {antardasha} sub-influences."
        
        return f"You are in {mahadasha} Mahadasha ({maha_influence[:50]}...) with {antardasha} Antardasha sub-period ({antar_influence[:50]}...). The combination creates a unique influence where {mahadasha}'s overall themes are colored by {antardasha}'s specific energies."
