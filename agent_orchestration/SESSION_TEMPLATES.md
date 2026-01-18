# Session Starter Templates

## Purpose

These templates provide the exact copy-paste structure for starting agent sessions in the manual orchestration workflow.

---

## 1. Orchestrator Session Starter

Copy this entire block when starting an Orchestrator session:

```markdown
# ORCHESTRATOR SESSION — [DATE]

## System Prompt
[Paste contents of prompts/ORCHESTRATOR_AGENT.md]

---

## Current Project State

### Roadmap (from .orchestra/state/roadmap.json)
```json
[Paste current roadmap.json content]
```

### Active Blockers (from .orchestra/state/blockers.json)
```json
[Paste current blockers.json content]
```

### Recent Git Activity (from .orchestra/git_log.md)
```
[Paste last 2 session entries from git_log.md]
```

---

## Agent States Summary

### Accuracy Agent
- Last task: [TASK_ID]
- Status: [completed/in_progress/blocked]
- Checkpoint: [Brief summary or "none"]

### Backend Agent
- Last task: [TASK_ID]
- Status: [completed/in_progress/blocked]
- Checkpoint: [Brief summary or "none"]

### Frontend Agent
- Last task: [TASK_ID]
- Status: [completed/in_progress/blocked]
- Checkpoint: [Brief summary or "none"]

### Infra Agent
- Last task: [TASK_ID]
- Status: [completed/in_progress/blocked]
- Checkpoint: [Brief summary or "none"]

### QA Agent
- Last task: [TASK_ID]
- Status: [completed/in_progress/blocked]
- Checkpoint: [Brief summary or "none"]

---

## Session Objectives

[User: Add what you want to accomplish this session]

1. 
2. 
3. 

---

## Instructions

Continue orchestration. Review state, process any completed work, update roadmap, and assign next priority tasks.
```

---

## 2. Sub-Agent Session Starter (Generic Template)

```markdown
# [AGENT NAME] SESSION — [DATE]

## System Prompt
[Paste contents of prompts/[AGENT]_AGENT.md]

---

## Current Assignment

### Task from Orchestrator
```markdown
---
TASK_ID: [XXX-NNN]
PRIORITY: [P0/P1/P2/P3]
PHASE: [1/2/3/4]

### Objective
[From orchestrator assignment]

### Context
[From orchestrator assignment]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Dependencies
- Blocked by: [TASK_IDs or "none"]
- Blocks: [TASK_IDs or "none"]
---
```

---

## Your Previous Checkpoint (if continuing)

```json
[Paste from .orchestra/state/agent_states/[agent].json → current_task.checkpoint]
```

---

## Relevant Files

### [file1.py]
```python
[Paste file contents]
```

### [file2.json]
```json
[Paste file contents]
```

---

## Instructions

[For new task]: Begin task execution following your protocol.
[For continuation]: Resume from checkpoint. Your next steps were: [list from checkpoint]
```

---

## 3. Accuracy Agent Session Starter

```markdown
# ACCURACY AGENT SESSION — [DATE]

## System Prompt
[Paste contents of prompts/ACCURACY_AGENT.md]

---

## Current Assignment

### Task
```markdown
---
TASK_ID: ACC-[NNN]
PRIORITY: P0
PHASE: 1

### Objective
[e.g., "Validate Vimshottari dasha calculation against JHora"]

### Context
[e.g., "Backend is waiting on validated dasha module. QA has prepared reference fixtures."]

### Acceptance Criteria
- [ ] All test cases within tolerance (±1 day for dates)
- [ ] 10+ diverse birth data validated
- [ ] Automated regression tests added
- [ ] Discrepancies documented with root cause

### Dependencies
- Blocked by: none
- Blocks: BE-012, FE-015
---
```

---

## Checkpoint (if continuing)
```json
{
  "completed_steps": [
    "Extracted JHora reference for 5 charts",
    "Identified discrepancy in Moon nakshatra calculation"
  ],
  "next_steps": [
    "Fix nakshatra boundary at 360°/0° wrap",
    "Re-run validation on all 10 test cases"
  ],
  "files_modified_uncommitted": [
    "src/calc/nakshatra.py"
  ]
}
```

---

## Relevant Files

### src/calc/dasha.py
```python
[Paste current implementation]
```

### src/calc/nakshatra.py
```python
[Paste current implementation]
```

### tests/fixtures/jhora_reference/dasha_ref_001.json
```json
[Paste JHora reference data]
```

---

## JHora Reference (if needed)

For manual comparison, use these settings in JHora:
- Ayanamsa: Lahiri (Chitrapaksha)
- House System: Whole Sign
- Node: Mean

---

## Instructions

[For new task]: Begin validation following your Validation Protocol.
[For continuation]: Resume from checkpoint. Fix nakshatra boundary issue first.
```

---

## 4. Handoff: Agent-to-Agent

When one agent completes work that unblocks another:

```markdown
# HANDOFF RECORD

## Metadata
- **From:** [Source Agent]
- **To:** [Target Agent]  
- **Task Completed:** [TASK_ID]
- **Date:** [DATE]

## Summary
[1-2 sentences describing what was accomplished]

## Artifacts Produced

| File | Type | Description |
|------|------|-------------|
| `src/calc/planets.py` | Modified | Fixed Rahu/Ketu mean node calculation |
| `tests/accuracy/test_planets.py` | New | 15 test cases, all passing |
| `tests/fixtures/jhora_reference/planets_ref_001.json` | New | JHora reference for 10 charts |

## Validation Status
- All accuracy tests: ✓ PASSING
- JHora comparison: ✓ WITHIN TOLERANCE
- Edge cases covered: ✓ YES

## For Recipient

### What you can now do
[e.g., "Backend can now wrap planetary calculation in /api/v1/charts endpoint"]

### API/Interface
```python
from src.calc.planets import calculate_planetary_positions

result = calculate_planetary_positions(birth_data)
# Returns: PlanetaryPositions with 9 planets
# Each planet has: longitude, latitude, speed, sign, nakshatra, pada, retrograde
```

### Test Data
Use `tests/fixtures/jhora_reference/planets_ref_001.json` for expected response format.

## Git State
- Branch: `feature/planetary-accuracy`
- Last commit: `a1b2c3d - fix: planetary positions match JHora`
- Status: Ready to merge to develop
```

---

## 5. Session Closer Template

At the end of every agent session, output:

```markdown
# SESSION CLOSE — [AGENT] — [DATE]

## Task Status
- **Task ID:** [XXX-NNN]
- **Status:** [COMPLETED / IN_PROGRESS / BLOCKED]
- **Progress:** [X]%

## Work Completed This Session
1. [Action taken]
2. [Action taken]
3. [Action taken]

## Files Changed
| File | Change |
|------|--------|
| `path/file.py` | [Description] |

## Git Commands Executed
```bash
git checkout -b [branch]
git add [files]
git commit -m "[message]"
```

## Checkpoint (if not completed)
```json
{
  "completed_steps": ["..."],
  "next_steps": ["..."],
  "files_modified_uncommitted": ["..."],
  "blockers": []
}
```

## Handoff Required
- [ ] Yes → Generate handoff record for [Agent]
- [x] No

## Questions for Orchestrator
- [If any, otherwise "None"]

## Updated Agent State (for .orchestra/state/agent_states/[agent].json)
```json
{
  "agent": "[agent]",
  "last_session": {
    "started": "[ISO timestamp]",
    "ended": "[ISO timestamp]"
  },
  "current_task": {
    "id": "[TASK_ID]",
    "status": "[status]",
    "progress_pct": [X],
    "checkpoint": { ... }
  },
  "context_needed_next_session": [
    "path/to/file1.py",
    "path/to/file2.json"
  ]
}
```
```

---

## Quick Reference: Copy-Paste Checklist

### Starting a Session
- [ ] Select correct agent prompt file
- [ ] Gather current state files (roadmap, blockers, agent state)
- [ ] Identify relevant code files for context
- [ ] Compose session starter with all elements
- [ ] Paste into new Claude conversation

### Ending a Session
- [ ] Capture agent's session close output
- [ ] Update `.orchestra/state/agent_states/[agent].json`
- [ ] Append git commands to `.orchestra/git_log.md`
- [ ] If task completed: update `roadmap.json`
- [ ] If handoff needed: create handoff record
- [ ] If blocked: update `blockers.json`

---

*End of Session Starter Templates*
