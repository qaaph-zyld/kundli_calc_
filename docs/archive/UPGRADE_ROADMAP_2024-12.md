# Kundli Calculator - Accuracy-First Upgrade Roadmap
**Date:** December 2024  
**Standard:** Lahiri Ayanamsa + Whole Sign Houses  
**Reference:** Jagannatha Hora

---

## Competitor Benchmark Summary

### Web Competitors (Primary Comparison)
| Feature | AstroSage | Astro.com | Our App | Gap |
|---------|-----------|-----------|---------|-----|
| Chart accuracy | ✅ Swiss Eph | ✅ Swiss Eph | ✅ Swiss Eph | None |
| Vimshottari Dasha | ✅ | ✅ | ✅ | None |
| Divisional Charts | 16+ | 6 | 16 | None |
| Yogas | 50+ | 10 | 60+ coded | ⚠️ Not exposed |
| KP System | ✅ | ❌ | ⚠️ Coded | ⚠️ Not verified |
| Transits | ✅ | ✅ | ⚠️ Coded | ⚠️ Not verified |
| Ashtakavarga | Full | Basic | ⚠️ Coded | ⚠️ Not verified |
| Multi-language | 10+ | 5+ | ❌ | ❌ Missing |
| Mobile UX | ✅ | ✅ | ⚠️ Basic | ⚠️ Needs work |
| PDF Reports | 50pg | Basic | Basic | ⚠️ Needs expansion |

### Desktop Reference (Accuracy Standard)
| Feature | Jagannatha Hora | Our App | Status |
|---------|-----------------|---------|--------|
| Planetary positions | Reference | ±0.1° | ✅ Verified |
| Ascendant | Reference | ±0.1° | ✅ Verified |
| Vimshottari Dasha | Reference | ±2 days | ✅ Verified |
| Nakshatra/Pada | Reference | Exact | ✅ Verified |
| KP Sub-lords | Reference | ? | ❓ Not verified |
| Ashtakavarga bindus | Reference | ? | ❓ Not verified |
| Shadbala values | Reference | ? | ❓ Not verified |
| Advanced Dashas | Reference | ? | ❓ Not verified |

---

## Phase 1: Core Accuracy & Reliability (PRIORITY)

### 1.1 API Completeness ✅ DONE
**Status:** Completed just now
- [x] Register yogas endpoint `/api/v1/yogas`
- [x] Register transits endpoint `/api/v1/transits`
- [x] Register KP endpoint `/api/v1/kp`
- [x] Register shadbala endpoint `/api/v1/shadbala`
- [x] Register ashtakavarga endpoint `/api/v1/ashtakavarga`
- [x] Register bhava endpoint `/api/v1/bhava`
- [x] Register prediction endpoint `/api/v1/prediction`
- [x] Register additional_dashas endpoint `/api/v1/dashas`
- [x] Register horoscope endpoint `/api/v1/horoscope`
- [x] Register compatibility endpoint `/api/v1/compatibility`

### 1.2 Accuracy Verification Tests
**Effort:** 4-6 hours | **Impact:** Critical

Create reference tests comparing to JHora for:
- [ ] KP cuspal sub-lords (5 levels)
- [ ] Ashtakavarga bindu values (per planet)
- [ ] Shadbala component values
- [ ] Yogini Dasha periods
- [ ] Ashtottari Dasha periods
- [ ] Transit positions at specific dates

**Deliverable:** `tests/test_jhora_full_reference.py`

### 1.3 Fix Known Calculation Issues
- [ ] Verify Rahu/Ketu always retrograde
- [ ] Validate outer planet (Uranus/Neptune/Pluto) positions
- [ ] Check special lagna calculations
- [ ] Verify Ashtakavarga trikona/ekadhi reductions

### 1.4 Add Regression Test Suite
**Effort:** 2-3 hours | **Impact:** High

Create fixture-based tests that don't require running API:
- [ ] User's birth chart (Oct 9, 1990, Loznica) as baseline
- [ ] Famous chart references (Gandhi, Nehru, etc.)
- [ ] Edge cases (0° Aries, retrograde planets)

---

## Phase 2: Developer Experience & Robustness

### 2.1 Test Infrastructure
- [ ] Remove empty test files
- [ ] Add pytest fixtures for common test data
- [ ] Create mock Swiss Ephemeris for unit tests
- [ ] Add CI test for all endpoints

### 2.2 Error Handling
- [ ] Improve API error messages
- [ ] Add input validation for edge cases
- [ ] Handle timezone edge cases
- [ ] Add logging for calculation steps

### 2.3 Performance
- [ ] Add response time logging
- [ ] Implement calculation caching
- [ ] Profile heavy endpoints (charts/calculate)
- [ ] Target: <2s for full chart calculation

### 2.4 Documentation
- [ ] Update OpenAPI spec to match actual endpoints
- [ ] Add calculation formula documentation
- [ ] Document ayanamsa/house system options
- [ ] Add API usage examples

---

## Phase 3: Feature Expansion

### 3.1 Complete KP System
- [ ] Verify cuspal sub-lords (Star, Sub, Sub-Sub)
- [ ] Add planet significator tables
- [ ] Implement ruling planets (RP)
- [ ] Add horary chart support (1-249)

### 3.2 Additional Dasha Systems
- [ ] Verify Yogini Dasha
- [ ] Verify Ashtottari Dasha
- [ ] Add Chara Dasha (Jaimini)
- [ ] Add Narayana Dasha

### 3.3 Enhanced Transit Analysis
- [ ] Real-time transit positions
- [ ] Transit over natal chart overlay
- [ ] Gochara predictions from Moon
- [ ] Sade Sati phase tracking

### 3.4 Ashtakavarga Enhancement
- [ ] Sarva Ashtakavarga (SAV) display
- [ ] Bhinna Ashtakavarga (BAV) per planet
- [ ] Transit scoring using Ashtakavarga
- [ ] Sodhya pinda calculations

### 3.5 Missing Features
- [ ] Prashna (Horary) charts
- [ ] Muhurta finder
- [ ] Birth time rectification
- [ ] Special lagnas (Hora, Ghati, Varnada)

---

## Phase 4: UX & Workflow

### 4.1 Frontend Integration
- [ ] Connect KPSystemPanel to `/api/v1/kp`
- [ ] Connect MuhurtaPanel to backend
- [ ] Add loading states for slow calculations
- [ ] Improve error display

### 4.2 Chart Display
- [ ] Add planetary aspect lines
- [ ] Show nakshatra/pada in chart
- [ ] Add dignity indicators (exalted/debilitated)
- [ ] Improve mobile chart rendering

### 4.3 Reports
- [ ] Expand PDF report (30+ pages)
- [ ] Add interpretation text
- [ ] Include dasha timeline visualization
- [ ] Add remedy suggestions

### 4.4 Internationalization
- [ ] Complete Hindi translations
- [ ] Add Sanskrit terminology option
- [ ] Support multiple date formats
- [ ] Add timezone selector

---

## Immediate Execution Queue

### Now (This Session)
1. ✅ Register missing API endpoints
2. Create KP verification test against JHora
3. Create Ashtakavarga verification test
4. Create Shadbala verification test
5. Test all new endpoints work correctly

### Next Session
6. Fix any accuracy issues found
7. Add regression test suite
8. Connect frontend panels to new endpoints
9. Update documentation

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| API Endpoints | 12 | 22 ✅ |
| JHora-verified features | 5 | 15 |
| Test coverage | ~40% | 80% |
| Calculation accuracy | ±0.1° | ±0.05° |
| Chart load time | 3-5s | <2s |
| Frontend panels connected | 8 | 15 |

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| KP calculations wrong | High | Verify against JHora before exposing |
| Breaking existing accuracy | Critical | Regression tests before changes |
| Performance degradation | Medium | Benchmark before/after |
| Frontend breaks | Medium | E2E tests for critical flows |
