# Ennegram v0.1 Standalone Tooling

This workspace hosts Ennegram as standalone tooling. It can index and recall against any target repository via `ENNEGRAM_TARGET_ROOT`, while per-repo runtime data and wiki canon live in separately configured roots.

## Structure

- `config/` runtime configuration
- `schema/` data and memory schemas
- `wiki/` template seed location (canonical wiki is external per target repo)
- `<data-root>/logs` correction and ingestion logs
- `<data-root>/reports` validation and ingest outputs

## CLI Usage

From `Engram_v01_Workspace`:

- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py init --data-root /path/to/ennegram-data/repo-name --wiki-root /path/to/ennegram-wiki/repo-name`
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py ingest`
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py recall "session_doc pipeline"`
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py r "session_doc pipeline"` (short alias)
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py r "where is chunking implemented" --mode code` (force code lookup)
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py validate`
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py correct architecture --verdict partial --note "Missing router detail"`
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py promote caveats --note "Chunk ranges too broad caused narrative bleed" --source-uri SESSION_DOC_PIPELINE.md --title "Chunk range finding"`
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py memory-log --tail 20`
- `ENNEGRAM_TARGET_ROOT=/path/to/repo python3 ennegram_cli.py sync-mempalace --mark-synced`

Recall behavior is wiki-first: it returns matches from the configured per-repo wiki root first, then appends code/docs fallback matches from paths configured in `ennegram/config/ennegram.yaml` against `ENNEGRAM_TARGET_ROOT`.
`init --data-root ...` is required once per target repo; `--wiki-root` is optional and defaults to `<data-root>/wiki`. The mapping is then reused automatically.
Use `--mode code` when wiki is sparse and you want implementation-first retrieval.

## Makefile Shortcuts

- `make en-help`
- `make en-help ENNEGRAM_TARGET_ROOT=/path/to/repo`
- `make en-init ENNEGRAM_DATA_ROOT=/path/to/ennegram-data/repo-name [ENNEGRAM_WIKI_ROOT=/path/to/ennegram-wiki/repo-name]`
- `make en-ingest`
- `make en-recall QUERY="scene editor quote ledger"`
- `make en_r QUERY="scene editor quote ledger"` (short alias)
- `make en-code QUERY="where is chunking implemented"` (force code lookup)
- `make en-validate`
- `make en-correct ENTRY_ID=runbook VERDICT=partial NOTE="Need clearer incident step"`
- `make en-promote WIKI_ENTRY=caveats NOTE="Chunk ranges too broad caused narrative bleed" SOURCE_URI="SESSION_DOC_PIPELINE.md" TITLE="Chunk range finding"`
- `make en-memory-log TAIL=20`
- `make en-sync-mempalace MARK_SYNCED=1`

## Living Memory Flow

- `en-recall`, `en-correct`, and `en-promote` emit interaction events under `<data-root>/logs/memory_events.jsonl`.
- `en-memory-log` shows those events for quick inspection.
- `en-sync-mempalace` prepares adapter artifacts:
  - push payload: `<data-root>/reports/mempalace_push_payload.json`
  - pull template: `<data-root>/reports/mempalace_pull_template.json`
- Optional pull import: provide a JSON array via `--import-file`; imported items are appended to `<data-root>/logs/mempalace_imports.jsonl`.

## MCP Server Mode

Ennegram can run as an MCP server (not just CLI) via `ennegram_mcp_server.py`.

Start manually:

- `python3 ennegram_mcp_server.py`

Register in your MCP config (see `.mcp.json.template`) with:

- command: `python3`
- args: `[/absolute/path/to/Engram_v01_Workspace/ennegram_mcp_server.py]`
- env: `ENNEGRAM_TARGET_ROOT=/path/to/repo`

Available MCP tools:

- `list_wiki_entries`
- `read_wiki_entry`
- `en_ingest`
- `en_validate`
- `en_recall`
- `en_r` (short alias)
- `en_correct`
- `en_promote`
- `en_memory_log`
- `en_sync_mempalace`
