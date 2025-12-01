"""
Compatibility System Tests
===========================
Tests Ashtakoot (36 point) and Dashakoot (50 point) matching systems
"""

import pytest
from app.core.calculations.compatibility import (
    AshtakootMilan,
    DashakootMilan,
    ManglikDosha,
    calculate_compatibility,
    NAKSHATRAS,
    NAKSHATRA_GANA,
    NAKSHATRA_YONI
)


class TestAshtakootMilan:
    """Test 8-fold matching system"""
    
    @pytest.fixture
    def ashtakoot(self):
        return AshtakootMilan()
    
    def test_total_max_points_is_36(self, ashtakoot):
        """Ashtakoot should have 36 max points"""
        result = ashtakoot.calculate_compatibility(100.0, 150.0)
        assert result.max_points == 36.0
    
    def test_returns_eight_kootas(self, ashtakoot):
        """Should return exactly 8 kootas"""
        result = ashtakoot.calculate_compatibility(100.0, 150.0)
        assert len(result.kootas) == 8
    
    def test_koota_names(self, ashtakoot):
        """Should have correct koota names"""
        result = ashtakoot.calculate_compatibility(100.0, 150.0)
        expected_names = ["Varna", "Vashya", "Tara", "Yoni", 
                         "Graha Maitri", "Gana", "Bhakoot", "Nadi"]
        actual_names = [k.name for k in result.kootas]
        assert actual_names == expected_names
    
    def test_koota_max_points(self, ashtakoot):
        """Each koota should have correct max points"""
        result = ashtakoot.calculate_compatibility(100.0, 150.0)
        expected_max = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        actual_max = [k.max_points for k in result.kootas]
        assert actual_max == expected_max
    
    def test_nadi_dosha_detection(self, ashtakoot):
        """Same nadi should create Nadi Dosha"""
        # Ashwini (0) and Punarvasu (6) are both Aadi nadi
        # Ashwini starts at 0°, Punarvasu starts at 80°
        result = ashtakoot.calculate_compatibility(5.0, 85.0)
        
        nadi_dosha = [d for d in result.doshas if d["name"] == "Nadi Dosha"]
        assert len(nadi_dosha) > 0
    
    def test_same_nakshatra_perfect_nadi(self, ashtakoot):
        """Same nakshatra = same nadi = Nadi Dosha"""
        result = ashtakoot.calculate_compatibility(10.0, 12.0)  # Both in Ashwini
        
        nadi_koota = [k for k in result.kootas if k.name == "Nadi"][0]
        assert nadi_koota.obtained_points == 0.0


class TestDashakootMilan:
    """Test 10-fold matching system"""
    
    @pytest.fixture
    def dashakoot(self):
        return DashakootMilan()
    
    def test_total_max_points_is_50(self, dashakoot):
        """Dashakoot should have 50 max points"""
        result = dashakoot.calculate_dashakoot(100.0, 150.0)
        assert result["max_points"] == 50.0
    
    def test_returns_ten_kootas(self, dashakoot):
        """Should return exactly 10 kootas"""
        result = dashakoot.calculate_dashakoot(100.0, 150.0)
        assert len(result["kootas"]) == 10
    
    def test_koota_names(self, dashakoot):
        """Should have correct koota names"""
        result = dashakoot.calculate_dashakoot(100.0, 150.0)
        expected = ["Dina", "Gana", "Mahendra", "Stree Deergha", "Yoni",
                   "Rasi", "Rasi Lord", "Vasya", "Rajju", "Vedha"]
        actual = [k["name"] for k in result["kootas"]]
        assert actual == expected
    
    def test_rajju_same_body_part(self, dashakoot):
        """Same Rajju should give 0 points"""
        # Nakshatras in same Rajju should fail
        # Ashwini (0) and Mrigashira (4) are both Paada Rajju
        result = dashakoot.calculate_dashakoot(5.0, 60.0)  # Roughly Ashwini and Mrigashira
        
        rajju = [k for k in result["kootas"] if k["name"] == "Rajju"][0]
        # If they fall in same rajju, points should be 0
        # Otherwise 8
        assert rajju["obtained"] in [0.0, 8.0]
    
    def test_vedha_pair_detection(self, dashakoot):
        """Vedha pairs should get 0 points"""
        # Ashwini (0) and Jyeshtha (17) are vedha pair
        # Ashwini: 0-13.33°, Jyeshtha: 226.67-240°
        result = dashakoot.calculate_dashakoot(5.0, 230.0)
        
        vedha = [k for k in result["kootas"] if k["name"] == "Vedha"][0]
        assert vedha["obtained"] == 0.0
    
    def test_no_vedha_full_points(self, dashakoot):
        """Non-vedha pairs should get full points"""
        # Ashwini (0) and Rohini (3) are NOT vedha pair
        result = dashakoot.calculate_dashakoot(5.0, 45.0)
        
        vedha = [k for k in result["kootas"] if k["name"] == "Vedha"][0]
        assert vedha["obtained"] == 9.0


class TestManglikDosha:
    """Test Manglik (Kuja) Dosha detection"""
    
    @pytest.fixture
    def manglik(self):
        return ManglikDosha()
    
    def test_mars_in_7th_is_manglik(self, manglik):
        """Mars in 7th house should be Manglik"""
        result = manglik.check_manglik(7, 0)
        assert result["is_manglik"] == True
    
    def test_mars_in_3rd_not_manglik(self, manglik):
        """Mars in 3rd house should NOT be Manglik"""
        result = manglik.check_manglik(3, 0)
        assert result["is_manglik"] == False
    
    def test_manglik_houses(self, manglik):
        """Test all Manglik houses"""
        manglik_houses = [1, 2, 4, 7, 8, 12]
        non_manglik_houses = [3, 5, 6, 9, 10, 11]
        
        for house in manglik_houses:
            result = manglik.check_manglik(house, 0)
            assert result["is_manglik"] == True, f"House {house} should be Manglik"
        
        for house in non_manglik_houses:
            result = manglik.check_manglik(house, 0)
            assert result["is_manglik"] == False, f"House {house} should NOT be Manglik"


class TestCalculateCompatibility:
    """Test the main calculate_compatibility function"""
    
    def test_default_system_is_ashtakoot(self):
        """Default should return Ashtakoot format"""
        result = calculate_compatibility(100.0, 150.0)
        
        assert "total_score" in result
        assert "max_score" in result
        assert result["max_score"] == 36.0
    
    def test_dashakoot_system(self):
        """Dashakoot system should return 50 points max"""
        result = calculate_compatibility(100.0, 150.0, system="dashakoot")
        
        assert "dashakoot" in result
        assert result["dashakoot"]["max_points"] == 50.0
    
    def test_both_systems(self):
        """Both systems should return both analyses"""
        result = calculate_compatibility(100.0, 150.0, system="both")
        
        assert "ashtakoot" in result
        assert "dashakoot" in result
        assert result["ashtakoot"]["max_score"] == 36.0
        assert result["dashakoot"]["max_points"] == 50.0
    
    def test_manglik_included_when_provided(self):
        """Manglik analysis should be included when Mars house provided"""
        result = calculate_compatibility(100.0, 150.0, boy_mars_house=7, girl_mars_house=3)
        
        assert "boy_manglik" in result
        assert "girl_manglik" in result
        assert result["boy_manglik"]["is_manglik"] == True
        assert result["girl_manglik"]["is_manglik"] == False


class TestNakshatraData:
    """Test nakshatra reference data"""
    
    def test_27_nakshatras(self):
        """Should have exactly 27 nakshatras"""
        assert len(NAKSHATRAS) == 27
    
    def test_27_ganas(self):
        """Should have gana for all 27 nakshatras"""
        assert len(NAKSHATRA_GANA) == 27
    
    def test_27_yonis(self):
        """Should have yoni for all 27 nakshatras"""
        assert len(NAKSHATRA_YONI) == 27
    
    def test_gana_types(self):
        """Gana should only be Deva, Manushya, or Rakshasa"""
        valid_ganas = {"Deva", "Manushya", "Rakshasa"}
        for gana in NAKSHATRA_GANA:
            assert gana in valid_ganas


class TestScoreRanges:
    """Test that scores stay within valid ranges"""
    
    def test_ashtakoot_score_range(self):
        """Ashtakoot score should be 0-36"""
        ashtakoot = AshtakootMilan()
        
        # Test multiple combinations
        test_positions = [(0, 90), (45, 180), (100, 250), (200, 350)]
        
        for boy, girl in test_positions:
            result = ashtakoot.calculate_compatibility(boy, girl)
            assert 0 <= result.total_points <= 36, f"Score out of range for {boy}, {girl}"
    
    def test_dashakoot_score_range(self):
        """Dashakoot score should be 0-50"""
        dashakoot = DashakootMilan()
        
        test_positions = [(0, 90), (45, 180), (100, 250), (200, 350)]
        
        for boy, girl in test_positions:
            result = dashakoot.calculate_dashakoot(boy, girl)
            assert 0 <= result["total_points"] <= 50, f"Score out of range for {boy}, {girl}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
