# Vedic Astrology Platform — Multi-Agent Orchestration System

## Overview

This orchestration system enables coordinated development of a Vedic astrology web platform using multiple specialized AI agents in a manual copy-paste workflow.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (You)                              │
│     Copy-paste prompts between this system and Claude sessions  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                           │
│           Coordination · Planning · Progress Tracking           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┬─────────────────────┐
        ▼                 ▼                 ▼                     ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   ACCURACY    │ │   BACKEND     │ │   FRONTEND    │ │     QA        │
│    AGENT      │ │    AGENT      │ │    AGENT      │ │    AGENT      │
│               │ │               │ │               │ │               │
│ Calculations  │ │ Python API    │ │ Next.js UI    │ │ Testing       │
│ JHora Valid.  │ │ Data Layer    │ │ UX/Visuals    │ │ Fixtures      │
└───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
                                           │
                                    ┌──────┴──────┐
                                    ▼             │
                             ┌───────────┐        │
                             │   INFRA   │◄───────┘
                             │   AGENT   │
                             │           │
                             │ CI/CD     │
                             │ Vercel    │
                             └───────────┘
```

---

## Directory Structure

```
orchestration-system/
├── README.md                          # This file
├── STATE_HANDOFF_SPEC.md              # State file format specifications
├── SESSION_TEMPLATES.md               # Copy-paste templates for sessions
│
├── prompts/                           # Agent system prompts
│   ├── ORCHESTRATOR_AGENT.md
│   ├── ACCURACY_AGENT.md
│   ├── BACKEND_AGENT.md
│   ├── FRONTEND_AGENT.md
│   ├── INFRA_AGENT.md
│   └── QA_AGENT.md
│
├── scripts/                           # Automation tools
│   └── jhora_extract.py               # JHora reference data extraction
│
├── fixtures/                          # Test data
│   └── sample_birth_data.json         # Standard test cases
│
└── state/                             # Runtime state (create in your project)
    ├── roadmap.json
    ├── blockers.json
    ├── git_log.md
    ├── agent_states/
    │   ├── accuracy.json
    │   ├── backend.json
    │   ├── frontend.json
    │   ├── infra.json
    │   └── qa.json
    └── decisions/
        └── ADR-001-example.md
```

---

## Quick Start

### 1. Initialize Project State

Create `.orchestra/state/` directory in your project root:

```bash
mkdir -p .orchestra/state/agent_states
mkdir -p .orchestra/state/decisions
```

Initialize `roadmap.json`:

```json
{
  "schema_version": "1.0",
  "last_updated": "2025-01-18T00:00:00Z",
  "updated_by": "orchestrator",
  "current_phase": {
    "id": 0,
    "name": "Project Assessment",
    "started": "2025-01-18T00:00:00Z"
  },
  "phases": [
    {"id": 0, "name": "Project Assessment", "status": "in_progress"},
    {"id": 1, "name": "Accuracy & Reliability", "status": "pending"},
    {"id": 2, "name": "Developer Experience", "status": "pending"},
    {"id": 3, "name": "Feature Expansion", "status": "pending"},
    {"id": 4, "name": "UX & Workflow", "status": "pending"}
  ],
  "tasks": []
}
```

Initialize `blockers.json`:

```json
{
  "schema_version": "1.0",
  "last_updated": "2025-01-18T00:00:00Z",
  "active_blockers": [],
  "resolved_blockers": []
}
```

### 2. Run First Orchestrator Session

1. Open new Claude conversation
2. Copy contents of `prompts/ORCHESTRATOR_AGENT.md`
3. Add current state (roadmap, blockers)
4. Request: "Begin Phase 0: Project Assessment. Analyze the codebase."
5. Provide codebase structure when requested

### 3. Execute Agent Tasks

For each task the Orchestrator assigns:

1. Open new Claude conversation for that agent
2. Copy agent's system prompt from `prompts/[AGENT]_AGENT.md`
3. Add task assignment from Orchestrator
4. Add relevant code files as context
5. Let agent execute
6. Capture output and update state files

---

## Workflow Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. ORCHESTRATOR SESSION                                         │
│    - Review current state                                       │
│    - Process completed agent work                               │
│    - Update roadmap                                             │
│    - Assign next priority tasks                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. AGENT SESSION(S)                                             │
│    - Execute assigned task                                      │
│    - Produce code/tests/docs                                    │
│    - Output session close report                                │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. STATE UPDATE                                                 │
│    - Update agent_states/[agent].json                           │
│    - Append to git_log.md                                       │
│    - Create handoff if needed                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
                         [Return to 1]
```

---

## Priority System

| Priority | Meaning | Examples |
|----------|---------|----------|
| **P0** | Critical, blocks everything | Accuracy validation, security fixes |
| **P1** | High, core functionality | Core calculations, main API endpoints |
| **P2** | Medium, important features | Additional features, optimizations |
| **P3** | Low, nice to have | UX polish, documentation updates |

---

## Agent Reference

| Agent | Focus | Key Outputs |
|-------|-------|-------------|
| **Orchestrator** | Coordination | Roadmap updates, task assignments |
| **Accuracy** | Calculations | Validated calc modules, JHora comparison |
| **Backend** | API | Endpoints, data models, API docs |
| **Frontend** | UI/UX | Components, pages, user flows |
| **Infra** | DevOps | CI/CD, deployment, monitoring |
| **QA** | Testing | Test suites, fixtures, coverage |

---

## JHora Validation Workflow

### Setup

1. Install Jagannatha Hora on Windows (or Wine on Linux/Mac)
2. Configure default settings:
   - Ayanamsa: Lahiri (Chitrapaksha)
   - House System: Whole Sign
   - Node: Mean

### Creating Reference Data

```bash
# Generate template for manual entry
python scripts/jhora_extract.py template \
  --birth-data fixtures/sample_birth_data.json \
  --output fixtures/jhora_reference/new_ref.json

# Validate completed reference
python scripts/jhora_extract.py validate \
  --input fixtures/jhora_reference/new_ref.json
```

### Validation Tolerances

| Calculation | Tolerance |
|-------------|-----------|
| Planetary longitude | ±0.01° |
| Dasha dates | ±1 day |
| Nakshatra pada | Exact |

---

## Git Workflow

### Branch Strategy

```
main          ← Production (deploy trigger)
  │
  └── develop ← Integration (staging deploy)
        │
        ├── feature/ACC-001-planetary-positions
        ├── feature/BE-005-chart-endpoint
        └── feature/FE-010-chart-wheel
```

### Commit Convention

```
type: short description

Types:
  feat:     New feature
  fix:      Bug fix
  refactor: Code restructuring
  test:     Adding tests
  docs:     Documentation
  chore:    Maintenance

Examples:
  feat: add Vimshottari dasha calculation
  fix: correct nakshatra boundary at 360°
  test: add JHora reference fixtures for dasha
```

---

## Escalation Rules

Agents escalate to Orchestrator, Orchestrator escalates to User.

### Agent → Orchestrator

- Tolerance exceeded (accuracy)
- Blocked >1 session
- Unclear requirements
- Dependency proposal

### Orchestrator → User

- 🔴 Proprietary dependency proposed
- 🔴 Breaking API change
- 🔴 Database schema migration
- 🔴 >1% accuracy deviation unexplained
- 🟡 Major architectural decision

---

## Files Reference

| File | Purpose | Updated By |
|------|---------|------------|
| `roadmap.json` | Task status | Orchestrator |
| `blockers.json` | Active blockers | Any agent |
| `git_log.md` | Git commands | All agents |
| `agent_states/*.json` | Agent checkpoints | Each agent |
| `decisions/ADR-*.md` | Architecture decisions | Orchestrator |

---

## Troubleshooting

### Agent Lost Context

Re-provide the checkpoint from `agent_states/[agent].json` and relevant files listed in `context_needed_next_session`.

### Conflicting Agent Outputs

Escalate to Orchestrator for resolution. Document decision in ADR.

### JHora Values Don't Match

1. Verify JHora settings (Lahiri, Whole Sign, Mean node)
2. Check timezone and DST handling
3. Document discrepancy with screenshots if needed

### State Files Out of Sync

Orchestrator session should reconcile state. Provide all state files and recent git log.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-18 | Initial release |

---

*End of README*
