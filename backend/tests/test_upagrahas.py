"""
Tests for Upagraha (Sub-Planet) Calculations
"""
import pytest
from datetime import datetime, timedelta
from app.core.calculations.upagrahas import UpagrahaCalculator


class TestUpagrahaCalculations:
    """Test upagraha calculation accuracy"""
    
    def test_dhuma_calculation(self):
        """Test Dhuma (Smoke) calculation from Sun"""
        # Sun at 172.5° (Virgo)
        sun_longitude = 172.5
        dhuma = UpagrahaCalculator.calculate_dhuma(sun_longitude)
        
        # Dhuma = Sun + 133°20' = 172.5 + 133.333 = 305.833° (Aquarius)
        expected = (172.5 + 133.333333) % 360
        assert abs(dhuma - expected) < 0.01, f"Dhuma should be {expected}°, got {dhuma}°"
        
        # Verify sign
        sign, sign_num = UpagrahaCalculator.get_upagraha_sign(dhuma)
        assert sign == "Aquarius", f"Dhuma should be in Aquarius, got {sign}"
    
    def test_vyatipata_calculation(self):
        """Test Vyatipata (Calamity) calculation"""
        dhuma = 305.833
        vyatipata = UpagrahaCalculator.calculate_vyatipata(dhuma)
        
        # Vyatipata = 360° - Dhuma
        expected = (360 - dhuma) % 360
        assert abs(vyatipata - expected) < 0.01
    
    def test_parivesha_calculation(self):
        """Test Parivesha (Halo) calculation"""
        vyatipata = 54.167
        parivesha = UpagrahaCalculator.calculate_parivesha(vyatipata)
        
        # Parivesha = Vyatipata + 180°
        expected = (vyatipata + 180) % 360
        assert abs(parivesha - expected) < 0.01
    
    def test_indrachapa_calculation(self):
        """Test Indrachapa (Rainbow) calculation"""
        parivesha = 234.167
        indrachapa = UpagrahaCalculator.calculate_indrachapa(parivesha)
        
        # Indrachapa = 360° - Parivesha
        expected = (360 - parivesha) % 360
        assert abs(indrachapa - expected) < 0.01
    
    def test_upaketu_calculation(self):
        """Test Upaketu (Secondary Ketu) calculation"""
        indrachapa = 125.833
        upaketu = UpagrahaCalculator.calculate_upaketu(indrachapa)
        
        # Upaketu = Indrachapa + 16°40'
        expected = (indrachapa + 16.666667) % 360
        assert abs(upaketu - expected) < 0.01
    
    def test_upagraha_chain(self):
        """Test the complete chain of primary upagrahas"""
        sun = 172.5  # Virgo
        
        dhuma = UpagrahaCalculator.calculate_dhuma(sun)
        vyatipata = UpagrahaCalculator.calculate_vyatipata(dhuma)
        parivesha = UpagrahaCalculator.calculate_parivesha(vyatipata)
        indrachapa = UpagrahaCalculator.calculate_indrachapa(parivesha)
        upaketu = UpagrahaCalculator.calculate_upaketu(indrachapa)
        
        # Verify all are valid longitudes
        for name, value in [
            ('Dhuma', dhuma),
            ('Vyatipata', vyatipata),
            ('Parivesha', parivesha),
            ('Indrachapa', indrachapa),
            ('Upaketu', upaketu)
        ]:
            assert 0 <= value < 360, f"{name} longitude {value}° out of range"
    
    def test_mandi_calculation(self):
        """Test Mandi (Son of Saturn) calculation"""
        saturn = 309.2  # Capricorn
        mandi = UpagrahaCalculator.calculate_mandi(saturn)
        
        # Mandi = Saturn + 133°20'
        expected = (saturn + 133.333333) % 360
        assert abs(mandi - expected) < 0.01
    
    def test_kala_calculation(self):
        """Test Kala (Time) calculation"""
        sun = 172.5
        kala = UpagrahaCalculator.calculate_kala(sun)
        
        # Kala = Sun + 220°
        expected = (sun + 220) % 360
        assert abs(kala - expected) < 0.01
    
    def test_mrityu_calculation(self):
        """Test Mrityu (Death) calculation"""
        sun = 172.5
        mrityu = UpagrahaCalculator.calculate_mrityu(sun)
        
        # Mrityu = Sun + 237°30'
        expected = (sun + 237.5) % 360
        assert abs(mrityu - expected) < 0.01
    
    def test_ardhaprahara_calculation(self):
        """Test Ardhaprahara (Half Watch) calculation"""
        sun = 172.5
        ardhaprahara = UpagrahaCalculator.calculate_ardhaprahara(sun)
        
        # Ardhaprahara = Sun + 255°
        expected = (sun + 255) % 360
        assert abs(ardhaprahara - expected) < 0.01
    
    def test_calculate_all_upagrahas(self):
        """Test calculating all upagrahas at once"""
        sun = 172.5
        saturn = 309.2
        
        upagrahas = UpagrahaCalculator.calculate_all_upagrahas(
            sun_longitude=sun,
            saturn_longitude=saturn
        )
        
        # Verify all expected upagrahas are present
        expected_upagrahas = [
            'Dhuma', 'Vyatipata', 'Parivesha', 'Indrachapa', 'Upaketu',
            'Kala', 'Mrityu', 'Ardhaprahara', 'Mandi'
        ]
        
        for name in expected_upagrahas:
            assert name in upagrahas, f"{name} not in results"
            assert 0 <= upagrahas[name] < 360, f"{name} longitude out of range"
    
    def test_format_upagraha_positions(self):
        """Test formatting upagraha positions with sign info"""
        upagrahas = {
            'Dhuma': 305.833,
            'Vyatipata': 54.167
        }
        
        formatted = UpagrahaCalculator.format_upagraha_positions(upagrahas)
        
        # Verify Dhuma formatting
        assert 'Dhuma' in formatted
        dhuma_info = formatted['Dhuma']
        assert dhuma_info['sign'] == 'Aquarius'
        assert dhuma_info['sign_num'] == 11
        assert 'formatted' in dhuma_info
        
        # Verify Vyatipata formatting
        assert 'Vyatipata' in formatted
        vyat_info = formatted['Vyatipata']
        assert vyat_info['sign'] == 'Taurus'
        assert vyat_info['sign_num'] == 2
    
    def test_edge_cases(self):
        """Test edge cases for longitude wrapping"""
        # Test at 360° boundary
        sun_at_end = 359.5
        dhuma = UpagrahaCalculator.calculate_dhuma(sun_at_end)
        assert 0 <= dhuma < 360
        
        # Test at 0°
        sun_at_start = 0.5
        dhuma2 = UpagrahaCalculator.calculate_dhuma(sun_at_start)
        assert 0 <= dhuma2 < 360
    
    def test_get_upagraha_sign(self):
        """Test zodiac sign determination"""
        test_cases = [
            (0, "Aries", 1),
            (30, "Taurus", 2),
            (60, "Gemini", 3),
            (90, "Cancer", 4),
            (120, "Leo", 5),
            (150, "Virgo", 6),
            (180, "Libra", 7),
            (210, "Scorpio", 8),
            (240, "Sagittarius", 9),
            (270, "Capricorn", 10),
            (300, "Aquarius", 11),
            (330, "Pisces", 12),
            (359, "Pisces", 12),
        ]
        
        for longitude, expected_sign, expected_num in test_cases:
            sign, num = UpagrahaCalculator.get_upagraha_sign(longitude)
            assert sign == expected_sign, f"At {longitude}°: expected {expected_sign}, got {sign}"
            assert num == expected_num, f"At {longitude}°: expected sign #{expected_num}, got #{num}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
