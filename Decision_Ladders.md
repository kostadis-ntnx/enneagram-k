# Decision Ladders

Use ladders to stage escalation instead of jumping to irreversible actions too early.

## Ladder Template

### Ladder Name: Memory Trust Escalation

### Stage 1: Ambient Signals (Deniable)

- Signal examples: occasional low-confidence recalls, minor stale metadata, rising "verify" prompts.
- Decision options: monitor, assign owner, run targeted validation.
- Consequence if ignored: weak trust erosion and avoidable review churn.

### Stage 2: Material Evidence (Contested)

- Evidence examples: repeated provenance gaps in same domain, stale pages used in active tickets.
- Decision options: enforce refresh deadline, block affected workflow until validated.
- Consequence if ignored: incorrect AI guidance enters implementation path.

### Stage 3: Conflicting Testimony (Ambiguous)

- Conflict examples: mempalace recall contradicts canonical page; multiple owners assert different truths.
- Decision options: mark `conflicted`, favor canon temporarily, run conflict review.
- Consequence if ignored: teams cherry-pick context and diverge in behavior.

### Stage 4: Hard Proof (Irreversible)

- Proof condition: production-impacting decision traced to uncited or invalid memory.
- Required decision: pause affected automation path, apply guardrail hardening, publish incident note.
- Irreversible consequences: reduced team trust, delayed delivery, and stricter governance burden.

## Design Rules

- Do not jump from Stage 1 to Stage 4 without an explicit reason.
- Ensure each stage offers agency, not only exposition.
- Attach cost to every upside.
- Record major decisions and rationale immediately.

## Decision Log

| Date | Ladder | Stage | Decision | Why | Cost Accepted | Revisit Date |
|---|---|---|---|---|---|---|
| 2026-04-15 | Memory Trust Escalation | 1 | Enable provenance warnings only | collect baseline without blocking | possible false positives in early phase | 2026-04-22 |
