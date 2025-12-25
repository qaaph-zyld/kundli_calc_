"""
Request Validation Middleware
=============================
Validates incoming requests and provides helpful error messages.
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Callable
import logging
from datetime import datetime
import pytz

from app.core.errors.error_messages import ErrorMessages, ErrorCode

logger = logging.getLogger(__name__)


class RequestValidationMiddleware:
    """Middleware for validating and enriching requests"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Validate request here if needed
        await self.app(scope, receive, send)


def validate_date_format(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_time_format(time_str: str) -> bool:
    """Validate time format (HH:MM:SS)"""
    try:
        datetime.strptime(time_str, "%H:%M:%S")
        return True
    except ValueError:
        return False


def validate_datetime_format(datetime_str: str) -> bool:
    """Validate ISO datetime format"""
    try:
        datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate geographic coordinates"""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def validate_timezone(timezone_str: str) -> bool:
    """Validate timezone identifier"""
    try:
        pytz.timezone(timezone_str)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False


def validate_ayanamsa_system(system: str) -> bool:
    """Validate ayanamsa system"""
    valid_systems = [
        'lahiri', 'raman', 'kp', 'yukteshwar',
        'true_chitra', 'fagan_bradley', 'deluce', 'sassanian'
    ]
    return system.lower() in valid_systems


def validate_house_system(system: str) -> bool:
    """Validate house system"""
    valid_systems = ['W', 'P', 'K', 'E', 'B', 'O', 'R', 'C', 'A', 'V', 'H']
    return system.upper() in valid_systems


def validate_birth_date_not_future(date_str: str) -> bool:
    """Validate birth date is not in the future"""
    try:
        birth_date = datetime.strptime(date_str, "%Y-%m-%d")
        return birth_date <= datetime.now()
    except ValueError:
        return False


class InputValidator:
    """Comprehensive input validator"""
    
    @staticmethod
    def validate_chart_request(data: dict) -> dict:
        """
        Validate chart calculation request
        
        Args:
            data: Request data dictionary
            
        Returns:
            Validation result with errors if any
            
        Raises:
            HTTPException: If validation fails
        """
        errors = []
        
        # Validate date
        if 'date' in data or 'date_time' in data:
            date_field = 'date' if 'date' in data else 'date_time'
            date_value = data[date_field]
            
            if isinstance(date_value, str):
                if 'T' in date_value or 'Z' in date_value:
                    # ISO format
                    if not validate_datetime_format(date_value):
                        errors.append(
                            ErrorMessages.format_validation_error(
                                date_field, date_value, ErrorCode.INVALID_DATE_FORMAT,
                                "Expected ISO format: YYYY-MM-DDTHH:MM:SSZ"
                            )
                        )
                else:
                    # Simple date format
                    if not validate_date_format(date_value):
                        errors.append(
                            ErrorMessages.format_validation_error(
                                date_field, date_value, ErrorCode.INVALID_DATE_FORMAT
                            )
                        )
                    elif not validate_birth_date_not_future(date_value):
                        errors.append(
                            ErrorMessages.format_validation_error(
                                date_field, date_value, ErrorCode.FUTURE_DATE
                            )
                        )
        
        # Validate time
        if 'time' in data:
            time_value = data['time']
            if not validate_time_format(time_value):
                errors.append(
                    ErrorMessages.format_validation_error(
                        'time', time_value, ErrorCode.INVALID_TIME_FORMAT
                    )
                )
        
        # Validate coordinates
        if 'latitude' in data and 'longitude' in data:
            lat = data['latitude']
            lon = data['longitude']
            if not validate_coordinates(lat, lon):
                errors.append(
                    ErrorMessages.format_validation_error(
                        'coordinates', f"lat={lat}, lon={lon}",
                        ErrorCode.INVALID_COORDINATES
                    )
                )
        
        # Validate timezone
        if 'timezone' in data:
            tz = data['timezone']
            if not validate_timezone(tz):
                errors.append(
                    ErrorMessages.format_validation_error(
                        'timezone', tz, ErrorCode.INVALID_TIMEZONE
                    )
                )
        
        # Validate ayanamsa
        if 'ayanamsa' in data:
            ayanamsa = data['ayanamsa']
            if isinstance(ayanamsa, str) and not validate_ayanamsa_system(ayanamsa):
                errors.append(
                    ErrorMessages.format_validation_error(
                        'ayanamsa', ayanamsa, ErrorCode.INVALID_AYANAMSA
                    )
                )
        
        # Validate house system
        if 'house_system' in data:
            house_sys = data['house_system']
            if not validate_house_system(house_sys):
                errors.append(
                    ErrorMessages.format_validation_error(
                        'house_system', house_sys, ErrorCode.INVALID_HOUSE_SYSTEM
                    )
                )
        
        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": True,
                    "type": "validation_errors",
                    "errors": errors,
                    "message": "Request validation failed"
                }
            )
        
        return {"valid": True}


async def validation_exception_handler(request: Request, exc: HTTPException):
    """Handle validation exceptions with user-friendly messages"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail if isinstance(exc.detail, dict) else {
            "error": True,
            "message": str(exc.detail)
        }
    )
