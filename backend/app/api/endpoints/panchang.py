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
        # Ensure all parameters are correct types
        lat = float(request.latitude)
        lon = float(request.longitude)
        
        # Calculate using simpler approach: find when Sun altitude crosses horizon
        # Search for sunrise around 6am local time
        jd_sunrise = jd0 + 0.25  # 6am UTC
        # Calculate Sun's position
        sun_pos = swe.calc_ut(jd_sunrise, swe.SUN, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)[0]
        
        # For more accurate sunrise/sunset, iterate to find horizon crossing
        # Simplified: use approximate calculation based on Sun's declination
        # This is a basic implementation - production should use swe.rise_trans correctly
        
        # Rough sunrise/sunset calculation
        # Hour angle at sunrise: cos(H) = -tan(lat)*tan(decl)
        sun_ecl = swe.calc_ut(jd0 + 0.5, swe.SUN, swe.FLG_SWIEPH)[0]  # noon position
        sun_lon = sun_ecl[0]
        # Convert to equatorial
        sun_eq = swe.calc_ut(jd0 + 0.5, swe.SUN, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)[0]
        decl = sun_eq[1] * math.pi / 180.0  # declination in radians
        lat_rad = lat * math.pi / 180.0
        
        # Hour angle calculation (simplified, ignores refraction and sun's radius)
        cos_h = -math.tan(lat_rad) * math.tan(decl)
        if cos_h < -1:
            # Midnight sun
            h_angle = math.pi
        elif cos_h > 1:
            # Polar night
            h_angle = 0
        else:
            h_angle = math.acos(cos_h)
        
        # Convert hour angle to time
        sunrise_hour = 12.0 - (h_angle * 180.0 / math.pi) / 15.0 - lon / 15.0
        sunset_hour = 12.0 + (h_angle * 180.0 / math.pi) / 15.0 - lon / 15.0
        
        # Build datetime objects from calculated JD
        sr_jd = jd0 + sunrise_hour / 24.0
        ss_jd = jd0 + sunset_hour / 24.0
        
        # Convert JD to datetime
        y, m, day, ut = swe.revjul(sr_jd)
        hr = int(ut)
        mi = int((ut - hr) * 60)
        sec_float = ((ut - hr) * 60 - mi) * 60
        se = min(59, max(0, int(round(sec_float))))  # Clamp to 0-59
        sunrise = datetime(int(round(y)), int(round(m)), int(round(day)), hr, mi, se)
        
        y2, m2, day2, ut2 = swe.revjul(ss_jd)
        hr2 = int(ut2)
        mi2 = int((ut2 - hr2) * 60)
        sec_float2 = ((ut2 - hr2) * 60 - mi2) * 60
        se2 = min(59, max(0, int(round(sec_float2))))  # Clamp to 0-59
        sunset = datetime(int(round(y2)), int(round(m2)), int(round(day2)), hr2, mi2, se2)
        
        return SunTimesResponse(sunrise_utc=sunrise, sunset_utc=sunset)
    except Exception as e:
        import traceback
        raise HTTPException(status_code=400, detail=f"Error calculating sun times: {str(e)}\n{traceback.format_exc()}")
