# Canon Guardrails

Use this file to define what cannot drift.

## Hard Constraints

- LLM-wiki content is canonical source of truth for repo context.
- Mempalace cannot silently mutate canonical pages.
- No retrieval may be presented as authoritative without provenance.

## Operational Rules

- All canonical pages must declare owner and `last_validated_at`.
- Conflicts between memory and canon resolve in favor of canon until explicitly revised.
- Low-confidence or missing-provenance recalls must trigger verify-first behavior.

## Fail States

- Canonical page is stale beyond configured threshold and still used as active source.
- Memory item conflicts with canon and remains unresolved across one weekly cycle.
- AI output is accepted based on uncited memory where source should exist.

## Recovery Patterns

- Recovery for fail state 1: assign owner, refresh content, re-run validation, and log update timestamp.
- Recovery for fail state 2: mark memory item `conflicted`, capture correction, re-index from canonical source.
- Recovery for fail state 3: invalidate output decision, verify source, and add prevention check to pipeline.

## Integrity Checks (Per Session / Sprint)

- [ ] Did we violate any hard constraints?
- [ ] Did we trade short-term speed for long-term coherence?
- [ ] Did we preserve user/stakeholder agency?
- [ ] Did consequences match decisions?

## Escalation Policy

When a guardrail conflict appears:

1. Pause execution.
2. Name the violated constraint.
3. Choose one: preserve canon, explicitly revise canon, or branch.
4. Log rationale in `Decision_Ladders.md`.

Escalation SLA:
- Critical violations: same-day response.
- Non-critical integrity drift: resolve within one weekly cycle.
