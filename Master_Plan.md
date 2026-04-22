# Master Plan

## Project Snapshot

- Domain: AI-enabled software engineering productivity
- Project name: Engram v0.1
- Owner: AI Enablement / Developer Productivity (pilot owner: TBD)
- Start date: 2026-04-15
- Current phase: v0.1 planning and pilot setup

## Problem Statement

Engineering teams lose time and quality when each AI session starts cold, repo-specific caveats are hidden as tribal knowledge, and documentation drifts from implementation. Engram v0.1 targets developers and AI enablement teams by introducing a repo-native context contract that keeps canonical knowledge discoverable, retrievable, and validated. The urgency is immediate because teams are already relying on AI for coding, test authoring, deployment automation, and service operations; without structure and validation, output quality and trust degrade as usage scales.

## Strategic Outcome

Within one pilot repository, developers can bootstrap an AI-ready knowledge layer in minutes, retrieve context with provenance and freshness signals, and correct memory mistakes in a feedback loop. Success is not only a generated artifact; it is repeated behavior: teams maintain canonical wiki pages as part of normal engineering rhythm, run validation before major changes, and treat memory correction as routine hygiene. The system should feel lightweight enough to use daily while making context drift visible and actionable.

## Objectives (90-Day Horizon)

1. Objective A: Ship an end-to-end Engram v0.1 CLI flow (`init -> ingest -> recall -> validate -> correct -> doctor`) for one pilot repo.
2. Objective B: Improve AI-assisted development outcomes in pilot tasks (faster first acceptable output, fewer context-related review rounds).
3. Objective C: Establish measurable knowledge reliability via provenance coverage, staleness tracking, and correction auditability.

## Non-Goals

- Full autonomous wiki authoring without human review.
- Cross-repo global knowledge graph and enterprise-grade federation.
- ML model fine-tuning, custom embedding training, or ranking research.
- Deep IAM/authorization frameworks beyond simple ownership and role checks.
- Replacing existing code review; Engram complements review with better context.

## Critical Assumptions

- Teams will maintain LLM-wiki pages if update friction is low and ownership is explicit.
- Mempalace can serve as effective retrieval/index infrastructure over canonical wiki content.
- Developers will provide corrections when retrieval is wrong if correction is one command and clearly logged.

## Core Architecture

Describe the system as components and flows:

- Inputs: Repo-local LLM-wiki pages, metadata (`owner`, `last_validated_at`, refs), and optional operational notes from active workstreams.
- Processing/decision layer: Engram CLI validates canonical docs, indexes into mempalace, retrieves context with provenance/confidence, and enforces conflict/fallback rules.
- Outputs: Structured recalls for AI sessions, validation reports, correction logs, and updated index entries.
- Feedback loops: User correction loop (`correct`) feeds re-indexing; weekly validation cadence flags drift; decision logs update canonical pages and retrieval behavior.

## Milestones

- M1 (Week 1-2): Finalize schema + CLI command contracts; scaffold pilot repo with `engram init`.
- M2 (Week 3): Implement and test `ingest` + `recall` with mandatory provenance and confidence.
- M3 (Week 4-5): Implement `validate` + `correct` + correction audit log; add conflict handling.
- M4 (Week 6): Pilot evaluation against KPI targets and produce v0.2 decision memo.

## Metrics

- Leading indicators: percent of recalls with provenance; percent canonical pages with owner/freshness metadata; correction turnaround time.
- Lagging indicators: reduction in time-to-first-acceptable AI output; reduction in context-related PR revision rounds; user trust score trend.
- Failure signals: high stale-page ratio, unresolved memory/wiki conflicts, low correction adoption, or users bypassing Engram flow.

## Decision Cadence

- Daily: Capture correction events and decision rationale in canonical logs.
- Weekly: Run validation sweep, stale-page review, and pilot KPI checkpoint.
- Monthly: Evaluate architecture and process adjustments; approve v0.2 scope changes.

## Open Questions

- Q1: What minimal metadata set balances rigor and developer adoption friction?
- Q2: Should `validate` fail hard on low confidence, or only on missing provenance/freshness?
- Q3: How should Engram handle inferred knowledge that lacks direct canonical citation?
