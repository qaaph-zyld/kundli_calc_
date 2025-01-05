"""
Request Validation Module
PGF Protocol: VAL_002
Gate: GATE_2
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
import pytz
from app.models.location import Location

class AyanamsaSystem(str, Enum):
    LAHIRI = "lahiri"
    RAMAN = "raman"
    KP = "krishnamurti"
    FAGAN_BRADLEY = "fagan_bradley"
    TROPICAL = "tropical"

class HouseSystem(str, Enum):
    PLACIDUS = "placidus"
    KOCH = "koch"
    EQUAL = "equal"
    WHOLE_SIGN = "whole_sign"
    REGIOMONTANUS = "regiomontanus"
    CAMPANUS = "campanus"

class ChartType(str, Enum):
    RASI = "rasi"
    NAVAMSA = "navamsa"
    HORA = "hora"
    DREKKANA = "drekkana"
    CHATURTHAMSA = "chaturthamsa"
    SAPTAMSA = "saptamsa"
    DASAMSA = "dasamsa"
    DWADASAMSA = "dwadasamsa"

class CalculationType(str, Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    ADVANCED = "advanced"

class KundliRequest(BaseModel):
    """Base model for Kundli calculation requests"""
    date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    time: str = Field(..., description="Birth time in HH:MM:SS format")
    latitude: float = Field(..., description="Latitude in decimal degrees", ge=-90, le=90)
    longitude: float = Field(..., description="Longitude in decimal degrees", ge=-180, le=180)
    timezone: str = Field(..., description="Timezone name (e.g., 'Asia/Kolkata')")
    ayanamsa: AyanamsaSystem = Field(
        default=AyanamsaSystem.LAHIRI,
        description="Ayanamsa system to use"
    )
    house_system: HouseSystem = Field(
        default=HouseSystem.PLACIDUS,
        description="House system to use"
    )
    chart_types: List[ChartType] = Field(
        default=[ChartType.RASI],
        description="Types of charts to calculate"
    )
    calculation_type: CalculationType = Field(
        default=CalculationType.BASIC,
        description="Level of calculation detail"
    )
    language: str = Field(
        default="en",
        description="Language for predictions and interpretations"
    )

    @validator("date")
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

    @validator("time")
    def validate_time(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM:SS")

    @validator("timezone")
    def validate_timezone(cls, v: str) -> str:
        try:
            pytz.timezone(v)
            return v
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Unknown timezone: {v}")

    def to_datetime(self) -> datetime:
        """Convert date and time to datetime object"""
        dt_str = f"{self.date} {self.time}"
        naive_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        tz = pytz.timezone(self.timezone)
        return tz.localize(naive_dt)

    def to_location(self) -> Location:
        """Convert coordinates to Location object"""
        return Location(
            latitude=self.latitude,
            longitude=self.longitude
        )

class TransitRequest(KundliRequest):
    """Model for transit calculations"""
    transit_date: str = Field(..., description="Transit date in YYYY-MM-DD format")
    transit_time: str = Field(..., description="Transit time in HH:MM:SS format")
    
    @validator("transit_date")
    def validate_transit_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid transit date format. Use YYYY-MM-DD")
    
    @validator("transit_time")
    def validate_transit_time(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Invalid transit time format. Use HH:MM:SS")
    
    def to_transit_datetime(self) -> datetime:
        """Convert transit date and time to datetime object"""
        dt_str = f"{self.transit_date} {self.transit_time}"
        naive_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        tz = pytz.timezone(self.timezone)
        return tz.localize(naive_dt)

class MatchingRequest(BaseModel):
    """Model for compatibility matching requests"""
    person1: KundliRequest
    person2: KundliRequest
    match_factors: Optional[List[str]] = Field(
        default=["ashtakoot", "dashakoot", "guna_milan"],
        description="Factors to consider for matching"
    )

class PredictionRequest(KundliRequest):
    """Model for prediction requests"""
    prediction_start: Optional[str] = Field(
        None,
        description="Start date for predictions (YYYY-MM-DD)"
    )
    prediction_end: Optional[str] = Field(
        None,
        description="End date for predictions (YYYY-MM-DD)"
    )
    domains: Optional[List[str]] = Field(
        default=["general", "career", "relationship", "health", "finance"],
        description="Domains for predictions"
    )

    @validator("prediction_start")
    def validate_prediction_start(cls, v: Optional[str]) -> Optional[str]:
        if v:
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Invalid prediction start date format. Use YYYY-MM-DD")
        return v

    @validator("prediction_end")
    def validate_prediction_end(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        if v:
            try:
                end_date = datetime.strptime(v, "%Y-%m-%d")
                if "prediction_start" in values and values["prediction_start"]:
                    start_date = datetime.strptime(values["prediction_start"], "%Y-%m-%d")
                    if end_date <= start_date:
                        raise ValueError("Prediction end date must be after start date")
                return v
            except ValueError as e:
                if str(e) == "Prediction end date must be after start date":
                    raise
                raise ValueError("Invalid prediction end date format. Use YYYY-MM-DD")
        return v

class DashaRequest(KundliRequest):
    """Model for dasha period calculations"""
    dasha_system: str = Field(
        default="vimshottari",
        description="Dasha system to use"
    )
    levels: int = Field(
        default=2,
        description="Number of dasha levels to calculate",
        ge=1,
        le=4
    )

class MuhurtaRequest(BaseModel):
    """Model for muhurta calculations"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    activity_type: str = Field(..., description="Type of activity")
    location: Location
    timezone: str = Field(..., description="Timezone name")
    duration_hours: Optional[float] = Field(
        None,
        description="Required duration in hours",
        gt=0
    )

    @validator("date")
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
