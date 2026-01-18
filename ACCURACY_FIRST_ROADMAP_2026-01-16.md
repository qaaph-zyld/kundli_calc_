# Accuracy-First Roadmap
**Date:** 2026-01-16  
**Mission:** Desktop-grade accuracy + Modern web UX + Classical knowledge depth

---

## Roadmap Philosophy

**Priority Order:**
1. **Accuracy & Correctness** - Non-negotiable foundation
2. **Developer Experience & Robustness** - Enable confident changes
3. **Feature Expansion** - Build on validated foundation
4. **UX & Workflow** - Polish the experience

**Execution Style:**
- Autonomous execution (minimal asks for approval)
- Coherent, mergeable commits
- Continuous progress with phase summaries
- Pause only for irreversible decisions or ambiguous requirements

---

## Phase 1: Core Accuracy & Reliability (P0)

**Goal:** Establish unquestionable calculation correctness

### Task 1.1: Document Calculation Formulas ⚡ CAN START NOW
**Priority:** P0  
**Effort:** 2-3 days  
**Dependencies:** None  
**Blocker:** None

**Scope:**
1. Planetary position calculations (Swiss Ephemeris usage)
2. Ayanamsa systems (formulas, precession rates)
3. House systems (Whole Sign, Placidus, etc.)
4. Vimshottari dasha (nakshatra-based calculation)
5. Yoga detection logic (classical conditions)
6. Divisional charts (division formulas)
7. Shadbala (component formulas)
8. Ashtakavarga (bindus and reductions)

**Output:** `docs/CALCULATION_FORMULAS_COMPLETE.md` with:
- Explicit mathematical formulas
- Classical text citations (BPHS chapter/verse)
- Code module references
- Example calculations

**Impact:** 
- Enable verification of correctness
- Facilitate debugging
- Build trust through transparency
- Educational value

**Autonomous Action:** START IMMEDIATELY

---

### Task 1.2: Create JHora Reference Data Template & Instructions ⚡ CAN START NOW
**Priority:** P0  
**Effort:** 0.5 days  
**Dependencies:** None  
**Blocker:** Manual JHora work required after this

**Scope:**
1. Enhanced `reference_charts/README.md` with step-by-step JHora export
2. JSON schema for reference data
3. Reference chart diversity requirements (10-15 charts)
4. Validation script template
5. Semi-automated data entry helper (if possible)

**Output:**
- Clear instructions for manual JHora work
- JSON templates for each chart
- Validation scripts ready to run
- Priority chart list (which charts to generate first)

**Impact:**
- Unblock accuracy validation
- Minimize manual effort
- Ensure consistent reference data format

**Autonomous Action:** START IMMEDIATELY

---

### Task 1.3: Automated Accuracy Test Execution ⏳ BLOCKED
**Priority:** P0  
**Effort:** 0.5 days (once unblocked)  
**Dependencies:** Task 1.2 complete + manual JHora data generation  
**Blocker:** Requires user to generate JHora reference data

**Scope:**
1. Execute all accuracy tests with reference data
2. Generate accuracy report
3. Fix any calculation discrepancies found
4. Document tolerance achievements
5. Create regression test suite

**Output:**
- Accuracy validation report (pass/fail by tolerance)
- Fixed calculation issues
- Regression prevention tests

**Impact:** 
- Proven accuracy claims
- Confidence in calculations
- Prevent future regressions

**Autonomous Action:** PREPARE (execute when unblocked)

---

### Task 1.4: Yoga Detection Classical Verification ⚡ CAN START NOW
**Priority:** P0  
**Effort:** 3-5 days  
**Dependencies:** None  
**Blocker:** None

**Scope:**
1. Review all 60+ yoga implementations in `extended_yogas.py`
2. Cross-reference with BPHS, Saravali, Phaladeepika
3. Document each yoga's classical definition
4. Verify condition logic matches classical rules
5. Add classical text citations to code comments
6. Create yoga validation test cases

**Output:**
- `docs/YOGA_CLASSICAL_VERIFICATION.md`
- Code comments with verse citations
- Yoga accuracy test suite
- Discrepancy report (if any)

**Impact:**
- Ensure yoga detection correctness
- Build trust in interpretations
- Educational value (show classical sources)

**Autonomous Action:** START IMMEDIATELY

---

## Phase 2: Developer Experience & Robustness (P1)

**Goal:** Enable confident changes and catch regressions

### Task 2.1: Fix Linting Errors & Enforce Quality ⚡ CAN START NOW
**Priority:** P1  
**Effort:** 1-2 days  
**Dependencies:** None  
**Blocker:** None

**Scope:**
1. Run flake8, black, isort on entire codebase
2. Fix all linting errors
3. Remove `continue-on-error` from CI
4. Add pre-commit hooks (optional)
5. Document code style guidelines

**Output:**
- Zero linting errors
- CI fails on quality issues
- Code style guide

**Impact:**
- Prevent technical debt accumulation
- Improve code maintainability
- Catch errors earlier

**Autonomous Action:** START IMMEDIATELY

---

### Task 2.2: Establish Test Coverage Baseline ⚡ CAN START NOW
**Priority:** P1  
**Effort:** 0.5 days  
**Dependencies:** None  
**Blocker:** None

**Scope:**
1. Run pytest with coverage reporting
2. Generate coverage report (HTML + terminal)
3. Document baseline coverage percentage
4. Identify low-coverage critical modules
5. Set coverage targets (80% overall, 90% for calculations)

**Output:**
- Coverage baseline report
- Coverage targets document
- CI coverage enforcement (future)

**Impact:**
- Visibility into test gaps
- Prevent coverage regression
- Guide test development priorities

**Autonomous Action:** START IMMEDIATELY

---

### Task 2.3: Frontend UX Audit ⚡ CAN START NOW
**Priority:** P1  
**Effort:** 1 day assessment  
**Dependencies:** None  
**Blocker:** None

**Scope:**
1. Review all frontend components
2. Test key workflows (input → chart → report → export)
3. Compare vs Astrosage/Astro.com UX
4. Document UX gaps and strengths
5. Create prioritized UX improvement backlog

**Output:**
- `docs/FRONTEND_UX_AUDIT.md`
- UX improvement backlog
- Screenshots/comparisons

**Impact:**
- Understand current UX quality
- Guide UX improvements
- Competitive positioning

**Autonomous Action:** START IMMEDIATELY

---

### Task 2.4: Implement Load Testing ⚡ CAN START NOW
**Priority:** P1  
**Effort:** 1-2 days  
**Dependencies:** None  
**Blocker:** None

**Scope:**
1. Set up Locust load testing framework
2. Create load test scenarios (chart calculation, dasha, yogas)
3. Test with 10, 50, 100, 200 concurrent users
4. Identify bottlenecks
5. Document performance characteristics
6. Add to CI/CD (optional)

**Output:**
- Locust test scripts
- Load testing report
- Performance bottleneck analysis
- Scaling recommendations

**Impact:**
- Understand capacity limits
- Identify optimization opportunities
- Production readiness validation

**Autonomous Action:** START IMMEDIATELY

---

## Phase 3: Feature Expansion (P2)

**Goal:** Address feature gaps identified in competitor analysis

### Task 3.1: Enhanced City Autocomplete ⚡ CAN START NOW
**Priority:** P2  
**Effort:** 1-2 days  
**Dependencies:** Task 2.3 (UX audit) recommended first  
**Blocker:** None

**Scope:**
1. Integrate Nominatim city search API
2. Add timezone detection
3. Implement autocomplete UI
4. Add location history (user accounts)
5. Test with international locations

**Output:**
- City autocomplete feature
- Timezone auto-detection
- Location history

**Impact:**
- Match Astrosage/Astro.com UX
- Reduce user errors
- Improve onboarding

**Autonomous Action:** PREPARE (can start after UX audit)

---

### Task 3.2: Chart Visualization Improvements ⚡ CAN START NOW
**Priority:** P2  
**Effort:** 2-3 days  
**Dependencies:** Task 2.3 (UX audit) recommended first  
**Blocker:** None

**Scope:**
1. Enhance D3.js chart rendering
2. Add South/North/East Indian style toggle
3. Implement interactive tooltips
4. Add print optimization
5. Improve mobile chart display

**Output:**
- Enhanced chart visualization
- Multiple chart style options
- Better mobile experience

**Impact:**
- Match or exceed JHora visual quality
- Improve user satisfaction
- Professional appearance

**Autonomous Action:** PREPARE (can start after UX audit)

---

### Task 3.3: Mobile Responsiveness Testing ⚡ CAN START NOW
**Priority:** P2  
**Effort:** 1-2 days  
**Dependencies:** Task 2.3 (UX audit) recommended first  
**Blocker:** None

**Scope:**
1. Test on multiple mobile devices (Chrome DevTools)
2. Fix responsive issues
3. Optimize touch interactions
4. Test form inputs on mobile
5. Validate chart display on small screens

**Output:**
- Mobile responsiveness report
- Fixed mobile issues
- Touch-optimized interactions

**Impact:**
- Capture mobile user segment
- Match GaneshaSpeaks mobile UX
- Broader reach

**Autonomous Action:** PREPARE (can start after UX audit)

---

## Phase 4: UX & Workflow Polish (P3)

**Goal:** Deliver exceptional user experience

### Task 4.1: Report Template Refinement
**Priority:** P3  
**Effort:** 1-2 days  
**Dependencies:** Phases 1-3 complete  

### Task 4.2: Progressive Web App (PWA)
**Priority:** P3  
**Effort:** 2-3 days  
**Dependencies:** Task 3.3 complete  

### Task 4.3: Internationalization (i18n)
**Priority:** P3  
**Effort:** 3-5 days  
**Dependencies:** UX polish complete  

### Task 4.4: User Accounts & Chart History
**Priority:** P3  
**Effort:** 3-5 days  
**Dependencies:** Backend architecture review  

---

## Execution Schedule

### Week 1: Foundation (Autonomous Start)
- ✅ Day 1-2: Document calculation formulas (Task 1.1)
- ✅ Day 2: Create JHora reference template (Task 1.2)
- ✅ Day 3-5: Yoga classical verification (Task 1.4)
- ✅ Day 2: Fix linting errors (Task 2.1)
- ✅ Day 2: Test coverage baseline (Task 2.2)

**Deliverables Week 1:**
- Calculation formula documentation
- JHora reference instructions
- Yoga verification report
- Zero linting errors
- Coverage baseline

### Week 2: Validation & Assessment
- ⏳ Day 1: Frontend UX audit (Task 2.3)
- ⏳ Day 2-3: Load testing (Task 2.4)
- ⏳ User action: Generate JHora reference data (manual)
- ⏳ Day 4: Execute accuracy tests (Task 1.3, once unblocked)
- ⏳ Day 5: Accuracy report and fixes

**Deliverables Week 2:**
- UX audit report
- Load testing report
- Accuracy validation (if JHora data available)

### Week 3+: Feature Enhancement
- Enhanced city autocomplete (Task 3.1)
- Chart visualization improvements (Task 3.2)
- Mobile responsiveness (Task 3.3)
- Progressive enhancement based on priorities

---

## Success Criteria

### Phase 1 (Core Accuracy)
- [x] Calculation formulas documented with citations
- [ ] JHora reference data available (requires user)
- [ ] Accuracy tests 100% passing within tolerances
- [x] Yoga detection verified vs classical texts
- [ ] Zero known calculation errors

### Phase 2 (Developer Experience)
- [ ] Zero linting errors, CI enforces quality
- [ ] Test coverage ≥ 80% overall, ≥ 90% calculations
- [ ] UX audit complete with improvement backlog
- [ ] Load testing complete, capacity known
- [ ] Performance optimizations implemented

### Phase 3 (Feature Expansion)
- [ ] City autocomplete with timezone detection
- [ ] Chart visualization matches/exceeds competitors
- [ ] Mobile experience validated
- [ ] All competitor UX gaps addressed

### Phase 4 (UX Polish)
- [ ] Professional report templates
- [ ] PWA with offline capability
- [ ] Hindi/English i18n
- [ ] User accounts and history

---

## Risk Mitigation

### Risk: JHora Reference Data Dependency
**Mitigation:** 
- Proceed with all non-blocked tasks immediately
- Create comprehensive instructions for user
- Prepare automated validation once data available

### Risk: Accuracy Issues Found
**Mitigation:**
- Swiss Ephemeris is industry-standard (low risk)
- Fix any discrepancies immediately
- Document tolerance reasoning
- Maintain regression test suite

### Risk: UX Changes Break Functionality
**Mitigation:**
- Frontend-backend integration tests already passing
- E2E tests with Playwright
- Incremental changes with testing

### Risk: Performance Bottlenecks
**Mitigation:**
- Already fast (~0.2s chart calculation)
- Redis caching configured
- Load testing will identify issues early
- Scalable architecture (Docker, ready for K8s)

---

## Autonomous Execution Plan

**Starting immediately (no approval needed):**
1. Task 1.1: Document calculation formulas
2. Task 1.2: JHora reference template
3. Task 1.4: Yoga classical verification
4. Task 2.1: Fix linting errors
5. Task 2.2: Test coverage baseline

**Next priority (start after above):**
6. Task 2.3: Frontend UX audit
7. Task 2.4: Load testing

**Blocked (requires user):**
- Task 1.3: Accuracy test execution (needs JHora data)

**Approach:**
- Work in parallel where possible
- Commit logical units frequently
- Update plan based on findings
- Report phase summaries
- Only pause for genuinely ambiguous items

---

## Metrics & Tracking

### Accuracy Metrics
- Planetary position error: Target ±0.01° (36 arcseconds)
- Ayanamsa error: Target ±0.001°
- Dasha date error: Target ±1 day
- Yoga detection accuracy: Target 95%+ classical match

### Quality Metrics
- Linting errors: 0
- Test coverage: 80%+ overall, 90%+ calculations
- CI green builds: 100%
- Code review pass rate: Target 100%

### Performance Metrics
- Chart calculation P95: < 500ms
- API response P95: < 500ms
- Concurrent users: 100+ sustained
- Uptime: 99.9%

### UX Metrics
- Input form completion: < 60s
- Chart comprehension: User testing scores
- Mobile usability: Lighthouse scores
- Error rate: < 1% of requests

---

**Roadmap Status:** ACTIVE  
**Current Phase:** 1 (Core Accuracy) + 2 (Developer Experience) in parallel  
**Next Review:** After Week 1 deliverables  
**Autonomous Execution:** APPROVED - Proceed without approval for P0-P2 tasks
