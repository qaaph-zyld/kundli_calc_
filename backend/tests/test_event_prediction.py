"""
Tests for Event Prediction Engine
"""

import pytest
from backend.app.core.timing.event_prediction_engine import (
    EventPredictionEngine,
    EventPrediction
)


class TestEventPrediction:
    
    def test_engine_initialization(self):
        """Test event prediction engine initializes"""
        engine = EventPredictionEngine()
        assert engine is not None
        assert engine.career_engine is not None
    
    def test_career_breakthrough_strong_promise(self):
        """Test career breakthrough with strong natal promise"""
        engine = EventPredictionEngine()
        
        chart_data = {
            "planets": {
                "Sun": {"house": 10, "sign": "Aries", "dignity": "exalted"},
                "Saturn": {"house": 6, "sign": "Capricorn", "dignity": "own_sign"},
                "Mercury": {"house": 2, "sign": "Gemini", "dignity": "own_sign"}
            },
            "house_lords": {10: "Sun", 6: "Saturn", 2: "Mercury"},
            "active_yogas": ["Dharma_Karma_Adhipati_Yoga", "Raja_Yoga"]
        }
        
        result = engine.predict_career_breakthrough(chart_data)
        
        assert result.event_type == "career_breakthrough"
        assert result.event_possible is True
        assert result.natal_promise_strength >= 60
        assert len(result.timing_windows) > 0
        assert result.confidence >= 50
    
    def test_marriage_prediction(self):
        """Test marriage timing prediction"""
        engine = EventPredictionEngine()
        
        chart_data = {
            "planets": {
                "Venus": {"house": 7, "sign": "Pisces", "dignity": "exalted"},
                "Jupiter": {"house": 11, "sign": "Sagittarius", "dignity": "own_sign"}
            },
            "house_lords": {7: "Venus", 2: "Mercury", 11: "Jupiter"},
            "active_yogas": []
        }
        
        result = engine.predict_marriage(chart_data)
        
        assert result.event_type == "marriage"
        assert result.natal_promise_strength > 0
        assert isinstance(result.timing_windows, list)
        assert len(result.recommendations) > 0
    
    def test_wealth_gain_prediction(self):
        """Test wealth gain prediction"""
        engine = EventPredictionEngine()
        
        chart_data = {
            "planets": {
                "Jupiter": {"house": 2, "sign": "Sagittarius", "dignity": "own_sign"},
                "Venus": {"house": 11, "sign": "Taurus", "dignity": "own_sign"}
            },
            "house_lords": {2: "Jupiter", 11: "Venus", 5: "Mercury", 9: "Mars"},
            "active_yogas": ["Dhana_Yoga", "Lakshmi_Yoga"]
        }
        
        result = engine.predict_wealth_gain(chart_data)
        
        assert result.event_type == "wealth_gain"
        assert result.event_possible is True
        assert result.natal_promise_strength >= 60
        assert len(result.timing_windows) > 0
    
    def test_weak_natal_promise(self):
        """Test event with weak natal promise"""
        engine = EventPredictionEngine()
        
        chart_data = {
            "planets": {
                "Sun": {"house": 12, "sign": "Libra", "dignity": "debilitated"},
                "Saturn": {"house": 8, "sign": "Aries", "dignity": "debilitated"}
            },
            "house_lords": {10: "Mars", 6: "Venus", 2: "Moon"},
            "active_yogas": []
        }
        
        result = engine.predict_career_breakthrough(chart_data)
        
        assert result.event_possible is False
        assert result.natal_promise_strength < 40
        assert "Weak natal indication" in result.synthesis
    
    def test_timing_window_generation(self):
        """Test timing window generation"""
        engine = EventPredictionEngine()
        
        chart_data = {
            "planets": {
                "Venus": {"house": 7, "sign": "Libra", "dignity": "own_sign"},
                "Jupiter": {"house": 9, "sign": "Sagittarius", "dignity": "own_sign"}
            },
            "house_lords": {7: "Venus", 2: "Mercury", 11: "Jupiter"},
            "active_yogas": []
        }
        
        result = engine.predict_marriage(chart_data)
        
        if result.timing_windows:
            window = result.timing_windows[0]
            assert window.period is not None
            assert 0 <= window.confidence <= 100
            assert window.likelihood in ["very_high", "high", "moderate", "low"]
            assert len(window.triggers) > 0
    
    def test_confidence_scoring(self):
        """Test confidence scoring validation"""
        engine = EventPredictionEngine()
        
        # Strong chart
        strong_chart = {
            "planets": {
                "Jupiter": {"house": 2, "sign": "Sagittarius", "dignity": "own_sign"},
                "Venus": {"house": 11, "sign": "Taurus", "dignity": "own_sign"}
            },
            "house_lords": {2: "Jupiter", 11: "Venus"},
            "active_yogas": ["Dhana_Yoga"]
        }
        
        result = engine.predict_wealth_gain(strong_chart)
        
        assert 0 <= result.confidence <= 100
        assert result.confidence >= 50  # Strong chart should have good confidence
    
    def test_spiritual_awakening_prediction(self):
        """Test spiritual awakening prediction"""
        engine = EventPredictionEngine()
        
        chart_data = {
            "planets": {
                "Jupiter": {"house": 12, "sign": "Pisces", "dignity": "own_sign"},
                "Ketu": {"house": 9, "sign": "Sagittarius", "dignity": "neutral"}
            },
            "house_lords": {12: "Jupiter", 9: "Mars", 8: "Saturn"},
            "active_yogas": []
        }
        
        result = engine.predict_spiritual_awakening(chart_data)
        
        assert result.event_type == "spiritual_awakening"
        assert result.natal_promise_strength > 0
