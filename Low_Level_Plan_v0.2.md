# Ennegram v0.2 Low-Level Plan

## 10 Working Day Execution Plan (Narrowed Scope)

### Day 1 - Contract and Baseline Setup
- Freeze v0.2 scope to precision + measurement improvements only.
- Define a simple relevance rating rubric (1-5) for recall outcomes.
- Add baseline metric capture placeholders to `v0.2_review.md`.

### Day 2 - Section-Level Index Design
- Define section anchor format for wiki ingestion (`#H2`, `#H3`, or line anchors).
- Decide chunking/section split rules for markdown pages.
- Document ingestion tradeoffs and expected retrieval behavior.

### Day 3 - Implement Section-Level Ingest
- Extend ingest to index section-level entries (not page-top only).
- Preserve backward compatibility for existing page-level entries where needed.
- Regenerate `ingest_report.json` and verify index integrity.

### Day 4 - Recall Anchor Surfacing
- Ensure recall output surfaces section-level anchors when available.
- Keep confidence/provenance formatting consistent.
- Validate no regressions in wiki-first behavior.

### Day 5 - Fallback Re-Ranking Tuning
- Add/adjust intent-aware boosts (symbol/file query hints).
- Reduce generic low-signal fallback dominance.
- Keep low-confidence warnings explicit.

### Day 6 - Metrics Bootstrap
- Add a repeatable baseline capture command or report workflow.
- Capture baseline metrics before v0.2 pilot reruns.
- Store outputs in `ennegram/reports/` with timestamped snapshots.

### Day 7 - Pilot Session A (v0.2)
- Run 2 real tasks with updated system.
- Record TTFA, misses/task, trust score, and relevance ratings.
- Log at least one correction if mismatch occurs.

### Day 8 - Pilot Session B (v0.2)
- Run 2 additional real tasks.
- Confirm behavior stability across task types (implementation vs policy lookup).
- Re-run `make en-ingest && make en-validate`.

### Day 9 - Tightening (Top 2 Frictions Only)
- Fix only top two observed frictions from v0.2 pilot.
- Re-run pilot spot checks for those failure modes.
- Snapshot updated metrics.

### Day 10 - Review and Decision
- Complete `v0.2_review.md` with baseline vs pilot deltas.
- Confirm exit criteria and residual risks.
- Decide continue to v0.3, continue narrowed, or hold.

## Operating Rules (v0.2)
- Optimize precision before adding features.
- Keep one source of truth for each metric.
- Avoid broad refactors outside the three v0.2 themes.
