# Ennegram v0.1 TODO

## Now

- [ ] Copy scaffold into one real target repo (`ennegram_cli.py`, `ennegram/`, `Makefile`).
- [ ] Replace placeholder wiki content with repo-specific architecture, decisions, caveats, and runbook details.
- [ ] Ensure all `source_refs` point to real local files or valid URLs.
- [ ] Run `make en-init && make en-ingest && make en-validate` in the target repo.
- [ ] Capture a baseline metric snapshot (time-to-first-acceptable output, context misses, trust score).

## This Week

- [ ] Use `make en-recall` during at least 3 real coding tasks and log misses.
- [ ] Use `make en-correct` whenever recall is partial/incorrect.
- [ ] Review `ennegram/reports/corrections_summary.json` and identify top recurring gaps.
- [ ] Update at least 2 canonical wiki pages based on correction feedback.
- [ ] Re-run `make en-ingest && make en-validate` after each wiki update.

## Before v0.1 Sign-off

- [ ] Demonstrate end-to-end flow working consistently for 2 weeks.
- [ ] Achieve >= 90% provenance coverage on recalls.
- [ ] Keep stale canonical pages under 10%.
- [ ] Compare pilot metrics vs baseline and document deltas.
- [ ] Write `v0.1_review.md` with wins, misses, and v0.2 candidates.
