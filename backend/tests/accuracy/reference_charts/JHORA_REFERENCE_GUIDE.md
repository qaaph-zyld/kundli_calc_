# JHora Reference Data Generation Guide
**Purpose:** Generate accurate reference data for automated accuracy validation  
**Software:** Jagannatha Hora (JHora) version 8.0 or later  
**Estimated Time:** 2-4 hours for 10-15 charts  
**Priority:** P0 - Blocks accuracy validation

---

## Why JHora?

**Industry Standard:**
- Used by professional Vedic astrologers worldwide
- Based on Swiss Ephemeris (same as our platform)
- Extensively validated over 15+ years
- Transparent calculation methods
- Free and widely available

**Validation Approach:**
- Generate diverse birth charts in JHora
- Export planetary positions, houses, dashas
- Store in JSON format
- Automated comparison with our calculations
- Target tolerance: ±0.01° for planets, ±1 day for dashas

---

## Prerequisites

### Software Installation
1. **Download JHora:**
   - Official site: https://www.vedicastrologer.org/jh/
   - Version: 8.0 or later recommended
   - Platform: Windows (runs on Linux via Wine if needed)

2. **Install JHora:**
   - Extract to folder (e.g., `C:\JHora`)
   - Run `JHora.exe`
   - No complex setup required

### JHora Configuration (Critical)

**Set these preferences BEFORE generating charts:**

1. **Open JHora → Preferences (F10)**

2. **Ayanamsa Tab:**
   - Select: **Lahiri (Chitrapaksha)**
   - This MUST match our default setting

3. **House System:**
   - Select: **Whole Sign**
   - This is the Vedic default we use

4. **Time Zone:**
   - Verify timezone database is current
   - JHora auto-detects from location

5. **Display Preferences:**
   - Sidereal zodiac (default for Vedic)
   - Decimal degrees (easier for data entry)

**Verify Settings:**
```
View → Chart Info
Should show:
- Ayanamsa: Lahiri
- House System: Whole Sign (W)
- Zodiac: Sidereal
```

---

## Chart Selection Strategy

### Diversity Requirements (10-15 charts minimum)

**1. Standard Chart (REQUIRED)**
- Date: 1990-01-15
- Time: 12:00 PM IST
- Place: Delhi, India (28.6139°N, 77.209°E)
- Purpose: Baseline reference, commonly used

**2. Western Location (REQUIRED)**
- Date: 1985-07-04
- Time: 10:30 AM EDT
- Place: New York, USA (40.7128°N, 74.0060°W)
- Purpose: Timezone variety, Western hemisphere

**3. Historical Date (REQUIRED)**
- Date: 1950-08-15
- Time: 12:00 PM IST
- Place: Mumbai, India
- Purpose: Test historical calculations

**4. Modern Date (REQUIRED)**
- Date: 2020-06-21
- Time: 9:00 AM IST
- Place: Bangalore, India
- Purpose: Recent calculations

**5. Celebrity Charts (RECOMMENDED, 2-3)**
- Choose from documented births
- Verify accuracy of birth data
- Purpose: Real-world validation

**6. Edge Cases (RECOMMENDED, 2-3)**
- Birth at 0° Aries ascendant
- Multiple retrograde planets (e.g., late 2019)
- Planet at sign boundary (e.g., 29°59' of a sign)
- Purpose: Test boundary conditions

**7. User's Actual Chart (OPTIONAL)**
- If you have accurate birth data
- Purpose: Personal accuracy verification

---

## Step-by-Step Data Generation

### Step 1: Create Chart in JHora

1. **Open JHora**

2. **Enter Birth Data (F2):**
   ```
   Name: Reference_Chart_01
   Date: DD-MM-YYYY (e.g., 15-01-1990)
   Time: HH:MM:SS (24-hour format)
   Place: [Type city name]
   ```

3. **Verify Location:**
   - JHora will show latitude/longitude
   - Verify coordinates are correct
   - Note timezone offset shown

4. **Generate Chart (Enter)**

### Step 2: Export Planetary Positions

1. **View Planetary Positions:**
   - Go to: `Horoscope → Planetary Details`
   - Or press: `Alt+P`

2. **Record the following for EACH planet:**

**For Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn:**
```
Planet: [Name]
Longitude (Sidereal): [XXX.XXXX]° in [Sign]
Latitude: [±XX.XXXX]°
Distance: [X.XXXXXX] AU
Speed: [±X.XXXX] °/day
Nakshatra: [Name]
Pada: [1-4]
Retrograde: [Yes/No]
Sign: [Name]
Degree in Sign: [XX.XXXX]°
```

**For Rahu & Ketu:**
```
Planet: Rahu/Ketu
Longitude: [XXX.XXXX]°
Sign: [Name]
Nakshatra: [Name]
Pada: [1-4]
```

### Step 3: Export House Data

1. **View Houses:**
   - Go to: `Horoscope → House Cusps`
   - Verify "Whole Sign" is shown

2. **Record:**
```
Ascendant (Lagna): [XXX.XXXX]° in [Sign]
Midheaven (MC): [XXX.XXXX]° in [Sign]

House 1: [Sign], Cusp: [XXX.XXXX]°
House 2: [Sign], Cusp: [XXX.XXXX]°
...
House 12: [Sign], Cusp: [XXX.XXXX]°
```

**Note for Whole Sign:**
- Each house = one complete sign
- Cusps are at sign boundaries (0°, 30°, 60°, etc.)

### Step 4: Export Vimshottari Dasha

1. **View Dasha:**
   - Go to: `Dasha → Vimshottari`
   - Set start date to birth date

2. **Record:**
```
Moon's Longitude: [XXX.XXXX]°
Birth Nakshatra: [Name] (#[1-27])

Mahadasha at Birth:
  Planet: [Name]
  Start Date: [DD-MM-YYYY]
  End Date: [DD-MM-YYYY]
  Balance: [X.XX] years

Next 9 Mahadashas:
  1. [Planet]: [Start] to [End], [XX] years
  2. [Planet]: [Start] to [End], [XX] years
  ...
  9. [Planet]: [Start] to [End], [XX] years
```

### Step 5: Export Yoga Information (Optional but Recommended)

1. **View Yogas:**
   - Go to: `Analysis → Yogas`
   - JHora shows detected yogas

2. **Record prominent yogas:**
```
Yoga Name: [Sanskrit/English name]
Forming Planets: [List]
Houses Involved: [List]
Description: [Brief]
```

**Note:** Yoga detection varies by implementation. Our platform detects 60+ yogas, JHora may show different set.

---

## JSON Template for Each Chart

Save each chart as `reference_chart_XX.json` in this directory:

```json
{
  "chart_id": "reference_chart_01",
  "description": "Standard Indian birth chart - baseline reference",
  "source": "JHora 8.0",
  "generated_date": "2026-01-16",
  
  "birth_data": {
    "date": "1990-01-15",
    "time": "12:00:00",
    "timezone": "Asia/Kolkata",
    "timezone_offset": "+05:30",
    "utc_time": "1990-01-15T06:30:00Z",
    "location": {
      "name": "Delhi, India",
      "latitude": 28.6139,
      "longitude": 77.209,
      "altitude": 0
    }
  },
  
  "calculation_settings": {
    "ayanamsa": "Lahiri",
    "ayanamsa_value": 23.72,
    "house_system": "Whole Sign",
    "zodiac": "Sidereal"
  },
  
  "planets": {
    "Sun": {
      "longitude": 271.12,
      "latitude": 0.00,
      "distance": 0.98,
      "speed": 1.02,
      "sign": "Capricorn",
      "sign_number": 10,
      "degree_in_sign": 1.12,
      "nakshatra": "Uttara Ashadha",
      "nakshatra_number": 21,
      "pada": 1,
      "retrograde": false,
      "house": 10
    },
    "Moon": {
      "longitude": 140.91,
      "latitude": -5.13,
      "distance": 0.0026,
      "speed": 13.28,
      "sign": "Leo",
      "sign_number": 5,
      "degree_in_sign": 20.91,
      "nakshatra": "Purva Phalguni",
      "nakshatra_number": 11,
      "pada": 4,
      "retrograde": false,
      "house": 5
    },
    "Mars": {
      "longitude": 236.02,
      "latitude": 0.78,
      "distance": 1.42,
      "speed": 0.61,
      "sign": "Scorpio",
      "sign_number": 8,
      "degree_in_sign": 26.02,
      "nakshatra": "Jyeshtha",
      "nakshatra_number": 18,
      "pada": 4,
      "retrograde": false,
      "house": 8
    },
    "Mercury": {
      "longitude": 257.79,
      "latitude": -0.42,
      "distance": 1.32,
      "speed": 1.48,
      "sign": "Sagittarius",
      "sign_number": 9,
      "degree_in_sign": 17.79,
      "nakshatra": "Purva Ashadha",
      "nakshatra_number": 20,
      "pada": 2,
      "retrograde": false,
      "house": 9
    },
    "Jupiter": {
      "longitude": 69.67,
      "latitude": -0.23,
      "distance": 5.98,
      "speed": 0.23,
      "sign": "Gemini",
      "sign_number": 3,
      "degree_in_sign": 9.67,
      "nakshatra": "Ardra",
      "nakshatra_number": 6,
      "pada": 3,
      "retrograde": false,
      "house": 3
    },
    "Venus": {
      "longitude": 277.10,
      "latitude": 1.22,
      "distance": 1.69,
      "speed": 1.23,
      "sign": "Capricorn",
      "sign_number": 10,
      "degree_in_sign": 7.10,
      "nakshatra": "Uttara Ashadha",
      "nakshatra_number": 21,
      "pada": 3,
      "retrograde": false,
      "house": 10
    },
    "Saturn": {
      "longitude": 263.57,
      "latitude": -0.89,
      "distance": 9.12,
      "speed": 0.12,
      "sign": "Sagittarius",
      "sign_number": 9,
      "degree_in_sign": 23.57,
      "nakshatra": "Purva Ashadha",
      "nakshatra_number": 20,
      "pada": 4,
      "retrograde": false,
      "house": 9
    },
    "Rahu": {
      "longitude": 293.98,
      "sign": "Capricorn",
      "sign_number": 10,
      "degree_in_sign": 23.98,
      "nakshatra": "Dhanishta",
      "nakshatra_number": 23,
      "pada": 2,
      "house": 10
    },
    "Ketu": {
      "longitude": 113.98,
      "sign": "Cancer",
      "sign_number": 4,
      "degree_in_sign": 23.98,
      "nakshatra": "Pushya",
      "nakshatra_number": 8,
      "pada": 2,
      "house": 4
    }
  },
  
  "houses": {
    "ascendant": 96.45,
    "ascendant_sign": "Cancer",
    "midheaven": 15.23,
    "cusps": {
      "1": {"sign": "Cancer", "longitude": 90.00},
      "2": {"sign": "Leo", "longitude": 120.00},
      "3": {"sign": "Virgo", "longitude": 150.00},
      "4": {"sign": "Libra", "longitude": 180.00},
      "5": {"sign": "Scorpio", "longitude": 210.00},
      "6": {"sign": "Sagittarius", "longitude": 240.00},
      "7": {"sign": "Capricorn", "longitude": 270.00},
      "8": {"sign": "Aquarius", "longitude": 300.00},
      "9": {"sign": "Pisces", "longitude": 330.00},
      "10": {"sign": "Aries", "longitude": 0.00},
      "11": {"sign": "Taurus", "longitude": 30.00},
      "12": {"sign": "Gemini", "longitude": 60.00}
    }
  },
  
  "vimshottari_dasha": {
    "moon_longitude": 140.91,
    "birth_nakshatra": {
      "name": "Purva Phalguni",
      "number": 11,
      "lord": "Venus"
    },
    "mahadasha_at_birth": {
      "planet": "Mercury",
      "start_date": "1988-05-15",
      "end_date": "2005-05-15",
      "balance_years": 14.67
    },
    "sequence": [
      {
        "planet": "Mercury",
        "start_date": "1988-05-15",
        "end_date": "2005-05-15",
        "years": 17
      },
      {
        "planet": "Ketu",
        "start_date": "2005-05-15",
        "end_date": "2012-05-15",
        "years": 7
      },
      {
        "planet": "Venus",
        "start_date": "2012-05-15",
        "end_date": "2032-05-15",
        "years": 20
      }
    ]
  },
  
  "yogas": [
    {
      "name": "Gajakesari Yoga",
      "planets": ["Jupiter", "Moon"],
      "houses": [3, 5],
      "description": "Moon and Jupiter in Kendra"
    }
  ],
  
  "notes": "Standard reference chart for baseline validation. All values manually verified in JHora."
}
```

---

## Data Entry Tips

### Precision
- **Planetary longitudes:** Record to 2 decimal places minimum (0.01°)
- **Ayanamsa:** Record to 2 decimal places (e.g., 23.72°)
- **Dasha dates:** Record exact dates (DD-MM-YYYY)
- **Dasha balance:** Record to 2 decimal places (e.g., 14.67 years)

### Double-Check
- Verify ayanamsa is Lahiri before recording
- Verify house system is Whole Sign
- Cross-check planet signs with longitudes
- Verify Rahu-Ketu are exactly 180° apart

### Common Mistakes to Avoid
1. **Wrong ayanamsa:** Accidentally using KP or Raman instead of Lahiri
2. **Tropical zodiac:** Verify sidereal mode is active
3. **Wrong house system:** Placidus instead of Whole Sign
4. **Timezone errors:** Verify UTC offset is correct
5. **Copy-paste errors:** Double-check all numbers

---

## Validation Checklist

After generating each chart, verify:

- [ ] JHora preferences set to Lahiri + Whole Sign
- [ ] All 9 planets recorded (Sun through Ketu)
- [ ] Ascendant and 12 house cusps recorded
- [ ] Vimshottari dasha balance calculated
- [ ] At least 5 mahadasha periods recorded
- [ ] JSON file is valid (test with JSON validator)
- [ ] Coordinates match the location
- [ ] Timezone offset is correct
- [ ] Rahu and Ketu are 180° apart (±0.01°)
- [ ] Planet signs match longitudes (e.g., 45° = Taurus)

---

## Priority Chart List

Generate in this order for maximum validation coverage:

1. **reference_chart_01.json** - Standard Indian (Delhi 1990)
2. **reference_chart_02.json** - Western location (NY 1985)
3. **reference_chart_03.json** - Historical (Mumbai 1950)
4. **reference_chart_04.json** - Modern (Bangalore 2020)
5. **reference_chart_05.json** - User's actual chart (if available)
6. **reference_chart_06.json** - Celebrity chart (verified data)
7. **reference_chart_07.json** - Edge case: 0° Aries ascendant
8. **reference_chart_08.json** - Edge case: Multiple retrogrades
9. **reference_chart_09.json** - Edge case: Sign boundary planet
10. **reference_chart_10.json** - Random chart for diversity

**Minimum for validation:** Charts 1-4 (4 charts)  
**Recommended for thorough validation:** Charts 1-10 (10 charts)  
**Comprehensive validation:** Charts 1-15 (add 5 more diverse charts)

---

## Automated Validation Script

Once JSON files are ready, run:

```bash
cd backend
pytest tests/accuracy/test_jhora_reference.py -v
```

**What the script will test:**
- Planetary positions within ±0.01° tolerance
- Ascendant within ±0.01° tolerance
- House cusps within ±0.1° tolerance
- Dasha dates within ±1 day tolerance
- Ayanamsa within ±0.001° tolerance
- Nakshatra assignments (exact match)

**Expected output:**
```
tests/accuracy/test_jhora_reference.py::test_planetary_positions[chart_01] PASSED
tests/accuracy/test_jhora_reference.py::test_house_cusps[chart_01] PASSED
tests/accuracy/test_jhora_reference.py::test_dasha_periods[chart_01] PASSED
...
```

---

## Semi-Automated Data Entry (Optional)

If you have many charts to generate, consider:

1. **JHora Batch Mode:**
   - Create text file with birth data
   - Use JHora command-line mode (if available)

2. **Screen Scraping:**
   - Use AutoHotkey or similar to automate data entry
   - Risk: Less reliable, needs supervision

3. **Manual is Safest:**
   - 10-15 charts = 2-4 hours manual entry
   - Ensures accuracy
   - Recommended approach

---

## Troubleshooting

### Issue: Different Planetary Positions
**Solution:** Verify ayanamsa setting. Even 0.1° ayanamsa difference = different planets positions.

### Issue: Different House Cusps
**Solution:** Verify house system is "Whole Sign" not "Placidus" or "Equal"

### Issue: Different Dasha Balance
**Solution:** Check if JHora is using True Node vs Mean Node for Rahu/Ketu. We use Mean Node.

### Issue: Timezone Confusion
**Solution:** Always work in UTC internally. Record timezone offset clearly.

### Issue: JSON Validation Errors
**Solution:** Use online JSON validator (jsonlint.com) to find syntax errors.

---

## Contact & Support

**For Questions:**
- Review this guide thoroughly first
- Check `backend/tests/accuracy/STATUS.md` for current test status
- Examine existing test templates in `test_jhora_reference.py`

**For Automation Help:**
- Test framework is ready, just needs reference data
- All test assertions are pre-written
- Just provide JSON files and run pytest

---

## Success Criteria

**You're done when:**
- [ ] 4-10 JSON reference chart files created
- [ ] All files pass JSON validation
- [ ] Spot-check: Our calculator matches JHora within tolerance
- [ ] Pytest test suite runs and shows comparison results
- [ ] Any discrepancies documented and investigated

**Estimated Impact:**
- Unblocks P0 accuracy validation
- Enables regression testing for all calculations
- Builds confidence in calculation accuracy
- Provides baseline for future accuracy improvements

---

**Guide Status:** Complete  
**Version:** 1.0  
**Last Updated:** 2026-01-16  
**Next Step:** Generate first 4 reference charts for baseline validation
