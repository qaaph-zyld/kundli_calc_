"""
Transit Analysis Accuracy Tests
================================
Verifies Gochara (transit) calculations against BPHS and classical references.

References:
- BPHS Chapter 65 (Gochara Phala)
- Phaladeepika Chapter 26
- Saravali Chapter 53
"""

import pytest
from datetime import datetime
from app.core.calculations.transit_analysis import (
    TransitAnalyzer,
    TransitResult,
    GOCHARA_BENEFIC_HOUSES,
    VEDHA_POINTS,
    SIGN_NAMES,
    NAKSHATRAS
)

# Reference chart: Oct 9, 1990, 09:10 AM, Loznica
# Moon at 58.32° (Taurus = sign 1)
NATAL_MOON_SIGN = 1  # Taurus
NATAL_PLANETS = {
    "Sun": 172.05,
    "Moon": 58.32,
    "Mars": 49.86,
    "Mercury": 162.58,
    "Jupiter": 105.82,
    "Venus": 166.03,
    "Saturn": 265.17,
    "Rahu": 279.82,
    "Ketu": 99.82
}


class TestGocharaBeneficHouses:
    """Test Gochara benefic house rules per BPHS"""
    
    def test_sun_benefic_houses(self):
        """Sun is benefic in 3, 6, 10, 11 from Moon"""
        assert GOCHARA_BENEFIC_HOUSES["Sun"] == [3, 6, 10, 11]
    
    def test_moon_benefic_houses(self):
        """Moon is benefic in 1, 3, 6, 7, 10, 11 from Moon"""
        assert GOCHARA_BENEFIC_HOUSES["Moon"] == [1, 3, 6, 7, 10, 11]
    
    def test_mars_benefic_houses(self):
        """Mars is benefic in 3, 6, 11 from Moon"""
        assert GOCHARA_BENEFIC_HOUSES["Mars"] == [3, 6, 11]
    
    def test_mercury_benefic_houses(self):
        """Mercury is benefic in 2, 4, 6, 8, 10, 11 from Moon"""
        assert GOCHARA_BENEFIC_HOUSES["Mercury"] == [2, 4, 6, 8, 10, 11]
    
    def test_jupiter_benefic_houses(self):
        """Jupiter is benefic in 2, 5, 7, 9, 11 from Moon"""
        assert GOCHARA_BENEFIC_HOUSES["Jupiter"] == [2, 5, 7, 9, 11]
    
    def test_venus_benefic_houses(self):
        """Venus is benefic in 1, 2, 3, 4, 5, 8, 9, 11, 12 from Moon"""
        assert GOCHARA_BENEFIC_HOUSES["Venus"] == [1, 2, 3, 4, 5, 8, 9, 11, 12]
    
    def test_saturn_benefic_houses(self):
        """Saturn is benefic in 3, 6, 11 from Moon"""
        assert GOCHARA_BENEFIC_HOUSES["Saturn"] == [3, 6, 11]
    
    def test_rahu_ketu_benefic_houses(self):
        """Rahu/Ketu are benefic in 3, 6, 10, 11 from Moon"""
        assert GOCHARA_BENEFIC_HOUSES["Rahu"] == [3, 6, 10, 11]
        assert GOCHARA_BENEFIC_HOUSES["Ketu"] == [3, 6, 10, 11]


class TestVedhaPoints:
    """Test Vedha (obstruction) rules per classical texts"""
    
    def test_sun_vedha(self):
        """Sun Vedha points: 3-9, 6-12, 10-4, 11-5"""
        assert VEDHA_POINTS["Sun"] == {3: 9, 6: 12, 10: 4, 11: 5}
    
    def test_moon_vedha(self):
        """Moon Vedha points"""
        assert VEDHA_POINTS["Moon"] == {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8}
    
    def test_mars_vedha(self):
        """Mars Vedha points: 3-12, 6-9, 11-5"""
        assert VEDHA_POINTS["Mars"] == {3: 12, 6: 9, 11: 5}
    
    def test_saturn_vedha(self):
        """Saturn Vedha points same as Mars: 3-12, 6-9, 11-5"""
        assert VEDHA_POINTS["Saturn"] == {3: 12, 6: 9, 11: 5}
    
    def test_jupiter_vedha(self):
        """Jupiter Vedha points: 2-12, 5-4, 7-3, 9-10, 11-8"""
        assert VEDHA_POINTS["Jupiter"] == {2: 12, 5: 4, 7: 3, 9: 10, 11: 8}


class TestTransitAnalyzer:
    """Test TransitAnalyzer calculations"""
    
    @pytest.fixture
    def analyzer(self):
        return TransitAnalyzer(NATAL_MOON_SIGN, NATAL_PLANETS)
    
    def test_initialization(self, analyzer):
        """Analyzer should initialize with natal data"""
        assert analyzer.natal_moon_sign == 1  # Taurus
        assert analyzer.natal_moon_house == 1
    
    def test_transit_house_calculation(self, analyzer):
        """Transit house from Moon should be calculated correctly"""
        # If Moon is in Taurus (1), and Saturn transits Sagittarius (8)
        # House from Moon = (8 - 1) + 1 = 8
        transit_positions = {
            "Saturn": 265.0,  # Sagittarius
            "Jupiter": 30.0,  # Taurus
        }
        
        result = analyzer.analyze_transit(transit_positions, datetime.now())
        
        # Find Saturn's result
        saturn_result = next(
            (g for g in result["gochara_results"] if g["planet"] == "Saturn"),
            None
        )
        assert saturn_result is not None
        # Sagittarius (8) from Taurus (1) = house 8
        assert saturn_result["house_from_moon"] == 8
    
    def test_benefic_transit_detection(self, analyzer):
        """Should detect benefic transits correctly"""
        # Jupiter in 2nd from Moon (Gemini) is benefic
        transit_positions = {
            "Jupiter": 75.0,  # Gemini = 2nd from Taurus
        }
        
        result = analyzer.analyze_transit(transit_positions, datetime.now())
        
        jupiter_result = next(
            (g for g in result["gochara_results"] if g["planet"] == "Jupiter"),
            None
        )
        assert jupiter_result is not None
        assert jupiter_result["is_benefic"] == True
    
    def test_malefic_transit_detection(self, analyzer):
        """Should detect malefic transits correctly"""
        # Saturn in 8th from Moon is malefic
        transit_positions = {
            "Saturn": 265.0,  # Sagittarius = 8th from Taurus
        }
        
        result = analyzer.analyze_transit(transit_positions, datetime.now())
        
        saturn_result = next(
            (g for g in result["gochara_results"] if g["planet"] == "Saturn"),
            None
        )
        assert saturn_result is not None
        # 8th house is not in Saturn's benefic list [3, 6, 11]
        assert saturn_result["is_benefic"] == False
    
    def test_gochara_result_structure(self, analyzer):
        """Gochara results should have required fields"""
        transit_positions = {"Jupiter": 75.0}
        
        result = analyzer.analyze_transit(transit_positions, datetime.now())
        
        gochara = result["gochara_results"][0]
        assert "planet" in gochara
        assert "house_from_moon" in gochara
        assert "is_benefic" in gochara
        assert "has_vedha" in gochara
        assert "ashtakavarga_score" in gochara
        assert "result" in gochara
        assert "interpretation" in gochara


class TestSadeSati:
    """Test Sade Sati (7.5 year Saturn transit) detection"""
    
    @pytest.fixture
    def analyzer(self):
        return TransitAnalyzer(NATAL_MOON_SIGN, NATAL_PLANETS)
    
    def test_sade_sati_active_when_saturn_near_moon(self, analyzer):
        """Sade Sati active when Saturn in 12th, 1st, or 2nd from Moon"""
        # Saturn in Taurus (same as Moon) = Sade Sati peak
        transit_positions = {"Saturn": 45.0}  # Taurus
        
        result = analyzer.analyze_transit(transit_positions, datetime.now())
        
        assert result["sade_sati"]["is_active"] == True
        assert result["sade_sati"]["phase"] == "peak"
    
    def test_sade_sati_rising_phase(self, analyzer):
        """Sade Sati rising when Saturn in 12th from Moon"""
        # 12th from Taurus is Aries (0)
        transit_positions = {"Saturn": 15.0}  # Aries
        
        result = analyzer.analyze_transit(transit_positions, datetime.now())
        
        assert result["sade_sati"]["is_active"] == True
        assert result["sade_sati"]["phase"] == "rising"
    
    def test_sade_sati_setting_phase(self, analyzer):
        """Sade Sati setting when Saturn in 2nd from Moon"""
        # 2nd from Taurus is Gemini (2)
        transit_positions = {"Saturn": 75.0}  # Gemini
        
        result = analyzer.analyze_transit(transit_positions, datetime.now())
        
        assert result["sade_sati"]["is_active"] == True
        assert result["sade_sati"]["phase"] == "setting"
    
    def test_sade_sati_inactive(self, analyzer):
        """Sade Sati inactive when Saturn far from Moon sign"""
        # Saturn in Sagittarius (8) - not near Taurus
        transit_positions = {"Saturn": 265.0}
        
        result = analyzer.analyze_transit(transit_positions, datetime.now())
        
        assert result["sade_sati"]["is_active"] == False


class TestTransitConstants:
    """Test transit system constants"""
    
    def test_twelve_signs(self):
        """Should have 12 zodiac signs"""
        assert len(SIGN_NAMES) == 12
    
    def test_sign_order(self):
        """Signs should be in correct order"""
        assert SIGN_NAMES[0] == "Aries"
        assert SIGN_NAMES[6] == "Libra"
        assert SIGN_NAMES[11] == "Pisces"
    
    def test_27_nakshatras(self):
        """Should have 27 nakshatras"""
        assert len(NAKSHATRAS) == 27
    
    def test_nakshatra_order(self):
        """Nakshatras should be in correct order"""
        assert NAKSHATRAS[0] == "Ashwini"
        assert NAKSHATRAS[4] == "Mrigashira"
        assert NAKSHATRAS[26] == "Revati"
    
    def test_all_planets_have_benefic_houses(self):
        """All major planets should have benefic house definitions"""
        required_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        for planet in required_planets:
            assert planet in GOCHARA_BENEFIC_HOUSES


class TestTransitResultTypes:
    """Test TransitResult enum"""
    
    def test_result_types_exist(self):
        """All result types should exist"""
        assert TransitResult.EXCELLENT.value == "excellent"
        assert TransitResult.GOOD.value == "good"
        assert TransitResult.NEUTRAL.value == "neutral"
        assert TransitResult.CHALLENGING.value == "challenging"
        assert TransitResult.DIFFICULT.value == "difficult"
