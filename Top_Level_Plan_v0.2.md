# Ennegram v0.2 Top-Level Plan

## Goal
Improve recall precision and measurement rigor without expanding product surface area.

## Scope (In)
- Section-level wiki indexing/anchors for higher-signal recall hits
- Fallback re-ranking improvements for implementation-detail queries
- Baseline metrics bootstrap so KPI deltas are quantitatively measurable from day 1
- Continued single-repo operation in `CampaignGenerator`

## Scope (Out)
- New command families beyond the existing core loop
- Autonomous wiki authoring
- Multi-repo federation/governance
- Heavy UI redesigns

## Core Contract
- Canonical truth remains on-disk LLM-wiki pages.
- Recall must keep explicit provenance and confidence for every surfaced result.
- Validation remains mandatory before trust-sensitive use.
- Corrections remain first-class feedback into indexing/ranking behavior.

## Milestones
- M1: Precision indexing model agreed and implemented (section-level anchors)
- M2: Fallback ranking tuned with intent-aware boosts
- M3: Metrics bootstrap command/report in place and used before pilot
- M4: Pilot rerun completed with measurable deltas

## Success Metrics
- Reduce context misses per task by >=30% from v0.1 pilot level.
- Increase top-result relevance score (manual 1-5 rating) to >=4.5 average.
- Maintain provenance coverage at 100% on recalled items shown to operator.
- Maintain validation hygiene (`errors=0`, `warnings=0`) on weekly cadence.

## Exit Criteria
- v0.2 improvements implemented and exercised on at least 4 real tasks.
- Baseline and pilot metrics captured with explicit numeric deltas.
- At least 2 metrics show clear improvement over v0.1 pilot.
- Residual risks documented with next-scope recommendation (v0.3 or hold).
