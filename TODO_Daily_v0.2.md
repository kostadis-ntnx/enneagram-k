# Ennegram v0.2 Daily TODO (10-Day)

## Day 1 - Contract and Baseline Setup
- [x] Freeze v0.2 scope to precision + measurement only.
- [x] Define recall relevance rating rubric (1-5).
- [x] Initialize `v0.2_review.md` baseline placeholders.

## Day 2 - Section-Level Index Design
- [x] Define section anchor format for wiki ingest.
- [x] Define markdown section split rules.
- [x] Document design tradeoffs briefly.

## Day 3 - Section-Level Ingest Implementation
- [x] Implement section-level ingest entries.
- [x] Preserve compatibility with existing index use.
- [x] Run ingest and inspect report.

## Day 4 - Recall Anchor Surfacing
- [x] Ensure recall prints section-level anchors when available.
- [x] Confirm provenance/confidence formatting unchanged.
- [x] Spot-check wiki-first ordering.

## Day 5 - Fallback Re-Ranking Tuning
- [x] Improve fallback ranking for implementation-detail queries.
- [x] Reduce generic low-signal fallback dominance.
- [x] Verify low-confidence warnings remain visible.

## Day 6 - Metrics Bootstrap
- [ ] Add repeatable baseline capture workflow/command.
- [ ] Capture baseline metric snapshot.
- [ ] Store baseline snapshot in reports.

## Day 7 - Pilot Session A
- [ ] Use Ennegram in 2 real coding tasks.
- [ ] Capture TTFA, misses/task, trust, relevance ratings.
- [ ] Log at least one correction if mismatch occurs.

## Day 8 - Pilot Session B
- [ ] Use Ennegram in 2 more real tasks.
- [ ] Capture same metric set as Day 7.
- [ ] Re-run `make en-ingest && make en-validate`.

## Day 9 - Tightening
- [ ] Fix top 2 frictions only.
- [ ] Re-run targeted checks.
- [ ] Snapshot updated metrics.

## Day 10 - Review and Decision
- [ ] Complete `v0.2_review.md`.
- [ ] Confirm v0.2 exit criteria.
- [ ] Decide continue, narrow, or hold.
