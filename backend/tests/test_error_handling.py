"""
Error Handling Tests
==================
Tests for user-friendly error messages and validation.
"""

import pytest
from fastapi import HTTPException
from datetime import datetime, timezone

from app.core.errors.error_messages import ErrorMessages, ErrorCode, create_validation_error
from app.middleware.request_validator import (
    validate_date_format, validate_time_format, validate_coordinates,
    validate_timezone, validate_ayanamsa_system, validate_house_system,
    InputValidator
)


class TestErrorMessages:
    """Test error message generation"""
    
    def test_get_error_response(self):
        """Test error response generation"""
        response = ErrorMessages.get_error_response(ErrorCode.INVALID_DATE_FORMAT)
        
        assert response["error"] is True
        assert response["error_code"] == "INVALID_DATE_FORMAT"
        assert "message" in response
        assert "detail" in response
        assert "solution" in response
    
    def test_error_response_with_field(self):
        """Test error response with field information"""
        response = ErrorMessages.get_error_response(
            ErrorCode.INVALID_DATE_FORMAT,
            field="birth_date"
        )
        
        assert response["field"] == "birth_date"
    
    def test_format_validation_error(self):
        """Test validation error formatting"""
        error = ErrorMessages.format_validation_error(
            field="date",
            value="invalid-date",
            error_code=ErrorCode.INVALID_DATE_FORMAT
        )
        
        assert error["error"] is True
        assert error["field"] == "date"
        assert error["invalid_value"] == "invalid-date"


class TestValidationFunctions:
    """Test individual validation functions"""
    
    def test_validate_date_format_valid(self):
        """Test valid date formats"""
        assert validate_date_format("1990-10-09") is True
        assert validate_date_format("2000-01-01") is True
    
    def test_validate_date_format_invalid(self):
        """Test invalid date formats"""
        assert validate_date_format("10-09-1990") is False
        assert validate_date_format("1990/10/09") is False
        assert validate_date_format("invalid") is False
    
    def test_validate_time_format_valid(self):
        """Test valid time formats"""
        assert validate_time_format("14:30:00") is True
        assert validate_time_format("00:00:00") is True
        assert validate_time_format("23:59:59") is True
    
    def test_validate_time_format_invalid(self):
        """Test invalid time formats"""
        assert validate_time_format("14:30") is False
        assert validate_time_format("2:30 PM") is False
        assert validate_time_format("invalid") is False
    
    def test_validate_coordinates_valid(self):
        """Test valid coordinates"""
        assert validate_coordinates(28.6139, 77.2090) is True  # Delhi
        assert validate_coordinates(0, 0) is True
        assert validate_coordinates(-33.8688, 151.2093) is True  # Sydney
    
    def test_validate_coordinates_invalid(self):
        """Test invalid coordinates"""
        assert validate_coordinates(100, 0) is False  # Lat > 90
        assert validate_coordinates(0, 200) is False  # Lon > 180
        assert validate_coordinates(-100, 0) is False  # Lat < -90
    
    def test_validate_timezone_valid(self):
        """Test valid timezones"""
        assert validate_timezone("Asia/Kolkata") is True
        assert validate_timezone("America/New_York") is True
        assert validate_timezone("UTC") is True
    
    def test_validate_timezone_invalid(self):
        """Test invalid timezones"""
        assert validate_timezone("Invalid/Timezone") is False
        assert validate_timezone("Not_A_Real_TZ") is False
    
    def test_validate_ayanamsa_system_valid(self):
        """Test valid ayanamsa systems"""
        assert validate_ayanamsa_system("lahiri") is True
        assert validate_ayanamsa_system("kp") is True
        assert validate_ayanamsa_system("RAMAN") is True  # Case insensitive
    
    def test_validate_ayanamsa_system_invalid(self):
        """Test invalid ayanamsa systems"""
        assert validate_ayanamsa_system("invalid") is False
    
    def test_validate_house_system_valid(self):
        """Test valid house systems"""
        assert validate_house_system("W") is True  # Whole Sign
        assert validate_house_system("P") is True  # Placidus
        assert validate_house_system("w") is True  # Case insensitive
    
    def test_validate_house_system_invalid(self):
        """Test invalid house systems"""
        assert validate_house_system("X") is False


class TestInputValidator:
    """Test comprehensive input validator"""
    
    def test_validate_valid_chart_request(self):
        """Test validation of valid chart request"""
        data = {
            "date": "1990-10-09",
            "time": "14:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata",
            "ayanamsa": "lahiri",
            "house_system": "W"
        }
        
        result = InputValidator.validate_chart_request(data)
        assert result["valid"] is True
    
    def test_validate_invalid_date(self):
        """Test validation catches invalid date"""
        data = {
            "date": "invalid-date",
            "time": "14:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata"
        }
        
        with pytest.raises(HTTPException) as exc_info:
            InputValidator.validate_chart_request(data)
        
        assert exc_info.value.status_code == 422
        assert "validation_errors" in exc_info.value.detail["type"]
    
    def test_validate_invalid_coordinates(self):
        """Test validation catches invalid coordinates"""
        data = {
            "date": "1990-10-09",
            "time": "14:30:00",
            "latitude": 100,  # Invalid
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata"
        }
        
        with pytest.raises(HTTPException):
            InputValidator.validate_chart_request(data)
    
    def test_validate_future_date(self):
        """Test validation catches future date"""
        future_date = datetime.now().strftime("%Y-%m-%d")
        # Add a day to make it future (this is a simplified test)
        
        data = {
            "date": "2099-12-31",  # Definitely future
            "time": "14:30:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata"
        }
        
        with pytest.raises(HTTPException):
            InputValidator.validate_chart_request(data)


class TestErrorResponseStructure:
    """Test error response structure consistency"""
    
    def test_all_error_codes_have_messages(self):
        """Test all error codes have defined messages"""
        for error_code in ErrorCode:
            assert error_code in ErrorMessages.MESSAGES
            message_data = ErrorMessages.MESSAGES[error_code]
            assert "message" in message_data
            assert "detail" in message_data
            assert "solution" in message_data
    
    def test_validation_error_structure(self):
        """Test validation error has consistent structure"""
        error = create_validation_error(
            field="test_field",
            value="test_value",
            error_type="test_error",
            expected_format="YYYY-MM-DD"
        )
        
        assert error["error"] is True
        assert error["type"] == "validation_error"
        assert error["field"] == "test_field"
        assert error["value"] == "test_value"
        assert error["error_type"] == "test_error"
        assert error["expected_format"] == "YYYY-MM-DD"
