# 🧪 COMPREHENSIVE TESTING GUIDE

**Purpose:** Ensure all features work correctly before production deployment  
**Status:** Pre-Production Testing Checklist  
**Date:** November 4, 2024

---

## 📋 TABLE OF CONTENTS

1. [Quick Start Testing](#quick-start-testing)
2. [Feature-by-Feature Testing](#feature-by-feature-testing)
3. [Calculation Accuracy Verification](#calculation-accuracy-verification)
4. [Edge Cases & Error Handling](#edge-cases--error-handling)
5. [Cross-Browser Testing](#cross-browser-testing)
6. [Mobile/Responsive Testing](#mobile-responsive-testing)
7. [API Testing](#api-testing)
8. [Performance Testing](#performance-testing)
9. [Security Testing](#security-testing)
10. [Known Test Cases with Expected Results](#known-test-cases)

---

## 🚀 QUICK START TESTING

### **Step 1: Start the Application**

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend/next-app
npm run dev
```

**Verify:**
- ✅ Backend running at `http://localhost:8000`
- ✅ Frontend running at `http://localhost:3000`
- ✅ No console errors in browser
- ✅ API docs accessible at `http://localhost:8000/docs`

### **Step 2: Quick Smoke Test (5 minutes)**

1. Open `http://localhost:3000`
2. Fill in birth details with known data
3. Click "Generate Chart"
4. Verify chart displays without errors
5. Try one feature from each category

**If all pass → Proceed to detailed testing**  
**If any fail → Fix issues first**

---

## 🔬 FEATURE-BY-FEATURE TESTING

### **1. BASIC CHART CALCULATION** ⭐ (Priority: CRITICAL)

#### Test Case 1.1: Valid Birth Chart
**Input:**
```
Date: 1990-01-15
Time: 14:30
Location: New Delhi, India
Latitude: 28.6139
Longitude: 77.2090
Ayanamsa: Lahiri
House System: Placidus
```

**Expected Output:**
- ✅ Chart displays within 3 seconds
- ✅ All planets show positions
- ✅ Ascendant calculated
- ✅ Houses numbered 1-12
- ✅ No console errors

**How to Verify:**
1. Check planetary positions are reasonable (0-360°)
2. Ascendant sign should match (check with JHora/other software)
3. Moon sign should be displayed
4. All 9 planets + Rahu/Ketu visible

#### Test Case 1.2: Different Time Zones
**Test with:**
- USA (New York): Lat 40.7128, Lon -74.0060
- UK (London): Lat 51.5074, Lon -0.1278
- India (Mumbai): Lat 19.0760, Lon 72.8777
- Australia (Sydney): Lat -33.8688, Lon 151.2093

**Verify:** Charts calculate correctly for all time zones

#### Test Case 1.3: Edge Cases - Dates
- Birth date at midnight (00:00)
- Birth date at 23:59
- Leap year date (Feb 29, 2000)
- Very old date (1920)
- Recent date (2024)

---

### **2. CHART VISUALIZATION** 🎨 (Priority: HIGH)

#### Test Case 2.1: South Indian Chart
**Steps:**
1. Generate a chart
2. Select "South Indian (D1)"
3. Verify visual layout

**Expected:**
- ✅ Diamond shape visible
- ✅ All 12 houses shown
- ✅ Planets in correct houses
- ✅ Planet symbols/names readable
- ✅ Signs labeled correctly
- ✅ Ascendant marked

#### Test Case 2.2: North Indian Chart
**Steps:**
1. Click "North Indian (D1)" button
2. Verify diamond/rhombus layout

**Expected:**
- ✅ Diamond orientation correct
- ✅ Fixed houses (house 1 always at top)
- ✅ Signs rotate based on ascendant
- ✅ Hover tooltips work
- ✅ Planetary details show on hover

#### Test Case 2.3: Divisional Charts
**Test all 6 chart types:**
- D1 (Rasi) - Main birth chart
- D2 (Hora) - Wealth
- D3 (Drekkana) - Siblings
- D9 (Navamsa) - Marriage
- D10 (Dasamsa) - Career
- D12 (Dwadasamsa) - Parents

**Verify:**
- ✅ Each chart displays different planetary positions
- ✅ Charts calculated correctly (compare with reference)
- ✅ No overlap in planet symbols
- ✅ Chart info text updates

---

### **3. YOGAS DETECTION** 🌟 (Priority: HIGH)

#### Test Case 3.1: Known Yoga Charts
**Use these famous charts with known yogas:**

**Chart A - Gaja Kesari Yoga:**
```
Date: 1990-05-20
Time: 10:30
Location: New Delhi
Expected: Gaja Kesari Yoga (Jupiter-Moon in angles)
```

**Chart B - Raj Yoga:**
```
Date: 1985-11-07
Time: 14:15
Location: Mumbai
Expected: Raj Yoga (Kendra-Trikona lords)
```

**How to Verify:**
1. Click "Show Analysis"
2. Check Yogas section
3. Verify detected yogas match expectations
4. Check strength indicators (weak/moderate/strong)
5. Read effects descriptions

#### Test Case 3.2: No Yogas Chart
**Create chart with no major yogas**
- Verify "No significant yogas" message appears
- Or only weak yogas detected

#### Test Case 3.3: Multiple Yogas
**Test chart with 3+ yogas**
- ✅ All yogas listed
- ✅ Expandable effects work
- ✅ Color coding correct (green/red/yellow)

---

### **4. DOSHAS DETECTION** ⚠️ (Priority: HIGH)

#### Test Case 4.1: Mangal Dosha (Mars Affliction)
**Known Mangal Dosha Chart:**
```
Mars in houses: 1, 2, 4, 7, 8, or 12
Expected: Mangal Dosha detected with severity
```

**Verify:**
- ✅ Dosha detected
- ✅ Severity level shown (mild/moderate/severe)
- ✅ Effects described
- ✅ Remedies expandable and listed

#### Test Case 4.2: Kala Sarpa Dosha
**All planets between Rahu-Ketu axis**
- ✅ Dosha detected
- ✅ Type specified (if partial/full)
- ✅ Remedies provided

#### Test Case 4.3: Multiple Doshas
**Test with 3+ doshas present**
- ✅ All doshas listed
- ✅ Chart health score calculated (0-100)
- ✅ Color coding by severity
- ✅ Remedies for each dosha

#### Test Case 4.4: No Doshas
**Clean chart**
- ✅ "No significant doshas" or high health score
- ✅ Green indicators

---

### **5. ASHTAKOOT MATCHING** 💑 (Priority: HIGH)

#### Test Case 5.1: Excellent Match
**Generate two compatible charts**

**Person 1:**
```
Date: 1990-01-15
Time: 10:00
Location: Delhi
Moon: Taurus (example)
```

**Person 2:**
```
Date: 1992-03-20
Time: 14:00
Location: Delhi
Moon: Virgo (example)
```

**Expected:**
- ✅ Total score displayed (out of 36)
- ✅ Percentage calculated
- ✅ Compatibility rating shown
- ✅ All 8 kootas listed with scores
- ✅ Detailed descriptions for each
- ✅ Recommendations provided

#### Test Case 5.2: Poor Match
**Test incompatible charts (same Nadi, etc.)**
- ✅ Low score (< 18)
- ✅ "Poor" or "Average" rating
- ✅ Nadi dosha warning displayed
- ✅ Consultation recommendation

#### Test Case 5.3: Verify Individual Kootas
**Check each koota calculation:**
1. **Varna** (1pt) - Caste compatibility
2. **Vashya** (2pt) - Attraction
3. **Tara** (3pt) - Birth star
4. **Yoni** (4pt) - Physical compatibility
5. **Graha Maitri** (5pt) - Mental
6. **Gana** (6pt) - Temperament
7. **Bhakoot** (7pt) - Rasi
8. **Nadi** (8pt) - Health/genetics

**Compare with JHora or other calculators**

---

### **6. PLANETARY STRENGTH (SHADBALA)** 💪 (Priority: MEDIUM)

#### Test Case 6.1: Strong Planet
**Chart with exalted planet (e.g., Sun in Aries)**
- ✅ High strength score (> 450 Rupas for Sun)
- ✅ "Very Strong" or "Strong" badge
- ✅ Green progress bar
- ✅ > 100% of required strength
- ✅ Positive interpretation

#### Test Case 6.2: Weak Planet
**Chart with debilitated planet (e.g., Sun in Libra)**
- ✅ Low strength score (< 300 Rupas)
- ✅ "Weak" or "Very Weak" badge
- ✅ Red progress bar
- ✅ < 70% of required strength
- ✅ Negative interpretation

#### Test Case 6.3: Overall Chart Strength
**Verify summary statistics:**
- ✅ Average strength calculated
- ✅ Strongest planet identified
- ✅ Weakest planet identified
- ✅ Overall rating (Excellent/Good/Average/Weak)
- ✅ Recommendations provided

#### Test Case 6.4: Shadbala Components
**Check all 6 components contribute:**
1. Sthana Bala (positional)
2. Dig Bala (directional)
3. Kala Bala (temporal)
4. Chesta Bala (motional)
5. Naisargika Bala (natural)
6. Drik Bala (aspectual)

**Verify:** Total adds up correctly

---

### **7. SPECIAL POINTS** ⭐ (Priority: MEDIUM)

#### Test Case 7.1: Brighu Bindu Calculation
**Formula:** (Rahu longitude + Moon longitude) / 2

**Manual Verification:**
1. Note Rahu longitude from chart
2. Note Moon longitude from chart
3. Calculate: (Rahu + Moon) / 2
4. Compare with displayed Brighu Bindu
5. Verify sign and house placement

#### Test Case 7.2: Gulika & Mandi
**Verify:**
- ✅ Positions calculated
- ✅ Sign placement shown
- ✅ House number correct
- ✅ Descriptions displayed

#### Test Case 7.3: Bhava & Hora Lagna
**Check formulas:**
- Bhava Lagna: (Asc + Sun - Moon) mod 360
- Hora Lagna: (Asc + (Sun - Moon)/2) mod 360

**Verify calculations match**

---

### **8. TRANSIT CALCULATIONS** 🌍 (Priority: MEDIUM)

#### Test Case 8.1: Today's Transits
1. Go to `/transits` page
2. Enter birth details
3. Click "Today" button
4. Click "Calculate Transits"

**Expected:**
- ✅ Current planetary positions shown
- ✅ Dates match today
- ✅ Transit predictions generated
- ✅ Important aspects listed

#### Test Case 8.2: Future Transits
**Select date 1 month ahead**
- ✅ Planetary positions different from today
- ✅ Future predictions shown

#### Test Case 8.3: Past Transits
**Select past date (1 year ago)**
- ✅ Historical positions shown
- ✅ Past transit effects described

---

### **9. BIRTH TIME RECTIFICATION** ⏰ (Priority: MEDIUM)

#### Test Case 9.1: Basic Rectification
**Input:**
```
Approximate Time: 14:00
Uncertainty: ±30 minutes
Life Events: 3 events with dates
```

**Expected:**
- ✅ Corrected time suggested
- ✅ Adjustment shown (e.g., +15 minutes)
- ✅ Confidence score displayed (60-95%)
- ✅ Reasoning provided (4+ points)
- ✅ Before/After comparison visible

#### Test Case 9.2: Multiple Life Events
**Add 5+ life events**
- ✅ All events accepted
- ✅ Higher confidence score
- ✅ More detailed reasoning

#### Test Case 9.3: Large Uncertainty
**Test with ±4 hours uncertainty**
- ✅ Larger adjustment possible
- ✅ Lower confidence score
- ✅ Recommendation to reduce uncertainty

---

### **10. SAVE & LOAD CHARTS** 💾 (Priority: HIGH)

#### Test Case 10.1: Save Chart (Authenticated)
1. Sign up/login
2. Generate chart
3. Click "Save Chart"
4. Enter name
5. Save

**Verify:**
- ✅ Success message shown
- ✅ Chart appears in "My Charts"
- ✅ Name displayed correctly

#### Test Case 10.2: Load Chart
1. Go to "My Charts"
2. Click on saved chart
3. Verify chart loads

**Expected:**
- ✅ All chart data restored
- ✅ Birth details match
- ✅ Analysis available

#### Test Case 10.3: Delete Chart
- ✅ Delete button works
- ✅ Confirmation dialog appears
- ✅ Chart removed from list

---

### **11. PDF EXPORT** 📄 (Priority: MEDIUM)

#### Test Case 11.1: Export Chart to PDF
1. Generate chart
2. Click "Export PDF"
3. Wait for download

**Verify:**
- ✅ PDF downloads
- ✅ Chart image included
- ✅ Birth details visible
- ✅ Planetary positions listed
- ✅ File opens correctly

---

### **12. USER AUTHENTICATION** 🔐 (Priority: HIGH)

#### Test Case 12.1: Sign Up
1. Click "Sign Up"
2. Enter email and password
3. Submit

**Expected:**
- ✅ Success message
- ✅ Email confirmation sent
- ✅ Redirected to dashboard

#### Test Case 12.2: Login
1. Enter credentials
2. Click "Login"

**Verify:**
- ✅ Logged in successfully
- ✅ User name shown in header
- ✅ "My Charts" accessible

#### Test Case 12.3: Logout
- ✅ Logout button works
- ✅ Redirected to home
- ✅ Protected routes inaccessible

---

## 🎯 CALCULATION ACCURACY VERIFICATION

### **Method 1: Compare with Jagannatha Hora**

1. **Download JHora** (free)
2. **Generate same chart in both apps**
3. **Compare outputs:**

| Element | Your App | JHora | Match? |
|---------|----------|-------|--------|
| Ascendant | | | ✅/❌ |
| Sun position | | | ✅/❌ |
| Moon position | | | ✅/❌ |
| Mars position | | | ✅/❌ |
| Mercury position | | | ✅/❌ |
| Jupiter position | | | ✅/❌ |
| Venus position | | | ✅/❌ |
| Saturn position | | | ✅/❌ |
| Rahu position | | | ✅/❌ |
| Ketu position | | | ✅/❌ |

**Acceptable difference:** ± 1 degree (due to different ephemeris versions)

### **Method 2: Online Calculators**

**Test against:**
- AstroSage.com
- Astro-Seek.com
- Vedic Astrology Calculator

**Compare key elements:**
- Ascendant sign
- Moon sign
- Sun sign
- Nakshatra
- Basic yogas

### **Method 3: Known Celebrity Charts**

**Test with publicly available charts:**
1. Mahatma Gandhi (Oct 2, 1869, 7:12 AM, Porbandar)
2. Jawaharlal Nehru (Nov 14, 1889, 11:30 PM, Allahabad)
3. APJ Abdul Kalam (Oct 15, 1931, 12:00 AM, Rameswaram)

**Verify:** Matches published chart data

---

## ⚠️ EDGE CASES & ERROR HANDLING

### **1. Invalid Inputs**

#### Test Case E1: Missing Required Fields
- ✅ Error message displayed
- ✅ Form validation prevents submission
- ✅ User-friendly error text

#### Test Case E2: Invalid Date
**Try:**
- Feb 30 (doesn't exist)
- Month 13
- Year 1800 (too old?)

**Expected:**
- ✅ Graceful error handling
- ✅ Clear error message

#### Test Case E3: Invalid Coordinates
**Try:**
- Latitude > 90 or < -90
- Longitude > 180 or < -180

**Expected:**
- ✅ Validation error
- ✅ Helpful message

#### Test Case E4: API Failure
**Simulate:**
- Backend down
- Network timeout
- 500 error response

**Expected:**
- ✅ User-friendly error message
- ✅ No app crash
- ✅ Retry option or guidance

---

## 🌐 CROSS-BROWSER TESTING

### **Desktop Browsers:**

| Browser | Version | Status | Notes |
|---------|---------|--------|-------|
| Chrome | Latest | ⬜ | |
| Firefox | Latest | ⬜ | |
| Safari | Latest | ⬜ | Mac only |
| Edge | Latest | ⬜ | |
| Opera | Latest | ⬜ | Optional |

**Test on each:**
1. Chart generation
2. All visualizations render
3. Buttons work
4. Forms submit
5. Navigation works
6. No console errors

---

## 📱 MOBILE/RESPONSIVE TESTING

### **Devices to Test:**

| Device Type | Screen Size | Status | Critical Features |
|-------------|-------------|--------|-------------------|
| iPhone SE | 375x667 | ⬜ | Chart readable, forms usable |
| iPhone 12 | 390x844 | ⬜ | All features accessible |
| Samsung Galaxy | 412x915 | ⬜ | Android compatibility |
| iPad | 768x1024 | ⬜ | Tablet layout optimized |
| Desktop | 1920x1080 | ⬜ | Full features visible |

**Key Checks:**
- ✅ Charts scale properly
- ✅ Forms are touch-friendly
- ✅ Navigation accessible
- ✅ No horizontal scrolling
- ✅ Text readable (min 14px)
- ✅ Buttons large enough (44x44px min)

### **Responsive Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

## 🔌 API TESTING

### **Using FastAPI Docs (http://localhost:8000/docs)**

#### Test Case API-1: Calculate Chart
```bash
curl -X POST "http://localhost:8000/api/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "date_time": "1990-01-15T14:30:00Z",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "altitude": 0,
    "ayanamsa_type": "LAHIRI",
    "house_system": "PLACIDUS"
  }'
```

**Expected:** 200 OK with JSON chart data

#### Test Case API-2: Transit Calculations
```bash
curl -X POST "http://localhost:8000/api/transits" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_datetime": "1990-01-15T14:30:00Z",
    "transit_date": "2024-11-04",
    "latitude": 28.6139,
    "longitude": 77.2090
  }'
```

**Expected:** 200 OK with transit data

#### Test Case API-3: Error Handling
**Send invalid request:**
- Missing required fields
- Invalid date format
- Out of range coordinates

**Expected:** 422 Validation Error with details

---

## ⚡ PERFORMANCE TESTING

### **Test Case P1: Chart Generation Speed**

**Measure time from click to display:**
- ✅ Target: < 3 seconds
- ✅ Acceptable: < 5 seconds
- ❌ Slow: > 5 seconds

**Tools:**
- Browser DevTools Network tab
- Console.time() / Console.timeEnd()

### **Test Case P2: Page Load Speed**

**First load:**
- ✅ Target: < 2 seconds
- Check Lighthouse score (aim for 90+)

### **Test Case P3: Multiple Charts**
**Generate 10 charts in succession:**
- ✅ No memory leaks
- ✅ Performance doesn't degrade
- ✅ No browser crashes

### **Test Case P4: Large Data Sets**
**Test with:**
- 50+ saved charts
- Complex calculations (all features on)

**Expected:**
- ✅ Still responsive
- ✅ No lag

---

## 🔒 SECURITY TESTING

### **Test Case S1: Authentication**
- ✅ Cannot access "/my-charts" without login
- ✅ Cannot save charts without auth
- ✅ JWT tokens expire properly
- ✅ Password requirements enforced

### **Test Case S2: Input Validation**
- ✅ SQL injection attempts blocked
- ✅ XSS attempts sanitized
- ✅ API rate limiting works (if implemented)

### **Test Case S3: Data Privacy**
- ✅ User can only see their own charts
- ✅ Cannot access other users' data via URL manipulation

---

## 📊 KNOWN TEST CASES WITH EXPECTED RESULTS

### **TEST CASE #1: Mahatma Gandhi**
```
Date: October 2, 1869
Time: 07:12 AM
Place: Porbandar, India
Lat: 21.6417
Lon: 69.6293
```

**Expected Results:**
- Ascendant: Libra
- Moon: Leo
- Sun: Virgo
- Nakshatra: Purvaphalguni (Moon)
- Known Yogas: Check published analyses

### **TEST CASE #2: Modern Example**
```
Date: January 1, 2000
Time: 12:00 PM
Place: New Delhi
Lat: 28.6139
Lon: 77.2090
```

**Expected:**
- Ascendant: ~Aries (depends on exact time)
- Calculate with JHora for comparison
- All 9 planets should appear in reasonable positions

### **TEST CASE #3: Edge - Midnight Birth**
```
Date: June 15, 1995
Time: 00:00 AM
Place: Mumbai
```

**Verify:** No errors with midnight time

### **TEST CASE #4: Edge - Southern Hemisphere**
```
Date: March 20, 2010
Time: 15:30
Place: Sydney, Australia
Lat: -33.8688
Lon: 151.2093
```

**Verify:** Handles negative latitudes correctly

---

## ✅ TESTING CHECKLIST

### **Phase 1: Critical Features (Must Pass)**
- [ ] Chart generation works
- [ ] All planets display correctly
- [ ] Ascendant calculated
- [ ] Charts visualization renders
- [ ] Analysis features work
- [ ] No critical errors in console
- [ ] Mobile responsive

### **Phase 2: Advanced Features**
- [ ] Ashtakoot matching
- [ ] Planetary strength
- [ ] Special points
- [ ] Transit calculations
- [ ] Birth time rectification
- [ ] PDF export
- [ ] Save/load charts

### **Phase 3: Polish & UX**
- [ ] Error messages user-friendly
- [ ] Loading states clear
- [ ] All buttons work
- [ ] Navigation intuitive
- [ ] Help text available
- [ ] Forms validated

### **Phase 4: Cross-Platform**
- [ ] Chrome tested
- [ ] Firefox tested
- [ ] Safari tested (if available)
- [ ] Mobile tested (iOS/Android)
- [ ] Tablet tested

### **Phase 5: Performance**
- [ ] Fast chart generation (< 3s)
- [ ] No memory leaks
- [ ] Lighthouse score > 80
- [ ] Works on slow connections

---

## 🐛 BUG TRACKING

### **Found a Bug? Document it:**

**Template:**
```
Bug ID: BUG-001
Severity: High/Medium/Low
Feature: Chart Generation
Steps to Reproduce:
1. Step 1
2. Step 2
3. Step 3

Expected Result:
[What should happen]

Actual Result:
[What actually happened]

Screenshots:
[If applicable]

Browser/Device:
[Chrome 119, Windows 11]

Status: Open/In Progress/Fixed
```

---

## 📝 TEST REPORT TEMPLATE

After testing, fill this out:

```
TEST REPORT
===========

Date: [Date]
Tester: [Name]
Version: [App version]

SUMMARY:
- Total Tests: [Number]
- Passed: [Number]
- Failed: [Number]
- Blocked: [Number]
- Pass Rate: [Percentage]

CRITICAL ISSUES:
1. [Issue description]
2. [Issue description]

MINOR ISSUES:
1. [Issue description]
2. [Issue description]

RECOMMENDATIONS:
1. [Recommendation]
2. [Recommendation]

READY FOR PRODUCTION: YES / NO / WITH FIXES

Signature: [Name]
```

---

## 🎯 FINAL VERIFICATION CHECKLIST

Before declaring "Production Ready":

- [ ] All critical features tested and working
- [ ] Calculations verified against reference software
- [ ] No critical bugs remaining
- [ ] Cross-browser compatibility confirmed
- [ ] Mobile responsive working
- [ ] Performance acceptable (< 3s charts)
- [ ] Security basics in place
- [ ] Error handling graceful
- [ ] User authentication working
- [ ] Data persistence working
- [ ] Documentation complete
- [ ] Tested with 10+ different birth charts
- [ ] API endpoints tested
- [ ] Edge cases handled
- [ ] At least 2 people tested the app

---

## 📚 ADDITIONAL RESOURCES

### **Comparison Tools:**
- Jagannatha Hora (desktop software)
- AstroSage.com (online)
- Astro-Seek.com (online)

### **Testing Tools:**
- Chrome DevTools
- Lighthouse (performance)
- Postman (API testing)
- BrowserStack (cross-browser)

### **Validation Data:**
- Swiss Ephemeris test cases
- Published celebrity charts
- Astrology textbooks

---

**🎯 TESTING GOAL: Achieve 95%+ test coverage before production deployment**

**Status:** Ready to begin testing ✅  
**Estimated Time:** 4-6 hours for comprehensive testing  
**Team Size:** 1-3 testers recommended
