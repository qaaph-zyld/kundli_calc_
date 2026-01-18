# State Handoff Protocol

## Overview

This document defines the file formats and procedures for maintaining continuity across manually-orchestrated AI agent sessions. Each agent session receives a context package and produces a state output upon completion.

---

## Directory Structure

```
/project-root
├── .orchestra/                    # Orchestration state (git-tracked)
│   ├── STATE.md                   # Current project state snapshot
│   ├── ROADMAP.md                 # Master roadmap with status
│   ├── BLOCKERS.md                # Active blockers
│   ├── DECISIONS.md               # Architectural Decision Records
│   ├── sessions/                  # Session logs
│   │   ├── 2024-01-15_accuracy_001.md
│   │   └── 2024-01-15_backend_002.md
│   └── handoffs/                  # Inter-agent handoffs
│       ├── accuracy_to_qa.md
│       └── backend_to_frontend.md
├── docs/
│   └── api-spec.yaml              # OpenAPI spec (Backend → Frontend contract)
├── tests/
│   └── fixtures/
│       └── jhora_reference/       # JHora validation data
└── scripts/
    └── jhora/                     # JHora automation
```

---

## File Format Specifications

### 1. STATE.md — Project State Snapshot

**Purpose:** Single source of truth for current project status. Updated by Orchestrator after each session.

```markdown
# Project State

**Last Updated:** [ISO timestamp]
**Updated By:** [Agent Role]
**Session ID:** [YYYY-MM-DD_role_nnn]

## Current Phase
[Phase N: Name] — [X% complete]

## Active Tasks

| Task ID | Agent | Status | Priority | Description |
|---------|-------|--------|----------|-------------|
| ACC-001 | Accuracy | IN_PROGRESS | P0 | Validate planetary longitude calculations |
| BE-003 | Backend | BLOCKED | P1 | API endpoint for chart generation |
| FE-001 | Frontend | QUEUED | P2 | Chart visualization component |

## Completed This Cycle
- [Task ID]: [One-line summary] — [Date]

## Git State
```bash
Branch: [current branch]
Last Commit: [hash] — [message]
Uncommitted Changes: [Yes/No]
```

## Critical Context for Next Session
- [Bullet point of important context]
- [Anything the next agent MUST know]

## Files Modified This Session
- `path/to/file.py` — [change summary]
```

---

### 2. ROADMAP.md — Master Roadmap

**Purpose:** Phased task breakdown with dependencies and status tracking.

```markdown
# Project Roadmap

## Phase 1: Accuracy & Reliability [CURRENT]
Target: JHora parity on all core calculations

### Tasks

#### ACC-001: Planetary Position Validation [IN_PROGRESS]
- **Assigned:** Accuracy Agent
- **Priority:** P0
- **Dependencies:** None
- **Acceptance Criteria:**
  - [ ] All 9 planets within ±0.01° of JHora
  - [ ] 20+ test cases covering edge dates
  - [ ] Automated regression tests
- **Status Notes:** [Latest update from agent]
- **Blocked By:** None
- **Blocking:** BE-003, FE-002

#### ACC-002: Dasha Calculation Validation [QUEUED]
- **Assigned:** Accuracy Agent
- **Priority:** P0
- **Dependencies:** ACC-001
- **Acceptance Criteria:**
  - [ ] Vimshottari dasha dates within ±1 day of JHora
  - [ ] Bhukti/Antardasha validated
  - [ ] 10+ reference charts validated
- **Status Notes:** Waiting on planetary position fixes
- **Blocked By:** ACC-001
- **Blocking:** BE-004

---

## Phase 2: Developer Experience [PENDING]
[Tasks listed but not started]

## Phase 3: Feature Expansion [PENDING]
[Tasks listed but not started]

## Phase 4: UX & Workflow [PENDING]
[Tasks listed but not started]
```

---

### 3. Session Log Format — `sessions/YYYY-MM-DD_role_nnn.md`

**Purpose:** Complete record of what an agent did in a session. Enables resumption and audit.

```markdown
# Session Log

**Session ID:** 2024-01-15_accuracy_001
**Agent Role:** Accuracy Agent
**Date:** 2024-01-15
**Duration:** ~2 hours equivalent
**Orchestrator Task:** ACC-001

---

## Objective
Validate planetary longitude calculations against JHora reference for Lahiri ayanamsa.

## Starting State
- Branch: `feature/accuracy-validation`
- Last commit: `a1b2c3d` — "Add Swiss Ephemeris integration"
- Pending from last session: Fix Sun position calculation off by 0.03°

## Work Performed

### 1. Root Cause Analysis — Sun Position Discrepancy
**Finding:** Ayanamsa application was using mean instead of true ayanamsa.
**Fix:** Modified `src/calc/ayanamsa.py` line 45-52

### 2. Test Case Expansion
Added 15 new test cases to `tests/fixtures/jhora_reference/planetary_positions.json`
- Edge cases: year boundaries, retrograde periods, eclipse dates

### 3. Validation Results
| Planet | Max Deviation | Status |
|--------|---------------|--------|
| Sun | 0.008° | ✓ PASS |
| Moon | 0.005° | ✓ PASS |
| Mars | 0.012° | ⚠ MARGINAL |
| ... | ... | ... |

## Git Operations
```bash
git add src/calc/ayanamsa.py tests/fixtures/jhora_reference/
git commit -m "fix: correct ayanamsa calculation to use true ayanamsa

- Resolves Sun position discrepancy (was 0.03°, now <0.01°)
- Added 15 new JHora reference test cases
- Mars still marginally outside tolerance, see ACC-001-note"

git push origin feature/accuracy-validation
```

## Files Changed
| File | Lines | Change Type |
|------|-------|-------------|
| `src/calc/ayanamsa.py` | +12 -8 | Modified |
| `tests/fixtures/jhora_reference/planetary_positions.json` | +340 | Modified |
| `tests/test_planetary_positions.py` | +45 | Modified |

## Blockers Encountered
- **BLOCKER:** Mars calculation exceeds tolerance by 0.002°
  - **Root cause:** Suspected orbital perturbation calculation
  - **Action needed:** Deep dive into Swiss Ephemeris flags
  - **Blocking:** Full ACC-001 completion

## Handoffs Generated
- `handoffs/accuracy_to_qa.md` — New test fixtures ready for QA review

## Recommendations for Next Session
1. Continue with Mars position investigation — check `SEFLG_SPEED` flag
2. Once Mars resolved, proceed to ACC-002 (Dasha validation)

## End State
- Branch: `feature/accuracy-validation`
- Last commit: `d4e5f6g` — "fix: correct ayanamsa calculation..."
- Task status: IN_PROGRESS (90% complete, Mars blocker)
```

---

### 4. Handoff Format — `handoffs/source_to_target.md`

**Purpose:** Explicit communication between agents when one's output feeds another's input.

```markdown
# Agent Handoff

**From:** Accuracy Agent
**To:** QA Agent
**Date:** 2024-01-15
**Related Task:** ACC-001 → QA-001

---

## Handoff Type
[DATA | CODE | SPEC | BLOCKER_ESCALATION]

## Summary
Planetary position calculation validated for 8/9 planets. New JHora reference fixtures added. Ready for QA to verify test coverage and add edge cases.

## Artifacts Delivered

### Files Ready for QA
| File | Purpose | Action Needed |
|------|---------|---------------|
| `tests/fixtures/jhora_reference/planetary_positions.json` | Reference data | Verify format, add edge cases |
| `tests/test_planetary_positions.py` | Test suite | Review coverage, suggest additions |

### Validation Data Included
```json
{
  "reference_source": "JHora 8.0",
  "ayanamsa": "Lahiri",
  "house_system": "Whole Sign",
  "test_cases_count": 35,
  "validation_date": "2024-01-15"
}
```

## Assumptions Made
- JHora 8.0 output is authoritative
- Tolerance of ±0.01° is acceptable for production use

## Known Issues
- Mars position: 0.012° deviation on 3 test cases (under investigation)

## Questions for Recipient
1. Should we add retrograde-specific test cases?
2. Is 35 test cases sufficient coverage for Phase 1?

## Unblock Criteria
QA Agent confirms test suite is adequate → ACC-001 can close (pending Mars fix)
```

---

### 5. BLOCKERS.md — Active Blockers

**Purpose:** Centralized blocker tracking for orchestrator to prioritize.

```markdown
# Active Blockers

## Critical (Blocking P0 Tasks)

### BLOCK-001: Mars Position Deviation
- **Reported:** 2024-01-15
- **Reporter:** Accuracy Agent
- **Blocking Tasks:** ACC-001
- **Description:** Mars longitude calculation exceeds tolerance by 0.002° on 3 test cases
- **Root Cause:** Under investigation — suspected orbital perturbation flags
- **Escalation:** None yet
- **Owner:** Accuracy Agent
- **ETA:** Next session

---

## Medium (Blocking P1-P2 Tasks)

### BLOCK-002: [Title]
...

---

## Resolved This Week
- ~~BLOCK-000: Sun position discrepancy~~ — Fixed 2024-01-15 (ayanamsa calculation)
```

---

### 6. DECISIONS.md — Architectural Decision Records

**Purpose:** Document significant technical decisions for future reference.

```markdown
# Architectural Decision Records

## ADR-001: Lahiri Ayanamsa as Default

**Date:** 2024-01-10
**Status:** Accepted
**Context:** Multiple ayanamsa systems exist (Lahiri, Raman, KP, etc.)
**Decision:** Use Lahiri (Chitrapaksha) as default, with option for user override
**Rationale:** 
- Most widely used in India
- JHora default aligns with our validation strategy
- Indian government standard
**Consequences:** 
- Must validate all calculations specifically against Lahiri
- Future: add ayanamsa selector to UI

---

## ADR-002: Swiss Ephemeris for Planetary Calculations

**Date:** 2024-01-10
**Status:** Accepted
**Context:** Need accurate planetary position calculations
**Decision:** Use Swiss Ephemeris via `pyswisseph` wrapper
**Rationale:**
- Industry standard accuracy (sub-arc-second)
- Open source (GPL for free tier, professional license available)
- Same engine JHora uses internally
**Consequences:**
- Must include ephemeris data files in deployment
- ~50MB additional storage for full ephemeris range

---

## ADR-003: [Title]
...
```

---

## Orchestrator Workflow

### Starting a New Agent Session

1. **Prepare Context Package:**
```markdown
## Context Package for [Agent Role]

### Required Reading (copy into agent context)
1. STATE.md (current snapshot)
2. ROADMAP.md (relevant section for this agent)
3. Most recent session log for this agent role
4. Any pending handoffs TO this agent

### Task Assignment
[Copy from ROADMAP.md]

### Specific Instructions
[Any orchestrator guidance]
```

2. **Copy-Paste to Agent Session:**
   - System prompt (from `multi-agent-framework.md`)
   - Context package (above)
   - Relevant code files if needed

3. **Agent Executes:**
   - Agent works autonomously
   - Produces session log
   - Generates handoffs if needed

4. **Capture Output:**
   - Copy agent's final session log
   - Save to `sessions/YYYY-MM-DD_role_nnn.md`
   - Update STATE.md
   - Update ROADMAP.md task status
   - Save any handoffs

5. **Commit State:**
```bash
git add .orchestra/
git commit -m "orchestra: [Agent] session [ID] - [summary]"
```

---

## Git Commit Convention for Orchestration

```
orchestra: [Agent] session [ID] - [summary]
  │         │            │          │
  │         │            │          └── Brief description
  │         │            └── Session identifier
  │         └── accuracy|backend|frontend|infra|qa
  └── Prefix for orchestration commits
```

**Examples:**
```
orchestra: accuracy session 001 - planetary position validation progress
orchestra: state update - phase 1 at 60% completion
orchestra: blocker resolved - BLOCK-001 Mars position fixed
```
