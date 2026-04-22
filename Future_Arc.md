# Future Arc (Optional)

This file exists for long-range ideas that may never run.

## Optionality Rule

- This arc may never happen.
- Run only if stakeholder/user interest is explicit.
- If not activated, treat as background and close the current project cleanly.

## Activation Triggers

- Trigger 1: Pilot repo meets at least two KPI targets for two consecutive monthly reviews.
- Trigger 2: Two additional teams request adoption with named maintainers.
- Trigger 3: Canon + memory validation overhead remains acceptable (<2 hours/week/team).

## Why This Arc Exists

The unresolved tension is between local repo reliability and organization-wide context reuse. v0.1 prioritizes single-repo trust and workflow fit; the future arc explores whether this can scale to multi-repo consistency without creating governance drag or noisy memory artifacts.

## Scope

- In scope:
  - multi-repo pattern library for canonical page types
  - cross-repo retrieval routing with provenance boundaries
  - role-based governance for shared operational knowledge
- Out of scope:
  - autonomous global canon merges without human ownership
  - replacing team-level architectural decision authority
  - broad enterprise platform redesign

## Four-Act Template

### Act I: Re-entry

- How the arc begins: move from one proven pilot to two additional repos with different change velocity profiles.
- New constraints: heterogeneous standards, ownership contention, and interoperability expectations.

### Act II: Acquisition

- What must be gathered/learned: adoption patterns, validation burden per repo, and common schema friction points.
- Primary risks: false standardization, overfitted templates, and centralized bottlenecks.

### Act III: Confrontation

- Core challenge: balancing consistency across repos with local autonomy and speed.
- Failure-forward outcomes: if global model fails, retain per-repo Engram baseline with documented divergence.

### Act IV: Settlement

- Force one explicit final choice.
- Define 3 viable endings and their costs.

Three viable endings:
1. Federated model: shared schema, local ownership (cost: moderate governance overhead).
2. Platform model: central policy with strict controls (cost: reduced team flexibility).
3. Local-first model: independent repo instances with optional sync (cost: reduced cross-repo discoverability).

## Exit Criteria

- A formal decision is made on federated vs platform vs local-first scaling, backed by observed operational and trust metrics from at least three repositories.
