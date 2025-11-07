# ✅ MANUAL TESTING CHECKLIST
**Print this and check off each item as you test**

**Browser URL:** http://localhost:3100  
**Expected Time:** 30-45 minutes  
**Date:** _____________

---

## 🚀 QUICK START

**Before starting:**
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3100
- [ ] Browser open to http://localhost:3100
- [ ] Chrome DevTools open (F12) for console monitoring

---

## TEST 1: HOME PAGE & BASIC CHART GENERATION
**Time:** 5 minutes | **Priority:** CRITICAL

### Steps:
1. [ ] Navigate to http://localhost:3100
2. [ ] Verify page loads without errors
3. [ ] Check browser console - should be no red errors

### Fill Birth Details Form:
4. [ ] Name: "Test User"
5. [ ] Date: 1990-01-15 (use date picker or type)
6. [ ] Time: 14:30 (use time picker or type)
7. [ ] Location autocomplete: Type "New Delhi"
8. [ ] OR Manual: Lat 28.6139, Lon 77.2090
9. [ ] Click "Generate Chart" button

### Verify Results:
10. [ ] Chart generates within 5 seconds
11. [ ] Loading indicator appears during calculation
12. [ ] South Indian chart visible (diamond shape)
13. [ ] Planetary positions displayed below/beside chart
14. [ ] No error messages shown
15. [ ] Browser console still clean (no errors)

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 2: CHART TYPE SWITCHING
**Time:** 3 minutes | **Priority:** HIGH

### From previous chart:
1. [ ] Locate chart type buttons (should be near chart)
2. [ ] Click "South Indian (D1)" - chart should display
3. [ ] Click "North Indian (D1)" - layout changes to rhombus
4. [ ] Verify planets rotate correctly in North Indian style
5. [ ] Click "Navamsa (D9)" - NEW chart with different positions
6. [ ] Click "Hora (D2)" - different chart
7. [ ] Click "Drekkana (D3)" - different chart
8. [ ] Click "Dasamsa (D10)" - different chart
9. [ ] Click "Dwadasamsa (D12)" - different chart
10. [ ] All charts render without errors

### Verify Chart Info:
11. [ ] Chart description updates for each type
12. [ ] Planetary positions change for divisional charts
13. [ ] Navigation smooth, no lag

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 3: ANALYSIS - YOGAS DETECTION
**Time:** 4 minutes | **Priority:** HIGH

### Steps:
1. [ ] Generate a new chart (or use existing)
2. [ ] Click "Show Analysis" button (if not already shown)
3. [ ] Scroll to find "Yogas" section

### Verify Yogas Section:
4. [ ] Section header "Yogas" visible
5. [ ] At least 1 yoga card displayed (or "No yogas" message)
6. [ ] Each yoga card shows:
   - [ ] Yoga name
   - [ ] Strength indicator (weak/moderate/strong)
   - [ ] Color coding (green=beneficial, red=malefic)
7. [ ] Click on a yoga card to expand
8. [ ] "Effects" description appears
9. [ ] Effects text is readable and makes sense

### Test Multiple Charts:
10. [ ] Try different birth dates to see different yogas
11. [ ] Verify yoga detection changes with different charts

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 4: ANALYSIS - DOSHAS DETECTION
**Time:** 4 minutes | **Priority:** HIGH

### In Analysis Section:
1. [ ] Locate "Doshas" section
2. [ ] Chart health score displayed (0-100)
3. [ ] Color-coded score bar (red/yellow/green)

### Verify Doshas Cards:
4. [ ] If doshas present, cards shown with:
   - [ ] Dosha name (e.g., "Mangal Dosha")
   - [ ] Severity level (Mild/Moderate/Severe)
   - [ ] Severity color coding
   - [ ] "Show Remedies" button
5. [ ] Click "Show Remedies" on any dosha
6. [ ] Remedies list expands
7. [ ] Multiple remedies listed (gemstones, mantras, etc.)
8. [ ] Click button again - remedies collapse

### Test Edge Case:
9. [ ] Generate chart with Mars in 1st, 4th, 7th, 8th, or 12th house
10. [ ] Verify Mangal Dosha detected (if applicable)

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 5: PLANETARY STRENGTH (SHADBALA)
**Time:** 3 minutes | **Priority:** MEDIUM

### In Analysis Section:
1. [ ] Locate "Planetary Strength" section
2. [ ] Summary statistics box visible:
   - [ ] Average strength shown
   - [ ] Strongest planet identified
   - [ ] Weakest planet identified
   - [ ] Overall rating displayed

### Verify Individual Planets:
3. [ ] For each planet (Sun, Moon, Mars, etc.):
   - [ ] Name displayed
   - [ ] Progress bar showing strength
   - [ ] Color coding (green=strong, red=weak)
   - [ ] Percentage shown (e.g., "125% of required")
   - [ ] Badge (Very Strong/Strong/Average/Weak/Very Weak)
4. [ ] Click or hover on a planet
5. [ ] Interpretation text visible
6. [ ] Strength details readable

### Check Recommendations:
7. [ ] "Recommendations" box at bottom of section
8. [ ] At least 2-3 recommendations listed
9. [ ] Recommendations make sense for weak planets

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 6: SPECIAL POINTS
**Time:** 2 minutes | **Priority:** MEDIUM

### In Analysis Section:
1. [ ] Locate "Special Points" section
2. [ ] Brighu Bindu card visible:
   - [ ] Longitude shown
   - [ ] Sign displayed
   - [ ] House number shown
   - [ ] Description text
3. [ ] Gulika card visible with same info
4. [ ] Mandi card visible
5. [ ] Bhava Lagna card visible
6. [ ] Hora Lagna card visible

### Verify Accuracy:
7. [ ] All longitudes are 0-360°
8. [ ] Signs are valid (Aries-Pisces)
9. [ ] House numbers are 1-12
10. [ ] Descriptions are meaningful

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 7: ASHTAKOOT MATCHING (COMPATIBILITY)
**Time:** 6 minutes | **Priority:** HIGH

### Navigate to Compare Page:
1. [ ] Click "⚖️ Compare" button in header
2. [ ] Page loads with 2 forms side-by-side

### Fill Person 1:
3. [ ] Date: 1990-01-15
4. [ ] Time: 10:00
5. [ ] Location: New Delhi (28.6139, 77.2090)
6. [ ] Click "Calculate Chart" for Person 1
7. [ ] Chart 1 displays

### Fill Person 2:
8. [ ] Date: 1992-03-20
9. [ ] Time: 14:00
10. [ ] Location: Mumbai (19.0760, 72.8777)
11. [ ] Click "Calculate Chart" for Person 2
12. [ ] Chart 2 displays

### Verify Ashtakoot Section:
13. [ ] Ashtakoot section appears (purple gradient)
14. [ ] Total score out of 36 displayed
15. [ ] Percentage calculated
16. [ ] Compatibility rating shown (Excellent/Good/etc.)
17. [ ] All 8 Kootas listed:
    - [ ] Varna (1 point max)
    - [ ] Vashya (2 points max)
    - [ ] Tara (3 points max)
    - [ ] Yoni (4 points max)
    - [ ] Graha Maitri (5 points max)
    - [ ] Gana (6 points max)
    - [ ] Bhakoot (7 points max)
    - [ ] Nadi (8 points max)
18. [ ] Each koota shows:
    - [ ] Points scored / max points
    - [ ] Description of compatibility aspect
19. [ ] Recommendation text at bottom
20. [ ] If Nadi dosha, warning displayed

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 8: TRANSIT CALCULATIONS
**Time:** 4 minutes | **Priority:** MEDIUM

### Navigate to Transits:
1. [ ] Click "🌍 Transits" button in header
2. [ ] Transits page loads

### Fill Form:
3. [ ] Birth Date: 1990-01-15
4. [ ] Birth Time: 14:30
5. [ ] Latitude: 28.6139
6. [ ] Longitude: 77.2090
7. [ ] Click "Today" button
8. [ ] Today's date auto-fills in Transit Date
9. [ ] Click "🔮 Calculate Transits"

### Verify Results:
10. [ ] Transit date displayed in header
11. [ ] Current Planetary Positions card shows:
    - [ ] All 9 planets listed
    - [ ] Sign for each planet
    - [ ] Longitude (degrees) shown
12. [ ] Important Aspects card (if any)
13. [ ] Transit Effects card with predictions
14. [ ] Info box about transits at bottom
15. [ ] No errors in console

### Test Past/Future:
16. [ ] Change transit date to 1 month ago
17. [ ] Recalculate - positions change
18. [ ] Change to 1 month future
19. [ ] Recalculate - positions change again

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 9: BIRTH TIME RECTIFICATION
**Time:** 5 minutes | **Priority:** MEDIUM

### Navigate to Rectification:
1. [ ] Click "⏰ Rectify" button in header
2. [ ] Rectification page loads
3. [ ] Info box explaining rectification visible

### Fill Birth Details:
4. [ ] Approximate Date: 1990-01-15
5. [ ] Approximate Time: 14:00
6. [ ] Time Uncertainty: Select "±30 minutes"
7. [ ] Latitude: 28.6139
8. [ ] Longitude: 77.2090

### Add Life Events:
9. [ ] Event 1 Type: Marriage
10. [ ] Event 1 Date: 2015-05-20
11. [ ] Event 1 Description: "Got married in Delhi"
12. [ ] Click "+ Add Another Event"
13. [ ] Event 2 Type: Career
14. [ ] Event 2 Date: 2010-08-15
15. [ ] Event 2 Description: "Started new job"
16. [ ] Click "🔮 Rectify Birth Time"

### Verify Results:
17. [ ] Result section appears
18. [ ] Suggested Birth Time displayed
19. [ ] Before/After comparison shown
20. [ ] Adjustment in minutes (e.g., "+15 minutes")
21. [ ] Confidence score (percentage)
22. [ ] Confidence level (High/Moderate/Low)
23. [ ] Reasoning section with 4+ points
24. [ ] "Next Steps" guidance box
25. [ ] All text readable and makes sense

### Test Remove Event:
26. [ ] Generate new rectification
27. [ ] Add 3 events
28. [ ] Click "Remove" on middle event
29. [ ] Verify event is removed
30. [ ] Form still works

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 10: SAVE & LOAD CHARTS (Authentication)
**Time:** 5 minutes | **Priority:** HIGH

**Note:** Requires Supabase authentication setup

### Sign Up/Login:
1. [ ] Click user icon or "Sign Up" button
2. [ ] If not signed up:
   - [ ] Enter email
   - [ ] Enter password
   - [ ] Click "Sign Up"
   - [ ] Verify account (check email if required)
3. [ ] If already have account:
   - [ ] Enter credentials
   - [ ] Click "Login"
4. [ ] Verify logged in (user name/email in header)

### Save Chart:
5. [ ] Generate any birth chart
6. [ ] Look for "💾 Save Chart" button
7. [ ] Click save button
8. [ ] Enter chart name: "Test Chart 1"
9. [ ] Click "Save"
10. [ ] Success message appears
11. [ ] Chart name visible somewhere

### View Saved Charts:
12. [ ] Click user icon → "📊 My Charts"
13. [ ] My Charts page loads
14. [ ] Saved chart appears in list
15. [ ] Chart name matches "Test Chart 1"
16. [ ] Birth details preview visible

### Load Chart:
17. [ ] Click on saved chart
18. [ ] Chart loads on main page
19. [ ] All birth details match original
20. [ ] Planetary positions match
21. [ ] Analysis features still work

### Delete Chart (Optional):
22. [ ] Go back to My Charts
23. [ ] Look for delete/remove button
24. [ ] Click delete
25. [ ] Confirmation dialog appears
26. [ ] Confirm deletion
27. [ ] Chart removed from list

### Logout:
28. [ ] Click user icon
29. [ ] Click "Logout"
30. [ ] Redirected to home
31. [ ] User icon shows "Sign In" again

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 11: MOBILE RESPONSIVENESS
**Time:** 5 minutes | **Priority:** HIGH

### Desktop Browser Mobile Mode:
1. [ ] Open Chrome DevTools (F12)
2. [ ] Click device toolbar icon (phone icon)
3. [ ] Select "iPhone 12 Pro" or similar
4. [ ] Page resizes to mobile view

### Test Mobile Layout:
5. [ ] Header fits on screen
6. [ ] Navigation buttons accessible
7. [ ] Form fields large enough
8. [ ] Date/time pickers work
9. [ ] "Generate Chart" button visible and tappable

### Generate Chart on Mobile:
10. [ ] Fill form (smaller fields)
11. [ ] Submit form
12. [ ] Chart displays (may be smaller)
13. [ ] Chart is readable
14. [ ] Scroll works smoothly
15. [ ] No horizontal scrolling required

### Test Navigation:
16. [ ] Click "Compare" - mobile menu works
17. [ ] Click "Transits" - page loads
18. [ ] Click "Rectify" - page loads
19. [ ] Back button works
20. [ ] All pages responsive

### Test Different Sizes:
21. [ ] Switch to "iPad" (tablet)
22. [ ] Layout adjusts appropriately
23. [ ] Switch to "iPhone SE" (small phone)
24. [ ] Still usable, no breaks

### Actual Mobile Device (If Available):
25. [ ] Find your computer's IP address
26. [ ] Open http://[YOUR-IP]:3100 on phone
27. [ ] Test chart generation
28. [ ] Test navigation
29. [ ] Test form inputs

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## TEST 12: ERROR HANDLING & EDGE CASES
**Time:** 4 minutes | **Priority:** MEDIUM

### Test Invalid Inputs:
1. [ ] Leave date field empty, try submit
   - [ ] Error message appears
2. [ ] Enter invalid date (e.g., Feb 30)
   - [ ] Validation error shown
3. [ ] Enter latitude > 90
   - [ ] Error message shown
4. [ ] Enter negative time
   - [ ] Validation prevents or shows error

### Test Unusual Dates:
5. [ ] Birth at midnight (00:00)
   - [ ] Chart generates correctly
6. [ ] Birth at 23:59
   - [ ] Chart generates correctly
7. [ ] Leap year date (Feb 29, 2000)
   - [ ] Chart generates correctly
8. [ ] Very old date (Jan 1, 1920)
   - [ ] Chart generates (or shows limitation)
9. [ ] Future date (Jan 1, 2050)
   - [ ] Chart generates

### Test Network Issues:
10. [ ] Stop backend server
11. [ ] Try to generate chart
    - [ ] Error message appears
    - [ ] Error is user-friendly
    - [ ] App doesn't crash
12. [ ] Restart backend
13. [ ] Try again - works

### Browser Console Check:
14. [ ] Open console (F12)
15. [ ] Verify no unhandled errors
16. [ ] Check for warnings (acceptable)
17. [ ] No infinite loops or crashes

**Result:** ⬜ PASS  ⬜ FAIL  
**Notes:** ________________________________

---

## FINAL VERIFICATION CHECKLIST

### Core Functionality:
- [ ] Charts generate correctly
- [ ] All chart types display
- [ ] Yogas detection works
- [ ] Doshas detection works
- [ ] Planetary strength displays
- [ ] Special points calculate
- [ ] Ashtakoot matching works
- [ ] Transit calculations work
- [ ] Rectification works
- [ ] Save/load functionality (if auth setup)

### User Experience:
- [ ] Forms are intuitive
- [ ] Buttons work
- [ ] Navigation clear
- [ ] Loading states visible
- [ ] Error messages helpful
- [ ] No crashes or freezes
- [ ] Performance acceptable (< 10s per chart)

### Visual/Design:
- [ ] Charts look good
- [ ] Colors appropriate
- [ ] Text readable
- [ ] Layout not broken
- [ ] Mobile responsive
- [ ] No visual glitches

### Technical:
- [ ] No console errors (critical)
- [ ] Console warnings acceptable
- [ ] Network requests succeed
- [ ] API responses valid
- [ ] Data persists (if applicable)

---

## 📊 FINAL SCORE

**Total Tests:** 12  
**Tests Passed:** _____ / 12  
**Pass Rate:** _____ %

### Grading:
- **12/12 (100%):** ✅ Perfect - Production Ready
- **10-11/12 (83-92%):** ✅ Excellent - Minor fixes needed
- **8-9/12 (67-75%):** ⚠️ Good - Some work needed
- **6-7/12 (50-58%):** ⚠️ Fair - Significant work needed
- **< 6/12 (< 50%):** ❌ Needs Major Fixes

**Your Score:** ⬜ Production Ready  ⬜ Needs Minor Fixes  ⬜ Needs Work

---

## 🐛 BUGS FOUND

**List any bugs discovered during testing:**

1. _________________________________________________
   Severity: ⬜ Critical  ⬜ High  ⬜ Medium  ⬜ Low

2. _________________________________________________
   Severity: ⬜ Critical  ⬜ High  ⬜ Medium  ⬜ Low

3. _________________________________________________
   Severity: ⬜ Critical  ⬜ High  ⬜ Medium  ⬜ Low

---

## ✅ RECOMMENDATION

Based on your testing results:

**If 10+ tests passed:**
✅ **READY FOR BETA LAUNCH**
- Deploy to production
- Monitor for issues
- Gather user feedback

**If 8-9 tests passed:**
⚠️ **ALMOST READY**
- Fix critical bugs found
- Re-test failed areas
- Deploy after fixes

**If < 8 tests passed:**
❌ **MORE WORK NEEDED**
- Review all failures
- Fix critical issues
- Complete retest cycle

---

**Testing Completed By:** _____________________  
**Date:** _____________________  
**Time Spent:** _____________________  
**Overall Assessment:** _____________________

**Signature:** _____________________
