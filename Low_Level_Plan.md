# Ennegram v0.1 Low-Level Plan

## 10 Working Day Execution Plan

### Day 1 - Contract Freeze
- Create `v0.1_scope.md` with in/out, success metrics, and exit criteria.
- Lock canonical truth + write-authority rules.
- Define accepted file formats and naming.

### Day 2 - Structure and Templates
- Create folder layout for wiki, schema, config, logs, reports.
- Define required metadata fields:
  - `owner`
  - `last_validated_at`
  - `source_refs`
  - `status`
- Create initial wiki templates: architecture, decisions, caveats, runbook.

### Day 3 - Implement `init`
- Scaffold all folders/files with defaults.
- Ensure idempotent behavior (safe re-run).
- Add basic command help and example invocation.

### Day 4 - Implement `ingest`
- Parse canonical pages and metadata.
- Skip invalid pages with clear reasons.
- Output ingest report (`indexed`, `skipped`, `errors`).

### Day 5 - Implement `recall`
- Query mempalace by prompt/topic.
- Return top results with:
  - provenance (file + anchor/section)
  - confidence
  - freshness signal
- Add fallback behavior for low-confidence recall.

### Day 6 - Implement `validate`
- Add checks for:
  - missing required metadata
  - stale pages
  - broken references
  - provenance gaps
- Emit human-readable and JSON reports.
- Separate `error` and `warning` severity.

### Day 7 - Add Manual Correction Loop
- Define `corrections.jsonl` schema.
- Document correction workflow (when/how to log).
- Log first real correction and map it to source update.

### Day 8 - Pilot Session A
- Use flow in two real coding tasks.
- Measure:
  - time-to-first-acceptable output
  - context misses
  - trust score (1-5)
- Capture friction notes immediately.

### Day 9 - Pilot Session B + Tightening
- Run two more real tasks.
- Fix top two friction points only.
- Re-run `validate` + `ingest` after fixes.

### Day 10 - Review and Decision
- Compare baseline versus pilot results.
- Write `v0.1_review.md`:
  - wins
  - misses
  - residual risks
  - v0.2 candidates (max 3)
- Decide continue, adjust, or pause.

## Lightweight Solo Operating Rules
- Build only one new command per week.
- Do not add features without a metric they should move.
- Prefer text-first, inspectable artifacts over hidden automation.
- Avoid refactors unless they unblock the pilot loop.
