"""
Tests for Comprehensive Report Generator
"""

import pytest
from backend.app.core.reports.report_generator import (
    ComprehensiveReportGenerator,
    ComprehensiveReport
)


class TestReportGenerator:
    
    def test_generator_initialization(self):
        """Test report generator initializes"""
        generator = ComprehensiveReportGenerator()
        assert generator is not None
        assert generator.career_engine is not None
        assert generator.relationship_engine is not None
        assert generator.wealth_engine is not None
    
    def test_comprehensive_report_generation(self):
        """Test comprehensive report generation"""
        generator = ComprehensiveReportGenerator()
        
        chart_data = {
            "name": "Test Chart",
            "birth_data": {},
            "planets": {
                "Sun": {"house": 10, "sign": "Aries", "dignity": "exalted"},
                "Moon": {"house": 4, "sign": "Cancer", "dignity": "own_sign"},
                "Jupiter": {"house": 9, "sign": "Sagittarius", "dignity": "own_sign"}
            },
            "house_lords": {10: "Sun", 7: "Venus", 2: "Mercury"},
            "active_yogas": ["Dharma_Karma_Adhipati_Yoga"],
            "current_dasha": "Sun"
        }
        
        report = generator.generate_comprehensive_report(chart_data)
        
        assert isinstance(report, ComprehensiveReport)
        assert report.report_id is not None
        assert report.executive_summary is not None
        assert len(report.life_areas) > 0
        assert report.timing_forecast is not None
    
    def test_executive_summary_generation(self):
        """Test executive summary generation"""
        generator = ComprehensiveReportGenerator()
        
        chart_data = {
            "planets": {
                "Sun": {"house": 10, "sign": "Aries", "dignity": "exalted"}
            },
            "house_lords": {10: "Sun"},
            "active_yogas": []
        }
        
        report = generator.generate_comprehensive_report(chart_data)
        
        assert report.executive_summary.overall_strength > 0
        assert isinstance(report.executive_summary.key_strengths, list)
        assert isinstance(report.executive_summary.dominant_themes, list)
        assert len(report.executive_summary.synthesis) > 50
    
    def test_bibliography_compilation(self):
        """Test bibliography compilation"""
        generator = ComprehensiveReportGenerator()
        
        chart_data = {
            "planets": {
                "Sun": {"house": 10, "sign": "Aries", "dignity": "exalted"},
                "Jupiter": {"house": 9, "sign": "Sagittarius", "dignity": "own_sign"}
            },
            "house_lords": {10: "Sun", 2: "Mercury"},
            "active_yogas": []
        }
        
        report = generator.generate_comprehensive_report(
            chart_data,
            include_sources=True
        )
        
        assert len(report.bibliography) > 0
