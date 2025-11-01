"""Panchang calculation endpoints."""
from typing import Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import math
import swisseph as swe

router = APIRouter()

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

YOGAS = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti"
]

class PanchangRequest(BaseModel):
    """Request model for Panchang calculation."""
    date_time: datetime = Field(..., description="Date and time in UTC")

class PanchangResponse(BaseModel):
    tithi_number: int
    tithi_elapsed: float
    nakshatra_name: str
    nakshatra_number: int
    nakshatra_pada: int
    yoga_name: str
    yoga_number: int
    karana_number: int

class SunTimesRequest(BaseModel):
    date: datetime = Field(..., description="Date in UTC (time ignored; sunrise/sunset computed for that day)")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")

class SunTimesResponse(BaseModel):
    sunrise_utc: datetime
    sunset_utc: datetime

@router.post("/calculate", response_model=PanchangResponse)
async def calculate_panchang(request: PanchangRequest):
    """
    Calculate tithi, nakshatra, yoga, and karana for the given datetime (UTC).
    """
    try:
        dt = request.date_time
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 + dt.second / 3600.0)
        # Solar and Lunar longitudes (geocentric)
        sun = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)[0]
        moon = swe.calc_ut(jd, swe.MOON, swe.FLG_SWIEPH)[0]
        sun_lon = sun[0] % 360
        moon_lon = moon[0] % 360

        # Tithi
        diff = (moon_lon - sun_lon) % 360.0
        tithi_number = int(diff // 12.0) + 1  # 1..30
        tithi_elapsed = (diff % 12.0) / 12.0  # 0..1 fraction

        # Nakshatra (Moon)
        nak_len = 360.0 / 27.0
        nak_num0 = int(moon_lon // nak_len)
        nak_pada = int(((moon_lon % nak_len) / (nak_len / 4.0))) + 1
        nak_name = NAKSHATRAS[nak_num0]

        # Yoga (Sun + Moon)
        s_plus_m = (sun_lon + moon_lon) % 360.0
        yoga_num0 = int(s_plus_m // nak_len)
        yoga_name = YOGAS[yoga_num0]

        # Karana (half tithi)
        karana_number = int(diff // 6.0) + 1  # 1..60 cyclic (simplified)

        return PanchangResponse(
            tithi_number=tithi_number,
            tithi_elapsed=round(tithi_elapsed, 4),
            nakshatra_name=nak_name,
            nakshatra_number=nak_num0 + 1,
            nakshatra_pada=nak_pada,
            yoga_name=yoga_name,
            yoga_number=yoga_num0 + 1,
            karana_number=karana_number,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating Panchang: {str(e)}")

@router.post("/sun_times", response_model=SunTimesResponse)
async def calculate_sun_times(request: SunTimesRequest):
    """
    Calculate sunrise and sunset UTC for a given date and location.
    """
    try:
        d = request.date
        jd0 = swe.julday(d.year, d.month, d.day, 0.0)
        flags_rise = swe.CALC_RISE | swe.BIT_DISC_CENTER
        flags_set = swe.CALC_SET | swe.BIT_DISC_CENTER
        # Returns (retflag, (tret0, tret1, tret2, tret3))
        sr = swe.rise_trans(jd0, swe.SUN, request.longitude, request.latitude, flags_rise)
        ss = swe.rise_trans(jd0, swe.SUN, request.longitude, request.latitude, flags_set)
        sr_jd = sr[1][0]
        ss_jd = ss[1][0]
        y, m, day, ut = swe.revjul(sr_jd, swe.GREG_CAL)
        hr = int(ut)
        mi = int((ut - hr) * 60)
        se = int(round((((ut - hr) * 60) - mi) * 60))
        sunrise = datetime(int(y), int(m), int(day), hr, mi, se)
        y2, m2, day2, ut2 = swe.revjul(ss_jd, swe.GREG_CAL)
        hr2 = int(ut2)
        mi2 = int((ut2 - hr2) * 60)
        se2 = int(round((((ut2 - hr2) * 60) - mi2) * 60))
        sunset = datetime(int(y2), int(m2), int(day2), hr2, mi2, se2)
        return SunTimesResponse(sunrise_utc=sunrise, sunset_utc=sunset)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating sun times: {str(e)}")
