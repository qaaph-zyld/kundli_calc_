# KUNDLI CALCULATOR UPGRADE ROADMAP
## Accuracy-First Development Plan

**Created:** December 1, 2024  
**Baseline:** Lahiri Ayanamsa + Whole Sign Houses  
**Reference Standard:** Jagannatha Hora (JHora) for calculations  

---

## 🏆 COMPETITOR ANALYSIS

### Primary Web Competitors

| Feature | AstroSage | Drikpanchang | Prokerala | **Our App** |
|---------|-----------|--------------|-----------|-------------|
| **Chart Generation** | ✅ | ✅ | ✅ | ✅ |
| **Multiple Ayanamsas** | ✅ (5+) | ✅ (4) | ✅ (3) | ✅ (4) |
| **Vimshottari Dasha** | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| **Extended Dashas** | ⚠️ Limited | ⚠️ Limited | ❌ | ✅ 15+ |
| **KP System** | ✅ Full | ❌ | ❌ | ⚠️ Needs work |
| **Divisional Charts** | ✅ D1-D60 | ✅ D1-D12 | ⚠️ Basic | ✅ D1-D60 |
| **Yogas** | ✅ 50+ | ✅ 30+ | ⚠️ Basic | ✅ 50+ |
| **Ashtakavarga** | ✅ | ✅ | ❌ | ✅ |
| **Transits** | ✅ | ✅ | ⚠️ | ⚠️ |
| **Compatibility** | ✅ | ✅ | ✅ | ⚠️ |
| **Panchang** | ✅ | ✅ Full | ⚠️ | ✅ |
| **Multi-language** | ✅ 8+ | ✅ 5 | ⚠️ 2 | ⚠️ Setup only |
| **PDF Export** | ✅ | ✅ | ✅ | ✅ |
| **Mobile App** | ✅ | ✅ | ✅ | ❌ |
| **API Access** | ❌ | ❌ | ❌ | ✅ **Advantage** |

### Desktop Reference (JHora)
- Gold standard for calculation accuracy
- All dasha systems with correct timing
- Extensive varga chart support
- Free, open-source

### Gap Summary

| Category | Gap Level | Priority |
|----------|-----------|----------|
| **Accuracy vs JHora** | ⚠️ Unverified | 🔴 CRITICAL |
| **KP System** | ⚠️ Incomplete | 🟡 HIGH |
| **Transit Predictions** | ⚠️ Basic | 🟡 HIGH |
| **Multi-language Content** | ⚠️ Infrastructure only | 🟢 MEDIUM |
| **Mobile App** | ❌ Missing | 🟢 MEDIUM |
| **API Quality** | ✅ Ahead | ✅ Strength |

---

## 📋 PHASED UPGRADE ROADMAP

### PHASE 1: Core Accuracy & Reliability (PRIORITY)
**Goal:** Ensure all calculations match JHora with Lahiri + Whole Sign

| Task | Complexity | Impact | Status |
|------|------------|--------|--------|
| 1.1 Fix default house system to Whole Sign | Low | High | 🔄 TODO |
| 1.2 Validate planetary positions vs JHora | Medium | Critical | 🔄 TODO |
| 1.3 Validate Vimshottari Dasha timing | Medium | Critical | 🔄 TODO |
| 1.4 Fix mock values in ayanamsa.py | Low | High | 🔄 TODO |
| 1.5 Add JHora reference test suite | High | Critical | 🔄 TODO |
| 1.6 Verify Navamsa (D9) calculations | Medium | High | 🔄 TODO |
| 1.7 Fix yoga detection accuracy | High | High | 🔄 TODO |
| 1.8 Add birth rectification warnings | Low | Medium | 🔄 TODO |

**Deliverables:**
- Automated test suite comparing to JHora reference values
- All planetary positions within 0.1° of JHora
- All dasha dates within 1 day of JHora
- Clear documentation of calculation formulas

---

### PHASE 2: Developer Experience & Robustness
**Goal:** Reliable CI/CD, comprehensive testing, observability

| Task | Complexity | Impact |
|------|------------|--------|
| 2.1 Add missing requirements (prometheus_client etc.) | Low | High |
| 2.2 Create comprehensive API tests | Medium | High |
| 2.3 Add E2E frontend tests (Playwright) | High | High |
| 2.4 Set up proper CI with health checks | Medium | Medium |
| 2.5 Add structured logging | Low | Medium |
| 2.6 Performance benchmarks | Medium | Medium |
| 2.7 API rate limiting | Low | Medium |

**Deliverables:**
- 80%+ test coverage
- Green CI pipeline
- Performance dashboard
- API documentation improvements

---

### PHASE 3: Feature Expansion
**Goal:** Match/exceed competitor feature depth

| Task | Complexity | Impact |
|------|------------|--------|
| 3.1 Complete KP System | High | High |
| 3.2 Add Lal Kitab predictions | High | Medium |
| 3.3 Improve transit predictions | Medium | High |
| 3.4 Add Varshphal (annual horoscope) | High | Medium |
| 3.5 Improve compatibility matching | Medium | High |
| 3.6 Add Muhurta improvements | Medium | Medium |
| 3.7 Add famous charts database | Low | Low |

**Deliverables:**
- Feature parity with Astrosage for core features
- Working KP system with sublords
- Comprehensive transit analysis

---

### PHASE 4: UX & Workflow
**Goal:** Modern, clear web UX matching competitors

| Task | Complexity | Impact |
|------|------------|--------|
| 4.1 Improve chart rendering quality | Medium | High |
| 4.2 Add chart type switcher (North/South/Circle) | Low | Medium |
| 4.3 Mobile responsive improvements | Medium | High |
| 4.4 Multi-language content population | High | Medium |
| 4.5 Improve interpretations/explanations | High | High |
| 4.6 Add birth time rectification UI | Medium | Medium |
| 4.7 Chart comparison feature | Medium | Medium |

**Deliverables:**
- Polished, professional UX
- Mobile-first design
- Clear interpretations for non-astrologers

---

## 🚀 IMMEDIATE NEXT ACTIONS (Phase 1.1-1.4)

### 1. Fix Default House System to Whole Sign
**File:** `backend/app/core/astronomical/framework.py`
**Issue:** Line 344 uses Placidus ('P') as default
**Fix:** Change to Whole Sign ('W')

### 2. Remove Mock Values in Ayanamsa
**File:** `backend/app/core/calculations/ayanamsa.py`  
**Issue:** Lines 107-113 use hardcoded test values
**Fix:** Use Swiss Ephemeris swe.get_ayanamsa_ut() properly

### 3. Add JHora Reference Tests
**Create:** `backend/tests/test_jhora_reference.py`
**Content:** Test cases with known JHora outputs

### 4. Verify Dasha Calculations
**File:** `backend/app/core/calculations/dasha_system.py`
**Action:** Validate nakshatra balance calculation

---

## 📊 SUCCESS METRICS

### Accuracy Metrics
- [ ] All planetary positions within 0.05° of JHora
- [ ] All dasha dates within 1 day of JHora
- [ ] All varga charts matching JHora
- [ ] Yoga detection accuracy >95%

### Quality Metrics
- [ ] 80%+ test coverage
- [ ] API response time <200ms
- [ ] Zero critical bugs
- [ ] CI pipeline always green

### User Metrics (future)
- [ ] Chart generation success rate >99%
- [ ] User retention rate tracking
- [ ] Feature usage analytics

---

## 🔧 TECHNOLOGY STACK (Current)

### Backend
- **Framework:** FastAPI (Python 3.9+)
- **Ephemeris:** Swiss Ephemeris (pyswisseph)
- **Database:** MongoDB + PostgreSQL
- **Cache:** Redis
- **Monitoring:** Prometheus + Grafana

### Frontend
- **Framework:** Next.js 14 (React 18)
- **Styling:** CSS Modules
- **Charts:** D3.js, Custom SVG
- **i18n:** i18next
- **Auth:** Supabase

### All OSS/Free Tier Tools
- No paid dependencies
- Self-hostable infrastructure
- Free tier cloud options available

---

*This roadmap follows accuracy-first principles with Lahiri ayanamsa and Whole Sign houses as defaults.*
