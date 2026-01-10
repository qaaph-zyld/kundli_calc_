"""
Comprehensive Report Generation System
======================================

Generates narrative reports from multi-engine analysis combining:
- Executive summary (strengths/challenges/themes)
- Life area deep dives (career/relationships/wealth)
- Timing forecast (year-by-year for next 5 years)
- Active yogas with activation windows
- Current transit analysis
- Complete bibliography with verse citations
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

from app.core.knowledge.engine.career_synthesis_engine import CareerSynthesisEngine
from app.core.knowledge.engine.relationship_synthesis_engine import RelationshipSynthesisEngine
from app.core.knowledge.engine.wealth_synthesis_engine import WealthSynthesisEngine
from app.core.timing.yoga_activation_engine import YogaActivationEngine
from app.core.timing.transit_engine import TransitIntelligenceEngine


@dataclass
class ExecutiveSummary:
    """Executive summary of chart analysis"""
    overall_strength: float
    key_strengths: List[str]
    key_challenges: List[str]
    dominant_themes: List[str]
    synthesis: str


@dataclass
class LifeAreaReport:
    """Report section for a life area"""
    area: str
    content: str
    strength_score: float
    key_points: List[str]
    timing_forecast: str
    sources: List[Dict[str, str]]


@dataclass
class YearForecast:
    """Forecast for a specific year"""
    year: int
    dasha_period: str
    major_themes: List[str]
    opportunities: List[str]
    challenges: List[str]
    synthesis: str


@dataclass
class TimingForecast:
    """Multi-year timing analysis"""
    current_period: str
    year_by_year: Dict[int, YearForecast]
    major_transitions: List[Dict[str, Any]]


@dataclass
class ComprehensiveReport:
    """Complete astrological report"""
    report_id: str
    generated_at: datetime
    chart_owner: str
    birth_data: Dict[str, Any]
    executive_summary: ExecutiveSummary
    life_areas: Dict[str, LifeAreaReport]
    timing_forecast: TimingForecast
    active_yogas: List[Dict[str, Any]]
    current_transits: Dict[str, Any]
    bibliography: List[str]
    metadata: Dict[str, Any]


class ComprehensiveReportGenerator:
    """Generate comprehensive astrological reports"""
    
    def __init__(self):
        self.career_engine = CareerSynthesisEngine()
        self.relationship_engine = RelationshipSynthesisEngine()
        self.wealth_engine = WealthSynthesisEngine()
        self.yoga_activation = YogaActivationEngine()
        self.transit_engine = TransitIntelligenceEngine()
    
    def generate_comprehensive_report(
        self,
        chart_data: Dict[str, Any],
        sections: Optional[List[str]] = None,
        format_type: str = "narrative",
        include_sources: bool = True,
        time_period: int = 5
    ) -> ComprehensiveReport:
        """Generate complete astrological report"""
        
        if sections is None:
            sections = ["executive_summary", "career", "relationships", "wealth", "timing"]
        
        report_id = str(uuid.uuid4())
        
        # Generate life area analyses
        life_areas = {}
        if "career" in sections:
            life_areas["career"] = self._generate_career_report(chart_data)
        if "relationships" in sections:
            life_areas["relationships"] = self._generate_relationship_report(chart_data)
        if "wealth" in sections:
            life_areas["wealth"] = self._generate_wealth_report(chart_data)
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(chart_data, life_areas)
        
        # Generate timing forecast
        timing_forecast = self._generate_timing_forecast(chart_data, time_period)
        
        # Get active yogas
        active_yogas = self._analyze_active_yogas(chart_data)
        
        # Get current transits
        current_transits = self._get_current_transits(chart_data)
        
        # Compile bibliography
        bibliography = self._compile_bibliography(life_areas, include_sources)
        
        return ComprehensiveReport(
            report_id=report_id,
            generated_at=datetime.now(),
            chart_owner=chart_data.get("name", "Unknown"),
            birth_data=chart_data.get("birth_data", {}),
            executive_summary=executive_summary,
            life_areas=life_areas,
            timing_forecast=timing_forecast,
            active_yogas=active_yogas,
            current_transits=current_transits,
            bibliography=bibliography,
            metadata={
                "sections_included": sections,
                "format": format_type,
                "time_period_years": time_period
            }
        )
    
    def _generate_career_report(self, chart_data: Dict) -> LifeAreaReport:
        """Generate career section"""
        result = self.career_engine.synthesize_career_analysis(
            chart_data, chart_data.get("current_dasha")
        )
        
        return LifeAreaReport(
            area="career",
            content=result.synthesis,
            strength_score=result.strength_score,
            key_points=result.recommendations,
            timing_forecast=result.timing.get("current_period", ""),
            sources=result.sources
        )
    
    def _generate_relationship_report(self, chart_data: Dict) -> LifeAreaReport:
        """Generate relationships section"""
        result = self.relationship_engine.synthesize_relationship_analysis(
            chart_data, chart_data.get("current_dasha")
        )
        
        return LifeAreaReport(
            area="relationships",
            content=result.synthesis,
            strength_score=result.strength_score,
            key_points=result.recommendations,
            timing_forecast=result.timing.get("current_period", ""),
            sources=result.sources
        )
    
    def _generate_wealth_report(self, chart_data: Dict) -> LifeAreaReport:
        """Generate wealth section"""
        result = self.wealth_engine.synthesize_wealth_analysis(
            chart_data, chart_data.get("current_dasha")
        )
        
        return LifeAreaReport(
            area="wealth",
            content=result.synthesis,
            strength_score=result.strength_score,
            key_points=result.recommendations,
            timing_forecast=result.timing.get("current_period", ""),
            sources=result.sources
        )
    
    def _generate_executive_summary(
        self,
        chart_data: Dict,
        life_areas: Dict[str, LifeAreaReport]
    ) -> ExecutiveSummary:
        """Generate executive summary"""
        
        strengths = [area.strength_score for area in life_areas.values()]
        overall_strength = sum(strengths) / len(strengths) if strengths else 50.0
        
        key_strengths = []
        key_challenges = []
        
        for area_name, area_report in life_areas.items():
            if area_report.strength_score >= 75:
                key_strengths.append(
                    f"Strong {area_name}: {area_report.key_points[0] if area_report.key_points else 'Favorable indicators'}"
                )
            elif area_report.strength_score < 50:
                key_challenges.append(
                    f"{area_name.title()} requires attention and focused effort"
                )
        
        dominant_themes = self._identify_dominant_themes(chart_data, life_areas)
        
        synthesis = self._generate_summary_synthesis(
            overall_strength, key_strengths, key_challenges, dominant_themes
        )
        
        return ExecutiveSummary(
            overall_strength=overall_strength,
            key_strengths=key_strengths[:5],
            key_challenges=key_challenges[:4],
            dominant_themes=dominant_themes[:3],
            synthesis=synthesis
        )
    
    def _generate_timing_forecast(
        self,
        chart_data: Dict,
        years: int
    ) -> TimingForecast:
        """Generate multi-year timing forecast"""
        
        current_year = datetime.now().year
        year_forecasts = {}
        
        for year_offset in range(years):
            year = current_year + year_offset
            forecast = self._generate_year_forecast(chart_data, year, year_offset)
            year_forecasts[year] = forecast
        
        current_period = self._analyze_current_period(chart_data)
        major_transitions = self._identify_major_transitions(chart_data, years)
        
        return TimingForecast(
            current_period=current_period,
            year_by_year=year_forecasts,
            major_transitions=major_transitions
        )
    
    def _identify_dominant_themes(
        self,
        chart_data: Dict,
        life_areas: Dict[str, LifeAreaReport]
    ) -> List[str]:
        """Identify 2-3 dominant life themes"""
        
        themes = []
        
        for area_name, area_report in life_areas.items():
            if area_report.strength_score >= 80:
                themes.append(f"{area_name.title()} excellence")
        
        if len(themes) < 2:
            themes.append("Balanced life approach")
        
        return themes[:3]
    
    def _generate_summary_synthesis(
        self,
        overall_strength: float,
        strengths: List[str],
        challenges: List[str],
        themes: List[str]
    ) -> str:
        """Generate executive summary narrative"""
        
        parts = []
        
        parts.append(
            f"This chart shows an overall strength of {overall_strength:.1f}/100, "
            f"indicating a {'strong' if overall_strength >= 70 else 'moderate' if overall_strength >= 50 else 'challenging'} "
            f"life path with distinct patterns."
        )
        
        if strengths:
            parts.append(f"\n\nKey Strengths: {', '.join(strengths[:3])}")
        
        if challenges:
            parts.append(f"\n\nAreas Requiring Attention: {', '.join(challenges[:3])}")
        
        if themes:
            parts.append(f"\n\nDominant Life Themes: {', '.join(themes)}")
        
        return "".join(parts)
    
    def _generate_year_forecast(
        self,
        chart_data: Dict,
        year: int,
        offset: int
    ) -> YearForecast:
        """Generate forecast for specific year"""
        
        dasha_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        dasha_period = dasha_planets[offset % 9]
        
        return YearForecast(
            year=year,
            dasha_period=f"{dasha_period} influence",
            major_themes=[f"{dasha_period} period themes"],
            opportunities=[f"Opportunities related to {dasha_period}"],
            challenges=[f"Challenges during {dasha_period} period"],
            synthesis=f"Year {year} forecast based on {dasha_period} influence"
        )
    
    def _analyze_current_period(self, chart_data: Dict) -> str:
        """Analyze current dasha period"""
        
        current_dasha = chart_data.get("current_dasha", "Unknown")
        return f"Currently in {current_dasha} mahadasha period with associated effects active."
    
    def _identify_major_transitions(
        self,
        chart_data: Dict,
        years: int
    ) -> List[Dict[str, Any]]:
        """Identify major dasha/transit transitions"""
        
        return [
            {
                "type": "dasha_change",
                "description": "Major dasha transition expected",
                "timing": "Within forecast period"
            }
        ]
    
    def _analyze_active_yogas(self, chart_data: Dict) -> List[Dict[str, Any]]:
        """Get all active yogas with activation windows"""
        
        active_yogas = chart_data.get("active_yogas", [])
        yoga_list = []
        
        for yoga_name in active_yogas:
            activation = self.yoga_activation.calculate_activation_windows(
                yoga_name=yoga_name,
                involved_planets=["Jupiter", "Moon"],  # Simplified
                formation_strength=80.0
            )
            
            yoga_list.append({
                "name": yoga_name,
                "formation_strength": activation.formation_strength,
                "timing": activation.overall_timing_note
            })
        
        return yoga_list
    
    def _get_current_transits(self, chart_data: Dict) -> Dict[str, Any]:
        """Get current transit analysis"""
        
        transits = self.transit_engine.get_current_transits(chart_data)
        
        return {
            "jupiter": {
                "sign": transits.jupiter.sign,
                "house": transits.jupiter.house_in_natal
            },
            "saturn": {
                "sign": transits.saturn.sign,
                "house": transits.saturn.house_in_natal
            },
            "synthesis": transits.synthesis
        }
    
    def _compile_bibliography(
        self,
        life_areas: Dict[str, LifeAreaReport],
        include_sources: bool
    ) -> List[str]:
        """Compile complete bibliography"""
        
        if not include_sources:
            return []
        
        sources_set = set()
        
        for area_report in life_areas.values():
            for source in area_report.sources:
                if isinstance(source, str):
                    sources_set.add(source)
                elif isinstance(source, dict):
                    citation = f"{source.get('text', 'Unknown')}, Ch. {source.get('chapter', 'N/A')}"
                    sources_set.add(citation)
        
        return sorted(list(sources_set))
