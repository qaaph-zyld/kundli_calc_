# Accuracy-First Upgrade Roadmap
**Created:** December 18, 2024  
**Primary Goal:** Maximize astrological accuracy and consistency  
**Baseline:** Lahiri Ayanamsa + Whole Sign Houses

---

## PHASE 1: Core Accuracy & Reliability (Week 1-2)

### 1.1 Fix Test Infrastructure [HIGH]
- [ ] Fix SQLite "table exists" error in test fixtures
- [ ] Fix Pydantic V1→V2 deprecation warnings
- [ ] Fix FastAPI lifecycle deprecation
- [ ] Ensure all tests can run cleanly

### 1.2 Dasha Verification [CRITICAL]
- [ ] Add JHora reference for dasha balance at birth
- [ ] Verify Vimshottari mahadasha sequence dates
- [ ] Verify bhukti/antardasha timing
- [ ] Add automated tests for dasha accuracy
- [ ] Document dasha calculation formulas

### 1.3 KP System Verification [CRITICAL]
- [ ] Verify sub-lord boundary tables match KP standards
- [ ] Test sub-lord calculations against JHora
- [ ] Verify significator determination logic
- [ ] Add KP accuracy tests

### 1.4 Additional Reference Charts [HIGH]
- [ ] Add 5+ more JHora-verified charts
- [ ] Include edge cases (southern hemisphere, boundary dates)
- [ ] Create comprehensive test suite

---

## PHASE 2: Developer Experience & Robustness (Week 2-3)

### 2.1 Code Quality
- [ ] Migrate all Pydantic V1 validators to V2
- [ ] Update FastAPI lifespan handlers
- [ ] Add type hints to untyped functions
- [ ] Run and fix mypy/pyright issues

### 2.2 Test Coverage
- [ ] Target 80% backend coverage
- [ ] Add E2E tests with Playwright
- [ ] Add API integration tests
- [ ] Add frontend unit tests

### 2.3 CI/CD Fixes
- [ ] Fix Poetry vs pip mismatch in workflows
- [ ] Add accuracy verification to CI
- [ ] Add coverage reporting
- [ ] Add pre-commit hooks

### 2.4 Observability
- [ ] Add structured logging
- [ ] Add calculation timing metrics
- [ ] Set up error tracking

---

## PHASE 3: Feature Expansion (Week 3-4)

### 3.1 Complete Shadbala [HIGH]
- [ ] Implement all 6 strength components:
  - Sthana Bala (positional)
  - Dig Bala (directional)
  - Kala Bala (temporal)
  - Chesta Bala (motional)
  - Naisargika Bala (natural)
  - Drik Bala (aspectual)
- [ ] Verify against JHora values
- [ ] Add to API and frontend

### 3.2 Ashtakavarga Verification
- [ ] Verify bindu calculations for all planets
- [ ] Add Sarvashtakavarga
- [ ] Test against JHora

### 3.3 Yoga Enhancement
- [ ] Review all 60+ yoga detection rules
- [ ] Add 40 more yogas (target: 100)
- [ ] Cite BPHS/classical sources

### 3.4 Additional Ayanamsas
- [ ] Add Yukteshwar
- [ ] Add True Chitrapaksha
- [ ] Add Djwhal Khul
- [ ] Verify each against known values

---

## PHASE 4: UX & Workflow (Week 4-5)

### 4.1 Error Handling
- [ ] User-friendly error messages
- [ ] Input validation feedback
- [ ] Network error recovery

### 4.2 UI Improvements
- [ ] Loading states for all async ops
- [ ] Dark mode support
- [ ] Mobile responsiveness fixes
- [ ] Chart legends and help tooltips

### 4.3 Export Quality
- [ ] Improve PDF layout
- [ ] Add print stylesheet
- [ ] Add chart image export

### 4.4 Localization
- [ ] Complete Hindi translation
- [ ] Add Sanskrit planet names option

---

## IMMEDIATE EXECUTION TASKS

### Today's Priority (Accuracy-First)
1. **Fix test fixtures** - Enable full test suite
2. **Fix Pydantic deprecations** - Clean warnings
3. **Verify dasha calculations** - Add JHora comparison test
4. **Document calculation methods** - Add formula references

### Files to Modify
1. `backend/tests/conftest.py` - Fix DB fixture
2. `backend/app/api/endpoints/shadbala.py` - Pydantic V2
3. `backend/app/api/endpoints/lal_kitab.py` - Pydantic V2
4. `backend/app/api/endpoints/varshphal.py` - Pydantic V2
5. `backend/app/main.py` - Lifespan handlers
6. `backend/tests/test_accuracy_verification.py` - Fix fixture usage

---

## SUCCESS METRICS

### Phase 1 Complete When:
- [ ] All JHora reference tests pass (target: 50+)
- [ ] Zero Pydantic deprecation warnings
- [ ] Dasha timing within 1 day of JHora
- [ ] KP sub-lords 100% match JHora

### Phase 2 Complete When:
- [ ] 80% test coverage
- [ ] CI pipeline green
- [ ] All deprecations resolved

### Phase 3 Complete When:
- [ ] Shadbala matches JHora ±5%
- [ ] 100+ yogas implemented
- [ ] All ashtakavarga verified

### Phase 4 Complete When:
- [ ] Mobile Lighthouse score > 80
- [ ] PDF export professional quality
- [ ] Hindi translation complete

---

**Starting Execution Now...**
