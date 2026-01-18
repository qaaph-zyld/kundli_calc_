"""
PDF Export System for Comprehensive Reports
==========================================

Professional PDF generation with formatting, charts, and citations.
Uses WeasyPrint for HTML-to-PDF conversion.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from weasyprint import CSS, HTML

from .report_generator import ComprehensiveReport


class PDFExporter:
    """Export comprehensive reports to professional PDF format"""

    def __init__(self):
        self.template_dir = Path(__file__).parent / "templates"
        self.static_dir = Path(__file__).parent / "static"

        # Ensure directories exist
        self.template_dir.mkdir(exist_ok=True)
        self.static_dir.mkdir(exist_ok=True)

    def export_to_pdf(
        self, report: ComprehensiveReport, template: str = "professional", include_charts: bool = False
    ) -> bytes:
        """
        Export report to PDF using ReportLab.

        Args:
            report: ComprehensiveReport object
            template: Template style
            include_charts: Include chart diagrams

        Returns:
            PDF file as bytes
        """

        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # Add custom styles
        styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#1a1a1a"),
                spaceAfter=30,
            )
        )

        # Cover page
        story.append(Paragraph("Comprehensive Astrological Analysis", styles["CustomTitle"]))
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(f"<b>{report.chart_owner}</b>", styles["Heading2"]))
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(f"Report Generated: {report.generated_at.strftime('%B %d, %Y')}", styles["Normal"]))
        story.append(PageBreak())

        # Executive Summary
        story.append(Paragraph("Executive Summary", styles["Heading1"]))
        story.append(Spacer(1, 0.2 * inch))
        story.append(
            Paragraph(
                f"<b>Overall Chart Strength: {report.executive_summary.overall_strength:.1f}/100</b>",
                styles["Heading3"],
            )
        )
        story.append(Spacer(1, 0.2 * inch))

        # Key Strengths
        story.append(Paragraph("<b>Key Strengths:</b>", styles["Heading3"]))
        for strength in report.executive_summary.key_strengths:
            story.append(Paragraph(f"• {strength}", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

        # Key Challenges
        story.append(Paragraph("<b>Key Challenges:</b>", styles["Heading3"]))
        for challenge in report.executive_summary.key_challenges:
            story.append(Paragraph(f"• {challenge}", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

        # Synthesis
        story.append(Paragraph("<b>Synthesis:</b>", styles["Heading3"]))
        story.append(Paragraph(report.executive_summary.synthesis, styles["Normal"]))
        story.append(PageBreak())

        # Life Areas
        story.append(Paragraph("Life Area Analysis", styles["Heading1"]))
        for area_name, area_report in report.life_areas.items():
            story.append(Paragraph(area_name.title(), styles["Heading2"]))
            story.append(Paragraph(f"<b>Strength Score: {area_report.strength_score:.1f}/100</b>", styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(area_report.content, styles["Normal"]))
            story.append(Spacer(1, 0.2 * inch))

        story.append(PageBreak())

        # Bibliography
        story.append(Paragraph("Bibliography & Classical Sources", styles["Heading1"]))
        story.append(Paragraph("All interpretations sourced from classical Vedic astrology texts:", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

        for i, citation in enumerate(report.bibliography, 1):
            story.append(Paragraph(f"{i}. {citation}", styles["Normal"]))

        # Build PDF
        doc.build(story)

        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

    def _generate_html(self, report: ComprehensiveReport, template: str) -> str:
        """Generate HTML from report data"""

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Astrological Analysis Report</title>
        </head>
        <body>
            <div class="cover-page">
                <h1>Comprehensive Astrological Analysis</h1>
                <h2>{report.chart_owner}</h2>
                <p class="birth-data">
                    Report ID: {report.report_id}<br>
                    Generated: {report.generated_at.strftime('%B %d, %Y at %H:%M')}
                </p>
            </div>
            
            <div class="page-break"></div>
            
            <div class="toc">
                <h2>Table of Contents</h2>
                <ul>
                    <li>Executive Summary</li>
                    <li>Life Area Analysis
                        <ul>
                            <li>Career & Status</li>
                            <li>Relationships & Marriage</li>
                            <li>Wealth & Prosperity</li>
                        </ul>
                    </li>
                    <li>Timing Forecast</li>
                    <li>Active Yogas</li>
                    <li>Current Transits</li>
                    <li>Bibliography</li>
                </ul>
            </div>
            
            <div class="page-break"></div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                
                <div class="strength-score">
                    <h3>Overall Chart Strength: {report.executive_summary.overall_strength:.1f}/100</h3>
                </div>
                
                <h3>Key Strengths</h3>
                <ul class="strengths">
                    {''.join(f'<li>{s}</li>' for s in report.executive_summary.key_strengths)}
                </ul>
                
                <h3>Key Challenges</h3>
                <ul class="challenges">
                    {''.join(f'<li>{c}</li>' for c in report.executive_summary.key_challenges)}
                </ul>
                
                <h3>Dominant Life Themes</h3>
                <ul class="themes">
                    {''.join(f'<li>{t}</li>' for t in report.executive_summary.dominant_themes)}
                </ul>
                
                <div class="synthesis">
                    <h3>Synthesis</h3>
                    <p>{report.executive_summary.synthesis}</p>
                </div>
            </div>
            
            <div class="page-break"></div>
            
            <div class="section">
                <h2>Life Area Analysis</h2>
        """

        # Life Areas
        for area_name, area_report in report.life_areas.items():
            html += f"""
            <div class="life-area">
                <h3>{area_name.title()}</h3>
                
                <div class="strength-score">
                    <strong>Strength Score: {area_report.strength_score:.1f}/100</strong>
                </div>
                
                <h4>Key Points</h4>
                <ul>
                    {''.join(f'<li>{kp}</li>' for kp in area_report.key_points)}
                </ul>
                
                <h4>Analysis</h4>
                <p>{area_report.content}</p>
                
                <h4>Timing Forecast</h4>
                <p>{area_report.timing_forecast}</p>
            </div>
            """

        html += '</div><div class="page-break"></div>'

        # Timing Forecast
        html += f"""
        <div class="section">
            <h2>Timing Forecast</h2>
            
            <h3>Current Period</h3>
            <p>{report.timing_forecast.current_period}</p>
            
            <h3>Year-by-Year Forecast</h3>
        """

        for year, forecast in sorted(report.timing_forecast.year_by_year.items()):
            html += f"""
            <div class="year-forecast">
                <h4>{year}</h4>
                <p><strong>Dasha Period:</strong> {forecast.dasha_period}</p>
                <p>{forecast.synthesis}</p>
            </div>
            """

        html += '</div><div class="page-break"></div>'

        # Bibliography
        html += """
        <div class="section">
            <h2>Bibliography & Classical Sources</h2>
            <p>All interpretations sourced from classical Vedic astrology texts:</p>
            <ol class="bibliography">
        """

        for citation in report.bibliography:
            html += f"<li>{citation}</li>"

        html += """
            </ol>
            
            <div class="footnote">
                <p><strong>Calculation Methods:</strong></p>
                <ul>
                    <li>Ayanamsa: Lahiri (Chitrapaksha)</li>
                    <li>House System: Whole Sign Houses</li>
                </ul>
            </div>
        </div>
        
        </body>
        </html>
        """

        return html

    def _load_css(self, template: str) -> str:
        """Load CSS styling"""

        css = """
        @page {
            size: A4;
            margin: 2.5cm 2cm;
        }
        
        body {
            font-family: Georgia, serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }
        
        h1 { font-size: 24pt; color: #1a1a1a; }
        h2 { font-size: 18pt; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8pt; }
        h3 { font-size: 14pt; color: #34495e; }
        h4 { font-size: 12pt; color: #555; }
        
        .cover-page {
            text-align: center;
            padding-top: 30%;
        }
        
        .page-break {
            page-break-after: always;
        }
        
        .strength-score {
            background: #f8f9fa;
            padding: 15pt;
            margin: 15pt 0;
            border-left: 4px solid #3498db;
        }
        
        ul.strengths li { color: #27ae60; margin: 8pt 0; }
        ul.challenges li { color: #e74c3c; margin: 8pt 0; }
        ul.themes li { color: #8e44ad; margin: 8pt 0; font-weight: bold; }
        
        .synthesis {
            background: #fffef7;
            padding: 15pt;
            border-left: 4px solid #f39c12;
            margin: 15pt 0;
        }
        
        .life-area {
            margin: 20pt 0;
        }
        
        .year-forecast {
            background: #f8f9fa;
            padding: 15pt;
            margin: 15pt 0;
            border-left: 4px solid #9b59b6;
        }
        
        .bibliography {
            font-size: 10pt;
            line-height: 1.8;
        }
        
        .footnote {
            margin-top: 30pt;
            padding-top: 15pt;
            border-top: 1px solid #ddd;
            font-size: 9pt;
            color: #666;
        }
        """

        return css

    def save_pdf(self, pdf_bytes: bytes, filename: str) -> str:
        """Save PDF to file"""
        filepath = Path(filename)
        filepath.write_bytes(pdf_bytes)
        return str(filepath.absolute())
