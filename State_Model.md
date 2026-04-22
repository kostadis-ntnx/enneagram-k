# State Model

Define how critical entities move through states.

## Entity Types

- Canonical wiki pages
- Memory/index entries (mempalace)
- Validation and correction pipeline

## Default Three-State Pattern

Use this unless a different model is necessary:

- `Ready`: full function, low risk
- `Strained`: usable with complications
- `Burned`: unavailable until repaired/replaced

## Transition Rules

- Ready -> Strained triggers:
  - content age exceeds freshness window
  - rising unresolved warnings
  - frequent low-confidence retrievals for same area
- Strained -> Burned triggers:
  - missing provenance on required recalls
  - unresolved canon-memory conflicts across one full weekly cycle
  - validation failures ignored on high-impact workflows
- Burned -> Ready recovery path:
  - freeze impacted area for authoritative usage
  - restore canonical page correctness and ownership
  - reconcile index entries via re-ingest
  - pass validation with zero blocking failures

## Exposure / Pressure Mapping

Map environment pressure to degradation risk:

- Low pressure: stable repo, low change velocity, predictable workflows.
- Medium pressure: moderate refactors, onboarding activity, increasing AI usage.
- High pressure: incident response, migration bursts, frequent architecture changes.

## Recovery Actions

- Quick fix: patch stale metadata, hot-fix broken references, re-run targeted validation.
- Full rebuild: regenerate wiki section ownership + references and re-index dependent memories.
- Strategic replacement: replace unreliable memory pathways or page structure with simpler canonical model.

## Tracking Table (Template)

| Entity | State | Last Change | Trigger | Owner | Next Action |
|---|---|---|---|---|---|
| Architecture page | Ready | 2026-04-15 | init | pilot-owner | monitor freshness weekly |
| Retrieval entry set | Strained | 2026-04-15 | low confidence spike | memory-owner | run correction sweep |
| Validation pipeline | Ready | 2026-04-15 | baseline configured | tools-owner | enforce pre-merge checks |
