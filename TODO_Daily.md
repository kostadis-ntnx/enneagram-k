# Ennegram v0.1 Daily TODO (10-Day)

## Standalone Quickstart
- Run from `Engram_v01_Workspace`.
- Default target repo is `CampaignGenerator`.
- First repo setup: `./en init --data-root /path/to/ennegram-data/repo-name --wiki-root /path/to/ennegram-wiki/repo-name`
- `./en ingest`
- `./en r "where is chunking implemented" --mode code --max-results 3`
- Override target inline: `./en --target /path/to/repo r "query"`

## Day 1 - Contract Freeze
- [ ] Confirm v0.1 in-scope and out-of-scope items.
- [ ] Confirm success metrics and exit criteria.
- [ ] Confirm canonical truth and write-authority rules.

## Day 2 - Structure and Templates
- [x] Verify `ennegram/` directory structure in target repo.
- [x] Replace wiki placeholders with real repo content.
- [x] Validate frontmatter metadata is complete in every wiki page.

## Day 3 - Init Command Confidence
- [x] Run `make en-init` twice and confirm idempotent behavior.
- [x] Confirm no unexpected file overwrites.
- [x] Note any setup friction in `v0.1_review.md` draft notes.

## Day 4 - Ingest Reliability
- [x] Run `make en-ingest`.
- [x] Review `ennegram/reports/ingest_report.json`.
- [x] Fix any skipped entries and re-run ingest.

## Day 5 - Recall Quality
- [x] Run `make en-recall QUERY="..."` for 2 active tasks.
- [x] Confirm each response includes provenance and confidence.
- [x] Log at least one observed gap or edge case.

## Day 6 - Validate Rules
- [x] Run `make en-validate`.
- [x] Resolve validation errors/warnings.
- [x] Re-run until clean, then snapshot report.

## Day 7 - Correction Loop
- [x] Log corrections with `make en-correct` for real misses.
- [x] Review `ennegram/reports/corrections_summary.json`.
- [x] Update one wiki page based on correction patterns.

## Day 8 - Pilot Session A
- [x] Use Ennegram in 2 real coding tasks.
- [x] Capture metrics (time-to-first-acceptable output, context misses, trust score).
- [x] Add short notes on what helped and what slowed you down.

## Day 9 - Pilot Session B + Tightening
- [x] Use Ennegram in 2 more real tasks.
- [x] Fix top 2 friction points only (avoid broad refactor).
- [x] Re-run `make en-ingest && make en-validate`.

## Day 10 - Review and Decision
- [x] Compare baseline and pilot metric deltas.
- [x] Write `v0.1_review.md` (wins, misses, residual risks).
- [x] List up to 3 v0.2 candidates.
- [x] Decide: continue, adjust scope, or pause.
