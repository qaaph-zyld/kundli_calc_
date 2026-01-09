"""
Report Generation API Endpoints
================================

Comprehensive astrological report generation.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.core.reports.report_generator import ComprehensiveReportGenerator

router = APIRouter()


class ReportRequest(BaseModel):
    """Request for comprehensive report"""
    chart_data: Dict[str, Any]
    sections: Optional[List[str]] = None
    format: str = "narrative"
    include_sources: bool = True
    time_period: int = 5


@router.post("/comprehensive")
async def generate_comprehensive_report(request: ReportRequest):
    """Generate comprehensive astrological report"""
    try:
        generator = ComprehensiveReportGenerator()
        
        report = generator.generate_comprehensive_report(
            chart_data=request.chart_data,
            sections=request.sections,
            format_type=request.format,
            include_sources=request.include_sources,
            time_period=request.time_period
        )
        
        return {
            "report_id": report.report_id,
            "generated_at": report.generated_at.isoformat(),
            "chart_owner": report.chart_owner,
            "executive_summary": {
                "overall_strength": report.executive_summary.overall_strength,
                "key_strengths": report.executive_summary.key_strengths,
                "key_challenges": report.executive_summary.key_challenges,
                "dominant_themes": report.executive_summary.dominant_themes,
                "synthesis": report.executive_summary.synthesis
            },
            "life_areas": {
                area_name: {
                    "area": area.area,
                    "content": area.content,
                    "strength_score": area.strength_score,
                    "key_points": area.key_points,
                    "timing_forecast": area.timing_forecast
                }
                for area_name, area in report.life_areas.items()
            },
            "timing_forecast": {
                "current_period": report.timing_forecast.current_period,
                "year_by_year": {
                    year: {
                        "year": forecast.year,
                        "dasha_period": forecast.dasha_period,
                        "major_themes": forecast.major_themes,
                        "opportunities": forecast.opportunities,
                        "challenges": forecast.challenges,
                        "synthesis": forecast.synthesis
                    }
                    for year, forecast in report.timing_forecast.year_by_year.items()
                },
                "major_transitions": report.timing_forecast.major_transitions
            },
            "active_yogas": report.active_yogas,
            "current_transits": report.current_transits,
            "bibliography": report.bibliography,
            "metadata": report.metadata,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )
