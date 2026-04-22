# Ennegram v0.1 Top-Level Plan

## Goal
Build a solo-operator v0.1 that reduces LLM cold-start friction, improves context reliability, and creates a lightweight correction loop for memory errors.

## Scope (In)
- CLI commands: `init`, `ingest`, `recall`, `validate`
- Repo-local LLM-wiki as canonical source of truth
- Mempalace as indexing/retrieval layer
- Manual correction logging via `corrections.jsonl`
- Single-repo pilot validation

## Scope (Out)
- Autonomous wiki writing without review
- Multi-repo federation and shared governance
- Advanced ranking/retrieval tuning
- Full MCP bootstrap orchestration
- Heavy enterprise auth/permissions

## Core Contract
- Canonical truth is on-disk LLM-wiki pages.
- Retrieval layer never silently mutates canon.
- Every recall includes provenance and confidence.
- Validation enforces freshness, ownership, and integrity.
- Corrections are logged and fed back into indexing.

## Milestones
- M1: Define schema and scaffolding contract.
- M2: Deliver `init` and stable repo layout.
- M3: Deliver `ingest` and `recall` with source attribution.
- M4: Deliver `validate` and drift reporting.
- M5: Run pilot tasks and record KPI deltas.

## Success Metrics
- Time-to-first-acceptable output improves by >=30%.
- Context-related revision loops reduce by >=20%.
- Provenance coverage on recalls >=90%.
- Stale canonical pages remain <10% at weekly check.

## Exit Criteria
- End-to-end flow works reliably: `init -> ingest -> recall -> validate`
- Used on real tasks for two consecutive weeks
- At least two KPI targets show measurable improvement
- v0.2 backlog is derived from observed usage
