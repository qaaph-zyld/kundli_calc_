"""
Tests for PDF Export System
"""

import pytest
from datetime import datetime

# Skip entire module due to WeasyPrint GTK dependency not available on Windows
pytestmark = pytest.mark.skip(reason="WeasyPrint GTK library not available on Windows")

from backend.app.core.reports.pdf_exporter import PDFExporter
from backend.app.core.reports.report_generator import (
    ComprehensiveReport,
    ExecutiveSummary,
    TimingForecast,
    LifeAreaReport
)


class TestPDFExport:
    
    def test_exporter_initialization(self):
        """Test PDF exporter initializes"""
        exporter = PDFExporter()
        assert exporter is not None
        assert exporter.template_dir.exists()
        assert exporter.static_dir.exists()
    
    def test_pdf_generation(self):
        """Test PDF generation from report"""
        
        report = ComprehensiveReport(
            report_id="test-123",
            generated_at=datetime.now(),
            chart_owner="Test User",
            birth_data={"datetime": "1990-01-01", "location": "Test City"},
            executive_summary=ExecutiveSummary(
                overall_strength=75.0,
                key_strengths=["Strong career indicators"],
                key_challenges=["Relationship requires attention"],
                dominant_themes=["Career focus"],
                synthesis="Test synthesis narrative"
            ),
            life_areas={
                "career": LifeAreaReport(
                    area="career",
                    content="Career analysis content",
                    strength_score=80.0,
                    key_points=["Leadership potential", "Authority roles"],
                    timing_forecast="Peak during Sun dasha",
                    sources=["BPHS Ch. 24"]
                )
            },
            timing_forecast=TimingForecast(
                current_period="Sun Mahadasha",
                year_by_year={},
                major_transitions=[]
            ),
            active_yogas=[],
            current_transits={},
            bibliography=["BPHS Ch. 24", "Saravali Ch. 32"],
            metadata={}
        )
        
        exporter = PDFExporter()
        pdf_bytes = exporter.export_to_pdf(report)
        
        # Verify PDF was generated
        assert len(pdf_bytes) > 0
        assert pdf_bytes[:4] == b'%PDF'  # PDF file signature
    
    def test_pdf_file_size(self):
        """Test PDF file size is reasonable"""
        
        report = ComprehensiveReport(
            report_id="test-456",
            generated_at=datetime.now(),
            chart_owner="Test User 2",
            birth_data={},
            executive_summary=ExecutiveSummary(
                overall_strength=65.0,
                key_strengths=["Test"],
                key_challenges=["Test"],
                dominant_themes=["Test"],
                synthesis="Test"
            ),
            life_areas={},
            timing_forecast=TimingForecast(
                current_period="Test",
                year_by_year={},
                major_transitions=[]
            ),
            active_yogas=[],
            current_transits={},
            bibliography=["Test"],
            metadata={}
        )
        
        exporter = PDFExporter()
        pdf_bytes = exporter.export_to_pdf(report)
        
        # Verify reasonable file size (< 3MB)
        assert len(pdf_bytes) < 3 * 1024 * 1024
    
    def test_html_generation(self):
        """Test HTML generation from report"""
        
        report = ComprehensiveReport(
            report_id="test-789",
            generated_at=datetime.now(),
            chart_owner="Test User 3",
            birth_data={},
            executive_summary=ExecutiveSummary(
                overall_strength=70.0,
                key_strengths=["Test strength"],
                key_challenges=["Test challenge"],
                dominant_themes=["Test theme"],
                synthesis="Test synthesis"
            ),
            life_areas={},
            timing_forecast=TimingForecast(
                current_period="Test period",
                year_by_year={},
                major_transitions=[]
            ),
            active_yogas=[],
            current_transits={},
            bibliography=["Test source"],
            metadata={}
        )
        
        exporter = PDFExporter()
        html = exporter._generate_html(report, "professional")
        
        # Verify HTML contains key elements
        assert "<!DOCTYPE html>" in html
        assert report.chart_owner in html
        assert "Executive Summary" in html
        assert "Bibliography" in html
