"""MCP server for Ennegram operations in this repository.

Usage:
    python ennegram_mcp_server.py
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP


ROOT = Path(__file__).resolve().parent
ENNEGRAM_CLI = ROOT / "ennegram_cli.py"
TEMPLATE_WIKI_ROOT = ROOT / "ennegram" / "wiki"
REPO_DATA_REGISTRY_PATH = ROOT / "ennegram" / "repo_data_roots.json"
TARGET_ROOT = Path(os.environ.get("ENNEGRAM_TARGET_ROOT", ".")).resolve()


mcp = FastMCP(
    "ennegram",
    instructions=(
        "Ennegram MCP server for repo context operations. "
        "Use wiki-first recall, then code/docs fallback. "
        "Promote durable findings into wiki canon and keep memory logs synced."
    ),
)


async def _run_cli(args: list[str]) -> str:
    env = dict(os.environ)
    env["ENNEGRAM_TARGET_ROOT"] = str(TARGET_ROOT)
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        str(ENNEGRAM_CLI),
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=str(ROOT),
        env=env,
    )
    stdout, _ = await proc.communicate()
    output = stdout.decode("utf-8", errors="replace").strip()
    if not output:
        output = "(no output)"
    return output


def _configured_wiki_root() -> Path:
    env_wiki_root = os.environ.get("ENNEGRAM_WIKI_ROOT")
    if env_wiki_root:
        return Path(env_wiki_root).expanduser().resolve()

    if REPO_DATA_REGISTRY_PATH.exists():
        try:
            parsed = json.loads(REPO_DATA_REGISTRY_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            parsed = {}
        repos = parsed.get("repos", {}) if isinstance(parsed, dict) else {}
        if isinstance(repos, dict):
            configured = repos.get(str(TARGET_ROOT))
            if isinstance(configured, str):
                return (Path(configured).expanduser().resolve() / "wiki")
            if isinstance(configured, dict):
                wiki_root = configured.get("wiki_root")
                if isinstance(wiki_root, str):
                    return Path(wiki_root).expanduser().resolve()
                data_root = configured.get("data_root")
                if isinstance(data_root, str):
                    return Path(data_root).expanduser().resolve() / "wiki"

    return TEMPLATE_WIKI_ROOT


@mcp.tool()
def list_wiki_entries() -> str:
    """List available Ennegram wiki entries."""
    wiki_root = _configured_wiki_root()
    if not wiki_root.exists():
        return f"Wiki directory not found: {wiki_root}"
    entries = sorted(path.stem for path in wiki_root.glob("*.md"))
    if not entries:
        return "No wiki entries found."
    return "Wiki entries:\n" + "\n".join(f"- {entry}" for entry in entries)


@mcp.tool()
def read_wiki_entry(entry: str) -> str:
    """Read an Ennegram wiki entry by id (e.g. caveats, architecture)."""
    wiki_root = _configured_wiki_root()
    path = wiki_root / f"{entry}.md"
    if not path.exists():
        return f"Wiki entry not found: {path}"
    return path.read_text(encoding="utf-8")


@mcp.tool()
async def en_ingest() -> str:
    """Ingest wiki canon into Ennegram index."""
    return await _run_cli(["ingest"])


@mcp.tool()
async def en_validate() -> str:
    """Validate wiki metadata, freshness, and source references."""
    return await _run_cli(["validate"])


@mcp.tool()
async def en_recall(query: str, max_results: int = 5) -> str:
    """Run wiki-first recall with code/docs fallback."""
    return await _run_cli(["recall", query, "--max-results", str(max_results)])


@mcp.tool()
async def en_r(query: str, max_results: int = 5) -> str:
    """Short alias for en_recall."""
    return await en_recall(query=query, max_results=max_results)


@mcp.tool()
async def en_code(query: str, max_results: int = 5) -> str:
    """Code-focused recall (skip wiki/docs and search code fallback only)."""
    return await _run_cli(["recall", query, "--mode", "code", "--max-results", str(max_results)])


@mcp.tool()
async def en_correct(
    entry_id: str,
    verdict: str,
    note: str,
    source_uri: str = "",
) -> str:
    """Log a correction for a recalled entry.

    verdict must be one of: correct, partial, incorrect.
    """
    args = ["correct", entry_id, "--verdict", verdict, "--note", note]
    if source_uri:
        args.extend(["--source-uri", source_uri])
    return await _run_cli(args)


@mcp.tool()
async def en_promote(
    wiki_entry: str,
    note: str,
    title: str = "",
    source_refs: list[str] | None = None,
) -> str:
    """Promote a durable finding into wiki canon and memory logs."""
    args = ["promote", wiki_entry, "--note", note]
    if title:
        args.extend(["--title", title])
    for ref in source_refs or []:
        args.extend(["--source-uri", ref])
    return await _run_cli(args)


@mcp.tool()
async def en_memory_log(tail: int = 20, event_type: str = "") -> str:
    """Inspect Ennegram interaction memory events."""
    args = ["memory-log", "--tail", str(tail)]
    if event_type:
        args.extend(["--event-type", event_type])
    return await _run_cli(args)


@mcp.tool()
async def en_sync_mempalace(mark_synced: bool = False, import_file: str = "") -> str:
    """Prepare mempalace push/pull artifacts and optionally import pulled memories."""
    args = ["sync-mempalace"]
    if import_file:
        args.extend(["--import-file", import_file])
    if mark_synced:
        args.append("--mark-synced")
    return await _run_cli(args)


if __name__ == "__main__":
    mcp.run()
