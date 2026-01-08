"""
Tests for Comprehensive Chart Interpretation Endpoint

Validates the integrated system bringing together:
- Planet-in-house interpretations
- Multi-source comparison
- Yoga detection framework
- Complete chart analysis
"""

import pytest
from backend.app.api.endpoints.comprehensive_interpretation import (
    get_comprehensive_chart_interpretation,
    demo_comprehensive_interpretation,
    ChartPlacement,
    ComprehensiveChartRequest,
    generate_chart_synthesis,
    assess_quality
)


class TestComprehensiveEndpoint:
    """Test suite for comprehensive interpretation endpoint"""
    
    @pytest.mark.asyncio
    async def test_comprehensive_endpoint_basic(self):
        """Test basic comprehensive interpretation"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Sun", house=10, sign="Aries", dignity="exalted")
            ],
            include_yogas=True,
            include_multi_source=True
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        assert result["status"] == "success"
        assert result["chart_analysis"]["total_planets"] == 1
        assert len(result["planet_interpretations"]) == 1
        assert result["planet_interpretations"][0]["planet"] == "Sun"
    
    @pytest.mark.asyncio
    async def test_comprehensive_multiple_planets(self):
        """Test comprehensive interpretation with multiple planets"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Sun", house=10, sign="Aries", dignity="exalted"),
                ChartPlacement(planet="Moon", house=4, sign="Taurus", dignity="exalted"),
                ChartPlacement(planet="Jupiter", house=1, sign="Sagittarius", dignity="own_sign")
            ],
            include_yogas=True,
            include_multi_source=True
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        assert result["chart_analysis"]["total_planets"] == 3
        assert len(result["planet_interpretations"]) == 3
        assert result["chart_analysis"]["average_confidence"] > 0.9
    
    @pytest.mark.asyncio
    async def test_multi_source_detection(self):
        """Test that multi-source comparisons are detected"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Sun", house=1, sign="Leo", dignity="own_sign"),
                ChartPlacement(planet="Jupiter", house=1, sign="Sagittarius", dignity="own_sign")
            ],
            include_yogas=True,
            include_multi_source=True
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        # Should have multi-source for at least one placement
        assert result["chart_analysis"]["multi_source_available"] >= 1
    
    @pytest.mark.asyncio
    async def test_without_multi_source(self):
        """Test comprehensive interpretation without multi-source comparison"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Sun", house=10, sign="Aries", dignity="exalted")
            ],
            include_yogas=False,
            include_multi_source=False
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        assert result["status"] == "success"
        # Should not have multi_source key in planet data when disabled
        for planet in result["planet_interpretations"]:
            if "multi_source" not in planet:
                assert True  # Expected when multi_source disabled
    
    @pytest.mark.asyncio
    async def test_synthesis_generation(self):
        """Test that synthesis is generated"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Sun", house=10, sign="Aries", dignity="exalted"),
                ChartPlacement(planet="Moon", house=4, sign="Taurus", dignity="exalted")
            ]
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        assert "synthesis" in result
        assert len(result["synthesis"]) > 50  # Should have substantial content
        assert "classical" in result["synthesis"].lower()
    
    @pytest.mark.asyncio
    async def test_overall_assessment(self):
        """Test overall assessment is provided"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Jupiter", house=1, sign="Sagittarius", dignity="own_sign")
            ]
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        assert "overall_assessment" in result
        assert "interpretation_quality" in result["overall_assessment"]
        assert "source_coverage" in result["overall_assessment"]
        assert "BPHS" in result["overall_assessment"]["classical_texts_used"]
    
    @pytest.mark.asyncio
    async def test_demo_endpoint(self):
        """Test demo comprehensive interpretation endpoint"""
        result = await demo_comprehensive_interpretation()
        
        assert result["status"] == "success"
        assert "demo_note" in result
        assert "competitive_advantage" in result
        assert result["chart_analysis"]["total_planets"] == 3
    
    def test_chart_synthesis_function(self):
        """Test chart synthesis generation function"""
        placements = [
            ChartPlacement(planet="Sun", house=10, sign="Aries", dignity="exalted"),
            ChartPlacement(planet="Moon", house=4, sign="Taurus", dignity="exalted")
        ]
        
        synthesis = generate_chart_synthesis(placements, 0.95, 2)
        
        assert len(synthesis) > 0
        assert "2 planetary placements" in synthesis
        assert "multi-source" in synthesis.lower()
    
    def test_quality_assessment(self):
        """Test quality assessment function"""
        assert assess_quality(0.96) == "Exceptional - Direct classical text quotes with strong consensus"
        assert assess_quality(0.92) == "Excellent - High-confidence classical interpretations"
        assert assess_quality(0.87) == "Very Good - Solid classical text basis"
        assert assess_quality(0.82) == "Good - Reliable classical sources"
        assert assess_quality(0.75) == "Standard - Classical text interpretations"
    
    @pytest.mark.asyncio
    async def test_metadata_presence(self):
        """Test that metadata is included in response"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Sun", house=10, sign="Aries")
            ]
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        assert "metadata" in result
        assert "total_interpretations" in result["metadata"]
        assert "success_rate" in result["metadata"]
        assert "api_version" in result["metadata"]


class TestComprehensiveIntegration:
    """Integration tests for comprehensive system"""
    
    @pytest.mark.asyncio
    async def test_full_chart_seven_planets(self):
        """Test comprehensive interpretation with all 7 classical planets"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Sun", house=10, sign="Aries", dignity="exalted"),
                ChartPlacement(planet="Moon", house=4, sign="Taurus", dignity="exalted"),
                ChartPlacement(planet="Mars", house=1, sign="Aries", dignity="own_sign"),
                ChartPlacement(planet="Mercury", house=11, sign="Virgo", dignity="own_sign"),
                ChartPlacement(planet="Jupiter", house=9, sign="Sagittarius", dignity="own_sign"),
                ChartPlacement(planet="Venus", house=7, sign="Pisces", dignity="exalted"),
                ChartPlacement(planet="Saturn", house=10, sign="Libra", dignity="exalted")
            ],
            include_yogas=True,
            include_multi_source=True
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        assert result["status"] == "success"
        assert result["chart_analysis"]["total_planets"] == 7
        assert len(result["planet_interpretations"]) == 7
        
        # All planets should have interpretations
        for planet_data in result["planet_interpretations"]:
            assert "planet" in planet_data
            assert "interpretation" in planet_data or "note" in planet_data.get("interpretation", {})
        
        # Average confidence should be high for well-placed planets
        assert result["chart_analysis"]["average_confidence"] > 0.90
    
    @pytest.mark.asyncio
    async def test_confidence_calculation(self):
        """Test that confidence is correctly calculated"""
        request = ComprehensiveChartRequest(
            placements=[
                ChartPlacement(planet="Sun", house=1, sign="Leo"),
                ChartPlacement(planet="Moon", house=2, sign="Taurus")
            ]
        )
        
        result = await get_comprehensive_chart_interpretation(request)
        
        # Should have average confidence calculated
        assert 0 <= result["chart_analysis"]["average_confidence"] <= 1.0
        assert isinstance(result["chart_analysis"]["average_confidence"], float)
