"""
Tests for Dasha-Integrated Interpretation System
"""

import pytest
from backend.app.api.endpoints.dasha_interpretation import (
    get_dasha_integrated_interpretation,
    demo_dasha_integrated,
    DashaInterpretationRequest
)


class TestDashaIntegration:
    """Test dasha-integrated interpretation endpoints"""
    
    @pytest.mark.asyncio
    async def test_dasha_integrated_active_now(self):
        """Test when natal planet = current dasha (active now)"""
        request = DashaInterpretationRequest(
            planet="Sun",
            house=10,
            sign="Aries",
            dignity="exalted",
            current_dasha="Sun"
        )
        
        result = await get_dasha_integrated_interpretation(request)
        
        assert result["status"] == "success"
        assert result["timing_analysis"]["is_active_now"] is True
        assert "ACTIVE NOW" in result["timing_analysis"]["activation_status"]
        assert result["current_dasha_period"]["planet"] == "Sun"
    
    @pytest.mark.asyncio
    async def test_dasha_integrated_future_activation(self):
        """Test when natal planet != current dasha (future activation)"""
        request = DashaInterpretationRequest(
            planet="Sun",
            house=10,
            sign="Aries",
            dignity="exalted",
            current_dasha="Moon"
        )
        
        result = await get_dasha_integrated_interpretation(request)
        
        assert result["status"] == "success"
        assert result["timing_analysis"]["is_active_now"] is False
        assert "Future activation" in result["timing_analysis"]["activation_status"]
        assert result["current_dasha_period"]["planet"] == "Moon"
    
    @pytest.mark.asyncio
    async def test_natal_interpretation_included(self):
        """Test that natal interpretation is included"""
        request = DashaInterpretationRequest(
            planet="Jupiter",
            house=9,
            sign="Sagittarius",
            current_dasha="Jupiter"
        )
        
        result = await get_dasha_integrated_interpretation(request)
        
        assert "natal_interpretation" in result
        assert "synthesis" in result["natal_interpretation"]
        assert "strength" in result["natal_interpretation"]
        assert result["natal_interpretation"]["confidence"] > 0
    
    @pytest.mark.asyncio
    async def test_dasha_period_details(self):
        """Test that dasha period details are complete"""
        request = DashaInterpretationRequest(
            planet="Sun",
            house=10,
            sign="Aries",
            current_dasha="Saturn"
        )
        
        result = await get_dasha_integrated_interpretation(request)
        
        dasha_period = result["current_dasha_period"]
        assert dasha_period["planet"] == "Saturn"
        assert "duration_years" in dasha_period
        assert "general_effects" in dasha_period
        assert "favorable_for" in dasha_period
        assert "remedial_measures" in dasha_period
    
    @pytest.mark.asyncio
    async def test_integrated_guidance(self):
        """Test that integrated guidance is provided"""
        request = DashaInterpretationRequest(
            planet="Venus",
            house=7,
            sign="Pisces",
            current_dasha="Venus"
        )
        
        result = await get_dasha_integrated_interpretation(request)
        
        assert "integrated_guidance" in result
        guidance = result["integrated_guidance"]
        assert "timing_window" in guidance
        assert "focus_areas" in guidance
        assert "recommendations" in guidance
        assert len(guidance["recommendations"]) > 0
    
    @pytest.mark.asyncio
    async def test_demo_endpoint(self):
        """Test demo dasha-integrated endpoint"""
        result = await demo_dasha_integrated()
        
        assert result["status"] == "success"
        assert "demo_note" in result
        assert result["planet"] == "Sun"
        assert result["house"] == 10
