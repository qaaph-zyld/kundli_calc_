# ⚡ QUICK TEST GUIDE - START TESTING IN 5 MINUTES

**Goal:** Verify core functionality works before detailed testing  
**Time:** 15-20 minutes  
**Difficulty:** Easy

---

## 🚀 STEP 1: START THE APP (2 minutes)

### Terminal 1 - Backend
```bash
cd backend
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Check:** Should see: "Application startup complete"

### Terminal 2 - Frontend
```bash
cd frontend/next-app
npm run dev
```

**✅ Check:** Should see: "Local: http://localhost:3000"

### Verify Everything is Running
1. Open browser: `http://localhost:3000` → Should see Kundli Calculator homepage
2. Open API docs: `http://localhost:8000/docs` → Should see FastAPI documentation
3. Check console: No red errors

**✅ If all green → Continue**  
**❌ If errors → Check backend/frontend logs**

---

## 🧪 STEP 2: SMOKE TEST - BASIC FEATURES (10 minutes)

### Test #1: Generate Basic Chart (2 min)

**Input these values:**
```
Name: Test User
Date: 1990-01-15
Time: 14:30
Location: New Delhi, India
Latitude: 28.6139
Longitude: 77.2090
```

**Click:** "Generate Chart"

**✅ Verify:**
- [ ] Chart appears within 3 seconds
- [ ] South Indian chart visible (diamond shape)
- [ ] Planetary positions shown
- [ ] Ascendant displayed
- [ ] No errors in console (F12)

**✅ PASS** = Chart shows, no errors  
**❌ FAIL** = Error message or no chart

---

### Test #2: Chart Switching (1 min)

**Click each button:**
- [ ] "South Indian (D1)" → Chart displays
- [ ] "North Indian (D1)" → Different style chart
- [ ] "Navamsa (D9)" → New chart (planets in different positions)
- [ ] "Hora (D2)" → Another divisional chart

**✅ PASS** = All charts display without errors  
**❌ FAIL** = Charts don't load or errors appear

---

### Test #3: Analysis Features (3 min)

**Click:** "Show Analysis" button

**✅ Verify sections appear:**
- [ ] Ascendant description (at top)
- [ ] Yogas section (green/red cards)
- [ ] Doshas section (color-coded by severity)
- [ ] Planetary Strength section (with progress bars)
- [ ] Special Points section (Brighu Bindu, etc.)

**Click:** A dosha card's "Show Remedies" button
- [ ] Remedies list expands

**✅ PASS** = All sections visible, remedies expand  
**❌ FAIL** = Missing sections or errors

---

### Test #4: Ashtakoot Matching (4 min)

**1. Click:** "⚖️ Compare" in header

**2. Fill Person 1:**
```
Date: 1990-01-15
Time: 10:00
Location: New Delhi (28.6139, 77.2090)
```

**3. Fill Person 2:**
```
Date: 1992-03-20
Time: 14:00  
Location: Mumbai (19.0760, 72.8777)
```

**4. Click:** "Calculate Chart" for both

**✅ Verify:**
- [ ] Both charts display side by side
- [ ] Compatibility score shows (out of 100)
- [ ] Ashtakoot section appears (out of 36)
- [ ] All 8 kootas listed with scores
- [ ] Total score and percentage calculated
- [ ] Compatibility rating shown (Excellent/Good/etc.)

**✅ PASS** = Ashtakoot displays with all 8 kootas  
**❌ FAIL** = Missing sections or calculation errors

---

### Test #5: Transit Calculations (2 min)

**1. Click:** "🌍 Transits" in header

**2. Fill form:**
```
Birth Date: 1990-01-15
Birth Time: 14:30
Latitude: 28.6139
Longitude: 77.2090
```

**3. Click:** "Today" button (auto-fills transit date)

**4. Click:** "🔮 Calculate Transits"

**✅ Verify:**
- [ ] Current planetary positions displayed
- [ ] Today's date shown
- [ ] Planet list with signs and degrees
- [ ] Page loads without errors

**✅ PASS** = Transits show current positions  
**❌ FAIL** = Errors or no data

---

### Test #6: Birth Time Rectification (2 min)

**1. Click:** "⏰ Rectify" in header

**2. Fill form:**
```
Approximate Date: 1990-01-15
Approximate Time: 14:00
Time Uncertainty: ±30 minutes
Latitude: 28.6139
Longitude: 77.2090
```

**3. Add 1 life event:**
```
Type: Marriage
Date: 2015-05-20
Description: Got married in Delhi
```

**4. Click:** "🔮 Rectify Birth Time"

**✅ Verify:**
- [ ] Suggested time appears
- [ ] Before/After comparison shown
- [ ] Confidence score displayed (%)
- [ ] Reasoning points listed
- [ ] Adjustment in minutes shown

**✅ PASS** = Rectification result displays  
**❌ FAIL** = Errors or no results

---

## 📊 STEP 3: QUICK ACCURACY CHECK (3 minutes)

### Compare with Known Chart

**Test Chart: Gandhi**
```
Date: October 2, 1869
Time: 07:12 AM
Location: Porbandar (21.6417, 69.6293)
```

**Generate chart, then verify:**

**Expected Results:**
- Ascendant: **Libra** (Tula)
- Moon: **Leo** (Simha)
- Sun: **Virgo** (Kanya)

**✅ Check your results:**
- [ ] Ascendant = Libra ✅
- [ ] Moon in Leo ✅
- [ ] Sun in Virgo ✅

**If matches → Calculations accurate! ✅**  
**If doesn't match → Check Swiss Ephemeris setup ⚠️**

---

## 🌐 STEP 4: MOBILE TEST (2 minutes)

### Open on Phone
1. Find your computer's IP address
2. Open `http://[YOUR-IP]:3000` on phone
3. Try generating a chart

**✅ Verify:**
- [ ] Page loads on mobile
- [ ] Forms are usable
- [ ] Charts display (might be small but visible)
- [ ] Buttons are tappable
- [ ] No major layout breaks

**✅ PASS** = Usable on mobile  
**⚠️ NEEDS WORK** = Layout broken or unusable

---

## 💾 STEP 5: SAVE/LOAD TEST (2 minutes)

### Test Chart Persistence

**1. Sign Up/Login** (if not already)
- Click "Sign Up" or "Login"
- Create account or use existing

**2. Save a Chart**
- Generate any chart
- Click "💾 Save Chart"
- Enter name: "Test Chart 1"
- Click Save

**✅ Verify:**
- [ ] Success message appears
- [ ] Chart saved

**3. Load Chart**
- Click "👤" → "📊 My Charts"
- Click on saved chart

**✅ Verify:**
- [ ] Chart loads correctly
- [ ] All data preserved
- [ ] Birth details match

**✅ PASS** = Save and load works  
**❌ FAIL** = Data not persisting

---

## 📝 QUICK TEST RESULTS

### Fill this out after testing:

```
Date: ___________
Time taken: _____ minutes

RESULTS:
☐ Test #1: Basic Chart Generation - PASS / FAIL
☐ Test #2: Chart Switching - PASS / FAIL
☐ Test #3: Analysis Features - PASS / FAIL
☐ Test #4: Ashtakoot Matching - PASS / FAIL
☐ Test #5: Transit Calculations - PASS / FAIL
☐ Test #6: Birth Time Rectification - PASS / FAIL
☐ Test #7: Accuracy Check - PASS / FAIL
☐ Test #8: Mobile Test - PASS / FAIL  
☐ Test #9: Save/Load - PASS / FAIL

TOTAL: ___/9 PASSED

CRITICAL ISSUES FOUND:
1. _______________________
2. _______________________
3. _______________________

READY FOR DETAILED TESTING: YES / NO
```

---

## 🎯 NEXT STEPS

### ✅ If 9/9 or 8/9 PASS:
**Excellent! Your app is working!**
- Proceed to comprehensive testing (see TESTING_GUIDE.md)
- Test with more birth charts
- Do cross-browser testing
- Test edge cases

### ⚠️ If 6-7/9 PASS:
**Good progress, minor issues:**
- Fix failing tests
- Re-test failed features
- Check console for errors
- Review error logs

### ❌ If < 6/9 PASS:
**Needs attention:**
- Check backend is running properly
- Verify database connection
- Check frontend build
- Review logs for errors
- May need debugging session

---

## 🐛 COMMON ISSUES & FIXES

### Issue: "Connection refused" or API errors
**Fix:**
```bash
# Check backend is running
ps aux | grep uvicorn  # Mac/Linux
tasklist | findstr python  # Windows

# Restart backend if needed
cd backend
python -m uvicorn main:app --reload --port 8000
```

### Issue: Charts not displaying
**Fix:**
- Check browser console (F12) for errors
- Verify planetary_positions in API response
- Check network tab for failed requests

### Issue: Ashtakoot not showing
**Fix:**
- Verify both charts calculated successfully
- Check console for JavaScript errors
- Ensure backend returned Moon nakshatras

### Issue: Save/Load not working
**Fix:**
- Check Supabase connection
- Verify authentication working
- Check browser cookies enabled

### Issue: Mobile layout broken
**Fix:**
- Clear browser cache
- Check viewport meta tag
- Test in Chrome mobile mode (F12 → Device toolbar)

---

## 🎊 SUCCESS CRITERIA

**Your app is READY for detailed testing if:**
- ✅ 8-9 tests pass
- ✅ Charts generate consistently
- ✅ No critical errors in console
- ✅ Core features work as expected
- ✅ Mobile is usable (even if not perfect)

**Congratulations! You can now:**
1. Do comprehensive testing (TESTING_GUIDE.md)
2. Test with real users
3. Prepare for deployment
4. Gather feedback

---

**⏱️ Total Time: 15-20 minutes**  
**🎯 Goal: Verify core functionality before deep testing**  
**📋 Next: See TESTING_GUIDE.md for complete testing**

**Ready? Let's test! 🚀**
