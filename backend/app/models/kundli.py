from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum

class AyanamsaType(str, Enum):
    LAHIRI = "lahiri"
    RAMAN = "raman"
    KP = "krishnamurti"
    TROPICAL = "tropical"

class HouseSystem(str, Enum):
    PLACIDUS = "placidus"
    KOCH = "koch"
    EQUAL = "equal"
    WHOLE_SIGN = "whole_sign"

class ChartType(str, Enum):
    RASI = "rasi"
    NAVAMSA = "navamsa"
    DASHAMSA = "dashamsa"

class Planet(BaseModel):
    name: str
    longitude: float
    latitude: Optional[float]
    speed: Optional[float]
    house: int
    sign: str
    nakshatra: str
    nakshatra_pada: int
    is_retrograde: bool

class House(BaseModel):
    number: int
    sign: str
    degree: float
    planets: List[str] = []

class KundliChart(BaseModel):
    type: ChartType
    houses: List[House]
    planets: List[Planet]

class KundliRequest(BaseModel):
    date: datetime
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str
    ayanamsa: AyanamsaType = AyanamsaType.LAHIRI
    house_system: HouseSystem = HouseSystem.PLACIDUS
    chart_types: List[ChartType] = [ChartType.RASI]
    language: Optional[str] = "en"

    @validator('date')
    def validate_date(cls, v):
        if v > datetime.now():
            raise ValueError("Birth date cannot be in the future")
        return v

class KundliResponse(BaseModel):
    request: KundliRequest
    charts: List[KundliChart]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    id: str

class Prediction(BaseModel):
    category: str
    description: str
    strength: float  # 0 to 1
    time_period: Optional[str]
    planets_involved: List[str]
    houses_involved: List[int]

class KundliPredictions(BaseModel):
    kundli_id: str
    predictions: List[Prediction]
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class TransitRequest(BaseModel):
    birth_kundli_id: str
    transit_date: datetime
    chart_types: List[ChartType] = [ChartType.RASI]

class TransitResponse(BaseModel):
    birth_kundli: KundliResponse
    transit_charts: List[KundliChart]
    aspects: List[dict]  # Define detailed aspect structure
    predictions: List[Prediction]

class MatchingRequest(BaseModel):
    kundli1_id: str
    kundli2_id: str
    match_factors: Optional[List[str]] = None

class MatchingResponse(BaseModel):
    kundli1: KundliResponse
    kundli2: KundliResponse
    total_score: float  # 0 to 36 points
    factor_scores: dict  # Individual scores for each factor
    compatibility_report: List[dict]  # Detailed analysis
    recommendations: List[str]
