#!/usr/bin/env python3
"""Minimal Ennegram v0.1 CLI scaffold."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


TOOL_ROOT = Path(__file__).resolve().parent
TARGET_ROOT = Path(os.environ.get("ENNEGRAM_TARGET_ROOT", ".")).resolve()
ENNEGRAM_ROOT = TOOL_ROOT / "ennegram"
TEMPLATE_WIKI_ROOT = ENNEGRAM_ROOT / "wiki"
REPO_DATA_REGISTRY_PATH = ENNEGRAM_ROOT / "repo_data_roots.json"
UNCONFIGURED_DATA_ROOT = ENNEGRAM_ROOT / "_unconfigured_data_root"
UNCONFIGURED_WIKI_ROOT = ENNEGRAM_ROOT / "_unconfigured_wiki_root"
DATA_ROOT = UNCONFIGURED_DATA_ROOT
ACTIVE_WIKI_ROOT = UNCONFIGURED_WIKI_ROOT
REPORTS_ROOT = DATA_ROOT / "reports"
LOGS_ROOT = DATA_ROOT / "logs"
INDEX_PATH = LOGS_ROOT / "index.json"
CORRECTIONS_PATH = LOGS_ROOT / "corrections.jsonl"
PROMOTIONS_PATH = LOGS_ROOT / "promotions.jsonl"
MEMORY_EVENTS_PATH = LOGS_ROOT / "memory_events.jsonl"
MEMPALACE_IMPORTS_PATH = LOGS_ROOT / "mempalace_imports.jsonl"
MEMPALACE_SYNC_STATE_PATH = LOGS_ROOT / "mempalace_sync_state.json"
STALE_DAYS = 30
VALID_STATUS = {"active", "stale", "conflicted", "deprecated"}
FALLBACK_TEXT_SUFFIXES = {".md", ".txt", ".py", ".ts", ".tsx", ".js", ".vue", ".yaml", ".yml", ".json"}
DEFAULT_CONFIG: Dict[str, Any] = {
    "validation": {
        "freshness_days": 30,
        "require_owner": True,
        "require_last_validated_at": True,
        "require_source_refs": True,
    },
    "recall": {
        "min_confidence_to_assert": 0.6,
        "max_results": 3,
        "fallback_paths": "README.md,CLAUDE.md,SESSION_DOC_PIPELINE.md,SCENE_EXTRACTION.md,config,server,frontend/src",
        "fallback_max_files": 300,
        "wiki_min_confidence_for_trust": 0.7,
        "prefer_code_when_query_mentions_code": True,
    },
}


def _set_data_root(path: Path) -> None:
    global DATA_ROOT
    global REPORTS_ROOT
    global LOGS_ROOT
    global INDEX_PATH
    global CORRECTIONS_PATH
    global PROMOTIONS_PATH
    global MEMORY_EVENTS_PATH
    global MEMPALACE_IMPORTS_PATH
    global MEMPALACE_SYNC_STATE_PATH

    DATA_ROOT = path
    REPORTS_ROOT = DATA_ROOT / "reports"
    LOGS_ROOT = DATA_ROOT / "logs"
    INDEX_PATH = LOGS_ROOT / "index.json"
    CORRECTIONS_PATH = LOGS_ROOT / "corrections.jsonl"
    PROMOTIONS_PATH = LOGS_ROOT / "promotions.jsonl"
    MEMORY_EVENTS_PATH = LOGS_ROOT / "memory_events.jsonl"
    MEMPALACE_IMPORTS_PATH = LOGS_ROOT / "mempalace_imports.jsonl"
    MEMPALACE_SYNC_STATE_PATH = LOGS_ROOT / "mempalace_sync_state.json"


def _set_wiki_root(path: Path) -> None:
    global ACTIVE_WIKI_ROOT
    ACTIVE_WIKI_ROOT = path


def _normalize_path(raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    return candidate


def _load_repo_data_roots() -> Dict[str, Dict[str, str]]:
    if not REPO_DATA_REGISTRY_PATH.exists():
        return {}
    try:
        parsed = json.loads(REPO_DATA_REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    repos = parsed.get("repos", {})
    if not isinstance(repos, dict):
        return {}
    cleaned: Dict[str, Dict[str, str]] = {}
    for key, value in repos.items():
        if not isinstance(key, str):
            continue
        # Backward compatibility with old registry format: {target_repo: "/path/to/data_root"}.
        if isinstance(value, str):
            data_root = value
            wiki_root = str(Path(value) / "wiki")
            cleaned[key] = {"data_root": data_root, "wiki_root": wiki_root}
            continue
        if not isinstance(value, dict):
            continue
        data_root = value.get("data_root")
        wiki_root = value.get("wiki_root")
        if isinstance(data_root, str) and isinstance(wiki_root, str):
            cleaned[key] = {"data_root": data_root, "wiki_root": wiki_root}
    return cleaned


def _save_repo_data_roots(repo_data_roots: Dict[str, Dict[str, str]]) -> None:
    REPO_DATA_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"repos": repo_data_roots}
    REPO_DATA_REGISTRY_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _configure_runtime_paths(args: argparse.Namespace) -> None:
    target_key = str(TARGET_ROOT)
    repo_data_roots = _load_repo_data_roots()
    configured_paths = repo_data_roots.get(target_key)
    configured_data_root = configured_paths.get("data_root") if configured_paths else None
    configured_wiki_root = configured_paths.get("wiki_root") if configured_paths else None
    env_data_root = os.environ.get("ENNEGRAM_DATA_ROOT")
    env_wiki_root = os.environ.get("ENNEGRAM_WIKI_ROOT")
    command = str(getattr(args, "command", ""))

    if env_data_root:
        _set_data_root(_normalize_path(env_data_root))
        if env_wiki_root:
            _set_wiki_root(_normalize_path(env_wiki_root))
        elif configured_wiki_root:
            _set_wiki_root(Path(configured_wiki_root))
        else:
            _set_wiki_root(DATA_ROOT / "wiki")
        return

    if command == "init":
        init_data_root = getattr(args, "data_root", None)
        init_wiki_root = getattr(args, "wiki_root", None)
        if init_data_root:
            resolved_data_root = _normalize_path(init_data_root)
            resolved_wiki_root = (
                _normalize_path(init_wiki_root)
                if init_wiki_root
                else (resolved_data_root / "wiki")
            )
            _set_data_root(resolved_data_root)
            _set_wiki_root(resolved_wiki_root)
            repo_data_roots[target_key] = {
                "data_root": str(resolved_data_root),
                "wiki_root": str(resolved_wiki_root),
            }
            _save_repo_data_roots(repo_data_roots)
            return
        if configured_data_root and configured_wiki_root:
            _set_data_root(Path(configured_data_root))
            _set_wiki_root(Path(configured_wiki_root))
            return
        raise RuntimeError(
            "No repo roots configured for target repo. Run `init --data-root /path/to/data [--wiki-root /path/to/wiki]` once."
        )

    if configured_data_root and configured_wiki_root:
        _set_data_root(Path(configured_data_root))
        _set_wiki_root(Path(configured_wiki_root))
        return

    raise RuntimeError(
        "No repo roots configured for target repo. Run `init --data-root /path/to/data [--wiki-root /path/to/wiki]` first."
    )


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def load_config() -> Dict[str, Any]:
    config_path = ENNEGRAM_ROOT / "config" / "ennegram.yaml"
    if not config_path.exists():
        return DEFAULT_CONFIG

    parsed: Dict[str, Any] = {}
    current_section: str | None = None
    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        if raw_line.startswith("  "):
            if current_section is None:
                continue
            line = raw_line.strip()
            if ":" not in line:
                continue
            key, raw_value = line.split(":", 1)
            parsed.setdefault(current_section, {})[key.strip()] = _parse_scalar(raw_value)
            continue

        if ":" not in raw_line:
            continue
        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value == "":
            current_section = key
            parsed.setdefault(current_section, {})
        else:
            parsed[key] = _parse_scalar(value)
            current_section = None

    return _deep_merge(DEFAULT_CONFIG, parsed)


def parse_frontmatter(markdown_text: str) -> Tuple[Dict[str, Any], str]:
    lines = markdown_text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, markdown_text

    metadata: Dict[str, Any] = {}
    current_list_key: str | None = None
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            break
        stripped = line.strip()
        if stripped.startswith("- ") and current_list_key:
            metadata[current_list_key].append(stripped[2:].strip().strip('"'))
            i += 1
            continue
        if ":" in stripped:
            key, raw_value = stripped.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()
            if raw_value == "":
                metadata[key] = []
                current_list_key = key
            else:
                metadata[key] = _parse_scalar(raw_value)
                current_list_key = None
        i += 1

    body = "\n".join(lines[i + 1 :]) if i < len(lines) else markdown_text
    return metadata, body


def _render_frontmatter(metadata: Dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f'  - "{item}"')
            continue
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = str(value)
        lines.append(f'{key}: "{rendered}"')
    lines.append("---")
    return "\n".join(lines)


def _resolve_wiki_target(target: str) -> Path:
    normalized_target = target[5:] if target.startswith("wiki/") else target
    if target.endswith(".md"):
        candidate = TOOL_ROOT / target
        if candidate.exists():
            return candidate
        candidate = ACTIVE_WIKI_ROOT / normalized_target
        return candidate
    return ACTIVE_WIKI_ROOT / f"{normalized_target}.md"


def _seed_wiki_if_missing() -> None:
    ACTIVE_WIKI_ROOT.mkdir(parents=True, exist_ok=True)
    if any(ACTIVE_WIKI_ROOT.glob("*.md")):
        return
    if not TEMPLATE_WIKI_ROOT.exists():
        return
    for template_file in sorted(TEMPLATE_WIKI_ROOT.glob("*.md")):
        destination = ACTIVE_WIKI_ROOT / template_file.name
        if destination.exists():
            continue
        destination.write_text(template_file.read_text(encoding="utf-8"), encoding="utf-8")


def _ensure_promoted_findings_section(body: str) -> str:
    if "## Promoted Findings" in body:
        return body.rstrip()
    section_prefix = "\n\n## Promoted Findings\n"
    return body.rstrip() + section_prefix


def _slugify_anchor(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def _split_large_section(text: str, max_chars: int = 12000) -> List[str]:
    if len(text) <= max_chars:
        return [text]
    parts: List[str] = []
    remaining = text
    while len(remaining) > max_chars:
        cut = remaining.rfind("\n", 0, max_chars)
        if cut <= 0:
            cut = max_chars
        chunk = remaining[:cut].strip()
        if chunk:
            parts.append(chunk)
        remaining = remaining[cut:].lstrip("\n")
    if remaining.strip():
        parts.append(remaining.strip())
    return parts


def _extract_section_entries(body: str) -> List[Dict[str, Any]]:
    lines = body.splitlines()
    sections: List[Dict[str, Any]] = []
    if not lines:
        return sections

    headings: List[Tuple[int, int, str]] = []
    heading_re = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
    for idx, line in enumerate(lines):
        m = heading_re.match(line)
        if not m:
            continue
        level = len(m.group(1))
        if level not in {2, 3}:
            continue
        title = m.group(2).strip().strip("#").strip()
        headings.append((idx, level, title))

    if not headings:
        intro = body.strip()
        if intro:
            sections.append(
                {
                    "source_anchor": "intro",
                    "summary": _summary_from_text(intro),
                    "body": intro,
                    "section_level": 0,
                    "section_parent": None,
                }
            )
        return sections

    intro = "\n".join(lines[: headings[0][0]]).strip()
    if intro:
        sections.append(
            {
                "source_anchor": "intro",
                "summary": _summary_from_text(intro),
                "body": intro,
                "section_level": 0,
                "section_parent": None,
            }
        )

    counts: Dict[str, int] = {}
    anchors_meta: List[Dict[str, Any]] = []
    current_h2_slug = "unscoped"
    for idx, level, title in headings:
        title_slug = _slugify_anchor(title)
        if level == 2:
            base = f"h2:{title_slug}"
            count = counts.get(base, 0) + 1
            counts[base] = count
            anchor = base if count == 1 else f"{base}~{count}"
            current_h2_slug = anchor.split(":", 1)[1]
            parent = None
        else:
            base = f"h3:{current_h2_slug}/{title_slug}"
            count = counts.get(base, 0) + 1
            counts[base] = count
            anchor = base if count == 1 else f"{base}~{count}"
            parent = f"h2:{current_h2_slug}"
        anchors_meta.append(
            {
                "line_index": idx,
                "level": level,
                "anchor": anchor,
                "title": title,
                "parent": parent,
            }
        )

    for i, meta in enumerate(anchors_meta):
        start = meta["line_index"]
        end = anchors_meta[i + 1]["line_index"] if i + 1 < len(anchors_meta) else len(lines)
        section_text = "\n".join(lines[start:end]).strip()
        if not section_text:
            continue
        section_parts = _split_large_section(section_text, max_chars=12000)
        for part_idx, part_text in enumerate(section_parts, 1):
            anchor = meta["anchor"]
            summary = part_text.splitlines()[0].strip() if part_text.splitlines() else _summary_from_text(part_text)
            if len(section_parts) > 1:
                anchor = f"{anchor}::part-{part_idx}"
                summary = f"{summary} (part {part_idx})"
            sections.append(
                {
                    "source_anchor": anchor,
                    "summary": summary[:120],
                    "body": part_text,
                    "section_level": meta["level"],
                    "section_parent": meta["parent"],
                }
            )
    return sections


def load_wiki_entries() -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for md_file in sorted(ACTIVE_WIKI_ROOT.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(content)
        entries.append(
            {
                "id": md_file.stem,
                "path": f"wiki/{md_file.relative_to(ACTIVE_WIKI_ROOT)}",
                "metadata": metadata,
                "body": body,
                "summary": body.strip().splitlines()[0] if body.strip() else "",
                "sections": _extract_section_entries(body),
            }
        )
    return entries


def command_init(_: argparse.Namespace) -> int:
    targets = [
        ENNEGRAM_ROOT / "config",
        ENNEGRAM_ROOT / "schema",
        ACTIVE_WIKI_ROOT,
        REPORTS_ROOT,
        LOGS_ROOT,
    ]
    for target in targets:
        target.mkdir(parents=True, exist_ok=True)
    _seed_wiki_if_missing()

    if not CORRECTIONS_PATH.exists():
        CORRECTIONS_PATH.write_text("", encoding="utf-8")
    if not PROMOTIONS_PATH.exists():
        PROMOTIONS_PATH.write_text("", encoding="utf-8")
    if not MEMORY_EVENTS_PATH.exists():
        MEMORY_EVENTS_PATH.write_text("", encoding="utf-8")
    if not MEMPALACE_IMPORTS_PATH.exists():
        MEMPALACE_IMPORTS_PATH.write_text("", encoding="utf-8")
    if not MEMPALACE_SYNC_STATE_PATH.exists():
        MEMPALACE_SYNC_STATE_PATH.write_text(
            json.dumps({"last_synced_event_index": 0}, indent=2),
            encoding="utf-8",
        )

    print(f"Initialized Ennegram data at {DATA_ROOT} and wiki at {ACTIVE_WIKI_ROOT}.")
    return 0


def _missing_required(metadata: Dict[str, Any], settings: Dict[str, Any]) -> List[str]:
    required: List[str] = []
    validation_cfg = settings["validation"]
    if validation_cfg.get("require_owner", True):
        required.append("owner")
    if validation_cfg.get("require_last_validated_at", True):
        required.append("last_validated_at")
    if validation_cfg.get("require_source_refs", True):
        required.append("source_refs")
    required.append("status")
    return [field for field in required if field not in metadata]


def command_ingest(_: argparse.Namespace) -> int:
    settings = load_config()
    entries = load_wiki_entries()
    indexed: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []

    for entry in entries:
        missing = _missing_required(entry["metadata"], settings)
        if missing:
            skipped.append({"id": entry["id"], "reason": f"missing metadata: {missing}"})
            continue

        source_refs = entry["metadata"].get("source_refs")
        if isinstance(source_refs, str):
            source_refs = [source_refs]

        indexed.append(
            {
                "id": entry["id"],
                "source_uri": entry["path"],
                "source_anchor": "top",
                "summary": entry["summary"],
                "confidence": 1.0,
                "last_validated_at": entry["metadata"]["last_validated_at"],
                "status": entry["metadata"]["status"],
                "source_refs": source_refs or [],
                "body": entry["body"],
            }
        )
        for section in entry.get("sections", []):
            indexed.append(
                {
                    "id": f"{entry['id']}::{section['source_anchor']}",
                    "source_uri": entry["path"],
                    "source_anchor": section["source_anchor"],
                    "summary": section["summary"],
                    "confidence": 1.0,
                    "last_validated_at": entry["metadata"]["last_validated_at"],
                    "status": entry["metadata"]["status"],
                    "source_refs": source_refs or [],
                    "body": section["body"],
                    "section_parent": section.get("section_parent"),
                    "section_level": section.get("section_level"),
                }
            )

    LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(indexed, indent=2), encoding="utf-8")

    report = {
        "indexed": len(indexed),
        "skipped": skipped,
        "generated_at": datetime.now(UTC).isoformat(),
    }
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORTS_ROOT / "ingest_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Indexed {len(indexed)} entries. Skipped {len(skipped)}.")
    return 0


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_]+", text.lower()))


def _score_match(query: str, entry: Dict[str, Any]) -> float:
    query_tokens = _tokenize(query)
    if not query_tokens:
        return 0.0
    haystack_tokens = _tokenize((entry.get("summary", "") + " " + entry.get("body", "")).lower())
    overlap = len(query_tokens.intersection(haystack_tokens))
    return overlap / len(query_tokens)


def _parse_csv_paths(raw: Any) -> List[str]:
    if isinstance(raw, list):
        return [str(part).strip() for part in raw if str(part).strip()]
    if not isinstance(raw, str):
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _should_skip_dir(path: Path) -> bool:
    blocked = {".git", "node_modules", "__pycache__", ".venv", "ennegram"}
    return any(part in blocked for part in path.parts)


def _iter_fallback_files(settings: Dict[str, Any]) -> List[Path]:
    recall_cfg = settings["recall"]
    targets = _parse_csv_paths(recall_cfg.get("fallback_paths", ""))
    max_files = int(recall_cfg.get("fallback_max_files", 300))
    files: List[Path] = []

    for target in targets:
        candidate = TARGET_ROOT / target
        if not candidate.exists():
            continue
        if candidate.is_file():
            if candidate.suffix.lower() in FALLBACK_TEXT_SUFFIXES:
                files.append(candidate)
            if len(files) >= max_files:
                break
            continue

        for file_path in candidate.rglob("*"):
            if len(files) >= max_files:
                break
            if not file_path.is_file():
                continue
            if _should_skip_dir(file_path.relative_to(TARGET_ROOT)):
                continue
            if file_path.suffix.lower() not in FALLBACK_TEXT_SUFFIXES:
                continue
            files.append(file_path)
        if len(files) >= max_files:
            break
    return files


def _summary_from_text(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:120]
    return "(no summary)"


def _best_line_match(query: str, text: str) -> Tuple[float, str, str]:
    """Return (line_score, summary, anchor) for the best matching line in text."""
    query_tokens = _tokenize(query)
    if not query_tokens:
        return 0.0, _summary_from_text(text), "top"

    best_score = 0.0
    best_line = ""
    best_line_no = 0
    for idx, raw_line in enumerate(text.splitlines(), 1):
        stripped = raw_line.strip()
        if not stripped:
            continue
        overlap = len(query_tokens.intersection(_tokenize(stripped)))
        if overlap <= 0:
            continue
        score = overlap / len(query_tokens)
        if score > best_score:
            best_score = score
            best_line = stripped
            best_line_no = idx

    if best_score <= 0:
        return 0.0, _summary_from_text(text), "top"
    return best_score, best_line[:120], f"L{best_line_no}"


def _is_generic_fallback_summary(summary: str) -> bool:
    stripped = summary.strip().lower()
    if not stripped:
        return True
    generic_prefixes = (
        "#",
        "##",
        "###",
        "import ",
        "from ",
        "<script",
        "<template",
        '"""',
        "'''",
    )
    return any(stripped.startswith(prefix) for prefix in generic_prefixes)


def _query_symbol_tokens(query: str) -> set[str]:
    """Extract symbol-like tokens from query (snake_case, dotted paths, names)."""
    symbols = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_\.]*", query))
    return {s.lower() for s in symbols if len(s) > 2}


def _fallback_rank_adjustment(
    query: str,
    source_type: str,
    source_uri: str,
    summary: str,
    line_anchor: str,
) -> float:
    """Heuristic re-ranking adjustment for fallback results."""
    adjust = 0.0
    lower_query = query.lower()
    query_tokens = _tokenize(query)
    summary_tokens = _tokenize(summary)
    symbol_tokens = _query_symbol_tokens(query)
    source_lower = source_uri.lower()

    # Implementation-style queries should bias toward code fallback.
    if source_type == "code" and any(h in lower_query for h in ("where", "implemented", "implementation", "function", "class", "router", "script", "default")):
        adjust += 0.06

    # Reward exact symbol/path mentions in source path.
    if any(sym in source_lower for sym in symbol_tokens):
        adjust += 0.08

    # Reward lexical overlap in the matched summary line.
    if query_tokens:
        overlap = len(query_tokens.intersection(summary_tokens))
        adjust += min(0.10, overlap / len(query_tokens) * 0.12)

    # Penalize generic matched lines and weak line anchors.
    if _is_generic_fallback_summary(summary):
        adjust -= 0.07
    if line_anchor == "top":
        adjust -= 0.05
    if len(summary.strip()) < 18:
        adjust -= 0.03

    return adjust


def _classify_source_type(path: Path) -> str:
    if path.suffix.lower() in {".py", ".ts", ".tsx", ".js", ".vue"}:
        return "code"
    return "docs"


def _fallback_recall(
    query: str,
    settings: Dict[str, Any],
    excluded_source_uris: set[str],
) -> List[Tuple[float, Dict[str, Any]]]:
    matches: List[Tuple[float, Dict[str, Any]]] = []
    for file_path in _iter_fallback_files(settings):
        relative_uri = str(file_path.relative_to(TARGET_ROOT))
        if relative_uri in excluded_source_uris:
            continue
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        file_score = _score_match(query, {"summary": _summary_from_text(text), "body": text})
        line_score, line_summary, line_anchor = _best_line_match(query, text)
        # Favor line-local specificity to reduce generic top-of-file fallback noise.
        source_type = _classify_source_type(file_path)
        score = (0.4 * file_score) + (0.6 * line_score)
        score += _fallback_rank_adjustment(
            query=query,
            source_type=source_type,
            source_uri=relative_uri,
            summary=line_summary,
            line_anchor=line_anchor,
        )
        score = round(max(0.0, min(1.0, score)), 3)
        if score <= 0:
            continue
        item = {
            "id": relative_uri,
            "summary": line_summary,
            "source_uri": relative_uri,
            "source_anchor": line_anchor,
            "confidence": score,
            "last_validated_at": "n/a",
            "source_type": source_type,
        }
        matches.append((score, item))
    matches.sort(key=lambda pair: pair[0], reverse=True)
    return matches


def _partition_fallback_results(
    fallback_scored: List[Tuple[float, Dict[str, Any]]],
) -> Tuple[List[Tuple[float, Dict[str, Any]]], List[Tuple[float, Dict[str, Any]]]]:
    code_results: List[Tuple[float, Dict[str, Any]]] = []
    docs_results: List[Tuple[float, Dict[str, Any]]] = []
    for score, item in fallback_scored:
        if item.get("source_type") == "code":
            code_results.append((score, item))
        else:
            docs_results.append((score, item))
    return code_results, docs_results


def _print_recall_item(item: Dict[str, Any], min_confidence: float) -> None:
    print("-" * 60)
    print(f"id: {item['id']}")
    print(f"summary: {item['summary'] or '(no summary)'}")
    print(f"provenance: {item['source_uri']}#{item['source_anchor']}")
    print(f"source_type: {item.get('source_type', 'wiki')}")
    print(f"confidence: {item['confidence']}")
    print(f"last_validated_at: {item['last_validated_at']}")
    if float(item["confidence"]) < min_confidence:
        print("note: low-confidence recall; verify against canonical source.")


def _query_prefers_code(query: str, settings: Dict[str, Any]) -> bool:
    if not settings["recall"].get("prefer_code_when_query_mentions_code", True):
        return False
    code_hints = {
        "code",
        "python",
        "typescript",
        "javascript",
        "implemented",
        "implementation",
        "function",
        "class",
        "router",
        "script",
        "where in code",
    }
    lower = query.lower()
    return any(hint in lower for hint in code_hints)


def _wiki_rank_score(score: float, item: Dict[str, Any]) -> float:
    """Prefer section-anchored wiki entries over legacy top-level entries."""
    anchor = str(item.get("source_anchor", "top"))
    if anchor == "top":
        return score
    if anchor.startswith("h3:"):
        return score + 0.04
    if anchor.startswith("h2:"):
        return score + 0.03
    if anchor == "intro":
        return score + 0.02
    return score + 0.01


def _select_wiki_results(
    wiki_scored: List[Tuple[float, Dict[str, Any]]],
    max_results: int,
) -> List[Tuple[float, Dict[str, Any]]]:
    """Return top wiki results, preferring section anchors over `top`."""
    section_hits: List[Tuple[float, Dict[str, Any]]] = []
    top_hits: List[Tuple[float, Dict[str, Any]]] = []
    for pair in wiki_scored:
        if pair[1].get("source_anchor") == "top":
            top_hits.append(pair)
        else:
            section_hits.append(pair)
    selected = section_hits[:max_results]
    if len(selected) < max_results:
        selected += top_hits[: max_results - len(selected)]
    return selected


def command_recall(args: argparse.Namespace) -> int:
    settings = load_config()
    query = args.query
    mode = args.mode
    max_results = args.max_results if args.max_results is not None else settings["recall"]["max_results"]
    min_confidence = float(settings["recall"]["min_confidence_to_assert"])
    wiki_confidence_threshold = float(settings["recall"]["wiki_min_confidence_for_trust"])
    entries: List[Dict[str, Any]] = []
    if INDEX_PATH.exists():
        entries = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    elif mode in {"auto", "wiki", "all"}:
        print("No wiki index found. Run `ingest` to enable wiki-first recall.")

    wiki_scored: List[Tuple[float, Dict[str, Any]]] = []
    if mode in {"auto", "wiki", "all"}:
        for entry in entries:
            score = _score_match(query, entry)
            if score <= 0:
                continue
            enriched = dict(entry)
            enriched["confidence"] = round(score, 3)
            enriched["source_type"] = "wiki"
            wiki_scored.append((score, enriched))
        wiki_scored.sort(key=lambda item: _wiki_rank_score(item[0], item[1]), reverse=True)

    wiki_uris = {entry.get("source_uri", "") for _, entry in wiki_scored}
    fallback_scored: List[Tuple[float, Dict[str, Any]]] = []
    if mode in {"auto", "code", "docs", "all"}:
        fallback_scored = _fallback_recall(query, settings, wiki_uris)

    code_results, docs_results = _partition_fallback_results(fallback_scored)
    if mode == "code":
        docs_results = []
        wiki_scored = []
    elif mode == "docs":
        code_results = []
        wiki_scored = []
    elif mode == "wiki":
        code_results = []
        docs_results = []

    if not wiki_scored and not code_results and not docs_results:
        _log_memory_event(
            "recall",
            {
                "query": query,
                "wiki_results": 0,
                "code_results": 0,
                "docs_results": 0,
                "top_result": None,
            },
        )
        print("No matching context found.")
        return 0

    code_intent = _query_prefers_code(query, settings)
    wiki_low_confidence = not wiki_scored or wiki_scored[0][0] < wiki_confidence_threshold
    prioritize_code = mode == "code" or (mode == "auto" and code_intent and wiki_low_confidence)

    if prioritize_code and code_results:
        print("== Code Results (Prioritized) ==")
        for _, item in code_results[:max_results]:
            _print_recall_item(item, min_confidence)
    wiki_display = _select_wiki_results(wiki_scored, max_results)
    if wiki_scored and mode in {"auto", "wiki", "all"}:
        print("== Wiki Results ==")
        for _, item in wiki_display:
            _print_recall_item(item, min_confidence)
    if code_results and not prioritize_code:
        print("== Code Fallback Results ==")
        for _, item in code_results[:max_results]:
            _print_recall_item(item, min_confidence)
    if docs_results:
        print("== Docs Fallback Results ==")
        for _, item in docs_results[:max_results]:
            _print_recall_item(item, min_confidence)

    top_item = None
    if wiki_display:
        top_item = wiki_display[0][1]
    elif code_results:
        top_item = code_results[0][1]
    elif docs_results:
        top_item = docs_results[0][1]
    _log_memory_event(
        "recall",
        {
            "query": query,
            "wiki_results": len(wiki_scored),
            "code_results": len(code_results),
            "docs_results": len(docs_results),
            "mode": mode,
            "top_result": {
                "id": top_item.get("id"),
                "source_type": top_item.get("source_type"),
                "confidence": top_item.get("confidence"),
            }
            if top_item
            else None,
        },
    )
    return 0


def _is_stale(raw_date: str, stale_days: int) -> bool:
    try:
        validated = date.fromisoformat(raw_date)
    except ValueError:
        return True
    return (date.today() - validated).days > stale_days


def _is_external_ref(reference: str) -> bool:
    return reference.startswith("http://") or reference.startswith("https://")


def _resolve_local_ref(reference: str) -> Path | None:
    if _is_external_ref(reference):
        return None
    normalized_ref = reference[5:] if reference.startswith("wiki/") else reference
    candidate_paths = [
        TARGET_ROOT / reference,
        ACTIVE_WIKI_ROOT / normalized_ref,
        ENNEGRAM_ROOT / reference,
        TOOL_ROOT / reference,
    ]
    for candidate in candidate_paths:
        if candidate.exists():
            return candidate
    return None


def command_validate(_: argparse.Namespace) -> int:
    settings = load_config()
    freshness_days = int(settings["validation"]["freshness_days"])
    entries = load_wiki_entries()
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    for entry in entries:
        metadata = entry["metadata"]
        missing = _missing_required(metadata, settings)
        if missing:
            errors.append({"id": entry["id"], "issue": f"missing metadata: {missing}"})
            continue

        if _is_stale(str(metadata["last_validated_at"]), freshness_days):
            warnings.append({"id": entry["id"], "issue": "stale content"})

        if metadata.get("status") not in VALID_STATUS:
            errors.append({"id": entry["id"], "issue": "invalid status value"})

        refs = metadata.get("source_refs")
        if isinstance(refs, str):
            refs = [refs]
        if not isinstance(refs, list):
            errors.append({"id": entry["id"], "issue": "source_refs must be a list or string"})
            continue
        for ref in refs:
            if not isinstance(ref, str):
                warnings.append({"id": entry["id"], "issue": "source ref is not a string"})
                continue
            if _is_external_ref(ref):
                continue
            if _resolve_local_ref(ref) is None:
                warnings.append({"id": entry["id"], "issue": f"unresolved source ref: {ref}"})

    result = {
        "errors": errors,
        "warnings": warnings,
        "files_scanned": len(entries),
        "generated_at": datetime.now(UTC).isoformat(),
    }
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORTS_ROOT / "validate_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"Validation complete. errors={len(errors)} warnings={len(warnings)} files={len(entries)}")
    return 1 if errors else 0


def _append_jsonl(path: Path, record: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


def _log_memory_event(event_type: str, payload: Dict[str, Any]) -> None:
    event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": event_type,
        "payload": payload,
    }
    _append_jsonl(MEMORY_EVENTS_PATH, event)


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    records: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            records.append(parsed)
    return records


def _build_corrections_summary(corrections: List[Dict[str, Any]]) -> Dict[str, Any]:
    verdict_counts: Dict[str, int] = {"correct": 0, "partial": 0, "incorrect": 0}
    by_entry: Dict[str, int] = {}
    for item in corrections:
        verdict = item.get("verdict")
        if verdict in verdict_counts:
            verdict_counts[verdict] += 1
        entry_id = str(item.get("entry_id", "unknown"))
        by_entry[entry_id] = by_entry.get(entry_id, 0) + 1
    return {
        "total": len(corrections),
        "verdict_counts": verdict_counts,
        "entries_with_corrections": by_entry,
        "generated_at": datetime.now(UTC).isoformat(),
    }


def command_correct(args: argparse.Namespace) -> int:
    correction = {
        "timestamp": datetime.now(UTC).isoformat(),
        "entry_id": args.entry_id,
        "verdict": args.verdict,
        "note": args.note,
        "source_uri": args.source_uri or "",
    }
    _append_jsonl(CORRECTIONS_PATH, correction)

    corrections: List[Dict[str, Any]] = []
    for line in CORRECTIONS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                corrections.append(parsed)
        except json.JSONDecodeError:
            continue

    summary = _build_corrections_summary(corrections)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORTS_ROOT / "corrections_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    _log_memory_event(
        "correction",
        {
            "entry_id": args.entry_id,
            "verdict": args.verdict,
            "note": args.note,
            "source_uri": args.source_uri or "",
            "total_corrections": summary["total"],
        },
    )

    print(
        "Logged correction: "
        f"entry_id={args.entry_id} verdict={args.verdict}. "
        f"Total corrections={summary['total']}."
    )
    return 0


def command_promote(args: argparse.Namespace) -> int:
    target_path = _resolve_wiki_target(args.wiki_entry)
    if not target_path.exists():
        print(f"Wiki entry not found: {target_path}")
        return 1

    raw = target_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(raw)
    now = datetime.now(UTC)
    stamp = now.isoformat()
    day_stamp = now.date().isoformat()

    refs = args.source_uri or []
    title = args.title or f"Finding {day_stamp}"

    body = _ensure_promoted_findings_section(body)
    lines = [body, f"\n### {title}", f"- Date: {stamp}", f"- Finding: {args.note}"]
    if refs:
        lines.append("- Source refs:")
        for ref in refs:
            lines.append(f"  - `{ref}`")
    updated_body = "\n".join(lines).rstrip() + "\n"

    if metadata:
        metadata["last_validated_at"] = day_stamp
        existing_refs = metadata.get("source_refs", [])
        if isinstance(existing_refs, str):
            existing_refs = [existing_refs]
        if not isinstance(existing_refs, list):
            existing_refs = []
        for ref in refs:
            if ref not in existing_refs:
                existing_refs.append(ref)
        if existing_refs:
            metadata["source_refs"] = existing_refs
        rendered = _render_frontmatter(metadata)
        target_path.write_text(f"{rendered}\n\n{updated_body}", encoding="utf-8")
    else:
        target_path.write_text(updated_body, encoding="utf-8")

    promotion_record = {
        "timestamp": stamp,
        "wiki_entry": str(target_path.relative_to(TOOL_ROOT)),
        "title": title,
        "note": args.note,
        "source_refs": refs,
    }
    _append_jsonl(PROMOTIONS_PATH, promotion_record)
    _log_memory_event(
        "promotion",
        {
            "wiki_entry": str(target_path.relative_to(TOOL_ROOT)),
            "title": title,
            "note": args.note,
            "source_refs": refs,
        },
    )
    print(f"Promoted finding into {target_path.relative_to(TOOL_ROOT)}.")
    return 0


def command_memory_log(args: argparse.Namespace) -> int:
    events = _read_jsonl(MEMORY_EVENTS_PATH)
    if args.event_type:
        events = [event for event in events if event.get("event_type") == args.event_type]
    if not events:
        print("No memory events found.")
        return 0

    tail_count = max(1, int(args.tail))
    for event in events[-tail_count:]:
        event_type = event.get("event_type", "unknown")
        timestamp = event.get("timestamp", "n/a")
        payload = event.get("payload", {})
        print("-" * 60)
        print(f"time: {timestamp}")
        print(f"type: {event_type}")
        print(f"payload: {json.dumps(payload, ensure_ascii=True)}")
    return 0


def _load_sync_state() -> Dict[str, Any]:
    if not MEMPALACE_SYNC_STATE_PATH.exists():
        return {"last_synced_event_index": 0}
    try:
        parsed = json.loads(MEMPALACE_SYNC_STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"last_synced_event_index": 0}
    if not isinstance(parsed, dict):
        return {"last_synced_event_index": 0}
    return parsed


def _save_sync_state(state: Dict[str, Any]) -> None:
    MEMPALACE_SYNC_STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def command_sync_mempalace(args: argparse.Namespace) -> int:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    state = _load_sync_state()
    events = _read_jsonl(MEMORY_EVENTS_PATH)
    last_synced_index = int(state.get("last_synced_event_index", 0))
    new_events = events[last_synced_index:]

    push_payload = {
        "repo": TARGET_ROOT.name,
        "generated_at": datetime.now(UTC).isoformat(),
        "from_event_index": last_synced_index,
        "to_event_index": len(events),
        "events": new_events,
    }
    push_path = REPORTS_ROOT / "mempalace_push_payload.json"
    push_path.write_text(json.dumps(push_payload, indent=2), encoding="utf-8")

    pull_template = {
        "repo": TARGET_ROOT.name,
        "generated_at": datetime.now(UTC).isoformat(),
        "instructions": "Populate memories from mempalace as a JSON list and pass via --import-file.",
        "memories": [],
    }
    pull_template_path = REPORTS_ROOT / "mempalace_pull_template.json"
    pull_template_path.write_text(json.dumps(pull_template, indent=2), encoding="utf-8")

    imported_count = 0
    if args.import_file:
        import_path = Path(args.import_file)
        if not import_path.is_absolute():
            import_path = TARGET_ROOT / args.import_file
        if not import_path.exists():
            print(f"Import file not found: {import_path}")
            return 1
        try:
            imported_raw = json.loads(import_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("Import file is not valid JSON.")
            return 1
        if not isinstance(imported_raw, list):
            print("Import file must be a JSON array.")
            return 1
        for item in imported_raw:
            if isinstance(item, dict):
                _append_jsonl(
                    MEMPALACE_IMPORTS_PATH,
                    {
                        "timestamp": datetime.now(UTC).isoformat(),
                        "memory": item,
                    },
                )
                imported_count += 1
        _log_memory_event(
            "mempalace_import",
            {
                "import_file": str(import_path.relative_to(TARGET_ROOT)),
                "imported_count": imported_count,
            },
        )

    if args.mark_synced:
        state["last_synced_event_index"] = len(events)
        _save_sync_state(state)

    _log_memory_event(
        "mempalace_sync",
        {
            "new_events": len(new_events),
            "push_payload": str(push_path.relative_to(TOOL_ROOT)),
            "pull_template": str(pull_template_path.relative_to(TOOL_ROOT)),
            "mark_synced": bool(args.mark_synced),
            "imported_count": imported_count,
        },
    )

    print(f"Prepared mempalace push payload: {push_path.relative_to(TOOL_ROOT)}")
    print(f"Prepared mempalace pull template: {pull_template_path.relative_to(TOOL_ROOT)}")
    print(f"New events since last sync: {len(new_events)}")
    if imported_count:
        print(f"Imported memories: {imported_count}")
    if args.mark_synced:
        print("Sync cursor advanced.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ennegram v0.1 CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create required directories")
    init_parser.add_argument(
        "--data-root",
        default=None,
        help="Directory for per-repo runtime data (logs/reports/index). Required on first init per target repo.",
    )
    init_parser.add_argument(
        "--wiki-root",
        default=None,
        help="Directory for per-repo canonical wiki files. Defaults to <data-root>/wiki.",
    )
    init_parser.set_defaults(func=command_init)

    ingest_parser = subparsers.add_parser("ingest", help="Index canonical wiki files")
    ingest_parser.set_defaults(func=command_ingest)

    recall_parser = subparsers.add_parser(
        "recall",
        aliases=["r"],
        help="Retrieve indexed context",
    )
    recall_parser.add_argument("query", help="Search query")
    recall_parser.add_argument("--max-results", type=int, default=None, help="Maximum results")
    recall_parser.add_argument(
        "--mode",
        choices=["auto", "wiki", "code", "docs", "all"],
        default="auto",
        help="Recall mode (auto is wiki-first with code intent handling)",
    )
    recall_parser.set_defaults(func=command_recall)

    validate_parser = subparsers.add_parser("validate", help="Validate canonical wiki integrity")
    validate_parser.set_defaults(func=command_validate)

    correct_parser = subparsers.add_parser("correct", help="Log a recall correction")
    correct_parser.add_argument("entry_id", help="Indexed entry id being corrected")
    correct_parser.add_argument(
        "--verdict",
        required=True,
        choices=["correct", "partial", "incorrect"],
        help="Correction verdict",
    )
    correct_parser.add_argument("--note", required=True, help="Short rationale for correction")
    correct_parser.add_argument("--source-uri", default=None, help="Optional canonical source path")
    correct_parser.set_defaults(func=command_correct)

    promote_parser = subparsers.add_parser(
        "promote",
        help="Promote a code/docs finding into a wiki entry",
    )
    promote_parser.add_argument(
        "wiki_entry",
        help="Wiki entry id (e.g. caveats) or markdown path",
    )
    promote_parser.add_argument("--note", required=True, help="Finding to append")
    promote_parser.add_argument("--title", default=None, help="Optional heading for this finding")
    promote_parser.add_argument(
        "--source-uri",
        action="append",
        default=[],
        help="Source reference path (repeat for multiple refs)",
    )
    promote_parser.set_defaults(func=command_promote)

    memory_log_parser = subparsers.add_parser(
        "memory-log",
        help="Inspect interaction memory events",
    )
    memory_log_parser.add_argument("--tail", type=int, default=20, help="Number of events to show")
    memory_log_parser.add_argument(
        "--event-type",
        default=None,
        help="Optional event type filter (recall, correction, promotion, mempalace_sync, mempalace_import)",
    )
    memory_log_parser.set_defaults(func=command_memory_log)

    sync_parser = subparsers.add_parser(
        "sync-mempalace",
        help="Prepare push/pull adapter artifacts for mempalace sync",
    )
    sync_parser.add_argument(
        "--import-file",
        default=None,
        help="Optional JSON array file to import pulled memories",
    )
    sync_parser.add_argument(
        "--mark-synced",
        action="store_true",
        help="Advance sync cursor after preparing push payload",
    )
    sync_parser.set_defaults(func=command_sync_mempalace)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        _configure_runtime_paths(args)
    except RuntimeError as exc:
        print(str(exc))
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
