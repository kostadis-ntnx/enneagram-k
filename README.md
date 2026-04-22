# enneagram-k

Standalone Ennegram tooling for repository-aware context indexing and recall.

This project is intentionally separated from application repositories. It can target any repo for recall, while storing per-repo operational data and wiki canon outside the tool repository.

## What This Tool Does

- Indexes canonical wiki knowledge into a searchable memory index.
- Answers queries with wiki-first recall and code/docs fallback.
- Logs corrections and promotions to improve knowledge quality over time.
- Supports mempalace sync workflows via generated push/pull artifacts.
- Runs as either a CLI tool or an MCP server.

## Core Design

- **Tooling repository**: this repository (`enneagram-k`) holds code, templates, and config.
- **Target repository**: the repo you want Ennegram to reason about (set via `ENNEGRAM_TARGET_ROOT`).
- **Data root (per target repo)**: logs/reports/index storage outside this repo.
- **Wiki root (per target repo)**: canonical wiki markdown outside this repo.

This keeps Ennegram reusable and avoids mixing tool internals with product codebases.

## Repository Layout

- `ennegram_cli.py`: main CLI entry point.
- `ennegram_mcp_server.py`: MCP server exposing Ennegram operations.
- `en`: shell wrapper for convenient local usage.
- `ennegram/config/`: tool configuration (`ennegram.yaml`).
- `ennegram/schema/`: schema files.
- `ennegram/wiki/`: template seed location (not canonical per-repo wiki storage).

## Quick Start

From this repository root:

1. Initialize once for a target repo:
   - `ENNEGRAM_TARGET_ROOT=/path/to/target/repo ./en init --data-root /path/to/ennegram-data/repo-name --wiki-root /path/to/ennegram-wiki/repo-name`
   - `--wiki-root` is optional and defaults to `<data-root>/wiki`.
2. Ingest wiki:
   - `ENNEGRAM_TARGET_ROOT=/path/to/target/repo ./en ingest`
3. Run recall:
   - `ENNEGRAM_TARGET_ROOT=/path/to/target/repo ./en r "where is chunking implemented" --mode code --max-results 3`

After first `init`, roots are remembered per target repo and reused automatically.

## Wrapper Script (`./en`)

- Defaults target repo to `CampaignGenerator` in this environment.
- Supports inline override:
  - `./en --target /path/to/repo r "query"`
- Forwards remaining args directly to `ennegram_cli.py`.

## Common Commands

- `./en init --data-root ... [--wiki-root ...]`
- `./en ingest`
- `./en recall "query" --max-results 5`
- `./en r "query"` (alias)
- `./en r "query" --mode code`
- `./en validate`
- `./en correct <entry_id> --verdict <correct|partial|incorrect> --note "..."`
- `./en promote <wiki_entry> --note "..." [--title "..."] [--source-uri "..."]`
- `./en memory-log --tail 20`
- `./en sync-mempalace [--import-file path.json] [--mark-synced]`

## Data Produced Per Repo

Under `<data-root>`:

- `logs/index.json`
- `logs/corrections.jsonl`
- `logs/promotions.jsonl`
- `logs/memory_events.jsonl`
- `logs/mempalace_sync_state.json`
- `logs/mempalace_imports.jsonl`
- `reports/ingest_report.json`
- `reports/validate_report.json`
- `reports/corrections_summary.json`
- `reports/mempalace_push_payload.json`
- `reports/mempalace_pull_template.json`

Under `<wiki-root>`:

- Canonical wiki markdown pages (for example: `architecture.md`, `runbook.md`, `decisions.md`, `caveats.md`).

## MCP Mode

Run:

- `python3 ennegram_mcp_server.py`

The server uses the configured target repo roots and exposes tools like:

- `list_wiki_entries`
- `read_wiki_entry`
- `en_ingest`
- `en_validate`
- `en_recall`
- `en_r`
- `en_correct`
- `en_promote`
- `en_memory_log`
- `en_sync_mempalace`

## Notes

- First-time setup for each target repo requires `init --data-root` (and optional `--wiki-root`).
- If the configured wiki root is empty at init time, Ennegram can seed it from template markdown found in `ennegram/wiki/`.
- Keep canonical wiki content in the configured external wiki root, not in this tooling repo.
