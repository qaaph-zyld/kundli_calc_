# JHora Reference Charts

This directory contains reference chart data exported from Jagannatha Hora (JHora) for accuracy validation.

## Purpose

These reference charts serve as the "ground truth" for validating our calculation accuracy. JHora is considered the gold standard for Vedic astrology calculations.

## How to Generate Reference Charts

### Prerequisites
- Jagannatha Hora software installed
- Set preferences to:
  - Ayanamsa: Lahiri (Chitrapaksha)
  - House System: Whole Sign
  - Time zone: Proper timezone for birth location

### Steps

1. **Open JHora**

2. **Enter Birth Data**
   - File → New Chart (or press F2)
   - Enter:
     - Name: Test Chart 1 (or descriptive name)
     - Date: YYYY-MM-DD
     - Time: HH:MM:SS
     - Place: Select from database or enter coordinates
     - Timezone: Select appropriate timezone

3. **Verify Settings**
   - Options → Preferences
   - Ayanamsa tab: Select "Lahiri"
   - Horoscopes tab: Default house system = "Whole Sign"

4. **Export Planet Positions**
   - View → Planetary Positions (or press F5)
   - Note down for each planet:
     - Tropical longitude
     - Sidereal longitude
     - Sign
     - Degree within sign
     - House
     - Retrograde status

5. **Export House Cusps**
   - View → Houses
   - Note down all 12 house cusps

6. **Export Dasha Periods**
   - View → Vimshottari Dasha (or press F6)
   - Note current mahadasha and antardasha
     - Planet name
     - Start date
     - End date
     - Balance at birth

7. **Export Yogas** (Optional)
   - View → Yogas
   - List active yogas

8. **Create JSON File**
   - Use template below
   - Save as `chart_<number>_<name>.json`
   - Example: `chart_001_leo_ascendant.json`

## JSON Template

```json
{
  "chart_info": {
    "name": "Test Chart 1",
    "description": "Leo ascendant, strong Sun",
    "source": "JHora v8.0",
    "validated_date": "2026-01-10"
  },
  "birth_data": {
    "datetime": "1990-05-15 10:30:00",
    "timezone": "Asia/Kolkata",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "place_name": "New Delhi, India"
  },
  "settings": {
    "ayanamsa": "Lahiri",
    "ayanamsa_value": 23.6512,
    "house_system": "Whole Sign"
  },
  "planets": {
    "Sun": {
      "tropical_longitude": 54.2345,
      "sidereal_longitude": 30.5833,
      "sign": "Taurus",
      "degree_in_sign": 0.5833,
      "house": 10,
      "nakshatra": "Krittika",
      "nakshatra_pada": 1,
      "retrograde": false
    },
    "Moon": {
      "tropical_longitude": 255.1234,
      "sidereal_longitude": 231.4722,
      "sign": "Scorpio",
      "degree_in_sign": 21.4722,
      "house": 4,
      "nakshatra": "Jyeshtha",
      "nakshatra_pada": 2,
      "retrograde": false
    },
    "Mars": {
      "tropical_longitude": 12.5678,
      "sidereal_longitude": 348.9166,
      "sign": "Pisces",
      "degree_in_sign": 28.9166,
      "house": 8,
      "nakshatra": "Revati",
      "nakshatra_pada": 4,
      "retrograde": false
    }
    // ... Add all 9 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
  },
  "houses": {
    "1": {"sign": "Leo", "cusp": 120.0},
    "2": {"sign": "Virgo", "cusp": 150.0},
    "3": {"sign": "Libra", "cusp": 180.0},
    "4": {"sign": "Scorpio", "cusp": 210.0},
    "5": {"sign": "Sagittarius", "cusp": 240.0},
    "6": {"sign": "Capricorn", "cusp": 270.0},
    "7": {"sign": "Aquarius", "cusp": 300.0},
    "8": {"sign": "Pisces", "cusp": 330.0},
    "9": {"sign": "Aries", "cusp": 0.0},
    "10": {"sign": "Taurus", "cusp": 30.0},
    "11": {"sign": "Gemini", "cusp": 60.0},
    "12": {"sign": "Cancer", "cusp": 90.0}
  },
  "dashas": {
    "current_mahadasha": {
      "planet": "Sun",
      "start": "1989-03-15",
      "end": "1995-03-15",
      "duration_years": 6
    },
    "current_antardasha": {
      "planet": "Mercury",
      "start": "1989-03-15",
      "end": "1989-08-01",
      "duration_months": 5.4
    },
    "balance_at_birth": {
      "mahadasha": "Sun",
      "years": 4,
      "months": 10,
      "days": 0
    }
  },
  "yogas": [
    {
      "name": "Gaja Kesari",
      "planets": ["Jupiter", "Moon"],
      "houses": [9, 4],
      "strength": "Strong"
    },
    {
      "name": "Budha Aditya",
      "planets": ["Mercury", "Sun"],
      "houses": [10, 10],
      "strength": "Moderate"
    }
  ],
  "divisional_charts": {
    "D9_navamsa": {
      "ascendant_sign": "Sagittarius",
      "ascendant_degree": 240.5,
      "planets": {
        "Sun": {"sign": "Pisces", "degree": 345.2},
        "Moon": {"sign": "Gemini", "degree": 75.8}
        // ... all planets in D9
      }
    }
  }
}
```

## Recommended Test Charts

Create at least 3 reference charts with variety:

1. **Chart 1**: Common ascendant (Leo/Aries/Sagittarius)
2. **Chart 2**: Retrograde planets present
3. **Chart 3**: Multiple yogas active
4. **Chart 4**: Unusual planetary configurations
5. **Chart 5**: Your own birth chart (known data)

## Validation Tolerance

- **Planet positions**: ±0.01° (36 arcseconds)
- **Ayanamsa**: ±0.001° (3.6 arcseconds)
- **House cusps**: Exact (Whole Sign = sign boundaries)
- **Dasha dates**: ±1 day

## Notes

- Use UTC or clearly specify timezone
- Double-check data entry (typos = failed tests)
- Test edge cases (retrograde stations, sign boundaries)
- Update `validated_date` when re-validating
