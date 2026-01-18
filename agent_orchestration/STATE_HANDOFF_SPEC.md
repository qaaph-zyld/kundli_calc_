# State Handoff Specification v1.0

## Purpose

This document defines the canonical file formats for state persistence and inter-agent communication in a manual copy-paste orchestration workflow.

---

## Directory Structure

```
/project-root
├── .orchestra/                    # Orchestration state (gitignored sensitive, tracked structure)
│   ├── state/
│   │   ├── roadmap.json          # Master roadmap with task status
│   │   ├── agent_states/
│   │   │   ├── accuracy.json     # Accuracy agent last known state
│   │   │   ├── backend.json      # Backend agent last known state
│   │   │   ├── frontend.json     # Frontend agent last known state
│   │   │   ├── infra.json        # Infra agent last known state
│   │   │   └── qa.json           # QA agent last known state
│   │   └── blockers.json         # Active blockers
│   ├── handoffs/
│   │   └── YYYYMMDD_HHMMSS_[from]_to_[to].json  # Handoff records
│   ├── decisions/
│   │   └── ADR-NNN-[title].md    # Architectural Decision Records
│   └── git_log.md                # Git commands executed log
├── docs/
│   └── ...                       # Project documentation
└── tests/
    └── fixtures/
        └── jhora_reference/      # JHora validation data
```

---

## File Format Definitions

### 1. roadmap.json

```json
{
  "schema_version": "1.0",
  "last_updated": "2025-01-18T14:30:00Z",
  "updated_by": "orchestrator",
  "current_phase": {
    "id": 1,
    "name": "Accuracy & Reliability",
    "started": "2025-01-15T00:00:00Z",
    "target_completion": "2025-02-15T00:00:00Z"
  },
  "phases": [
    {
      "id": 0,
      "name": "Project Assessment",
      "status": "completed",
      "completed": "2025-01-14T00:00:00Z"
    },
    {
      "id": 1,
      "name": "Accuracy & Reliability",
      "status": "in_progress",
      "progress_pct": 35
    },
    {
      "id": 2,
      "name": "Developer Experience",
      "status": "pending"
    },
    {
      "id": 3,
      "name": "Feature Expansion",
      "status": "pending"
    },
    {
      "id": 4,
      "name": "UX & Workflow",
      "status": "pending"
    }
  ],
  "tasks": [
    {
      "id": "ACC-001",
      "phase": 1,
      "title": "Validate planetary longitude calculations",
      "assigned_to": "accuracy",
      "status": "completed",
      "priority": "P0",
      "created": "2025-01-15T00:00:00Z",
      "completed": "2025-01-17T00:00:00Z",
      "acceptance_criteria": [
        "All 9 planets within ±0.01° of JHora",
        "10+ test cases validated",
        "Automated tests added"
      ],
      "depends_on": [],
      "blocks": ["ACC-002", "BE-003"],
      "artifacts": [
        "tests/accuracy/test_planetary_positions.py",
        "tests/fixtures/jhora_reference/planets_ref_001.json"
      ],
      "notes": "Rahu/Ketu using mean node, matches JHora default"
    },
    {
      "id": "ACC-002",
      "phase": 1,
      "title": "Validate Vimshottari dasha calculations",
      "assigned_to": "accuracy",
      "status": "in_progress",
      "priority": "P0",
      "created": "2025-01-17T00:00:00Z",
      "acceptance_criteria": [
        "Mahadasha dates within ±1 day of JHora",
        "Bhukti dates within ±1 day",
        "Antardasha dates within ±1 day"
      ],
      "depends_on": ["ACC-001"],
      "blocks": ["FE-005"],
      "checkpoint": {
        "last_action": "Identified discrepancy in Moon nakshatra pada calculation",
        "next_action": "Review nakshatra boundary logic in src/calc/nakshatra.py",
        "files_modified": ["src/calc/dasha.py"]
      }
    }
  ]
}
```

### 2. agent_states/[agent].json

```json
{
  "schema_version": "1.0",
  "agent": "accuracy",
  "last_session": {
    "started": "2025-01-18T10:00:00Z",
    "ended": "2025-01-18T12:30:00Z",
    "duration_minutes": 150
  },
  "current_task": {
    "id": "ACC-002",
    "status": "in_progress",
    "progress_pct": 60,
    "checkpoint": {
      "summary": "Dasha calculation logic reviewed. Found nakshatra boundary issue.",
      "completed_steps": [
        "Extracted JHora reference data for 10 test charts",
        "Compared Mahadasha start dates - 3/10 within tolerance",
        "Identified root cause: Moon longitude → nakshatra mapping edge case"
      ],
      "next_steps": [
        "Fix nakshatra boundary calculation at 0°/360° wrap",
        "Re-run validation suite",
        "Add edge case test fixtures"
      ],
      "files_touched": [
        "src/calc/dasha.py",
        "src/calc/nakshatra.py",
        "tests/fixtures/jhora_reference/dasha_ref_001.json"
      ],
      "uncommitted_changes": true,
      "last_git_command": "git add tests/fixtures/jhora_reference/"
    }
  },
  "context_needed_next_session": [
    "src/calc/nakshatra.py (full file)",
    "src/calc/dasha.py:calculate_vimshottari() function",
    "tests/fixtures/jhora_reference/dasha_ref_001.json",
    "JHora nakshatra calculation reference"
  ],
  "blockers": [],
  "questions_for_orchestrator": [],
  "handoff_ready": false
}
```

### 3. Handoff Record (handoffs/YYYYMMDD_HHMMSS_[from]_to_[to].json)

```json
{
  "schema_version": "1.0",
  "timestamp": "2025-01-18T12:30:00Z",
  "from_agent": "accuracy",
  "to_agent": "backend",
  "task_id": "ACC-001",
  "handoff_type": "completion",
  "summary": "Planetary position calculations validated against JHora. All 9 planets within tolerance.",
  "artifacts_produced": [
    {
      "path": "src/calc/planets.py",
      "change_type": "modified",
      "description": "Fixed Rahu/Ketu calculation to use mean node"
    },
    {
      "path": "tests/accuracy/test_planetary_positions.py",
      "change_type": "new",
      "description": "15 test cases covering all planets, edge dates"
    },
    {
      "path": "tests/fixtures/jhora_reference/planets_ref_001.json",
      "change_type": "new",
      "description": "JHora reference data for 10 birth charts"
    }
  ],
  "validation_status": {
    "all_tests_pass": true,
    "jhora_comparison": "all_within_tolerance",
    "edge_cases_covered": ["year_boundary", "timezone_edge", "polar_latitude"]
  },
  "unblocks_tasks": ["ACC-002", "BE-003"],
  "notes_for_recipient": "Backend can now safely wrap planetary calculation in API. See test fixtures for expected response format.",
  "git_state": {
    "branch": "feature/planetary-accuracy",
    "last_commit": "a1b2c3d",
    "commit_message": "fix: planetary positions now match JHora within 0.01°"
  }
}
```

### 4. blockers.json

```json
{
  "schema_version": "1.0",
  "last_updated": "2025-01-18T14:00:00Z",
  "active_blockers": [
    {
      "id": "BLK-001",
      "created": "2025-01-18T11:00:00Z",
      "reported_by": "accuracy",
      "severity": "high",
      "title": "JHora uses different ayanamsa precision than documented",
      "description": "JHora internal ayanamsa calculation differs from published Lahiri formula by ~2 arc-seconds. Need to determine which to match.",
      "affects_tasks": ["ACC-003"],
      "proposed_resolution": "Match JHora exactly for consistency, document deviation from published formula",
      "requires_user_decision": true,
      "status": "awaiting_user_input"
    }
  ],
  "resolved_blockers": [
    {
      "id": "BLK-000",
      "title": "Swiss Ephemeris data files missing",
      "resolved": "2025-01-16T00:00:00Z",
      "resolution": "Downloaded from official source, added to repo"
    }
  ]
}
```

### 5. git_log.md

```markdown
# Git Command Execution Log

## 2025-01-18

### Session: Accuracy Agent (10:00 - 12:30)

```bash
# Branch creation
git checkout -b feature/dasha-accuracy

# Staging changes
git add tests/fixtures/jhora_reference/dasha_ref_001.json
git add src/calc/dasha.py

# Status check (uncommitted)
git status
# Modified: src/calc/nakshatra.py (not staged)
```

### Session: Backend Agent (13:00 - 14:30)

```bash
# Sync with main
git checkout main
git pull origin main

# Merge completed feature
git merge feature/planetary-accuracy

# Push
git push origin main
```

---

## 2025-01-17

### Session: Accuracy Agent

```bash
git checkout -b feature/planetary-accuracy
git add src/calc/planets.py
git add tests/accuracy/test_planetary_positions.py
git add tests/fixtures/jhora_reference/planets_ref_001.json
git commit -m "fix: planetary positions now match JHora within 0.01°"
```
```

### 6. ADR Template (decisions/ADR-NNN-[title].md)

```markdown
# ADR-001: Use Mean Node for Rahu/Ketu Calculations

## Status
Accepted

## Date
2025-01-17

## Context
JHora offers both Mean Node and True Node calculations for Rahu/Ketu. 
Our platform needs to choose a default that matches JHora's default behavior.

## Decision
Use **Mean Node** as the default calculation method for Rahu/Ketu positions.

## Rationale
1. JHora defaults to Mean Node
2. Traditional Vedic astrology texts primarily reference Mean Node
3. True Node can be offered as an optional setting later

## Consequences
- Planetary position tests will validate against Mean Node values
- API response will include `node_type: "mean"` field
- Future: Add user preference for True Node

## Alternatives Considered
1. **True Node default**: Rejected - does not match JHora default
2. **User must always specify**: Rejected - adds friction for common case
```

---

## Session Lifecycle Protocol

### Starting a New Agent Session

1. **Load State Files:**
   ```
   Read: .orchestra/state/roadmap.json
   Read: .orchestra/state/agent_states/[your_agent].json
   Read: .orchestra/state/blockers.json
   Read: .orchestra/git_log.md (last 2 sessions)
   ```

2. **Provide to Agent:**
   - Current task from roadmap
   - Agent's last checkpoint
   - Files listed in `context_needed_next_session`
   - Any relevant handoff records

3. **Agent Prompt Structure:**
   ```
   [Agent System Prompt]
   
   ---
   ## Current State
   [Paste roadmap.json excerpt for current task]
   [Paste agent_state.json]
   
   ---
   ## Context Files
   [Paste requested file contents]
   
   ---
   ## Instructions
   Continue from checkpoint. Your next steps are:
   [From agent_state.checkpoint.next_steps]
   ```

### Ending an Agent Session

1. **Agent Outputs:**
   - Updated `agent_states/[agent].json`
   - Handoff record if task completed
   - Git commands executed (for git_log.md)
   - Any blockers encountered

2. **Orchestrator Updates:**
   - `roadmap.json` task status
   - `blockers.json` if new blockers
   - `git_log.md` append

3. **Handoff to Next Agent:**
   - Create handoff JSON if cross-agent dependency resolved
   - Include handoff in next agent's session context

---

## Validation Rules

### JSON Schema Validation
All `.json` files must pass schema validation before committing. Schemas stored in `.orchestra/schemas/`.

### Required Fields
- Every task must have: `id`, `title`, `assigned_to`, `status`, `priority`
- Every agent state must have: `agent`, `last_session`, `current_task`
- Every handoff must have: `from_agent`, `to_agent`, `task_id`, `artifacts_produced`

### Status Transitions
```
pending → in_progress → completed
pending → blocked → in_progress → completed
in_progress → blocked → in_progress
```

Invalid transitions trigger orchestrator review.
