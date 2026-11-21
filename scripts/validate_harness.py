#!/usr/bin/env python3
"""Google Harness² surface validator, MD-to-HTML sync checker, and rule tree auditor."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

_SCRIPT_DIR = str(Path(__file__).resolve().parent)
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from build_rules_html import compile_rules  # noqa: E402
from resolve_rule import (  # noqa: E402
    extract_ai_block,
    load_model_catalog,
    load_skill_hierarchy,
    load_tree_from_html,
    load_tree_from_md,
)
from scan_skills_security import scan_skills_root  # noqa: E402

ALWAYS_ON_MAX = 8_000
NODE_AI_BYTES_WARN = 1_500
NODE_AI_BYTES_MAX = 2_800
RECOMMENDED_MAX_DEPTH = 3
EXPECTED_MIN_NODES = 28
EXPECTED_MIN_SKILLS = 9
VALID_TIERS = {"low", "mid", "high"}
VALID_EFFORTS = {"low", "medium", "high"}
VALID_PILLARS = {"prompt", "context", "harness", "loop", "graph"}
VALID_POLICIES = {
    "effort-first-with-verifier",
    "capacity-switch-sensitive",
    "grounding-over-thinking",
    "overthinking-guard-low",
}
REQUIRED_ACTIVE_GEMINI_MODELS = (
    "gemini-3.5-flash-lite",
    "gemini-decision-1",
    "gemini-4-hydrogen",
    "gemini-4-argon",
    "gemini-4-carbon",
)
DEPRECATED_MODEL_RE = re.compile(r"\bgemini-(?:2\.5|2\.0|1\.5)(?:-[a-z0-9._-]+)?\b", re.I)
JINJA_TRAPS = re.compile(r"\{\{|\{%|\{#")


def _parse_skill_frontmatter(skill_md: Path) -> tuple[str, str]:
    raw = skill_md.read_text(encoding="utf-8")[:1200]
    m_desc = re.search(r"^description:\s*(.+)$", raw, re.M)
    m_name = re.search(r"^name:\s*(\S+)\s*$", raw, re.M)
    return (m_name.group(1) if m_name else "", m_desc.group(1).strip() if m_desc else "")


def _check_md_html_parity(md_nodes: dict, html_nodes: dict) -> list[str]:
    """Ensure every MD source node matches its compiled HTML node across all routing fields."""
    errs: list[str] = []
    md_ids = set(md_nodes)
    html_ids = set(html_nodes)
    if missing_html := sorted(md_ids - html_ids):
        errs.append(f"MD nodes missing compiled HTML: {', '.join(missing_html)}")
    if extra_html := sorted(html_ids - md_ids):
        errs.append(f"HTML nodes missing MD source: {', '.join(extra_html)}")

    parity_fields = (
        "parent",
        "depth",
        "title",
        "tier",
        "effort",
        "skills",
        "pillars",
        "keywords",
        "escalate_when",
        "escalation_policy",
        "workload",
        "summary",
        "rules",
        "escalation_note",
    )
    for nid in sorted(md_ids & html_ids):
        m_node = md_nodes[nid]
        h_node = html_nodes[nid]
        for fld in parity_fields:
            if getattr(m_node, fld) != getattr(h_node, fld):
                errs.append(f"MD-vs-HTML parity mismatch on {nid!r}.{fld}")
        m_children = [(c.target, c.href, c.tier, c.when, c.label) for c in m_node.children]
        h_children = [(c.target, c.href, c.tier, c.when, c.label) for c in h_node.children]
        if m_children != h_children:
            errs.append(f"MD-vs-HTML parity mismatch on {nid!r}.children")
    return errs


def validate_harness(root: Path) -> tuple[list[str], list[str], dict]:
    """Validate Harness² invariants, MD single-source, HTML sync, and catalog rules. Returns (errors, warnings, summary)."""
    errors: list[str] = []
    warnings: list[str] = []

    agents_md = root / "AGENTS.md"
    if not agents_md.is_file():
        errors.append("missing AGENTS.md")
        return errors, warnings, {}
    agents_text = agents_md.read_text(encoding="utf-8")
    if not agents_text.strip():
        errors.append("AGENTS.md must not be empty")
    if len(agents_text) > ALWAYS_ON_MAX:
        errors.append(f"AGENTS.md is {len(agents_text)} chars (> {ALWAYS_ON_MAX} cap)")
    if m := JINJA_TRAPS.search(agents_text):
        errors.append(f"AGENTS.md contains Jinja brace trap {m.group(0)!r}")

    # Validate .agents/skills/*/SKILL.md + trigger lines in AGENTS.md
    skills_dir = root / ".agents" / "skills"
    skill_meta: dict[str, str] = {}
    if skills_dir.is_dir():
        for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
            sdir = skill_md.parent.name
            fm_name, fm_desc = _parse_skill_frontmatter(skill_md)
            if not fm_desc:
                errors.append(f"{skill_md.relative_to(root)} missing YAML description:")
            if fm_name and fm_name != sdir:
                errors.append(f"{skill_md.relative_to(root)} name:{fm_name!r} != dir {sdir!r}")
            if sdir not in agents_text:
                errors.append(f"skill {sdir!r} is missing a verbatim trigger line in AGENTS.md")
            skill_meta[sdir] = fm_desc
    if len(skill_meta) < EXPECTED_MIN_SKILLS:
        errors.append(f"expected at least {EXPECTED_MIN_SKILLS} skills, found {len(skill_meta)}")

    # Compile-check Python helpers in scripts/
    for py_file in sorted((root / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{py_file.relative_to(root)} compile error: {exc.msg}")

    # Security scan all skills & verify hierarchy registration
    sec_report = scan_skills_root(skills_dir)
    for f in sec_report["findings"]:
        if f["severity"] in {"CRITICAL", "HIGH"}:
            errors.append(
                f"security gate blocked {f['skill']}/{f['file']}:{f['line']} [{f['rule_id']}] {f['reason']}"
            )
        else:
            warnings.append(
                f"security warning {f['skill']}/{f['file']}:{f['line']} [{f['rule_id']}] {f['reason']}"
            )

    rules_root = root / "rules"
    hierarchy = load_skill_hierarchy(rules_root)
    h_skills = hierarchy.get("skills", {})
    for sk in skill_meta:
        if sk not in h_skills:
            errors.append(f"skill {sk!r} missing from rules/skill-hierarchy.json (flat/unranked skill prohibited)")
    for sk in sorted(set(h_skills) - set(skill_meta)):
        errors.append(f"rules/skill-hierarchy.json references non-existent skill {sk!r}")

    # Validate rules/model-catalog.json (v3.0 active Gemini models, zero deprecated models)
    cat_path = rules_root / "model-catalog.json"
    catalog = load_model_catalog(rules_root)
    if not cat_path.is_file():
        errors.append("missing rules/model-catalog.json")
    else:
        cat_raw = cat_path.read_text(encoding="utf-8")
        if m_dep := DEPRECATED_MODEL_RE.search(cat_raw):
            errors.append(f"rules/model-catalog.json contains deprecated model {m_dep.group(0)!r}")
        lineage_models = catalog.get("gemini_lineage_specs", {}).get("models", {})
        for req_model in REQUIRED_ACTIVE_GEMINI_MODELS:
            if req_model not in lineage_models:
                errors.append(f"rules/model-catalog.json missing required active model spec {req_model!r}")

    # Validate Markdown single-source-of-truth (rules/src/**/*.md) + build_rules_html.py --check sync
    src_root = rules_root / "src"
    md_nodes: dict = {}
    md_html_in_sync = False
    if not (src_root / "router.md").is_file():
        errors.append("missing Markdown single source of truth: rules/src/router.md")
    else:
        md_nodes = load_tree_from_md(rules_root)
        if "root" not in md_nodes:
            errors.append("rules/src/router.md must define rule_id: root")
        if "meta.anti-hallucination" not in md_nodes:
            errors.append("missing required branch rule_id='meta.anti-hallucination' in rules/src/")
        if len(md_nodes) < EXPECTED_MIN_NODES:
            errors.append(f"expected at least {EXPECTED_MIN_NODES} MD rule nodes, found {len(md_nodes)}")

        for nid, mnode in md_nodes.items():
            md_path = rules_root / mnode.rel_path
            md_raw = md_path.read_text(encoding="utf-8")
            if m := JINJA_TRAPS.search(md_raw):
                errors.append(f"{mnode.rel_path} contains Jinja brace trap {m.group(0)!r}")
            if m_dep := DEPRECATED_MODEL_RE.search(md_raw):
                errors.append(f"{mnode.rel_path} references deprecated model {m_dep.group(0)!r}")
            if mnode.tier not in VALID_TIERS:
                errors.append(f"{mnode.rel_path} invalid tier={mnode.tier!r}")
            if mnode.effort not in VALID_EFFORTS:
                errors.append(f"{mnode.rel_path} invalid effort={mnode.effort!r}")
            if mnode.parent and mnode.parent not in md_nodes:
                errors.append(f"{mnode.rel_path} missing parent {mnode.parent!r}")
            for sk in mnode.skills:
                if sk not in skill_meta:
                    errors.append(f"{mnode.rel_path} references unknown skill {sk!r}")
            for pl in mnode.pillars:
                if pl not in VALID_PILLARS:
                    errors.append(f"{mnode.rel_path} invalid pillar {pl!r}")
            if mnode.escalation_policy and mnode.escalation_policy not in VALID_POLICIES:
                errors.append(f"{mnode.rel_path} invalid escalation_policy {mnode.escalation_policy!r}")
            for link in mnode.children:
                if link.target not in md_nodes:
                    errors.append(f"{mnode.rel_path} broken child target {link.target!r}")

        sync_ok, sync_issues, _ = compile_rules(root, check=True)
        md_html_in_sync = sync_ok
        for issue in sync_issues:
            errors.append(f"MD-to-HTML sync check failed: {issue}")

    # Validate compiled HTML rule tree
    html_nodes = load_tree_from_html(rules_root)
    if "root" not in html_nodes:
        errors.append("rules/router.html must define data-rule-id='root'")
    if len(html_nodes) < EXPECTED_MIN_NODES:
        errors.append(f"expected at least {EXPECTED_MIN_NODES} HTML rule nodes, found {len(html_nodes)}")

    for nid, node in html_nodes.items():
        html_path = rules_root / node.rel_path
        raw = html_path.read_text(encoding="utf-8")
        if "<!-- AI-RULE-START -->" not in raw or "<!-- AI-RULE-END -->" not in raw:
            errors.append(f"{node.rel_path} missing AI-RULE-START/END markers")
        ai_block = extract_ai_block(raw)
        if "<style" in ai_block.lower() or "<script" in ai_block.lower():
            errors.append(f"{node.rel_path} embeds inline <style> or <script> inside AI-RULE block")
        if node.tier not in VALID_TIERS:
            errors.append(f"{node.rel_path} invalid data-tier={node.tier!r}")
        if node.effort not in VALID_EFFORTS:
            errors.append(f"{node.rel_path} invalid data-effort={node.effort!r}")
        if node.parent and node.parent not in html_nodes:
            errors.append(f"{node.rel_path} missing parent {node.parent!r}")
        if node.ai_bytes > NODE_AI_BYTES_MAX:
            errors.append(f"{node.rel_path} AI block is {node.ai_bytes}B (> {NODE_AI_BYTES_MAX}B cap)")
        elif node.ai_bytes > NODE_AI_BYTES_WARN:
            warnings.append(f"{node.rel_path} AI block is {node.ai_bytes}B (above {NODE_AI_BYTES_WARN}B target)")
        if node.depth > RECOMMENDED_MAX_DEPTH:
            warnings.append(
                f"{node.rel_path} depth={node.depth} exceeds recommended depth {RECOMMENDED_MAX_DEPTH} (arXiv:2607.17598)"
            )

        for sk in node.skills:
            if sk not in skill_meta:
                errors.append(f"{node.rel_path} references unknown skill {sk!r}")
        for pl in node.pillars:
            if pl not in VALID_PILLARS:
                errors.append(f"{node.rel_path} invalid data-pillars value {pl!r}")
        if node.escalation_policy and node.escalation_policy not in VALID_POLICIES:
            errors.append(f"{node.rel_path} invalid data-escalation-policy {node.escalation_policy!r}")

        for link in node.children:
            if link.target not in html_nodes:
                errors.append(f"{node.rel_path} broken child target {link.target!r}")
                continue
            resolved_href = (html_path.parent / link.href).resolve()
            expected_file = (rules_root / html_nodes[link.target].rel_path).resolve()
            if resolved_href != expected_file:
                errors.append(
                    f"{node.rel_path} href {link.href!r} resolves to {resolved_href.name}, "
                    f"expected {expected_file.name}"
                )

    if md_nodes and html_nodes:
        errors.extend(_check_md_html_parity(md_nodes, html_nodes))

    summary = {
        "always_on_chars": len(agents_text),
        "always_on_cap": ALWAYS_ON_MAX,
        "skills": len(skill_meta),
        "md_nodes": len(md_nodes),
        "html_nodes": len(html_nodes),
        "md_html_in_sync": md_html_in_sync,
        "total_md_bytes": sum(n.file_bytes for n in md_nodes.values()),
        "total_ai_bytes": sum(n.ai_bytes for n in html_nodes.values()),
        "total_file_bytes": sum(n.file_bytes for n in html_nodes.values()),
        "model_catalog_version": catalog.get("version", ""),
    }
    # Legacy fallback only when MD compiler sources are absent; otherwise scripts/build_rules_html.py owns tree-data.js.
    if not errors and not (src_root / "router.md").is_file():
        sync_tree_data_js(rules_root, html_nodes, skill_meta, hierarchy)
    return errors, warnings, summary


def sync_tree_data_js(rules_root: Path, nodes: dict, skill_meta: dict[str, str], hierarchy: dict) -> None:
    """Legacy fallback emitter for rules/assets/tree-data.js when MD sources are absent."""
    catalog = load_model_catalog(rules_root)
    payload = {
        "generated_by": "scripts/validate_harness.py",
        "skills": skill_meta,
        "skill_hierarchy": hierarchy,
        "catalog": catalog,
        "nodes": {
            nid: {
                "rule_id": n.rule_id,
                "parent": n.parent,
                "depth": n.depth,
                "title": n.title,
                "tier": n.tier,
                "effort": n.effort,
                "skills": n.skills,
                "pillars": n.pillars,
                "keywords": n.keywords,
                "escalate_when": n.escalate_when,
                "escalation_policy": n.escalation_policy,
                "workload": n.workload,
                "rel_path": n.rel_path,
                "summary": n.summary,
                "rules": n.rules,
                "escalation_note": n.escalation_note,
                "ai_bytes": n.ai_bytes,
                "file_bytes": n.file_bytes,
                "children": [
                    {
                        "href": c.href,
                        "target": c.target,
                        "tier": c.tier,
                        "when": c.when,
                        "label": c.label,
                    }
                    for c in n.children
                ],
            }
            for nid, n in nodes.items()
        },
    }
    out = rules_root / "assets" / "tree-data.js"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "// Auto-generated by scripts/validate_harness.py — do not hand-edit.\n"
        f"window.RULE_TREE_DATA = {json.dumps(payload, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors, warnings, summary = validate_harness(root)
    for w in warnings:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[ERROR] {e}", file=sys.stderr)
    print(f"[SUMMARY] {json.dumps(summary, ensure_ascii=False)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
