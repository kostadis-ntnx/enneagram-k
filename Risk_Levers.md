# Risk Levers

Track who can force outcomes and under what conditions.

## Lever Inventory

| Lever Name | Holder | Trigger Condition | Blast Radius | Mitigation | Current Status |
|---|---|---|---|---|---|
| Validation Gate | Platform owner | Blocking checks enabled in CI | systemic | staged rollout, exception process | active |
| Canon Write Authority | Repo maintainers | direct edits to canonical pages | local | CODEOWNERS + review policy | active |
| Retrieval Confidence Threshold | Engram operator | threshold increased/decreased | local/systemic | monitor recall quality trend | latent |
| MCP Availability | Tooling owner | connector outage/misconfig | local | `doctor` command + fallback mode | latent |

## Lever Template

### Lever: Validation Gate

- Holder: Platform owner / pilot maintainer
- What it controls: whether unvalidated context can flow into normal delivery path
- Why it matters: strongest mechanism to prevent drift becoming production behavior
- Trigger condition: repeated unresolved blocking validation failures
- Earliest warning signs: warning volume spikes and stale-page backlog grows
- Immediate consequences: reduced throughput while validation debt is paid
- Downstream consequences: improved reliability if managed; team frustration if overused
- Mitigation path: phased enforcement, documented exceptions, and visible ROI metrics
- Owner: Engram pilot owner

## Deployment Rules

- Never deploy maximum-force levers as an opener.
- Prefer one clean deployment over repeated threats.
- Preserve ambiguity only when ambiguity itself is strategic.
- If a lever is used, document the outcome and trust impact.

## Review Questions

- Which levers are currently active?
- Which are bluff, which are real?
- Which can be neutralized through design instead of reaction?
